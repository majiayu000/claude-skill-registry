---
name: reuse-health-inline
description: Inline orchestration workflow for code duplication detection and consolidation. Provides step-by-step phases for reuse-hunter detection, priority-based consolidation with reuse-fixer, and verification cycles.
version: 2.0.0
---

# Code Reuse Health Check (Inline Orchestration)

You ARE the orchestrator. Execute this workflow directly without spawning a separate orchestrator agent.

## Workflow Overview

```
Detection → Validate → Consolidate by Priority → Verify → Repeat if needed
```

**Max iterations**: 3
**Priorities**: high → medium → low

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
       "content": "Duplication detection",
       "status": "in_progress",
       "activeForm": "Detecting duplications"
     },
     {
       "content": "Consolidate high priority duplications",
       "status": "pending",
       "activeForm": "Consolidating high priority"
     },
     {
       "content": "Consolidate medium priority duplications",
       "status": "pending",
       "activeForm": "Consolidating medium priority"
     },
     {
       "content": "Consolidate low priority duplications",
       "status": "pending",
       "activeForm": "Consolidating low priority"
     },
     {
       "content": "Verification scan",
       "status": "pending",
       "activeForm": "Verifying consolidation"
     }
   ]
   ```

---

## Phase 2: Detection

**Invoke reuse-hunter** via Task tool:

```
subagent_type: "reuse-hunter"
description: "Detect all code duplications"
prompt: |
  Scan the entire codebase for code duplications:
  - Duplicated TypeScript interfaces/types
  - Duplicated Zod schemas
  - Duplicated constants and configuration objects
  - Copy-pasted utility functions
  - Similar code patterns that should be abstracted
  - Categorize by priority (high/medium/low)

  Generate: reuse-hunting-report.md

  Return summary with duplication counts per priority.
```

**After reuse-hunter returns**:

1. Read `reuse-hunting-report.md`
2. Parse duplication counts by priority
3. If zero duplications → skip to Final Summary
4. Update TodoWrite: mark detection complete

---

## Phase 3: Quality Gate (Detection)

Run inline validation:

```bash
pnpm type-check
pnpm build
```

- If both pass → proceed to consolidation
- If fail → report to user, exit

---

## Phase 4: Consolidation Loop

**For each priority** (high → medium → low):

1. **Check if duplications exist** for this priority
   - If zero → skip to next priority

2. **Update TodoWrite**: mark current priority in_progress

3. **Invoke reuse-fixer** via Task tool:

   ```
   subagent_type: "reuse-fixer"
   description: "Consolidate {priority} duplications"
   prompt: |
     Read reuse-hunting-report.md and consolidate all {priority} priority duplications.

     For each duplication:
     1. Backup files before editing
     2. Determine canonical location (usually shared-types or shared package)
     3. Create/update canonical file with the type/schema/constant
     4. Replace duplicates with imports/re-exports
     5. Log change to .tmp/current/changes/reuse-changes.json

     Generate/update: reuse-consolidation-implemented.md

     Return: count of consolidated items, count of failed consolidations.
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

After all priorities consolidated:

1. **Update TodoWrite**: mark verification in_progress

2. **Invoke reuse-hunter** (verification mode):

   ```
   subagent_type: "reuse-hunter"
   description: "Verification scan"
   prompt: |
     Re-scan codebase after consolidation.
     Compare with previous reuse-hunting-report.md.

     Report:
     - Duplications resolved (count)
     - Duplications remaining (count)
     - New duplications introduced (count)
   ```

3. **Decision**:
   - If duplications_remaining == 0 → Final Summary
   - If iteration < 3 AND duplications_remaining > 0 → Go to Phase 2
   - If iteration >= 3 → Final Summary with remaining items

---

## Phase 6: Final Summary

Generate summary for user:

```markdown
## Code Reuse Health Check Complete

**Iterations**: {count}/3
**Status**: {SUCCESS/PARTIAL}

### Results

- Found: {total} duplications
- Consolidated: {consolidated} ({percentage}%)
- Remaining: {remaining}

### By Priority

- High: {consolidated}/{total}
- Medium: {consolidated}/{total}
- Low: {consolidated}/{total}

### Validation

- Type Check: {status}
- Build: {status}

### Artifacts

- Detection: `reuse-hunting-report.md`
- Consolidation: `reuse-consolidation-implemented.md`
```

---

## Error Handling

**If quality gate fails**:

```
Rollback available: .tmp/current/changes/reuse-changes.json

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

## Duplication Categories

**Types/Interfaces** (shared-types):

- Database types
- API types
- Zod schemas
- Common enums

**Constants** (shared-types):

- Configuration objects
- MIME types, file limits
- Feature flags

**Utilities** (shared package or re-export):

- Helper functions
- Validation utilities
- Formatters

**Single Source of Truth Pattern**:

1. Canonical location: `packages/shared-types/src/`
2. Other packages: `export * from '@package/shared-types/{module}'`
3. NEVER copy code between packages

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
