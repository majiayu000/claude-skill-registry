---
name: superspec:plan
description: |
  Use after specs are validated to create TDD implementation plan.
  Each Scenario in Specs becomes a test case in the plan.
  Combines bite-sized TDD tasks with spec references.
---

# Writing Implementation Plans

## Overview

Create implementation plans that:
1. Reference Specs for traceability
2. **ENFORCE TDD discipline (RED → GREEN → REFACTOR)** - This is MANDATORY
3. Are bite-sized (2-5 minutes per step)
4. Assume engineer has zero context

**Announce at start:** "I'm using the plan-writing skill to create the implementation plan."

## TDD Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Every task in the plan MUST follow this structure:
1. **Write test** - Based on Scenario
2. **Run test, CAPTURE OUTPUT** - Must show FAIL
3. **Implement minimal code**
4. **Run test, CAPTURE OUTPUT** - Must show PASS
5. **Commit with Spec reference**

The plan must include explicit `Run:` and `Expected:` lines to enforce this.

## Prerequisites

Before creating plan:
1. Proposal approved (`superspec/changes/[id]/proposal.md`)
2. Design documented (`superspec/changes/[id]/design.md`) - **Required**
3. Specs written and validated (`superspec/changes/[id]/specs/**/*.md`)
4. Run `superspec validate [id] --strict` passes

## The Spec-Plan Connection

```
Spec                                    Plan
═══════════════════════════════════════════════════════════════════════

### Requirement: 2FA Setup          →   ## Task 1: Implement 2FA Setup
                                        **Spec Reference:** 2FA Setup

#### Scenario: Generate QR code     →   ### Step 1.1: Write failing test (RED)
- WHEN user requests 2FA setup          test('generates QR code when 2FA setup requested')
- THEN generates TOTP secret            - WHEN: user.request2FASetup()
- AND displays QR code                  - THEN: expect(result.qrCode).toBeDefined()

                                    →   ### Step 1.2: Implement (GREEN)
                                        Minimal code to pass test

                                    →   ### Step 1.3: Commit
                                        Refs: Requirement: 2FA Setup, Scenario: Generate QR

═══════════════════════════════════════════════════════════════════════
```

## Plan Document Structure

Create: `superspec/changes/[change-id]/plan.md`

```markdown
# [Feature] Implementation Plan

> **For Claude:** REQUIRED SKILL: Use superspec:execute to implement this plan.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

**Related Specs:**
- `superspec/changes/[id]/specs/[capability-1]/spec.md`
- `superspec/changes/[id]/specs/[capability-2]/spec.md`

---

## Task 1: [Component/Feature Name]

**Spec Reference:** `### Requirement: [Name]`

**Files:**
- Create: `exact/path/to/new-file.ts`
- Modify: `exact/path/to/existing.ts:123-145`
- Test: `tests/exact/path/to/test.ts`

### Step 1.1: Write failing test (RED)

**Scenario:** `#### Scenario: [Name]`

```typescript
// WHEN [condition from Scenario]
// THEN [result from Scenario]
test('[Scenario Name]', async () => {
  // WHEN
  const result = await action(input);

  // THEN
  expect(result).toEqual(expected);
});
```

**Run:** `npm test -- --grep "[Scenario Name]"`
**Expected:** FAIL - "action is not defined" or similar

### Step 1.2: Implement minimal code (GREEN)

```typescript
export async function action(input: Input): Promise<Output> {
  // Minimal implementation to pass test
  return expected;
}
```

**Run:** `npm test -- --grep "[Scenario Name]"`
**Expected:** PASS

### Step 1.3: Refactor (if needed)

[Clean up code while keeping tests green]

### Step 1.4: Commit

```bash
git add tests/path/test.ts src/path/file.ts
git commit -m "feat([capability]): implement [scenario]

Refs: superspec/changes/[id]/specs/[capability]/spec.md
Requirement: [Name]
Scenario: [Name]"
```

---

## Task 2: [Next Component]

**Spec Reference:** `### Requirement: [Name]`

