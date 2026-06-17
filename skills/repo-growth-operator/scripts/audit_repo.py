#!/usr/bin/env python3
"""
audit_repo.py — Score a GitHub repo across the Open Source Growth Score dimensions.

Usage:
    python audit_repo.py <repo_url>

Returns a JSON report with score, dimension breakdown, and top adoption blockers.
"""

import json
import sys
import urllib.request
import urllib.error
import re
from html.parser import HTMLParser


class ReadmeParser(HTMLParser):
    """Minimal parser to extract text content from rendered README HTML."""
    def __init__(self):
        super().__init__()
        self._text = []
        self._capture = False
        self._skip_tags = {"script", "style", "code", "pre"}

    def handle_starttag(self, tag, attrs):
        if tag in self._skip_tags:
            self._capture = False

    def handle_endtag(self, tag):
        if tag in self._skip_tags:
            self._capture = True

    def handle_data(self, data):
        if self._capture:
            self._text.append(data.strip())

    @property
    def text(self):
        return " ".join(t for t in self._text if t)


def fetch_readme(repo_url):
    """Fetch README content from GitHub."""
    match = re.match(r"https?://github\.com/([^/]+)/([^/]+)", repo_url)
    if not match:
        raise ValueError(f"Invalid GitHub URL: {repo_url}")

    owner, repo = match.group(1), match.group(2).rstrip("/")
    api_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    req = urllib.request.Request(api_url, headers={"Accept": "application/vnd.github.v3.raw"})
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        print(f"Warning: Could not fetch README ({e.code}). Running reduced audit.", file=sys.stderr)
        return ""


def score_readme(readme):
    """Score README quality dimensions."""
    scores = {}

    # Positioning (max 15)
    positioning = 0
    lines = readme.split("\n")
    first_200_chars = readme[:200].lower()

    if len(readme) > 100:
        positioning += 3
    if any(marker in first_200_chars for marker in ["why", "problem", "pain", "solves"]):
        positioning += 3
    if any(marker in first_200_chars for marker in ["install", "get started", "quick start", "usage"]):
        positioning += 3
    if any(marker in first_200_chars for marker in ["for developers", "for teams", "for engineers"]):
        positioning += 2

    scores["positioning"] = min(positioning, 15)

    # Install flow (max 15)
    install = 0
    if re.search(r"```(?:bash|sh|shell)?\s*(?:npx|pip|npm|brew|git clone|skills add)", readme):
        install += 5
    if re.search(r"prerequisites?", readme, re.IGNORECASE):
        install += 3
    if re.search(r"```(?:bash|sh|shell)", readme):
        install += 4
    if any(marker in readme.lower() for marker in ["verify", "test it", "try it", "check"]):
        install += 3

    scores["install_flow"] = min(install, 15)

    # First useful output (max 15)
    first_use = 0
    example_sections = re.findall(r"(?:example|try this|demo|usage|sample).*?(?=\n##|\Z)", readme, re.IGNORECASE | re.DOTALL)
    for section in example_sections:
        if re.search(r"```", section):
            first_use += 5
            if re.search(r"(?:output|result|returns)", section, re.IGNORECASE):
                first_use += 5
            break
    scores["first_useful_output"] = min(first_use, 15)

    # Demo / proof (max 10)
    demo = 0
    if ".gif" in readme.lower():
        demo += 4
    if re.search(r"!\[.*\]\(.*\)", readme):
        demo += 3
    if re.search(r"(?:youtube|loom|vimeo|asciinema)", readme, re.IGNORECASE):
        demo += 3
    scores["demo"] = min(demo, 10)

    # Total
    total = sum(scores.values())
    return scores, total


def find_blockers(scores, readme):
    """Identify the biggest adoption blockers."""
    blockers = []

    if scores.get("positioning", 0) < 10:
        blockers.append("No clear one-line value prop above the fold.")
    if scores.get("install_flow", 0) < 10:
        blockers.append("No obvious one-command install above the fold.")
    if scores.get("first_useful_output", 0) < 10:
        blockers.append("No 'try this first' section with expected output.")
    if scores.get("demo", 0) < 5:
        blockers.append("No animated demo or screenshot showing real output.")
    if "license" not in readme.lower()[:3000]:
        blockers.append("No license visible in README.")
    if "contributing" not in readme.lower():
        blockers.append("No contribution path (CONTRIBUTING.md or contributing section).")

    return blockers[:7]


def main():
    if len(sys.argv) < 2:
        print("Usage: python audit_repo.py <repo_url>", file=sys.stderr)
        sys.exit(1)

    repo_url = sys.argv[1]
    readme = fetch_readme(repo_url)
    scores, total = score_readme(readme)
    blockers = find_blockers(scores, readme)

    report = {
        "url": repo_url,
        "score": total,
        "max_score": 55,
        "dimensions": scores,
        "biggest_adoption_blockers": blockers,
        "note": "This script scores out of 55 (POS+INSTALL+FIRST_USE+DEMO). "
                "Full scorecard dimensions require repo metadata inspection."
    }

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
