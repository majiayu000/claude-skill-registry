---
name: codebase-quality:documentation
description: Documentation maintenance including CLAUDE.md sync, status tracking, and quality validation. Use when completing features, merging PRs, checking documentation freshness, or updating deployment status. Last skill in codebase-quality chain. Triggers on documentation update, CLAUDE.md sync, doc status, feature complete, bd close, merge to main, doc validation.
version: 1.0.0
title: "Codebase Quality:Documentation"
status: active
---

# Documentation Sub-Skill

Part of the [codebase-quality](../using-codebase-quality/SKILL.md) skill family.

## Purpose

Maintain accurate, up-to-date documentation across the codebase including CLAUDE.md files, solution designs, and deployment status tracking.

## Priority

**RUN LAST** in codebase-quality chain.

Documentation updates should reflect clean, secure code. Run after security and code-quality pass.

## Quick Reference

### Commands

```bash
# Full documentation check/update
/codebase-quality docs

# Specific operations
/codebase-quality docs update <module>
/codebase-quality docs status <feature>
/codebase-quality docs validate
/codebase-quality docs sync-claude-md
```

### Invocation

```python
# After code quality passes
Skill("codebase-quality:documentation")

# Specific sub-functions
Skill("codebase-quality:documentation:update")
Skill("codebase-quality:documentation:status")
Skill("codebase-quality:documentation:validate")
```

## Documentation Capabilities

### 1. Doc Updater

**Purpose**: Update docs after feature implementations

**Automatic Triggers**:
- `bd close <bd-id>` - Beads task completion
- Feature marked `passes: true` in feature_list.json
- PR merged to main

**Process**:
```
Feature Complete (bd close)
    ↓
1. Scan git diff for changed files
   git diff HEAD~5 --name-only
    ↓
2. Identify affected documentation:
   - Module CLAUDE.md (if patterns changed)
   - codebase_documentation/ (if architecture changed)
   - solution_designs/ (mark as implemented)
   - INDEX.md (if new docs created)
    ↓
3. Generate suggested updates
    ↓
4. Apply updates or present for review
    ↓
5. Commit with "docs(module): Update for <bd-id>"
```

**Example CLAUDE.md Update**:

```markdown
## Key Patterns (BEFORE)
- React Server Components for data fetching
- Tailwind CSS for styling

## Key Patterns (AFTER)
- React Server Components for data fetching
- Tailwind CSS for styling
- Custom hooks in `hooks/` for shared state ← NEW
```

### 2. Status Tracker

**Purpose**: Track deployment status of documented features

**Status Lifecycle**:
```
draft → approved → implementing → implemented → staged → rolled-out
  │                                                           │
  └──────────────── deprecated ◄──────────────────────────────┘
```

**Status Metadata Format** (YAML frontmatter):
```yaml
---
title: Room Instantiation Parameterization
type: solution_design
status: implemented
created_at: 2025-12-01
implemented_at: 2025-12-15
deployed_at: null
deployed_in: null
last_updated: 2025-12-19
related_beads: [bd-a1b2, bd-c3d4]
owners:
  - orchestrator
  - backend-solutions-engineer
---
```

**Automatic Status Updates**:

| Event | Status Update |
|-------|---------------|
| `bd close` | → `implemented` |
| Merge to staging | → `staged` |
| Merge to main | → `rolled-out` |

### 3. CLAUDE.md Sync

**Purpose**: Keep CLAUDE.md files synchronized across codebase

**Hierarchy**:
```
my-project/CLAUDE.md (root)
    ├── my-project-backend/CLAUDE.md
    │       ├── eddy_validate/CLAUDE.md
    │       └── user_chat/CLAUDE.md
    ├── my-project-frontend/CLAUDE.md
    └── my-project-communication/CLAUDE.md
```

**Sync Rules**:
1. Child inherits from parent
2. Child can override specific sections
3. New patterns propagate up
4. New directories get CLAUDE.md generated