[Repeat structure...]
```

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**

| Step | Action |
|------|--------|
| Write test | Write ONE test for ONE Scenario |
| Run test | Verify it fails correctly |
| Implement | Write MINIMAL code to pass |
| Run test | Verify it passes |
| Commit | Commit with Spec reference |

**NOT bite-sized (too big):**
```markdown
- [ ] Implement 2FA system  ❌ Too vague
- [ ] Add all tests         ❌ Multiple tests
```

**Bite-sized (correct):**
```markdown
- [ ] Write test for Scenario: Generate QR code
- [ ] Run test, verify fails
- [ ] Implement generateQRCode()
- [ ] Run test, verify passes
- [ ] Commit
```

## Spec-to-Test Mapping

### One Scenario = One Test (minimum)

```markdown
#### Scenario: Valid login
- WHEN valid credentials
- THEN grants access
```

Becomes:

```typescript
test('Valid login - grants access when valid credentials', async () => {
  // WHEN valid credentials
  const result = await login({ email: 'valid@test.com', password: 'valid' });

  // THEN grants access
  expect(result.success).toBe(true);
  expect(result.token).toBeDefined();
});
```

### Complex Scenarios = Multiple Tests

```markdown
#### Scenario: Rate limiting
- WHEN 5 failed attempts
- THEN account locked
- AND notification sent
```

May become:

```typescript
test('Rate limiting - locks account after 5 failed attempts', async () => {
  // WHEN 5 failed attempts
  for (let i = 0; i < 5; i++) {
    await login({ email: 'user@test.com', password: 'wrong' });
  }

  // THEN account locked
  const status = await getAccountStatus('user@test.com');
  expect(status.locked).toBe(true);
});

test('Rate limiting - sends notification on lock', async () => {
  // Setup: trigger lock
  // ...

  // AND notification sent
  expect(mockNotify).toHaveBeenCalledWith(
    'user@test.com',
    'Account locked due to failed login attempts'
  );
});
```

## Task File Generation

Also create: `superspec/changes/[change-id]/tasks.md`

**IMPORTANT:** This file must be updated during execution! See `superspec:execute` skill.

```markdown
# Implementation Tasks for [Change ID]

## Status
- Total Tasks: X
- Completed: 0
- In Progress: 0
- Pending: X

**Last Updated:** YYYY-MM-DD HH:MM

---

## Phase 1: [Phase Name]

**Status:** PENDING | IN_PROGRESS | COMPLETE

- [ ] 1.1 Write test for Scenario: [name]
  - Spec: `### Requirement: X` → `#### Scenario: Y`
  - Completed: _(date when done)_
- [ ] 1.2 Implement [function/component]
  - Completed: _(date when done)_
- [ ] 1.3 Commit: feat([cap]): [description]
  - Completed: _(date when done)_

**Phase 1 Completed:** _(date when all tasks done)_

---

## Phase 2: [Next Phase]

**Status:** PENDING | IN_PROGRESS | COMPLETE

- [ ] 2.1 Write test for Scenario: [name]
  - Spec: `### Requirement: X` → `#### Scenario: Y`
- [ ] 2.2 Implement [function/component]
- [ ] 2.3 Commit

---

## Completion Tracking

| Phase | Tasks | Completed | Status |
|-------|-------|-----------|--------|
| Phase 1 | 3 | 0 | PENDING |
| Phase 2 | 3 | 0 | PENDING |
| **Total** | **6** | **0** | **0%** |
```

### Document Update Reminder

Add this reminder at the end of tasks.md:

```markdown
---

## IMPORTANT: Document Update Rules

After completing each task:
1. Mark task as `[x]` with completion date
2. Update Status counts at top
3. Update Phase status when all phase tasks done
4. Update Completion Tracking table

See `/superspec:execute` skill for details.
```

## Git Worktree Setup

Before implementation, set up isolated environment:

```bash
# Check for worktree directory
ls -la .worktrees/ 2>/dev/null || ls -la worktrees/ 2>/dev/null

# Create worktree
git worktree add .worktrees/[change-id] -b feature/[change-id]

# Navigate and verify
cd .worktrees/[change-id]
npm test  # or project-specific test command
```

## Complete Example

```markdown
# Two-Factor Authentication Implementation Plan

> **For Claude:** REQUIRED SKILL: Use superspec:execute to implement this plan.

**Goal:** Add TOTP-based 2FA to user authentication system

**Architecture:** TOTP library for code generation/verification, QR code for setup, encrypted secret storage

**Tech Stack:** otplib, qrcode, existing auth middleware

**Related Specs:**
- `superspec/changes/add-2fa/specs/two-factor-auth/spec.md`
- `superspec/changes/add-2fa/specs/user-auth/spec.md` (delta)

---

## Task 1: 2FA Setup - Generate QR Code

**Spec Reference:** `### Requirement: 2FA Setup`

**Files:**
- Create: `src/auth/totp.ts`
- Create: `src/api/routes/2fa.ts`
- Test: `tests/auth/totp.test.ts`

