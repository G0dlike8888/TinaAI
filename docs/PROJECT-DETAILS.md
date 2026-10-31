# TinaAI – AI Transaction Investigation Note Assistant

A local, bilingual (English / Bulgarian) advisory MVP that reviews an investigation note against
the rule or alert context that triggered it. Given a synthetic rule and a synthetic note, the
assistant reports which facts the note actually supports, highlights genuinely material
documentation gaps, and examines whether the documented evidence carries the human analyst's
stated reasoning.

What it deliberately is **not**:

- It does not classify activity, and does not determine whether activity is fraudulent,
  suspicious or legitimate.
- It does not score, grade or approve notes.
- It does not make closure, escalation, restriction or filing decisions.
- It is not an AML or compliance system, and it performs no transaction monitoring and no case
  management.
- Every investigative and operational decision stays with the human reviewer.

Financial-investigation, AML and anti-fraud contexts appear here only as **synthetic
demonstration domains**. All bundled rules, notes and scenarios are fictional, the distributable
folder contains no real customer, company or case data, and nothing here claims to be an
operational AML system.

## SoftUni exam submission

This repository is the exam project for the SoftUni course **AI-Assisted Development**. It was
built with AI coding tools: Claude Code (`claude-opus-5`, `claude-fable-5`) for the
implementation, tests, launcher and audits; Codex (`gpt-5.6-sol`) for prompt engineering and
coordination; and reviews by other models (Qwen, KAT, DeepSeek, Gemini, Kimi) before the final
architecture decision. The exam document describes each module, the key prompts, the tests and
a tool comparison.

TinaAI is the public name of the project and the title shown in the app. Inside the contract and
the Skill the product keeps its original name, "AI Investigation Note Quality Assistant", because
those files are hash-pinned and tested.

## What makes this project substantive

The project treats the assistant's behaviour as a governed, testable system rather than a single
prompt inside an interface. That claim is carried by artifacts, all present in this folder or
documented in it:

- a **versioned, hash-pinned behavioural contract** (`01 Contract/`) with explicit boundaries for
  evidence handling, human decision ownership and prohibited behaviour;
- **human-authored synthetic rules, notes and scenarios** — the assistant was built, tested and
  evaluated using this material (no training or fine-tuning is involved or claimed; behaviour is
  governed by the contract and measured against human-marked keys);
- **iterative Human Micro-Batch (HMB) research** — 29 documented rounds (see the next section);
- a **locked, pre-registered held-out evaluation** (n=50) with the marking key hashed before any
  response was read;
- **honest publication of missed targets and known defects** — both pre-registered evaluation
  bars were missed, and that fact leads the evidence section rather than being buried;
- a **separately measured experimental gating filter** (post-generation control, pre-test only);
- **three distinct distribution forms** — the pinned contract, a packaged Claude Skill, and a
  standalone Streamlit demo — each carrying its own, non-transferable evidence status;
- **Custom rule-and-note testing** — reviewers can probe the assistant with their own fictional
  material, not just the bundled scenarios;
- **fail-closed contract-integrity checking** — the demo verifies the pinned contract
  byte-for-byte on every run and refuses to start on a mismatch;
- a **bilingual English/Bulgarian UI**;
- **API-key and secret-handling safeguards** throughout the app and launcher;
- a **one-click Windows launcher** for non-technical reviewers;
- **90 offline automated tests** (no API key, no network);
- **adversarial engineering and public-safety review**, with findings and fixes on record.

The process was human-led and AI-assisted: the domain owner supplied the domain judgement,
marking and adjudication; AI sessions assisted with engineering, mechanical extraction and
review. The depth of that division of labour is documented below.

## Human adjudication and research depth

The assistant emerged from **29 documented Human Micro-Batch research rounds**, culminating in
HMB-29, with at least 99 distinct notes personally adjudicated across development and held-out
evaluation — not from a single prompt-generation session.

Three aggregate figures summarise the human work. They measure **different units and must not be
added together**:

