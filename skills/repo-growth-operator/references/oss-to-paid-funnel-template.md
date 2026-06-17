# OSS-to-Paid Funnel Template

Design the conversion path from free open-source skill to paid / hosted product.

## The principle

> OSS layer = reusable skill, prompt, workflow.
> Paid layer = hosted data, auth, compute, storage, team features, support, compliance.

Never cripple the OSS project. The free version must be genuinely useful on its own.

## Funnel layers

### Layer 1: Free (OSS)

Everything in the repo:
- All skills / workflows / prompts.
- Runs with the user's own API keys.
- Self-serve documentation.
- Community support via issues.

### Layer 2: Paid trigger

The specific pain point that justifies payment:
- Live third-party API data (Search Console, GA4, CRM, etc.).
- Multi-user / team workspaces.
- Scheduled / automated runs.
- Persistent storage of outputs.
- SLA / support.
- Compliance / audit trail.

### Layer 3: CTA placement

- README "Upgrade" section below the install instructions.
- In skill output: "To automate this with live data, connect [Service]."
- Not pushed into every response. Present but not intrusive.

## CTA copy pattern

```
Use the open-source skill locally. Connect [Service Name] when your agent needs
[live data / team features / scheduled reports / compliance].

[Get started →](https://example.com)
```

## Anti-patterns

- Do not remove features from the OSS version to create artificial scarcity.
- Do not add tracking or ads to the OSS version.
- Do not make the install experience worse for free users.
- Do not hide documentation behind a paywall.

## Example

| Layer | What | Where |
|---|---|---|
| Free | All SEO workflows, audit templates, content briefs | GitHub repo |
| Paid trigger | Live GSC/GA4 data, multi-client workspaces | hosted service |
| CTA | "Connect RefreshAgent when your agent needs live data" | README + skill output footer |
