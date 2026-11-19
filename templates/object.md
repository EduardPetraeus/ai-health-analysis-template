---
source: <source>
object: <object, lowercase_with_underscores>
id: <source>.<object>
status: draft | current
verified_by:
last_checked: YYYY-MM-DD
---

# <source>.<object>

*Template for `semantics/sources/<source>/<object>.md`. Rules: `METHOD.md § 6`.*

## 1. What the object is
*One to three sentences. **Grain:** one row is ... . How the object comes about
(measurement, computed by the provider, manual entry).*

## 2. Relations
*To other objects (key and direction) and to concepts in the ontology.*

## 3. Fields
*One field per row. The name is the canonical one; delivery names are in section 4.
Status: documented, partial or undocumented. An undocumented field is not used for
conclusions.*

| Field | Meaning | Unit, coding or scale | Concept `id` | Source of definition | Status |
|---|---|---|---|---|---|

## 4. Deliveries
*One table per delivery: what each field is called there and how it differs (rounding,
unit, language, calculation). A mapping is verified on data, with the command and output
recorded where it was verified.*

### <Delivery name, e.g. "CSV export 2026">
| Field | Column in delivery | Difference | Verified |
|---|---|---|---|

## 5. Time
*Time zone, daylight saving, which timestamp defines the day.*

## 6. Caveats and context
*What the object cannot carry; what absence means; known breaks in the data.*

## 7. Sources
| What | URL | Retrieved |
|---|---|---|
