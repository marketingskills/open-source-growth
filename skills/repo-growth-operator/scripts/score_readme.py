#!/usr/bin/env python3
"""
score_readme.py — Score a README across positioning, install clarity, and conversion.

Usage:
    python score_readme.py <path-to-readme.md> [--json]

Returns a detailed score with specific improvement suggestions.
"""

import sys
import json
import re


def score_readme_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    return score_readme_content(content)


def score_readme_content(content):
    lines = content.split("\n")
    lower = content.lower()
    first_500 = content[:500].lower()

    results = {}
    suggestions = []

    # --- Header / positioning ---
    header_score = 0
    h1 = ""
    for line in lines:
        if line.startswith("# "):
            h1 = line[2:].strip()
            break

    if h1:
        header_score += 2
        if len(h1) < 60:
            header_score += 2
    else:
        suggestions.append("Add an H1 title to the README.")

    if any(marker in first_500 for marker in ["why", "for ", "problem", "solves"]):
        header_score += 3
    else:
        suggestions.append("Add a 'why this exists' or problem statement above the fold.")

    install_pattern = r"```(?:bash|sh|shell)?\s*(?:npx|pip|npm|brew|git clone|skills add)"
    if re.search(install_pattern, content):
        header_score += 4
    else:
        suggestions.append("Add a one-command install block.")

    if re.search(r"```", content):
        header_score += 2
    else:
        suggestions.append("Add code/prompt examples.")

    results["header_positioning"] = min(header_score, 15)

    # --- Install clarity ---
    install_score = 0
    install_blocks = re.findall(r"##?\s*(?:install|setup|getting started|quick start)", lower)
    if install_blocks:
        install_score += 3
    else:
        suggestions.append("Add an ## Install section.")

    if re.search(r"prerequisites?", lower):
        install_score += 3
    else:
        suggestions.append("Document prerequisites.")

    if re.search(install_pattern, content):
        install_score += 5
    else:
        suggestions.append("Include a single copy-paste install command.")

    if re.search(r"(?:verify|check|test|try)", lower[:2000]):
        install_score += 4
    else:
        suggestions.append("Add a verification step after install.")

    results["install_clarity"] = min(install_score, 15)

    # --- Conversion ---
    conv_score = 0
    if any(marker in lower for marker in ["upgrade", "pricing", "pro ", "enterprise", "hosted", "saas"]):
        conv_score += 5
    else:
        suggestions.append("Add an upgrade / hosted option section.")

    if re.search(r"!\[.*\]\(.*\)", content):
        conv_score += 3

    if re.search(r"(?:star|fork|contribute|follow)", lower[:3000]):
        conv_score += 2
    else:
        suggestions.append("Add a call-to-action for stars or contributions.")

    results["conversion"] = min(conv_score, 10)

    # --- Trust ---
    trust_score = 0
    if re.search(r"license", lower[:2000]):
        trust_score += 3
    else:
        suggestions.append("Add a License section or badge.")

    if re.search(r"contributing", lower):
        trust_score += 3
    else:
        suggestions.append("Add a Contributing section.")

    if re.search(r"```", content) and re.search(r"!\[.*\]", content):
        trust_score += 4

    results["trust"] = min(trust_score, 10)

    total = sum(results.values())

    return {
        "total_score": total,
        "max_score": 50,
        "dimensions": results,
        "suggestions": suggestions[:10],
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python score_readme.py <path-to-readme.md> [--json]", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    result = score_readme_file(filepath)

    if "--json" in sys.argv:
        print(json.dumps(result, indent=2))
    else:
        print(f"Score: {result['total_score']}/{result['max_score']}")
        print()
        for dim, score in result["dimensions"].items():
            print(f"  {dim}: {score}")
        print()
        if result["suggestions"]:
            print("Suggestions:")
            for s in result["suggestions"]:
                print(f"  - {s}")


if __name__ == "__main__":
    main()
