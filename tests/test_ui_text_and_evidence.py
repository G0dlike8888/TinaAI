"""Bilingual parity, message safety, and evidence-figure fidelity.

Covers required test areas 10 (message safety side) and 13: the figures the
demo shows must match the immutable evidence record, including both missed
bars and the no-inheritance caveat.
"""
import re

from ui_text import UI_TEXT


def _all_text(lang: str) -> str:
    return "\n".join(str(v) for v in UI_TEXT[lang].values())


# --- bilingual parity ----------------------------------------------------
def test_language_dicts_have_identical_key_sets():
    assert set(UI_TEXT["bg"].keys()) == set(UI_TEXT["en"].keys())


def test_no_empty_ui_strings():
    for lang in ("bg", "en"):
        for key, value in UI_TEXT[lang].items():
            assert str(value).strip(), f"{lang}:{key} is empty"


# --- message safety ------------------------------------------------------
def test_no_raw_exception_interpolation_anywhere():
    for lang in ("bg", "en"):
        for key, value in UI_TEXT[lang].items():
            assert "{exc}" not in str(value), f"{lang}:{key}"
            assert "Traceback" not in str(value), f"{lang}:{key}"


def test_error_messages_are_concise_and_have_no_placeholders():
    for lang in ("bg", "en"):
        for key, value in UI_TEXT[lang].items():
            if key.startswith("err_"):
                assert "{" not in str(value), f"{lang}:{key}"


def test_integrity_error_text_never_suggests_repinning():
    for lang in ("bg", "en"):
        text = UI_TEXT[lang]["integrity_error_title"]
        assert "VERIFY.md" in text
    assert "Do not change the expected hash" in (
        UI_TEXT["en"]["integrity_error_title"]
    )
    assert "Не променяйте очаквания хеш" in (
        UI_TEXT["bg"]["integrity_error_title"]
    )


# --- evidence figures match the immutable record -------------------------
def test_evidence_record_carries_the_canonical_figures(project_root):
    record = (
        project_root
        / "04 Evidence and Records"
        / "Held-Out Evaluation Result - Finding and Restraint n=50 v0.1.md"
    ).read_text(encoding="utf-8")
    assert "4 / 8 = **50.0%**" in record
    assert "32 / 58 = **55.2%**" in record
    assert "≥ 60%" in record
    assert "≤ 25%" in record
    assert "Both bars miss" in record


def test_demo_shows_the_same_figures_with_both_missed_bars():
    for lang in ("bg", "en"):
        methodology = UI_TEXT[lang]["methodology_md"]
        assert "50.0%" in methodology, lang
        assert "(4/8)" in methodology, lang
        assert "55.2%" in methodology, lang
        assert "(32/58)" in methodology, lang
        assert "60%" in methodology, lang
        assert "25%" in methodology, lang
        assert "n=50" in methodology, lang
        assert "claude-haiku-4-5" in methodology, lang
        assert "2f574a66" in methodology, lang
    # Both bars explicitly marked missed, per language.
    assert UI_TEXT["bg"]["methodology_md"].count("непокрит") >= 2
    assert UI_TEXT["en"]["methodology_md"].count("missed") >= 2


def test_demo_carries_the_no_inheritance_caveat():
    assert "не се пренасят" in UI_TEXT["bg"]["methodology_md"]
    assert "do not carry over" in UI_TEXT["en"]["methodology_md"]
    # And the Skill/demo separation is documented in both languages.
    for lang in ("bg", "en"):
        assert "2f574a66" in UI_TEXT[lang]["demo_vs_skill_md"]


def test_gating_figure_carries_its_conditions_and_pretest_label():
    for lang in ("bg", "en"):
        pretest = UI_TEXT[lang]["pretest_md"]
        assert "66.1%" in pretest, lang
        assert "claude-haiku-4-5" in pretest, lang
        assert "pre-test" in pretest.lower(), lang
        gating_info = UI_TEXT[lang]["gating_info"]
        assert "66.1%" in gating_info, lang
    assert "неконфирматорен" in UI_TEXT["bg"]["gating_info"]
    assert "non-confirmatory" in UI_TEXT["en"]["gating_info"]


def test_no_validation_or_readiness_overclaims():
    for lang in ("bg", "en"):
        text = _all_text(lang).lower()
        assert "production ready" not in text
        assert "production-ready" not in text
        assert "regulator" not in text
    # English-side wording that would overclaim measurement status.
    en = _all_text("en")
    assert not re.search(r"\bvalidated\b", en), (
        "demo text must not describe anything as validated"
    )


def test_synthetic_and_no_real_data_warnings_exist():
    for lang in ("bg", "en"):
        assert UI_TEXT[lang]["synthetic_warning"].strip()
        assert UI_TEXT[lang]["no_real_data"].strip()
    assert "Do not paste real data" in UI_TEXT["en"]["no_real_data"]
    assert "Не поставяйте реални данни" in UI_TEXT["bg"]["no_real_data"]
