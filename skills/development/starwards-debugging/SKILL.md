---
name: starwards-debugging
description: Systematic debugging for Starwards - four-phase framework (root cause investigation, pattern analysis, hypothesis testing, implementation) with Colyseus state inspection, Tweakpane debugging, multiplayer sync issues, and monorepo-specific troubleshooting
version: 2025-11-05
related_skills:
  - starwards-tdd (write test for bug before fixing)
  - starwards-verification (verify fix with full test suite)
  - starwards-monorepo (debug build dependencies)
  - starwards-colyseus (debug state sync issues)
  - starwards-ci-debugging (debug GitHub Actions failures)
  - using-superpowers (announce skill usage)
---

# Systematic Debugging for Starwards

## Overview

Random fixes waste time. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes.

**Starwards-specific:** Debug state sync issues, decorator problems, UI/server mismatches, and multiplayer race conditions.

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

**Any technical issue:**
- Test failures (Jest, Playwright)
- State sync problems (Colyseus)
- UI not updating (Tweakpane, React)
- Build failures (webpack, tsup, tsc)
- Decorator issues (@gameField, @range, @tweakable)
- Multiplayer race conditions

## The Four Phases

### Phase 1: Root Cause Investigation

**1. Read Error Messages Carefully**

**TypeScript errors:**
```bash
npm run test:types
# Read FULL error including file:line
# Check @gameField decorator order (must be last)
# Verify @range types match property type
```

**Jest test failures:**
```bash
npm test
# Read expected vs actual values
# Check if float precision issue (use toBeCloseTo)
# Verify async operations completed (await harness.waitForSync())
```

**Playwright failures:**
```bash
npm run test:e2e
# Check screenshot diffs in test-results/
# Verify data-id selectors match actual panel titles
# Check if timing issue (add proper waits, not arbitrary timeouts)
```

**Webpack errors:**
```bash
cd modules/browser && npm start
# Check browser console (F12) for actual error
# Webpack overlay shows [object Object] - this is a known issue
# Look for import/export mismatches
```

**2. Reproduce Consistently**

**For state sync issues:**
```typescript
// Add logging to both client and server
console.log('[CLIENT] Shield strength:', state.shield.strength);
console.log('[SERVER] Shield strength:', manager.state.shield.strength);

// Verify both show same value
// If different → state sync problem
// If same → UI rendering problem
```

**For multiplayer bugs:**
- Test with 1 client (works?)
- Test with 2 clients (breaks?)
- Test with concurrent actions (race condition?)

**3. Check Recent Changes**

```bash
git diff HEAD~1               # Last commit
git log --oneline -5          # Recent commits
git diff --stat origin/master # All changes on branch
```

**Common culprits:**
- @gameField decorator added/removed → rebuild core
- Schema change → restart server
- Widget change → clear browser cache
- Package update → npm ci && npm run build

**4. Gather Evidence in Multi-Component Systems**

**Starwards has 4 layers: Browser → WebSocket → Server → State**

Add diagnostic logging at each boundary:

```typescript
// Layer 1: Browser widget
console.log('[WIDGET] Sending command:', value);
room.send({type: '/Spaceship/ship-0/shield/power', value});

// Layer 2: Network (Chrome DevTools → Network → WS)
// Verify WebSocket message sent

// Layer 3: Server room
this.onMessage((client, message) => {
  console.log('[SERVER] Received:', message);
});

// Layer 4: State manager
console.log('[MANAGER] Shield power updated:', this.state.shield.power);
```

Run once to see WHERE it breaks:
- Widget logs but no WS message → room.send() issue
- WS message sent but server doesn't log → onMessage() not registered
- Server logs but state doesn't change → command handler bug

**5. Trace Data Flow**

**Example: Shield strength not updating**

Trace backward:
```
UI shows 500 ← Where does UI get value?
  ↓
pane.addBinding(shield, 'strength') ← What is shield?
  ↓
shield = ship.state.shield ← Does ship.state exist?
  ↓
ship.state from ShipDriver ← Is driver connected?
  ↓
driver.state from Colyseus room.state ← Is state synced?
```

Find the layer where data stops flowing correctly.

### Phase 2: Pattern Analysis

**1. Find Working Examples**

**For ship systems:**
```bash
# Look at existing systems
modules/core/src/ship/reactor.ts    # Has @gameField
modules/core/src/ship/armor.ts      # Has @range
modules/core/src/ship/warp.ts       # Has commands
```

