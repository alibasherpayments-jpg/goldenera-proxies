"""
Start handler — /start, /help, language onboarding, and Reply Keyboard menu navigation.
"""
import logging
import random
import time
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload

from app.core.database import AsyncSessionLocal
from app.models.user import User, Wallet
from app.models.proxy import Proxy
from app.bot.i18n import t, LANGUAGES
from app.bot.keyboards.main import (
    reply_main_menu_kb,
    language_kb,
    initial_language_kb,
    support_kb,
    back_kb,
    deposit_methods_kb,
    proxy_card_kb,
    SUPPORT_URL,
    ALL_BUY_TEXTS,
    ALL_MY_PROXIES_TEXTS,
    ALL_DEPOSIT_TEXTS,
    ALL_WALLET_TEXTS,
    ALL_SUPPORT_TEXTS,
    ALL_LANG_TEXTS,
)

logger = logging.getLogger(__name__)
router = Router(name="start")


# ─── Helpers ──────────────────────────────────────────────────────────────────

async def generate_unique_account_id(session: AsyncSession) -> str:
    """Generates a random unique 10-digit numeric ID for each user."""
    for _ in range(25):
        cand = str(random.randint(1000000000, 9999999999))
        res = await session.execute(select(User).where(User.account_id == cand))
        if res.scalar_one_or_none() is None:
            return cand
    return str(int(time.time() * 1000))[:10]


