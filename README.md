# 🌟 GoldenEra — 5G & Residential Proxies Reselling System
### Telegram Bot + Modern Admin Web Dashboard + Automated Multi-Payment

نظام متكامل واحترافي لبيع وإعادة بيع البروكسيات (PRIME, HYPER, NEXUS, TITAN) متصل بـ **Magnum Reseller API v1.4.0** مع لوحة تحكم عصرية ونظام شحن وإيداع ذكي يدعم **4 لغات** ومصمم ليعمل على **الاستضافات المجانية**.

---

## 🚀 المميزات الرئيسية

### 1. بوت تيليجرام تفاعلي حديث (Interactive Telegram Bot)
- **دعم 4 لغات أساسية**: 🇸🇦 العربية، 🇺🇸 الإنجليزية، 🇷🇺 الروسية، 🇮🇳 الهندية (مع إمكانية التبديل الفوري بنقرة واحدة).
- **معالج شراء ذكي وسلس (Purchase Wizard)**: اختيار الفئة، السيرفر والموقع، النمط (Rotate / Inject)، إدخال البيانات، والتأكيد.
- **تكامل غير متزامن فوري مع Magnum API**: وضع الطلب في قائمة الانتظار، السحب التلقائي، وإرسال بطاقة البروكسي لحظياً للمستخدم فور تجهيزها.
- **بطاقة بروكسي ذكية وعصرية**:
  - عرض تفاصيل الاتصال (Host, Ports, Credentials, Expiry, Ready URL).
  - 🔄 **تدوير الـ IP فوري** (Instant IP Rotation لبروكسيات NEXUS).
  - 🔑 **تغيير كلمة المرور** بضغطة زر.
  - 🔀 **التحويل بين Rotate و Inject**.
  - ♻️ **تجديد الاشتراك** قبل الانتهاء.
- **نظام إشعارات تلقائي (Expiry Alerts)**: تنبيه المستخدم قبل انتهاء صلاحية البروكسي بـ 24 ساعة وساعتين.

### 2. بوابات الشحن بالـ Transaction ID
- **🟡 Binance / USDT (TRC20) — تلقائي بالكامل (Auto-Confirm)**:
  - العميل يحول ويدخل الـ **Transaction ID (TxID)**.
  - يفحص النظام صلاحية المعاملة وشبكة البلوكشين وقيمتها ويمنع تكرار الـ TxID، ويشحن المحفظة تلقائياً بالدولار فور التأكيد.
- **🔴 Vodafone Cash — تأكيد سريع بنقرة زر (One-Click Approval)**:
  - يدخل العميل رقم المحول منه والـ **Transaction ID**.
  - يصل إشعار فوري لـ **تيليجرام الأدمن** بأزرار تفاعلية: `[ ✅ قبول وشحن الرصيد ]` و `[ ❌ رفض الإيداع ]`.
  - وتظهر في نفس اللحظة داخل لوحة تحكم الويب للموافقة أو الرفض بنقرة واحدة.

### 3. لوحة تحكم الإدارة العصرية (Admin Web Dashboard)
- **تصميم عصري ونظيف**: Dark Minimalist Theme مستوحى من Linear و Vercel بعيداً عن التدرجات المبتذلة (No AI Slop).
- **أقسام اللوحة**:
  - 📊 **لوحة المؤشرات (KPIs)**: المستخدمين، البروكسيات النشطة، أرباح اليوم، رصيدك في Magnum.
  - 👥 **المستخدمين والمحافظ**: عرض الأرصدة، البحث، وتعديل الرصيد يدوياً لأي مستخدم.
  - 💳 **إدارة الإيداعات المعلقة**: مراجعة إيداعات فودافون كاش والموافقة عليها.
  - 🔌 **مراقبة البروكسيات النشطة**: قائمة حية بكل البروكسيات المباعة وصلاحياتها.
  - ⚙️ **التسعير وهوامش الربح**: ضبط نسبة الربح التلقائية (`Markup %`)، سعر صرف الدولار للجنيه (`USD/EGP`)، ورقم فودافون كاش.
  - 📢 **الإذاعة الجماعية (Broadcaster)**: إرسال تنبيهات وعروض لجميع مستخدمي البوت دفعة واحدة.

