---
type: definition-of-done
version: v0.4
status: "ACCEPTED, carried forward from v0.3. This revision updates the attempt counter
  only — attempts 2, 3 and 4 recorded with outcomes; a fifth attempt is blocked pending an
  instrument fix. No bar, dryness count or escalation-path term changed. The addendum below
  records HMB-29/Candidate 4, run under a separate, redesigned instrument, not as 'attempt 5' of
  the flawed suppression metric this document originally referred to."
supersedes: "Definition of Done - The Contract v0.3 ACCEPTED — its attempt table stopped at
  attempt 2 marked \"Running.\" Three more attempts and one instrument-validity finding happened
  the same day and were not reflected."
area: product
raised_by: "The domain owner: he does not want an endless project, and asked for a
  definition of a good contract rather than inventing new clauses after every run."
source_class: company-neutral
cloud_safe: yes
project: ai-investigation-note-assistant
---

# Definition of done — the contract

## The problem this closes

Every round of testing has produced new clause candidates. The coverage finding explains why and
guarantees it will continue: **detection tracks specification.** What the contract names, the
assistant finds; what it does not name, it misses. So every new note reveals a gap type the contract
does not cover, which suggests a clause, which is tested, which reveals the next one.

There is no natural end to that. Without a stopping rule the contract grows for as long as anyone
keeps looking, and "test until the results are good" has no last iteration.

## The finish line already exists in the plan

The domain owner's stated arc ends with him personally reviewing one hundred notes. That step has
been treated as validation performed after the work is done.

**It is not validation. It is the finish line, and it is the only non-circular measure available.**

Every figure this project holds was produced on twenty notes that the contract was subsequently
developed against. Measuring the contract on those notes again cannot establish that it is good — it
establishes that it was tuned. The hundred-note set is material the contract has never seen, and a
pre-registered bar on unseen material is what "good" has to mean.

## Three parts, and the third is the one that ends it

### Part 1 — when clause development stops

**Dryness rule.** Clause development ends after **two consecutive rounds** in which no new candidate
emerges that has both:

- **a real note behind it** — not a synthetic case, not a hypothetical, and
- **a marked case that failed** — an actual demand the domain owner marked, which the current
  contract handles wrongly.

An idea missing either half is recorded as an observation, not a candidate. Observations do not
extend development.

**Why two and not one.** One dry round is plausibly a quiet round. Two is a pattern. This is the
same shape as the loop-until-dry discipline used elsewhere, and the number is a decision, not a
calculation.

**What this rules out.** "We thought of something that might help" no longer opens a round. Neither
does a candidate derived only from reasoning about the contract text, which is how the rejected
no-self-filling clause was born.

### Part 2 — when the contract is good

**Measured on the hundred-note set, which the contract has never been developed against.**

Two measures. **Both must hold.** Bars fixed before the run, never adjusted after.

| Measure | What it asks | Bar |
|---|---|---|
| **Finding** | Of the gaps the domain owner marks on those notes, what share does the assistant raise? | **≥ 60%** |
| **Restraint** | Of the demands the assistant makes, what share does the domain owner mark as things it should have left alone? | **≤ 25%** |

**Both accepted by the domain owner, as proposed.** They are informed by where the
project currently sits — roughly 40% finding under a contract that named only one gap type, and 64%
of demands wrong on the clean-note round — so both represent real improvement rather than a rubber
stamp. **They do not move.**

**Why both, and why neither alone.** A contract that raises nothing scores perfectly on restraint. A
contract that raises everything scores perfectly on finding. The product is only useful where both
hold at once, and every round so far has failed one of them.

**If the bars are missed**, the contract is not good yet and development reopens — but under Part 1's
dryness rule, from candidates with real cases behind them, not from ideas.

### How the hundred are selected — fixed before the run

The domain owner's stated method: once the contract is judged good against the two bars, the
assistant is run over a larger base of notes and he reviews one hundred of them.

**Which hundred is decided before he sees any response.** Random selection, or a stated rule applied
to the base — either is fine; choosing after reading is not. Picking the interesting-looking ones is
not dishonesty, it is what anyone does unprompted, and it moves the result.

The selection rule is written down with the run, alongside the base it was drawn from.

### The attempt counter — the guard against fitting twenty notes

Every failed test against the twenty-note development set, followed by a revision and a retry,
teaches the project something about those twenty notes. After enough attempts, **passing means only
that enough attempts were made.**

**Each attempt is numbered and recorded.** The count so far:

| Attempt | What was tested | Outcome |
|---|---|---|
| 1 | Candidate clause — no self-filling of identified gaps | Failed. +9.6 against a pre-registered 15-point bar. Not adopted. |
| 2 | HMB-28 — Candidates 3 and 5 together (additive) | Suppression ~18.2%, well under the 60% pre-registered bar. Not adopted. **The build carried an undetected 1,424-character preamble inside the system prompt — a confound, recorded, not corrected retroactively.** |
| 3 | HMB-28 — Boundary 4 table restated (additive) | Suppression ~18.2%, same order of magnitude as attempt 2. Not adopted. Same preamble confound (1,396 chars), also undetected at the time. Adjudication concluded *"enumeration is attention"* — naming a class in the contract makes the assistant attend to it regardless of surrounding instruction not to. |
| 4 | Subtractive probe — deletion of the §4 Boundary 1 six-item list, no additions (build verified byte-identical to v0.8 apart from the deletion; no preamble) | Suppression ~20%, same order of magnitude as attempts 2 and 3. Not adopted. **This attempt's clean build, contrasted with attempts 2–3, is what surfaced the preamble confound in the first place.** |

