from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings


connect_args = {}
if "sqlite" in settings.DATABASE_URL:
    connect_args = {"check_same_thread": False}
elif "postgresql" in settings.DATABASE_URL:
    connect_args = {
        "ssl": True,
        "server_settings": {"search_path": "goldenera,public"},
    }

engine_kwargs = {
    "echo": False,
    "connect_args": connect_args,
}
if "postgresql" in settings.DATABASE_URL:
    engine_kwargs.update({
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "pool_size": 3,
        "max_overflow": 0,
    })

engine = create_async_engine(
    settings.DATABASE_URL,
    **engine_kwargs,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def create_tables():
    import app.models  # noqa: F401
    from sqlalchemy import text
    import logging
    log = logging.getLogger(__name__)

    async with engine.begin() as conn:
        if "postgresql" in settings.DATABASE_URL:
            await conn.execute(text("CREATE SCHEMA IF NOT EXISTS goldenera;"))
        await conn.run_sync(Base.metadata.create_all)

        # Safe schema updates for existing tables
        try:
            if "postgresql" in settings.DATABASE_URL:
                await conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS account_id VARCHAR(32);"))
                await conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS has_selected_language BOOLEAN DEFAULT FALSE;"))
                await conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS uq_users_account_id ON users(account_id);"))
            else:
                try:
                    await conn.execute(text("ALTER TABLE users ADD COLUMN account_id VARCHAR(32);"))
                except Exception:
                    pass
                try:
                    await conn.execute(text("ALTER TABLE users ADD COLUMN has_selected_language BOOLEAN DEFAULT 0;"))
                except Exception:
                    pass
        except Exception as e:
            log.warning(f"Schema migration warning: {e}")
