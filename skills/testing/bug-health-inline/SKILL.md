---
name: bug-health-inline
description: Inline orchestration workflow for automated bug detection and fixing. Provides step-by-step phases for bug-hunter detection, priority-based fixing with bug-fixer, and verification cycles.
version: 2.0.0
---

# Bug Health Check (Inline Orchestration)

You ARE the orchestrator. Execute this workflow directly without spawning a separate orchestrator agent.

## Workflow Overview

```
Detection → Validate → Fix by Priority → Verify → Repeat if needed
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
     { "content": "Bug detection", "status": "in_progress", "activeForm": "Detecting bugs" },
     { "content": "Fix critical bugs", "status": "pending", "activeForm": "Fixing critical bugs" },
     { "content": "Fix high priority bugs", "status": "pending", "activeForm": "Fixing high bugs" },
     {
       "content": "Fix medium priority bugs",
       "status": "pending",
       "activeForm": "Fixing medium bugs"
     },
     { "content": "Fix low priority bugs", "status": "pending", "activeForm": "Fixing low bugs" },
     { "content": "Verification scan", "status": "pending", "activeForm": "Verifying fixes" }
   ]
   ```

---

## Phase 2: Detection

**Invoke bug-hunter** via Task tool:

```
subagent_type: "bug-hunter"
description: "Detect all bugs"
prompt: |
  Scan the entire codebase for bugs:
  - Run type-check and build
  - Check for security vulnerabilities
  - Find dead code and debug statements
  - Categorize by priority (critical/high/medium/low)

  Generate: bug-hunting-report.md

  Return summary with bug counts per priority.
```

**After bug-hunter returns**:

1. Read `bug-hunting-report.md`
2. Parse bug counts by priority
3. If zero bugs → skip to Final Summary
4. Update TodoWrite: mark detection complete

---

## Phase 3: Quality Gate (Detection)

Run inline validation:

```bash
pnpm type-check
pnpm build
```

- If both pass → proceed to fixing
- If fail → report to user, exit

---

## Phase 4: Fixing Loop

**For each priority** (critical → high → medium → low):

1. **Check if bugs exist** for this priority
   - If zero → skip to next priority

2. **Update TodoWrite**: mark current priority in_progress

3. **Invoke bug-fixer** via Task tool:

   ```
   subagent_type: "bug-fixer"
   description: "Fix {priority} bugs"
   prompt: |
     Read bug-hunting-report.md and fix all {priority} priority bugs.

     For each bug:
     1. Backup file before editing
     2. Implement fix
     3. Log change to .tmp/current/changes/bug-changes.json

     Generate/update: bug-fixes-implemented.md

     Return: count of fixed bugs, count of failed fixes.
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

After all priorities fixed:

1. **Update TodoWrite**: mark verification in_progress

2. **Invoke bug-hunter** (verification mode):

   ```
   subagent_type: "bug-hunter"
   description: "Verification scan"
   prompt: |
     Re-scan codebase after fixes.
     Compare with previous bug-hunting-report.md.

     Report:
     - Bugs fixed (count)
     - Bugs remaining (count)
     - New bugs introduced (count)
   ```

3. **Decision**:
   - If bugs_remaining == 0 → Final Summary
   - If iteration < 3 AND bugs_remaining > 0 → Go to Phase 2
   - If iteration >= 3 → Final Summary with remaining bugs

---

## Phase 6: Final Summary

Generate summary for user:

```markdown
## Bug Health Check Complete

**Iterations**: {count}/3
**Status**: {SUCCESS/PARTIAL}

### Results

- Found: {total} bugs
- Fixed: {fixed} ({percentage}%)
- Remaining: {remaining}

### By Priority

- Critical: {fixed}/{total}
- High: {fixed}/{total}
- Medium: {fixed}/{total}
- Low: {fixed}/{total}

### Validation

- Type Check: {status}
- Build: {status}

### Artifacts

- Detection: `bug-hunting-report.md`
- Fixes: `bug-fixes-implemented.md`
```

---

## Error Handling

**If quality gate fails**:

```
Rollback available: .tmp/current/changes/bug-changes.json

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