async def get_or_create_user(
    session: AsyncSession, tg_user
) -> tuple[User, Wallet]:
    """
    Upsert a Telegram user with unique random account_id and ensure a wallet exists.
    Returns (User, Wallet) — both are attached to *session*.
    """
    result = await session.execute(
        select(User).where(User.telegram_id == tg_user.id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        account_id = await generate_unique_account_id(session)
        user = User(
            telegram_id=tg_user.id,
            account_id=account_id,
            username=tg_user.username,
            first_name=tg_user.first_name,
            last_name=tg_user.last_name,
            language="ar",
            has_selected_language=False,
        )
        session.add(user)
        await session.flush()
    else:
        if not user.account_id:
            user.account_id = await generate_unique_account_id(session)
        user.username = tg_user.username
        user.first_name = tg_user.first_name
        user.last_name = tg_user.last_name

    wallet_result = await session.execute(
        select(Wallet).where(Wallet.user_id == user.id)
    )
    wallet = wallet_result.scalar_one_or_none()

    if wallet is None:
        wallet = Wallet(user_id=user.id, balance=0.0, total_deposited=0.0, total_spent=0.0)
        session.add(wallet)

    await session.commit()
    await session.refresh(user)
    await session.refresh(wallet)
    return user, wallet


def _build_welcome(user: User, wallet: Wallet) -> str:
    lang = user.language or "ar"
    acc_id = user.account_id or str(user.telegram_id)
    balance_usd = f"{wallet.balance:.2f}"
    points = int(round(wallet.balance * 100))

    if lang == "ar":
        return (
            f"⚡️ *أهلاً بك في جولدن إيرا | GOLDENERA 5G*\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"🆔 *معرّف الحساب:* `{acc_id}`\n"
            f"🎯 *النقاط:* `{points} نقطة` (${balance_usd})\n"
            f"🌐 *اللغة الحالية:* 🇸🇦 العربية\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"🚀 *أقوى وأسرع بروكسيات 5G وسكنية نقية 100%*\n"
            f"• سرعات اتصال فائقة تصل إلى 1 Gbps\n"
            f"• تدوير فوري للآيبي ومواقع جغرافية متعددة\n"
            f"• تسليم فوري وتلقائي بمجرد الشراء\n\n"
            f"👇 *استخدم أزرار القائمة بالأسفل للتنقل بسهولة:*"
        )
    elif lang == "ru":
        return (
            f"⚡️ *Добро пожаловать в GOLDENERA 5G*\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"🆔 *ID аккаунта:* `{acc_id}`\n"
            f"🎯 *Баллы:* `{points} баллов` (${balance_usd})\n"
            f"🌐 *Язык:* 🇷🇺 Русский\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"🚀 *Быстрые мобильные 5G и резидентские прокси*\n"
            f"• Скорость до 1 Гбит/с\n"
            f"• Мгновенная ротация IP\n"
            f"• Автоматическая выдача\n\n"
            f"👇 *Используйте кнопки меню внизу для навигации:*"
        )
    elif lang == "hi":
        return (
            f"⚡️ *GoldenEra 5G प्रॉक्सी में आपका स्वागत है*\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"🆔 *अकाउंट आईडी:* `{acc_id}`\n"
            f"🎯 *पॉइंट्स:* `{points} पॉइंट्स` (${balance_usd})\n"
            f"🌐 *भाषा:* 🇮🇳 हिन्दी\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"🚀 *हाई-स्पीड 5G और रेसिडेंशियल प्रॉक्सी*\n"
            f"• 1 Gbps तक की स्पीड\n"
            f"• तुरंत IP रोटेशन\n"
            f"• तुरंत डिलीवरी\n\n"
            f"👇 *नेविगेट करने के लिए नीचे दिए गए मेनू का उपयोग करें:*"
        )
    else:
        return (
            f"⚡️ *WELCOME TO GOLDENERA 5G PROXIES*\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"🆔 *Account ID:* `{acc_id}`\n"
            f"🎯 *Points:* `{points} pts` (${balance_usd})\n"
            f"🌐 *Language:* 🇬🇧 English\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"🚀 *Fastest 5G Mobile & Residential Proxies*\n"
            f"• Ultra-fast speeds up to 1 Gbps\n"
            f"• Instant IP rotation & Multiple Geo-Locations\n"
            f"• Instant automated delivery\n\n"
            f"👇 *Use the bottom menu buttons to navigate:* "
        )


# ─── /start ───────────────────────────────────────────────────────────────────

@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    async with AsyncSessionLocal() as session:
        user, wallet = await get_or_create_user(session, message.from_user)

    # First-time start: ask user to select language first!
    if not user.has_selected_language:
        acc_id = user.account_id or str(user.telegram_id)
        welcome_prompt = (
            f"👋 *Welcome to GoldenEra 5G Proxies!*\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"🆔 *Account Created! Your ID:* `{acc_id}`\n\n"
            f"🌐 *Please select your language to continue:*\n"
            f"يرجى اختيار لغتك المفضلة للمتابعة:\n"
            f"Пожалуйста, выберите язык для продолжения:\n"
            f"कृपया जारी रखने के लिए अपनी भाषा चुनें:"
        )
        await message.answer(
            text=welcome_prompt,
            parse_mode="Markdown",
            reply_markup=initial_language_kb(),
        )
        return

    # Send welcome text with bottom Reply Keyboard
    await message.answer(
        text=_build_welcome(user, wallet),
        parse_mode="Markdown",
        reply_markup=reply_main_menu_kb(user.language),
    )


# ─── lang_init:{code} ─────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("lang_init:"))
async def cb_lang_init(callback: CallbackQuery) -> None:
    code = callback.data.split(":", 1)[1]
    if code not in LANGUAGES:
        code = "ar"

    async with AsyncSessionLocal() as session:
        res = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = res.scalar_one_or_none()
        if user is None:
            user, wallet = await get_or_create_user(session, callback.from_user)
        else:
            if not user.account_id:
                user.account_id = await generate_unique_account_id(session)
            user.language = code
            user.has_selected_language = True
            wallet_res = await session.execute(
                select(Wallet).where(Wallet.user_id == user.id)
            )
            wallet = wallet_res.scalar_one_or_none()
            if wallet is None:
                wallet = Wallet(user_id=user.id, balance=0.0, total_deposited=0.0, total_spent=0.0)
                session.add(wallet)
            await session.commit()
            await session.refresh(user)
            await session.refresh(wallet)

    try:
        await callback.message.delete()
    except Exception:
        pass

    # Send welcome with persistent bottom Reply Keyboard
    await callback.message.answer(
        text=_build_welcome(user, wallet),
        parse_mode="Markdown",
        reply_markup=reply_main_menu_kb(user.language),
    )
    await callback.answer()


# ─── /help ────────────────────────────────────────────────────────────────────

@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        lang = user.language if user else "ar"

    support_text = (
        "💬 *الدعم الفني المباشر | Support*\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "لأي استفسار، مساعدة فنية، أو مشاكل في شحن الرصيد والبروكسيات، يمكنك التواصل مباشرة مع الإدارة عبر تيليجرام:\n\n"
        "👤 *حساب الدعم:* [@BumBoyAliBasher](https://t.me/BumBoyAliBasher)\n"
        "⏰ *متاحين للرد السريع على مدار الساعة*"
    ) if lang == "ar" else (
        "💬 *Customer Support*\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "For any assistance, billing inquiries, or technical support, contact our team directly on Telegram:\n\n"
        "👤 *Support Contact:* [@BumBoyAliBasher](https://t.me/BumBoyAliBasher)\n"
        "⏰ *Available 24/7 for fast assistance*"
    )

    await message.answer(
        text=support_text,
        parse_mode="Markdown",
        reply_markup=support_kb(lang),
    )


# ─── Reply Keyboard Handlers (Large Bottom Buttons) ───────────────────────────

@router.message(F.text.in_(ALL_BUY_TEXTS))
async def handle_reply_buy(message: Message) -> None:
    async with AsyncSessionLocal() as session:
        user_res = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = user_res.scalar_one_or_none()
        lang = user.language if user else "ar"

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t("catalog_prime_hyper", lang), callback_data="buy:cat:prime")],
            [InlineKeyboardButton(text=t("catalog_nexus", lang), callback_data="buy:cat:nexus")],
            [InlineKeyboardButton(text=t("catalog_titan", lang), callback_data="buy:cat:titan")],
        ]
    )
    text = (
        "🚀 *اختر باقة البروكسي التي تناسبك:*\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "⚡️ *PRIME / HYPER*: بروكسيات 5G فائقة السرعة وتدوير غير محدود.\n"
        "🔄 *NEXUS*: تدوير فوري للآيبي ومواقع جغرافية متعددة.\n"
        "💎 *TITAN*: بروكسيات سكنية فائقة النقاء للأعمال الحساسة.\n"
    ) if lang == "ar" else (
        "🚀 *Select a Proxy Package:*\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "⚡️ *PRIME / HYPER*: High-speed 5G Mobile proxies with unlimited rotation.\n"
        "🔄 *NEXUS*: Instant API IP rotation and extensive geo-locations.\n"
        "💎 *TITAN*: Elite Residential proxies for sensitive operations.\n"
    )
    await message.answer(text=text, parse_mode="Markdown", reply_markup=kb)


