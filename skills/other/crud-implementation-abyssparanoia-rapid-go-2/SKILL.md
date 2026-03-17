---
name: crud-implementation
description: Complete workflow guide for implementing new CRUD entities. Use when adding a new resource, implementing full CRUD operations, or needing an overview of the database-to-API flow. Triggers: "new entity", "add resource", "implement CRUD", "create table and API". Orchestrates add-database-table, add-domain-entity, and add-api-endpoint skills.
---

# CRUD Implementation Workflow

Entry point for implementing a new entity with full CRUD operations.

## Workflow Overview

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│  add-database-table │ --> │  add-domain-entity  │ --> │  add-api-endpoint   │
│                     │     │                     │     │                     │
│  - Migration SQL    │     │  - Domain model     │     │  - Usecase          │
│  - Constant tables  │     │  - Repository       │     │  - Proto definition │
│  - SQLBoiler gen    │     │  - Marshaller       │     │  - gRPC handler     │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
```

## Quick Start

| Step | Skill | Key Command |
|------|-------|-------------|
| 1 | **add-database-table** | `make migrate.create` then `make migrate.up` |
| 2 | **add-domain-entity** | `make generate.mock` |
| 3 | **add-api-endpoint** | `make generate.buf` |

## Before You Start

1. Know the entity name and its fields
2. Identify relationships to existing entities
3. Determine which API actor (admin/public/debug)

## Step-by-Step

### Step 1: Database Layer

Use the **add-database-table** skill for:
- Creating migration file with table DDL
- Adding indexes and foreign keys
- Creating constant tables for enum fields
- Running `make migrate.up` to generate SQLBoiler

### Step 2: Domain Layer

Use the **add-domain-entity** skill for:
- Domain model with constructor and update methods
- Repository interface with query structs
- Marshaller (DB model <-> domain model)
- Repository implementation

### Step 3: API Layer

Use the **add-api-endpoint** skill for:
- Usecase input/output structs
- Interactor interface and implementation
- Protocol Buffers messages and RPCs
- gRPC handler and marshaller
- DI registration

## Final Verification

```bash
make lint.go && make test
```

## Related Skills

- **code-investigation** - Analyze existing patterns before implementation
- **review-pr** - Self-review before creating PR
- **create-pull-request** - PR creation with proper format