**For widgets:**
```bash
# Look at working widgets
modules/browser/src/widgets/armor.ts       # Tweakpane panel
modules/browser/src/widgets/targeting.ts   # Command sending
```

**For tests:**
```bash
# Look at test patterns
modules/core/test/ship-test-harness.ts     # Multiplayer testing
modules/e2e/test/pilot-screen.spec.ts      # E2E testing
```

**2. Compare Against References**

Read docs COMPLETELY:
- `docs/PATTERNS.md` - Common patterns and gotchas
- `docs/TECHNICAL_REFERENCE.md` - @gameField, JSON Pointer, decorators
- `docs/testing/UTILITIES.md` - Test harness usage

**3. Identify Differences**

Use diff tools:
```bash
# Compare your new system to existing one
diff modules/core/src/ship/shield.ts modules/core/src/ship/armor.ts
```

Look for:
- Missing @gameField decorator
- Wrong decorator order (@gameField must be last)
- Missing MapSchema/ArraySchema for collections
- Type mismatches (float32 vs number)

**4. Understand Dependencies**

**For new ship systems:**
- Needs: @gameField decorator, added to ShipState, manager update loop
- Optional: Command handler, widget, E2E test

**For new widgets:**
- Needs: createPane() call, ship.state binding, registered in Dashboard
- Optional: data-id attribute for E2E tests

**For multiplayer features:**
- Needs: State sync via @gameField, command handler in room, client-side sending
- Optional: Typed command vs JSON Pointer

### Phase 3: Hypothesis and Testing

**1. Form Single Hypothesis**

**Good:**
- "Shield strength doesn't sync because @gameField decorator is missing"
- "Widget doesn't update because onChange listener not set up"
- "Test fails because float32 precision loss, need toBeCloseTo()"

**Bad:**
- "State sync issue" (too vague)
- "Something wrong with Colyseus" (blaming framework)
- "Might be a race condition" (guessing)

**2. Test Minimally**

**Example: Test @gameField hypothesis**

```typescript
// Before: (no decorator)
strength = 1000;

// After: (add decorator)
@gameField('float32') strength = 1000;

// Rebuild core, restart server, verify
```

ONE change at a time.

**3. Verify Before Continuing**

```bash
# Did it work?
npm test
npm run test:e2e

# If NO: Form NEW hypothesis
# If YES: Proceed to Phase 4
```

**4. When You Don't Know**

Say: "I don't understand why Colyseus state isn't syncing"

Don't say: "Let me try adding more decorators and see what happens"

Ask for help or research in:
- `docs/PATTERNS.md`
- Colyseus documentation
- Existing codebase examples

### Phase 4: Implementation

**1. Create Failing Test**

Use **starwards-tdd** skill to write proper test.

**For state sync bug:**
```typescript
test('shield strength syncs to client', async () => {
  const harness = new ShipTestHarness();
  await harness.connect();

  harness.shipManager.state.shield.strength = 750;
  await harness.waitForSync();

  expect(harness.shipDriver.state.shield.strength).toBe(750);

  await harness.cleanup();
});
```

**2. Implement Single Fix**

Address root cause only.

```typescript
// If root cause is: @gameField missing
@gameField('float32') strength = 1000;
```

NO "while I'm here" improvements.

**3. Verify Fix**

```bash
# Run the specific test
npm test -- shield-sync.spec.ts

# Run full suite
npm test
npm run test:e2e
npm run test:types
```

**4. If 3+ Fixes Failed**

**Pattern:**
- Each fix reveals new shared state issue
- "Need massive refactoring" for simple feature
- Fixes create new symptoms elsewhere

**STOP and question:**
- Is this architecture sound?
- Should we refactor instead of patching?
- Discuss with team before attempting fix #4

## Starwards-Specific Debugging Tools

### 1. Colyseus Monitor

```bash
# Access at http://localhost:2567/colyseus-monitor
# Login: admin / admin
# View: Active rooms, connected clients, state tree
```

**Use for:**
- Inspecting live state values
- Seeing connected clients
- Monitoring room creation/disposal

### 2. Chrome DevTools

**Network Tab → WS:**
- See WebSocket messages
- Verify commands sent
- Check state patches received

**Console:**
- Client-side errors
- Webpack HMR logs
- State change logging

**Sources:**
- Source maps enabled
- Breakpoints in TypeScript
- Step through React render

### 3. VSCode Debugger

