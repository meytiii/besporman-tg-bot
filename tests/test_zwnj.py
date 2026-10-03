from pathlib import Path
import pytest
from besporman_tg_bot.utils.zwnj_sanitizer import scan_directory_for_zwnj

def test_zero_zwnj_across_entire_project():
    project_root = Path(__file__).resolve().parent.parent

    violations = scan_directory_for_zwnj(project_root)

    if violations:
        report = ["CRITICAL ERROR: ZWNJ (\\u200c) detected in project files:"]
        for file_path, line_no, line_content in violations:
            report.append(f"  - {file_path}:{line_no} -> {line_content}")
        pytest.fail("\n".join(report))

def test_zwnj_sanitizer_utility():
    from besporman_tg_bot.utils.zwnj_sanitizer import contains_zwnj, sanitize_zwnj

    bad_string = "می\u200cخواهم بهترین\u200cها را بسازم"
    assert contains_zwnj(bad_string) is True

    clean_string = sanitize_zwnj(bad_string)
    assert contains_zwnj(clean_string) is False
    assert clean_string == "می خواهم بهترین ها را بسازم"
