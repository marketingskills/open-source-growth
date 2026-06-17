#!/usr/bin/env python3
"""
star_repo.py — Check if gh CLI is available and optionally star a repo.

Usage:
    python star_repo.py marketingskills/seo

Checks gh availability, asks for confirmation, and stars the repo.
Logs to .repo-growth/social-proof.jsonl.
"""

import sys
import json
import os
import subprocess
from datetime import datetime


LOG_DIR = ".repo-growth"
LOG_FILE = os.path.join(LOG_DIR, "social-proof.jsonl")


def log_action(action, repo, result, note=""):
    os.makedirs(LOG_DIR, exist_ok=True)
    entry = {
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "action": action,
        "repo": repo,
        "result": result,
        "note": note,
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")


def has_gh():
    try:
        subprocess.run(["gh", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def gh_auth_status():
    try:
        result = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def star_repo(owner, repo):
    """Star a repo via gh CLI."""
    full_name = f"{owner}/{repo}"
    try:
        result = subprocess.run(
            ["gh", "api", "-X", "PUT", f"/user/starred/{full_name}"],
            capture_output=True, text=True
        )
        if result.returncode == 0 or "204" in result.stderr or result.stderr == "":
            return True, "Starred successfully"
        else:
            return False, result.stderr.strip()
    except Exception as e:
        return False, str(e)


def main():
    if len(sys.argv) < 2:
        print("Usage: python star_repo.py <owner/repo>", file=sys.stderr)
        sys.exit(1)

    repo_input = sys.argv[1].strip()
    if "/" not in repo_input:
        print("Error: Format as owner/repo", file=sys.stderr)
        sys.exit(1)

    owner, repo = repo_input.split("/", 1)

    if not has_gh():
        print("gh CLI not found. Install it: https://cli.github.com/")
        log_action("star", repo_input, "skipped", "gh CLI not available")
        sys.exit(1)

    if not gh_auth_status():
        print("gh CLI found but not authenticated. Run: gh auth login")
        log_action("star", repo_input, "skipped", "gh not authenticated")
        sys.exit(1)

    print(f"Would you like to star {repo_input} on GitHub? [y/N] ", end="")
    try:
        response = input().strip().lower()
    except (EOFError, KeyboardInterrupt):
        response = "n"

    if response in ("y", "yes"):
        success, message = star_repo(owner, repo)
        if success:
            print(f"Starred {repo_input} successfully!")
            log_action("star", repo_input, "success", "User confirmed")
        else:
            print(f"Failed to star: {message}")
            log_action("star", repo_input, "failed", message)
    else:
        print("Skipped.")
        log_action("star", repo_input, "skipped", "User declined")


if __name__ == "__main__":
    main()
