---
name: 003-agents-installation
description: Use when you need to install the embedded robot agents into either .cursor/agents or .claude/agents, selecting the destination interactively and copying the embedded agent definitions from project assets. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.14.0
---
# Embedded agents installer

Install a predefined set of embedded agent definitions from repository assets into a user-selected target directory. This is an interactive skill.

**What is covered in this Skill?**

- Interactive target selection (`.cursor/agents` or `.claude/agents`)
- Deterministic copy of the embedded six-agent bundle
- Idempotent re-installation with clear overwrite reporting

## Constraints

This skill installs only the embedded robot agents bundle and must ask for destination before writing files.

- **MUST** ask the user to choose `.cursor/agents` or `.claude/agents` before installing
- **MUST** copy all embedded files from `skills-generator/src/main/resources/system-prompts/assets/agents/`
- **MUST** preserve file names and report overwrite actions

## When to use this skill

- Install embedded agents
- Bootstrap .cursor/agents
- Bootstrap .claude/agents
- Copy robot agents

## Reference

For detailed guidance, examples, and constraints, see [references/003-agents-installation.md](references/003-agents-installation.md).
