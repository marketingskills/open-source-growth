# open-source-growth

> Growth skills for open-source repos. Give your AI agent a growth team for your open-source project.

[![License](https://img.shields.io/github/license/marketingskills/open-source-growth?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](CONTRIBUTING.md)

This repo contains agent skills that help founders, developers, and open-source maintainers grow their projects — from "random GitHub repo" to trusted, installable, shareable project.

## Skills included

| Skill | What it does |
|---|---|
| [repo-growth-operator](skills/repo-growth-operator/) | Audit README, fix install flow, generate demos, create launch packs, scaffold trust files, and design monetisation. |
| [ecosystem-inclusion-operator](skills/ecosystem-inclusion-operator/) | Find relevant awesome lists, directories, and repos. Open non-spammy PRs. Track progress with `/loop`. |

## Why this exists

Building an open-source repo is one thing. Making it discoverable, trustworthy, and installable is a completely different skill. These skills package that skill so your AI agent can help you grow your repo the same way a growth team would.

## Quick start

```bash
# Install a skill
npx skills add marketingskills/open-source-growth

# Audit your repo
# Use the repo-growth-operator's "repo-audit" mode

# Start ecosystem inclusion
# Use the ecosystem-inclusion-operator with /discover-targets
```

## Mode examples

```
"Audit this open-source skill repo for adoption, trust, and conversion: https://github.com/marketingskills/seo"

"Rewrite this README to maximise installs, stars, and first-run success."

"Find relevant awesome lists and start inclusion PRs for my repo."
```

## Ethical growth

Every suggestion in these skills is governed by an [ethical growth policy](skills/repo-growth-operator/references/ethical-growth-policy.md). We do not recommend spam, fake stars, fake contributors, or deceptive metadata.

## Related

- [`marketingskills/seo`](https://github.com/marketingskills/seo) — Open-source SEO workflows for AI agents.

## License

MIT © marketingskills
