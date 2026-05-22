---
description: Spring Boot backend development patterns for [PROJECT_NAME]
globs:
  - "src/main/java/**/*.java"
  - "src/main/kotlin/**/*.kt"
  - "src/test/**/*.java"
alwaysApply: false
---

# Spring Boot Backend Skill

> Project: [PROJECT_NAME]
> Framework: Spring Boot [VERSION]
> Generated: [DATE]

## Quick Reference

### Architecture
- **Controllers**: REST endpoints, thin, delegate to services
- **Services**: Business logic, transactions
- **Repositories**: Data access with Spring Data JPA
- **DTOs**: Request/response objects

### Dependency Injection
- Constructor injection (preferred)
- @Autowired for field injection (avoid)

### Transactions
- @Transactional on service methods
- Read-only for queries

## Available Modules

| Module | File | Use When |
|--------|------|----------|
| Service Patterns | services.md | Business logic |
| Repository Patterns | models.md | JPA, queries |
| API Design | api-design.md | REST controllers |
| Testing | testing.md | JUnit, Mockito |
| Dos and Don'ts | dos-and-donts.md | Project learnings |

## Project Context

### Tech Stack
<!-- Extracted from agent-os/product/tech-stack.md -->
- **Framework:** Spring Boot [SPRING_VERSION]
- **Java Version:** [JAVA_VERSION]
- **Database:** [DATABASE]
- **ORM:** [ORM_LIBRARY]
- **Testing:** [TESTING_FRAMEWORK]
- **Authentication:** [AUTH_LIBRARY]

### Architecture Patterns
<!-- Extracted from agent-os/product/architecture-decision.md -->

**Service Layer:**
[SERVICE_LAYER_PATTERN]

**API Design:**
[API_DESIGN_PATTERN]

**Data Access:**
[DATA_ACCESS_PATTERN]

**Error Handling:**
[ERROR_HANDLING_PATTERN]

### Project Structure
<!-- Extracted from agent-os/product/architecture-structure.md -->
```
[PROJECT_STRUCTURE]
```

### Naming Conventions
[NAMING_CONVENTIONS]

---

## Self-Learning

→ Füge Erkenntnisse zu `dos-and-donts.md` hinzu.
