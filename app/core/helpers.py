"""
Shared database helper utilities.
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.order import SystemSetting
from app.core.config import settings


async def get_setting(session: AsyncSession, key: str, default: Optional[str] = None) -> Optional[str]:
    """Retrieve a system setting value from the database."""
    result = await session.execute(select(SystemSetting).where(SystemSetting.key == key))
    setting = result.scalar_one_or_none()
    return setting.value if setting else default


async def set_setting(session: AsyncSession, key: str, value: str) -> None:
    """Set or update a system setting."""
    result = await session.execute(select(SystemSetting).where(SystemSetting.key == key))
    setting = result.scalar_one_or_none()
    if setting:
        setting.value = value
    else:
        session.add(SystemSetting(key=key, value=value))
    await session.commit()


async def get_markup_percent(session: AsyncSession) -> float:
    val = await get_setting(session, "markup_percent")
    try:
        return float(val) if val else settings.DEFAULT_MARKUP_PERCENT
    except ValueError:
        return settings.DEFAULT_MARKUP_PERCENT


async def get_usd_to_egp_rate(session: AsyncSession) -> float:
    val = await get_setting(session, "usd_to_egp_rate")
    try:
        return float(val) if val else settings.USD_TO_EGP_RATE
    except ValueError:
        return settings.USD_TO_EGP_RATE


async def get_vodafone_number(session: AsyncSession) -> str:
    val = await get_setting(session, "vodafone_cash_number")
    return val or settings.VODAFONE_CASH_NUMBER


def apply_markup(base_price: float, markup_percent: float) -> float:
    """Apply markup percentage to a base price and round to 2 decimals."""
    return round(base_price * (1 + markup_percent / 100), 2)
