# Reanalysis · 2026-11-19_home-bp-app-flag

**Analysis run:** 2026-11-19 · **By:** example author (AI session) · **Question:** Does the
app's "Stage 1 Hypertension" label hold up when home blood pressure is measured and
averaged the way guidelines describe?

*Synthetic data. Every number below is printed by `analysis.py` and stored in
`example/data-folder/analyses/2026-11-19_home-bp-app-flag/results.csv`.*

## 1. Data
| Source and object | Path | Fields used | Trust tier |
|---|---|---|---|
| `home-bp-app.reading` | `example/data-folder/home-bp-app/raw/export-2026-11-18.csv` (sha256 starts `562a0b80`) | Date, Time, SYS (mmHg), DIA (mmHg), Pulse (bpm), Category, Note | Raw export |

Semantics: [`example/semantics/sources/home-bp-app/reading.md`](../../semantics/sources/home-bp-app/reading.md).

## 2. Extraction
`analysis.py`: `load()` reads the CSV and runs `validate_extract` (84 expected rows,
plausible ranges); `run()` removes exact duplicates with `deduplicate()` and asserts the
preregistered 2, validates that date and time are then unique, and excludes the
`cuff loose` reading, asserting the preregistered 1.

## 3. Definitions
- Period: 2026-09-02 to 2026-11-14, 74 calendar days. Protocol week 2026-11-08 to
  2026-11-14, 7 days; primary uses 2026-11-09 to 2026-11-14, 6 days.
- Protocol reading: `Note == "protocol"`. Ad hoc reading: every other analysed reading.
- Numerator and denominator for label shares: ad hoc readings labelled Stage 1 or 2, out
  of all ad hoc readings.
- Excluded: 2 exact duplicate rows (identical date, time, values, note; cause
  undocumented, the owner does not know it); 1 reading noted `cuff loose` (owner
  confirmed invalid). Keeping the duplicates changes only ad hoc shares (42/55), not the
  primary endpoint (review round 1).
- Groups: protocol week boundaries from the owner's brief, field 4.

## 4. Calculation
Mean of readings per day, then the mean of the day means. 95 % interval:
mean ± t(0.975, df = days − 1) × SD(day means) / √days, with t = 2.571 for 5 df (standard
table). Day means are used because two readings a minute apart are not independent.

## 5. Result
| Metric | Value |
|---|---|
| Rows analysed | 81 of 84 raw (2 duplicates, 1 excluded) |
| App label equals office cut points per reading | 81/81 readings |
| **Primary: protocol mean, days 2 to 7** | **125.5/78.4 mmHg** (24 readings over 6 days) |
| 95 % interval, systolic | 122.6 to 128.5 |
| 95 % interval, diastolic | 76.1 to 80.7 |
| Sensitivity: all 7 days | 126.0/78.3 mmHg |
| Ad hoc readings labelled Stage 1 or 2 | 40/53 (75 %) |
| Ad hoc mean, no note | 128.7/77.5 mmHg (n = 26) |
| Ad hoc mean, with a context note | 134.1/81.6 mmHg (n = 27) |
| Highest single reading (systolic) | 145/70 on 2026-09-10 |
| Highest diastolic reading | 133/89 on 2026-10-02 |
| Any reading >180/120 | No |

## 6. Caveats
- One protocol week only. Blood pressure varies across weeks and seasons.
- Cuff validation status unknown; a non validated cuff can be biased in either direction.
- Empty notes mean unknown context, so "no note" readings may still include coffee or
  rushing.
- The diastolic interval reaches 80.7, inside the range the app's office cut points call
  Stage 1. Those cut points are office categories; their home equivalents under AHA/ACC
  2025 were not verified and are not used.

## 7. How to run it again
`python3 example/analyses/2026-11-19_home-bp-app-flag/analysis.py` from the repository
root, Python 3.9 or later, no packages. `--check` reruns and compares with the committed
results. With a new export: add it as a new file, update `RAW` and `EXPECTED_RAW_ROWS`
deliberately, and update the protocol dates.

