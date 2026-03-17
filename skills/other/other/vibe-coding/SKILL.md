---
name: vibe-coding
description: LLM-readable code standards. Functions ≤50 lines, files ≤200 lines, nesting ≤3 levels. SRP, DRY, KISS, Early Return.
---

# SKILL: Vibe Coding (Code Quality Standards)

> **Purpose**: Enforce LLM-readable code standards for maintainable code
> **Target**: Coder Agent during Green/Refactor phases

## Quick Reference

| Target | Limit | Action |
|--------|-------|--------|
| **Function** | ≤50 lines | Split functions |
| **File** | ≤200 lines | Extract modules |
| **Nesting** | ≤3 levels | Early return |

## Principles

- **SRP**: One function = one responsibility
- **DRY**: No duplicate code blocks, extract common logic
- **KISS**: Simplest solution that works, avoid over-engineering
- **Early Return**: Return early to reduce nesting, keep happy path at top
- **Self-Documenting Code**: Names reveal intent, no unnecessary comments (see REFERENCE.md)
- **Single Abstraction Level**: Functions operate at one conceptual level (see REFERENCE.md)
- **Principle of Least Surprise**: Predictable behavior, no hidden side effects (see REFERENCE.md)

## AI Rules

**Enforce during ALL code generation**:
- Functions ≤50 lines, Files ≤200 lines, Nesting ≤3 levels
- SRP, DRY, KISS, Early Return pattern

## Further Reading

**Internal**: @.claude/skills/vibe-coding/REFERENCE.md - SOLID principles, refactoring patterns | @.claude/skills/tdd/SKILL.md - Red-Green-Refactor

**External**: [Clean Code](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882) | [Refactoring](https://www.amazon.com/Refactoring-Improving-Existing-Addison-Wesney-Signature/dp/0201485672)
