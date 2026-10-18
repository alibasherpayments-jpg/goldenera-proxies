"""
Admin REST API routes — all protected by JWT cookie auth.
"""
from datetime import datetime, timezone, date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import select, func, update, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import AsyncSessionLocal
from app.core.config import settings
from app.dashboard.auth import get_current_admin
from app.models.user import User, Wallet
from app.models.deposit import Deposit, DepositStatus
from app.models.proxy import Proxy
from app.models.order import Order, SystemSetting
from app.services.magnum_client import magnum

router = APIRouter()


# ── DB helper ──────────────────────────────────────────────────────────────

async def get_db_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        return session


# ── Pydantic schemas ────────────────────────────────────────────────────────

class BalanceAdjust(BaseModel):
    amount: float
    note: str = ""


class SettingsUpdate(BaseModel):
    markup_percent: Optional[float] = None
    usd_to_egp_rate: Optional[float] = None
    vodafone_cash_number: Optional[str] = None


class BroadcastBody(BaseModel):
    message: str


# ── Stats ───────────────────────────────────────────────────────────────────

@router.get("/admin/api/stats")
async def get_stats(_admin=Depends(get_current_admin)):
    async with AsyncSessionLocal() as db:
        total_users = (await db.execute(select(func.count(User.id)))).scalar_one()

        active_proxies = (
            await db.execute(select(func.count(Proxy.id)).where(Proxy.is_active == True))
        ).scalar_one()

        today_start = datetime.now(timezone.utc).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        today_revenue_row = await db.execute(
            select(func.coalesce(func.sum(Order.amount_deducted), 0)).where(
                Order.status == "succeeded",
                Order.created_at >= today_start,
            )
        )
        today_revenue = float(today_revenue_row.scalar_one())

        today_orders = (
            await db.execute(
                select(func.count(Order.id)).where(Order.created_at >= today_start)
            )
        ).scalar_one()

        pending_deposits_count = (
            await db.execute(
                select(func.count(Deposit.id)).where(Deposit.status == DepositStatus.PENDING)
            )
        ).scalar_one()

    # Magnum wallet balance
    magnum_balance = 0.0
    try:
        wallet_data = await magnum.get_wallet()
        magnum_balance = float(wallet_data.get("balance", 0))
    except Exception:
        magnum_balance = -1.0  # signal error

    return {
        "total_users": total_users,
        "active_proxies": active_proxies,
        "today_revenue": round(today_revenue, 2),
        "magnum_balance": round(magnum_balance, 2),
        "pending_deposits_count": pending_deposits_count,
        "today_orders": today_orders,
    }


# ── Users ────────────────────────────────────────────────────────────────────

@router.get("/admin/api/users")
async def list_users(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    search: Optional[str] = None,
    _admin=Depends(get_current_admin),
):
    offset = (page - 1) * per_page
    async with AsyncSessionLocal() as db:
        q = select(User).options(selectinload(User.wallet)).order_by(desc(User.created_at))
        if search:
            q = q.where(
                (User.username.ilike(f"%{search}%"))
                | (User.first_name.ilike(f"%{search}%"))
                | (User.telegram_id == int(search) if search.isdigit() else False)
            )
        total = (await db.execute(select(func.count()).select_from(q.subquery()))).scalar_one()
        users_result = await db.execute(q.offset(offset).limit(per_page))
        users = users_result.scalars().all()

        return {
            "total": total,
            "page": page,
            "per_page": per_page,
            "users": [
                {
                    "id": u.id,
                    "telegram_id": u.telegram_id,
                    "username": u.username,
                    "first_name": u.first_name,
                    "last_name": u.last_name,
                    "language": u.language,
                    "is_banned": u.is_banned,
                    "is_admin": u.is_admin,
                    "balance": round(u.wallet.balance if u.wallet else 0.0, 4),
                    "total_deposited": round(u.wallet.total_deposited if u.wallet else 0.0, 4),
                    "total_spent": round(u.wallet.total_spent if u.wallet else 0.0, 4),
                    "created_at": u.created_at.isoformat() if u.created_at else None,
                }
                for u in users
            ],
        }


@router.get("/admin/api/users/{telegram_id}")
async def get_user_detail(telegram_id: int, _admin=Depends(get_current_admin)):
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(User)
            .options(
                selectinload(User.wallet),
                selectinload(User.proxies),
                selectinload(User.deposits),
            )
            .where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "id": user.id,
            "telegram_id": user.telegram_id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "language": user.language,
            "is_banned": user.is_banned,
            "is_admin": user.is_admin,
            "balance": round(user.wallet.balance if user.wallet else 0.0, 4),
            "total_deposited": round(user.wallet.total_deposited if user.wallet else 0.0, 4),
            "total_spent": round(user.wallet.total_spent if user.wallet else 0.0, 4),
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "proxies": [
                {
                    "id": p.id,
                    "request_id": p.request_id,
                    "category": p.category,
                    "country": p.country,
                    "country_name": p.country_name,
                    "is_active": p.is_active,
                    "expiry_date": p.expiry_date.isoformat() if p.expiry_date else None,
                    "price_paid": p.price_paid,
                }
                for p in user.proxies
            ],
            "deposits": [
                {
                    "id": d.id,
                    "method": d.method,
                    "status": d.status,
                    "txid": d.txid,
                    "amount_usd": d.amount_usd,
                    "amount_local": d.amount_local,
                    "created_at": d.created_at.isoformat() if d.created_at else None,
                }
                for d in user.deposits
            ],
        }


