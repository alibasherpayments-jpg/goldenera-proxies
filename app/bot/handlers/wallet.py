"""
Wallet handler — displays user balance, total deposited, and spent amounts.
"""
import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.user import User, Wallet
from app.bot.i18n import t

logger = logging.getLogger(__name__)
router = Router(name="wallet")


@router.callback_query(F.data == "menu:wallet")
async def show_wallet(callback: CallbackQuery):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User, Wallet)
            .join(Wallet, Wallet.user_id == User.id)
            .where(User.telegram_id == callback.from_user.id)
        )
        row = result.first()
        if not row:
            await callback.answer(t("error_generic", "ar"), show_alert=True)
            return

        user, wallet = row
        lang = user.language or "ar"

        text = (
            f"{t('wallet_title', lang)}\n\n"
            f"{t('wallet_body', lang, balance=f'{wallet.balance:.2f}', reserved='0.00', total_spent=f'{wallet.total_spent:.2f}')}"
        )

        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=t("menu_deposit", lang), callback_data="deposit:main"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=t("btn_back", lang), callback_data="menu:main"
                    )
                ],
            ]
        )

        try:
            await callback.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
        except Exception:
            await callback.message.answer(text, reply_markup=kb, parse_mode="Markdown")

        await callback.answer()
