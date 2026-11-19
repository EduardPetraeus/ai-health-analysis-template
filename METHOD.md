# METHOD: how every analysis is done

**Mandatory for every analysis in this folder.** If a skill, a prompt or another file
disagrees with this file, this file wins and the other one is out of date.

**The core rule: a number without a written method is not a result. It is a claim.**

Every analysis leaves a folder from which another session, with no access to the
conversation where it was made, can reach the same numbers.

---

## 1. Why the rules exist

Files are memory, not truth. A session reading a number cannot see how it was computed,
which period it covers or what was left out. Without that, the number can neither be
checked nor defended, and it gets copied into new files anyway, looking more certain with
every copy.

A typical case: a habit log shows **27 of 28 logged days (96 %)**. Traced back to the raw
log, the period turns out to be **35 calendar days**, seven of them with no entry at all.
Counted that way it is **27 of 35 days (77 %)**. Both numbers are correct. Which one
answers the question depends entirely on the denominator, and the data cannot say whether
the seven silent days were days without the habit or days without logging. If the method
is not written down, nobody can tell which number they are looking at.

## 2. Five requirements for every number

Every number, percentage, average or test result in an analysis has:

| # | Requirement | Example |
|---|---|---|
| 1 | **Source:** file or table **and field** | `home-bp-app/raw/export.csv → systolic`, not "my app" |
| 2 | **Numerator and denominator** defined | `27/35 calendar days (77 %)`, not `77 %` |
| 3 | **Date range** as real dates | `2026-09-01 to 2026-10-05`, not "five weeks" |
| 4 | **What was left out, and why** | deleted rows, days without data, test entries, outliers |
| 5 | **Date of calculation** | data grows; yesterday's number does not cover today |

Write the denominator into the number itself. Tables must read without the prose, and the
prose without the tables.

**A field that does not apply is written out, never left as `—` or `n/a`.** An empty field
cannot be told apart from a forgotten one. Write *why* it does not apply: "No denominator.
This is a single reading of one lab value, not a count."

---

## 3. Phase 0: the brief and the hypothesis

**No analysis starts, not even phase 1, before the brief is filled in.** Template:
[`templates/brief.md`](templates/brief.md).

The brief is the owner's half of the method. The AI may interview the owner through it,
with one rule that protects the whole analysis:

> **The owner writes the hypothesis (field 7) and what would change their mind (field 8)
> in their own words, before anyone looks at the data, and before the AI suggests
> anything.** After the owner has answered, the AI may sharpen it, and both versions are
> kept.

The plan then turns the brief into:

| Field | Requirement |
|---|---|
| **Hypothesis** | A statement that can turn out wrong. Not a topic |
| **Null hypothesis** | What "nothing to see here" would look like in the numbers |
| **Primary endpoint** | **One** measure the conclusion stands or falls on |
| **Secondary endpoints** | Everything else. They can never carry a conclusion alone |
| **Exploratory or confirmatory** | Exploratory results generate hypotheses; they decide nothing |
| **Owner's expectation** | Copied verbatim from the brief |
| **Falsification** | A concrete observation that would overturn the conclusion |

Why first and not last: a hypothesis written after the results is a rationalization
(HARKing, *hypothesizing after results are known*). It is not dishonesty; it is how memory
works. Promoting whatever looked interesting to the main finding afterwards is
outcome switching. Both are prevented only by writing things down before measuring.

An exploratory analysis is allowed, but it must say so, and its findings stay
hypotheses.

## 4. Source agreement

An AI may never choose the data on its own and start computing. The order is:

1. **Find the sources** and list them: path, fields, date range, row count.
2. **Show the list to the owner** with what each will be used for.
3. **Ask about known gaps.** The owner knows things about their data that are written
   nowhere: a device that was replaced, a habit that was removed from an app, a week of
   illness.
4. **Only then compute.**

