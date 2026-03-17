---
name: multi-llm-consult
description: Consult external LLMs (Gemini, OpenAI/Codex, Qwen) for second opinions, alternative plans, independent reviews, or delegated tasks. Use when a user asks for another model's perspective, wants to compare answers, or requests delegating a subtask to Gemini/Codex/Qwen.
---

# Multi-LLM Consult

## Overview

Use a bundled script to query external LLM providers with a sanitized prompt and return a concise comparison.

## Setup

- Configure API keys in the TUI: open the Command Palette (Ctrl+P) and run **Configure LLM Providers**.
- Keys are stored in `settings.json` under `llm_providers`.

## Workflow

1. Identify the **purpose** (`second-opinion`, `plan`, `review`, `delegate`).
2. Summarize the task and **sanitize sensitive data** before sending it out.
3. Run the consult script with the chosen provider.
4. Compare responses and reconcile with your own plan before acting.

## Consult Script

Always run `--help` first:

```bash
python scripts/consult_llm.py --help
```

Example: second opinion

```bash
python scripts/consult_llm.py \
  --provider gemini \
  --purpose second-opinion \
  --prompt "We plan to refactor module X. What risks or gaps do you see?"
```

Example: delegate a review

```bash
python scripts/consult_llm.py \
  --provider qwen \
  --purpose review \
  --prompt-file /tmp/review_request.md \
  --context-file /tmp/patch.diff
```

Example: plan check with Codex (OpenAI)

```bash
python scripts/consult_llm.py \
  --provider codex \
  --purpose plan \
  --prompt "Draft a 5-step plan for implementing feature Y."
```

## Output Handling

- Treat responses as advisory; verify against repo constraints and current state.
- Summarize the external response in 3-6 bullets before acting.
- If responses conflict, call out the differences explicitly and choose a path.

## References

- Provider defaults and configuration: `references/providers.md`
