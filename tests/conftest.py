"""Shared fixtures for the offline test suite.

No test in this suite makes a real Anthropic request or needs an API key.
The Anthropic client is always replaced by FakeClient (below) or blocked
outright.
"""
from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

import httpx
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEMO_DIR = PROJECT_ROOT / "03 Demo"
APP_PATH = DEMO_DIR / "app.py"

# Make the demo modules importable exactly as app.py imports them.
if str(DEMO_DIR) not in sys.path:
    sys.path.insert(0, str(DEMO_DIR))


@pytest.fixture
def project_root() -> Path:
    return PROJECT_ROOT


@pytest.fixture
def demo_dir() -> Path:
    return DEMO_DIR


@pytest.fixture
def app_path() -> Path:
    return APP_PATH


class FakeStreamChunk:
    def __init__(self, text: str):
        self.type = "content_block_delta"
        self.delta = SimpleNamespace(text=text)


class FakeClient:
    """Scripted stand-in for anthropic.Anthropic.

    ``script`` is consumed one item per messages.create() call:
      - an Exception instance is raised;
      - with stream=True, a list of strings becomes streamed chunks;
      - otherwise a string becomes a single text content block.
    Every call's kwargs are recorded in ``calls``.
    """

    def __init__(self, script):
        self.calls: list[dict] = []
        self._script = list(script)
        self.messages = SimpleNamespace(create=self._create)

    def _create(self, **kwargs):
        self.calls.append(kwargs)
        if not self._script:
            raise AssertionError(
                "FakeClient received more API calls than scripted"
            )
        item = self._script.pop(0)
        if isinstance(item, BaseException):
            raise item
        if kwargs.get("stream"):
            return iter(FakeStreamChunk(t) for t in item)
        return SimpleNamespace(
            content=[SimpleNamespace(type="text", text=item)]
        )


@pytest.fixture
def fake_client_factory():
    return FakeClient


def make_api_status_error(cls, status_code: int):
    """Build a real anthropic APIStatusError subclass instance for tests."""
    request = httpx.Request("POST", "https://api.anthropic.com/v1/messages")
    response = httpx.Response(status_code, request=request)
    return cls("scripted test error", response=response, body=None)


@pytest.fixture
def api_error_factory():
    return make_api_status_error
