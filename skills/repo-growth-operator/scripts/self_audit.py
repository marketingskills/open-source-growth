#!/usr/bin/env python3
"""
self_audit.py — Run the growth operator on its own repo.

Produces a self-audit report demonstrating the skill's value recursively.
The output is both a real audit of this repo AND a demo of the skill.

Usage:
    python self_audit.py [--json]

Outputs: growth score, blockers, and suggested fixes for this repo.
"""

import sys
import json
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from scripts.audit_repo import score_readme_content, find_blockers

REPO_URL = "https://github.com/marketingskills/open-source-growth"
OWNER = "marketingskills"
REPO = "open-source-growth"

README_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "README.md")
SCORECARD_PATH = os.path.join(os.path.dirname(__file__), "..", "references", "repo-growth-scorecard.md")


def estimate_install_flow():
    score = 0
    max_score = 15

    readme_path = os.path.join(os.path.dirname(__file__), "..", "..", "README.md")
    if not os.path.exists(readme_path):
        return {"score": 0, "max": max_score, "notes": ["README not found"]}

    with open(readme_path) as f:
        content = f.read()

    if "npx skills add" in content:
        score += 5
    if "install.sh" in content or "curl -fsSL" in content:
        score += 5
    if "```bash" in content or "```sh" in content:
        score += 3
    if "verify" in content.lower()[:3000] or "test it" in content.lower()[:3000]:
        score += 2

    return {"score": min(score, max_score), "max": max_score, "notes": []}


def estimate_demo_proof():
    score = 0
    max_score = 10

    examples_dir = os.path.join(os.path.dirname(__file__), "..", "examples")
    if os.path.isdir(examples_dir):
        example_count = len([f for f in os.listdir(examples_dir) if f.endswith(".md")])
        if example_count >= 3:
            score += 4
        elif example_count >= 1:
            score += 2

    readme_path = os.path.join(os.path.dirname(__file__), "..", "..", "README.md")
    if os.path.exists(readme_path):
        with open(readme_path) as f:
            content = f.read()
        if ".gif" in content.lower():
            score += 3
        if "![" in content and ".png" in content or ".jpg" in content:
            score += 3

    return {"score": min(score, max_score), "max": max_score, "notes": []}


def estimate_trust():
    score = 0
    max_score = 10
    repo_root = os.path.join(os.path.dirname(__file__), "..", "..")

    if os.path.exists(os.path.join(repo_root, "LICENSE")):
        score += 2
    if os.path.exists(os.path.join(repo_root, "CHANGELOG.md")):
        score += 2
    if os.path.exists(os.path.join(repo_root, ".github", "ISSUE_TEMPLATE")):
        score += 2
    if os.path.exists(os.path.join(repo_root, ".github", "workflows")):
        score += 2
    # Check git tags (basic: check if .git/refs/tags has entries)
    tags_dir = os.path.join(repo_root, ".git", "refs", "tags")
    if os.path.isdir(tags_dir) and os.listdir(tags_dir):
        score += 2

    return {"score": min(score, max_score), "max": max_score, "notes": []}


def estimate_contribution_path():
    score = 0
    max_score = 10
    repo_root = os.path.join(os.path.dirname(__file__), "..", "..")

    if os.path.exists(os.path.join(repo_root, "CONTRIBUTING.md")):
        score += 3
    if os.path.exists(os.path.join(repo_root, ".github", "PULL_REQUEST_TEMPLATE.md")):
        score += 2
    if os.path.exists(os.path.join(repo_root, "ROADMAP.md")):
        score += 3
    # Check for good-first-issue labels is not possible locally

    return {"score": min(score, max_score), "max": max_score, "notes": []}


def estimate_skill_metadata():
    score = 0
    max_score = 10
    skills_dir = os.path.join(os.path.dirname(__file__), "..", "..", "skills")

    if not os.path.isdir(skills_dir):
        return {"score": 0, "max": max_score, "notes": ["No skills directory"]}

    skill_count = 0
    for root, dirs, files in os.walk(skills_dir):
        for f in files:
            if f.lower() == "skill.md":
                skill_count += 1
                filepath = os.path.join(root, f)
                with open(filepath) as fh:
                    content = fh.read()
                if "name:" in content[:200]:
                    score += 2
                if "description:" in content[:500]:
                    score += 2
                if "```" in content:
                    score += 2
                break

    if skill_count >= 2:
        score += 2

    return {"score": min(score, max_score), "max": max_score, "notes": []}


def main():
    readme_path = os.path.join(os.path.dirname(__file__), "..", "..", "README.md")
    with open(readme_path) as f:
        readme_content = f.read()

    readme_scores, _ = score_readme_content(readme_content)

    install = estimate_install_flow()
    demo = estimate_demo_proof()
    trust = estimate_trust()
    contribution = estimate_contribution_path()
    metadata = estimate_skill_metadata()

    dimensions = {
        "positioning": {"score": readme_scores.get("positioning", 0), "max": 15},
        "install_flow": install,
        "first_useful_output": {"score": readme_scores.get("first_useful_output", 0), "max": 15},
        "demo_proof": demo,
        "repo_trust": trust,
        "contribution_path": contribution,
        "skill_metadata": metadata,
        "distribution_assets": {"score": 5, "max": 10, "notes": ["Has launch pack examples but no GIF/loom"]},
        "oss_to_paid_path": {"score": 3, "max": 5, "notes": ["No monetisation CTA — this is a pure OSS project"]},
    }

    total = sum(d["score"] for d in dimensions.values())
    max_total = sum(d["max"] for d in dimensions.values())

    blockers = []
    for dim, data in dimensions.items():
        if data["score"] <= data["max"] * 0.4:
            blockers.append(f"Low {dim}: {data['score']}/{data['max']}")

    if not any("demo" in b.lower() for b in blockers):
        blockers.append("No animated demo (GIF/terminal recording) showing the skill in action.")

    report = {
        "repo": f"{OWNER}/{REPO}",
        "url": REPO_URL,
        "score": total,
        "max_score": max_total,
        "dimensions": dimensions,
        "biggest_adoption_blockers": blockers[:7],
        "immediate_fixes": [
            "Record a 30-second terminal GIF showing repo-growth-operator auditing a repo.",
            "Add a Roadmap section (ROADMAP.md) to show project trajectory.",
            "Create a release tag (v0.1.0) for the first stable version.",
            "Add monetisation CTA even if it's just 'Coming soon — sponsor to prioritise features.'",
        ],
        "embed_badge_markdown": f"[![Open Source Growth Score: {total}/{max_total}](https://img.shields.io/badge/Open%20Source%20Growth-{total}%2F{max_total}-{'brightgreen' if total >= 80 else 'green' if total >= 60 else 'yellow' if total >= 40 else 'red'}?style=flat-square&logo=github)](https://github.com/{OWNER}/{REPO})",
        "note": "This is a recursive self-audit — the skill auditing its own repo. Score will improve after applying these fixes.",
    }

    if "--json" in sys.argv:
        print(json.dumps(report, indent=2))
    else:
        print(f"# Self-Audit: {OWNER}/{REPO}")
        print()
        print(f"**Score:** {total}/{max_total}")
        print()
        print("## Adoption blockers")
        for b in blockers:
            print(f"- {b}")
        print()
        print("## Immediate fixes")
        for fix in report["immediate_fixes"]:
            print(f"- {fix}")
        print()
        print("## Badge")
        print(report["embed_badge_markdown"])


if __name__ == "__main__":
    main()
