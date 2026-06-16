---
name: 004-commands-installation
description: Use when you need to install the embedded project commands into command directories (.github/commands, .claude/commands, .cursor/command, .codex/commands), selecting the destination interactively and copying the embedded command definitions from project assets. This should trigger for requests such as Install embedded commands; Bootstrap .cursor/command; Bootstrap .claude/commands; Copy project commands; Install project command suite. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# Embedded commands installer

Install a predefined set of embedded project commands from repository assets into a user-selected target directory. This is an interactive skill.

**What is covered in this Skill?**

- Interactive target selection (`.github/commands`, `.claude/commands`, `.cursor/command`, or `.codex/commands`)
- Deterministic copy of all embedded commands defined via XInclude from `assets/commands`
- Idempotent re-installation with clear overwrite reporting
- Support for four command framework destinations

## Constraints

This skill installs only the embedded project commands bundle and must ask for destination before writing files.

- **MUST** ask the user to choose one of four command destinations before installing
- **MUST** copy all embedded command files defined in `references/004-commands-installation.md`
- **MUST** preserve file names from the reference content and report overwrite actions
- **MUST** create the destination directory if it does not exist

## Reference

For detailed guidance, examples, and constraints, see [references/004-commands-installation.md](references/004-commands-installation.md).
