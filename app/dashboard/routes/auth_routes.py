"""
Admin auth routes — login / logout pages and POST handler.
"""
from fastapi import APIRouter, Form, Response, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.dashboard.auth import authenticate_admin, create_access_token
from app.dashboard.static.login_html import LOGIN_HTML

router = APIRouter()


@router.get("/admin/login", response_class=HTMLResponse)
async def login_page():
    return HTMLResponse(content=LOGIN_HTML)


@router.post("/admin/login")
async def login_submit(
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
):
    if not authenticate_admin(username, password):
        return HTMLResponse(
            content=LOGIN_HTML.replace(
                "<!--ERROR_SLOT-->",
                '<div class="error-msg">Invalid username or password.</div>',
            ),
            status_code=401,
        )

    token = create_access_token({"sub": username})
    resp = RedirectResponse(url="/admin/dashboard", status_code=302)
    resp.set_cookie(
        key="admin_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 8,  # 8 hours
    )
    return resp


@router.get("/admin/logout")
async def logout():
    resp = RedirectResponse(url="/admin/login", status_code=302)
    resp.delete_cookie("admin_token")
    return resp
