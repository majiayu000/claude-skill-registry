---
name: complete
description: "Complete task: validate, document, review, commit, and merge to develop. Use when all implementation is done and ready to finalize."
model: claude-sonnet-4-20250514
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task
---

# /complete

Complete a task with full validation, documentation updates, reviews, and automatic merge to develop.

## Usage

```bash
/complete careerbrain 002         # Complete specific issue
/complete careerbrain             # Complete current/active issue
```

## What It Does

1. Validate PLAN completion and spec compliance
2. Update all project documentation
3. Create final commit with doc changes
4. Run mandatory code review + security audit
5. Merge to develop branch
6. Clean up feature branch

**GitFlow Pattern**: `feature/*` → `develop` (automatic) | `develop` → `main` (requires PR)

## Prerequisites

- All implementation complete (code written)
- Active issue with completed work
- PLAN.md exists with phases mostly complete

## Execution Flow

### 1. Check PLAN.md Completion
```
✓ All phases complete (5/5)
  or
✗ Incomplete phases:
  - [ ] 1.3 - Implement session refresh
```

### 2. Spec Compliance Validation

**Acceptance Scenario Coverage:**
- Search tests matching each Given/When/Then scenario
- Create missing tests if needed

**Success Metrics Verification:**
- Check performance, coverage, accessibility

**Out-of-Scope Enforcement:**
- Scan for code that violates out-of-scope items

**Agent Constraints Check:**
- Verify no dependencies added (if constrained)
- Check no files outside scope modified

### 3. Update Spec Status Markers

If the TASK has an `implements:` field, update inline status markers in the spec:

```markdown
# Before (in spaces/[project]/docs/specs/*.md)
- 🚧 User registration with email/password

# After
- ✅ User registration with email/password
```

This provides public visibility into what's implemented.

### 4. Update All Documentation

Scan and validate ALL docs in `spaces/[project]/docs/`:
- architecture-overview.md
- data-model.md
- api-overview.md
- README.md

### 5. Update CHANGELOG

**MANDATORY**: Add entries under `[Unreleased]` section.

Categories:
- `### Added` - New features (TASKs)
- `### Fixed` - Bug fixes (BUGs)
- `### Changed` - Modifications
- `### Security` - Security updates

### 6. Final WORKLOG Entry

```markdown
## YYYY-MM-DD HH:MM - COMPLETED

Issue ### complete and ready for merge.

Summary:
- [What was implemented]
- [What was deferred]
```

### 7. Update Status

Set issue frontmatter: `status: complete`

### 8. Create Final Commit

Stage and commit documentation changes.

### 9. Run Final Reviews

If not already done:
1. Launch code-reviewer agent
2. Launch security-auditor agent
3. Block if CRITICAL issues

### 10. Merge to Develop

```bash
git checkout develop
git pull origin develop
git merge --no-ff feature/###-slug
git push origin develop
git branch -d feature/###-slug
```

### 11. Suggest Next Steps

```
Next actions:
1. Start next task: /implement project ### --full
2. View status: /project-status project
3. Merge to main (requires PR): gh pr create --base main --head develop
```

## Documentation Checklist

Before merge, verify:
1. **PLAN.md** - All phases checked off
2. **Linked SPEC** - Updated to reflect what was built
3. **architecture-overview.md** - Reflects changes
4. **ADRs** - New decisions documented
5. **CHANGELOG.md** - User-facing changes
6. **WORKLOG.md** - Final summary
7. **README.md** - Updated if API changed

## Workflow

```
/issue → /plan → /implement → /commit → /complete
                                            ↓
                                    Update docs + CHANGELOG
                                            ↓
                                    Run reviews
                                            ↓
                                    Merge to develop
```
