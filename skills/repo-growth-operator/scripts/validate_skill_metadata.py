#!/usr/bin/env python3
"""
validate_skill_metadata.py — Check all SKILL.md files in a repo for metadata quality.

Usage:
    python validate_skill_metadata.py <path-to-repo>

Scores each SKILL.md across the marketplace optimisation dimensions.
Flags missing or weak metadata. Ban deceptive patterns.
"""

import sys
import json
import os
import re


DECEPTIVE_PATTERNS = [
    r"\b(best|fastest|easiest|most powerful|#1|top-rated|leading)\b",
    r"\b(free|unlimited)\s+(forever|lifetime)\b",
    r"\b(guaranteed|promised)\s+(results|rankings|traffic)\b",
    r"\b(secret|hidden|undisclosed)\b",
    r"\b(instantly|immediately)\s+(fix|solve|grow|improve)\b",
]


SKILL_MD_REQUIRED_FIELDS = ["name", "description"]


def validate_skill_file(filepath):
    """Validate a single SKILL.md file."""
    with open(filepath, "r") as f:
        content = f.read()

    rel_path = os.path.relpath(filepath, start=os.path.commonpath([filepath]))
    result = {
        "file": filepath,
        "score": 0,
        "max_score": 20,
        "checks": [],
        "warnings": [],
        "deceptive_patterns_found": [],
    }

    # Check front matter
    fm_match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not fm_match:
        result["checks"].append({"check": "front_matter", "pass": False, "detail": "No YAML front matter found"})
        result["warnings"].append("Missing YAML front matter block.")
        return result
    else:
        result["checks"].append({"check": "front_matter", "pass": True, "detail": "YAML front matter exists"})
        result["score"] += 2

    front_matter = fm_match.group(1)

    # Check required fields
    for field in SKILL_MD_REQUIRED_FIELDS:
        pattern = rf"^{re.escape(field)}:\s*\S" if field == "name" else rf"^{re.escape(field)}:\s*\S"
        if re.search(pattern, front_matter, re.MULTILINE):
            result["checks"].append({"check": f"field_{field}", "pass": True, "detail": f"'{field}' is present"})
            result["score"] += 2
        else:
            result["checks"].append({"check": f"field_{field}", "pass": False, "detail": f"'{field}' is missing or empty"})
            result["warnings"].append(f"Missing required field: {field}")

    # Check for example prompts
    if re.search(r"```", content):
        result["checks"].append({"check": "example_prompts", "pass": True, "detail": "Code blocks found (likely example prompts)"})
        result["score"] += 2
    else:
        result["checks"].append({"check": "example_prompts", "pass": False, "detail": "No example prompts found"})
        result["warnings"].append("No example prompts or code blocks in skill definition.")

    # Check for trigger phrases
    if re.search(r"(?:use\s+when|triggers?|when\s+to\s+use)", content, re.IGNORECASE):
        result["checks"].append({"check": "trigger_phrases", "pass": True, "detail": "Trigger/use-when section found"})
        result["score"] += 2
    else:
        result["checks"].append({"check": "trigger_phrases", "pass": False, "detail": "No trigger or use-when section"})
        result["warnings"].append("Missing trigger phrases or 'use when' guidance.")

    # Check for dependencies
    if re.search(r"(?:dependencies?|requires?|prerequisites?)", content, re.IGNORECASE):
        result["checks"].append({"check": "dependencies", "pass": True, "detail": "Dependencies documented"})
        result["score"] += 2
    else:
        result["checks"].append({"check": "dependencies", "pass": False, "detail": "No dependencies documented"})
        result["warnings"].append("Dependencies not documented.")

    # Check for safety notes
    if re.search(r"(?:safety|caution|warning|note|security)", content, re.IGNORECASE):
        result["checks"].append({"check": "safety_notes", "pass": True, "detail": "Safety notes found"})
        result["score"] += 2
    else:
        result["checks"].append({"check": "safety_notes", "pass": False, "detail": "No safety notes"})

    # Check for category tags
    if re.search(r"(?:tags?|categories?|keywords?)", front_matter, re.IGNORECASE):
        result["checks"].append({"check": "category_tags", "pass": True, "detail": "Category tags found in front matter"})
        result["score"] += 2
    else:
        result["checks"].append({"check": "category_tags", "pass": False, "detail": "No category tags"})
        result["warnings"].append("No category/tag metadata in front matter.")

    # Check description length
    desc_match = re.search(r'^description:\s*["\']?(.*?)["\']?\s*$', front_matter, re.MULTILINE)
    if desc_match:
        desc = desc_match.group(1)
        if len(desc) < 20:
            result["warnings"].append("Description is very short (< 20 chars).")
        elif len(desc) > 500:
            result["warnings"].append("Description is very long (> 500 chars). Consider shortening.")
        result["checks"].append({"check": "description_length", "pass": True, "detail": f"Description is {len(desc)} chars"})
        result["score"] += 2
    else:
        result["checks"].append({"check": "description_length", "pass": False, "detail": "Could not parse description"})

    # Check for deceptive patterns
    for pattern in DECEPTIVE_PATTERNS:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            for m in matches:
                result["deceptive_patterns_found"].append(m)
            result["score"] -= 2  # penalty
            result["warnings"].append(f"Deceptive pattern detected: {matches[0]}")

    result["score"] = max(0, result["score"])
    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_skill_metadata.py <path-to-repo>", file=sys.stderr)
        sys.exit(1)

    repo_path = sys.argv[1]
    if not os.path.isdir(repo_path):
        print(f"Error: {repo_path} is not a directory", file=sys.stderr)
        sys.exit(1)

    results = []
    for root, dirs, files in os.walk(repo_path):
        for f in files:
            if f.lower() == "skill.md":
                filepath = os.path.join(root, f)
                result = validate_skill_file(filepath)
                results.append(result)

    summary = {
        "repo": repo_path,
        "skills_validated": len(results),
        "results": results,
    }

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