When sources disagree, the trust order in [DATA.md § 3](DATA.md#3-trust-order) decides.

## 5. The five phases

Phase 0 is the brief and hypothesis (§ 3); phases 1 to 5 follow. Run in order. The
owner's "ok" to the plan approves phases 0 to 3 together, after the
owner has answered the plan's questions about the data.

**What may happen before the ok, and what may not.** Describing the data is allowed and
belongs in phase 2: row counts, date range, column names, distinct codes, duplicates,
gaps. Computing anything the hypothesis will be judged on (a mean, a rate, a comparison
with a threshold) is not. And for a new analysis, nobody opens data values before the
owner has written brief fields 7 and 8; column headers are fine.

| Phase | Content | Output |
|---|---|---|
| **1. Scientific ground truth** | Find reference values and thresholds, each with a specific citation (title, source, year, link). Ask: was this threshold derived in a population like the owner? | Sources table in the plan |
| **2. Data manifest and source criticism** | Exact file paths and fields. Justify source choice. Report gaps, missing timestamps and odd patterns at the same level as findings | Manifest in the plan |
| **3. Method** | Restate the hypothesis verbatim and how the method decides it. Statistical methods, exclusions, the primary endpoint. Questions for the owner | Method in the plan |
| | **🛑 STOP.** No code, no calculation, no conclusion until the owner approves the plan | Owner's "ok" |
| **4. Execution** | A fully commented script, saved in the analysis folder, that can be rerun unchanged on new data. Data outputs go to the data folder, never the repository | `analysis.py` |
| **5. Documentation** | `reanalysis.md` written *while* working, then `conclusion.md` | Folder complete |

If the method cannot decide the hypothesis, the method is wrong, or the hypothesis must be
cut down. That happens in phase 3, not afterwards.

**A change to the approved method goes back to the owner.** Smaller deviations are
allowed if they are written down with the old wording, the new wording and the reason.

---

## 6. Semantics before numbers

**No field is used in an analysis before its meaning is documented.** A model that only
has column names and values guesses, and a correct number with the wrong meaning ruins an
analysis just as surely as a wrong number.

1. **Where a definition may come from, in this order:**
   1. the export's own description (a README in the export, column headers with units);
   2. the provider's official documentation;
   3. peer reviewed validation studies.

   Not forums, blogs, third party libraries or AI answers. If the provider is unknown or
   publishes nothing, a field's meaning may be **decoded on the data** (state the rule you
   suspect, test it on every row, report the match count) and marked *partial*, never
   *documented*. The example decodes an app's label this way.
2. **"Undocumented" is a valid answer** and better than a guess. An undocumented field is
   not used for conclusions.
3. **An export is not an API.** The same object can arrive with different field names,
   units or rounding in different deliveries. A mapping between them is verified on data
   before it is trusted.
4. **Every source and object has one file** in `semantics/sources/`, built from
   [`templates/source.md`](templates/source.md) and
   [`templates/object.md`](templates/object.md). A field missing from the catalog is
   added before it is used.
5. **Labels from apps and tests are semantics too.** "Stage 1", "dysbiosis", "poor
   recovery": find the definition behind the label (which guideline, which threshold,
   applied to which kind of measurement) before comparing anything to it.

Concepts and where each kind of knowledge lives: [`semantics/CONCEPTS.md`](semantics/CONCEPTS.md).

## 7. Evidence standards

These have each cost a real error at least once.

1. **A negative statement needs a positive control.** A search that finds nothing proves
   nothing until you have seen the same search find something you know is there. Run the
   control in the same step and write both results down. "No X found" without a control is
   a gap, not a finding. Helper: `tools/extract_checks.py → grep_with_positive_control`.
2. **Validate before writing; fail hard, never write half.** A half extract that looks
   complete is worse than none. Check expected row count (as a deliberate constant),
   duplicate keys, plausible ranges and column swaps *before* the first byte is written,
   and raise an error rather than print a warning. Helper:
   `tools/extract_checks.py → validate_extract`.
3. **A parsed extract is a claim about the source, not the source.** Spot check it
   against the raw file with a different tool than the one that made it.
4. **Unknown is not zero.** Missing records mean unknown. A habit log stops when the habit
   is removed from the app, while the behavior may continue.
