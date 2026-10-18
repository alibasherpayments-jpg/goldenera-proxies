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
    binance_id: Optional[str] = None
    binance_api_key: Optional[str] = None
    binance_secret_key: Optional[str] = None


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

        recent_orders_rows = await db.execute(
            select(Order).options(selectinload(Order.user)).order_by(desc(Order.created_at)).limit(10)
        )
        recent_orders = [
            {
                "id": o.id,
                "user_id": o.user_id,
                "telegram_id": o.user.telegram_id if o.user else o.user_id,
                "account_id": o.user.account_id if o.user and o.user.account_id else (str(o.user.telegram_id) if o.user else "—"),
                "username": o.user.username if o.user else None,
                "product_code": o.product_code,
                "status": o.status,
                "amount": o.amount_deducted,
                "created_at": o.created_at.isoformat() if o.created_at else None,
            }
            for o in recent_orders_rows.scalars().all()
        ]

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
        "recent_orders": recent_orders,
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
            search_clean = search.strip()
            q = q.where(
                (User.username.ilike(f"%{search_clean}%"))
                | (User.first_name.ilike(f"%{search_clean}%"))
                | (User.account_id.ilike(f"%{search_clean}%"))
                | (User.telegram_id == int(search_clean) if search_clean.isdigit() else False)
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
                    "account_id": u.account_id or str(u.telegram_id),
                    "telegram_id": u.telegram_id,
                    "username": u.username,
                    "first_name": u.first_name,
                    "last_name": u.last_name,
                    "language": u.language,
                    "is_banned": u.is_banned,
                    "is_admin": u.is_admin,
                    "balance": round(u.wallet.balance if u.wallet else 0.0, 2),
                    "points": int(round((u.wallet.balance if u.wallet else 0.0) * 100)),
                    "total_deposited": round(u.wallet.total_deposited if u.wallet else 0.0, 2),
                    "total_spent": round(u.wallet.total_spent if u.wallet else 0.0, 2),
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


@router.get("/admin/api/users/{telegram_id}/transactions")
async def get_user_transactions(telegram_id: int, _admin=Depends(get_current_admin)):
    async with AsyncSessionLocal() as db:
        user_res = await db.execute(select(User).where(User.telegram_id == telegram_id))
        user = user_res.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        deposits_res = await db.execute(
            select(Deposit).where(Deposit.user_id == user.id).order_by(desc(Deposit.created_at))
        )
        deposits = deposits_res.scalars().all()

        orders_res = await db.execute(
            select(Order).where(Order.user_id == user.id).order_by(desc(Order.created_at))
        )
        orders = orders_res.scalars().all()

        txs = []
        for d in deposits:
            txs.append({
                "type": "deposit",
                "method": d.method,
                "amount": d.amount_usd,
                "status": d.status,
                "txid": d.txid,
                "details": f"Deposit via {d.method.upper()}",
                "date": d.created_at.isoformat() if d.created_at else None,
            })

        for o in orders:
            txs.append({
                "type": "order",
                "method": o.request_type,
                "amount": -o.amount_deducted,
                "status": o.status,
                "txid": o.magnum_request_id or "—",
                "details": f"Proxy {o.request_type.title()} ({o.product_code})",
                "date": o.created_at.isoformat() if o.created_at else None,
            })

        txs.sort(key=lambda x: x["date"] or "", reverse=True)
        return {
            "account_id": user.account_id or str(user.telegram_id),
            "telegram_id": user.telegram_id,
            "username": user.username,
            "transactions": txs,
        }


@router.get("/admin/api/transactions")
async def list_all_transactions(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    _admin=Depends(get_current_admin),
):
    async with AsyncSessionLocal() as db:
        deposits_res = await db.execute(
            select(Deposit, User)
            .join(User, User.id == Deposit.user_id)
            .order_by(desc(Deposit.created_at))
            .limit(100)
        )
        orders_res = await db.execute(
            select(Order, User)
            .join(User, User.id == Order.user_id)
            .order_by(desc(Order.created_at))
            .limit(100)
        )

        all_txs = []
        for d, u in deposits_res.all():
            all_txs.append({
                "id": f"DEP-{d.id}",
                "user_id": u.id,
                "account_id": u.account_id or str(u.telegram_id),
                "telegram_id": u.telegram_id,
                "username": u.username or u.first_name or "—",
                "type": "deposit",
                "amount": d.amount_usd,
                "status": d.status,
                "method": d.method,
                "reference": d.txid,
                "date": d.created_at.isoformat() if d.created_at else None,
            })

        for o, u in orders_res.all():
            all_txs.append({
                "id": f"ORD-{o.id}",
                "user_id": u.id,
                "account_id": u.account_id or str(u.telegram_id),
                "telegram_id": u.telegram_id,
                "username": u.username or u.first_name or "—",
                "type": "order",
                "amount": -o.amount_deducted,
                "status": o.status,
                "method": o.request_type,
                "reference": o.magnum_request_id or o.product_code,
                "date": o.created_at.isoformat() if o.created_at else None,
            })

        all_txs.sort(key=lambda x: x["date"] or "", reverse=True)
        total = len(all_txs)
        offset = (page - 1) * per_page
        paginated = all_txs[offset : offset + per_page]

        return {
            "total": total,
            "page": page,
            "per_page": per_page,
            "transactions": paginated,
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
                    "user_account_id": d.user.account_id if d.user and d.user.account_id else (str(d.user.telegram_id) if d.user else "—"),
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
                points = int(round(deposit.amount_usd * 100))
                total_pts = int(round((deposit.user.wallet.balance if deposit.user.wallet else 0.0) * 100))
                bal_usd = f"{deposit.user.wallet.balance:.2f}" if deposit.user.wallet else "0.00"
                await bot.send_message(
                    chat_id=deposit.user.telegram_id,
                    text=(
                        f"✅ <b>تم قبول إيداعك بنجاح!</b>\n\n"
                        f"💰 المبلغ: <b>${deposit.amount_usd:.2f}</b>\n"
                        f"🎯 النقاط المضافة: <b>+{points} نقطة</b>\n"
                        f"💎 رصيد محفظتك: <b>{total_pts} نقطة (${bal_usd})</b>\n"
                        f"📋 المعرّف: <code>{deposit.txid}</code>\n\n"
                        f"شكراً لك! يمكنك الآن شراء البروكسيات مباشرة 🎉"
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
                    "location": p.display_location,
                    "flag": p.flag,
                    "protocol": p.protocol,
                    "host": p.host,
                    "port": p.port,
                    "auth_username": p.username,
                    "auth_password": p.password,
                    "is_active": p.is_active,
                    "price_paid": p.price_paid,
                    "expiry_date": p.expiry_date.isoformat() if p.expiry_date else None,
                    "created_at": p.created_at.isoformat() if p.created_at else None,
                    "user_telegram_id": p.user.telegram_id if p.user else None,
                    "user_account_id": p.user.account_id if p.user and p.user.account_id else (str(p.user.telegram_id) if p.user else "—"),
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
        "binance_id": rows.get("binance_id", getattr(settings, "BINANCE_ID", "538860756") or "538860756"),
        "binance_api_key": rows.get("binance_api_key", settings.BINANCE_API_KEY),
        "has_binance_secret": bool(rows.get("binance_secret_key") or settings.BINANCE_SECRET_KEY),
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
    if body.binance_id is not None:
        updates["binance_id"] = body.binance_id.strip()
    if body.binance_api_key is not None:
        updates["binance_api_key"] = body.binance_api_key.strip()
    if body.binance_secret_key is not None and body.binance_secret_key.strip() and not body.binance_secret_key.startswith("••"):
        updates["binance_secret_key"] = body.binance_secret_key.strip()

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


# ── Redeem Codes API ──────────────────────────────────────────────────────────

class RedeemCodeCreate(BaseModel):
    code: str
    code_type: str = "balance"
    reward_amount: float
    reward_type: str = "fixed"
    min_deposit: float = 0.0
    max_uses: int = 1
    expires_at: Optional[str] = None
    note: Optional[str] = None


@router.get("/admin/api/redeem/stats")
async def api_get_redeem_stats(_admin=Depends(get_current_admin)):
    from app.services.redeem_service import get_redeem_stats
    return await get_redeem_stats()


@router.get("/admin/api/redeem/codes")
async def api_get_redeem_codes(tab: str = "all", _admin=Depends(get_current_admin)):
    from app.services.redeem_service import list_redeem_codes
    return await list_redeem_codes(tab)


@router.post("/admin/api/redeem/codes")
async def api_create_redeem_code(body: RedeemCodeCreate, _admin=Depends(get_current_admin)):
    code_clean = body.code.strip().upper()
    if not code_clean:
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    if body.reward_amount <= 0:
        raise HTTPException(status_code=400, detail="Reward amount must be greater than zero")

    exp_dt = None
    if body.expires_at:
        try:
            exp_dt = datetime.fromisoformat(body.expires_at)
            if exp_dt.tzinfo is None:
                exp_dt = exp_dt.replace(tzinfo=timezone.utc)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid expiration date format")

    from app.models.redeem import RedeemCode
    async with AsyncSessionLocal() as db:
        # Check duplicate code
        dup = (await db.execute(select(RedeemCode).where(func.upper(RedeemCode.code) == code_clean))).scalar_one_or_none()
        if dup:
            raise HTTPException(status_code=400, detail=f"Code '{code_clean}' already exists")

        new_code = RedeemCode(
            code=code_clean,
            code_type=body.code_type,
            reward_amount=body.reward_amount,
            reward_type=body.reward_type,
            min_deposit=max(0.0, body.min_deposit),
            max_uses=max(1, body.max_uses),
            used_count=0,
            expires_at=exp_dt,
            is_active=True,
            note=body.note.strip() if body.note else None,
        )
        db.add(new_code)
        await db.commit()
        await db.refresh(new_code)

    return {"success": True, "code": new_code.code, "id": new_code.id}


@router.post("/admin/api/redeem/codes/{code_id}/toggle")
async def api_toggle_redeem_code(code_id: int, _admin=Depends(get_current_admin)):
    from app.models.redeem import RedeemCode
    async with AsyncSessionLocal() as db:
        c = await db.get(RedeemCode, code_id)
        if not c:
            raise HTTPException(status_code=404, detail="Code not found")
        c.is_active = not c.is_active
        await db.commit()
    return {"success": True, "is_active": c.is_active}


@router.delete("/admin/api/redeem/codes/{code_id}")
async def api_delete_redeem_code(code_id: int, _admin=Depends(get_current_admin)):
    from app.models.redeem import RedeemCode
    async with AsyncSessionLocal() as db:
        c = await db.get(RedeemCode, code_id)
        if not c:
            raise HTTPException(status_code=404, detail="Code not found")
        await db.delete(c)
        await db.commit()
    return {"success": True}


@router.get("/admin/api/redeem/usages")
async def api_get_redeem_usages(_admin=Depends(get_current_admin)):
    from app.services.redeem_service import list_recent_usages
    return await list_recent_usages(limit=50)
