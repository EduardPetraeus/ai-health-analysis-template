# Review · 2026-11-19_home-bp-app-flag

*Written by a session that did not plan or execute the analysis ([ROLES.md § 4](../../../ROLES.md#4-review)).
A verdict is a command and its output, not an opinion. Synthetic data.*

**Reviewer:** separate AI session, model `claude-fable-5-2` (whether the executor ran on a
different model is not known to the reviewer) · **Date:** 2026-11-19 · **Round:** 1

All commands were run from the repository root. Reviewer code lives outside the
repository in `/tmp/review-scratch/` (`recompute.py`, `planted.py`); it reads the raw CSV
directly and does not import `analysis.py`. This review changed no file other than this
one.

## Expectation before reading the results

Written after reading `brief.md` and `plan.md` only, before opening `reanalysis.md`,
`conclusion.md` or `results.csv`, and before computing anything:

> Primary endpoint below 135/85 but not normal: roughly 126 to 132 systolic and 78 to 83
> diastolic, inside the ESC home *elevated* band. Upper 95 % limits probably below
> 135/85, diastolic the closer call. Ad hoc readings clearly higher than protocol
> readings. App label equal to office cut points per reading. No reading above 180/120.

Outcome: the direction and the band were right. The systolic mean (125.5) came out just
under the expected range; diastolic (78.4) inside it. Nothing in the result surprised the
reviewer enough to suggest a hidden error.

## Checks

| # | Check | Command | Output | Verdict |
|---|---|---|---|---|
| 1a | Raw file matches its generator | `python3 example/data-folder/home-bp-app/generate.py --check` | `generate.py --check: OK, committed file matches the generator` (exit 0). `sha256sum` of the raw file starts `562a0b80`, as stated in `reanalysis.md` § 1 | ✅ |
| 1b | Script reruns and reproduces `results.csv` | `python3 example/analyses/2026-11-19_home-bp-app-flag/analysis.py --check` | `analysis.py --check: OK, results reproduce exactly` (exit 0) | ✅ |
| 1c | Independent recomputation of every number in `reanalysis.md` § 5 | `python3 /tmp/review-scratch/recompute.py example/data-folder/home-bp-app/raw/export-2026-11-18.csv` (own code, t quantile from scipy: 2.5706 for 5 df) | 84 raw rows, 2 duplicates (2026-09-15 16:20, 2026-10-06 11:49), 1 `cuff loose` (2026-10-17, 98/61), 81 analysed. Primary, 24 readings over 6 days 2026-11-09 to 2026-11-14: systolic 125.5417 (122.5947 to 128.4886), diastolic 78.3750 (76.0713 to 80.6787). All 7 days: 126.0000/78.3214. Ad hoc 40/53 (75.5 %). No note 128.69/77.46 (n = 26). With note 134.07/81.59 (n = 27). Max 145/70 on 2026-09-10. Readings above 180/120: 0. Every value rounds to the figure in § 5 | ✅ |
| 2 | Every field used is documented in `semantics/` | Read `example/semantics/sources/home-bp-app/reading.md`; recomputed the label rule on all analysed rows | All seven columns documented. Claim `81/81` reproduced: own office rule equals `Category` on 81/81 analysed rows. Alternative rules are rejected by the data: strict `>` instead of `≥` matches 76/84 raw rows, a systolic only rule 67/84. Gap: no reading has systolic 140 or diastolic ≥90, so the Stage 2 boundary is not identified (finding 3) | ✅ with finding 3 |
| 3 | Every number meets METHOD § 2 | Read `reanalysis.md` § 1 to 5 and `conclusion.md` against the five requirements | `reanalysis.md`: source, denominators, dates, exclusions and run date present. `conclusion.md`: no real dates for the protocol week or the everyday readings; "for a week" hides that the primary is 24 readings over 6 days; n missing for the two note groups (finding 4) | ❌ for `conclusion.md` |
| 4 | Thresholds match their cited sources (source opened, not just titled) | WebFetch of each link on 2026-11-19 | **PMC9904446 opened:** Box 16 gives the home threshold for hypertension as at least 135/85 mmHg; Box 15 gives 7 days (not fewer than 3), duplicate morning and evening readings, 5 min rest, 1 min apart, and calls discarding day 1 a matter of debate; Box 8 gives validated upper arm cuffs only. Matches. **revespcardiol.org opened:** Table 1, column "Daytime ABPM / HBPM": non elevated <120/70, elevated 120/70 to <135/85, hypertension ≥135/85. Matches. **heart.org opened:** "higher than 180/120 mm Hg", wait at least 1 minute and measure again, symptoms listed. Matches. **Day 1 study:** DOI page could not be fetched; verified instead from the PubMed record (PMID 35762478, [doi](https://doi.org/10.1097/HJH.0000000000003157)): 2,122 participants, Finland, Greece and UK, day 1 about 2.8/1.4 mmHg higher, plateau after day 3. Matches. **ACC press release: could not be fetched (client error).** The AHA/ACC office cut points and "unchanged from 2017" are therefore not verified by this review. **ESC 2024 full text:** not opened by the executor (stated) and not by the reviewer | ✅ for the three thresholds the conclusion rests on; ACC not verified |
| 5 | Hypothesis in `reanalysis.md` § 9 matches the approved plan verbatim | String match of `"I think the app is right. My blood pressure is in the hypertension range."` in `brief.md`, `plan.md`, `reanalysis.md` | `plan: True reanalysis: True brief: True` | ✅ |
| 6 | Negative statements have positive controls | Own check on the raw file, then the same check with a planted 185/125 row | "No reading above 180/120": real data `False`, with planted row `True`, so the check can fire. Maxima over all 84 raw rows: systolic 145, diastolic 89. The escalation lines "T2 not fired" and "T4, T5 and T6 not fired" have no data behind them (finding 2). `results.csv` reports the highest systolic reading only (finding 7) | ❌ for T2 and T6 |
| 7 | A planted error is caught by the analysis checks | Copied the raw CSV to `/tmp/review-scratch/planted.csv`, appended one row `2026-11-14,21:30,127,79,66,Elevated,protocol`, ran `validate_extract(rows, 84, key_field="row", ranges=...)` via `planted.py` | Untouched file: `PASS 84`. Planted: `CAUGHT: expected 84 rows, got 85. Change the constant deliberately, or find the missing row`. Second plant (84 rows, one systolic set to 12): `CAUGHT: SYS (mmHg)=12 outside [70, 250] in row 11: suspect a column shift` | ✅ |
| 8 | No data files and no living file dependencies | `ls` of the analysis folder; `grep -niE "status/\|health-status\|follow-up" *.md *.py` with control pattern `reanalysis` (1 hit, the search works) | Folder holds only `.md` and `.py`; output is in `example/data-folder/`. Two hits: `brief.md:18` names `status/health-status.md` as the place for baseline facts, `plan.md:79` is a write boundary. No value is taken from either. `analysis.py` opens only the raw CSV and `results.csv` | ✅ with finding 8 |
| 9 | `conclusion.md` within one page and section 5 filled in | Word count in Python, table rows removed | 406 words including headings and the header lines, 360 without headings. Tables have two columns. Section 5 has four concrete points | ✅ |
| 10 | Every number in `conclusion.md` equals `results.csv` and the recomputation | Read line by line | 125.5/78.4 ✅ · 135/85 ✅ · 40 of 53 (75 %) ✅ (75.47 %) · 134.1/81.6 ✅ · "about 5/4 higher" ✅ (5.4/4.1) · 145/70 ✅ · 122.6 to 128.5 and 76.1 to 80.7 ✅ · 126.0/78.3 ✅ · flag row equals `status/follow-up.md` (125.5/78.4, MONITOR, 2027-02-19) ✅ | ✅ |
| 11 | Repository check | `python3 tools/check.py` before this file existed | `2 problem(s)`: both are broken links to this `review.md` (from `example/README.md:32` and `conclusion.md:4`). Rerun after this file was written: both link errors are gone. One new error remains, `config.py not named in tools/README.md`, about a file added to `tools/` by another session while this review ran; it is outside this analysis and outside what the reviewer may edit | ✅ for this analysis; ❌ repository wide until `tools/README.md` lists `config.py` |

## Findings, ranked by consequence

No number is wrong. The answer ("below the home hypertension threshold of 135/85, in the
ESC elevated band") is reproduced and its three thresholds were confirmed at the source.
The findings below are about meaning and method, and none of them changes a number.

1. **Wrong meaning or wrong number:**

   1. **`conclusion.md` § 3 generalises beyond what was verified.** "Home thresholds are
      lower than office ones" is confirmed for ESH 2021 and ESC 2024 (135/85 against
      140/90). The app's labels come from the AHA/ACC system, whose home values the
      knowledge file and § 5 of the same conclusion declare not verified. The sentence
      also invites a wrong reading: against the app's own Stage 1 cut point of 130/80,
      the threshold applied here (135/85) is higher, not lower. The label fails because
      it is put on single readings and because a different guideline's home threshold is
      applied, and the text should say exactly that.
   2. **Escalation triggers are written as "not fired" where METHOD § 9 requires "could
      not be checked".** T2: `plan.md` § 3 itself says the guideline handling of elevated
      blood pressure depends on overall cardiovascular risk, "which this analysis cannot
      estimate"; the conclusion then reports "T2 not fired as a referral". T6: nothing in
      `brief.md`, `plan.md` or `reanalysis.md` records that the owner was asked about
      symptoms, yet the conclusion reports "T6 not fired". T5 is asserted with no
      reasoning although the risk estimate named in § 5 may need a clinician. A trigger
      without data behind it may not be reported as not triggered.
   3. **The decoded label rule is only partly identified.** `81/81` is true and
      reproduced, and the Stage 1 boundary is well tested (5 readings with systolic 130,
      9 with diastolic 80; a strict `>` rule fails on 8 of 84 raw rows). No reading has
      systolic 140 or diastolic ≥90, so the data cannot tell "≥140" from ">140" and never
      exercise the diastolic Stage 2 arm. `reading.md` § 4 states the full rule as
      decoded. Consequence here is nil (the "Stage 1 or 2" share does not depend on that
      boundary), but the next analysis that reuses the rule would inherit an untested
      half. The cut points themselves could not be checked against the ACC page in this
      review (check 4).
   4. **`conclusion.md` does not meet METHOD § 2 on its own.** "Measured properly for a
      week" is 24 readings over 6 days, 2026-11-09 to 2026-11-14, with day 1 left out by
      plan. The 53 everyday readings cover 2026-09-02 to 2026-11-07. The note groups have
      n = 27 and n = 26. None of this is in the page the owner reads, and the three
      removed rows are not mentioned.
   5. **"App sync" as the cause of the two duplicates is an assumption written as a
      fact** (`plan.md` § 2, `reading.md` § 6). The plan's owner questions cover the
      protocol and the loose cuff, not the duplicates, and there is no provider
      documentation. Treating identical rows as one reading is defensible. Impact
      checked: with both rows kept, ad hoc becomes 42/55 (76.4 %), with note 133.9/81.8
      (n = 28), no note 128.4/77.6 (n = 27). The primary endpoint is untouched (both
      duplicates are ad hoc readings).

2. **Reproducibility:**

   6. None blocking. `--check` reproduces byte for byte, the independent recomputation
      agrees on every value, and `reanalysis.md` alone was enough to rebuild the numbers.
      One weakness in the validation: `validate_extract` is called with
      `key_field="row"`, a line number the script itself assigns, so its duplicate key
      check can never fire. The duplicates are found by `deduplicate()`, not by
      validation. `example/README.md` says they "were caught by validation", which is not
      what the code does.

3. **Form:**

   7. `highest_single_reading` is chosen by systolic first, so the highest diastolic
      reading (133/89 on 2026-10-02) appears nowhere. The statement "none above 180/120"
      is correct, but its diastolic half rests on a number that is not reported.
   8. `brief.md` § 3 points to `status/health-status.md`; `example/status/` contains only
      `follow-up.md`. No value is taken from it, so it is a dangling pointer, not a
      forbidden dependency. The brief is frozen; note it in the example README instead of
      editing the brief.
   9. Source notes for the knowledge file, no change required: the SEC table's home
      column is shared with daytime ambulatory values; the SEC page carries a correction
      to its central figure (office hypertension systolic ≥140, not ≥120) that does not
      touch Table 1; the ESH paper also states there was no evidence of improvement from
      discarding day 1, which supports reporting both versions as the plan does.

## Verdict

❌ **Fixes needed.** The numbers and the answer are reproduced and stand. Five fixes,
none of which may change any value in `results.csv` other than the one added row in
fix 5:

| # | Fix | Expected result after the fix |
|---|---|---|
| 1 | `conclusion.md` § 3: replace "home thresholds are lower than office ones" with a statement limited to the verified guidelines (European home hypertension threshold 135/85 against office 140/90), and say that the app's label comes from a different guideline's office categories | No sentence in `conclusion.md` makes a claim about AHA/ACC home thresholds; § 3 and § 5 no longer disagree |
| 2 | `conclusion.md` § 7: write T2 as "could not be checked: overall cardiovascular risk not estimated", and T6 as "could not be checked" unless the owner is asked about symptoms and the answer and date are recorded; give one line of reasoning for T5. This touches escalation, so the owner sees it ([ROLES.md § 3](../../../ROLES.md#3-what-only-the-owner-approves)) | Each of T1 to T7 reads fired, not fired with its evidence, or could not be checked with the reason; none is "not fired" without data |
| 3 | `conclusion.md` § 2 or § 3: add the protocol dates and counts (24 readings over 6 days, 2026-11-09 to 2026-11-14, day 1 left out), the date range of the 53 everyday readings (2026-09-02 to 2026-11-07) and n for the two note groups | Every number in the conclusion carries denominator and real dates; word count stays at about 400 without tables; all values still equal `results.csv` |
| 4 | `example/semantics/sources/home-bp-app/reading.md` § 4 and § 6: state that the Stage 2 boundary (systolic exactly 140, diastolic ≥90) is not exercised by this delivery, and mark "app sync" as an assumption not confirmed by the provider or the owner | `category` stays `partial` with the untested part named; `81/81` unchanged |
| 5 | `analysis.py`: add the highest diastolic reading as a result row; correct the sentence in `example/README.md` so that duplicates are "removed by `deduplicate()`", not "caught by validation"; update `reanalysis.md` § 5 with the new row | `results.csv` gains one row (`133/89 on 2026-10-02`), all 27 existing rows unchanged; `analysis.py --check` prints `OK` after regeneration; `python3 tools/check.py` reports 0 problems |

Round 2 reruns checks 1b, 3, 6, 10 and 11 after the fixes.

---

## Round 2

**Reviewer:** separate AI session, model `claude-fable-5-2`, not the round 1 reviewer
session and not the executor · **Date:** 2026-11-19 · **Round:** 2

All commands were run from the repository root. Reviewer code lives outside the
repository in `/tmp/review2/` (`recompute.py`, `wc.py`, `keyctl.py`); it reads the raw CSV
directly and does not import `analysis.py`. No web access was used in this round, by
instruction, so no source was reopened. This round changed no file other than this one,
and only by appending this section.

The repository has no commit yet, so there is no history to diff against. The versions
that round 1 reviewed were recovered from unreachable blobs in the git object store
(`git fsck --unreachable --no-reflogs`): `results.csv` `647abcba`, `plan.md` `b8e8814b`,
`conclusion.md` `bdc410ca`, `reanalysis.md` `ac9cac0d`, `analysis.py` `1ceafa98`,
`follow-up.md` `f391bab5`, `example/README.md` `77d9da6f`. Their content matches what
round 1 quotes.

### Checks

| # | Check | Command | Output | Verdict |
|---|---|---|---|---|
| 1a | Raw file matches its generator | `python3 example/data-folder/home-bp-app/generate.py --check` | `generate.py --check: OK, committed file matches the generator` (exit 0). `sha256sum` of the raw file: `562a0b80f136…`, unchanged | ✅ |
| 1b | Script reruns and reproduces `results.csv` | `python3 example/analyses/2026-11-19_home-bp-app-flag/analysis.py --check` | `analysis.py --check: OK, results reproduce exactly` (exit 0) | ✅ |
| 1c | Independent recomputation | `python3 /tmp/review2/recompute.py example/data-folder/home-bp-app/raw/export-2026-11-18.csv` (own code, t quantile from scipy) | 84 raw rows, 2 duplicates (2026-09-15 16:20, 2026-10-06 11:49), date and time unique after their removal, 1 `cuff loose` (2026-10-17, 98/61), 81 analysed, label match 81/81. Primary, 24 readings over 6 days 2026-11-09 to 2026-11-14: systolic 125.5417 (122.5947 to 128.4886), diastolic 78.3750 (76.0713 to 80.6787). All 7 days, 28 readings: 126.0000/78.3214. Ad hoc 40/53 (75.47 %), dates 2026-09-02 to 2026-11-07. No note 128.69/77.46 (n = 26). With note 134.07/81.59 (n = 27). Highest systolic 145/70 on 2026-09-10 (no tie), highest diastolic 133/89 on 2026-10-02 (no tie). All 28 rows of `results.csv` equal these values after rounding | ✅ |
| 3 | Every number meets METHOD § 2 | Read `conclusion.md` against the five requirements | Primary: 24 readings over 6 days, 2026-11-09 to 2026-11-14, day 1 left out. Everyday readings: 40 of 53, 2026-09-02 to 2026-11-07. Note groups: n = 27 and n = 26. Three removed rows named in § 4. Run date in the header. The source file and field are reached through the link to `reanalysis.md` § 1, not written in the page | ✅ |
| 6 | Negative statements have positive controls | Same script: crisis test on the data, then with a planted 185/125 row and a planted 150/121 row (diastolic arm only) | Analysed rows `False`, all 84 raw rows `False`, planted 185/125 `True`, planted 150/121 `True`. Raw maxima: systolic 145, diastolic 89. T1 line in `conclusion.md` now names both maxima. T2 and T3 read could not be checked with a reason. T6 has an answer behind it, but see finding 1. T4 reads "not applicable" (finding 2) | ✅ for T1, T2, T3, T5, T7; ❌ for T4 and for the dating of T6 |
| 6b | The new duplicate key check can fire (round 1 finding 6) | `python3 /tmp/review2/keyctl.py example/data-folder/home-bp-app/raw/export-2026-11-18.csv tools` (calls `validate_extract` with the date and time key, then with one key copied onto another row) | `untouched: PASS 82`; `planted: CAUGHT: duplicate key: ['2026-09-07 20:54']` | ✅ |
| 9 | `conclusion.md` length and form | `python3 /tmp/review2/wc.py …/conclusion.md` (table rows removed) | 420 words with headings and header lines (round 1 counting: 406 before the fixes), 374 without headings, 353 without headings and the three header lines. Tables have two columns. Section 5 has four points | ✅ about 400 |
| 10 | Every number in `conclusion.md`, `reanalysis.md` § 5, `example/README.md` and `example/status/follow-up.md` equals `results.csv` | Read line by line against `results.csv` and check 1c | `conclusion.md`: 125.5/78.4 ✅ · 24 readings over 6 days ✅ · 2026-11-09 to 2026-11-14 ✅ · 135/85 and 140/90 ✅ (knowledge file) · 40 of 53 ✅ · 2026-09-02 to 2026-11-07 ✅ · 134.1/81.6 (n = 27) ✅ · 128.7/77.5 (n = 26) ✅ · three rows set aside (2 + 1) ✅ · 145/70 and 133/89 ✅ · 180/120 ✅ · 122.6 to 128.5 and 76.1 to 80.7 ✅ · 126.0/78.3 ✅ · 120/70 to <135/85 ✅. `reanalysis.md` § 5: all 12 rows ✅, including the new `133/89 on 2026-10-02`; § 3 "42/55 with duplicates kept" equals round 1 finding 5 ✅. `example/README.md`: 81 of 81 ✅ · 135/85 vs 140/90 ✅ · 125.5/78.4 ✅ · 40 of 53 ✅ · two duplicates and one `cuff loose` ✅. `follow-up.md`: 125.5/78.4 ✅ · ESCALATED (T7, routine) equals `conclusion.md` § 6 ✅ · review date 2027-02-19 equals § 7 ✅ | ✅ |
| 11 | Repository check | `python3 tools/check.py` | `check.py: OK (73 files checked, 4 warning(s))` (exit 0). The four warnings concern the unconfirmed root `status/` files and a missing `private_terms` entry, not this analysis | ✅ |
| 12 | `results.csv` changed only by the added row | `git cat-file -p 647abcba > /tmp/review2/results_old.csv; diff /tmp/review2/results_old.csv example/data-folder/analyses/2026-11-19_home-bp-app-flag/results.csv` | `25a26` / `> highest_diastolic_reading,133/89 on 2026-10-02`. Nothing else. 27 metric rows before, 28 now | ✅ |
| 13 | Decision rule in `plan.md` § 0 | Applied to the recomputed interval | Upper ends 128.4886 < 135 and 80.6787 < 85: first branch, hypothesis rejected for this week. Equals `primary_below_home_hypertension_135_85 = True` and the answer in `conclusion.md` § 2. The rejection branch has the same content as step 7 of the plan round 1 reviewed; the other two branches were added after the result (finding 1) | ✅ for the decision; ❌ for how the rule is dated |
| 14 | No diagnosis claim (DISCLAIMER item 1) | `grep -rniE "not hypertension\|you (do not \|don't )?have hypertension\|is hypertensive\|diagnos" example --include=*.md`, with control pattern `clinician's call` (2 hits, the search works) | Hits outside this file: `conclusion.md:15` "Whether you have hypertension is a clinician's call, not this analysis's", `plan.md:17` (scope note saying the same), three lines of general guideline text in the knowledge file. The earlier "Not hypertension" in `example/README.md` and "Elevated is not hypertension" in `conclusion.md` are gone. `conclusion.md` compares an average with a threshold and stops there | ✅ |
| 15 | Hypothesis still verbatim | `grep -c` of the sentence in `brief.md`, `plan.md`, `reanalysis.md` | 1, 1, 1 | ✅ |
| 16 | What changed in `plan.md` after round 1 | `git cat-file -p b8e8814b \| diff - …/plan.md` | 9 hunks. Added after the result: the decision rule row with its "supported" and "inconclusive" branches; the scope note; "highest systolic and diastolic readings" as a secondary endpoint; the owner answers "Do you know why two rows are identical? No." and "Any new symptoms since your last check up? No." under the heading "answered before the ok (2026-11-19)"; the trigger list under the heading "set before the result", including the rule that fires T7; "as recommended for short schedules in the 2022 schedule study". `grep -niE "revis\|round 1\|after review" plan.md` finds nothing | ❌ finding 1 |

### The five fixes from round 1

| # | Expected result | Evidence | Met? |
|---|---|---|---|
| 1 | No sentence in `conclusion.md` makes a claim about AHA/ACC home thresholds; § 3 and § 5 no longer disagree | § 3 now reads "US **office** categories … European guidelines use 135/85 at home, 140/90 in the office". § 5 keeps "What your average means under US home categories; not verified". No other sentence touches US home values. Still open from round 1 check 4, and not checkable in this round: the US office cut points themselves were not confirmed at the ACC page by any reviewer | ✅ met |
| 2 | Each of T1 to T7 reads fired, not fired with its evidence, or could not be checked with the reason | T1 not fired with both maxima ✅. T2 could not be checked, reason given ✅. T3 could not be checked, reason given ✅. T5 not fired with one line of reasoning ✅. T7 fired with reason ✅. T4 reads "not applicable", a fourth state that METHOD § 9 does not have ❌. T6 reads not fired with the owner's answer, but the answer is recorded in the plan as given before the ok, which the recovered plan and round 1 contradict ❌ (finding 1) | ❌ partly |
| 3 | Every number in the conclusion carries denominator and real dates; about 400 words; values equal `results.csv` | Checks 3, 9 and 10 | ✅ met |
| 4 | `category` stays `partial` with the untested part named; `81/81` unchanged | `reading.md` § 3: `partial`. § 4 has "Untested part (review round 1)" naming systolic exactly 140 and diastolic 90 or more. § 6: "The cause is not documented; app sync is likely but unconfirmed". `81/81` unchanged and reproduced | ✅ met |
| 5 | `results.csv` gains one row, 27 existing rows unchanged; `--check` prints `OK`; `tools/check.py` reports 0 problems | Checks 12, 1b and 11. `reanalysis.md` § 5 has the new row. `example/README.md` now says the duplicates were "found when describing the file, preregistered in the plan, and asserted by the script": not the wording round 1 proposed, but true of the code (`assert len(duplicates) == EXPECTED_DUPLICATES`) and of the plan round 1 reviewed (its "Expected results" line already said 2 duplicates). `analysis.py` changed beyond the fix (two assertions and a second `validate_extract` on date and time); this answers round 1 finding 6 and changes no value (check 12, check 6b) | ✅ met |

**Is firing T7 consistent with METHOD § 9 and DISCLAIMER.md?** Yes. METHOD § 9 defines T7
as "the analysis cannot tell whether the finding is dangerous" and calls it the honest
counterweight: a risk that cannot be bounded is a reason to escalate. The average lies in
a range whose handling the European guideline ties to overall cardiovascular risk, the
analysis has no risk estimate, so T2 cannot be checked and the finding cannot be bounded.
T7 follows from T2 being uncheckable, and the earlier "T7 not fired: the finding is
bounded" was the weaker reading. The action matches the level in the table (book a
clinician). "Routine" is not in METHOD § 9, but it does not contradict it: T7 carries no
urgency level and T1, the only urgent trigger, is not fired with evidence. Flag status
`ESCALATED` matches METHOD § 10, and the flag is in both `conclusion.md` § 6 and
`status/follow-up.md`. Against DISCLAIMER.md: item 1 holds (check 14), item 2 holds (the
advice is to see a clinician for an assessment, with no treatment step), item 5 is
exactly what was done. What is not consistent is how the supporting record was written
into the plan (finding 1), not the escalation itself.

Not checkable by the reviewer: whether the repository's owner has seen this change of
escalation and of `status/follow-up.md`, which [ROLES.md § 3](../../../ROLES.md#3-what-only-the-owner-approves)
items 4 and 7 require.

### Findings, ranked by consequence

No number is wrong and no number changed apart from the one added row. The answer and
the escalation stand. The findings are about the trail.

1. **Wrong meaning or wrong number:**

   1. **`plan.md` was rewritten after the result and presents the additions as made
      before it.** The plan is the preregistration (METHOD § 3 and § 14). Check 16 shows
      what was added after round 1. Three of the additions carry a false time:
      - "Questions for the owner, answered before the ok (2026-11-19)" now contains the
        duplicates question and the symptoms question. Round 1 recorded that neither was
        in the plan ("nothing in `brief.md`, `plan.md` or `reanalysis.md` records that
        the owner was asked about symptoms"; "the plan's owner questions cover the
        protocol and the loose cuff, not the duplicates"). The T6 line in
        `conclusion.md` cites this entry as its evidence.
      - "Escalation triggers, set before the result" now contains a rule under which T7
        fires in the elevated range. It was written with the result known. The plan
        round 1 reviewed said "T4 to T7 assessed at closing".
      - The decision rule row gained a "supported" and an "inconclusive" branch after the
        result. The branch that decided the hypothesis is unchanged in content, so the
        decision itself is not affected.

      `reanalysis.md` § 9 still says "Nothing in the method was changed after the plan
      was approved", and the plan still ends "Approved by the owner before the script was
      written" with no revision note. METHOD § 5 allows smaller deviations only "if they
      are written down with the old wording, the new wording and the reason". The folder
      now contradicts itself: a reader who goes from `plan.md` to round 1 above finds the
      review describing a plan that no longer exists. Asking the owner about symptoms
      after round 1 was the right thing to do, and round 1 asked for it with "the answer
      and date recorded". The date recorded is the wrong one. In an example whose purpose
      is to show the method, this is the one thing it must not show.
   2. **T4 is reported as "not applicable"** in `conclusion.md` § 7 and `plan.md` § 3.
      METHOD § 9 has three states and § 12 says there is no `n/a`. The content is fine
      (one marker, so no combination exists to assess); the state must be one of the
      three.
   3. **A new source claim in `plan.md` § 3 step 5 is not verified.** "The primary
      discards it, as recommended for short schedules in the 2022 schedule study"
      replaced "the older convention of discarding it". Round 1 confirmed from the
      abstract only that day 1 runs about 2.8/1.4 mmHg higher and that values plateau
      after day 3. The knowledge file says of this study "abstract read; authors and full
      text not read" and attributes "it matters most for short schedules" to the ESH
      paper, not to the study. Whether the study recommends discarding day 1 could not be
      checked in this round (no web access). Until it is, the claim is a claim.

2. **Reproducibility:**

   4. None. `--check` reproduces byte for byte, the independent recomputation agrees on
      all 28 rows, and the new duplicate key validation fires on a planted duplicate.

3. **Form:**

   5. `example/README.md`, row "Review": "A separate session on another model reran
      everything". Round 1 states that whether the executor ran on a different model is
      not known to the reviewer, and both reviewer sessions report the same model id. The
      same row says the problems "were fixed before closing", which is true only once
      this round's fixes are in.
   6. `example/README.md`, row "Knowledge": "**home** thresholds are lower than office
      ones (135/85 vs 140/90 in Europe)". The parenthesis limits it, so it is not wrong,
      but it is the general sentence that fix 1 removed from the conclusion.
      `reading.md` says "differ", which is the safer wording.
   7. The decision rule and "hypothesis as tested" write "at or above 135/85" without
      saying whether one arm is enough. Guidelines define hypertension on either arm. As
      written, a week with only one lower end above its threshold falls into
      "inconclusive", which is the cautious outcome, and the case did not occur. Worth
      one clause when the plan is touched for finding 1.
   8. `plan.md` § 0 now gives the null hypothesis as "below 135/85"; `reanalysis.md` § 9
      keeps the earlier wording "with the upper end of its interval also below". Same
      meaning in effect, two wordings.

### Verdict

❌ **Fixes needed.** Fixes 1, 3, 4 and 5 from round 1 are met; fix 2 is met in substance
but not in its record. Every number, the answer, the T7 escalation and the flag stand.
Four fixes, none of which may change `results.csv` or any number:

| # | Fix | Expected result after the fix |
|---|---|---|
| 1 | `plan.md`: add a dated revision note at the top listing what was changed after review round 1, each with old wording, new wording and reason (METHOD § 5). Move the duplicates answer and the symptoms answer out from under "answered before the ok" into an entry dated as asked after round 1. Head the trigger list so that it says which lines were set before the result (T1, T2, T3 in substance) and which were written at closing or after round 1 (T4 to T7). Mark the two added decision rule branches the same way. `reanalysis.md` § 9: replace "Nothing in the method was changed after the plan was approved" with a sentence that names the post review additions and says the deciding branch was unchanged. `conclusion.md` § 7, T6: cite the answer with its real time | `grep -niE "revis\|round 1" plan.md` finds the note. No sentence in the folder says a post review addition was made before the ok or before the result. Round 1's quotes of the plan are explained by the note. `diff` of `results.csv` against `647abcba` still shows only the one added row |
| 2 | `conclusion.md` § 7 and `plan.md` § 3: write T4 as "not fired", with the reason (one marker analysed, so no combination exists to assess) | T1 to T7 each read fired, not fired with evidence, or could not be checked with a reason. `grep -n "not applicable"` in both files finds nothing |
| 3 | `plan.md` § 3 step 5: either open the 2022 study, confirm that it recommends discarding day 1 for short schedules and record what was read in the knowledge file, or return to a wording the verified sources carry (ESH 2021 calls it debated; the 2022 study found day 1 about 2.8/1.4 mmHg higher). The change goes into the revision note of fix 1 | The sentence states only what a named reader has read at the source, or the unverified part is marked as such |
| 4 | `example/README.md`, row "Review": drop "on another model" or replace it with what is known (a separate session; model of the executor not recorded). Optional in the same edit: row "Knowledge", "differ from" instead of "are lower than", and the either arm clause from finding 7 | No statement about the reviewing model that the review files do not support. `python3 tools/check.py` still prints `OK`. Word count of `conclusion.md` stays at about 400 without tables |

The escalation change (T7 fired, flag `ESCALATED`) and the edit to
`status/follow-up.md` go to the repository's owner for confirmation if that has not
happened ([ROLES.md § 3](../../../ROLES.md#3-what-only-the-owner-approves)).

Round 3 needs only checks 1b, 10, 11, 12 and 16, plus a reading of the revision note.

---

## Round 3

**Reviewer:** separate AI session, model `claude-fable-5-2`, not the executor and not a
reviewer session of round 1 or 2 · **Date:** 2026-11-19 · **Round:** 3

All commands were run from the repository root. Reviewer code lives outside the
repository in `/tmp/review3/` (`dates.py`, `wc.py`); it reads the raw CSV directly and
does not import `analysis.py`. No web access was used, by instruction, so no source was
reopened. This round changed no file other than this one, and only by appending this
section. The repository still has no commit; the approved plan and the round 1
`results.csv` were read from the git object store (`b8e8814b`, `647abcba`).

### Checks

| # | Check | Command | Output | Verdict |
|---|---|---|---|---|
| 1a | Raw file matches its generator | `python3 example/data-folder/home-bp-app/generate.py --check` | `generate.py --check: OK, committed file matches the generator` (exit 0) | ✅ |
| 1b | Script reruns and reproduces `results.csv` | `python3 example/analyses/2026-11-19_home-bp-app-flag/analysis.py --check` | `analysis.py --check: OK, results reproduce exactly` (exit 0) | ✅ |
| 10 | Every number in `conclusion.md` and `example/README.md` equals `results.csv` | Read line by line against `results.csv`; dates and counts that `results.csv` does not hold recomputed with `python3 /tmp/review3/dates.py example/data-folder/home-bp-app/raw/export-2026-11-18.csv` | `dates.py`: `raw 84`, `analysed 81`, `primary 24 6 2026-11-09 2026-11-14`, `adhoc 53 2026-09-02 2026-11-07`. `conclusion.md`: 125.5/78.4 ✅ · 24 readings over 6 days ✅ · 2026-11-09 to 2026-11-14 ✅ · 40 of 53 ✅ · 2026-09-02 to 2026-11-07 ✅ · 134.1/81.6 (n = 27) ✅ · 128.7/77.5 (n = 26) ✅ · three rows set aside (2 + 1) ✅ · 145/70 and 133/89 ✅ · none above 180/120 (`False`) ✅ · 122.6 to 128.5 and 76.1 to 80.7 ✅ · 126.0/78.3 ✅. `example/README.md`: 81 of 81 ✅ · 125.5/78.4 ✅ · 40 of 53 ✅ · two duplicates, one `cuff loose` ✅. Thresholds 135/85, 140/90, 120/70 and the date 2027-02-19 are not results; they equal the knowledge file and `status/follow-up.md` as in round 2, unchanged | ✅ |
| 11 | Repository check | `python3 tools/check.py` | `check.py: OK (73 files checked, 4 warning(s))` (exit 0). Same four warnings as round 2 (unconfirmed root `status/` files, no `private_terms`), none about this analysis | ✅ |
| 12 | `results.csv` changed only by the added row | `git cat-file -p 647abcba \| diff - example/data-folder/analyses/2026-11-19_home-bp-app-flag/results.csv` | `25a26` / `> highest_diastolic_reading,133/89 on 2026-10-02`. Nothing else | ✅ |
| 16 | `plan.md` body equals the approved version | `git cat-file -p b8e8814b > /tmp/r3_plan_old.md; head -n 92 …/plan.md \| cmp - /tmp/r3_plan_old.md`; `sha256sum` of the first 5412 bytes of `plan.md` and of the blob; `git cat-file -p b8e8814b \| diff - …/plan.md` | `cmp`: identical. Both hashes `43ad8ce22285…`. `diff`: one hunk, `92a93,111`, additions only (0 removed lines): a rule and the section "Revision 1 · 2026-11-19, after review round 1" | ✅ |
| 17 | Revision note exists and is found | `grep -niE "revis\|round 1" …/plan.md` | 9 hits, lines 96 to 110: the heading, the intro line and the table rows | ✅ |
| 18 | No "not applicable" trigger state | `grep -n "not applicable" …/plan.md …/conclusion.md` | No hit (exit 1). With line breaks ignored there is one match in `plan.md` lines 69 to 70: T3, "not applicable to one protocol week; reported as not checkable". That is approved text, about T3, and it resolves to one of the three states. T4 reads "not fired" with its reason in `conclusion.md:51` and `plan.md:106` | ✅ |
| 19 | No sentence dates a post review addition before the ok or before the result | `grep -rnEi "before the ok\|before the result\|preregist\|before any data\|set before\|answered before\|before the script\|after the result\|approved" example --include=*.md --include=*.py`, this file left out; control `grep -c "Approved by the owner before the script was written" …/plan.md` gives 1, so the search works | 14 hits, each read. `plan.md:104` "Two questions asked before the ok": true of the blob (protocol, loose cuff). `plan.md:106` "T1 to T3 set before the result": true of the blob. `plan.md:92` and `:3`: approval of the body, which is the approved text. `plan.md:64`, `reanalysis.md:20` to `21`, `example/README.md:25`, `analysis.py:31`: "preregistered" 2 duplicates and 1 exclusion, which the blob's "Expected results" line holds. `brief.md:4`: fields 7 and 8, untouched. `reanalysis.md:99` to `103` and `conclusion.md:53` date the additions after the result. No hit puts a post review addition before the ok or the result | ✅ |
| 20 | Reasons in the revision table match what round 1 says | `sed -n 1,134p …/review.md \| grep -niE "inconclusive\|convention\|branch\|outcome\|decision"` | One hit, line 24, "Outcome:" of the reviewer's expectation. Round 1 says nothing about a missing inconclusive outcome and nothing about "older convention" (finding 1) | ❌ |
| 9 | `conclusion.md` length | `python3 /tmp/review3/wc.py …/conclusion.md` (table rows removed) | 425 words with headings and header lines (round 2: 420), 379 without headings | ✅ about 400 |

### The four fixes from round 2

| # | Expected result | Evidence | Met? |
|---|---|---|---|
| 1 | `grep` finds the revision note. No sentence in the folder says a post review addition was made before the ok or before the result. Round 1's quotes of the plan are explained. `results.csv` differs from `647abcba` only by the one added row | Checks 16, 17, 19 and 12. The executor restored the body byte for byte and put the note at the end instead of at the top, which is stronger than what round 2 asked: round 1's quotes are now literally true of the file. The two later owner answers stand under "asked after the result". The triggers row separates T1 to T3 from T4 to T7 and states that writing T4 to T7 at closing went against METHOD § 9. The two added decision outcomes are marked as added, with the deciding branch unchanged. `reanalysis.md` § 9 names the additions and says the deciding rule and earlier numbers are unchanged. `conclusion.md` T6 reads "owner, asked during review, `plan.md` Revision 1" | ✅ met; three cells of the note need correcting (finding 1) |
| 2 | T1 to T7 each read fired, not fired with evidence, or could not be checked with a reason; `grep -n "not applicable"` finds nothing | Check 18. `conclusion.md` § 7: T1 not fired with both maxima, T2 and T3 could not be checked with reasons, T4 not fired with reason, T5 not fired with reason, T6 not fired with the owner's answer and its real time, T7 fired with reason | ✅ met |
| 3 | The day 1 sentence states only what a named reader has read at the source | The unverified sentence is gone with the restored body. Step 5 is back to the approved "older convention" wording, and Revision 1 replaces it with: a free choice, ESH 2021 calls it debated, the 2022 study found day 1 about 2.8/1.4 mmHg higher, both versions reported. Round 1 check 4 confirmed both statements at the source | ✅ met |
| 4 | No statement about the reviewing model that the review files do not support; `check.py` prints `OK`; conclusion about 400 words | `example/README.md:28` now reads "Separate review sessions reran everything", with no model claim. Row "Knowledge" reads "differ from". Checks 11 and 9. The optional either arm clause was not added; Revision 1 writes "lower ends", plural, which reads as both arms | ✅ met |

Not checkable by the reviewer, carried over from round 2: whether the repository's owner
has seen Revision 1, the fired T7 and the edit to `status/follow-up.md`
([ROLES.md § 3](../../../ROLES.md#3-what-only-the-owner-approves) items 4, 6 and 7).
Revision 1 does not record it either way.

### Findings, ranked by consequence

No number is wrong, none changed, and the false times that round 2 found are gone. One
finding is about what the revision note says of this review file; the rest is form.

1. **Wrong meaning or wrong number:**

   1. **Three cells of Revision 1 do not match their stated origin** (check 20). The note
      exists to make the trail true, so its own provenance has to hold.
      - Row "Decision outcomes", reason: "Round 1 noted no inconclusive outcome". Round 1
        does not mention outcomes, branches or the decision rule.
      - Row "Day 1", reason: "Round 1 could not support 'older convention'". Round 1 does
        not mention that wording. Its note 9 says the ESH paper found no evidence of
        improvement from discarding day 1, which is the nearest thing and is not the same
        statement.
      - Row "Secondary endpoint", before: "Highest single reading by systolic". The
        approved § 0 lists four secondary endpoints and this is not one of them. It was a
        row in the script and in `results.csv`, not wording of the plan.

      None of the three puts an addition before the ok or the result, and none touches a
      number. If the two reasons came from somewhere other than round 1 (the "Scope" row
      names a "repository review"), the cells should name that origin.

2. **Reproducibility:**

   2. None. `--check` reproduces byte for byte and the body of the plan equals the
      approved blob.

3. **Form:**

   3. Revision 1 is headed "after review round 1" and introduced as added "during review
      round 1". The "Day 1" row and the "not fired" wording of T4 answer round 2. The
      same applies to "Revised 2026-11-19 after review round 1" in the header of
      `conclusion.md`. All on the same date, so nothing is misdated by day.
   4. The approved § 4 says the review is done by "a separate session on a different
      model". All three reviewer sessions report the same model id and the executor's
      model is not recorded. ROLES § 4 says "ideally", so nothing is broken, but the plan
      promised more than the record shows and Revision 1 is the place to say so.
   5. The header of `plan.md` and the row for `plan.md` in the folder's `README.md` say
      "approved" without pointing to the revision at the end. The body cannot carry a
      pointer without ceasing to equal the blob; the folder `README.md` can.

### Verdict

❌ **Fixes needed**, one, wording only. All four round 2 fixes are met, every number, the
answer, the T7 escalation and the flag stand, and no sentence in the folder dates a post
review addition before the ok or the result.

| # | Fix | Expected result after the fix |
|---|---|---|
| 1 | `plan.md`, Revision 1 only, body untouched: give the rows "Decision outcomes" and "Day 1" a reason that names where the change really came from, or no attribution; write the "before" cell of "Secondary endpoint" as what it was (a row in the script and `results.csv`, not a secondary endpoint of the approved plan). Optional in the same edit: head the revision "after review rounds 1 and 2", add one line that the reviewing model was the same in all rounds and the executor's model is not recorded, and point to the revision from the folder `README.md` | Every "Round 1" or "Round 2" reference in Revision 1 can be found in this file by `grep`. `head -n 92 plan.md \| cmp - <blob b8e8814b>` still reports identical. `diff` of `results.csv` against `647abcba` still shows only the one added row. `python3 tools/check.py` still prints `OK` |

Round 4 needs only checks 16 and 11 and a reading of the three cells.

---

## Round 4

**Reviewer:** separate AI session, model `claude-fable-5-2`, not the executor and not a
reviewer session of rounds 1 to 3 · **Date:** 2026-11-19 · **Round:** 4

All commands were run from the repository root. The only reviewer file outside the
repository is `/tmp/review4/plan_old.md`, the approved plan written out from the git
object store. No web access was used, by instruction. This round changed no file other
than this one, and only by appending this section. Scope as set by round 3: checks 16 and
11, the two `--check` scripts of `.github/workflows/check.yml`, and a reading of the
edited cells of Revision 1.

### Checks

| # | Check | Command | Output | Verdict |
|---|---|---|---|---|
| 16 | `plan.md` body equals the approved version | `git cat-file -p b8e8814b > /tmp/review4/plan_old.md; head -n 92 …/plan.md \| cmp - /tmp/review4/plan_old.md`; `head -c 5412 …/plan.md \| sha256sum` and `sha256sum /tmp/review4/plan_old.md`; `git cat-file -p b8e8814b \| diff - …/plan.md` | Blob is 92 lines, 5412 bytes. `cmp`: identical (exit 0). Both hashes `43ad8ce22285…`. `diff`: one hunk, `92a93,112`, 0 removed lines | ✅ |
| 11 | Repository check | `python3 tools/check.py` | `check.py: OK (73 files checked, 4 warning(s))` (exit 0). Same four warnings as rounds 2 and 3, none about this analysis | ✅ |
| 1a | Raw file matches its generator | `python3 example/data-folder/home-bp-app/generate.py --check` | `generate.py --check: OK, committed file matches the generator` (exit 0) | ✅ |
| 1b | Script reruns and reproduces `results.csv` | `python3 example/analyses/2026-11-19_home-bp-app-flag/analysis.py --check` | `analysis.py --check: OK, results reproduce exactly` (exit 0) | ✅ |
| 12 | `results.csv` changed only by the added row | `git cat-file -p 647abcba \| diff - example/data-folder/analyses/2026-11-19_home-bp-app-flag/results.csv` | `25a26` / `> highest_diastolic_reading,133/89 on 2026-10-02`. Nothing else | ✅ |
| 20 | Every round reference in Revision 1 is found in this file | Each "Why" cell of `plan.md` lines 103 to 111 read against lines 1 to 291 of this file | See the table below. Every "Round 1" and "Round 2" reference resolves | ✅ |

### The three cells of round 3 finding 1, and the other edits

| Cell | Now reads | Against this file | Verdict |
|---|---|---|---|
| "Decision outcomes", why | "Added by the executor while fixing round 1 finding 2, after a repository review noted that no inconclusive outcome was preregistered; the rejecting branch, which decided the result, is unchanged" | Round 1 finding 2 exists and is the escalation trigger finding, which is the work the cell says the executor was doing. The claim that round 1 noted a missing outcome is gone. The origin is now the executor plus a "repository review" that is not this file; `grep -rn "repository review" --include=*.md .` finds it only in `plan.md` and in round 3's own text, so that review left no record here and the cell is the executor's statement | ✅ attribution no longer false; origin outside this file not checkable |
| "Day 1", why | "No verified source for 'older convention' was found; round 2 flagged an unverified replacement wording" | Round 2 finding 3 (line 237): "A new source claim in `plan.md` § 3 step 5 is not verified", about the wording that had replaced "the older convention of discarding it". Matches. The first half makes no claim about any round | ✅ |
| "Secondary endpoint", before | "Not in the plan; the script reported the highest reading by systolic" | Round 1 finding 7: `highest_single_reading` is chosen by systolic first. The cell no longer presents it as wording of the approved plan | ✅ |
| Other "Why" cells, unchanged since round 3 | "Round 1, finding 5", "finding 2", "finding 7", "finding 6"; first row cites round 1 without a number | Finding 5 is the app sync assumption, 2 the triggers, 7 the highest diastolic reading, 6 the validation key weakness. The first row's two reasons are findings 5 and 2 | ✅ |
| Heading and intro | "after review rounds 1 and 2"; "The executor ran on Claude Opus 5.5; the reviewers on Claude Fable 5.2" | The heading answers round 3 form finding 3 for `plan.md`. All four reviewer headers in this file give `claude-fable-5-2`, which agrees with the second half. The executor's model is the executor's statement; no file or command here can confirm it. If true, the approved § 4 promise of "a different model" holds (round 3 form finding 4) | ✅ consistent; executor model not checkable |
| Folder `README.md`, row `plan.md` | "Phases 0 to 3 and the owner overview as approved, then a dated Revision 1 with every change made after the result" | Answers round 3 form finding 5. "Every change" is true of the plan; changes to other files are listed in `reanalysis.md` § 9, as read in round 3 | ✅ |

### Findings, ranked by consequence

1. **Wrong meaning or wrong number:** none. The three cells no longer attribute anything
   to a round that the round does not say.
2. **Reproducibility:** none. Body identical to the blob, both `--check` scripts pass,
   `results.csv` differs from `647abcba` by the one added row only.
3. **Form**, none blocking:
   1. The header of `conclusion.md` still reads "Revised 2026-11-19 after review round 1"
      (round 3 form finding 3, second half). Same date, so nothing is misdated by day.
      It was not part of the round 3 fix.
   2. Two origins in Revision 1 rest on the executor's word alone: the "repository
      review" (rows "Decision outcomes" and "Scope") and the executor's model. Neither
      touches a number or a time.

Not checkable by the reviewer, carried over from rounds 2 and 3: whether the repository's
owner has seen Revision 1, the fired T7 and the edit to `status/follow-up.md`
([ROLES.md § 3](../../../ROLES.md#3-what-only-the-owner-approves) items 4, 6 and 7).

### Verdict

✅ **Green.** The round 3 fix is met: its four expected results hold (checks 20, 16, 12
and 11). Every number, the answer, the T7 escalation and the flag stand as reviewed in
rounds 1 to 3. No further round is needed. What remains is the owner's part, listed
above, and the optional one word fix in the header of `conclusion.md`.
