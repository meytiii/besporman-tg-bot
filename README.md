# بسپر من — Bespor Man Telegram Bot

ربات تلگرام تعاملی، ثبت و پیگیری سفارشات، نمایش نمونه کارها، رضایت مشتریان و پل ارتباطی تیم توسعه نرم افزار **بسپر من**.

---

## ۱. معماری و ساختار پروژه (Architecture)

این ربات با معماری ماژولار و مبتنی بر استاندارد لایه ای توسعه داده شده است:

```text
src/besporman_tg_bot/
├── core/                  # تنظیمات سیستم، متغیرهای محیطی و متون فارسی
│   ├── config.py          # پیکربندی با Pydantic Settings
│   └── texts.py           # تمام متون فارسی، دکمه ها و پیام های سیستم (کاملا بدون نیم فاصله)
├── db/                    # لایه پایگاه داده و مدل های ORM
│   ├── base.py            # اتصال ناهمگام (Async Engine)، Session Maker و تنظیم حالت WAL در SQLite
│   ├── models.py          # جداول Users, Orders, Messages, Portfolio, Testimonials, AuditLogs
│   └── seed.py            # داده های اولیه و نگه دارنده های نمونه کارها و رضایت ها
├── handlers/              # کنترل کننده های رویداد و منطق تلگرام
│   ├── common.py          # دستور /start، لغو عملیات و بازگشت به منو
│   ├── order.py           # جریان ثبت سفارش با توضیحات آزاد و تخصیص شناسه ترتیبی
│   ├── services.py        # معرفی ۶ حوزه تخصصی کاری تیم
│   ├── portfolio.py       # کاتالوگ اینلاین نمونه کارها و ثبت سفارش مشابه
│   ├── testimonials.py    # نمایش تصادفی رضایت مشتریان با رعایت کامل حریم خصوصی
│   ├── team.py            # معرفی اعضای تیم (م.خ و ط.ذ) و تحویل رزومه
│   ├── support.py         # دریافت پیام های پشتیبانی با فیلتر هوشمند کلمات نامناسب
│   ├── admin_orders.py    # مدیریت تغییر وضعیت سفارشات توسط ادمین ها
│   ├── admin_bridge.py    # پل ارتباطی ناشناس مشتری و تیم توسعه به نام «بسپر من»
│   └── admin_panel.py     # پنل مدیریتی، داشبورد آماری و لاگ های سیستمی
├── keyboards/             # چیدمان کیبوردها و کلیدهای اینلاین
│   ├── user_kb.py         # کیبوردهای منوی اصلی، انصراف و پیمایش کاربر
│   └── admin_kb.py        # کلیدهای کنترل سفارش و تغییر وضعیت برای ادمین
├── middlewares/           # میدل ویرهای میانجی
│   ├── db_middleware.py   # تزریق AsyncSession به ازای هر آپدیت
│   ├── user_middleware.py # ثبت و به روز رسانی خودکار پروفایل کاربر
│   ├── throttling_middleware.py # ضد اسپم و محدودسازی نرخ ارسال (Rate Limiting)
│   └── admin_filter.py    # احراز هویت ادمین ها صرفا بر اساس شناسه عددی تلگرام
├── states/                # ماشین حالت FSM برای گفتگوهای چند مرحله ای
│   └── user_states.py     # کلاس های StatesGroup
└── utils/                 # ابزارهای کمکی
    ├── profanity_filter.py # فیلتر هوشمند ضد رکاکت فارسی و انگلیسی بدون خطای مثبت کاذب
    └── zwnj_sanitizer.py   # اسکنر و پاک ساز کاراکترهای نیم فاصله (U+200C)
```

---

## ۲. پیش نیازها و نصب (Installation)

این پروژه از پایتون نسخه 3.10 یا بالاتر و ابزار مدرن مدیریت پکیج **uv** استفاده می کند.

```bash
# نصب وابستگی ها با استفاده از uv
uv sync
```

---

## ۳. تنظیم متغیرهای محیطی (Configuration & Environment Variables)

یک فایل به نام `.env` در ریشه پروژه بسازید (می توانید از روی نمونه `.env.example` کپی کنید):

```bash
cp .env.example .env
```

| متغیر | توضیح | مقدار پیش فرض |
| :--- | :--- | :--- |
| `BOT_TOKEN` | توکن ربات دریافتی از BotFather | الزامی |
| `ADMIN_IDS` | لیست شناسه های عددی تلگرام مدیران | `[347382968, 106629087]` |
| `DATABASE_URL` | آدرس اتصال به دیتابیس (SQLite یا PostgreSQL) | `sqlite+aiosqlite:///./besporman.db` |
| `ENVIRONMENT` | محیط اجرا (`development` یا `production`) | `development` |
| `LOG_LEVEL` | سطح لاگ نویسی (`INFO`, `DEBUG`, `WARNING`) | `INFO` |
| `RATE_LIMIT_BURST` | حداکثر پیام مجاز در پنجره زمانی | `5` |
| `RATE_LIMIT_PERIOD` | مدت زمان پنجره کنترل اسپم (ثانیه) | `3.0` |
| `WEBHOOK_MODE` | فعال سازی وب هوک به جای لانگ پولینگ | `false` |
| `WEBHOOK_URL` | آدرس دامنه دارای SSL برای وب هوک | `https://your-domain.com/webhook` |
| `WEBHOOK_PATH` | مسیر اندپوینت وب هوک | `/webhook` |
| `WEBAPP_HOST` | آی پی سرور وب هوک | `0.0.0.0` |
| `WEBAPP_PORT` | پورت سرور وب هوک | `8080` |

---

## ۴. مدیران مجاز تلگرام (Admin IDs)

