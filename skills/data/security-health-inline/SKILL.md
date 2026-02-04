---
name: security-health-inline
description: Inline orchestration workflow for security vulnerability detection and remediation. Provides step-by-step phases for security-scanner detection, priority-based fixing with vulnerability-fixer, and verification cycles.
version: 2.0.0
---

# Security Health Check (Inline Orchestration)

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
     {
       "content": "Security scan",
       "status": "in_progress",
       "activeForm": "Scanning for vulnerabilities"
     },
     {
       "content": "Fix critical vulnerabilities",
       "status": "pending",
       "activeForm": "Fixing critical vulnerabilities"
     },
     {
       "content": "Fix high priority vulnerabilities",
       "status": "pending",
       "activeForm": "Fixing high vulnerabilities"
     },
     {
       "content": "Fix medium priority vulnerabilities",
       "status": "pending",
       "activeForm": "Fixing medium vulnerabilities"
     },
     {
       "content": "Fix low priority vulnerabilities",
       "status": "pending",
       "activeForm": "Fixing low vulnerabilities"
     },
     { "content": "Verification scan", "status": "pending", "activeForm": "Verifying fixes" }
   ]
   ```

---

## Phase 2: Detection

**Invoke security-scanner** via Task tool:

```
subagent_type: "security-scanner"
description: "Detect all vulnerabilities"
prompt: |
  Scan the entire codebase for security vulnerabilities:
  - SQL injection
  - XSS vulnerabilities
  - Authentication/authorization issues
  - RLS policy violations
  - Hardcoded secrets
  - Insecure dependencies
  - Categorize by priority (critical/high/medium/low)

  Generate: security-scan-report.md

  Return summary with vulnerability counts per priority.
```

**After security-scanner returns**:

1. Read `security-scan-report.md`
2. Parse vulnerability counts by priority
3. If zero vulnerabilities → skip to Final Summary
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

1. **Check if vulnerabilities exist** for this priority
   - If zero → skip to next priority

2. **Update TodoWrite**: mark current priority in_progress

3. **Invoke vulnerability-fixer** via Task tool:

   ```
   subagent_type: "vulnerability-fixer"
   description: "Fix {priority} vulnerabilities"
   prompt: |
     Read security-scan-report.md and fix all {priority} priority vulnerabilities.

     For each vulnerability:
     1. Backup file before editing
     2. Implement fix
     3. Log change to .tmp/current/changes/security-changes.json

     Generate/update: security-fixes-implemented.md

     Return: count of fixed vulnerabilities, count of failed fixes.
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

2. **Invoke security-scanner** (verification mode):

   ```
   subagent_type: "security-scanner"
   description: "Verification scan"
   prompt: |
     Re-scan codebase after fixes.
     Compare with previous security-scan-report.md.

     Report:
     - Vulnerabilities fixed (count)
     - Vulnerabilities remaining (count)
     - New vulnerabilities introduced (count)
   ```

3. **Decision**:
   - If vulnerabilities_remaining == 0 → Final Summary
   - If iteration < 3 AND vulnerabilities_remaining > 0 → Go to Phase 2
   - If iteration >= 3 → Final Summary with remaining vulnerabilities

---

## Phase 6: Final Summary

Generate summary for user:

```markdown
## Security Health Check Complete

**Iterations**: {count}/3
**Status**: {SUCCESS/PARTIAL}

### Results

- Found: {total} vulnerabilities
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

- Detection: `security-scan-report.md`
- Fixes: `security-fixes-implemented.md`
```

---

## Error Handling

**If quality gate fails**:

```
Rollback available: .tmp/current/changes/security-changes.json

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
