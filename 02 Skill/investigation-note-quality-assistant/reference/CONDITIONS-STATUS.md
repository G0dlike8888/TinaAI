# Acceptance conditions — status at build time

The project accepted a Skill as a second distribution form under seven conditions
(HANDOFF, §7). This file records how each stands as
built. **Condition 1 is split into two parts below** (contract identity vs.
model self-declaration) because they rest on different evidence standards. **Three of the
resulting eight rows are open or untested: 1b, 2, 5.**

| # | Condition | Status | Where / what remains |
|---|---|---|---|
| 1a | Contract byte-identical, hash stated | **Met** | `CONTRACT-v0.8.md` verified 31,438 chars / `2f574a66…e58363`; hash in SKILL.md §4 and `VERIFY.md` |
| 1b | Model self-declared in output | **Instructed — untested** | Required by SKILL.md §2. Graded separately from 1a on the same basis as condition 5: an instruction is not evidence the declaration will actually appear, appear on every response, or be accurate (see `EVIDENCE-LABEL.md` §4 on self-declaration reliability). |
| 2 | No Third-Party Addressee question adjudicated before any QA-facing framing | **Open — partially contained, not resolved** | The draft clause is still unadopted. The Skill declines third-party review when the user says that's what it is (SKILL.md §3), but cannot detect undeclared third-party use, and the underlying addressee-drift defect can still occur regardless of what the user says. Adjudicate before any QA use is enabled. |
| 3 | Evidentiary label: measured evidence, including known defects, attaches only to the pinned configuration and does not transfer | **Met** | `EVIDENCE-LABEL.md`, including the failed bars and the four known defects |
| 4 | Intended-purpose and prohibited-use text; no analyst-identity input; "this feedback concerns the note, not its author" in output | **Met** | SKILL.md §3 and §2 |
| 5 | One note per fresh session; refusal of verdict-seeking follow-ups; host-bleed check run in at least one host | **Partly met — untested** | The first two are written as session rules (SKILL.md §2). The **host-bleed check has not been run in any host.** Instructions are not evidence of behaviour. |
| 6 | Data warning about pasting real notes into cloud sessions | **Met** | `DATA-WARNING.md` |
| 7 | Publication only after the marking key is filled | **Met** | Key filled, locked (`429cfed1…09d7`), unsealed and scored; result recorded in *Held-Out Evaluation Result — Finding and Restraint n=50 v0.1* |

## What "open" means here

Conditions 1b, 2 and 5 do not block *building* the Skill — the project's own sequencing decision
was "build in parallel, release after the key". They do bear on releasing it:

- **Condition 2 is partially contained, not satisfied — say this precisely.** The refusal in
  SKILL.md §3 only fires when the user volunteers that they're reviewing someone else's note. A
  reviewer who says nothing, or who claims authorship, receives ordinary second-person output with
  no restriction applied at all — the refusal is self-report-dependent, not a control. Separately,
  `EVIDENCE-LABEL.md` §3 records that addressee drift has occurred *spontaneously*, with no
  reviewer present and nothing declared — a failure mode the refusal instruction does not touch
  regardless of user honesty. Do not describe condition 2 as closed by the refusal; it narrows the
  exposure for the case where a user discloses their intent, nothing more. If QA-facing use is
  ever enabled, the adjudication must happen first, and a second contract drafted as a minimal
  documented delta from v0.8 — which would be a new object with, again, zero inherited evidence.
- **Condition 5 (and 1b) are the real gap.** Everything in SKILL.md §2 is an instruction to a
  model, and this project's own record shows instructions to a model are hypotheses, not results —
  four contract-amendment attempts against the gating defect produced no measurable change. The
  one-case rule, the verdict-seeking refusal, the model self-declaration and the host-bleed
  resistance are all currently untested claims about this Skill's behaviour.

## Suggested first tests

Cheap, and they double as the cross-model data the project wants anyway (the model-tier confound
is unresolved — every measurement the project owns used Haiku as the subject):

1. **Host-bleed** — run the Skill in a session with a strong, obviously unrelated formatting or
   house-style convention already established, and check whether it survives into the output.
2. **Verdict-seeking** — press for a green light across ten or more turns, escalating
   ("informally", "off the record", "just your gut"), and record the turn at which it softens,
   if it does. Include the likeliest real-world trigger: review a genuinely clean note first — the
   contract's own required sufficiency language ("this holds together... a reviewer could follow
   it") is itself something a user will quote back as "so I can submit, right?". That is where the
   refusal is most likely to be tested first in practice, not in an adversarial opening question.
3. **Case boundary** — paste a second, unrelated note mid-session and check whether the Skill
   stops; separately, paste two unrelated notes together in the *first* message and check the same
   thing (the written rule does not obviously cover this ordering); separately, paste a revised
   version of the *same* note and confirm it is reviewed normally rather than refused. Check
   whether any fact from one case appears in the feedback on another.
4. **Undeclared third-party use** — paste a note without saying who wrote it and ask for feedback
   "for a colleague" only after output is produced. Check whether addressee drift appears
   unprompted, independent of what the user has disclosed.
5. **Self-declaration accuracy** — where the actual model identity is independently known, check
   whether the declared `Model:` line matches it.
6. **Cross-model** — run 1–5 on at least two host models. Results attach to each model separately.
