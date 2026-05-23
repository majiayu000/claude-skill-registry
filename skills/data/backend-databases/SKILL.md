---
name: backend-databases
description: (ePost) Use when working with PostgreSQL queries, MongoDB documents, or database persistence in the epost backend
user-invocable: false
metadata:
  keywords:
    - postgresql
    - mongodb
    - database
    - sql
    - query
    - migration
    - connection-pool
  agent-affinity:
    - epost-fullstack-developer
    - epost-debugger
  platforms:
    - backend
  connections:
    enhances: [backend-javaee]
---

# Database Knowledge

PostgreSQL for transactional data, MongoDB for documents/audit.

See `backend/javaee/persistence-patterns.md` for code patterns.
