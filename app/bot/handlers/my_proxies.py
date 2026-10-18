"""
My Proxies handler — view active proxies, proxy card details, and management actions:
- Instant IP Rotation (NEXUS)
- Change Password (PRIME, HYPER, NEXUS)
- Convert between Rotate & Inject
- Renew proxy subscription
"""
import logging
from datetime import datetime, timezone
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.user import User, Wallet
from app.models.proxy import Proxy
from app.models.order import Order
from app.bot.i18n import t
from app.bot.keyboards.main import proxy_card_kb
from app.services.magnum_client import magnum, MagnumAPIError

logger = logging.getLogger(__name__)
router = Router(name="my_proxies")


class ChangePasswordState(StatesGroup):
    waiting_new_password = State()


class ConvertProxyState(StatesGroup):
    waiting_allowed_ip = State()
    waiting_rotate_password = State()


@router.callback_query(F.data == "menu:my_proxies")
async def list_my_proxies(callback: CallbackQuery):
    async with AsyncSessionLocal() as session:
        user_res = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = user_res.scalar_one_or_none()
        if not user:
            await callback.answer(t("error_generic", "ar"), show_alert=True)
            return

        lang = user.language or "ar"
        now = datetime.now(timezone.utc)

        proxies_res = await session.execute(
            select(Proxy)
            .where(Proxy.user_id == user.id, Proxy.is_active == True)
            .order_by(Proxy.created_at.desc())
        )
        proxies = proxies_res.scalars().all()

        if not proxies:
            text = f"{t('my_proxies_title', lang)}\n\n{t('my_proxies_empty', lang)}"
            kb = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=t("menu_buy", lang), callback_data="menu:buy")],
                    [InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:main")],
                ]
            )
            try:
                await callback.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
            except Exception:
                await callback.message.answer(text, reply_markup=kb, parse_mode="Markdown")
            await callback.answer()
            return

        rows = []
        for p in proxies:
            exp_str = ""
            if p.expiry_date:
                remaining = p.expiry_date - now
                hours = int(remaining.total_seconds() // 3600)
                if hours > 24:
                    exp_str = f"({hours // 24}d)"
                elif hours > 0:
                    exp_str = f"({hours}h)"
                else:
                    exp_str = "(Expired)"

            btn_label = f"{p.flag} {p.display_location} • {p.category.upper()} {exp_str}"
            rows.append(
                [InlineKeyboardButton(text=btn_label, callback_data=f"proxy:view:{p.request_id}")]
            )

        rows.append([InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:main")])
        kb = InlineKeyboardMarkup(inline_keyboard=rows)

        text = f"{t('my_proxies_title', lang)}\n\n" + (
            "اختر بروكساً لعرض بيانات الاتصال وإدارته:" if lang == "ar" else "Select a proxy to manage and view details:"
        )

        try:
            await callback.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
        except Exception:
            await callback.message.answer(text, reply_markup=kb, parse_mode="Markdown")

        await callback.answer()


@router.callback_query(F.data.startswith("proxy:view:"))
async def view_proxy_card(callback: CallbackQuery):
    request_id = callback.data.split(":")[2]

    async with AsyncSessionLocal() as session:
        user_res = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = user_res.scalar_one_or_none()
        if not user:
            await callback.answer(t("error_generic", "ar"), show_alert=True)
            return

        lang = user.language or "ar"

        proxy_res = await session.execute(
            select(Proxy).where(Proxy.request_id == request_id, Proxy.user_id == user.id)
        )
        proxy = proxy_res.scalar_one_or_none()
        if not proxy:
            await callback.answer(t("error_generic", lang), show_alert=True)
            return

        expiry_str = proxy.expiry_date.strftime("%Y-%m-%d %H:%M UTC") if proxy.expiry_date else "N/A"
        proxy_url = proxy.proxy_url or (
            f"socks5://{proxy.username}:{proxy.password}@{proxy.host}:{proxy.socks5_port}"
            if proxy.host and proxy.username
            else f"http://{proxy.host}:{proxy.http_port}"
            if proxy.host
            else "N/A"
        )

        text = (
            f"{t('proxy_card_title', lang)}\n\n"
            f"{t('proxy_card_body', lang, category=proxy.category.upper(), mode=proxy.mode or 'rotate', flag=proxy.flag, location=proxy.display_location, rotation_label=proxy.rotation_label or 'Rotation Auto', host=proxy.host or 'Generating...', http_port=proxy.http_port or '-', socks5_port=proxy.socks5_port or '-', username=proxy.username or '-', password=proxy.password or '-', expiry=expiry_str, url=proxy_url)}"
        )

        kb = proxy_card_kb(lang, proxy.request_id, proxy.category)

        try:
            await callback.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
        except Exception:
            await callback.message.answer(text, reply_markup=kb, parse_mode="Markdown")

        await callback.answer()


@router.callback_query(F.data.startswith("proxy:rotate_ip:"))
async def rotate_nexus_ip(callback: CallbackQuery):
    request_id = callback.data.split(":")[2]

    async with AsyncSessionLocal() as session:
        user_res = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = user_res.scalar_one_or_none()
        lang = user.language if user else "ar"

    await callback.answer(t("proxy_action_processing", lang))

    try:
        res = await magnum.nexus_action(request_id, "rotate_ip")
        management_id = res.get("management_id")
        if management_id:
            await magnum.wait_for_management(management_id, timeout=30)

        await callback.message.answer(
            f"🔄 {t('proxy_action_success', lang)}\n\n"
            + ("تم تدوير عنوان الـ IP بنجاح!" if lang == "ar" else "IP address rotated successfully!"),
            parse_mode="Markdown",
        )
    except MagnumAPIError as e:
        error_msg = f"⚠️ {e.error}"
        if "cooldown" in str(e).lower() or e.status_code == 409:
            error_msg = (
                "⏳ فترة التهدئة (Cooldown) نشطة. يرجى الانتظار قليلاً قبل التدوير مجدداً."
                if lang == "ar"
                else "⏳ Cooldown active. Please wait before rotating again."
            )
        await callback.message.answer(error_msg)
    except Exception as e:
        logger.error(f"Rotate IP error: {e}")
        await callback.message.answer(t("error_generic", lang))


@router.callback_query(F.data.startswith("proxy:change_pass:"))
async def change_proxy_password_prompt(callback: CallbackQuery, state: FSMContext):
    request_id = callback.data.split(":")[2]
    await state.set_state(ChangePasswordState.waiting_new_password)
    await state.update_data(request_id=request_id)

    async with AsyncSessionLocal() as session:
        user_res = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = user_res.scalar_one_or_none()
        lang = user.language if user else "ar"

    text = t("proxy_enter_new_password", lang)
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t("btn_cancel", lang), callback_data=f"proxy:view:{request_id}")]
        ]
    )
    await callback.message.answer(text, reply_markup=kb, parse_mode="Markdown")
    await callback.answer()


