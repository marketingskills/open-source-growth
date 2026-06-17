# Example: Repo Audit for `marketingskills/seo`

This is an example output from running `repo-audit` mode against the `marketingskills/seo` repo.

## Growth Score

| Dimension | Score | Max |
|---|---|---|
| Positioning | 8 | 15 |
| Install flow | 10 | 15 |
| First useful output | 7 | 15 |
| Demo / proof | 3 | 10 |
| Repo trust | 5 | 10 |
| Contribution path | 2 | 10 |
| Skill metadata | 6 | 10 |
| Distribution assets | 2 | 10 |
| OSS-to-paid path | 3 | 5 |
| **Total** | **46** | **100** |

## Biggest adoption blockers

1.  **No "first useful prompt" section.** The README lists skills but doesn't show a single copy-paste prompt that produces immediate value.
2.  **No animated demo.** Users can't see the workflow working before they install.
3.  **No contribution path.** No CONTRIBUTING.md, no issue templates, no PR template.
4.  **Launch assets not drafted.** No LinkedIn post, X thread, HN title, or Product Hunt tagline ready.
5.  **OSS-to-paid CTA is unclear.** The RefreshAgent upgrade path exists but isn't surfaced in the README.

## Immediate fixes

1. Add a "Try this first" section with the "traffic drop detective" prompt and expected output screenshot.
2. Record a 60-second terminal GIF showing the full workflow.
3. Generate CONTRIBUTING.md, CHANGELOG.md, issue templates, and PR template.
4. Draft launch assets.
5. Add an "Upgrade" section pointing to RefreshAgent.

## Suggested README hero

```markdown
# marketingskills/seo

> Open-source SEO workflows for your AI agent.

⚡ **Try this first:** `Analyse my Search Console data and find pages losing clicks.`

[Install](#install) · [Skills](#skills) · [Examples](#examples) · [Upgrade](#upgrade)
```

## First demo idea

**Title:** "I gave Claude Code live Search Console access in 30 seconds."

**Steps:**
1. Install `marketingskills/seo`.
2. Ask agent: "Find pages losing clicks in the last 28 days."
3. Agent runs the SEO skill, retrieves data, presents findings.
4. Agent generates an action plan with content update suggestions.
5. Save as a client-ready report.

**Assets:**
- 30-second terminal GIF
- 90-second Loom
- README hero screenshot
- LinkedIn carousel
- Launch post

## 7-day action plan

| Day | Action |
|---|---|
| 1 | Add "Try this first" section + screenshot |
| 2 | Record terminal GIF and add to README |
| 3 | Generate trust files (CONTRIBUTING, CHANGELOG, templates) |
| 4 | Draft LinkedIn + X launch posts |
| 5 | Draft HN + Reddit + Product Hunt assets |
| 6 | Add Upgrade section with RefreshAgent CTA |
| 7 | Full README rewrite → publish |
