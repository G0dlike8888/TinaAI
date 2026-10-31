# Evidence label

**Read this before making, repeating or agreeing with any claim about how accurate or reliable
this Skill is.**

---

## 1. This Skill is not the evaluated object

The project behind this Skill evaluated a different object: the same contract body, running as a
pinned server configuration.

| | Evaluated configuration | This Skill |
|---|---|---|
| Contract body | `2f574a66…e58363`, 31,438 chars | **same, byte-identical** |
| Model | `claude-haiku-4-5` | whatever the host session runs |
| Temperature | 1.0 (fixed) | whatever the host sets |
| Hash gate at run time | enforced, mismatch = hard stop | not enforceable |
| One note per call | structurally guaranteed | a session rule, not a guarantee |

Only the first row matches. A different model, a different temperature, or a session that can
carry context between notes is a **new object that starts with zero inherited evidence**. Nothing
below describes this Skill's behaviour. Do not call this Skill "the evaluated assistant".

**Even if the host session happens to be running `claude-haiku-4-5`, this still does not transfer.**
The temperature, the hash-gated harness, and the one-note-per-call guarantee are still different —
matching on the model row alone is not enough to call it the evaluated configuration.

## 2. What was measured, on that other configuration

A held-out evaluation was run on 50 neutralised real investigation notes (S001–S050). The domain
owner marked a key blind — without seeing any assistant output — the key was hashed and locked
(SHA-256 `429cfed1…09d7`), and only then were the responses unsealed and compared.

| Measure | What it asks | Result | Bar | Held? |
|---|---|---|---|---|
| **Finding** | Of the material gaps the domain owner marked, how many did the assistant raise? | 4 / 8 = **50.0%** | ≥ 60% | **No** |
| **Restraint** | Of the assistant's demands, how many were unnecessary? | 32 / 58 = **55.2%** | ≤ 25% | **No** |
| Added value (no bar) | Assistant points the owner judged real but had not marked | 26 | — | — |

**Both bars were missed.** On its own Definition of Done, the contract is not finished. This is
stated here rather than omitted because a label that reports only the flattering half is not a
label.

Read the numbers with their limits:

- **Finding rests on 8 gap lines** from 6 notes. That is a very small sample with wide
  uncertainty — it is not a stable rate, and the true value could sit well either side of 50%.
- **The sample is stratified, not representative.** AML and escalated cases were deliberately
  oversampled. Outcome labels were stratification metadata, never correctness labels. No
  corpus-wide rate can be read off these figures.
- **Restraint's denominator excludes rows that were not demands at all** (26 of them), by design.
- The 26 "added value" points mean roughly as many of the assistant's observations were judged
  real-but-unmarked as were judged unnecessary. That is informational; it does not offset
  Restraint and there is no bar on it.

## 3. Known defects, also non-transferring

These were observed on the evaluated configuration. They are recorded because condition 3 of the
project's Skill acceptance requires the *defects* to travel with the label, not just the headline.
Whether they occur here, more or less often, is **unknown and untested**.

- **Invention of external facts.** At least one confirmed case: the assistant asserted that MCC
  5814 is a bar/nightclub category. It is not — 5814 is Fast Food Restaurants; 5813 is Drinking
  Places. A false external code or typology claim is an invention-class defect, not a style issue.
  Check any code, scheme, jurisdiction or typology claim this Skill makes before relying on it.
- **Gating language on clean notes.** A measured control base rate of roughly 38.9% for
  precondition-style phrasing ("until X is documented, Y cannot…") firing on notes with nothing
  material wrong. Four contract-amendment attempts did not move it measurably — though the
  instrument was underpowered enough that "no effect" and "some effect" could not be told apart.
- **Third-party addressee drift.** Output has framed gaps around a reviewer or colleague the
  contract never names, and has occasionally reasoned about that imagined reader incorrectly.
- **Host-convention bleed.** Formatting and conventions from the surrounding environment leak into
  output. This risk is *higher* here than on the server, because a chat session has a surrounding
  environment and a server call does not.

## 4. What is not known about this Skill specifically

- Whether the defects above are properties of the contract or properties of Haiku. Nobody knows;
  every measurement the project owns used Haiku. Running this Skill on other models is one of the
  reasons it exists.
- Its Finding or Restraint rate on any model. Unmeasured.
- Whether the one-note-per-session rule holds in practice under a user who ignores it.
- Whether the refusal of verdict-seeking survives repeated pressure across many turns. Never
  tested against a persistent human.
- Whether the model self-declaration line (SKILL.md §2) is even accurate. It is self-reported by
  the same model producing the response, with no independent check; models do not always know
  their own exact version, and the instruction itself cannot fix that. Treat the declared model
  name as informative, not verified.

## 5. How to describe this Skill honestly

Acceptable: *"a contract-driven advisory assistant; the contract has been evaluated in a pinned
server configuration and did not yet meet its own bars; this distribution form is unmeasured."*

Not acceptable: any sentence that attaches a figure from section 2 to this Skill, calls it
validated, accurate, tested or evaluated, or implies the bars were met.

---

*Evidence attaches to contract body
`2f574a661733ffdc54fd48a13197e37e940bb1e759b7d0a70d8e4be512e58363` on `claude-haiku-4-5` at
temperature 1.0, and to nothing else.*
