---
name: convert
description: "Convert tasks.md to prd.json with smart routing classification. Use after creating tasks. Triggers on: convert to prd, generate prd.json, convert tasks."
---

# Tasks to PRD Converter (with Smart Routing)

Convert user stories from tasks.md into prd.json format WITH automatic routing classification.

> **Note:** This command is typically auto-run by the `/relentless.tasks` skill.
> Manual execution is only needed if you edit `tasks.md` by hand after generation.

---

## The Job

**⚠️ CRITICAL: This skill requires executing the `relentless convert` CLI command. Do NOT generate prd.json manually!**

1. Locate tasks.md in the current feature directory
2. Validate story structure, dependencies, and TDD compliance
3. Preview conversion (show story count, dependency chain)
4. **EXECUTE the CLI command:** `relentless convert relentless/features/NNN-feature/tasks.md --feature <feature-name>`
5. Validate the generated prd.json HAS routing metadata
6. Display routing summary (cost estimates per story)
7. Report next step

---

## Why Routing Matters

Routing is the **core value** of Relentless:

- **Simple tasks** use cheap models (haiku, flash) - saves money
- **Complex tasks** use SOTA models (opus, gpt-5) - ensures quality
- **Estimated costs** BEFORE execution - no surprises
- **Compare estimated vs actual** after execution - learn and improve

Without routing, you lose the intelligent cost optimization that makes Relentless valuable.

---

## Step 1: Find Feature Directory

Look in `relentless/features/` for the most recent feature:

```bash
ls -la relentless/features/
```

Verify:
- [ ] tasks.md exists in the feature directory
- [ ] spec.md exists (for context)
- [ ] Feature directory follows naming convention (NNN-feature-name)

If tasks.md doesn't exist, suggest running `/relentless.tasks` first.

---

## Step 2: Validate tasks.md Structure

The CLI now **automatically validates** tasks.md before conversion. You can also validate manually:

```bash
relentless validate relentless/features/NNN-feature/tasks.md
```

### Validation Checks

The validator checks for:
- [ ] Each story has unique ID (US-XXX format)
- [ ] Each story has acceptance criteria (after filtering)
- [ ] Dependencies reference existing stories
- [ ] No circular dependencies
- [ ] No underscore format in dependencies (US_001 should be US-001)

### Automatic Filtering (with Warnings)

The following criteria are automatically filtered during conversion:
- **Standalone file paths**: `` `src/file.ts` `` → Add context: "`src/file.ts` contains X"
- **Section markers**: `**Files:**` → Move outside acceptance criteria section
- **Short text**: Less than 3 characters

### Example Valid Story

```markdown
### US-001: Create User Registration

**Description:** As a new user, I want to register so I can access the app.

**Acceptance Criteria:**
- [ ] POST /api/register endpoint exists
- [ ] Email validation works
- [ ] Password is hashed
- [ ] `src/auth/register.ts` contains the registration handler
- [ ] Unit tests pass
- [ ] Integration test passes

**Dependencies:** None
**Phase:** Foundation
**Priority:** 1
```

### Example Validation Output

```
Validating tasks.md...

⚠️  2 validation warning(s):
  [FILTERED_CRITERIA]
    2 acceptance criteria will be filtered during conversion

  📝 2 criteria will be filtered during conversion
     US-003: "`src/queue/types.ts`"
     US-004: "**"
```

---

## Step 3: Run Conversion (with Routing)

**⚠️ IMPORTANT: Execute this bash command using the Bash tool. Do NOT generate prd.json manually!**

```bash
relentless convert relentless/features/NNN-feature/tasks.md --feature <feature-name>
```

Replace `NNN-feature` with the actual feature directory name (e.g., `001-user-auth`).

### Options

| Flag | Description |
|------|-------------|
| `--mode <mode>` | Routing mode: free, cheap, good (default), genius |
| `--skip-routing` | Skip routing (NOT recommended) |
| `--auto-number` | Auto-number feature directory |
| `--with-checklist` | Merge checklist criteria |

### Expected Output

```
Converting tasks.md...

Classifying 6 stories for routing (mode: good)...
  US-001: simple -> claude/haiku-4.5 ($0.0012)
  US-002: medium -> claude/sonnet-4.5 ($0.0034)
  US-003: complex -> claude/opus-4.5 ($0.0156)
  US-004: simple -> claude/haiku-4.5 ($0.0010)
  US-005: medium -> claude/sonnet-4.5 ($0.0028)
  US-006: expert -> claude/opus-4.5 ($0.0234)

Total estimated cost: $0.0474

Created relentless/features/NNN-feature/
  prd.json - 6 stories
  Routing metadata included
  prd.md - from tasks.md
  progress.txt - progress log
```

