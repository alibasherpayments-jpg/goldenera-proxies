"""
GoldenEra 5G Proxies — Main entry point.
Runs the Telegram bot + FastAPI admin dashboard in one unified process.
"""
import asyncio
import logging
import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Update

from app.core.config import settings
from app.core.database import create_tables, engine
from app.bot.handlers import start, deposit, wallet, my_proxies, catalog
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
dp.include_router(wallet.router)
dp.include_router(my_proxies.router)
dp.include_router(catalog.router)


# ── FastAPI Lifespan ───────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting GoldenEra Proxies Bot...")
    await create_tables()
    logger.info("✅ Database tables ready.")

    if settings.is_production and settings.WEBHOOK_BASE_URL:
        webhook_url = f"{settings.WEBHOOK_BASE_URL}/webhook"
        await bot.set_webhook(webhook_url, drop_pending_updates=True)
        logger.info(f"✅ Webhook set to {webhook_url}")
    else:
        # Development: polling mode
        asyncio.create_task(_run_polling())
        logger.info("🔄 Bot running in long-polling mode.")

    # Start expiry notification background task
    asyncio.create_task(expiry_notification_loop(bot))
    logger.info("⏰ Expiry notification loop started.")

    yield

    # Shutdown
    logger.info("🛑 Shutting down...")
    await bot.session.close()
    await engine.dispose()


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


@app.get("/health")
async def health():
    return {"status": "ok", "service": "goldenera-proxies-bot"}


# Webhook endpoint (production)
@app.post("/webhook")
async def webhook(update: dict):
    telegram_update = Update.model_validate(update)
    await dp.feed_update(bot=bot, update=telegram_update)
    return {"ok": True}


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
