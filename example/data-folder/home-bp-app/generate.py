#!/usr/bin/env python3
"""Generate the SYNTHETIC home blood pressure export used by the example.

No real person's data. Every value comes from a seeded random generator, so everyone
who runs this gets the same file, byte for byte.

  python3 example/data-folder/home-bp-app/generate.py           write raw/export-2026-11-18.csv
  python3 example/data-folder/home-bp-app/generate.py --check   verify the committed file

The file imitates a typical consumer app export:
  * 2026-09-01 to 2026-11-07: ad hoc single readings at random times, some with
    context notes ("after coffee", "stressful day", "just got home"), which raise
    the reading;
  * 2026-11-08 to 2026-11-14: a protocol week, two readings morning and evening
    after 5 minutes of seated rest, noted "protocol". Day 1 runs a little higher;
  * the app labels EACH reading with a category using office blood pressure cut
    points;
  * two rows are duplicated by an app sync, and one reading is noted "cuff loose".
"""

import csv
import hashlib
import io
import random
import sys
from datetime import date, timedelta
from pathlib import Path

SEED = 20261119
OUT = Path(__file__).resolve().parent / "raw" / "export-2026-11-18.csv"
HEADER = ["Date", "Time", "SYS (mmHg)", "DIA (mmHg)", "Pulse (bpm)", "Category", "Note"]

# The synthetic person's "true" home blood pressure, measured properly.
TRUE_SYS, TRUE_DIA = 126.0, 78.0
NOISE_SYS, NOISE_DIA = 6.0, 4.0
CONTEXT = {  # added to a reading taken in this context
    "": (0.0, 0.0),
    "after coffee": (7.0, 4.0),
    "stressful day": (5.0, 3.0),
    "just got home": (9.0, 4.0),
}
DAY1_EFFECT = (3.0, 1.5)


def app_category(sys_, dia):
    """How the fictional app labels a single reading (office cut points)."""
    if sys_ >= 140 or dia >= 90:
        return "Stage 2 Hypertension"
    if sys_ >= 130 or dia >= 80:
        return "Stage 1 Hypertension"
    if sys_ >= 120:
        return "Elevated"
    return "Normal"


def reading(rng, extra_sys=0.0, extra_dia=0.0, evening=False):
    s = TRUE_SYS + (2.0 if evening else 0.0) + extra_sys + rng.gauss(0, NOISE_SYS)
    d = TRUE_DIA + extra_dia + rng.gauss(0, NOISE_DIA)
    p = 66 + rng.gauss(0, 5)
    return round(s), round(d), round(p)


def build_rows():
    rng = random.Random(SEED)
    rows = []
    day = date(2026, 9, 1)
    while day <= date(2026, 11, 7):
        if rng.random() < 0.72:  # most days have one ad hoc reading
            hour = rng.randint(6, 22)
            minute = rng.randint(0, 59)
            note = rng.choices(list(CONTEXT), weights=[55, 20, 12, 13])[0]
            if note == "just got home":
                hour = 16 + hour % 5
            s, d, p = reading(rng, *CONTEXT[note], evening=hour >= 17)
            rows.append([day.isoformat(), f"{hour:02d}:{minute:02d}", s, d, p,
                         app_category(s, d), note])
        day += timedelta(days=1)

    for i in range(7):  # protocol week
        day = date(2026, 11, 8) + timedelta(days=i)
        extra = DAY1_EFFECT if i == 0 else (0.0, 0.0)
        for hour, minute, evening in ((7, 5, False), (21, 30, True)):
            for k in range(2):
                s, d, p = reading(rng, *extra, evening=evening)
                rows.append([day.isoformat(), f"{hour:02d}:{minute + k:02d}", s, d, p,
                             app_category(s, d), "protocol"])

    # Data quirks a careful analysis must catch.
    rows.insert(12, list(rows[11]))  # app sync duplicate
    rows.insert(30, list(rows[29]))  # app sync duplicate
    rows.insert(40, ["2026-10-17", "18:40", 98, 61, 70, app_category(98, 61), "cuff loose"])
    rows.sort(key=lambda r: (r[0], r[1]))  # stable: duplicates stay adjacent
    return rows


def render(rows):
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(HEADER)
    writer.writerows(rows)
    return buffer.getvalue()


def main(argv):
    text = render(build_rows())
    if "--check" in argv:
        committed = OUT.read_text(encoding="utf-8")
        same = hashlib.sha256(text.encode()).hexdigest() == hashlib.sha256(committed.encode()).hexdigest()
        print("generate.py --check:", "OK, committed file matches the generator" if same else "MISMATCH")
        return 0 if same else 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.name}: {text.count(chr(10)) - 1} rows, sha256 {hashlib.sha256(text.encode()).hexdigest()[:16]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
