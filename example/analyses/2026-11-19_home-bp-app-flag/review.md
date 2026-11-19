# Review · 2026-11-19_home-bp-app-flag

*Written by a session that did not plan or execute the analysis (`ROLES.md § 4`). A
verdict is a command and its output, not an opinion. The file shows the latest review
only; earlier rounds live in git history.*

**Reviewer:** separate session, Claude Fable 5.2 (executor: Claude Opus 5.5) · **Date:** 2026-11-19 · **Commit reviewed:** 5fc0b38

*Synthetic example. No web access in this session: sources could not be opened.*

## Expectation before reading the results
No independent expectation. This session read the previous review (of commit `d62d117`),
including its numbers, before recomputing anything. The recomputation below was still
written without importing or copying `analysis.py`.

## Checks

Scratch code: `/tmp/final-review-3/recompute.py`, written by the reviewer, standard
library only, reading the raw CSV directly. Planted errors were made in a scratch clone
(`/tmp/final-review-3/copy`, at `5fc0b38`), never in the repository. The three fixes
requested by the previous review are followed up in output 4.

| # | Check | Command | Output | Verdict |
|---|---|---|---|---|
| 1 | Script reruns and reproduces every number in `reanalysis.md` § 5 | `python3 -B example/data-folder/home-bp-app/generate.py --check`; `python3 -B example/analyses/2026-11-19_home-bp-app-flag/analysis.py --check`; `python3 -B tools/check.py`; `python3 -I recompute.py <raw csv>` | `generate.py --check: OK, committed file matches the generator`, exit 0; `analysis.py --check: OK, results reproduce exactly`, exit 0; `check.py: OK (77 files checked, 4 warning(s))`, exit 0; own recomputation matches every row of § 5 and all 41 rows of `results.csv` (output 1) | ✅ |
| 2 | Every field used is documented in `semantics/` | Each column of `head -1 <raw csv>` searched with `grep -c -F` in `example/semantics/sources/home-bp-app/reading.md` | 7 of 7 columns found (1 or 2 hits each). `Category` has no provider documentation and is used only as a secondary endpoint | ✅ |
| 3 | Every number meets METHOD § 2 | Each number in `reanalysis.md`, `conclusion.md`, `example/README.md`, `example/results.md` and `example/status/follow-up.md` compared with `results.csv` | Every number in § 5, § 10 and the conclusion has a row, a denominator and dates. The § 10 interval (77.1 to 79.6) and its decision now have rows `alt_readings_unit_*`. The alarm count reads "0 of 84 raw readings" with the row `raw_readings_above_alarm_180_120,0` | ✅ |
| 4 | Thresholds match their cited sources, opened and read. Without web access: could not be checked | None possible | Could not be checked. Internal agreement only: 135/85, 130/80, 120/70, 180/120 and 5 mmHg are the same in `plan.md`, `analysis.py`, `reanalysis.md` § 8 and the knowledge file | Could not be checked |
| 5 | Preregistration commit exists and precedes the data; changes after it are listed | `git log --format=%h -- <file>` for raw CSV, `plan.md`, `results.csv`; `git diff b68dc6e d1bc466 -- plan.md`; `git diff d1bc466 d62d117 -- plan.md results.csv`; `git diff d62d117 HEAD -- plan.md results.csv analysis.py`; `git show b68dc6e:<plan.md>` | Raw CSV: `b68dc6e` only. Plan and results: `b68dc6e`, `d1bc466`, `d62d117`, `5fc0b38`. No commit precedes the data; § 9 says so ("not provable"), which is the honest statement. Every difference in the three diffs is found in § 9 under a commit (output 4) | ✅ |
| 6 | Negative statements have positive controls | Same filter with a lower limit; a wrong label rule; both in `recompute.py`. In the scratch clone: `ALARM` lowered to 140/90 in the script | Above 180/120: 0 of 84 raw rows; control above 140/85: 14 of 84. Highest readings 145/70 and 133/89. Script with the limit at 140/90: `STOP`, six readings listed, exit 1, so the stop can fire on this data. Label rule matches 81 of 81; a wrong rule (140/90 only) matches 10 of 81, so the test can fail | ✅ |
| 7 | A planted error is caught by the analysis checks | Fourteen plants in the scratch clone, then `analysis.py`, both `--check` commands and `tools/check.py` (output 3) | Every plant in the data or the script is caught, including a reading above 180/120 in the excluded `cuff loose` row and in the second copy of a duplicate pair. A changed number in a document is not caught by any tool (note 3) | ✅ |
| 8 | No data files and no living file dependencies | `git ls-files` filtered for data extensions; `grep -n 'status/'` in the analysis folder | Two CSV files tracked, both synthetic and inside `example/data-folder/`. One mention of `status/`, a write permission in `plan.md` § 4; no value is taken from a status file | ✅ |
| 9 | `conclusion.md` within one page, section 5 filled in, no advice or urgency without a source | Word count without table rows and headings; search for advice and urgency words | 396 words, 61 lines; tables have 2 columns; section 5 has four points including "No trigger fired does not mean the value is unimportant; this method cannot rule out disease." Two hits for advice or urgency words: a question to the clinician ("Should my overall cardiovascular risk be assessed?") and "No source used here makes it urgent". No advice, no deadline | ✅ |
| 10 | The statistics hold: assumptions stated, an alternative analysis or threshold source tried, the conclusion follows from the numbers | Alternatives in `recompute.py` (output 2) | Assumptions and device error are stated in `reanalysis.md` § 4 and `plan.md` § 3. The readings unit alternative in § 10 reproduces. The conclusion follows from the numbers | ✅ |

