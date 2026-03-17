---
name: context-update
description: Update CLAUDE.md files to improve efficiency and structure. Use when optimizing LLM context files, implementing review recommendations, splitting large files, or adding design doc pointers.
allowed-tools: Read, Grep, Glob, Edit, Write
context: fork
agent: context-doc-agent
---

# LLM Context Update

Updates CLAUDE.md and child CLAUDE.md files to improve context efficiency
based on review findings or user requests.

This skill runs in a forked context to avoid cluttering the main
conversation with detailed file modifications.

## Overview

This skill implements improvements to CLAUDE.md files:

- Refactor overly detailed sections into design docs
- Add @ syntax pointers to design documentation
- Split large files into hierarchical children
- Remove duplication across files
- Ensure imperative, high-level instructions

## Instructions

### 1. Understand Current State

**Read configuration:**

Load `.claude/design/design.config.json` to understand:

- Line limits for root and child files
- Module structure
- Design doc locations
- Quality standards

**Read existing CLAUDE.md files:**

Understand current structure and content before modifying.

**Check for review report:**

If user mentions review findings or provides a report, prioritize those
recommendations.

### 2. Determine Update Strategy

Based on the situation, choose approach:

#### Strategy A: Refactor detailed sections

When a section is too detailed for CLAUDE.md:

1. Create design doc at `.claude/design/{module}/{topic}.md`
2. Move detailed content to design doc
3. Replace with high-level summary + @ pointer
4. Add frontmatter to design doc

#### Strategy B: Add design doc pointers

When design docs exist but aren't referenced:

1. Find relevant design docs
2. Add pointer section with @ syntax
3. Include guidance on when to load context

#### Strategy C: Split into child files

When root CLAUDE.md is too large:

1. Identify module-specific sections
2. Create `{module}/CLAUDE.md` for each module
3. Move module details to child files
4. Keep only high-level overview in root
5. Add pointers to child files

#### Strategy D: Remove duplication

When content is repeated across files:

1. Keep content in most specific location
2. Replace duplicates with pointers
3. Ensure clear hierarchy

### 3. Execute Updates

**For each file modification:**

#### Step 1: Create design doc (if needed)

If moving content to design doc:

```markdown
---
status: current
module: {module-name}
category: {category}
created: YYYY-MM-DD
updated: YYYY-MM-DD
last-synced: YYYY-MM-DD
---

# {Topic Name}

## Overview
[Content moved from CLAUDE.md]

## Current State
[Detailed implementation details]

## Rationale
[Why this approach was chosen]
```

#### Step 2: Update CLAUDE.md

Replace detailed section with:

```markdown
## {Topic}

[1-2 sentence high-level summary]

**For detailed information:**
- Architecture → `@./.claude/design/{module}/architecture.md`
- Performance → `@./.claude/design/{module}/performance.md`

**When to load:**
Load these docs when working on {specific scenarios}.
**Do NOT load unless directly relevant to your task.**
```

#### Step 3: Create child CLAUDE.md (if splitting)

For new child file at `{module}/CLAUDE.md`:

```markdown
# {Module Name}

High-level guidance specific to this module.

## Module Overview
[Brief description]

## Key Commands
[Module-specific commands]

## Design Documentation

Complex systems have detailed design docs:

**When working on these areas, load relevant context:**
- {Topic} → `@../.claude/design/{module}/{topic}.md`

## Common Tasks
[Module-specific task guidance]
```

#### Step 4: Update root CLAUDE.md references

In root CLAUDE.md, replace module details with:

```markdown
## {Module Name}

[1 sentence description]

See `{module}/CLAUDE.md` for module-specific guidance.
```

### 4. Validate Changes

After modifications:

**Line count check:**

- Count lines in modified files
- Ensure within limits (root: 500, child: 300)
- If still over, identify additional sections to refactor

**Link validation:**

- Verify all @ syntax pointers reference existing files
- Check relative paths are correct
- Ensure file:line notation if needed

**Content check:**

