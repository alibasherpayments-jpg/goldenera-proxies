"""
نظام الترجمة متعدد اللغات
Supported: ar (Arabic), en (English), ru (Russian), hi (Hindi)
"""
from typing import Dict, Any

LANGUAGES = {
    "ar": "🇸🇦 العربية",
    "en": "🇺🇸 English",
    "ru": "🇷🇺 Русский",
    "hi": "🇮🇳 हिन्दी",
}

_translations: Dict[str, Dict[str, str]] = {

    # ─────────────────────────────────────────
    #  COMMON / NAVIGATION
    # ─────────────────────────────────────────
    "btn_back": {
        "ar": "◀️ رجوع",
        "en": "◀️ Back",
        "ru": "◀️ Назад",
        "hi": "◀️ वापस",
    },
    "btn_close": {
        "ar": "✖️ إغلاق",
        "en": "✖️ Close",
        "ru": "✖️ Закрыть",
        "hi": "✖️ बंद करें",
    },
    "btn_cancel": {
        "ar": "❌ إلغاء",
        "en": "❌ Cancel",
        "ru": "❌ Отмена",
        "hi": "❌ रद्द करें",
    },
    "btn_confirm": {
        "ar": "✅ تأكيد",
        "en": "✅ Confirm",
        "ru": "✅ Подтвердить",
        "hi": "✅ पुष्टि करें",
    },
    "btn_refresh": {
        "ar": "🔄 تحديث",
        "en": "🔄 Refresh",
        "ru": "🔄 Обновить",
        "hi": "🔄 ताज़ा करें",
    },
    "loading": {
        "ar": "⏳ جاري التحميل...",
        "en": "⏳ Loading...",
        "ru": "⏳ Загрузка...",
        "hi": "⏳ लोड हो रहा है...",
    },
    "error_generic": {
        "ar": "⚠️ حدث خطأ غير متوقع. يرجى المحاولة مجدداً.",
        "en": "⚠️ An unexpected error occurred. Please try again.",
        "ru": "⚠️ Произошла непредвиденная ошибка. Попробуйте ещё раз.",
        "hi": "⚠️ एक अप्रत्याशित त्रुटि हुई। कृपया पुनः प्रयास करें।",
    },

    # ─────────────────────────────────────────
    #  LANGUAGE SELECTION
    # ─────────────────────────────────────────
    "lang_select_title": {
        "ar": "🌐 اختر لغتك المفضلة",
        "en": "🌐 Choose your preferred language",
        "ru": "🌐 Выберите предпочитаемый язык",
        "hi": "🌐 अपनी पसंदीदा भाषा चुनें",
    },
    "lang_changed": {
        "ar": "✅ تم تغيير اللغة إلى العربية.",
        "en": "✅ Language changed to English.",
        "ru": "✅ Язык изменён на русский.",
        "hi": "✅ भाषा हिन्दी में बदल दी गई।",
    },

    # ─────────────────────────────────────────
    #  START / WELCOME
    # ─────────────────────────────────────────
    "welcome_title": {
        "ar": "**✦ مرحباً بك في GoldenEra Proxies**",
        "en": "**✦ Welcome to GoldenEra Proxies**",
        "ru": "**✦ Добро пожаловать в GoldenEra Proxies**",
        "hi": "**✦ GoldenEra Proxies में आपका स्वागत है**",
    },
    "welcome_body": {
        "ar": (
            "أسرع وأموثق خدمة لبيع البروكسيات الاحترافية.\n\n"
            "📦 **PRIME & HYPER** — بروكسيات 5G دوارة وثابتة\n"
            "🌐 **NEXUS** — تحكم كامل وتدوير فوري\n"
            "🛡️ **TITAN** — ISP سكنية بأعلى جودة\n\n"
            "رصيدك الحالي: `{balance}$`"
        ),
        "en": (
            "The fastest and most trusted professional proxy service.\n\n"
            "📦 **PRIME & HYPER** — Rotating & Static 5G Proxies\n"
            "🌐 **NEXUS** — Full Control & Instant Rotation\n"
            "🛡️ **TITAN** — Premium Residential ISP Proxies\n\n"
            "Your balance: `{balance}$`"
        ),
        "ru": (
            "Самый быстрый и надёжный сервис профессиональных прокси.\n\n"
            "📦 **PRIME & HYPER** — Ротационные и статические 5G-прокси\n"
            "🌐 **NEXUS** — Полный контроль и мгновенная ротация\n"
            "🛡️ **TITAN** — Премиум резидентские ISP-прокси\n\n"
            "Ваш баланс: `{balance}$`"
        ),
        "hi": (
            "सबसे तेज़ और सबसे भरोसेमंद प्रोफेशनल प्रॉक्सी सेवा।\n\n"
            "📦 **PRIME & HYPER** — रोटेटिंग और स्टैटिक 5G प्रॉक्सी\n"
            "🌐 **NEXUS** — पूर्ण नियंत्रण और तुरंत रोटेशन\n"
            "🛡️ **TITAN** — प्रीमियम रेज़िडेंशियल ISP प्रॉक्सी\n\n"
            "आपका बैलेंस: `{balance}$`"
        ),
    },
    # ─────────────────────────────────────────
    #  MAIN MENU BUTTONS
    # ─────────────────────────────────────────
    "menu_buy": {
        "ar": "🛒 شراء بروكسي",
        "en": "🛒 Buy Proxy",
        "ru": "🛒 Купить прокси",
        "hi": "🛒 प्रॉक्सी खरीदें",
    },
    "menu_my_proxies": {
        "ar": "📦 بروكسياتي",
        "en": "📦 My Proxies",
        "ru": "📦 Мои прокси",
        "hi": "📦 मेरी प्रॉक्सी",
    },
    "menu_deposit": {
        "ar": "💳 شحن الرصيد",
        "en": "💳 Deposit",
        "ru": "💳 Пополнить баланс",
        "hi": "💳 बैलेंस जमा करें",
    },
    "menu_wallet": {
        "ar": "👛 محفظتي",
        "en": "👛 My Wallet",
        "ru": "👛 Мой кошелёк",
        "hi": "👛 मेरा वॉलेट",
    },
    "menu_support": {
        "ar": "🎧 الدعم الفني",
        "en": "🎧 Support",
        "ru": "🎧 Поддержка",
        "hi": "🎧 सहायता",
    },
    "menu_language": {
        "ar": "🌐 اللغة",
        "en": "🌐 Language",
        "ru": "🌐 Язык",
        "hi": "🌐 भाषा",
    },

    # ─────────────────────────────────────────
    #  WALLET
    # ─────────────────────────────────────────
    "wallet_title": {
        "ar": "👛 **محفظتي**",
        "en": "👛 **My Wallet**",
        "ru": "👛 **Мой кошелёк**",
        "hi": "👛 **मेरा वॉलेट**",
    },
    "wallet_body": {
        "ar": "💵 **الرصيد المتاح:** `{balance}$`\n🔒 **المحجوز:** `{reserved}$`\n📊 **إجمالي المدفوعات:** `{total_spent}$`",
        "en": "💵 **Available Balance:** `{balance}$`\n🔒 **Reserved:** `{reserved}$`\n📊 **Total Spent:** `{total_spent}$`",
        "ru": "💵 **Доступный баланс:** `{balance}$`\n🔒 **Зарезервировано:** `{reserved}$`\n📊 **Всего потрачено:** `{total_spent}$`",
        "hi": "💵 **उपलब्ध बैलेंस:** `{balance}$`\n🔒 **आरक्षित:** `{reserved}$`\n📊 **कुल खर्च:** `{total_spent}$`",
    },

    # ─────────────────────────────────────────
    #  DEPOSIT
    # ─────────────────────────────────────────
    "deposit_choose_method": {
        "ar": (
            "💳 *شحن الرصيد والمحفظة | Deposit Methods*\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "اختر وسيلة الدفع المناسبة لشحن حسابك فوراً:\n\n"
            "🟡 *Binance Pay (ID / USDT)*\n"
            "• شحن فوري وتلقائي 100%\n"
            "• `1$` دولار = `100` نقطة\n\n"
            "🔴 *Vodafone Cash (فودافون كاش)*\n"
            "• سعر الصرف الحالي: `1$ = {rate} ج.م`\n"
            "• تحويل بالجنيه المصري واعتماد فوري\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "👇 *اضغط على الطريقة التي تناسبك للمتابعة:*"
        ),
        "en": (
            "💳 *Deposit Funds | Payment Methods*\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "Select your preferred payment method to top up:\n\n"
            "🟡 *Binance Pay (ID / USDT)*\n"
            "• Instant 100% automated credit\n"
            "• `$1.00` USD = `100` points\n\n"
            "🔴 *Vodafone Cash*\n"
            "• Current exchange rate: `1$ = {rate} EGP`\n"
            "• Local Egyptian Pound transfer\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "👇 *Tap a payment method below to proceed:*"
        ),
        "ru": (
            "💳 *Пополнение баланса | Способы оплаты*\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "Выберите удобный способ пополнения кошелька:\n\n"
            "🟡 *Binance Pay (ID / USDT)*\n"
            "• Мгновенное автозачисление 100%\n"
            "• `$1.00` USD = `100` баллов\n\n"
            "🔴 *Vodafone Cash*\n"
            "• Текущий курс: `1$ = {rate} EGP`\n"
            "• Оплата в местной валюте (EGP)\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "👇 *Выберите способ оплаты ниже:*"
        ),
        "hi": (
            "💳 *फंड जमा करें | भुगतान के तरीके*\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "वॉलेट रिचार्ज करने के लिए अपना पसंदीदा तरीका चुनें:\n\n"
            "🟡 *Binance Pay (ID / USDT)*\n"
            "• 100% तुरंत और स्वचालित क्रेडिट\n"
            "• `$1.00` USD = `100` पॉइंट्स\n\n"
            "🔴 *Vodafone Cash*\n"
            "• वर्तमान विनिमय दर: `1$ = {rate} EGP`\n"
            "• स्थानीय मुद्रा (EGP) में भुगतान\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "👇 *आगे बढ़ने के लिए नीचे एक तरीका चुनें:*"
        ),
    },
    "deposit_select_method": {
        "ar": (
            "💳 *شحن الرصيد والمحفظة | Deposit Methods*\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "اختر وسيلة الدفع المناسبة لشحن حسابك فوراً:\n\n"
            "🟡 *Binance Pay (ID / USDT)*\n"
            "• شحن فوري وتلقائي 100%\n"
            "• `1$` دولار = `100` نقطة\n\n"
            "🔴 *Vodafone Cash (فودافون كاش)*\n"
            "• سعر الصرف الحالي: `1$ = {rate} ج.م`\n"
            "• تحويل بالجنيه المصري واعتماد فوري\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "👇 *اضغط على الطريقة التي تناسبك للمتابعة:*"
        ),
        "en": (
            "💳 *Deposit Funds | Payment Methods*\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "Select your preferred payment method to top up:\n\n"
            "🟡 *Binance Pay (ID / USDT)*\n"
            "• Instant 100% automated credit\n"
            "• `$1.00` USD = `100` points\n\n"
            "🔴 *Vodafone Cash*\n"
            "• Current exchange rate: `1$ = {rate} EGP`\n"
            "• Local Egyptian Pound transfer\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "👇 *Tap a payment method below to proceed:*"
        ),
        "ru": (
            "💳 *Пополнение баланса | Способы оплаты*\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "Выберите удобный способ пополнения кошелька:\n\n"
            "🟡 *Binance Pay (ID / USDT)*\n"
            "• Мгновенное автозачисление 100%\n"
            "• `$1.00` USD = `100` баллов\n\n"
            "🔴 *Vodafone Cash*\n"
            "• Текущий курс: `1$ = {rate} EGP`\n"
            "• Оплата в местной валюте (EGP)\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "👇 *Выберите способ оплаты ниже:*"
        ),
        "hi": (
            "💳 *फंड जमा करें | भुगतान के तरीके*\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "वॉलेट रिचार्ज करने के लिए अपना पसंदीदा तरीका चुनें:\n\n"
            "🟡 *Binance Pay (ID / USDT)*\n"
            "• 100% तुरंत और स्वचालित क्रेडिट\n"
            "• `$1.00` USD = `100` पॉइंट्स\n\n"
            "🔴 *Vodafone Cash*\n"
            "• वर्तमान विनिमय दर: `1$ = {rate} EGP`\n"
            "• स्थानीय मुद्रा (EGP) में भुगतान\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "👇 *आगे बढ़ने के लिए नीचे एक तरीका चुनें:*"
        ),
    },
    "deposit_btn_binance": {
        "ar": "🟡 Binance Pay (فوري تلقائي)",
        "en": "🟡 Binance Pay (Instant Auto)",
        "ru": "🟡 Binance Pay (Мгновенно)",
        "hi": "🟡 Binance Pay (तुरंत क्रेडिट)",
    },
    "deposit_btn_vodafone": {
        "ar": "🔴 Vodafone Cash (فودافون كاش)",
        "en": "🔴 Vodafone Cash (EGP)",
        "ru": "🔴 Vodafone Cash (EGP)",
        "hi": "🔴 Vodafone Cash (EGP)",
    },
    "deposit_binance_instructions": {
        "ar": (
            "🟡 أرسل عبر Binance Pay على هذا الـ ID:\n"
            "`{binance_id}`\n"
            "(اضغط لنسخ الـ ID)\n\n"
            "وبعد التحويل أرسل الـ TXID هنا 👇"
        ),
        "en": (
            "🟡 Send via Binance Pay to this ID:\n"
            "`{binance_id}`\n"
            "(Tap to copy ID)\n\n"
            "After transfer, send your TXID here 👇"
        ),
        "ru": (
            "🟡 Отправьте через Binance Pay на этот ID:\n"
            "`{binance_id}`\n"
            "(Нажмите для копирования ID)\n\n"
            "После перевода отправьте ваш TXID сюда 👇"
        ),
        "hi": (
            "🟡 इस ID पर Binance Pay के माध्यम से भेजें:\n"
            "`{binance_id}`\n"
            "(ID कॉपी करने के लिए टैप करें)\n\n"
            "ट्रांसफर के बाद, अपना TXID यहाँ भेजें 👇"
        ),
    },
    "deposit_enter_txid": {
        "ar": "✏️ أرسل الآن رقم المعاملة (Order ID / TXID):",
        "en": "✏️ Send your Order ID / Transaction ID (TXID) now:",
        "ru": "✏️ Отправьте номер транзакции (Order ID / TXID) сейчас:",
        "hi": "✏️ अपना Order ID / Transaction ID (TXID) अभी भेजें:",
    },
    "deposit_enter_amount_usd": {
        "ar": "💵 يرجى إدخال المبلغ الذي قمت بتحويله بالدولار (USDT $):\n(مثال: `10` أو `25.5`)",
        "en": "💵 Please enter the amount transferred in USD (USDT $):\n(e.g., `10` or `25.5`)",
        "ru": "💵 Введите переведенную сумму в USD (USDT $):\n(например: `10` или `25.5`)",
        "hi": "💵 कृपया USD में ट्रांसफर की गई राशि दर्ज करें (USDT $):\n(उदा: `10` या `25.5`)",
    },
    "deposit_txid_used": {
        "ar": "❌ هذا الـ TxID مستخدم مسبقاً. يرجى التحقق من المعرف.",
        "en": "❌ This TxID has already been used. Please check your transaction ID.",
        "ru": "❌ Этот TxID уже использован. Проверьте идентификатор транзакции.",
        "hi": "❌ यह TxID पहले से उपयोग किया जा चुका है। कृपया अपना Transaction ID जाँचें।",
    },
    "deposit_txid_verifying": {
        "ar": "🔍 جاري التحقق من عملية Binance Pay...",
        "en": "🔍 Verifying Binance Pay transaction...",
        "ru": "🔍 Проверка транзакции Binance Pay...",
        "hi": "🔍 Binance Pay लेनदेन सत्यापित हो रहा है...",
    },
    "deposit_binance_success": {
        "ar": (
            "✅ **تم شحن النقاط بنجاح!**\n\n"
            "💵 المبلغ المستلم: `${amount}`\n"
            "🎯 النقاط المضافة: `+{points}` نقطة\n"
            "💎 رصيد محفظتك الحالي: `{points_total}` نقطة (${balance})\n\n"
            "شكراً لك! يمكنك الآن شراء البروكسيات مباشرة 🚀"
        ),
        "en": (
            "✅ **Points credited successfully!**\n\n"
            "💵 Received Amount: `${amount}`\n"
            "🎯 Points Added: `+{points}` pts\n"
            "💎 Current Balance: `{points_total}` pts (${balance})\n\n"
            "Thank you! You can now purchase proxies immediately 🚀"
        ),
        "ru": (
            "✅ **Баллы успешно начислены!**\n\n"
            "💵 Получено: `${amount}`\n"
            "🎯 Начислено: `+{points}` баллов\n"
            "💎 Ваш баланс: `{points_total}` баллов (${balance})\n\n"
            "Спасибо! Теперь вы можете покупать прокси 🚀"
        ),
        "hi": (
            "✅ **पॉइंट्स सफलतापूर्वक जोड़ दिए गए!**\n\n"
            "💵 प्राप्त राशि: `${amount}`\n"
            "🎯 जोड़े गए पॉइंट्स: `+{points}`\n"
            "💎 वर्तमान बैलेंस: `{points_total}` पॉइंट्स (${balance})\n\n"
            "धन्यवाद! अब आप प्रॉक्सी खरीद सकते हैं 🚀"
        ),
    },
    "deposit_binance_pending": {
        "ar": (
            "✅ **تم استلام بيانات الإيداع بنجاح!**\n\n"
            "📋 رقم المعاملة: `{txid}`\n"
            "💵 المبلغ: `${amount}` (`{points}` نقطة)\n\n"
            "⏳ جاري مراجعة التحويل واعتماد النقاط فوراً في حسابك."
        ),
        "en": (
            "✅ **Deposit submitted successfully!**\n\n"
            "📋 TXID / Order ID: `{txid}`\n"
            "💵 Amount: `${amount}` (`{points}` pts)\n\n"
            "⏳ Your transaction is under review and points will be credited shortly."
        ),
        "ru": (
            "✅ **Заявка на пополнение принята!**\n\n"
            "📋 TXID / Order ID: `{txid}`\n"
            "💵 Сумма: `${amount}` (`{points}` баллов)\n\n"
            "⏳ Транзакция проверяется и баллы будут начислены в ближайшее время."
        ),
        "hi": (
            "✅ **जमा विवरण सफलतापूर्वक प्राप्त हुआ!**\n\n"
            "📋 TXID / Order ID: `{txid}`\n"
            "💵 राशि: `${amount}` (`{points}` पॉइंट्स)\n\n"
            "⏳ लेनदेन की समीक्षा की जा रही है और जल्द ही पॉइंट्स जोड़ दिए जाएंगे।"
        ),
    },
    "deposit_binance_not_found": {
        "ar": "⏳ لم يتم العثور على العملية في حساب Binance بعد.\n\nيرجى التأكد من إدخال **رقم العملية أو رقم الطلب (TXID / Order ID)** الموضح في إيصال Binance Pay، أو انتظر لحظات وأعد المحاولة.",
        "en": "⏳ Transaction not found on Binance yet.\n\nPlease verify your **TXID / Order ID** from your Binance Pay receipt, or wait a minute and try again.",
        "ru": "⏳ Транзакция пока не найдена в Binance.\n\nПожалуйста, проверьте **TXID / Order ID** в чеке Binance Pay или подождите минуту и попробуйте снова.",
        "hi": "⏳ Binance पर लेनदेन अभी तक नहीं मिला।\n\nकृपया अपनी रसीद से **TXID / Order ID** की जाँच करें या एक मिनट प्रतीक्षा करें और पुनः प्रयास करें।",
    },
    "deposit_vodafone_instructions": {
        "ar": (
            "🔴 **الإيداع عبر Vodafone Cash**\n\n"
            "1️⃣ حوّل المبلغ إلى رقم الكاش التالي:\n"
            "`{vodafone_number}`\n"
            "_(اضغط على الرقم لنسخه فوراً)_\n\n"
            "💱 سعر الصرف: `1$ = {rate} ج.م`\n\n"
            "2️⃣ بعد إتمام التحويل، أرسل **رقم عملية التحويل (Transaction ID)** هنا 👇"
        ),
        "en": (
            "🔴 **Deposit via Vodafone Cash**\n\n"
            "1️⃣ Send the transfer to:\n"
            "`{vodafone_number}`\n"
            "_(Tap number to copy)_\n\n"
            "💱 Current rate: `1$ = {rate} EGP`\n\n"
            "2️⃣ After payment, send your **Transaction ID** here 👇"
        ),
        "ru": (
            "🔴 **Пополнение через Vodafone Cash**\n\n"
            "1️⃣ Переведите сумму на номер:\n"
            "`{vodafone_number}`\n"
            "_(Нажмите для копирования)_\n\n"
            "💱 Курс обмена: `1$ = {rate} EGP`\n\n"
            "2️⃣ После перевода отправьте **Transaction ID** сюда 👇"
        ),
        "hi": (
            "🔴 **Vodafone Cash के माध्यम से जमा करें**\n\n"
            "1️⃣ इस नंबर पर राशि भेजें:\n"
            "`{vodafone_number}`\n"
            "_(कॉपी करने के लिए टैप करें)_\n\n"
            "💱 विनिमय दर: `1$ = {rate} EGP`\n\n"
            "2️⃣ ट्रांसफर के बाद, अपना **Transaction ID** यहाँ भेजें 👇"
        ),
    },
    "deposit_vf_enter_phone": {
        "ar": "📱 أدخل رقم هاتفك المحوّل منه:",
        "en": "📱 Enter your sender phone number:",
        "ru": "📱 Введите номер телефона отправителя:",
        "hi": "📱 अपना भेजने वाला फ़ोन नंबर दर्ज करें:",
    },
    "deposit_vf_enter_txid": {
        "ar": "🔢 أرسل الآن رقم عملية التحويل (Transaction ID):",
        "en": "🔢 Send your Transaction ID now:",
        "ru": "🔢 Отправьте Transaction ID сейчас:",
        "hi": "🔢 अपना Transaction ID अभी भेजें:",
    },
    "deposit_vf_enter_amount": {
        "ar": "💵 يرجى إدخال المبلغ الذي قمت بتحويله بالدولار (USDT $):\n(مثال: `10` أو `25.5`)",
        "en": "💵 Please enter the amount transferred in USD (USDT $):\n(e.g., `10` or `25.5`)",
        "ru": "💵 Введите сумму перевода в USD (USDT $):\n(например: `10` или `25.5`)",
        "hi": "💵 कृपया ट्रांसफर की गई राशि USD में दर्ज करें (USDT $):\n(उदा: `10` या `25.5`)",
    },
    "deposit_vf_pending": {
        "ar": (
            "✅ **تم استلام بيانات الإيداع بنجاح!**\n\n"
            "📋 رقم العملية: `{txid}`\n"
            "💵 المبلغ: `${amount}` (`{amount_egp}` ج.م)\n"
            "🎯 النقاط المستحقة: `+{points}` نقطة\n\n"
            "⏳ طلبك قيد المراجعة وسيتم إضافة النقاط لمحفظتك فور موافقة الإدارة."
        ),
        "en": (
            "✅ **Deposit request received successfully!**\n\n"
            "📋 Transaction ID: `{txid}`\n"
            "💵 Amount: `${amount}` (`{amount_egp}` EGP)\n"
            "🎯 Points to receive: `+{points}` pts\n\n"
            "⏳ Your request is under review and points will be credited shortly."
        ),
        "ru": (
            "✅ **Заявка на пополнение принята!**\n\n"
            "📋 Transaction ID: `{txid}`\n"
            "💵 Сумма: `${amount}` (`{amount_egp}` EGP)\n"
            "🎯 Будет начислено: `+{points}` баллов\n\n"
            "⏳ Заявка проверяется и баллы будут начислены в ближайшее время."
        ),
        "hi": (
            "✅ **जमा अनुरोध सफलतापूर्वक प्राप्त हुआ!**\n\n"
            "📋 Transaction ID: `{txid}`\n"
            "💵 राशि: `${amount}` (`{amount_egp}` EGP)\n"
            "🎯 पॉइंट्स: `+{points}`\n\n"
            "⏳ समीक्षा के बाद जल्द ही पॉइंट्स जोड़ दिए जाएंगे।"
        ),
    },
    "deposit_vf_approved": {
        "ar": "🎉 **تم قبول إيداعك!**\n\n💵 المبلغ المضاف: `{amount}$`\n💼 رصيدك الآن: `{balance}$`",
        "en": "🎉 **Your deposit has been approved!**\n\n💵 Amount added: `{amount}$`\n💼 Your balance: `{balance}$`",
        "ru": "🎉 **Ваш депозит одобрен!**\n\n💵 Добавлена сумма: `{amount}$`\n💼 Ваш баланс: `{balance}$`",
        "hi": "🎉 **आपकी जमा राशि स्वीकृत हो गई!**\n\n💵 जोड़ी गई राशि: `{amount}$`\n💼 आपका बैलेंस: `{balance}$`",
    },
    "deposit_vf_rejected": {
        "ar": "❌ **تم رفض طلب الإيداع.**\n\nإذا كنت تعتقد أن هذا خطأ، تواصل مع الدعم الفني.",
        "en": "❌ **Your deposit was rejected.**\n\nIf you believe this is an error, contact support.",
        "ru": "❌ **Ваш депозит отклонён.**\n\nЕсли вы считаете, что это ошибка, свяжитесь с поддержкой.",
        "hi": "❌ **आपकी जमा राशि अस्वीकार कर दी गई।**\n\nयदि आपको लगता है यह गलती है, तो सहायता से संपर्क करें।",
    },

    # ─────────────────────────────────────────
    #  CATALOG / BUY
    # ─────────────────────────────────────────
    "catalog_choose_category": {
        "ar": "📦 **اختر فئة البروكسي**",
        "en": "📦 **Choose Proxy Category**",
        "ru": "📦 **Выберите категорию прокси**",
        "hi": "📦 **प्रॉक्सी श्रेणी चुनें**",
    },
    "catalog_prime_hyper": {
        "ar": "⚡ PRIME & HYPER — 5G دوار / ثابت",
        "en": "⚡ PRIME & HYPER — 5G Rotate / Inject",
        "ru": "⚡ PRIME & HYPER — 5G Ротация / Статик",
        "hi": "⚡ PRIME & HYPER — 5G रोटेट / इंजेक्ट",
    },
    "catalog_nexus": {
        "ar": "🌐 NEXUS — تحكم كامل وتدوير فوري",
        "en": "🌐 NEXUS — Full Control & Instant Rotation",
        "ru": "🌐 NEXUS — Полный контроль и ротация",
        "hi": "🌐 NEXUS — पूर्ण नियंत्रण और तुरंत रोटेशन",
    },
    "catalog_titan": {
        "ar": "🛡️ TITAN — ISP سكنية عالية الجودة",
        "en": "🛡️ TITAN — Premium Residential ISP",
        "ru": "🛡️ TITAN — Премиум резидентский ISP",
        "hi": "🛡️ TITAN — प्रीमियम रेज़िडेंशियल ISP",
    },
    "catalog_choose_server": {
        "ar": "🌍 **اختر الموقع / السيرفر**",
        "en": "🌍 **Choose Location / Server**",
        "ru": "🌍 **Выберите локацию / сервер**",
        "hi": "🌍 **स्थान / सर्वर चुनें**",
    },
    "catalog_server_full": {
        "ar": "⛔ ممتلئ",
        "en": "⛔ Full",
        "ru": "⛔ Полный",
        "hi": "⛔ भरा हुआ",
    },
    "catalog_choose_mode": {
        "ar": "⚙️ **اختر نمط الاستخدام**",
        "en": "⚙️ **Choose Usage Mode**",
        "ru": "⚙️ **Выберите режим использования**",
        "hi": "⚙️ **उपयोग का तरीका चुनें**",
    },
    "catalog_mode_rotate": {
        "ar": "🔄 Rotate — دوار (يوزر + باسورد)",
        "en": "🔄 Rotate — Rotating (username + password)",
        "ru": "🔄 Rotate — Ротация (логин + пароль)",
        "hi": "🔄 Rotate — रोटेटिंग (यूज़रनेम + पासवर्ड)",
    },
    "catalog_mode_inject": {
        "ar": "💉 Inject — IP مصرّح (قائمة IPs)",
        "en": "💉 Inject — IP Whitelist (allowed IPs)",
        "ru": "💉 Inject — Белый список IP",
        "hi": "💉 Inject — IP व्हाइटलिस्ट (अनुमत IPs)",
    },
    "catalog_choose_duration": {
        "ar": "⏱️ **اختر مدة الاشتراك**",
        "en": "⏱️ **Choose Subscription Duration**",
        "ru": "⏱️ **Выберите длительность подписки**",
        "hi": "⏱️ **सदस्यता अवधि चुनें**",
    },
    "catalog_enter_username": {
        "ar": "👤 أدخل اسم المستخدم (username) للبروكسي:\n_(استخدم أحرف إنجليزية وأرقام فقط)_",
        "en": "👤 Enter the proxy username:\n_(Use English letters and numbers only)_",
        "ru": "👤 Введите имя пользователя прокси:\n_(Используйте только латинские буквы и цифры)_",
        "hi": "👤 प्रॉक्सी username दर्ज करें:\n_(केवल अंग्रेज़ी अक्षर और संख्याएँ उपयोग करें)_",
    },
    "catalog_enter_password": {
        "ar": "🔑 أدخل كلمة المرور للبروكسي:\n_(8 أحرف على الأقل، تحتوي على أرقام وحروف)_",
        "en": "🔑 Enter the proxy password:\n_(At least 8 chars with letters and numbers)_",
        "ru": "🔑 Введите пароль для прокси:\n_(Минимум 8 символов, буквы и цифры)_",
        "hi": "🔑 प्रॉक्सी पासवर्ड दर्ज करें:\n_(कम से कम 8 वर्ण, अक्षर और संख्याएँ)_",
    },
    "catalog_enter_allowed_ip": {
        "ar": "🌐 أدخل عنوان IP المصرّح له (IPv4):\n_(مثال: 203.0.113.10)_",
        "en": "🌐 Enter the allowed IP address (IPv4):\n_(Example: 203.0.113.10)_",
        "ru": "🌐 Введите разрешённый IP-адрес (IPv4):\n_(Пример: 203.0.113.10)_",
        "hi": "🌐 अनुमत IP पता दर्ज करें (IPv4):\n_(उदाहरण: 203.0.113.10)_",
    },
    "catalog_order_summary": {
        "ar": (
            "📋 **ملخص الطلب**\n\n"
            "• الفئة: `{category}`\n"
            "• النمط: `{mode}`\n"
            "• الموقع: `{location}`\n"
            "• المدة: `{duration}`\n"
            "• السعر: `{price}$`\n\n"
            "💼 رصيدك الحالي: `{balance}$`\n\n"
            "هل تريد تأكيد الشراء؟"
        ),
        "en": (
            "📋 **Order Summary**\n\n"
            "• Category: `{category}`\n"
            "• Mode: `{mode}`\n"
            "• Location: `{location}`\n"
            "• Duration: `{duration}`\n"
            "• Price: `{price}$`\n\n"
            "💼 Your balance: `{balance}$`\n\n"
            "Confirm your purchase?"
        ),
        "ru": (
            "📋 **Сводка заказа**\n\n"
            "• Категория: `{category}`\n"
            "• Режим: `{mode}`\n"
            "• Локация: `{location}`\n"
            "• Длительность: `{duration}`\n"
            "• Цена: `{price}$`\n\n"
            "💼 Ваш баланс: `{balance}$`\n\n"
            "Подтвердить покупку?"
        ),
        "hi": (
            "📋 **ऑर्डर सारांश**\n\n"
            "• श्रेणी: `{category}`\n"
            "• मोड: `{mode}`\n"
            "• स्थान: `{location}`\n"
            "• अवधि: `{duration}`\n"
            "• मूल्य: `{price}$`\n\n"
            "💼 आपका बैलेंस: `{balance}$`\n\n"
            "क्या आप खरीदारी की पुष्टि करते हैं?"
        ),
    },
    "catalog_insufficient_balance": {
        "ar": "❌ **رصيد غير كافٍ!**\n\nتحتاج `{needed}$` لإتمام هذه العملية.\nرصيدك الحالي: `{balance}$`\n\nاشحن رصيدك الآن!",
        "en": "❌ **Insufficient Balance!**\n\nYou need `{needed}$` to complete this order.\nYour balance: `{balance}$`\n\nTop up now!",
        "ru": "❌ **Недостаточно средств!**\n\nНужно `{needed}$` для завершения заказа.\nВаш баланс: `{balance}$`\n\nПополните баланс!",
        "hi": "❌ **अपर्याप्त बैलेंस!**\n\nइस ऑर्डर को पूरा करने के लिए `{needed}$` चाहिए।\nआपका बैलेंस: `{balance}$`\n\nअभी टॉप अप करें!",
    },
    "catalog_order_placed": {
        "ar": "✅ **تم إرسال طلبك!**\n\n⏳ جاري إنشاء البروكسي، سيصلك تلقائياً خلال لحظات...",
        "en": "✅ **Order placed!**\n\n⏳ Creating your proxy, you'll receive it automatically in moments...",
        "ru": "✅ **Заказ оформлен!**\n\n⏳ Создаём прокси, вы получите его автоматически через несколько секунд...",
        "hi": "✅ **ऑर्डर दे दिया गया!**\n\n⏳ आपकी प्रॉक्सी बनाई जा रही है, आपको कुछ ही समय में प्राप्त होगी...",
    },

    # ─────────────────────────────────────────
    #  PROXY CARD
    # ─────────────────────────────────────────
    "proxy_card_title": {
        "ar": "🟢 **بروكسي جاهز للاستخدام**",
        "en": "🟢 **Proxy Ready to Use**",
        "ru": "🟢 **Прокси готов к использованию**",
        "hi": "🟢 **प्रॉक्सी उपयोग के लिए तैयार**",
    },
    "proxy_card_body": {
        "ar": (
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📦 **{category}** — `{mode}`\n"
            "🌍 {flag} `{location}`\n"
            "🔄 {rotation_label}\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🖥️ **Host:** `{host}`\n"
            "🔌 **HTTP Port:** `{http_port}`\n"
            "🔌 **SOCKS5 Port:** `{socks5_port}`\n"
            "👤 **Username:** `{username}`\n"
            "🔑 **Password:** `{password}`\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📅 ينتهي: `{expiry}`\n"
            "🔗 `{url}`"
        ),
        "en": (
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📦 **{category}** — `{mode}`\n"
            "🌍 {flag} `{location}`\n"
            "🔄 {rotation_label}\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🖥️ **Host:** `{host}`\n"
            "🔌 **HTTP Port:** `{http_port}`\n"
            "🔌 **SOCKS5 Port:** `{socks5_port}`\n"
            "👤 **Username:** `{username}`\n"
            "🔑 **Password:** `{password}`\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📅 Expires: `{expiry}`\n"
            "🔗 `{url}`"
        ),
        "ru": (
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📦 **{category}** — `{mode}`\n"
            "🌍 {flag} `{location}`\n"
            "🔄 {rotation_label}\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🖥️ **Хост:** `{host}`\n"
            "🔌 **HTTP порт:** `{http_port}`\n"
            "🔌 **SOCKS5 порт:** `{socks5_port}`\n"
            "👤 **Логин:** `{username}`\n"
            "🔑 **Пароль:** `{password}`\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📅 Истекает: `{expiry}`\n"
            "🔗 `{url}`"
        ),
        "hi": (
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📦 **{category}** — `{mode}`\n"
            "🌍 {flag} `{location}`\n"
            "🔄 {rotation_label}\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🖥️ **होस्ट:** `{host}`\n"
            "🔌 **HTTP पोर्ट:** `{http_port}`\n"
            "🔌 **SOCKS5 पोर्ट:** `{socks5_port}`\n"
            "👤 **यूज़रनेम:** `{username}`\n"
            "🔑 **पासवर्ड:** `{password}`\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📅 समाप्ति: `{expiry}`\n"
            "🔗 `{url}`"
        ),
    },
    "proxy_btn_rotate_ip": {
        "ar": "🔄 تدوير الـ IP",
        "en": "🔄 Rotate IP",
        "ru": "🔄 Сменить IP",
        "hi": "🔄 IP बदलें",
    },
    "proxy_btn_change_pass": {
        "ar": "🔑 تغيير الباسورد",
        "en": "🔑 Change Password",
        "ru": "🔑 Сменить пароль",
        "hi": "🔑 पासवर्ड बदलें",
    },
    "proxy_btn_change_location": {
        "ar": "🌍 تغيير الموقع",
        "en": "🌍 Change Location",
        "ru": "🌍 Сменить локацию",
        "hi": "🌍 स्थान बदलें",
    },
    "proxy_btn_convert": {
        "ar": "🔀 التحويل Rotate / Inject",
        "en": "🔀 Convert Rotate / Inject",
        "ru": "🔀 Конвертировать Rotate / Inject",
        "hi": "🔀 Rotate / Inject रूपांतरित करें",
    },
    "proxy_btn_renew": {
        "ar": "♻️ تجديد",
        "en": "♻️ Renew",
        "ru": "♻️ Обновить",
        "hi": "♻️ नवीनीकरण करें",
    },
    "proxy_btn_copy_url": {
        "ar": "📋 نسخ الـ URL",
        "en": "📋 Copy URL",
        "ru": "📋 Копировать URL",
        "hi": "📋 URL कॉपी करें",
    },
    "proxy_action_success": {
        "ar": "✅ تم تنفيذ الإجراء بنجاح!",
        "en": "✅ Action completed successfully!",
        "ru": "✅ Действие выполнено успешно!",
        "hi": "✅ कार्रवाई सफलतापूर्वक पूरी हुई!",
    },
    "proxy_action_processing": {
        "ar": "⏳ جاري تنفيذ الإجراء...",
        "en": "⏳ Processing action...",
        "ru": "⏳ Выполняется...",
        "hi": "⏳ कार्रवाई हो रही है...",
    },
    "proxy_enter_new_password": {
        "ar": "🔑 أدخل كلمة المرور الجديدة:",
        "en": "🔑 Enter the new password:",
        "ru": "🔑 Введите новый пароль:",
        "hi": "🔑 नया पासवर्ड दर्ज करें:",
    },

    # ─────────────────────────────────────────
    #  MY PROXIES LIST
    # ─────────────────────────────────────────
    "my_proxies_title": {
        "ar": "📦 **بروكسياتي النشطة**",
        "en": "📦 **My Active Proxies**",
        "ru": "📦 **Мои активные прокси**",
        "hi": "📦 **मेरी सक्रिय प्रॉक्सी**",
    },
    "my_proxies_empty": {
        "ar": "📭 ليس لديك أي بروكسيات نشطة حالياً.\n\nاشتر بروكسيك الأول الآن!",
        "en": "📭 You have no active proxies yet.\n\nBuy your first proxy now!",
        "ru": "📭 У вас пока нет активных прокси.\n\nКупите свой первый прокси!",
        "hi": "📭 अभी आपके पास कोई सक्रिय प्रॉक्सी नहीं है।\n\nअभी अपनी पहली प्रॉक्सी खरीदें!",
    },
    "proxy_expires_soon": {
        "ar": "⚠️ **تنبيه انتهاء صلاحية!**\n\nبروكسيك في `{location}` سينتهي خلال `{hours}` ساعة.\n\nجدد الآن لضمان الاستمرارية!",
        "en": "⚠️ **Expiry Alert!**\n\nYour `{location}` proxy expires in `{hours}` hours.\n\nRenew now to stay connected!",
        "ru": "⚠️ **Предупреждение об истечении!**\n\nВаш прокси `{location}` истекает через `{hours}` часов.\n\nОбновите сейчас!",
        "hi": "⚠️ **समाप्ति चेतावनी!**\n\nआपकी `{location}` प्रॉक्सी `{hours}` घंटे में समाप्त हो जाएगी।\n\nअभी नवीनीकरण करें!",
    },

    # ─────────────────────────────────────────
    #  ADMIN NOTIFICATIONS (sent to admin chat)
    # ─────────────────────────────────────────
    "admin_vf_deposit_notify": {
        "ar": (
            "💰 **طلب إيداع جديد — Vodafone Cash**\n\n"
            "👤 العميل: [{name}](tg://user?id={user_id}) — `{user_id}`\n"
            "🔢 Transaction ID: `{txid}`\n"
            "💵 المبلغ: `{amount_egp} ج.م` = `{amount_usd}$`\n"
            "🕐 الوقت: `{time}`\n\n"
            "هل تقبل هذا الإيداع؟"
        ),
        "en": (
            "💰 **New Deposit Request — Vodafone Cash**\n\n"
            "👤 User: [{name}](tg://user?id={user_id}) — `{user_id}`\n"
            "🔢 Transaction ID: `{txid}`\n"
            "💵 Amount: `{amount_egp} EGP` = `{amount_usd}$`\n"
            "🕐 Time: `{time}`\n\n"
            "Do you approve this deposit?"
        ),
    },
    "admin_btn_approve": {
        "ar": "✅ قبول وشحن الرصيد",
        "en": "✅ Approve & Credit",
        "ru": "✅ Одобрить и зачислить",
        "hi": "✅ स्वीकृत करें और जमा करें",
    },
    "admin_btn_reject": {
        "ar": "❌ رفض الإيداع",
        "en": "❌ Reject Deposit",
        "ru": "❌ Отклонить депозит",
        "hi": "❌ जमा अस्वीकार करें",
    },
    "admin_deposit_approved_confirm": {
        "ar": "✅ تم قبول الإيداع وإضافة الرصيد للعميل بنجاح.",
        "en": "✅ Deposit approved and balance credited successfully.",
        "ru": "✅ Депозит одобрен и баланс успешно зачислен.",
        "hi": "✅ जमा स्वीकृत और बैलेंस सफलतापूर्वक जमा।",
    },
    "admin_deposit_rejected_confirm": {
        "ar": "❌ تم رفض الإيداع وإشعار العميل.",
        "en": "❌ Deposit rejected and user notified.",
        "ru": "❌ Депозит отклонён, пользователь уведомлён.",
        "hi": "❌ जमा अस्वीकार और उपयोगकर्ता को सूचित किया गया।",
    },

    # ─────────────────────────────────────────
    #  SUPPORT
    # ─────────────────────────────────────────
    "support_message": {
        "ar": "🎧 **الدعم الفني**\n\nللتواصل مع فريق الدعم، راسلنا على: @GoldenEraSupport\n\nساعات العمل: 24/7",
        "en": "🎧 **Support**\n\nContact our support team: @GoldenEraSupport\n\nAvailable: 24/7",
        "ru": "🎧 **Поддержка**\n\nСвяжитесь с нашей поддержкой: @GoldenEraSupport\n\nДоступно: 24/7",
        "hi": "🎧 **सहायता**\n\nहमारी सहायता टीम से संपर्क करें: @GoldenEraSupport\n\nउपलब्ध: 24/7",
    },
}


def t(key: str, lang: str = "ar", **kwargs: Any) -> str:
    """
    Translate a key to the given language.
    Falls back to English, then key itself.
    Supports .format(**kwargs) placeholders.
    """
    translations = _translations.get(key, {})
    text = translations.get(lang) or translations.get("en") or key
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass
    return text
