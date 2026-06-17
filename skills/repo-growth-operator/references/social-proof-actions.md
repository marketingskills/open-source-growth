# Social Proof Actions

Use this mode when the skill can interact with GitHub on behalf of the user (e.g., via `gh` CLI or API). These actions build social proof for the repo being grown.

## Available actions

| Action | Command | Effect |
|---|---|---|
| Star | `gh api -X PUT /user/starred/{owner}/{repo}` | Adds a GitHub star |
| Watch | `gh api -X PUT /user/subscriptions/{owner}/{repo}` | Subscribes to notifications |
| Fork | `gh api -X POST /repos/{owner}/{repo}/forks` | Creates a fork |
| Follow user | `gh api -X PUT /user/following/{username}` | Follows a GitHub user |

## Workflow

1. Check if `gh` CLI is available (`command -v gh`).
2. Check if user is authenticated (`gh auth status`).
3. For each action, ask the user before executing — never auto-execute.
4. Confirm success by checking the response.
5. Log the action in `.repo-growth/social-proof.jsonl`.

## Prompt template

```
I can star {repo} on GitHub for you. This takes 2 seconds and helps the project.
Run: gh api -X PUT /user/starred/{owner}/{repo}

Shall I do it?
```

## When to ask

- **Star**: When the repo scores 60+ on the growth audit. The user already finds it valuable enough to audit.
- **Watch**: Only when the user wants to track the repo's progress over time.
- **Fork**: When the user might want to contribute. Only offer if they show interest in contributing.
- **Follow**: When the repo's maintainer is notable in the space.

## Rules

- Never auto-execute. Always ask for explicit confirmation.
- Never fake stars (create multiple accounts, bot accounts, etc.).
- Never pressure the user. One gentle offer per session is enough.
- If the `gh` CLI is not available, tell the user: "I can do this if you install the GitHub CLI (`gh`)."
- Log every action in `.repo-growth/social-proof.jsonl`.

## Log format

```jsonl
{"date":"2026-06-17","action":"star","repo":"owner/repo","result":"success","note":"User confirmed"}
{"date":"2026-06-17","action":"star","repo":"owner/repo","result":"skipped","note":"gh CLI not available"}
```
