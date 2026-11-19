# Reanalysis · 2026-11-19_home-bp-app-flag

**Analysis run:** 2026-11-19 · **By:** Claude Opus 5.5 (AI session) · **Question:** Does
the app's "Stage 1 Hypertension" label hold up when home blood pressure is measured and
averaged the way guidelines describe?

*Synthetic data. Every number below is printed by `analysis.py` and stored in
`example/data-folder/analyses/2026-11-19_home-bp-app-flag/results.csv`.*

## 1. Data
| Source and object | Path | Fields used | Trust tier |
|---|---|---|---|
| `home-bp-app.reading` | `example/data-folder/home-bp-app/raw/export-2026-11-18.csv` | Date, Time, SYS (mmHg), DIA (mmHg), Pulse (bpm), Category, Note | Raw export |

Semantics: [`example/semantics/sources/home-bp-app/reading.md`](../../semantics/sources/home-bp-app/reading.md).

## 2. Extraction
`analysis.py`: `load()` reads the CSV and runs `validate_extract` (84 expected rows,
plausible ranges); `alarm_check()` then checks every raw reading against 180/120 and stops
the script on a hit; `run()` removes exact duplicates and asserts 2, validates that date
and time are then unique, excludes the `cuff loose` reading and asserts 1.

## 3. Definitions
- Period: 2026-09-02 to 2026-11-14, 74 calendar days. Protocol week 2026-11-08 to
  2026-11-14; the primary uses 2026-11-09 to 2026-11-14.
- Protocol reading: `Note == "protocol"`. Everyday reading: every other analysed reading.
- Label share: everyday readings labelled Stage 1 or 2, out of all everyday readings.
- Excluded: 2 exact duplicate rows (identical date, time, values and note; cause not
  documented); 1 reading noted `cuff loose` (owner confirmed invalid).
- Missing data: a protocol day counts only with both morning and evening sessions. All 6
  primary days were complete. Everyday readings have no expected schedule, so missing
  days there are not missing data.
- Protocol week boundaries: from the owner's brief, field 5.

## 4. Calculation
Mean of the readings per day, then the mean of the day means. 95 % interval: mean ±
t(0.975, days − 1) × SD(day means) / √days, with t = 2.571 for 5 degrees of freedom
(standard table). Decision rule from `plan.md` § 0, applied to ESC 2024 (135/85) and to
AHA/ACC (130/80).

**Assumptions:** the six days are independent and roughly normal, one week represents the
owner, and the cuff has no bias. The interval covers only day to day variation within
this week. It does not cover week to week variation or device error. A validated cuff
may still read up to 5 mmHg off on average, which is larger than the diastolic margin to
either threshold (§ 5).

## 5. Result
| Metric | Value |
|---|---|
| Rows analysed | 81 of 84 raw (2 duplicates, 1 excluded) |
| Readings above 180/120 | 0 of 84 raw readings, checked before any exclusion |
| **Protocol mean, days 2 to 7** | **125.5/78.4 mmHg** (24 readings, 6 complete days) |
| 95 % interval, systolic | 122.6 to 128.5 |
| 95 % interval, diastolic | 76.1 to 80.7 |
| **Decision, ESC 2024 (135/85)** | **Rejected**: both upper ends below |
| **Decision, AHA/ACC (130/80)** | **Inconclusive**: diastolic interval spans 80 |
| Primary mean in the ESC home elevated band (120/70 to <135/85) | Yes |
| Margin from upper end to ESC threshold | 6.5 systolic, 4.3 diastolic |
| Margin from upper end to AHA/ACC threshold | 1.5 systolic, −0.7 diastolic |
| Sensitivity, all 7 days | 126.0/78.3; same two decisions |
| Everyday readings labelled Stage 1 or 2 | 40/53 |
| Everyday mean, no note | 128.7/77.5 (n = 26) |
| Everyday mean, with a note | 134.1/81.6 (n = 27) |
| Highest reading, systolic | 145/70 on 2026-09-10 |
| Highest reading, diastolic | 133/89 on 2026-10-02 |
| App label equals the per reading rule | 81/81 |

## 6. Caveats
- One protocol week. Blood pressure varies between weeks.
- Cuff validation unknown; device error alone could move either decision.
- Empty notes mean unknown context.
- The note comparison and the label match are descriptive. In synthetic data the label
  match is built in, because the same rule generated the labels; with real data it is
  the test that matters.
- The synthetic data have no week effect and no missing sessions, which is where a t
  interval works best. Real data are messier.

## 7. How to run it again
`python3 example/analyses/2026-11-19_home-bp-app-flag/analysis.py` from the repository
root, Python 3.9 or later, no packages. `--check` reruns and compares with the committed
results. With a new export: add it as a new file and update `RAW`, `EXPECTED_RAW_ROWS`
and the protocol dates deliberately.

