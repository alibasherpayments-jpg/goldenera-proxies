"""
Admin page routes — serve the HTML shell pages.
All protected routes redirect to /admin/login if not authenticated.
"""
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.dashboard.auth import get_current_admin
from app.dashboard.static.dashboard_html import DASHBOARD_HTML
from app.dashboard.static.users_html import USERS_HTML
from app.dashboard.static.transactions_html import TRANSACTIONS_HTML
from app.dashboard.static.deposits_html import DEPOSITS_HTML
from app.dashboard.static.proxies_html import PROXIES_HTML
from app.dashboard.static.settings_html import SETTINGS_HTML
from app.dashboard.static.broadcast_html import BROADCAST_HTML

router = APIRouter()


def _auth_guard(admin):
    """Used as a Depends — raises 401 which we catch and redirect."""
    return admin


@router.get("/admin", include_in_schema=False)
async def admin_root():
    return RedirectResponse(url="/admin/dashboard", status_code=302)


@router.get("/admin/dashboard", response_class=HTMLResponse)
async def dashboard_page(admin=Depends(get_current_admin)):
    return HTMLResponse(content=DASHBOARD_HTML.replace("{{ADMIN_USER}}", admin.get("sub", "admin")))


@router.get("/admin/users", response_class=HTMLResponse)
async def users_page(admin=Depends(get_current_admin)):
    return HTMLResponse(content=USERS_HTML.replace("{{ADMIN_USER}}", admin.get("sub", "admin")))


@router.get("/admin/transactions", response_class=HTMLResponse)
async def transactions_page(admin=Depends(get_current_admin)):
    return HTMLResponse(content=TRANSACTIONS_HTML.replace("{{ADMIN_USER}}", admin.get("sub", "admin")))


@router.get("/admin/deposits", response_class=HTMLResponse)
async def deposits_page(admin=Depends(get_current_admin)):
    return HTMLResponse(content=DEPOSITS_HTML.replace("{{ADMIN_USER}}", admin.get("sub", "admin")))


@router.get("/admin/proxies", response_class=HTMLResponse)
async def proxies_page(admin=Depends(get_current_admin)):
    return HTMLResponse(content=PROXIES_HTML.replace("{{ADMIN_USER}}", admin.get("sub", "admin")))


@router.get("/admin/settings", response_class=HTMLResponse)
async def settings_page(admin=Depends(get_current_admin)):
    return HTMLResponse(content=SETTINGS_HTML.replace("{{ADMIN_USER}}", admin.get("sub", "admin")))


@router.get("/admin/broadcast", response_class=HTMLResponse)
async def broadcast_page(admin=Depends(get_current_admin)):
    return HTMLResponse(content=BROADCAST_HTML.replace("{{ADMIN_USER}}", admin.get("sub", "admin")))
