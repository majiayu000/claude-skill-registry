---
name: debug
description: Systematic debugging with structured reproduction and root cause analysis.
last_updated: 2025-12-20
---

# Debug Skill

## Overview

Don't guess; verify. This skill guides you through the systematic process of identifying, reproducing, and fixing bugs.

## When To Use

- **Users report a bug**
- **You encounter an unexpected error**
- **Tests are failing inexplicably**

## Instrumentation

```bash
# Log usage when using this skill
Call MCP `call_tool_logger_manager` { action: "logSkill", name: "debug", outcome: "manual" }
```

## What do you want to do?

1. **Reproduce an issue** → `workflows/reproduce-issue.md`
2. **Find Root Cause** → `workflows/root-cause-analysis.md`
3. **Create Bug Report** → `templates/bug-report.template.md`
4. **Research Error Messages** → `references/common-errors.md`

## The Golden Rule of Debugging

> **"If you haven't reproduced it, you haven't fixed it."**

Always implement a reproduction case (test or script) BEFORE attempting a fix. Create a minimal reproduction test case that triggers the issue.

> [!NOTE]
> No top-level `debug/` folder exists. Use `skills/debug/` for guidance.
