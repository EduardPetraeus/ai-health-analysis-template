# Fewer permission prompts in Claude Code (optional)

Claude Code asks before it runs a command it has not been allowed. During an analysis
that can mean dozens of prompts for commands that only read. If you use Claude Code, you
can allow the read only ones for this folder. Nothing here is required, and other AI
tools ignore it.

Create `.claude/settings.local.json` in the repository with the block below, and change
the path to your own data folder, written out in full. `check.py` refuses `.json` files,
so this file never reaches a commit.

```json
{
  "permissions": {
    "additionalDirectories": ["/Users/you/health-data"],
    "allow": [
      "Bash(head:*)",
      "Bash(tail:*)",
      "Bash(wc:*)",
      "Bash(ls:*)",
      "Bash(grep:*)",
      "Bash(sort:*)",
      "Bash(cut:*)",
      "Bash(git status:*)",
      "Bash(git log:*)",
      "Bash(git diff:*)",
      "Bash(git show:*)",
      "Bash(git ls-files:*)",
      "Bash(git check-ignore:*)",
      "Bash(python3 tools/check.py:*)"
    ],
    "deny": [
      "Bash(git push:*)"
    ]
  }
}
```

**What is left out on purpose:** commands that can write or delete files (`rm`, `mv`,
`sed -i`), commands that can run anything (`awk`, `perl`, `python3` in general), and
network commands. Claude Code still asks before those, which is the point.

Claude Code asks about chained commands (`cd x && git y`, loops, heredocs) even when each
part is allowed, so the AI should run one command per tool call.

When a command is refused, the AI should say "permission denied", not "a hook blocked
it". The hook only ever prints `check.py` output.

Check Claude Code's own settings documentation if a rule does not behave as expected;
the rule syntax belongs to Claude Code, not to this template.