## 8. Scientific basis and source criticism
| Claim | Source | Type | How it was read | Link |
|---|---|---|---|---|
| Home hypertension ≥135/85; protocol | Parati, Stergiou et al., J Hypertens 2021 | Position paper | Full text | [PMC9904446](https://pmc.ncbi.nlm.nih.gov/articles/PMC9904446) |
| ACC/AHA home stage 1 threshold 130/80, same as office | Same paper, describing the 2017 ACC/AHA guideline | Position paper | Full text | [PMC9904446](https://pmc.ncbi.nlm.nih.gov/articles/PMC9904446) |
| AHA/ACC 2025 keeps the 2017 criteria | ACC press release, 2025 | Summary by the issuing body | Full page | [acc.org](https://www.acc.org/About-ACC/Press-Releases/2025/08/13/20/03/New-high-blood-pressure-guideline-emphasizes-prevention-early-treatment-to-reduce-cvd-risk) |
| ESC 2024 home thresholds | McEvoy et al., Eur Heart J 2024, table as reproduced in Rev Esp Cardiol 2025 | Guideline via commentary | Commentary table | [table](https://www.revespcardiol.org/en-comments-on-2024-esc-guidelines-articulo-S1885585725000477) |
| Day 1 higher; discard it, especially in short schedules | Kyriakoulis et al., J Hypertens 2022 | Observational, 2,122 people | Abstract | [doi](https://doi.org/10.1097/HJH.0000000000003157) |
| Validation allows mean device error up to 5 mmHg | ISO 81060-2 criterion 1, as stated in a validation study | Validation study | Table | [PMC7154042](https://pmc.ncbi.nlm.nih.gov/articles/PMC7154042/table/T0002) |
| Single reading >180/120 is severe | American Heart Association | Patient guidance | Full page | [heart.org](https://www.heart.org/en/health-topics/high-blood-pressure/understanding-blood-pressure-readings/hypertensive-crisis-when-you-should-call-911-for-high-blood-pressure) |

The ESC home values come from a commentary, not the guideline text; they agree with the
ESH 2021 home threshold.

## 9. Integrity
- **Preregistration:** not provable. The example was written and run in one session
  before the repository had a commit, so no commit predates the data.
- **Escalation triggers:** T1 not fired (highest 145/70 and 133/89, none above 180/120).
  T2 could not be checked (needs a risk estimate). T3 could not be checked (one week). T4
  not fired (one marker). T5 not fired (no clinician ordered test needed). T6 not fired
  (no new symptoms, owner). **T7 fired:** the guidelines disagree, and the meaning
  depends on risk this analysis cannot estimate. No source used here makes it urgent.
- **Changes after the first result.** The repository's first commit, `b68dc6e`,
  already holds the plan, the data and a result, so the original approved plan is not in
  git. What changed after the first result:
  - Before `b68dc6e`, after the first review rounds: owner questions about duplicates and
    symptoms; triggers T4 to T7; the supported and inconclusive outcomes; the highest
    diastolic reading; asserted counts of duplicates (2) and exclusions (1) and the check
    that date and time are unique; the reason for discarding day 1.
  - `d1bc466`, after an external review showed the AHA/ACC home threshold is 130/80: the
    AHA/ACC comparison and per guideline decisions; *confirmatory* changed to
    *retrospective*; the scope note; the complete day rule; the margin and device error
    step; the day 1 reason reworded to cite both sources; the comparison count changed
    from 2 to every comparison made; three result rows that rested on the earlier single
    threshold removed.
  - `d62d117`, after the final review: the alarm check stops the script; the ESC elevated
    band became a result row; the count went from 89 to 91.
  - The commit "Final review round 2 fixes": the alarm check runs on all 84 raw readings
    before any exclusion; the readings unit alternative became result rows; the count
    went from 91 to 95.
  - The commit "Hard T1 stop, two step preregistration, review checks the conclusion",
    after the green review of `5fc0b38`: the trigger list moved here from conclusion § 7,
    and conclusion § 2 opens with an everyday sentence, to follow the updated conclusion
    template. No number changed.

  The (fictional) owner approved each changed plan with "ok" on 2026-11-19. The ESC
  decision, the primary endpoint and every number in it are unchanged throughout.
- **Hypothesis:** "I think the app is right. My blood pressure is in the hypertension range."
- **Decision and outcome:** ESC 2024 rejected; AHA/ACC inconclusive.
- **Primary endpoint:** protocol week mean, days 2 to 7.
- **Kind of analysis:** retrospective with a plan; the owner had seen the readings.
- **Comparisons held against a reference:** 95 (84 raw readings against the alarm
  limit; systolic and diastolic against two guidelines for the primary and the
  sensitivity analysis; the primary mean against the ESC elevated band; the readings unit
  alternative against AHA/ACC diastolic). The two primary decisions decide the answer.
- **What would falsify it:** a new protocol week, with a validated cuff, whose interval
  lies at or above a threshold.

## 10. Alternatives and replication
- **Other ways:** all readings instead of day means (narrower interval, overstated
  certainty); separate morning and evening means; 24 hour ambulatory monitoring (better,
  but needs a clinician).
- **Free choices:** day 1, the averaging unit, the complete day rule, which guideline.
  Two of them change the AHA/ACC decision: the guideline itself, and the averaging unit.
  With all 24 readings as the unit instead of days, the diastolic interval is 77.1 to
  79.6 and AHA/ACC becomes *rejected* (`alt_readings_unit_*` in `results.csv`). That interval overstates certainty, because two
  readings a minute apart are not independent, which is why the plan uses days.
- **Replication:** a second protocol week with a cuff confirmed as clinically validated.