### Output 1: own recomputation from the raw CSV

```
raw 84 dup 2 loose 1 [('2026-10-17', '18:40', '98', '61')] analysed 81
raw above 180/120: 0 of 84 | control raw above 140/85: 14 of 84
date+time unique after dedup: True
PRIMARY days 6 (2026-11-09..2026-11-14) readings 24 all days am+pm True t 2.5706
  sys 125.542 CI 122.595..128.489 | dia 78.375 CI 76.071..80.679
  ESC 135/85: rejected | AHA/ACC 130/80: inconclusive
  margins ESC 6.51/4.32 AHA 1.51/-0.68
  ESC elevated band: True
SENS all7 days 7 (2026-11-08..2026-11-14) readings 28 all days am+pm True t 2.4469
  sys 126.000 CI 123.377..128.623 | dia 78.321 CI 76.463..80.179
  ESC 135/85: rejected | AHA/ACC 130/80: inconclusive
everyday 53 2026-09-02..2026-11-07 Stage1or2 40/53 no note n=26 128.69/77.46 note n=27 134.07/81.59
highest sys 145/70 2026-09-10 | highest dia 133/89 2026-10-02
label rule match 81/81 | wrong rule match 10
comparisons: 84 raw alarm + 8 guideline + 2 ESC band + 1 readings unit = 95
```

The t quantile was computed by numerical integration, not taken from a table. Every
value rounds to the value in `results.csv`. The primary endpoint (125.5/78.4, 24
readings, 6 complete days, 2026-11-09 to 2026-11-14) and both decisions (ESC 2024
rejected, AHA/ACC inconclusive) are confirmed.

### Output 2: alternative analyses (primary days)

```
ALT unit = 24 readings: t 2.0687 dia 77.131..79.619 -> rejected (dia vs 80)
  sys 123.573..127.510 | full rule AHA/ACC: rejected | ESC: rejected
ALT device bias -5: ESC rejected AHA rejected
ALT device bias +5: ESC inconclusive AHA supported
ALT morning n=12 124.25/78.42 evening n=12 126.83/78.33
```

`results.csv` holds `alt_readings_unit_dia_ci95_low,77.1`,
`alt_readings_unit_dia_ci95_high,79.6` and `alt_readings_unit_decision_aha_dia,rejected`:
all three match. A constant device error of 5 mmHg moves both decisions, as § 6 says.
With six day means, normality and independence cannot be tested; they stay assumptions.

