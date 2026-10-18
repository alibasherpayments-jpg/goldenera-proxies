"""
Catalog & Purchase Wizard handler:
Category -> Server -> Mode -> Credentials -> Confirmation -> Async Fulfillment
"""
import asyncio
import logging
from datetime import datetime, timezone
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.core.helpers import get_markup_percent, apply_markup
from app.models.user import User, Wallet
from app.models.proxy import Proxy
from app.models.order import Order
from app.bot.i18n import t
from app.services.magnum_client import magnum, MagnumAPIError

logger = logging.getLogger(__name__)
router = Router(name="catalog")


class BuyWizard(StatesGroup):
    waiting_username = State()
    waiting_password = State()
    waiting_allowed_ip = State()


# ─── Step 1: Choose Category ──────────────────────────────────────────────────

@router.callback_query(F.data == "menu:buy")
async def choose_category(callback: CallbackQuery):
    async with AsyncSessionLocal() as session:
        user_res = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = user_res.scalar_one_or_none()
        lang = user.language if user else "ar"

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t("catalog_prime", lang), callback_data="buy:cat:prime")],
            [InlineKeyboardButton(text=t("catalog_hyper", lang), callback_data="buy:cat:hyper")],
            [InlineKeyboardButton(text=t("catalog_nexus", lang), callback_data="buy:cat:nexus")],
            [InlineKeyboardButton(text=t("catalog_titan", lang), callback_data="buy:cat:titan")],
            [InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:main")],
        ]
    )

    text = t("catalog_choose_category", lang)

    try:
        await callback.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    except Exception:
        await callback.message.answer(text, reply_markup=kb, parse_mode="Markdown")
    await callback.answer()


# ─── Step 2: Choose Server / Location ─────────────────────────────────────────

@router.callback_query(F.data.startswith("buy:cat:"))
async def choose_server(callback: CallbackQuery, state: FSMContext):
    category = callback.data.split(":")[2]
    await state.update_data(category=category)

    async with AsyncSessionLocal() as session:
        user_res = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = user_res.scalar_one_or_none()
        lang = user.language if user else "ar"

    wait_msg = await callback.message.answer(t("loading", lang))
    await callback.answer()

    try:
        catalog_servers = await magnum.get_servers()
        all_servers = catalog_servers.get("servers", [])
        nexus_servers = catalog_servers.get("nexus_store_servers", [])

        if category == "nexus":
            servers_list = nexus_servers or [s for s in all_servers if s.get("category", "").lower() == "nexus"]
        elif category == "titan":
            servers_list = [s for s in all_servers if s.get("category", "").lower() == "titan"]
        elif category == "hyper":
            servers_list = [s for s in all_servers if s.get("category", "").lower() == "hyper"]
        elif category == "prime":
            servers_list = [s for s in all_servers if s.get("category", "").lower() == "prime"]
        else:
            servers_list = [s for s in all_servers if s.get("category", "").lower() == category.lower()]

        if not servers_list:
            servers_list = all_servers[:10]

        rows = []
        for s in servers_list[:10]:
            srv_id = s.get("server_id")
            c_name = s.get("country_name") or s.get("country", "")
            city = s.get("city") or s.get("state", "")
            avail = s.get("availability", "available")
            is_full = avail == "full"

            flag = "🌐"
            c_code = s.get("country", "")
            if len(c_code) == 2:
                flag = "".join(chr(ord(c) + 127397) for c in c_code.upper())

            label = f"{flag} {c_name} ({city})"
            if is_full:
                label += f" — {t('catalog_server_full', lang)}"

            cb_data = f"buy:full:{srv_id}" if is_full else f"buy:srv:{srv_id}"
            rows.append([InlineKeyboardButton(text=label, callback_data=cb_data)])

        rows.append([InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:buy")])
        kb = InlineKeyboardMarkup(inline_keyboard=rows)

        cat_labels = {
            "prime": "⚡ PRIME 5G",
            "hyper": "🚀 HYPER 5G",
            "nexus": "🌐 NEXUS",
            "titan": "🛡️ TITAN",
        }
        cat_name = cat_labels.get(category, category.upper())
        text = f"📍 *سيرفرات {cat_name} المتاحة:*" if lang == "ar" else f"📍 *Available {cat_name} Servers:*"
        await wait_msg.edit_text(text, reply_markup=kb, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Catalog servers error: {e}")
        err_msg = (
            "⚠️ لا يمكن جلب السيرفرات حالياً، يرجى المحاولة لاحقاً." if lang == "ar"
            else "⚠️ Could not fetch servers at the moment, please try again."
        )
        kb_back = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:buy")]])
        await wait_msg.edit_text(err_msg, reply_markup=kb_back, parse_mode="Markdown")


@router.callback_query(F.data.startswith("buy:full:"))
async def server_is_full_alert(callback: CallbackQuery):
    async with AsyncSessionLocal() as session:
        user_res = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = user_res.scalar_one_or_none()
        lang = user.language if user else "ar"

    msg = "⛔ هذا السيرفر ممتلئ حالياً. يرجى اختيار سيرفر آخر متاح." if lang == "ar" else "⛔ This server is currently full. Please choose another."
    await callback.answer(msg, show_alert=True)


# ─── Step 3: Choose Mode (Rotate / Inject) ────────────────────────────────────

@router.callback_query(F.data.startswith("buy:srv:"))
async def choose_mode(callback: CallbackQuery, state: FSMContext):
    server_id = callback.data.split(":")[2]
    await state.update_data(server_id=server_id)

    async with AsyncSessionLocal() as session:
        user_res = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = user_res.scalar_one_or_none()
        lang = user.language if user else "ar"

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t("catalog_mode_rotate", lang), callback_data="buy:mode:rotate"
                )
            ],
            [
                InlineKeyboardButton(
                    text=t("catalog_mode_inject", lang), callback_data="buy:mode:inject"
                )
            ],
            [InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:buy")],
        ]
    )

    text = "⚙️ *اختر طريقة الاتصال بالبروكسي:*" if lang == "ar" else "⚙️ *Select proxy connection mode:*"

    try:
        await callback.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    except Exception:
        await callback.message.answer(text, reply_markup=kb, parse_mode="Markdown")
    await callback.answer()


