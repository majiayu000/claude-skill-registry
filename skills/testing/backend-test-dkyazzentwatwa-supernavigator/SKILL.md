---
name: backend-test
description: Generate backend tests (unit, integration, mocks). Auto-invoke when user says "write test for", "add test", "test this", or "create test".
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
version: 1.0.0
---

# Backend Test Generator

Generate comprehensive backend tests with Jest/Vitest including fixtures and mocks.

## When to Invoke

Auto-invoke when user mentions:
- "Write test for"
- "Add test"
- "Test this"
- "Create test"
- "Test [component/function]"

## What This Does

1. Generates test file with describe/it blocks
2. Creates test fixtures
3. Generates mocks for dependencies
4. Includes edge cases
5. Follows testing best practices

## Success Criteria

- [ ] Test file generated with proper structure
- [ ] Tests cover happy path and error cases
- [ ] Mocks isolate unit under test
- [ ] Fixtures provide test data
- [ ] Tests are runnable and pass

**Auto-invoke when writing backend tests** 🧪
