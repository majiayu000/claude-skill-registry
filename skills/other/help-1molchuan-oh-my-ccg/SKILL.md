---
name: help
description: oh-my-ccg 帮助与使用指南
---

# oh-my-ccg Help

Display the help and usage guide for oh-my-ccg.

## Output the following:

```
oh-my-ccg v1.0.0 — Unified Claude Code Plugin
RPI Workflow + Multi-Model Orchestration + Agent System

COMMANDS:
  /oh-my-ccg:init              Initialize environment (OpenSpec + Codex + Gemini)
  /oh-my-ccg:research "desc"   Research phase: requirements → constraint sets
  /oh-my-ccg:plan              Plan phase: constraints → zero-decision executable plan
  /oh-my-ccg:impl              Impl phase: mechanical execution of plan
  /oh-my-ccg:review            Dual-model cross-review (available anytime)
  /oh-my-ccg:cancel            Cancel active orchestration modes
  /oh-my-ccg:help              This help message

RPI WORKFLOW:
  init → research → /clear → plan → /clear → impl → review

  State persists across /clear in .oh-my-ccg/state/rpi-state.json

AGENTS (8):
  explore (H)   — Codebase discovery
  analyst (O)   — Requirements & constraints  (+Codex)
  planner (O)   — Task decomposition         (+Codex +Gemini)
  executor (S)  — Code implementation
  verifier (S)  — Completion verification     (+Codex)
  reviewer (S)  — Comprehensive review        (+Codex +Gemini)
  critic (O)    — Plan/design challenge       (+Codex)
  writer (H)    — Documentation               (+Gemini)

  Model tiers: O=Opus, S=Sonnet, H=Haiku
  +Codex/+Gemini = automatic multi-model routing

MULTI-MODEL ROUTING:
  Backend tasks → Codex (gpt-5.3-codex)
  Frontend tasks → Gemini (gemini-3-pro-preview)
  Cross-validation → Both in parallel

HUD PRESETS:
  minimal   — Single line status
  focused   — Default, 4-line view
  full      — Complete with model status
  analytics — Cost and cache tracking

Configure: .oh-my-ccg/config.json
```
