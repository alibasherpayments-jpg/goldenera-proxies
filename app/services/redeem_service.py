import math
import random
import string
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload

from app.core.database import AsyncSessionLocal
from app.models.user import User, Wallet
from app.models.redeem import RedeemCode, RedeemUsage


def generate_code_string(prefix: str = "GOLD") -> str:
    """Generate an aesthetic, human-friendly promo code like GOLD-8K2M-9P4X."""
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    p1 = "".join(random.choices(chars, k=4))
    p2 = "".join(random.choices(chars, k=4))
    clean_prefix = prefix.strip().upper().replace(" ", "") if prefix else "GOLD"
    return f"{clean_prefix}-{p1}-{p2}"


async def get_redeem_stats() -> Dict[str, Any]:
    """Calculate totals for admin dashboard overview cards."""
    now = datetime.now(timezone.utc)
    async with AsyncSessionLocal() as session:
        all_codes = (await session.execute(select(RedeemCode))).scalars().all()
        usages_res = await session.execute(
            select(func.count(RedeemUsage.id), func.coalesce(func.sum(RedeemUsage.reward_credited), 0.0))
            .where(RedeemUsage.status == "completed")
        )
        total_used_count, total_credited = usages_res.first() or (0, 0.0)

        active_count = 0
        expired_count = 0
        exhausted_count = 0

        for c in all_codes:
            if not c.is_active:
                continue
            if c.used_count >= c.max_uses:
                exhausted_count += 1
            elif c.expires_at and c.expires_at <= now:
                expired_count += 1
            else:
                active_count += 1

        return {
            "total_codes": len(all_codes),
            "active_codes": active_count,
            "expired_codes": expired_count,
            "exhausted_codes": exhausted_count,
            "total_redemptions": total_used_count or 0,
            "total_rewards_credited": round(float(total_credited or 0.0), 2),
        }


async def list_redeem_codes(tab: str = "all") -> List[Dict[str, Any]]:
    """
    List codes with computed live status:
    - 'active': is_active and used_count < max_uses and not expired
    - 'used': used_count >= max_uses
    - 'expired': expires_at <= now and used_count < max_uses
    """
    now = datetime.now(timezone.utc)
    async with AsyncSessionLocal() as session:
        query = select(RedeemCode).order_by(desc(RedeemCode.created_at))
        codes = (await session.execute(query)).scalars().all()

        results = []
        for c in codes:
            # Determine status
            if not c.is_active:
                status = "disabled"
            elif c.used_count >= c.max_uses:
                status = "used"
            elif c.expires_at and c.expires_at <= now:
                status = "expired"
            else:
                status = "active"

            if tab != "all" and status != tab:
                continue

            results.append({
                "id": c.id,
                "code": c.code,
                "code_type": c.code_type,
                "reward_amount": c.reward_amount,
                "reward_type": c.reward_type,
                "min_deposit": c.min_deposit,
                "max_uses": c.max_uses,
                "used_count": c.used_count,
                "remaining_uses": max(0, c.max_uses - c.used_count),
                "expires_at": c.expires_at.isoformat() if c.expires_at else None,
                "is_active": c.is_active,
                "status": status,
                "note": c.note or "",
                "created_at": c.created_at.isoformat() if c.created_at else None,
            })
        return results


async def list_recent_usages(limit: int = 50) -> List[Dict[str, Any]]:
    """List recent code redemptions with user details."""
    async with AsyncSessionLocal() as session:
        query = (
            select(RedeemUsage)
            .options(selectinload(RedeemUsage.code_obj), selectinload(RedeemUsage.user))
            .order_by(desc(RedeemUsage.used_at))
            .limit(limit)
        )
        rows = (await session.execute(query)).scalars().all()
        output = []
        for u in rows:
            output.append({
                "id": u.id,
                "code": u.code_obj.code if u.code_obj else "—",
                "code_type": u.code_obj.code_type if u.code_obj else "—",
                "user_id": u.user_id,
                "account_id": u.user.account_id if u.user and u.user.account_id else (str(u.user.telegram_id) if u.user else "—"),
                "username": u.user.username if u.user else None,
                "first_name": u.user.first_name if u.user else None,
                "reward_credited": u.reward_credited,
                "status": u.status,
                "used_at": u.used_at.isoformat() if u.used_at else None,
            })
        return output


