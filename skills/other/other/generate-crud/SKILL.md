---
name: generate-crud
description: Generate complete CRUD operations for an entity
argument-hint: "<entity-name> [--with-tests] [--with-dto]"
tags: [codegen, crud, scaffold, productivity]
user-invocable: true
---

# Generate CRUD Operations

Generate Controller, Service, Repository, DTO, and Tests for an entity.

## What To Do

1. **Analyze existing patterns**: Read an existing entity implementation to match conventions.
2. **Generate files**:
   - Controller with GET (all, by id), POST, PUT, DELETE endpoints
   - Service interface + implementation with validation
   - Repository interface + implementation (CosmosDB)
   - DTO with ToDomain() and FromDomain() static methods
   - Unit tests for service layer
3. **Register in DI**: Add service and repository to Program.cs

## Arguments
- `<entity-name>`: Entity name in PascalCase
- `--with-tests`: Generate test file (default: true)
- `--with-dto`: Generate DTO classes (default: true)