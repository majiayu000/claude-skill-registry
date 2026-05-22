---
name: doc-maintenance
description: |
  Automatic documentation updates after task completion. Use when:
  (1) completing tasks, (2) adding features, (3) fixing bugs,
  (4) refactoring code. Updates root PLAN.md (consolidated) and
  README.md when features change. Chains markdown-writer for style.
category: documentation
user-invocable: true
---

# Documentation Maintenance

Automatically updates project documentation after task completion.

## Consolidated Plan Location

All plan updates go to root `PLAN.md`. This is the single source of truth for project planning. Package-level PLAN.md files should be consolidated into the root PLAN.md.

## Trigger Conditions

Invoke after:
- Completing any task
- Adding a new feature
- Fixing a bug
- Refactoring code
- Resolving a blocked item

Also invoke explicitly with:
- `/doc-maintenance`
- "update documentation"
- "sync docs"

### Pre-Merge Cleanup

When owner says **"clean up before merge"** or similar, run this checklist:

```bash
# 1. Sync CLAUDE.md with installed skills (removes stale refs)
skills claudemd sync

# 2. Scan for test artifacts and slop
skills hygiene scan

# 3. If slop found, clean it
skills hygiene clean --confirm

# 4. Validate chain config (if chain files changed)
chain validate

# 5. Update PLAN.md with completed work
# (follow doc-maintenance procedure below)

# 6. Commit and push
git add -A && git commit -m "chore: pre-merge cleanup" && git push
```

This is the standard cleanup before any PR merge.

## Procedure

### Step 1: Read Current State

Read these files:
- `PLAN.md` (root, consolidated project plan)
- `README.md` (feature documentation)
- `packages/*/PLAN.md` (check for package-level plans to consolidate into root)
- Recent git commits (what changed)

### Step 2: Consolidate Package Plans

If `packages/*/PLAN.md` files exist, consolidate their content into root `PLAN.md`:

1. Each package gets a section: `## Package: {name}`
2. Move completed items to the Completed section
3. Move pending items to the appropriate sprint/backlog section
4. Delete the package-level PLAN.md after consolidation

Structure for root `PLAN.md`:
```markdown
# Project Plan

## Current Sprint
- Active work items across all packages

## Package: chain
- Package-specific in-progress work

## Package: cli
- Package-specific in-progress work

## Backlog
- Future work items

## Completed
- Timestamped completed items

## Blocked
- Items waiting on dependencies
```

### Step 3: Analyze Changes

Determine what was accomplished:
- Which PLAN.md items are now complete?
- Were new features added?
- Were bugs fixed?
- Did refactoring occur?
- Were new issues discovered?

### Step 4: Update PLAN.md

**Mark completed items:**
```markdown
## Current Sprint
- [x] Implement user authentication  # Was [ ]
- [ ] Add password reset flow
```

**Add discovered work:**
```markdown
## Backlog
- [ ] Discovered: Need rate limiting for auth endpoints
- [ ] Tech debt: Refactor auth middleware
```

**Move completed items with timestamp:**
```markdown
## Completed
- [x] Implement user authentication (2026-01-30)
```

**Update blocked items:**
```markdown
## Blocked
- Password reset: Waiting for email service setup
```

### Step 5: Update README.md (If Features Changed)

**When to update README.md:**
- New user-facing feature added
- API changed
- New command available
- Installation steps changed

**What to update:**
- Features list
- Usage examples
- API reference
- Installation instructions

### Step 6: Report Changes

Output a summary:

```
Documentation updated:

PLAN.md:
  - Marked complete: "Implement user authentication"
  - Added to backlog: "Need rate limiting for auth endpoints"
  - Moved to completed: 1 item
  - Consolidated from: packages/chain/PLAN.md

README.md:
  - Updated features list with authentication
  - Added auth usage example
```

## Skill Chaining

### With markdown-writer

All documentation updates MUST follow markdown-writer style:
- Short sentences, direct claims
- No em dashes
- Active voice
- Tables for structured data

Implicitly chain markdown-writer when editing any .md file.

### After TDD Completion

When TDD workflow completes (GREEN phase):
1. Mark the related PLAN.md task as complete
2. Add any discovered edge cases to backlog

### After Bug Fix

When a bug is fixed:
1. Mark bug item as complete in PLAN.md
2. Add regression test to PLAN.md if not present

### After Refactoring

When refactoring completes:
1. Mark refactoring task as complete
2. Update any affected API documentation

### Terminal Chain

After any documentation update: **repo-hygiene** (clean stale references)

## Update Patterns

### Marking Tasks Complete

**Before:**
```markdown
- [ ] Implement feature X
```

**After:**
```markdown
- [x] Implement feature X
```

### Adding Discovered Work

When you discover new tasks during implementation:

```markdown
## Backlog
- [ ] (discovered) New task from implementation
- [ ] (tech debt) Code that needs cleanup
- [ ] (bug) Issue found during testing
```

### Timestamping Completed Items

Add date to completed items:

```markdown
## Completed
- [x] Task description (2026-01-30)
```

### Feature Documentation

When adding a feature to README.md:

```markdown
## Features

- **Authentication**: Secure user login with JWT tokens
- **Password Reset**: Email-based password recovery
```

## Rationalizations (Do Not Skip)

| Rationalization | Why It's Wrong | Required Action |
|-----------------|----------------|-----------------|
| "Too small to document" | Small changes accumulate | Update PLAN.md |
| "I'll remember" | Context is lost between sessions | Write it down |
| "README is fine" | Feature docs get stale | Verify accuracy |
| "Just a bug fix" | Bugs deserve tracking | Mark complete |
| "Package has its own PLAN" | Fragmentation causes confusion | Consolidate to root PLAN.md |

## Example Session

**Task:** Add user authentication

**After completion:**

```
/doc-maintenance

Analyzing changes...

Found:
- New auth middleware in src/middleware/auth.ts
- New login endpoint in src/routes/auth.ts
- 5 new test files
- Git commit: "Add JWT authentication"
- packages/chain/PLAN.md exists (needs consolidation)

Updates:

PLAN.md:
  Current Sprint:
    - [x] Implement user authentication
  Backlog:
    + [ ] (discovered) Add refresh token support
    + [ ] (discovered) Rate limit login attempts
  Consolidated:
    - Merged packages/chain/PLAN.md content

README.md:
  Features:
    + Authentication: JWT-based user authentication
  Usage:
    + Added auth example code
```

## Notes

- All plan updates go to root `PLAN.md` (consolidated)
- Package-level PLAN.md files should be consolidated, not maintained separately
- Never removes items from PLAN.md (only marks complete)
- Preserves existing formatting
- Adds timestamps to completed items
- Creates backlog items for discovered work
- Only updates README.md when features change
- Always follows markdown-writer style
