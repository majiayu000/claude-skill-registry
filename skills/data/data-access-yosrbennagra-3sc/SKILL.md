---
name: data-access
description: Implement data access for the .NET 8 WPF widget host app using EF Core or Dapper. Use when creating repositories, unit of work, migrations, DbContext configuration, and query patterns while keeping clean architecture boundaries.
---

# Data Access

## Overview

Define reliable persistence patterns using EF Core or Dapper without leaking infrastructure concerns into domain or UI.

## Constraints

- .NET 8
- Clean architecture boundaries
- Prefer repositories and unit of work for write operations

## Definition of done (DoD)

- Repository interfaces in Application layer, implementations in Infrastructure
- DbContext lifetime is per-operation (using statement or scoped)
- Read queries use AsNoTracking where applicable
- Migrations are tested with test database before merge
- No raw SQL outside Infrastructure layer
- Integration tests exist for repository operations

## Workflow

1. Decide EF Core vs Dapper based on query complexity and tracking needs.
2. Define interfaces in Application/Domain and implement in Infrastructure.
3. Configure DbContext or connection factory and register via DI.
4. Use migrations for schema changes and keep seed data explicit.
5. Keep data models aligned to domain entities or mapping layer.

## EF Core guidance

- Use `DbContext` per unit of work.
- Use `AsNoTracking` for read-only queries.
- Keep migrations small and reversible.

## Dapper guidance

- Use parameterized queries only.
- Map results to DTOs, not EF entities.
- Keep SQL in Infrastructure.

## References

- `references/ef-core.md` for configuration and migrations.
- `references/dapper.md` for query patterns.
- `references/repositories-uow.md` for repository/unit of work boundaries.
