# TinaAI – AI Transaction Investigation Note Assistant

[![CI](https://github.com/G0dlike8888/TinaAI/actions/workflows/ci.yml/badge.svg)](https://github.com/G0dlike8888/TinaAI/actions/workflows/ci.yml)

**The context.** Banks, payment institutions and other fintech companies run transaction
monitoring and fraud-detection systems. When a rule fires (for example an unusual transfer
pattern, a card used in two countries within an hour, or many small payments just under a
limit), the system raises an alert and a human analyst investigates it. The analyst then writes
an **investigation note**: what was checked, what was found, and why the alert was closed or
escalated. These notes are read later by colleagues, quality reviewers, auditors and regulators,
so a note that leaves out facts or does not support its own conclusion is a real operational
and compliance risk.

**What TinaAI does.** It helps the analyst check the note before it is submitted. It is a
local, bilingual (English / Bulgarian) advisory assistant that reviews an investigation note
against the rule or alert context that triggered it. Given a synthetic rule and a synthetic note,
it reports which facts the note supports, the material documentation gaps, and whether the
documented evidence carries the analyst's stated reasoning.

It is **not** a decision system: it does not classify activity, score or approve notes, or make
closure, escalation or filing decisions. It is not an AML or compliance system. Every decision
stays with the human reviewer. All bundled rules, notes and scenarios are fictional.

This is the exam project for the SoftUni course **AI-Assisted Development**. It was built with
Claude Code (`claude-opus-5`, `claude-fable-5`) and Codex (`gpt-5.6-sol`), with architecture
reviews by other models (Qwen, KAT, DeepSeek, Gemini, Kimi). The exam document describes each
module, the key prompts, the tests and a tool comparison.

## Quick start

**Windows:** double-click `START-ASSISTANT.bat`. It sets up Python and the environment, asks for
your Anthropic API key (hidden, never reused from disk) and opens the app in the browser.

**macOS / Linux:**

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp "03 Demo/.streamlit/secrets.toml.example" "03 Demo/.streamlit/secrets.toml"
# edit 03 Demo/.streamlit/secrets.toml and paste your own Anthropic API key
cd "03 Demo" && python -m streamlit run app.py
```

The key file is git-ignored; never commit or share it. Without a key the app still opens, shows
a warning and keeps the Analyze button disabled. Step-by-step guides for non-technical readers:
`START-HERE-EN.md` and `START-HERE-BG.md`.

## Tests

```
python -m pytest
```

90 offline tests: no API key, no network, no cost. They cover contract integrity and tampering,
input limits, request construction against a mocked client, error mapping, secret scanning,
bilingual text parity, evidence-figure fidelity and rendered UI flows (Streamlit AppTest).

GitHub Actions runs the same suite on Ubuntu and Windows on every push and pull request
(`.github/workflows/ci.yml`).

## Modules

| Module | Where | What it does |
|---|---|---|
| Behavioural contract | `01 Contract/` | The assistant's rules: advisory scope, evidence standard, no invention, refusal boundaries, human decision ownership |
| Contract integrity | `03 Demo/contract_integrity.py` | Verifies the contract byte for byte against a SHA-256-pinned reference on every run; any mismatch stops the app, with no fallback prompt |
| Input and API layer | `03 Demo/demo_logic.py` | Input limits checked before any call, the Anthropic request, timeout and retries, safe error messages, the optional experimental filter |
| Bilingual UI | `03 Demo/app.py`, `ui_text.py` | Streamlit interface in English and Bulgarian, bundled scenarios and Custom mode |
| Tests | `tests/` | The offline pytest suite above |
| Evaluation records | `04 Evidence and Records/` | Pre-registered success bars, locked marking key, held-out result |
| Claude Skill | `02 Skill/` | The same contract packaged as a Claude Skill |
| Windows launcher | `START-ASSISTANT.bat`, `tools/launcher.ps1` | One-click setup and start for non-technical users |

## Evaluation and limitations

- On a locked held-out set of 50 notes the contract missed both of its pre-registered targets
  (Finding 50.0% vs ≥ 60%, Restraint 55.2% vs ≤ 25%). Details:
  [`docs/PROJECT-DETAILS.md`](docs/PROJECT-DETAILS.md).
- The 90 tests check the engineering behaviour, not the quality of the model's answers.
- Use only synthetic or fully anonymised material. Never paste real notes, customer data,
  account numbers or names.

## More detail

The full project description, methodology, evidence status, safeguards and audit history are in
[`docs/PROJECT-DETAILS.md`](docs/PROJECT-DETAILS.md). Technical run notes and troubleshooting:
`03 Demo/HOW_TO_RUN.md`.

## Licence

MIT, see `LICENSE`.
