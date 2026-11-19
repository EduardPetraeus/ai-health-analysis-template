# Module: verified autopilot (opt in)

**Off by default.** Use it only when the owner writes `Level: 3` in a brief. It changes
how work is organized, not how analysis is done: [METHOD.md](../../METHOD.md) applies
unchanged.

The idea: the analysis work runs on its own, with the owner in the loop only where it
matters. **The direction never runs on autopilot.** The owner writes the brief, confirms
the data and approves the plan, exactly as in [ROLES.md § 3](../../ROLES.md#3-what-only-the-owner-approves).

## 1. Who does what

Planner, executor and reviewer are as in [ROLES.md § 1](../../ROLES.md#1-the-participants).
The module adds one role:

| Role | Does | Never |
|---|---|---|
| **Coordinator** (one AI session) | Writes prompts for the other sessions, follows their work, runs its own independent checks, logs every decision, contacts the owner only when needed | Accepts a claim without checking the actual file. Does the analysis itself |

Each role runs in its own session. **A session never switches model midway**; a new model
gets a new session with a handover file.

## 2. Lifecycle

| Step | Who | Result | Gate |
|---|---|---|---|
| 1. Direction | **Owner** | `brief.md` | Never automated |
| 2. Plan | Coordinator and planner | `plan.md` for all phases, with preregistered expectations | Coordinator challenges the plan in writing, then freezes it with a hash |
| 3. Approval | **Owner** | "ok" to a short overview | Approves phases 0 to 3 together |
| 4. Execution | Executor, followed by coordinator | Phases 4 and 5 | Coordinator checks intermediate results against the files |
| 5. Review | Reviewer and coordinator, separately | `review.md` | Rounds of fixes, each with a preregistered expected result, until green |
| 6. Closing | Coordinator, report to **owner** | Closing checklist green | Not done before it is green |

## 3. Proof standard

These are requirements, not good habits, in addition to the review rules in
[ROLES.md § 4](../../ROLES.md#4-review) and the evidence standards in
[METHOD.md § 7](../../METHOD.md#7-evidence-standards):

1. **Preregistration.** Before any run that writes results, the expected outcome is
   written down: row counts, which files change, which stay identical.
2. **Independent rerun.** The coordinator reruns the script in a clean environment. The
   output must match exactly.
3. **A third method.** Spot checks use a different tool than the executor used.
4. **Sources opened and read.** A source seen only as a title carries nothing.
5. **Traceability.** Every number can be followed from report to file to source; every
   file has a hash in the log.
6. **Blind planning.** If earlier results exist, the planner does not read them until the
   plan is frozen.
7. **Never read a hash or a number from a screenshot.** Recompute it or read it as text.

All sessions sharing one model family share its blind spots. The checks above catch
errors in execution; only the owner's direction and a reviewer on a different session
(ideally a different model) guard the plan itself.

## 4. Mandate and escalation

The coordinator may decide alone: intermediate gates after checking the files, small
deviations with a written reason, rounds of fixes, documentation.

**Always goes to the owner:** everything in [ROLES.md § 3](../../ROLES.md#3-what-only-the-owner-approves),
any number that contradicts an earlier delivered result, and doubt.

**Resource limits are written in advance** when a task downloads data or runs long:
maximum network, maximum time, minimum free disk, and "if it fails, no new run without
the owner".

**Rhythm.** Check in rarely; waiting is free, and every check costs context and usage.
The owner hears immediately only about what is critical or blocked on them. Everything
else comes as one summary in three points: done, left, needs you.

## 5. Files in the analysis folder

In addition to the standard files ([METHOD.md § 8](../../METHOD.md#8-the-analysis-folder)):

| File | Content |
|---|---|
| `brief-raw.txt` | The owner's first message, byte for byte, saved before anything else and never edited |
| `log.md` | The coordinator's log: every action and decision with a timestamp and what was checked |
| `prompts/` | Every prompt sent to another session, with its hash |
| `challenge-1.md` | The coordinator's written challenge to the plan |
| `HANDOVER.md` | State for the next session ([ROLES.md § 6](../../ROLES.md#6-handover-between-sessions)) |

## 6. Remote control (optional, separate decision)

**Off unless the brief also says `Remote control: yes`.** Some setups let one AI session operate another AI application, for example a
coordinator typing prompts into a research tool while the owner is away. If you use it:

1. **Approval prompts in the controlled app are pressed by the owner**, never by the
   coordinator. Permission cards exist so a human decides; an agent clicking them
   defeats their purpose.
2. Paste the full prompt and verify the text in the field before sending; typed input
   can be mangled by focus changes.
3. Everything that matters is written to files, never only to a chat. Chats get
   summarized and lose detail.
4. The owner can stop it at any time, and the coordinator says plainly when it is
   running.

## 7. Known limits

- The method proves that numbers are in their sources and nothing vanished or doubled.
  It does not prove that a source is clinically right for the owner.
- Same model family in every role, unless the owner chooses otherwise (§ 3).
- Sessions can lose context; that is why everything must live in files.
