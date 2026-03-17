---
name: template-new-skill
description: Generate a skeleton template for a new Claude Code Skill.
allowed-tools: Read, Grep, Glob, Bash:just
id: B90F6D72-BB47-434C-8BDC-3C880E13AC9A
---

# Template New Skill

This Skill provides read-only file access.

## Instructions

1. Use Read to view file contents
2. Use Grep to search within files
3. Use Glob to find files by pattern

## Requirements

Packages must be installed in your environment:

```bash
NAME="skill name here" \
SCOPE="personal||project" \
DESC="Some description of the skill here" \
just init
```