---

## Step 4: Validate Routing Output

After conversion, verify the prd.json has routing metadata:

```bash
cat relentless/features/<feature>/prd.json | jq '.userStories[0].routing'
```

### Expected Routing Structure

```json
{
  "complexity": "simple",
  "harness": "claude",
  "model": "haiku-4.5",
  "mode": "good",
  "estimatedCost": 0.0012,
  "classificationReasoning": "Task classified as simple (confidence: 85%)..."
}
```

**CRITICAL:** If routing is missing, the conversion was run with `--skip-routing`. Re-run without that flag.

---

## Step 5: Report Summary

After successful conversion, provide this summary:

```markdown
## Conversion Complete

**Feature:** NNN-feature-name
**Stories:** 6 total

### Routing Summary

| Story  | Complexity | Harness/Model        | Est. Cost |
|--------|------------|----------------------|-----------|
| US-001 | simple     | claude/haiku-4.5     | $0.0012   |
| US-002 | medium     | claude/sonnet-4.5    | $0.0034   |
| US-003 | complex    | claude/opus-4.5      | $0.0156   |
| US-004 | simple     | claude/haiku-4.5     | $0.0010   |
| US-005 | medium     | claude/sonnet-4.5    | $0.0028   |
| US-006 | expert     | claude/opus-4.5      | $0.0234   |

**Total Estimated Cost:** $0.0474

### Files Created

- `relentless/features/<feature>/prd.json` - PRD with routing
- `relentless/features/<feature>/prd.md` - Copy of tasks.md

### Next Steps

1. Review routing decisions (adjust mode if needed)
2. Run `/relentless.analyze` to check consistency
3. Run `relentless run --feature <name> --mode good`
```

---

## Complexity Classification

The classifier determines complexity based on:

| Complexity | Indicators | Example |
|------------|------------|---------|
| **simple** | Basic CRUD, single file, straightforward | "Add logging to function" |
| **medium** | Multiple files, some logic | "Create REST endpoint with validation" |
| **complex** | Architecture changes, multiple systems | "Implement OAuth2 authentication" |
| **expert** | Novel solutions, deep expertise | "Design event sourcing system" |

---

## Mode-Model Matrix

| Mode | Simple | Medium | Complex | Expert |
|------|--------|--------|---------|--------|
| free | glm-4.7 | glm-4.7 | grok-code-fast-1 | grok-code-fast-1 |
| cheap | haiku-4.5 | gemini-flash | gpt-5.2-low | gpt-5.2-low |
| good | sonnet-4.5 | sonnet-4.5 | opus-4.5 | opus-4.5 |
| genius | opus-4.5 | opus-4.5 | opus-4.5 | opus-4.5 |

---

## Troubleshooting

### "Tasks.md not found"

Run `/relentless.tasks` first to generate tasks.md from spec.md and plan.md.

### "No routing metadata"

The conversion was run with `--skip-routing`. Re-run:
```bash
relentless convert relentless/features/<feature>/tasks.md --feature <feature-name>
```

### "Validation failed"

The tasks.md has format issues. Run validation to see details:
```bash
relentless validate relentless/features/<feature>/tasks.md
```

Common issues:
- **DUPLICATE_STORY_ID**: Two stories have the same ID
- **MISSING_DEPENDENCY**: A story depends on non-existent story ID
- **CIRCULAR_DEPENDENCY**: Stories form a dependency loop

### "Criteria will be filtered"

Some acceptance criteria don't meet format requirements. Fix by:
- Adding context to file paths: `` `src/file.ts` `` → "`src/file.ts` contains X"
- Moving section markers outside acceptance criteria
- Writing longer, more descriptive criteria

### "Invalid dependency"

A story references a non-existent story ID. Check the `Dependencies:` line.

### "Circular dependency detected"

Stories reference each other in a cycle. Example: US-001 depends on US-002, and US-002 depends on US-001.

### "Dependency uses underscore format"

Use dashes in story IDs: `US-001` not `US_001`.

---

## Notes

- Always run conversion WITH routing (default behavior)
- Routing metadata enables intelligent cost optimization
- Review complexity classifications before running
- Use `--mode free` for testing/experimentation
- Use `--mode good` (default) for production work
- Use `--mode genius` for critical/complex features
