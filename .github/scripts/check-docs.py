#!/usr/bin/env python3
"""Check Blaze documentation naming, language parity, and relative links."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
EXTERNAL_PREFIXES = (
    "http://",
    "https://",
    "mailto:",
    "tel:",
    "data:",
    "#",
)
INVALID_CHINESE_SUFFIX = re.compile(r"(?:_CN|_cn|-CN|-cn)\.md$|\.zh\.md$")
IGNORED_DIRECTORIES = {".git", "target"}


def markdown_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*.md")
        if not any(part in IGNORED_DIRECTORIES for part in path.parts)
    )


def check_names(files: list[Path], root: Path) -> list[str]:
    return [
        f"{path.relative_to(root)}: Chinese documents must use the _zh.md suffix"
        for path in files
        if INVALID_CHINESE_SUFFIX.search(path.name)
    ]


def check_root_pairs(root: Path) -> list[str]:
    errors: list[str] = []
    for english, chinese in (("README.md", "README_zh.md"), ("CHANGELOG.md", "CHANGELOG_zh.md")):
        if not (root / english).is_file():
            errors.append(f"missing root document: {english}")
        if not (root / chinese).is_file():
            errors.append(f"missing root document: {chinese}")
    return errors


def check_adjacent_pairs(directory: Path, root: Path) -> list[str]:
    if not directory.is_dir():
        return []

    errors: list[str] = []
    for path in sorted(directory.rglob("*.md")):
        if path.name.endswith("_zh.md"):
            counterpart = path.with_name(f"{path.name[:-6]}.md")
        else:
            counterpart = path.with_name(f"{path.stem}_zh.md")
        if not counterpart.is_file():
            errors.append(
                f"{path.relative_to(root)}: missing language counterpart "
                f"{counterpart.relative_to(root)}"
            )
    return errors


def relative_markdown_tree(directory: Path) -> set[Path]:
    if not directory.is_dir():
        return set()
    return {path.relative_to(directory) for path in directory.rglob("*.md")}


def check_guide_parity(root: Path) -> list[str]:
    english_root = root / "docs/user-guide/en"
    chinese_root = root / "docs/user-guide/zh"
    english = relative_markdown_tree(english_root)
    chinese = relative_markdown_tree(chinese_root)

    errors = [
        f"docs/user-guide/en/{path}: missing docs/user-guide/zh/{path}"
        for path in sorted(english - chinese)
    ]
    errors.extend(
        f"docs/user-guide/zh/{path}: missing docs/user-guide/en/{path}"
        for path in sorted(chinese - english)
    )
    return errors


def strip_fenced_code(text: str) -> str:
    return re.sub(r"```.*?```|~~~.*?~~~", "", text, flags=re.DOTALL)


def check_links(files: list[Path], root: Path) -> list[str]:
    errors: list[str] = []
    for path in files:
        text = strip_fenced_code(path.read_text(encoding="utf-8", errors="replace"))
        for match in LINK_RE.finditer(text):
            target = match.group(1).strip("<>")
            if target.startswith(EXTERNAL_PREFIXES):
                continue

            path_part = unquote(target.split("#", 1)[0].split("?", 1)[0])
            if not path_part:
                continue

            resolved = (path.parent / path_part).resolve()
            try:
                resolved.relative_to(root)
            except ValueError:
                errors.append(
                    f"{path.relative_to(root)}: relative link leaves the repository: {target}"
                )
                continue

            if not resolved.exists():
                errors.append(f"{path.relative_to(root)}: broken relative link: {target}")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    files = markdown_files(root)
    errors: list[str] = []
    errors.extend(check_names(files, root))
    errors.extend(check_root_pairs(root))
    errors.extend(check_adjacent_pairs(root / "docs/design", root))
    errors.extend(check_guide_parity(root))
    errors.extend(check_links(files, root))

    if errors:
        print(f"Documentation checks failed with {len(errors)} error(s):")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Documentation checks passed for {len(files)} Markdown file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
