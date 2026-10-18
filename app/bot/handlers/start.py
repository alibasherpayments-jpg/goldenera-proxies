"""
Start handler — /start, /help, main menu callbacks, language selection.
"""
import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.user import User, Wallet
from app.bot.i18n import t, LANGUAGES
from app.bot.keyboards.main import main_menu_kb, language_kb, back_kb

logger = logging.getLogger(__name__)
router = Router(name="start")


# ─── Helpers ──────────────────────────────────────────────────────────────────

async def get_or_create_user(
    session: AsyncSession, tg_user
) -> tuple[User, Wallet]:
    """
    Upsert a Telegram user and ensure a wallet exists.
    Returns (User, Wallet) — both are attached to *session*.
    """
    result = await session.execute(
        select(User).where(User.telegram_id == tg_user.id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        user = User(
            telegram_id=tg_user.id,
            username=tg_user.username,
            first_name=tg_user.first_name,
            last_name=tg_user.last_name,
            language="ar",
        )
        session.add(user)
        await session.flush()  # Populate user.id before creating wallet
    else:
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
    lang = user.language
    title = t("welcome_title", lang)
    body = t("welcome_body", lang, balance=f"{wallet.balance:.2f}")
    return f"{title}\n\n{body}"


# ─── /start ───────────────────────────────────────────────────────────────────

@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    async with AsyncSessionLocal() as session:
        user, wallet = await get_or_create_user(session, message.from_user)

    await message.answer(
        text=_build_welcome(user, wallet),
        parse_mode="Markdown",
        reply_markup=main_menu_kb(user.language),
    )


# ─── /help ────────────────────────────────────────────────────────────────────

@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = result.scalar_one_or_none()
        lang = user.language if user else "ar"

    await message.answer(
        text=t("support_message", lang),
        parse_mode="Markdown",
        reply_markup=back_kb(lang),
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

    await callback.message.edit_text(
        text=t("support_message", lang),
        parse_mode="Markdown",
        reply_markup=back_kb(lang),
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
            user.language = new_lang
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
