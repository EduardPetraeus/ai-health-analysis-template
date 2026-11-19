# METHOD: how every analysis is done

**Mandatory for every analysis in this folder.** If a skill, a prompt or another file
disagrees with this file, this file wins and the other one is out of date.

**The core rule: a number without a written method is not a result. It is a claim.**

Every analysis leaves a folder from which another session, with no access to the
conversation where it was made, can reach the same numbers.

Words that may be new are explained in [GLOSSARY.md](GLOSSARY.md).

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

## 3. Phase 0: the brief, safety and the hypothesis

**No analysis starts, not even phase 1, before the brief is filled in.** Template:
[`templates/brief.md`](templates/brief.md).

**Safety comes first.** The brief asks about new symptoms, pregnancy, age under 18,
known diagnoses, medication, and any single value the owner has already seen marked as
very high or alarming, before anything else. New or worrying symptoms, or a pregnancy,
stop the analysis: the AI advises contacting a clinician, or emergency services if it
feels urgent. An alarming value the owner has seen is checked against the T1 alarm limit
at once (§ 9), before the brief continues. The other answers decide whether published
thresholds apply to the owner at all.

The brief is the owner's half of the method. The AI may interview the owner through it,
with one rule that protects the whole analysis:

> **The owner writes the hypothesis (field 8) and what would change their mind (field 9)
> in their own words, before anyone opens the data values, and before the AI suggests
> anything.** After the owner has answered, the AI may sharpen it; the plan says which
> words are the owner's.

The plan then turns the brief into:

| Field | Requirement |
|---|---|
| **Hypothesis** | A statement that can turn out wrong. Not a topic |
| **Decision rule** | Three outcomes, each with numbers: supported, rejected, inconclusive. Say whether "and" or "or" joins two values (systolic and diastolic, for example) |
| **Primary endpoint** | **One** measure the decision rests on |
| **Secondary endpoints** | Everything else. They can never carry a conclusion alone |
| **Kind of analysis** | *Confirmatory* only if the owner has not seen the data the endpoint is computed from. If they have, it is *retrospective with a preregistered plan*. *Exploratory* results generate hypotheses and decide nothing |
| **Which guideline applies** | The owner's country and their clinician's guideline, if known. If unknown, the plan names every guideline it compares against, before the data are opened |

Why first and not last: a hypothesis written after the results is a rationalization
(HARKing, *hypothesizing after results are known*). Promoting whatever looked interesting
to the main finding afterwards is outcome switching. Both are prevented only by writing
things down before measuring, and by being able to prove when it was written:

> **Preregistration is two commits.** The brief is committed as soon as fields 8 and 9
> are written, before any data value is opened. The approved plan is committed after the
> owner's ok, before anything the decision rule judges is computed. `reanalysis.md` § 9
> records both commits. Without git, a SHA256 hash of each file is written to its last
> line and repeated in § 9.

## 4. Source agreement

An AI may never choose the data on its own and start computing. The order is:

1. **Find the sources** and list them: path, fields, date range, row count.
2. **Show the list to the owner** with what each will be used for.
3. **Ask about known gaps,** one question per message, recommended answer first. The owner
   knows things about their data that are written nowhere: a device that was replaced, a
   habit that was removed from an app, a week of illness.
4. **Only then compute.**

