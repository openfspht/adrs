#!/usr/bin/env python3

import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = ROOT / "spec"
MATRIX = SPEC / "matrice-de-conformite.md"
NORMATIVE = [
    "modele-de-donnees",
    "cycle-de-vie",
    "idempotence",
    "api-paiements",
    "capacites",
    "webhooks",
    "authentification",
    "conformite",
]
SUBJECTS = {"passerelle", "opérateur natif", "client", "serveur simulé", "suite", "exploitant", "déclarant", "spécification"}
VERIFICATIONS = {"test", "à écrire", "non testable", "sans objet"}
NEEDS_DETAIL = {"test", "non testable"}

RULE = re.compile(r"^\*\*(\d+(?:\.\d+)*)\.")
NUMBERED_HEADING = re.compile(r"^#{2,4} (\d+(?:\.\d+)*)\.")
ROW = re.compile(r"^\| \[(\d+(?:\.\d+)*)\]\(([a-z-]+)\.md\) \| ([^|]*) \| ([^|]*) \| ([^|]*) \|$")


def units(name: str) -> list[str]:
    found: list[str] = []
    heading: str | None = None
    in_code = False
    for line in (SPEC / f"{name}.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("```"):
            in_code = not in_code
        if in_code:
            continue
        if rule := RULE.match(line):
            found.append(rule.group(1))
            heading = None
        elif numbered := NUMBERED_HEADING.match(line):
            heading = numbered.group(1)
        elif line.startswith("#"):
            heading = None
        elif heading and line.strip():
            found.append(heading)
            heading = None
    return found


def matrix() -> tuple[dict[tuple[str, str, str], tuple[str, str]], list[str]]:
    rows: dict[tuple[str, str, str], tuple[str, str]] = {}
    errors: list[str] = []
    for number, line in enumerate(MATRIX.read_text(encoding="utf-8").splitlines(), 1):
        if not line.startswith("| ["):
            continue
        match = ROW.match(line)
        if not match:
            errors.append(f"line {number}: malformed row")
            continue
        section, name, subject, verification, detail = (part.strip() for part in match.groups())
        key = (name, section, subject)
        if key in rows:
            errors.append(f"line {number}: {name} {section} listed twice for {subject}")
        if subject not in SUBJECTS:
            errors.append(f"line {number}: unknown subject {subject!r}")
        if verification not in VERIFICATIONS:
            errors.append(f"line {number}: unknown verification {verification!r}")
        elif verification in NEEDS_DETAIL and not detail:
            errors.append(f"line {number}: {verification!r} needs a test or a reason")
        rows[key] = (verification, detail)
    return rows, errors


def main() -> None:
    expected = [(name, section) for name in NORMATIVE for section in units(name)]
    rows, errors = matrix()
    listed = {(name, section) for name, section, _ in rows}
    missing = [(name, section) for name, section in expected if (name, section) not in listed]
    if "--missing" in sys.argv:
        print("\n".join(f"| [{section}]({name}.md) | passerelle | à écrire |  |" for name, section in missing))
        return
    errors += [f"{name} {section}: missing from the matrix" for name, section in missing]
    errors += [f"{name} {section}: no such rule" for name, section in sorted(listed - set(expected))]
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    counts = Counter(verification for verification, _ in rows.values())
    print(f"{len(listed)} rules, {len(rows)} obligations: " + ", ".join(f"{counts[v]} {v}" for v in sorted(VERIFICATIONS)))


if __name__ == "__main__":
    main()
