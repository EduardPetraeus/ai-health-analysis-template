# Concepts: what we mean by semantics, and where each kind of knowledge lives

Read this before writing or using anything in `semantics/`. It is short on purpose.

## Why

A model that only has column names and values guesses. A tag called `awake` in a sleep
log is read as "woke up in the morning" when it means "awake during the night"; a column called `score` turns out to be a
provider's proprietary index on a scale nobody wrote down. The number is right and the
meaning is wrong, and the analysis is ruined anyway.

## The words, as used here

The industry uses these words in different ways. These definitions are ours.

| Word | Meaning here | Lives in |
|---|---|---|
| **Source** | A provider or app that delivers data, with what it measures, its devices and deliveries | `sources/<source>/README.md` |
| **Delivery** | One way a source delivers data: an export, an API, a PDF report. The same object can arrive in several deliveries with different field names | sections in the source and object files |
| **Object** | A well defined thing from a source with a grain: what one row is (one reading, one night, one lab result) | `sources/<source>/<object>.md` |
| **Field** | A property of an object, with meaning, unit, coding, scale, time zone and the source of its definition | the table in the object file |
| **Concept** | What a field measures, independent of the source (systolic blood pressure, resting heart rate). Two sources can carry the same concept, or two concepts under the same name | `ontology/<domain>.md` |
| **Relation** | How objects and concepts connect (a reading belongs to a device; a night has a resting heart rate) | relation sections in source and object files; across domains in the ontology |
| **Metric** | A formula that computes a number from fields, with grain, filters and version | `metrics/<metric>.md` |
| **Context** | Rules and caveats that cannot be written as a formula ("absence means not logged, not zero") | caveat sections in object files |
| **Label** | A category a provider puts on a value ("stage 1", "elevated", "dysbiosis"). A label is a field too: document which definition and threshold it applies | the object file |

No knowledge graph. Markdown with fixed sections is enough as long as a session can find
the right file by following the READMEs.

## One home per kind of knowledge

1. **What the provider says a field means:** `sources/`.
2. **What a concept is, across providers:** `ontology/`. Object files point to the
   concept `id`.
3. **How a number is computed:** `metrics/`.
4. **How an analysis used the data:** that analysis's `reanalysis.md`.
5. **General medical knowledge:** `knowledge/`.

If the same thing appears in two places, one of them is a pointer that says where the
original is.

## How the documentation stays true

The rules are in [METHOD.md § 6](../METHOD.md#6-semantics-before-numbers). For the files
here, in addition: every file has a status and a last checked date in its front matter,
and a new export format or API version gets a new delivery section, while old ones are
marked superseded, never deleted.