### Output 3: planted errors (scratch clone)

`sha256sum` of `results.csv` before any plant starts with `70b4063a8fc7054e`.

| Plant | Command and output |
|---|---|
| None (control) | `analysis.py --check`: `OK, results reproduce exactly`, exit 0 |
| The excluded `cuff loose` reading (line 42, 2026-10-17 18:40) changed from 98/61 to 190/125 | `analysis.py`: `STOP: reading above 180/120 (190/125 on 2026-10-17 18:40). Tell the owner now (trigger T1); nothing else is computed or written.`, exit 1. `sha256sum` of `results.csv` unchanged (`70b4063a8fc7054e`); `git status --short` shows only the planted file. `--check`: same message, exit 1. With `results.csv` moved away first: exit 1 and no file is created |
| Same row changed to 181/61 (systolic only) | `STOP: reading above 180/120 (181/61 on 2026-10-17 18:40)`, exit 1, `results.csv` unchanged |
| Same row changed to 98/121 (diastolic only) | `STOP: reading above 180/120 (98/121 on 2026-10-17 18:40)`, exit 1, `results.csv` unchanged |
| Same row changed to exactly 180/120 (control: not above) | `analysis.py --check`: `OK, results reproduce exactly`, exit 0 |
| Same row changed to 255/130 (above the plausible range) | `AssertionError: SYS (mmHg)=255 outside [70, 250] in row 42: suspect a column shift`, exit 1, `results.csv` unchanged (note 2) |
| Second copy of a duplicate pair (line 14) changed to 200/100 | `STOP: reading above 180/120 (200/100 on 2026-09-15 16:20)`, exit 1 |
| Protocol reading 2026-11-10 07:05 changed from 118/75 to 185/121 | `STOP: reading above 180/120 (185/121 on 2026-11-10 07:05)`, exit 1, `results.csv` unchanged |
| Protocol reading 2026-11-12 07:05 diastolic 83 changed to 87 | `analysis.py --check`: `MISMATCH`, exit 1. `generate.py --check`: `MISMATCH`, exit 1 |
| AHA/ACC threshold in the script changed to 135/85 | `analysis.py --check`: `MISMATCH`, exit 1 |
| t quantile for 23 degrees of freedom changed to 2.807 | `analysis.py --check`: `MISMATCH`, exit 1; the rows become 76.7, 80.1 and `not rejected`, so the new rows can fail |
| Comparison count taken from the analysed rows instead of the raw rows | `analysis.py --check`: `MISMATCH`, exit 1 |

| Plant in a document | `tools/check.py` |
|---|---|
| None (control) | `check.py: OK (77 files checked, 4 warning(s))`, exit 0 |
| A line with struck text (two tildes around a number) added to `conclusion.md` | `ERROR: struck through text in example/analyses/2026-11-19_home-bp-app-flag/conclusion.md:63; keep one truth, git holds history`, exit 1 |
| A level 2 heading "Revision 2" added to `reanalysis.md` | `ERROR: revision section in example/analyses/2026-11-19_home-bp-app-flag/reanalysis.md:144; keep one truth, git holds history`, exit 1 |
| § 10 interval in `reanalysis.md` changed from 77.1 to 76.1 | `check.py: OK`, exit 0; `analysis.py --check`: OK, exit 0 (not caught, note 3) |

### Output 4: the previous review's three fixes, verified against `5fc0b38`

