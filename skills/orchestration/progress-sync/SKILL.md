---
name: progress-sync
description: Comprehensive progress synchronization expert for multi-system sync (tasks.md → living docs → GitHub/JIRA/ADO). Use when syncing progress across systems, creating missing external issues, or understanding /sw:sync-progress command. AUTO-CREATES missing issues when external links are absent.
---

# Progress Sync Expert

I'm the comprehensive progress synchronization expert for SpecWeave. I help you understand and use the `/sw:sync-progress` command for end-to-end progress synchronization.

---

## ⚠️ CRITICAL: AUTO-CREATE IS MANDATORY

**When `/sw:sync-progress` is executed and no external issue exists, it MUST automatically create the issue using the Skill tool.**

The command MUST invoke:
- `Skill({ skill: "sw-github:create", args: "<increment-id>" })` for GitHub
- `Skill({ skill: "sw-jira:create", args: "<increment-id>" })` for JIRA
- `Skill({ skill: "sw-ado:create", args: "<increment-id>" })` for Azure DevOps

**DO NOT just report "No issues linked" - ACTUALLY CREATE THE ISSUE.**

---

## What is /sw:sync-progress?

**The TRUE "single button" to sync progress across all systems**:

```
tasks.md → spec.md ACs → living docs → AUTO-CREATE external issues → sync external tools (GitHub/JIRA/ADO)
```

**One command does EVERYTHING - including creating missing external issues!**
```bash
/sw:sync-progress
```

**No more "No GitHub issue linked" errors!** The command auto-creates missing issues.

### ✅ Archived Increment Behavior

**For archived/completed increments, this command ALWAYS creates issues for historical tracking:**

| Situation | Action |
|-----------|--------|
| Issue EXISTS | ✅ Sync final state + Close/Transition |
| NO issue linked | ✅ AUTO-CREATE + IMMEDIATELY CLOSE (historical tracking) |

**Why?** Historical tracking is important! Completed work should have external issues for:
- Team visibility
- Sprint retrospectives
- Release notes generation
- Audit trails

**For all increments (active or completed)**: Auto-creates issues if missing (the "single button" philosophy)

---

## When to Use This Command

### ✅ Use /sw:sync-progress when:

1. **First-time sync (no external issue yet)**: Just created increment, want to sync → auto-creates GitHub/JIRA/ADO issues!
2. **After completing tasks**: You've marked tasks as done in tasks.md and want to sync everywhere
3. **Before closing increment**: Final sync before `/sw:done` to ensure all systems in sync
4. **Progress check**: Want to update status line and external tools with latest progress
5. **After bulk task completion**: Completed multiple tasks, sync all at once
6. **Manual sync trigger**: Hooks didn't fire or you want to force a sync
7. **"No GitHub issue linked" error**: This command fixes that by auto-creating the issue!

### ❌ Don't use when:

1. **Only want to sync ACs**: Use `/sw:sync-acs` instead (faster, more targeted)
2. **Only want to sync docs**: Use `/sw:sync-specs` instead
3. **Only want to sync GitHub (issue already exists)**: Use `/sw-github:sync` instead
4. **Increment not started**: No tasks to sync yet
5. **Don't want auto-create**: Use `--no-create` flag or manual commands

---

## How It Works

**Multi-Phase Orchestration**:

```
Phase 1: Tasks → ACs (spec.md)
  └─ Reads completed tasks from tasks.md
  └─ Finds linked ACs (via "Satisfies ACs" field)
  └─ Marks ACs as complete in spec.md: [ ] → [x]
  └─ Updates metadata.json with AC count

Phase 2: Spec → Living Docs (User Stories)
  └─ Syncs spec.md to living docs structure
  └─ Updates user story completion status
  └─ Generates/updates feature ID if needed

Phase 3: AUTO-CREATE External Issues (NEW!)
  ├─ Checks each configured external tool for linked issues
  ├─ If no issue exists → AUTO-CREATE via /sw-github:create, /sw-jira:create, /sw-ado:create
  ├─ Respects permissions (canUpsertInternalItems, canUpdateExternalItems)
  └─ Skip with --no-create flag if needed

Phase 4: Sync to External Tools (Two-Way)
  ├─ GitHub: Two-way sync (push progress, pull team changes)
  ├─ JIRA: Two-way sync (push tasks, pull status)
  └─ Azure DevOps: Two-way sync (push comments, pull updates)

Phase 5: Status Line Cache
  └─ Updates status line with latest completion %
```

---

## Usage Examples

### Example 1: First-Time Sync (No GitHub Issue Yet) ⭐

**Scenario**: Just created increment, completed tasks, never created a GitHub issue. Want to sync.

```bash
# Single command does EVERYTHING
/sw:sync-progress
```