**Terminal 3:**
```bash
# Instead of: node -r ts-node/register/transpile-only modules/server/src/dev.ts
# Use VSCode: F5 → "Run Server" (launches with debugger)
```

**Set breakpoints in:**
- `modules/server/src/ship/room.ts` - Command handlers
- `modules/core/src/ship/ship-manager.ts` - Update loops
- `modules/core/src/logic/space-manager.ts` - Physics

### 4. Tweakpane Debugging

Add temporary debug panel:

```typescript
const debugPane = createPane({title: 'DEBUG', container});

// Monitor live values
debugPane.addBinding(shield, 'strength', {readonly: true});
debugPane.addBinding(shield, 'power');
debugPane.addBinding(shield, 'effectiveness', {readonly: true});
```

### 5. Test Infrastructure

**ShipTestHarness:**
```typescript
const harness = new ShipTestHarness();
harness.shipManager.state // Server state
harness.shipDriver.state  // Client state
await harness.waitForSync(); // Wait for replication
```

**MultiClientDriver:**
```typescript
const driver = new MultiClientDriver();
await driver.start();
const [c1, c2] = await Promise.all([
  driver.joinShip('ship-1'),
  driver.joinShip('ship-1')
]);
// Test multiplayer scenarios
```

See `docs/testing/UTILITIES.md` for full API.

### 6. Logging Best Practices

```typescript
// GOOD: Scoped, structured
console.log('[ShieldManager.update] strength:', this.state.shield.strength, 'rate:', rechargeRate);

// BAD: Generic, unclear
console.log('shield', shield);
```

Use prefixes: `[CLIENT]`, `[SERVER]`, `[MANAGER]`, `[WIDGET]`

## Common Starwards Issues

| Symptom | Root Cause | Solution |
|---------|-----------|----------|
| State doesn't sync | Missing @gameField | Add decorator, rebuild core |
| Widget doesn't update | No onChange listener | Add state.onChange(() => update()) |
| Test fails with close values | Float32 precision | Use toBeCloseTo(expected, 1) |
| Angle values wrong | Not wrapped to [0, 360] | Use toPositiveDegreesDelta() |
| Effectiveness always 0 | System broken or no power | Check broken flag, power level |
| Webpack overlay shows [object Object] | Error wrapped by webpack | Check browser console (F12) |
| E2E test can't find panel | Wrong data-id | Use exact panel title in data-id |
| Build fails after core change | Core not rebuilt | npm run build:core or build:watch |
| Server doesn't see changes | Not restarted | Restart Terminal 3 (server) |

## Red Flags - STOP and Follow Process

- "Just try adding @gameField everywhere"
- "Let me restart everything and see if it works"
- "Probably a Colyseus bug"
- "I'll add setTimeout() to fix the race condition"
- Proposing fixes before checking browser console
- Blaming TypeScript strict mode
- "One more decorator tweak" (after 2+ failures)

## Integration with Other Skills

- **starwards-tdd** - Write failing test for bug before fixing
- **starwards-verification** - Verify fix with full test suite
- **starwards-monorepo** - Understand build dependencies
- **starwards-ci-debugging** - Debug GitHub Actions failures when tests pass locally but fail in CI

## Quick Debugging Checklist

```bash
# 1. Verify build is fresh
npm run build

# 2. Check types
npm run test:types

# 3. Run tests
npm test

# 4. Check browser console
# Open http://localhost:3000, press F12

# 5. Check server logs
# Look at Terminal 3 output

# 6. Check network
# Chrome DevTools → Network → WS

# 7. Check Colyseus monitor
# http://localhost:2567/colyseus-monitor
```

## Real-World Debugging Flow

**Example: "Shield widget shows wrong value"**

**Phase 1: Investigate**
1. Browser console: No errors ✓
2. Colyseus monitor: Server shows strength=800
3. Widget shows: 500
4. Hypothesis: State not syncing OR UI not updating

**Phase 2: Pattern**
1. Check working widget: armor.ts uses addBinding
2. My widget: Also uses addBinding
3. Difference: Armor has onChange listener, mine doesn't!

**Phase 3: Hypothesis**
"Widget doesn't update because Tweakpane binding isn't reactive to Colyseus state changes"

**Test minimally:**
```typescript
shield.state.onChange(() => {
  pane.refresh(); // Force Tweakpane update
});
```

**Phase 4: Implement**
1. Write E2E test that fails
2. Add onChange listener
3. Verify test passes
4. Verify manually in browser

Done!
