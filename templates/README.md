# templates

Copy a template, never edit it in place. The rules each template serves live in
[METHOD.md](../METHOD.md); the templates only give them a shape.

| File | Used for | Copied to |
|---|---|---|
| `brief.md` | The owner's brief: goal, scope, data, hypothesis, what would change their mind | `analyses/<name>/brief.md` |
| `plan.md` | Phases 0 to 3 and the overview the owner approves | `analyses/<name>/plan.md` |
| `reanalysis.md` | Ten sections that let another session reach the same numbers | `analyses/<name>/reanalysis.md` |
| `review.md` | The independent review, with commands and outputs | `analyses/<name>/review.md` |
| `conclusion.md` | The one page the owner reads | `analyses/<name>/conclusion.md` |
| `source.md` | What a data source is and delivers | `semantics/sources/<source>/README.md` |
| `object.md` | One object from a source and its fields | `semantics/sources/<source>/<object>.md` |
| `metric.md` | A formula computed from documented fields | `semantics/metrics/<metric>.md` |
| `ontology.md` | Concepts of one domain, across sources | `semantics/ontology/<domain>.md` |
| `knowledge.md` | General knowledge on a topic, with numbered sources | `knowledge/<topic>.md` |
| `handover.md` | State for the next session when work stops unfinished | `analyses/<name>/HANDOVER.md` |

Do not make a variant of a template for a special domain. Five variants drift apart
exactly like five copies of a rule. When a field does not fit, write why it does not
apply.
