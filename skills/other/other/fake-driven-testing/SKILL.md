---
name: fake-driven-testing
description:
  This skill should be used when writing tests, fixing bugs, adding features,
  or modifying the gateway layer. Use when you need guidance on testing architecture,
  working with fakes, implementing ABC gateway interfaces, or understanding the defense-in-depth
  testing strategy. Essential for maintaining test quality and understanding where
  different types of tests belong.
---

# Fake-Driven Testing Architecture for Python

**Use this skill when**: Writing tests, fixing bugs, adding features, or modifying gateway layers in Python projects.

**Prerequisites**: For Python code standards, load the `dignified-python-313` skill first. This skill focuses on testing architecture, not Python syntax.

## Overview

This skill provides a **defense-in-depth testing strategy** with five layers for Python applications:

```
┌─────────────────────────────────────────┐
│  Layer 5: Business Logic Integration Tests (5%)  │  ← Smoke tests over real system
├─────────────────────────────────────────┤
│  Layer 4: Business Logic Tests (70%)   │  ← Tests over fakes (MOST TESTS)
├─────────────────────────────────────────┤
│  Layer 3: Pure Unit Tests (10%)        │  ← Zero dependencies, isolated testing
├─────────────────────────────────────────┤
│  Layer 2: Integration Sanity Tests (10%)│  ← Fast validation with mocking
├─────────────────────────────────────────┤
│  Layer 1: Fake Infrastructure Tests (5%)│  ← Verify test doubles work
└─────────────────────────────────────────┘
```

**Philosophy**: Test business logic extensively over fast in-memory fakes. Use real implementations sparingly for integration validation.

**Terminology note**: The "gateway layer" (also called adapters/providers) refers to thin wrappers around heavyweight external APIs (databases, filesystems, HTTP APIs, message queues, etc.). The pattern matters more than the name.

## Quick Decision: What Should I Read?

**Adding a feature or fixing a bug?**
→ Read `quick-reference.md` first, then `workflows.md#adding-a-new-feature`

**Need to understand where to put a test?**
→ Read `testing-strategy.md`

**Working with Python-specific patterns?**
→ Read `python-specific.md`

**Adding/changing a gateway interface?**
→ Read `gateway-architecture.md`, then `workflows.md#adding-a-gateway-method`

**Creating a backend (higher-level abstraction over gateways)?**
→ Read `gateway-architecture.md#gateways-vs-backends` - backends compose gateways and do NOT have fakes

**Need to implement a specific pattern (CliRunner, builders, etc.)?**
→ Read `patterns.md`

**Not sure if I'm doing it right?**
→ Read `anti-patterns.md`

**Just need a quick lookup?**
→ Read `quick-reference.md`

## When to Read Each Reference Document

### 📖 `gateway-architecture.md`

**Read when**:

