# AI Health Analysis Template

**Analyze your own health data with AI, the way a careful scientist would.**

A ready-made folder of plain Markdown rules and templates. You give it to your own AI
assistant, and the AI follows a fixed scientific method: hypothesis before data, sources
agreed before any number is computed, every number traceable, and a separate review
before you trust a result.

> ⚠️ **This is not medical advice.** It is a working method for people who want to do
> this kind of analysis themselves, shared as inspiration. It does not diagnose, it does
> not recommend treatment, and it does not replace a clinician. Read
> [DISCLAIMER.md](DISCLAIMER.md) before you start.

---

## Why this exists

Consumer health tests and apps give you labels: *"dysbiosis"*, *"stage 1 hypertension"*,
*"poor recovery"*. A label is a claim. Behind it sits a definition, a threshold, a
measurement protocol and a population someone chose. Change any of them and the label
can change too.

An AI assistant will happily analyze your data, but left alone it guesses what a column
means, picks its own data, and writes conclusions that grow more certain every time they
are copied. This template removes those failure modes by design:

| Without a method | With this template |
|---|---|
| The AI picks the data | You agree on the sources before anything is computed |
| The question drifts to whatever looks interesting | A hypothesis and one primary endpoint are written down first |
| Column meanings are guessed | Every field is documented from the provider's own docs, or marked *undocumented* |
| A number with no trail | Every number has its source, numerator and denominator, date range, exclusions and date of calculation |
| The same AI checks its own work | A separate review reruns the analysis before you trust it |
| Findings live in a chat and vanish | Each analysis is a folder anyone can rerun, with its history in git |

See it work in [`example/`](example/): an app says a (synthetic) person has *stage 1
hypertension*. The method finds out what that label actually rests on.

---

## Get started

You need an AI assistant that can read and write files in a folder on your computer
(for example Claude Code, Claude Desktop, Cursor or Codex). A GitHub account and Python
are optional: GitHub gives you version history, Python runs the safety check and the
example. You don't write code; the AI does the typing. Expect the setup conversation to
take half an hour, and a first analysis an evening. New words are explained in
[GLOSSARY.md](GLOSSARY.md).

### 1. Make your own private copy

Click **Use this template → Create a new repository** at the top of this page.

> 🔒 **Choose Private.** Your copy will hold your own health status, your analyses and
> their conclusions. Your raw data stays outside the repository (step 2), but your
> conclusions are personal too.

Then get it onto your computer: in your new repository click **Code**, and either open
it with GitHub Desktop or copy the address and run `git clone <address>` in a terminal.

No GitHub account? On this page click **Code → Download ZIP** and unpack it anywhere.
Everything works the same, except version history and the commit safety check.

### 2. Put your data somewhere outside the folder

Create a folder for your exports, for example `~/health-data/`. Lab reports, app exports,
wearable data: anything goes there, never inside the repository. The AI will help you
organize it in step 3.

### 3. Hand it to your AI

Open your AI tool in the repository folder (in Claude Code: run `claude` inside the
folder; in desktop apps: open or attach the folder) and paste this:

```text
Read START_HERE.md and set this up for me.
```

