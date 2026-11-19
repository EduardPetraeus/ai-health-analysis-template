#!/usr/bin/env python3
"""Example analysis: does the app's "Stage 1 Hypertension" label hold up?

SYNTHETIC DATA. Follows the approved plan in plan.md. Standard library only.

  python3 example/analyses/2026-11-19_home-bp-app-flag/analysis.py           run, write results
  python3 example/analyses/2026-11-19_home-bp-app-flag/analysis.py --check   rerun, compare with committed results

In a real analysis the data folder comes from config.yaml (DATA.md). The example keeps
its synthetic data folder inside example/ so it runs out of the box.
"""

import csv
import hashlib
import io
import statistics
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "tools"))
from extract_checks import validate_extract  # noqa: E402

NAME = HERE.name
DATA = REPO / "example" / "data-folder"
RAW = DATA / "home-bp-app" / "raw" / "export-2026-11-18.csv"
OUT = DATA / "analyses" / NAME / "results.csv"

# --- Preregistered constants (plan.md section 3) -----------------------------------
EXPECTED_RAW_ROWS = 84              # a claim about the source; fails if it changes
PROTOCOL_FIRST_DAY = date(2026, 11, 8)
PROTOCOL_DAYS = 7
EXCLUDE_NOTES = {"cuff loose"}      # measurement known to be invalid
EXPECTED_DUPLICATES = 2             # identical rows seen when listing the file (plan.md section 2)
EXPECTED_EXCLUDED = 1
# Thresholds, each with its source in reanalysis.md section 8.
HOME_HYPERTENSION = (135, 85)       # ESH 2021 position paper; ESC 2024
HOME_ELEVATED = (120, 70)           # ESC 2024, home: 120/70 to <135/85
CRISIS = (180, 120)                 # AHA patient guidance, single reading
# Two sided 95 % t quantiles by degrees of freedom (standard tables).
T_975 = {4: 2.776, 5: 2.571, 6: 2.447}


def app_rule(sys_, dia):
    """The label rule the app is hypothesized to use (office cut points, per reading)."""
    if sys_ >= 140 or dia >= 90:
        return "Stage 2 Hypertension"
    if sys_ >= 130 or dia >= 80:
        return "Stage 1 Hypertension"
    if sys_ >= 120:
        return "Elevated"
    return "Normal"


def load():
    with RAW.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    for i, r in enumerate(rows):
        r["row"] = i + 2  # line number in the file, header is line 1
    validate_extract(
        rows, EXPECTED_RAW_ROWS, key_field="row",
        ranges={"SYS (mmHg)": (70, 250), "DIA (mmHg)": (40, 150), "Pulse (bpm)": (30, 200)},
    )
    return rows


def deduplicate(rows):
    seen, kept, dropped = set(), [], []
    for r in rows:
        key = tuple(r[c] for c in ("Date", "Time", "SYS (mmHg)", "DIA (mmHg)", "Pulse (bpm)", "Note"))
        (dropped if key in seen else kept).append(r)
        seen.add(key)
    return kept, dropped


def mean_ci(day_means):
    n = len(day_means)
    m = statistics.mean(day_means)
    half = T_975[n - 1] * statistics.stdev(day_means) / n ** 0.5
    return m, m - half, m + half


def protocol_summary(rows, skip_first_day):
    days = {}
    for r in rows:
        if r["Note"] != "protocol":
            continue
        d = date.fromisoformat(r["Date"])
        if skip_first_day and d == PROTOCOL_FIRST_DAY:
            continue
        days.setdefault(d, []).append((int(r["SYS (mmHg)"]), int(r["DIA (mmHg)"])))
    readings = [x for v in days.values() for x in v]
    sys_day = [statistics.mean(s for s, _ in v) for v in days.values()]
    dia_day = [statistics.mean(d for _, d in v) for v in days.values()]
    return {
        "days": len(days), "readings": len(readings),
        "sys": mean_ci(sys_day), "dia": mean_ci(dia_day),
    }


