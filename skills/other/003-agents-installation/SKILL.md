---
name: 003-agents-installation
description: Use when you need to install the embedded robot agents into either .cursor/agents or .claude/agents, selecting the destination interactively and copying the embedded agent definitions from project assets. This should trigger for requests such as Install embedded agents; Bootstrap .cursor/agents; Bootstrap .claude/agents; Copy robot agents. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Embedded agents installer

Install a predefined set of embedded agent definitions from repository assets into a user-selected target directory. This is an interactive skill.

**What is covered in this Skill?**

- Interactive target selection (`.cursor/agents` or `.claude/agents`)
- Deterministic copy of all embedded agents defined via XInclude from `assets/agents`
- Idempotent re-installation with clear overwrite reporting

## Constraints

This skill installs only the embedded robot agents bundle and must ask for destination before writing files.

- **MUST** ask the user to choose `.cursor/agents` or `.claude/agents` before installing
- **MUST** copy all embedded agent files defined in `references/003-agents-installation.md`
- **MUST** preserve file names from the reference content and report overwrite actions

## When to use this skill

- Install embedded agents
- Bootstrap .cursor/agents
- Bootstrap .claude/agents
- Copy robot agents

## Workflow

1. **Choose destination**

Ask exactly one question to choose `.cursor/agents` or `.claude/agents` and wait for an explicit answer before copying files.

Step constraints:
- Do not copy any file until destination is explicitly confirmed
- If destination is ambiguous, ask a clarification question

2. **Install embedded agents**

Create the destination directory if needed, then copy all embedded agent files defined in the reference content, preserving filenames and warning before overwriting existing files.

3. **Report installation result**

Return a concise checklist with selected destination, created/updated files, overwrite actions, and an optional verification command.

## Reference

For detailed guidance, examples, and constraints, see [references/003-agents-installation.md](references/003-agents-installation.md).
