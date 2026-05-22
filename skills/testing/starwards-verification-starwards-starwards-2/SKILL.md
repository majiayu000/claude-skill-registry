---
name: starwards-verification
description: Evidence-based completion verification for Starwards - run actual npm test commands, check E2E snapshots, verify TypeScript types, and confirm build success before claiming work is complete; evidence before assertions always
version: 2025-11-05
related_skills:
  - starwards-tdd (verification patterns for TDD)
  - starwards-debugging (verify fix worked)
  - starwards-monorepo (understand test commands)
  - starwards-ci-debugging (verify CI passes after push)
  - using-superpowers (announce skill usage)
---

# Verification Before Completion - Starwards

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** "Evidence before claims, always."

**Starwards-specific:** Run project commands, check all module tests, verify E2E snapshots.

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate Function

```
BEFORE claiming any status:

1. IDENTIFY: Which Starwards command proves this claim?
2. RUN: Execute the EXACT command (fresh, complete)
3. READ: Full output, exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## Starwards Verification Commands

### Unit & Integration Tests

```bash
# All tests (core, server, node-red)
npm test
# Expected: "Tests: X passed, X total" with 0 failures

# Specific module
npm test -- --projects=core
npm test -- --projects=server
# Expected: All tests in that module pass

# Specific file
npm test -- modules/core/test/shield.spec.ts
# Expected: All tests in file pass

# Specific test by name
npm test -- --testNamePattern="shield recharge"
# Expected: Matching tests pass

# Watch mode (during development)
npm test -- --watch
# Not for verification - use for dev only
```

**Verification pattern:**
```
✅ Correct:
[Run: npm test]
[Output shows: Tests: 215 passed, 215 total]
"All tests pass"

❌ Wrong:
"Tests should pass now"
"I fixed the bug, so tests will pass"
```

### E2E Tests

```bash
# All E2E tests
npm run test:e2e
# Expected: All tests pass, 0 failures

# Specific test file
npm run test:e2e -- ecr-screen.spec.ts
# Expected: All tests in file pass

# With visible browser (debugging only)
npm run test:e2e -- --headed
# Not for verification - use for debugging

# Update snapshots (after intentional visual changes)
npm run test:e2e -- --update-snapshots
# Then verify updated snapshots look correct
# Then commit new snapshots with changes
```

**Verification pattern:**
```
✅ Correct:
[Run: npm run test:e2e]
[Output shows: 18 passed (2.1m)]
[Check test-results/ - no failures]
"All E2E tests pass"

❌ Wrong:
"E2E tests probably pass, I only changed server code"
"Manual testing shows it works"
```

### Type Checking

```bash
# Full TypeScript type check
npm run test:types
# Expected: No errors, clean output

# Specific module (manual)
cd modules/core && npx tsc --noEmit
# Expected: No type errors
```

**Verification pattern:**
```
✅ Correct:
[Run: npm run test:types]
[Output shows no errors, exit code 0]
"TypeScript types are correct"

❌ Wrong:
"VSCode shows no red squiggles"
"Types should be fine"
```

### Code Formatting

```bash
# Check formatting (doesn't modify files)
npm run test:format
# Expected: No formatting errors

# Fix formatting (modifies files)
npm run lint:fix
# Expected: Files auto-formatted, then test:format passes

# Just Prettier
npm run prettier
# Expected: All files formatted correctly

# Just ESLint
npm run lint
# Expected: No linting errors
```

**Verification pattern:**
```
✅ Correct:
[Run: npm run test:format]
[Output: All files pass]
"Code formatting is correct"

❌ Wrong:
"I used Prettier plugin, so formatting is fine"
"Code looks formatted to me"
```

### Build

```bash
# Build all modules
npm run build
# Expected: All modules build successfully, no errors

# Build specific module
npm run build:core
npm run build:browser
npm run build:server
npm run build:node-red
# Expected: Module builds successfully

# Clean build (recommended)
npm run clean && npm run build
# Expected: Fresh build with no errors
```

**Verification pattern:**
```
✅ Correct:
[Run: npm run build]
[Output shows: core ✓, browser ✓, server ✓, node-red ✓]
[Exit code: 0]
"Build succeeds"

