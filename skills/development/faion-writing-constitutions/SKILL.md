---
name: faion-writing-constitutions
user-invocable: false
description: "SDD Framework: Creates constitution.md through codebase analysis OR Socratic dialogue for new projects. Triggers on \"constitution.md\", \"constitution\", \"project constitution\", \"project standards\"."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(ls:*), Bash(cat:*), Bash(git log:*), AskUserQuestion
---

# SDD: Writing Constitutions

**Communication: User's language. Docs: English.**

## Philosophy

**Constitution.md** — immutable project principles for ALL features.

**Two modes:**
1. Existing Project → codebase analysis
2. New Project → Socratic dialogue

## MODE 1: Existing Project

**Workflow:** Detect → Analyze Structure → Tech Stack → Patterns → Draft → Review

**Analyze:**
- Directory layout, CLAUDE.md, README.md
- Config files (pyproject.toml, package.json)
- Architecture patterns, naming, linters, testing

**Present findings:**
```markdown
**Analysis:**
1. Tech: Python 3.11, Django 4.2, PostgreSQL
2. Architecture: Layered (views → services → models)
3. Standards: black + isort + flake8
Does this match? What to change?
```

## MODE 2: New Project

**Workflow:** Vision → Tech Choices → Architecture → Standards → Draft → Review

### Vision (Socratic)
"Tell me about the project. What problem does it solve?"

Apply Five Whys to get to real need.

### Tech Choices (Alternatives)

For each decision — present A/B/C with pros/cons:
- Backend: Django vs FastAPI vs NestJS
- Database: PostgreSQL vs MongoDB vs SQLite

### Architecture (Trade-offs)
- Monolith vs Microservices
- REST vs GraphQL
- ORM vs Raw SQL

### Standards
- Linter, formatter, type hints
- Testing coverage, CI/CD
- Git conventions

## Draft (Both Modes)

Section by section with validation:
1. Overview → "Correct?"
2. Technology Stack → "Everything listed?"
3. Architecture Patterns → "Matches vision?"
4. Code Standards → "Agreed?"

## Save

```bash
mkdir -p aidocs/sdd/{project}
# Write constitution.md
```

Create CLAUDE.md navigation hub.

## Anti-patterns

- ❌ Copying without understanding
- ❌ Over-engineering at start
- ❌ Ignoring team expertise

## Output

`aidocs/sdd/{project}/constitution.md` → Next: `faion-writing-specifications`
