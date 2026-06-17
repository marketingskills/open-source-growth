#!/usr/bin/env python3
"""
discover_github_targets.py — Discover candidate target repos for ecosystem inclusion.

Usage:
    python discover_github_targets.py --category "seo" --category "marketing" --category "mcp"

Searches GitHub for awesome lists, directories, and resource repos in given categories.
Outputs a JSON list of candidate targets with basic metadata.
"""

import sys
import json
import urllib.request
import urllib.parse
import urllib.error
import re
import time
from collections import defaultdict


GITHUB_API_BASE = "https://api.github.com"


def github_search(query, max_results=30):
    """Search GitHub repos using the search API."""
    params = urllib.parse.urlencode({"q": query, "per_page": min(max_results, 100), "sort": "stars"})
    url = f"{GITHUB_API_BASE}/search/repositories?{params}"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github.v3+json"})

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("items", [])
    except urllib.error.HTTPError as e:
        print(f"Warning: GitHub API error ({e.code}) for query '{query}'", file=sys.stderr)
        return []


def generate_queries(categories):
    """Generate GitHub search queries for each category."""
    queries = []
    for cat in categories:
        queries.extend([
            f"awesome {cat} in:name,description,readme",
            f"{cat} resources in:name,description",
            f"{cat} tools list in:name,description",
            f"awesome-{cat} in:name",
            f"{cat} directory in:name,description stars:>100",
        ])
    return queries


def score_candidate(repo):
    """Quick pre-score a candidate before detailed scoring."""
    score = 0
    desc = (repo.get("description") or "").lower()
    topics = [t.lower() for t in repo.get("topics", [])]

    score += min(repo.get("stargazers_count", 0) // 100, 15)
    score += 5 if repo.get("has_issues") else 0
    score += 3 if repo.get("has_wiki") else 0

    recent = repo.get("pushed_at", "")
    if recent:
        score += 5

    key_terms = ["awesome", "list", "resources", "tools", "directory", "curated", "collection"]
    for term in key_terms:
        if term in repo.get("name", "").lower() or term in topics:
            score += 2

    return min(score, 50)


def main():
    if len(sys.argv) < 2:
        print("Usage: python discover_github_targets.py --category <cat1> --category <cat2>", file=sys.stderr)
        print("Example: python discover_github_targets.py --category seo --category mcp --category marketing", file=sys.stderr)
        sys.exit(1)

    categories = []
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--category" and i + 1 < len(sys.argv):
            categories.append(sys.argv[i + 1])
            i += 2
        else:
            i += 1

    if not categories:
        categories = ["seo", "marketing", "mcp", "agent", "analytics", "devrel"]

    print(f"Discovering targets for categories: {', '.join(categories)}", file=sys.stderr)

    queries = generate_queries(categories)
    seen_urls = set()
    candidates = []

    for query in queries:
        results = github_search(query)
        for repo in results:
            url = repo.get("html_url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                score = score_candidate(repo)
                candidates.append({
                    "repo": repo.get("full_name", ""),
                    "url": url,
                    "description": repo.get("description", ""),
                    "stars": repo.get("stargazers_count", 0),
                    "topics": repo.get("topics", []),
                    "pre_score": score,
                    "last_push": repo.get("pushed_at", ""),
                    "has_issues": repo.get("has_issues", False),
                })

        time.sleep(0.1)  # Be gentle to the API

    candidates.sort(key=lambda c: c["pre_score"], reverse=True)

    report = {
        "categories": categories,
        "total_candidates": len(candidates),
        "candidates": candidates[:100],
    }

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