# ─── Step 4: Collect Credentials ─────────────────────────────────────────────

@router.callback_query(F.data.startswith("buy:mode:"))
async def ask_credentials(callback: CallbackQuery, state: FSMContext):
    mode = callback.data.split(":")[2]
    await state.update_data(mode=mode)

    async with AsyncSessionLocal() as session:
        user_res = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = user_res.scalar_one_or_none()
        lang = user.language if user else "ar"

    if mode == "rotate":
        await state.set_state(BuyWizard.waiting_username)
        text = t("catalog_enter_username", lang)
    else:
        await state.set_state(BuyWizard.waiting_allowed_ip)
        text = t("catalog_enter_allowed_ip", lang)

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t("btn_cancel", lang), callback_data="menu:main")]
        ]
    )
    await callback.message.answer(text, reply_markup=kb, parse_mode="Markdown")
    await callback.answer()


@router.message(BuyWizard.waiting_allowed_ip)
async def process_allowed_ip(message: Message, state: FSMContext):
    allowed_ip = message.text.strip()
    await state.update_data(allowed_ip=allowed_ip)

    # Proceed to confirmation
    await show_order_summary(message, state)


@router.message(BuyWizard.waiting_username)
async def process_username(message: Message, state: FSMContext):
    username = message.text.strip().replace(" ", "")
    await state.update_data(username=username)

    async with AsyncSessionLocal() as session:
        user_res = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = user_res.scalar_one_or_none()
        lang = user.language if user else "ar"

    await state.set_state(BuyWizard.waiting_password)
    await message.answer(t("catalog_enter_password", lang), parse_mode="Markdown")


@router.message(BuyWizard.waiting_password)
async def process_password(message: Message, state: FSMContext):
    password = message.text.strip().replace(" ", "")
    if len(password) < 6:
        await message.answer("⚠️ Password must be at least 6 characters.")
        return

    await state.update_data(password=password)

    # Proceed to confirmation
    await show_order_summary(message, state)


