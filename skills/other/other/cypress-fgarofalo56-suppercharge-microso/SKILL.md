---
name: cypress
description: Write end-to-end tests with Cypress including browser automation, API testing, component testing, and visual regression. Use for E2E testing, integration testing, or frontend QA automation.
---

# Cypress E2E Testing

## Quick Reference

| Command | Purpose |
|---------|---------|
| `npx cypress open` | Open Cypress GUI |
| `npx cypress run` | Run tests headless |
| `npx cypress run --spec "path"` | Run specific test |
| `npx cypress run --browser chrome` | Use specific browser |

## 1. Setup

### Installation

```bash
npm install --save-dev cypress
npx cypress open  # First run creates folder structure
```

### Configuration (cypress.config.js)

```javascript
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    viewportWidth: 1280,
    viewportHeight: 720,
    video: true,
    screenshotOnRunFailure: true,
    defaultCommandTimeout: 10000,
    requestTimeout: 10000,
    responseTimeout: 30000,
    retries: {
      runMode: 2,
      openMode: 0
    },
    env: {
      apiUrl: 'http://localhost:3001/api'
    },
    setupNodeEvents(on, config) {
      // Plugins
      return config;
    }
  },
  component: {
    devServer: {
      framework: 'react',
      bundler: 'vite'
    }
  }
});
```

### Project Structure

```
cypress/
├── e2e/                    # E2E test files
│   ├── auth/
│   │   └── login.cy.js
│   └── dashboard/
│       └── dashboard.cy.js
├── fixtures/               # Test data
│   └── users.json
├── support/
│   ├── commands.js         # Custom commands
│   └── e2e.js             # Global hooks
└── downloads/              # Downloaded files
```

## 2. Basic Tests

### Test Structure

```javascript
describe('Login Page', () => {
  beforeEach(() => {
    cy.visit('/login');
  });

  it('displays login form', () => {
    cy.get('[data-cy=email]').should('be.visible');
    cy.get('[data-cy=password]').should('be.visible');
    cy.get('[data-cy=submit]').should('contain', 'Login');
  });

  it('shows error for invalid credentials', () => {
    cy.get('[data-cy=email]').type('invalid@example.com');
    cy.get('[data-cy=password]').type('wrongpassword');
    cy.get('[data-cy=submit]').click();

    cy.get('[data-cy=error]')
      .should('be.visible')
      .and('contain', 'Invalid credentials');
  });

  it('redirects to dashboard on success', () => {
    cy.get('[data-cy=email]').type('user@example.com');
    cy.get('[data-cy=password]').type('password123');
    cy.get('[data-cy=submit]').click();

    cy.url().should('include', '/dashboard');
    cy.get('[data-cy=welcome]').should('contain', 'Welcome');
  });

  it.skip('skipped test', () => {
    // This test is skipped
  });

  it.only('only this test runs', () => {
    // Only this test runs in this describe block
  });
});
```

### Selectors

```javascript
// Best practice: Use data-cy attributes
cy.get('[data-cy=submit-button]');

// CSS selectors
cy.get('.btn-primary');
cy.get('#login-form');
cy.get('button[type="submit"]');

// Contains text
cy.contains('Submit');
cy.contains('button', 'Submit');

// Find within element
cy.get('.form').find('input');
cy.get('.form').within(() => {
  cy.get('input').first().type('text');
});

// Parent/child navigation
cy.get('input').parent();
cy.get('.list').children();
cy.get('li').first();
cy.get('li').last();
cy.get('li').eq(2);  // Third item
```

## 3. Actions

### Typing and Clicking

```javascript
// Type text
cy.get('input').type('Hello World');
cy.get('input').type('Hello{enter}');  // With Enter key
cy.get('input').type('{selectall}{backspace}');  // Clear
cy.get('input').clear().type('New text');

// Special keys
cy.get('input').type('{ctrl+a}');
cy.get('input').type('{shift}{alt}');
cy.get('input').type('{moveToEnd}');

// Clicking
cy.get('button').click();
cy.get('button').click({ force: true });  // Force click
cy.get('button').dblclick();
cy.get('button').rightclick();
cy.get('.area').click(50, 100);  // Coordinates

// Multiple elements
cy.get('.checkbox').click({ multiple: true });
```

### Form Interactions

