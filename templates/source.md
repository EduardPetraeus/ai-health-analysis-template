---
source: <source folder name, as in the data folder>
provider: <company or app>
status: draft | current
verified_by:
last_checked: YYYY-MM-DD
---

# <Source>

*Template for `semantics/sources/<source>/README.md`. Rules: `METHOD.md § 6`
and `semantics/CONCEPTS.md`. Delete the italic guidance when
filling in.*

## 1. What the source is and measures
*Two to five sentences: what the provider measures, how (sensor, app, lab, manual
entry), and what it cannot measure.*

## 2. Devices and periods
| Device or app version | From | To | Source of this information |
|---|---|---|---|

## 3. Deliveries
*One row per way the data arrive. Exports and APIs side by side. Old deliveries are
marked superseded, never deleted.*

| Delivery | Type | Path in data folder | Period | Documentation | Status |
|---|---|---|---|---|---|

## 4. Objects
| Object | Grain: one row is | File | Deliveries |
|---|---|---|---|

## 5. Relations between objects
*Which objects refer to each other, with which key; what aggregates into what.*

## 6. Concepts
*Which concepts in `semantics/ontology/` the source carries, by `id`.*

## 7. Time
*Time zone per delivery, daylight saving, how a "day" is defined.*

## 8. Personal data and other people's data
*Names, IDs, location data, files about other people or payments that are not opened.*

## 9. Official documentation
| What | URL | Retrieved |
|---|---|---|

## 10. Undocumented and open questions
*Ranked by how much they matter for analyses.*
