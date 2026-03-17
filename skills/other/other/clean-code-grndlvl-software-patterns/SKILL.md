---
name: clean-code
description: "Clean Code principles and practices reference based on Robert Martin's work. Use this skill when reviewing code quality, naming conventions, refactoring, or applying SOLID principles. Auto-activates for code smell detection, style improvements, and maintainability concerns."
---

# Clean Code Reference

A comprehensive reference for writing clean, maintainable code based on Robert Martin's "Clean Code" and related works. This skill provides language-agnostic principles with examples that apply to any programming language.

## When This Skill Activates

This skill automatically activates when you:
- Review code for quality or maintainability
- Need guidance on naming conventions
- Discuss refactoring or code smells
- Apply SOLID principles
- Improve code readability or structure
- Write or review unit tests

## Quick Reference

### SOLID Principles
| Principle | Summary | Violation Sign |
|-----------|---------|----------------|
| [Single Responsibility (SRP)](solid/single-responsibility.md) | One reason to change | Class does too many things |
| [Open/Closed (OCP)](solid/open-closed.md) | Open for extension, closed for modification | Modifying existing code for new features |
| [Liskov Substitution (LSP)](solid/liskov-substitution.md) | Subtypes must be substitutable | Subclass breaks parent behavior |
| [Interface Segregation (ISP)](solid/interface-segregation.md) | No forced dependencies on unused methods | Fat interfaces |
| [Dependency Inversion (DIP)](solid/dependency-inversion.md) | Depend on abstractions, not concretions | High-level modules import low-level |

### Clean Code Practices
| Practice | Key Points |
|----------|------------|
| [Meaningful Names](practices/meaningful-names.md) | Intention-revealing, pronounceable, searchable |
| [Functions](practices/functions.md) | Small, do one thing, one level of abstraction |
| [Comments](practices/comments.md) | Code should be self-documenting; comments explain why, not what |
| [Formatting](practices/formatting.md) | Consistent style, vertical density, horizontal alignment |
| [Error Handling](practices/error-handling.md) | Exceptions over error codes, fail fast, don't return null |
| [Unit Testing](practices/unit-testing.md) | F.I.R.S.T. principles, one assert per test, test behavior |
| [Code Smells](practices/code-smells.md) | Recognition and refactoring of common problems |
| [Boy Scout Rule](practices/boy-scout-rule.md) | Leave code cleaner than you found it |

## The Boy Scout Rule

> "Leave the campground cleaner than you found it."

Every time you touch code, make it a little better. Small, incremental improvements compound over time.

## Code Quality Checklist

Before committing code, verify:

- [ ] **Names** - Are all names intention-revealing?
- [ ] **Functions** - Is each function doing exactly one thing?
- [ ] **Comments** - Are comments explaining why, not what?
- [ ] **DRY** - Is there any duplicated logic?
- [ ] **SOLID** - Are principles being followed?
- [ ] **Tests** - Is the code tested and testable?
- [ ] **Error Handling** - Are errors handled gracefully?

## Language Translation Notes

Examples use generic pseudocode. Adapt to your language:
- **PHP**: `class`, `function`, `->`, type hints
- **JavaScript/TypeScript**: `class`, arrow functions, `.`
- **Python**: `class`, `def`, `.`, type hints
- **Java/C#**: Direct mapping with access modifiers

---

*Based on concepts from "Clean Code: A Handbook of Agile Software Craftsmanship" by Robert C. Martin, 2008.*
