# Review · <YYYY-MM-DD_topic>

*Written by a session that did not plan or execute the analysis (`ROLES.md § 4`). A
verdict is a command and its output, not an opinion. The file shows the latest review
only; earlier rounds live in git history.*

**Reviewer:** <session, model> · **Date:** YYYY-MM-DD · **Commit reviewed:** <hash>

## Expectation before reading the results
*What the reviewer expects the primary endpoint to be, written before opening
`conclusion.md`. Write "no expectation" if none.*

## Checks

| # | Check | Command | Output | Verdict |
|---|---|---|---|---|
| 1 | Script reruns and reproduces every number in `reanalysis.md` § 5 | | | ✅ / ❌ |
| 2 | Every field used is documented in `semantics/` | | | |
| 3 | Every number meets METHOD § 2 | | | |
| 4 | Thresholds match their cited sources, opened and read. Without web access: could not be checked | | | |
| 5 | Brief commit precedes any read of data values; plan commit precedes any judged calculation; changes after them are listed | | | |
| 6 | Negative statements have positive controls | | | |
| 7 | A planted error is caught by the analysis checks | | | |
| 8 | No data files and no living file dependencies | | | |
| 9 | `conclusion.md` within one page, section 5 filled in, no advice or urgency without a source | | | |
| 10 | The statistics hold: assumptions stated, an alternative analysis or threshold source tried, the conclusion follows from the numbers | | | |
| 11 | Every number and every counted claim in `conclusion.md` ("all 9 days", "most readings") matches a command output, quoted here | | | |
| 12 | If T1 fired: nothing was computed after it, and the conclusion quotes the source's instruction | | | |

## Findings, ranked by consequence
1. **Wrong meaning or wrong number:**
2. **Reproducibility:**
3. **Form:**

## Verdict
✅ green (no finding of rank 1 or 2, and none in `conclusion.md`) / ❌ fixes needed (list, each with the expected result
after the fix)

## Next step for the owner
*One message: which chat gets which findings, with the fix prompt from `README.md` § 5,
and that a new review chat follows. The reviewer commits this file.*
