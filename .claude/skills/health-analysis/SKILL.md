---
name: health-analysis
description: Run a personal health data analysis with the method in this repository (brief, hypothesis first, source agreement, five phases with a stop before any calculation, reanalysis, independent review, one page conclusion). Use for any analysis, baseline, lab report or wearable interpretation, extract from a PDF or export, or update of status files in this folder.
---

# Health analysis

This skill is a workflow and a list of mistakes to avoid. **It points to the rules;
where it summarizes one, the repository file wins** and this skill is out of date.

## Step 0: read, in this order

1. `START_HERE.md`: rule 0, hard rules, router.
2. `results.md`: is the question already answered?
3. `METHOD.md`: all of it.
4. `ROLES.md` § 3: what only the owner approves.
5. `learnings.md`: patterns that cost errors before.
6. Whatever the router points to for this task.

## The workflow

1. **Brief.** Copy `templates/brief.md` into `analyses/YYYY-MM-DD_<topic>/`. Interview
   the owner one field at a time, safety questions first. Fields 8 and 9 in the owner's
   own words, before you open any data values and before you suggest anything. Commit
   the brief as soon as fields 8 and 9 are written. Recommend level 1 until the owner has
   closed an analysis.
2. **Semantics.** Every field the analysis will use is documented in `semantics/` from
   official sources, or marked undocumented and not used for conclusions.
3. **Plan.** `templates/plan.md`, phases 0 to 3, ending with the owner overview.
4. **Stop.** End your turn and wait for the owner's "ok". No script, no number, no file
   with results before that. Then commit the plan.
5. **Execute.** `analysis.py` in the analysis folder; data outputs to the data folder.
   Check every value against the T1 alarm limit first. **A hit ends the analysis:** quote
   the source, stop, offer nothing else, even if asked. Validate before writing; fail
   hard. Write `reanalysis.md` as you go, then `conclusion.md`.
6. **Review.** A separate session reruns everything, the conclusion included
   (`templates/review.md`), and commits `review.md`. The executing session fixes rank 1
   and 2 findings; a new review session follows.
7. **Close.** Flags in `status/follow-up.md`, a row in `results.md`, the closing
   checklist in METHOD § 12, then `python3 tools/check.py`.

## Mistakes this method has paid for

- Reporting "nothing found" from a search that could not have found anything. Run a
  positive control first: `tools/extract_checks.py`.
- Using a percentage without its denominator.
- Reading a provider's label ("stage 1", "elevated") as a fact instead of finding the
  definition and the measurement it assumes.
- Turning a document date into an event date.
- Letting the same session that wrote the plan review it.
- Offering to continue past an alarm value because the owner feels fine. The owner cannot
  waive T1.
- Writing "all 9 days" when it was 8: every counted claim in the conclusion needs a
  command output.
- Telling the owner "a hook blocked it" when a tool permission was denied.
- Asking three things in one message.

## Never

- Present a result as a diagnosis or a treatment recommendation (`DISCLAIMER.md`).
- Write data into the repository.
- Write your recommendation into a file as if it were the owner's decision.
