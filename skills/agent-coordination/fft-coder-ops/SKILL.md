---
name: fft-coder-ops
description: Operate FFT_nano coding delegation flows safely using /coder and /coder-plan, preserving main-chat-only policy, request-id tracking, and non-duplicative streaming behavior.
---

# FFT Coder Ops

Use this skill when handling coding delegation operations in FFT_nano.

## Guardrails

- Never run destructive git commands unless explicitly requested.
- Preserve unrelated worktree changes.
- Never bypass main-chat-only coder delegation safety rules.
- Do not add automatic delegation; delegation remains explicit trigger-based.

## Delegation Triggers

Explicit execute:

- `/coder <task>`
- `use coding agent`
- `use your coding agent skill`

Explicit plan-only:

- `/coder-plan <task>`

Natural-language coding requests without explicit trigger must not auto-delegate.

## Chat Safety Rules

- Delegation is only available in main/admin chat.
- Non-main chats may request coding help, but must be handled directly or rejected for delegation.
- Scheduled tasks must not trigger coder delegation.

## Runtime Expectations

- Execute mode delegates once and returns delegated outcome.
- Plan mode returns implementation/test plan without direct edits in outer orchestrator turn.
- Delegation run IDs are generated (`coder-<timestamp>-<suffix>`) and surfaced in progress messages.
- Progress streaming should avoid final duplicate full-message sends.

## Operator Commands

Main Telegram chat commands:

- `/coder <task>`
- `/coder-plan <task>`

Alias phrases in main chat:

- `use coding agent`
- `use your coding agent skill`

## Validation Checklist

- Non-main `/coder` is rejected with safety message.
- Main `/coder` triggers delegation run start message.
- Main `/coder-plan` triggers plan run start message.
- Existing Telegram delegation safety rules remain unchanged.
