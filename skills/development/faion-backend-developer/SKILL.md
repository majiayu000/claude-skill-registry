---
name: faion-backend-developer
description: "Backend orchestrator: coordinates systems (Go, Rust, DB) and enterprise (Java, C#, PHP, Ruby)."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite, Skill
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Backend Developer Orchestrator

Coordinates two specialized backend sub-skills for systems-level and enterprise web development.

## Purpose

Routes backend tasks to appropriate sub-skill based on language and context.

---

## Context Discovery

### Auto-Investigation

Detect backend stack from project:

| Signal | How to Check | What It Tells Us |
|--------|--------------|------------------|
| `go.mod` | `Glob("**/go.mod")` | Go project → :systems |
| `Cargo.toml` | `Glob("**/Cargo.toml")` | Rust project → :systems |
| `pom.xml` | `Glob("**/pom.xml")` | Java Maven → :enterprise |
| `build.gradle` | `Glob("**/build.gradle*")` | Java Gradle → :enterprise |
| `*.csproj` | `Glob("**/*.csproj")` | C# .NET → :enterprise |
| `composer.json` | `Glob("**/composer.json")` | PHP → :enterprise |
| `Gemfile` | `Glob("**/Gemfile")` | Ruby → :enterprise |
| DB config | `Grep("postgres\|mysql\|mongodb", "**/*")` | Database type |

### Discovery Questions

#### Q1: Backend Language (if not detected)

```yaml
question: "What backend language are you using?"
header: "Language"
multiSelect: false
options:
  - label: "Go"
    description: "High-performance, concurrent services"
  - label: "Rust"
    description: "Memory-safe, systems programming"
  - label: "Java (Spring)"
    description: "Enterprise, Spring Boot"
  - label: "C# (.NET)"
    description: "Microsoft ecosystem"
  - label: "PHP (Laravel)"
    description: "Web applications"
  - label: "Ruby (Rails)"
    description: "Rapid development"
```

**Routing:**
- "Go" or "Rust" → `Skill(faion-backend-systems)`
- "Java", "C#", "PHP", "Ruby" → `Skill(faion-backend-enterprise)`

#### Q2: Backend Task Type

```yaml
question: "What type of backend work?"
header: "Task"
multiSelect: false
options:
  - label: "Build new service/API"
    description: "Create from scratch"
  - label: "Database design/optimization"
    description: "Schema, queries, performance"
  - label: "Add caching/queues"
    description: "Infrastructure patterns"
  - label: "Fix bugs/refactor"
    description: "Improve existing code"
```

**Routing:**
- "Database" → database-design, sql-optimization
- "Caching/queues" → caching-strategy, message-queues
- Others → language-specific methodologies

---

## Sub-Skills

| Sub-skill | Focus | Methodologies |
|-----------|-------|---------------|
| **faion-backend-developer:systems** | Go, Rust, databases, caching | 22 |
| **faion-backend-developer:enterprise** | Java, C#, PHP, Ruby frameworks | 25 |

## Routing Logic

**Route to :systems for:**
- Go microservices, concurrency, HTTP handlers
- Rust backend services, async, ownership
- Database design, SQL optimization, NoSQL
- Caching strategies, message queues
- Low-level error handling

**Route to :enterprise for:**
- Java Spring Boot, JPA, Hibernate
- C# ASP.NET Core, Entity Framework
- PHP Laravel, Eloquent, queues
- Ruby Rails, ActiveRecord, Sidekiq
- Enterprise patterns and testing

## Integration

Invoked by parent skill `faion-software-developer` for backend work. Automatically selects appropriate sub-skill based on task context.

## Related Skills

| Skill | Relationship |
|-------|--------------|
| faion-python-developer | Python backends (Django, FastAPI) |
| faion-javascript-developer | Node.js backends |
| faion-api-developer | API design patterns |
| faion-testing-developer | Backend testing strategies |

---

*faion-backend-developer v1.0 | Orchestrator for 47 methodologies*
