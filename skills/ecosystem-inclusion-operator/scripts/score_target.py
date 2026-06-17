#!/usr/bin/env python3
"""
score_target.py — Score a single target repo for ecosystem inclusion fit.

Usage:
    python score_target.py <repo_url>

Returns a detailed scoring breakdown and action recommendation.
"""

import sys
import json
import urllib.request
import urllib.error
import re


GITHUB_API_BASE = "https://api.github.com"


def fetch_repo_info(repo_url):
    match = re.match(r"https?://github\.com/([^/]+)/([^/]+)", repo_url)
    if not match:
        raise ValueError(f"Invalid GitHub URL: {repo_url}")

    owner, repo = match.group(1), match.group(2).rstrip("/")
    api_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}"
    req = urllib.request.Request(api_url, headers={"Accept": "application/vnd.github.v3+json"})

    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"Error fetching repo: {e.code}", file=sys.stderr)
        return None


def score_target(info):
    if not info:
        return {"error": "No repo info available", "score": 0}

    scores = {}
    total = 0

    # Audience fit (max 25)
    audience = 0
    desc = (info.get("description") or "").lower()
    topics = [t.lower() for t in info.get("topics", [])]
    name = info.get("name", "").lower()

    key_terms = ["awesome", "list", "resources", "tools", "directory", "curated"]
    if any(t in name or t in topics for t in key_terms):
        audience += 10
    if desc and len(desc) > 30:
        audience += 5
    if info.get("has_wiki"):
        audience += 5
    if info.get("has_pages"):
        audience += 5

    scores["audience_fit"] = min(audience, 25)
    total += scores["audience_fit"]

    # Repo activity (max 15)
    activity = 0
    pushed = info.get("pushed_at", "")
    if pushed:
        activity += 5
    if info.get("open_issues_count", 0) < 50:
        activity += 5
    if info.get("size", 0) > 100:
        activity += 5

    scores["repo_activity"] = min(activity, 15)
    total += scores["repo_activity"]

    # Contribution friendliness (max 15)
    contrib = 0
    if info.get("has_issues"):
        contrib += 5
    if info.get("has_projects"):
        contrib += 3
    if info.get("license"):
        contrib += 4
    if info.get("permissions", {}).get("push"):
        contrib += 3

    scores["contribution_friendliness"] = min(contrib, 15)
    total += scores["contribution_friendliness"]

    # Inclusion precedent not scoreable from API alone -> default mid
    scores["inclusion_precedent"] = 8
    total += scores["inclusion_precedent"]

    # Traffic / authority (max 10)
    stars = info.get("stargazers_count", 0)
    traffic = 0
    if stars >= 10000:
        traffic = 10
    elif stars >= 1000:
        traffic = 8
    elif stars >= 100:
        traffic = 5
    elif stars >= 10:
        traffic = 2
    scores["traffic_authority"] = traffic
    total += traffic

    # Low spam risk (max 10)
    spam_risk = 10
    if info.get("archived"):
        spam_risk -= 5
    if not info.get("license"):
        spam_risk -= 3
    scores["low_spam_risk"] = max(spam_risk, 0)
    total += scores["low_spam_risk"]

    # Commercial relevance (max 10) — heuristic
    commercial = 0
    if any(t in topics for t in ["seo", "marketing", "analytics", "saas", "business", "startup"]):
        commercial += 5
    if stars > 100:
        commercial += 5
    scores["commercial_relevance"] = min(commercial, 10)
    total += scores["commercial_relevance"]

    return {"score": total, "dimensions": scores}


def classify(score):
    if score >= 80:
        return "Open tailored PR"
    elif score >= 60:
        return "Open issue first or draft PR"
    elif score >= 40:
        return "Add to backlog"
    else:
        return "Skip"


def main():
    if len(sys.argv) < 2:
        print("Usage: python score_target.py <repo_url>", file=sys.stderr)
        sys.exit(1)

    repo_url = sys.argv[1]
    info = fetch_repo_info(repo_url)

    if not info:
        print(json.dumps({"url": repo_url, "error": "Could not fetch repo info", "score": 0}))
        sys.exit(1)

    result = score_target(info)
    action = classify(result["score"])

    report = {
        "url": repo_url,
        "name": info.get("full_name", ""),
        "stars": info.get("stargazers_count", 0),
        "description": info.get("description", ""),
        "score": result["score"],
        "dimensions": result["dimensions"],
        "recommended_action": action,
    }

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
