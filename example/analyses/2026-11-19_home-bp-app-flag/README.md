# 2026-11-19_home-bp-app-flag

**Synthetic example.** Does an app's "Stage 1 Hypertension" label hold up?

| File | What | Read |
|---|---|---|
| `brief.md` | The owner's brief, hypothesis written before the data | 1st |
| `plan.md` | Phases 0 to 3 and the owner overview as approved, then a dated Revision 1 with every change made after the result | 2nd |
| `analysis.py` | The script; `--check` reruns and compares | |
| `reanalysis.md` | Ten sections: how to reach the same numbers | 3rd |
| `review.md` | Independent review by a separate session | 4th |
| `conclusion.md` | The one page the owner reads | Start here if you only read one |

Data output: `example/data-folder/analyses/2026-11-19_home-bp-app-flag/results.csv`.

**Note on `review.md`:** the reviewers cite git objects (for example `b8e8814b` for the
approved plan and `647abcba` for the first `results.csv`) from before the repository's
first commit. They are not in the published history. The approved plan survives
verbatim as the first part of `plan.md`, and the first `results.csv` equals the current
one minus the row `highest_diastolic_reading`.
