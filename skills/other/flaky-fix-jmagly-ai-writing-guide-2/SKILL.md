---
name: flaky-fix
description: Suggest and apply fixes for flaky tests based on detected patterns. Use after flaky-detect identifies unreliable tests that need repair.
version: 1.0.0
---

# Flaky Fix Skill

## Purpose

Analyze flaky test patterns and suggest or auto-apply fixes. Based on FlakyFix research showing LLMs can automatically repair flaky tests with targeted prompts.

## Research Foundation

| Finding | Source | Reference |
|---------|--------|-----------|
| LLM Auto-repair | FlakyFix (2023) | [arXiv:2307.00012](https://arxiv.org/html/2307.00012v4) - 70%+ success rate |
| Flaky Taxonomy | Google (2016) | [Flaky Tests Study](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html) |
| Pattern-based Fixes | FlaKat (2024) | [arXiv:2403.01003](https://arxiv.org/abs/2403.01003) |

## When This Skill Applies

- After `flaky-detect` identifies flaky tests
- User asks to "fix flaky test" or "make test reliable"
- CI is failing intermittently on specific tests
- Test marked as flaky needs repair

## Trigger Phrases

| Natural Language | Action |
|------------------|--------|
| "Fix this flaky test" | Analyze and suggest fix |
| "Make this test reliable" | Apply deterministic patterns |
| "Why is this test flaky?" | Root cause analysis + fix |
| "Auto-fix flaky tests" | Batch fix safe patterns |
| "Remove timing dependency" | Specific timing fix |

## Fix Patterns by Category

### 1. Timing Issues (45% of flaky tests)

#### Problem: Uses Real Time
```typescript
// FLAKY: Time-dependent
it('should expire after 1 hour', () => {
  const token = createToken();
  expect(token.expiresAt).toBeGreaterThan(Date.now());
});
```

#### Fix: Mock Time
```typescript
// FIXED: Mocked time
it('should expire after 1 hour', () => {
  const fixedTime = new Date('2024-01-01T00:00:00Z');
  vi.setSystemTime(fixedTime);

  const token = createToken();

  expect(token.expiresAt).toBe(fixedTime.getTime() + 3600000);
  vi.useRealTimers();
});
```

#### Problem: Explicit Sleep/Delay
```typescript
// FLAKY: Arbitrary delay
it('should complete async operation', async () => {
  startAsyncOperation();
  await sleep(100);  // Race condition!
  expect(result).toBeDefined();
});
```

#### Fix: Proper Async Handling
```typescript
// FIXED: Wait for actual completion
it('should complete async operation', async () => {
  const result = await startAsyncOperation();
  expect(result).toBeDefined();
});

// Or use waitFor for DOM
it('should show loading state', async () => {
  render(<Component />);
  await waitFor(() => {
    expect(screen.getByText('Loaded')).toBeInTheDocument();
  });
});
```

### 2. Async Issues (25% of flaky tests)

#### Problem: Missing Await
```typescript
// FLAKY: Promise not awaited
it('should fetch data', () => {
  const promise = fetchData();
  promise.then(data => {
    expect(data).toBeDefined();  // May not run before test ends
  });
});
```

#### Fix: Proper Async/Await
```typescript
// FIXED: Awaited promise
it('should fetch data', async () => {
  const data = await fetchData();
  expect(data).toBeDefined();
});
```

#### Problem: Race Condition
```typescript
// FLAKY: Order not guaranteed
it('should process items', async () => {
  const results = [];
  items.forEach(async item => {
    results.push(await process(item));
  });
  expect(results.length).toBe(3);  // Race!
});
```

#### Fix: Sequential or Parallel Await
```typescript
// FIXED: Guaranteed order
it('should process items', async () => {
  const results = await Promise.all(
    items.map(item => process(item))
  );
  expect(results.length).toBe(3);
});
```

### 3. Test Order Dependencies (20% of flaky tests)

#### Problem: Shared State
```typescript
// FLAKY: Shared state between tests
let counter = 0;

it('should increment', () => {
  counter++;
  expect(counter).toBe(1);  // Fails if other test runs first
});
```

#### Fix: Test Isolation
```typescript
// FIXED: Isolated state
describe('counter', () => {
  let counter;

  beforeEach(() => {
    counter = 0;  // Fresh state each test
  });

  it('should increment', () => {
    counter++;
    expect(counter).toBe(1);
  });
});
```

### 4. Non-deterministic Values (10% of flaky tests)

#### Problem: Random/UUID Values
```typescript
// FLAKY: Random ID
it('should create user with ID', () => {
  const user = createUser();
  expect(user.id).toBe('expected-id');  // Random!
});
```

#### Fix: Mock Random Generation
```typescript
// FIXED: Deterministic ID
it('should create user with ID', () => {
  vi.mock('uuid', () => ({
    v4: () => 'test-uuid-1234'
  }));

  const user = createUser();
  expect(user.id).toBe('test-uuid-1234');
});
```

### 5. Environment Dependencies (15% of flaky tests)

#### Problem: Network Calls
```typescript
// FLAKY: Real network
it('should fetch from API', async () => {
  const data = await fetch('https://api.example.com/data');
  expect(data).toBeDefined();  // Network failures!
});
```

#### Fix: Mock Network
```typescript
// FIXED: Mocked network
it('should fetch from API', async () => {
  vi.mock('node-fetch', () => ({
    default: vi.fn().mockResolvedValue({
      json: () => ({ success: true })
    })
  }));

  const data = await fetchFromApi();
  expect(data.success).toBe(true);
});
```

## Auto-Fix Rules

### Safe to Auto-Fix (Apply Automatically)

| Pattern | Detection | Fix |
|---------|-----------|-----|
| `Date.now()` in assertion | Regex | Wrap with `vi.setSystemTime()` |
| Missing `await` on async | AST analysis | Add `await` keyword |
| `setTimeout` in test | Regex | Replace with `vi.advanceTimersByTime()` |
| `Math.random()` | Regex | Mock with deterministic value |

### Requires Review (Suggest Only)

| Pattern | Why Review Needed |
|---------|-------------------|
| Shared test state | May require architectural changes |
| Database fixtures | Needs isolation strategy |
| External service calls | Mock design decision |
| Complex async flows | Multiple fix approaches |

## Output Format

```markdown
## Flaky Test Fix Report

### Test: `test/api/login.test.ts:45`

**Root Cause**: Timing - uses `Date.now()` in assertion
**Confidence**: HIGH (pattern match)
**Auto-fixable**: YES

#### Original Code
```typescript
it('should create token with expiry', () => {
  const token = createToken();
  expect(token.expiresAt).toBeGreaterThan(Date.now());
});
```

#### Suggested Fix
```typescript
it('should create token with expiry', () => {
  const now = new Date('2024-01-01T12:00:00Z');
  vi.setSystemTime(now);

  const token = createToken();

  expect(token.expiresAt).toBe(now.getTime() + TOKEN_LIFETIME);
  vi.useRealTimers();
});
```

#### Changes Summary
- Added: `vi.setSystemTime()` for deterministic time
- Added: `vi.useRealTimers()` cleanup
- Changed: Assertion to exact value match

#### Verification
Run 10x to confirm fix:
```bash
for i in {1..10}; do npm test -- test/api/login.test.ts:45; done
```

### Batch Fix Summary

| Test | Category | Auto-Fixed | Status |
|------|----------|-----------|--------|
| login.test.ts:45 | Timing | Yes | ✅ Fixed |
| user.test.ts:23 | Async | Yes | ✅ Fixed |
| db.test.ts:67 | State | No | Suggested |
| api.test.ts:12 | Network | No | Suggested |

**Auto-fixed**: 2 tests
**Manual review**: 2 tests
**Estimated stability improvement**: +1.5%
```

## Integration Points

- Works with `flaky-detect` for test identification
- Reports to Test Engineer for complex fixes
- Feeds into CI stability metrics
- Updates `.aiwg/testing/flaky-fixes.md`

## Script Reference

### flaky_fixer.py
Analyze and fix flaky tests:
```bash
python scripts/flaky_fixer.py --test test/api/login.test.ts --auto-fix
```

### batch_fix.py
Fix multiple flaky tests:
```bash
python scripts/batch_fix.py --input flaky-report.json --safe-only
```