When sources disagree, the trust order in [DATA.md § 3](DATA.md#3-trust-order) decides.

## 5. The five phases

Phase 0 is the brief (§ 3); phases 1 to 5 follow, in order. The owner's "ok" to the plan
approves phases 0 to 3 together, after the owner has answered the plan's questions.

**When data may be read.** Three steps, in this order:

1. **Until the brief is committed** (§ 3): only column headers (`head -1 <file>`).
2. **After the brief commit, before the ok:** the data may be described but not judged.
   First find the T1 alarm limits with their source (§ 9), or write that none exist.
   Then tell the owner what will be read and why, in one line, and read it. Row counts,
   date range, distinct codes, duplicates and gaps are allowed. Anything the decision
   rule will judge (a mean, a rate, a comparison with a threshold) is not.
3. **After the ok and the plan commit:** phases 4 and 5.

**Reading any value column counts as opening values,** distinct codes and app labels
included. From that moment every single value is checked against the T1 alarm limits.

**A T1 hit ends computation in this analysis.** The AI shows the values, quotes what the
limit's source says to do, and stops. It does not offer to continue, and it computes no
average or other summary, even if the owner asks; the owner cannot approve continuing
past T1 ([ROLES.md § 3](ROLES.md#3-what-only-the-owner-approves)). A new analysis may
start once the step the source names has happened, for example measuring again or
seeing a clinician, and its brief records that step. If the owner reports symptoms, T6
applies as well.

| Phase | Content | Output |
|---|---|---|
| **1. Scientific ground truth** | Thresholds and reference values, each with a citation (title, source, year, link) and a note on whether it was opened and read. Does the population behind it match the owner? Yes, no or unknown. If the AI cannot open sources, the reviewer must open each one | Sources table in the plan |
| **2. Data manifest and source criticism** | Exact paths and fields. Justify source choice. Report gaps, missing timestamps and odd patterns at the same level as findings | Manifest in the plan |
| **3. Method** | How the decision rule is computed. Statistical method and its assumptions, minimum data for a valid result, how incomplete days are handled, exclusions, how sensitive the answer is to measurement error | Method in the plan |
| | **🛑 STOP.** No calculation and no conclusion until the owner approves the plan, and the commit (§ 3) exists | Owner's "ok" |
| **4. Execution** | A commented script, saved in the analysis folder, that can be rerun unchanged on new data. Data outputs go to the data folder, never the repository | `analysis.py` |
| **5. Documentation** | `reanalysis.md` written *while* working, then `conclusion.md` | Folder complete |

If the method cannot decide the hypothesis, the method is wrong, or the hypothesis must be
cut down. That happens in phase 3, not afterwards. **A change to the approved method goes
back to the owner** and is recorded in `reanalysis.md` § 9 with the commit that made it.

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
   *documented*.
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
   applied to which kind of measurement, and to one reading or an average) before
   comparing anything to it.

Concepts and where each kind of knowledge lives: [`semantics/CONCEPTS.md`](semantics/CONCEPTS.md).

## 7. Evidence standards

These have each cost a real error at least once.

1. **A negative statement needs a positive control.** A search that finds nothing proves
   nothing until you have seen the same search find something you know is there. Run the
   control in the same step and write both results down. "No X found" without a control is
   a gap, not a finding. Helper: `tools/extract_checks.py → grep_with_positive_control`.
2. **Validate before writing; fail hard, never write half.** Check expected row count (as
   a deliberate constant), duplicate keys, plausible ranges and column swaps *before* the
   first byte is written, and raise an error rather than print a warning. Helper:
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
8. **State the uncertainty, and allow "unresolved".** Give the interval and name the
   uncertainties it does not cover (device error, one measurement period, a population
   that may not match). Never translate a 95 % interval into "95 % sure". "Unresolved" is
   a valid main answer when the decision rule lands there.

## 8. The analysis folder

One folder per analysis: `analyses/YYYY-MM-DD_<topic>/`, dated the day the analysis
started.

| File | Content | Template |
|---|---|---|
| `README.md` | Index of the folder, the question in one line, status | |
| `brief.md` | The owner's brief | [brief](templates/brief.md) |
| `plan.md` | Phases 0 to 3, approved by the owner | [plan](templates/plan.md) |
| `analysis.py` | The script, rerunnable unchanged | |
| `reanalysis.md` | Ten sections: how to reach the same numbers from scratch | [reanalysis](templates/reanalysis.md) |
| `review.md` | The independent review, with commands and outputs | [review](templates/review.md) |
| `conclusion.md` | The one page the owner reads | [conclusion](templates/conclusion.md) |

### One truth per file

**Every file shows only the current truth.** No struck through text, no old and new
versions side by side, no revision tables. Git holds the history: the commit message
says what changed and why, and `git log` shows the rest. Two versions of the same text in
one repository confuse every reader, human or AI.

What git cannot show by itself is written as facts in `reanalysis.md` § 9: the two
commits that preregistered the brief and the plan, and the commits that changed the plan
or the answer after that. One line each.

### `reanalysis.md` is written while working, not afterwards

Written afterwards, it documents what you remember, not what you did. The test: another
session reading **only** this file reaches the same numbers.

### `conclusion.md` is one page

At most about 400 words, tables not counted. Tables are tall and narrow (at most three
columns) so they read on a phone. **It starts with an answer the owner could repeat to a
clinician in one everyday sentence.** Method words (trigger numbers, interval names)
belong in `reanalysis.md`; the conclusion names a fired trigger in plain words.
**Section 5, "What this does NOT answer", is never left out.** The conclusion describes
what the comparison shows and lists questions to take to a clinician. It gives no
advice, deadlines or urgency that are not quoted from a cited source.

**The conclusion is written before the review,** so the review checks it like every other
file: each number and each counted claim in it against a command output.

### Analyses do not depend on living files

`status/` files change; an analysis must still make sense later.

1. An analysis may reference raw data, literature, its own files and other analyses.
2. If it needs a value from a `status/` file (height, a start date), it **copies the
   value in, with source and date**.
3. The test: *could this sentence become untrue if the living file changes?* If yes, it
   is a forbidden dependency. Naming `status/follow-up.md` as the place where a flag is
   tracked is fine, as long as nothing from it is repeated.

### Count every comparison

`reanalysis.md` § 9 states **how many** values were held against a reference, all of
them: single readings against alarm limits, averages against categories, every
sensitivity variant. Hold 35 markers against reference intervals and some fall outside by
chance alone. That is arithmetic, not a finding. Name which comparisons decide the answer.

---

## 9. Escalation triggers, written before the result

"Only if it is critical" is not a threshold; it is a mood, and a mood drifts toward not
acting. The list below is checked for every analysis and the result written out. A trigger
that cannot be checked is written as "could not be checked" with the reason, never as
"not fired".

| # | Trigger | What to do |
|---|---|---|
| T1 | A value crosses a **published alarm limit** | Computation ends (§ 5). Exactly what the limit's source says to do, quoted. No offer to continue; the owner cannot approve continuing. Checked on every value as soon as any value is read |
| T2 | A guideline names the finding as an **indication for referral** or further workup | Take it to a clinician, with the guideline named |
| T3 | The same marker moves the wrong way over **at least three independent measurements**, by more than its documented variation | Take it to a clinician. Without a sourced figure for the variation: could not be checked |
| T4 | A **combination** of markers that a guideline names as a pattern needing assessment | Take it to a clinician, with the guideline named |
| T5 | The question **cannot be closed without a test only a clinician can order** | Take it to a clinician |
| T6 | The owner reports **new or worrying symptoms** at any point | Stop the analysis. Advise contacting a clinician, or emergency services if it feels urgent |
| T7 | **The analysis cannot tell whether the finding matters for the owner's health** | Take it to a clinician |

Rules:

1. **Limits are never invented.** Phase 1 finds each limit **with source and link**, or
   writes that none exists. Where possible, alarm limits come from the same guideline as
   the categories.
2. **No urgency without a source.** "Take it to a clinician" carries no deadline unless a
   cited source gives one.
3. **No trigger fired does not mean the value is unimportant.** Every conclusion says so:
   this method cannot rule out disease.
4. The list, and the plan's handling of a trigger, may not be edited in a session that
   has seen a result that would trigger it.

## 10. Flags

A value outside its reference, in the average or the most recent measurements, is a
flag. A single old outlier that is neither is history, not a flag. Every flag is written
in **both** `conclusion.md` § 6 and a row in `status/follow-up.md`, because a flag that
lives only in an analysis folder is never followed up.

| Status | Meaning |
|---|---|
| `NEW` | Registered, not yet reviewed with the owner |
| `REVIEWED` | Reviewed, decision made |
| `MONITOR` | Measure again; **must have a review date** chosen by the owner or a cited source |
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

- [ ] Brief filled in, safety questions answered, hypothesis and field 9 in the owner's
      words before data values were opened
- [ ] Brief committed before data values were opened, plan committed after the ok and
      before any judged calculation; both commits in `reanalysis.md` § 9
- [ ] Plan approved by the owner before any calculation
- [ ] Every field used is documented in `semantics/`, or marked undocumented and not used
      for conclusions
- [ ] Every number meets the five requirements (§ 2), denominator written into the number
- [ ] Statistical assumptions written in `reanalysis.md` § 4, sensitivity to measurement
      error stated
- [ ] `reanalysis.md` has all ten sections; § 8 has a link per external claim and says
      whether each source was opened; § 9 counts every comparison
- [ ] No dependency on a living file (§ 8)
- [ ] Escalation triggers T1 to T7 checked and written out in `reanalysis.md` (§ 9); after
      a T1 hit, nothing was computed
- [ ] Every flag in both `conclusion.md` § 6 and `status/follow-up.md` (§ 10)
- [ ] Negative statements have a positive control or stand as gaps (§ 7)
- [ ] Review done by a separate session that reran the analysis and checked every number
      in `conclusion.md`, at every level, and the last review is green and committed
      ([ROLES.md § 4](ROLES.md#4-review))
- [ ] `conclusion.md` within one page, section 5 filled in, no advice or urgency without a
      cited source
- [ ] Every file shows one truth: no struck through text, no old versions (§ 8)
- [ ] One row in [`results.md`](results.md)
- [ ] New general knowledge in `knowledge/`, new semantics in `semantics/`, each with
      sources
- [ ] Every new file listed in its folder's README; `python3 tools/check.py` passes
- [ ] Learning candidates proposed to the owner ([learnings.md](learnings.md))

## 13. Changing the method

Files show the current rule only; git keeps the history, and the commit message says what
changed and why. A rule that should trigger an action needs a number, a date or a list,
or it is not finished. Patterns worth remembering go through
[learnings.md](learnings.md), which decides whether they become a rule here.

## 14. Standards this method draws on

The rules above borrow from established research practice. They do not make an analysis
compliant with any of these standards.

| Standard | What it contributes here | Link |
|---|---|---|
| **EQUATOR Network** | Reporting guidelines: what a report should contain. Closest fit for these self analyses: observational reporting (STROBE style items such as missing data and bias) | [equator-network.org](https://www.equator-network.org/reporting-guidelines/) |
| **CENT** | Reporting of planned N of 1 *trials* (randomized crossover periods). It applies only if an analysis is set up as such a trial; most analyses here are observational | [CENT 2015](https://www.equator-network.org/reporting-guidelines/consort-cent/) |
| **TOP Guidelines** | A policy framework for transparency: registration, analysis plan, data and code transparency, reproducibility | [Center for Open Science](https://www.cos.io/initiatives/top-guidelines) |
| **GRADE** | Rating certainty of a whole body of evidence per outcome. Used here only as inspiration; a single source is described by type and by how directly it was read | [GRADE](https://www.cochrane.org/learn/courses-and-resources/cochrane-methodology/grade) |

The two commits of brief and plan act as a preregistration. `reanalysis.md` § 7 is
reproduction (same data, same answer); § 10 is replication (new data, does it still
hold?).