### Step 1.1: Write failing test (RED)

**Scenario:** `#### Scenario: Generate setup QR code`

```typescript
import { generate2FASetup } from '../src/auth/totp';

test('Generate setup QR code - returns QR and manual code', async () => {
  // WHEN user requests 2FA setup
  const result = await generate2FASetup('user-123');

  // THEN generates TOTP secret AND displays QR code AND manual code
  expect(result.secret).toBeDefined();
  expect(result.qrCodeDataUrl).toMatch(/^data:image\/png;base64/);
  expect(result.manualEntryCode).toMatch(/^[A-Z2-7]{32}$/);
});
```

**Run:** `npm test -- --grep "Generate setup QR code"`
**Expected:** FAIL - "generate2FASetup is not defined"

### Step 1.2: Implement minimal code (GREEN)

```typescript
// src/auth/totp.ts
import { authenticator } from 'otplib';
import QRCode from 'qrcode';

export interface TOTPSetup {
  secret: string;
  qrCodeDataUrl: string;
  manualEntryCode: string;
}

export async function generate2FASetup(userId: string): Promise<TOTPSetup> {
  const secret = authenticator.generateSecret();
  const otpauth = authenticator.keyuri(userId, 'MyApp', secret);
  const qrCodeDataUrl = await QRCode.toDataURL(otpauth);

  return {
    secret,
    qrCodeDataUrl,
    manualEntryCode: secret,
  };
}
```

**Run:** `npm test -- --grep "Generate setup QR code"`
**Expected:** PASS

### Step 1.3: Commit

```bash
git add src/auth/totp.ts tests/auth/totp.test.ts
git commit -m "feat(2fa): implement QR code generation for setup

Refs: superspec/changes/add-2fa/specs/two-factor-auth/spec.md
Requirement: 2FA Setup
Scenario: Generate setup QR code"
```

---

## Task 2: 2FA Setup - Verify Setup Code

**Spec Reference:** `### Requirement: 2FA Setup`

**Files:**
- Modify: `src/auth/totp.ts`
- Test: `tests/auth/totp.test.ts`

### Step 2.1: Write failing test (RED)

**Scenario:** `#### Scenario: Verify setup with valid code`

```typescript
test('Verify setup - enables 2FA when valid code provided', async () => {
  // Setup
  const setup = await generate2FASetup('user-123');
  const validCode = authenticator.generate(setup.secret);

  // WHEN user enters valid TOTP code during setup
  const result = await verify2FASetup('user-123', setup.secret, validCode);

  // THEN 2FA is enabled AND backup codes generated
  expect(result.enabled).toBe(true);
  expect(result.backupCodes).toHaveLength(10);
});
```

**Run:** `npm test -- --grep "Verify setup"`
**Expected:** FAIL - "verify2FASetup is not defined"

[Continue pattern...]
```

## Output

After creating plan and tasks:

**"Plan created:**
- `superspec/changes/[id]/plan.md` - Implementation plan
- `superspec/changes/[id]/tasks.md` - Task checklist

**Git Worktree:** Run `/superspec:git-worktree` to set up isolated environment

**Next step:** `/superspec:execute` - Execute plan with subagent-driven TDD"

## Execution Handoff

After saving plan, offer execution choice:

**"Two execution options:**

**1. Subagent-Driven (this session)**
- Fresh subagent per task
- Two-stage review (spec + quality)
- Fast iteration

**2. Parallel Session (separate)**
- Open new session in worktree
- Batch execution with checkpoints

**Which approach?"**

## Integration

### Required Skills

- **superspec:brainstorm** - Creates Specs that this plan references
- **superspec:execute** - Executes this plan with TDD enforcement
- **tdd** - Subagents use this during execution

### Execution Options

When plan is ready, user can choose:
- **subagent-development** - Fresh subagent per task with two-stage review (default)
- **executing-plans** - Batch execution with checkpoints (alternative)
- **dispatching-parallel-agents** - For 2+ independent tasks in parallel

### TDD Evidence Reminder

Add this reminder box at the end of every plan.md:

```markdown
---

## ⚠️ TDD Evidence Required

When executing this plan, implementers MUST:

1. **Show failing test output** before writing implementation
2. **Show passing test output** after implementation
3. **Provide evidence in report format:**

```
## TDD Evidence

### RED Phase
Test code: [show test]
Run output: [paste FAILING output]

### GREEN Phase
Implementation: [show code]
Run output: [paste PASSING output]
```

**No TDD evidence = implementation rejected. Code must be deleted and restarted.**
```
