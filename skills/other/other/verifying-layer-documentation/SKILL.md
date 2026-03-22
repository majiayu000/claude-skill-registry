---
name: verifying-layer-documentation
description: Use after layer analysis to detect gaps in documentation. Outputs a work list for completing-layer-documentation.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(mkdir:*, ls:*)
  - Write(docs/unwind/**)
---

# Verifying Layer Documentation

**Purpose:** Detect gaps between documentation and source code. Output is a work list for the next skill to fix.

**Output:** `docs/unwind/layers/{layer}/gaps.md` - list of missing items only

**Does NOT:**
- Write about what's correct
- Assign scores
- Apply fixes (that's the next skill's job)

## Process

For each layer, compare documentation against source and output ONLY the gaps.

### Step 1: Read Documentation

```
Read docs/unwind/layers/{layer}/index.md
Follow links to all section files
Build list of documented items
```

### Step 2: Read Source

```
Read source files for the layer (from architecture.md entry_points)
Build list of actual items in code
```

### Step 3: Find Gaps

Compare the two lists:
- Items in source but NOT in documentation → **MISSING**
- Items documented incorrectly → **INACCURATE**

Note: All items should already have [MUST/SHOULD/DON'T] tags (see analysis-principles.md section 9). If items lack tags, that indicates the analysis skill was not followed correctly - not a verification gap.

### Step 4: Write gaps.md

Write ONLY the gaps to `docs/unwind/layers/{layer}/gaps.md`

## Output Format

```markdown
# {Layer} Documentation Gaps

## Missing Items

### {item_name}
- **Type:** table|service|endpoint|entity|etc
- **Location:** {source_file}:{line_start}-{line_end}
- **Category:** MUST|SHOULD|DON'T
- **Section:** {which section file it belongs in}

### {next_item}
...

## Inaccuracies

### {item_name}
- **Location:** {source_file}:{lines}
- **Issue:** {what's wrong}
- **Actual:** {what code shows}
```

## Example gaps.md

```markdown
# Database Documentation Gaps

## Missing Items

### audit_logs table
- **Type:** table
- **Location:** src/schema.ts:412-445
- **Category:** SHOULD
- **Section:** schema.md

### user_sessions table
- **Type:** table
- **Location:** src/schema.ts:450-478
- **Category:** MUST
- **Section:** schema.md

### settings JSONB schema
- **Type:** jsonb_schema
- **Location:** src/schema.ts:89 (organisation.settings)
- **Category:** MUST
- **Section:** jsonb-schemas.md

## Inaccuracies

### users.status column
- **Location:** src/schema.ts:45
- **Issue:** Wrong type documented
- **Actual:** enum('active', 'suspended', 'deleted') not varchar
```

## Agent Dispatch

For each layer, dispatch verification in parallel:

```
Task(subagent_type="general-purpose")
  description: "Find gaps in [layer] documentation"
  prompt: |
    Compare docs/unwind/layers/{layer}/ against source code.

    Entry points: [from architecture.md]
    Link format: [from architecture.md]

    Output ONLY gaps to docs/unwind/layers/{layer}/gaps.md

    DO NOT:
    - Write about what's correct
    - Assign scores
    - Fix anything

    ONLY list:
    - Missing items (with source location, category, target section)
    - Inaccuracies (with what's wrong and actual value)
```

## Layer-Specific Gap Detection

### Database Layer
- Missing tables
- Missing columns
- Missing JSONB schemas
- Missing indexes
- Missing FK relationships

### Service Layer
- Missing services
- Missing formulas
- Missing edge cases
- Missing constants

### API Layer
- Missing endpoints
- Missing route files
- Missing permission documentation
- Missing error responses

### Domain Model
- Missing entities
- Missing enums
- Missing validation rules
- Missing state transitions

### Frontend Layer
- Missing pages
- Missing user flows
- Missing permission gates

## Next Step

After gaps.md files are created, run `completing-layer-documentation` to fix all gaps.
