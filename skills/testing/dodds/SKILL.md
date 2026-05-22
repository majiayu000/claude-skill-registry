---
name: dodds-testing-practices
description: Write JavaScript code in the style of Kent C. Dodds, testing advocate and React educator. Emphasizes testing best practices, React patterns, and developer productivity. Use when writing tests or building maintainable React applications.
---

# Kent C. Dodds Style Guide

## Overview

Kent C. Dodds is a testing advocate, educator, and creator of Testing Library. His philosophy centers on writing tests that give confidence, avoiding implementation details, and making React code maintainable.

## Core Philosophy

> "The more your tests resemble the way your software is used, the more confidence they can give you."

> "Write tests. Not too many. Mostly integration."

> "Avoid testing implementation details."

Dodds believes tests should focus on user behavior, not internal mechanics, and that fewer well-written tests beat many brittle ones.

## Design Principles

1. **Test User Behavior**: Test what users see and do, not how code works internally.

2. **Confidence Over Coverage**: Tests should give confidence, not just increase metrics.

3. **Integration Over Unit**: Integration tests give the best ROI.

4. **Avoid Implementation Details**: Tests shouldn't break when refactoring.

## When Writing Code

### Always

- Query elements the way users find them (by role, label, text)
- Test user flows, not individual functions
- Use realistic data in tests
- Make tests independent and isolated
- Write accessible components (they're easier to test!)
- Prefer integration tests over unit tests for UI

### Never

- Test implementation details (internal state, method names)
- Use test IDs when semantic queries work
- Mock everything—use real components when possible
- Write tests that break on refactoring
- Snapshot test entire components
- Test third-party libraries

### Prefer

- `getByRole` over `getByTestId`
- `userEvent` over `fireEvent`
- Real network calls in integration tests (with MSW)
- Factories over fixtures
- Async assertions over arbitrary waits

## Code Patterns

### Testing Library Queries

```javascript
// Query Priority (use in this order)
// 1. Accessible queries (reflect user experience)
// 2. Semantic queries
// 3. Test IDs (last resort)

// BEST: Accessible queries
screen.getByRole('button', { name: /submit/i });
screen.getByRole('textbox', { name: /email/i });
screen.getByRole('heading', { level: 1 });
screen.getByLabelText(/password/i);

// GOOD: Semantic queries
screen.getByText(/welcome back/i);
screen.getByPlaceholderText(/search/i);
screen.getByAltText(/profile photo/i);

// LAST RESORT: Test IDs
screen.getByTestId('complex-chart');


// BAD: Implementation details
container.querySelector('.submit-btn');  // CSS class = implementation
wrapper.find('SubmitButton');            // Component name = implementation
screen.getByTestId('submit');            // When role exists
```

### Testing User Interactions

```javascript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('allows users to submit the form', async () => {
    const user = userEvent.setup();
    const onSubmit = jest.fn();
    
    render(<ContactForm onSubmit={onSubmit} />);
    
    // Type in fields - like a real user
    await user.type(
        screen.getByRole('textbox', { name: /name/i }),
        'Alice Smith'
    );
    await user.type(
        screen.getByRole('textbox', { name: /email/i }),
        'alice@example.com'
    );
    await user.type(
        screen.getByRole('textbox', { name: /message/i }),
        'Hello there!'
    );
    
    // Submit the form
    await user.click(screen.getByRole('button', { name: /send/i }));
    
    // Assert on the result
    expect(onSubmit).toHaveBeenCalledWith({
        name: 'Alice Smith',
        email: 'alice@example.com',
        message: 'Hello there!'
    });
});


// BAD: Testing implementation
test('sets state when input changes', () => {
    const { container } = render(<Form />);
    const input = container.querySelector('input');
    
    fireEvent.change(input, { target: { value: 'test' } });
    
    expect(wrapper.state('value')).toBe('test');  // Implementation detail!
});
```

### Async Testing

```javascript
import { render, screen, waitFor } from '@testing-library/react';

test('loads and displays user data', async () => {
    render(<UserProfile userId="123" />);
    
    // Wait for loading to finish
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
    
    // Wait for content - findBy queries include built-in waiting
    const userName = await screen.findByRole('heading', { name: /alice/i });
    expect(userName).toBeInTheDocument();
    
    // For multiple assertions, use waitFor
    await waitFor(() => {
        expect(screen.getByText(/alice@example.com/i)).toBeInTheDocument();
        expect(screen.getByRole('img', { name: /avatar/i })).toBeInTheDocument();
    });
});


// BAD: Arbitrary timeouts
await new Promise(r => setTimeout(r, 1000));  // Flaky and slow
```

### Mocking with MSW

```javascript
import { rest } from 'msw';
import { setupServer } from 'msw/node';

// Set up mock server
const server = setupServer(
    rest.get('/api/user/:id', (req, res, ctx) => {
        return res(ctx.json({
            id: req.params.id,
            name: 'Alice',
            email: 'alice@example.com'
        }));
    }),
    
    rest.post('/api/login', async (req, res, ctx) => {
        const { email, password } = await req.json();
        
        if (password === 'correct') {
            return res(ctx.json({ token: 'fake-token' }));
        }
        return res(ctx.status(401), ctx.json({ error: 'Invalid credentials' }));
    })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

test('handles login error', async () => {
    const user = userEvent.setup();
    render(<LoginForm />);
    
    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.type(screen.getByLabelText(/password/i), 'wrong');
    await user.click(screen.getByRole('button', { name: /log in/i }));
    
    expect(await screen.findByText(/invalid credentials/i)).toBeInTheDocument();
});
```

### Custom Render Functions

```javascript
// test-utils.js
import { render } from '@testing-library/react';
import { ThemeProvider } from './theme';
import { UserProvider } from './user-context';
import { BrowserRouter } from 'react-router-dom';

function AllProviders({ children }) {
    return (
        <BrowserRouter>
            <ThemeProvider>
                <UserProvider>
                    {children}
                </UserProvider>
            </ThemeProvider>
        </BrowserRouter>
    );
}

function customRender(ui, options) {
    return render(ui, { wrapper: AllProviders, ...options });
}

// Re-export everything
export * from '@testing-library/react';
export { customRender as render };


// In tests
import { render, screen } from './test-utils';

test('shows user dashboard', () => {
    render(<Dashboard />);  // Automatically wrapped with all providers
});
```

### The Testing Trophy

```javascript
// Static Analysis (ESLint, TypeScript) - catches typos, type errors
// Unit Tests - test pure functions, utilities
// Integration Tests - test features, user flows (MOST OF YOUR TESTS)
// E2E Tests - critical paths only

// Unit test example - pure function
test('formatCurrency formats correctly', () => {
    expect(formatCurrency(1234.5)).toBe('$1,234.50');
    expect(formatCurrency(0)).toBe('$0.00');
    expect(formatCurrency(-50)).toBe('-$50.00');
});

// Integration test example - feature
test('user can add item to cart', async () => {
    const user = userEvent.setup();
    render(<App />);
    
    // Navigate to product
    await user.click(screen.getByRole('link', { name: /products/i }));
    await user.click(screen.getByRole('link', { name: /widget/i }));
    
    // Add to cart
    await user.click(screen.getByRole('button', { name: /add to cart/i }));
    
    // Verify cart
    expect(screen.getByRole('status')).toHaveTextContent('1 item');
    await user.click(screen.getByRole('link', { name: /cart/i }));
    expect(screen.getByText(/widget/i)).toBeInTheDocument();
});
```

### React Patterns

```javascript
// Prop Collections and Getters
function useToggle(initialOn = false) {
    const [on, setOn] = useState(initialOn);
    
    const toggle = () => setOn(prev => !prev);
    
    // Prop getter - composable with user's props
    const getTogglerProps = ({ onClick, ...props } = {}) => ({
        'aria-pressed': on,
        onClick: (...args) => {
            onClick?.(...args);
            toggle();
        },
        ...props
    });
    
    return { on, toggle, getTogglerProps };
}

// Usage
function App() {
    const { on, getTogglerProps } = useToggle();
    
    return (
        <button
            {...getTogglerProps({
                onClick: () => console.log('clicked!'),
                className: 'toggle-btn'
            })}
        >
            {on ? 'ON' : 'OFF'}
        </button>
    );
}


// Control Props Pattern
function Toggle({ on: controlledOn, onChange, initialOn = false }) {
    const [internalOn, setInternalOn] = useState(initialOn);
    
    // Is this controlled or uncontrolled?
    const isControlled = controlledOn !== undefined;
    const on = isControlled ? controlledOn : internalOn;
    
    function toggle() {
        if (!isControlled) {
            setInternalOn(prev => !prev);
        }
        onChange?.(!on);
    }
    
    return <button onClick={toggle}>{on ? 'ON' : 'OFF'}</button>;
}
```

## Mental Model

Dodds approaches testing by asking:

1. **What does the user see?** Query by visible elements
2. **What does the user do?** Simulate real interactions
3. **What does the user expect?** Assert on visible outcomes
4. **Does this test implementation?** If yes, refactor the test
5. **Would this break on refactor?** If yes, it's too coupled

## Signature Dodds Moves

- Query by role first, test ID last
- userEvent over fireEvent
- MSW for network mocking
- Integration tests as the default
- Custom render with providers
- Test user behavior, not code structure
