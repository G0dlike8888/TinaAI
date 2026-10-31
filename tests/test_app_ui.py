"""Streamlit AppTest coverage: rendered flows with a mocked client only.

No test here constructs a real Anthropic client or sends a request. Covers
required test areas 4 (UI side), 8 (UI side), 9 (UI side) and 11 (UI side):
fail-closed integrity UI, missing-key handling, over-limit rejection before
any client exists, base/gated/error flows, gating off by default, state
preservation across language switch, and reset behaviour.
"""
import hashlib

import anthropic
import pytest
from streamlit.testing.v1 import AppTest

import contract_integrity
import demo_logic
from ui_text import UI_TEXT

from conftest import APP_PATH, FakeClient, make_api_status_error

TEST_KEY = "test-key-not-a-real-credential"


def _app() -> AppTest:
    at = AppTest.from_file(str(APP_PATH), default_timeout=30)
    at.secrets["ANTHROPIC_API_KEY"] = TEST_KEY
    return at


def _all_rendered_text(at: AppTest) -> str:
    parts = []
    for attr in ("markdown", "error", "warning", "info", "caption", "code"):
        for element in getattr(at, attr):
            parts.append(str(element.value))
    return "\n".join(parts)


def _fill_and_click_analyze(at: AppTest, rule="rule text", note="note text"):
    at.text_area(key="rule_text").set_value(rule)
    at.text_area(key="note_text").set_value(note)
    at.button(key="analyze_btn").click().run()


# --- startup and configuration states -----------------------------------
def test_app_runs_clean_with_key_configured():
    at = _app()
    at.run()
    assert not at.exception


def test_missing_key_disables_analysis_and_warns_without_leaking():
    at = AppTest.from_file(str(APP_PATH), default_timeout=30)
    at.run()
    assert not at.exception
    assert at.button(key="analyze_btn").disabled is True
    rendered = _all_rendered_text(at)
    assert UI_TEXT["bg"]["missing_key_warning"][:30] in rendered
    assert "sk-ant" not in rendered


def test_placeholder_key_counts_as_missing():
    at = AppTest.from_file(str(APP_PATH), default_timeout=30)
    at.secrets["ANTHROPIC_API_KEY"] = demo_logic.EXAMPLE_KEY_PLACEHOLDER
    at.run()
    assert at.button(key="analyze_btn").disabled is True


def test_integrity_failure_fails_closed_in_ui(monkeypatch):
    def _broken(*args, **kwargs):
        raise contract_integrity.ContractIntegrityError(
            "induced-for-test: verification mismatch"
        )

    monkeypatch.setattr(
        contract_integrity, "load_verified_contract", _broken
    )
    at = _app()
    at.run()
    assert not at.exception
    rendered = _all_rendered_text(at)
    assert UI_TEXT["bg"]["integrity_error_title"][:25] in rendered
    assert UI_TEXT["en"]["integrity_error_title"][:25] in rendered
    # The script stopped before any analysis control was rendered.
    assert len(at.button) == 0
    assert len(at.text_area) == 0


# --- input safety --------------------------------------------------------
def test_empty_inputs_warn_and_send_nothing(monkeypatch):
    def _forbidden(_key):
        raise AssertionError("client must not be constructed")

    monkeypatch.setattr(demo_logic, "create_client", _forbidden)
    at = _app()
    at.run()
    at.button(key="analyze_btn").click().run()
    assert not at.exception
    assert UI_TEXT["bg"]["empty_warning"] in _all_rendered_text(at)
    assert at.session_state["last_result"] is None


def test_over_limit_note_rejected_before_client_exists(monkeypatch):
    def _forbidden(_key):
        raise AssertionError("client must not be constructed")

    monkeypatch.setattr(demo_logic, "create_client", _forbidden)
    at = _app()
    at.run()
    _fill_and_click_analyze(
        at, note="x" * (demo_logic.MAX_NOTE_CHARS + 1)
    )
    assert not at.exception
    rendered = _all_rendered_text(at)
    assert f"{demo_logic.MAX_NOTE_CHARS:,}" in rendered
    assert at.session_state["last_result"] is None
    assert at.session_state["pending_request"] is None


