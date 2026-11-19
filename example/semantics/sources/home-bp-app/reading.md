---
source: home-bp-app
object: reading
id: home-bp-app.reading
status: current
verified_by: example author, 2026-11-19
last_checked: 2026-11-19
---

# home-bp-app.reading

*Filled in from [`templates/object.md`](../../../../templates/object.md).*

## 1. What the object is
**Grain:** one row is one cuff measurement, taken when the person pressed start. The app
stores what the cuff reports and adds a category label computed by the app.

## 2. Relations
Carries `cardiovascular.systolic_bp`, `cardiovascular.diastolic_bp` and
`cardiovascular.pulse_rate`. No keys to other objects.

## 3. Fields
| Field | Meaning | Unit, coding or scale | Concept `id` | Source of definition | Status |
|---|---|---|---|---|---|
| `date` | Local date of the reading | YYYY-MM-DD | | Column header | documented |
| `time` | Local time of the reading | HH:MM | | Column header | documented |
| `systolic_mmhg` | Systolic pressure | mmHg, integer | `cardiovascular.systolic_bp` | Column header with unit | documented |
| `diastolic_mmhg` | Diastolic pressure | mmHg, integer | `cardiovascular.diastolic_bp` | Column header with unit | documented |
| `pulse_bpm` | Pulse during the measurement | beats per minute | `cardiovascular.pulse_rate` | Column header with unit | documented |
| `category` | The app's label for **this single reading** | Normal, Elevated, Stage 1 Hypertension, Stage 2 Hypertension | | **No provider documentation.** Rule reconstructed on data, § 4 | partial |
| `note` | Free text typed by the person | Tags in use: empty, `after coffee`, `stressful day`, `just got home`, `cuff loose`, `protocol` | | Owner, stated in the brief | documented |

## 4. Deliveries

### CSV export 2026-11-18: `raw/export-2026-11-18.csv`
| Field | Column in delivery | Difference | Verified |
|---|---|---|---|
| `date` | `Date` | | |
| `time` | `Time` | | |
| `systolic_mmhg` | `SYS (mmHg)` | | |
| `diastolic_mmhg` | `DIA (mmHg)` | | |
| `pulse_bpm` | `Pulse (bpm)` | | |
| `category` | `Category` | See below | ✅ 81/81 rows |
| `note` | `Note` | | |

**How `Category` was decoded.** Hypothesis: the app applies the AHA/ACC office categories
to each reading on its own (Stage 2 if ≥140 or ≥90; Stage 1 if ≥130 or ≥80; Elevated if
systolic 120 to 129 and diastolic below 80; otherwise Normal). Test: `app_rule()` in
[`analysis.py`](../../../analyses/2026-11-19_home-bp-app-flag/analysis.py), applied to every
analysed row. Result: `app_label_matches_office_rule = 81/81`.

**Untested part (review round 1):** no reading in this delivery has a systolic of exactly
140 or a diastolic of 90 or more, so the Stage 2 boundary (≥ or >, and the diastolic arm)
is not exercised. Reuse the rule for Stage 2 only after a delivery that tests it.

**What that means:** the label is an **office** category applied to **one** home
reading, without any averaging or measurement protocol. Guidelines define categories on
averages of properly taken readings, and home thresholds differ from office thresholds
([`knowledge/home-blood-pressure.md`](../../../knowledge/home-blood-pressure.md)).

## 5. Time
Local phone time; no time zone or daylight saving information. A "day" is the local
calendar date.

## 6. Caveats and context
- A note is only present when the person typed one. **No note does not mean rested and
  seated**; it means unknown.
- The export contains **exact duplicate rows** (two in this delivery). The cause is not
  documented; app sync is likely but unconfirmed. Identical date, time, values and note
  are treated as one reading.
- A reading noted `cuff loose` is a known invalid measurement and is excluded.
- Readings taken one minute apart on the same occasion are not independent; average by
  day before computing uncertainty.

## 7. Sources
| What | URL | Retrieved |
|---|---|---|
| AHA/ACC 2025 categories (used to decode the label), ACC press release | https://www.acc.org/About-ACC/Press-Releases/2025/08/13/20/03/New-high-blood-pressure-guideline-emphasizes-prevention-early-treatment-to-reduce-cvd-risk | 2026-11-19 |
