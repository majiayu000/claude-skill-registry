---
name: tdd
description: Use when writing production code that needs tests - new features, bug fixes, refactoring. Enforces RED-GREEN-REFACTOR cycle before any implementation.
argument-hint: "[feature-or-file]"
user-invocable: true
---

# TDD Skill

Write the test first. Watch it fail. Write minimal code to pass.

## The Iron Law

**No production code without a failing test first.**

Every line of production code must be justified by a test that failed without it.
No exceptions. No shortcuts. No "I'll test after."

---

## Agent Workflow

```
1. DETECT  -> Identify stack, test framework, existing test patterns
2. RED     -> Write ONE failing test for the next behavior
3. VERIFY  -> Run test, confirm it fails for the EXPECTED reason
4. GREEN   -> Write the SIMPLEST code that makes the test pass
5. VERIFY  -> Run tests, confirm ALL pass (new + existing)
6. REFACTOR -> Clean up while keeping all tests green
7. REPEAT  -> Next behavior = next failing test
```

**CRITICAL**: Never skip VERIFY steps. A test that passes on first run proves nothing.

---

## RED-GREEN-REFACTOR Cycle

See [references/red-green-refactor.md](references/red-green-refactor.md) for the detailed cycle with rules and verification steps.

---

## Reference Guide

| Topic | Reference |
|-------|-----------|
| Full RED-GREEN-REFACTOR cycle | [red-green-refactor.md](references/red-green-refactor.md) |
| Common mistakes and red flags | [anti-patterns.md](references/anti-patterns.md) |
| Per-stack test commands | [stack-commands.md](references/stack-commands.md) |

---

## Quick Reference: Test Commands

| Stack | Run Tests | Watch Mode |
|-------|-----------|------------|
| React/Next.js | `npx vitest run` | `npx vitest` |
| Laravel | `php artisan test` | `php artisan test --watch` |
| Swift | `swift test` | - |
| Generic TS | `bunx vitest run` | `bunx vitest` |
| Go | `go test ./...` | - |
| Rust | `cargo test` | `cargo watch -x test` |

---

## Forbidden Behaviors

- Never write production code before a failing test
- Never skip the VERIFY RED step
- Never accept a test that passes on first run without investigation
- Never mock what you can test directly
- Never write more than one test at a time in RED phase
- Never add features beyond what the current test requires
