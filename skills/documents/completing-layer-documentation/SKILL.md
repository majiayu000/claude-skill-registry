---
name: completing-layer-documentation
description: Use after verifying-layer-documentation to fix all gaps found. Reads gaps.md and adds missing documentation.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(mkdir:*, ls:*)
  - Write(docs/unwind/**)
  - Edit(docs/unwind/**)
  - Task
---

# Completing Layer Documentation

**Purpose:** Process gaps.md files and add all missing documentation to layer files.

**Input:** `docs/unwind/layers/{layer}/gaps.md` from verification step
**Output:** Updated section files with gaps filled

## Process

### Step 1: Read gaps.md

For each layer, read `docs/unwind/layers/{layer}/gaps.md` to get:
- Missing items (with source location and target section)
- Inaccuracies (with what needs fixing)
- Uncategorized items (needing tags)

### Step 2: Dispatch Completion Agents

For each layer with gaps, dispatch an agent to fix them:

```
Task(subagent_type="general-purpose")
  description: "Complete [layer] documentation gaps"
  prompt: |
    Read docs/unwind/layers/{layer}/gaps.md for the work list.

    For each MISSING item:
    1. Read the source file at the specified location
    2. Document the item following analysis-principles.md
    3. Add to the specified section file
    4. Include the [MUST/SHOULD/DON'T] tag

    For each INACCURACY:
    1. Read the source file
    2. Fix the documentation to match actual code

    For each UNCATEGORIZED item:
    1. Add appropriate [MUST/SHOULD/DON'T] tag

    Link format: [from architecture.md]

    After completion:
    - Update index.md with correct counts
    - Delete gaps.md (work complete)
```

### Step 3: Verify Completion

After agents complete, check that:
- All gaps.md files are deleted (indicates completion)
- Section files have been updated
- Index.md counts are accurate

## Agent Prompt Template

```
Complete the documentation gaps for the {LAYER} layer.

## Work List

Read: docs/unwind/layers/{layer}/gaps.md

## Source Linking

Use this format: {link_format from architecture.md}

## For Each Missing Item

1. Read source at the specified location
2. Document following the layer's format (see analyzing-{layer}-layer skill)
3. Add to the correct section file
4. Include [MUST/SHOULD/DON'T] tag as specified

## For Each Inaccuracy

1. Read source at the specified location
2. Edit the documentation to match actual code

## For Each Uncategorized Item

1. Find the item in the section file
2. Add the appropriate tag based on:
   - MUST: Core functionality, business logic, external contracts
   - SHOULD: Valuable patterns, good practices
   - DON'T: Tech-specific implementation details

## When Complete

1. Update index.md with accurate counts
2. Delete gaps.md to signal completion
```

## Parallel Execution

Layers can be completed in parallel - no dependencies between layer completions:

```
Task(subagent_type="general-purpose", description="Complete database gaps")
Task(subagent_type="general-purpose", description="Complete service-layer gaps")
Task(subagent_type="general-purpose", description="Complete api gaps")
... (all in parallel)
```

## Example Completion Flow

**Input gaps.md:**
```markdown
# Database Documentation Gaps

## Missing Items

### audit_logs table
- **Type:** table
- **Location:** src/schema.ts:412-445
- **Category:** SHOULD
- **Section:** schema.md
```

**Agent actions:**
1. Read `src/schema.ts:412-445`
2. Extract table definition
3. Add to `schema.md`:
```markdown
### audit_logs [SHOULD]

```sql
CREATE TABLE audit_logs (
  id SERIAL PRIMARY KEY,
  ...
);
```

| Column | Type | Nullable | Default | Constraints |
|--------|------|----------|---------|-------------|
| id | SERIAL | NO | auto | PRIMARY KEY |
...
```
4. Update index.md table count
5. Delete gaps.md

## Handling Large Gap Lists

If a layer has many gaps (20+):
- Process incrementally - write after each item
- Don't buffer all changes
- This prevents token exhaustion

## After Completion

When all layers are complete:
- All gaps.md files should be deleted
- Run `synthesizing-findings` to generate final documentation
