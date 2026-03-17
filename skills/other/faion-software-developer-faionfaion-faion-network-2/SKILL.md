---
name: faion-software-developer
description: "Full-stack development: Python, JavaScript, Go, APIs, testing, frontend."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite, Skill
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Software Developer Orchestrator

Coordinates 7 specialized sub-skills for comprehensive software development.

## Purpose

Routes development tasks to appropriate specialized sub-skills based on technology, domain, and task type.

---

## Context Discovery

### Auto-Investigation

Detect tech stack from project files BEFORE asking questions:

| Signal | How to Check | Detected Stack |
|--------|--------------|----------------|
| `manage.py` | `Glob("**/manage.py")` | Django → faion-python-developer |
| `pyproject.toml` with fastapi | `Grep("fastapi", "**/pyproject.toml")` | FastAPI → faion-python-developer |
| `pyproject.toml` with django | `Grep("django", "**/pyproject.toml")` | Django → faion-python-developer |
| `package.json` with react | `Grep("react", "**/package.json")` | React → faion-javascript-developer |
| `package.json` with next | `Grep("next", "**/package.json")` | Next.js → faion-javascript-developer |
| `package.json` with express | `Grep("express", "**/package.json")` | Node.js → faion-javascript-developer |
| `go.mod` | `Glob("**/go.mod")` | Go → faion-backend-systems |
| `Cargo.toml` | `Glob("**/Cargo.toml")` | Rust → faion-backend-systems |
| `pom.xml` or `build.gradle` | `Glob("**/pom.xml")` | Java → faion-backend-enterprise |
| `*.csproj` | `Glob("**/*.csproj")` | C# → faion-backend-enterprise |
| `composer.json` | `Glob("**/composer.json")` | PHP → faion-backend-enterprise |
| `Gemfile` | `Glob("**/Gemfile")` | Ruby → faion-backend-enterprise |
| `tailwind.config.*` | `Glob("**/tailwind.config.*")` | Tailwind → faion-frontend-developer |

**Also check for patterns:**
- `Glob("**/services/*.py")` → Service layer exists, follow pattern
- `Glob("**/tests/**")` → Tests exist, check style
- `Grep("class.*ViewSet", "**/*.py")` → DRF ViewSets used

### Discovery Questions

Use `AskUserQuestion` if stack not detected or task type unclear.

#### Q1: Task Type (if unclear from request)

```yaml
question: "What type of development task is this?"
header: "Task"
multiSelect: false
options:
  - label: "Build new feature"
    description: "Create new functionality from scratch"
  - label: "Fix a bug"
    description: "Something isn't working correctly"
  - label: "Refactor / improve"
    description: "Restructure without changing behavior"
  - label: "Add tests"
    description: "Improve test coverage"
  - label: "Review / audit code"
    description: "Check quality, find issues"
```

**Routing:**
- "Build new feature" → Full workflow, may need architecture
- "Fix a bug" → Investigate first, minimal targeted changes
- "Refactor / improve" → `Skill(faion-code-quality)`
- "Add tests" → `Skill(faion-testing-developer)`
- "Review / audit code" → `Skill(faion-code-quality)`

#### Q2: Tech Stack (only if not auto-detected)

```yaml
question: "What's the primary technology?"
header: "Stack"
multiSelect: false
options:
  - label: "Python (Django/FastAPI)"
    description: "Python backend development"
  - label: "JavaScript/TypeScript"
    description: "React, Node.js, Next.js"
  - label: "Go"
    description: "Go backend services"
  - label: "Other (Rust/Java/C#/PHP/Ruby)"
    description: "Enterprise or systems languages"
```

**Routing:**
- "Python" → `Skill(faion-python-developer)`
- "JavaScript/TypeScript" → `Skill(faion-javascript-developer)`
- "Go" → `Skill(faion-backend-systems)`
- "Other" → `Skill(faion-backend-enterprise)`

#### Q3: Code Area (for large codebases)

