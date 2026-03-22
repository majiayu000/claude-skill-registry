---
name: jest
description: Jest testing framework for JavaScript/TypeScript
category: Testing-BDD
---

# Skill: jest

## What I do

I provide Jest testing expertise: test structure, mocking strategies, async testing, snapshot tests, and coverage configuration for JavaScript/TypeScript projects.

## When to use me

- Writing unit or integration tests in JavaScript/TypeScript
- Mocking modules, functions, or timers
- Testing async code (promises, async/await, callbacks)
- Setting up test configuration and coverage thresholds
- Debugging flaky or slow tests

## Core principles

1. **Arrange-Act-Assert** - Clear test structure with setup, action, and verification
2. **Mock at boundaries** - Mock external dependencies, not internal implementation
3. **Test behaviour, not implementation** - Assert outcomes, not function calls
4. **Isolate tests** - Each test runs independently, no shared mutable state
5. **Fast feedback** - Keep tests fast; mock network/disk; use `--watch`

## Patterns & examples

**Basic test structure:**
```javascript
describe('CartService', () => {
  let cart;

  beforeEach(() => {
    cart = new CartService();
  });

  it('adds item and updates total', () => {
    cart.addItem({ id: 1, price: 9.99 });

    expect(cart.items).toHaveLength(1);
    expect(cart.total).toBeCloseTo(9.99);
  });

  it('throws on negative quantity', () => {
    expect(() => cart.addItem({ id: 1, qty: -1 }))
      .toThrow('Quantity must be positive');
  });
});
```

**Mocking modules:**
```javascript
// ✅ Correct: mock at module boundary
jest.mock('./api-client');
const { fetchUser } = require('./api-client');

fetchUser.mockResolvedValue({ id: 1, name: 'Alice' });

it('loads user profile', async () => {
  const profile = await loadProfile(1);
  expect(profile.name).toBe('Alice');
  expect(fetchUser).toHaveBeenCalledWith(1);
});

// ❌ Wrong: mocking internal implementation details
jest.spyOn(service, '_privateHelper');  // brittle
```

**Async testing:**
```javascript
// ✅ Correct: async/await pattern
it('fetches data successfully', async () => {
  const data = await fetchData('/api/items');
  expect(data).toEqual(expect.arrayContaining([
    expect.objectContaining({ id: 1 })
  ]));
});

// ✅ Correct: testing rejections
it('rejects on network error', async () => {
  await expect(fetchData('/bad')).rejects.toThrow('Network error');
});
```

**Timer mocking:**
```javascript
beforeEach(() => jest.useFakeTimers());
afterEach(() => jest.useRealTimers());

it('debounces search input', () => {
  const handler = jest.fn();
  const search = debounce(handler, 300);

  search('he');
  search('hel');
  search('hello');

  jest.advanceTimersByTime(300);
  expect(handler).toHaveBeenCalledTimes(1);
  expect(handler).toHaveBeenCalledWith('hello');
});
```

**Snapshot testing:**
```javascript
// ✅ Correct: small, focused snapshots
it('renders user card', () => {
  const { container } = render(<UserCard name="Alice" role="admin" />);
  expect(container.firstChild).toMatchSnapshot();
});

// ❌ Wrong: snapshotting entire page (brittle, noisy diffs)
expect(document.body).toMatchSnapshot();
```

## Anti-patterns to avoid

- ❌ Testing implementation details (spying on private methods)
- ❌ Large snapshot files (snapshot entire components, not pages)
- ❌ Shared mutable state between tests (use `beforeEach` for fresh state)
- ❌ Forgetting `await` on async assertions (test passes falsely)
- ❌ Over-mocking (mock boundaries, not everything—test real logic)

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Testing-BDD/Jest.md`

## Related skills

- `javascript` - Core JS/TS idioms and patterns
- `bdd-workflow` - Red-Green-Refactor cycle
- `clean-code` - SOLID principles in test code
- `cypress` - E2E testing (complementary to Jest unit tests)
