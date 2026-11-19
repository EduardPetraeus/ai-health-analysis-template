# Ontology: cardiovascular

| Concept `id` | Definition | Unit | Carried by |
|---|---|---|---|
| `cardiovascular.systolic_bp` | Peak arterial pressure during a heartbeat, as measured by a cuff | mmHg | `home-bp-app.reading.systolic_mmhg` |
| `cardiovascular.diastolic_bp` | Lowest arterial pressure between heartbeats, as measured by a cuff | mmHg | `home-bp-app.reading.diastolic_mmhg` |
| `cardiovascular.pulse_rate` | Heartbeats per minute during the measurement | bpm | `home-bp-app.reading.pulse_bpm` |

**Context that belongs to the concept, not the source:** whether a home reading and an
office reading share a threshold depends on the guideline. ESC 2024 uses 135/85 at home
and 140/90 in the office; AHA/ACC use 130/80 for both
([`knowledge/home-blood-pressure.md`](../../knowledge/home-blood-pressure.md)).
