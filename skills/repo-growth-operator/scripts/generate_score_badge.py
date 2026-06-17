#!/usr/bin/env python3
"""
generate_score_badge.py — Generate shields.io badge URL for Open Source Growth Score.

Usage:
    python generate_score_badge.py <score>

Outputs markdown and URL for a custom shields.io badge.
Supports color coding: green (80+), yellow (50-79), red (<50).
"""

import sys
import json


def score_to_color(score):
    if score >= 80:
        return "brightgreen"
    elif score >= 60:
        return "green"
    elif score >= 40:
        return "yellow"
    elif score >= 20:
        return "orange"
    else:
        return "red"


def generate_badge(score, max_score=100):
    color = score_to_color(score)
    label = "Open Source Growth"
    message = f"{score}/{max_score}"

    url = f"https://img.shields.io/badge/{label}-{message}-{color}?style=flat-square&logo=github"

    markdown = f"[![Open Source Growth Score: {message}]({url})](https://github.com/marketingskills/open-source-growth)"

    return {
        "url": url,
        "markdown": markdown,
        "score": score,
        "max_score": max_score,
        "color": color,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_score_badge.py <score>", file=sys.stderr)
        print("Example: python generate_score_badge.py 81", file=sys.stderr)
        sys.exit(1)

    try:
        score = int(sys.argv[1])
    except ValueError:
        print("Error: Score must be an integer", file=sys.stderr)
        sys.exit(1)

    result = generate_badge(score)

    if "--json" in sys.argv:
        print(json.dumps(result, indent=2))
    else:
        print("Badge URL:")
        print(f"  {result['url']}")
        print()
        print("README Markdown:")
        print(f"  {result['markdown']}")


if __name__ == "__main__":
    main()
