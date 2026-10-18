"""
Inline keyboard builders for GoldenEra 5G Proxies bot.
All labels come from the i18n t() function.
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.bot.i18n import t, LANGUAGES


def main_menu_kb(lang: str) -> InlineKeyboardMarkup:
    """Main menu with 6 options arranged in a 2-column grid."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t("menu_buy", lang), callback_data="menu:buy"),
                InlineKeyboardButton(text=t("menu_my_proxies", lang), callback_data="menu:my_proxies"),
            ],
            [
                InlineKeyboardButton(text=t("menu_deposit", lang), callback_data="deposit:main"),
                InlineKeyboardButton(text=t("menu_wallet", lang), callback_data="menu:wallet"),
            ],
            [
                InlineKeyboardButton(text=t("menu_support", lang), callback_data="menu:support"),
                InlineKeyboardButton(text=t("menu_language", lang), callback_data="menu:language"),
            ],
        ]
    )


def language_kb() -> InlineKeyboardMarkup:
    """Language selector — one button per supported language."""
    buttons = [
        InlineKeyboardButton(text=label, callback_data=f"lang:{code}")
        for code, label in LANGUAGES.items()
    ]
    # Two buttons per row
    rows = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def back_kb(lang: str) -> InlineKeyboardMarkup:
    """Single back button that navigates to main menu."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:main")]
        ]
    )


def deposit_methods_kb(lang: str) -> InlineKeyboardMarkup:
    """Deposit method chooser: Binance, Vodafone Cash, Back."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t("deposit_btn_binance", lang), callback_data="deposit:binance"
                )
            ],
            [
                InlineKeyboardButton(
                    text=t("deposit_btn_vodafone", lang), callback_data="deposit:vf"
                )
            ],
            [
                InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:main")
            ],
        ]
    )


def confirm_cancel_kb(lang: str, confirm_cb: str) -> InlineKeyboardMarkup:
    """Confirm + Cancel row."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t("btn_confirm", lang), callback_data=confirm_cb
                ),
                InlineKeyboardButton(
                    text=t("btn_cancel", lang), callback_data="menu:main"
                ),
            ]
        ]
    )


def proxy_card_kb(lang: str, request_id: str, category: str) -> InlineKeyboardMarkup:
    """
    Action keyboard for a proxy card.

    PRIME / HYPER  : Change Password | Change Location | Convert | Renew
    NEXUS          : Rotate IP | Change Password | Change Location | Change Protocol | Renew
    TITAN          : Renew only
    Always appends: Back → my_proxies
    """
    cat = category.lower()
    rows: list[list[InlineKeyboardButton]] = []

    if cat in ("prime", "hyper"):
        rows.append(
            [
                InlineKeyboardButton(
                    text=t("proxy_btn_change_pass", lang),
                    callback_data=f"proxy:change_pass:{request_id}",
                ),
                InlineKeyboardButton(
                    text=t("proxy_btn_change_location", lang),
                    callback_data=f"proxy:change_loc:{request_id}",
                ),
            ]
        )
        rows.append(
            [
                InlineKeyboardButton(
                    text=t("proxy_btn_convert", lang),
                    callback_data=f"proxy:convert:{request_id}",
                ),
                InlineKeyboardButton(
                    text=t("proxy_btn_renew", lang),
                    callback_data=f"proxy:renew:{request_id}",
                ),
            ]
        )
    elif cat == "nexus":
        rows.append(
            [
                InlineKeyboardButton(
                    text=t("proxy_btn_rotate_ip", lang),
                    callback_data=f"proxy:rotate_ip:{request_id}",
                ),
                InlineKeyboardButton(
                    text=t("proxy_btn_change_pass", lang),
                    callback_data=f"proxy:change_pass:{request_id}",
                ),
            ]
        )
        rows.append(
            [
                InlineKeyboardButton(
                    text=t("proxy_btn_change_location", lang),
                    callback_data=f"proxy:change_loc:{request_id}",
                ),
                InlineKeyboardButton(
                    text="🔄 Change Protocol",
                    callback_data=f"proxy:change_proto:{request_id}",
                ),
            ]
        )
        rows.append(
            [
                InlineKeyboardButton(
                    text=t("proxy_btn_renew", lang),
                    callback_data=f"proxy:renew:{request_id}",
                )
            ]
        )
    else:
        # TITAN — renew only
        rows.append(
            [
                InlineKeyboardButton(
                    text=t("proxy_btn_renew", lang),
                    callback_data=f"proxy:renew:{request_id}",
                )
            ]
        )

    # Always: Back to my proxies
    rows.append(
        [
            InlineKeyboardButton(
                text=t("btn_back", lang), callback_data="menu:my_proxies"
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)


def admin_deposit_approve_kb(deposit_id: int) -> InlineKeyboardMarkup:
    """Approve / Reject buttons sent to admins (always in Arabic)."""
    lang = "ar"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t("admin_btn_approve", lang),
                    callback_data=f"admin:approve:{deposit_id}",
                ),
                InlineKeyboardButton(
                    text=t("admin_btn_reject", lang),
                    callback_data=f"admin:reject:{deposit_id}",
                ),
            ]
        ]
    )