5. **Document date is not event date.** For every date taken from a file, ask: is this
   when it happened, or when it was written? An approximate date ("end of May") is never
   turned into an exact day.
6. **Search discipline.** Case insensitive (`-i`), real alternation (`grep -E "a|b"`, not
   `\|`), whole folder, not just the subfolder you work in.
7. **Units travel with values.** Read the unit from the report row and store it next to
   the value. The same marker is reported in different units by different labs.
8. **Conclude on probability.** Answer with what the data show and how likely the
   opposite is. A limitation of the method is written next to the answer, not used as a
   reason to leave the question open.

## 8. The analysis folder

One folder per analysis: `analyses/YYYY-MM-DD_<topic>/`, dated the day the analysis
started.

| File | Content | Template |
|---|---|---|
| `README.md` | Index of the folder's files, the question in one line, status, and which sessions worked on it | |
| `brief.md` | The owner's brief, never edited after the plan is approved | [brief](templates/brief.md) |
| `plan.md` | Phases 0 to 3, approved by the owner | [plan](templates/plan.md) |
| `analysis.py` | The script, rerunnable unchanged | |
| `reanalysis.md` | Ten sections: how to reach the same numbers from scratch | [reanalysis](templates/reanalysis.md) |
| `review.md` | The independent review, with commands and outputs | [review](templates/review.md) |
| `conclusion.md` | The one page the owner reads | [conclusion](templates/conclusion.md) |

### `reanalysis.md` is written while working, not afterwards

Written afterwards, it documents what you remember, not what you did. The test: another
session reading **only** this file reaches the same numbers.

### `conclusion.md` is one page

At most about 400 words, tables not counted. Tables are tall and narrow (at most three
columns) so they read on a phone. **Section 5, "What this does NOT answer", is never left
out.** Without it a conclusion grows more certain every time it is quoted.

### Frozen result, living action

An analysis is a frozen snapshot. `status/` files are living. **References only go from
living to frozen, never the other way.**

1. An analysis may reference raw data, literature, its own files and other analyses.
2. An analysis may not depend on a living file. If it needs a value from one (height, a
   start date), it **copies the value in, with source and date**.
3. The test: *could this sentence become untrue if the living file changes?* If yes, it
   is a forbidden dependency.
