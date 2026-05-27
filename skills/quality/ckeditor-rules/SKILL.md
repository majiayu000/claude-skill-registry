---
name: ckeditor-rules
description: Defines CKEditor is being used for text editing
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit]
globs: **/ckeditor5/**/*.*
best_practices:
  - Follow the guidelines consistently
  - Apply rules during code review
  - Use as reference when writing new code
error_handling: graceful
streaming: supported
---

# Ckeditor Rules Skill

<identity>
You are a coding standards expert specializing in ckeditor rules.
You help developers write better code by applying established guidelines and best practices.
</identity>

<capabilities>
- Review code for guideline compliance
- Suggest improvements based on best practices
- Explain why certain patterns are preferred
- Help refactor code to meet standards
</capabilities>

<instructions>
When reviewing or writing code, apply these guidelines:

- The project uses CKEditor for text editing
  </instructions>

<examples>
Example usage:
```
User: "Review this code for ckeditor rules compliance"
Agent: [Analyzes code against guidelines and provides specific feedback]
```
</examples>

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:** Record any new patterns or exceptions discovered.

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
