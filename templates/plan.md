# Plan · <YYYY-MM-DD_topic>

*Written by the planner from `brief.md`. Covers phases 0 to 3 (`METHOD.md § 5`). Ends
with a short overview for the owner and then **stops**. Anything the planner proposes
that the owner has not yet decided is marked* (proposed) *until the owner's ok.*

**Brief:** [`brief.md`](brief.md) · **Status:** draft / approved YYYY-MM-DD by the owner

## 0. Hypothesis and decision rule

| Field | Content |
|---|---|
| Owner's hypothesis (verbatim, brief field 8) | |
| Owner's falsification (verbatim, brief field 9) | |
| Hypothesis as tested | |
| Decision rule: supported | *numbers; say "and" or "or"* |
| Decision rule: rejected | |
| Decision rule: inconclusive | |
| Primary endpoint (one) | |
| Secondary endpoints | |
| Kind of analysis | confirmatory / retrospective with preregistered plan / exploratory, and why |
| Guidelines compared against | *from brief field 10. If the owner does not know, every relevant guideline, European and US at least, each with its threshold for this kind of measurement* |

## 1. Scientific ground truth

| Claim or threshold | Source (title, year) | Type | Link | Opened and read? | Matches the owner? (yes, no, unknown) |
|---|---|---|---|---|---|

*Type: guideline · systematic review · RCT · observational study · position paper ·
expert statement · patient information.*

## 2. Data manifest

| Source and object | Path (relative to `data_path`) | Fields used | Period | Rows | Semantics documented? |
|---|---|---|---|---|---|

**Gaps and oddities found when describing the data:**

**Questions for the owner** (asked one at a time, recommended answer first, only those
whose answer could change the result; answers written here before the ok):

## 3. Method

*Step by step: filters, exclusions, aggregation, statistics. The assumptions behind the
statistics. Minimum data for a valid result and what happens with incomplete days. How
large a measurement error would change the answer. Free choices another analyst could
have made differently.*

**Expected results, preregistered:** *(row counts, which outputs will exist)*

**Escalation triggers:** *(T1 to T7, each with its sourced limit and what the source says
to do, or "no source found"; which cannot be checked and why. A T1 hit ends computation;
the plan never offers to continue past it, `METHOD.md § 5`)*

**Comparisons held against a reference:** *(count all of them, and name the ones that
decide the answer)*

## 4. Execution and review

- Script: `analysis.py` in this folder. Data outputs to `<data_path>/analyses/<name>/`.
- Review: who reviews (separate session, model) and what it reruns.
- Files this analysis may write: *(list)*. Files it may not touch: *(list)*.

## Overview for the owner

*Short, plain language, so "ok" is enough:*

- **What we are trying to find out:**
- **Your hypothesis, and how we test it:**
- **How we decide:** *the guideline's simple comparison (the average against the
  threshold) and this plan's stricter rule, if it has one, with what each says when the
  result lands close to the threshold*
- **Data we will use, and their weak spots:**
- **What this can NOT answer:**
- **What comes back to you:**

🛑 **Stop here until the owner says ok. Then commit `plan.md` before anything the decision
rule judges is computed. `brief.md` was committed when fields 8 and 9 were written
(`METHOD.md § 3`).**