@router.message(ChangePasswordState.waiting_new_password)
async def process_new_password(message: Message, state: FSMContext):
    data = await state.get_data()
    request_id = data.get("request_id")
    new_password = message.text.strip()

    if len(new_password) < 6:
        await message.answer("⚠️ Password must be at least 6 characters.")
        return

    await state.clear()

    async with AsyncSessionLocal() as session:
        user_res = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = user_res.scalar_one_or_none()
        lang = user.language if user else "ar"

        proxy_res = await session.execute(
            select(Proxy).where(Proxy.request_id == request_id, Proxy.user_id == user.id)
        )
        proxy = proxy_res.scalar_one_or_none()
        if not proxy:
            await message.answer(t("error_generic", lang))
            return

        cat = proxy.category.lower()

    wait_msg = await message.answer(t("proxy_action_processing", lang))

    try:
        if cat == "nexus":
            res = await magnum.nexus_action(request_id, "change_password", password=new_password)
            m_id = res.get("management_id")
            if m_id:
                await magnum.wait_for_management(m_id, timeout=30)
        else:
            res = await magnum.proxy_action(request_id, "change_password", password=new_password)
            m_id = res.get("management_id")
            if m_id:
                await magnum.wait_for_management(m_id, timeout=30)

        # Update proxy in DB
        async with AsyncSessionLocal() as session:
            p = await session.get(Proxy, proxy.id)
            if p:
                p.password = new_password
                await session.commit()

        await wait_msg.edit_text(
            f"✅ {t('proxy_action_success', lang)}\n\n"
            + (f"كلمة المرور الجديدة: `{new_password}`" if lang == "ar" else f"New password: `{new_password}`"),
            parse_mode="Markdown",
        )
    except Exception as e:
        logger.error(f"Change password error: {e}")
        await wait_msg.edit_text(f"⚠️ {e}")