def test_synthetic_data_warning_visible_before_analysis():
    at = _app()
    at.run()
    rendered = _all_rendered_text(at)
    assert UI_TEXT["bg"]["synthetic_warning"][:40] in rendered
    assert UI_TEXT["bg"]["no_real_data"][:30] in rendered


# --- scenarios -----------------------------------------------------------
def test_scenario_selectbox_offers_custom_plus_all_ten():
    at = _app()
    at.run()
    # AppTest reports the display labels (after format_func); the underlying
    # option ids are asserted via set_value in test_scenario_load_populates.
    options = at.selectbox(key="scenario_selector").options
    assert len(options) == 11
    assert options[0] == "Custom"
    for i in range(1, 11):
        label = demo_logic.SCENARIOS[f"scenario_{i}"]["label_bg"]
        assert label in options


@pytest.mark.parametrize("scenario_id", list(demo_logic.SCENARIOS.keys()))
def test_scenario_load_populates_inputs(scenario_id):
    at = _app()
    at.run()
    # The load button is only rendered once a non-Custom scenario is
    # selected, so the selection needs its own rerun first.
    at.selectbox(key="scenario_selector").set_value(scenario_id).run()
    at.button(key="load_scenario_btn").click().run()
    assert (
        at.session_state["rule_text"]
        == demo_logic.SCENARIOS[scenario_id]["rule"]
    )
    assert (
        at.session_state["note_text"]
        == demo_logic.SCENARIOS[scenario_id]["note"]
    )


# --- Custom mode: free text first, presets optional ----------------------
def test_custom_mode_shows_free_text_inputs_immediately():
    at = _app()
    at.run()
    # Custom is the default selection: both free-text fields are present
    # with the Custom labels, no load action is required, and the guidance
    # caption is shown.
    assert (
        at.text_area(key="rule_text").label
        == UI_TEXT["bg"]["custom_rule_label"]
    )
    assert (
        at.text_area(key="note_text").label
        == UI_TEXT["bg"]["custom_note_label"]
    )
    rendered = _all_rendered_text(at)
    assert UI_TEXT["bg"]["custom_mode_caption"][:40] in rendered
    # The scenario-load button is hidden in Custom mode...
    assert not any(b.key == "load_scenario_btn" for b in at.button)
    # ...while the optional presets remain available (collapsed section).
    assert at.selectbox(key="gating_rule_selector") is not None
    assert UI_TEXT["bg"]["preset_caption"][:40] in rendered


def test_scenario_mode_restores_standard_labels_and_load_button():
    at = _app()
    at.run()
    at.selectbox(key="scenario_selector").set_value("scenario_1").run()
    assert at.text_area(key="rule_text").label == UI_TEXT["bg"]["rule_label"]
    assert at.text_area(key="note_text").label == UI_TEXT["bg"]["note_label"]
    assert any(b.key == "load_scenario_btn" for b in at.button)
    # The preset section is a Custom-mode tool only.
    assert not any(s.key == "gating_rule_selector" for s in at.selectbox)


def test_selecting_custom_does_not_erase_typed_text():
    at = _app()
    at.run()
    at.selectbox(key="scenario_selector").set_value("scenario_1").run()
    at.button(key="load_scenario_btn").click().run()
    assert at.session_state["rule_text"] != ""
    at.selectbox(key="scenario_selector").set_value("Custom").run()
    assert (
        at.session_state["rule_text"]
        == demo_logic.SCENARIOS["scenario_1"]["rule"]
    )
    assert (
        at.session_state["note_text"]
        == demo_logic.SCENARIOS["scenario_1"]["note"]
    )


def test_gating_preset_loads_rule_only_and_keeps_note():
    at = _app()
    at.run()
    at.text_area(key="note_text").set_value("my own thin note")
    at.selectbox(key="gating_rule_selector").set_value("gating_rule_2")
    at.button(key="load_gating_rule_btn").click().run()
    assert (
        at.session_state["rule_text"]
        == demo_logic.GATING_TEST_RULES["gating_rule_2"]["rule"]
    )
    # The note is never touched by a preset load.
    assert at.session_state["note_text"] == "my own thin note"
    assert at.session_state["preset_confirm_pending"] is None


