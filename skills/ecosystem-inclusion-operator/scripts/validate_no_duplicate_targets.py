#!/usr/bin/env python3
"""
validate_no_duplicate_targets.py — Check .repo-growth/targets.yaml for duplicate entries.

Usage:
    python validate_no_duplicate_targets.py

Returns a report of any duplicates found or confirms clean state.
"""

import sys
import json
import os
import re


TARGETS_FILE = ".repo-growth/targets.yaml"


def load_targets():
    targets = []
    if not os.path.exists(TARGETS_FILE):
        print(json.dumps({"status": "no_file", "message": f"{TARGETS_FILE} not found"}))
        return targets

    with open(TARGETS_FILE) as f:
        content = f.read()

    current = {}
    for line in content.split("\n"):
        if line.startswith("  - repo:"):
            if current:
                targets.append(current)
            current = {"repo": line.split(":", 1)[1].strip().strip('"')}
        elif current:
            kv_match = re.match(r"\s+(\w+):\s*\"?(.*?)\"?$", line)
            if kv_match and kv_match.group(1) != "notes":
                current[kv_match.group(1)] = kv_match.group(2).strip().strip('"').strip("'")

    if current:
        targets.append(current)
    return targets


def main():
    targets = load_targets()

    if not targets:
        print(json.dumps({"status": "empty", "message": "No targets to validate"}))
        return

    seen = {}
    duplicates = []

    for t in targets:
        repo = t.get("repo", "").lower()
        if repo in seen:
            duplicates.append({
                "repo": repo,
                "first_entry": seen[repo],
                "second_entry": t,
                "status_first": seen.get("status", ""),
                "status_second": t.get("status", ""),
            })
        else:
            seen[repo] = t

    if duplicates:
        report = {
            "status": "duplicates_found",
            "total_targets": len(targets),
            "duplicate_count": len(duplicates),
            "duplicates": duplicates,
            "recommendation": "Use append_log.py to merge duplicate entries, then remove one from targets.yaml.",
        }
    else:
        report = {
            "status": "clean",
            "total_targets": len(targets),
            "duplicate_count": 0,
            "message": "No duplicate targets found.",
        }

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
