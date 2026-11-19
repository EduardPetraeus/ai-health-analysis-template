# Review · 2026-11-19_home-bp-app-flag

*Written by a session that did not plan or execute the analysis (`ROLES.md § 4`). A
verdict is a command and its output, not an opinion. The file shows the latest review
only; earlier rounds live in git history.*

**Reviewer:** separate session, Claude Fable 5.2 (executor: Claude Opus 5.5) · **Date:** 2026-11-19 · **Commit reviewed:** d1bc466

*Synthetic example. No web access in this session: sources could not be opened.*

## Expectation before reading the results
Written after `METHOD.md`, `ROLES.md` § 4, the template, `brief.md` and `plan.md`, before
any data value, `results.csv`, `reanalysis.md` or `conclusion.md` was opened:

> The protocol week mean (days 2 to 7) is lower than the everyday readings and lands
> between the two home thresholds: roughly 126 to 133 systolic and 78 to 84 diastolic.
> ESC 2024 (135/85) rejected or inconclusive; AHA/ACC (130/80) inconclusive or
> supported. The guidelines probably disagree, so T7 fires. No reading above 180/120.
> The app label is probably a per reading rule with 130/80 cut points.

Outcome: decisions, T7, alarm count and label rule as expected. The mean (125.5/78.4)
is slightly lower than the expected range.

## Checks

Scratch code: `recompute.py` and `docnums.py`, written by the reviewer, standard library
only, reading the raw CSV directly. `analysis.py` was not imported. Planted errors were
made in a scratch copy of the repository, never in the repository itself.

| # | Check | Command | Output | Verdict |
|---|---|---|---|---|
| 1 | Script reruns and reproduces every number in `reanalysis.md` § 5 | `python3 -B example/data-folder/home-bp-app/generate.py --check`; `python3 -B example/analyses/2026-11-19_home-bp-app-flag/analysis.py --check`; `python3 -B tools/check.py`; `python3 -I recompute.py <raw csv>` | `OK, committed file matches the generator`; `OK, results reproduce exactly`; `check.py: OK (77 files checked, 4 warning(s))`; own recomputation matches every row of § 5 (output 1 below) | ✅ |
| 2 | Every field used is documented in `semantics/` | Each column of `head -1 <raw csv>` searched in `reading.md` | 7 of 7 columns found in the delivery table; `Category` marked partial and used only as a secondary endpoint | ✅ |
| 3 | Every number meets METHOD § 2 | `python3 -I docnums.py results.csv <six documents>` plus reading | 0 decimal or ratio values outside `results.csv` or the cited thresholds in `conclusion.md` (19 values), `reanalysis.md` (29), `example/README.md` (5), `follow-up.md` (2). Denominators, dates and exclusions are written with the numbers. One statement has no row behind it (finding 4) | ✅ |
| 4 | Thresholds match their cited sources, opened and read. Without web access: could not be checked | None possible | Could not be checked. Internal agreement only: 135/85, 130/80, 120/70, 180/120 and 5 mmHg are the same in `plan.md`, `analysis.py`, `reanalysis.md` § 8 and the knowledge file | Could not be checked |
| 5 | Preregistration commit exists and precedes the data; changes after it are listed | `git log --format=%h -- <file>` for raw CSV, `plan.md`, `results.csv`; `git diff b68dc6e d1bc466 -- plan.md results.csv` | Raw CSV: `b68dc6e`. Plan and results: `b68dc6e`, `d1bc466`. Data, plan and result entered git in the same first commit, so no commit precedes the data. § 9 says so ("not provable"). The list of later changes is incomplete and names no commit (finding 3) | ❌ |
| 6 | Negative statements have positive controls | Same filter with a lower limit; boundary counts in `recompute.py` | Above 180/120: 0 of 81; control above 140/85: 13 of 81. Highest readings 145/70 and 133/89. Systolic exactly 140: 0, diastolic 90 or more: 0; control systolic 140 or more: 6. Wrong label rule (140/90 only) matches 26 of 81, so the 81 of 81 test can fail | ✅ |
| 7 | A planted error is caught by the analysis checks | Eight plants in a scratch copy, then both `--check` commands and `tools/check.py` (output 3 below) | Changed reading, deleted session, extra duplicate, changed threshold and changed label are all caught. A planted 185/121 reading gives only `MISMATCH` and, in a normal run, exit 0 (finding 2). Document plants are not caught by `tools/check.py` (finding 7) | ✅ for data and thresholds, ❌ for the alarm |
| 8 | No data files and no living file dependencies | `git ls-files` filtered for data extensions; search for `status/` in the analysis folder | Two CSV files tracked, both synthetic and inside `example/data-folder/`. One mention of `status/`, a write permission in `plan.md` § 4; no value is taken from a status file | ✅ |
| 9 | `conclusion.md` within one page, section 5 filled in, no advice or urgency without a source | Word count without table rows, headings and header; search for advice and urgency words | 388 words; tables have 2 columns; section 5 has four points including "No trigger fired does not mean the value is unimportant; this method cannot rule out disease." No deadline, no urgency ("No source used here makes it urgent"), no advice. Two wording points (finding 6) | ✅ |
| 10 | The statistics hold: assumptions stated, an alternative analysis or threshold source tried, the conclusion follows from the numbers | Alternatives in `recompute.py` (output 2 below) | Assumptions and device error are stated in `reanalysis.md` § 4 and `plan.md` § 3. The conclusion follows from the numbers. One alternative changes the AHA/ACC decision, and § 10 says none does (finding 1) | ✅ with finding 1 |

