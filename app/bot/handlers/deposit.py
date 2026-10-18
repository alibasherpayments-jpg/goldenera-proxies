"""
Deposit handler — Binance USDT TRC20 and Vodafone Cash flows.
Includes FSM states, admin approve/reject callbacks.
"""
import logging
from datetime import datetime, timezone

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.core.config import settings
from app.models.user import User, Wallet
from app.models.deposit import Deposit
from app.models.order import SystemSetting
from app.bot.i18n import t
from app.bot.keyboards.main import (
    deposit_methods_kb,
    back_kb,
    admin_deposit_approve_kb,
    main_menu_kb,
    reply_main_menu_kb,
)
from app.services.binance_service import (
    verify_deposit_txid,
    get_binance_id,
    BinanceVerificationError,
)

logger = logging.getLogger(__name__)
router = Router(name="deposit")


# ─── FSM States ───────────────────────────────────────────────────────────────

class BinanceDeposit(StatesGroup):
    waiting_txid = State()


class DepositVF(StatesGroup):
    waiting_txid = State()
    waiting_amount = State()


# ─── Helpers ──────────────────────────────────────────────────────────────────

async def _get_user_and_wallet(tg_id: int):
    """Fetch user + wallet by telegram_id; returns (user, wallet) or (None, None)."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == tg_id)
        )
        user = result.scalar_one_or_none()
        if user is None:
            return None, None
        wallet_result = await session.execute(
            select(Wallet).where(Wallet.user_id == user.id)
        )
        wallet = wallet_result.scalar_one_or_none()
        return user, wallet


async def _get_egp_rate() -> float:
    """Read USD→EGP rate from SystemSetting or fall back to config."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(SystemSetting).where(SystemSetting.key == "usd_to_egp_rate")
        )
        setting = result.scalar_one_or_none()
        if setting:
            try:
                return float(setting.value)
            except ValueError:
                pass
    return settings.USD_TO_EGP_RATE


async def _get_vodafone_number() -> str:
    """Read Vodafone Cash number dynamically from SystemSetting or fallback to config."""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(SystemSetting).where(SystemSetting.key == "vodafone_cash_number")
            )
            setting = result.scalar_one_or_none()
            if setting and setting.value and setting.value.strip():
                return setting.value.strip()
    except Exception as e:
        logger.warning("Could not read vodafone_cash_number: %s", e)
    return getattr(settings, "VODAFONE_CASH_NUMBER", "") or "010xxxxxxxx"


# ─── deposit:main ─────────────────────────────────────────────────────────────

@router.callback_query(F.data == "deposit:main")
async def cb_deposit_main(callback: CallbackQuery) -> None:
    user, _wallet = await _get_user_and_wallet(callback.from_user.id)
    lang = user.language if user else "ar"
    rate = await _get_egp_rate()

    await callback.message.edit_text(
        text=t("deposit_choose_method", lang, rate=f"{rate:.2f}"),
        parse_mode="Markdown",
        reply_markup=deposit_methods_kb(lang),
    )
    await callback.answer()


# ─── deposit:binance ──────────────────────────────────────────────────────────

@router.callback_query(F.data == "deposit:binance")
async def cb_deposit_binance(callback: CallbackQuery, state: FSMContext) -> None:
    user, _wallet = await _get_user_and_wallet(callback.from_user.id)
    lang = user.language if user else "ar"
    binance_id = await get_binance_id()

    await callback.message.edit_text(
        text=t(
            "deposit_binance_instructions",
            lang,
            binance_id=binance_id,
        ),
        parse_mode="Markdown",
        reply_markup=back_kb(lang),
    )
    await state.set_state(BinanceDeposit.waiting_txid)
    await state.update_data(lang=lang, binance_id=binance_id)
    await callback.answer()


