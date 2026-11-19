# ROLES: who does what, and what only the owner approves

## 1. The participants

| Role | Does | Never does |
|---|---|---|
| **Owner** (the person whose data it is) | Sets the direction in the brief, confirms which data to use, approves the plan, approves every change to `status/`, reads the conclusion | Needs to follow the details |
| **Planner** (an AI session) | Turns the brief into a plan for phases 0 to 3, documents semantics, gives the owner one clear overview to approve | Reviews its own plan |
| **Executor** (an AI session) | Runs phases 4 and 5 exactly as planned, writes `reanalysis.md` while working | Deviates from the plan without writing old wording, new wording and reason |
| **Reviewer** (a separate AI session) | Reruns the analysis and checks every claim against files ([§ 4](#4-review)) | Accepts a number it has not reproduced |

Under level 1 one session plays planner and executor. **The review is always a separate
session, at every level:** the owner opens a new chat and pastes the review prompt from
[README.md](README.md#5-have-it-reviewed).

## 2. Three levels

| Level | Setup | When |
|---|---|---|
| **1. Single chat** (default) | One session plans and executes; the owner approves the plan and reads the conclusion | Getting started, small questions |
| **2. Separate roles** (recommended) | Planner, executor and reviewer in separate sessions; the reviewer ideally on a different model | Anything the owner will act on |
| **3. Autopilot** (opt in) | A coordinating session drives the others and contacts the owner only when needed | Only when the owner switches it on: [`modules/autopilot/`](modules/autopilot/README.md) |

Nothing moves up a level unless the owner says so. The level is written in each brief.
When interviewing the owner for a brief, the AI recommends a level and, for level 2 and
3, which model runs which role, with a one line reason.

## 3. What only the owner approves

These never run on autopilot, at any level:

1. **The direction:** the brief, including the hypothesis and what would change their
   mind.
2. **The data:** which sources are used ([METHOD.md § 4](METHOD.md#4-source-agreement)).
3. **The plan**, before any calculation.
4. **Every change to `status/`.** The AI may draft; the owner confirms each change.
5. **Anything involving another person's data:** who, for what, and how consent was
   given. Consent passed on verbally by the owner is logged as exactly that.
6. **A deviation from the approved method.**
7. **Any escalation trigger** ([METHOD.md § 9](METHOD.md#9-escalation-triggers-written-before-the-result)).

Everything else (semantics, knowledge, results catalog, READMEs, the analysis files) is
written and verified by the AI, which records who checked a file and when: in the
`verified_by` field where the file has front matter, otherwise in a line at the top.

**An AI never writes its own recommendation into a file as if it were the owner's
decision.** A recommendation is written as a recommendation, with who made it.

## 4. Review

The review is what catches the errors nobody else sees. No analysis closes without one.

1. **A different session than the one that planned or executed.** Ideally a different
   model, because the same model shares the same blind spots.
2. **The reviewer reruns things.** A verdict is a command and its output, not an opinion.
   An unreproduced number fails.
3. **Blind where possible.** If prior results exist, the reviewer writes its own
   expectation before reading them.
4. **Planted errors.** Where a check exists, the reviewer plants one deliberate error and
   confirms the check catches it.
5. Findings go in `review.md` ([template](templates/review.md)), ranked by consequence:
   wrong meaning or wrong number first, then reproducibility, then form.

Rounds of fixes continue until the review is green. Each fix states its expected result
before it is run.

## 5. Ownership is by folder

| Folder or file | Written by |
|---|---|
| `status/` | Owner approves every change |
| `analyses/<name>/` | The planner and executor of that analysis; after closing, changed only through a new review, with the commit listed in `reanalysis.md` § 9 |
| `semantics/`, `knowledge/`, `results.md`, READMEs | AI, verified and dated |
| `learnings.md` | AI proposes; owner decides |
| `METHOD.md`, `ROLES.md`, `DATA.md`, `START_HERE.md`, `templates/` | Changed only with the owner's explicit yes |

**Never two sessions in the same folder at the same time.** Without file locking, the
folder is the only safe boundary. Parallel work happens in separate folders (waves,
[METHOD.md § 11](METHOD.md#11-large-analyses-waves)).

## 6. Handover between sessions

A session that stops before the work is done leaves a `HANDOVER.md` in the analysis
folder, from [`templates/handover.md`](templates/handover.md): what is done, what is
left, what needs the owner, and which files are the current truth. Chat history is never the handover; the next session cannot see it.
