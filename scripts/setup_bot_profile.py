"""
Setup Telegram Bot Profile: Description, Short Description, and Profile Photo.
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from aiogram import Bot
from aiogram.types import InputProfilePhotoStatic, FSInputFile
from app.core.config import settings

DESC_AR = """🌐 مرحباً بك في بوت GoldenEra 5G Proxies الرسمي!

🚀 بوابتك الأولى للحصول على أقوى بروكسيات 5G فائقة السرعة والمصممة لأعلى مستويات الحماية والأداء.

⚡ مميزات الخدمة:
• بروكسيات 5G / 4G حقيقية ونظيفة 100%.
• دعم كامل لبروتوكولات HTTP و SOCKS5.
• تدوير فوري وعالي الدقة للـ IP (IP Rotation).
• استقرار فائق وسرعات اتصال متطورة.
• طرق شحن سريعة: فودافون كاش (Vodafone Cash)، باينانس (Binance Pay)، وأكواد الشحن (Redeem Codes).

اضغط على Start للبدء وتصفح الباقات وشحن رصيدك فوراً!"""

DESC_EN = """🌐 Welcome to GoldenEra 5G Proxies official bot!

🚀 Your premium destination for ultra-fast, dedicated 5G/4G mobile proxies engineered for maximum security and performance.

⚡ Features:
• 100% Clean Mobile 5G & 4G IPs
• Full HTTP & SOCKS5 protocols support
• Instant automated & manual IP rotation
• High uptime, low ping & ultimate stability
• Instant deposit methods: Vodafone Cash, Binance Pay & Redeem Codes

Press Start to browse packages and activate your proxies!"""

SHORT_AR = "البوت الرسمي لـ GoldenEra 5G — أسرع وأقوى بروكسيات 5G بتدوير فوري للـ IP ودعم فودافون كاش وباينانس."
SHORT_EN = "Fast & secure 5G mobile proxies with instant IP rotation. Official bot for GoldenEra 5G Proxies."


async def setup_bot_profile():
    bot = Bot(token=settings.BOT_TOKEN)
    try:
        # 1. Descriptions
        await bot.set_my_description(description=DESC_AR, language_code="ar")
        await bot.set_my_description(description=DESC_EN, language_code="")
        await bot.set_my_short_description(short_description=SHORT_AR, language_code="ar")
        await bot.set_my_short_description(short_description=SHORT_EN, language_code="")
        print("✅ Bot descriptions updated successfully.")

        # 2. Profile Photo
        logo_path = "static/logo_web.png"
        if not os.path.exists(logo_path):
            logo_path = "static/logo.png"

        if os.path.exists(logo_path):
            await bot.set_my_profile_photo(photo=InputProfilePhotoStatic(photo=FSInputFile(logo_path)))
            print(f"✅ Bot profile photo updated from {logo_path}.")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(setup_bot_profile())
