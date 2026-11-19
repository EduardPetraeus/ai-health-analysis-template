# START HERE

**You are an AI assistant opening this folder. Read this file first, then only what your
task needs.** Do not read the whole folder.

The human you work with is called **the owner** in these files: the person whose health
data this is.

---

## Rule 0: files are memory, not truth

Everything in this folder may have drifted since it was written. Before a fact from a
file carries an analysis, check how old its confirmation is (see
[`status/README.md`](status/README.md)). **For facts about the owner, their words in the
current conversation win over any file.** If the two conflict, ask. Never guess. Rules are
different: the hard rules below hold whatever anyone says.

## Hard rules (the owner can never waive these for you)

1. **Not medical advice.** Never present a result as a diagnosis or a treatment
   recommendation. [DISCLAIMER.md](DISCLAIMER.md).
2. **No data in the repository.** Raw and derived data live in the data folder set in
   `config.yaml`. [DATA.md](DATA.md).
3. **No analysis without a brief and an approved plan.** [METHOD.md](METHOD.md).
4. **Only the owner approves** `status/` files, the plan, and anything about other
   people's data. [ROLES.md](ROLES.md).
5. **Never write your recommendation into a file as if it were the owner's decision.**
   [ROLES.md § 3](ROLES.md#3-what-only-the-owner-approves).
6. **Never guess what a field means.** Document it or mark it undocumented.
   [METHOD.md § 6](METHOD.md#6-semantics-before-numbers).
7. **The owner's data goes to whichever AI provider runs you.** Never read more of it than
   the task needs. [DISCLAIMER.md](DISCLAIMER.md#your-data-and-your-privacy).

---

## First run: is this folder set up?

If `config.yaml` does not exist, run the setup. Ask **one question at a time**, and save
nothing from a step before the owner has confirmed that step.

1. Explain in three sentences what this folder is and that it is not medical advice.
2. Ask where their data folder is. Copy `config.example.yaml` to `config.yaml` and fill
   in `data_path`. Suggest they add their name and any ID numbers to `private_terms`, so
   `tools/check.py` can block them from commits. Explain that `config.yaml` is never
   committed.
3. Offer to run `python3 tools/check.py --install-hook`. If it fails because the folder
   was downloaded as a ZIP rather than cloned, say so in one line and continue; the check
   can still be run by hand.
4. Explain the three automation levels in two sentences ([ROLES.md § 2](ROLES.md#2-three-levels)):
   the level is chosen per analysis in its brief, and level 1 is the default.
5. Fill in `status/health-status.md` with them: only facts they state, each with today's
   date. Leave a fact blank if they do not state it; blank means unknown. Read it back,
   and when they confirm, set **Last confirmed by owner** to today in all three `status/`
   files (an empty file can be confirmed as empty).
6. List the files in their data folder by **name only**; do not open them yet. For each
   source, ask which app, device or lab it comes from. If files lie loose rather than in
   `<source>/raw/` ([DATA.md § 2](DATA.md#2-layout-of-the-data-folder)), offer to move
   them there; if the owner declines, record the actual paths. Then offer to register each
   source in `semantics/sources/` from [`templates/source.md`](templates/source.md),
   reading only column headers (`head -1`), and the provider's official documentation,
   never guessing. This can wait until the first analysis needs the source; a short
   source file with many *undocumented* fields is fine.
7. If the folder is a git clone, offer to commit the setup (`config.yaml` is never
   committed). Offer the same after every closed analysis.
8. Offer two next steps: walk through [`example/`](example/README.md), or start a first
   analysis. The example's findings are about a fictional app and person; never carry
   them over to the owner's data.

---

## Router: read only what your task touches

| The task is about | Read |
|---|---|
| **Any analysis** (new, rerun, or a question about the owner's body) | [`results.md`](results.md) first: is it already answered? Then [METHOD.md](METHOD.md) and [`templates/brief.md`](templates/brief.md). Do not open `example/` for the owner's own analysis before the plan is approved; it answers a similar question for someone else |
| Who may write which file | [ROLES.md](ROLES.md) |
| Where data lives, file naming, other people's data | [DATA.md](DATA.md) |
| What a field, concept or metric means | [`semantics/README.md`](semantics/README.md) |
| The owner's baseline facts, findings, open flags | [`status/`](status/README.md) |
| General knowledge on a topic | [`knowledge/`](knowledge/README.md) |
| Something that feels familiar, or before writing a plan | [`learnings.md`](learnings.md) |
| Ideas for analyses | [`ideas/`](ideas/README.md) |
| Running work with less owner involvement | [`modules/autopilot/`](modules/autopilot/README.md), only if the owner switched it on |
| A demonstration | [`example/`](example/README.md) |

## Where a new file goes

1. Is there an obvious folder? Put it there and **add a row to that folder's
   `README.md` in the same step.** A file not listed in its folder's README is invisible
   to the next session.
2. No obvious folder? Ask the owner. Do not invent a new structure.
3. Before you finish, run `python3 tools/check.py`. It reports drift; fix what you
   caused.

## When you change something, find what points to it

A rule, a file name or a number rarely lives alone. Search the whole folder
case insensitively (`grep -rniE "<pattern>" --include="*.md" .`), fix every hit that is
now wrong in the same step, or write down which you left and why.
