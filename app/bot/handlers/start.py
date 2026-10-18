"""
Start handler — /start, /help, main menu callbacks, initial & ongoing language selection.
"""
import logging
import random
import time
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.user import User, Wallet
from app.bot.i18n import t, LANGUAGES
from app.bot.keyboards.main import (
    main_menu_kb,
    language_kb,
    initial_language_kb,
    support_kb,
    back_kb,
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
        # Backfill account_id if not present
        if not user.account_id:
            user.account_id = await generate_unique_account_id(session)
        # Keep profile fields up to date
        user.username = tg_user.username
        user.first_name = tg_user.first_name
        user.last_name = tg_user.last_name

    # Ensure wallet exists
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
    points = f"{(wallet.balance * 100):.0f}"

    if lang == "ar":
        return (
            f"⚡️ *أهلاً بك في جولدن إيرا للبروكسيات | GOLDENERA 5G*\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"🆔 *معرّف الحساب (ID):* `{acc_id}`\n"
            f"💎 *الرصيد المتاح:* `${balance_usd}`\n"
            f"🎯 *رصيد النقاط:* `{points} نقطة`\n"
            f"🌐 *اللغة الحالية:* 🇸🇦 العربية\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"🚀 *أقوى وأسرع بروكسيات 5G وسكنية نقية 100%*\n"
            f"• سرعات اتصال فائقة تصل إلى 1 Gbps\n"
            f"• تدوير فوري وتغطية دولية واسعة\n"
            f"• تسليم فوري وتلقائي بمجرد الشراء\n\n"
            f"👇 *اختر من القائمة أدناه للبدء:*"
        )
    elif lang == "ru":
        return (
            f"⚡️ *Добро пожаловать в GOLDENERA 5G*\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"🆔 *ID аккаунта:* `{acc_id}`\n"
            f"💎 *Баланс:* `${balance_usd}`\n"
            f"🎯 *Баллы:* `{points} pts`\n"
            f"🌐 *Язык:* 🇷🇺 Русский\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"🚀 *Быстрые мобильные 5G и резидентские прокси*\n"
            f"• Скорость до 1 Гбит/с\n"
            f"• Мгновенная ротация IP\n"
            f"• Автоматическая выдача\n\n"
            f"👇 *Выберите действие из меню:*"
        )
    elif lang == "hi":
        return (
            f"⚡️ *GoldenEra 5G प्रॉक्सी में आपका स्वागत है*\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"🆔 *अकाउंट आईडी:* `{acc_id}`\n"
            f"💎 *बैलेंस:* `${balance_usd}`\n"
            f"🎯 *अंक (Points):* `{points} pts`\n"
            f"🌐 *भाषा:* 🇮🇳 हिन्दी\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"🚀 *हाई-स्पीड 5G और रेसिडेंशियल प्रॉक्सी*\n"
            f"• 1 Gbps तक की स्पीड\n"
            f"• तुरंत IP रोटेशन\n"
            f"• तुरंत डिलीवरी\n\n"
            f"👇 *शुरू करने के लिए नीचे चुनें:*"
        )
    else:
        return (
            f"⚡️ *WELCOME TO GOLDENERA 5G PROXIES*\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"🆔 *Account ID:* `{acc_id}`\n"
            f"💎 *Balance:* `${balance_usd}`\n"
            f"🎯 *Points:* `{points} Points`\n"
            f"🌐 *Language:* 🇬🇧 English\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"🚀 *Fastest 5G Mobile & Residential Proxies*\n"
            f"• Ultra-fast speeds up to 1 Gbps\n"
            f"• Instant IP rotation & Multiple Geo-Locations\n"
            f"• Instant automated delivery\n\n"
            f"👇 *Select an option below to proceed:*"
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

    await message.answer(
        text=_build_welcome(user, wallet),
        parse_mode="Markdown",
        reply_markup=main_menu_kb(user.language),
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

    await callback.message.edit_text(
        text=_build_welcome(user, wallet),
        parse_mode="Markdown",
        reply_markup=main_menu_kb(user.language),
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


# ─── menu:main ────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "menu:main")
async def cb_menu_main(callback: CallbackQuery) -> None:
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

    await callback.message.edit_text(
        text=_build_welcome(user, wallet),
        parse_mode="Markdown",
        reply_markup=main_menu_kb(user.language),
    )
    await callback.answer()


# ─── menu:support ─────────────────────────────────────────────────────────────

@router.callback_query(F.data == "menu:support")
async def cb_menu_support(callback: CallbackQuery) -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
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

    await callback.message.edit_text(
        text=support_text,
        parse_mode="Markdown",
        reply_markup=support_kb(lang),
    )
    await callback.answer()


# ─── menu:language ────────────────────────────────────────────────────────────

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


# ─── lang:{code} ──────────────────────────────────────────────────────────────

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

    # Acknowledge in the new language, then show main menu
    await callback.message.edit_text(
        text=t("lang_changed", new_lang) + "\n\n" + _build_welcome(user, wallet),
        parse_mode="Markdown",
        reply_markup=main_menu_kb(new_lang),
    )
    await callback.answer()
