---
name: test-skill
description: A test skill for validating the unified skills system
version: "2.0.0"
license: MIT
disable-model-invocation: true
allowed-tools: Bash, Read, Edit
argument-hint: "[--verbose] <target>"
compatibility: Requires Node.js 22+
model: claude-sonnet-4-20250514
context: fork
tags:
  - testing
  - fixtures
  - validation
metadata:
  author: test-author
  tags:
    - quality
  category: testing
---

# Test Skill

This is a test skill for the unified skills system.

## Usage

Use $ARGUMENTS to pass arguments to this skill.

```bash
echo "Running test skill with args: $ARGUMENTS"
```

## Details

This skill validates that all frontmatter fields are correctly parsed.
