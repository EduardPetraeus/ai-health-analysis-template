# Conclusion · 2026-11-19_home-bp-app-flag

**Analysis:** 2026-11-19 · **Full trail:** [`reanalysis.md`](reanalysis.md) ·
[`review.md`](review.md) · *Revised 2026-11-19 after review rounds 1 and 2.*

*Synthetic example. Not medical advice ([DISCLAIMER.md](../../../DISCLAIMER.md)).*

## 1. What we asked
Does my app's "Stage 1 Hypertension" label hold up when my blood pressure is measured and
averaged the way guidelines describe?

## 2. The answer
No. Your protocol week average, 125.5/78.4 mmHg (24 readings over 6 days, 2026-11-09 to
2026-11-14, day 1 left out), is below the European home threshold for hypertension of
135/85. Whether you have hypertension is a clinician's call, not this analysis's.

## 3. What it means for you
- The app labels **each single reading** with US **office** categories. Guidelines apply
  categories to **averages**; European guidelines use 135/85 at home, 140/90 in the office.
- 40 of your 53 everyday readings (2026-09-02 to 2026-11-07) got a Stage 1 or 2 label.
  Readings with a note such as coffee or just got home averaged 134.1/81.6 (n = 27),
  against 128.7/77.5 without a note (n = 26).
- Your average is in the European *elevated* range.

## 4. What you learned
The label describes the app's rule, not your blood pressure. Three rows were set aside
first: two identical duplicates and one loose cuff reading.

## 5. What this does NOT answer
- Whether you need treatment, or your overall heart and stroke risk.
- Whether one week represents you.
- Whether your cuff is accurate; its validation is unknown.
- What your average means under US home categories; not verified.

## 6. Flags

| Home blood pressure | |
|---|---|
| Value | 125.5/78.4 mmHg, protocol week |
| Reference and source | ESC 2024 home: non elevated below 120/70; elevated 120/70 to <135/85 |
| Status | ESCALATED (T7), routine |

## 7. What happens now
- **Book a routine clinician appointment for a risk assessment**, bringing the protocol
  week average, not the app's label.
- Repeat a protocol week by 2027-02-19 with a validated cuff.
- Escalation triggers:
  - T1 not fired: highest readings 145/70 and 133/89, none above 180/120.
  - T2 could not be checked: needs a risk estimate this analysis lacks.
  - T3 could not be checked: one protocol week only.
  - T4 not fired: one marker, so no combination to assess.
  - T5 not fired: the question needed no clinician ordered test.
  - T6 not fired: no new symptoms (owner, asked during review, `plan.md` Revision 1).
  - **T7 fired:** without that estimate, what the elevated average means cannot be bounded.

## 8. How sure are we
Fairly sure for this week: the whole 95 % interval (122.6 to 128.5 / 76.1 to 80.7) is
below 135/85; keeping day 1 gives 126.0/78.3. A new protocol week with a validated cuff
averaging 135/85 or more would overturn it.
