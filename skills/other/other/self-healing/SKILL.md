---
name: self-healing
description: "Self-healing codebase system. Monitors runtime errors, test failures, and build breaks. Automatically diagnoses root cause, generates fix, validates fix, and applies if safe. Zero human intervention for routine failures."
---

# Self-Healing Codebase

Automated fault detection and repair. When a test fails, a build breaks, or a runtime error is logged, the healing pipeline wakes up, finds the root cause, generates a minimal fix, validates it, and applies it -- all without human intervention, as long as confidence is above the safety threshold.

## Trigger Conditions

The healing pipeline activates on any of these events:

| Trigger | Signal | Source |
|---------|--------|--------|
| Test failure | Any test exits non-zero | CI logs, `npm test` output |
| Build break | Compiler/bundler error | CI logs, `npm run build` output |
| Runtime error | Unhandled exception, 5xx response | Application logs, Vercel logs |
| Type error | `tsc --noEmit` fails | Pre-commit hook, CI |
| Lint failure | ESLint/Prettier error blocking CI | CI logs |

### Signals NOT Handled

The following always require human review -- do NOT auto-heal:

- Security vulnerabilities (auth bypass, injection, XSS)
- Database migrations (schema changes, data loss risk)
- Dependency version conflicts (breaking API changes)
- Flaky tests (non-deterministic failures -- use `replay` agent instead)

## The 4-Phase Healing Pipeline

```
DETECT    ->    DIAGNOSE    ->    FIX    ->    VALIDATE
  |                |               |               |
Trigger        Root cause       Minimal         Re-run
fires          identified       patch           test suite
               confidence       applied         Pass? DONE
               scored           to branch       Fail? ROLLBACK
```

### Phase 1: Detect

Capture the full failure context:

```
- Error message (exact, not summarized)
- Stack trace (all frames, not truncated)
- File and line number of origin
- Recent git changes touching that file (last 3 commits)
- Environment (Node version, OS, CI vs local)
```

Pass all context to the Diagnose phase. Incomplete context = low confidence = no auto-fix.

### Phase 2: Diagnose

The `sleuth` agent performs root cause analysis:

1. Read the failing file at the reported line
2. Trace the call stack upward (max 3 frames)
3. Check if a recent git commit introduced the regression (`git log -5 -- <file>`)
4. Classify the failure type:

| Type | Examples | Confidence Boost |
|------|----------|-----------------|
| Regression | Line added in last commit causes error | +20% |
| Null reference | `Cannot read property X of undefined` | +10% |
| Import error | Module not found, wrong path | +15% |
| Type mismatch | TS type error at known location | +15% |
| Config error | Missing env var, wrong format | +10% |
| Logic error | Wrong condition, off-by-one | 0% (harder to auto-fix) |

**Confidence score** = base 50% + type bonus + evidence quality bonus (0-30%).

If final confidence < 80%: log the diagnosis, notify in `thoughts/HEALING.md`, stop. Do not attempt fix.

### Phase 3: Fix

The `spark` agent generates the minimal fix:

**Before touching any file:**
```bash
git stash push -u -m "self-healing: pre-fix stash for <error-id>"
```

Fix rules:
- Change the minimum number of lines necessary
- Do not refactor surrounding code
- Do not add features
- Do not change function signatures
- Add a comment: `// self-healing fix: <short reason>`

**Fix size limits:**
- Maximum 20 lines changed per fix
- Maximum 3 files touched per fix
- If fix requires more than this, confidence is forced to 0 -- escalate to human

### Phase 4: Validate

The `verifier` agent runs the relevant test suite:

```bash
# For test failures: run the specific failing test + its file's full suite
npm test -- --testPathPattern="<failing-file>"

# For build breaks: re-run the build
npm run build

# For type errors: re-run type check
npx tsc --noEmit

# For runtime errors: run integration tests if available
npm run test:integration
```

**Decision:**

```
Validation PASS:
  -> git stash drop (discard the safety stash)
  -> Commit the fix: "fix: self-healing repair for <error-id>"
  -> Log to thoughts/HEALING.md
  -> Update MTTR metric

Validation FAIL:
  -> git stash pop --index (restore pre-fix state exactly)
  -> Log failure to thoughts/HEALING.md
  -> Escalate to human with full diagnosis report
  -> Do NOT retry automatically (prevents loop)
```

## Safety Rules

