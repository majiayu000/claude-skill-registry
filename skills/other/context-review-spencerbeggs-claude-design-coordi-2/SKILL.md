---
name: context-review
description: Review CLAUDE.md files for quality, efficiency, and structure. Use when auditing LLM context files, checking documentation organization, preparing for context optimization, or ensuring lean imperative instructions.
allowed-tools: Read, Grep, Glob
context: fork
agent: context-doc-agent
---

# LLM Context Review

Reviews CLAUDE.md and child CLAUDE.md files to ensure they provide
efficient, focused context for AI assistants without token waste.

## Overview

This skill analyzes CLAUDE.md files against quality standards defined in
`.claude/design/design.config.json` and the LLM Context Agent design document.
It checks line counts, content structure, design doc pointers, and
identifies opportunities for improvement.

## Instructions

### 1. Locate Configuration

Read `.claude/design/design.config.json` to understand quality standards:

- Root CLAUDE.md max lines (default: 500)
- Child CLAUDE.md max lines (default: 300)
- Required design doc pointers setting
- Module structure for monorepos

### 2. Find CLAUDE.md Files

Search for CLAUDE.md files in the repository:

- Root: `CLAUDE.md` or `CLAUDE.local.md`
- Children: `{module}/CLAUDE.md` for each module
- Monorepo packages: Check each package directory

### 3. Analyze Each File

For each CLAUDE.md file found:

**Line Count Check:**

- Count total lines (excluding blank lines)
- Compare against limits (root: 500, child: 300)
- Flag files exceeding limits

**Content Structure Check:**

- Verify high-level imperative instructions (not details)
- Check for design doc pointers using @ syntax or links
- Identify overly detailed sections (candidate for design docs)
- Look for duplicated information between files

**Design Doc Pointer Check:**

- Find references to design documentation
- Verify @ syntax is used correctly: `@./.claude/design/module/doc.md`
- Ensure pointers include guidance on when to load context
- Check that docs being pointed to actually exist

**Hierarchy Check:**

- Verify child CLAUDE.md files exist where appropriate
- Check for modules with complex docs that should have children
- Identify opportunities to split large root files

### 4. Generate Report

Create a comprehensive review report with:

**Summary:**

- Total CLAUDE.md files found
- Average line count
- Files over limit count
- Missing design doc pointers count

**Issues by File:**

Group by severity (high, medium, low):

- **High:** Files exceeding line limits by >20%
- **High:** Missing design doc pointers when design docs exist
- **High:** Overly detailed sections that should be design docs
- **Medium:** Files approaching line limits (>80%)
- **Medium:** No child CLAUDE.md for complex modules
- **Low:** Minor structure improvements

**Recommendations:**

Actionable suggestions:

1. Which sections to move to design docs
2. Where to create child CLAUDE.md files
3. How to improve @ syntax pointer clarity
4. What duplicated content to consolidate

**Example Issue:**

```text
### High Priority

CLAUDE.md: 687 lines (limit: 500, 37% over)
- "Testing" section is very detailed (120 lines) → move to design doc
- "Architecture" duplicates content in pkgs/my-package/CLAUDE.md
- Missing pointer to `.claude/design/my-package/architecture.md`

Recommendation:
1. Create `.claude/design/project/testing-strategy.md` for testing details
2. Add pointer: "For testing details → @./.claude/design/project/testing-strategy.md"
3. Remove architecture duplication, keep only pointer to package CLAUDE.md
```

### 5. Quality Metrics

Calculate and report:

- **Efficiency Score:** Percentage of files within limits
- **Pointer Coverage:** Percentage of design docs with CLAUDE.md pointers
- **Hierarchy Health:** Appropriate child files for module complexity
- **Duplication Level:** Amount of repeated content across files

## Output Format

Generate markdown report with structure:

```markdown
# CLAUDE.md Review Report

**Date:** YYYY-MM-DD
**Repository:** {name}
**Type:** {monorepo|single-package}

## Summary

- CLAUDE.md files: X
- Average line count: Y
- Files over limit: Z
- Overall efficiency: N%

## Issues Found

### High Priority
[List of high-priority issues with file locations and recommendations]

### Medium Priority
[List of medium-priority issues]

### Low Priority
[List of low-priority issues]

## Recommendations

1. [Specific actionable recommendation]
2. [Specific actionable recommendation]
...

## Quality Metrics

- Efficiency Score: X%
- Pointer Coverage: Y%
- Hierarchy Health: Z%
- Duplication Level: N%

## Next Steps

[Suggested order of operations to address issues]
```

## Special Cases

**Monorepo:**

Review both root CLAUDE.md and package-level files. Check for appropriate
delegation between root and children.

**No design docs yet:**

If `.claude/design/` doesn't exist, note that design documentation system
should be set up first.

**CLAUDE.local.md:**

These override CLAUDE.md and should follow same standards. Review both if
present, noting which takes precedence.

## Success Criteria

A good review report:

- Identifies specific line numbers for problematic sections
- Provides concrete recommendations, not vague suggestions
- Prioritizes issues by impact on context efficiency
- Includes actionable next steps in recommended order