@router.message(F.text.in_(ALL_MY_PROXIES_TEXTS))
async def handle_reply_my_proxies(message: Message) -> None:
    async with AsyncSessionLocal() as session:
        user_res = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = user_res.scalar_one_or_none()
        if not user:
            user, _ = await get_or_create_user(session, message.from_user)

        lang = user.language or "ar"

        proxies_res = await session.execute(
            select(Proxy)
            .where(Proxy.user_id == user.id, Proxy.is_active == True)
            .order_by(desc(Proxy.created_at))
        )
        active_proxies = proxies_res.scalars().all()

    if not active_proxies:
        no_proxies_text = (
            "🔌 *ليس لديك أي بروكسيات نشطة حالياً.*\n\n"
            "يمكنك شراء بروكسي 5G فائق السرعة الآن بالضغط على زر *🚀 شراء بروكسي 5G* بالأسفل."
        ) if lang == "ar" else (
            "🔌 *You have no active proxies at the moment.*\n\n"
            "You can purchase high-speed 5G proxies by tapping *🚀 Buy 5G Proxies* below."
        )
        await message.answer(text=no_proxies_text, parse_mode="Markdown")
        return

    title = t("my_proxies_title", lang, count=len(active_proxies))
    await message.answer(text=f"*{title}*", parse_mode="Markdown")

    for p in active_proxies:
        card_text = (
            f"🔌 *{p.product_name or p.product_code}*\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"📍 *Location:* {p.country_name or p.country}\n"
            f"🌐 *Host:* `{p.host}`\n"
            f"🔌 *Port:* `{p.port}`\n"
            f"👤 *Username:* `{p.username}`\n"
            f"🔑 *Password:* `{p.password}`\n"
            f"📅 *Expires:* {p.expiry_date.strftime('%Y-%m-%d %H:%M') if p.expiry_date else '—'}\n"
        )
        await message.answer(
            text=card_text,
            parse_mode="Markdown",
            reply_markup=proxy_card_kb(lang, p.request_id, p.category),
        )


