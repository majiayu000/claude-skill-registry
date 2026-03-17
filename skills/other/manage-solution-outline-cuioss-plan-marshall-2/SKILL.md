---
name: manage-solution-outline
description: Manage solution outline documents - standards, examples, validation, and deliverable extraction
user-invocable: false
allowed-tools: Read, Glob, Bash
---

# Manage Solution Outline Skill

This skill provides structure guidelines, examples, and operations for `solution_outline.md` documents. Load this skill when creating or modifying solution outlines.

## When to Load This Skill

Load this skill in Step 0 when:
- Creating a solution outline (via `solution-outline-agent` thin agent)
- Reviewing or updating an existing solution outline
- Validating solution document structure

**First action**: Load `plan-marshall:analyze-project-architecture` skill for module information and architectural context.

**Not needed for**: Creating tasks from deliverables (use manage-tasks skill)

---

## Document Structure

Solution outlines have a fixed structure with required and optional sections:

```markdown
# Solution: {title}

plan_id: {plan_id}
created: {timestamp}
compatibility: {value} — {long description}

## Summary          ← REQUIRED: 2-3 sentences describing the approach

## Overview         ← REQUIRED: ASCII diagram showing architecture/flow

## Deliverables     ← REQUIRED: Numbered ### sections

## Approach         ← OPTIONAL: Execution strategy

## Dependencies     ← OPTIONAL: External requirements

## Risks and Mitigations  ← OPTIONAL: Risk analysis
```

See [standards/structure.md](standards/structure.md) for detailed requirements.

---

## Deliverables Format

Deliverables use numbered `###` headings:

```markdown
## Deliverables

### 1. Create JwtValidationService class

Description of what this deliverable produces.

**Location**: `src/main/java/de/cuioss/auth/jwt/JwtValidationService.java`

**Responsibilities**:
- Validate JWT signature
- Check token expiration

### 2. Add configuration support

Description...
```

**Key Rules**:
- Numbers must be sequential starting from 1
- Titles should be concrete work items (not abstract goals)
- Each deliverable should be independently achievable
- Include location, responsibilities, or success criteria

See [standards/deliverables.md](standards/deliverables.md) for reference format.

---

## Overview Diagrams

The Overview section contains ASCII diagrams showing component relationships. Different task types use different diagram patterns:

| Task Type | Diagram Style |
|-----------|---------------|
| Feature | Component/class relationships with dependencies |
| Refactoring | BEFORE → AFTER transformation comparison |
| Bugfix | Problem sequence + Solution architecture |
| Documentation | File structure with cross-references |
| Plugin | Integration flow with build phases |

See [standards/diagrams.md](standards/diagrams.md) for patterns and examples.

---

## Examples by Task Type

Examples provide starting points for different task categories:

| Example | Use When |
|---------|----------|
| [examples/java-feature.md](examples/java-feature.md) | Java feature implementation |
| [examples/javascript-feature.md](examples/javascript-feature.md) | JavaScript/frontend feature |
| [examples/plugin-feature.md](examples/plugin-feature.md) | Claude Code plugin development |
| [examples/refactoring.md](examples/refactoring.md) | Code refactoring tasks |
| [examples/bugfix.md](examples/bugfix.md) | Bug fix with root cause analysis |
| [examples/documentation-task.md](examples/documentation-task.md) | Documentation creation/updates |

---

## Writing the Solution Document

### Step 0: Load Project Architecture

Load project architecture knowledge via the `plan-marshall:analyze-project-architecture` skill:

```
Skill: plan-marshall:analyze-project-architecture
```

Then query module information:

```bash
python3 .plan/execute-script.py plan-marshall:analyze-project-architecture:architecture info
python3 .plan/execute-script.py plan-marshall:analyze-project-architecture:architecture module --name {module-name}
```

Use the returned structure for:

| Section | Use For |
|---------|---------|
| `modules.{name}.responsibility` | Understand what each module does |
| `modules.{name}.purpose` | Understand module classification (library, extension, etc.) |
| `modules.{name}.key_packages` | Identify architecturally significant packages |
| `modules.{name}.skills_by_profile` | Know which skills apply per profile |
| `modules.{name}.tips` | Apply implementation guidance |
| `modules.{name}.insights` | Leverage learned knowledge |
| `internal_dependencies` | Know what depends on what |

### Step 1: Analyze Request

Read the request document to understand:
- What is being requested
- Scope and constraints
- Success criteria

### Step 2: Design Architecture

Before writing, determine:
- Components involved
- Dependencies between components
- Execution order

### Step 3: Create Diagram

Draw ASCII diagram showing:
- New components (boxed)
- Existing components (labeled)
- Dependencies (arrows)
- Package/file structure

### Step 4: Write and Validate Document

Write using stdin with validation to handle ASCII box-drawing characters:

