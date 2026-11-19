# Plan · 2026-11-19_home-bp-app-flag

**Brief:** [`brief.md`](brief.md) · **Status:** approved 2026-11-19 by the (fictional)
owner: "ok"

## 0. Hypothesis and endpoints

| Field | Content |
|---|---|
| Owner's hypothesis (verbatim) | "I think the app is right. My blood pressure is in the hypertension range." |
| Owner's falsification (verbatim) | "If my average from the proper measurement week is clearly below the threshold that applies to home measurements." |
| Hypothesis as tested | The mean home blood pressure of the protocol week is at or above the home hypertension threshold of 135/85 mmHg |
| Null hypothesis | The protocol week mean is below 135/85, with the upper end of its 95 % interval also below |
| Primary endpoint | Protocol week mean home systolic and diastolic blood pressure, days 2 to 7, averaged by day |
| Secondary endpoints | Same mean including day 1; share of ad hoc readings the app labels Stage 1 or 2; ad hoc means with and without a context note; whether the app label equals office cut points per reading |
| Exploratory or confirmatory | Confirmatory for the primary endpoint; secondary endpoints are descriptive |

## 1. Scientific ground truth

| Claim or threshold | Source | Type | Population match |
|---|---|---|---|
| Home hypertension ≥135/85 mmHg | ESH 2021 home monitoring position paper; ESC 2024 | Position paper; guideline | General adult population |
| ESC home *elevated BP* 120/70 to <135/85 | ESC 2024, via SEC commentary table | Guideline, secondary reproduction | General adult population |
| AHA/ACC categories (office) | 2025 AHA/ACC guideline, via ACC press release | Guideline summary | General adult population |
| Measurement protocol: 7 days, duplicates morning and evening, 5 min rest | ESH 2021 | Position paper | |
| Day 1 runs higher | J Hypertens 2022;40:1380–1387 | Observational, 2,122 people | |
| Severe single reading >180/120 | AHA patient guidance | Patient guidance | |

Full list with links: [`example/knowledge/home-blood-pressure.md`](../../knowledge/home-blood-pressure.md).

## 2. Data manifest

| Source and object | Path (relative to data folder) | Fields used | Period | Rows | Semantics documented? |
|---|---|---|---|---|---|
| `home-bp-app.reading` | `home-bp-app/raw/export-2026-11-18.csv` | all seven | 2026-09-02 to 2026-11-14 | 84 | Yes; `category` partly, decoded on data |

**Gaps and oddities found when listing the file:** two exact duplicate rows (app sync);
one reading noted `cuff loose`; context notes are optional, so an empty note means
unknown, not rested; cuff validation status unknown.

**Questions for the owner, answered:** Was the protocol week done seated after rest?
"Yes, 5 minutes, back supported." Is the `cuff loose` reading invalid? "Yes."

## 3. Method

1. Read the raw file; validate before use: 84 rows expected (constant), plausible ranges
   for systolic, diastolic and pulse. Fail hard otherwise.
2. Remove exact duplicates (same date, time, values and note). Exclude `cuff loose`.
3. Decode the label: apply office cut points to each reading and count matches with
   `Category`.
4. Primary endpoint: protocol readings on days 2 to 7; mean per day, then the mean of the
   six day means, with a 95 % interval from the t distribution on the day means (readings
   within a day are not independent).
5. Sensitivity: the same with all seven days. ESH 2021 calls discarding day 1 debated, so
   both are reported; the primary uses the older convention of discarding it.
6. Secondary: ad hoc readings (not `protocol`): share labeled Stage 1 or 2; mean with and
   without a note.
7. Decide: if the upper ends of both intervals are below 135/85, the hypothesis is
   rejected for the protocol week.

**Free choices:** discarding day 1; averaging by day; treating untagged ad hoc readings
as unknown context.

**Expected results, preregistered:** 84 raw rows, 2 duplicates, 1 exclusion, 81 analysed;
24 protocol readings over 6 days in the primary; `results.csv` with one row per metric.

**Escalation triggers:** T1, any reading >180/120 (AHA). T2, referral indication: the
guideline management of elevated BP depends on overall cardiovascular risk, which this
analysis cannot estimate. T3, worsening over three independent measurements: not
applicable to one protocol week; reported as not checkable. T4 to T7 assessed at closing.

**Number of metrics held against a reference:** 2 (protocol mean systolic and diastolic).

## 4. Execution and review

- Script: `analysis.py` in this folder; output to `data-folder/analyses/2026-11-19_home-bp-app-flag/results.csv`.
- Review: a separate session on a different model reruns the script and checks every
  number and source.
- May write: this folder, the output folder. May not touch: raw data, `status/` files
  other than adding a flag row after the owner agrees.

## Overview for the owner

- **What we are finding out:** whether your app's "Stage 1" label holds up.
- **How we test your hypothesis:** your proper measurement week, averaged, against the
  home threshold of 135/85.
- **Data and weak spots:** one app export; notes are optional; your cuff's validation is
  unknown; only one proper week.
- **What this can NOT answer:** your overall heart risk, or whether you need treatment.
- **What comes back to you:** any reading above 180/120 immediately; the final answer.

🛑 Approved by the owner before the script was written.

---

## Revision 1 · 2026-11-19, after review rounds 1 and 2

*Added after the result was known, during review rounds 1 and 2 ([`review.md`](review.md)).
The executor ran on Claude Opus 5.5; the reviewers on Claude Fable 5.2. The
approved plan above is left exactly as it was approved, so the review's quotes of it stay
true. Nothing here changed the deciding rule (§ 3 step 7) or any number.*

| What | Before | After | Why |
|---|---|---|---|
| Owner questions | Two questions asked before the ok | Two more asked after the result: "Do you know why two rows are identical?" "No." "Any new symptoms since your last check up?" "No." | Round 1: the duplicates' cause was stated as app sync without evidence, and T6 had no data behind it |
| Duplicates | "two exact duplicate rows (app sync)" | Cause undocumented; app sync likely but unconfirmed | Round 1, finding 5 |
| Escalation triggers | T1 to T3 set before the result; "T4 to T7 assessed at closing" | T4 not fired (one marker, no combination to assess); T5 not fired (no clinician ordered test needed to answer the question); T6 not fired (owner answer above); T7 fired, because T2 could not be checked and the meaning of an elevated average cannot be bounded without a risk estimate | Round 1, finding 2. Writing T4 to T7 at closing went against METHOD § 9; that weakness is recorded here rather than hidden |
| Decision outcomes | Only the rejecting branch was written | Also "supported" (lower ends at or above 135/85) and "inconclusive" (anything in between) | Added by the executor while fixing round 1 finding 2, after a repository review noted that no inconclusive outcome was preregistered; the rejecting branch, which decided the result, is unchanged |
| Secondary endpoint | Not in the plan; the script reported the highest reading by systolic | Also the highest diastolic reading | Round 1, finding 7 |
| Validation | Row count and ranges | Also: 2 duplicates and 1 exclusion asserted, and date plus time unique after deduplication | Round 1, finding 6 |
| Day 1 | "the older convention of discarding it" | Discarding day 1 is a free choice: ESH 2021 calls it debated, and the 2022 study found day 1 about 2.8/1.4 mmHg higher. Both versions are reported | No verified source for "older convention" was found; round 2 flagged an unverified replacement wording |
| Scope | Owner asked "is it hypertension or not" | The analysis compares an average with published thresholds; a diagnosis is a clinician's call | Repository review |

*The (fictional) owner saw this revision, the fired T7 and the new `status/follow-up.md` row, and answered "ok" on 2026-11-19.*
