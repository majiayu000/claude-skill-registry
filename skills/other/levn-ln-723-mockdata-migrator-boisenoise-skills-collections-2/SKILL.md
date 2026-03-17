---
name: ln-723-mockdata-migrator
description: Migrates mock data from Drizzle ORM schemas to C# MockData classes
---

# ln-723-mockdata-migrator

**Type:** L3 Worker
**Category:** 7XX Project Bootstrap
**Parent:** ln-720-structure-migrator

Migrates mock data from ORM schemas to .NET MockData classes with realistic sample data.

---

## Purpose & Scope

| Aspect | Description |
|--------|-------------|
| **Input** | ORM schema files (Drizzle, Prisma, TypeORM) |
| **Output** | C# MockData static classes |
| **Primary ORM** | Drizzle (others supported) |

**Scope boundaries:**
- Parses ORM schema definitions
- Generates C# entities and MockData classes
- Creates realistic sample data
- Does not generate database migrations or EF Core configs

---

## Workflow

| Phase | Name | Actions | Output |
|-------|------|---------|--------|
| 1 | Parse Schema | Read ORM file, extract table definitions | Entity model |
| 2 | Map Types | Apply type mapping rules, detect nullable | C# type definitions |
| 3 | Generate MockData | Create static class, generate sample data | MockData.cs files |
| 4 | Verify | Compile check, relationship validation | Valid C# code |

---

## Phase 1: Parse Schema

Extract entity definitions from ORM schema.

| Step | Action | Reference |
|------|--------|-----------|
| 1.1 | Locate schema file(s) | — |
| 1.2 | Identify ORM type (Drizzle/Prisma/TypeORM) | Detect by syntax |
| 1.3 | Extract table definitions | `drizzle_patterns.md` |
| 1.4 | Extract column definitions | `drizzle_patterns.md` |
| 1.5 | Identify constraints (PK, FK, nullable) | `drizzle_patterns.md` |
| 1.6 | Extract enum definitions | `drizzle_patterns.md` |

**Output:** Entity model with columns, types, and constraints.

---

## Phase 2: Map Types

Convert ORM types to C# types.

| Step | Action | Reference |
|------|--------|-----------|
| 2.1 | Map column types to C# | `type_mapping.md` |
| 2.2 | Determine nullable status | `type_mapping.md` |
| 2.3 | Identify primary keys | `type_mapping.md` |
| 2.4 | Map foreign keys | `relationship_mapping.md` |
| 2.5 | Transform names (snake_case → PascalCase) | `drizzle_patterns.md` |

**Type mapping summary:**

| ORM Type | C# Type | Nullable Rule |
|----------|---------|---------------|
| uuid | Guid | No (PK), Depends (FK) |
| varchar | string | Check .notNull() |
| integer | int | No |
| boolean | bool | No |
| timestamp | DateTime | Depends |

---

## Phase 3: Generate MockData

Create C# MockData class with sample data.

| Step | Action | Reference |
|------|--------|-----------|
| 3.1 | Create MockData class | `data_generation.md` |
| 3.2 | Generate GUIDs for entities | `data_generation.md` |
| 3.3 | Generate sample data per field | `data_generation.md` |
| 3.4 | Ensure FK relationships valid | `relationship_mapping.md` |
| 3.5 | Create accessor methods | `data_generation.md` |

**Generation order by dependency:**

| Order | Entity Type | Generate After |
|-------|-------------|----------------|
| 1 | Root entities (no FK) | First |
| 2 | First-level children | Parents exist |
| 3 | Second-level children | Grandparents exist |
| N | Deepest children | All ancestors exist |

---

## Phase 4: Verify

Validate generated code.

| Check | Method | Expected |
|-------|--------|----------|
| Syntax valid | Compile check | No errors |
| FKs valid | Cross-reference | All FKs point to existing IDs |
| Types correct | Type analysis | Proper C# types |
| Names follow convention | Pattern check | PascalCase |

---

## Supported ORM Detection

| ORM | Detection Pattern |
|-----|-------------------|
| Drizzle | `pgTable()`, `mysqlTable()`, `sqliteTable()` |
| Prisma | `model X {` syntax |
| TypeORM | `@Entity()`, `@Column()` decorators |

---

## Entity Transformation Rules

| Source | Target | Transformation |
|--------|--------|----------------|
| Table name (plural, snake) | Class name (singular, Pascal) | `user_profiles` → `UserProfile` |
| Column name (snake) | Property name (Pascal) | `created_at` → `CreatedAt` |
| Enum name | Enum type (Pascal) | `status_enum` → `StatusEnum` |
| FK column | Navigation property | `user_id` → `UserId` |

---

## MockData Class Structure

| Component | Purpose |
|-----------|---------|
| Private static list | Holds immutable mock data |
| GetAll() method | Returns full list as IEnumerable |
| GetById(Guid id) | Finds single entity by ID |
| GetBy{FK}Id(Guid id) | Filters by foreign key |

---

## Sample Data Guidelines

| Field Type | Sample Count | Distribution |
|------------|--------------|--------------|
| Root entities | 3-5 items | Varied status/priority |
| Child entities | 5-10 items | Distributed across parents |
| Leaf entities | 10-20 items | Realistic variety |

---

## Critical Rules

- **Single Responsibility:** Generate only MockData, no database code
- **Idempotent:** Can re-run to regenerate
- **Valid Relationships:** All FKs must reference existing parent IDs
- **Realistic Data:** Use domain-appropriate values, not random strings
- **Generation Order:** Parents before children
- **Consistent GUIDs:** Use fixed GUIDs for reproducibility

---

## Definition of Done

- [ ] Schema file parsed successfully
- [ ] All tables/entities extracted
- [ ] Type mappings applied correctly
- [ ] MockData class generated per feature/entity group
- [ ] Sample data includes 5-10 items per entity
- [ ] Foreign keys reference valid parent IDs
- [ ] Accessor methods generated (GetAll, GetById)
- [ ] Code compiles without errors

---

## Risk Mitigation

| Risk | Detection | Mitigation |
|------|-----------|------------|
| Parse failure | Exception during parse | Support multiple schema formats |
| Invalid type mapping | Unknown ORM type | Log warning, use string as fallback |
| FK mismatch | FK references non-existent ID | Generate parents first, validate after |
| Name collision | Duplicate class names | Prefix with feature name |
| Circular references | Self-referencing with cycles | Limit depth, validate graph |

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/type_mapping.md` | ORM to C# type conversion rules |
| `references/drizzle_patterns.md` | Drizzle schema parsing patterns |
| `references/data_generation.md` | Realistic sample data patterns |
| `references/relationship_mapping.md` | FK handling and generation order |

---

**Version:** 2.0.0
**Last Updated:** 2026-01-10
