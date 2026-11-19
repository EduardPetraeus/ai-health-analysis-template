# Conclusion · 2026-11-19_home-bp-app-flag

**Analysis:** 2026-11-19 · **Full trail:** [`reanalysis.md`](reanalysis.md) ·
[`review.md`](review.md)

*Synthetic example. Not medical advice ([DISCLAIMER.md](../../../DISCLAIMER.md)).*

## 1. What we asked
Does my app's "Stage 1 Hypertension" label hold up when my blood pressure is measured and
averaged the way guidelines describe?

## 2. The answer
It depends on the guideline. Your protocol week average, 125.5/78.4 mmHg, is below the
European home threshold of 135/85. Against the US home threshold of 130/80 it is
unresolved: the diastolic could be just above or just below.

## 3. What the comparison shows
- The app labels **each single reading**. Guidelines apply categories to an **average**
  of properly taken readings.
- 40 of your 53 everyday readings (2026-09-02 to 2026-11-07) got a Stage 1 or 2 label.
  Readings with a note such as coffee or just got home averaged 134.1/81.6 (n = 27),
  against 128.7/77.5 without a note (n = 26).
- The average comes from 24 readings over 6 complete days, 2026-11-09 to 2026-11-14.

## 4. What you learned
The label describes the app's rule, applied one reading at a time. Which guideline you
are measured against matters as much as your numbers. Three rows were set aside first:
two identical duplicates and one loose cuff reading.

## 5. What this does NOT answer
- Whether you need treatment, or your overall heart and stroke risk.
- Whether one week represents you.
- Whether your cuff is accurate: a validated cuff may read up to 5 mmHg off, more than
  the diastolic margin.
- No trigger fired does not mean the value is unimportant; this method cannot rule out
  disease.

## 6. Flags

| Home blood pressure | |
|---|---|
| Value | 125.5/78.4 mmHg, protocol week |
| Reference and source | ESC 2024 home: elevated 120/70 to <135/85. AHA/ACC home stage 1: 130/80 |
| Status | ESCALATED (T7) |

## 7. Questions to take to a clinician
- Which guideline do you use, and where does a home average of 125.5/78.4 fall in it?
- Should my overall cardiovascular risk be assessed?
- Is my cuff on a validated list?

Triggers: T1 not fired (highest 145/70 and 133/89, none above 180/120). T2 could not be
checked (needs a risk estimate). T3 could not be checked (one week). T4 not fired (one
marker). T5 not fired (no clinician ordered test needed). T6 not fired (no new symptoms,
owner). **T7 fired:** the guidelines disagree, and the meaning depends on risk this
analysis cannot estimate. No source used here makes it urgent.

## 8. How sure are we
For the European threshold, fairly sure for this week: the whole interval (122.6 to
128.5 / 76.1 to 80.7) is below 135/85, and keeping day 1 gives 126.0/78.3. For the US
threshold we cannot tell. The interval covers this week only, not device error. A new
protocol week with a validated cuff would settle it.