@router.message(F.text.in_(ALL_DEPOSIT_TEXTS))
async def handle_reply_deposit(message: Message) -> None:
    async with AsyncSessionLocal() as session:
        user_res = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = user_res.scalar_one_or_none()
        lang = user.language if user else "ar"

        from app.core.helpers import get_usd_to_egp_rate
        rate = await get_usd_to_egp_rate(session)

    rate_str = f"{int(rate)}" if float(rate).is_integer() else f"{float(rate):.2f}"
    text = t("deposit_choose_method", lang, rate=rate_str)
    await message.answer(
        text=text,
        parse_mode="Markdown",
        reply_markup=deposit_methods_kb(lang),
    )


@router.message(F.text.in_(ALL_WALLET_TEXTS))
async def handle_reply_wallet(message: Message) -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User, Wallet)
            .join(Wallet, Wallet.user_id == User.id)
            .where(User.telegram_id == message.from_user.id)
        )
        row = result.first()
        if not row:
            user, wallet = await get_or_create_user(session, message.from_user)
        else:
            user, wallet = row

        lang = user.language or "ar"
        acc_id = user.account_id or str(user.telegram_id)
        balance_usd = f"{wallet.balance:.2f}"
        deposited = f"{wallet.total_deposited:.2f}"
        spent = f"{wallet.total_spent:.2f}"

        if lang == "ar":
            text = (
                f"💳 *محفظتي وتفاصيل الحساب | My Wallet*\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"🆔 *معرّف الحساب (ID):* `{acc_id}`\n"
                f"💎 *الرصيد المتاح:* `${balance_usd}`\n"
                f"📈 *إجمالي المشحون:* `${deposited}`\n"
                f"🛒 *إجمالي المشتريات:* `${spent}`\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"💡 *شحن الرصيد:* يمكنك شحن رصيدك فوراً وبأمان عبر Binance Pay (ID: `538860756`) أو محفظة فودافون كاش."
            )
        else:
            text = (
                f"💳 *My Wallet & Account Profile*\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"🆔 *Account ID:* `{acc_id}`\n"
                f"💎 *Available Balance:* `${balance_usd}`\n"
                f"📈 *Total Deposited:* `${deposited}`\n"
                f"🛒 *Total Spent:* `${spent}`\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"💡 *Top-up:* Instant deposits supported via Binance Pay (ID: `538860756`) and Vodafone Cash."
            )

        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=t("menu_deposit", lang), callback_data="deposit:main"),
                    InlineKeyboardButton(text=t("menu_redeem", lang), callback_data="redeem:enter"),
                ]
            ]
        )
        await message.answer(text=text, reply_markup=kb, parse_mode="Markdown")


