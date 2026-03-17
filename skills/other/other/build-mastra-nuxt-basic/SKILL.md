---
name: build-mastra-nuxt-basic
description: Use when creating a Nuxt frontend Mastra agent with pnpm using a minimum viable plain chat assistant (non-weather agent). Trigger for requests like "Nuxt + Mastra basic setup", "pnpm Nuxt Mastra chat assistant", or "replace weather agent with normal chat agent".
license: Apache-2.0
metadata:
  version: "1.0.1"
  domain: mastra-nuxt
  level: basic
---

# Build Mastra Nuxt Basic

Use this skill when the user wants the smallest working Nuxt + Mastra chat assistant.

## Scope

- Frontend framework: Nuxt
- Package manager: pnpm only
- Agent style: plain chat assistant
- Explicitly avoid default weather assistant workflow

## Workflow (MVP)

1. Create Nuxt app (or reuse existing app).
2. Run `pnpm dlx mastra@latest init`.
3. Replace generated weather agent usage with `chat-agent`.
4. Configure the agent model as `model="deepseek/deepseek-chat"` (use DeepSeek, not OpenAI default).
5. Add Nuxt route `server/api/chat.ts` and wire `agentId: 'chat-agent'`.
6. Add chat UI in `app/app.vue` using AI SDK UI.
7. Run local verification (`pnpm dev`) and test send/receive chat.

## Hard Constraints

- Must use `pnpm`.
- Must not keep weather-specific naming in final implementation (`weather-agent`, weather prompt, weather tool).
- Must use DeepSeek model for this skill's agent setup: `model="deepseek/deepseek-chat"`.
- Must not default to OpenAI API in this skill flow.
- Keep changes minimal and rollback-friendly.
- Never put API keys in source code.

## Execution Notes

- Load `references/nuxt-mastra-chat-mvp.md` before implementation.
- If Mastra output path differs from defaults, locate actual export path with:
  - `rg "export const mastra" -n`
- If APIs differ by version, prioritize installed package docs over memory.

## Deliverable Format

- Provide:
  1. minimal changed files list
  2. run commands
  3. acceptance checks
  4. rollback note
