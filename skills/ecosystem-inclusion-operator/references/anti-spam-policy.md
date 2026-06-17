# Anti-Spam Policy

These are hard constraints. The agent must enforce them.

## Daily limits

- PRs opened: max 3 per day
- Issues opened: max 5 per day
- Follow-ups: 1 per PR, 14 days after no response, then stop

## Banned actions

- Opening generic / untailored PRs (same body text on every submission).
- Submitting to repos unrelated to the promoted project's category.
- Hiding commercial affiliation in PR descriptions or issue bodies.
- Using fake neutrality ("I just found this project..." when you are the maintainer).
- Adding tracking links, UTM parameters, or analytics pixels.
- Repeatedly following up after a maintainer says no.
- Arguing with maintainers in PR or issue comments.
- Submitting to repos with an explicit "no promotional PRs" or "no self-promotion" policy.
- Creating multiple accounts to bypass limits.

## PR body template

```
Hi! I maintain `owner/repo`, [one-line description].

I noticed this repo has a section for [category], so I'm proposing a small
addition. I kept the description neutral and can adjust or remove it if it
doesn't fit the list's scope.
```

## Enforcement

If any of these rules are violated, the action must be cancelled and logged in `decisions.md` with the reason. The agent should never suggest a workaround.
