---
name: frontend-testing
description: Implement comprehensive frontend testing using Jest, Vitest, React Testing Library, and Cypress. Use when building robust test suites for UI and integration tests.
---

# Frontend Testing

## Overview

Build comprehensive test suites for frontend applications including unit tests, integration tests, and end-to-end tests with proper coverage and assertions.

## When to Use

- Component testing
- Integration testing
- End-to-end testing
- Regression prevention
- Quality assurance
- Test-driven development

## Implementation Examples

### 1. **Jest Unit Testing (React)**

```typescript
// Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { Button } from './Button';

describe('Button Component', () => {
  it('renders button with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button')).toHaveTextContent('Click me');
  });

  it('calls onClick handler when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click</Button>);

    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('disables button when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });

  it('applies variant styles correctly', () => {
    const { container } = render(<Button variant="primary">Click</Button>);
    const button = container.querySelector('button');
    expect(button).toHaveClass('bg-blue-500');
  });

  it('applies size classes correctly', () => {
    const { container } = render(<Button size="lg">Click</Button>);
    const button = container.querySelector('button');
    expect(button).toHaveClass('px-6 py-3 text-lg');
  });
});

// hooks.test.ts
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('initializes with default value', () => {
    const { result } = renderHook(() => useCounter());
    expect(result.current.count).toBe(0);
  });

  it('increments count', () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });

  it('decrements count', () => {
    const { result } = renderHook(() => useCounter(5));

    act(() => {
      result.current.decrement();
    });

    expect(result.current.count).toBe(4);
  });

  it('resets count', () => {
    const { result } = renderHook(() => useCounter(5));

    act(() => {
      result.current.increment();
      result.current.reset();
    });

    expect(result.current.count).toBe(5);
  });
});
```

### 2. **React Testing Library Integration Tests**

```typescript
// UserForm.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { UserForm } from './UserForm';

describe('UserForm Integration', () => {
  beforeEach(() => {
    // Clear mocks before each test
    jest.clearAllMocks();
  });

  it('submits form with valid data', async () => {
    const handleSubmit = jest.fn();
    render(<UserForm onSubmit={handleSubmit} />);

    await userEvent.type(screen.getByLabelText(/name/i), 'John Doe');
    await userEvent.type(screen.getByLabelText(/email/i), 'john@example.com');
    await userEvent.type(screen.getByLabelText(/password/i), 'password123');

    fireEvent.click(screen.getByRole('button', { name: /submit/i }));

    await waitFor(() => {
      expect(handleSubmit).toHaveBeenCalledWith({
        name: 'John Doe',
        email: 'john@example.com',
        password: 'password123'
      });
    });
  });

  it('displays validation errors for empty fields', async () => {
    render(<UserForm onSubmit={jest.fn()} />);

    fireEvent.click(screen.getByRole('button', { name: /submit/i }));

    await waitFor(() => {
      expect(screen.getByText(/name is required/i)).toBeInTheDocument();
      expect(screen.getByText(/email is required/i)).toBeInTheDocument();
    });
  });

  it('displays validation error for invalid email', async () => {
    render(<UserForm onSubmit={jest.fn()} />);

    await userEvent.type(screen.getByLabelText(/email/i), 'invalid-email');
    fireEvent.click(screen.getByRole('button', { name: /submit/i }));

    await waitFor(() => {
      expect(screen.getByText(/invalid email/i)).toBeInTheDocument();
    });
  });
});

// UserList.test.tsx with data fetching
import { render, screen, waitFor } from '@testing-library/react';
import { UserList } from './UserList';

describe('UserList with API', () => {
  beforeEach(() => {
    jest.spyOn(global, 'fetch').mockClear();
  });

  it('displays loading state initially', () => {
    (global.fetch as jest.Mock).mockImplementation(
      () => new Promise(() => {}) // Never resolves
    );

    render(<UserList />);
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it('fetches and displays users', async () => {
    const mockUsers = [
      { id: 1, name: 'User 1', email: 'user1@example.com' },
      { id: 2, name: 'User 2', email: 'user2@example.com' }
    ];

    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockUsers
    });

    render(<UserList />);

    await waitFor(() => {
      expect(screen.getByText('User 1')).toBeInTheDocument();
      expect(screen.getByText('User 2')).toBeInTheDocument();
    });
  });

  it('displays error message on fetch failure', async () => {
    (global.fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'));

    render(<UserList />);

    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    });
  });
});
```

### 3. **Vitest for Vue Testing**