def test_gating_preset_requires_confirmation_over_nonempty_rule():
    at = _app()
    at.run()
    at.text_area(key="rule_text").set_value("my carefully typed rule")
    at.text_area(key="note_text").set_value("my carefully typed note")
    at.selectbox(key="gating_rule_selector").set_value("gating_rule_3")
    at.button(key="load_gating_rule_btn").click().run()
    # First click: nothing replaced, confirmation armed against the exact
    # (preset, rule text) pair, warning visible.
    assert at.session_state["rule_text"] == "my carefully typed rule"
    assert at.session_state["preset_confirm_pending"] == {
        "preset": "gating_rule_3",
        "rule": "my carefully typed rule",
    }
    assert (
        UI_TEXT["bg"]["preset_overwrite_warning"][:30]
        in _all_rendered_text(at)
    )
    # Second click on the same preset: rule replaced, note untouched.
    at.button(key="load_gating_rule_btn").click().run()
    assert (
        at.session_state["rule_text"]
        == demo_logic.GATING_TEST_RULES["gating_rule_3"]["rule"]
    )
    assert at.session_state["note_text"] == "my carefully typed note"
    assert at.session_state["preset_confirm_pending"] is None


# --- base analysis path --------------------------------------------------
def test_base_flow_uses_verified_contract_and_displays_response(monkeypatch):
    client = FakeClient([["Analysis part one. ", "Part two."]])
    monkeypatch.setattr(demo_logic, "create_client", lambda _key: client)
    at = _app()
    at.run()
    _fill_and_click_analyze(at)
    assert not at.exception

    stored = at.session_state["last_result"]
    assert stored["kind"] == "base"
    assert stored["base_text"] == "Analysis part one. Part two."
    assert at.session_state["pending_request"] is None

    # Exactly one API call; its system prompt is the verified pinned body,
    # and the user payload rode in the user message.
    (call,) = client.calls
    assert (
        hashlib.sha256(call["system"].encode("utf-8")).hexdigest()
        == contract_integrity.PINNED_SHA256
    )
    assert "rule text" in call["messages"][0]["content"]

    # The response is rendered as-is, with no added labels around it.
    rendered = _all_rendered_text(at)
    assert "Analysis part one. Part two." in rendered
    # Analyze button is enabled again after the run completes.
    assert at.button(key="analyze_btn").disabled is False

    # The configured key never reaches the page or session state.
    assert TEST_KEY not in rendered
    assert TEST_KEY not in str(at.session_state)


def test_provider_error_maps_to_safe_message(monkeypatch):
    client = FakeClient(
        [make_api_status_error(anthropic.AuthenticationError, 401)]
    )
    monkeypatch.setattr(demo_logic, "create_client", lambda _key: client)
    at = _app()
    at.run()
    _fill_and_click_analyze(at)
    assert not at.exception

    stored = at.session_state["last_result"]
    assert stored == {"kind": "error", "category": "auth"}
    rendered = _all_rendered_text(at)
    assert UI_TEXT["bg"]["err_auth"][:30] in rendered
    # The raw exception text never reaches the page.
    assert "scripted test error" not in rendered
    assert "Traceback" not in rendered


# --- experimental gating branch ------------------------------------------
def test_gating_checkbox_is_off_by_default():
    at = _app()
    at.run()
    assert at.checkbox(key="apply_gating").value is False


def test_gated_flow_keeps_base_and_shows_filtered_separately(monkeypatch):
    client = FakeClient([["The base analysis."], "The filtered analysis."])
    monkeypatch.setattr(demo_logic, "create_client", lambda _key: client)
    at = _app()
    at.run()
    at.checkbox(key="apply_gating").check()
    _fill_and_click_analyze(at)
    assert not at.exception

    stored = at.session_state["last_result"]
    assert stored["kind"] == "gated"
    assert stored["base_text"] == "The base analysis."
    assert stored["filtered_text"] == "The filtered analysis."
    assert stored["filter_failed"] is False

    assert len(client.calls) == 2
    base_call, filter_call = client.calls
    assert base_call["stream"] is True
    assert "<<<TEXT-" in filter_call["system"]
    assert "The base analysis." in filter_call["messages"][0]["content"]

    rendered = _all_rendered_text(at)
    assert "The filtered analysis." in rendered
    assert "The base analysis." in rendered
    # Alert elements drop the leading emoji, so match on the text body.
    assert "Приложен е Post-generation filter" in rendered
    assert UI_TEXT["bg"]["filtered_header"].lstrip("# ") in rendered


