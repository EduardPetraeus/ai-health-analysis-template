# Plan · <YYYY-MM-DD_topic>

*Written by the planner from `brief.md`. Covers phases 0 to 3 (`METHOD.md § 5`).
Ends with a short overview for the owner and then **stops**.*

**Brief:** [`brief.md`](brief.md) · **Status:** draft / approved YYYY-MM-DD by the owner

## 0. Hypothesis and endpoints

| Field | Content |
|---|---|
| Owner's hypothesis (verbatim from brief field 7) | |
| Owner's falsification (verbatim from brief field 8) | |
| Hypothesis as tested (sharpened, if needed) | |
| Null hypothesis | |
| Primary endpoint (one) | |
| Secondary endpoints | |
| Exploratory or confirmatory | |

## 1. Scientific ground truth

| Claim or threshold | Source (title, year) | Type | Link | Population match |
|---|---|---|---|---|

*Type: guideline · systematic review · RCT · observational study · expert statement ·
popular science.*

## 2. Data manifest

| Source and object | Path (relative to `data_path`) | Fields used | Period | Rows | Semantics documented? |
|---|---|---|---|---|---|

**Gaps and oddities found:** *(listed at the same level as findings)*

**Questions for the owner about the data** (answered before the owner's ok; write the
answers here):

## 3. Method

*How the numbers are made, step by step: filters, exclusions, aggregation, statistics,
how the primary endpoint decides the hypothesis. Free choices another analyst could have
made differently.*

**Expected results, preregistered:** *(row counts, which outputs will exist, what the
endpoint will be compared against)*

**Escalation triggers:** *(which of T1 to T7 can apply here, and the sourced limit for
each, or "no source found")*

**Number of metrics that will be held against a reference:**

## 4. Execution and review

- Script: `analysis.py` in this folder. Data outputs to `<data_path>/analyses/<name>/`.
- Review: who reviews (separate session, model) and what it reruns.
- Files this analysis may write: *(list)*. Files it may not touch: *(list)*.

## Overview for the owner

*Short, plain language, so "ok" is enough:*

- **What we are trying to find out:**
- **Your hypothesis, and how we test it:**
- **Data we will use, and their weak spots:**
- **What this can NOT answer:**
- **What comes back to you:**

🛑 **Stop here until the owner says ok.**
