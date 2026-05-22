---
name: faion-software-developer
description: "Developer role: Python, JavaScript/TypeScript, backend, APIs, testing, automation, UI design. Full-stack development with 68 methodologies."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite, Skill
---

# Developer Domain Skill

**Communication: User's language. Code: English.**

## Purpose

Orchestrates all software development activities. Covers programming languages, frameworks, testing, API design, and automation.

---

## Agents

| Agent | Purpose |
|-------|---------|
| faion-code-agent | Code generation and review |
| faion-test-agent | Test generation and execution |
| faion-frontend-brainstormer-agent | Generate 3-5 design variants |
| faion-storybook-agent | Setup/maintain Storybook |
| faion-frontend-component-agent | Develop components with stories |

---

## References

Detailed technical context for each area:

| Reference | Content | Lines |
|-----------|---------|-------|
| [python.md](references/python.md) | Python, Django, FastAPI, pytest, typing | ~1760 |
| [javascript.md](references/javascript.md) | TypeScript, React, Node.js, Bun, testing | ~1350 |
| [backend.md](references/backend.md) | Backend architecture, databases, caching | ~3180 |
| [api-design.md](references/api-design.md) | REST, GraphQL, OpenAPI, versioning | ~2250 |
| [testing.md](references/testing.md) | Unit, integration, E2E, TDD, coverage | ~1810 |
| [browser-automation.md](references/browser-automation.md) | Puppeteer, Playwright, scraping | ~1490 |
| [methodologies.md](references/methodologies.md) | 68 development methodologies (M-DEV-*) | ~1573 |
| [documentation.md](references/documentation.md) | CLAUDE.md creation templates | ~180 |
| [frontend-design.md](references/frontend-design.md) | UI brainstorming, Storybook workflow | ~90 |
| [django/](references/django/) | Django-specific patterns (7 files) | ~600 |

**Total:** ~14,280 lines of technical reference

---

## Quick Reference

### Language Selection

| Language | When to Use |
|----------|-------------|
| **Python** | Backend APIs, data processing, ML, scripting |
| **TypeScript** | Frontend, Node.js backend, full-stack |
| **Go** | High-performance services, CLI tools |
| **Rust** | Systems programming, WASM |

### Framework Selection

| Framework | Use Case |
|-----------|----------|
| **Django** | Full-featured web apps, admin panels |
| **FastAPI** | Modern async APIs, microservices |
| **React** | Complex UIs, SPAs |
| **Next.js** | Full-stack React, SSR/SSG |
| **Express** | Simple Node.js APIs |
| **Bun** | Fast TypeScript runtime |

### Testing Strategy

| Level | Coverage | Tools |
|-------|----------|-------|
| Unit | 70% | pytest, Vitest, Jest |
| Integration | 20% | pytest-django, Supertest |
| E2E | 10% | Playwright, Cypress |

---

## Methodologies (32)

### Python (M-PY-*)

| ID | Name | Purpose |
|----|------|---------|
| M-PY-001 | Project Setup Poetry | Dependency management |
| M-PY-002 | Django Patterns | Models, views, services |
| M-PY-003 | FastAPI Patterns | Routes, dependencies, Pydantic |
| M-PY-004 | pytest Patterns | Fixtures, mocking, parametrize |
| M-PY-005 | Type Hints | Type safety, mypy |
| M-PY-006 | Code Formatting | Black, isort, flake8 |
| M-PY-007 | Virtual Environments | venv, Poetry, pyenv |
| M-PY-008 | Async Python | asyncio, concurrent execution |

### JavaScript/TypeScript (M-JS-*)

| ID | Name | Purpose |
|----|------|---------|
| M-JS-001 | Component Architecture | React feature-based structure |
| M-JS-002 | TypeScript Strict Mode | Type safety patterns |
| M-JS-003 | React Hooks | Custom hooks best practices |
| M-JS-004 | Node.js Service Layer | Controller-Service-Repository |
| M-JS-005 | Error Handling | Custom errors, middleware |
| M-JS-006 | Testing Pyramid | Unit, integration, E2E balance |
| M-JS-007 | Package Management | pnpm, lockfiles, security |
| M-JS-008 | Performance | Memoization, virtualization |

### Backend (M-BE-*)

| ID | Name | Purpose |
|----|------|---------|
| M-BE-001 | Clean Architecture | Layers, dependencies |
| M-BE-002 | Database Design | Normalization, indexes |
| M-BE-003 | Caching Strategy | Redis, in-memory, CDN |
| M-BE-004 | Authentication | JWT, sessions, OAuth |
| M-BE-005 | Rate Limiting | Token bucket, sliding window |
| M-BE-006 | Background Jobs | Celery, BullMQ, cron |
| M-BE-007 | Logging & Monitoring | Structured logs, metrics |
| M-BE-008 | Error Recovery | Retry, circuit breaker |

### API Design (M-API-*)

| ID | Name | Purpose |
|----|------|---------|
| M-API-001 | REST Conventions | Resources, verbs, status codes |
| M-API-002 | OpenAPI/Swagger | Documentation, code generation |
| M-API-003 | Versioning | URL, header, query strategies |
| M-API-004 | Pagination | Cursor, offset, keyset |
| M-API-005 | Error Responses | Consistent error format |
| M-API-006 | GraphQL Patterns | Schema, resolvers, N+1 |
| M-API-007 | WebSocket Design | Real-time communication |
| M-API-008 | API Security | CORS, rate limits, validation |

---

## Workflows

### New Feature Development

```
1. Understand requirements
2. Design API/data model
3. Write failing tests (TDD)
4. Implement code
5. Pass tests
6. Code review
7. Deploy
```

### Code Review Checklist

- [ ] Follows project conventions
- [ ] Has appropriate tests
- [ ] No security vulnerabilities
- [ ] Error handling complete
- [ ] Performance considered
- [ ] Documentation updated

### Debugging Process

```
1. Reproduce the issue
2. Check logs and stack trace
3. Isolate the problem
4. Write failing test
5. Fix the issue
6. Verify fix
7. Add regression test
```

---

## Code Quality Tools

### Python

```bash
# Format
black src/ && isort src/

# Lint
flake8 src/ && mypy src/

# Test
pytest --cov=src
```

### JavaScript/TypeScript

```bash
# Format
prettier --write .

# Lint
eslint . --fix

# Test
vitest run --coverage
```

### Pre-commit

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks: [{ id: black }]
  - repo: https://github.com/pycqa/isort
    rev: 5.13.0
    hooks: [{ id: isort }]
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks: [{ id: mypy }]
```

---

## Project Templates

### Python Backend

```
project/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models/
│   ├── services/
│   ├── api/
│   └── utils/
├── tests/
├── pyproject.toml
└── Dockerfile
```

### TypeScript Full-Stack

```
project/
├── apps/
│   ├── web/          # Next.js frontend
│   └── api/          # Express/Fastify backend
├── packages/
│   ├── ui/           # Shared components
│   ├── config/       # Shared configs
│   └── types/        # Shared types
├── pnpm-workspace.yaml
└── turbo.json
```

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| faion-devops | Deployment, CI/CD |
| faion-ml | AI/ML integrations |
| faion-sdd | Specification-driven development |

---

## Error Handling

| Issue | Action |
|-------|--------|
| Unknown language | Ask user or infer from files |
| Missing context | Read references/ for patterns |
| Complex architecture | Use Task tool with Explore agent |

---

*Developer Domain Skill v3.0*
*10 Reference Areas | 68 Methodologies | 5 Agents*
*Consolidated from: faion-development, faion-dev-django, faion-dev-docs, faion-dev-frontend*
