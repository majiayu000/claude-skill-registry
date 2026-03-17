---
name: tdd
description: Test-Driven Development (TDD) skill for Red-Green-Refactor cycle. Use when implementing features with tests first, minimal code to pass, then refactor. Teammates execute TDD autonomously within their own context in Agent Teams.
---

# SKILL: Test-Driven Development (TDD)

> **Purpose**: Execute TDD Red-Green-Refactor cycle for feature implementation
> **Target**: Coder teammates implementing features with test-first methodology in Agent Teams
> **⚠️ Teammates Only**: This skill is for coder teammates in Agent Teams. Team Lead delegates via teammate spawn.

---

## Quick Start

### When to Use This Skill
- Implement new feature with test coverage
- Fix bug with regression tests
- Refactor code with test safety net

### Quick Reference
```bash
# Red: pytest tests/test_feature.py -k "SC-1"  # FAIL
# Green: [Implement feature]
# Refactor: [Refactor code]
# Verify: pytest  # ALL PASS
```

## What This Skill Covers

### In Scope
- Red-Green-Refactor cycle execution
- Test-first development methodology
- Minimal implementation for Green phase

### Out of Scope
- Test framework selection → @.claude/skills/tdd/REFERENCE.md
- Coverage thresholds → @.claude/skills/ralph-loop/SKILL.md
- Code quality standards → @.claude/skills/vibe-coding/SKILL.md

## Core Concepts

### The TDD Cycle: Red-Green-Refactor

**Phase 1: Red** - Write Failing Test
```python
def test_add_two_numbers():
    result = calculator.add(2, 3)
    assert result == 5
```
Run test → Confirm it FAILS (❌)

**Phase 2: Green** - Minimal Implementation
```python
def add(a, b):
    return a + b  # Just enough to pass
```
Run test → Confirm it PASSES (✅)

**Phase 3: Refactor** - Improve Quality
```python
def add(a: int, b: int) -> int:
    """Add two integers with type safety."""
    return a + b
```
Run ALL tests → Confirm ALL PASS (✅)

### Why TDD Matters
- **Tests drive design**: API designed from usage perspective
- **Regression safety**: Refactor without fear
- **Living documentation**: Tests show intended behavior
- **Fast feedback**: Catch issues immediately

## Further Reading

**Internal**: @.claude/skills/tdd/REFERENCE.md - Advanced TDD concepts, patterns, and examples | @.claude/skills/ralph-loop/SKILL.md - Autonomous completion loop | @.claude/skills/vibe-coding/SKILL.md - Code quality standards | @.claude/skills/tdd/REFERENCE.md - Test framework detection

**External**: [Test-Driven Development by Kent Beck](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530) | [Growing Object-Oriented Software, Guided by Tests](https://www.amazon.com/Growing-Object-Oriented-Software-Guided-Tests/dp/0321503627)
