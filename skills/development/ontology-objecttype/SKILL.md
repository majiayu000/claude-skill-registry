---
name: ontology-objecttype
description: |
  ObjectType Definition Assistant for Ontology-Driven-Architecture (ODA) migration.
  Analyzes existing codebases to identify ObjectType candidates through interactive workflow.
  Uses L1/L2/L3 Progressive Disclosure for analysis results.
user-invocable: true
model: opus
version: "3.0.0"
argument-hint: "analyze <path> | resume <session-id> | help"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Task
  - mcp__sequential-thinking__sequentialthinking
  - AskUserQuestion
  - WebSearch
  - WebFetch
hooks:
  Setup:
    - type: command
      command: "source /home/palantir/.claude/skills/shared/workload-files.sh"
      timeout: 5000
---

# /ontology-objecttype - ObjectType Definition Assistant

> **Version:** 3.0.0 | **Model:** opus

---

## Overview

| Aspect | Description |
|--------|-------------|
| **Purpose** | Analyze codebases and define ObjectTypes for ODA migration |
| **Output** | L1: Candidate summary / L2: Per-class analysis / L3: Full YAML definitions |
| **Reference** | `.claude/rules/ontology.md` for naming conventions |

---

## Cross-Skill Integration

| Skill | Relationship |
|-------|--------------|
| `/ontology-core` | Validates generated ObjectType definitions |
| `/ontology-why` | Called for "why?" questions about design decisions |
| `/ontology-linktype` | (Planned) LinkType definition after ObjectType completion |

---

## Commands

| Command | Description |
|---------|-------------|
| `analyze <path>` | Analyze project/file for ObjectType candidates |
| `resume <session-id>` | Resume previous analysis session |
| `help` | Show usage information |

---

## Detection Patterns

| Pattern | Detection Method | Example |
|---------|-----------------|---------|
| Python class | `class ClassName:` | `class Employee:` |
| SQLAlchemy ORM | `Base` or `declarative_base()` | `class User(Base):` |
| Django ORM | `models.Model` | `class Article(models.Model):` |
| Pydantic | `BaseModel` | `class Config(BaseModel):` |

---

## Interactive Workflow (Phase 1-4)

### Phase 1: Context Clarification

**Purpose:** Clarify source type and business domain

```python
AskUserQuestion(questions=[
    {
        "question": "What is your source for this ObjectType definition?",
        "header": "Source Type",
        "options": [
            {"label": "Existing source code", "description": "Python, Java, TypeScript"},
            {"label": "Database schema", "description": "SQL DDL, ORM models"},
            {"label": "Business requirements", "description": "Requirements documents"},
            {"label": "Manual definition", "description": "New domain model"}
        ]
    }
])
```

**Validation Gate:** `source_validity`

### Phase 2: Entity Discovery

**Purpose:** Extract entities + PK strategy + Property type mapping

1. Scan source code for entity candidates
2. Select Primary Key strategy (single_column / composite / composite_hashed)
3. Map Python types to Foundry DataTypes

**Validation Gates:** `candidate_extraction`, `pk_determinism`

### Phase 3: Link Definition

**Purpose:** Detect relationships and define cardinality

| Cardinality | FK Location | Backing Table |
|-------------|-------------|---------------|
| ONE_TO_ONE | Either side | No |
| ONE_TO_MANY | "Many" side | No |
| MANY_TO_ONE | "Many" side | No |
| MANY_TO_MANY | - | Yes (required) |

**Validation Gate:** `link_integrity`

### Phase 4: Validation & Output

**Purpose:** Final validation and YAML generation

**Validation Gate:** `semantic_consistency`

---

## Validation Gates

| Gate | Phase | Description |
|------|-------|-------------|
| `source_validity` | 1 | Source path accessible, domain context provided |
| `candidate_extraction` | 2 | At least one entity with class name and properties |
| `pk_determinism` | 2 | PK is STRING, required, follows determinism rules |
| `link_integrity` | 3 | M:N has join table, FK references valid targets |
| `semantic_consistency` | 4 | API names follow conventions, all types valid |

---

## PK Strategy Options

| Strategy | Description | Use Case |
|----------|-------------|----------|
| `single_column` | Use existing unique column | `employee_id`, `user_uuid` |
| `composite` | Combine columns with separator | `company_id + dept_id` |
| `composite_hashed` | SHA256 hash of combined columns | Long composite keys |

---

## DataType Mapping

| Category | Types |
|----------|-------|
| Primitive | STRING, INTEGER, LONG, FLOAT, DOUBLE, BOOLEAN, DECIMAL |
| Temporal | DATE, TIMESTAMP, DATETIME, TIMESERIES |
| Complex | ARRAY (requires itemType), STRUCT (requires fields), JSON |
| Spatial | GEOPOINT, GEOSHAPE |
| Media | MEDIA_REFERENCE, BINARY, MARKDOWN |
| AI/ML | VECTOR (requires dimension) |

---

## Output Format

### L1 - Candidate Summary

```
Found 12 Entity Candidates
  ObjectType candidates (8): Employee, Department, Project...
  Review needed (2): DTO/Mixin patterns
  Excluded (2): Helper/Config classes
```

### L2 - Per-Class Analysis

```yaml
entity_name: Employee
pk_strategy: single_column
pk_column: employee_id
properties:
  - api_name: employeeId
    data_type: STRING
    required: true
    is_pk: true
```

### L3 - Full YAML Definition

```yaml
# objecttype-Employee.yaml
api_name: Employee
display_name: Employee
primary_key:
  source_columns: [employee_id]
  strategy: single_column
properties:
  - api_name: employeeId
    data_type: STRING
    required: true
links:
  - link_type_name: EmployeeToDepartment
    target_object_type: Department
    cardinality: MANY_TO_ONE
```

---

## Session State

```json
{
  "session_id": "obj-a1b2c3",
  "target_path": "/home/palantir/my-project",
  "current_phase": "phase_2_entity",
  "phase_results": {
    "phase_1_context": { "status": "completed" },
    "phase_2_entity": { "status": "in_progress" },
    "phase_3_link": { "status": "pending" },
    "phase_4_output": { "status": "pending" }
  }
}
```

---

## Reference System

### Local Reference (ontology-definition package)

```
/home/palantir/park-kyungchan/palantir/Ontology-Definition/
├── ontology_definition/types/    # Type definitions
├── ontology_definition/core/     # Enums, base classes
└── tests/                        # Usage examples
```

### External References (WebSearch/WebFetch)

Trusted sources only:
- `palantir.com/docs/*` (Official documentation)
- `github.com/palantir/*` (Official repositories)
- Palantir case studies and conference materials

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Path not found | Prompt for correct path |
| No Python files | Show available file types |
| No classes found | Suggest manual definition |
| Session expired | Start new or resume with `--resume` |

---

## Version History

| Version | Change |
|---------|--------|
| 1.0.0 | Initial ObjectType definition assistant |
| 1.1.0 | Phase 1-4 interactive workflow, L1/L2/L3 output |
| 3.0.0 | Frontmatter normalization, MCP tool inclusion, duplicate removal |

**End of Skill Definition**
