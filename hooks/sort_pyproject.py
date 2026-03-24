#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path


def sort_array_section(text: str, section_name: str) -> str:
    # Matches:
    # dependencies = [
    #   "...",
    # ]
    pattern = re.compile(
        rf"(^\s*{re.escape(section_name)}\s*=\s*\[\s*\n)(.*?)(^\s*\])",
        re.MULTILINE | re.DOTALL,
    )

    def _repl(match: re.Match[str]) -> str:
        head = match.group(1)
        body = match.group(2)
        tail = match.group(3)

        lines = body.splitlines()
        # Keep non-empty logical lines, case-insensitive sort.
        items = [ln for ln in lines if ln.strip()]
        items_sorted = sorted(items, key=lambda s: s.lower())

        if items_sorted:
            return f"{head}" + "\n".join(items_sorted) + "\n" + tail
        return f"{head}{tail}"

    return pattern.sub(_repl, text)


def process_file(path: Path, sections: list[str]) -> tuple[bool, str, str]:
    original = path.read_text(encoding="utf-8")
    updated = original

    for section in sections:
        updated = sort_array_section(updated, section)

    changed = updated != original

    return changed, original, updated


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sort selected array sections in pyproject.toml."
    )
    parser.add_argument(
        "files",
        nargs="*",
        default=["pyproject.toml"],
        help="Files to process (default: pyproject.toml)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Do not write changes; exit non-zero if any file would change.",
    )
    parser.add_argument(
        "--sections",
        nargs="+",
        default=["dependencies", "dev"],
        help="Section names to sort (default: dependencies dev)",
    )
    parser.add_argument(
        "--diff",
        action="store_true",
        help="Print unified diff for changed files.",
    )

    args = parser.parse_args()

    had_changes = False
    for file_name in args.files:
        path = Path(file_name)
        if not path.exists():
            print(f"[sort-pyproject] Skipping missing file: {path}", file=sys.stderr)
            continue

        changed, original, updated = process_file(path, args.sections)
        if not changed:
            continue

        had_changes = True
        if args.diff:
            diff = difflib.unified_diff(
                original.splitlines(keepends=True),
                updated.splitlines(keepends=True),
                fromfile=str(path),
                tofile=str(path),
            )
            sys.stdout.writelines(diff)

        if not args.check:
            path.write_text(updated, encoding="utf-8")
            print(f"[sort-pyproject] Updated {path}")

    if args.check and had_changes:
        print("[sort-pyproject] Files need sorting.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
