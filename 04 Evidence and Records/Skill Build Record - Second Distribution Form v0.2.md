---
type: build-record
version: v0.2
status: "BUILT, then revised after Fable 5 adversarial review. The Skill folder
  exists, packaged, and has had one full adversarial pre-release pass with all findings applied.
  NOT RELEASED — three of the resulting eight condition-rows are open or untested (see §3). No
  behavioural test has been run in any host."
area: product
source_class: company-neutral
project: ai-investigation-note-assistant
---

# Skill build record — second distribution form

Records what was built against the project's HANDOFF §7, which accepted a Claude Skill as a second distribution form under seven conditions,
and the Fable 5 adversarial review + fix pass that followed.

## 1. What was built

`investigation-note-quality-assistant.skill` — a zip of:

| File | Purpose |
|---|---|
| `SKILL.md` | Entry point. Loads the contract, sets the session operating rules, states intended purpose and prohibited use, points at the evidence label and data warning. |
| `reference/CONTRACT-v0.8.md` | The contract body, byte-identical. |
| `reference/EVIDENCE-LABEL.md` | What was measured, on what, why it does not transfer, and the known defects. |
| `reference/DATA-WARNING.md` | What may and may not be pasted into a session. |
| `reference/VERIFY.md` | Manual hash check and what to do on a mismatch. |
| `reference/CONDITIONS-STATUS.md` | The seven conditions (eight rows — condition 1 split), three recorded open/untested. |

Present in this folder under `../02 Skill/` (both unpacked and as the `.skill` archive).

## 2. Contract integrity

`reference/CONTRACT-v0.8.md` was produced from `Template v0.8 - Assistant Contract.md` (this
folder, `../01 Contract/`) by stripping YAML frontmatter and applying `.strip()`, UTF-8.

- Length **31,438 characters** — matches the pinned value.
- SHA-256 **`2f574a661733ffdc54fd48a13197e37e940bb1e759b7d0a70d8e4be512e58363`** — matches the
  pinned hash.
- Verified **five** times across the build and the revision pass: on write, re-read from disk,
  after extracting the v1 package, after the wrapper-file fix pass (contract untouched), and again
  after extracting the v2 package. All five agree.

No contract text was changed at any point. No second contract was drafted (§4 explains why not).

## 3. Fable 5 adversarial review — findings and disposition

A fresh Fable 5 subagent, with no prior context on this build, was given all six Skill files plus
the full contract and the project's evidence/condition record, and asked to find what a competent
author would miss before handing the package to a stranger. It returned 11 findings, most severe
first: **1 BLOCKER, 5 MAJOR, 4 MINOR, 1 NOTE.** All 11 were applied. None required touching the
contract.

**BLOCKER — fixed.** `CONDITIONS-STATUS.md` stated that because the Skill refuses third-party
review, the unadopted addressee clause "cannot bite." False: the refusal fires only when the user
*says* they are reviewing someone else's note; a silent or misattributed reviewer gets ordinary
author-addressed output, and the addressee-drift defect can occur with no reviewer declared at
all. The package carried a safety claim its own evidence label contradicted. Fixed by rewriting
condition 2's status to "partially contained, not resolved" in both `CONDITIONS-STATUS.md` and
`SKILL.md` §3, spelling out exactly what the refusal does and does not cover.

**MAJOR (5) — all fixed:**

1. `SKILL.md` §2 and the contract's §6 each implicitly claimed supremacy over the other, and the
   mandated model-declaration line is exactly the kind of prefix §6 forbids. Fixed: §2 now names
   the model line and the addressee sentence as the *only* two enumerated exceptions to §6, states
   they are required by acceptance conditions 1 and 4 specifically, and reaffirms §6 governs
   everything else against every environment including host formatting conventions.
2. The one-note-per-session rule forbade the product's core revision workflow (draft → feedback →
   revised draft) and had a literal loophole (two unrelated notes pasted together in the first
   message never triggered it). Fixed: redefined as "one *case* per session" — a case includes the
   note, its rule/alert, its own revisions, and follow-ups; a different case triggers the stop
   regardless of whether it arrives first or fifth.
3. The data-handling check's only behavioural instruction lived in `DATA-WARNING.md`, a file
   nothing tells the model to read before reviewing. Fixed: the check now lives in `SKILL.md` §2
   as a session rule, with `DATA-WARNING.md` kept as the detailed backing reference; both now state
   plainly that the check is heuristic and one sentence ("it's synthetic") defeats it.
4. The model self-declaration example (`claude-sonnet-4-6`) was a realistic model string a host
   model would likely copy verbatim, quietly corrupting the cross-model evidence this line exists
   to collect. Fixed: replaced with an explicit placeholder and an "if unsure, write `unknown` —
   never guess or copy the example" instruction; `EVIDENCE-LABEL.md` now also notes the
   declaration is self-reported and unverified.
