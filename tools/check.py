#!/usr/bin/env python3
"""check.py: keeps data and private terms out of commits, and the folder free of drift.

Usage:
  python3 tools/check.py                  check the working tree
  python3 tools/check.py --staged         check what is staged for commit (used by the hook)
  python3 tools/check.py --install-hook   install as a git pre-commit hook

Blocking checks (exit 1):
  1. Allowed files only: outside the example, only text file types the method uses
     (.md, .py, .yaml, .yml and a few named files) may be committed. Everything else,
     including any data export, is refused (DATA.md section 1). config.yaml is refused.
  2. Size: nothing over 1 MB.
  3. Private terms: none of the terms in config.yaml under private_terms, in file
     contents or file names, also across line breaks.
  4. Index: every folder has a README.md that names each file and subfolder in it.
  5. Links: every relative Markdown link points to an existing file and heading.

Warnings (exit 0):
  6. Status files whose owner confirmation is missing, invalid or expired, and baseline
     facts in status/health-status.md stated more than 365 days ago.

Standard library only. It reports; it never changes a file.
"""

import re
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import config  # noqa: E402

ROOT = config.ROOT

ALLOWED_SUFFIXES = {".md", ".py", ".yaml", ".yml"}
ALLOWED_NAMES = {"LICENSE", ".gitignore"}
# The only data files allowed anywhere: the example's synthetic data, by exact path.
ALLOWED_DATA_FILES = {
    "example/data-folder/home-bp-app/raw/export-2026-11-18.csv",
    "example/data-folder/analyses/2026-11-19_home-bp-app-flag/results.csv",
}
NEVER_COMMIT = {"config.yaml"}
MAX_BYTES = 1_000_000
SKIP_DIRS = {".git", "__pycache__", ".venv", "node_modules"}
README_EXEMPT_DIRS = {".github", ".github/workflows"}
ROOT_EXEMPT_FILES = {".gitignore", "README.md"}
TERM_SCAN_EXEMPT = {"config.example.yaml"}


# ---------------------------------------------------------------- helpers

def git(*args):
    try:
        result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True)
    except FileNotFoundError:
        return None
    if result.returncode != 0:
        return None
    return result.stdout.decode("utf-8", errors="replace")


def candidate_files(staged):
    """Relative paths that are, or would be, committed. NUL separated, so any name works."""
    if staged:
        out = git("diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z")
        return sorted(p for p in (out or "").split("\0") if p)
    out = git("ls-files", "--cached", "--others", "--exclude-standard", "-z")
    if out is not None:
        return sorted(p for p in out.split("\0") if p and (ROOT / p).exists())
    # No git (for example a ZIP download): walk the folder, skipping hidden system files.
    files = []
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts) or path.name in {".DS_Store", "config.yaml"}:
            continue
        if path.is_file():
            files.append(rel.as_posix())
    return sorted(files)


