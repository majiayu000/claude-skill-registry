---
name: tmux-layout
description: "Use this skill when the operator wants a prepared tmux visualization layout for the session's side-channels (STATE.md tail, CI-watch, events.jsonl tail). Renders a 4-pane default layout or debug layout. Read-only side-channel observability — the coordinator chat stays in the operator's original terminal. Trigger phrases: \"tmux layout\", \"split panes for ci watch\", \"visualize session side-channels\", \"show me state-md tail and ci\"."
metadata:
  model: inherit
  color: cyan
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
---

# tmux-layout

> **Portable mirror — generated, do not edit.** The canonical skill body lives at
> [`skills/tmux-layout/SKILL.md`](../../../skills/tmux-layout/SKILL.md); read that file for the full instructions.
> This mirror carries only agentskills.io-spec-legal frontmatter so harnesses that
> discover skills under `.agents/skills/` can find and route to the skill.
>
> Regenerate with `node scripts/generate-agents-skills.mjs`.