```yaml
question: "Which area of the codebase?"
header: "Area"
multiSelect: false
options:
  - label: "Backend / API"
    description: "Server-side logic, database"
  - label: "Frontend / UI"
    description: "User interface, components"
  - label: "Both (full-stack)"
    description: "Changes span frontend and backend"
  - label: "Infrastructure"
    description: "Build, deploy, CI/CD"
```

#### Q4: Existing Patterns (for existing codebases)

```yaml
question: "Should I follow existing patterns in the codebase?"
header: "Patterns"
multiSelect: false
options:
  - label: "Yes, match existing style"
    description: "I'll investigate and follow conventions"
  - label: "No, use best practices"
    description: "Apply modern patterns regardless"
  - label: "Improve while matching"
    description: "Follow style but suggest improvements"
```

**Action:**
- "Yes, match existing" → Read existing code first, extract patterns
- "No, use best practices" → Apply methodology defaults
- "Improve while matching" → Note improvements in comments/TODOs

---

## Sub-Skills

| Sub-skill | Methodologies | Focus |
|-----------|---------------|-------|
| faion-python-developer | 24 | Django, FastAPI, async, pytest, type hints |
| faion-javascript-developer | 18 | React, Node.js, Next.js, TypeScript, Bun |
| faion-backend-developer | 47 | Go, Rust, Java, C#, PHP, Ruby, databases |
| faion-frontend-developer | 18 | Tailwind, CSS-in-JS, design tokens, PWA, a11y |
| faion-api-developer | 19 | REST, GraphQL, OpenAPI, auth, versioning |
| faion-testing-developer | 12 | Unit, integration, E2E, TDD, mocking |
| faion-devtools-developer | 46 | Automation, architecture, code quality, CI/CD |

**Total:** 184 methodologies across 7 sub-skills

## Routing Logic

| Task Type | Route To |
|-----------|----------|
| Python/Django/FastAPI code | faion-python-developer |
| JavaScript/TypeScript/React/Node.js code | faion-javascript-developer |
| Go/Rust/Java/C#/PHP/Ruby code | faion-backend-developer |
| Database design, caching | faion-backend-developer |
| Tailwind/CSS/UI libraries | faion-frontend-developer |
| Design tokens, PWA, accessibility | faion-frontend-developer |
| REST/GraphQL API design | faion-api-developer |
| API auth, versioning, rate limiting | faion-api-developer |
| Testing (any type) | faion-testing-developer |
| Browser automation, web scraping | faion-devtools-developer |
| Code review, refactoring | faion-devtools-developer |
| Architecture patterns (DDD, CQRS) | faion-devtools-developer |
| CI/CD, monorepo, tooling | faion-devtools-developer |

## Multi-Skill Tasks

For tasks spanning multiple domains, coordinate relevant sub-skills:

**Full-stack Python app:**
1. faion-python-developer (backend)
2. faion-api-developer (API design)
3. faion-frontend-developer (UI)
4. faion-testing-developer (tests)

**React + Node.js app:**
1. faion-javascript-developer (React + Node.js)
2. faion-frontend-developer (styling)
3. faion-api-developer (API)
4. faion-testing-developer (tests)

**Microservices architecture:**
1. faion-backend-developer (services in Go/Rust/Java)
2. faion-api-developer (API gateway)
3. faion-devtools-developer (architecture patterns)
4. faion-testing-developer (integration tests)

## Agents

| Agent | Purpose |
|-------|---------|
| faion-code-agent | Code generation and review |
| faion-test-agent | Test generation and execution |
| faion-frontend-brainstormer-agent | Generate 3-5 design variants |
| faion-storybook-agent | Setup/maintain Storybook |
| faion-frontend-component-agent | Develop components with stories |

## Related Skills

| Skill | Relationship |
|-------|--------------|
| faion-net | Parent orchestrator for all projects |
| faion-software-architect | Architecture design decisions |
| faion-devops-engineer | Deployment, infrastructure |
| faion-ml-engineer | AI/ML integrations |
| faion-sdd | Specification-driven development |

## Usage

Invoked via `/faion-net` or directly as `/faion-software-developer`. Automatically routes to appropriate sub-skill.

---

*faion-software-developer v2.0 | Orchestrator | 7 sub-skills | 184 methodologies*
