#!/usr/bin/env python3
"""
render_progress_report.py — Render a progress report from .repo-growth logs.

Usage:
    python render_progress_report.py

Reads prs.jsonl and targets.yaml from .repo-growth/ and outputs a Markdown summary.
"""

import sys
import json
import os
from datetime import datetime, timedelta


LOG_DIR = ".repo-growth"
PRS_FILE = os.path.join(LOG_DIR, "prs.jsonl")
TARGETS_FILE = os.path.join(LOG_DIR, "targets.yaml")


def load_prs():
    events = []
    if not os.path.exists(PRS_FILE):
        return events
    with open(PRS_FILE) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return events


def load_targets():
    # Simple YAML-free parser for targets.yaml
    import re
    targets = []
    if not os.path.exists(TARGETS_FILE):
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


def render_report():
    prs = load_prs()
    targets = load_targets()

    print("# Ecosystem Inclusion Progress Report")
    print()
    print(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print()

    # Stats
    total_prs = len([e for e in prs if e.get("action") == "opened_pr"])
    merged_prs = len([e for e in prs if e.get("status") == "merged"])
    rejected_prs = len([e for e in prs if e.get("status") == "rejected"])
    open_prs = len([e for e in prs if e.get("status") == "open"])
    skipped = len([e for e in prs if e.get("action") == "skipped"])

    qualified_targets = len([t for t in targets if t.get("status") == "qualified"])
    discovered_targets = len(targets)

    print("## Summary")
    print()
    print(f"| Metric | Value |")
    print(f"|---|---|")
    print(f"| Targets discovered | {discovered_targets} |")
    print(f"| Targets qualified | {qualified_targets} |")
    print(f"| PRs opened | {total_prs} |")
    print(f"| Merged | {merged_prs} |")
    print(f"| Rejected | {rejected_prs} |")
    print(f"| Still open | {open_prs} |")
    print(f"| Skipped | {skipped} |")
    print()

    # Recent PRs
    recent = [e for e in prs if e.get("action") == "opened_pr"]
    if recent:
        print("## Recent PRs")
        print()
        for e in recent[-10:]:
            status = e.get("status", "unknown")
            print(f"- [{status}] {e.get('repo', '?')} → {e.get('url', '?')}")
        print()

    # Targets by status
    if targets:
        print("## Target Status")
        print()
        statuses = {}
        for t in targets:
            s = t.get("status", "unknown")
            statuses[s] = statuses.get(s, 0) + 1
        for s, count in sorted(statuses.items(), key=lambda x: -x[1]):
            print(f"- {s}: {count}")
        print()

    print("---")
    print("Next: Review targets.yaml for the highest-scoring qualified target and prepare a PR.")


def main():
    render_report()


if __name__ == "__main__":
    main()
