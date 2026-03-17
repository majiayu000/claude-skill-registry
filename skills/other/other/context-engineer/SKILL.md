---
name: context-engineer
version: 1.0.1
description: Context window optimizer — analyze, audit, and optimize your agent's context utilization. Know exactly where your tokens go before they're sent.
author: Anvil AI
license: MIT
homepage: https://github.com/cacheforge-ai/cacheforge-skills
user-invocable: true
tags:
  - cacheforge
  - context-engineering
  - token-optimization
  - llm
  - ai-agents
  - prompt-optimization
  - observability
  - discord
  - discord-v2
metadata: {"openclaw":{"emoji":"🔬","homepage":"https://github.com/cacheforge-ai/cacheforge-skills","requires":{"bins":["python3"]}}}
---

## When to use this skill

Use this skill when the user wants to:
- Understand where their context window tokens are going
- Analyze workspace files (SKILL.md, SOUL.md, MEMORY.md, etc.) for bloat
- Audit tool definitions for redundancy and overhead
- Get a comprehensive context efficiency report
- Compare before/after snapshots to measure optimization progress
- Optimize system prompts for token efficiency

## Commands

```bash
# Analyze workspace context files — token counts, efficiency scores, recommendations
python3 skills/context-engineer/context.py analyze --workspace ~/.openclaw/workspace

# Analyze with a custom budget and save a snapshot for later comparison
python3 skills/context-engineer/context.py analyze --workspace ~/.openclaw/workspace --budget 128000 --snapshot before.json

# Audit tool definitions for overhead and overlap
python3 skills/context-engineer/context.py audit-tools --config ~/.openclaw/openclaw.json

# Generate a comprehensive context engineering report
python3 skills/context-engineer/context.py report --workspace ~/.openclaw/workspace --format terminal

# Compare two snapshots to see projected token savings
python3 skills/context-engineer/context.py compare --before before.json --after after.json
```

## What It Analyzes

- **System prompt efficiency** — Length, redundancy detection, compression potential
- **Tool definition overhead** — Count tools, per-tool token cost, identify unused/overlapping
- **Memory file bloat** — MEMORY.md size, stale entries, optimization suggestions
- **Skill overhead** — Installed skills contributing to context, per-skill token cost
- **Context budget** — What % of model context window is consumed by static content vs available for conversation

## Options

- `--workspace PATH` — Path to workspace directory (default: `~/.openclaw/workspace`)
- `--config PATH` — Path to OpenClaw config file (default: `~/.openclaw/openclaw.json`)
- `--budget N` — Context window token budget (default: 200000)
- `--snapshot FILE` — Save analysis snapshot to FILE for later comparison
- `--format terminal` — Output format (currently: terminal)

## Notes

- Token estimates are approximate (~4 characters per token). For precise counts, use a model-specific tokenizer.
- No external dependencies required — runs with Python 3 stdlib only.
- Built by Anvil AI — context engineering experts. https://labs.anvil-ai.io
