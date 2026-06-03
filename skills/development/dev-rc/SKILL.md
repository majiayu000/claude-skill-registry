---
name: dev-rc
description: Release candidate preparation. Final checks before merge - QA, security, review, changelog. The last gate before shipping.
---

# Dev RC - Release Candidate

The final gate. QA passed? Security clean? Ready to ship.

## Philosophy

"A release candidate is a promise. Don't make promises you can't keep."

## Prerequisites

Before running /dev-rc, you should have:
- ✓ Code complete
- ✓ Tests passing (/dev-qa)
- ✓ Security audit clean (/dev-security)

If not done, we'll run them.

## Flow

### 1. Pre-flight Check

```bash
# Current state
git status
git log --oneline -5

# What's the diff from main?
git diff main...HEAD --stat
```

Show Tako:
```
Release Candidate Check

Branch: {branch}
Commits: {N} ahead of main
Files: {N} changed
Lines: +{added} -{removed}

Proceeding with RC checks...
```

### 2. Run QA (if not recent)

Check if QA was run in last hour:
- If yes: Skip, show previous results
- If no: Run /dev-qa quick

Must pass to continue.

### 3. Run Security (if not recent)

Check if security audit was run in last hour:
- If yes: Skip, show previous results
- If no: Run /dev-security quick

Must pass (CRITICAL/HIGH = 0) to continue.

### 4. Final Code Review

Delegate to Garry:
```
"Garry, final review before release.

This is going to main. Check:
1. All requirements met from the dev-cycle session
2. No debug code left behind
3. No TODO/FIXME that should block release
4. Documentation updated if needed
5. Breaking changes documented

Diff: {git diff main...HEAD}

Give me a go/no-go."
```

### 5. Changelog Entry

Ask Tako:
```
Generate changelog entry?

Based on commits:
{git log main...HEAD --oneline}

Options:
1. Yes, generate for me
2. Yes, I'll write it
3. Skip changelog
```

If generating:
```markdown
## [Unreleased]

### Added
- {new features from commits}

### Changed
- {modifications from commits}

### Fixed
- {bug fixes from commits}
```

### 6. RC Summary

```
## Release Candidate Summary

### Checks
- QA: ✓ PASSED
- Security: ✓ PASSED
- Review: ✓ APPROVED

### Changes
{git diff main...HEAD --stat summary}

### Commits
{git log main...HEAD --oneline}

### Changelog
{generated or provided entry}

---

RC Status: READY

Next steps:
1. /dev-finish - Commit, PR, close cycle
2. Manual review - Look at the diff yourself
3. Hold - Not ready yet
```

### 7. If Checks Fail

```
## Release Candidate: NOT READY

### Blockers
- QA: ✗ 2 test failures
- Security: ✓ Passed
- Review: ⚠ TODO found in src/auth.ts

### Required Actions
1. Fix test failures
2. Remove or address TODO

Run /dev-qa to fix tests, then /dev-rc again.
```

## Quick Mode

```
/dev-rc quick
```

Skip interactive prompts:
- Auto-run QA quick
- Auto-run security quick
- Auto-generate changelog
- Show summary only

## Integration

**With dev-cycle**: Final phase before finish
**With dev-qa**: Runs QA if needed
**With dev-security**: Runs security if needed
**With dev-finish**: Natural next step after RC passes

## RC Checklist

| Check | Tool | Blocker? |
|-------|------|----------|
| Tests pass | dev-qa | Yes |
| Lint clean | dev-qa | Yes |
| Build works | dev-qa | Yes |
| No critical vulns | dev-security | Yes |
| No high vulns | dev-security | Yes |
| Requirements met | Garry | Yes |
| No debug code | Garry | Yes |
| Docs updated | Garry | No |

## Agent Roles

- **Garry**: Final approval, completeness check
- **Bob**: Fixes any last-minute issues
- **Sentinel**: Security gate (via dev-security)
- **Arlo**: Data validation if applicable