@router.patch("/admin/api/users/{telegram_id}/balance")
async def adjust_balance(
    telegram_id: int,
    body: BalanceAdjust,
    admin=Depends(get_current_admin),
):
    async with AsyncSessionLocal() as db:
        user_result = await db.execute(
            select(User).options(selectinload(User.wallet)).where(User.telegram_id == telegram_id)
        )
        user = user_result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not user.wallet:
            raise HTTPException(status_code=400, detail="User has no wallet")

        user.wallet.balance = round(user.wallet.balance + body.amount, 6)
        if body.amount > 0:
            user.wallet.total_deposited = round(user.wallet.total_deposited + body.amount, 6)
        await db.commit()

    return {"success": True, "new_balance": user.wallet.balance, "note": body.note}


@router.patch("/admin/api/users/{telegram_id}/ban")
async def toggle_ban(telegram_id: int, admin=Depends(get_current_admin)):
    async with AsyncSessionLocal() as db:
        user_result = await db.execute(select(User).where(User.telegram_id == telegram_id))
        user = user_result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.is_banned = not user.is_banned
        await db.commit()
        return {"success": True, "telegram_id": telegram_id, "is_banned": user.is_banned}


# ── Deposits ─────────────────────────────────────────────────────────────────

@router.get("/admin/api/deposits")
async def list_deposits(
    status_filter: Optional[str] = Query(None, alias="status"),
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    _admin=Depends(get_current_admin),
):
    offset = (page - 1) * per_page
    async with AsyncSessionLocal() as db:
        q = (
            select(Deposit)
            .options(selectinload(Deposit.user))
            .order_by(desc(Deposit.created_at))
        )
        if status_filter:
            q = q.where(Deposit.status == status_filter)

        total = (await db.execute(select(func.count()).select_from(q.subquery()))).scalar_one()
        result = await db.execute(q.offset(offset).limit(per_page))
        deposits = result.scalars().all()

        return {
            "total": total,
            "page": page,
            "per_page": per_page,
            "deposits": [
                {
                    "id": d.id,
                    "user_telegram_id": d.user.telegram_id if d.user else None,
                    "user_name": (
                        d.user.first_name or d.user.username if d.user else "Unknown"
                    ),
                    "method": d.method,
                    "status": d.status,
                    "txid": d.txid,
                    "sender_phone": d.sender_phone,
                    "amount_usd": d.amount_usd,
                    "amount_local": d.amount_local,
                    "exchange_rate": d.exchange_rate,
                    "review_note": d.review_note,
                    "created_at": d.created_at.isoformat() if d.created_at else None,
                }
                for d in deposits
            ],
        }


@router.post("/admin/api/deposits/{deposit_id}/approve")
async def approve_deposit(deposit_id: int, admin=Depends(get_current_admin)):
    async with AsyncSessionLocal() as db:
        dep_result = await db.execute(
            select(Deposit)
            .options(selectinload(Deposit.user).selectinload(User.wallet))
            .where(Deposit.id == deposit_id)
        )
        deposit = dep_result.scalar_one_or_none()
        if not deposit:
            raise HTTPException(status_code=404, detail="Deposit not found")
        if deposit.status != DepositStatus.PENDING:
            raise HTTPException(status_code=400, detail=f"Deposit is already {deposit.status}")

        deposit.status = DepositStatus.APPROVED
        deposit.reviewed_by = int(admin.get("sub", 0)) if str(admin.get("sub", "")).isdigit() else None

        # Credit wallet
        if deposit.user and deposit.user.wallet:
            deposit.user.wallet.balance = round(
                deposit.user.wallet.balance + deposit.amount_usd, 6
            )
            deposit.user.wallet.total_deposited = round(
                deposit.user.wallet.total_deposited + deposit.amount_usd, 6
            )

        await db.commit()

        # Notify user via Telegram bot
        if deposit.user:
            try:
                from app.bot.instance import bot
                await bot.send_message(
                    chat_id=deposit.user.telegram_id,
                    text=(
                        f"✅ <b>تم قبول إيداعك</b>\n\n"
                        f"💰 المبلغ: <b>${deposit.amount_usd:.2f}</b>\n"
                        f"📋 المعرّف: <code>{deposit.txid}</code>\n\n"
                        f"رصيدك تم تحديثه. شكراً لك! 🎉"
                    ),
                    parse_mode="HTML",
                )
            except Exception:
                pass  # Don't fail the API call if notification fails

    return {"success": True, "deposit_id": deposit_id, "new_status": "approved"}