5. No fallback existed for a host where the Skill's reference files aren't readable — the model
   would have every incentive to proceed from `SKILL.md`'s two-paragraph summary alone. Fixed: one
   explicit instruction to refuse to run rather than substitute the summary for the contract.

**MINOR (4) and NOTE (1) — all fixed:** hedged two overconfident legal claims in
`DATA-WARNING.md` (banking-secrecy personal liability, GDPR Article 44 transfer framing);
removed "SAR/STR narrative" as a Skill-trigger in the frontmatter description (outside the
evaluated document class); added a trailing-newline warning and exact byte count to `VERIFY.md`
(the likelier accidental corruption than the CRLF case it already covered); split acceptance
condition 1 into 1a (contract identity — met) and 1b (model self-declaration — graded
"instructed, untested," on the same standard condition 5 already used) so an untested behavioural
claim wasn't marked "Met" on weaker evidence than a comparable one nearby; added the
Haiku-host edge case, the dangling internal wiki-links note, and the "clean-note sufficiency
language will itself get quoted back as a submit request" observation to the suggested-test list.

**Net effect:** condition rows needing attention before release went from 2 to 3 (1b, 2, 5) —
not because anything got worse, but because condition 1 was previously overstating what "met"
meant for its behavioural half.

## 4. Conditions status — three rows open or untested

| # | Condition | Status |
|---|---|---|
| 1a | Byte-identical contract, hash stated | Met |
| 1b | Model self-declared in output | **Instructed — untested** |
| 2 | No Third-Party Addressee question adjudicated before QA-facing framing | **Open — partially contained, not resolved** |
| 3 | Evidentiary label, non-transfer, defects included | Met |
| 4 | Intended-purpose / prohibited-use, no analyst identity, "about the note, not its author" | Met |
| 5 | One case per session, verdict-seeking refusal, host-bleed check run in ≥1 host | **Partly met — untested** |
| 6 | Data warning | Met |
| 7 | Publication only after the marking key is filled | Met (key locked and scored) |

**Condition 2 is partially contained, not resolved.** The refusal only fires on user disclosure;
it does not detect undeclared third-party use and does not touch the addressee-drift defect at
all. The draft addendum addressing this remains unadopted. If QA-facing use is ever wanted, the
adjudication comes first.

**Conditions 1b and 5 are the real gap.** Model self-declaration, the one-case rule, the
verdict-seeking refusal and host-bleed resistance are all written as instructions and none has
been tested. This project's own record is the reason to be blunt about that: four contract-
amendment attempts against a different clause candidate produced no measurable change earlier in
the project. An instruction to a model is a hypothesis.

## 5. Why no second contract was drafted

The project's HANDOFF accepted a separate Skill contract as a minimal delta from v0.8, principally
to solve the addressee problem. With the Skill scoped analyst-facing, that problem does not arise
as a matter of *stated scope* — though §3 above records that the scoping is enforced only when the
user discloses their intent. Keeping the contract byte-identical also keeps condition 1a trivially
satisfied and keeps the object one step closer to the evaluated configuration.

A second contract remains the right move *if and when* QA-facing use is enabled. It would be a new
object with zero inherited evidence.

## 6. Evidence position

The label states, in the Skill itself: Finding **50.0%** (4/8) and Restraint **55.2%** (32/58) on
n=50, both bars missed, measured on contract body `2f574a66…e58363` running `claude-haiku-4-5` at
temperature 1.0 — and that none of it transfers to the Skill, which runs on the host session's
model at the host's temperature (including, now explicitly, if the host happens to also be
`claude-haiku-4-5` — temperature and harness still differ). The four known defects (MCC invention,
~38.9% gating base rate, third-party addressee drift, host-convention bleed) travel with the
label, per condition 3.

The Skill is described nowhere as validated, accurate or evaluated.

## 7. Next actions

1. Run the six suggested tests in `CONDITIONS-STATUS.md` (in the Skill folder) — host-bleed,
   verdict-seeking under pressure, case-boundary handling, undeclared third-party use,
   self-declaration accuracy, and all of the above cross-model on ≥2 hosts. This closes conditions
   1b and 5 and simultaneously produces cross-model evidence the project has never had.
2. Record each model's results separately. No result transfers between hosts.
3. Adjudicate the addressee clause only if QA-facing use is wanted.

## Related

- `Definition of Done - The Contract v0.4.md` (this folder)
- `Held-Out Evaluation Result - Finding and Restraint n=50 v0.1.md` (this folder) — the figures the label carries
- `Key Lock Record and n=50 Amendment - S001-S050 v0.1.md` (this folder) — key hash and stratification caveat