```bash
python3 .plan/execute-script.py \
  pm-workflow:manage-solution-outline:manage-solution-outline write \
  --plan-id {plan_id} \
  [--force] <<'EOF'
# Solution: {title}

## Summary
...

## Overview
```
┌─────────────┐
│  Component  │
└─────────────┘
```

## Deliverables
...
EOF
```

**Parameters**:
- `--plan-id` (required): Plan identifier
- `--force`: Overwrite existing solution outline

**Note**: Validation runs automatically on write - checks for required sections (Summary, Overview, Deliverables) and numbered deliverable format (`### N. Title`). If validation fails, the file is NOT written.

**Why heredoc?** Solution outlines contain ASCII diagrams with box-drawing characters (│, ─, ┌, └). Using `<<'EOF'` (quoted) preserves content exactly without variable expansion or escaping issues.

---

## Deliverable References

When tasks reference deliverables, use the full reference format:

```toon
deliverable: "1. Create JwtValidationService class"
```

**Reference Format Rules**:
- Include number and full title
- Format: `N. Title` (number, dot, space, title)
- Title must match exactly what's in solution document

**Validation**:
```bash
python3 .plan/execute-script.py pm-workflow:manage-solution-outline:manage-solution-outline \
  list-deliverables \
  --plan-id {plan_id}
```

---

## Integration

**Loaded by**:
- `pm-workflow:solution-outline-agent` (thin agent that loads domain skills from references.json)
- Domain skills: `pm-plugin-development:ext-outline-plugin`, etc.

**Data Sources** (via skills):
- `plan-marshall:analyze-project-architecture` - Project architecture knowledge (modules, responsibilities, packages)
- `marshal.json` - Module domains for skill routing
- Request document - What is being requested

**Scripts Used**:

**Script**: `pm-workflow:manage-solution-outline:manage-solution-outline`

| Command | Parameters | Description |
|---------|------------|-------------|
| `write` | `--plan-id [--force]` | Write solution from stdin (validates automatically) |
| `validate` | `--plan-id` | Validate structure |
| `read` | `--plan-id [--raw] [--deliverable-number N]` | Read solution or specific deliverable |
| `list-deliverables` | `--plan-id` | Extract deliverables list |
| `exists` | `--plan-id` | Check if solution exists |

**Related Skills**:
- `plan-marshall:analyze-project-architecture` - Project architecture knowledge (load in Step 0)
- `pm-workflow:manage-tasks` - Task creation with deliverable references
- `pm-workflow:manage-plan-documents` - Request document operations

---

## Script Output Examples

### write

**Output** (TOON):
```toon
status: success
plan_id: my-feature
file: solution_outline.md
action: created
validation:
  deliverable_count: 3
  sections_found: summary,overview,deliverables
  compatibility: breaking — Clean-slate approach, no deprecation nor transitionary comments
```

### validate

**Output** (TOON):
```toon
status: success
plan_id: my-feature
file: solution_outline.md
validation:
  sections_found: summary,overview,deliverables
  deliverable_count: 3
  deliverables:
    - 1. Create JwtValidationService class
    - 2. Add configuration support
    - 3. Create unit tests
  compatibility: breaking — Clean-slate approach, no deprecation nor transitionary comments
```

### list-deliverables

**Output** (TOON):
```toon
status: success
plan_id: my-feature
deliverable_count: 3
deliverables:
  - number: 1
    title: Create JwtValidationService class
    reference: 1. Create JwtValidationService class
  - number: 2
    title: Add configuration support
    reference: 2. Add configuration support
```

### read

**Output** (TOON):
```toon
status: success
plan_id: my-feature
file: solution_outline.md
content:
  _header: # Solution: JWT Validation...
  summary: Implement JWT validation service...
  overview: Component architecture diagram...
  deliverables: ### 1. Create JwtValidationService...
```

With `--raw`: Returns raw markdown content.

With `--deliverable-number N`: Returns a specific deliverable by number.

**Example**: Read deliverable 3:
```bash
python3 .plan/execute-script.py pm-workflow:manage-solution-outline:manage-solution-outline read \
  --plan-id {plan_id} \
  --deliverable-number 3
```

**Output** (TOON):
```toon
status: success
plan_id: my-feature
deliverable:
  number: 3
  title: Implement unit tests
  reference: 3. Implement unit tests
  metadata:
    change_type: feature
    execution_mode: automated
    domain: java
    module: jwt-service
    depends: 1
  profiles:
    - testing
  affected_files:
    - src/test/java/de/cuioss/jwt/JwtValidationServiceTest.java
```

If deliverable not found, returns error with available numbers:
```toon
status: error
error: deliverable_not_found
plan_id: my-feature
number: 999
available:
  - 1
  - 2
  - 3
```

### exists

**Output** (TOON):
```toon
status: success
plan_id: my-feature
file: solution_outline.md
exists: true
```

Returns exit code 0 if exists, 1 if not.