```javascript
// Select dropdown
cy.get('select').select('Option 1');
cy.get('select').select(['Option 1', 'Option 2']);  // Multi-select

// Checkbox/Radio
cy.get('[type="checkbox"]').check();
cy.get('[type="checkbox"]').uncheck();
cy.get('[type="radio"]').check('value');

// File upload
cy.get('input[type="file"]').selectFile('cypress/fixtures/image.png');
cy.get('input[type="file"]').selectFile([
  'cypress/fixtures/file1.pdf',
  'cypress/fixtures/file2.pdf'
]);

// Focus/blur
cy.get('input').focus();
cy.get('input').blur();

// Scroll
cy.get('.container').scrollTo('bottom');
cy.get('.element').scrollIntoView();
cy.scrollTo(0, 500);
```

## 4. Assertions

```javascript
// Should assertions
cy.get('h1').should('be.visible');
cy.get('button').should('be.disabled');
cy.get('input').should('have.value', 'text');
cy.get('.list').should('have.length', 5);
cy.get('a').should('have.attr', 'href', '/about');
cy.get('div').should('have.class', 'active');
cy.get('p').should('contain', 'Hello');
cy.get('.item').should('exist');
cy.get('.modal').should('not.exist');

// Chained assertions
cy.get('button')
  .should('be.visible')
  .and('be.enabled')
  .and('contain', 'Submit');

// Callback assertions
cy.get('input').should(($input) => {
  expect($input).to.have.value('expected');
  expect($input.attr('placeholder')).to.eq('Enter text');
});

// Wait for condition
cy.get('.loading').should('not.exist');
cy.get('.data').should('have.length.greaterThan', 0);
```

## 5. API Testing

### Intercept and Stub

```javascript
describe('API Interactions', () => {
  it('stubs API response', () => {
    cy.intercept('GET', '/api/users', {
      statusCode: 200,
      body: [{ id: 1, name: 'John' }]
    }).as('getUsers');

    cy.visit('/users');
    cy.wait('@getUsers');

    cy.get('.user').should('have.length', 1);
  });

  it('stubs with fixture', () => {
    cy.intercept('GET', '/api/users', {
      fixture: 'users.json'
    }).as('getUsers');

    cy.visit('/users');
    cy.wait('@getUsers');
  });

  it('modifies response', () => {
    cy.intercept('GET', '/api/users', (req) => {
      req.continue((res) => {
        res.body.push({ id: 999, name: 'Injected' });
      });
    });
  });

  it('delays response', () => {
    cy.intercept('GET', '/api/users', (req) => {
      req.continue((res) => {
        res.delay = 2000;
      });
    });
  });

  it('simulates error', () => {
    cy.intercept('GET', '/api/users', {
      statusCode: 500,
      body: { error: 'Server error' }
    });

    cy.visit('/users');
    cy.get('.error').should('contain', 'Something went wrong');
  });
});
```

### Make API Requests

```javascript
it('tests API directly', () => {
  cy.request('GET', '/api/users').then((response) => {
    expect(response.status).to.eq(200);
    expect(response.body).to.have.length.greaterThan(0);
  });

  cy.request({
    method: 'POST',
    url: '/api/users',
    body: { name: 'John', email: 'john@example.com' },
    headers: { Authorization: 'Bearer token' }
  }).then((response) => {
    expect(response.status).to.eq(201);
    expect(response.body.id).to.exist;
  });
});
```

## 6. Custom Commands

### Define Commands (support/commands.js)

```javascript
// Login command
Cypress.Commands.add('login', (email, password) => {
  cy.session([email, password], () => {
    cy.visit('/login');
    cy.get('[data-cy=email]').type(email);
    cy.get('[data-cy=password]').type(password);
    cy.get('[data-cy=submit]').click();
    cy.url().should('include', '/dashboard');
  });
});

// API login command
Cypress.Commands.add('apiLogin', (email, password) => {
  cy.request({
    method: 'POST',
    url: '/api/auth/login',
    body: { email, password }
  }).then((response) => {
    window.localStorage.setItem('token', response.body.token);
  });
});

// Custom assertion
Cypress.Commands.add('shouldBeWithinRange', { prevSubject: true }, (subject, min, max) => {
  const value = parseFloat(subject.text());
  expect(value).to.be.within(min, max);
});

// Drag and drop
Cypress.Commands.add('dragTo', { prevSubject: true }, (subject, targetSelector) => {
  cy.wrap(subject).trigger('dragstart');
  cy.get(targetSelector).trigger('drop');
  cy.wrap(subject).trigger('dragend');
});
```