- **At least 99 distinct notes personally marked or adjudicated.** By HMB-26 the cumulative
  development corpus contained 49 distinct notes personally adjudicated by the domain owner. The
  final held-out evaluation then required the domain owner to blind-mark 50 additional notes —
  every key mark written before any paired assistant response was opened.
- **92 explicit item-level adjudications in the final scoring stage**, in addition to the
  original note marking: during the final n=50 scoring the domain owner assigned substantive
  verdicts to 84 mechanically extracted assistant response points, and coverage of the 8 key
  material-gap lines was separately adjudicated.
- **480 model runs in HMB-29** — a separate, pre-registered, statistically powered experiment on
  a candidate contract amendment (its decisive null result is recorded in
  `04 Evidence and Records/Definition of Done - The Contract v0.4.md`; the candidate was not
  adopted). These are model runs, not personally reviewed notes.

The cloud AI session's role in scoring was mechanical only — extraction, tallying and file
assembly. It assigned none of the substantive domain verdicts.

These are process and effort figures, not performance claims: they establish who did the
judgement work, not that the assistant is accurate, independently validated or production-ready.
The measured results — both pre-registered bars missed — are in
[Evidence status and known limitations](#evidence-status-and-known-limitations). The detailed HMB
research remains in a separate private archive; only aggregate, company-neutral evidence records
are included in this folder (see
[Provenance and private research archive](#provenance-and-private-research-archive)).

## Core workflow

1. Supply a synthetic rule or alert context — one of the ten bundled demonstration scenarios, or
   your own fictional one in Custom mode.
2. Supply a synthetic investigation note.
3. Review the assistant's account of the supported facts, the reasoning, and the material
   documentation gaps.
4. Optionally, enable the experimental gating filter and compare the unchanged base response with
   the filtered result — the base response always remains available, unchanged.
5. Keep every investigative or operational decision with the human reviewer. The assistant
   advises; it never decides.

Ten synthetic demonstration scenarios ship with the demo. Custom mode lets reviewers enter their
own fictional rule and note; it has had no formal behavioural validation of its own. **Never
paste real data** — no real investigation notes, customer data, account numbers, names or
internal rule/system name strings, anywhere in the app.

## Quick start

### The one-click way (Windows) — recommended

**Double-click `START-ASSISTANT.bat`.** It handles everything a non-technical person would
otherwise do by hand:

1. opens with a short product introduction, then waits for Enter;
2. checks that the required folders are present (`01 Contract`, `02 Skill`, `03 Demo/app.py`) —
   the byte-level contract integrity check happens in the app itself, on every run;
3. finds Python 3.10 or newer — and if none is installed (or only an older Python is present),
   offers to install it via `winget`, falling back to opening python.org;
4. creates the isolated `.venv` environment and installs the dependencies (rebuilding it silently
   if the folder was moved or renamed);
5. **asks for your Anthropic API key in the terminal — on every normal start.** Keys are never
   reused from disk, so a shared or inherited copy can never silently run on someone else's
   credential. Input is hidden as you type. The key is verified against Anthropic with a free
   authenticated call before being accepted; a mistyped or revoked key is rejected on the spot.
   One deliberate exception: if Anthropic cannot be reached at that moment (no internet), a key
   that at least looks like one (`sk-ant-…`) is accepted **unverified**, with a visible warning.
   The key is written only to the git-ignored `03 Demo\.streamlit\secrets.toml`, is never printed
   and never sent anywhere except to Anthropic, and the launcher deletes that file again when the
   app stops (best effort — an abruptly closed window can leave it behind, but it is overwritten
   and never reused at the next start);
6. starts the app on the first free port from 8501 upward and opens your browser.

You need a supported Windows, an internet connection, permission to install Python if it is
missing, and your own Anthropic Console API key with API credit. **Git, Node.js, an IDE and
Claude Code are not required.** On restricted corporate machines (blocked `winget`, blocked
installs, strict antivirus) the launcher names the blocker in plain language and the manual path
in `START-HERE-EN.md` applies.

Leave the console window open — it keeps the app running; close it or press `Ctrl+C` to stop.
`START-ASSISTANT.bat` is a small wrapper; the logic lives in `tools/launcher.ps1`, which is plain
text and meant to be read before you trust it — deliberately not a compiled `.exe`, which is
exactly what SmartScreen and antivirus block and what a reviewer cannot audit. Run
`START-ASSISTANT.bat -CheckOnly` from a terminal to verify the setup without prompting,
installing or starting anything (the API key is not part of the check — it is asked fresh on
every normal start).

**Before sharing this folder with someone: double-click `PREPARE-TO-SHARE.bat`.** It removes your
personal API key (a billable credential — `.gitignore` protects it from git, not from folder
copies) and the machine-specific `.venv` and caches. The recipient double-clicks
`START-ASSISTANT.bat` and is asked for **their own** key.

### The manual way

**Prefer to understand each step, or not on Windows?** See `START-HERE-EN.md` (English) or
`START-HERE-BG.md` (Bulgarian) — everything from zero, with every error message explained. The
condensed technical instructions and troubleshooting are in `03 Demo/HOW_TO_RUN.md`. The short
version, from this folder:

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Run the offline test suite** (no API key, no network, no cost):

```
python -m pytest
```

**Run the demo** — needs your own Anthropic API key. Copy
`03 Demo\.streamlit\secrets.toml.example` to `03 Demo\.streamlit\secrets.toml` and replace the
`PASTE-YOUR-OWN-KEY-HERE` placeholder with your key (from console.anthropic.com; the file is
git-ignored and must never be shared or pasted anywhere). Then:

```
cd "03 Demo"
streamlit run app.py
```

Streamlit opens `http://localhost:8501` itself; stop with `Ctrl+C`. If `streamlit` is not
recognised, use `python -m streamlit run app.py`.

**On macOS or Linux**, the same steps from this folder:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest
cp "03 Demo/.streamlit/secrets.toml.example" "03 Demo/.streamlit/secrets.toml"
# edit 03 Demo/.streamlit/secrets.toml and paste your own key
cd "03 Demo" && python -m streamlit run app.py
```

(The manual path uses a persistent `secrets.toml` you create
yourself; the always-ask behaviour is a property of the launcher, not of the app.)

Without a key the app still starts and renders fully — it shows a key warning and keeps the
Analyze button disabled, so nothing can be sent. `app.py` verifies the pinned contract against
the shipped evaluated reference on every run and **refuses to start on a mismatch**; keep
`01 Contract/`, `02 Skill/` and `03 Demo/` together as siblings, and never edit the expected hash
to make a mismatch pass (see `02 Skill/investigation-note-quality-assistant/reference/VERIFY.md`).

## Architecture and the three distribution forms

The project ships the same governed behaviour in three distinct forms. **Their evidence statuses
are different and do not transfer between forms.**

| Form | What it is | Status |
|---|---|---|
| **Pinned contract** (`01 Contract/`) | The behavioural specification itself — versioned, hash-pinned (SHA-256 `2f574a661733ffdc54fd48a13197e37e940bb1e759b7d0a70d8e4be512e58363`) | Formally evaluated on a locked held-out set (n=50); **missed both pre-registered bars** |
| **Claude Skill** (`02 Skill/`) | The contract packaged for a Claude host, with session rules, evidence label and data warning | Built and adversarially reviewed; **not behaviourally tested in any actual host**; three of eight condition rows open or untested; not equivalent to the demo |
| **Streamlit demo** (`03 Demo/`) | A separate local harness that calls the Anthropic API directly | Useful for portfolio demonstration and custom synthetic testing; **unevaluated as a configuration** — it inherits neither the n=50 result nor the Skill's status; not an MCP server, not the Skill |

**There is no MCP server.** The project holds a design candidate for one (the server hosting its
own pinned model rather than delegating to whatever a host runs), but no server code has been
written; "MCP-integrated" describes a possible future form, not anything in this folder.

The demo itself is small and inspectable: `app.py` (UI chrome), `contract_integrity.py`
(fail-closed load-and-verify of the pinned contract), `demo_logic.py` (scenarios, input limits,
request construction, gating filter, error mapping) and `ui_text.py` (bilingual chrome). A
separate React prototype exists entirely outside this folder — an independent, offline,
deterministic engineering prototype that does not implement Contract v0.8 and is not part of this
project's deliverables.

## Repository structure

| Path | Contents |
|---|---|
| `01 Contract/` | `Template v0.8 - Assistant Contract.md` — the pinned, evaluated contract. SHA-256 of the body (frontmatter stripped, whitespace-stripped): `2f574a661733ffdc54fd48a13197e37e940bb1e759b7d0a70d8e4be512e58363`. |
| `02 Skill/` | The Claude Skill distribution form — `investigation-note-quality-assistant/` (unpacked) and `investigation-note-quality-assistant.skill` (packaged). Built and reviewed; **not yet behaviourally tested in any host.** |
| `03 Demo/` | The Streamlit demo (`app.py`, `contract_integrity.py`, `demo_logic.py`, `ui_text.py`), `HOW_TO_RUN.md`, and `.streamlit/secrets.toml.example` (placeholder only). Ten synthetic scenarios and ten synthetic gating-test rules, all fictional. **Requires your own `.streamlit/secrets.toml` with an API key — never included here, never should be.** |
| `04 Evidence and Records/` | The four documents that establish what has actually been measured: the Definition of Done (the bars), the n=50 held-out evaluation result, the key-lock record, and the Skill build/review record. |
| `tests/` | Offline pytest suite (90 tests as collected by pytest): contract-integrity chain, input safety, secret handling, error mapping, gating mechanics, evidence-figure fidelity, rendered-app flows via Streamlit AppTest. Makes no API calls and needs no key. Run with `python -m pytest` from the project root (see `requirements.txt`, `pytest.ini`, `.gitignore`). |
| `START-ASSISTANT.bat`, `tools/launcher.ps1` | The one-click Windows launcher and its readable PowerShell logic. |
| `PREPARE-TO-SHARE.bat` | Removes your API key and machine-specific environment before the folder is passed on. |
| `START-HERE-EN.md`, `START-HERE-BG.md` | Step-by-step run guides for non-technical readers, in English and Bulgarian. |
| `LICENSE` | MIT. |

## Methodology and evidence

The evaluation discipline, in brief — the full account is in the app's **Methodology tab**, in
`01 Contract/` and in `04 Evidence and Records/`, and is deliberately not duplicated here:

- **Pre-registered bars.** `Definition of Done - The Contract v0.4.md` fixed two measures before
  the held-out run and never adjusted them: **Finding ≥ 60%** (share of the domain owner's marked
  gaps that the assistant raises) and **Restraint ≤ 25%** (share of the assistant's demands the
  domain owner judges unnecessary). Both must hold.
- **Locked key.** The held-out marking key was blind-marked by the domain owner, then locked and
  SHA-256-hashed **before** any paired assistant response was staged or read
  (`Key Lock Record and n=50 Amendment - S001-S050 v0.1.md`). The pre-registered n=100 was
  amended to n=50 for time/effort reasons, decided before any response was unsealed.
- **The result.** Finding **50.0% (4/8)** — bar ≥60%, **missed**. Restraint **55.2% (32/58
  demands judged unnecessary)** — bar ≤25%, **missed**. Measured against the pinned contract
  body, model `claude-haiku-4-5`, temperature 1.0
  (`Held-Out Evaluation Result - Finding and Restraint n=50 v0.1.md`). For information only, with
  no bar attached: 26 of the assistant's demands were judged to point at real issues beyond the
  blind key — roughly as many validated as real as were judged unnecessary.
- **The caveats that must travel with the figures.** The Finding denominator contains only 8
  marked gap lines — a very small sample with wide uncertainty, not a stable rate. The held-out
  set is stratified and non-representative (AML oversampled, escalated cases held equal rather
  than proportional, thin strata at n=6).
- **The experimental gating filter.** A narrow post-generation prompt that rewrites aggressive
  conditional constructions ("until X is documented, Y cannot be closed") into descriptive form.
  Its pre-test conversion is **66.1% against a 70% target**, measured on `claude-haiku-4-5` at
  temperature 0 against 56 already-known gating responses from HMB-29 — **pre-test screening
  only, non-confirmatory, experimental**. It is off by default, not part of the production logic,
  and the unchanged base response is always shown alongside the filtered one.

## Testing and engineering safeguards

- **Fail-closed contract integrity.** `contract_integrity.py` loads the pinned source, strips
  frontmatter by the one documented rule, and verifies the derived body byte-for-byte against the
  shipped evaluated reference (`2f574a66…e58363`, 31,438 characters, no trailing newline) on
  every run. Any mismatch fails closed with an error pointing at `VERIFY.md` — there is no
  fallback contract in code, and a test asserts that.
- **Secrets and errors contained.** The API key lives only in the untracked
  `.streamlit/secrets.toml` (placeholder example provided; a root `.gitignore` excludes the real
  file, venvs and caches). Requests carry a 60-second timeout and at most 2 SDK retries (never on
  auth/invalid-request). Provider failures map to concise bilingual messages; raw exception text
  is never rendered.
- **Input safety.** Both fields required; 4,000 / 16,000 character limits enforced before any API
  call, with bilingual messages — over-limit input is rejected, never truncated. The
  synthetic-data / no-real-data warning sits on the analysis page itself.
- **Output boundary preserved.** The base response is displayed exactly as returned — no parsing,
  scoring, badges, wrapping or footer-stripping. The gating filter stays opt-in, keeps its
  per-call nonce delimiters, and always preserves the base response.
- **90 offline tests** (`tests/`, as collected by pytest), including Streamlit AppTest flows
  against a mocked client and evidence-figure fidelity checks that pin the demo's displayed
  numbers to the immutable evidence record. Nothing in the suite calls the real API.
- **Deliberately not built:** no MCP server, no React/FastAPI integration, no database, accounts,
  telemetry, persistence or deployment stack; no model or prompt changes during hardening; no new
  evaluation or validation claims. The Skill's session rules (model self-declaration,
  one-case-per-session, addressee sentence, verdict-refusal flow, real-data check) are documented
  in the app's Methodology tab as *not implemented* by the demo.

## Evidence status and known limitations

- **The contract has not passed its own bar.** Held-out evaluation on n=50: Finding 50.0%
  (bar ≥60%, missed), Restraint 55.2% (bar ≤25%, missed). See
  `04 Evidence and Records/Held-Out Evaluation Result - Finding and Restraint n=50 v0.1.md`. This
  is not hidden or softened — it is the headline fact anyone picking up this folder needs first.
- **The Finding sample is small and the set is non-representative.** Only 8 marked gap lines feed
  the Finding figure, and the n=50 held-out set is stratified rather than representative.
- **The Skill is built but not released.** It passed one full adversarial review (Fable 5, 11
  findings, all fixed) but has had zero behavioural testing in any actual host. Three of its
  eight condition rows are open or untested — see
  `04 Evidence and Records/Skill Build Record - Second Distribution Form v0.2.md` and
  `02 Skill/investigation-note-quality-assistant/reference/CONDITIONS-STATUS.md`.
- **There is no MCP server** — a design direction exists on paper; no server code has ever been
  written. Building one would be new development work.
- **The demo is a separate, unevaluated harness.** It calls the Anthropic API directly, is
  neither an MCP server nor the Skill, and inherits neither the n=50 result nor the Skill's
  status. Its Custom mode has had no formal behavioural validation.
- **The gating filter is experimental.** 66.1% pre-test conversion against a 70% target,
  non-confirmatory pre-test screening only — "promising, not adopted, not rejected."
- **Known defects travel with the evidence label**, including one confirmed invention of an
  external fact (a wrong MCC category claim) on the evaluated configuration — check any code or
  typology claim before relying on it.

The result is a working, portfolio-ready local MVP with declared limitations — not a validated or
production-ready system.

## Sharing, privacy and public-safety preparation

Everything in this folder was written or copied fresh for this purpose, and none of it was pulled
from the project's real research material — no real notes, no real case IDs, no real company or
customer data, no internal rule-name strings from any source system. On that basis it should be
safe to publish.

That said: this folder was assembled by a cloud AI session, and the project's own governance
record (in the private research archive) documents two files elsewhere in the project that were
once mis-labelled as cloud-safe when they were not. **Give this folder one human read-through
before it goes anywhere public** — not because a specific problem is expected, but because the
person who built a document is the worst-positioned person to catch what got carried into it
unnoticed. Before this public repository was published, the files were scanned again for keys,
employer names and real data.

Practical checklist before sharing or publishing:

- run `PREPARE-TO-SHARE.bat` (removes your API key and the machine-specific `.venv`);
- confirm `03 Demo\.streamlit\secrets.toml` is gone — the key is a personal, billable credential,
  and `.gitignore` protects it from git, not from folder copies;
- remember that every runner supplies **their own** Anthropic API key — the launcher asks for it
  on every normal start and never reuses one from disk.

## Development and audit history

### Pre-publish audit (Fable 5, adversarial)

A fresh Fable 5 subagent with no prior context audited the folder for completeness and
public-safety: it read every file, hashed the contract, diffed the `.skill` zip against its
unpacked source, and regex-swept for secrets and employer/vendor identifiers. Result: **zero
secrets, zero real case data, zero employer/vendor names found** — that part of the "safe to
publish" claim above is verified, not assumed.

It found one **BLOCKER** and one **MAJOR**, both fixed:

- **BLOCKER — fixed.** The demo's "Validation" section fabricated a "200 notes, expert-assessed"
  validation that never happened, and never mentioned that the real n=50 held-out result missed
  both pre-registered bars. Replaced with the real Finding/Restraint figures and their
  conditions, in both languages.
- **MAJOR — fixed.** `app.py` hardcoded a corrupted, non-pinned copy of the contract instead of
  loading the pinned file, so it could drift from the evaluated body. It now loads
  `01 Contract/Template v0.8 - Assistant Contract.md` at startup and refuses to run if it cannot,
  rather than falling back to a paraphrase. Verified: the loaded text hashes to the pinned
  `2f574a66…e58363`.

Minor fixes in the same pass: `SKILL.md` corrected from a stale "two of seven conditions open" to
the accurate "three of eight"; the `.skill` zip repacked (contract body untouched, hash
unaffected); the 66.1% gating figure now carries its measurement conditions everywhere it appears
(`claude-haiku-4-5`, temperature 0, pre-test screening only — not confirmatory); a `LICENSE` file
added; and a likely-real local folder-name example in `HOW_TO_RUN.md` replaced with a neutral
one. This audit narrows what the human read-through still needs to catch — it does not replace it.

### Demo hardening pass

A follow-up engineering pass turned `03 Demo/` into a tested local MVP **without touching any
pinned artifact**: all protected files (`01 Contract/`, everything under `02 Skill/`, everything
under `04 Evidence and Records/`, `LICENSE`) were hash-verified before and after the pass and are
byte-identical, and no evidence record was edited. Everything that changed was demo-side, and is
summarised in [Testing and engineering safeguards](#testing-and-engineering-safeguards) above:
enforced contract integrity, secret and error containment, explicit input limits, the preserved
output boundary, and the 90-test offline suite.

## Provenance and private research archive

This repository contains only the portfolio-safe deliverables of the project. The detailed
working archive that produced them — the HMB research rounds, corpus selection and neutralisation
work, evaluation harness scripts, decision history, governance audits, and the raw and
neutralised note sets — is **private and excluded**. Parts of that archive contain material
unsuitable for publication, which is precisely why the separation exists; per its own governance
record, none of it belongs in a folder meant to be shared.

This folder is therefore the record of **what the project produced**, not the complete raw
research history of **how** it was produced. Only aggregate, company-neutral evidence records
(`04 Evidence and Records/`) carry the research results into the distributable form, and the
public project contains no real customer, company or case data.
