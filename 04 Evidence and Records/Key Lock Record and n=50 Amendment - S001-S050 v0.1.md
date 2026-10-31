---
type: pre-registration-amendment
version: v0.1
status: "RECORDED. Key locked and hashed BEFORE responses were staged or read this
  session, preserving the independence sequence required by Definition of Done v0.4 and the
  Own Words First ruling. Amends the sample size from n=100 (100-Note Held-Out Sample -
  Stratification Design v0.2) to n=50, following the same procedural pattern as
  Pre-Registration Amendment 1."
area: evaluation
source_class: company-neutral (structural/aggregate only; no note or response content)
project: ai-investigation-note-assistant
---

# Key lock record and n=50 amendment — S001–S050

## What changed

`KEY_marking_sheet.xlsx` is locked at n=50 (S001–S050) instead of the pre-registered n=100.
Domain owner's stated reason: time/effort — not a data-driven decision, made before any
response was unsealed or seen this session.

## Key lock

- File: `KEY_marking_sheet.xlsx`
- **SHA-256: `429cfed18151b47232f91aa21ecabf6f67e9c86ddbf81c4354759f52b51109d7`**
- Size: 16,442 bytes
- Locked/hashed: before any response file was staged or read in this session.
- Sitting log: Sitting 1, S1–S50.
- All 50 rows confirmed non-blank (S038 and S050 were completed after an initial pass that
  left them empty).

## Marking convention ruling (domain owner — overrides the literal GUIDE text)

The GUIDE sheet's literal instruction ("empty = not done, type OK for nothing material") is
superseded by the domain owner's actual practice, ruled acceptable as his own marking
convention:

- `gaps` cell contains text → one or more material gaps (Finding denominator).
- `gaps` cell empty **and** at least one other column (`minor_and_remarks` / `positives` /
  `comment`) has content → note was reviewed, no material gap (functionally equivalent to
  "OK").
- **All four columns empty → not yet marked.** This is the only state that still means
  "not done"; it was checked row-by-row for S001–S050 and none remain in this state.

Result under this convention: 6 of 50 notes carry material gaps (S009, S014, S020, S021,
S024, S028 — note S021's response also had non-gap content but the response was scored via a
different route, see the phase-2 workbook in the working ProjectWork archive), 8 material gap
lines total.

## Stratification check, n=50 vs the n=100 plan

S001–S050 against `selection_manifest.csv` domain/outcome fields (structural metadata only):

| Domain/Outcome | In S001–S050 | Half of n=100 plan | Full n=100 plan |
|---|---|---|---|
| Fraud / FP | 14 | 14.0 | 28 |
| Fraud / escalated | 11 | 13.5 | 27 |
| AML / FP | 6 | 7.5 | 15 |
| AML / escalated | 9 | 7.5 | 15 |
| unclassified / FP | 4 | 4.0 | 8 |
| unclassified / escalated | 6 | 3.5 | 7 |

No severe block-ordering skew — reasonably proportional. **Caveat that must travel with any
reported figure:** the thinner strata (unclassified/escalated n=6, AML/FP n=6) carry
correspondingly wider uncertainty than the original n=100 design assumed. This is in addition
to the three non-representativeness layers already recorded in the project's stratification
design (AML ~3x oversampled, escalated held equal not proportional, longest ~13% of corpus by
note length).

## Sequence preserved

1. Key marked blind (no responses seen) — confirmed.
2. Key locked, hashed, dated — this record.
3. Responses for S001–S050 unsealed and read this session, after step 2, to mechanically
   pre-extract phase-2 DEMANDS candidates. S051–S100 were never staged or read.

## What is still open

- Gating (G/N) rate for this batch not yet computed; remains fitted-not-validated per the
  existing rubric regardless of when computed.
- Codes pass (post-lock, pre-unseal) was not run as a separate step before this unsealing —
  a process deviation from the original design, not a rejection of it. May still be run
  retroactively; it is metadata, not measurement, so this does not invalidate Finding/Restraint.

## Related

- `Definition of Done - The Contract v0.4.md` (this folder) — the bars this run serves
- `Held-Out Evaluation Result - Finding and Restraint n=50 v0.1.md` (this folder) — the computed result
