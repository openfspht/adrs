#!/usr/bin/env python3

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OWN_URL = re.compile(r"^https://github\.com/openfspht/adrs/(?:blob|tree)/main/")
LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
HEADING = re.compile(r"^#{1,6} (.+)$", re.M)
NUMBERED_RULE = re.compile(r"^\*\*(\d+(?:\.\d+)*)\.", re.M)
NUMBERED_HEADING = re.compile(r"^#{2,4} (\d+(?:\.\d+)*)\.", re.M)
SECTION = re.compile(r"§\s?(\d+(?:\.\d+)*)")
CODE_BLOCK = re.compile(r"```.*?```", re.S)


def documents() -> list[Path]:
    return [ROOT / "README.md", *sorted((ROOT / "spec").glob("*.md")), *sorted((ROOT / "text").glob("*.md"))]


def slug(heading: str) -> str:
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", heading.strip().lower())
    text = re.sub(r"[`*_]", "", text)
    return re.sub(r"[^\w\- ]", "", text).replace(" ", "-")


def anchors(path: Path) -> set[str]:
    return {slug(h) for h in HEADING.findall(CODE_BLOCK.sub("", path.read_text(encoding="utf-8")))}


def sections(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    return set(NUMBERED_RULE.findall(text)) | set(NUMBERED_HEADING.findall(text))


def resolve(source: Path, target: str) -> Path | None:
    if OWN_URL.match(target):
        return ROOT / OWN_URL.sub("", target)
    if target.startswith(("http://", "https://", "mailto:")):
        return None
    return (source.parent / target).resolve() if target else source


def check(source: Path) -> list[str]:
    errors = []
    text = " ".join(source.read_text(encoding="utf-8").split())
    for label, url in LINK.findall(text):
        target, _, anchor = url.partition("#")
        path = resolve(source, target)
        if path is None:
            continue
        where = f"{source.relative_to(ROOT)}: [{label}]({url})"
        if not path.exists():
            errors.append(f"{where}: missing target")
            continue
        if path.suffix != ".md":
            continue
        if anchor and anchor not in anchors(path):
            errors.append(f"{where}: missing anchor")
        known = sections(path)
        errors += [f"{where}: missing §{number}" for number in SECTION.findall(label) if number not in known]
    return errors


def main() -> None:
    errors = [error for path in documents() for error in check(path)]
    print("\n".join(errors) or f"{len(documents())} documents, all links resolve")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
