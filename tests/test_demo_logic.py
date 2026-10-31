"""Streamlit-free logic: scenarios, validation, request construction,
configuration handling, provider-error mapping and the gating filter.

Covers required test areas 6, 7, 8 (logic side), 9, 10 and 11 (unit side).
"""
import re

import anthropic
import pytest

import demo_logic


# --- 6. ten synthetic scenarios with stable IDs -------------------------
def test_scenarios_have_stable_ids_and_content():
    expected_ids = [f"scenario_{i}" for i in range(1, 11)]
    assert list(demo_logic.SCENARIOS.keys()) == expected_ids
    for sid, scenario in demo_logic.SCENARIOS.items():
        assert scenario["rule"].strip(), sid
        assert scenario["note"].strip(), sid
        assert scenario["label_bg"].strip(), sid
        assert scenario["label_en"].strip(), sid


def test_gating_test_rules_have_stable_ids_and_content():
    expected_ids = [f"gating_rule_{i}" for i in range(1, 11)]
    assert list(demo_logic.GATING_TEST_RULES.keys()) == expected_ids
    for rid, rule in demo_logic.GATING_TEST_RULES.items():
        assert rule["rule"].strip(), rid
        assert rule["label_bg"].strip(), rid
        assert rule["label_en"].strip(), rid


# --- 7. request construction --------------------------------------------
def test_stream_analysis_request_construction(fake_client_factory):
    client = fake_client_factory([["chunk one ", "chunk two"]])
    out = "".join(
        demo_logic.stream_analysis(
            client, "THE VERIFIED CONTRACT BODY", "my rule", "my note"
        )
    )
    assert out == "chunk one chunk two"
    (call,) = client.calls
    assert call["model"] == demo_logic.MODEL_NAME
    assert call["max_tokens"] == demo_logic.BASE_MAX_TOKENS
    assert call["stream"] is True
    # The system prompt is exactly the injected (verified) contract body...
    assert call["system"] == "THE VERIFIED CONTRACT BODY"
    # ...and the user payload stays in the single user message.
    assert len(call["messages"]) == 1
    assert call["messages"][0]["role"] == "user"
    assert "my rule" in call["messages"][0]["content"]
    assert "my note" in call["messages"][0]["content"]
    assert "my rule" not in call["system"]


def test_user_message_never_asks_for_score():
    msg = demo_logic.build_user_message("r", "n")
    assert "Do not score, approve, or assign a PASS/FAIL status." in msg


# --- 8. missing/invalid configuration handled ---------------------------
class _RaisingMapping:
    def __getitem__(self, key):
        raise FileNotFoundError("no secrets file")


@pytest.mark.parametrize(
    "mapping",
    [
        {},
        {"ANTHROPIC_API_KEY": ""},
        {"ANTHROPIC_API_KEY": "   "},
        {"ANTHROPIC_API_KEY": demo_logic.EXAMPLE_KEY_PLACEHOLDER},
        {"ANTHROPIC_API_KEY": 12345},
        {"OTHER_KEY": "value"},
        _RaisingMapping(),
    ],
)
def test_resolve_api_key_rejects_unusable_configs(mapping):
    assert demo_logic.resolve_api_key(mapping) is None


def test_resolve_api_key_accepts_and_strips_a_real_looking_value():
    assert (
        demo_logic.resolve_api_key({"ANTHROPIC_API_KEY": " test-value \n"})
        == "test-value"
    )


def test_create_client_sets_timeout_and_bounded_retries():
    client = demo_logic.create_client("test-value")
    assert isinstance(client, anthropic.Anthropic)
    assert client.max_retries == demo_logic.MAX_RETRIES == 2
    assert client.timeout == demo_logic.REQUEST_TIMEOUT_SECONDS


# --- 9. over-limit inputs rejected before any client call ---------------
def test_validate_inputs_missing_fields():
    codes = {e["code"] for e in demo_logic.validate_inputs("", "")}
    assert codes == {"missing_rule", "missing_note"}
    codes = {e["code"] for e in demo_logic.validate_inputs("  \n ", "note")}
    assert codes == {"missing_rule"}


def test_validate_inputs_over_limit():
    long_rule = "r" * (demo_logic.MAX_RULE_CHARS + 1)
    long_note = "n" * (demo_logic.MAX_NOTE_CHARS + 1)
    errors = demo_logic.validate_inputs(long_rule, long_note)
    by_code = {e["code"]: e for e in errors}
    assert set(by_code) == {"rule_too_long", "note_too_long"}
    assert by_code["rule_too_long"]["length"] == demo_logic.MAX_RULE_CHARS + 1
    assert by_code["rule_too_long"]["limit"] == demo_logic.MAX_RULE_CHARS
    assert by_code["note_too_long"]["limit"] == demo_logic.MAX_NOTE_CHARS


