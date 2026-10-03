"""Intelligent Persian & English profanity / inappropriate language filter.

Designed to prevent offensive messages while avoiding false positives on legitimate words
(e.g., handles 'پیگیری', 'دستگیر', 'سکسکه' without false triggers).
"""

import re
import unicodedata
from typing import Set

# Character normalization table (Arabic to Persian variants)
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

# Inappropriate word roots (checked with token boundaries or exact stems)
# Stored in normalized form. No ZWNJ used.
BLOCKED_TERMS: Set[str] = {
    # Persian vulgarities & profanities (exact tokens / stems)
    "کص", "کسکش", "کصکش", "کونکش", "کونی", "کون",
    "جنده", "قحبه", "لاشی", "دیوس", "دئیوس", "حرومزاده",
    "حروم لقمه", "خارکصه", "مادرجنده", "ننه جنده", "کیر",
    "سکس", "پورن", "سیکتیر", "سیکتر", "کسشر", "کصشر", "کسشعر",
    "گه خور", "عوضی", "پدرسگ", "پدر سگ", "مادر قهوه", "مادرسگ",
    "بی ناموس", "بیناموس", "اوبی", "چس",
    # English vulgarities
    "fuck", "fucker", "fucking", "bitch", "cunt", "dick", "pussy",
    "asshole", "motherfucker", "bastard", "slut", "whore",
}

# Whitelist to ensure specific innocent words with similar substrings are never blocked
SAFE_EXCEPTIONS: Set[str] = {
    "پیگیری", "دستگیر", "دستگیری", "مسکن", "سکسکه",
    "کوسه", "پاینده", "تشکر", "عکس", "بسکتبال", "فروشگاه",
    "پروژه", "برنامه", "برنامه نویسی", "توسعه", "پشتیبانی"
}


def normalize_persian_text(text: str) -> str:
    """Normalize text: convert variants, remove harakat, collapse repetitions, remove hidden chars."""
    if not text:
        return ""

    # Normalize unicode
    text = unicodedata.normalize("NFKD", text)

    # Remove diacritics / tashkeel (0x064B - 0x0652) and zero-width characters
    cleaned_chars = []
    for ch in text:
        # Skip zero-width joiners/non-joiners and diacritics
        if ch in {"\u200c", "\u200b", "\u200d", "\ufeff"}:
            cleaned_chars.append(" ")
            continue
        code = ord(ch)
        if 0x064B <= code <= 0x0652 or code == 0x0670:
            continue
        # Apply char mapping
        cleaned_chars.append(CHAR_MAP.get(ch, ch))

    normalized = "".join(cleaned_chars).lower()

    # Remove symbols/punctuation that could be used for spacing obfuscation (e.g. "ف.ح.ش")
    # Replace non-alphanumeric chars with spaces
    normalized = re.sub(r"[^\w\s\u0600-\u06FF]", " ", normalized)

    # Collapse repeated consecutive characters (e.g., 'سسسسلااام' -> 'سلام')
    normalized = re.sub(r"(.)\1{2,}", r"\1", normalized)

    # Collapse whitespace
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def is_profane(text: str) -> bool:
    """Evaluate whether the given text contains prohibited profanity.

    Returns True if inappropriate content is detected, False otherwise.
    """
    if not text:
        return False

    normalized = normalize_persian_text(text)
    if not normalized:
        return False

    tokens = normalized.split()

    # Check safe exceptions first
    # If all tokens are safe exceptions, pass immediately
    filtered_tokens = [t for t in tokens if t not in SAFE_EXCEPTIONS]
    if not filtered_tokens:
        return False

    # Check individual tokens
    for token in filtered_tokens:
        if token in BLOCKED_TERMS:
            return True

    # Check multi-word profanities or exact substring patterns with boundaries
    for phrase in BLOCKED_TERMS:
        if " " in phrase:
            if phrase in normalized:
                return True
        else:
            # Check with word boundaries
            pattern = rf"(^|\s){re.escape(phrase)}(\s|$)"
            if re.search(pattern, normalized):
                # Verify it's not a safe compound
                if not any(token in SAFE_EXCEPTIONS for token in tokens if phrase in token):
                    return True

    return False