def run():
    raw = load()
    rows, duplicates = deduplicate(raw)
    assert len(duplicates) == EXPECTED_DUPLICATES, f"expected {EXPECTED_DUPLICATES} duplicates, found {len(duplicates)}"
    # After removing exact duplicates, date and time must identify a reading uniquely.
    for r in rows:
        r["key"] = f"{r['Date']} {r['Time']}"
    validate_extract(rows, EXPECTED_RAW_ROWS - EXPECTED_DUPLICATES, key_field="key")
    excluded = [r for r in rows if r["Note"] in EXCLUDE_NOTES]
    assert len(excluded) == EXPECTED_EXCLUDED, f"expected {EXPECTED_EXCLUDED} excluded, found {len(excluded)}"
    rows = [r for r in rows if r["Note"] not in EXCLUDE_NOTES]

    # Semantics check: does the app's Category equal the office rule per reading?
    label_matches = sum(app_rule(int(r["SYS (mmHg)"]), int(r["DIA (mmHg)"])) == r["Category"] for r in rows)

    primary = protocol_summary(rows, skip_first_day=True)
    sensitivity = protocol_summary(rows, skip_first_day=False)

    adhoc = [r for r in rows if r["Note"] != "protocol"]
    hyper_labels = [r for r in adhoc if r["Category"].startswith("Stage")]
    adhoc_plain = [r for r in adhoc if r["Note"] == ""]
    adhoc_context = [r for r in adhoc if r["Note"] != ""]
    max_row = max(rows, key=lambda r: (int(r["SYS (mmHg)"]), int(r["DIA (mmHg)"])))
    max_dia_row = max(rows, key=lambda r: (int(r["DIA (mmHg)"]), int(r["SYS (mmHg)"])))

    def m(rs, col):
        return statistics.mean(int(r[col]) for r in rs)

    results = [
        ("raw_rows", len(raw)),
        ("duplicates_removed", len(duplicates)),
        ("excluded_cuff_loose", len(excluded)),
        ("analysed_rows", len(rows)),
        ("app_label_matches_office_rule", f"{label_matches}/{len(rows)}"),
        ("protocol_days_used_primary", primary["days"]),
        ("protocol_readings_used_primary", primary["readings"]),
        ("primary_mean_sys", round(primary["sys"][0], 1)),
        ("primary_sys_ci95_low", round(primary["sys"][1], 1)),
        ("primary_sys_ci95_high", round(primary["sys"][2], 1)),
        ("primary_mean_dia", round(primary["dia"][0], 1)),
        ("primary_dia_ci95_low", round(primary["dia"][1], 1)),
        ("primary_dia_ci95_high", round(primary["dia"][2], 1)),
        ("sensitivity_all7_mean_sys", round(sensitivity["sys"][0], 1)),
        ("sensitivity_all7_mean_dia", round(sensitivity["dia"][0], 1)),
        ("adhoc_readings", len(adhoc)),
        ("adhoc_labelled_stage1_or_2", f"{len(hyper_labels)}/{len(adhoc)}"),
        ("adhoc_no_note_mean_sys", round(m(adhoc_plain, "SYS (mmHg)"), 1)),
        ("adhoc_no_note_mean_dia", round(m(adhoc_plain, "DIA (mmHg)"), 1)),
        ("adhoc_no_note_n", len(adhoc_plain)),
        ("adhoc_with_note_mean_sys", round(m(adhoc_context, "SYS (mmHg)"), 1)),
        ("adhoc_with_note_mean_dia", round(m(adhoc_context, "DIA (mmHg)"), 1)),
        ("adhoc_with_note_n", len(adhoc_context)),
        ("highest_single_reading", f"{max_row['SYS (mmHg)']}/{max_row['DIA (mmHg)']} on {max_row['Date']}"),
        ("highest_diastolic_reading", f"{max_dia_row['SYS (mmHg)']}/{max_dia_row['DIA (mmHg)']} on {max_dia_row['Date']}"),
        ("primary_below_home_hypertension_135_85",
         primary["sys"][2] < HOME_HYPERTENSION[0] and primary["dia"][2] < HOME_HYPERTENSION[1]),
        ("primary_in_esc_home_elevated_range",
         (primary["sys"][0] >= HOME_ELEVATED[0] or primary["dia"][0] >= HOME_ELEVATED[1])
         and primary["sys"][0] < HOME_HYPERTENSION[0] and primary["dia"][0] < HOME_HYPERTENSION[1]),
        ("any_reading_over_crisis_180_120",
         any(int(r["SYS (mmHg)"]) > CRISIS[0] or int(r["DIA (mmHg)"]) > CRISIS[1] for r in rows)),
    ]
    return results


def render(results):
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(["metric", "value"])
    writer.writerows(results)
    return buffer.getvalue()


def main(argv):
    text = render(run())
    if "--check" in argv:
        committed = OUT.read_text(encoding="utf-8")
        same = text == committed
        print("analysis.py --check:", "OK, results reproduce exactly" if same else "MISMATCH")
        return 0 if same else 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(text)
    print(f"wrote {OUT.relative_to(REPO)} sha256 {hashlib.sha256(text.encode()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