### Output 1: own recomputation from the raw CSV

```
raw_rows 84   duplicates 2   cuff loose 1 (2026-10-17 18:40 98/61)   analysed 81
date range 2026-09-02 to 2026-11-14 (74 calendar days)
PRIMARY days 2 to 7: days=6 incomplete=0 readings=24 (4 per day) t=2.5706
   sys mean 125.542 CI 122.595 to 128.489 | dia mean 78.375 CI 76.071 to 80.679
   ESC 135/85: rejected   AHA/ACC 130/80: inconclusive
   margins upper end: ESC 6.51/4.32  AHA 1.51/-0.68
SENSITIVITY all 7 days: days=7 readings=28 t=2.4469
   sys mean 126.000 CI 123.377 to 128.623 | dia mean 78.321 CI 76.463 to 80.179
   ESC 135/85: rejected   AHA/ACC 130/80: inconclusive
everyday 53 (2026-09-02 to 2026-11-07), Stage 1 or 2: 40/53
   no note: n=26 mean 128.69/77.46     with note: n=27 mean 134.07/81.59
highest sys 145/70 on 2026-09-10 | highest dia 133/89 on 2026-10-02
label = per reading AHA/ACC rule: 81/81      comparisons 81 + 8 = 89
```

The t quantile was computed by numerical integration, not taken from a table. Every
value rounds to the value in `results.csv`.

### Output 2: alternative analyses (primary days)

```
all 24 readings as the unit: sys 123.57 to 127.51, dia 77.13 to 79.62 -> ESC rejected, AHA/ACC rejected
morning only (n=12): 124.25/78.42      evening only (n=12): 126.83/78.33
device bias -5 mmHg: ESC rejected, AHA/ACC rejected
device bias +5 mmHg: ESC inconclusive, AHA/ACC supported
```

A constant device error of 5 mmHg moves both decisions, as `reanalysis.md` § 6 says.
With six day means, normality and independence cannot be tested; they stay assumptions.

### Output 3: planted errors (scratch copy)

| Plant | `analysis.py --check` | `generate.py --check` |
|---|---|---|
| None (control) | OK, exit 0 | OK, exit 0 |
| One protocol diastolic 80 changed to 70 | MISMATCH, exit 1 | MISMATCH, exit 1 |
| One evening session deleted (2 rows) | `AssertionError: expected 84 rows, got 82`, exit 1 | MISMATCH, exit 1 |
| A third duplicate row added | `AssertionError: expected 84 rows, got 85`, exit 1 | MISMATCH, exit 1 |
| AHA/ACC threshold in the script changed to 135/85 | MISMATCH, exit 1 | OK, exit 0 |
| One label changed from Elevated to Normal | MISMATCH, exit 1 | MISMATCH, exit 1 |
| One reading changed to 185/121 | MISMATCH, exit 1. Normal run: `readings_above_alarm_180_120,1`, results written, exit 0 | MISMATCH, exit 1 |

| Plant in a document | `tools/check.py` |
|---|---|
| `conclusion.md` mean changed to 135.5/78.4 | `check.py: OK`, exit 0 (not caught) |
| A numbered revision heading and struck text added to `conclusion.md` | `check.py: OK`, exit 0 (not caught) |

### Output 4: agreement between files, and leftover text

| Statement | `results.csv` | conclusion | reanalysis | example README | follow-up | results.md |
|---|---|---|---|---|---|---|
| Mean 125.5/78.4 | yes | same | same | same | same | not stated |
| ESC: below 135/85, rejected | rejected | same | same | same | "ESC elevated range" (finding 4) | same |
| AHA/ACC 130/80: inconclusive | inconclusive | "unresolved" | same | "unresolved", 80.7 | "unresolved" | "unresolved" |
| Label rule per reading, 81 of 81 | 81/81 | per reading | same | "US stage cut points", 81 of 81 | not stated | "US cut points per reading" |
| Flag status | not a metric | ESCALATED (T7) | not stated | not stated | ESCALATED (T7) | not stated |

The knowledge file gives the same thresholds (ESC home 135/85, AHA/ACC home stage 1
130/80, alarm above 180/120, ISO mean error up to 5 mmHg). No contradiction found
between the six files.

Search of the whole repository, `.git` excluded, case insensitive, this file excluded:

