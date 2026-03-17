---
name: ln-723-seed-data-generator
description: "Universal seed data generator: MIGRATE from ORM schemas or GENERATE from entity definitions to any target format"
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# ln-723-seed-data-generator

**Type:** L3 Worker
**Category:** 7XX Project Bootstrap
**Parent:** ln-720-structure-migrator

Universal seed data generator with two modes: MIGRATE (parse existing ORM schemas) or GENERATE (create from entity definitions). Outputs to any target format (C#, TypeScript, Python, JSON, SQL).

---

## Purpose & Scope

| Aspect | Description |
|--------|-------------|
| **Input** | ORM schema files (MIGRATE) or entity list (GENERATE) |
| **Output** | Seed data files in target format |
| **Modes** | MIGRATE: parse existing ORM → seed data. GENERATE: entity definitions → seed data |

**Scope boundaries:**
- Parses ORM schema definitions or accepts entity lists
- Generates seed data in requested target format
- Creates realistic sample data using faker libraries
- Does not generate database migrations, EF Core configs, or ORM models

---

## Mode Selection

| Mode | When | Input | Source |
|------|------|-------|--------|
| **MIGRATE** | TRANSFORM pipeline — existing ORM schemas found | ORM schema files | Drizzle, Prisma, TypeORM, EF Core, SQLAlchemy, Django ORM |
| **GENERATE** | CREATE pipeline — no existing schemas | Entity list from ln-700 Phase 0 | User-provided or starter template (User, Role) |

If GENERATE mode receives no entity list, generate starter template with `User` (id, name, email, role, createdAt) and `Role` (id, name, description).

---

## Target Formats

| Format | Output File | Faker Library | Use Case |
|--------|-------------|---------------|----------|
| C# MockData | `MockData.cs` | Bogus | .NET projects |
| TypeScript fixtures | `seed.ts` | Faker.js | Node/React projects |
| Python factories | `factories.py` | Faker (Python) | Django/Flask projects |
| JSON | `seed.json` | — | API testing, import scripts |
| SQL | `seed.sql` | — | Direct DB seeding |

---

## Workflow

| Phase | Name | Actions | Output |
|-------|------|---------|--------|
| 1 | Parse/Define | 1A: Parse ORM schema (MIGRATE) or 1B: Accept entity list (GENERATE) | Entity model |
| 2 | Map Types | Apply universal type mapping to target format | Target type definitions |
| 3 | Generate Seed Data | Create seed files with faker-based realistic data | Seed data files |
| 4 | Verify | Validate relationships, check syntax | Valid seed files |

---

## Phase 1: Parse/Define

### 1A: MIGRATE Mode — Parse ORM Schema

| Step | Action | Reference |
|------|--------|-----------|
| 1A.1 | Locate schema file(s) | — |
| 1A.2 | Auto-detect ORM type | `orm_patterns.md` — ORM Auto-Detection table |
| 1A.3 | Extract table/model definitions | `orm_patterns.md` — per-ORM parsing section |
| 1A.4 | Extract column definitions with types | `orm_patterns.md` |
| 1A.5 | Identify constraints (PK, FK, nullable, unique) | `orm_patterns.md` |
| 1A.6 | Extract enum definitions | `orm_patterns.md` |

### 1B: GENERATE Mode — Accept Entity Definitions

| Step | Action | Reference |
|------|--------|-----------|
| 1B.1 | Receive entity list from orchestrator (or use starter template) | — |
| 1B.2 | Parse entity definitions (name, fields, types) | — |
| 1B.3 | Infer relationships from field names (`userId` → FK to User) | `relationship_mapping.md` |
| 1B.4 | Apply default constraints (id = PK, `*Id` = FK) | — |

**Output:** Entity model with columns, types, and constraints.

---

## Phase 2: Map Types

Convert entity types to target format types.

| Step | Action | Reference |
|------|--------|-----------|
| 2.1 | Select target format (from orchestrator params) | — |
| 2.2 | Map column types to target format | `type_mapping.md` — Universal Type Mapping table |
| 2.3 | Determine nullable status per target | `type_mapping.md` |
| 2.4 | Map foreign keys and relationships | `relationship_mapping.md` |
| 2.5 | Transform names to target convention | See Name Conventions table below |

**Name Conventions by Target:**

| Target | Class/Model | Property/Field | File |
|--------|-------------|----------------|------|
| C# | PascalCase singular | PascalCase | PascalCase.cs |
| TypeScript | PascalCase singular | camelCase | camelCase.ts |
| Python | PascalCase singular | snake_case | snake_case.py |
| JSON | camelCase | camelCase | kebab-case.json |
| SQL | snake_case plural | snake_case | snake_case.sql |

---

## Phase 3: Generate Seed Data

Create seed files with realistic data using faker libraries.

| Step | Action | Reference |
|------|--------|-----------|
| 3.1 | Determine generation order (parents → children) | `relationship_mapping.md` |
| 3.2 | Generate IDs (GUIDs/UUIDs) for all entities | `data_generation.md` |
| 3.3 | Generate field values using faker | `data_generation.md`, `type_mapping.md` — Faker Integration |
| 3.4 | Ensure FK relationships valid (child references existing parent ID) | `relationship_mapping.md` |
| 3.5 | Write seed file in target format | — |

**Faker integration rule:** All generated seed files MUST use faker libraries for realistic data with **deterministic seeding** (fixed seed value for reproducibility).

| Target | Faker Setup |
|--------|-------------|
| C# | `var faker = new Bogus.Faker(); Randomizer.Seed = new Random(42);` |
| TypeScript | `import { faker } from '@faker-js/faker'; faker.seed(42);` |
| Python | `from faker import Faker; fake = Faker(); Faker.seed(42)` |

**Generation order by dependency:**

| Order | Entity Type | Generate After |
|-------|-------------|----------------|
| 1 | Root entities (no FK) | First |
| 2 | First-level children | Parents exist |
| 3 | Second-level children | Grandparents exist |
| N | Deepest children | All ancestors exist |

---

## Phase 4: Verify

| Check | Method | Expected |
|-------|--------|----------|
| Syntax valid | Language-specific check | No syntax errors |
| FKs valid | Cross-reference | All FKs point to existing IDs |
| Types correct | Type analysis | Proper types for target format |
| Names follow convention | Pattern check | Per-target naming convention |
| Faker deterministic | Re-run with same seed | Identical output |

---

## Supported ORM Detection

| ORM | Detection Pattern | Ecosystem |
|-----|-------------------|-----------|
| Drizzle | `pgTable()`, `mysqlTable()`, `sqliteTable()` | Node.js |
| Prisma | `model X {` syntax in `.prisma` files | Node.js |
| TypeORM | `@Entity()`, `@Column()` decorators | Node.js |
| EF Core | `DbContext`, `DbSet<>`, `[Table]` attributes | .NET |
| SQLAlchemy | `Base = declarative_base()`, `Column()` | Python |
| Django ORM | `models.Model`, `models.CharField()` | Python |

---

## Entity Transformation Rules

| Source | Target | Transformation |
|--------|--------|----------------|
| Table name (plural, snake) | Class name (singular, Pascal) | `user_profiles` → `UserProfile` |
| Column name (snake) | Property name (target convention) | `created_at` → `CreatedAt` / `createdAt` / `created_at` |
| Enum name | Enum type (Pascal) | `status_enum` → `StatusEnum` |
| FK column | Navigation property | `user_id` → `UserId` / `userId` |

---

## Sample Data Guidelines

| Field Type | Sample Count | Distribution |
|------------|--------------|--------------|
| Root entities | 3-5 items | Varied status/priority |
| Child entities | 5-10 items | Distributed across parents |
| Leaf entities | 10-20 items | Realistic variety |

---

## Critical Rules

- **Single Responsibility:** Generate only seed data, no ORM models or migrations
- **Idempotent:** Can re-run with same seed to produce identical output
- **Valid Relationships:** All FKs must reference existing parent IDs
- **Faker Required:** Use faker libraries for realistic data, never random strings
- **Deterministic Seeding:** Fixed seed value (42) for reproducibility across re-runs
- **Generation Order:** Parents before children, always
- **Mode Awareness:** MIGRATE parses files; GENERATE accepts definitions — never mix

---

## Definition of Done

- [ ] Mode determined (MIGRATE or GENERATE)
- [ ] Entity model extracted/defined with all fields and constraints
- [ ] Target format selected and type mappings applied
- [ ] Seed data files generated with faker-based realistic values
- [ ] Deterministic seeding verified (re-run produces identical output)
- [ ] Foreign keys reference valid parent IDs
- [ ] Names follow target format conventions
- [ ] Sample data includes 5-10 items per entity

---

## Risk Mitigation

| Risk | Detection | Mitigation |
|------|-----------|------------|
| Unknown ORM type | Auto-detection fails | Log warning, ask orchestrator for ORM hint |
| Invalid type mapping | Unknown column type | Use string as fallback, log warning |
| FK mismatch | FK references non-existent ID | Generate parents first, validate after |
| No entity list in GENERATE | Empty input | Use starter template (User, Role) |
| Name collision | Duplicate class/table names | Prefix with feature name |
| Circular references | Self-referencing with cycles | Limit depth, validate graph |

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/orm_patterns.md` | ORM auto-detection and schema parsing patterns (Drizzle, Prisma, TypeORM, EF Core, SQLAlchemy, Django) |
| `references/type_mapping.md` | Universal type mapping (ORM-agnostic → C#, TypeScript, Python) + Faker integration |
| `references/data_generation.md` | Realistic sample data patterns and generation rules |
| `references/relationship_mapping.md` | FK handling, generation order, relationship inference |

---

**Version:** 3.0.0
**Last Updated:** 2026-02-07