async def redeem_code_by_user(telegram_id: int, raw_code: str, lang: str = "ar") -> Dict[str, Any]:
    """
    Validate and redeem a promo code for a Telegram user.
    Handles:
    - Direct balance / points gift
    - Deposit bonus activation
    Includes strict row locks and duplicate usage checks.
    """
    code_str = raw_code.strip().upper()
    if not code_str:
        return {"success": False, "error": "empty_code"}

    now = datetime.now(timezone.utc)

    async with AsyncSessionLocal() as session:
        # 1. Fetch user & wallet with row lock
        user_res = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = user_res.scalar_one_or_none()
        if not user:
            return {"success": False, "error": "user_not_found"}

        wallet_res = await session.execute(
            select(Wallet).where(Wallet.user_id == user.id).with_for_update()
        )
        wallet = wallet_res.scalar_one_or_none()
        if not wallet:
            wallet = Wallet(user_id=user.id, balance=0.0, total_deposited=0.0, total_spent=0.0)
            session.add(wallet)

        # 2. Find RedeemCode with row lock
        code_res = await session.execute(
            select(RedeemCode).where(func.upper(RedeemCode.code) == code_str).with_for_update()
        )
        code_obj = code_res.scalar_one_or_none()
        if not code_obj:
            return {"success": False, "error": "not_found"}

        if not code_obj.is_active:
            return {"success": False, "error": "inactive"}

        if code_obj.used_count >= code_obj.max_uses:
            return {"success": False, "error": "exhausted"}

        if code_obj.expires_at and code_obj.expires_at <= now:
            return {"success": False, "error": "expired"}

        # 3. Check if user already redeemed this code
        usage_res = await session.execute(
            select(RedeemUsage).where(
                RedeemUsage.code_id == code_obj.id,
                RedeemUsage.user_id == user.id,
            )
        )
        existing_usage = usage_res.scalar_one_or_none()
        if existing_usage:
            return {"success": False, "error": "already_used"}

        # 4. Process Redemption
        if code_obj.code_type == "balance":
            reward_usd = float(code_obj.reward_amount)
            points = int(round(reward_usd * 100))

            wallet.balance = round(wallet.balance + reward_usd, 6)
            wallet.total_deposited = round(wallet.total_deposited + reward_usd, 6)
            code_obj.used_count += 1

            usage = RedeemUsage(
                code_id=code_obj.id,
                user_id=user.id,
                reward_credited=reward_usd,
                status="completed",
            )
            session.add(usage)
            await session.commit()
            await session.refresh(wallet)

            return {
                "success": True,
                "code_type": "balance",
                "reward_amount": reward_usd,
                "points": points,
                "balance": round(wallet.balance, 2),
                "points_total": int(round(wallet.balance * 100)),
            }

        elif code_obj.code_type == "deposit_bonus":
            # Activate pending deposit bonus
            usage = RedeemUsage(
                code_id=code_obj.id,
                user_id=user.id,
                reward_credited=code_obj.reward_amount,
                status="pending_deposit",
            )
            session.add(usage)
            await session.commit()

            return {
                "success": True,
                "code_type": "deposit_bonus",
                "reward_amount": code_obj.reward_amount,
                "reward_type": code_obj.reward_type,
                "min_deposit": code_obj.min_deposit,
            }

        return {"success": False, "error": "unknown_type"}


async def check_and_apply_deposit_bonus(session, user_id: int, deposit_amount_usd: float) -> float:
    """
    Called when a deposit is approved or verified.
    Checks if user has an active 'pending_deposit' bonus promo.
    If conditions met, credits the bonus to user and marks promo completed.
    Returns the bonus amount in USD (0.0 if none).
    """
    try:
        now = datetime.now(timezone.utc)
        query = (
            select(RedeemUsage)
            .options(selectinload(RedeemUsage.code_obj))
            .where(
                RedeemUsage.user_id == user_id,
                RedeemUsage.status == "pending_deposit",
            )
            .order_by(RedeemUsage.used_at.asc())
        )
        res = await session.execute(query)
        pending_list = res.scalars().all()

        for usage in pending_list:
            code = usage.code_obj
            if not code or not code.is_active:
                continue
            if code.expires_at and code.expires_at <= now:
                continue
            if code.used_count >= code.max_uses:
                continue

            # Check min deposit requirement
            if deposit_amount_usd >= code.min_deposit:
                if code.reward_type == "percentage":
                    bonus_usd = round(deposit_amount_usd * (code.reward_amount / 100.0), 2)
                else:
                    bonus_usd = round(code.reward_amount, 2)

                if bonus_usd > 0:
                    code.used_count += 1
                    usage.reward_credited = bonus_usd
                    usage.status = "completed"
                    return bonus_usd

    except Exception as e:
        import logging
        logging.getLogger(__name__).error("Error applying deposit bonus: %s", e)

    return 0.0