def read_text(rel, staged):
    if staged:
        return git("show", f":{rel}") or ""
    try:
        return (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def github_slug(heading):
    """GitHub's heading anchor: lowercase, punctuation removed, spaces to hyphens."""
    text = heading.strip().lower()
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[`*]", "", text)
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def fence_toggle(line):
    stripped = line.strip()
    return stripped.startswith("```") or stripped.startswith("~~~")


def anchors_in(path):
    anchors, seen, in_code = set(), {}, False
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if fence_toggle(line):
            in_code = not in_code
            continue
        heading = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if heading and not in_code:
            slug = github_slug(heading.group(1))
            count = seen.get(slug, 0)
            anchors.add(slug if count == 0 else f"{slug}-{count}")
            seen[slug] = count + 1
    return anchors


# ---------------------------------------------------------------- checks

def check_allowed_and_size(files):
    problems = []
    for rel in files:
        name = Path(rel).name
        if rel in NEVER_COMMIT:
            problems.append(f"{rel} must never be committed (it holds your private terms)")
            continue
        allowed = (rel in ALLOWED_DATA_FILES or name in ALLOWED_NAMES
                   or Path(rel).suffix.lower() in ALLOWED_SUFFIXES)
        if not allowed:
            problems.append(f"not an allowed file type (data belongs in your data folder): {rel}")
        path = ROOT / rel
        if path.exists() and path.stat().st_size > MAX_BYTES:
            problems.append(f"file over 1 MB: {rel}")
    return problems


def term_pattern(term):
    words = [re.escape(w) for w in term.split()]
    body = r"\s+".join(words)
    start = r"\b" if re.match(r"\w", term) else ""
    end = r"\b" if re.search(r"\w$", term) else ""
    return re.compile(start + body + end, re.IGNORECASE)


def check_private_terms(files, staged):
    terms = config.private_terms()
    if not terms:
        return [], "no private_terms in config.yaml (add your name and IDs there)"
    patterns = [(i + 1, term_pattern(t)) for i, t in enumerate(terms)]
    problems = []
    for rel in files:
        if rel in TERM_SCAN_EXEMPT or rel in NEVER_COMMIT:
            continue
        for number, rx in patterns:
            if rx.search(rel):
                problems.append(f"private term #{number} in the file name {rel}")
        text = read_text(rel, staged)
        for number, rx in patterns:
            match = rx.search(text)
            if match:
                line = text.count("\n", 0, match.start()) + 1
                problems.append(f"private term #{number} in {rel}:{line}")
    return problems, None


def readme_tokens(text):
    """Names a README refers to: backticked text and link targets."""
    tokens = set()
    text = re.sub(r"(?ms)^\s*(```|~~~).*?^\s*\1", "", text)  # drop fenced code blocks
    for code in re.findall(r"`([^`]+)`", text):
        tokens.add(code.strip().rstrip("/"))
    for target in re.findall(r"\]\(([^)\s#]+)", text):
        parts = target.rstrip("/").split("/")
        tokens.add(parts[-1])
        tokens.add(target.rstrip("/"))
        if parts[-1] == "README.md" and len(parts) > 1:
            tokens.add(parts[-2])  # a link to name/README.md names the folder
    return tokens


def check_index(files):
    problems = []
    file_set = set(files)
    dirs = set()
    for rel in files:
        parent = Path(rel).parent
        while parent.as_posix() != ".":
            dirs.add(parent.as_posix())
            parent = parent.parent
    for d in sorted(dirs):
        if d in README_EXEMPT_DIRS:
            continue
        readme = f"{d}/README.md"
        if readme not in file_set:
            problems.append(f"folder without README.md: {d}/")
            continue
        tokens = readme_tokens((ROOT / readme).read_text(encoding="utf-8", errors="ignore"))
        children = {Path(f).relative_to(d).parts[0] for f in files if f.startswith(d + "/")}
        for child in sorted(children - {"README.md"}):
            if child not in tokens:
                problems.append(f"{child} not named in {readme} (name it in backticks or a link)")
    tokens = readme_tokens((ROOT / "README.md").read_text(encoding="utf-8", errors="ignore"))
    for rel in files:
        if "/" not in rel and rel not in ROOT_EXEMPT_FILES and rel not in tokens:
            problems.append(f"root file {rel} not named in README.md")
    return problems


def check_links(files):
    problems = []
    link_rx = re.compile(r"(?<!!)\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
    for rel in files:
        if not rel.endswith(".md"):
            continue
        source = ROOT / rel
        if not source.exists():
            continue
        in_code = False
        for n, line in enumerate(source.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            if fence_toggle(line):
                in_code = not in_code
                continue
            if in_code:
                continue
            line = re.sub(r"`[^`]*`", "", line)  # links inside inline code are not links
            targets = link_rx.findall(line)
            definition = re.match(r"^\s{0,3}\[[^\]]+\]:\s*<?([^\s>]+)>?", line)
            if definition:  # reference style link: [name]: target
                targets.append(definition.group(1))
            for target in targets:
                if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
                    continue
                path_part, _, anchor = target.partition("#")
                dest = source if not path_part else (source.parent / path_part).resolve()
                if not dest.exists():
                    problems.append(f"broken link in {rel}:{n} -> {target}")
                    continue
                if anchor and dest.is_file() and dest.suffix == ".md":
                    if anchor not in anchors_in(dest):
                        problems.append(f"missing heading in {rel}:{n} -> {target}")
    return problems


def check_status_freshness():
    warnings = []
    for path in sorted((ROOT / "status").glob("*.md")):
        if path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        rel = path.relative_to(ROOT).as_posix()
        confirmed = re.search(r"\*\*Last confirmed by owner:\*\*[ \t]*(\S*)", text)
        valid = re.search(r"\*\*Valid for:\*\*\s*(\d+)", text)
        value = confirmed.group(1) if confirmed else ""
        if not value:
            warnings.append(f"{rel}: not yet confirmed by the owner; facts here may not carry an analysis")
            continue
        try:
            confirmed_on = date.fromisoformat(value)
        except ValueError:
            warnings.append(f"{rel}: confirmation date {value!r} is not YYYY-MM-DD")
            continue
        if not valid:
            warnings.append(f"{rel}: no **Valid for:** line")
            continue
        age, limit = (date.today() - confirmed_on).days, int(valid.group(1))
        if age > limit:
            warnings.append(f"{rel}: confirmed {age} days ago, valid for {limit}; confirm before use")
    warnings += check_baseline_fields()
    return warnings


BASELINE_FIELD_DAYS = 365  # stated in status/health-status.md, section Baseline facts


def check_baseline_fields():
    """Each baseline fact carries its own date in the last column; warn when it is old."""
    path = ROOT / "status" / "health-status.md"
    if not path.exists():
        return []
    warnings, in_section = [], False
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if line.startswith("## "):
            in_section = line.strip().lower().startswith("## baseline facts")
            continue
        if not in_section or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or not cells[1]:
            continue
        stated = re.match(r"^\d{4}-\d{2}-\d{2}$", cells[-1])
        if not stated:
            continue
        try:
            age = (date.today() - date.fromisoformat(cells[-1])).days
        except ValueError:
            warnings.append(f"status/health-status.md: {cells[0]} has an invalid date {cells[-1]!r}")
            continue
        if age > BASELINE_FIELD_DAYS:
            warnings.append(f"status/health-status.md: {cells[0]} stated {age} days ago; confirm before use")
    return warnings


# ---------------------------------------------------------------- main

HOOK_MARKER = "# installed by tools/check.py"


def install_hook(force):
    hooks = ROOT / ".git" / "hooks"
    if not hooks.exists():
        print("No .git folder: this copy was not cloned with git, so there is no commit to")
        print("protect. Nothing to install; run `python3 tools/check.py` by hand before sharing.")
        return 0
    hook = hooks / "pre-commit"
    if hook.exists() and HOOK_MARKER not in hook.read_text(errors="ignore") and not force:
        print(f"{hook.relative_to(ROOT)} already exists and was not written by check.py.")
        print("Add `python3 tools/check.py --staged` to it yourself, or rerun with --force.")
        return 1
    hook.write_text(f'#!/bin/sh\n{HOOK_MARKER}\nexec "{sys.executable}" tools/check.py --staged\n',
                    encoding="utf-8")
    hook.chmod(0o755)
    print(f"Installed {hook.relative_to(ROOT)}. Every commit is now checked.")
    return 0


def main(argv):
    if "--install-hook" in argv:
        return install_hook("--force" in argv)
    staged = "--staged" in argv
    files = candidate_files(staged)
    all_files = candidate_files(False)

    blocking = check_allowed_and_size(files)
    term_problems, term_note = check_private_terms(files, staged)
    blocking += term_problems
    blocking += check_index(all_files)
    blocking += check_links(all_files)
    warnings = check_status_freshness()
    if term_note:
        warnings.append(term_note)

    for w in warnings:
        print(f"warning: {w}")
    for p in blocking:
        print(f"ERROR: {p}")
    if blocking:
        print(f"\n{len(blocking)} problem(s). Nothing was changed; fix and run again.")
        return 1
    print(f"check.py: OK ({len(files)} files checked, {len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
