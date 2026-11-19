"""Mechanical helpers for the evidence standards in METHOD.md section 7.

Principle behind both functions: a half extract that looks complete is worse than
no extract. They fail hard instead of warning.

Standard library only, so they run anywhere.
"""

import re
from pathlib import Path


def validate_extract(rows, expected_count, key_field, ranges=None,
                     decimals=None, forbidden_patterns=None):
    """Validate an extract BEFORE it is written. Raises AssertionError on failure.

    rows                list of dicts, one per data row
    expected_count      a deliberate constant: a claim about the source that can fail
    key_field           field that must be unique (catches parse duplicates)
    ranges              {field: (min, max)} plausible limits; catches column shifts
    decimals            {field: n} expected decimal places; catches column swaps that
                        ranges miss when two fields have overlapping values
    forbidden_patterns  regexes no value may match (names, IDs)

    Returns the number of validated rows, so the call can sit in an assert.
    """
    assert rows, "the extract is empty: do not write it"
    assert len(rows) == expected_count, (
        f"expected {expected_count} rows, got {len(rows)}. Change the constant "
        "deliberately, or find the missing row"
    )
    missing = [f for f in [key_field] + list(ranges or {}) if f not in rows[0]]
    assert not missing, (
        f"fields {missing} not in the extract. Columns: {sorted(rows[0])}. "
        "Check delimiter and header before validating"
    )
    keys = [r[key_field] for r in rows]
    duplicates = sorted({k for k in keys if keys.count(k) > 1})
    assert not duplicates, (
        f"duplicate {key_field}: {duplicates}. Usually a parse error, where a line "
        "broken in two was read as the next row"
    )
    for field, (low, high) in (ranges or {}).items():
        filled = [r for r in rows if r.get(field) not in (None, "")]
        assert filled, f"{field} is empty in every row: suspect a wrong column name or a shift"
        for r in rows:
            value = r.get(field)
            if value is None or value == "":
                continue
            assert low <= float(value) <= high, (
                f"{field}={value} outside [{low}, {high}] in row {r[key_field]}: "
                "suspect a column shift"
            )
    # Range checks alone are not enough: two fields with overlapping ranges can
    # swap places without breaking any limit. A decimal signature catches it when
    # the source formats the fields differently.
    for field, places in (decimals or {}).items():
        for r in rows:
            value = str(r.get(field, "")).strip()
            if not value or "." not in value:
                continue
            found = len(value.split(".")[1])
            assert found == places, (
                f"{field}={value} has {found} decimals, expected {places} in row "
                f"{r[key_field]}: strong sign of swapped columns"
            )
    for pattern in forbidden_patterns or []:
        rx = re.compile(pattern, re.IGNORECASE)
        for r in rows:
            for field, value in r.items():
                assert not rx.search(str(value)), (
                    f"forbidden pattern {pattern!r} in {field}={value!r}"
                )
    return len(rows)


def grep_with_positive_control(pattern, control, root=".", file_glob="*.md"):
    """A search that refuses to report zero before a control search found something.

    pattern   what you are looking for (Python regex, case insensitive; use | for "or")
    control   a term you KNOW is in the material
    Raises RuntimeError if the control finds nothing: then you are searching the
    wrong material or with a broken pattern, and a zero result proves nothing.

    Pure Python, so it works on every operating system.
    Returns the list of hits as "file:line:text".
    """
    root = Path(root)

    def run(p):
        rx = re.compile(p, re.IGNORECASE)
        hits = []
        for path in sorted(root.rglob(file_glob)):
            if not path.is_file() or ".git" in path.parts:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for n, line in enumerate(text.splitlines(), 1):
                if rx.search(line):
                    hits.append(f"{path.relative_to(root)}:{n}:{line.strip()}")
        return hits

    control_hits = run(control)
    if not control_hits:
        raise RuntimeError(
            f"positive control {control!r} found 0 hits in {str(root)!r}: wrong material "
            f"or wrong pattern. A zero result for {pattern!r} proves nothing"
        )
    hits = run(pattern)
    print(f"positive control {control!r}: {len(control_hits)} hits, the search works")
    print(f"search {pattern!r}: {len(hits)} hits")
    return hits
