# Example: README Before/After

## Before (typical weak README)

```markdown
# seo-skills

Some SEO tools for Claude Code.

## Installation

npx skills add marketingskills/seo

## Skills

- seo-audit
- content-analysis
- proposal-gen

## License

MIT
```

## After (growth-optimised README)

```markdown
# marketingskills/seo

> Open-source SEO workflows for your AI agent.
> Technical audits, content analysis, and live Search Console data.

⚡ **Try this first:**

```
Analyse my Search Console data and find pages losing clicks in the last 28 days.
```

[Install](#install) · [Skills](#skills) · [Examples](#examples) · [Upgrade](#upgrade)

---

## Why this exists

SEO data lives in Search Console. Analysis happens in spreadsheets.
These skills bridge that gap: your agent runs the workflows, you get the insights.

## Install

```bash
npx skills add marketingskills/seo
```

Verify it works:

```bash
skills list | grep seo
```

## Try this first

Paste this into your agent:

```
Find content decay in my Search Console data and suggest updates for the top 5 declining pages.
```

Expected output: a table with pages, click loss, and specific content update suggestions.

![Example output](assets/demo-output.png)

## Skills included

| Skill | What it does |
|---|---|
| `seo-audit` | Technical SEO audit of any URL |
| `content-analysis` | Finds content decay and refresh opportunities |
| `proposal-gen` | Generates client-ready SEO proposals |
| `traffic-detective` | Identifies pages losing search traffic |

## Demo

![Demo GIF](assets/demo.gif)

## Upgrade

Use the open-source skills locally. Connect RefreshAgent when your agent needs
live Google Search Console or GA4 data.

[Get started with live data →](https://refreshagent.com)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). All contributions welcome.

## Roadmap

- [x] Technical SEO audit
- [x] Content refresh planner
- [ ] Keyword gap analysis
- [ ] Competitor SEO analysis
- [ ] Scheduled SEO reports

## License

MIT © marketingskills
```

## Key changes

1. **Hero section** now includes value prop + try-it-first prompt
2. **Install** includes verification step
3. **"Try this first"** shows expected output
4. **Demo section** with GIF placeholder
5. **Upgrade section** makes the commercial path clear
6. **Contributing** section appears
7. **Roadmap** shows project is alive
8. **Skills table** provides quick-scan utility