**What happens**:
1. ✅ Tasks → ACs marked complete in spec.md
2. ✅ User stories synced to living docs
3. ✅ **GitHub issue AUTO-CREATED** (#123)
4. ✅ GitHub issue synced with task progress
5. ✅ Status line shows completion %

**No more "No GitHub issue linked" errors!**

### Example 2: After Completing Tasks (Issue Exists)

**Scenario**: You completed 5 tasks and marked them in tasks.md. GitHub issue already exists.

```bash
# Single command syncs everything
/sw:sync-progress
```

**What happens**:
1. ✅ 5 tasks → 12 ACs marked complete in spec.md
2. ✅ 2 user stories marked complete in living docs
3. ✅ GitHub issue #123 detected, synced with progress
4. ✅ Epic issue checklist updated (5/37 tasks complete)
5. ✅ Status line shows 68% → 85% completion

### Example 3: Before Closing Increment

**Scenario**: All 37 tasks complete, ready to close. Ensure final sync.

```bash
# Final sync before closure
/sw:sync-progress 0053

# Then close increment
/sw:done 0053
```

**Why important**: `/sw:done` validates completion. Final sync ensures:
- All ACs marked complete
- All user stories synced
- All GitHub issues closed
- Status line shows 100%

### Example 4: Dry-Run (Preview Mode)

**Scenario**: Want to see what will be synced before executing.

```bash
# Preview mode
/sw:sync-progress 0053 --dry-run
```

**Output**:
```
🔍 DRY-RUN MODE (No changes made)

Would sync:
   • 37 completed tasks → 70 ACs in spec.md
   • spec.md → 6 user stories in living docs
   • Living docs → 6 GitHub issues (would close completed)
   • Status line cache (would update completion %)

Run without --dry-run to execute sync.
```

### Example 5: Local-Only Sync (No External Tools)

**Scenario**: Offline work, don't want to sync to GitHub/JIRA yet.

```bash
# Skip external tools
/sw:sync-progress 0053 --no-github --no-jira --no-ado
```

**What syncs**:
- ✅ Tasks → ACs (spec.md)
- ✅ Spec → Living docs
- ❌ External tools (skipped)
- ✅ Status line cache

---

## Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `--dry-run` | Preview without executing | `--dry-run` |
| `--no-create` | Skip auto-creation of missing issues | `--no-create` |
| `--no-github` | Skip GitHub sync | `--no-github` |
| `--no-jira` | Skip JIRA sync | `--no-jira` |
| `--no-ado` | Skip Azure DevOps sync | `--no-ado` |
| `--force` | Force sync even if validation fails | `--force` |

**Combine flags**:
```bash
# Full sync with auto-create (DEFAULT - just works!)
/sw:sync-progress

# Sync only, don't create missing issues
/sw:sync-progress 0053 --no-create

# Dry-run with no external tools
/sw:sync-progress --dry-run --no-github

# Force sync, skip GitHub
/sw:sync-progress --force --no-github
```

---

## Comparison with Other Sync Commands

| Command | Scope | Auto-Create? | When to Use |
|---------|-------|--------------|-------------|
| `/sw:sync-acs` | Tasks → ACs only | ❌ | Quick AC update |
| `/sw:sync-specs` | Spec → Docs only | ❌ | After spec changes |
| `/sw-github:create` | Create GitHub issue | ✅ | Manual issue creation |
| `/sw-github:sync` | Docs → GitHub only | ❌ | GitHub-only sync (issue must exist) |
| `/sw:sync-progress` | **Tasks → Docs → Create → Sync** | ✅ | **Complete sync** ✅ (RECOMMENDED!) |

**Rule of thumb**:
- Need **complete sync** (just works) → Use `/sw:sync-progress` ✅
- Need **targeted sync** → Use specific command (`sync-acs`, `sync-specs`)
- Need **sync only** (no auto-create) → Use `/sw:sync-progress --no-create`

---

## Auto-Detection

**Smart increment detection**:

```bash
# Explicit increment ID
/sw:sync-progress 0053

# Auto-detect from active increment
/sw:sync-progress
```

**How auto-detection works**:
1. Reads `.specweave/state/active-increment.json`
2. Finds first active increment ID
3. Uses that increment for sync

---

## External Tool Configuration

**Automatic detection of configured tools**:

The command checks `.specweave/config.json` for:
- GitHub: `"provider": "github"`
- JIRA: `"provider": "jira"`
- Azure DevOps: `"provider": "azure-devops"`

**Only configured tools are synced**:

```
✅ GitHub integration detected → Will sync
ℹ️  No JIRA integration → Skip
ℹ️  No ADO integration → Skip
```

---

## Error Handling

**Graceful degradation**:

| Error Type | Behavior | Impact |
|------------|----------|--------|
| AC sync fails | ❌ Abort sync | Critical - blocks all sync |
| Docs sync fails | ❌ Abort sync | Critical - blocks external sync |
| GitHub sync fails | ⚠️ Log warning, continue | Non-critical - docs still synced |
| JIRA sync fails | ⚠️ Log warning, continue | Non-critical - docs still synced |
| ADO sync fails | ⚠️ Log warning, continue | Non-critical - docs still synced |

**Philosophy**: Core sync (tasks → docs) must succeed. External tool sync is best-effort.

---

## Troubleshooting

### Issue: "No active increment found"

**Error**:
```
❌ No active increment found
```

**Fix**:
```bash
# Provide increment ID explicitly
/sw:sync-progress 0053
```

---

### Issue: "AC sync had warnings"

**Error**:
```
⚠️  AC sync had warnings: 5 ACs not found in spec.md
```

**Fix**:
```bash
# Embed ACs from living docs into spec.md
/sw:embed-acs 0053

# Then retry sync
/sw:sync-progress 0053
```

**Why this happens**: spec.md missing inline ACs (ADR-0064 requirement).

---

### Issue: "GitHub rate limit exceeded"

**Error**:
```
⚠️  GitHub sync had warnings: Rate limit exceeded
```

**Fix**: Non-critical. Docs are synced. Retry later when rate limit resets:

```bash
# Retry GitHub sync only (when rate limit resets)
/sw-github:sync 0053
```

---

## Integration with Workflow

**Typical increment workflow with progress sync**:

```bash
# 1. Plan increment
/sw:increment "Safe feature deletion"

# 2. Execute tasks
/sw:do

# [Complete tasks manually or via sub-agents...]

# 3. Sync progress after each batch of tasks
/sw:sync-progress

# 4. Final sync before closure
/sw:sync-progress 0053

# 5. Validate quality
/sw:validate 0053 --quality

# 6. Close increment
/sw:done 0053
```

---

## Best Practices

### ✅ DO:

1. **Sync after task batches**: Complete 3-5 tasks → sync → continue
2. **Final sync before closure**: Ensure 100% sync before `/sw:done`
3. **Use dry-run first**: Preview changes with `--dry-run`
4. **Check external tools**: Verify GitHub/JIRA after sync
5. **Review status line**: Ensure completion % updated correctly

### ❌ DON'T:

1. **Don't sync for every task**: Batching is more efficient
2. **Don't skip final sync**: Always sync before `/sw:done`
3. **Don't ignore warnings**: AC sync warnings indicate missing ACs
4. **Don't force sync without understanding**: `--force` bypasses validation
5. **Don't sync before tasks complete**: Sync when progress actually changed

---

## Architecture

**Why comprehensive sync is needed**:

```
Problem: Manual multi-step sync is error-prone
  1. Update spec.md ACs manually
  2. Run /sw:sync-specs
  3. Run /sw-github:sync
  4. Run /sw:update-status
  5. Check each system for correctness

Solution: Single command orchestrates all steps
  /sw:sync-progress → Does all 4 steps automatically
```

**Benefits**:
- ✅ **Single command**: One button for complete sync
- ✅ **Guaranteed consistency**: All systems synced together
- ✅ **Error resilience**: Non-critical failures don't block core sync
- ✅ **Audit trail**: Comprehensive report shows what synced
- ✅ **Dry-run support**: Preview before executing

---

## Background

Before this command, users had to manually:
1. Run `/sw:sync-acs`
2. Run `/sw:sync-specs`
3. Run `/sw-github:sync`
4. Run `/sw:update-status`

Now: **One command does all 4 steps** ✅

---

## Related Commands

- `/sw:sync-acs` - Sync tasks → ACs only
- `/sw:sync-specs` - Sync spec → living docs only
- `/sw:sync-tasks` - Sync external → tasks (bidirectional)
- `/sw-github:sync` - Sync docs → GitHub only
- `/sw-jira:sync` - Sync docs → JIRA only
- `/sw-ado:sync` - Sync docs → ADO only
- `/sw:update-status` - Update status line cache

---

**I'm here to help you sync progress efficiently across all systems!**

Ask me:
- "How do I sync progress to GitHub?"
- "What's the difference between sync-progress and sync-acs?"
- "How do I preview sync without executing?"
- "Why did my GitHub sync fail?"
- "When should I use --dry-run?"

## Project-Specific Learnings

**Before starting work, check for project-specific learnings:**

```bash
# Check if skill memory exists for this skill
cat .specweave/skill-memories/progress-sync.md 2>/dev/null || echo "No project learnings yet"
```

Project learnings are automatically captured by the reflection system when corrections or patterns are identified during development. These learnings help you understand project-specific conventions and past decisions.