- Adding or changing gateway/ABC interfaces
- Understanding the ABC/Real/Fake/DryRun pattern
- Need examples of gateway implementations
- Want to understand what gateways are (and why they're thin)
- **Creating a backend** (higher-level abstraction that composes gateways)

**Contents**:

- What are gateway classes? (naming: gateways/adapters/providers)
- The four implementations (ABC, Real, Fake, DryRun)
- Code examples for each
- When to add/change gateway methods
- Design principles (keep gateways thin)
- Common gateway types (Database, API, FileSystem, MessageQueue)
- **Gateways vs Backends** - critical distinction for DI boundaries

### 📖 `testing-strategy.md`

**Read when**:

- Deciding where to put a test
- Understanding the five testing layers
- Need test distribution guidance (5/70/10/10/5 rule)
- Want to know which layer tests what

**Contents**:

- Layer 1: Unit tests of fakes (verify test infrastructure)
- Layer 2: Integration sanity tests with mocking (quick validation)
- Layer 3: Pure unit tests (zero dependencies, isolated testing)
- Layer 4: Business logic over fakes (majority of tests)
- Layer 5: Business logic integration tests (smoke tests over real systems)
- Decision tree: where should my test go?
- Test distribution examples

### 📖 `python-specific.md`

**Read when**:

- Working with pytest fixtures
- Need Python mocking patterns
- Testing Flask/FastAPI/Django applications
- Understanding Python testing tools
- Need Python-specific commands

**Contents**:

- pytest fixtures and parametrization
- Mocking with unittest.mock and pytest-mock
- Testing web frameworks (Flask, FastAPI, Django)
- Python testing commands
- Type hints in tests
- Python packaging for test utilities

### 📖 `workflows.md`

**Read when**:

- Adding a new feature (step-by-step)
- Fixing a bug (step-by-step)
- Adding a gateway method (complete checklist)
- Changing an interface (what to update)
- Managing dry-run features

**Contents**:

- Adding a new feature (TDD workflow)
- Fixing a bug (reproduce → fix → regression test)
- Adding a gateway method (8-step checklist with examples)
- Changing an interface (update all layers)
- Managing dry-run features (wrapping pattern)
- Testing with builder patterns

### 📖 `patterns.md`

**Read when**:

- Implementing constructor injection for fakes
- Adding mutation tracking to fakes
- Using CliRunner for CLI tests
- Building complex test scenarios with builders
- Testing dry-run behavior
- Need code examples of specific patterns

**Contents**:

- Constructor injection (how and why)
- Mutation tracking properties (read-only access)
- Using CliRunner (not subprocess)
- Builder patterns for complex scenarios
- Simulated environment pattern
- Error injection pattern
- Dry-run testing pattern

### 📖 `anti-patterns.md`

**Read when**:

- Unsure if your approach is correct
- Want to avoid common mistakes
- Reviewing code for bad patterns
- Debugging why tests are slow/brittle

**Contents**:

- ❌ Testing speculative features
- ❌ Hardcoded paths in tests (catastrophic)
- ❌ Not updating all layers
- ❌ Using subprocess in unit tests
- ❌ Complex logic in gateway classes
- ❌ Fakes with I/O operations
- ❌ Testing implementation details
- ❌ Incomplete test coverage for gateways

### 📖 `quick-reference.md`

**Read when**:

- Quick lookup for file locations
- Finding example tests to reference
- Looking up common fixtures
- Need command reference
- Want test distribution guidelines

**Contents**:

- Decision tree (where to add test)
- File location map (source + tests)
- Common fixtures (tmp_path, CliRunner, etc.)
- Common test patterns (code snippets)
- Example tests to reference
- Useful commands (pytest, ty, etc.)
- Quick checklist for adding gateway methods

## Quick Navigation by Task

### I'm adding a new feature

1. **Quick start**: `quick-reference.md` → Decision tree
2. **Step-by-step**: `workflows.md#adding-a-new-feature`
3. **Patterns**: `patterns.md` (CliRunner, builders)
4. **Avoid**: `anti-patterns.md` (speculative tests, hardcoded paths)

### I'm fixing a bug

1. **Step-by-step**: `workflows.md#fixing-a-bug`
2. **Patterns**: `patterns.md#constructor-injection-for-fakes`
3. **Examples**: `quick-reference.md#example-tests-to-reference`

### I'm adding/changing a gateway method

1. **Understanding**: `gateway-architecture.md`
2. **Step-by-step**: `workflows.md#adding-a-gateway-method`
3. **Checklist**: `quick-reference.md#quick-checklist-adding-a-new-gateway-method`
4. **Avoid**: `anti-patterns.md#not-updating-all-layers`

### I don't know where my test should go

1. **Decision tree**: `quick-reference.md#decision-tree`
2. **Detailed guide**: `testing-strategy.md`
3. **Examples**: `quick-reference.md#example-tests-to-reference`

### I need to implement a pattern

1. **All patterns**: `patterns.md`
2. **Examples**: `quick-reference.md#common-test-patterns`

### I think I'm doing something wrong

1. **Anti-patterns**: `anti-patterns.md`
2. **Correct approach**: `workflows.md`

## Visual Layer Guide

```
┌──────────────────────────────────────────────────────────────┐
│ Layer 5: Business Logic Integration Tests (5%)               │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Real database, filesystem, APIs, actual subprocess        │ │
│ │ Purpose: Smoke tests, catch integration issues           │ │
│ │ When: Sparingly, for critical workflows                  │ │
│ │ Speed: Seconds per test                                   │ │
│ │ Location: tests/e2e/ or tests/integration/               │ │
│ └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ Layer 4: Business Logic Tests (70%) ← MOST TESTS HERE       │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ FakeDatabase, FakeApiClient, FakeFileSystem              │ │
│ │ Purpose: Test features and business logic extensively    │ │
│ │ When: For EVERY feature and bug fix                      │ │
│ │ Speed: Milliseconds per test                              │ │
│ │ Location: tests/unit/, tests/services/, tests/commands/  │ │
│ └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ Layer 3: Pure Unit Tests (10%)                               │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Zero dependencies, no fakes, no mocks                    │ │
│ │ Purpose: Test isolated utilities and helpers             │ │
│ │ When: For pure functions, data structures, parsers       │ │
│ │ Speed: Milliseconds per test                              │ │
│ │ Location: tests/unit/                                     │ │
│ └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ Layer 2: Integration Sanity Tests (10%)                      │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ RealDatabase with mocked connections                     │ │
│ │ Purpose: Quick validation, catch syntax errors           │ │
│ │ When: When adding/changing real implementation           │ │
│ │ Speed: Fast (mocked)                                      │ │
│ │ Location: tests/integration/test_real_*.py               │ │
│ └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ Layer 1: Fake Infrastructure Tests (5%)                      │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ Test FakeDatabase itself                                 │ │
│ │ Purpose: Verify test infrastructure is reliable          │ │
│ │ When: When adding/changing fake implementation           │ │
│ │ Speed: Milliseconds per test                              │ │
│ │ Location: tests/unit/fakes/test_fake_*.py               │ │
│ └──────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

## Key Principles

1. **Thin gateway layer**: Wrap external state, push complexity to business logic
2. **Fast tests over fakes**: 70% of tests should use in-memory fakes
3. **Defense in depth**: Fakes → sanity tests → pure unit → business logic → integration
4. **Test what you're building**: No speculative tests, only active work
5. **Update all layers**: When changing interfaces, update ABC/real/fake/dry-run
6. **Gateways vs Backends**: Gateways have fakes; backends compose gateways and do NOT have fakes

## Layer Selection Guide

**Distinguishing Layer 3 (Pure Unit) from Layer 4 (Business Logic):**

- **Layer 3 (Pure Unit Tests)**: ZERO dependencies - no fakes, no mocks, no external state
  - Testing string utilities: `sanitize_branch_name("feat/FOO")` → `"feat-foo"`
  - Testing parsers: `parse_git_status("## main")` → `{"branch": "main"}`
  - Testing data structures: `LinkedList.append()` without any external dependencies

- **Layer 4 (Business Logic Tests)**: Uses fakes for external dependencies
  - Testing commands: `create_worktree(fake_git, name="feature")`
  - Testing workflows: `submit_pr(fake_gh, fake_git, ...)`
  - Testing business logic that coordinates multiple integrations

**If your test imports a Fake\*, it belongs in Layer 4, not Layer 3.**

## Default Testing Strategy

**When in doubt**:

- Write test over fakes (Layer 4) for business logic
- Write pure unit test (Layer 3) for utilities/helpers with no dependencies
- Use `pytest` with fixtures
- Use `tmp_path` fixture (not hardcoded paths)
- Follow examples in `quick-reference.md`

## Summary

**For quick tasks**: Start with `quick-reference.md`

**For understanding**: Start with `testing-strategy.md` or `gateway-architecture.md`

**For step-by-step guidance**: Use `workflows.md`

**For implementation details**: Use `patterns.md`

**For validation**: Check `anti-patterns.md`

**For Python specifics**: Check `python-specific.md`
