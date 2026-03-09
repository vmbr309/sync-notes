#!/usr/bin/env python3

"""
notes-sync

a simple script for syncing a notes repo with git, for personal use. Coded (for now) with LLM help.

Variables are stored using Charmbracelet Skate.

//vmbr

"""

from pathlib import Path
import subprocess
import datetime
import argparse

# defining colors

GREEN = "\033[92m"
BLUE = "\033[94m"
RED = "\033[91m"
RESET = "\033[0m"


def skate_get(key: str, default: str | None = None) -> str | None:
    """Retrieve envvars from Skate."""
    try:
        result = subprocess.run(
            ["skate", "get", key], capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return default


def run(cmd: list[str], check: bool = True) -> None:
    """Execute and print a shell command."""
    print(f"{BLUE}Running:{RESET}", " ".join(cmd))

    try:
        subprocess.run(cmd, check=check, text=True)

    except subprocess.CalledProcessError as e:
        print(f"{RED}Command failed: {RESET} {' '.join(cmd)}")
        print(f"{RED}Exit code:{RESET}", e.returncode)
        exit(e.returncode)


def git(repo: Path, *args: str, check: bool = True) -> None:
    """Run a git command inside the repository"""
    cmd = ["git", "-C", str(repo), *args]
    run(cmd, check=check)


def repo_has_changes(repo: Path) -> bool:
    """Return true if the repository contains uncommitted changes."""
    result = subprocess.run(
        ["git", "-C", str(repo), "status", "--porcelain"],
        capture_output=True,
        text=True,
    )

    return bool(result.stdout.strip())


def main() -> None:
    print(f"{BLUE}Syncing notes repository...{RESET}")
    parser = argparse.ArgumentParser(
        description="Synchronize a notes repository using Git."
    )

    parser.add_argument(
        "repo", nargs="?", help="Path to the repository (overrides Skate config)"
    )

    parser.add_argument("-m", "--message", help="Custom commit message")

    args = parser.parse_args()

    repo_path = args.repo or skate_get("NOTES_REPO")
    repo = Path(repo_path)

    if not repo.is_dir():
        print(f"{RED}ERROR: Repo path is invalid:{RESET} {repo}")
        exit(1)

    base_msg = args.message or skate_get("NOTES_COMMIT_MSG", "notes sync")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    msg = f"{base_msg} - {timestamp}"

    git(repo, "pull")

    if repo_has_changes(repo):
        git(repo, "add", ".")
        git(repo, "commit", "-m", msg)
        git(repo, "push")

        print(f"{GREEN}☑︎ Notes synced successfully{RESET}")

    else:
        print(f"{GREEN}☑︎ No changes detected. Repo already up to date.{RESET}")


if __name__ == "__main__":
    main()
