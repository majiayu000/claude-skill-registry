---
title: "Mutation Testing Skill"
type: github
url: "https://github.com/citypaul/.dotfiles/blob/main/claude/.claude/skills/mutation-testing/SKILL.md"
stars: 0
language: "Markdown"
tags:
  - testing
  - tdd
  - claude-code
  - code-quality
authors:
  - paul-hammond
summary: "Code coverage lies about test quality—mutation testing exposes weak tests by asking 'if I introduced a bug here, would my tests catch it?'"
date: 2026-01-06
---

## Overview

Mutation testing evaluates test effectiveness by introducing small intentional bugs (mutations) into code and checking whether tests fail. Tests that pass despite mutations are weak and need strengthening. This Claude Code skill provides a systematic approach to performing mutation testing during code review.

## Core Question

> "Are my tests actually catching bugs?"

Code coverage tells you what code your tests execute. Mutation testing tells you if your tests would detect changes to that code.

## Mutation Operators

The skill catalogs operators across multiple categories:

| Category | Examples |
|----------|----------|
| Arithmetic | `+` to `-`, `*` to `/` |
| Conditionals | `>=` to `>`, boundary value shifts |
| Logical | `&&` to `||`, `??` changes |
| Boolean literals | `true` to `false` |
| Block statements | Removing entire function bodies |
| String/Array | Empty vs. populated values |
| Methods | `startsWith()` to `endsWith()`, `some()` to `every()` |

## Systematic Analysis Process

1. Identify changed code files
2. Generate mental mutants (apply mutation operators to code)
3. Verify test coverage for each potential mutant
4. Document findings (killed, survived, no coverage, equivalent)

## Critical Patterns

**Surviving mutants often occur with:**
- Tests using identity values (0, 1, empty strings)
- Assertions that only verify "no error thrown"
- Testing only one side of conditional branches
- Missing boundary value tests
- Tests not verifying side effects

**Strengthening weak tests:**
- Add boundary value cases (exactly at threshold)
- Test all meaningful branch combinations
- Use non-identity values that reveal operator differences
- Verify observable outcomes and method calls

## Metrics

- **Mutation Score**: `killed / valid × 100`
- Target: >90% indicates strong tests
- 60-80% shows moderate effectiveness with room for improvement

## When to Use

- Reviewing branch code changes
- Verifying test effectiveness after TDD
- Finding missing edge case tests
- Validating that refactoring didn't weaken tests

## Connections

- [[claude-code-skills]] - This mutation testing guide is itself a Claude Code skill, demonstrating how specialized testing knowledge can be packaged for automatic activation during code review
