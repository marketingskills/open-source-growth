# Progress Log Specification

The agent must maintain a durable `.repo-growth/` directory at the root of the repository being promoted.

## `loop-state.md`

```markdown
# Repo Growth Loop State

Repo being promoted: <owner/repo>
Primary CTA: <install command>
Commercial bridge: <paid service description>
Last run: <YYYY-MM-DD>
Current mode: <ecosystem inclusion | discovery | pr-preparation>
Daily PR limit: 3
Daily issue limit: 5

## Current priority

<Single sentence describing the current priority.>

## Do not target

- Dead repos (no activity in 12+ months)
- Lists with no external submissions
- Repos where commercial projects are forbidden
- Repos where the addition would be purely promotional
- Any repo already contacted in the last 14 days

## Next action

Pick the highest-scoring target in targets.yaml with status = qualified.
```

## `targets.yaml`

```yaml
targets:
  - repo: "owner/name"
    url: "https://github.com/owner/name"
    category: "mcp-directory"
    status: "qualified"  # discovered | qualified | prepared | pr_opened | merged | rejected | skipped | backlog
    score: 84
    fit_reason: "Has marketing/analytics section and accepts server/tool listings"
    contribution_rules: "Alphabetical list, one-line description, no marketing claims"
    proposed_contribution: "Add owner/repo to Marketing/SEO section"
    next_action: "Open PR"
    last_checked: "2026-06-17"
    pr_url: null
    issue_url: null
    follow_up_after: null
    notes: []
```

## `prs.jsonl`

Append-only. One JSON object per line.

```jsonl
{"date":"2026-06-17","repo":"owner/awesome-list","action":"opened_pr","url":"https://github.com/owner/awesome-list/pull/123","status":"open","score":84}
{"date":"2026-06-18","repo":"other/awesome-tools","action":"skipped","reason":"No commercial/open-core projects allowed","score":42}
```

## `decisions.md`

```markdown
# Decisions

## 2026-06-17

Skipped `xyz/awesome-tools` because the repo has not accepted a PR in 18 months.

Opened PR to `abc/awesome-mcp` because it has a Marketing Analytics section and accepted similar additions last week.

Learning: Directory PRs need neutral descriptions. Avoid saying "best", "fastest", or "easiest".
```

## `assets/`

| File | Content |
|---|---|
| `short-description.md` | 100–200 chars for directory listings |
| `long-description.md` | 1–2 sentences for README entries |
| `pr-template.md` | PR body template used across submissions |
| `issue-template.md` | Issue body template for suggest-before-PR targets |
| `directory-listing.md` | The canonical listing line |
