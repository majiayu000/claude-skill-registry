---
name: analyzing-projects
description: Guides systematic project analysis, codebase exploration, and architecture pattern recognition. Use when understanding new codebases, onboarding to projects, or investigating system structure.
license: MIT
compatibility: opencode
metadata:
  category: exploration
  audience: developers
---

# Analyzing Projects

Systematic approaches to understanding codebases, identifying patterns, and mapping system architecture.

## When to Use This Skill

- Onboarding to a new codebase
- Understanding unfamiliar code before making changes
- Investigating how features are implemented
- Mapping dependencies between modules
- Identifying architectural patterns in use

---

## Core Analysis Framework

### The 5-Layer Discovery Process

```
Layer 1: Surface Scan
  └─ Entry points, config files, directory structure

Layer 2: Dependency Mapping
  └─ Package managers, imports, module relationships

Layer 3: Architecture Recognition
  └─ Patterns (MVC, hexagonal, microservices)

Layer 4: Flow Tracing
  └─ Request paths, data flow, state management

Layer 5: Quality Assessment
  └─ Test coverage, code health, technical debt
```

---

## Phase 1: Surface Scan

### Entry Point Discovery

Start by identifying how the application launches:

1. **Look for standard entry files**:
   - `main.*`, `index.*`, `app.*`, `server.*`
   - `cmd/` directory (Go)
   - `src/main/` (Java)
   - `bin/` scripts

2. **Check configuration files**:
   - `package.json` (scripts.start, main)
   - `Makefile`, `Taskfile`
   - Docker/Compose files
   - CI/CD configs (`.github/workflows/`)

3. **Map directory structure**:
   ```
   Quick heuristics:
   ├── src/           → Source code
   ├── lib/           → Internal libraries
   ├── pkg/           → Public packages (Go)
   ├── internal/      → Private packages (Go)
   ├── tests/         → Test files
   ├── docs/          → Documentation
   ├── scripts/       → Build/deploy scripts
   └── config/        → Configuration
   ```

### Initial Questions to Answer

- What language(s) and framework(s)?
- What's the build system?
- How is the app deployed?
- Where are the main entry points?

---

## Phase 2: Dependency Mapping

### Package Manager Analysis

| File | Ecosystem | Key Sections |
|------|-----------|--------------|
| `package.json` | Node.js | dependencies, devDependencies |
| `requirements.txt` / `pyproject.toml` | Python | direct dependencies |
| `go.mod` | Go | require blocks |
| `Cargo.toml` | Rust | dependencies |
| `pom.xml` / `build.gradle` | Java | dependencies |

### Internal Module Relationships

1. **Trace imports** from entry points
2. **Build a mental model** of layers:
   ```
   Presentation Layer (routes, controllers, views)
         ↓
   Application Layer (services, use cases)
         ↓
   Domain Layer (entities, business logic)
         ↓
   Infrastructure Layer (database, external APIs)
   ```

3. **Identify shared utilities** imported across modules

---

## Phase 3: Architecture Recognition

### Common Patterns to Identify

| Pattern | Indicators | Typical Structure |
|---------|------------|-------------------|
| **MVC** | controllers/, models/, views/ | Clear separation of concerns |
| **Hexagonal** | ports/, adapters/, domain/ | Dependency inversion |
| **Microservices** | services/, docker-compose | Independent deployable units |
| **Monolith** | Single large app, shared DB | Everything in one deployment |
| **Serverless** | functions/, handlers/ | Event-driven, stateless |

### Architecture Questions

- How are concerns separated?
- Where does business logic live?
- How are external dependencies abstracted?
- What's the data access pattern?

---

## Phase 4: Flow Tracing

### Request Path Analysis

For web applications, trace a request end-to-end:

```
HTTP Request
    ↓
Router/Routes (maps URL → handler)
    ↓
Middleware (auth, logging, validation)
    ↓
Controller/Handler (orchestrates)
    ↓
Service/Use Case (business logic)
    ↓
Repository/DAO (data access)
    ↓
Database/External API
```

### State Management Analysis

For frontend applications:
- Where is state stored? (Redux, Zustand, Context)
- How does data flow? (unidirectional, bidirectional)
- What triggers re-renders?

---

## Phase 5: Quality Assessment

### Code Health Indicators

| Indicator | Good Sign | Warning Sign |
|-----------|-----------|--------------|
| Test coverage | >70% coverage | No tests, or tests ignored |
| Dependencies | Recent versions | Major versions behind |
| Documentation | README updated | Stale or missing docs |
| Build time | Under 2 minutes | Over 10 minutes |
| Error handling | Consistent patterns | Swallowed exceptions |

### Technical Debt Markers

- TODO/FIXME comments
- Disabled tests
- Large functions (>50 lines)
- Deep nesting (>4 levels)
- Duplicated code blocks
- Hardcoded values

---

## Analysis Strategies by Goal

### Goal: Make a Bug Fix

1. Find where the bug manifests
2. Trace back to the root cause
3. Understand the affected area only
4. Check for related tests

### Goal: Add a New Feature

1. Find similar existing features
2. Understand the patterns they use
3. Map the modules that need changes
4. Identify integration points

### Goal: Full Codebase Understanding

1. Complete all 5 phases
2. Document architecture decisions
3. Create a mental map of key flows
4. Identify ownership areas

---

## Parallel Analysis Pattern

When exploring a large codebase, parallelize by module:

```
Spawn subagents for each major area:
├─ Subagent 1: Analyze src/auth (authentication module)
├─ Subagent 2: Analyze src/api (API layer)
├─ Subagent 3: Analyze src/db (data layer)
├─ Subagent 4: Analyze src/ui (frontend)
└─ Subagent 5: Analyze tests/ (test patterns)

Synthesize findings into unified architecture view.
```

---

## Output Templates

### Quick Architecture Summary

```markdown
## Project Overview
- **Language**: [Primary language]
- **Framework**: [Main framework]
- **Architecture**: [Pattern identified]
- **Entry Point**: [Main file]

## Key Modules
| Module | Responsibility | Key Files |
|--------|----------------|-----------|
| [Name] | [What it does] | [Files]   |

## Data Flow
[Request lifecycle diagram]

## Notable Patterns
- [Pattern 1]: [Where/how used]
- [Pattern 2]: [Where/how used]
```

### Onboarding Checklist

```markdown
## Getting Started
- [ ] Clone and install dependencies
- [ ] Run the app locally
- [ ] Run the test suite
- [ ] Trace one request end-to-end
- [ ] Find where [core feature] is implemented
```

---

## Anti-Patterns to Avoid

1. **Analysis Paralysis** - Don't try to understand everything before starting
2. **Ignoring Tests** - Tests often document expected behavior
3. **Skipping Config** - Configuration reveals deployment context
4. **Surface-Only** - Don't stop at directory structure
5. **Assuming Patterns** - Verify patterns, don't assume from naming

---

## Quick Reference

```
SURFACE SCAN:
  entry points → config files → directory structure

DEPENDENCY MAP:
  package manager → import tracing → layer identification

ARCHITECTURE:
  pattern recognition → separation of concerns → abstractions

FLOW TRACING:
  request path → data flow → state management

QUALITY CHECK:
  test coverage → code health → technical debt
```
