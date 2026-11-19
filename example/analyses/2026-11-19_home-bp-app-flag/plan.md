# Plan · 2026-11-19_home-bp-app-flag

**Brief:** [`brief.md`](brief.md) · **Status:** approved 2026-11-19 by the (fictional)
owner. How the plan changed after the first result: `reanalysis.md` § 9.

## 0. Hypothesis and decision rule

| Field | Content |
|---|---|
| Owner's hypothesis (verbatim) | "I think the app is right. My blood pressure is in the hypertension range." |
| Owner's falsification (verbatim) | "If my average from the proper measurement week is clearly below the threshold that applies to home measurements." |
| Hypothesis as tested | The protocol week's mean home blood pressure is at or above the home threshold of each guideline compared |
| Decision rule: supported | The lower end of the 95 % interval is at or above the threshold, for systolic **or** diastolic |
| Decision rule: rejected | The upper ends of both intervals are below the threshold, systolic **and** diastolic |
| Decision rule: inconclusive | Anything else |
| Primary endpoint | Protocol week mean home systolic and diastolic, days 2 to 7, averaged by day |
| Secondary endpoints | Same mean with all 7 days; share of everyday readings the app labels Stage 1 or 2; everyday means with and without a note; highest systolic and diastolic readings; whether the label matches a per reading rule |
| Kind of analysis | Retrospective with a preregistered plan: the owner has seen the readings in the app |
| Guidelines compared against | Both, since the owner does not know which applies: ESC 2024 (home hypertension 135/85) and AHA/ACC (home stage 1 130/80) |
| Scope note | The analysis compares an average with published thresholds. A diagnosis is a clinician's call |

## 1. Scientific ground truth

Sources with links: [`example/knowledge/home-blood-pressure.md`](../../knowledge/home-blood-pressure.md).

| Claim or threshold | Source | Opened and read? | Matches the owner? |
|---|---|---|---|
| ESC 2024 home: elevated 120/70 to <135/85, hypertension ≥135/85 | ESC 2024, as tabulated in a society commentary | Commentary table | Unknown: owner's country not stated |
| AHA/ACC: home stage 1 threshold 130/80, same as office | ESH 2021 position paper, describing the ACC/AHA guideline; ACC 2025 press release (criteria unchanged) | Full text; press release | Unknown |
| Protocol: 7 days (not fewer than 3), two readings morning and evening, 5 min seated rest | ESH 2021 position paper | Full text | Adults: yes |
| Day 1 runs higher; discard it, especially in short schedules | Kyriakoulis et al. 2022 | Abstract | Adults: yes |
| Device error accepted by validation: mean difference up to 5 mmHg | ISO 81060-2, as stated in a validation study | Table | General |
| Single reading higher than 180/120: severe | American Heart Association | Patient page | Adults, not pregnant: yes |

## 2. Data manifest

| Source and object | Path (relative to data folder) | Fields | Period | Rows | Semantics |
|---|---|---|---|---|---|
| `home-bp-app.reading` | `home-bp-app/raw/export-2026-11-18.csv` | all seven | 2026-09-02 to 2026-11-14 | 84 | Documented, except `category`: no provider documentation, decoded on data as a secondary endpoint |

**Gaps and oddities found when describing the file:** two exact duplicate rows (cause not
documented); one reading noted `cuff loose`; notes are optional, so an empty note means
unknown context; cuff validation status unknown.

**Questions for the owner, with answers:** Was the protocol week done seated after rest?
"Yes, 5 minutes, back supported." Is the `cuff loose` reading invalid? "Yes." Do you know
why two rows are identical? "No." Any new symptoms since your last check up? "No."

## 3. Method

1. Validate the raw file before use: 84 rows (constant), plausible ranges. Fail hard
   otherwise.
2. Remove exact duplicates (2 expected), then require date and time to be unique.
   Exclude `cuff loose` (1 expected).
3. Safety: check every reading against the AHA alarm limit of 180/120 before anything
   else.
4. Primary endpoint: protocol readings on days 2 to 7. A day counts only with both its
   morning and evening session; at least 3 complete days are required. Mean per day,
   then the mean of the day means, with a 95 % t interval on the day means.
   **Assumptions:** days are independent and roughly normal; one week represents the
   owner; the cuff has no bias. Readings within a day are not independent, which is why
   days are the unit.
5. Apply the decision rule (§ 0) separately for ESC 2024 and AHA/ACC.
6. Sensitivity: all 7 days. Discarding day 1 is a free choice: ESH 2021 calls it
   debated, the 2022 schedule study recommends it for short schedules.
7. Measurement error: report the distance from each interval's upper end to each
   threshold, next to the device error a validated cuff may have.
8. Secondary endpoints as listed, all descriptive.

**Expected results:** 84 raw rows, 2 duplicates, 1 exclusion, 81 analysed; 24 protocol
readings over 6 complete days in the primary.

**Escalation triggers:**
- T1: any single reading above 180/120. AHA says to wait at least a minute and measure
  again, and to call emergency services if it stays that high with symptoms.
- T2: ESC 2024 ties the handling of elevated blood pressure to overall cardiovascular
  risk, which this analysis does not estimate: could not be checked.
- T3: one protocol week: could not be checked.
- T4: one marker, no combination to assess: not fired.
- T5: fired only if answering the question needs a test only a clinician can order.
- T6: owner reports no new symptoms (answered above).
- T7: fired if the answer differs between the two guidelines or lands in a range whose
  meaning depends on overall risk.

**Comparisons held against a reference:** every analysed reading against the alarm
limit; systolic and diastolic against two guidelines for the primary and the sensitivity
analysis; the primary mean against the ESC elevated band. The two primary decisions decide the answer.

## 4. Execution and review

- Script: `analysis.py`. Output: `example/data-folder/analyses/2026-11-19_home-bp-app-flag/results.csv`.
- Review: a separate session on another model reruns everything.
- May write: this folder and the output folder. May not touch: raw data; `status/` only
  with the owner's ok.

## Overview for the owner

- **What we are finding out:** whether your app's "Stage 1" label holds up.
- **How we test your hypothesis:** your proper measurement week, averaged, against the
  home thresholds of both the European and the US guideline.
- **Data and weak spots:** one app export; notes are optional; your cuff's validation is
  unknown; only one proper week.
- **What this can NOT answer:** your overall heart risk, or whether you need treatment.
- **What comes back to you:** any reading above 180/120 immediately; the final answer.
