---
name: careful-delete
description: |
  Before any destructive or irreversible operation (rm -rf, DROP TABLE, DELETE,
  force push, branch deletion, truncate), orchestrate a safety cycle: assess
  blast radius → confirm explicitly → document what happened. Chains pre-mortem
  and you-sure with built-in documentation. No dangerous operation executes
  without ceremony.
allowed-tools: |
  bash: git, rm, drop, delete, truncate
  file: read
---

# Careful Delete

<purpose>
An elixir for dangerous operations. Destructive commands are irreversible - there's
no undo for `rm -rf`, no rollback for a force push to main. This chains risk
assessment → explicit confirmation → documentation, adding just enough friction
to prevent "oops" moments that ruin your day.
</purpose>

## Prerequisites

This elixir works best with these skills installed:

| Skill | Purpose | If Missing |
|-------|---------|------------|
| pre-mortem | Blast radius assessment | Falls back to built-in checklist |
| you-sure | Explicit confirmation gate | Falls back to built-in confirmation |
| retrospective | Document what happened | Skipped (optional) |

## When To Activate

<triggers>
**File operations:**
- `rm -rf`
- `rm -r` on directories
- Deleting multiple files
- Emptying directories

**Database operations:**
- `DROP TABLE`, `DROP DATABASE`
- `DELETE FROM` without WHERE (or with broad WHERE)
- `TRUNCATE`
- Schema migrations that drop columns/tables

**Git operations:**
- `git push --force` (especially to main/master)
- `git branch -D` (force delete)
- `git reset --hard`
- `git clean -fd`
- Deleting remote branches

**Cloud/Infrastructure:**
- Deleting cloud resources
- Terminating instances
- Removing DNS records
- Revoking credentials

**Keywords in user request:**
- "delete all", "remove everything", "wipe", "nuke"
- "force push", "hard reset"
- "drop the table", "truncate"
</triggers>

## Instructions

### Phase 1: Assess Blast Radius

<phase_blast_radius>
**If pre-mortem skill installed:** Invoke with focus on "what could go wrong."

**If not installed:**

```markdown
## Blast Radius Assessment

**What's being deleted:**
- [ ] Specific items: [list them]
- [ ] Estimated count: [number of files/rows/resources]
- [ ] Size/scope: [GB, row count, etc.]

**Affected systems:**
- [ ] Production data at risk?
- [ ] Other services depend on this?
- [ ] Users will be affected?
- [ ] Backups exist?

**Recovery options:**
- [ ] Can be restored from backup: [Yes/No, how long]
- [ ] Can be recreated: [Yes/No, effort required]
- [ ] Truly irreversible: [Yes/No]

**Risk level:** [Low / Medium / High / STOP]
```

**GATE:** Do not proceed if:
- Risk level is "STOP"
- Production data at risk AND no backup verified
- You can't list exactly what will be deleted
- Blast radius is unclear

If high risk: Suggest safer alternatives first.
</phase_blast_radius>

### Phase 2: Confirm Explicitly

<phase_confirm>
**If you-sure skill installed:** Invoke it now.

**If not installed:**

Present the confirmation checklist:

```markdown
## Confirmation Required

**You are about to:**
[Exact command or operation]

**This will delete:**
- [Item 1]
- [Item 2]
- [Item N]

**This action is:** [Reversible / Irreversible]

**Backup status:** [Verified / Not verified / No backup]

---

⚠️ Type the following to confirm:

"I confirm deletion of [specific thing] with [consequence]"

Example: "I confirm deletion of users table with loss of 50k records"
```

**GATE:** Do not proceed without:
- User typing the exact confirmation phrase
- NOT just "yes" or "confirm" or "do it"
- The confirmation must include WHAT is being deleted

If user tries to skip: Repeat the requirement. This gate exists for a reason.
</phase_confirm>

### Phase 3: Execute

<phase_execute>
**After confirmation received:**

1. Execute the exact command discussed (no modifications)
2. Capture the output
3. Note the timestamp

```markdown
## Execution Log

**Timestamp:** [ISO 8601]
**Command:** [exact command run]
**Output:**
```
[captured output]
```
**Status:** [Success / Failed / Partial]
```
</phase_execute>

### Phase 4: Document (Brief)

<phase_document>
**If retrospective skill installed:** Invoke for significant deletions.

**If not installed, capture minimally:**

```markdown
## Deletion Record

**Date:** [date]
**What was deleted:** [brief description]
**Why:** [reason]
**Deleted by:** [who requested]
**Recovery possible:** [Yes/No]
```

For routine deletions (temp files, test data): Skip this phase.
For significant deletions (production data, important branches): Always document.
</phase_document>

## Output Format

```markdown
## Careful Delete: [Brief description]

### Blast Radius
- Deleting: [what]
- Count: [how many]
- Reversible: [Yes/No]
- Backup: [status]

### Confirmation
User confirmed: "[their confirmation phrase]"

### Execution
- Command: `[command]`
- Timestamp: [time]
- Result: [success/failure]

### Record
[Brief note if significant deletion]
```

## NEVER

- Execute destructive commands without explicit confirmation
- Accept "yes" or "do it" as confirmation (require specific phrase)
- Proceed when blast radius is unclear
- Skip confirmation because "it's just test data" (verify first)
- Run broader deletion than what was confirmed
- Assume backups exist without verification

## ALWAYS

- List exactly what will be deleted before asking for confirmation
- Require confirmation phrase that includes the specific thing being deleted
- Verify backup status for important data
- Capture execution output
- Suggest safer alternatives when risk is high

## Example

**User:** "Delete the old user sessions table, we migrated to Redis"

**Phase 1 - Blast Radius:**
> Blast Radius Assessment:
>
> **What's being deleted:**
> - Table: `user_sessions`
> - Estimated rows: 2.3 million
> - Size: ~400MB
>
> **Affected systems:**
> - [x] Production data - but confirmed migrated to Redis
> - [ ] Other services depend on this - checked, none reference it
> - [ ] Users affected - no, sessions now in Redis
> - [x] Backups exist - daily backup from 6 hours ago
>
> **Recovery:** Can restore from backup within 30 minutes if needed
>
> **Risk level:** Medium (production table, but verified unused)

**Phase 2 - Confirm:**
> You are about to run:
> ```sql
> DROP TABLE user_sessions;
> ```
>
> This will permanently delete:
> - 2.3 million session records
> - 400MB of data
>
> This action is: **Irreversible** (but restorable from backup)
>
> ⚠️ Type to confirm:
> "I confirm deletion of user_sessions table with 2.3M records"

**User:** "I confirm deletion of user_sessions table with 2.3M records"

**Phase 3 - Execute:**
> Execution Log:
> - Timestamp: 2024-01-15T14:32:00Z
> - Command: `DROP TABLE user_sessions;`
> - Output: `Query OK, 0 rows affected (0.45 sec)`
> - Status: Success

**Phase 4 - Document:**
> Deletion Record:
> - Table `user_sessions` dropped
> - 2.3M records removed
> - Reason: Migrated to Redis, table no longer used
> - Backup available: daily_backup_20240115
