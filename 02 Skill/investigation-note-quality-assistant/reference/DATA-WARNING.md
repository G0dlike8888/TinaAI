# Data warning — what may be pasted into a session

This Skill runs inside a chat session with a hosted model. Whatever is pasted into it leaves the
machine it was typed on.

## The default assumption

**Do not paste real investigation notes.** A real note typically contains customer personal data
(names, account and card identifiers, transaction detail, sometimes device or location data),
confidential case material, and internal rule or system names. Pasting that into an ordinary
consumer subscription or a personal API account is very likely a breach of:

- your employer's data-handling and outsourcing rules;
- the GDPR obligations your employer carries as controller — most directly, Article 28's
  requirement for a processor agreement, which an ordinary consumer or personal API account does
  not have. (International-transfer rules under Chapter V/Article 44 may also apply, but whether
  they are already satisfied depends on the provider's own certification status — e.g.
  participation in a recognised transfer framework — which this warning does not attempt to
  verify. Article 28's point stands regardless.)
- confidentiality and, in some jurisdictions, banking-secrecy duties — these bind the institution
  in every jurisdiction and, in at least some (e.g. Bulgaria's Credit Institutions Act), extend to
  individual employees personally; whether that is true in *most* jurisdictions is not something
  this warning can verify, so treat it as a live possibility rather than an exception;
- in some jurisdictions, SAR/STR confidentiality rules and tipping-off offences, where the note
  relates to a suspicion report — whether pasting into an AI session falls within scope of a given
  jurisdiction's offence is untested and not something this warning can verify.

"Anonymising" by deleting the customer name is not sufficient. Amounts, dates, merchant names,
rule identifiers and narrative detail routinely re-identify a case.

## What is safe

- **Synthetic notes** written for practice or demonstration.
- **Fully neutralised notes** — stripped of names, identifiers, case and account references,
  internal system and rule-name strings, and any distinguishing amount/date combination — where
  neutralisation was carried out under a documented process, not ad hoc.

## The narrow exception

Real notes may be appropriate **only** where all of the following hold:

1. your organisation runs an enterprise agreement whose terms cover this category of data;
2. that agreement has been reviewed and the deployment approved by the people responsible for it
   — data protection, information security, compliance;
3. your organisation has explicitly permitted this specific use, in writing;
4. any works-council or employee-representation consultation your jurisdiction requires has
   happened.

Your own judgement that it is "probably fine" is not one of these four. If you are unsure whether
your organisation has done 1–4, it has not, and the answer is no.

## If a real note is pasted anyway

The assistant checks for this before reviewing (SKILL.md §2): if the pasted material looks like
real case content, it says so briefly and proceeds only if the user confirms the exception above
applies. Two limits on that check, stated plainly rather than implied:

- **It is a heuristic, not a detector.** Real and fully neutralised notes can be textually
  indistinguishable — a well-neutralised note may trigger the check unnecessarily, and a real note
  with the more obvious identifiers already stripped may pass it unnoticed.
- **It is bypassable in one sentence.** A user who simply says "it's synthetic" satisfies the
  check regardless of whether that is true. The check cannot verify the claim.

Its purpose is to prompt the question at the point it matters, not to guarantee the answer. It
cannot undo a disclosure that has already happened — the point of asking is that the user is
prompted to raise it, not that the assistant can prevent or detect it.
