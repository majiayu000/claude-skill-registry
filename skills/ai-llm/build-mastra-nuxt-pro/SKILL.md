---
name: build-mastra-nuxt-pro
description: Use when creating a production-minded Nuxt frontend Mastra agent with pnpm, based on a plain chat assistant (not weather), including preflight checks, architecture decisions, troubleshooting, and acceptance gates.
license: Apache-2.0
metadata:
  version: "1.0.1"
  domain: mastra-nuxt
  level: pro
---

# Build Mastra Nuxt Pro

Use this skill when the user wants a complete Nuxt + Mastra implementation path with reliability checks.

## Trigger

- "Create Nuxt Mastra agent in production style"
- "Nuxt + Mastra full setup with checklist"
- "pnpm Nuxt Mastra pro workflow"

## Target Outcome

- Nuxt frontend chat UX with streaming
- Mastra plain chat assistant (`chat-agent`) instead of weather assistant
- Clear PDCA-style implementation and verification
- Operational guardrails for env, routing, and regression checks

## Stage-Gated Workflow

1. Preflight
2. Scaffold and dependency setup
3. Agent conversion (weather -> chat) with DeepSeek model `model="deepseek/deepseek-chat"`
4. API route integration
5. UI integration
6. Validation and acceptance
7. Optional hardening

## Must-Follow Constraints

- Use `pnpm` only.
- Keep agent as generic chat assistant unless user asks for tools.
- Default model for this skill is DeepSeek chat: `model="deepseek/deepseek-chat"`.
- Do not use OpenAI API as the default model path in this skill flow.
- Do not include secrets in source/docs/logs.
- Keep all edits incremental and rollback-friendly.
- If versions conflict, prioritize installed package docs and types.

## Required References

- `references/quickstart.md`
- `references/architecture.md`
- `references/troubleshooting.md`
- `references/acceptance-checklist.md`

## Scripts

- Run `scripts/preflight.sh` before coding.
- Use script output to decide whether to install/fix prerequisites first.

## Deliverables

1. change plan + impact surface
2. implementation steps with expected output
3. file-level change list
4. validation commands and pass/fail criteria
5. rollback plan
