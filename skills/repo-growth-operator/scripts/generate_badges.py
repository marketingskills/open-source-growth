#!/usr/bin/env python3
"""
generate_badges.py — Generate shields.io badge markdown for a repo.

Usage:
    python generate_badges.py --owner marketingskills --repo seo

Outputs markdown badge snippets for README inclusion.
"""

import sys
import argparse


BADGE_TEMPLATES = {
    "stars": "[![GitHub Stars](https://img.shields.io/github/stars/{owner}/{repo}?style=flat-square&logo=github)](https://github.com/{owner}/{repo})",
    "license": "[![License](https://img.shields.io/github/license/{owner}/{repo}?style=flat-square)](LICENSE)",
    "last_commit": "[![Last Commit](https://img.shields.io/github/last-commit/{owner}/{repo}?style=flat-square)](https://github.com/{owner}/{repo}/commits)",
    "issues": "[![Issues](https://img.shields.io/github/issues/{owner}/{repo}?style=flat-square)](https://github.com/{owner}/{repo}/issues)",
    "prs": "[![PRs](https://img.shields.io/github/issues-pr/{owner}/{repo}?style=flat-square)](https://github.com/{owner}/{repo}/pulls)",
    "release": "[![Release](https://img.shields.io/github/v/release/{owner}/{repo}?style=flat-square)](https://github.com/{owner}/{repo}/releases)",
    "downloads": "[![Downloads](https://img.shields.io/github/downloads/{owner}/{repo}/total?style=flat-square)](https://github.com/{owner}/{repo}/releases)",
}


def main():
    parser = argparse.ArgumentParser(description="Generate shields.io badges for README")
    parser.add_argument("--owner", required=True, help="GitHub owner/org")
    parser.add_argument("--repo", required=True, help="GitHub repo name")
    parser.add_argument("--badges", nargs="+",
                        default=["stars", "license", "last_commit", "issues", "prs", "release"],
                        help=f"Badge types: {list(BADGE_TEMPLATES.keys())}")
    args = parser.parse_args()

    print("<!-- Badges -->")
    print('<p align="center">')
    for badge in args.badges:
        if badge in BADGE_TEMPLATES:
            url = BADGE_TEMPLATES[badge].format(owner=args.owner, repo=args.repo)
            print(f"  {url}")
    print("</p>")


if __name__ == "__main__":
    main()
