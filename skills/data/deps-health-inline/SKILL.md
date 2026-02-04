---
name: deps-health-inline
description: Inline orchestration workflow for dependency audit and updates. Provides step-by-step phases for dependency-auditor detection, priority-based updates with dependency-updater, and verification cycles.
version: 2.0.0
---

# Dependency Health Check (Inline Orchestration)

You ARE the orchestrator. Execute this workflow directly without spawning a separate orchestrator agent.

## Workflow Overview

```
Audit → Validate → Update by Priority → Verify → Repeat if needed
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
   - Check lockfile exists (pnpm-lock.yaml, package-lock.json, yarn.lock)

3. **Initialize TodoWrite**:
   ```json
   [
     {
       "content": "Dependency audit",
       "status": "in_progress",
       "activeForm": "Auditing dependencies"
     },
     {
       "content": "Fix critical dependency issues",
       "status": "pending",
       "activeForm": "Fixing critical deps"
     },
     {
       "content": "Fix high priority dependency issues",
       "status": "pending",
       "activeForm": "Fixing high deps"
     },
     {
       "content": "Fix medium priority dependency issues",
       "status": "pending",
       "activeForm": "Fixing medium deps"
     },
     {
       "content": "Fix low priority dependency issues",
       "status": "pending",
       "activeForm": "Fixing low deps"
     },
     { "content": "Verification audit", "status": "pending", "activeForm": "Verifying updates" }
   ]
   ```

---

## Phase 2: Detection

**Invoke dependency-auditor** via Task tool:

```
subagent_type: "dependency-auditor"
description: "Audit all dependencies"
prompt: |
  Audit the entire codebase for dependency issues:
  - Security vulnerabilities (npm audit / pnpm audit)
  - Outdated packages (major/minor/patch)
  - Unused dependencies (via Knip)
  - Deprecated packages
  - License compliance issues
  - Categorize by priority (critical/high/medium/low)

  Generate: dependency-scan-report.md

  Return summary with issue counts per priority.
```

**After dependency-auditor returns**:

1. Read `dependency-scan-report.md`
2. Parse issue counts by priority
3. If zero issues → skip to Final Summary
4. Update TodoWrite: mark audit complete

---

## Phase 3: Quality Gate (Detection)

Run inline validation:

```bash
pnpm type-check
pnpm build
```

- If both pass → proceed to updates
- If fail → report to user, exit

---

## Phase 4: Update Loop

**For each priority** (critical → high → medium → low):

1. **Check if issues exist** for this priority
   - If zero → skip to next priority

2. **Update TodoWrite**: mark current priority in_progress

3. **Invoke dependency-updater** via Task tool:

   ```
   subagent_type: "dependency-updater"
   description: "Update {priority} dependencies"
   prompt: |
     Read dependency-scan-report.md and fix all {priority} priority issues.

     For each issue:
     1. Backup package.json and lockfile
     2. Update ONE dependency at a time
     3. Run type-check and build after each update
     4. If fails, rollback and skip
     5. Log change to .tmp/current/changes/deps-changes.json

     Generate/update: dependency-updates-implemented.md

     Return: count of updated deps, count of failed updates.
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

After all priorities updated:

1. **Update TodoWrite**: mark verification in_progress

2. **Invoke dependency-auditor** (verification mode):

   ```
   subagent_type: "dependency-auditor"
   description: "Verification audit"
   prompt: |
     Re-audit dependencies after updates.
     Compare with previous dependency-scan-report.md.

     Report:
     - Issues fixed (count)
     - Issues remaining (count)
     - New issues introduced (count)
   ```

3. **Decision**:
   - If issues_remaining == 0 → Final Summary
   - If iteration < 3 AND issues_remaining > 0 → Go to Phase 2
   - If iteration >= 3 → Final Summary with remaining issues

---

## Phase 6: Final Summary

Generate summary for user:

```markdown
## Dependency Health Check Complete

**Iterations**: {count}/3
**Status**: {SUCCESS/PARTIAL}

### Results

- Found: {total} dependency issues
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

- Audit: `dependency-scan-report.md`
- Updates: `dependency-updates-implemented.md`
```

---

## Error Handling

**If quality gate fails**:

```
Rollback available: .tmp/current/changes/deps-changes.json

To rollback:
1. Read changes log
2. Restore package.json and lockfile from .tmp/current/backups/
3. Run pnpm install
4. Re-run workflow
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
