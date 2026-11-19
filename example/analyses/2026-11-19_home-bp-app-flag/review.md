# Review · 2026-11-19_home-bp-app-flag

*Written by a session that did not plan or execute the analysis (`ROLES.md § 4`). A
verdict is a command and its output, not an opinion. The file shows the latest review
only; earlier rounds live in git history.*

**Reviewer:** separate session, Claude Fable 5.2 (executor: Claude Opus 5.5) · **Date:** 2026-11-19 · **Commit reviewed:** d62d117

*Synthetic example. No web access in this session: sources could not be opened.*

## Expectation before reading the results
No independent expectation. This session read the previous review (of commit `d1bc466`),
including its numbers, before recomputing anything. The recomputation below was still
written without importing or copying `analysis.py`.

## Checks

Scratch code: `/tmp/final-review-2/recompute.py`, written by the reviewer, standard
library only, reading the raw CSV directly. Planted errors were made in a scratch clone
(`/tmp/final-review-2/copy`), never in the repository. The six fixes requested by the
previous review are followed up in output 4.

| # | Check | Command | Output | Verdict |
|---|---|---|---|---|
| 1 | Script reruns and reproduces every number in `reanalysis.md` § 5 | `python3 -B example/data-folder/home-bp-app/generate.py --check`; `python3 -B example/analyses/2026-11-19_home-bp-app-flag/analysis.py --check`; `python3 -B tools/check.py`; `python3 -I recompute.py <raw csv>` | `OK, committed file matches the generator`, exit 0; `OK, results reproduce exactly`, exit 0; `check.py: OK (77 files checked, 4 warning(s))`, exit 0; own recomputation matches every row of § 5 and all 38 rows of `results.csv` (output 1) | ✅ |
| 2 | Every field used is documented in `semantics/` | Each column of `head -1 <raw csv>` searched with `grep -c -F` in `example/semantics/sources/home-bp-app/reading.md` | 7 of 7 columns found (1 or 2 hits each). `Category` has no provider documentation and is used only as a secondary endpoint | ✅ |
| 3 | Every number meets METHOD § 2 | Each number in `reanalysis.md`, `conclusion.md`, `example/README.md`, `example/results.md` and `example/status/follow-up.md` compared with `results.csv` | All numbers in § 5 and in the conclusion have a row, a denominator and dates. One result in `reanalysis.md` § 10 (77.1 to 79.6, AHA/ACC rejected) has no row and is not produced by `analysis.py`, although the file's header says every number is (finding 2) | ❌ |
| 4 | Thresholds match their cited sources, opened and read. Without web access: could not be checked | None possible | Could not be checked. Internal agreement only: 135/85, 130/80, 120/70, 180/120 and 5 mmHg are the same in `plan.md`, `analysis.py`, `reanalysis.md` § 8 and the knowledge file | Could not be checked |
| 5 | Preregistration commit exists and precedes the data; changes after it are listed | `git log --format=%h -- <file>` for raw CSV, `plan.md`, `results.csv`; `git show --stat b68dc6e d1bc466`; `git diff b68dc6e d1bc466 -- plan.md results.csv`; `git diff d1bc466 HEAD` | Raw CSV: `b68dc6e` only. Plan and results: `b68dc6e`, `d1bc466`, `d62d117`. No commit precedes the data; § 9 says so ("not provable"), which is the honest statement. § 9 now has one line per commit and the owner's approval. Three plan changes are still not in the list (finding 3) | ✅ for the statement, ❌ for the list |
| 6 | Negative statements have positive controls | Same filter with a lower limit; a wrong label rule; both in `recompute.py` | Above 180/120: 0 of 81, and 0 of 84 raw rows; control above 140/85: 13 of 81. Highest readings 145/70 and 133/89. Label rule matches 81 of 81; a wrong rule (140/90 only) matches 10 of 81, so the test can fail | ✅ |
| 7 | A planted error is caught by the analysis checks | Ten plants in the scratch clone, then `analysis.py`, both `--check` commands and `tools/check.py` (output 3) | Changed reading, changed thresholds, a reading above 180/120 among the analysed rows, struck text and a revision heading are all caught. A reading above 180/120 in the excluded `cuff loose` row is not caught (finding 1) | ✅ except finding 1 |
| 8 | No data files and no living file dependencies | `git ls-files` filtered for data extensions; `grep -n 'status/'` in the analysis folder | Two CSV files tracked, both synthetic and inside `example/data-folder/`. One mention of `status/`, a write permission in `plan.md` § 4; no value is taken from a status file | ✅ |
| 9 | `conclusion.md` within one page, section 5 filled in, no advice or urgency without a source | Word count without table rows and headings; search for advice and urgency words | 398 words (384 without the header lines); tables have 2 columns; section 5 has four points including "No trigger fired does not mean the value is unimportant; this method cannot rule out disease." Two hits for advice or urgency words: a question to the clinician ("Should my overall cardiovascular risk be assessed?") and "No source used here makes it urgent". No advice, no deadline | ✅ |
| 10 | The statistics hold: assumptions stated, an alternative analysis or threshold source tried, the conclusion follows from the numbers | Alternatives in `recompute.py` (output 2) | Assumptions and device error are stated in `reanalysis.md` § 4 and `plan.md` § 3. § 10 now says correctly that the averaging unit also changes the AHA/ACC decision; own recomputation gives the same interval. The conclusion follows from the numbers | ✅ |