**CLAUDE.md Template**:
```markdown
# [Module Name] - CLAUDE.md

> Inherits from: [CLAUDE.md](../../../CLAUDE.md)

## Module Overview
[Brief description]

## Key Patterns
[Framework-specific patterns]

## Directory Structure
[Key directories]

## Critical Files
[Important files to understand]

## Testing Strategy
[How to test this module]

## Dependencies
[Key dependencies]

## Recent Changes
[Changelog]
```

### 4. Doc Quality Checker

**Purpose**: Validate documentation completeness and accuracy

**Checks**:

| Check | Severity | Description |
|-------|----------|-------------|
| CLAUDE.md exists | HIGH | Every major module needs CLAUDE.md |
| Status current | MEDIUM | Deployed features marked rolled-out |
| No stale references | HIGH | No refs to deleted files |
| INDEX.md current | LOW | Cross-references valid |
| Recent updates | LOW | Docs updated in last 30 days |

## Documentation Report Format

```markdown
# Documentation Report - 2025-12-19

## Summary
- **Files Updated**: 3
- **Status Changes**: 2
- **Validation Issues**: 1

## Updates Applied

### CLAUDE.md Updates

**my-project-frontend/CLAUDE.md**:
```diff
+ - Custom hooks in `hooks/` for shared state
+ - Beads integration for task management
```

### Status Changes

**solution_designs/room-instantiation.md**:
- Status: `implementing` → `implemented`
- implemented_at: 2025-12-19
- related_beads: [bd-a1b2, bd-c3d4, bd-e5f6]

**solution_designs/beads-integration.md**:
- Status: `implemented` → `rolled-out`
- deployed_at: 2025-12-19
- deployed_in: PR #129

## Validation Issues

### WARN: Stale INDEX.md Reference
- `INDEX.md:45` references `OLD_FEATURE.md` (file missing)
- **Action**: Update or remove reference

## Passed Checks

✅ All modules have CLAUDE.md (12/12)
✅ All API endpoints documented
✅ All solution_designs have valid status
```

## Integration with Beads

### On bd close

```bash
bd close bd-a1b2 --reason "Validated"
    ↓
codebase-quality:documentation triggered
    ↓
1. Find related solution_design by bead ID
2. Update status to "implemented"
3. Set implemented_at timestamp
4. Update module CLAUDE.md if patterns changed
5. Commit doc changes
```

### Mapping File

The sync script creates `.claude/state/taskmaster-beads-mapping.json`:
```json
{
  "mappings": [
    { "task_id": "1", "bead_id": "bd-a1b2", "solution_design": "room-instantiation.md" }
  ]
}
```

## Integration with Orchestrator

### In Phase 2 Completion

```
Orchestrator: Feature validated, bd close
    ↓
Skill("codebase-quality:documentation")
    ↓
1. Scan changed files
2. Update relevant docs
3. Update status metadata
4. Commit with feature
```

### In Pre-Merge

```
/codebase-quality pre-merge
    ↓
documentation check:
- CLAUDE.md stale → Warn
- Status outdated → Warn
- Missing docs → Warn
- (never blocks - documentation is advisory)
```

## Best Practices

1. **Update Immediately**: Run doc update right after feature completion
2. **Status First**: Always update status before CLAUDE.md content
3. **Inherit Properly**: Use inheritance links in child CLAUDE.md
4. **Validate Regularly**: Run validation weekly
5. **Commit Together**: Commit docs with related code

## Output Locations

| Output | Location |
|--------|----------|
| CLAUDE.md files | Module directories |
| Status updates | Document frontmatter |
| Documentation report | `.claude/docs/doc-reports/` |
| Validation results | `.claude/docs/validation/` |

## Chaining

Documentation is the **last** skill in the chain:

```python
# Full audit order
Skill("codebase-quality:security")       # 1. Security first
Skill("codebase-quality:code-quality")   # 2. Code quality
Skill("codebase-quality:documentation")  # 3. Documentation last
```

After documentation:
- Generate final quality report
- Exit codebase-quality mode
- Or loop back if changes needed

---

**Skill Version**: 1.0.0
**Last Updated**: 2025-12-19
**Parent Skill**: [using-codebase-quality](../using-codebase-quality/SKILL.md)
