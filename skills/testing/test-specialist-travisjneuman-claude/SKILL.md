---
name: test-specialist
description: This skill should be used when writing test cases, fixing bugs, analyzing code for potential issues, or improving test coverage for JavaScript/TypeScript applications. Use this for unit tests, integration tests, end-to-end tests, debugging runtime errors, logic bugs, performance issues, security vulnerabilities, and systematic code analysis.
---

# Test Specialist

Systematic testing methodologies and debugging techniques for JS/TS applications.

## When to Use

**Use for:**

- Writing unit, integration, or E2E tests
- Fixing bugs and debugging
- Improving test coverage
- Analyzing code for potential issues
- Security and performance testing

**Don't use when:**

- Code review → use `generic-code-reviewer`
- Technical debt → use `tech-debt-analyzer`
- Feature development → use `generic-feature-developer`

## Testing Stack by Project

| Project Type  | Unit Tests  | Component       | E2E        |
| ------------- | ----------- | --------------- | ---------- |
| React/Next.js | Vitest/Jest | Testing Library | Playwright |
| Node.js       | Vitest/Jest | Supertest       | Playwright |
| Static        | Jest        | -               | Playwright |

## Test Patterns

### Unit Tests (AAA Pattern)

```typescript
describe("calculateTotal", () => {
  test("sums amounts correctly", () => {
    // Arrange
    const items = [{ amount: 100 }, { amount: 50 }];
    // Act
    const total = calculateTotal(items);
    // Assert
    expect(total).toBe(150);
  });

  test("handles empty list", () => {
    expect(calculateTotal([])).toBe(0);
  });
});
```

### Component Tests (User Behavior)

```typescript
// ✅ Test user behavior, not implementation
it('creates item when user clicks Add', async () => {
  const user = userEvent.setup();
  render(<ItemList />);

  await user.click(screen.getByRole('button', { name: /add/i }));
  await user.type(screen.getByLabelText(/title/i), 'New item');
  await user.click(screen.getByRole('button', { name: /save/i }));

  expect(screen.getByText('New item')).toBeInTheDocument();
});
```

### E2E Tests (Playwright)

```typescript
import { test, expect } from "@playwright/test";

test("user can complete checkout", async ({ page }) => {
  await page.goto("/products");

  // Add to cart
  await page.click('button:has-text("Add to Cart")');
  await page.click('a:has-text("Cart")');

  // Checkout
  await page.click('button:has-text("Checkout")');
  await page.fill('[name="email"]', "test@example.com");
  await page.click('button:has-text("Place Order")');

  // Verify
  await expect(page.locator("h1")).toContainText("Order Confirmed");
});
```

### Integration Tests

```typescript
test("POST /items creates item", async () => {
  const response = await request(app)
    .post("/api/items")
    .send({ name: "Test" })
    .expect(201);

  expect(response.body).toMatchObject({ id: expect.any(Number) });
});
```

## Bug Analysis Process

1. **Reproduce** - Document exact steps, expected vs actual
2. **Isolate** - Binary search, minimal reproduction
3. **Root Cause** - Trace execution, check assumptions, git blame
4. **Fix** - Write failing test first, implement fix
5. **Validate** - Run full suite, test edge cases

## Debugging Checklist

When debugging an issue:

- [ ] Can reproduce consistently
- [ ] Minimal reproduction created
- [ ] Console/network logs checked
- [ ] State at failure point inspected
- [ ] Git blame checked for recent changes
- [ ] Failing test written before fix

## Common Bug Patterns

### Race Conditions

```typescript
test("handles concurrent updates", async () => {
  const promises = Array.from({ length: 100 }, () => increment());
  await Promise.all(promises);
  expect(getCount()).toBe(100);
});
```

### Null Safety

```typescript
test.each([null, undefined, "", 0])("handles invalid input: %p", (input) => {
  expect(() => process(input)).toThrow("Invalid");
});
```

### Boundary Values

```typescript
test("handles edge cases", () => {
  expect(paginate([], 1, 10)).toEqual([]); // empty
  expect(paginate([item], 1, 10)).toEqual([item]); // single
  expect(paginate(items25, 3, 10)).toHaveLength(5); // partial last page
});
```

## Security Tests

```typescript
test("prevents SQL injection", async () => {
  const malicious = "'; DROP TABLE users; --";
  await expect(search(malicious)).resolves.not.toThrow();
});

test("sanitizes XSS", () => {
  const xss = '<script>alert("xss")</script>';
  expect(sanitize(xss)).not.toContain("<script>");
});

test("requires auth", async () => {
  await request(app).post("/api/items").expect(401);
});
```

## Performance Tests

```typescript
test("handles large datasets efficiently", () => {
  const largeList = Array.from({ length: 10000 }, (_, i) => ({ value: i }));
  const start = performance.now();
  process(largeList);
  expect(performance.now() - start).toBeLessThan(100);
});
```

## Coverage Targets

| Code Type      | Target |
| -------------- | ------ |
| Critical paths | 90%+   |
| Business logic | 85%+   |
| UI components  | 75%+   |
| Utilities      | 70%+   |

## Test Quality Principles

1. **One behavior per test**
2. **Descriptive names** - test names explain scenario
3. **Independent tests** - no shared state
4. **Cover edge cases** - null, empty, boundaries, errors
5. **Mock external deps** - tests should be fast
6. **Test behavior** - not implementation details

## Workflow Decision Tree

| Situation          | Action                               |
| ------------------ | ------------------------------------ |
| Adding feature     | Write test first (TDD)               |
| Fixing bug         | Write failing test, then fix         |
| Improving coverage | Find gaps, prioritize critical paths |
| Code review        | Check edge cases, error handling     |

## See Also

- [Code Review Standards](../_shared/CODE_REVIEW_STANDARDS.md) - Quality requirements
- Project `CLAUDE.md` - Testing rules
