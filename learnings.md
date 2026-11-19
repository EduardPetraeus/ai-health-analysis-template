# Learnings: patterns that are expensive to discover twice

Not events, not summaries, not rules. **Patterns** that would make a future session do
something differently.

## How something gets here

Everything starts local, in an analysis folder. At the end of each analysis, the AI
tests every notable event against two questions, in this order:

| # | Question | Then |
|---|---|---|
| 1 | Does it change what an AI **may** or **must** do? | It is a **rule**: propose a change to the file that owns the topic |
| 2 | Would a future session otherwise **repeat an investigation or a mistake**? | It is a **learning**: propose it here |
| 3 | Neither | It stays local |

The AI proposes; the owner decides. A learning grants no permissions and never overrides
a rule. It points to the rule rather than copying it.

---

## Seed learnings

These came from the self analysis this template was distilled from. Each has cost at
least one real error.

### L1 · "Only if it is critical" is not a threshold. It is a mood
A principle without a threshold is interpreted by whichever session is in the room, and
the drift always goes to the comfortable side: not confirming, not escalating, not
deciding. **Do instead:** any rule that should trigger an action gets a number, a date or
a list. See METHOD § 9.

### L2 · One field doing two jobs must become two fields
"Is this value current?" and "when do I measure again?" have different answers. So do a
reference interval and a decision limit. One field forces a compromise that is wrong
both ways. **Do instead:** split it. The price is one column.

### L3 · A claim in your own files is not verified because it is written there
Old sessions wrote guesses that later read like facts. **Do instead:** before a fact from
a file carries advice or an analysis, check its confirmation date (START_HERE, rule 0).

### L4 · A role model spreads its flaws, not just its virtues
An earlier analysis held up as "do it like this" was copied, including the parts that
were wrong. **Do instead:** before pointing to an example, read it and list what not to
copy.

### L5 · Remove the possibility of an error rather than adding a check
A check catches an error after it happens and can be forgotten. A design that makes the
error impossible cannot. **Do instead:** ask first whether the design can rule it out.
Data outside the repository is an example.

### L6 · A parsed extract is a claim about the source, not the source
Parsers silently swap columns, merge lines and drop rows. **Do instead:** spot check the
extract against the raw file with a different tool. See METHOD § 7.

### L7 · A control that reads from inside cannot see what was left out
Self reported checksums, file counts and "all done" statements failed repeatedly. **Do
instead:** verify state at the source, from outside, and treat a self report as a claim.

### L8 · The review finds what nobody else sees
In more than one analysis the most serious error was found only by the independent
reviewer that reran everything, not by the executor and not by the coordinator. **Do
instead:** never skip the review for a result someone will act on. See ROLES § 4.

### L9 · Conclude on probability; a limitation of the method is not an open finding
Holding a question open because the method has a blind spot leaves the owner with
nothing to decide on. **Do instead:** answer with what the data show and how likely the
opposite is, and write the blind spot next to the answer.

### L10 · Pilot against the hardest input, not the easiest
A check that passed on the smallest file failed on the largest. **Do instead:** read the
input's conventions first, and pilot time and memory on the biggest or messiest unit.

### L11 · Frequent check ins cost more than they give
Polling a running job every few minutes burns context and usage while adding nothing.
**Do instead:** check rarely unless something expires; waiting is free.

### L12 · The same marker in two units
Two labs reported the same marker in different units, and a comparison silently mixed
them. **Do instead:** read the unit from each report row and store it with the value.

---

## Learnings from this copy

*Added by the owner's own analyses. Situation, what happened, what to do instead, and the
evidence (which analysis).*
