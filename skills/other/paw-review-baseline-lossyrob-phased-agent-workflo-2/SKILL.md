---
name: paw-review-baseline
description: Analyzes the codebase at the PR's base commit to establish baseline understanding for review comparison.
---

# Baseline Research Activity Skill

Analyze the codebase **at the base commit** (before PR changes) to document how the system worked, what patterns existed, and what context informs understanding of the changes.

> **Reference**: Follow Core Review Principles from `paw-review-workflow` skill.

## CRITICAL: Baseline Only

**Your only job is to document the pre-change codebase as it existed.**

- DO NOT analyze the PR changes or compare before/after
- DO NOT suggest improvements or identify issues
- DO NOT critique the implementation
- ONLY describe what existed before: behavior, patterns, conventions, integration points

## Responsibilities

- Checkout base commit safely (with state restoration)
- Research how affected modules functioned before changes
- Document integration points and dependencies
- Identify patterns and conventions in affected areas
- Create CodeResearch.md with baseline understanding

## Non-Responsibilities

- PR change analysis or before/after comparison (understanding skill)
- Quality evaluation or recommendations (evaluation skills)
- Workflow orchestration (handled by workflow skill)

## Prerequisites

- ReviewContext.md must exist with base commit SHA
- ResearchQuestions.md should exist with research questions

## Multi-Repository Mode

When reviewing PRs across multiple repositories:

### Detection

Multi-repo mode activates when:
- Multiple PR URLs/numbers provided in input
- Multiple workspace folders open (detected via multiple `.git` directories)
- ReviewContext.md contains `related_prs` entries

### Per-Repository Processing

Process each repository's base commit independently:

1. **Iterate Repositories**: For each PR in the review set:
   - Read its ReviewContext.md from `.paw/reviews/PR-<number>-<repo-slug>/`
   - Extract base commit SHA and repository path
   
2. **Checkout and Research**: For each repository:
   - Navigate to repository root
   - Checkout base commit
   - Conduct baseline research
   - Create CodeResearch.md in that PR's artifact directory
   - Restore original state before moving to next repository

3. **State Restoration**: Between repositories:
   - Restore each repository to its original branch/HEAD
   - Verify clean working state before proceeding

### Cross-Repository Pattern Identification

When analyzing multiple repositories, also document:

- **Shared Conventions**: Common patterns used across repos (naming, error handling, API styles)
- **Interface Contracts**: How repositories communicate (API schemas, shared types, event formats)
- **Dependency Relationships**: Which repo depends on which (import paths, package dependencies)

Add a "Cross-Repository Patterns" section to each CodeResearch.md noting patterns that appear across the repository set.

### Error Handling

If one repository fails:
- Document the failure in that PR's artifact directory
- Continue with remaining repositories
- Report partial completion status

## Execution Steps

### Step 1: Sync Remote State

**Desired End State**: The base commit SHA (from ReviewContext.md) is locally available.

1. Extract from ReviewContext.md: remote name, base branch, base commit SHA
2. Ensure the repository has the latest remote state for the base branch
3. Verify the base commit is reachable locally
4. If the commit cannot be reached, report the blocker with context

### Step 2: Checkout Base Commit

**Desired End State**: Working directory is at the base commit, with ability to restore original state.

1. Record current branch/HEAD for later restoration
2. Checkout the base commit
3. Confirm the working directory reflects the pre-change state

**CRITICAL**: All subsequent research must analyze code at this commit.

### Step 3: Read Research Questions

1. Read `ResearchQuestions.md`
2. Note list of changed files from ReviewContext.md
3. Identify modules/areas needing baseline documentation

### Step 4: Analyze Pre-Change Codebase

Focus on areas identified in research prompt:

**Behavioral Documentation**:
- How modules functioned before changes
- Entry points, data flows, contracts
- Error handling approaches

**Integration Mapping**:
- Components depending on changed modules
- External dependencies
- API contracts and interfaces

**Pattern Recognition**:
- Coding conventions in affected areas
- Testing patterns for similar components
- Documentation patterns

**Test Coverage Baseline**:
- Existing tests for affected areas
- Test patterns and utilities used

### Step 5: Create CodeResearch.md

Write to `.paw/reviews/<identifier>/CodeResearch.md`:
- YAML frontmatter with metadata
- Answer questions from research prompt
- Document behavioral understanding
- Include file:line references (at base commit)
- Use template structure below

### Step 6: Update ReviewContext.md

Add CodeResearch.md to Artifacts section to signal completion.

### Step 7: Restore Original State

**Desired End State**: Working directory returned to original branch, clean state confirmed.

## Validation Criteria

Before completing:
- [ ] Base commit verified reachable
- [ ] Research conducted at base commit (not current HEAD)
- [ ] Research questions answered
- [ ] Behavioral understanding documented (not implementation details)
- [ ] Patterns and conventions identified
- [ ] File:line references included
- [ ] CodeResearch.md saved with valid frontmatter
- [ ] ReviewContext.md updated
- [ ] Original state restored

## Completion Response

```
Activity complete.
Artifact saved: .paw/reviews/<identifier>/CodeResearch.md
Status: Success
Summary: Baseline documented at commit <sha> - [N] modules analyzed, [M] patterns identified.

Original branch restored: <original-branch>
```

---

## CodeResearch.md Template

```markdown
---
date: <YYYY-MM-DD HH:MM:SS TZ>
git_commit: <base commit SHA>
branch: <base branch>
repository: <repository name>
topic: "Baseline Analysis for <PR Title or Branch>"
tags: [review, baseline, pre-change]
status: complete
last_updated: <YYYY-MM-DD>
---

# Baseline Research: <PR Title or Branch>

**Date**: <timestamp>
**Base Commit**: <sha>
**Base Branch**: <base-branch>
**Repository**: <repository>

**Context**: Documents how the system worked **before** PR changes to inform specification derivation and impact evaluation.

## Research Questions

<Questions from ResearchQuestions.md>

## Summary

<High-level overview of pre-change system state>

## Baseline Behavior

### <Module/Area 1>

**How it worked before changes:**
- Description of behavior (`file.ext:line`)
- Key functions and responsibilities
- Data flow and transformations
- Error handling approach

**Integration points:**
- Components that depended on this (`file.ext:line`)
- External dependencies
- API contracts and interfaces

### <Module/Area 2>

...

## Patterns & Conventions

**Established patterns observed:**
- Naming conventions
- Code organization patterns
- Error handling patterns
- Testing patterns

**File references:**
- `path/to/file.py:123` - Example of pattern X
- `another/file.ts:45-67` - Example of pattern Y

## Test Coverage Baseline

**Existing tests for affected areas:**
- `test/path/file.test.ts` - What was tested
- Coverage level (if measurable)
- Test patterns and conventions

## Performance Context

<If relevant to changes>
- Hot paths identified
- Performance characteristics
- Resource usage patterns

## Documentation Context

**Relevant documentation:**
- README sections
- API documentation
- Inline comments and explanations

## Open Questions

<Areas that need clarification or couldn't be fully documented>
```
