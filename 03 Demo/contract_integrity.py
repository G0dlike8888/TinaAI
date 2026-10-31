"""Contract integrity — loading and verification of the pinned contract.

This module is deliberately free of Streamlit imports so the entire
fail-closed loading path can be tested without executing the UI.

What it enforces, in order:

1. Both contract artifacts exist on disk:
   - the canonical source  ``01 Contract/Template v0.8 - Assistant Contract.md``
   - the shipped reference ``02 Skill/investigation-note-quality-assistant/
     reference/CONTRACT-v0.8.md`` (the evaluated body, hash-pinned)
2. The shipped reference verifies exactly as described by the Skill's
   ``reference/VERIFY.md``: read as UTF-8 text, hash the UTF-8 encoding of
   that text, expect 31,438 characters / 31,641 bytes / no trailing newline /
   SHA-256 ``2f574a66…e58363``.
3. The body derived from the canonical source (YAML frontmatter stripped by
   the one rule documented below, then ``.strip()``) equals the shipped
   reference text exactly, character for character.

Any failure raises :class:`ContractIntegrityError` — the demo refuses to
start or analyze. There is no fallback contract anywhere in this codebase,
hardcoded or paraphrased, by design: a demo running an unverified contract
would silently detach itself from the evidence record.

If verification fails, the fix is never to change the expected values here.
Per VERIFY.md: find out which copy changed and why.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

# Pinned values for the evaluated contract body. Provenance: the Skill's
# reference/VERIFY.md and the evidence records in "04 Evidence and Records".
# These constants describe the artifact; they are not tunable configuration.
PINNED_SHA256 = "2f574a661733ffdc54fd48a13197e37e940bb1e759b7d0a70d8e4be512e58363"
PINNED_CHAR_COUNT = 31_438
PINNED_BYTE_COUNT = 31_641

_DEMO_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = _DEMO_DIR.parent
CANONICAL_CONTRACT_PATH = (
    PROJECT_ROOT / "01 Contract" / "Template v0.8 - Assistant Contract.md"
)
SHIPPED_REFERENCE_PATH = (
    PROJECT_ROOT
    / "02 Skill"
    / "investigation-note-quality-assistant"
    / "reference"
    / "CONTRACT-v0.8.md"
)

# Guidance appended to every integrity error. It must never suggest editing
# the expected hash/counts — VERIFY.md: "Do not update the expected hash to
# make the mismatch go away. Find out which copy changed and why."
_MISMATCH_GUIDANCE = (
    "The demo refuses to run on an unverified contract and has no fallback "
    "text. Do not update the expected hash or counts to make this pass — "
    "per the Skill's reference/VERIFY.md, find out which copy changed and "
    "why (the most likely accidental corruption is an editor or Git adding "
    "a trailing newline)."
)


class ContractIntegrityError(RuntimeError):
    """The pinned contract could not be loaded and verified.

    Raised for: missing files, character/byte-count mismatch, hash mismatch,
    unexpected trailing content, or a canonical body that no longer equals
    the shipped evaluated reference.
    """


def strip_frontmatter(text: str) -> str:
    """Strip YAML frontmatter using the one rule the pinned hash was built with.

    The rule (unchanged from the original demo and from the Skill build
    record): if the document starts with ``---``, split on ``---`` at most
    twice and keep everything after the second marker; otherwise return the
    text unchanged. This is intentionally the exact historical rule — do not
    "improve" it, because the derived body is verified against the pinned
    hash afterwards and any divergence fails closed there.
    """
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2]
    return text


def derive_contract_body(raw_source_text: str) -> str:
    """Frontmatter-stripped, whitespace-stripped body of the canonical source."""
    return strip_frontmatter(raw_source_text).strip()


def _verify_reference_bytes(reference_path: Path, raw: bytes) -> str:
    """Verify the shipped reference exactly as VERIFY.md describes.

    Returns the decoded text on success; raises ContractIntegrityError on
    any deviation.
    """
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ContractIntegrityError(
            f"Shipped contract reference is not valid UTF-8: {reference_path}. "
            + _MISMATCH_GUIDANCE
        ) from exc

    problems = []
    if raw.startswith(b"\xef\xbb\xbf"):
        problems.append("a UTF-8 BOM is present (none expected)")
    if raw.endswith(b"\n") or raw.endswith(b"\r"):
        problems.append(
            "trailing end-of-line content was added (the file as shipped "
            "does not end in a newline)"
        )
    if len(text) != PINNED_CHAR_COUNT:
        problems.append(
            f"character count is {len(text):,}, expected {PINNED_CHAR_COUNT:,}"
        )
    if len(raw) != PINNED_BYTE_COUNT:
        problems.append(
            f"byte count is {len(raw):,}, expected {PINNED_BYTE_COUNT:,}"
        )
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if digest != PINNED_SHA256:
        problems.append(
            f"SHA-256 of the UTF-8 text is {digest}, expected {PINNED_SHA256}"
        )
    if problems:
        raise ContractIntegrityError(
            f"Shipped contract reference failed verification "
            f"({reference_path}): " + "; ".join(problems) + ". "
            + _MISMATCH_GUIDANCE
        )
    return text


def load_verified_contract(
    canonical_path: Path = CANONICAL_CONTRACT_PATH,
    reference_path: Path = SHIPPED_REFERENCE_PATH,
) -> str:
    """Load, verify and return the pinned contract body.

    The returned string is the text sent verbatim as the system prompt.
    Every failure mode raises :class:`ContractIntegrityError`; this function
    never returns a substitute or partial contract.
    """
    if not canonical_path.is_file():
        raise ContractIntegrityError(
            f"Pinned contract source not found: {canonical_path}. The demo "
            "must live inside the project folder structure, with '03 Demo/' "
            "and '01 Contract/' as siblings — it refuses to fall back to a "
            "hardcoded or paraphrased contract."
        )
    if not reference_path.is_file():
        raise ContractIntegrityError(
            f"Shipped contract reference not found: {reference_path}. "
            "Without the evaluated reference body the loaded contract "
            "cannot be verified, and the demo refuses to run unverified."
        )

    try:
        raw_reference = reference_path.read_bytes()
    except OSError as exc:
        raise ContractIntegrityError(
            f"Shipped contract reference could not be read: {reference_path}. "
            "The file may be locked by another process or its permissions "
            "may have changed. " + _MISMATCH_GUIDANCE
        ) from exc
    reference_text = _verify_reference_bytes(reference_path, raw_reference)

    try:
        raw_source = canonical_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ContractIntegrityError(
            f"Pinned contract source is not valid UTF-8: {canonical_path}. "
            + _MISMATCH_GUIDANCE
        ) from exc
    except OSError as exc:
        raise ContractIntegrityError(
            f"Pinned contract source could not be read: {canonical_path}. "
            "The file may be locked by another process or its permissions "
            "may have changed. " + _MISMATCH_GUIDANCE
        ) from exc

    derived_body = derive_contract_body(raw_source)
    if derived_body != reference_text:
        raise ContractIntegrityError(
            "The contract body derived from the canonical source does not "
            f"match the shipped evaluated reference ({canonical_path} vs "
            f"{reference_path}): derived body is {len(derived_body):,} "
            f"characters, reference is {len(reference_text):,}. "
            + _MISMATCH_GUIDANCE
        )
    return derived_body