@router.message(F.text.in_(ALL_SUPPORT_TEXTS))
async def handle_reply_support(message: Message) -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        lang = user.language if user else "ar"

    support_text = (
        "💬 *الدعم الفني المباشر | Direct Support*\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "لأي استفسار، مساعدة فنية، أو مشاكل في شحن الرصيد والبروكسيات، يمكنك التواصل مباشرة مع الإدارة عبر تيليجرام:\n\n"
        "👤 *حساب الدعم:* [@BumBoyAliBasher](https://t.me/BumBoyAliBasher)\n"
        "⏰ *متاحين للرد السريع على مدار الساعة*"
    ) if lang == "ar" else (
        "💬 *Customer Support*\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "For any assistance, billing inquiries, or technical support, contact our team directly on Telegram:\n\n"
        "👤 *Support Contact:* [@BumBoyAliBasher](https://t.me/BumBoyAliBasher)\n"
        "⏰ *Available 24/7 for fast assistance*"
    )

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💬 Open Support Chat", url=SUPPORT_URL)]
        ]
    )
    await message.answer(text=support_text, parse_mode="Markdown", reply_markup=kb)


@router.message(F.text.in_(ALL_LANG_TEXTS))
async def handle_reply_language(message: Message) -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        lang = user.language if user else "ar"

    await message.answer(
        text=t("lang_select_title", lang),
        parse_mode="Markdown",
        reply_markup=language_kb(),
    )


# ─── Ongoing Inline Callbacks ─────────────────────────────────────────────────

@router.callback_query(F.data == "menu:main")
async def cb_menu_main(callback: CallbackQuery, state: FSMContext = None) -> None:
    if state:
        await state.clear()

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            user, wallet = await get_or_create_user(session, callback.from_user)
        else:
            if not user.account_id:
                user.account_id = await generate_unique_account_id(session)
            wallet_result = await session.execute(
                select(Wallet).where(Wallet.user_id == user.id)
            )
            wallet = wallet_result.scalar_one_or_none()
            if wallet is None:
                wallet = Wallet(user_id=user.id, balance=0.0, total_deposited=0.0, total_spent=0.0)
                session.add(wallet)
                await session.commit()
                await session.refresh(wallet)

    try:
        await callback.message.edit_text(
            text=_build_welcome(user, wallet),
            parse_mode="Markdown",
        )
    except Exception:
        await callback.message.answer(
            text=_build_welcome(user, wallet),
            parse_mode="Markdown",
            reply_markup=reply_main_menu_kb(user.language),
        )
    await callback.answer()


@router.callback_query(F.data == "menu:language")
async def cb_menu_language(callback: CallbackQuery) -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        lang = user.language if user else "ar"

    await callback.message.edit_text(
        text=t("lang_select_title", lang),
        parse_mode="Markdown",
        reply_markup=language_kb(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("lang:"))
async def cb_lang_select(callback: CallbackQuery) -> None:
    new_lang = callback.data.split(":", 1)[1]
    if new_lang not in LANGUAGES:
        await callback.answer("Unknown language.", show_alert=True)
        return

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            user, wallet = await get_or_create_user(session, callback.from_user)
        else:
            if not user.account_id:
                user.account_id = await generate_unique_account_id(session)
            user.language = new_lang
            user.has_selected_language = True
            wallet_result = await session.execute(
                select(Wallet).where(Wallet.user_id == user.id)
            )
            wallet = wallet_result.scalar_one_or_none()
            if wallet is None:
                wallet = Wallet(user_id=user.id, balance=0.0, total_deposited=0.0, total_spent=0.0)
                session.add(wallet)
            await session.commit()
            await session.refresh(user)
            await session.refresh(wallet)

    # Edit message and refresh persistent bottom reply keyboard
    try:
        await callback.message.delete()
    except Exception:
        pass

    await callback.message.answer(
        text=t("lang_changed", new_lang) + "\n\n" + _build_welcome(user, wallet),
        parse_mode="Markdown",
        reply_markup=reply_main_menu_kb(new_lang),
    )
    await callback.answer()
