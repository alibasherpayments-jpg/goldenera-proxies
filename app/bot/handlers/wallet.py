"""
Wallet handler — displays user account ID, balance, deposited and spent amounts.
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
        elif lang == "ru":
            text = (
                f"💳 *Мой кошелек и аккаунт | My Wallet*\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"🆔 *ID аккаунта:* `{acc_id}`\n"
                f"💎 *Доступный баланс:* `${balance_usd}`\n"
                f"📈 *Всего пополнено:* `${deposited}`\n"
                f"🛒 *Всего потрачено:* `${spent}`\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"💡 Пополняйте баланс через Binance Pay (ID: `538860756`) или Vodafone Cash."
            )
        elif lang == "hi":
            text = (
                f"💳 *मेरा वॉलेट और अकाउंट | My Wallet*\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"🆔 *अकाउंट आईडी:* `{acc_id}`\n"
                f"💎 *उपलब्ध बैलेंस:* `${balance_usd}`\n"
                f"📈 *कुल जमा:* `${deposited}`\n"
                f"🛒 *कुल खर्च:* `${spent}`\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"💡 आप Binance Pay (ID: `538860756`) या Vodafone Cash से तुरंत रिचार्ज कर सकते हैं।"
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
