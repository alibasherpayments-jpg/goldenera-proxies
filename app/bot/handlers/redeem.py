"""
Redeem Code handler for GoldenEra 5G Proxies bot.
Handles promo code input, direct balance crediting, and deposit bonus activation.
"""
import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.bot.i18n import t
from app.bot.keyboards.main import (
    back_kb,
    reply_main_menu_kb,
    ALL_REDEEM_TEXTS,
)
from app.services.redeem_service import redeem_code_by_user

logger = logging.getLogger(__name__)
router = Router(name="redeem")


class RedeemState(StatesGroup):
    waiting_code = State()


async def _get_user_lang(tg_id: int) -> str:
    async with AsyncSessionLocal() as session:
        user_res = await session.execute(select(User).where(User.telegram_id == tg_id))
        user = user_res.scalar_one_or_none()
        return user.language if user and user.language else "ar"


@router.message(F.text.in_(ALL_REDEEM_TEXTS))
@router.message(Command("redeem"))
async def cmd_redeem_entry(message: Message, state: FSMContext) -> None:
    lang = await _get_user_lang(message.from_user.id)
    await state.set_state(RedeemState.waiting_code)
    await state.update_data(lang=lang)
    await message.answer(
        text=t("redeem_enter_code", lang),
        parse_mode="Markdown",
        reply_markup=back_kb(lang),
    )


@router.callback_query(F.data == "redeem:enter")
async def cb_redeem_entry(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await _get_user_lang(callback.from_user.id)
    await state.set_state(RedeemState.waiting_code)
    await state.update_data(lang=lang)
    await callback.message.edit_text(
        text=t("redeem_enter_code", lang),
        parse_mode="Markdown",
        reply_markup=back_kb(lang),
    )
    await callback.answer()


@router.message(RedeemState.waiting_code)
async def fsm_redeem_code(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("lang") or await _get_user_lang(message.from_user.id)
    raw_code = message.text.strip() if message.text else ""

    if not raw_code:
        await message.answer(t("redeem_enter_code", lang))
        return

    # Basic sanitization
    if len(raw_code) < 3 or len(raw_code) > 64:
        await message.answer(t("redeem_err_not_found", lang))
        return

    res = await redeem_code_by_user(message.from_user.id, raw_code, lang)

    if res.get("success"):
        await state.clear()
        code_type = res.get("code_type")

        if code_type == "balance":
            msg = t(
                "redeem_success_balance",
                lang,
                amount=f"{res['reward_amount']:.2f}",
                points=res["points"],
                balance=f"{res['balance']:.2f}",
                points_total=res["points_total"],
            )
        else:
            msg = t(
                "redeem_success_bonus",
                lang,
                amount=f"{res['reward_amount']:.2f}",
                min_deposit=f"{res['min_deposit']:.2f}",
            )

        await message.answer(text=msg, parse_mode="Markdown", reply_markup=reply_main_menu_kb(lang))
        return

    # Error handling
    err = res.get("error")
    if err == "not_found":
        err_msg = t("redeem_err_not_found", lang)
    elif err == "inactive":
        err_msg = t("redeem_err_inactive", lang)
    elif err == "expired":
        err_msg = t("redeem_err_expired", lang)
    elif err == "exhausted":
        err_msg = t("redeem_err_exhausted", lang)
    elif err == "already_used":
        err_msg = t("redeem_err_already_used", lang)
    else:
        err_msg = t("redeem_err_not_found", lang)

    await message.answer(text=err_msg, parse_mode="Markdown", reply_markup=reply_main_menu_kb(lang))