**Between attempt 4 and any attempt 5 [against this same flawed suppression instrument], an
instrument-validity finding was made and is recorded in [[Separability and Reliability - Finding
v0.1]].** The zero-in-4 suppression measure used in all three attempts above cannot distinguish no
effect from a 50% reduction — a true 50% reduction produces roughly the same zero-count as the
null. No A/A baseline (control against control) has ever been run, so the measurement's noise floor
is unknown. **Attempts 2, 3 and 4 therefore do not show that their clauses failed. They show that
this instrument could not have detected success if it had occurred.** A fifth attempt against the
*same* instrument was never planned; instead a properly powered, pre-registered instrument was built
from scratch for the next candidate — see the addendum below.

**The same investigation separately found that part of the assistant's task may be unreachable in
principle on some claims** — an independent predictor given note, rule and letter definitions but not
the key scored *below* the constant-answer baseline on gap/not-gap (63.6% vs. 68.2%), while the
domain owner reproduced his own gap/not-gap calls at 93.3% on a blind re-mark. The gap between those
two figures is unlikely to be entirely key noise, meaning some share of the distinction lives in
analyst knowledge the note does not carry — a ceiling no contract wording can raise. This bears on
Part 2's bars and is not yet reconciled with them; see Open below.

**The number of attempts against the development set is reported alongside the hundred-note result**,
always. A contract that passed on attempt two and one that passed on attempt eight are not the same
contract, and the difference is invisible without the count.

### Addendum — HMB-29 / Candidate 4, a separate instrument, not "attempt 5"

Candidate 4 (the red light, a two-directional §6 gating amendment) was designed, pre-registered, and
tested via HMB-29 under a **newly built, statistically powered instrument** (12 runs/note/arm, 480
total, z-test, pre-registered invalidation gate) — not the flawed zero-in-4 suppression metric that
attempts 1–4 used. It is recorded here as its own line, distinct from the numbered attempt table
above, because merging it in would misrepresent which instrument produced which result.

**Result: NOT ADOPTED.** Control 23.33%, treatment 22.08%, ratio 0.9464 against a required ≤0.40 —
decisive, well-powered null (z=0.33, p≈0.74, 95% CI 0.68–1.32, power >99%). Diagnosed as
"instruction non-uptake, not evasion." **Untested confound, recorded not resolved:** every run in
this lineage used `claude-haiku-4-5` as both subject and judge; whether a larger model would follow
the same wording differently is unknown.

**A post-generation filter mechanism (not a wording-level contract clause) is the project's current
attempt at the same gap.** This is architecturally distinct from everything in the attempt table
above: it edits the response after generation rather than amending the instructions the generator
follows, so it is not counted against the twenty-note development-set attempt history at all.

This is why Part 2 measures on notes the contract has never seen. The attempt counter makes the
development-set result honest; the held-out set makes the final result meaningful. Neither substitutes
for the other.

### Part 3 — what the contract does not fix, declared

**This is the part that actually ends the project, and it is the part no document currently
carries.**

A contract with an unwritten backlog of known problems is never finished — every reader, including
its author, sees the missing pieces and infers more work. A contract that states *"these failure
modes are out of scope, and here is why"* is finished, at a stated scope.

**A written out-of-scope list is a deliverable, not an admission.** For a template meant to be taken
and developed against a specific company, the boundary is more useful to the next person than
another clause would be.

**Known candidates for that list**, each already surfaced by the work:

- **Referent ambiguity.** A note saying *"activity was reviewed"* where a reader cannot tell whether
  *activity* means the account or only what triggered the rule. Real, and not a trust question.
- **Comprehensibility (Type E).** A sentence that cannot be parsed. Prohibition #13 forbids grading
  structure and length, and separating unreadability from style has not been solved.
- **Judgment accuracy.** Whether the analyst's conclusion is correct. Explicitly not the product,
  and the judgment track sits near chance regardless.
- **Anything requiring knowledge outside the note.** The assistant sees a note and a rule. It cannot
  know what the analyst saw in the system. **Now measured, not just asserted** — see the separability
  finding referenced above.
- **Gating language at the Haiku model tier, under a wording-level candidate — added with the addendum.**
  Candidate 4's decisive null result (above) is recorded here as a stated, known limitation of the
  Template Level contract text itself, not silently absorbed. The post-generation filter is a
  separate mechanism class attempting the same gap.

## What this costs, stated plainly

**Fixing a stopping rule means shipping something imperfect.** That is what a stopping rule is for.
There will be known failure modes the contract does not address on the day it is called done, and
they will be listed rather than fixed.

For a production system that would be a problem. For a template — something another person takes and
develops against their own rules and systems — a stated boundary is more honest and more useful than
an implied promise of completeness.

## Where this stands as of the final-project folder

The held-out run against this bar has now happened, at n=50 rather than the originally planned
n=100 (see `Key Lock Record and n=50 Amendment - S001-S050 v0.1.md` in this folder). Result: Finding
50.0% (bar ≥60%, missed) and Restraint 55.2% (bar ≤25%, missed) — see `Held-Out Evaluation Result -
Finding and Restraint n=50 v0.1.md` in this folder. **Both bars are missed on this evidence.** Per
this document's own text: "If the bars are missed, the contract is not good yet and development
reopens... under Part 1's dryness rule." The project's separate decision was to close the
candidate-development track for scope/time reasons and move to a demo/Skill phase instead — this is
explicitly *not* a claim that the contract passed Part 2.
