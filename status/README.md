# status

**The owner's own files.** The AI may draft a change; the owner confirms every change
before it is saved ([ROLES.md § 3](../ROLES.md#3-what-only-the-owner-approves)).

| File | Holds |
|---|---|
| `health-status.md` | Baseline facts (age, height, devices), known observations, measurements wished for |
| `follow-up.md` | Open flags from analyses, with status and review dates |
| `protocol.md` | What the owner currently does on purpose: routines, supplements, experiments |

## Confirmation: how old may a fact be?

Every file has two lines at the top:

```text
**Last confirmed by owner:** YYYY-MM-DD
**Valid for:** N days
```

Each file's validity lives only in its own header. If the confirmation is older than its
validity, or missing, a fact from the file **may
not carry an analysis** until the owner has confirmed it again. `tools/check.py` lists
files that have expired.

**How to confirm (for the AI):** present the file's checkable claims as a list of at most
ten lines and let the owner say yes or name the exceptions. "Is everything still right?"
is a rubber stamp, not a confirmation.

A single field can be confirmed on its own, dated next to the field. That does not reset
the file's date. `tools/check.py` also warns about baseline facts whose own date is more
than 365 days old.

## Three lists, three questions

| File | Answers |
|---|---|
| `health-status.md`, known observations | What we **know** |
| `health-status.md`, measurement wishes | What we **cannot know yet** |
| `follow-up.md` | What is **outside its reference and not yet assessed** |

Keep the boundary sharp, or the lists drift into each other.