### Output 1: own recomputation from the raw CSV

```
raw 84 dup 2 loose 1 analysed 81 dates 2026-09-02 2026-11-14
above 180/120: 0 | control above 140/85: 13
PRIMARY days 6 readings 24 [4, 4, 4, 4, 4, 4] t 2.5706
  sys 125.542 CI 122.595..128.489 | dia 78.375 CI 76.071..80.679
  ESC 135/85: rejected | AHA/ACC 130/80: inconclusive
  margins: ESC 6.51/4.32 AHA 1.51/-0.68
  ESC elevated band (>=120 or >=70, and <135 and <85): True
SENS all7 days 7 readings 28 [4, 4, 4, 4, 4, 4, 4] t 2.4469
  sys 126.000 CI 123.377..128.623 | dia 78.321 CI 76.463..80.179
  ESC 135/85: rejected | AHA/ACC 130/80: inconclusive
everyday 53 2026-09-02 2026-11-07 Stage1or2 40/53 no note n=26 128.69/77.46 note n=27 134.07/81.59
highest sys 145/70 2026-09-10 | highest dia 133/89 2026-10-02
label rule match 81/81 | wrong rule (140/90 only) match 10
comparisons: 81 alarm + 8 guideline + 2 ESC band = 91
```

The t quantile was computed by numerical integration, not taken from a table. Every
value rounds to the value in `results.csv`. The primary endpoint (125.5/78.4, 24
readings, 6 complete days, 2026-11-09 to 2026-11-14) and both decisions (ESC 2024
rejected, AHA/ACC inconclusive) are confirmed.

### Output 2: alternative analyses (primary days)

```
ALT unit=24 readings: t 2.0687 sys 123.57..127.51 dia 77.13..79.62 ESC rejected AHA rejected
ALT device bias -5: ESC rejected AHA rejected
ALT device bias +5: ESC inconclusive AHA supported
ALT morning n=12 124.25/78.42 evening n=12 126.83/78.33
```

`reanalysis.md` § 10 gives 77.1 to 79.6 and "rejected" for the 24 reading unit: correct.
A constant device error of 5 mmHg moves both decisions, as § 6 says. With six day means,
normality and independence cannot be tested; they stay assumptions.

### Output 3: planted errors (scratch clone)