@router.message(BinanceDeposit.waiting_txid)
async def fsm_binance_txid(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang: str = data.get("lang", "ar")
    txid = message.text.strip() if message.text else ""

    if not txid:
        await message.answer(t("deposit_enter_txid", lang))
        return

    # Check TxID not already used
    async with AsyncSessionLocal() as session:
        dup = await session.execute(
            select(Deposit).where(Deposit.txid == txid)
        )
        if dup.scalar_one_or_none():
            await message.answer(t("deposit_txid_used", lang), parse_mode="Markdown")
            await state.clear()
            return

    verifying_msg = await message.answer(
        t("deposit_txid_verifying", lang), parse_mode="Markdown"
    )

    try:
        result = await verify_deposit_txid(txid)
    except Exception as exc:
        logger.error("Verification error for txid %s: %s", txid, exc)
        result = {"valid": False, "confirmed": False}

    # Case 1: Verified automatically via Binance Pay API or TronScan
    if result.get("valid") and result.get("confirmed"):
        amount_usd: float = float(result.get("amount_usd", 0.0))
        points: int = int(round(amount_usd * 100))
        async with AsyncSessionLocal() as session:
            dup = await session.execute(select(Deposit).where(Deposit.txid == txid))
            if dup.scalar_one_or_none():
                await verifying_msg.edit_text(t("deposit_txid_used", lang), parse_mode="Markdown")
                await state.clear()
                return

            user_res = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
            user = user_res.scalar_one_or_none()
            if not user:
                await state.clear()
                return

            wallet_res = await session.execute(select(Wallet).where(Wallet.user_id == user.id))
            wallet = wallet_res.scalar_one_or_none()
            if not wallet:
                wallet = Wallet(user_id=user.id, balance=0.0, total_deposited=0.0, total_spent=0.0)
                session.add(wallet)

            wallet.balance = round(wallet.balance + amount_usd, 6)
            wallet.total_deposited = round(wallet.total_deposited + amount_usd, 6)

            deposit = Deposit(
                user_id=user.id,
                method="binance",
                status="approved",
                txid=txid,
                amount_usd=amount_usd,
            )
            session.add(deposit)
            await session.commit()
            await session.refresh(wallet)

        points_total = int(round(wallet.balance * 100))
        try:
            await verifying_msg.edit_text(
                text=t(
                    "deposit_binance_success",
                    lang,
                    amount=f"{amount_usd:.2f}",
                    points=points,
                    balance=f"{wallet.balance:.2f}",
                    points_total=points_total,
                ),
                parse_mode="Markdown",
                reply_markup=main_menu_kb(lang),
            )
        except Exception as e:
            logger.error("Error editing verifying message on success: %s", e)
            await message.answer(
                t(
                    "deposit_binance_success",
                    lang,
                    amount=f"{amount_usd:.2f}",
                    points=points,
                    balance=f"{wallet.balance:.2f}",
                    points_total=points_total,
                ),
                parse_mode="Markdown",
                reply_markup=main_menu_kb(lang),
            )
        await state.clear()
        return

    # Case 2: Not verified / not found in transaction history (do NOT ask for amount)
    try:
        await verifying_msg.edit_text(
            t("deposit_binance_not_found", lang),
            parse_mode="Markdown",
            reply_markup=back_kb(lang),
        )
    except Exception as e:
        logger.error("Error editing verifying message on not found: %s", e)
        await message.answer(
            t("deposit_binance_not_found", lang),
            parse_mode="Markdown",
            reply_markup=back_kb(lang),
        )
    await state.clear()


# ─── deposit:vf ───────────────────────────────────────────────────────────────

@router.callback_query(F.data == "deposit:vf")
async def cb_deposit_vf(callback: CallbackQuery, state: FSMContext) -> None:
    user, _wallet = await _get_user_and_wallet(callback.from_user.id)
    lang = user.language if user else "ar"
    rate = await _get_egp_rate()
    vodafone_number = await _get_vodafone_number()

    await callback.message.edit_text(
        text=t(
            "deposit_vodafone_instructions",
            lang,
            vodafone_number=vodafone_number,
            rate=f"{rate:.2f}",
        ),
        parse_mode="Markdown",
        reply_markup=back_kb(lang),
    )
    await state.set_state(DepositVF.waiting_txid)
    await state.update_data(lang=lang, rate=rate, vodafone_number=vodafone_number)
    await callback.answer()


@router.message(DepositVF.waiting_txid)
async def fsm_vf_txid(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang: str = data.get("lang", "ar")
    txid = message.text.strip() if message.text else ""

    if not txid:
        await message.answer(t("deposit_vf_enter_txid", lang))
        return

    # Check duplicate TxID
    async with AsyncSessionLocal() as session:
        dup = await session.execute(select(Deposit).where(Deposit.txid == txid))
        if dup.scalar_one_or_none():
            await message.answer(t("deposit_txid_used", lang), parse_mode="Markdown")
            await state.clear()
            return

    await state.update_data(txid=txid)
    await state.set_state(DepositVF.waiting_amount)
    await message.answer(t("deposit_vf_enter_amount", lang), parse_mode="Markdown")


@router.message(DepositVF.waiting_amount)
async def fsm_vf_amount(message: Message, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    lang: str = data.get("lang", "ar")
    txid: str = data.get("txid", "")
    rate: float = data.get("rate", settings.USD_TO_EGP_RATE)

    raw = message.text.strip().replace("$", "") if message.text else ""
    try:
        amount_usd = float(raw)
        if amount_usd <= 0:
            raise ValueError
    except ValueError:
        await message.answer(t("deposit_vf_enter_amount", lang))
        return

    amount_egp = round(amount_usd * rate, 2)
    points = int(round(amount_usd * 100))

    async with AsyncSessionLocal() as session:
        user_result = await session.execute(
            select(User).where(User.telegram_id == message.from_user.id)
        )
        user = user_result.scalar_one_or_none()
        if not user:
            await state.clear()
            return

        deposit = Deposit(
            user_id=user.id,
            method="vodafone_cash",
            status="pending",
            txid=txid,
            sender_phone="—",
            amount_usd=amount_usd,
            amount_local=amount_egp,
            exchange_rate=rate,
        )
        session.add(deposit)
        await session.commit()
        await session.refresh(deposit)
        deposit_id: int = deposit.id

    # Notify user
    await message.answer(
        t(
            "deposit_vf_pending",
            lang,
            txid=txid,
            amount=f"{amount_usd:.2f}",
            amount_egp=f"{amount_egp:.2f}",
            points=points,
        ),
        parse_mode="Markdown",
        reply_markup=main_menu_kb(lang),
    )
    await state.clear()

    # Notify ALL admins
    admin_notify_text = t(
        "admin_vf_deposit_notify",
        "ar",
        name=message.from_user.full_name,
        user_id=message.from_user.id,
        phone=phone,
        txid=txid,
        amount_egp=f"{amount_egp:.2f}",
        amount_usd=f"{amount_usd:.2f}",
        time=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    )

    for admin_id in settings.admin_ids:
        try:
            sent = await bot.send_message(
                chat_id=admin_id,
                text=admin_notify_text,
                parse_mode="Markdown",
                reply_markup=admin_deposit_approve_kb(deposit_id),
            )
            # Store admin message info for editing later
            async with AsyncSessionLocal() as session:
                dep_result = await session.execute(
                    select(Deposit).where(Deposit.id == deposit_id)
                )
                dep = dep_result.scalar_one_or_none()
                if dep and dep.admin_message_id is None:
                    dep.admin_message_id = sent.message_id
                    dep.admin_chat_id = admin_id
                    await session.commit()
        except Exception as exc:
            logger.error("Failed to notify admin %s: %s", admin_id, exc)


# ─── Admin: approve ───────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("admin:approve:"))
async def cb_admin_approve(callback: CallbackQuery, bot: Bot) -> None:
    deposit_id = int(callback.data.split(":")[-1])

    # Auth check
    async with AsyncSessionLocal() as session:
        admin_result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        admin = admin_result.scalar_one_or_none()

    is_admin = (admin and admin.is_admin) or (callback.from_user.id in settings.admin_ids)
    if not is_admin:
        await callback.answer("Unauthorized.", show_alert=True)
        return

    async with AsyncSessionLocal() as session:
        dep_result = await session.execute(
            select(Deposit).where(Deposit.id == deposit_id)
        )
        deposit = dep_result.scalar_one_or_none()

        if not deposit:
            await callback.answer("Deposit not found.", show_alert=True)
            return
        if deposit.status != "pending":
            await callback.answer("Already processed.", show_alert=True)
            return

        deposit.status = "approved"
        deposit.reviewed_by = callback.from_user.id

        # Credit the depositing user
        wallet_result = await session.execute(
            select(Wallet).where(Wallet.user_id == deposit.user_id)
        )
        wallet = wallet_result.scalar_one_or_none()
        if wallet:
            wallet.balance = round(wallet.balance + deposit.amount_usd, 6)
            wallet.total_deposited = round(wallet.total_deposited + deposit.amount_usd, 6)

        # Fetch the depositing user for notification
        user_result = await session.execute(
            select(User).where(User.id == deposit.user_id)
        )
        depositing_user = user_result.scalar_one_or_none()

        await session.commit()
        if wallet:
            await session.refresh(wallet)

    # Edit admin message
    await callback.message.edit_text(
        text=t("admin_deposit_approved_confirm", "ar"),
        parse_mode="Markdown",
    )
    await callback.answer(t("admin_deposit_approved_confirm", "ar"))

    # Notify depositing user
    if depositing_user and wallet:
        user_lang = depositing_user.language
        try:
            await bot.send_message(
                chat_id=depositing_user.telegram_id,
                text=t(
                    "deposit_vf_approved",
                    user_lang,
                    amount=f"{deposit.amount_usd:.2f}",
                    balance=f"{wallet.balance:.2f}",
                ),
                parse_mode="Markdown",
                reply_markup=main_menu_kb(user_lang),
            )
        except Exception as exc:
            logger.error("Failed to notify depositing user: %s", exc)


# ─── Admin: reject ────────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("admin:reject:"))
async def cb_admin_reject(callback: CallbackQuery, bot: Bot) -> None:
    deposit_id = int(callback.data.split(":")[-1])

    # Auth check
    async with AsyncSessionLocal() as session:
        admin_result = await session.execute(
            select(User).where(User.telegram_id == callback.from_user.id)
        )
        admin = admin_result.scalar_one_or_none()

    is_admin = (admin and admin.is_admin) or (callback.from_user.id in settings.admin_ids)
    if not is_admin:
        await callback.answer("Unauthorized.", show_alert=True)
        return

    async with AsyncSessionLocal() as session:
        dep_result = await session.execute(
            select(Deposit).where(Deposit.id == deposit_id)
        )
        deposit = dep_result.scalar_one_or_none()

        if not deposit:
            await callback.answer("Deposit not found.", show_alert=True)
            return
        if deposit.status != "pending":
            await callback.answer("Already processed.", show_alert=True)
            return

        deposit.status = "rejected"
        deposit.reviewed_by = callback.from_user.id

        user_result = await session.execute(
            select(User).where(User.id == deposit.user_id)
        )
        depositing_user = user_result.scalar_one_or_none()
        await session.commit()

    await callback.message.edit_text(
        text=t("admin_deposit_rejected_confirm", "ar"),
        parse_mode="Markdown",
    )
    await callback.answer(t("admin_deposit_rejected_confirm", "ar"))

    if depositing_user:
        user_lang = depositing_user.language
        try:
            await bot.send_message(
                chat_id=depositing_user.telegram_id,
                text=t("deposit_vf_rejected", user_lang),
                parse_mode="Markdown",
                reply_markup=main_menu_kb(user_lang),
            )
        except Exception as exc:
            logger.error("Failed to notify depositing user of rejection: %s", exc)
