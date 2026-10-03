import pytest
from besporman_tg_bot.utils.profanity_filter import is_profane, normalize_persian_text

@pytest.mark.parametrize(
    "clean_text",
    [
        "سلام، خسته نباشید. می خواستم درباره طراحی سایت فروشگاهی سوال بپرسم.",
        "لطفا پیگیری کنید وضعیت سفارش من رو.",
        "یک نرم افزار برای مدیریت مسکن و املاک نیاز داریم.",
        "سارقین در یک عملیات دستگیر شدند.",
        "عکس های نمونه کارهای ویندوزی رو دیدم، خیلی تمیز بودن.",
        "ما یک سیستم ثبت سفارش برای فروشگاه قطعات یدکی خودرو می خواهیم.",
        "تیم بسپر من واقعا کارشون درسته.",
        "سکسکه ام بند نمیاد، ولی پروژه ام رو تحویل بدید لطفا!",
        "کوسه های خلیج فارس در مستند نشان داده شدند.",
    ],
)
def test_profanity_filter_clean_texts(clean_text: str):
    assert is_profane(clean_text) is False

@pytest.mark.parametrize(
    "profane_text",
    [
        "این چه سیستم کسکشیه آخه؟",
        "کصکش های بی ناموس",
        "عوضی های لاشی",
        "حرومزاده ها پروژه رو تحویل ندادید",
        "fuck your system",
        "خیلی جنده هستید",
        "مادرجنده عوضی",
        "سیکتیر کن بابا",
        "پدر سگ پول منو پس بده",
    ],
)
def test_profanity_filter_blocked_texts(profane_text: str):
    assert is_profane(profane_text) is True

def test_normalization_removes_repeated_chars_and_diacritics():
    raw = "سسسسلاااام مَردُم"
    norm = normalize_persian_text(raw)
    assert "سلام" in norm
