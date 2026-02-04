---
name: cleanup-health-inline
description: Inline orchestration workflow for dead code detection and removal. Provides step-by-step phases for dead-code-hunter detection, priority-based cleanup with dead-code-remover, and verification cycles.
version: 2.0.0
---

# Cleanup Health Check (Inline Orchestration)

You ARE the orchestrator. Execute this workflow directly without spawning a separate orchestrator agent.

## Workflow Overview

```
Detection → Validate → Remove by Priority → Verify → Repeat if needed
```

**Max iterations**: 3
**Priorities**: critical → high → medium → low

---

## Phase 1: Pre-flight

1. **Setup directories**:

   ```bash
   mkdir -p .tmp/current/{plans,changes,backups}
   ```

2. **Validate environment**:
   - Check `package.json` exists
   - Check `type-check` and `build` scripts exist

3. **Initialize TodoWrite**:
   ```json
   [
     {
       "content": "Dead code detection",
       "status": "in_progress",
       "activeForm": "Detecting dead code"
     },
     {
       "content": "Remove critical dead code",
       "status": "pending",
       "activeForm": "Removing critical dead code"
     },
     {
       "content": "Remove high priority dead code",
       "status": "pending",
       "activeForm": "Removing high dead code"
     },
     {
       "content": "Remove medium priority dead code",
       "status": "pending",
       "activeForm": "Removing medium dead code"
     },
     {
       "content": "Remove low priority dead code",
       "status": "pending",
       "activeForm": "Removing low dead code"
     },
     { "content": "Verification scan", "status": "pending", "activeForm": "Verifying cleanup" }
   ]
   ```

---

## Phase 2: Detection

**Invoke dead-code-hunter** via Task tool:

```
subagent_type: "dead-code-hunter"
description: "Detect all dead code"
prompt: |
  Scan the entire codebase for dead code:
  - Unused imports and exports
  - Commented out code blocks
  - Unreachable code
  - Debug statements (console.log, debugger)
  - Unused variables and functions
  - Unused dependencies
  - Categorize by priority (critical/high/medium/low)

  Generate: dead-code-report.md

  Return summary with dead code counts per priority.
```

**After dead-code-hunter returns**:

1. Read `dead-code-report.md`
2. Parse dead code counts by priority
3. If zero dead code → skip to Final Summary
4. Update TodoWrite: mark detection complete

---

## Phase 3: Quality Gate (Detection)

Run inline validation:

```bash
pnpm type-check
pnpm build
```

- If both pass → proceed to removal
- If fail → report to user, exit

---

## Phase 4: Removal Loop

**For each priority** (critical → high → medium → low):

1. **Check if dead code exists** for this priority
   - If zero → skip to next priority

2. **Update TodoWrite**: mark current priority in_progress

3. **Invoke dead-code-remover** via Task tool:

   ```
   subagent_type: "dead-code-remover"
   description: "Remove {priority} dead code"
   prompt: |
     Read dead-code-report.md and remove all {priority} priority dead code.

     For each item:
     1. Backup file before editing
     2. Remove dead code
     3. Log change to .tmp/current/changes/cleanup-changes.json

     Generate/update: dead-code-cleanup-summary.md

     Return: count of removed items, count of failed removals.
   ```

4. **Quality Gate** (inline):

   ```bash
   pnpm type-check
   pnpm build
   ```

   - If FAIL → report error, suggest rollback, exit
   - If PASS → continue

5. **Update TodoWrite**: mark priority complete

6. **Repeat** for next priority

---

## Phase 5: Verification

After all priorities cleaned:

1. **Update TodoWrite**: mark verification in_progress

2. **Invoke dead-code-hunter** (verification mode):

   ```
   subagent_type: "dead-code-hunter"
   description: "Verification scan"
   prompt: |
     Re-scan codebase after cleanup.
     Compare with previous dead-code-report.md.

     Report:
     - Dead code removed (count)
     - Dead code remaining (count)
     - New dead code introduced (count)
   ```

3. **Decision**:
   - If dead_code_remaining == 0 → Final Summary
   - If iteration < 3 AND dead_code_remaining > 0 → Go to Phase 2
   - If iteration >= 3 → Final Summary with remaining items

---

## Phase 6: Final Summary

Generate summary for user:

```markdown
## Cleanup Health Check Complete

**Iterations**: {count}/3
**Status**: {SUCCESS/PARTIAL}

### Results

- Found: {total} dead code items
- Removed: {removed} ({percentage}%)
- Remaining: {remaining}

### By Priority

- Critical: {removed}/{total}
- High: {removed}/{total}
- Medium: {removed}/{total}
- Low: {removed}/{total}

### Validation

- Type Check: {status}
- Build: {status}

### Artifacts

- Detection: `dead-code-report.md`
- Cleanup: `dead-code-cleanup-summary.md`
```

---

## Error Handling

**If quality gate fails**:

```
Rollback available: .tmp/current/changes/cleanup-changes.json

To rollback:
1. Read changes log
2. Restore files from .tmp/current/backups/
3. Re-run workflow
```

**If worker fails**:

- Report error to user
- Suggest manual intervention
- Exit workflow

---

## Key Differences from Old Approach

| Old (Orchestrator Agent)  | New (Inline Skill)     |
| ------------------------- | ---------------------- |
| 9+ orchestrator calls     | 0 orchestrator calls   |
| ~1400 lines (cmd + agent) | ~150 lines             |
| Context reload each call  | Single session context |
| Plan files for each phase | Direct execution       |
| ~10,000+ tokens overhead  | ~500 tokens            |

---

## Worker Prompts

See `references/worker-prompts.md` for detailed prompts.
