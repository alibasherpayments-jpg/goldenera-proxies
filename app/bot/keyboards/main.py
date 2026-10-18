"""
Inline keyboard builders for GoldenEra 5G Proxies bot.
All labels come from the i18n t() function.
"""
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from app.bot.i18n import t, LANGUAGES


SUPPORT_URL = "https://t.me/BumBoyAliBasher"


REPLY_MENU_TEXTS = {
    "buy": {
        "ar": "🚀 شراء بروكسي 5G",
        "en": "🚀 Buy 5G Proxies",
        "ru": "🚀 Купить прокси",
        "hi": "🚀 प्रॉक्सी खरीदें",
    },
    "my_proxies": {
        "ar": "🔌 بروكسياتي النشطة",
        "en": "🔌 My Active Proxies",
        "ru": "🔌 Мои прокси",
        "hi": "🔌 मेरी प्रॉक्सी",
    },
    "deposit": {
        "ar": "💳 شحن الرصيد",
        "en": "💳 Deposit Funds",
        "ru": "💳 Пополнить баланс",
        "hi": "💳 फंड जमा करें",
    },
    "wallet": {
        "ar": "💼 المحفظة والحساب",
        "en": "💼 My Wallet",
        "ru": "💼 Мой кошелек",
        "hi": "💼 मेरा वॉलेट",
    },
    "support": {
        "ar": "💬 الدعم الفني",
        "en": "💬 Direct Support",
        "ru": "💬 Поддержка",
        "hi": "💬 सहायता",
    },
    "language": {
        "ar": "🌐 تغيير اللغة",
        "en": "🌐 Change Language",
        "ru": "🌐 Сменить язык",
        "hi": "🌐 भाषा बदलें",
    },
    "redeem": {
        "ar": "🎁 كود الهدية (Redeem)",
        "en": "🎁 Redeem Code",
        "ru": "🎁 Промокод",
        "hi": "🎁 प्रोमो कोड",
    },
}

ALL_BUY_TEXTS = set(REPLY_MENU_TEXTS["buy"].values()) | {"🚀 Buy 5G Proxies", "🚀 شراء بروكسي", "شراء بروكسي", "Buy 5G Proxies"}
ALL_MY_PROXIES_TEXTS = set(REPLY_MENU_TEXTS["my_proxies"].values()) | {"🔌 My Active Proxies", "🔌 بروكسياتي", "بروكسياتي", "My Active Proxies"}
ALL_DEPOSIT_TEXTS = set(REPLY_MENU_TEXTS["deposit"].values()) | {"💳 Deposit Funds", "💳 شحن الرصيد", "شحن الرصيد", "Deposit Funds"}
ALL_WALLET_TEXTS = set(REPLY_MENU_TEXTS["wallet"].values()) | {"💼 My Wallet", "💼 المحفظة والحساب", "💼 Wallet & Points", "💼 المحفظة والنقاط", "المحفظة", "Wallet & Points", "Wallet"}
ALL_SUPPORT_TEXTS = set(REPLY_MENU_TEXTS["support"].values()) | {"💬 Direct Support", "💬 الدعم الفني", "الدعم", "Direct Support"}
ALL_LANG_TEXTS = set(REPLY_MENU_TEXTS["language"].values()) | {"🌐 Change Language", "🌐 تغيير اللغة", "Language", "تغيير اللغة"}
ALL_REDEEM_TEXTS = set(REPLY_MENU_TEXTS["redeem"].values()) | {"🎁 Redeem Code", "🎁 كود الهدية", "كود الهدية", "Redeem Code", "Redeem"}


def reply_main_menu_kb(lang: str) -> ReplyKeyboardMarkup:
    """Bottom persistent menu buttons (native grid format replacing cards)."""
    lang_key = lang if lang in ("ar", "en", "ru", "hi") else "en"
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=REPLY_MENU_TEXTS["buy"][lang_key]),
                KeyboardButton(text=REPLY_MENU_TEXTS["my_proxies"][lang_key]),
            ],
            [
                KeyboardButton(text=REPLY_MENU_TEXTS["deposit"][lang_key]),
                KeyboardButton(text=REPLY_MENU_TEXTS["wallet"][lang_key]),
            ],
            [
                KeyboardButton(text=REPLY_MENU_TEXTS["redeem"][lang_key]),
                KeyboardButton(text=REPLY_MENU_TEXTS["language"][lang_key]),
            ],
            [
                KeyboardButton(text=REPLY_MENU_TEXTS["support"][lang_key]),
            ],
        ],
        resize_keyboard=True,
        is_persistent=True,
    )


def main_menu_kb(lang: str) -> InlineKeyboardMarkup:
    """Main menu with options arranged in a 2-column grid."""
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
                InlineKeyboardButton(text=t("menu_redeem", lang), callback_data="redeem:enter"),
                InlineKeyboardButton(text=t("menu_support", lang), url=SUPPORT_URL),
            ],
        ]
    )


def initial_language_kb() -> InlineKeyboardMarkup:
    """Language chooser presented when the user starts the bot for the first time."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇸🇦 العربية", callback_data="lang_init:ar"),
                InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_init:en"),
            ],
            [
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_init:ru"),
                InlineKeyboardButton(text="🇮🇳 हिन्दी", callback_data="lang_init:hi"),
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


def support_kb(lang: str) -> InlineKeyboardMarkup:
    """Support contact button + Back button."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💬 " + t("menu_support", lang),
                    url=SUPPORT_URL,
                )
            ],
            [
                InlineKeyboardButton(text=t("btn_back", lang), callback_data="menu:main")
            ],
        ]
    )


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