```typescript
// Button.spec.ts
import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import Button from './Button.vue';

describe('Button.vue', () => {
  it('renders slot content', () => {
    const wrapper = mount(Button, {
      slots: {
        default: 'Click me'
      }
    });
    expect(wrapper.text()).toContain('Click me');
  });

  it('emits click event', async () => {
    const wrapper = mount(Button);
    await wrapper.trigger('click');
    expect(wrapper.emitted('click')).toHaveLength(1);
  });

  it('disables button when disabled prop is true', () => {
    const wrapper = mount(Button, {
      props: { disabled: true }
    });
    expect(wrapper.attributes('disabled')).toBeDefined();
  });

  it('applies variant class', () => {
    const wrapper = mount(Button, {
      props: { variant: 'primary' }
    });
    expect(wrapper.classes()).toContain('bg-blue-500');
  });
});

// composable.spec.ts
import { describe, it, expect } from 'vitest';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('initializes with default value', () => {
    const { count } = useCounter();
    expect(count.value).toBe(0);
  });

  it('increments count', () => {
    const { count, increment } = useCounter();
    increment();
    expect(count.value).toBe(1);
  });
});
```

### 4. **Cypress E2E Testing**

```typescript
// cypress/e2e/login.cy.ts
describe('Login Flow', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000/login');
  });

  it('logs in with valid credentials', () => {
    cy.get('input[name="email"]').type('user@example.com');
    cy.get('input[name="password"]').type('password123');
    cy.get('button[type="submit"]').click();

    cy.url().should('include', '/dashboard');
    cy.get('h1').should('contain', 'Welcome');
  });

  it('displays error for invalid credentials', () => {
    cy.get('input[name="email"]').type('user@example.com');
    cy.get('input[name="password"]').type('wrongpassword');
    cy.get('button[type="submit"]').click();

    cy.get('.error-message').should('contain', 'Invalid credentials');
  });

  it('validates email field', () => {
    cy.get('input[name="email"]').type('invalid-email');
    cy.get('input[name="password"]').type('password123');
    cy.get('button[type="submit"]').click();

    cy.get('.error-message').should('contain', 'Invalid email');
  });
});

// cypress/e2e/user-management.cy.ts
describe('User Management', () => {
  beforeEach(() => {
    cy.login('admin@example.com', 'password123');
    cy.visit('http://localhost:3000/users');
  });

  it('creates a new user', () => {
    cy.get('button:contains("Add User")').click();

    cy.get('input[name="name"]').type('New User');
    cy.get('input[name="email"]').type('newuser@example.com');
    cy.get('button[type="submit"]').click();

    cy.get('.success-message').should('contain', 'User created');
    cy.get('table tbody').should('contain', 'New User');
  });

  it('edits an existing user', () => {
    cy.get('table tbody tr').first().contains('button', 'Edit').click();

    cy.get('input[name="name"]').clear().type('Updated Name');
    cy.get('button[type="submit"]').click();

    cy.get('.success-message').should('contain', 'User updated');
  });

  it('deletes a user with confirmation', () => {
    cy.get('table tbody tr').first().contains('button', 'Delete').click();
    cy.get('.modal button:contains("Confirm")').click();

    cy.get('.success-message').should('contain', 'User deleted');
  });
});

// cypress/support/commands.ts
Cypress.Commands.add('login', (email: string, password: string) => {
  cy.visit('http://localhost:3000/login');
  cy.get('input[name="email"]').type(email);
  cy.get('input[name="password"]').type(password);
  cy.get('button[type="submit"]').click();
  cy.url().should('include', '/dashboard');
});
```

### 5. **Test Coverage Configuration**

```javascript
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  roots: ['<rootDir>/src'],
  testMatch: ['**/__tests__/**/*.ts?(x)', '**/?(*.)+(spec|test).ts?(x)'],
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/index.tsx',
    '!src/reportWebVitals.ts'
  ],
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70
    }
  },
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1'
  },
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.ts'],
  transform: {
    '^.+\\.tsx?$': ['ts-jest', {
      tsconfig: {
        jsx: 'react-jsx'
      }
    }]
  }
};

// package.json scripts
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "cypress": "cypress open",
    "cypress:headless": "cypress run"
  }
}
```

## Best Practices

- Write tests alongside code (TDD)
- Test behavior, not implementation
- Use descriptive test names
- Keep tests focused and independent
- Mock external dependencies
- Aim for high coverage (>80%)
- Use semantic queries in React Testing Library
- Implement E2E tests for critical paths
- Test error scenarios
- Use CI/CD for automated testing

## Resources

- [Jest Documentation](https://jestjs.io/)
- [Vitest](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [Cypress Documentation](https://docs.cypress.io/)
- [Testing Library Best Practices](https://testing-library.com/docs/queries/about)