| Search | Hits |
|---|---|
| Two tildes (struck text) | 0 in text. 2 in `tools/check.py`, both code that recognises fenced blocks |
| Numbered revision or round headings | 0 |
| The word "revision" | 1: `METHOD.md` line 208, the rule itself |
| "office" | 2 leftovers: `example/data-folder/home-bp-app/generate.py` lines 16 to 17 and line 46 describe the app as "using office blood pressure cut points" (finding 5). All other hits are correct statements that AHA/ACC use 130/80 at home as in the office |

Positive control: the same searches on the previous content of this file gave 70 hits
for numbered rounds and 8 for "office".

## Findings, ranked by consequence
1. **Wrong meaning or wrong number:**
   - **Finding 1.** `reanalysis.md` § 10 says of the free choices (day 1, the averaging
     unit, the complete day rule, which guideline): "Only the guideline changes a
     decision." That is not true for the unit. With the 24 readings as the unit the
     diastolic interval is 77.1 to 79.6 and the AHA/ACC decision becomes rejected
     (output 2). The plan's choice of days as the unit is right, because readings
     within a day are not independent, but the US answer depends on it and the file
     says the opposite. No number in `results.csv` is wrong.
   - **Finding 2.** A reading above 180/120 does not stop `analysis.py`. It is written
     as one row among 37 and the run exits 0 (output 3). METHOD § 5 says a hit "stops
     everything and goes to the owner at once", and the brief, field 11, asks for the
     same. No reading is above the limit in this data, so nothing is wrong today; the
     script is meant to be rerun unchanged on new data.
   - No wrong number found. Primary endpoint, both guideline decisions and all
     secondary numbers reproduce from the raw CSV with independent code.
2. **Reproducibility:**
   - **Finding 3.** `reanalysis.md` § 9 states honestly that preregistration is not
     provable, and lists the main changes made after the first result. It names no
     commit, although METHOD § 8 asks for one line per commit, and the list is
     incomplete against `git diff b68dc6e d1bc466`. Missing: kind of analysis changed
     from confirmatory to retrospective; the measurement error step and the four
     margins; the asserted counts of duplicates and exclusions and the uniqueness
     check; the comparison count from 2 to 89; the reason given for discarding day 1;
     the scope note; the cause of the duplicates changed from app sync to not
     documented; three result rows removed. It also does not say whether the changed
     plan went back to the owner (METHOD § 5), while `plan.md` still reads "approved".
   - **Finding 4.** `example/status/follow-up.md` says the mean is in the "ESC elevated
     range". The statement is true (own check: 125.5/78.4 is at or above 120/70 and
     below 135/85), but `results.csv` has no row for it since `d1bc466` removed
     `primary_in_esc_home_elevated_range`, and the comparison is not among the 89
     counted in § 9. T7 rests partly on it.
3. **Form:**
   - **Finding 5.** `generate.py` still describes the label as "office cut points"
     (two places). The semantics file says the cut points are the AHA/ACC ones, the
     same at home and in the office. Comment text only; the generated file is not
     affected.
   - **Finding 6.** `conclusion.md` § 5: "a validated cuff may read up to 5 mmHg off"
     leaves out "on average"; the knowledge file gives the criterion as a mean
     difference with a standard deviation up to 8 mmHg, so a single cuff on a single
     person can be further off. § 8: "would settle it" promises more than a second week
     can; it may again be inconclusive.
   - **Finding 7.** `tools/check.py` has no check for struck text, revision sections or
     document numbers that differ from `results.csv` (output 3). The one truth rule is
     checked by hand only. This concerns the tool, not the example, and is not required
     for green.

## Verdict
❌ fixes needed. No number and no part of the answer changes.

| Fix | Expected result after the fix |
|---|---|
| 1. `reanalysis.md` § 10: state that the unit of the interval also changes the AHA/ACC decision, with the numbers; preferably add the variant as rows in `results.csv` | § 10 names two choices that change a decision (guideline; unit: 77.1 to 79.6 diastolic, AHA/ACC rejected) and says why days are used. `analysis.py --check` passes |
| 2. `analysis.py`: stop on any reading above 180/120, before any mean is computed | Planted 185/121 reading: non zero exit, a message with the reading and the AHA instruction, no results written. Unchanged data: `--check` still OK |
| 3. `reanalysis.md` § 9: one line per commit (`b68dc6e`: data, plan and first result together; `d1bc466`: second set of changes), the missing items from finding 3, and whether the owner approved the changed plan | Every difference in `git diff b68dc6e d1bc466 -- plan.md results.csv` can be found in § 9 |
| 4. Restore a result row for the ESC elevated range and count the comparison, or remove the phrase from `follow-up.md` | "ESC elevated range" has a row in `results.csv`; the count in § 9 and `comparisons_against_a_reference` include it |
| 5. `generate.py`: replace "office cut points" with the AHA/ACC cut points per reading | Searching "office" in `generate.py` gives 0 hits; `generate.py --check` still OK |
| 6. `conclusion.md`: "up to 5 mmHg off on average"; "could settle it" | Both sentences match the knowledge file and § 9; still at most about 400 words |

Could not be checked in this review: every threshold against its source (check 4).
The next review with web access must open each source in `reanalysis.md` § 8.