Remember that whatever the AI reads is sent to the company that runs it
([DISCLAIMER.md](DISCLAIMER.md#your-data-and-your-privacy)).

The AI will interview you, one question at a time:

1. where your data folder is (saved in `config.yaml`, which is never committed);
2. a few baseline facts about you (saved in `status/health-status.md`, which only you
   approve);
3. which data sources you have (registered in `semantics/sources/`).

### 4. Start your first analysis

```text
I want to start an analysis.
```

The AI walks you through the [analysis brief](templates/brief.md): what you want to
decide, what you expect, and which result would change your mind. Then it proposes a
plan, waits for your "ok", runs it, and reviews it.

### 5. Have it reviewed

When the analysis is done, open a **new** chat in the same folder, ideally with a
different model, and paste the review prompt:

```text
You did not make the analysis in analyses/<folder name>/. Review it as described in
ROLES.md section 4, using templates/review.md. Rerun everything; trust nothing you
have not reproduced.
```

**Want to see an example first?** Paste this instead:

```text
Read example/README.md and walk me through the example analysis.
```

---

## How it works

```text
 You                          Your AI
 ───                          ───────
 1. Brief: question,    ──▶   2. Plan: hypothesis, sources, method
    expectation, what              (stops and waits)
    would change your mind
 3. "ok"                ──▶   4. Runs the analysis, writes every step down
                              5. Separate review reruns it
 6. Read the conclusion ◀──   (one page, with what it does NOT answer)
```

You decide the direction, confirm the data, and approve the plan. The AI does the rest.

### Three levels of automation

| Level | What | Default? |
|---|---|---|
| **1. Single chat** | One AI conversation plans and runs; a second chat reviews; you approve the plan and read the conclusion | ✅ Yes |
| **2. Separate roles** | Planning, execution and review in separate conversations, ideally on different models | Recommended for anything you will act on |
| **3. Autopilot** | One AI coordinates the others and only contacts you when needed | Opt in: [`modules/autopilot/`](modules/autopilot/) |

Nothing runs on its own unless you switch it on.

---

## What is in the folder

| Path | What | Who writes it |
|---|---|---|
| [`START_HERE.md`](START_HERE.md) | The AI's entry point and router | Fixed |
| [`METHOD.md`](METHOD.md) | The scientific method: the rules every analysis follows | Fixed |
| [`ROLES.md`](ROLES.md) | Who does what, and what only you approve | Fixed |
| [`DATA.md`](DATA.md) | Where data lives and the rules for it | Fixed |
| [`templates/`](templates/) | Brief, plan, conclusion, reanalysis, review, source, object, metric | Fixed |
| [`status/`](status/) | Your health status, follow up list and protocol | **You** approve every change |
| [`analyses/`](analyses/) | One folder per analysis | AI |
| [`semantics/`](semantics/) | What your data means: sources, fields, concepts, metrics | AI, from official docs |
| [`knowledge/`](knowledge/) | General knowledge with sources, never findings about you | AI |
| [`results.md`](results.md) | Catalog of answered questions and reusable datasets | AI |
| [`learnings.md`](learnings.md) | Patterns that are expensive to discover twice | AI proposes, you decide |
| [`ideas/`](ideas/) | Analyses you might run later | Anyone |
| [`example/`](example/) | A complete analysis on synthetic data | Fixed |
| [`modules/autopilot/`](modules/autopilot/) | Optional: verified autopilot | Fixed |
| [`.claude/skills/`](.claude/skills/) | A thin skill that loads the method in Claude tools | Fixed |
| [`tools/check.py`](tools/check.py) | Blocks data and private terms from commits; checks indexes and links | Fixed |
| `config.example.yaml` | Copied to `config.yaml` at setup: your data path and private terms. Never committed | You |
| `AGENTS.md`, `CLAUDE.md` | Point AI tools to `START_HERE.md`; hold no rules | Fixed |
| [`GLOSSARY.md`](GLOSSARY.md) | Plain explanations of the words used | Fixed |
| [`DISCLAIMER.md`](DISCLAIMER.md), [`LICENSE`](LICENSE) | Not medical advice; MIT license | Fixed |

## Design principles

1. **One home per rule.** Every rule lives in exactly one file. Other files point to it
   and never copy it, because copies drift apart.
2. **Data never enters the repository.** Only Markdown, Python and YAML files are
   allowed; once you install the hook, `tools/check.py` blocks everything else, and your
   own private terms, before every commit.
3. **Your files are yours.** The AI drafts, but only you approve health status and
   protocol files.
4. **One truth per file.** Every file shows only the current version. No struck through
   text, no old versions side by side; git holds the history.
5. **Tool neutral.** Plain Markdown. Works with any AI that can read files.

## Safety net before you commit

Run once after setup:

```bash
python3 tools/check.py --install-hook
```

From then on every commit is checked for data files, your private terms (names, IDs,
anything you list in `config.yaml`), missing README entries and broken links. Without the
hook (for example a ZIP copy), run `python3 tools/check.py` yourself before sharing
anything.

## Credits and license

The method grew out of one person's long running self analysis with Claude Cowork,
Claude Science and Claude Code, and was distilled into this template. It draws on ideas
from international research standards (EQUATOR, TOP, GRADE, CENT) without claiming to
comply with them; see [METHOD.md § 14](METHOD.md#14-standards-this-method-draws-on).

MIT license. See [LICENSE](LICENSE).
