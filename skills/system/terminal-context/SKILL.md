---
name: terminal-context
description: >-
  Complete Kitty terminal awareness + control for coding agents: list panes/tabs,
  read scrollback, map ports→processes, parse per-pane git/last-command metadata
  (from shell hooks), and send commands/focus panes. Use when user mentions
  "another terminal", "is the server running", "what failed", or you need to
  run/inspect commands across panes.
---

# terminal-context

## Default rule
Prefer `tc-context`, `tc-output`, `tc-send`, and `tc-watch` over manual copy/paste when you need terminal state from other Kitty panes.

## Quickstart
1) `tc-context --summary`
2) `tc-context --insights`
3) `tc-output --cwd "$PWD" --lines 120 --match "error|failed|traceback"`
4) `tc-send --cwd "$PWD" "npm test"`
5) `tc-watch --cwd "$PWD" "ready|listening|compiled" --timeout 90`

## Safety contract
- Prefer read operations (`tc-context`, `tc-output`) before sending commands to other panes.
- Before destructive actions, confirm you have the correct pane and `cwd`.

## Setup
- For deterministic/non-interactive use, enable a Kitty socket (`listen_on`) and install shell hooks. See `references/SETUP.md`.
