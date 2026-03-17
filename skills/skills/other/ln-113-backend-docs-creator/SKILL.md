---
name: ln-113-backend-docs-creator
description: Creates 2 backend docs (api_spec.md, database_schema.md). L3 Worker invoked CONDITIONALLY when hasBackend or hasDatabase detected.
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Backend Documentation Creator

L3 Worker that creates 2 backend documentation files. CONDITIONAL - only invoked when project has backend or database.

## Purpose & Scope
- Creates api_spec.md (if hasBackend)
- Creates database_schema.md (if hasDatabase)
- Receives Context Store from ln-110-project-docs-coordinator
- OpenAPI 3.0 compliant API specification
- ER diagrams in Mermaid for database schema
- Never gathers context itself; uses coordinator input

## Invocation (who/when)
- **ln-110-project-docs-coordinator:** CONDITIONALLY invoked when:
  - `hasBackend=true` (express, fastify, nestjs, fastapi detected)
  - `hasDatabase=true` (pg, mongoose, prisma, sequelize detected)
- Never called directly by users

## Inputs
From coordinator:
- `contextStore`: Context Store with backend-specific data
  - API_TYPE (REST, GraphQL, gRPC)
  - API_ENDPOINTS (from route scan)
  - AUTH_SCHEME (JWT, OAuth2, API keys)
  - DATABASE_TYPE (PostgreSQL, MongoDB, MySQL)
  - SCHEMA_OVERVIEW (from migrations/models)
  - ER_DIAGRAM (generated from schema)
- `targetDir`: Project root directory
- `flags`: { hasBackend, hasDatabase }

## Documents Created (2, conditional)

| File | Condition | Questions | Auto-Discovery |
|------|-----------|-----------|----------------|
| docs/project/api_spec.md | hasBackend | Q39-Q40 | Medium |
| docs/project/database_schema.md | hasDatabase | Q41-Q42 | High |

## Workflow

### Phase 1: Check Conditions
1. Parse flags from coordinator
2. If `!hasBackend && !hasDatabase`: return early with empty result
3. Determine which documents to create

### Phase 2: Create Documents
For each applicable document:
1. Check if file exists (idempotent)
2. If exists: skip with log
3. If not exists:
   - Copy template
   - Replace placeholders with Context Store values
   - Generate ER diagram for database_schema.md
   - Mark `[TBD: X]` for missing data

### Phase 3: Self-Validate
1. Check SCOPE tag
2. Validate format:
   - api_spec.md: endpoint table, request/response examples
   - database_schema.md: ER diagram, table definitions
3. Check Maintenance section

### Phase 4: Return Status
```json
{
  "created": ["docs/project/api_spec.md"],
  "skipped": ["docs/project/database_schema.md"],
  "tbd_count": 2,
  "validation": "OK"
}
```

## Critical Notes
- **Conditional:** Skip entirely if no backend/database detected
- **OpenAPI compliant:** api_spec.md follows OpenAPI 3.0 structure
- **ER diagrams:** Generated in Mermaid erDiagram format
- **Idempotent:** Never overwrite existing files

### NO_CODE_EXAMPLES Rule (MANDATORY)
API spec documents **contracts**, NOT implementations:
- **ALLOWED in api_spec.md:** JSON request/response schemas (this IS the API contract), endpoint tables
- **FORBIDDEN:** Controller implementations, validation classes, service code, middleware examples
- **TEMPLATE RULE:** api_spec_template.md includes `<!-- NO_CODE_EXAMPLES: ... -->` tag - FOLLOW IT

### Stack Adaptation Rule (MANDATORY)
- Links must reference stack-appropriate docs (Microsoft for .NET, MDN for JS)
- API examples must match project stack (Express for Node.js, FastAPI for Python)

### Format Priority (MANDATORY)
Tables (endpoints, schemas) > Mermaid (ER diagrams) > Lists > Text

## Definition of Done
- Conditions checked (hasBackend, hasDatabase)
- Applicable documents created
- ER diagram generated (if database_schema.md created)
- Self-validation passed
- **Actuality verified:** all document facts match current code (paths, functions, APIs, configs exist and are accurate)
- Status returned to coordinator

## Reference Files
- Templates: `references/templates/api_spec_template.md`, `database_schema_template.md`
- Questions: `references/questions_backend.md` (Q39-Q42)

---
**Version:** 1.2.0
**Last Updated:** 2025-01-12