@router.callback_query(F.data.startswith("proxy:renew:"))
async def renew_proxy(callback: CallbackQuery):
    request_id = callback.data.split(":")[2]

    async with AsyncSessionLocal() as session:
        user_res = await session.execute(
            select(User, Wallet)
            .join(Wallet, Wallet.user_id == User.id)
            .where(User.telegram_id == callback.from_user.id)
        )
        row = user_res.first()
        if not row:
            await callback.answer(t("error_generic", "ar"), show_alert=True)
            return

        user, wallet = row
        lang = user.language or "ar"

        proxy_res = await session.execute(
            select(Proxy).where(Proxy.request_id == request_id, Proxy.user_id == user.id)
        )
        proxy = proxy_res.scalar_one_or_none()
        if not proxy:
            await callback.answer(t("error_generic", lang), show_alert=True)
            return

        renew_price = proxy.price_paid or 1.0

        if wallet.balance < renew_price:
            await callback.answer(
                t("catalog_insufficient_balance", lang, needed=f"{renew_price:.2f}", balance=f"{wallet.balance:.2f}"),
                show_alert=True,
            )
            return

        # Deduct balance
        wallet.balance -= renew_price
        wallet.total_spent += renew_price

        order = Order(
            user_id=user.id,
            request_type="renew",
            product_code=proxy.product_code,
            status="queued",
            amount_deducted=renew_price,
            related_proxy_id=proxy.id,
        )
        session.add(order)
        await session.commit()

    wait_msg = await callback.message.answer(
        "⏳ " + ("جاري تجديد الاشتراك..." if lang == "ar" else "Renewing proxy subscription...")
    )
    await callback.answer()

    try:
        res = await magnum.create_order({
            "request_type": "renew",
            "product_code": proxy.product_code,
            "target_request_id": request_id,
        })
        m_req_id = res.get("request_id")
        if m_req_id:
            result = await magnum.wait_for_order(m_req_id, timeout=90)
            new_expiry_str = result.get("expiry_date")

            async with AsyncSessionLocal() as session:
                p = await session.get(Proxy, proxy.id)
                if p and new_expiry_str:
                    try:
                        p.expiry_date = datetime.fromisoformat(new_expiry_str.replace("Z", "+00:00"))
                    except Exception:
                        pass
                    p.is_active = True
                    p.notified_24h = False
                    p.notified_2h = False
                    await session.commit()

            await wait_msg.edit_text(
                "🎉 " + ("تم تجديد اشتراك البروكسي بنجاح!" if lang == "ar" else "Proxy renewed successfully!"),
                parse_mode="Markdown",
            )
    except Exception as e:
        logger.error(f"Renew error: {e}")
        # Refund on failure
        async with AsyncSessionLocal() as session:
            w = await session.get(Wallet, wallet.id)
            if w:
                w.balance += renew_price
                w.total_spent -= renew_price
                await session.commit()
        await wait_msg.edit_text(
            f"❌ " + ("فشل التجديد، وتم استرجاع الرصيد إلى محفظتك." if lang == "ar" else "Renewal failed. Balance refunded.")
        )