def test_gated_filter_failure_preserves_base_with_warning(monkeypatch):
    client = FakeClient(
        [
            ["The base analysis."],
            make_api_status_error(anthropic.RateLimitError, 429),
        ]
    )
    monkeypatch.setattr(demo_logic, "create_client", lambda _key: client)
    at = _app()
    at.run()
    at.checkbox(key="apply_gating").check()
    _fill_and_click_analyze(at)
    assert not at.exception

    stored = at.session_state["last_result"]
    assert stored["kind"] == "gated"
    assert stored["filter_failed"] is True
    assert stored["filter_error_category"] == "rate_limit"
    assert stored["base_text"] == "The base analysis."

    rendered = _all_rendered_text(at)
    assert "The base analysis." in rendered
    assert UI_TEXT["bg"]["err_rate_limit"][:25] in rendered
    assert "scripted test error" not in rendered
    # The "filter applied" banner must NOT show when the filter failed —
    # only the fallback warning names the (failed) filter.
    assert "Приложен е Post-generation filter" not in rendered


def test_gated_empty_base_stream_is_not_silently_dropped(monkeypatch):
    client = FakeClient([[]])
    monkeypatch.setattr(demo_logic, "create_client", lambda _key: client)
    at = _app()
    at.run()
    at.checkbox(key="apply_gating").check()
    _fill_and_click_analyze(at)
    assert not at.exception
    # The completed-but-empty base call is stored like the non-gated
    # branch stores it; no second (filter) call is made on empty text.
    assert at.session_state["last_result"] == {
        "kind": "base",
        "base_text": "",
    }
    assert len(client.calls) == 1


def test_validation_failure_keeps_stored_result_visible(monkeypatch):
    client = FakeClient([["Kept result."]])
    monkeypatch.setattr(demo_logic, "create_client", lambda _key: client)
    at = _app()
    at.run()
    _fill_and_click_analyze(at)
    assert at.session_state["last_result"]["base_text"] == "Kept result."

    at.text_area(key="note_text").set_value("")
    at.button(key="analyze_btn").click().run()
    assert not at.exception
    rendered = _all_rendered_text(at)
    # Both the validation warning and the previous result are on screen.
    assert UI_TEXT["bg"]["empty_warning"] in rendered
    assert "Kept result." in rendered
    assert at.session_state["last_result"]["base_text"] == "Kept result."


# --- state preservation and reset ----------------------------------------
def test_language_switch_preserves_inputs_and_result(monkeypatch):
    client = FakeClient([["Preserved analysis."]])
    monkeypatch.setattr(demo_logic, "create_client", lambda _key: client)
    at = _app()
    at.run()
    _fill_and_click_analyze(at, rule="my rule", note="my note")

    at.radio(key="lang_selector").set_value("English").run()
    assert not at.exception
    assert at.session_state["rule_text"] == "my rule"
    assert at.session_state["note_text"] == "my note"
    rendered = _all_rendered_text(at)
    assert "Preserved analysis." in rendered
    # Chrome switched to English without touching the stored result.
    assert UI_TEXT["en"]["synthetic_warning"][:30] in rendered


def test_gating_toggle_after_run_keeps_result(monkeypatch):
    client = FakeClient([["Sticky analysis."]])
    monkeypatch.setattr(demo_logic, "create_client", lambda _key: client)
    at = _app()
    at.run()
    _fill_and_click_analyze(at)
    at.checkbox(key="apply_gating").check().run()
    assert not at.exception
    assert "Sticky analysis." in _all_rendered_text(at)
    # Toggling did not re-filter or erase; still the plain base result.
    assert at.session_state["last_result"]["kind"] == "base"


def test_reset_clears_inputs_and_result_without_submitting(monkeypatch):
    client = FakeClient([["To be cleared."]])
    monkeypatch.setattr(demo_logic, "create_client", lambda _key: client)
    at = _app()
    at.run()
    _fill_and_click_analyze(at)
    assert at.session_state["last_result"] is not None

    at.button(key="reset_btn").click().run()
    assert not at.exception
    assert at.session_state["rule_text"] == ""
    assert at.session_state["note_text"] == ""
    assert at.session_state["last_result"] is None
    # Reset made no API call: still exactly the one scripted call consumed.
    assert len(client.calls) == 1
