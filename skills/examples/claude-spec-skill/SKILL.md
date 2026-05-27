---
name: claude-spec-skill
description: A skill demonstrating all Claude Code spec fields.
argument-hint: "[issue-number] [--verbose]"
disable-model-invocation: true
user-invocable: false
allowed-tools: Read Write Bash(git:*)
model: claude-sonnet-4-5-20250929
context: fork
agent: reviewer
hooks:
  PreToolUse:
    - matcher: Bash
      command: echo "pre-tool hook"
---

# Claude Spec Skill

This skill tests parsing of all Claude Code specification frontmatter fields.

## Usage

Use this skill when testing Claude Code spec compliance.
