from pathlib import Path
import sys
from typing import List, Tuple

ZWNJ_CHAR = "\u200c"
ZWNJ_BYTES = b"\xe2\x80\x8c"

def contains_zwnj(text: str) -> bool:
    if not text:
        return False
    return ZWNJ_CHAR in text

def sanitize_zwnj(text: str) -> str:
    if not text:
        return ""
    return text.replace(ZWNJ_CHAR, " ")

def scan_directory_for_zwnj(root_path: Path) -> List[Tuple[str, int, str]]:
    violations: List[Tuple[str, int, str]] = []
    ignored_parts = {".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache"}

    for path in root_path.rglob("*"):
        if not path.is_file():
            continue
        if any(part in path.parts for part in ignored_parts):
            continue
        if path.suffix.lower() not in {".py", ".md", ".json", ".txt", ".sql", ".env", ".example", ".yaml", ".yml"}:
            continue

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        if ZWNJ_CHAR in content:
            for idx, line in enumerate(content.splitlines(), start=1):
                if ZWNJ_CHAR in line:
                    violations.append((str(path.relative_to(root_path)), idx, line.strip()))

    return violations

def main() -> None:
    root = Path.cwd()
    violations = scan_directory_for_zwnj(root)
    if violations:
        print(f"FAILED: {len(violations)} ZWNJ (U+200C) violations detected:")
        for file_path, line_no, content in violations:
            print(f"  [!] {file_path}:{line_no} -> {content}")
        sys.exit(1)
    print("SUCCESS: 0 occurrences of ZWNJ (U+200C) detected across entire project.")

if __name__ == "__main__":
    main()