### Use Custom Commands

```javascript
describe('Dashboard', () => {
  beforeEach(() => {
    cy.login('user@example.com', 'password123');
  });

  it('shows user data', () => {
    cy.visit('/dashboard');
    cy.get('[data-cy=user-name]').should('contain', 'John');
  });
});
```

## 7. Fixtures

### Create Fixtures

```json
// cypress/fixtures/users.json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  },
  {
    "id": 2,
    "name": "Jane Smith",
    "email": "jane@example.com"
  }
]
```

### Use Fixtures

```javascript
describe('Users', () => {
  beforeEach(() => {
    cy.fixture('users.json').as('usersData');
  });

  it('uses fixture data', function() {
    // Note: Use function() not arrow for 'this' context
    cy.intercept('GET', '/api/users', this.usersData);
    cy.visit('/users');
    cy.get('.user').should('have.length', 2);
  });

  it('uses fixture inline', () => {
    cy.fixture('users.json').then((users) => {
      cy.intercept('GET', '/api/users', users);
    });
  });
});
```

## 8. Page Objects

```javascript
// cypress/support/pages/LoginPage.js
class LoginPage {
  elements = {
    emailInput: () => cy.get('[data-cy=email]'),
    passwordInput: () => cy.get('[data-cy=password]'),
    submitButton: () => cy.get('[data-cy=submit]'),
    errorMessage: () => cy.get('[data-cy=error]')
  };

  visit() {
    cy.visit('/login');
    return this;
  }

  typeEmail(email) {
    this.elements.emailInput().type(email);
    return this;
  }

  typePassword(password) {
    this.elements.passwordInput().type(password);
    return this;
  }

  submit() {
    this.elements.submitButton().click();
    return this;
  }

  login(email, password) {
    this.typeEmail(email);
    this.typePassword(password);
    this.submit();
    return this;
  }

  assertError(message) {
    this.elements.errorMessage()
      .should('be.visible')
      .and('contain', message);
    return this;
  }
}

export default new LoginPage();

// Usage in tests
import loginPage from '../support/pages/LoginPage';

describe('Login', () => {
  it('shows error for invalid login', () => {
    loginPage
      .visit()
      .login('invalid@email.com', 'wrong')
      .assertError('Invalid credentials');
  });
});
```

## 9. Visual Testing

```javascript
// Install cypress-image-snapshot
// npm install --save-dev cypress-image-snapshot

// In support/commands.js
import { addMatchImageSnapshotCommand } from 'cypress-image-snapshot/command';
addMatchImageSnapshotCommand();

// In tests
describe('Visual Regression', () => {
  it('matches homepage snapshot', () => {
    cy.visit('/');
    cy.matchImageSnapshot('homepage');
  });

  it('matches component snapshot', () => {
    cy.get('.header').matchImageSnapshot('header');
  });
});
```

## 10. Environment and CI

### Environment Variables

```javascript
// cypress.config.js
env: {
  apiUrl: 'http://localhost:3001',
  username: 'testuser'
}

// Access in tests
cy.visit(Cypress.env('apiUrl') + '/users');

// CLI override
// npx cypress run --env apiUrl=http://staging.example.com
```

### CI Configuration (GitHub Actions)

```yaml
name: Cypress Tests
on: [push]

jobs:
  cypress:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: cypress-io/github-action@v6
        with:
          build: npm run build
          start: npm start
          wait-on: 'http://localhost:3000'
          record: true
        env:
          CYPRESS_RECORD_KEY: ${{ secrets.CYPRESS_RECORD_KEY }}
```

## Best Practices

1. **Use data-cy attributes** - Stable selectors
2. **Don't use cy.wait(ms)** - Use assertions instead
3. **Keep tests independent** - No shared state
4. **Use custom commands** - DRY test code
5. **Intercept API calls** - Control responses
6. **Use fixtures** - Consistent test data
7. **Implement retries** - Handle flakiness
8. **Run in CI** - Automated testing
9. **Use Page Objects** - For complex apps
10. **Test critical paths first** - Prioritize coverage
