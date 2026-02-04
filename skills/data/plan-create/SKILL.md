---
name: plan-create
description: Create new plan documents from templates. Use when starting new
  implementation work, documenting planned features, or organizing development
  tasks.
allowed-tools: Read, Write, Bash
context: fork
agent: design-doc-agent
---

# Plan Creation

Creates new plan documents from templates with proper frontmatter and
structure.

## Overview

This skill creates plan documents by:

1. Accepting plan metadata (name, title, type, modules, design docs)
2. Reading the appropriate template from `templates/` (co-located with skill)
3. Generating frontmatter with current dates and provided metadata
4. Writing the plan file to `.claude/plans/`
5. Validating the created plan using plan-validate skill
6. Reporting success or validation errors

## Quick Start

**Create basic plan:**

```bash
/plan-create "Cache Optimization Implementation"
```

**Create plan with module:**

```bash
/plan-create "Cache Optimization" --module=effect-type-registry
```

**Create plan with design doc link:**

```bash
/plan-create "Observability Phase 2" \
  --module=effect-type-registry \
  --implements=effect-type-registry/observability.md
```

**Create refactoring plan:**

```bash
/plan-create "Refactor Type Loading" --type=refactor
```

## How It Works

### 1. Parse Parameters

- `title`: Human-readable plan title [REQUIRED]
- `--name`: Plan file name (auto-generated from title if omitted)
- `--type`: Template type (feature, refactor, docs) [default: feature]
- `--module`: Module name (must exist in design.config.json)
- `--implements`: Design doc path(s) to link (comma-separated)
- `--owner`: Plan owner username
- `--estimated-effort`: Time estimate (e.g., "2-3 weeks")

### 2. Generate Plan Name

If `--name` not provided, convert title to kebab-case:

- "Cache Optimization Implementation" → "cache-optimization-implementation"
- "Add Feature X" → "add-feature-x"
- Validate kebab-case format: lowercase, hyphens only

### 3. Check for Conflicts

Ensure plan doesn't already exist:

- Check `.claude/plans/{name}.md`
- Check `.claude/plans/_archive/{name}.md`
- Report error if file exists

### 4. Read Template

Read template from `templates/` directory:

- `feature-plan.md` - Feature implementation (default)
- `refactor-plan.md` - Refactoring or architectural changes
- `docs-plan.md` - Documentation work

### 5. Generate Frontmatter

Create YAML frontmatter with:

**Required Fields:**

- `name`: Kebab-case plan identifier
- `title`: Human-readable title
- `created`: Current date (YYYY-MM-DD)
- `updated`: Current date (YYYY-MM-DD)
- `status`: "ready" (new plans start ready)
- `progress`: 0 (new plans have 0% progress)

**Optional Fields (if provided):**

- `implements`: Array of design doc paths
- `modules`: Array of module names
- `owner`: Plan owner username
- `estimated-effort`: Time estimate
- `categories`: Auto-set based on template type

**Always Null (for new plans):**

- `started`: null
- `completed`: null
- `actual-effort`: null
- `outcome`: null
- `archived`: null
- `archival-reason`: null

### 6. Write Plan File

Write to `.claude/plans/{name}.md` with:

- Generated frontmatter
- Template body content
- Proper YAML formatting

### 7. Validate Plan

Execute `.claude/scripts/validate-plan.sh` on created file:

- Validates frontmatter structure
- Checks required fields
- Validates status-progress alignment
- Reports any issues

### 8. Generate Report

Output creation results:

**Success:**

```text
✓ Plan created: cache-optimization-implementation.md
  Title: Cache Optimization Implementation
  Type: feature
  Module: effect-type-registry
  Status: ready (0%)
  Path: .claude/plans/cache-optimization-implementation.md

✓ Plan validation passed
```

**Failure:**

```text
✗ Plan creation failed: cache-optimization-implementation

Error: Plan file already exists
Path: .claude/plans/cache-optimization-implementation.md

Suggestion: Use a different name or update the existing plan
```

## Usage Patterns

### Create Basic Plan

```bash
# Simplest form - just a title
/plan-create "My Feature Implementation"
```

Creates:

- Name: `my-feature-implementation`
- Type: `feature` (default)
- Status: `ready`
- Progress: 0%

### Create Plan with Module

```bash
/plan-create "Add Caching" --module=effect-type-registry
```

Links plan to module for organization and discovery.

### Create Plan Linked to Design Doc

```bash
/plan-create "Implement Observability" \
  --module=effect-type-registry \
  --implements=effect-type-registry/observability.md
```

Creates bidirectional link:

- Plan → Design doc (via `implements` field)
- Design doc can discover plan via module/name

### Create with Custom Name

```bash
/plan-create "Phase 2: Advanced Features" \
  --name=advanced-features-phase-2
```

Useful when title doesn't convert well to kebab-case.

### Create Refactoring Plan

```bash
/plan-create "Refactor Type Loading System" --type=refactor
```

Uses refactor template with architecture focus.

### Create Documentation Plan

```bash
/plan-create "RSPress API Documentation" --type=docs
```

Uses docs template with writing phases.

### Create with All Metadata

```bash
/plan-create "Cache Optimization" \
  --module=effect-type-registry \
  --implements=effect-type-registry/cache-optimization.md \
  --owner=@spencerbeggs \
  --estimated-effort="2-3 weeks"
```

## Implementation Steps

1. **Parse arguments** from user input (title, flags)
2. **Generate plan name** from title (or use --name)
3. **Validate name format** (kebab-case)
4. **Check for conflicts** (file already exists)
5. **Read config** from `.claude/design/design.config.json`
6. **Validate module** exists in config (if provided)
7. **Read template** from `templates/{type}-plan.md`
8. **Generate frontmatter** with metadata
9. **Write plan file** to `.claude/plans/{name}.md`
10. **Validate plan** using plan-validate skill
11. **Generate report** with success/error details
12. **Return exit code** (0 = success, 1 = failure)

## Error Messages

### Plan Already Exists

```text
✗ Plan file already exists: {name}.md

Path: .claude/plans/{name}.md
Created: {date}

Options:
  1. Use a different name: --name=different-name
  2. Update existing plan: /plan-update {name}
  3. Archive old plan first: mv {path} {archive-path}
```

### Invalid Module

```text
✗ Module not found: {module}

Available modules:
  - effect-type-registry
  - rspress-plugin-api-extractor
  - design-doc-system

Fix: Use --module={valid-module} or omit --module flag
```

### Invalid Design Doc Path

```text
✗ Design doc not found: {path}

Searched: .claude/design/{path}

Fix: Verify design doc exists or omit --implements flag
```

### Invalid Name Format

```text
✗ Invalid plan name: {name}

Plan names must be kebab-case: lowercase, hyphens only
Valid examples: my-feature, cache-optimization-v2

Fix: Use --name={valid-name} or let name auto-generate from title
```

### Template Not Found

```text
✗ Template not found: {type}-plan.md

Available templates:
  - feature-plan.md
  - refactor-plan.md
  - docs-plan.md

Fix: Use --type=feature|refactor|docs
```

### Validation Failed

```text
✓ Plan created: {name}.md
✗ Plan validation failed

Errors (2):
  ✗ Missing required field: status
  ✗ progress: must be integer 0-100

The plan file was created but has validation errors.
Fix these errors before committing the plan.
```

## Examples

See [examples.md](./examples.md) for detailed usage examples.

## Related Skills

- `plan-validate` - Validate plan structure
- `plan-update` - Update plan status/progress
- `plan-list` - List all plans
- `design-init` - Create design docs
