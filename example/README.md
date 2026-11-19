# Example: the app says "Stage 1 Hypertension"

**Synthetic data, real method, real sources.** No real person's data is used anywhere in
this folder. Not medical advice.

> The findings belong to a fictional app and a fictional person. Your app may label
> readings differently. Reuse the method, never the results.

## The story

A person's blood pressure app labels most of their readings *Stage 1 Hypertension*.
They are worried and believe the app. Before booking a doctor, they run one analysis
with this template.

The method does not ask "is the app right?". It asks **what the label rests on**: which
definition, which threshold, applied to which kind of measurement.

## What the method found

| Step | What happened |
|---|---|
| Brief | Safety questions first. Then the owner wrote their hypothesis ("the app is right") and what would change their mind before the data were analysed |
| Semantics | The app has no data dictionary. The label was decoded on the data: it applies the US stage cut points to **each single reading** (81 of 81 matched) |
| Knowledge | Guidelines apply categories to an **average** of properly taken readings. The European home threshold is 135/85; the US one is 130/80 |
| Data quality | Two identical duplicate rows and one "cuff loose" reading were found when describing the file, and the script asserts both counts |
| Result | Proper week average 125.5/78.4. Below the European home threshold; unresolved against the US one, because the diastolic interval reaches 80.7 |
| Honesty | The answer depends on the guideline, and the overall risk could not be estimated, so the conclusion lists questions for a clinician instead of giving advice |
| Review | Separate review sessions on another model reran everything. One caught the AI rewriting its approved plan after the result; an external review caught that the first version had the US home threshold wrong. Both are fixed; the history is in git |

## Read it in this order

1. [`analyses/2026-11-19_home-bp-app-flag/conclusion.md`](analyses/2026-11-19_home-bp-app-flag/conclusion.md): the one page the owner reads
2. [`analyses/2026-11-19_home-bp-app-flag/brief.md`](analyses/2026-11-19_home-bp-app-flag/brief.md)
3. [`analyses/2026-11-19_home-bp-app-flag/plan.md`](analyses/2026-11-19_home-bp-app-flag/plan.md)
4. [`semantics/sources/home-bp-app/reading.md`](semantics/sources/home-bp-app/reading.md): how the label was decoded
5. [`analyses/2026-11-19_home-bp-app-flag/reanalysis.md`](analyses/2026-11-19_home-bp-app-flag/reanalysis.md)
6. [`analyses/2026-11-19_home-bp-app-flag/review.md`](analyses/2026-11-19_home-bp-app-flag/review.md)

## Run it yourself

From the repository root, Python 3.9 or later, nothing to install:

```bash
python3 example/data-folder/home-bp-app/generate.py --check
python3 example/analyses/2026-11-19_home-bp-app-flag/analysis.py
```

The first proves the synthetic export matches its generator. The second prints every
number in the conclusion.

## What is in this folder

It mirrors a real copy of the template, in miniature. Only files the example touches are
included.

| Path | Mirrors |
|---|---|
| `data-folder/` | Your data folder, which in real use lives **outside** the repository |
| `semantics/` | `semantics/` |
| `knowledge/` | `knowledge/` |
| `analyses/` | `analyses/` |
| `status/` | `status/`, showing only the flag row the analysis added |
| `results.md` | `results.md` |

## For an AI walking someone through this

Walk the owner through the files in the order above, one at a time. At each step, point
out which rule from [METHOD.md](../METHOD.md) it shows, and ask whether they want to go
on. End by offering to start their own first analysis with
[`templates/brief.md`](../templates/brief.md).
