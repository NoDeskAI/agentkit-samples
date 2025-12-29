# pip install python-frontmatter
from typing import Any
from pathlib import Path
import argparse
import subprocess
import sys
import frontmatter


def check_name(metadata: dict[str, Any]):
    name = metadata.get("name")
    if not name:
        raise ValueError("name is required")


def check_description(metadata: dict[str, Any]):
    description = metadata.get("description")
    if not description:
        raise ValueError("description is required")


def check_senarios(metadata: dict[str, Any]):
    senarios = metadata.get("senarios")
    if not senarios:
        raise ValueError("senarios is required")
    if len(senarios) != 4:
        raise ValueError("senarios should have 4 items")


def check_components(metadata: dict[str, Any]):
    standard_components = ["Identity", "MCP Toolset"]
    components = metadata.get("components")
    if not components:
        raise ValueError("components is required")
    if len(components) == 0:
        raise ValueError("components should have at least 1 item")
    for component in components:
        name = component.get("name")
        if not name:
            raise ValueError("component name is required")
        desc = component.get("desc")
        if not desc:
            raise ValueError("component desc is required")
        if component["name"] not in standard_components:
            raise ValueError(f"component name should be one of {standard_components}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="*")
    args = parser.parse_args(argv)

    if not args.files:
        post = frontmatter.load("README.md")
        check_name(post.metadata)
        check_description(post.metadata)
        check_senarios(post.metadata)
        check_components(post.metadata)
        return 0

    repo_root = Path(__file__).resolve().parent.parent
    use_cases_dir = repo_root / "02-use-cases"

    diff_commands = [
        ["git", "diff", "--name-only", "--diff-filter=ACMRT"],
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMRT"],
    ]

    changed_files: set[str] = set()
    for cmd in diff_commands:
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(repo_root),
        )
        changed_files.update(
            line.strip() for line in completed.stdout.splitlines() if line.strip()
        )

    failed = False

    for file_path in args.files:
        path = Path(file_path).resolve()
        try:
            rel = path.relative_to(repo_root)
        except ValueError:
            continue

        if path.name.lower() != "readme.md":
            continue

        if use_cases_dir not in path.parents:
            continue

        if str(rel) not in changed_files:
            continue

        post = frontmatter.load(path)

        try:
            check_name(post.metadata)
            check_description(post.metadata)
            check_senarios(post.metadata)
            check_components(post.metadata)
        except ValueError as exc:
            sys.stderr.write(f"{rel}: {exc}\n")
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
