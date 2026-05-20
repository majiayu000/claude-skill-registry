---
name: filesystem
description: Execution-layer skill for filesystem operations
---

## Commands

- fs.readFile
- fs.writeFile
- fs.applyPatch
- fs.glob

## Constraints

- Never access paths outside the active project workspace unless explicitly granted.
- Do not embed governance or routing logic in this skill; it only exposes filesystem capabilities.
