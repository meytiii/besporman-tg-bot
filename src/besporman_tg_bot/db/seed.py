import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from besporman_tg_bot.db.models import Portfolio, PortfolioMedia, Testimonial

logger = logging.getLogger(__name__)

INITIAL_PORTFOLIO = [
    {
        "title": "🌐 وبسایت فروشگاهی و درگاه پرداخت اختصاصی",
        "description": (
            "[PLACEHOLDER: پروژه نمونه]\n\n"
            "طراحی و پیاده سازی فروشگاه آنلاین با قابلیت اتصال به درگاه های بانکی، "
            "سیستم انبارداری و پنل مدیریت سفارشات. کاملا واکنش گرا و بهینه برای موبایل."
        ),
        "technologies": "Python, FastAPI, React, PostgreSQL",
        "sort_order": 1,
        "media": [
            {
                "file_id": "placeholder_storefront_1",
                "media_type": "PHOTO",
                "caption": "نمای صفحه اصلی و دسته بندی محصولات [PLACEHOLDER]",
                "sort_order": 1,
            }
        ],
    },
    {
        "title": "🖥 نرم افزار تحت ویندوز مدیریت فروش و صدور فاکتور",
        "description": (
            "[PLACEHOLDER: پروژه نمونه]\n\n"
            "نرم افزار حسابداری و انبارداری تحت سیستم عامل ویندوز با رابط کاربری مدرن، "
            "پشتیبانی از پرینترهای حرارتی و خروجی های گزارش گیری مالی اکسل و پی دی اف."
        ),
        "technologies": "C#, .NET, WPF, SQLite",
        "sort_order": 2,
        "media": [
            {
                "file_id": "placeholder_windows_app_1",
                "media_type": "PHOTO",
                "caption": "نمای ثبت فاکتور و جستجوی سریع کالا [PLACEHOLDER]",
                "sort_order": 1,
            }
        ],
    },
    {
        "title": "🤖 ربات تلگرام ثبت و پیگیری سفارشات",
        "description": (
            "[PLACEHOLDER: پروژه نمونه]\n\n"
            "ربات ثبت سفارش خودکار با قابلیت پرداخت درون برنامه ای، "
            "اطلاع رسانی آنی به مدیران از طریق کانال اختصاصی و پنل تحت وب."
        ),
        "technologies": "Python, aiogram 3, Redis, PostgreSQL",
        "sort_order": 3,
        "media": [
            {
                "file_id": "placeholder_tg_bot_1",
                "media_type": "PHOTO",
                "caption": "منوی ثبت سفارش و فاکتور ربات [PLACEHOLDER]",
                "sort_order": 1,
            }
        ],
    },
    {
        "title": "👥 سامانه اختصاصی CRM پیگیری ارتباط با مشتریان",
        "description": (
            "[PLACEHOLDER: پروژه نمونه]\n\n"
            "سیستم متمرکز برای ثبت سوابق تماس ها، یادآوری جلسات و پیگیری های فروش، "
            "تحلیل رفتار خریداران و تفکیک وظایف کارشناسان فروش."
        ),
        "technologies": "Python, Django, Vue.js, PostgreSQL",
        "sort_order": 4,
        "media": [
            {
                "file_id": "placeholder_crm_1",
                "media_type": "PHOTO",
                "caption": "داشبورد تحلیلی و کارتابل پیگیری مشتریان [PLACEHOLDER]",
                "sort_order": 1,
            }
        ],
    },
]

INITIAL_TESTIMONIALS = [
    {
        "file_id": "placeholder_testimonial_1",
        "caption": "[PLACEHOLDER: تصویر پیام رضایت مشتری شماره یک - فایل واقعی به زودی بارگذاری می شود]",
        "sort_order": 1,
    },
    {
        "file_id": "placeholder_testimonial_2",
        "caption": "[PLACEHOLDER: تصویر پیام رضایت مشتری شماره دو - فایل واقعی به زودی بارگذاری می شود]",
        "sort_order": 2,
    },
]

async def seed_initial_data(session: AsyncSession) -> None:
    res_port = await session.execute(select(Portfolio).limit(1))
    if res_port.scalar_one_or_none() is None:
        logger.info("Seeding initial portfolio items...")
        for p_data in INITIAL_PORTFOLIO:
            media_list = p_data.get("media", [])
            portfolio = Portfolio(
                title=p_data["title"],
                description=p_data["description"],
                technologies=p_data["technologies"],
                sort_order=p_data["sort_order"],
                is_active=True,
            )
            session.add(portfolio)
            await session.flush()

            for m_data in media_list:
                media = PortfolioMedia(
                    portfolio_id=portfolio.id,
                    file_id=m_data["file_id"],
                    media_type=m_data["media_type"],
                    caption=m_data["caption"],
                    sort_order=m_data["sort_order"],
                )
                session.add(media)

        await session.commit()
        logger.info("Portfolio seeding completed.")

    res_test = await session.execute(select(Testimonial).limit(1))
    if res_test.scalar_one_or_none() is None:
        logger.info("Seeding initial testimonials...")
        for t_data in INITIAL_TESTIMONIALS:
            testimonial = Testimonial(
                file_id=t_data["file_id"],
                caption=t_data["caption"],
                sort_order=t_data["sort_order"],
                is_active=True,
            )
            session.add(testimonial)

        await session.commit()
        logger.info("Testimonial seeding completed.")
