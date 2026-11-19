---
source: home-bp-app
provider: a fictional consumer blood pressure app (synthetic example)
status: current
verified_by: example author, 2026-11-19
last_checked: 2026-11-19
---

# home-bp-app

*Filled in from [`templates/source.md`](../../../../templates/source.md). The app is
fictional and its data synthetic; the guideline sources are real.*

## 1. What the source is and measures
A phone app that receives readings from an upper arm cuff monitor over Bluetooth, stores
them, and labels each one with a category. It measures blood pressure and pulse at the
moment of the reading. It cannot know whether the person rested, talked, had coffee or
had just walked in, except through the free text note the person types.

## 2. Devices and periods
| Device or app version | From | To | Source of this information |
|---|---|---|---|
| Upper arm cuff, one device throughout | September 2026 | mid November 2026 | Owner, stated in the brief |

Whether the cuff is clinically validated is **undocumented** (the owner does not know the
model's validation status). See section 10.

## 3. Deliveries
| Delivery | Type | Path in data folder | Period | Documentation | Status |
|---|---|---|---|---|---|
| CSV export 2026-11-18 | export | `home-bp-app/raw/export-2026-11-18.csv` | 2026-09-02 to 2026-11-14 | Column headers only; no data dictionary | current |

## 4. Objects
| Object | Grain: one row is | File | Deliveries |
|---|---|---|---|
| `reading` | One cuff measurement | [`reading.md`](reading.md) | CSV export 2026-11-18 |

## 5. Relations between objects
One object only. Several readings on the same occasion (the protocol week's duplicate
readings) are separate rows with times one minute apart; nothing in the export groups
them.

## 6. Concepts
`cardiovascular.systolic_bp`, `cardiovascular.diastolic_bp`, `cardiovascular.pulse_rate`.

## 7. Time
Local time of the phone, no time zone in the export. All readings fall in one time zone.

## 8. Personal data and other people's data
No name or ID in the export. The free text `Note` could contain personal text; it is used
only as the context tags listed in [`reading.md`](reading.md).

## 9. Official documentation
| What | URL | Retrieved |
|---|---|---|
| The app has no public data dictionary | none | 2026-11-19 |
| Guideline definitions used to interpret the label | see [`example/knowledge/home-blood-pressure.md`](../../../knowledge/home-blood-pressure.md) | 2026-11-19 |

## 10. Undocumented and open questions
1. **How the app assigns `Category`.** No documentation. Reconstructed from data in
   [`reading.md`](reading.md) § 4: it matches office cut points applied to each single
   reading, 81 of 81 rows.
2. **Whether the cuff is clinically validated.** Unknown; listed as a caveat.
