#!/usr/bin/env python3
"""
append_log.py — Append an event to the .repo-growth/prs.jsonl log.

Usage:
    python append_log.py --repo "owner/name" --action "opened_pr" --url "https://..." --score 84

Keeps the append-only event log for the ecosystem-inclusion workflow.
"""

import sys
import json
import os
from datetime import datetime


LOG_DIR = ".repo-growth"
LOG_FILE = os.path.join(LOG_DIR, "prs.jsonl")


def ensure_log_dir():
    os.makedirs(LOG_DIR, exist_ok=True)


def append_event(event):
    ensure_log_dir()
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")
    print(f"Logged: {event['action']} on {event['repo']}")


def main():
    event = {
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "repo": "",
        "action": "",
        "url": "",
        "status": "",
        "score": 0,
        "reason": "",
    }

    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--repo" and i + 1 < len(sys.argv):
            event["repo"] = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--action" and i + 1 < len(sys.argv):
            event["action"] = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--url" and i + 1 < len(sys.argv):
            event["url"] = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--status" and i + 1 < len(sys.argv):
            event["status"] = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--score" and i + 1 < len(sys.argv):
            event["score"] = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--reason" and i + 1 < len(sys.argv):
            event["reason"] = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    if not event["repo"] or not event["action"]:
        print("Usage: python append_log.py --repo owner/name --action opened_pr --url <url> --score 84 [--reason ...] [--status open]", file=sys.stderr)
        sys.exit(1)

    append_event(event)


if __name__ == "__main__":
    main()
