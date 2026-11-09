#!/usr/bin/env python3
"""Build the mdBook sources from spec/ and text/, then run mdbook.

src/ is output: rebuilt from scratch on every run and listed in .gitignore.
"""

import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
TEXT = os.path.join(ROOT, "text")

SPEC_GROUPS = [
    ("Fondations", ["modele-de-donnees", "cycle-de-vie", "idempotence"]),
    ("Protocole", ["api-paiements", "capacites", "webhooks", "authentification"]),
    ("Conformité", ["conformite", "matrice-de-conformite"]),
    ("Document informatif", ["architecture"]),
]

SPEC_TITLES = {
    "modele-de-donnees": "Modèle de données",
    "cycle-de-vie": "Cycle de vie et relevés",
    "idempotence": "Idempotence",
    "api-paiements": "API et erreurs",
    "capacites": "Capacités et plafonds",
    "webhooks": "Webhooks",
    "authentification": "Authentification",
    "conformite": "Conformité et serveur simulé",
    "matrice-de-conformite": "Matrice de conformité",
    "architecture": "Architecture et adaptateurs",
}

ADR = re.compile(r"^(\d{4})-.+\.md$")
ADR_TITLE = re.compile(r"^# ADR-\d{4} : (.+)$", re.M)


def adr_entries():
    entries = []
    for name in sorted(os.listdir(TEXT)):
        match = ADR.match(name)
        if not match:
            continue
        with open(os.path.join(TEXT, name), encoding="utf-8") as f:
            title = ADR_TITLE.search(f.read()).group(1)
        entries.append(f"- [{match.group(1)} {title}](text/{name})")
    return entries


def summary():
    lines = ["[Introduction](introduction.md)", "", "# Spécification", "",
             "- [Conventions](spec/README.md)"]
    for group, names in SPEC_GROUPS:
        lines.append(f"- [{group}]()")
        lines += [f"  - [{SPEC_TITLES[n]}](spec/{n}.md)" for n in names]
    lines += ["", "# Décisions", ""] + adr_entries()
    lines += ["", "---", "", "[Références](text/references.md)", ""]
    return "\n".join(lines)


def main():
    shutil.rmtree(SRC, ignore_errors=True)
    os.mkdir(SRC)
    for folder in ("spec", "text"):
        os.symlink(os.path.join(ROOT, folder), os.path.join(SRC, folder))
    shutil.copyfile(os.path.join(ROOT, "README.md"), os.path.join(SRC, "introduction.md"))

    with open(os.path.join(SRC, "SUMMARY.md"), "w", encoding="utf-8") as out:
        out.write(summary())

    result = subprocess.run(["mdbook", "build"], cwd=ROOT)
    if result.returncode != 0:
        sys.exit(result.returncode)
    print(f"{len(adr_entries())} ADR, {sum(len(n) for _, n in SPEC_GROUPS)} documents de spécification")


if __name__ == "__main__":
    main()
