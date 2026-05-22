---
name: cypress
description: Writes E2E and component tests with Cypress including selectors, commands, fixtures, and API testing. Use when testing web applications end-to-end, testing user flows, or writing integration tests.
---

# Cypress

Fast, reliable testing for anything that runs in a browser.

## Quick Start

**Install:**
```bash
npm install cypress --save-dev
```

**Open Cypress:**
```bash
npx cypress open
```

**Run headless:**
```bash
npx cypress run
```

## Project Structure

```
cypress/
  e2e/               # E2E test files
    home.cy.ts
    auth.cy.ts
  fixtures/          # Test data
    users.json
  support/
    commands.ts      # Custom commands
    e2e.ts          # E2E support file
    component.ts    # Component support file
  downloads/         # Downloaded files
cypress.config.ts    # Configuration
```

## Configuration

```typescript
// cypress.config.ts
import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    viewportWidth: 1280,
    viewportHeight: 720,
    defaultCommandTimeout: 10000,
    video: false,
    screenshotOnRunFailure: true,
    setupNodeEvents(on, config) {
      // Node event listeners
    },
  },
  component: {
    devServer: {
      framework: 'react',
      bundler: 'vite',
    },
  },
  env: {
    apiUrl: 'http://localhost:3001',
  },
});
```

## Basic Test

```typescript
// cypress/e2e/home.cy.ts
describe('Home Page', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('displays the welcome message', () => {
    cy.contains('h1', 'Welcome').should('be.visible');
  });

  it('navigates to about page', () => {
    cy.get('a[href="/about"]').click();
    cy.url().should('include', '/about');
    cy.contains('About Us').should('be.visible');
  });
});
```

## Selectors

### Best Practices

```typescript
// Prefer data-* attributes
cy.get('[data-testid="submit-button"]');
cy.get('[data-cy="user-name"]');

// By role (accessibility)
cy.get('button').contains('Submit');
cy.get('input[type="email"]');

// By text content
cy.contains('Sign In');
cy.contains('button', 'Submit');

// Avoid brittle selectors
// Bad: cy.get('.btn-primary-lg-submit')
// Bad: cy.get('#form > div:nth-child(3) > button')
```

### Chaining

```typescript
cy.get('[data-cy="user-form"]')
  .find('input[name="email"]')
  .type('test@example.com');

cy.get('[data-cy="user-list"]')
  .children()
  .first()
  .click();
```

## Commands

### Navigation

```typescript
cy.visit('/');
cy.visit('/users/123');
cy.go('back');
cy.go('forward');
cy.reload();
```

### Interactions

```typescript
// Click
cy.get('button').click();
cy.get('button').dblclick();
cy.get('button').rightclick();

// Type
cy.get('input').type('Hello World');
cy.get('input').type('test@email.com{enter}');
cy.get('input').clear().type('New value');

// Select
cy.get('select').select('Option 1');
cy.get('select').select(['opt1', 'opt2']);

// Checkbox/Radio
cy.get('input[type="checkbox"]').check();
cy.get('input[type="checkbox"]').uncheck();
cy.get('input[type="radio"]').check('value');

// File upload
cy.get('input[type="file"]').selectFile('cypress/fixtures/image.png');

// Scroll
cy.scrollTo('bottom');
cy.get('.container').scrollTo(0, 500);

// Focus/Blur
cy.get('input').focus();
cy.get('input').blur();
```

### Assertions

```typescript
// Visibility
cy.get('button').should('be.visible');
cy.get('.modal').should('not.exist');
cy.get('.loading').should('not.be.visible');

// Content
cy.get('h1').should('contain', 'Welcome');
cy.get('h1').should('have.text', 'Welcome Home');
cy.get('p').should('include.text', 'partial');

// Attributes
cy.get('input').should('have.value', 'test');
cy.get('a').should('have.attr', 'href', '/about');
cy.get('button').should('be.disabled');
cy.get('input').should('be.enabled');

// CSS
cy.get('div').should('have.class', 'active');
cy.get('div').should('have.css', 'display', 'flex');

// Length
cy.get('li').should('have.length', 5);
cy.get('li').should('have.length.greaterThan', 3);

// Chained
cy.get('input')
  .should('be.visible')
  .and('have.value', '')
  .and('be.enabled');
```

## Fixtures

### Load Fixture Data

```json
// cypress/fixtures/users.json
{
  "users": [
    { "id": 1, "name": "John", "email": "john@example.com" },
    { "id": 2, "name": "Jane", "email": "jane@example.com" }
  ]
}
```

```typescript
// In test
cy.fixture('users').then((data) => {
  const user = data.users[0];
  cy.get('[data-cy="email"]').type(user.email);
});

// Or with alias
beforeEach(() => {
  cy.fixture('users').as('usersData');
});

it('uses fixture data', function() {
  cy.get('[data-cy="email"]').type(this.usersData.users[0].email);
});
```

## API Testing

### cy.request