# ─── Step 5: Order Summary & Confirmation ────────────────────────────────────

async def show_order_summary(message: Message, state: FSMContext):
    data = await state.get_data()
    category = data.get("category", "prime")
    mode = data.get("mode", "rotate")
    server_id = data.get("server_id", "")

    # Product code
    product_code = f"{category}.{mode}.1d"

    async with AsyncSessionLocal() as session:
        user_res = await session.execute(
            select(User, Wallet)
            .join(Wallet, Wallet.user_id == User.id)
            .where(User.telegram_id == message.from_user.id)
        )
        row = user_res.first()
        if not row:
            return

        user, wallet = row
        lang = user.language or "ar"

        markup_percent = await get_markup_percent(session)

    # Base price defaults if catalog fails
    base_price = 0.70
    try:
        prods = await magnum.get_products()
        for p in prods.get("products", []):
            if p.get("code") == product_code or p.get("category") == category:
                base_price = float(p.get("price", 0.70))
                break
    except Exception:
        pass

    retail_price = apply_markup(base_price, markup_percent)
    await state.update_data(product_code=product_code, retail_price=retail_price)

    text = t(
        "catalog_order_summary",
        lang,
        category=category.upper(),
        mode=mode,
        location=server_id or "Auto",
        duration="24 Hours (1 Day)",
        price=f"{retail_price:.2f}",
        balance=f"{wallet.balance:.2f}",
    )

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t("btn_confirm", lang), callback_data="buy:confirm"
                )
            ],
            [
                InlineKeyboardButton(
                    text=t("btn_cancel", lang), callback_data="menu:main"
                )
            ],
        ]
    )

    await message.answer(text, reply_markup=kb, parse_mode="Markdown")


# ─── Step 6: Confirm & Async Fulfillment ──────────────────────────────────────

