"""Contract integrity: existence, pinned length/hash, derived-body equality,
fail-closed behaviour, and the absence of any fallback contract in code.

Covers required test areas 1-5.
"""
import hashlib
import shutil

import pytest

import contract_integrity as ci


# --- 1. canonical contract source exists --------------------------------
def test_canonical_contract_source_exists():
    assert ci.CANONICAL_CONTRACT_PATH.is_file()


# --- 2. shipped reference exists and matches expected length/hash -------
def test_shipped_reference_exists():
    assert ci.SHIPPED_REFERENCE_PATH.is_file()


def test_shipped_reference_matches_pinned_values():
    raw = ci.SHIPPED_REFERENCE_PATH.read_bytes()
    text = raw.decode("utf-8")
    assert len(text) == ci.PINNED_CHAR_COUNT == 31_438
    assert len(raw) == ci.PINNED_BYTE_COUNT == 31_641
    assert (
        hashlib.sha256(text.encode("utf-8")).hexdigest() == ci.PINNED_SHA256
    )
    # As shipped: no trailing newline, no BOM, LF-only line endings.
    assert not raw.endswith(b"\n")
    assert not raw.startswith(b"\xef\xbb\xbf")
    assert b"\r\n" not in raw


# --- 3. derived body equals the shipped reference exactly ---------------
def test_derived_body_equals_shipped_reference():
    raw_source = ci.CANONICAL_CONTRACT_PATH.read_text(encoding="utf-8")
    derived = ci.derive_contract_body(raw_source)
    reference = ci.SHIPPED_REFERENCE_PATH.read_text(encoding="utf-8")
    assert derived == reference


def test_load_verified_contract_returns_pinned_body():
    body = ci.load_verified_contract()
    assert len(body) == ci.PINNED_CHAR_COUNT
    assert (
        hashlib.sha256(body.encode("utf-8")).hexdigest() == ci.PINNED_SHA256
    )


def test_strip_frontmatter_rule_is_the_pinned_one():
    # The one explicit rule: leading '---' splits the document at the second
    # '---'; a document without leading '---' passes through unchanged.
    assert ci.strip_frontmatter("---\na: 1\n---\nbody") == "\nbody"
    assert ci.strip_frontmatter("no frontmatter here") == "no frontmatter here"
    # Unclosed frontmatter is not silently mangled...
    assert ci.strip_frontmatter("---\nonly one marker") == "---\nonly one marker"
    # ...and derive adds only whitespace stripping.
    assert ci.derive_contract_body("---\na: 1\n---\n\nbody\n") == "body"


# --- 4. missing or modified contract causes a fail-closed error ---------
@pytest.fixture
def contract_tree(tmp_path):
    """A temporary copy of both contract artifacts, safe to corrupt."""
    canonical = tmp_path / "01 Contract" / ci.CANONICAL_CONTRACT_PATH.name
    reference = tmp_path / "reference" / ci.SHIPPED_REFERENCE_PATH.name
    canonical.parent.mkdir(parents=True)
    reference.parent.mkdir(parents=True)
    shutil.copyfile(ci.CANONICAL_CONTRACT_PATH, canonical)
    shutil.copyfile(ci.SHIPPED_REFERENCE_PATH, reference)
    return canonical, reference


def test_valid_tree_loads(contract_tree):
    canonical, reference = contract_tree
    body = ci.load_verified_contract(canonical, reference)
    assert hashlib.sha256(body.encode("utf-8")).hexdigest() == ci.PINNED_SHA256


def test_missing_canonical_fails_closed(contract_tree):
    canonical, reference = contract_tree
    canonical.unlink()
    with pytest.raises(ci.ContractIntegrityError):
        ci.load_verified_contract(canonical, reference)


def test_missing_reference_fails_closed(contract_tree):
    canonical, reference = contract_tree
    reference.unlink()
    with pytest.raises(ci.ContractIntegrityError):
        ci.load_verified_contract(canonical, reference)


def test_modified_canonical_body_fails_closed(contract_tree):
    canonical, reference = contract_tree
    text = canonical.read_text(encoding="utf-8")
    canonical.write_text(
        text.replace("advisory", "adversary", 1), encoding="utf-8"
    )
    with pytest.raises(ci.ContractIntegrityError):
        ci.load_verified_contract(canonical, reference)


def test_reference_trailing_newline_fails_closed(contract_tree):
    canonical, reference = contract_tree
    reference.write_bytes(reference.read_bytes() + b"\n")
    with pytest.raises(ci.ContractIntegrityError) as excinfo:
        ci.load_verified_contract(canonical, reference)
    assert "trailing" in str(excinfo.value)


def test_reference_truncation_fails_closed(contract_tree):
    canonical, reference = contract_tree
    reference.write_bytes(reference.read_bytes()[:-100])
    with pytest.raises(ci.ContractIntegrityError):
        ci.load_verified_contract(canonical, reference)


def test_reference_content_tamper_same_length_fails_closed(contract_tree):
    canonical, reference = contract_tree
    raw = reference.read_bytes()
    tampered = raw.replace(b"advisory", b"adversary"[:8], 1)
    assert len(tampered) == len(raw)
    reference.write_bytes(tampered)
    with pytest.raises(ci.ContractIntegrityError) as excinfo:
        ci.load_verified_contract(canonical, reference)
    assert "SHA-256" in str(excinfo.value)


def test_canonical_trailing_content_fails_closed(contract_tree):
    canonical, reference = contract_tree
    with canonical.open("a", encoding="utf-8") as fh:
        fh.write("\n\nAppended stray paragraph.")
    with pytest.raises(ci.ContractIntegrityError):
        ci.load_verified_contract(canonical, reference)


def test_unreadable_reference_fails_closed(contract_tree, monkeypatch):
    canonical, reference = contract_tree

    def _locked(self):
        raise PermissionError("file locked by another process")

    monkeypatch.setattr(type(reference), "read_bytes", _locked)
    with pytest.raises(ci.ContractIntegrityError) as excinfo:
        ci.load_verified_contract(canonical, reference)
    assert "could not be read" in str(excinfo.value)


def test_error_never_suggests_changing_the_expected_hash(contract_tree):
    canonical, reference = contract_tree
    reference.write_bytes(reference.read_bytes() + b"\n")
    with pytest.raises(ci.ContractIntegrityError) as excinfo:
        ci.load_verified_contract(canonical, reference)
    message = str(excinfo.value)
    assert "Do not update the expected hash" in message
    # The error carries counts and paths, never the contract text itself.
    assert "Identity and boundary" not in message


# --- 5. no hardcoded fallback contract exists in demo code --------------
def test_no_hardcoded_fallback_contract_in_demo_code(demo_dir):
    # Distinctive contract-body phrases that legitimately exist only in the
    # pinned .md artifacts. None may appear in any demo .py file.
    markers = [
        "Anti-luck rule",
        "Identity and boundary",
        "the response is the entire output",
        "pinned-candidate",
        "Consolidated prohibitions",
        "Freeze status",
    ]
    for py_file in demo_dir.glob("*.py"):
        source = py_file.read_text(encoding="utf-8")
        for marker in markers:
            assert marker not in source, (
                f"{py_file.name} contains contract-body text ({marker!r}) — "
                "possible hardcoded fallback"
            )


def test_load_failure_raises_rather_than_returning_substitute(tmp_path):
    missing = tmp_path / "nowhere.md"
    with pytest.raises(ci.ContractIntegrityError):
        ci.load_verified_contract(missing, missing)
