---
name: flyway-consolidate
description: Analyze and consolidate Flyway SQL migrations into clean, domain-grouped CREATE TABLE migrations for pre-production projects. Use when consolidating database migrations, refactoring Flyway schemas, simplifying migration history, grouping tables by domain, or when user mentions "consolidate migrations", "merge migrations", "clean up Flyway", "refactor schema", "baseline migrations".
disable-model-invocation: true
---

# Flyway Migration Consolidation

Analyze incremental Flyway migrations and generate consolidated, domain-grouped CREATE TABLE migrations for pre-production projects where the database can be reset from scratch.

## When to Use

| Scenario | Apply? |
|----------|--------|
| Pre-production project with migration sprawl | Yes |
| Database can be reset from scratch | Yes |
| Many incremental ALTER TABLE migrations | Yes |
| Want domain-based organization before release | Yes |
| Production database exists | **No** |
| Migration history must be preserved | **No** |

## Consolidation Workflow

1. **Discover** — Find all `V*__*.sql` files using Glob
2. **Analyze** — Read each migration, identify CREATE/ALTER/INSERT operations and affected tables
3. **Infer final schema** — Apply all changes in order to determine the intended final state
4. **Group by domain** — Organize tables into logical business domains
5. **Resolve dependencies** — Topological sort by FK relationships
6. **Generate** — Produce clean CREATE TABLE migrations when user confirms

See [WORKFLOW.md](WORKFLOW.md) for detailed step-by-step process.

## Output Structure

Produce these deliverables in order:

### 1. Analysis Report
- Total migration count and breakdown by type (CREATE, ALTER, INSERT)
- Per-migration summary: what it does, which tables it affects
- Final table count and column inventory

### 2. Domain Grouping
- Tables organized by inferred business domain
- Migration-to-domain mapping showing which originals feed into each group

### 3. Proposed Structure
- New migration file list (e.g., V1–V6) with table assignments
- Dependency order rationale
- Reduction metrics (file count, estimated line savings)

### 4. Consolidated SQL (on request)
- Clean CREATE TABLE statements with final-form columns and constraints
- Separate migration for idempotent seed data
- Optional separate migration for performance indexes

## Domain Grouping Heuristics

| Signal | Assignment |
|--------|-----------|
| Table prefix (`user_*`, `order_*`) | Prefix-based domain |
| Foreign key cluster | Related tables share domain |
| Join tables (`user_roles`) | Domain of primary entity |
| Audit tables (`*_audit`, `*_history`) | Same domain as parent |
| Config/settings tables | Infrastructure domain |
| Explicit schema namespaces | Schema name as domain |

Present ambiguous cases to the user for decision.

## Critical Constraints

1. **Preserve the final schema exactly** — no tables, columns, constraints, or relationships lost
2. **Idempotent seed data** — use `ON CONFLICT DO NOTHING` or equivalent for INSERT statements
3. **Dependency order** — referenced tables created before foreign keys that point to them
4. **Prefer CREATE over ALTER** — final-form table definitions, not incremental changes
5. **History rewriting allowed** — pre-production only, database will be reset
6. **Document assumptions** — call out any ambiguities in the original migrations explicitly

## Tools

- **Glob** `**/V*__*.sql` and `**/R*__*.sql` to find versioned and repeatable migrations
- **Read** each migration file to parse SQL content
- **Grep** `CREATE TABLE`, `ALTER TABLE`, `FOREIGN KEY`, `INSERT INTO` to search across migrations

## Examples

See [EXAMPLES.md](EXAMPLES.md) for complete before/after consolidation scenarios and [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues:
- Column evolution chains collapsed into single CREATE TABLE
- Multi-domain consolidation (40 migrations to 6)
- FK dependency resolution across domains
- Seed data made idempotent

## Reminders

1. Always present the analysis report and proposed structure **before** generating SQL
2. Wait for user confirmation of domain groupings before generating consolidated files
3. Handle circular FK dependencies by deferring constraint creation with ALTER TABLE
4. Self-referential FKs: create table first, add FK in same migration via ALTER
5. Compare final column/constraint inventory against originals as a verification step
