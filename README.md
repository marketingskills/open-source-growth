# open-source-growth

> Growth skills for open-source repos. Give your AI agent a growth team for your open-source project.

[![License](https://img.shields.io/github/license/marketingskills/open-source-growth?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](CONTRIBUTING.md)

---

**Are you an agent?** Read [AGENTS.md](AGENTS.md) first. Then load `skills/repo-growth-operator/SKILL.md` or `skills/ecosystem-inclusion-operator/SKILL.md`.

**Are you a human?** 📋 Copy this prompt to any AI:

```
Help me grow my open-source repo using marketingskills/open-source-growth
```

---

## What this repo does

Two agent skills that turn "random GitHub repo" into a trusted, installable, shareable project.

| Skill | What it does |
|---|---|
| [repo-growth-operator](skills/repo-growth-operator/) | Audit README, fix install flow, generate demos, create launch packs, scaffold trust files, design monetisation, build social proof. |
| [ecosystem-inclusion-operator](skills/ecosystem-inclusion-operator/) | Find relevant awesome lists, directories, and repos. Score targets. Open non-spammy PRs. Track progress with `/loop`. Star high-quality targets. |

## Why this exists

Building an open-source repo is one thing. Making it discoverable, trustworthy, and installable is a completely different skill. These skills package that skill so your AI agent can help you grow your repo the same way a growth team would.

## Quick start

```bash
# Install the skills
npx skills add marketingskills/open-source-growth

# Or curl:
curl -fsSL https://raw.githubusercontent.com/marketingskills/open-source-growth/main/install.sh | bash

# Then ask your agent:
# "Audit my repo for adoption blockers"
```

## Example prompts

```
"Audit this open-source skill repo for adoption, trust, and conversion:
https://github.com/marketingskills/seo"

"Rewrite this README to maximise installs, stars, and first-run success."

"Find relevant awesome lists and start inclusion PRs for my repo."

"Star this high-quality target repo for me."  (requires gh CLI)
```

## Ethical growth

Every suggestion in these skills is governed by an [ethical growth policy](skills/repo-growth-operator/references/ethical-growth-policy.md). We do not recommend spam, fake stars, fake contributors, or deceptive metadata.

## Growth hacks this skill knows

Talk to your agent about any of these:

- **Repo audit** — score your repo, find adoption blockers
- **README rewrite** — install clarity + first-run success
- **Demo builder** — GIF scripts, Loom outlines, screenshots
- **Launch pack** — LinkedIn, X, HN, Reddit posts
- **Trust scaffolding** — issue templates, CI, CONTRIBUTING
- **Marketplace optimisation** — better SKILL.md metadata
- **Monetisation bridge** — OSS-to-paid conversion path
- **Ecosystem inclusion** — find and PR into relevant awesome lists
- **Social proof** — star, watch, fork via `gh` CLI
- **Install script** — `curl | bash` installer with auto-update

## Related

- [`marketingskills/seo`](https://github.com/marketingskills/seo) — Open-source SEO workflows for AI agents.

## License

MIT © marketingskills