@router.post("/admin/api/deposits/{deposit_id}/reject")
async def reject_deposit(deposit_id: int, admin=Depends(get_current_admin)):
    async with AsyncSessionLocal() as db:
        dep_result = await db.execute(
            select(Deposit)
            .options(selectinload(Deposit.user))
            .where(Deposit.id == deposit_id)
        )
        deposit = dep_result.scalar_one_or_none()
        if not deposit:
            raise HTTPException(status_code=404, detail="Deposit not found")
        if deposit.status != DepositStatus.PENDING:
            raise HTTPException(status_code=400, detail=f"Deposit is already {deposit.status}")

        deposit.status = DepositStatus.REJECTED
        deposit.reviewed_by = int(admin.get("sub", 0)) if str(admin.get("sub", "")).isdigit() else None
        await db.commit()

        # Notify user via Telegram bot
        if deposit.user:
            try:
                from app.bot.instance import bot
                await bot.send_message(
                    chat_id=deposit.user.telegram_id,
                    text=(
                        f"❌ <b>تم رفض طلب الإيداع</b>\n\n"
                        f"💰 المبلغ: <b>${deposit.amount_usd:.2f}</b>\n"
                        f"📋 المعرّف: <code>{deposit.txid}</code>\n\n"
                        f"إذا كنت تعتقد أن هذا خطأ، يرجى التواصل مع الدعم."
                    ),
                    parse_mode="HTML",
                )
            except Exception:
                pass

    return {"success": True, "deposit_id": deposit_id, "new_status": "rejected"}


# ── Proxies ──────────────────────────────────────────────────────────────────

@router.get("/admin/api/proxies")
async def list_proxies(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    active_only: bool = Query(True),
    _admin=Depends(get_current_admin),
):
    offset = (page - 1) * per_page
    async with AsyncSessionLocal() as db:
        q = select(Proxy).options(selectinload(Proxy.user)).order_by(desc(Proxy.created_at))
        if active_only:
            q = q.where(Proxy.is_active == True)

        total = (await db.execute(select(func.count()).select_from(q.subquery()))).scalar_one()
        result = await db.execute(q.offset(offset).limit(per_page))
        proxies = result.scalars().all()

        return {
            "total": total,
            "page": page,
            "per_page": per_page,
            "proxies": [
                {
                    "id": p.id,
                    "request_id": p.request_id,
                    "category": p.category,
                    "mode": p.mode,
                    "product_code": p.product_code,
                    "country": p.country,
                    "country_name": p.country_name,
                    "protocol": p.protocol,
                    "host": p.host,
                    "port": p.port,
                    "is_active": p.is_active,
                    "price_paid": p.price_paid,
                    "expiry_date": p.expiry_date.isoformat() if p.expiry_date else None,
                    "created_at": p.created_at.isoformat() if p.created_at else None,
                    "user_telegram_id": p.user.telegram_id if p.user else None,
                    "user_name": (
                        p.user.first_name or p.user.username if p.user else "Unknown"
                    ),
                }
                for p in proxies
            ],
        }


# ── System Settings ──────────────────────────────────────────────────────────

@router.get("/admin/api/settings")
async def get_settings(_admin=Depends(get_current_admin)):
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(SystemSetting))
        rows = {r.key: r.value for r in result.scalars().all()}

    return {
        "markup_percent": float(rows.get("markup_percent", settings.DEFAULT_MARKUP_PERCENT)),
        "usd_to_egp_rate": float(rows.get("usd_to_egp_rate", settings.USD_TO_EGP_RATE)),
        "vodafone_cash_number": rows.get("vodafone_cash_number", settings.VODAFONE_CASH_NUMBER),
    }


@router.patch("/admin/api/settings")
async def update_settings(body: SettingsUpdate, _admin=Depends(get_current_admin)):
    updates: dict[str, str] = {}
    if body.markup_percent is not None:
        updates["markup_percent"] = str(body.markup_percent)
    if body.usd_to_egp_rate is not None:
        updates["usd_to_egp_rate"] = str(body.usd_to_egp_rate)
    if body.vodafone_cash_number is not None:
        updates["vodafone_cash_number"] = body.vodafone_cash_number

    async with AsyncSessionLocal() as db:
        for key, value in updates.items():
            existing = await db.get(SystemSetting, key)
            if existing:
                existing.value = value
            else:
                db.add(SystemSetting(key=key, value=value))
        await db.commit()

    return {"success": True, "updated": list(updates.keys())}


# ── Broadcast ────────────────────────────────────────────────────────────────

@router.post("/admin/api/broadcast")
async def broadcast_message(body: BroadcastBody, _admin=Depends(get_current_admin)):
    if not body.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(User.telegram_id).where(User.is_banned == False)
        )
        telegram_ids = result.scalars().all()

    sent = 0
    failed = 0
    try:
        from app.bot.instance import bot
        for tg_id in telegram_ids:
            try:
                await bot.send_message(chat_id=tg_id, text=body.message, parse_mode="HTML")
                sent += 1
            except Exception:
                failed += 1
    except ImportError:
        raise HTTPException(status_code=500, detail="Bot instance not available")

    return {"success": True, "sent": sent, "failed": failed, "total": len(telegram_ids)}
