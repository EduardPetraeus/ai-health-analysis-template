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
| Brief | The owner wrote their hypothesis ("the app is right") and what would change their mind ("a proper week's average clearly below the home threshold") **before** any data were opened |
| Semantics | The app has no data dictionary. The label was decoded on the data: it applies **office** cut points to **each single reading** (81 of 81 matched) |
| Knowledge | Guidelines define categories on **averages** of properly taken readings, and **home** thresholds differ from office ones (135/85 vs 140/90 in Europe) |
| Data quality | Two identical duplicate rows and one "cuff loose" reading were found when describing the file, preregistered in the plan, and asserted by the script |
| Result | Proper week average 125.5/78.4, whole 95 % interval below the home hypertension threshold of 135/85, in the European *elevated* range. Still, 40 of 53 everyday readings got a Stage 1 or 2 label |
| Honesty | The US home equivalents were not verified, so they are written as a gap and not used. The overall risk could not be estimated, so the analysis sends the owner to a clinician for it (trigger T7) rather than waiting |
| Review | Separate review sessions reran everything. Round 1 found five problems of meaning and method. Round 2 caught the executor rewriting the approved plan after the result without saying so; the plan was restored and the changes moved to a dated revision |

## Read it in this order

1. [`analyses/2026-11-19_home-bp-app-flag/brief.md`](analyses/2026-11-19_home-bp-app-flag/brief.md)
2. [`analyses/2026-11-19_home-bp-app-flag/plan.md`](analyses/2026-11-19_home-bp-app-flag/plan.md)
3. [`semantics/sources/home-bp-app/reading.md`](semantics/sources/home-bp-app/reading.md): how the label was decoded
4. [`analyses/2026-11-19_home-bp-app-flag/reanalysis.md`](analyses/2026-11-19_home-bp-app-flag/reanalysis.md)
5. [`analyses/2026-11-19_home-bp-app-flag/review.md`](analyses/2026-11-19_home-bp-app-flag/review.md)
6. [`analyses/2026-11-19_home-bp-app-flag/conclusion.md`](analyses/2026-11-19_home-bp-app-flag/conclusion.md): the one page the owner reads

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
included; `status/health-status.md`, which the brief points to, is left out.

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