| Plant | Command and output |
|---|---|
| None (control) | `analysis.py --check`: `OK, results reproduce exactly`, exit 0 |
| Protocol reading 2026-11-10 07:05 changed from 118/75 to 185/121 | `analysis.py`: `STOP: reading above 180/120 (185/121 on 2026-11-10 07:05). Tell the owner now (trigger T1); nothing else is computed or written.`, exit 1. `sha256sum` of `results.csv` unchanged; `git status` shows only the planted file. With `results.csv` deleted first: exit 1 and no file is created. `--check`: same message, exit 1 |
| Everyday reading 2026-09-02 changed to 181/76 (systolic only) | `STOP: reading above 180/120 (181/76 on 2026-09-02 12:54)`, exit 1, nothing written |
| Everyday reading changed to exactly 180/120 (control: not above) | Runs, `readings_above_alarm_180_120,0`, exit 0 |
| The excluded `cuff loose` reading (2026-10-17 18:40) changed from 98/61 to 190/125 | `analysis.py`: no message, exit 0, results written (finding 1) |
| Protocol reading 2026-11-12 07:05 diastolic 83 changed to 73 | `analysis.py --check`: `MISMATCH`, exit 1. `generate.py --check`: `MISMATCH`, exit 1 |
| AHA/ACC threshold in the script changed to 135/85 | `analysis.py --check`: `MISMATCH`, exit 1 |
| ESC elevated band in the script changed to 130/80 | `analysis.py --check`: `MISMATCH`, exit 1 |

| Plant in a document | `tools/check.py` |
|---|---|
| None (control) | `check.py: OK (77 files checked, 4 warning(s))`, exit 0 |
| A line with struck text (two tildes around a number) added to `conclusion.md` | `ERROR: struck through text in example/analyses/2026-11-19_home-bp-app-flag/conclusion.md:63; keep one truth, git holds history`, exit 1 |
| A level 2 heading "Revision 2" added to `conclusion.md` | `ERROR: revision section in example/analyses/2026-11-19_home-bp-app-flag/conclusion.md:63; keep one truth, git holds history`, exit 1 |
| A level 3 heading "revision history" (lower case) added to `METHOD.md` | `ERROR: revision section in METHOD.md:364; keep one truth, git holds history`, exit 1 |
| Two tildes inside a fenced block and inside inline code (control) | OK, exit 0 |
| A heading "Round 2 review", a bold "Revision 2:" line and a table with a Revision column | OK, exit 0 (not caught, finding 5) |
| Mean in `conclusion.md` changed to 135.5/78.4 | OK, exit 0 (not caught, finding 5) |

### Output 4: the previous review's fixes, verified against `d62d117`

| Fix requested | Verified how | Result |
|---|---|---|
| 1. § 10 states that the averaging unit changes the AHA/ACC decision | Read § 10; recomputed the 24 reading interval (output 2) | Closed. The numbers are right; they have no result row (finding 2) |
| 2. `analysis.py` stops on a reading above 180/120 | Three plants (output 3) | Closed for the 81 analysed readings: exit 1, nothing written. Open for the excluded row (finding 1) |
| 3. § 9 lists changes by commit | `git show --stat` of `b68dc6e` and `d1bc466`, both diffs | Partly closed: one line per commit, owner approval stated. Three items missing, and the third commit is named by position, not by hash (finding 3) |
| 4. ESC elevated band has a result row and is counted | `grep` in `results.csv`; own recomputation | Closed. `primary_mean_in_esc_home_elevated_band,True`; count 81 + 8 + 2 = 91 in `analysis.py`, `results.csv`, `plan.md` § 3 and § 9. `follow-up.md` ("ESC elevated range") now has a row behind it |
| 5. `generate.py` no longer says office cut points | `grep -c -i office generate.py`; control `grep -c 'AHA/ACC'` | Closed. 0 hits (control: 2 hits); `generate.py --check` OK. The remaining "office" hits in the repository are correct statements that AHA/ACC use 130/80 at home as in the office |
| 6. Conclusion wording | Read `conclusion.md` § 5 and § 8 against the knowledge file, line 61 | Closed. "up to 5 mmHg off on average" matches the criterion (mean difference up to 5 mmHg); "would narrow it" no longer promises a settled answer |
| `tools/check.py` (not required last time) | Two plants (output 3) | Rejects struck text and revision headings |

