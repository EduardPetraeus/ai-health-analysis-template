# DATA: where data lives and the rules for it

## 1. Data never enters the repository

The repository holds method, semantics and conclusions. **Data lives in a separate
folder**, set once in `config.yaml`:

```yaml
data_path: ~/health-data
```

`config.yaml` is listed in `.gitignore`. `tools/check.py` only lets Markdown, Python and
YAML files through (plus the two synthetic data files in `example/`), so a data export of
any type is refused before it can be committed, once the hook is installed
([README.md](README.md#safety-net-before-you-commit)). `.gitignore` is a convenience on top
and not the guard.

## 2. Layout of the data folder

One folder per source, three kinds of content:

```text
<data_path>/
  <source>/
    raw/        exactly as exported or downloaded; never edited
    derived/    produced by a script from raw; can always be rebuilt
    authored/   typed in by hand (a lab value from a paper report, a log)
  analyses/
    <YYYY-MM-DD_topic>/   data outputs of one analysis
```

| Kind | Rule |
|---|---|
| `raw/` | **Read only.** Never edited, renamed inside, or overwritten. A new export goes in a new dated subfolder |
| `derived/` | Written only by a script that is saved with the analysis or dataset that owns it |
| `authored/` | Hand typed values keep the source document's name, date and unit next to the value |
| `analyses/<name>/` | Same name as `analyses/<name>/` in the repository. **An analysis output is never the input to a new analysis**; go back to raw |

Source folder names are lowercase with hyphens (`home-bp-app`, `lab-reports`). Column
names in files you create are lowercase with underscores (`systolic_mmhg`).

## 3. Trust order

1. Raw export or original report.
2. Derived dataset, built by a documented script from raw.
3. A Markdown file. Never the source of a number, only evidence one was once computed.

A new kind of delivery (a different export format, an API) is trusted only after its
mapping to an already documented delivery has been checked on data
([METHOD.md § 6](METHOD.md#6-semantics-before-numbers)).

## 4. Personal identifiers

1. No names, ID numbers, addresses or sample IDs in anything committed. Scripts find the
   data folder with `data_path()` from `tools/config.py`, never an absolute path
   containing a user name.
2. List your own identifiers under `private_terms` in `config.yaml`. The pre commit check
   blocks any commit that contains them.
3. Location data in exports (GPS tracks, addresses) is not analyzed unless the brief
   explicitly asks for it.
4. Files in an export that are not health data (payment records, account settings) are
   not opened.

## 5. Other people's data

Data about a partner, child or anyone else needs their consent. The brief records who,
what the data may and may not be used for, and how consent was given. Extending the use
later is the owner's decision and covers only what is named. Another person's data is
never mixed into the owner's `status/` files.

## 6. Where analysis files go

| File | Location |
|---|---|
| Script, plan, reanalysis, review, conclusion | `analyses/<name>/` in the repository |
| Every data output (CSV, Parquet, charts built from data) | `<data_path>/analyses/<name>/` |

Before closing an analysis, confirm that `analyses/<name>/` in the repository contains no
data files. `python3 tools/check.py` does this for you.
