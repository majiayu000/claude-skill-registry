---
name: review-scope
description: Use before code review - determine if change is minor (review new code only) or major (review impacted code too)
allowed-tools:
  - Read
  - Grep
  - Glob
  - mcp__git__*
model: opus
---

# Review Scope

## Overview

Determine the appropriate scope for code review based on change size.

**Core principle:** Major changes need broader review. Minor changes need focused review.

**Question to answer:** Is this a minor change or a major change?

## Classification

### Minor Change

Review only NEW code.

**Indicators:**

| Indicator | Example |
|-----------|---------|
| Few files changed | 1-3 files |
| Isolated change | Single function modification |
| No API changes | Internal implementation only |
| No new dependencies | Uses existing code |
| Localized impact | Doesn't affect other modules |

**Examples:**
- Bug fix in single function
- Adding a field to existing model
- Small feature in existing module
- Updating constants/config
- Fixing typos

**Review scope:**
- Changed lines only
- New tests for changes
- Immediate function context

### Major Change

Review NEW code AND IMPACTED code.

**Indicators:**

| Indicator | Example |
|-----------|---------|
| Many files changed | 4+ files |
| Cross-cutting change | Touches multiple modules |
| API changes | Public interface modified |
| New dependencies | Adds libraries or modules |
| Behavioral changes | Affects existing functionality |
| Architecture impact | Changes patterns or structure |

**Examples:**
- New feature spanning multiple files
- Refactoring core module
- Changing authentication flow
- Adding new service layer
- Modifying database schema

**Review scope:**
- All changed code
- All code that calls changed code
- All code that changed code calls
- Integration points
- End-to-end flow

## Decision Flow

```
┌─────────────────────────────────────┐
│         FILES CHANGED               │
└─────────────────┬───────────────────┘
                  │
                  ▼
        ┌─────────────────┐
        │ > 3 files?      │
        └────────┬────────┘
                 │
       ┌─────────┴─────────┐
       │                   │
      Yes                  No
       │                   │
       ▼                   ▼
   MAJOR             ┌─────────────────┐
                     │ Public API      │
                     │ changed?        │
                     └────────┬────────┘
                              │
                     ┌────────┴────────┐
                     │                 │
                    Yes                No
                     │                 │
                     ▼                 ▼
                  MAJOR          ┌─────────────────┐
                                 │ Behavioral      │
                                 │ change?         │
                                 └────────┬────────┘
                                          │
                                 ┌────────┴────────┐
                                 │                 │
                                Yes                No
                                 │                 │
                                 ▼                 ▼
                              MAJOR             MINOR
```

## Finding Impacted Code

For major changes, identify impacted code:

### Find Callers

```bash
# Find all files that import the changed module
grep -r "import.*from.*'./changed-module'" src/

# Find all usages of changed function
grep -r "changedFunction" src/
```

### Find Dependencies

```bash
# What does the changed code import?
grep "import" src/changed-file.ts

# Trace the dependency chain
```

### Review Call Chain

```
Changed function
     │
     ├── Called by: parentFunction()  ← Review this
     │        │
     │        └── Called by: grandparent()  ← Review if behavior changed
     │
     └── Calls: childFunction()  ← Review if inputs changed
              │
              └── Calls: database.save()  ← Review if data shape changed
```

## Scope Documentation

Before starting review, document scope:

### Minor Change

```markdown
## Review Scope: MINOR

**Changed files:**
- src/utils/format.ts (10 lines)

**Review focus:**
- New formatDate() function
- Associated tests

**Not reviewing:**
- Callers of format module (unchanged behavior)
```

### Major Change

```markdown
## Review Scope: MAJOR

**Changed files:**
- src/services/auth.ts
- src/middleware/authenticate.ts
- src/routes/login.ts
- src/models/session.ts
- tests/auth.test.ts

**Impacted code to review:**
- src/routes/protected/* (use auth middleware)
- src/services/user.ts (calls auth service)

**Integration points:**
- Login flow end-to-end
- Session management
- Protected route access

**Review focus:**
- All changed code
- All callers of auth service
- Auth middleware consumers
- Session handling throughout
```

## Checklists by Scope

### Minor Change Review

- [ ] Changed lines reviewed
- [ ] New code meets all 7 criteria
- [ ] New tests exist
- [ ] Existing tests still pass
- [ ] No unintended side effects

### Major Change Review

All of minor, PLUS:

- [ ] All callers identified
- [ ] Caller behavior reviewed
- [ ] All callees identified
- [ ] Integration points reviewed
- [ ] End-to-end flow verified
- [ ] Impacted tests reviewed
- [ ] No regression in impacted areas

## Edge Cases

### When Uncertain

If unsure whether change is minor or major:

**Default to major.** Better to over-review than miss issues.

### Small Change with Large Impact

Sometimes few lines have large impact:

```typescript
// Small change, but MAJOR scope
// Changing default timeout affects all HTTP calls
const DEFAULT_TIMEOUT = 30000; // Was 5000
```

Review all code affected by the changed behavior.

### Large Refactor with No Behavior Change

Many files changed but pure refactor:

```typescript
// Renamed variable across 20 files
// No behavior change
```

Still MAJOR for structural review, but behavioral review is lighter.

## Integration

This skill is called by:
- `issue-driven-development` - Step 9
- `comprehensive-review` - Before starting review

This skill informs:
- How much code to review
- Which tests to examine
- What integration points to check
