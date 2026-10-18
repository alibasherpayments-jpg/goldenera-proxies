"""
Background task: poll expiring proxies and send Telegram notifications.
Runs as an asyncio task every 30 minutes.
"""
import asyncio
import logging
from datetime import datetime, timezone, timedelta
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.proxy import Proxy
from app.models.user import User
from app.bot.i18n import t

logger = logging.getLogger(__name__)


async def notify_expiring_proxies(bot):
    """Check for proxies expiring soon and notify their owners."""
    async with AsyncSessionLocal() as session:
        now = datetime.now(timezone.utc)
        in_24h = now + timedelta(hours=24)
        in_2h = now + timedelta(hours=2)

        # Proxies expiring in next 24h that haven't been notified
        result = await session.execute(
            select(Proxy).where(
                Proxy.is_active == True,
                Proxy.expiry_date <= in_24h,
                Proxy.expiry_date > now,
                Proxy.notified_24h == False,
            ).join(User)
        )
        proxies_24h = result.scalars().all()

        for proxy in proxies_24h:
            user = await session.get(User, proxy.user_id)
            if not user:
                continue
            hours_left = int((proxy.expiry_date - now).total_seconds() / 3600)
            try:
                await bot.send_message(
                    chat_id=user.telegram_id,
                    text=t("proxy_expires_soon", user.language,
                           location=proxy.display_location,
                           hours=hours_left),
                    parse_mode="Markdown",
                )
                proxy.notified_24h = True
                logger.info(f"Notified user {user.telegram_id} for 24h proxy expiry {proxy.request_id}")
            except Exception as e:
                logger.warning(f"Failed to notify user {user.telegram_id}: {e}")

        # Proxies expiring in next 2h
        result = await session.execute(
            select(Proxy).where(
                Proxy.is_active == True,
                Proxy.expiry_date <= in_2h,
                Proxy.expiry_date > now,
                Proxy.notified_2h == False,
            )
        )
        proxies_2h = result.scalars().all()

        for proxy in proxies_2h:
            user = await session.get(User, proxy.user_id)
            if not user:
                continue
            hours_left = max(1, int((proxy.expiry_date - now).total_seconds() / 3600))
            try:
                await bot.send_message(
                    chat_id=user.telegram_id,
                    text=t("proxy_expires_soon", user.language,
                           location=proxy.display_location,
                           hours=hours_left),
                    parse_mode="Markdown",
                )
                proxy.notified_2h = True
            except Exception as e:
                logger.warning(f"Failed to notify user {user.telegram_id}: {e}")

        # Mark expired proxies as inactive
        result = await session.execute(
            select(Proxy).where(
                Proxy.is_active == True,
                Proxy.expiry_date < now,
            )
        )
        expired = result.scalars().all()
        for proxy in expired:
            proxy.is_active = False

        await session.commit()


async def expiry_notification_loop(bot):
    """Run expiry checks every 30 minutes indefinitely."""
    while True:
        try:
            await notify_expiring_proxies(bot)
        except Exception as e:
            logger.error(f"Error in expiry notification loop: {e}")
        await asyncio.sleep(1800)  # 30 minutes