بر اساس مستندات پروژه، دو شناسه کاربری عددی زیر مجاز به دسترسی به امکانات مدیریتی هستند:

- `347382968`
- `106629087`

احراز هویت تنها از طریق شناسه عددی تلگرام (`from_user.id`) صورت می پذیرد و هرگز به یوزرنیم متکی نیست.

---

## ۵. پایگاه داده و مهاجرت ها (Database & Migrations)

سیستم به صورت پیش فرض از SQLite در حالت کارآمد **WAL (Write-Ahead Logging)** استفاده می کند و ساختار آن با دیتابیس های بزرگ مقیاس نظیر PostgreSQL کاملا سازگار است.

برای اجرای مایگریشن ها با Alembic:

```bash
# اعمال تمام مایگریشن ها
uv run alembic upgrade head

# ایجاد مایگریشن جدید در صورت تغییر مدل ها
uv run alembic revision --autogenerate -m "describe_changes"
```

---

## ۶. اجرای محلی و توسعه (Running Locally)

برای اجرای ربات در حالت لانگ پولینگ (Polling):

```bash
uv run besporman-tg-bot
```

یا مستقیما:

```bash
uv run python -m besporman_tg_bot.main
```

---

## ۷. استقرار در محیط پروداکشن (Production Deployment)

### الف) حالت لانگ پولینگ با Systemd (ساده ترین روش روی سرور لینوکس)
یک سرویس در `/etc/systemd/system/besporman.service` ایجاد کنید:

```ini
[Unit]
Description=Bespor Man Telegram Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/besporman-tg-bot
ExecStart=/path/to/besporman-tg-bot/.venv/bin/besporman-tg-bot
Restart=always
RestartSec=5
EnvironmentFile=/path/to/besporman-tg-bot/.env

[Install]
WantedBy=multi-user.target
```

سپس سرویس را فعال و روشن کنید:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now besporman
```

### ب) حالت وب هوک (Webhook Mode)
1. مقدار `WEBHOOK_MODE=true` را در فایل `.env` قرار دهید.
2. آدرس کامل دامنه معتبر دارای SSL خود را در `WEBHOOK_URL` وارد کنید.
3. در صورت نیاز پورت `WEBAPP_PORT` را پشت یک Reverse Proxy مثل Nginx قرار دهید.

---

## ۸. دستورات و ابزار ضد نیم فاصله (Zero ZWNJ Check)

در این پروژه به کار بردن کاراکتر نیم فاصله (`\u200c` / ZWNJ / کلید ترکیبی Ctrl+Shift+2) در کلیه متون، کلیدها، لاگ ها و محتوای دیتابیس اکیدا ممنوع است و همواره از فاصله معمولی استفاده می شود (مانند `می خواهم` به جای `می‌خواهم`).

برای اسکن کل پروژه و اطمینان از عدم وجود هرگونه کاراکتر نیم فاصله:

```bash
uv run besporman-zwnj-check
```

---

## ۹. اجرای تست ها (Testing)

پروژه دارای ۳۳ تست واحد و یکپارچه سازی است که عملکرد ماشین حالت، فیلتر کلمات نامناسب، مدل ها و نبود نیم فاصله را بررسی می کنند:

```bash
uv run pytest -v
```

---

## ۱۰. مدیریت محتوا (Content Management)

### افزودن و تغییر نمونه کارها (Portfolio)
اطلاعات نمونه کارها در جدول `portfolio` و فایل های ضمیمه در جدول `portfolio_media` ذخیره می شوند. نمونه کارهای اولیه در فایل [seed.py](file:///c:/Users/Mahdi/Desktop/Stuf/Github/besporman-tg-bot/src/besporman_tg_bot/db/seed.py) با تگ `[PLACEHOLDER]` تعریف شده اند که می توان به سادگی از طریق دیتابیس یا اسکریپت آنها را به روز کرد.

### رضایت مشتریان (Testimonials)
اسکرین شات های واقعی در جدول `testimonials` ذخیره می شوند. سیستم به صورت تصادفی یک تصویر را نمایش داده و دکمه «یکی دیگه نشون بده» را در اختیار مشتری می گذارد.

### فایل های رزومه (Resumes)
فایل های PDF رزومه دو توسعه دهنده هسته اصلی را در مسیر زیر قرار دهید:
- `assets/resumes/resume_dev1.pdf` (برای م.خ)
- `assets/resumes/resume_dev2.pdf` (برای ط.ذ)

در صورتی که فایل هنوز روی دیسک قرار نگرفته باشد، سیستم بدون کرش کردن، پیامی محترمانه مبنی بر در حال آماده سازی بودن فایل نمایش می دهد.

---

## ۱۱. استراتژی پشتیبان گیری (Backup Strategy)

برای دیتابیس پیش فرض SQLite:
```bash
# پشتیبان گیری ایمن حتی هنگام روشن بودن ربات با استفاده از دستور استاندارد sqlite3
sqlite3 besporman.db ".backup 'backup_$(date +%Y%m%d_%H%M%S).sqlite3'"
```

---

## ۱۲. عیب یابی (Troubleshooting)

- **خطای اتصال به تلگرام:** در صورتی که اتصال اینترنت محدود است، متغیرهای محیطی پراکسی `HTTPS_PROXY` را قبل از اجرای پایتون تنظیم کنید.
- **تداخل وب هوک و پولینگ:** قبل از اجرای لانگ پولینگ، دستور `delete_webhook` توسط ربات به صورت خودکار فراخوانی می شود تا صف های مانده تخلیه شوند.
- **بررسی لاگ ها:** لاگ ها با فرمت استاندارد خروجی استاندارد را پر می کنند و در صورت بروز خطا، جزئیات فنی به لاگ هدایت شده و کاربر پیام خطای دوستانه دریافت می نماید.
