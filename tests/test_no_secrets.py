"""No forbidden secret pattern in the project's shareable text files.

Covers required test area 12. Files that .gitignore excludes from tracking
(the real secrets.toml, virtual environments, caches) are skipped — the
scan asserts what a published copy of the folder would contain.
"""
import re
from pathlib import Path

SECRET_PATTERNS = [
    re.compile(r"sk-ant-[A-Za-z0-9_\-]{16,}"),
    re.compile(r"sk-[A-Za-z0-9]{32,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)authorization:\s*bearer\s+[A-Za-z0-9_\-.]{20,}"),
]

SKIP_DIR_NAMES = {
    ".venv", "venv", "__pycache__", ".pytest_cache", ".git",
    ".mypy_cache", ".ruff_cache", ".idea", ".vscode",
}
SKIP_FILE_NAMES = {"secrets.toml"}
TEXT_SUFFIXES = {
    ".py", ".md", ".toml", ".txt", ".json", ".example", ".cfg", ".ini",
    ".yaml", ".yml",
}


def _scannable_files(root: Path):
    for path in root.rglob("*"):
        if any(part in SKIP_DIR_NAMES for part in path.parts):
            continue
        if not path.is_file():
            continue
        if path.name in SKIP_FILE_NAMES:
            continue
        # Suffix-less tracked text files (LICENSE, .gitignore, dotfiles)
        # are scanned too — a credential pasted into any of them would
        # ship in a published copy just the same.
        if path.suffix.lower() in TEXT_SUFFIXES or path.suffix == "":
            yield path


def test_no_forbidden_secret_pattern_in_text_files(project_root):
    offenders = []
    for path in _scannable_files(project_root):
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(content):
                offenders.append((str(path), pattern.pattern))
    assert not offenders, f"secret-like content found: {offenders}"


def test_gitignore_protects_secrets_and_noise(project_root):
    gitignore = (project_root / ".gitignore").read_text(encoding="utf-8")
    for required in (
        ".streamlit/secrets.toml",
        ".env",
        ".venv/",
        "__pycache__/",
        ".pytest_cache/",
        ".coverage",
    ):
        assert required in gitignore, f".gitignore must exclude {required}"
    # The whole .streamlit directory must NOT be ignored: the committed
    # example file lives there.
    for line in gitignore.splitlines():
        stripped = line.strip()
        assert stripped not in (".streamlit", ".streamlit/"), (
            ".gitignore must not exclude the entire .streamlit directory"
        )


def test_secrets_example_contains_no_key_like_value(demo_dir):
    example = (demo_dir / ".streamlit" / "secrets.toml.example").read_text(
        encoding="utf-8"
    )
    assert "PASTE-YOUR-OWN-KEY-HERE" in example
    for pattern in SECRET_PATTERNS:
        assert not pattern.search(example)