def test_validate_inputs_at_limit_is_accepted():
    rule = "r" * demo_logic.MAX_RULE_CHARS
    note = "n" * demo_logic.MAX_NOTE_CHARS
    assert demo_logic.validate_inputs(rule, note) == []


# --- 10. provider error categories map to safe messages -----------------
def test_classify_provider_error_categories(api_error_factory):
    cases = [
        (api_error_factory(anthropic.AuthenticationError, 401), "auth"),
        (api_error_factory(anthropic.PermissionDeniedError, 403), "auth"),
        (api_error_factory(anthropic.RateLimitError, 429), "rate_limit"),
        (api_error_factory(anthropic.BadRequestError, 400), "invalid_request"),
        (
            api_error_factory(anthropic.UnprocessableEntityError, 422),
            "invalid_request",
        ),
        (
            api_error_factory(anthropic.InternalServerError, 500),
            "provider",
        ),
        (ValueError("anything unexpected"), "provider"),
    ]
    for exc, expected in cases:
        assert demo_logic.classify_provider_error(exc) == expected, exc

    request = __import__("httpx").Request(
        "POST", "https://api.anthropic.com/v1/messages"
    )
    timeout_exc = anthropic.APITimeoutError(request=request)
    assert demo_logic.classify_provider_error(timeout_exc) == "timeout"
    conn_exc = anthropic.APIConnectionError(
        message="conn down", request=request
    )
    assert demo_logic.classify_provider_error(conn_exc) == "connection"


def test_every_category_has_a_message_key():
    from ui_text import UI_TEXT

    for lang in ("bg", "en"):
        for category in demo_logic.ERROR_CATEGORIES:
            assert f"err_{category}" in UI_TEXT[lang]


# --- 11. gating filter behaviour (unit side) ----------------------------
def test_gating_filter_uses_fresh_nonce_each_call(fake_client_factory):
    markers = []
    for _ in range(2):
        client = fake_client_factory(["output text"])
        demo_logic.apply_gating_filter(client, "base text")
        (call,) = client.calls
        found = re.findall(r"<<<TEXT-([0-9a-f]{32})", call["system"])
        assert found, "nonce open marker missing from filter system prompt"
        markers.append(found[0])
    assert markers[0] != markers[1]


def test_gating_filter_wraps_base_text_in_markers(fake_client_factory):
    client = fake_client_factory(["ok"])
    demo_logic.apply_gating_filter(client, "THE BASE", nonce="ab" * 16)
    (call,) = client.calls
    open_marker, close_marker = demo_logic.make_nonce_markers("ab" * 16)
    assert call["messages"][0]["content"] == (
        f"{open_marker}\nTHE BASE\n{close_marker}"
    )
    assert call["model"] == demo_logic.MODEL_NAME
    assert call["max_tokens"] == demo_logic.FILTER_MAX_TOKENS
    assert "stream" not in call or not call["stream"]


def test_gating_filter_strips_only_exact_echoed_markers(fake_client_factory):
    nonce = "cd" * 16
    open_marker, close_marker = demo_logic.make_nonce_markers(nonce)
    echoed = f"{open_marker}\nfiltered body\n{close_marker}"
    client = fake_client_factory([echoed])
    assert (
        demo_logic.apply_gating_filter(client, "base", nonce=nonce)
        == "filtered body"
    )


def test_gating_filter_preserves_foreign_marker_like_text(fake_client_factory):
    # A marker with a DIFFERENT nonce is not ours and must not be stripped.
    foreign = "<<<TEXT-" + "9" * 32 + "\nbody\nTEXT-" + "9" * 32 + ">>>"
    client = fake_client_factory([foreign])
    result = demo_logic.apply_gating_filter(client, "base", nonce="ef" * 16)
    assert result == foreign


def test_strip_nonce_markers_leaves_mid_text_occurrences():
    open_marker, close_marker = demo_logic.make_nonce_markers("12" * 16)
    text = f"start {open_marker} middle {close_marker} end"
    assert (
        demo_logic.strip_nonce_markers(text, open_marker, close_marker)
        == text
    )


def test_gating_filter_does_not_mutate_base_text(fake_client_factory):
    base = "The base response.\nUntouched."
    client = fake_client_factory(["something else entirely"])
    filtered = demo_logic.apply_gating_filter(client, base)
    assert filtered == "something else entirely"
    assert base == "The base response.\nUntouched."


def test_gating_filter_failure_propagates_for_caller_fallback(
    fake_client_factory, api_error_factory
):
    client = fake_client_factory(
        [api_error_factory(anthropic.RateLimitError, 429)]
    )
    with pytest.raises(anthropic.RateLimitError):
        demo_logic.apply_gating_filter(client, "base")
