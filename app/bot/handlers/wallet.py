"""
Wallet handler — displays user account ID, balance, points, deposited and spent amounts.
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
        points = f"{(wallet.balance * 100):.0f}"
        deposited = f"{wallet.total_deposited:.2f}"
        spent = f"{wallet.total_spent:.2f}"

        if lang == "ar":
            text = (
                f"💳 *محفظتي وتفاصيل الحساب | My Wallet*\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"🆔 *معرّف الحساب (ID):* `{acc_id}`\n"
                f"💎 *الرصيد المتاح:* `${balance_usd}`\n"
                f"🎯 *رصيد النقاط:* `{points} نقطة`\n"
                f"📈 *إجمالي المشحون:* `${deposited}`\n"
                f"🛒 *إجمالي المشتريات:* `${spent}`\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"💡 *ملاحظة:* كل 1 دولار = 100 نقطة. يمكنك شحن الرصيد فوراً عبر Binance USDT TRC20 أو فودافون كاش."
            )
        elif lang == "ru":
            text = (
                f"💳 *Мой кошелек и аккаунт | My Wallet*\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"🆔 *ID аккаунта:* `{acc_id}`\n"
                f"💎 *Доступный баланс:* `${balance_usd}`\n"
                f"🎯 *Баллы:* `{points} pts`\n"
                f"📈 *Всего пополнено:* `${deposited}`\n"
                f"🛒 *Всего потрачено:* `${spent}`\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"💡 $1.00 USD = 100 баллов. Пополняйте через Binance USDT или Vodafone Cash."
            )
        elif lang == "hi":
            text = (
                f"💳 *मेरा वॉलेट और अकाउंट | My Wallet*\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"🆔 *अकाउंट आईडी:* `{acc_id}`\n"
                f"💎 *उपलब्ध बैलेंस:* `${balance_usd}`\n"
                f"🎯 *अंक (Points):* `{points} pts`\n"
                f"📈 *कुल जमा:* `${deposited}`\n"
                f"🛒 *कुल खर्च:* `${spent}`\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"💡 $1.00 = 100 अंक। आप Binance USDT या Vodafone Cash से रिचार्ज कर सकते हैं।"
            )
        else:
            text = (
                f"💳 *My Wallet & Account Profile*\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"🆔 *Account ID:* `{acc_id}`\n"
                f"💎 *Available Balance:* `${balance_usd}`\n"
                f"🎯 *Points Balance:* `{points} Points`\n"
                f"📈 *Total Deposited:* `${deposited}`\n"
                f"🛒 *Total Spent:* `${spent}`\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"💡 *Note:* $1.00 USD = 100 Points. You can top up instantly via Binance USDT or Vodafone Cash."
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
