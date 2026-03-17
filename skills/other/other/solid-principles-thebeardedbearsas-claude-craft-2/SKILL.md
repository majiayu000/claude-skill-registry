---
name: solid-principles
description: SOLID principles for object-oriented design. Use when reviewing code quality, refactoring, designing classes or interfaces, or discussing architecture patterns.
triggers:
  files: ["*.cs", "*.java", "*.ts", "*.py", "*.php", "*.rb", "*.go", "*.kt", "*.dart", "*.swift"]
  keywords: ["SOLID", "SRP", "OCP", "LSP", "ISP", "DIP", "refactor", "interface", "abstraction", "single responsibility", "open closed", "liskov", "dependency inversion", "interface segregation", "clean architecture"]
auto_suggest: true
---

# SOLID Principles

This skill provides universal SOLID principles guidelines for object-oriented code quality.

See @REFERENCE.md for detailed documentation.

## Quick Reference

- **S**RP: One reason to change per class
- **O**CP: Extend via interfaces, don't modify existing
- **L**SP: Subtypes substitutable for base types
- **I**SP: Small interfaces (< 5 methods)
- **D**IP: Depend on abstractions, not implementations