1. **Confidence gate**: Never apply a fix when confidence < 80%
2. **Scope gate**: Never touch security code, DB migrations, or auth logic
3. **Size gate**: Never change more than 20 lines or 3 files in one heal
4. **No retry loop**: If validation fails, stop. Human takes over.
5. **Always stash**: Every fix attempt must be preceded by a git stash
6. **One fix per trigger**: One error = one heal attempt. If the error recurs after a successful fix, it is a different problem -- do not re-heal automatically.

## Agent Roles

| Agent | Phase | Responsibility |
|-------|-------|----------------|
| `sleuth` | Diagnose | Root cause analysis, confidence scoring |
| `spark` | Fix | Minimal patch generation |
| `verifier` | Validate | Test suite execution, pass/fail decision |
| `self-learner` | Post-heal | Record the pattern for future prevention |
| `coroner` | Post-heal | Check if the same bug exists elsewhere in the codebase |

## Healing Log Format

Append each healing event to `thoughts/HEALING.md`:

```markdown
## Healing Event: 2026-04-07T10:15:00Z

### Trigger
- Type: Test failure
- File: src/api/users.test.ts
- Error: "Cannot read properties of undefined (reading 'id')"
- Stack: users.test.ts:42 -> users.ts:87 -> db/query.ts:31

### Diagnosis (sleuth)
- Root cause: db/query.ts:31 returns `null` when no row found; callers assume non-null
- Regression: commit abc123 (2026-04-06) removed the null guard
- Classification: Null reference (confidence: +10%)
- Evidence: stack trace + git blame confirm exact line + recent commit
- Final confidence: 85%

### Fix (spark)
- File: src/api/users.ts line 87
- Change: Added null check before accessing .id
- Lines changed: 3
- Stash: self-healing-20260407-101500

### Validation (verifier)
- Command: npm test -- --testPathPattern="src/api/users"
- Result: PASS (14 tests, 0 failures)
- Decision: KEEP

### Outcome
- Status: HEALED
- Time to repair: 4 minutes
- MTTR contribution: recorded

---

## Healing Event: 2026-04-07T14:22:00Z

### Trigger
- Type: Build break
- Error: Module '"./config"' has no exported member 'DATABASE_URL'

### Diagnosis (sleuth)
- Root cause: config.ts was refactored, export renamed to DB_URL
- Confidence: 91%

### Fix (spark)
- File: src/api/db.ts line 3
- Change: import { DB_URL as DATABASE_URL } from './config'
- Lines changed: 1

### Validation (verifier)
- Command: npm run build
- Result: PASS

### Outcome
- Status: HEALED
- Time to repair: 2 minutes
```

## Metrics

Track in `thoughts/HEALING.md` header section (update after each event):

```markdown
# Self-Healing Metrics (updated: 2026-04-07)

| Metric | Value |
|--------|-------|
| Total healing events | 23 |
| Successful auto-fixes | 19 (82.6%) |
| Escalated to human | 4 (17.4%) |
| Average MTTR (auto-fixed) | 3.8 minutes |
| Average MTTR (escalated) | 47 minutes |
| Most common trigger | Test failure (61%) |
| Most common fix type | Null reference guard |
```

### Key Metrics Defined

- **MTTR** (Mean Time To Repair): Time from trigger detection to validation PASS
- **Auto-fix success rate**: Healed / (Healed + Escalated)
- **False fix rate**: Fixes that passed validation but broke something else (caught by post-deploy monitoring)

## Scope Limits (Non-Negotiable)

The healing pipeline will NEVER auto-fix:

```
- Files matching: **/auth/**, **/security/**, **/middleware/auth*
- Files matching: **/migrations/**, **/schema.*
- Environment variables or secrets
- Package versions in package.json / requirements.txt
- CI/CD configuration (.github/**, vercel.json, Dockerfile)
- Any file touched by a security-related commit message
```

If the failing code is in a scoped-out path, the pipeline logs the trigger and immediately escalates with the full diagnosis -- no fix attempt.

## Activation

This skill is referenced by:
- PostToolUse hooks when test/build commands exit non-zero
- The `sentinel` agent during incident response
- The `verifier` agent when a final validation fails

To invoke manually:

```
Use self-healing to diagnose and fix the failing test in src/api/users.test.ts.
Error: "Cannot read properties of undefined (reading 'id')"
Stack trace: [paste full trace]
```
