---
name: consult
description: "Technical consultation without implementation. Use when the user invokes /consult or asks questions about the code or approach."
---

# Consult Command

## Behavior Profile

Use the `planner` skill as the behavior profile for this command.
Treat its rules as mandatory.

Follow `CLAUDE.md`, `conventions.md`, and `ARCHITECTURE.md`.

## Task

Answer technical questions or help understand code.

## Interaction Contract

- No confirmation needed
- No file creation
- Chat response only

## Algorithm

1. If question is missing, ask for it.
2. Study relevant parts of the codebase and patterns.
3. Respond with a brief, structured answer.
4. Use code only for illustration.

## Important

- Do not create files
- Do not implement changes