## 8. Scientific basis and source criticism
| Claim | Source | Type | Certainty (informal, with reason) | Population match | Link |
|---|---|---|---|---|---|
| Home hypertension ≥135/85 | Parati, Stergiou et al., J Hypertens 2021 | Position paper | Moderate: expert consensus, agrees with ESC 2024 | Adults | [PMC9904446](https://pmc.ncbi.nlm.nih.gov/articles/PMC9904446) |
| ESC home elevated 120/70 to <135/85; home hypertension ≥135/85 | McEvoy et al., Eur Heart J 2024, as tabulated in Rev Esp Cardiol 2025 | Guideline via expert commentary | Moderate: guideline full text not opened | Adults | [doi](https://doi.org/10.1093/eurheartj/ehae178), [table](https://www.revespcardiol.org/en-comments-on-2024-esc-guidelines-articulo-S1885585725000477) |
| AHA/ACC office categories unchanged from 2017 | ACC press release 2025 | Guideline summary | Moderate: summary by the issuing body; not reopened by the reviewer | US adults | [acc.org](https://www.acc.org/About-ACC/Press-Releases/2025/08/13/20/03/New-high-blood-pressure-guideline-emphasizes-prevention-early-treatment-to-reduce-cvd-risk) |
| Protocol: 7 days, duplicates, 5 min rest | Parati, Stergiou et al. 2021 | Position paper | Moderate: expert consensus | Adults | [PMC9904446](https://pmc.ncbi.nlm.nih.gov/articles/PMC9904446) |
| Day 1 about 2.8/1.4 higher | J Hypertens 2022;40:1380–1387, PMID 35762478 | Observational | Low to moderate: one pooled cross sectional analysis | Adults in Finland, Greece, UK | [doi](https://doi.org/10.1097/HJH.0000000000003157) |
| Severe reading >180/120 | American Heart Association | Patient guidance | Used as a safety limit only | Adults, not pregnant | [heart.org](https://www.heart.org/en/health-topics/high-blood-pressure/understanding-blood-pressure-readings/hypertensive-crisis-when-you-should-call-911-for-high-blood-pressure) |

**Source criticism.** The ESC home thresholds come from a reproduction of the guideline's
table by a national society's working group, not the guideline full text; they agree
with the ESH 2021 paper's home threshold, which lowers the risk of a transcription error.
The AHA/ACC home equivalents are a gap, stated rather than filled in.

## 9. Integrity
- **Hypothesis:** "I think the app is right. My blood pressure is in the hypertension range."
  Tested as: the protocol week mean is at or above 135/85.
- **Null hypothesis:** the mean is below 135/85, with the upper end of its interval also
  below.
- **Primary endpoint:** protocol week mean, days 2 to 7.
- **Secondary endpoints:** listed in `plan.md` § 0.
- **Exploratory or confirmatory:** confirmatory for the primary endpoint.
- **Number of metrics held against a reference:** 2 (systolic and diastolic mean). With
  two, chance alone is a minor concern.
- **What would falsify the conclusion:** a new protocol week, with a validated cuff,
  averaging at or above 135/85.
- **Did the result differ from the hypothesis?** Yes. The owner expected hypertension;
  the primary endpoint is below the home threshold with its whole interval. After the
  result, during review round 1, the plan gained a dated revision (`plan.md`, Revision 1):
  two owner questions, triggers T4 to T7, two more decision outcomes, one secondary
  endpoint and stricter validation. The deciding rule and every earlier number are
  unchanged.

## 10. Alternatives and replication
- **Other ways:** keep day 1 (done as sensitivity: 126.0/78.3); average all readings
  instead of day means (smaller interval, overstated certainty); use ambulatory 24 hour
  monitoring (better, but needs a clinician).
- **Free choices that could change the number:** day 1, the averaging unit, and whether
  untagged ad hoc readings are trusted. None moves the mean near 135/85.
- **Replication:** a second protocol week in about three months, with a cuff confirmed
  as clinically validated.
