---
metric: <metric name, lowercase_with_underscores>
version: 1
status: draft | current
approved_by_owner:
last_checked: YYYY-MM-DD
---

# <metric>

*Template for `semantics/metrics/<metric>.md`. A metric is a formula that computes a
number from documented fields. A metric the owner has not approved does not carry an
analysis.*

## 1. Definition
*One sentence in plain language.*

## 2. Formula
```text
<formula, using fields as source.object.field>
```

## 3. Grain and filters
- Grain: *(one value per day, per measurement, per week)*
- Filters and exclusions:
- Minimum data required for a valid value:

## 4. Inputs
| Field (`source.object.field`) | Unit | Documented in |
|---|---|---|

## 5. Source of the definition
| What | URL | Retrieved |
|---|---|---|

## 6. Caveats
*What the metric cannot be used for.*

## 7. Versions
| Version | Date | Change | Why |
|---|---|---|---|