Agreement between files: mean 125.5/78.4, ESC below or rejected, AHA/ACC inconclusive
or "unresolved", label rule per reading 81 of 81 and status ESCALATED (T7) are the same
in `results.csv`, `conclusion.md`, `reanalysis.md`, `example/README.md`,
`example/results.md` and `example/status/follow-up.md`. Search of the repository for
struck text and for headings starting with Revision or Round, this file excluded: 0 hits
in text (4 in `tools/check.py`, all code or its description; 1 in `METHOD.md` line 208,
the rule itself).

## Findings, ranked by consequence
1. **Wrong meaning or wrong number:**
   - No wrong number found. Primary endpoint, both guideline decisions and every row of
     `results.csv` reproduce from the raw CSV with independent code.
   - **Finding 1.** The alarm check runs after the `cuff loose` exclusion, so it covers
     81 of the 84 raw rows. A reading of 190/125 in the excluded row does not stop the
     script (output 3). METHOD § 5 says "every single value is checked against the alarm
     limits", and the brief, field 11, asks to be told about any reading that looks
     dangerous. In this data the excluded reading is 98/61 and the two duplicates equal
     rows that are checked, so "0 of 81" is also 0 of 84 and nothing is wrong today. The
     gap is narrow, but it is in the safety rule.
2. **Reproducibility:**
   - **Finding 2.** `reanalysis.md` § 10 reports a result (diastolic interval 77.1 to
     79.6 with 24 readings as the unit, AHA/ACC rejected) that `analysis.py` does not
     compute and `results.csv` does not hold. The header of the same file says "Every
     number below is printed by `analysis.py` and stored in" `results.csv`. The numbers
     are correct (output 2), but `--check` cannot notice if they stop being true.
   - **Finding 3.** § 9 is now organised by commit and states the owner's approval. Still
     missing against `git diff b68dc6e d1bc466 -- plan.md` and the plan in `b68dc6e`:
     the asserted counts of duplicates and exclusions with the uniqueness check (a
     method change, METHOD § 5); the changed reason for discarding day 1; the scope
     note. The line for the newest commit does not mention that the comparison count
     went from 89 to 91, and names the commit "the commit after `d1bc466`"; its hash is
     `d62d117`.
3. **Form:**
   - **Finding 4.** `plan.md` § 3 step 3 says the safety check comes "before anything
     else", but it is listed, and run, after validation, deduplication and exclusion.
     Fixing finding 1 should make the text and the order agree.
   - **Finding 5.** `tools/check.py` catches struck text and headings that start with
     "Revision". It does not catch headings such as "Round 2", revision tables (which
     METHOD § 8 also forbids) or a document number that differs from `results.csv`
     (output 3). This concerns the tool, not the example, and is not required for green.

## Verdict
❌ fixes needed. No number and no part of the answer changes. Five of the previous
review's six fixes are closed in full or for the data as it is; the three fixes below
are small.

| Fix | Expected result after the fix |
|---|---|
| 1. `analysis.py`: check every raw reading against 180/120 before the `cuff loose` exclusion; align `plan.md` § 3 step 3, the "0 of 81" denominator and the comparison count with what is then checked | The `cuff loose` row planted as 190/125: non zero exit, the STOP message, nothing written. Unchanged data: `analysis.py --check` OK |
| 2. Add the 24 reading variant to `analysis.py` and `results.csv` (interval ends and the AHA/ACC decision), or correct the header sentence in `reanalysis.md` and say where the § 10 numbers come from | Every computed number in `reanalysis.md` has a row in `results.csv`, or the header no longer claims it. `analysis.py --check` OK |
| 3. `reanalysis.md` § 9: add the three missing items to the commit where each happened, the count change 89 to 91, and the hash `d62d117` | Every difference in `git diff b68dc6e d1bc466 -- plan.md` and `git diff d1bc466 d62d117 -- plan.md results.csv` can be found in § 9; each commit is named by hash |

Could not be checked in this review: every threshold against its source (check 4).
The next review with web access must open each source in `reanalysis.md` § 8.