```typescript
describe('API Tests', () => {
  it('fetches users', () => {
    cy.request('GET', '/api/users').then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.have.length.greaterThan(0);
    });
  });

  it('creates a user', () => {
    cy.request({
      method: 'POST',
      url: '/api/users',
      body: {
        name: 'John Doe',
        email: 'john@example.com',
      },
    }).then((response) => {
      expect(response.status).to.eq(201);
      expect(response.body).to.have.property('id');
    });
  });

  it('handles auth', () => {
    cy.request({
      method: 'POST',
      url: '/api/login',
      body: { email: 'test@example.com', password: 'password' },
    }).then((response) => {
      expect(response.body).to.have.property('token');
      // Use token in subsequent requests
      cy.request({
        method: 'GET',
        url: '/api/profile',
        headers: {
          Authorization: `Bearer ${response.body.token}`,
        },
      });
    });
  });
});
```

### Intercept Network Requests

```typescript
describe('Mocking API', () => {
  it('mocks API response', () => {
    cy.intercept('GET', '/api/users', {
      statusCode: 200,
      body: [
        { id: 1, name: 'Mocked User' },
      ],
    }).as('getUsers');

    cy.visit('/users');
    cy.wait('@getUsers');
    cy.contains('Mocked User').should('be.visible');
  });

  it('mocks with fixture', () => {
    cy.intercept('GET', '/api/users', { fixture: 'users.json' }).as('getUsers');
    cy.visit('/users');
    cy.wait('@getUsers');
  });

  it('spies on requests', () => {
    cy.intercept('POST', '/api/users').as('createUser');

    cy.get('[data-cy="create-user-form"]').within(() => {
      cy.get('input[name="name"]').type('John');
      cy.get('button[type="submit"]').click();
    });

    cy.wait('@createUser').its('request.body').should('deep.equal', {
      name: 'John',
    });
  });

  it('delays response', () => {
    cy.intercept('GET', '/api/data', {
      delay: 2000,
      body: { data: 'slow response' },
    });

    cy.visit('/data');
    cy.get('.loading').should('be.visible');
    cy.get('.data').should('be.visible');
  });
});
```

## Custom Commands

```typescript
// cypress/support/commands.ts
declare global {
  namespace Cypress {
    interface Chainable {
      login(email: string, password: string): Chainable<void>;
      getByCy(selector: string): Chainable<JQuery<HTMLElement>>;
    }
  }
}

Cypress.Commands.add('login', (email, password) => {
  cy.session([email, password], () => {
    cy.visit('/login');
    cy.get('[data-cy="email"]').type(email);
    cy.get('[data-cy="password"]').type(password);
    cy.get('[data-cy="submit"]').click();
    cy.url().should('include', '/dashboard');
  });
});

Cypress.Commands.add('getByCy', (selector) => {
  return cy.get(`[data-cy="${selector}"]`);
});

export {};
```

```typescript
// Usage
describe('Dashboard', () => {
  beforeEach(() => {
    cy.login('test@example.com', 'password');
  });

  it('shows dashboard', () => {
    cy.visit('/dashboard');
    cy.getByCy('welcome-message').should('be.visible');
  });
});
```

## Component Testing

```typescript
// cypress/component/Button.cy.tsx
import Button from '../../src/components/Button';

describe('Button Component', () => {
  it('renders with text', () => {
    cy.mount(<Button>Click me</Button>);
    cy.contains('Click me').should('be.visible');
  });

  it('handles click', () => {
    const onClick = cy.stub().as('onClick');
    cy.mount(<Button onClick={onClick}>Click me</Button>);
    cy.get('button').click();
    cy.get('@onClick').should('have.been.calledOnce');
  });

  it('shows disabled state', () => {
    cy.mount(<Button disabled>Disabled</Button>);
    cy.get('button').should('be.disabled');
  });
});
```

## Waiting

```typescript
// Wait for element
cy.get('.loading').should('not.exist');
cy.get('.data').should('be.visible');

// Wait for network
cy.intercept('GET', '/api/data').as('getData');
cy.visit('/');
cy.wait('@getData');

// Wait for multiple
cy.wait(['@getUsers', '@getPosts']);

// Explicit wait (avoid when possible)
cy.wait(1000);
```

## Best Practices

1. **Use data-* attributes** - Stable selectors
2. **Don't use cy.wait(ms)** - Use assertions instead
3. **Reset state between tests** - Use beforeEach
4. **Use cy.session** - Cache authentication
5. **Use intercept for mocking** - Control network

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using arbitrary waits | Use assertions that retry |
| Brittle CSS selectors | Use data-testid attributes |
| Not cleaning up state | Use beforeEach/afterEach |
| Testing implementation | Test user behavior |
| Flaky tests | Use proper waiting strategies |

## Reference Files

- [references/commands.md](references/commands.md) - All commands
- [references/assertions.md](references/assertions.md) - Assertion types
- [references/ci.md](references/ci.md) - CI/CD integration
