---
name: faion-code-quality
description: "Code quality specialist: architecture patterns, refactoring, code review, development practices. 23 methodologies."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite, Skill
---

# Code Quality & Architecture Sub-Skill

Architecture patterns, code quality, refactoring, and development practices.

## Purpose

Handles architecture patterns, code decomposition, refactoring, code review, development practices, and tech debt management.

---

## Context Discovery

### Auto-Investigation

| Signal | Check For | Why |
|--------|-----------|-----|
| Architecture docs | ADRs, C4 diagrams, domain models | Architecture patterns in use |
| Code review comments | Review patterns, quality standards | Review culture |
| Linting config | ESLint, Prettier, ruff rules | Code quality standards |
| Tech debt tracking | Issue labels, debt backlog | Tech debt awareness |
| Documentation quality | CLAUDE.md, README patterns | Documentation standards |

### Discovery Questions

```yaml
questions:
  - question: "What's your code quality need?"
    options:
      - label: "Architecture design"
        description: "Use clean-architecture, domain-driven-design, cqrs-pattern"
      - label: "Code review"
        description: "Use code-review, code-review-process"
      - label: "Refactoring"
        description: "Use refactoring-patterns, code-decomposition-patterns"
      - label: "Tech debt management"
        description: "Use tech-debt-basics, tech-debt-management"

  - question: "What's your architecture approach?"
    options:
      - label: "Domain-driven"
        description: "Apply domain-driven-design"
      - label: "Microservices"
        description: "Apply microservices-design"
      - label: "Event-driven"
        description: "Apply event-sourcing-basics"
      - label: "Clean/layered"
        description: "Apply clean-architecture"

  - question: "Are you working with LLMs for code generation?"
    options:
      - label: "Yes, AI-assisted development"
        description: "Apply llm-friendly-architecture"
      - label: "No, traditional development"
        description: "Standard architecture patterns"
```

---

## When to Use

- Architecture patterns (DDD, CQRS, Clean Architecture, Event Sourcing)
- Code review and quality standards
- Refactoring patterns
- Code decomposition strategies
- Development practices (XP, pair/mob programming)
- Tech debt management
- Documentation standards
- LLM-friendly architecture

## Methodologies (23 files)

**Architecture (7):** clean-architecture, domain-driven-design, cqrs-pattern, microservices-design, llm-friendly-architecture, event-sourcing-basics, event-sourcing-implementation

**Code Quality (10):** code-review, code-review-basics, code-review-process, code-coverage, refactoring-patterns, code-quality-trends, documentation, claude-md-creation, tech-debt-basics, tech-debt-management

**Code Decomposition (3):** code-decomposition-patterns, code-decomposition-principles, framework-decomposition-patterns

**Dev Practices (3):** xp-extreme-programming, pair-programming, mob-programming

## Tools

**Code quality:** ESLint, Prettier, ruff, SonarQube
**Architecture:** C4 model, ADRs, UML

## Related Sub-Skills

| Sub-skill | Relationship |
|-----------|--------------|
| faion-automation-tooling | Tooling and automation |
| faion-software-architect | High-level architecture decisions |
| faion-testing-developer | Testing strategies |

## Integration

Invoked by parent skill `faion-devtools-developer` for code quality and architecture work.

---

*faion-code-quality v1.0 | 23 methodologies*
