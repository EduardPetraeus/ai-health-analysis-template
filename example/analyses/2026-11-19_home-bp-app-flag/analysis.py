#!/usr/bin/env python3
"""Example analysis: does the app's "Stage 1 Hypertension" label hold up?

SYNTHETIC DATA. Follows plan.md. Standard library only.

  python3 example/analyses/2026-11-19_home-bp-app-flag/analysis.py           run, write results
  python3 example/analyses/2026-11-19_home-bp-app-flag/analysis.py --check   rerun, compare with committed results

In a real analysis the data folder comes from config.yaml (tools/config.py, DATA.md). The
example keeps its synthetic data folder inside example/ so it runs out of the box.
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

# --- Constants from plan.md section 3 -----------------------------------------------
EXPECTED_RAW_ROWS = 84              # a claim about the source; fails if it changes
EXPECTED_DUPLICATES = 2             # identical rows seen when describing the file
EXPECTED_EXCLUDED = 1               # the reading noted "cuff loose"
EXCLUDE_NOTES = {"cuff loose"}
PROTOCOL_FIRST_DAY = date(2026, 11, 8)
MIN_COMPLETE_DAYS = 3               # ESH 2021: 7 days, not fewer than 3
SESSIONS_PER_DAY = 2                # morning and evening; a day missing one is incomplete

# Thresholds for the home average, each with its source in reanalysis.md section 8.
FRAMEWORKS = {
    "esc_2024": {"hypertension": (135, 85), "elevated": (120, 70)},
    "aha_acc": {"stage1": (130, 80), "elevated_sys": 120},
}
ALARM = (180, 120)                  # AHA: "higher than 180/120" for a single reading
DEVICE_MEAN_ERROR_ALLOWED = 5       # ISO 81060-2 criterion 1: mean difference up to 5 mmHg

# Two sided 95 % quantiles of Student's t by degrees of freedom (standard table).
T_975 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365,
         8: 2.306, 9: 2.262, 10: 2.228, 11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145,
         15: 2.131, 16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086, 21: 2.080,
         22: 2.074, 23: 2.069, 24: 2.064, 25: 2.060, 26: 2.056, 27: 2.052, 28: 2.048,
         29: 2.045, 30: 2.042}


def t975(df):
    if df not in T_975:
        raise SystemExit(f"no t quantile for {df} degrees of freedom; extend T_975 from a table")
    return T_975[df]


def app_rule(sys_, dia):
    """The rule the app is hypothesized to use: AHA/ACC categories applied to ONE reading."""
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
    half = t975(n - 1) * statistics.stdev(day_means) / n ** 0.5
    return m, m - half, m + half


def protocol_summary(rows, skip_first_day):
    days = {}
    for r in rows:
        if r["Note"] != "protocol":
            continue
        d = date.fromisoformat(r["Date"])
        if skip_first_day and d == PROTOCOL_FIRST_DAY:
            continue
        session = "am" if int(r["Time"][:2]) < 12 else "pm"
        days.setdefault(d, {}).setdefault(session, []).append((int(r["SYS (mmHg)"]), int(r["DIA (mmHg)"])))
    complete = {d: v for d, v in days.items() if len(v) == SESSIONS_PER_DAY}
    if len(complete) < MIN_COMPLETE_DAYS:
        raise SystemExit(f"only {len(complete)} complete days; plan requires {MIN_COMPLETE_DAYS}")
    readings = [x for v in complete.values() for s in v.values() for x in s]
    sys_day = [statistics.mean(s for sess in v.values() for s, _ in sess) for v in complete.values()]
    dia_day = [statistics.mean(d for sess in v.values() for _, d in sess) for v in complete.values()]
    return {"days": len(complete), "incomplete_days": len(days) - len(complete),
            "readings": len(readings), "sys": mean_ci(sys_day), "dia": mean_ci(dia_day)}


def decide(summary, threshold):
    """Three outcomes; hypertension range if systolic OR diastolic is at or above."""
    (s, s_lo, s_hi), (d, d_lo, d_hi) = summary["sys"], summary["dia"]
    t_sys, t_dia = threshold
    if s_lo >= t_sys or d_lo >= t_dia:
        return "supported"
    if s_hi < t_sys and d_hi < t_dia:
        return "rejected"
    return "inconclusive"


def run():
    raw = load()
    rows, duplicates = deduplicate(raw)
    assert len(duplicates) == EXPECTED_DUPLICATES, f"expected {EXPECTED_DUPLICATES} duplicates, found {len(duplicates)}"
    for r in rows:
        r["key"] = f"{r['Date']} {r['Time']}"
    validate_extract(rows, EXPECTED_RAW_ROWS - EXPECTED_DUPLICATES, key_field="key")
    excluded = [r for r in rows if r["Note"] in EXCLUDE_NOTES]
    assert len(excluded) == EXPECTED_EXCLUDED, f"expected {EXPECTED_EXCLUDED} excluded, found {len(excluded)}"
    rows = [r for r in rows if r["Note"] not in EXCLUDE_NOTES]

    # Safety first (METHOD section 5): every single value against the alarm limit.
    alarm_hits = [r for r in rows if int(r["SYS (mmHg)"]) > ALARM[0] or int(r["DIA (mmHg)"]) > ALARM[1]]

    label_matches = sum(app_rule(int(r["SYS (mmHg)"]), int(r["DIA (mmHg)"])) == r["Category"] for r in rows)

    primary = protocol_summary(rows, skip_first_day=True)
    sensitivity = protocol_summary(rows, skip_first_day=False)

    esc = FRAMEWORKS["esc_2024"]["hypertension"]
    aha = FRAMEWORKS["aha_acc"]["stage1"]

    adhoc = [r for r in rows if r["Note"] != "protocol"]
    hyper_labels = [r for r in adhoc if r["Category"].startswith("Stage")]
    adhoc_plain = [r for r in adhoc if r["Note"] == ""]
    adhoc_context = [r for r in adhoc if r["Note"] != ""]
    max_row = max(rows, key=lambda r: (int(r["SYS (mmHg)"]), int(r["DIA (mmHg)"])))
    max_dia_row = max(rows, key=lambda r: (int(r["DIA (mmHg)"]), int(r["SYS (mmHg)"])))

    def m(rs, col):
        return statistics.mean(int(r[col]) for r in rs)

    comparisons = len(rows) + 2 * 2 * 2  # every reading vs alarm; 2 frameworks x sys/dia x primary/sensitivity

    return [
        ("raw_rows", len(raw)),
        ("duplicates_removed", len(duplicates)),
        ("excluded_cuff_loose", len(excluded)),
        ("analysed_rows", len(rows)),
        ("readings_above_alarm_180_120", len(alarm_hits)),
        ("app_label_matches_rule_per_reading", f"{label_matches}/{len(rows)}"),
        ("protocol_complete_days_primary", primary["days"]),
        ("protocol_incomplete_days_primary", primary["incomplete_days"]),
        ("protocol_readings_primary", primary["readings"]),
        ("primary_mean_sys", round(primary["sys"][0], 1)),
        ("primary_sys_ci95_low", round(primary["sys"][1], 1)),
        ("primary_sys_ci95_high", round(primary["sys"][2], 1)),
        ("primary_mean_dia", round(primary["dia"][0], 1)),
        ("primary_dia_ci95_low", round(primary["dia"][1], 1)),
        ("primary_dia_ci95_high", round(primary["dia"][2], 1)),
        ("decision_esc_2024_home_135_85", decide(primary, esc)),
        ("decision_aha_acc_home_130_80", decide(primary, aha)),
        ("margin_to_esc_sys_upper", round(esc[0] - primary["sys"][2], 1)),
        ("margin_to_esc_dia_upper", round(esc[1] - primary["dia"][2], 1)),
        ("margin_to_aha_sys_upper", round(aha[0] - primary["sys"][2], 1)),
        ("margin_to_aha_dia_upper", round(aha[1] - primary["dia"][2], 1)),
        ("device_mean_error_allowed_by_iso", DEVICE_MEAN_ERROR_ALLOWED),
        ("sensitivity_all7_mean_sys", round(sensitivity["sys"][0], 1)),
        ("sensitivity_all7_mean_dia", round(sensitivity["dia"][0], 1)),
        ("sensitivity_all7_decision_esc", decide(sensitivity, esc)),
        ("sensitivity_all7_decision_aha", decide(sensitivity, aha)),
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
        ("comparisons_against_a_reference", comparisons),
    ]


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
