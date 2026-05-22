---
description: "Generar y ejecutar tests automatizados. Soporta Vitest, Jest, React Testing Library, Playwright."
user-invocable: true
argument-hint: "[generate|run|coverage] [file-or-pattern]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Test Skill

Eres un experto en testing. Tu rol es generar, ejecutar y mantener tests de alta calidad siguiendo las mejores prácticas.

## Frameworks Soportados

| Framework | Uso | Detección |
|-----------|-----|-----------|
| Vitest | Unit/Integration | `vitest.config.ts` |
| Jest | Unit/Integration | `jest.config.js` |
| React Testing Library | Components | `@testing-library/react` |
| Playwright | E2E | `playwright.config.ts` |
| Cypress | E2E | `cypress.config.ts` |

## Comandos

### GENERATE - Generar tests

```bash
# Detectar framework
cat package.json | jq '.devDependencies | keys[]' | grep -E "vitest|jest|playwright"
```

#### Template de Test (Vitest/Jest)

```typescript
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { functionToTest } from './module';

describe('ModuleName', () => {
  // Setup
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('functionToTest', () => {
    it('should handle valid input correctly', () => {
      // Arrange
      const input = { id: 1, name: 'Test' };
      const expected = { success: true, data: input };

      // Act
      const result = functionToTest(input);

      // Assert
      expect(result).toEqual(expected);
    });

    it('should throw error for invalid input', () => {
      // Arrange
      const invalidInput = null;

      // Act & Assert
      expect(() => functionToTest(invalidInput)).toThrow('Invalid input');
    });

    it('should handle edge cases', () => {
      // Arrange
      const edgeCase = { id: 0, name: '' };

      // Act
      const result = functionToTest(edgeCase);

      // Assert
      expect(result).toBeDefined();
    });
  });
});
```

#### Template de Test (React Component)

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi } from 'vitest';
import { ComponentName } from './ComponentName';

describe('ComponentName', () => {
  const defaultProps = {
    title: 'Test Title',
    onClick: vi.fn(),
  };

  const renderComponent = (props = {}) => {
    return render(<ComponentName {...defaultProps} {...props} />);
  };

  it('should render correctly', () => {
    renderComponent();

    expect(screen.getByText('Test Title')).toBeInTheDocument();
  });

  it('should handle click events', async () => {
    const user = userEvent.setup();
    renderComponent();

    await user.click(screen.getByRole('button'));

    expect(defaultProps.onClick).toHaveBeenCalledTimes(1);
  });

  it('should show loading state', () => {
    renderComponent({ isLoading: true });

    expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();
  });

  it('should display error message', () => {
    renderComponent({ error: 'Something went wrong' });

    expect(screen.getByText('Something went wrong')).toBeInTheDocument();
  });

  it('should be accessible', () => {
    const { container } = renderComponent();

    // Check for proper ARIA attributes
    expect(screen.getByRole('button')).toHaveAttribute('aria-label');
  });
});
```

#### Template de Test (API/Service)

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { UserService } from './user.service';
import { prisma } from '@/lib/prisma';

// Mock dependencies
vi.mock('@/lib/prisma', () => ({
  prisma: {
    user: {
      findUnique: vi.fn(),
      findMany: vi.fn(),
      create: vi.fn(),
      update: vi.fn(),
      delete: vi.fn(),
    },
  },
}));

describe('UserService', () => {
  let service: UserService;

  beforeEach(() => {
    service = new UserService();
    vi.clearAllMocks();
  });

  describe('getUserById', () => {
    it('should return user when found', async () => {
      // Arrange
      const mockUser = { id: '1', email: 'test@example.com' };
      vi.mocked(prisma.user.findUnique).mockResolvedValue(mockUser);

      // Act
      const result = await service.getUserById('1');

      // Assert
      expect(result).toEqual(mockUser);
      expect(prisma.user.findUnique).toHaveBeenCalledWith({
        where: { id: '1' },
      });
    });

    it('should return null when user not found', async () => {
      // Arrange
      vi.mocked(prisma.user.findUnique).mockResolvedValue(null);

      // Act
      const result = await service.getUserById('999');

      // Assert
      expect(result).toBeNull();
    });

    it('should handle database errors', async () => {
      // Arrange
      vi.mocked(prisma.user.findUnique).mockRejectedValue(
        new Error('Database connection failed')
      );

      // Act & Assert
      await expect(service.getUserById('1')).rejects.toThrow(
        'Database connection failed'
      );
    });
  });
});
```

### RUN - Ejecutar tests

```bash
# Vitest
pnpm vitest run
pnpm vitest run src/components/Button.test.tsx
pnpm vitest run --watch

# Jest
pnpm jest
pnpm jest src/components/Button.test.tsx

# Playwright
pnpm playwright test
pnpm playwright test --ui
```

### COVERAGE - Generar reporte de cobertura

```bash
# Vitest
pnpm vitest run --coverage

# Jest
pnpm jest --coverage

# Ver reporte
open coverage/index.html
```

## Mejores Prácticas

### Naming Conventions
```
ComponentName.test.tsx    # Component tests
service.test.ts           # Service tests
utils.test.ts             # Utility tests
api.e2e.test.ts          # E2E tests
```

### Test Structure (AAA Pattern)
```typescript
it('should do something', () => {
  // Arrange - Setup test data and conditions
  const input = createTestData();

  // Act - Execute the code under test
  const result = functionUnderTest(input);

  // Assert - Verify the results
  expect(result).toBe(expectedValue);
});
```

### What to Test

| Tipo | Qué testear | Ejemplo |
|------|-------------|---------|
| Unit | Pure functions | `formatDate()`, `calculateTotal()` |
| Integration | API + DB | Service methods |
| Component | User interactions | Button clicks, form submissions |
| E2E | User flows | Login → Dashboard → Logout |

### What NOT to Test
- Implementation details
- Third-party libraries
- Getters/setters simples
- Framework internals

## Coverage Goals

| Tipo | Mínimo | Ideal |
|------|--------|-------|
| Statements | 70% | 85% |
| Branches | 70% | 80% |
| Functions | 75% | 90% |
| Lines | 70% | 85% |

## Output Esperado

```
🧪 TEST GENERATION COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Target: src/services/user.service.ts
Framework: Vitest
Test file: src/services/user.service.test.ts

Tests Generated:
  ✅ getUserById - valid input
  ✅ getUserById - not found
  ✅ getUserById - database error
  ✅ createUser - success
  ✅ createUser - duplicate email
  ✅ updateUser - success
  ✅ deleteUser - success

Coverage Impact:
  Before: 65% → After: 82% (estimated)

Run Tests:
  pnpm vitest run src/services/user.service.test.ts

Next Steps:
  1. Review generated tests
  2. Add edge cases if needed
  3. Run: pnpm test
```
