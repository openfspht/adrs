#!/usr/bin/env python3
"""Build the mdBook sources from text/ and run mdbook.

src/ is output: it is rebuilt from scratch every run and is in .gitignore. The
ADRs live in text/ and are never written to from here.
"""

import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
TEXT = os.path.join(ROOT, "text")
SRC = os.path.join(ROOT, "src")

GROUPS = [
    ("Introduction", ["0001"]),
    ("Fondations", ["0002", "0003", "0004", "0005"]),
    ("Le protocole", ["0006", "0007", "0008", "0009", "0010"]),
    ("Paiement de proximité", ["0011", "0012"]),
    ("Implémentation", ["0013", "0014", "0015"]),
    ("Processus", ["0016"]),
]

SHORT = {
    "0001": "Architecture et périmètre",
    "0002": "Modèle de données",
    "0003": "Cycle de vie",
    "0004": "Idempotence",
    "0005": "Taxonomie des erreurs",
    "0006": "API HTTP",
    "0007": "Découverte de capacités",
    "0008": "Webhooks",
    "0009": "Authentification",
    "0010": "ISO 20022",
    "0011": "Demandes de confirmation",
    "0012": "Paiement de proximité",
    "0013": "Adaptateurs",
    "0014": "Serveur simulé",
    "0015": "Conformité",
    "0016": "Marques et nom",
}

ADR = re.compile(r"^\d{4}-.+\.md$")


def link(source, name):
    target = os.path.join(SRC, name)
    if not os.path.exists(target):
        os.symlink(source, target)


def write_introduction():
    # README links point into text/ for GitHub; in the book the ADRs sit beside it.
    with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as f:
        readme = f.read()
    with open(os.path.join(SRC, "introduction.md"), "w", encoding="utf-8") as out:
        out.write(readme.replace("](text/", "]("))


def main():
    shutil.rmtree(SRC, ignore_errors=True)
    os.mkdir(SRC)

    files = sorted(f for f in os.listdir(TEXT) if ADR.match(f))

    for name in files + ["references.md"]:
        source = os.path.join(TEXT, name)
        if os.path.exists(source):
            link(source, name)
    write_introduction()

    summary = ["[Introduction](introduction.md)", ""]
    for title, numbers in GROUPS:
        chapters = [next((f for f in files if f.startswith(n)), None) for n in numbers]
        chapters = [(n, f) for n, f in zip(numbers, chapters) if f]
        if not chapters:
            continue
        summary += [f"# {title}", ""]
        summary += [f"- [{n} {SHORT[n]}]({f})" for n, f in chapters]
        summary.append("")
    summary += ["---", "", "[Références](references.md)", ""]

    with open(os.path.join(SRC, "SUMMARY.md"), "w", encoding="utf-8") as out:
        out.write("\n".join(summary))

    result = subprocess.run(["mdbook", "build"], cwd=ROOT)
    if result.returncode != 0:
        sys.exit(result.returncode)
    print(f"{len(files)} ADR")


if __name__ == "__main__":
    main()
