---
name: final-check
description: Final validation before task completion. Verifies all skills were consulted, documentation updated, tests pass. HAS VETO POWER - blocks incomplete tasks.
allowed-tools: Read, Grep, Glob, Bash
---

# Final Check - Final Validation System

## VETO POWER

> **WARNING:** This skill HAS VETO POWER.
> If rule violated, MUST:
>
> 1. STOP and list violations
> 2. REQUIRE fix before approving
> 3. Re-validate after fixes

---

## Purpose

This skill is the LAST check before task completion:

- **Validates** all CLAUDE.md rules
- **Verifies** all skills were consulted
- **Confirms** documentation was updated
- **Ensures** nothing was forgotten
- **Blocks** incomplete tasks

---

## Mega Validation Checklist

### 1. CODEBASE-KNOWLEDGE

- [ ] Affected domain consulted BEFORE implementing?
- [ ] Domain file UPDATED after implementing?
- [ ] Commit hash added?
- [ ] Connections verified?

### 2. DOCS-TRACKER

- [ ] Changes detected via git diff?
- [ ] New documentation created (if needed)?
- [ ] Existing documentation updated?
- [ ] Changelog updated?

### 3. TEST-COVERAGE

- [ ] New files have test or exemption?
- [ ] New tRPC routes have unit test?
- [ ] New pages have E2E spec?
- [ ] E2E uses `auth.helper.ts` correctly?
- [ ] No `.skip()` added?
- [ ] All tests pass?

### 4. UI-UX-AUDIT

- [ ] Competitors researched (if UI)?
- [ ] Accessibility validated?
- [ ] Responsiveness tested?
- [ ] Skeleton created (if new component)?
- [ ] Zero horizontal overflow?

### 5. SECURITY-SCAN

- [ ] User ID always from session?
- [ ] Sensitive data not sent to frontend?
- [ ] Zod validation on all routes?
- [ ] OWASP Top 10 verified?
- [ ] No pending VETO?

### 6. QUALITY-GATE

- [ ] `bun run typecheck` passes?
- [ ] `bun run lint` passes?
- [ ] `bun run test` passes?
- [ ] `bun run test:e2e` passes?
- [ ] `bun run build` passes?

---

## Checklist by Task Type

### New Feature

```markdown
### Before Implementation

- [ ] Consulted codebase-knowledge domain?
- [ ] Researched competitors (if UI)?

### During Implementation

- [ ] Followed code patterns?
- [ ] Created skeleton for components?
- [ ] Validated inputs with Zod?
- [ ] User ID always from session?

### After Implementation

- [ ] Created unit tests?
- [ ] Created E2E tests?
- [ ] Updated codebase-knowledge?
- [ ] Updated docs/flows (if applicable)?
- [ ] Ran full quality-gate?
- [ ] Security-scan approved?
```

### Bug Fix

```markdown
### Before

- [ ] Consulted affected domain?
- [ ] Identified root cause?

### During

- [ ] Fix is minimal and focused?
- [ ] Doesn't introduce regression?

### After

- [ ] Test covering the bug?
- [ ] Updated domain with commit?
- [ ] Quality-gate passes?
```

### Refactor

```markdown
### Before

- [ ] Consulted affected domains?
- [ ] Mapped all dependencies?

### During

- [ ] Maintained existing behavior?
- [ ] Didn't break tests?

### After

- [ ] All tests pass?
- [ ] Updated affected domains?
- [ ] Quality-gate passes?
```

---

## Validation Flow

```
TASK COMPLETE? (developer thinks done)
        ↓
1. VERIFY CODEBASE-KNOWLEDGE → Consulted? Updated?
        ↓
2. VERIFY DOCS-TRACKER → Docs updated? Changelog?
        ↓
3. VERIFY TEST-COVERAGE → All files have tests? Pass?
        ↓
4. VERIFY UI-UX-AUDIT (if UI) → Research? Accessibility?
        ↓
5. VERIFY SECURITY-SCAN → No VETO? OWASP OK?
        ↓
6. VERIFY QUALITY-GATE → All checks pass?
        ↓
    ┌─────────┴─────────┐
    ↓                   ↓
VIOLATION           ALL OK
→ VETO              → APPROVED
→ LIST ISSUES       → CAN COMMIT
```

---

## Output Format

### Approved

```markdown
## FINAL CHECK - APPROVED

### Task Summary

- **Type:** Feature
- **Domain:** [domain]
- **Files:** X modified

### Verifications

- [x] Codebase-Knowledge: Consulted and updated
- [x] Docs-Tracker: Changelog updated
- [x] Test-Coverage: Unit 3/3, E2E 2/2 pass
- [x] UI-UX-Audit: Competitors researched, accessible
- [x] Security-Scan: No vulnerabilities
- [x] Quality-Gate: All checks pass

**STATUS: APPROVED** - Ready to commit
```

### Vetoed

```markdown
## FINAL CHECK - VETOED

### Task Summary

- **Type:** Feature
- **Domain:** [domain]

### Violations Found

#### ❌ Codebase-Knowledge

- **Violation:** Domain NOT updated after implementation
- **Action:** Update domain file with commit hash

#### ❌ Test-Coverage

- **Violation:** New file without test
- **File:** `components/NewComponent.tsx`
- **Action:** Create E2E spec

**STATUS: VETOED** - 2 violations. Fix before commit.

### Next Steps

1. Update domain file
2. Create test for new component
3. Re-run final-check
```

---

## VETO Rules

### IMMEDIATE VETO

1. Security-scan found critical vulnerability
2. Quality-gate doesn't pass
3. Tests failing
4. Codebase-knowledge not updated

### VETO BEFORE MERGE

1. Docs not updated
2. Skeleton missing (if new component)
3. Changelog not updated

### WARNING (No veto)

1. Coverage below ideal (but critical tests exist)
2. Optional docs missing

---

## Quick Command

```bash
# Run full validation
bun run typecheck && bun run lint && bun run test && bun run test:e2e && bun run build

# If all pass, manually verify:
# - codebase-knowledge updated?
# - docs updated?
# - skeleton created?
```

---

## Critical Rules

1. **HAS VETO POWER** - Last barrier before commit
2. **VERIFIES EVERYTHING** - All skills, all rules
3. **NO EXCUSES** - Rule is rule
4. **DOCUMENTS VIOLATIONS** - For learning

---

## Version

- **v2.0.0** - Generic template
