---
name: javascript-testing
description: Write and run JavaScript/TypeScript tests using Vitest or Jest with mocking, component testing, and coverage. Use when writing JS/TS tests, testing Svelte/React components, or setting up test configuration.
---

# JavaScript/TypeScript Testing Skill

## When to Activate

Activate this skill when:
- Writing JavaScript or TypeScript tests
- Testing Svelte, React, or Vue components
- Setting up Vitest or Jest configuration
- Working with mocks, spies, or test utilities
- Running tests or checking coverage

## Framework Selection

| Use Case | Framework |
|----------|-----------|
| SvelteKit, Vite projects | **Vitest** (recommended) |
| Non-Vite projects, React Native | **Jest** |

## Quick Commands

### Vitest
```bash
npx vitest              # Watch mode
npx vitest run          # Single run (CI)
npx vitest run --coverage
npx vitest --ui         # Visual UI
```

### Jest
```bash
pnpm test
pnpm test --watch
pnpm test --coverage
```

## Test Structure: AAA Pattern

```typescript
import { describe, it, expect, beforeEach } from 'vitest';

describe('UserService', () => {
    let userService: UserService;

    beforeEach(() => {
        userService = new UserService();
    });

    it('should create a new user with valid data', () => {
        // Arrange
        const email = 'test@example.com';
        const password = 'secure_pass123';

        // Act
        const result = userService.register(email, password);

        // Assert
        expect(result.success).toBe(true);
        expect(result.user.email).toBe(email);
    });
});
```

## Vitest Setup (SvelteKit)

```typescript
// vite.config.ts
import { defineConfig } from 'vitest/config';
import { sveltekit } from '@sveltejs/kit/vite';

export default defineConfig({
    plugins: [sveltekit()],
    test: {
        include: ['src/**/*.{test,spec}.{js,ts}'],
        globals: true,
        environment: 'jsdom',
        setupFiles: ['./src/tests/setup.ts'],
    }
});
```

## Mocking

### Vitest
```typescript
import { vi } from 'vitest';

vi.mock('./api', () => ({
    fetchUser: vi.fn()
}));

vi.mocked(fetchUser).mockResolvedValue({ id: 1, name: 'John' });
```

### Jest
```typescript
jest.mock('./api', () => ({
    fetchUser: jest.fn()
}));
```

## Component Testing (Svelte)

```typescript
import { render, screen, fireEvent } from '@testing-library/svelte';
import Counter from './Counter.svelte';

it('should increment count on click', async () => {
    render(Counter, { props: { initialCount: 0 } });

    const button = screen.getByRole('button', { name: /increment/i });
    await fireEvent.click(button);

    expect(screen.getByText('Count: 1')).toBeInTheDocument();
});
```

## Common Assertions

```typescript
// Equality
expect(value).toBe(expected);           // Strict ===
expect(value).toEqual(expected);        // Deep equality

// Truthiness
expect(value).toBeTruthy();
expect(value).toBeNull();

// Arrays/Objects
expect(array).toContain(item);
expect(obj).toHaveProperty('key');

// Exceptions
expect(() => fn()).toThrow('error');

// Async
await expect(promise).resolves.toBe(value);
await expect(promise).rejects.toThrow();
```

## Query Priority (Testing Library)

1. `getByRole` - Accessible queries (best)
2. `getByLabelText` - Form fields
3. `getByPlaceholderText` - Inputs
4. `getByText` - Non-interactive elements
5. `getByTestId` - Last resort

## Directory Structure

```
src/
├── lib/
│   ├── components/
│   │   ├── Button.svelte
│   │   └── Button.test.ts
│   └── utils/
│       ├── format.ts
│       └── format.test.ts
└── tests/
    ├── setup.ts
    └── integration/
```

## SvelteKit Testing

### Load Functions
```typescript
import { load } from './+page.server';

it('should fetch posts', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
        json: () => Promise.resolve([{ id: 1 }])
    });

    const result = await load({ fetch: mockFetch } as any);
    expect(result.posts).toHaveLength(1);
});
```

### Form Actions
```typescript
import { actions } from './+page.server';

it('should validate login', async () => {
    const formData = new FormData();
    formData.set('email', 'test@example.com');

    const request = new Request('http://localhost', {
        method: 'POST',
        body: formData
    });

    const result = await actions.default({ request } as any);
    expect(result.success).toBe(true);
});
```

## Related Resources

See `AgentUsage/testing_javascript.md` for complete documentation including:
- Jest configuration
- Async testing patterns
- SvelteKit-specific patterns
- CI/CD integration
