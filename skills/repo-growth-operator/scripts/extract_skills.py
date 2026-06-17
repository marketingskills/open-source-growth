#!/usr/bin/env python3
"""
extract_skills.py — Discover all SKILL.md files in a repo and extract their metadata.

Usage:
    python extract_skills.py <path-to-repo>

Outputs a JSON summary of all skills with their name, description, triggers, and prompts.
Useful for the marketplace-optimise workflow.
"""

import sys
import json
import os
import re
import yaml  # optional; falls back to regex


def parse_skill_metadata(filepath):
    """Extract YAML front matter from a SKILL.md file."""
    with open(filepath, "r") as f:
        content = f.read()

    # Try to parse YAML front matter
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {"error": "No YAML front matter found", "file": filepath}

    front_matter = match.group(1)

    metadata = {}
    try:
        import yaml
        metadata = yaml.safe_load(front_matter) or {}
    except ImportError:
        # Fallback: basic key-value extraction
        for line in front_matter.split("\n"):
            kv_match = re.match(r"^(\w+):\s*(.*)", line)
            if kv_match:
                key = kv_match.group(1)
                value = kv_match.group(2).strip().strip('"').strip("'")
                metadata[key] = value

    return {
        "file": filepath,
        "name": metadata.get("name", ""),
        "description": metadata.get("description", ""),
        "triggers": metadata.get("triggers", metadata.get("when_to_use", [])),
        "example_prompts": extract_example_prompts(content),
        "has_dependencies": "dependencies" in content.lower()[:2000],
        "has_safety_notes": "safety" in content.lower()[:2000],
    }


def extract_example_prompts(content):
    """Extract example prompts from the content."""
    prompts = []
    # Find text between triple backticks that looks like prompts
    code_blocks = re.findall(r"```(?:\w*)\n(.*?)```", content, re.DOTALL)
    for block in code_blocks:
        block = block.strip()
        if len(block) > 20 and len(block) < 2000:
            prompts.append(block[:200])
    return prompts[:5]


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_skills.py <path-to-repo>", file=sys.stderr)
        sys.exit(1)

    repo_path = sys.argv[1]
    if not os.path.isdir(repo_path):
        print(f"Error: {repo_path} is not a directory", file=sys.stderr)
        sys.exit(1)

    skills = []
    for root, dirs, files in os.walk(repo_path):
        for f in files:
            if f.lower() == "skill.md":
                filepath = os.path.join(root, f)
                rel_path = os.path.relpath(filepath, repo_path)
                metadata = parse_skill_metadata(filepath)
                metadata["file"] = rel_path
                skills.append(metadata)

    report = {
        "repo": repo_path,
        "skill_count": len(skills),
        "skills": skills,
    }

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
