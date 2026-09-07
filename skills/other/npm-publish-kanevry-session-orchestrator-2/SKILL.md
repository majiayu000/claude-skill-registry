---
name: npm-publish
description: Use when publishing this package to npm — a version release (npm publish), verifying the registry/pi.dev listing, or diagnosing npm auth failures (E403 2FA/token errors). Token-based flow via NPM_TOKEN in .env.local with a temp userconfig, the leakage gate before every publish, post-publish verification and marker/badge upkeep. Trigger on "publish to npm", "npm release", "E403 publish error".
metadata:
  user-invocable: "true"
  model: sonnet
---

# npm-publish

> **Portable mirror — generated, do not edit.** The canonical skill body lives at
> [`skills/npm-publish/SKILL.md`](../../../skills/npm-publish/SKILL.md); read that file for the full instructions.
> This mirror carries only agentskills.io-spec-legal frontmatter so harnesses that
> discover skills under `.agents/skills/` can find and route to the skill.
>
> Regenerate with `node scripts/generate-agents-skills.mjs`.
