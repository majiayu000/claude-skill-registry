---
name: person
description: People management. Dispatches to Ada.
argument-hint: "[action: onboard] [args...]"
---

# Person

Manage people in your network. This skill dispatches to Ada.

## Usage

- `/person onboard "firstname-lastname"` — Create person dossier

## Dispatch

Parse first argument and invoke Ada with the corresponding reference:
- `onboard` → Invoke @ada to execute `references/person/onboard.md`

If no subaction provided, show usage and ask which action to run.
