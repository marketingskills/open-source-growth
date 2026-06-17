---
name: ecosystem-inclusion-operator
description: >-
  Find relevant open-source ecosystems, directories, awesome lists, templates,
  examples, and integration repos where a project genuinely belongs. Score
  targets, prepare useful PRs, open issues or PRs, and maintain a durable
  progress log so the workflow can continue through repeated /loop runs. Use
  when the user wants to grow an open-source repo through ethical ecosystem
  inclusion.
---

# Ecosystem Inclusion Operator

Find where your repo belongs. Open useful, non-spammy PRs. Track every attempt in a durable progress log so the agent can keep going with `/loop`.

## Core workflow

1.  Understand the repo's audience, category, install command, and commercial relationship.
2.  Discover candidate target repos.
3.  Score each target for relevance, activity, and contribution fit.
4.  Read contribution guidelines before proposing changes.
5.  Choose one of: open PR / open issue first / add to backlog / skip.
6.  Create a tailored contribution.
7.  Log every action in `.repo-growth/`.
8.  On repeated `/loop` runs, continue from the log instead of starting over.

## Target types

| Target type | Inclusion angle |
|---|---|
| Awesome lists | Add to relevant category section |
| MCP directories | Add as tool/server entry |
| Agent skill directories | Add as skill pack |
| Claude Code / Codex resource lists | Add as example workflow |
| Adjacent tool repos (SEO, analytics, marketing) | Add integration docs or example |
| Starter kits / templates | Add as template |
| DevRel / open-source growth repos | Add the growth-operator itself |
| Agency / consultancy resource repos | Add as workflow example |

## Scoring system

Score every target /100 before acting:

| Dimension | Weight |
|---|---|
| Audience fit | 25 |
| Repo activity | 15 |
| Contribution friendliness | 15 |
| Inclusion precedent | 15 |
| Traffic / stars / authority | 10 |
| Low spam risk | 10 |
| Commercial relevance | 10 |

### Classification

| Score | Action |
|---|---|
| 80–100 | Open tailored PR |
| 60–79 | Open issue first or draft PR |
| 40–59 | Add to backlog |
| 0–39 | Skip |

## PR strategies

### 1. Directory / list addition PR
Smallest. One link + neutral description in the appropriate section.

### 2. Example workflow PR
More valuable. Add `examples/<integration>.md` with a full walkthrough.

### 3. Integration docs PR
Add docs teaching the target repo's users how to use your skill with their tool.

### 4. Template / starter PR
For starter-kit repos — add a full template directory.

### 5. Compatibility PR
Add actual code / connector support. Highest effort, highest value.

## Hard rules

- No spam PRs.
- No fake neutrality.
- No fake stars, fake users, or fake benchmarks.
- No irrelevant submissions.
- No repeated follow-ups.
- Always disclose if the repo is maintained by the same person/org.
- Prefer useful examples and docs over bare promotional links.
- Respect maintainers' scope and decisions.
- Do not open more than 3 PRs per day.
- Do not argue with maintainers.

## Commands

### `/discover-targets`
Find candidate repos matching the repo's category and audience.

### `/score-targets`
Score candidates and explain why.

### `/prepare-pr`
Create exact branch, file edit, commit message, and PR body.

### `/open-pr`
Open the PR if GitHub auth is available.

### `/update-pr-status`
Check existing PRs and update the log.

### `/follow-up`
Suggest polite follow-ups only when appropriate (max 1 after 14 days of no response).

### `/summarize-growth`
Report progress: targets found, PRs opened, merged, rejected, traffic impact.

## Progress log

Maintain in `.repo-growth/`:

| File | Purpose |
|---|---|
| `loop-state.md` | Current state, next action |
| `targets.yaml` | CRM of all targets with status and score |
| `prs.jsonl` | Append-only event log |
| `decisions.md` | Human-readable learning log |
| `assets/` | Reusable listing copy, PR templates |
| `evidence/` | Screenshots, notes |

See `references/progress-log-spec.md` for the exact format.

## Related skills

- `repo-growth-operator` – For wider repo adoption, README, launch, and monetisation work.