@router.callback_query(F.data == "buy:confirm")
async def execute_purchase(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await state.clear()

    product_code = data.get("product_code", "prime.rotate.1d")
    retail_price = float(data.get("retail_price", 1.0))
    category = data.get("category", "prime")
    mode = data.get("mode", "rotate")
    server_id = data.get("server_id")
    username = data.get("username", "client01")
    password = data.get("password", "Pass1234")
    allowed_ip = data.get("allowed_ip")

    async with AsyncSessionLocal() as session:
        user_res = await session.execute(
            select(User, Wallet)
            .join(Wallet, Wallet.user_id == User.id)
            .where(User.telegram_id == callback.from_user.id)
            .with_for_update()
        )
        row = user_res.first()
        if not row:
            await callback.answer(t("error_generic", "ar"), show_alert=True)
            return

        user, wallet = row
        lang = user.language or "ar"

        if wallet.balance < retail_price:
            await callback.answer(
                t("catalog_insufficient_balance", lang, needed=f"{retail_price:.2f}", balance=f"{wallet.balance:.2f}"),
                show_alert=True,
            )
            return

        # Deduct balance
        wallet.balance -= retail_price
        wallet.total_spent += retail_price

        order = Order(
            user_id=user.id,
            request_type="purchase",
            product_code=product_code,
            status="queued",
            amount_deducted=retail_price,
        )
        session.add(order)
        await session.commit()
        order_id = order.id
        user_id = user.id
        tg_id = user.telegram_id

    await callback.message.answer(t("catalog_order_placed", lang), parse_mode="Markdown")
    await callback.answer()

    # Launch asynchronous fulfillment task
    asyncio.create_task(
        _fulfill_order(
            bot=bot,
            order_id=order_id,
            user_id=user_id,
            tg_id=tg_id,
            lang=lang,
            category=category,
            mode=mode,
            product_code=product_code,
            server_id=server_id,
            username=username,
            password=password,
            allowed_ip=allowed_ip,
            retail_price=retail_price,
        )
    )


async def _fulfill_order(
    bot: Bot,
    order_id: int,
    user_id: int,
    tg_id: int,
    lang: str,
    category: str,
    mode: str,
    product_code: str,
    server_id: str,
    username: str,
    password: str,
    allowed_ip: str,
    retail_price: float,
):
    """Background task to poll Magnum API until proxy is ready and send it to the user."""
    try:
        # Build payload
        payload = {
            "request_type": "purchase",
            "product_code": product_code,
        }
        if server_id:
            payload["server_id"] = server_id

        if mode == "rotate":
            payload["username"] = username
            payload["password"] = password
        else:
            if allowed_ip:
                payload["allowed_ip"] = allowed_ip

        res = await magnum.create_order(payload)
        req_id = res.get("request_id")

        if not req_id:
            raise Exception("No request_id returned by Magnum API")

        # Update order in DB
        async with AsyncSessionLocal() as session:
            ord_row = await session.get(Order, order_id)
            if ord_row:
                ord_row.magnum_request_id = req_id
                ord_row.status = "dispatching"
                await session.commit()

        # Poll until complete
        proxy_data = await magnum.wait_for_order(req_id, timeout=120)

        # Parse proxy details
        exp_date = None
        exp_str = proxy_data.get("expiry_date")
        if exp_str:
            try:
                exp_date = datetime.fromisoformat(exp_str.replace("Z", "+00:00"))
            except Exception:
                pass

        async with AsyncSessionLocal() as session:
            new_proxy = Proxy(
                user_id=user_id,
                request_id=req_id,
                category=category,
                mode=mode,
                product_code=product_code,
                server_id=server_id,
                country=proxy_data.get("country"),
                country_name=proxy_data.get("country_name"),
                state=proxy_data.get("state"),
                city=proxy_data.get("city"),
                provider=proxy_data.get("provider"),
                rotation_label=proxy_data.get("rotation_label"),
                protocol=proxy_data.get("protocol", "SOCKS5"),
                host=proxy_data.get("host"),
                http_port=proxy_data.get("http_port"),
                socks5_port=proxy_data.get("socks5_port"),
                port=proxy_data.get("port"),
                username=proxy_data.get("username", username),
                password=proxy_data.get("password", password),
                proxy_url=proxy_data.get("url"),
                price_paid=retail_price,
                is_active=True,
                expiry_date=exp_date,
            )
            session.add(new_proxy)

            ord_row = await session.get(Order, order_id)
            if ord_row:
                ord_row.status = "succeeded"
                ord_row.related_proxy_id = new_proxy.id

            await session.commit()

            flag = new_proxy.flag
            loc = new_proxy.display_location
            exp_display = exp_date.strftime("%Y-%m-%d %H:%M UTC") if exp_date else "24 Hours"

        # Send Proxy Card via Telegram
        text = (
            f"🎉 {t('proxy_card_title', lang)}\n\n"
            f"{t('proxy_card_body', lang, category=category.upper(), mode=mode, flag=flag, location=loc, rotation_label=proxy_data.get('rotation_label', 'Rotation 30'), host=proxy_data.get('host', 'N/A'), http_port=proxy_data.get('http_port', '-'), socks5_port=proxy_data.get('socks5_port', '-'), username=proxy_data.get('username', username), password=proxy_data.get('password', password), expiry=exp_display, url=proxy_data.get('url', 'N/A'))}"
        )

        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=t("menu_my_proxies", lang), callback_data="menu:my_proxies"
                    )
                ]
            ]
        )
        await bot.send_message(chat_id=tg_id, text=text, reply_markup=kb, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Order fulfillment failed for order {order_id}: {e}")

        # Refund user balance
        async with AsyncSessionLocal() as session:
            user_res = await session.execute(select(Wallet).where(Wallet.user_id == user_id))
            w = user_res.scalar_one_or_none()
            if w:
                w.balance += retail_price
                w.total_spent -= retail_price

            ord_row = await session.get(Order, order_id)
            if ord_row:
                ord_row.status = "failed_refunded"
                ord_row.failure_reason = str(e)[:128]

            await session.commit()

        fail_msg = (
            f"❌ فشل إنشاء البروكسي: {e}\n\nتم استرجاع الرصيد بالكامل إلى محفظتك."
            if lang == "ar"
            else f"❌ Proxy creation failed: {e}\n\nFull amount has been refunded to your wallet."
        )
        await bot.send_message(chat_id=tg_id, text=fail_msg)
