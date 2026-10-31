# How to run the demo (AI Investigation Note Quality Assistant)

> **If you have never run anything from a terminal, read `START-HERE-EN.md` in the project root
> instead** (`START-HERE-BG.md` is the same guide in Bulgarian). It covers the same ground from
> zero —
> installing Python, opening a terminal, obtaining an API key, creating the secrets file — with
> every error message explained. This file is the condensed technical version.

The demo is a Streamlit app, file `app.py`, with its logic split across three
small modules (`contract_integrity.py`, `demo_logic.py`, `ui_text.py`). The
instructions below apply to anyone who has a copy of the project folder —
replace `<project-folder>` with wherever you placed the folder yourself (for
example `C:\Users\you\Projects\investigation-note-assistant`, or any other
location).

**Folder layout matters.** At every start (and every rerun) the app loads the
pinned contract from `../01 Contract/Template v0.8 - Assistant Contract.md`
and verifies it byte-for-byte against the evaluated reference body in
`../02 Skill/investigation-note-quality-assistant/reference/CONTRACT-v0.8.md`
(expected SHA-256 `2f574a66…e58363`, 31,438 characters). Keep `01 Contract/`,
`02 Skill/` and `03 Demo/` together, at the same level, or the app will refuse
to start — it has no hardcoded fallback contract, on purpose. If the integrity
check fails, do not edit the contract files or the expected hash; see
`02 Skill/investigation-note-quality-assistant/reference/VERIFY.md`.

---

## 1. One-time setup (first time only)

Open a terminal (PowerShell / Command Prompt on Windows, Terminal on
macOS/Linux) and check that Python is available:

```
python --version
```

On macOS/Linux the command is sometimes `python3 --version` instead. If neither
works, install Python from python.org first (on Windows, check "Add to PATH"
during installation). The project needs **Python 3.10 or newer** — the pinned
packages in `requirements.txt` do not install on older versions.

From the project folder (the one containing `requirements.txt`), create a
virtual environment and install the dependencies:

```
cd "<project-folder>"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

(On macOS/Linux: `python3 -m venv .venv`, then `source .venv/bin/activate`.)

If you prefer not to use a virtual environment, `pip install -r
requirements.txt` into your global Python also works — the venv just keeps the
project self-contained.

---

## 2. API key (one-time, before first run)

> Note: this section describes the **manual** path, where you create a persistent secrets file
> yourself. The one-click launcher (`START-ASSISTANT.bat`) does not use it that way — it asks for
> the key on every start, writes this file for the session, and deletes it when the app stops.

The app reads the key from `st.secrets["ANTHROPIC_API_KEY"]`, which comes from:

```
<project-folder>\03 Demo\.streamlit\secrets.toml
```

Copy the provided example file and put your own key in the copy:

```
copy "03 Demo\.streamlit\secrets.toml.example" "03 Demo\.streamlit\secrets.toml"
```

Then edit `secrets.toml` and replace the `PASTE-YOUR-OWN-KEY-HERE` placeholder
with your own Anthropic API key. Everyone who runs the demo uses **their own**
key — get one from console.anthropic.com (requires your own Anthropic
account/registration).

Without a valid-looking key the app still starts and renders fully; it shows a
key warning and keeps the Analyze button disabled, so no request can be
attempted. If the key is wrong or expired, the app shows a concise
authentication error (never the raw provider response) — get a fresh key from
the console and overwrite the value in the same file.

**Never share the contents of this file with anyone else or paste it into a
chat** — it contains a personal, billable credential and should never leave
your local machine. The repository's `.gitignore` excludes `secrets.toml` from
version control; only the placeholder `secrets.toml.example` is meant to be
shared.

---

## 3. Running the demo (every time after setup)

Open a terminal in the `03 Demo` folder (where `app.py` is located — Streamlit
reads `.streamlit/secrets.toml` relative to the folder you run from):

```
cd "<project-folder>\03 Demo"
streamlit run app.py
```

If `streamlit` is not recognized as a command (a PATH issue, or the venv is not
activated), use:

```
python -m streamlit run app.py
```

On a successful start, Streamlit automatically opens a browser tab (usually at
`http://localhost:8501`). If it doesn't open on its own, copy the address from
the terminal.

To stop the demo: press `Ctrl+C` in the terminal while it's running.

**Input limits.** The rule/alert field accepts up to 4,000 characters and the
note field up to 16,000. Over-limit input is rejected with a message before
any API call — the app never truncates or summarizes your text for you. All
bundled content is synthetic; never paste real investigation or customer data.

---

## 4. Running the offline test suite (optional, no API key needed)

From the project folder:

```
cd "<project-folder>"
python -m pytest
```

The suite (in `tests/`) verifies the contract-integrity chain, the input
validation, the error mapping, the gating-filter mechanics and the rendered
app flows — entirely offline, against a mocked client. It makes **no**
Anthropic requests, needs **no** API key, and costs nothing to run.

---

## 5. Quick troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `streamlit: command not found` | Packages not installed, or PATH doesn't see them | Step 1 above; if needed, `python -m streamlit run app.py` |
| App shows a red "Contract integrity check failed" box | The contract files were moved, edited, or a copy tool rewrote them (commonly: an added trailing newline) | Restore the original `01 Contract/` and `02 Skill/` files. Do **not** edit the expected hash — see `VERIFY.md` |
| 🔑 "No Anthropic API key found" warning; Analyze disabled | `secrets.toml` missing, empty, or still the placeholder | Step 2 above |
| In-app authentication error after clicking Analyze | Key in `secrets.toml` is wrong, expired, or revoked | Get your own key from console.anthropic.com → Step 2 |
| Page opens but is blank / import error | A package is missing | `pip install -r requirements.txt` again, in the same environment you run from |
| Over-limit message when clicking Analyze | Input longer than the field limit | Shorten the text yourself — the app never truncates it for you |
| `python -m pytest` reports every test passing but then exits with `PermissionError: [WinError 5] ... pytest-of-<user>\pytest-current` | Windows-only: a stale symlink in your global temp folder that pytest cannot remove without elevation. The tests themselves already passed | Run with your own temp folder: `python -m pytest --basetemp=.pytest-tmp` (that path is git-ignored), or delete `%LOCALAPPDATA%\Temp\pytest-of-<user>` from an elevated terminal |
| The result disappears when you switch language / toggle the gating checkbox | Old bug — already fixed (state persistence) | Make sure you're running the latest version of `app.py` |
| `streamlit` / `pytest` stop working after the project folder was moved or renamed | A virtual environment records absolute paths, so its console-script shims (`.venv\Scripts\streamlit.exe`) break on a rename — the interpreter itself (`.venv\Scripts\python.exe`) still works | Either invoke through the interpreter (`.venv\Scripts\python.exe -m streamlit run app.py`), or delete `.venv` and recreate it as in step 1 |

---

*Instructions for the local demo of "AI Investigation Note Quality Assistant".
Not part of the canonical project documents.*
