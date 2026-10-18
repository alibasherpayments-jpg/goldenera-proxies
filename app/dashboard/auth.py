"""
JWT-based admin authentication for the GoldenEra Admin Dashboard.
"""
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Cookie
from fastapi.responses import RedirectResponse

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = settings.DASHBOARD_SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8  # 8 hours


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> dict:
    """Decode and verify a JWT token. Raises HTTPException on failure."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )


async def get_current_admin(
    admin_token: Optional[str] = Cookie(None, alias="admin_token"),
) -> dict:
    """FastAPI dependency — validates the admin JWT cookie."""
    if not admin_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    return verify_token(admin_token)


def get_admin_optional(admin_token: Optional[str]) -> Optional[dict]:
    """Helper for HTML page routes to safely verify JWT without throwing 401."""
    if not admin_token:
        return None
    try:
        return verify_token(admin_token)
    except Exception:
        return None


async def authenticate_admin(username: str, password: str) -> bool:
    """
    Secure constant-time credential check.
    Supports Neon DB SystemSetting table and config fallbacks.
    Immune to timing attacks.
    """
    expected_user = settings.DASHBOARD_USERNAME
    expected_pass = settings.DASHBOARD_PASSWORD

    try:
        from app.core.database import AsyncSessionLocal
        from app.models.order import SystemSetting
        async with AsyncSessionLocal() as session:
            u_row = await session.get(SystemSetting, "dashboard_username")
            p_row = await session.get(SystemSetting, "dashboard_password")
            if u_row and u_row.value and u_row.value.strip():
                expected_user = u_row.value.strip()
            if p_row and p_row.value and p_row.value.strip():
                expected_pass = p_row.value.strip()
    except Exception:
        pass

    user_match = secrets.compare_digest(username.strip(), expected_user.strip())
    pass_match = secrets.compare_digest(password.strip(), expected_pass.strip())
    return user_match and pass_match


def authenticate_admin_sync(username: str, password: str) -> bool:
    """Sync fallback check with constant-time comparison."""
    expected_user = settings.DASHBOARD_USERNAME
    expected_pass = settings.DASHBOARD_PASSWORD
    return secrets.compare_digest(username.strip(), expected_user.strip()) and secrets.compare_digest(password.strip(), expected_pass.strip())
