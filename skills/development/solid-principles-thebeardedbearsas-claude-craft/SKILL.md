---
name: solid-principles
description: Principes SOLID. Use when reviewing code quality or refactoring.
triggers:
  files: ["*.cs"]
  keywords: ["SOLID", "SRP", "OCP", "LSP", "ISP", "DIP", "refactor", "interface", "abstraction"]
auto_suggest: true
---

# Principes SOLID

This skill provides SOLID principles guidelines for code quality.

See @REFERENCE.md for detailed documentation.

## Quick Reference

- **S**RP: One reason to change per class
- **O**CP: Extend via interfaces, don't modify existing
- **L**SP: Subtypes substitutable for base types
- **I**SP: Small interfaces (< 5 methods)
- **D**IP: Depend on abstractions, not implementations
