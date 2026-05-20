---
name: testing
description: Unified testing commands and patterns across frontend and backend.
last_updated: 2025-12-20
---

# Testing Skill

## Overview

Guidance and templates for testing in {PROJECT_NAME}. Covers React Component testing (Vitest/RTL) and Backend testing (Python/Pytest).

## When To Use

- **Writing new code**: Every new feature needs tests.
- **Fixing bugs**: Create a reproduction test first.
- **Refactoring**: Ensure green tests before and after.

## Instrumentation

```bash
# Log usage when using this skill
Call MCP `call_tool_logger_manager` { action: "logSkill", name: "testing", outcome: "manual" }
```

## What do you want to do?

1. **Test React Components** → `workflows/run-frontend-tests.md`
2. **Test Backend/API** → `workflows/run-backend-tests.md`
3. **Write a New Test** → `templates/component-test.template.tsx`
4. **Fix Test Failures** → `references/vitest-patterns.md`

## Quick Commands

```bash
# Frontend (Unit/Integration)
npm test
npm test -- -t "ComponentName"  # Run specific test

# Backend (API)
pytest
pytest -k "test_name"
```
