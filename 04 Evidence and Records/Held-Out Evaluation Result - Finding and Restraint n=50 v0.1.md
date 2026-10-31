---
type: finding
version: v0.1
status: "COMPLETE. Finding and Restraint computed for the first time against the
  held-out set (n=50, S001-S050). Domain owner performed all substantive matching (MATCH
  raised/DEMANDS verdict); the cloud session performed only mechanical extraction, tallying,
  and file assembly. Supersedes no prior document — this is the first time Part 2 of
  Definition of Done - The Contract v0.4 has been run for real."
area: evaluation
source_class: company-neutral (aggregate counts only; no note or response content)
project: ai-investigation-note-assistant
---

# Held-out evaluation result — Finding and Restraint, n=50

## The numbers

Measured against `Template v0.8 - Assistant Contract.md`, SHA-256
`2f574a661733ffdc54fd48a13197e37e940bb1e759b7d0a70d8e4be512e58363`, model `claude-haiku-4-5`,
temperature 1.0, on the locked key (SHA-256 `429cfed18151b47232f91aa21ecabf6f67e9c86ddbf81c4354759f52b51109d7`, n=50, S001–S050).

| Measure | Formula | Result | Bar (Definition of Done v0.4) | Holds? |
|---|---|---|---|---|
| **Finding** | raised=YES / all key gap lines | 4 / 8 = **50.0%** | ≥ 60% | **NO** |
| **Restraint** | UNNECESSARY / (UNNECESSARY + REAL-MISSED) | 32 / 58 = **55.2%** | ≤ 25% | **NO** |
| Added value (informational, no bar) | REAL-MISSED count | 26 | — | — |

**Both bars miss, on this evidence.** Definition of Done v0.4, Part 2: "Both must hold... If the
bars are missed, the contract is not good yet."

## What this evidence is and is not

- **n=8 gap lines** (from 6 of 50 notes carrying a marked material gap) is a very small sample
  for Finding — wide uncertainty, not a stable rate.
- **n=58** (UNNECESSARY+REAL-MISSED denominator) is a more workable size for Restraint, but
  still drawn from a stratified, non-representative n=50 (not the pre-registered n=100) — see
  `Key Lock Record and n=50 Amendment - S001-S050 v0.1.md` in this folder for the stratification
  caveat (thinner strata: unclassified/escalated n=6, AML/FP n=6).
- NOT-A-DEMAND rows (26) are excluded from the Restraint denominator by definition — they were
  never demands.
- REAL-MISSED (26) is reported for information only, per the pre-registered instrument design
  — it is not penalised and does not offset Restraint. It does indicate the assistant catches
  real issues beyond what the domain owner marked in his blind key; roughly as many of its
  points were validated as real (26) as were judged unnecessary (32).

## Matching provenance — who did what

- **MATCH (raised YES/PARTIAL/NO):** domain owner, note-by-note, comparing his own key gaps
  against the paired response text. Not performed by the cloud session.
- **DEMANDS (verdict UNNECESSARY/REAL-MISSED/NOT-A-DEMAND):** candidate rows mechanically
  pre-extracted by the cloud session per Own Words First ruling 3 ("may be mechanically
  pre-extracted... by a model"); verdicts assigned entirely by the domain owner. One row
  (S027) was added by the domain owner beyond the mechanical extraction, after he identified
  that the note contained assessable content ("Medium amounts", "regular online payments")
  the assistant's declined-response had missed — recorded as UNNECESSARY (the decline itself
  judged unwarranted).
- The cloud session's role throughout: candidate extraction, tallying, and file assembly only.
  No raised/verdict value was set by the cloud session.

## What this means for the project, as it stands

Definition of Done v0.4's own text: *"If the bars are missed, the contract is not good yet and
development reopens — but under Part 1's dryness rule, from candidates with real cases behind
them, not from ideas."*

However, `Candidate Track Closure and Demo Handoff v0.1` (written before this result
existed) already closed candidate-clause development for scope/time reasons and scoped the
next phase as a demo, explicitly *"not a finding that the candidate-mechanism approach is
exhausted or that gating is solved."* That closure decision stands. What changes now is that
**an honest label for the demo/Skill can finally be written** — this figure is what the
Skill's evidence label (see the Skill folder in this project) carries.

**This result does not block moving into Skill/demo work — it is what makes that work
honestly labellable.** The label must state Finding 50% / Restraint 55.2% on n=50, not imply
the contract passed Part 2, and must carry the n=50/stratification caveats above.

## Related

- `Definition of Done - The Contract v0.4.md` (this folder) — the bars
- `Key Lock Record and n=50 Amendment - S001-S050 v0.1.md` (this folder) — key hash, n=50 amendment, stratification check
- `Skill Build Record - Second Distribution Form v0.2.md` (this folder) — where these figures are carried into the Skill