4. Naming a living file as the place where follow up happens ("the flag is tracked in
   `status/follow-up.md`") is allowed, as long as nothing from that file is repeated.

In `conclusion.md`, sections 1 to 5 and 8 are frozen. The flag status in section 6 and
the next steps in section 7 may be updated, with a dated revision note at the top. A
change to the answer itself is a new analysis.

### Multiplicity

When more than one number is held against a reference, `reanalysis.md` § 9 states **how
many**. Hold 35 markers against reference intervals and some fall outside by chance
alone. That is arithmetic, not a finding.

---

## 9. Escalation triggers, written before the result

"Only if it is critical" is not a threshold; it is a mood, and a mood drifts toward not
acting. The list below is checked for every analysis and the result written out. **No
flags is also a result.** A trigger that cannot be checked is written as "could not be
checked: no data", never as "not triggered".

| # | Trigger | Level |
|---|---|---|
| T1 | A value crosses a **published alarm limit** from the lab or a guideline | 🔴 Contact a clinician now |
| T2 | A guideline names the finding as an **indication for referral** or further workup | 🟠 Book a clinician |
| T3 | The same marker moves the wrong way over **at least three independent measurements**, beyond known variation | 🟠 Book a clinician |
| T4 | A **combination** of markers that a guideline names as a pattern needing assessment | 🟠 Book a clinician |
| T5 | The question **cannot be closed without a test only a clinician can order** | 🟠 Book a clinician |
| T6 | The owner reports **new symptoms** | Stop the analysis; advise contacting a clinician, emergency services if urgent |
| T7 | **The analysis cannot tell whether the finding is dangerous** | 🟠 Book a clinician |

Thresholds are never invented. Phase 1 finds the concrete limit **with source and link**
for each marker, or writes that none exists. **T7 is the honest counterweight:** if the
risk cannot be bounded, that is a reason to escalate, not to wait.

The list may not be edited in a session that has seen a result that would trigger it.

## 10. Flags

A value outside its reference, in the average or the most recent measurements, is a
flag. A single old outlier that is neither is history, not a flag. Every flag is written
in **both** `conclusion.md` § 6 and a row in `status/follow-up.md`, because a flag that
lives only in a frozen analysis is never followed up.

| Status | Meaning |
|---|---|
| `NEW` | Registered, not yet reviewed with the owner |
| `REVIEWED` | Reviewed, decision made |
| `MONITOR` | Measure again; **must have a review date** |
| `CLOSED` | Not a finding; reason written |
| `ESCALATED` | A trigger in § 9 fired |

A flag leaves the list in exactly three ways: moved to *known observations* in
`status/health-status.md`, turned into a measurement wish, or closed with a reason. An
analysis establishes an observation, never a diagnosis.

A **reference interval** (where 95 % of a healthy population falls) and a **decision
limit** (a threshold tied to an outcome) are different objects. Keep them in separate
fields.

## 11. Large analyses: waves

An analysis too large for one session is split into **waves**, one subfolder each
(`w1-<domain>/`). The plan names every wave before the first starts. A wave writes only in
its own subfolder and never concludes across waves; a final consolidation step owns the
root files.

---

## 12. Closing checklist

An analysis is closed when every line is checked. A line that cannot be met is marked
`❌` with a pointer to where it is explained. **There is no `n/a`.** Every checklist with an
escape hatch degrades into the escape hatch.

- [ ] `brief.md` filled in before the data were opened; hypothesis in the owner's words
- [ ] `plan.md` approved by the owner before any calculation
- [ ] Every field used is documented in `semantics/`, or marked undocumented and not used
      for conclusions
- [ ] Every number meets the five requirements (§ 2), denominator written into the number
- [ ] `reanalysis.md` has all ten sections; § 8 has a clickable link per external claim;
      § 9 has the hypothesis verbatim and the number of metrics examined
- [ ] No dependency on a living file (§ 8)
- [ ] Escalation triggers T1 to T7 checked and written out (§ 9)
- [ ] Every flag in both `conclusion.md` § 6 and `status/follow-up.md` (§ 10)
- [ ] Negative statements have a positive control or stand as gaps (§ 7)
- [ ] Review done by a separate session that reran the analysis, at every level
      ([ROLES.md § 4](ROLES.md#4-review))
- [ ] `conclusion.md` within one page, section 5 filled in
- [ ] One row in [`results.md`](results.md)
- [ ] New general knowledge in `knowledge/`, new semantics in `semantics/`, each with
      sources
- [ ] Every new file listed in its folder's README; `python3 tools/check.py` passes
- [ ] Learning candidates proposed to the owner ([learnings.md](learnings.md))

## 13. Changing the method

Corrections are never silently overwritten. Git keeps history; the commit message says
what changed and why. A rule that should trigger an action needs a number, a date or a
list, or it is not finished. Patterns worth remembering go through
[learnings.md](learnings.md), which decides whether they become a rule here.

## 14. Standards this method implements

The rules above were not invented in this folder. They draw on:

| Standard | What it contributes | Link |
|---|---|---|
| **EQUATOR Network** | Reporting guidelines: what a report must contain | [equator-network.org](https://www.equator-network.org/reporting-guidelines/) |
| **CENT** (CONSORT extension for N of 1 trials) | Reporting single person studies | [CENT 2015](https://www.equator-network.org/reporting-guidelines/consort-cent/) |
| **TOP Guidelines** | Transparency: preregistration, data, code, replication | [TOP](https://www.apa.org/pubs/journals/resources/publishing-tips/transparency-openness-promotion-guidelines) |
| **GRADE** | Rating the certainty of evidence | [GRADE](https://www.cochrane.org/learn/courses-and-resources/cochrane-methodology/grade) |

The brief and the approved plan act as a preregistration. `reanalysis.md` § 7 is
reproduction (same data, same answer); § 10 is replication (new data, does it still
hold?).
