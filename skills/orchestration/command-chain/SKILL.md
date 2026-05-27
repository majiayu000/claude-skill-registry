---
name: command-chain
description: Use the /chain slash command to run the multi-phase agent chaining workflow with review loops. Use when: complex tasks needing explore/plan/build/quality/review gating.
---

# Command: /chain

Run the `/chain` workflow defined in `.claude/commands/chain.md`.

## Usage
`/chain <task_type> "<description>" [options]`

## Notes
- Task types: implement, fix, refactor, research, extend, clone, test, docs, security, ui, integration.
- Full options, phases, and output format: `.claude/commands/chain.md`.
