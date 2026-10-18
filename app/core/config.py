from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List
import secrets


class Settings(BaseSettings):
    # ── Telegram
    BOT_TOKEN: str
    ADMIN_CHAT_IDS: str = ""

    # ── Magnum API
    MAGNUM_API_KEY: str
    MAGNUM_BASE_URL: str = "https://api.magnumproxy.com"

    # ── Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./goldenera.db"

    # ── Dashboard Auth
    DASHBOARD_SECRET_KEY: str = secrets.token_hex(32)
    DASHBOARD_USERNAME: str = "admin"
    DASHBOARD_PASSWORD: str = "changeme"

    # ── Binance
    BINANCE_API_KEY: str = ""
    BINANCE_SECRET_KEY: str = ""
    BINANCE_WALLET_ADDRESS: str = ""
    BINANCE_MERCHANT_ID: str = ""

    # ── Vodafone Cash
    VODAFONE_CASH_NUMBER: str = ""

    # ── Currency & Pricing
    USD_TO_EGP_RATE: float = 52.0
    DEFAULT_MARKUP_PERCENT: float = 30.0

    # ── App
    ENVIRONMENT: str = "development"
    PORT: int = 8000
    WEBHOOK_BASE_URL: str = ""

    @property
    def admin_ids(self) -> List[int]:
        if not self.ADMIN_CHAT_IDS:
            return []
        return [int(x.strip()) for x in self.ADMIN_CHAT_IDS.split(",") if x.strip()]

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
