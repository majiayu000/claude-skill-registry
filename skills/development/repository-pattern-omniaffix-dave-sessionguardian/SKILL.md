---
name: repository-pattern
description: Use repositories to encapsulate database queries and provide a clean interface for data access Use when designing system architecture. Architecture category skill.
metadata:
  category: Architecture
  priority: medium
  is-built-in: true
  session-guardian-id: builtin_repository_pattern
---

# Repository Pattern

Use repositories to encapsulate database queries and provide a clean interface for data access. Repositories return domain objects, not database rows. The rest of the application works with repositories without knowing about the database. This enables: testing with in-memory repositories, switching databases, centralizing query logic. Define repository interfaces that the domain uses.