❌ Wrong:
"Linter passed, so build will work"
"Built successfully earlier"
```

### Complete Verification (Before PR/Commit)

```bash
# Full verification sequence
npm run clean          # Clear artifacts
npm ci                 # Fresh dependencies
npm run test:types     # TypeScript check
npm run test:format    # Formatting check
npm run build          # Build all modules
npm test               # Unit tests
npm run test:e2e       # E2E tests
```

**Verification pattern:**
```
✅ Correct:
[Run all 7 commands in sequence]
[All show success]
"All checks pass, ready to commit"

❌ Wrong:
"I ran tests yesterday, they passed"
"Only changed one file, don't need full verification"
```

## Module-Specific Verification

### After Changing Core Module

```bash
cd modules/core && npm run build:watch  # Should already be running
npm test -- --projects=core             # Core tests
npm test                                # All tests (server may depend on core)
```

**Why:** Server and other modules depend on core. Changes must not break dependents.

### After Changing Browser Module

```bash
npm run build:browser    # Rebuild browser
npm run test:e2e         # E2E tests verify UI
# Manual: Check http://localhost:3000 in browser
```

**Why:** Browser changes need visual verification.

### After Changing Server Module

```bash
npm run build:server     # Rebuild server
npm test -- --projects=server  # Server tests
# Restart Terminal 3 (API server)
npm run test:e2e         # E2E tests verify server behavior
```

**Why:** Server must be restarted to pick up changes.

## Common Verification Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| **Tests pass** | `npm test` output: 0 failures | Previous run, "should pass" |
| **E2E tests pass** | `npm run test:e2e` output: 0 failures | Manual browser testing |
| **Types correct** | `npm run test:types` clean | VSCode shows no errors |
| **Build succeeds** | `npm run build` exit 0 | Linter passing |
| **Formatting correct** | `npm run test:format` clean | Prettier plugin enabled |
| **Bug fixed** | Test for original bug passes | Code changed |
| **Regression test works** | Red-green cycle verified | Test passes once |
| **Ready to commit** | All 7 verification steps pass | Some tests passing |

## Red Flags - STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Done!")
- About to commit without running full verification
- Trusting VSCode error display instead of CLI
- Relying on partial verification ("just unit tests")
- "Tests passed yesterday"
- "Only changed CSS, don't need tests"
- "Build worked on my machine"

## Starwards-Specific Patterns

### Float Precision Verification

```typescript
// Claim: "Shield strength is 750"
test('shield strength matches expected', () => {
  expect(shield.strength).toBeCloseTo(750, 1); // ✅ Correct
  expect(shield.strength).toBe(750);            // ❌ Wrong (float32)
});
```

### Multiplayer Verification

```typescript
// Claim: "State syncs to all clients"
test('state syncs to multiple clients', async () => {
  const driver = new MultiClientDriver();
  await driver.start();

  const [c1, c2] = await Promise.all([
    driver.joinShip('ship-1'),
    driver.joinShip('ship-1')
  ]);

  driver.getShipManager('ship-1').state.shield.strength = 800;
  await driver.waitForSync();

  expect(c1.state.shield.strength).toBe(800);  // ✅ Both verified
  expect(c2.state.shield.strength).toBe(800);

  await driver.cleanup();
});
```

### E2E Visual Verification

```bash
# Claim: "UI displays shield strength correctly"
npm run test:e2e -- shield-widget.spec.ts
# ✅ Correct: Test passes, screenshot matches expected

# Check test-results/ for any failures
# Review updated snapshots if --update-snapshots used
```

## When To Apply

**ALWAYS before:**
- Committing changes (git commit)
- Creating PR (gh pr create)
- Marking task complete
- Claiming "bug fixed"
- Saying "tests pass"
- Moving to next feature

**Rule applies to:**
- Any success claim
- Any completion statement
- Any "done" or "finished" message
- Implications that work is complete

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "npm test worked earlier" | RUN it again, NOW |
| "Only changed comments" | Verify anyway |
| "VSCode shows no errors" | npm run test:types is source of truth |
| "Build worked locally" | Fresh build might fail |
| "E2E tests are slow" | That's not an excuse to skip them |
| "Manual testing showed it works" | Automated tests are required |
| "Tests flaky" | Fix flake, then verify |

## Integration with Other Skills

- **starwards-tdd** - Write tests BEFORE implementation
- **starwards-debugging** - Debug failures systematically
- **starwards-monorepo** - Understand module dependencies

## The Bottom Line

**"No shortcuts for verification."**

```bash
npm run test:types && \
npm run test:format && \
npm run build && \
npm test && \
npm run test:e2e
```

Run the commands. Read the output. THEN claim the result.

This is non-negotiable.
