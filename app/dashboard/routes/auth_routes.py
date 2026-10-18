"""
Admin auth routes — login / logout pages and POST handler.
"""
import asyncio
import time
from collections import defaultdict
from fastapi import APIRouter, Form, Response, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.core.config import settings
from app.dashboard.auth import authenticate_admin, create_access_token
from app.dashboard.static.login_html import LOGIN_HTML

router = APIRouter()

# ── Brute-force protection memory store ─────────────────────────────────────────
_FAILED_LOGINS = defaultdict(list)
_LOCKOUT_SECONDS = 900   # 15 minutes
_MAX_FAILURES = 5


def _is_ip_locked(ip: str) -> bool:
    now = time.time()
    valid_attempts = [t for t in _FAILED_LOGINS[ip] if now - t < _LOCKOUT_SECONDS]
    _FAILED_LOGINS[ip] = valid_attempts
    return len(valid_attempts) >= _MAX_FAILURES


def _record_failure(ip: str) -> None:
    _FAILED_LOGINS[ip].append(time.time())


def _clear_failures(ip: str) -> None:
    _FAILED_LOGINS.pop(ip, None)


@router.get("/admin/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return HTMLResponse(content=LOGIN_HTML)


@router.post("/admin/login")
async def login_submit(
    request: Request,
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
):
    client_ip = request.headers.get("x-forwarded-for") or (request.client.host if request.client else "unknown")
    if "," in client_ip:
        client_ip = client_ip.split(",")[0].strip()

    # 1. Check brute force lockout
    if _is_ip_locked(client_ip):
        return HTMLResponse(
            content=LOGIN_HTML.replace(
                "<!--ERROR_SLOT-->",
                '<div class="error-msg">⚠️ Too many failed attempts. Access locked for 15 minutes for security.</div>',
            ),
            status_code=429,
        )

    # 2. Check credentials asynchronously
    is_valid = await authenticate_admin(username, password)
    if not is_valid:
        _record_failure(client_ip)
        # Slow down brute-force bots
        await asyncio.sleep(1.0)
        return HTMLResponse(
            content=LOGIN_HTML.replace(
                "<!--ERROR_SLOT-->",
                '<div class="error-msg">❌ Invalid username or password.</div>',
            ),
            status_code=401,
        )

    # 3. Successful login: reset lockout counter
    _clear_failures(client_ip)
    token = create_access_token({"sub": username})
    resp = RedirectResponse(url="/admin/dashboard", status_code=302)
    resp.set_cookie(
        key="admin_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=settings.is_production,
        max_age=60 * 60 * 8,  # 8 hours
    )
    return resp


@router.get("/admin/logout")
async def logout():
    resp = RedirectResponse(url="/admin/login", status_code=302)
    resp.delete_cookie("admin_token")
    return resp
