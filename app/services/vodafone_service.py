"""
Services for handling Vodafone Cash deposit logic.
"""
from datetime import datetime
from typing import Optional


def calculate_usd_from_egp(amount_egp: float, rate: float) -> float:
    """Convert EGP amount to USD using the given exchange rate."""
    if rate <= 0:
        return 0.0
    return round(amount_egp / rate, 2)


def calculate_egp_from_usd(amount_usd: float, rate: float) -> float:
    """Convert USD amount to EGP using the given exchange rate."""
    return round(amount_usd * rate, 2)


def format_deposit_reference(deposit_id: int) -> str:
    """Generate a human-readable deposit reference."""
    return f"DEP-{deposit_id:06d}"