- Verify no critical information was lost
- Ensure instructions remain clear and actionable
- Check that hierarchy makes sense

**Duplication check:**

- Confirm no content is duplicated across files
- Verify proper pointer usage instead

### 5. Report Changes

Provide summary of modifications:

```markdown
# CLAUDE.md Update Summary

## Files Modified

### {file-path}
**Before:** {line-count} lines
**After:** {line-count} lines
**Change:** {percentage}% reduction

**Changes made:**
- Moved "{section-name}" to `.claude/design/{path}.md`
- Added pointer to {design-doc}
- [Other changes]

### {file-path}
[Similar structure]

## Files Created

### {file-path}
**Type:** Design document
**Lines:** {line-count}
**Purpose:** Detailed {topic} documentation

### {file-path}
**Type:** Child CLAUDE.md
**Lines:** {line-count}
**Purpose:** {Module} specific guidance

## Quality Improvements

- Total line reduction: {number} lines
- New design docs: {count}
- New child CLAUDE.md files: {count}
- Design doc pointers added: {count}

## Validation Results

✓ All files within line limits
✓ All pointers reference existing files
✓ No content duplication
✓ Clear instruction hierarchy

## Next Steps

[If further improvements needed, suggest them]
```

## Patterns and Examples

### Pattern: Moving section to design doc

**Before (CLAUDE.md):**

```markdown
## Testing Strategy

We use Vitest with multiple test types:

1. Unit tests run with mocked services...
   [50 lines of detailed testing instructions]

2. Integration tests make real API calls...
   [40 lines of integration test details]

3. Coverage is tracked using v8 provider...
   [30 lines of coverage configuration]
```

**After (CLAUDE.md):**

```markdown
## Testing

Run tests with `pnpm test` (unit) or `pnpm test:all` (includes integration).

**For detailed testing guidance:**
→ `@./.claude/design/project/testing-strategy.md`

Load this doc when writing tests, debugging test failures, or
configuring test infrastructure.
```

**New design doc (`.claude/design/project/testing-strategy.md`):**

Contains the detailed 120 lines of testing documentation with proper
frontmatter.

### Pattern: Adding @ syntax pointers

**Before:**

```markdown
## Architecture

The system uses Effect-TS for functional architecture. See the
architecture design doc for details.
```

**After:**

```markdown
## Architecture

The system uses Effect-TS for functional architecture.

**For architectural details:**
→ `@./.claude/design/{module}/architecture.md`

Load when making architectural changes or adding new systems.
```

### Pattern: Creating child CLAUDE.md

**Before (root CLAUDE.md has 200-line section for `my-package`):**

**After (root CLAUDE.md):**

```markdown
## Packages

### my-package

TypeScript type registry with Effect-TS architecture.
See `pkgs/my-package/CLAUDE.md` for package-specific guidance.
```

**New (`pkgs/my-package/CLAUDE.md`):**

```markdown
# my-package

TypeScript type definition registry with caching and VFS support.

## Development

Commands:
- `pnpm test` - Run unit tests
- `pnpm build` - Build package

## Design Documentation

**When working on these systems, load context:**
- Architecture → `@../.claude/design/my-package/architecture.md`
- Observability → `@../.claude/design/my-package/observability.md`

## Implementation Notes

[Package-specific high-level guidance]
```

## Special Considerations

**Preserve user customizations:**

Don't remove sections users explicitly added unless they're duplicates
or too detailed.

**Maintain CLAUDE.local.md:**

If present, apply same standards. Note it overrides CLAUDE.md.

**Monorepo hierarchies:**

Ensure clear delegation: root → package CLAUDE.md → design docs.

**Incremental updates:**

Don't try to fix everything at once. Prioritize high-impact changes.

## Success Criteria

A successful update:

- Reduces line counts to within limits
- Adds clear @ syntax pointers where appropriate
- Maintains all critical information
- Improves context efficiency without losing clarity
- Creates proper design doc hierarchy
- Reports changes clearly
