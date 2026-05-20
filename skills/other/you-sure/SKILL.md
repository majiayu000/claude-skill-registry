---
name: you-sure
description: |
  Before ANY destructive, irreversible, or high-impact action, pause and surface
  a clear checklist of what's about to happen. This includes: file deletions,
  database changes, production deployments, mass updates, permission changes,
  or anything that can't easily be undone. Require explicit confirmation before
  proceeding. Never auto-execute dangerous operations.
allowed-tools: |
  bash: ls, cat, head, grep, find, git
  file: read
---

# You Sure?

<purpose>
Claude will happily rm -rf, drop tables, or deploy to production if asked.
This skill adds a mandatory pause before dangerous operations. The goal isn't
to be annoying - it's to make sure the user knows exactly what's about to
happen and has a chance to catch mistakes.
</purpose>

## Dangerous Operations

<triggers>
Always trigger sanity check before:

**File Operations:**
- `rm`, `rm -rf`, `rmdir`
- Overwriting existing files
- `mv` on important files
- Bulk file operations (wildcards)

**Database:**
- `DROP TABLE`, `DROP DATABASE`
- `DELETE FROM` without WHERE or with broad WHERE
- `TRUNCATE`
- Schema migrations on production
- `UPDATE` on multiple rows

**Git:**
- `git push --force`
- `git reset --hard`
- `git clean -fd`
- Pushing to main/master directly
- Deleting branches

**Deployment:**
- Deploying to production
- Changing environment variables in prod
- Scaling down services
- Modifying infrastructure

**Permissions/Security:**
- Changing file permissions (`chmod 777`)
- Modifying user roles
- API key rotation
- Firewall rule changes

**Bulk Operations:**
- Any loop that modifies/deletes
- Batch API calls that mutate
- Mass email sends
- Bulk user modifications
</triggers>

## Instructions

### Step 1: Detect Dangerous Operation

When you're about to execute something from the trigger list, STOP.

### Step 2: Surface The Checklist

```
You Sure?

You're about to:
  [ ] [Specific action 1]
  [ ] [Specific action 2]
  [ ] [Specific action 3]

Impact:
  - [What will change]
  - [What could break]
  - [Affected scope: N files/rows/users]

Reversibility:
  - [Can this be undone? How?]
  - [Backup available: Yes/No]

Environment: [dev/staging/prod]

Type 'go' to proceed, or 'abort' to cancel.
```

### Step 3: Wait For Explicit Confirmation

Do NOT proceed on:
- "sure"
- "yes"
- "okay"
- "do it"

Only proceed on:
- "go"
- "confirmed"
- "proceed"

This forces intentionality.

### Step 4: After Confirmation, Execute Carefully

- Execute one step at a time for multi-step operations
- Verify each step before proceeding to next
- Stop immediately if anything unexpected happens

## Severity Levels

<severity>
**CRITICAL** - Production data, irreversible:
```
CRITICAL - You Sure?

This affects PRODUCTION and cannot be easily undone.

You're about to:
  [ ] DROP TABLE users (48,293 records)

This will permanently delete all user data.

Backup status: [Check for recent backup]
Rollback: Not possible without backup restore

Are you absolutely sure? Type 'confirmed' to proceed.
```

**HIGH** - Destructive but recoverable:
```
HIGH - You Sure?

You're about to:
  [ ] rm -rf ./build/*

This will delete 847 files in the build directory.
Recoverable: Yes (can rebuild)

Type 'go' to proceed.
```

**MEDIUM** - Notable changes:
```
You Sure?

You're about to:
  [ ] git push --force origin feature-branch

This will rewrite history on the remote branch.
Others pulling this branch will need to reset.

Type 'go' to proceed.
```
</severity>

## Smart Detection

Don't be annoying on obviously safe operations:

**DO trigger:**
- `rm -rf /important/path`
- `DELETE FROM users`
- `git push -f origin main`

**DON'T trigger:**
- `rm temp_file.txt` (single temp file)
- `DELETE FROM users WHERE id = 1` (single row, specific)
- `git push origin feature-branch` (normal push)

Use judgment:
- Known test/temp files -> skip
- Production paths -> always trigger
- Broad operations -> trigger
- Narrow, specific operations -> skip unless destructive

## NEVER

- Auto-execute destructive operations without confirmation
- Accept vague confirmation ("sure", "yep")
- Proceed if user seems uncertain
- Skip sanity check because user is in a hurry
- Execute destructive operations in a loop without per-batch confirmation

## ALWAYS

- Show exactly what will happen (not vague descriptions)
- Show affected scope (number of files/rows/users)
- State whether it's reversible
- Require explicit confirmation word
- Offer to show preview/dry-run when available

## Examples

### Example 1: Database Delete

```
User: "Delete all inactive users"

You Sure?

You're about to:
  [ ] DELETE FROM users WHERE last_active < '2024-01-01'

Impact:
  - Removes 12,847 user accounts
  - Associated data (orders, preferences) may cascade delete
  - Affected scope: ~24% of user base

Reversibility:
  - NOT reversible without backup restore
  - Last backup: 2 hours ago

Want me to:
A) Show a preview first (SELECT COUNT)
B) Proceed with delete

Type 'go' to proceed, or 'preview' to check first.
```

### Example 2: Force Push

```
User: "Force push to main"

CRITICAL - You Sure?

You're about to:
  [ ] git push --force origin main

Impact:
  - Rewrites shared history on main branch
  - Anyone who pulled main will have conflicts
  - CI/CD pipelines may retrigger

Reversibility:
  - Technically reversible if you have the old SHA
  - Others' local copies will be out of sync

This is rarely the right choice for main branch.
Did you mean to push to a feature branch?

Type 'confirmed' to force push to main anyway.
```

### Example 3: Bulk File Delete

```
User: "Clean up all the log files"

You Sure?

You're about to:
  [ ] rm -rf ./logs/*.log

Impact:
  - Deletes 234 log files
  - Total size: 2.3GB
  - Oldest file: 2024-01-15

Reversibility:
  - NOT reversible
  - No backup configured for logs/

Type 'go' to proceed.
```

### Example 4: Safe Operation (No Trigger)

```
User: "Delete that temp file we made"

[No sanity check needed - single temp file, user knows about it]

Done. Deleted temp_output.json
```
