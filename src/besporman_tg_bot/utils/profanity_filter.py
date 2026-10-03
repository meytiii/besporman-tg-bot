import re
import unicodedata
from typing import Set

CHAR_MAP = {
    "ك": "ک",
    "ي": "ی",
    "ى": "ی",
    "ئ": "ی",
    "ة": "ه",
    "ؤ": "و",
    "إ": "ا",
    "أ": "ا",
    "آ": "ا",
    "ء": "",
}

STRONG_BLOCKED_STEMS: Set[str] = {
    "کسکش", "کصکش", "کونکش", "جنده", "قحبه", "لاشی", "دیوس",
    "دئیوس", "حرومزاده", "حروم لقمه", "خارکصه", "مادرجنده", "ننه جنده",
    "سیکتیر", "سیکتر", "کسشر", "کصشر", "کسشعر", "پدرسگ", "پدر سگ",
    "مادر قهوه", "مادرسگ", "بی ناموس", "بیناموس", "اوبی",
    "fuck", "fucker", "fucking", "bitch", "cunt", "asshole", "motherfucker", "whore"
}

STANDALONE_BLOCKED_WORDS: Set[str] = {
    "کص", "کون", "کونی", "کیر", "سکس", "پورن", "عوضی", "چس",
    "dick", "pussy", "bastard", "slut"
}

COMMON_SUFFIXES = [
    "هایم", "هایت", "هایش", "هایمان", "هایتان", "هایشان",
    "هایی", "ها", "های", "تون", "شون", "مون", "تان", "شان",
    "مان", "یه", "رو", "ست", "تر", "ترین", "ام", "ات", "اش", "ی"
]

SAFE_EXCEPTIONS: Set[str] = {
    "پیگیری", "دستگیر", "دستگیری", "مسکن", "سکسکه",
    "کوسه", "پاینده", "تشکر", "عکس", "بسکتبال", "فروشگاه",
    "پروژه", "برنامه", "برنامه نویسی", "توسعه", "پشتیبانی",
    "کاربر", "سیستم", "شرکت", "مدیریت", "سفارش", "تیم"
}

def normalize_persian_text(text: str) -> str:
    if not text:
        return ""

    text = unicodedata.normalize("NFKD", text)

    cleaned_chars = []
    for ch in text:
        if ch in {"\u200c", "\u200b", "\u200d", "\ufeff"}:
            cleaned_chars.append(" ")
            continue
        code = ord(ch)
        if 0x064B <= code <= 0x0652 or code == 0x0670:
            continue
        cleaned_chars.append(CHAR_MAP.get(ch, ch))

    normalized = "".join(cleaned_chars).lower()
    normalized = re.sub(r"[^\w\s\u0600-\u06FF]", " ", normalized)
    normalized = re.sub(r"(.)\1{2,}", r"\1", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized

def _strip_persian_suffixes(word: str) -> str:
    for sfx in COMMON_SUFFIXES:
        if word.endswith(sfx) and len(word) > len(sfx) + 2:
            return word[:-len(sfx)]
    return word

def is_profane(text: str) -> bool:
    if not text:
        return False

    normalized = normalize_persian_text(text)
    if not normalized:
        return False

    tokens = normalized.split()

    for stem in STRONG_BLOCKED_STEMS:
        if " " in stem:
            if stem in normalized:
                return True
        else:
            for token in tokens:
                if stem in token:
                    if not any(safe in token for safe in SAFE_EXCEPTIONS):
                        return True

    for token in tokens:
        if any(safe in token for safe in SAFE_EXCEPTIONS):
            continue
        if token in STANDALONE_BLOCKED_WORDS:
            return True
        stemmed = _strip_persian_suffixes(token)
        if stemmed in STANDALONE_BLOCKED_WORDS:
            return True

    return False
