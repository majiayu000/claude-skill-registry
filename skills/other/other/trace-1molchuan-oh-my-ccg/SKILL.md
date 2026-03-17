---
name: trace
description: 显示 Agent 流程追踪时间线与摘要
---

# oh-my-ccg Trace

Display chronological agent flow trace.

## Usage
`/oh-my-ccg:trace` — Show full timeline
`/oh-my-ccg:trace --summary` — Aggregate statistics only
`/oh-my-ccg:trace --filter <type>` — Filter: hooks, skills, agents, tools

## Data Source
Reads from `.oh-my-ccg/state/hud-state.json` which is populated by hook scripts tracking tool calls, agent lifecycles, and skill activations.

## Timeline Format
```
[14:23:01] HOOK    SessionStart         → State restored (phase: PLAN)
[14:23:05] SKILL   oh-my-ccg-impl      → Activated
[14:23:08] AGENT   explore (H)          → Started (scanning codebase)
[14:23:12] TOOL    Glob                 → 23 files matched
[14:23:15] AGENT   explore (H)          → Completed (45s)
[14:23:16] AGENT   executor (S)         → Started
[14:23:30] TOOL    Write                → src/auth/login.ts
[14:24:00] AGENT   executor (S)         → Completed (44s)
```

## Summary Format
```
Session Summary:
  Duration: 19m
  Agents: 4 spawned (explore×1, executor×2, verifier×1)
  Tools: 47 calls (Write×12, Read×18, Bash×8, Glob×9)
  Skills: 2 activated (oh-my-ccg-impl, cancel)
  Hooks: 23 fired (PreToolUse×12, PostToolUse×8, Stop×3)
```
