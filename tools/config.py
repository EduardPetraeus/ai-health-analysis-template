"""Read config.yaml without third party packages.

Scripts call `data_path()` instead of hard coding a path (DATA.md section 4).
Supports the small subset of YAML that config.example.yaml uses:
`key: value` lines and lists of `- item`, with `#` comments.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config.yaml"


def _strip_comment(value):
    # A # starts a comment unless it is inside quotes.
    out, quote = [], None
    for ch in value:
        if ch in "'\"":
            quote = None if quote == ch else (quote or ch)
        if ch == "#" and quote is None:
            break
        out.append(ch)
    return "".join(out).strip().strip("'\"")


def load(path=CONFIG):
    """Return config.yaml as a dict of strings and lists. Empty dict if missing."""
    if not path.exists():
        return {}
    data, current = {}, None
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        item = re.match(r"^\s*-\s+(.*)$", raw)
        if item and current is not None:
            value = _strip_comment(item.group(1))
            if value:
                data.setdefault(current, []).append(value)
            continue
        pair = re.match(r"^([A-Za-z_][\w]*)\s*:\s*(.*)$", raw)
        if pair:
            key, value = pair.group(1), _strip_comment(pair.group(2))
            if value.startswith("[") and value.endswith("]"):
                data[key] = [_strip_comment(v) for v in value[1:-1].split(",") if v.strip()]
                current = None
            elif value:
                data[key] = value
                current = None
            else:
                data[key] = []
                current = key
    return data


def data_path():
    """The owner's data folder from config.yaml, with ~ expanded."""
    value = load().get("data_path")
    if not value or isinstance(value, list):
        raise SystemExit("config.yaml has no data_path. Run the setup in START_HERE.md.")
    return Path(value).expanduser()


def private_terms():
    terms = load().get("private_terms", [])
    return [terms] if isinstance(terms, str) else list(terms)