| Fix requested | Verified how | Result |
|---|---|---|
| 1. Alarm check on every raw reading before the `cuff loose` exclusion; plan text, denominator and count aligned | Plants in the excluded row and in a duplicate (output 3). Read `analysis.py` `run()`: `alarm_check(raw)` is the first call after `load()`. Read `plan.md` § 3 and `reanalysis.md` § 2 and § 5 | Closed. Exit 1, the STOP message, `results.csv` unchanged. `plan.md` § 3 step 2 now places the check before deduplication and exclusion, as the script runs it. Denominator is "0 of 84 raw readings" in § 5; `grep -rn "of 81"` finds only the label match (81 of 81), which is correct |
| 2. The 24 reading variant in `analysis.py` and `results.csv` | `readings_unit_interval()` read; own recomputation (output 2); t quantile plant (output 3) | Closed. Rows 77.1, 79.6 and `rejected` match 77.131 to 79.619. § 10 points to `alt_readings_unit_*`. The header claim of `reanalysis.md` now holds for § 10 |
| 3. § 9 by commit, with the missing items, the count changes and the hash `d62d117` | Each `+` and `-` line of the three diffs in check 5 looked up in § 9; `git show b68dc6e:<plan.md>` for what the first commit already held | Closed. Asserted counts (2 and 1), the uniqueness check and the day 1 reason stand under "Before `b68dc6e`", which matches the revision table in that commit; the day 1 rewording, the scope note and the count change from 2 stand under `d1bc466`; `d62d117` is named by hash with 89 to 91; the newest commit has 91 to 95. The newest commit is named by its subject, "Final review round 2 fixes", which is the subject of `5fc0b38` in `git log`; a commit cannot hold its own hash, so this is accepted |

Comparison count, three places: `results.csv` `comparisons_against_a_reference,95`;
`reanalysis.md` § 9 "95 (84 raw readings ...; the readings unit alternative against
AHA/ACC diastolic)" and "the count went from 91 to 95"; `plan.md` § 3 lists the same four
groups without a number (every raw reading, two guidelines for primary and sensitivity,
the ESC elevated band, the readings unit alternative). `analysis.py`:
`len(raw) + 2 * 2 * 2 + 2 + 1`. Own count: 84 + 8 + 2 + 1 = 95. Consistent.

Agreement between files: mean 125.5/78.4, ESC below or rejected, AHA/ACC inconclusive
or "unresolved", label rule per reading 81 of 81 and status ESCALATED (T7) are the same
in `results.csv`, `conclusion.md`, `reanalysis.md`, `example/README.md`,
`example/results.md` and `example/status/follow-up.md`. Search of the repository's
Markdown files for struck text and for headings starting with Revision or Round, this
file excluded: 0 hits.

## Findings, ranked by consequence
1. **Wrong meaning or wrong number:**
   - None. Primary endpoint, both guideline decisions, the readings unit alternative and
     every row of `results.csv` reproduce from the raw CSV with independent code. The
     alarm rule now covers all 84 raw rows.
2. **Reproducibility:**
   - None. The three fixes requested by the previous review are closed (output 4).
3. **Form** (notes, none required for green):
   - **Note 1.** The row `alt_readings_unit_decision_aha_dia` tests the diastolic interval
     only, and the count adds one comparison for it. § 10 says "AHA/ACC becomes
     *rejected*", which by the plan's rule also needs the systolic interval below 130.
     It is (123.6 to 127.5, output 2), but that interval is not computed by the script.
     The statement is true; its systolic half has no row.
   - **Note 2.** The range validation in `load()` runs before the alarm check. A systolic
     above 250 or a diastolic above 150 therefore stops the script with "suspect a column
     shift" instead of the T1 message (output 3). The script still stops, names the value
     and the row, and writes nothing.
   - **Note 3.** No tool compares a number in a document with `results.csv` (output 3,
     last row). This concerns `tools/check.py`, not the example, and was not required
     last time either.
   - **Note 4.** § 9 places the scope note under `d1bc466`. That commit added the row to
     `plan.md` § 0, but the sentence was already in the revision table of `b68dc6e`. The
     change is listed and is after the first result either way; only the commit is
     arguable.

## Verdict
✅ green for everything that could be checked. No number and no part of the answer
changed since the previous review. All three requested fixes are closed, and no new
fix is required; notes 1 to 4 are optional.

Could not be checked in this review: every threshold against its source (check 4).
The next review with web access must open each source in `reanalysis.md` § 8. Until
then the thresholds rest on the executor's reading and on agreement between the files.
