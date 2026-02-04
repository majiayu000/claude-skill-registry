---
name: model-switch
description: Switch the agent's model at runtime and restart. Use when the user asks to change models (e.g., "switch to kimi", "use opus", "go cheaper"), or when the agent decides a different model is better for the current workload.
---

# Model Switch

## Overview

This skill switches the agent's primary model by patching the gateway config and letting the gateway auto-restart. Use it when a user explicitly requests a model change or when you determine a different model is better suited for the task (cost, speed, quality).

## Workflow

### 1) Trigger
- User asks to change models ("switch to X", "use opus", "go cheaper")
- Or you decide a different model is better for the current workload

### 2) Map alias → full model ID
Use the reference table below to resolve common aliases. If the alias is unknown, ask for clarification or the exact model ID.

### 3) Patch gateway config
Update the primary model:
- `gateway config.patch` → `agents.defaults.model.primary = <full_model_id>`

### 4) Gateway restarts automatically
No manual restart needed.

### 5) Confirm to the user
Confirm the model switch in plain language.

## Reference: Known Model Aliases

| Alias | Full model ID |
| --- | --- |
| opus | anthropic/claude-opus-4-5 |
| sonnet | anthropic/claude-sonnet-4-5 |
| kimi | nvidia/moonshotai/kimi-k2.5 |
| codex | github-copilot/gpt-5.2-codex |

## Notes

- **Context resets after restart.** Warn the user if the switch happens mid-conversation.
- **Per-session override (no restart):** You can use the `session_status` tool with the `model` parameter to override the model for a single session without changing defaults.
