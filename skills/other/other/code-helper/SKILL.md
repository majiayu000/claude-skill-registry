---
name: code-helper
description: Assists with code quality tasks. Use when reviewing code, checking for issues, or improving code quality. NOT for: writing new features from scratch.
model: sonnet
hooks:
  PreToolUse:
    - matcher: Write|Edit
      type: prompt
      prompt: "Verify the proposed edit follows the code patterns in references/patterns.md before allowing."
---

# Code Helper

Provides guidance for code quality improvements.

## When to Use

- User asks for code review
- User wants to improve code quality
- User mentions "clean code" or "refactor"
- NOT for: writing new features from scratch

## Quick Reference

| Task | Action |
|------|--------|
| Review code | Read file, check patterns |
| Find issues | Use Grep for anti-patterns |
| Suggest fixes | Provide specific improvements |

## Review Process

1. Read the code file
2. Check against references/patterns.md
3. Identify issues
4. Suggest improvements with examples

## See Also

- `references/patterns.md` - Code patterns to check