---

## 🛠️ التثبيت والتشغيل المحلي (Local Setup)

### 1. إعداد المتطلبات
المشروع مبني على **Python 3.14 / 3.13 / 3.12**:
```bash
pip install -r requirements.txt
```

### 2. إعداد ملف البيئة `.env`
انسخ `.env.example` إلى `.env` وضع مفاتيحك:
```env
BOT_TOKEN=123456789:ABCdefGHI...
ADMIN_CHAT_IDS=123456789            # Telegram ID الخاص بك لتلقي إشعارات الشحن

MAGNUM_API_KEY=your_magnum_key
MAGNUM_BASE_URL=https://api.magnumproxy.com

DASHBOARD_USERNAME=admin
DASHBOARD_PASSWORD=your_secure_password

VODAFONE_CASH_NUMBER=01012345678
BINANCE_WALLET_ADDRESS=Txxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
USD_TO_EGP_RATE=52.0
DEFAULT_MARKUP_PERCENT=30.0
```

### 3. تشغيل النظام (بوت تيليجرام + لوحة التحكم في أمر واحد)
```bash
python main.py
```
* **رابط لوحة التحكم**: `http://localhost:8000/admin`
* **بيانات الدخول الافتراضية**:
  - المستخدم: `admin` (أو ما حددته في `.env`)
  - كلمة المرور: ما حددته في `.env`

---

## 🌐 الرفع على الاستضافة المجانية (Free-Tier Deployment)

تم تصميم المشروع ليعمل بالكامل داخل **عملية واحدة خفيفة (Single Unified Process)** تستهلك أقل من 100 ميجابايت رام، مما يجعلها مثالية للاستضافات المجانية:

### الخيار 1: النشر على Render.com (مجاني 100%)
1. ارفع المشروع إلى حسابك على GitHub.
2. ادخل على **Render.com** واضغط **New Blueprint Instance**.
3. اختر المستودع وسيقوم Render تلقائياً بقراءة ملف `render.yaml` وبناء المشروع وتشغيله.
4. املأ المتغيرات السرية في لوحة Render (مثل `BOT_TOKEN` و `MAGNUM_API_KEY`).

### الخيار 2: النشر على Koyeb أو Railway
يمكن استخدام الـ `Dockerfile` المرفق مباشرة في أي منصة سحابية تدعم دوكر.

---

## 🗄️ هيكل المشروع
```
f:\Projects\GoldenEra - 5G Proxies\
├── app/
│   ├── bot/
│   │   ├── handlers/        # معالجات البوت (start, catalog, my_proxies, deposit, wallet)
│   │   ├── keyboards/       # أزرار تيليجرام التفاعلية
│   │   ├── i18n.py          # نظام الترجمة لـ 4 لغات (AR, EN, RU, HI)
│   │   └── instance.py      # كائن البوت الموحد المشترك
│   ├── core/
│   │   ├── config.py        # إعدادات التطبيق
│   │   ├── database.py      # اتصال قاعدة البيانات (SQLite / PostgreSQL)
│   │   └── helpers.py       # دوال الهوامش والأسعار
│   ├── dashboard/
│   │   ├── routes/          # مسارات لوحة التحكم (auth, api, pages)
│   │   └── static/          # شاشات لوحة التحكم العصرية (Clean Minimalist)
│   ├── models/              # جداول قاعدة البيانات (User, Wallet, Proxy, Deposit, Order)
│   └── services/
│       ├── magnum_client.py # عميل Magnum Reseller API v1.4.0
│       ├── binance_service.py # التحقق الآلي من TRC20 TxID
│       ├── vodafone_service.py # معالجة إيداعات فودافون كاش
│       └── notifications.py # مهمة إشعارات انتهاء صلاحية البروكسيات
├── main.py                  # خادم FastAPI الموحد + محرك البوت
├── requirements.txt
├── Dockerfile
└── render.yaml
```
