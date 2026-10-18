"""
GoldenEra 5G Proxies — Main entry point.
Runs the Telegram bot + FastAPI admin dashboard in one unified process.
"""
import asyncio
import logging
import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Cookie, Request
from fastapi.responses import RedirectResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Update

from app.core.config import settings
from app.core.database import create_tables, engine
from app.bot.handlers import start, deposit, wallet, my_proxies, catalog, redeem
from app.services.notifications import expiry_notification_loop

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

from app.bot.instance import bot

# ── Dispatcher instance ───────────────────────────
dp = Dispatcher(storage=MemoryStorage())

# Register all routers
dp.include_router(start.router)
dp.include_router(deposit.router)
dp.include_router(redeem.router)
dp.include_router(wallet.router)
dp.include_router(my_proxies.router)
dp.include_router(catalog.router)


# ── FastAPI Lifespan ───────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await create_tables()
    except Exception as e:
        logger.warning(f"create_tables on lifespan startup: {e}")

    # Polling only in local development
    if not settings.is_production:
        asyncio.create_task(_run_polling())
        logger.info("🔄 Bot running in long-polling mode.")

    yield


# ── FastAPI App ────────────────────────────────────
app = FastAPI(
    title="GoldenEra Proxies API",
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan,
)

# Mount admin dashboard routes
from app.dashboard.routes import auth_routes, api_routes, page_routes
app.include_router(auth_routes.router)
app.include_router(api_routes.router)
app.include_router(page_routes.router)


@app.get("/")
async def root():
    return RedirectResponse(url="/admin")


# Mount static files & Favicon
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon_ico():
    if os.path.exists("static/favicon.ico"):
        return FileResponse("static/favicon.ico", media_type="image/x-icon")
    elif os.path.exists("static/logo.svg"):
        return FileResponse("static/logo.svg", media_type="image/svg+xml")
    return JSONResponse(status_code=404, content={"error": "Favicon not found"})


@app.get("/favicon.svg", include_in_schema=False)
async def favicon_svg():
    if os.path.exists("static/logo.svg"):
        return FileResponse("static/logo.svg", media_type="image/svg+xml")
    return JSONResponse(status_code=404, content={"error": "Favicon not found"})


@app.get("/health")
async def health():
    return {"status": "ok", "service": "goldenera-proxies-bot"}


# Webhook endpoint (production)
@app.post("/webhook")
async def webhook(update: dict):
    try:
        telegram_update = Update.model_validate(update)
        await dp.feed_update(bot=bot, update=telegram_update)
    except Exception as e:
        logger.error(f"Webhook update error: {e}")
    return {"ok": True}


@app.get("/set-webhook")
async def set_webhook_endpoint(
    url: str = None,
    secret_key: str = None,
    admin_token: str = Cookie(None, alias="admin_token"),
):
    from app.dashboard.auth import get_admin_optional
    is_admin = bool(get_admin_optional(admin_token)) or (secret_key and secret_key == settings.DASHBOARD_SECRET_KEY)
    if not is_admin:
        return JSONResponse(status_code=403, content={"error": "Forbidden: Admin authentication required."})

    target = url or settings.WEBHOOK_BASE_URL
    if not target:
        return {"error": "Target URL required. Pass ?url=https://your-domain.vercel.app or set WEBHOOK_BASE_URL"}
    target_clean = target.rstrip("/") + "/webhook"
    res = await bot.set_webhook(target_clean, drop_pending_updates=True)
    info = await bot.get_webhook_info()
    return {"success": res, "url": target_clean, "webhook_info": info.model_dump()}


@app.get("/webhook-info")
async def webhook_info(
    secret_key: str = None,
    admin_token: str = Cookie(None, alias="admin_token"),
):
    from app.dashboard.auth import get_admin_optional
    is_admin = bool(get_admin_optional(admin_token)) or (secret_key and secret_key == settings.DASHBOARD_SECRET_KEY)
    if not is_admin:
        return JSONResponse(status_code=403, content={"error": "Forbidden: Admin authentication required."})
    info = await bot.get_webhook_info()
    return info.model_dump()


# ── Polling helper (development only) ─────────────
async def _run_polling():
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"Polling error: {e}")


# ── Entry point ───────────────────────────────────
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=not settings.is_production,
        log_level="info",
    )
