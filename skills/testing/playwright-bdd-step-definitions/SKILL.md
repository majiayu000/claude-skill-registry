---
name: playwright-bdd-step-definitions
description: Use when creating step definitions with Given, When, Then, using createBdd() for step functions, implementing Page Object Model patterns, and sharing fixtures between steps.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# Playwright BDD Step Definitions

Expert knowledge of creating step definitions for Playwright BDD, including step functions, parameter types, fixtures, and Page Object Model integration.

## Overview

Step definitions connect Gherkin steps in feature files to executable code. Playwright BDD uses `createBdd()` to generate type-safe step definition functions that integrate with Playwright's fixtures and assertions.

## Basic Step Definitions

### Creating Step Functions

```typescript
// steps/common.steps.ts
import { createBdd } from 'playwright-bdd';

const { Given, When, Then } = createBdd();

Given('I am on the home page', async ({ page }) => {
  await page.goto('/');
});

When('I click the login button', async ({ page }) => {
  await page.getByRole('button', { name: 'Login' }).click();
});

Then('I should see the dashboard', async ({ page }) => {
  await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
});
```

### Step with Playwright Fixtures

All Playwright fixtures are available in step definitions:

```typescript
import { createBdd } from 'playwright-bdd';

const { Given, When, Then } = createBdd();

Given('I am logged in as {string}', async ({ page, context }, username: string) => {
  // Access page and context fixtures
  await page.goto('/login');
  await page.getByLabel('Username').fill(username);
  await page.getByRole('button', { name: 'Login' }).click();
});

When('I take a screenshot', async ({ page }) => {
  await page.screenshot({ path: 'screenshot.png' });
});

Then('the browser has {int} cookies', async ({ context }, count: number) => {
  const cookies = await context.cookies();
  expect(cookies).toHaveLength(count);
});
```

## Parameter Types

### Built-in Parameters

```typescript
// String parameter: {string}
Given('the user name is {string}', async ({}, name: string) => {
  console.log(name); // "John"
});

// Integer parameter: {int}
When('I wait {int} seconds', async ({}, seconds: number) => {
  await page.waitForTimeout(seconds * 1000);
});

// Float parameter: {float}
Then('the price is {float}', async ({}, price: number) => {
  console.log(price); // 19.99
});

// Word parameter: {word}
Given('I am on the {word} page', async ({ page }, pageName: string) => {
  await page.goto(`/${pageName}`);
});
```

### Anonymous Parameters

Use regex capture groups for flexible matching:

```typescript
// Match any text in quotes
Given(/^I enter "(.*)" in the search box$/, async ({ page }, query: string) => {
  await page.getByRole('searchbox').fill(query);
});

// Match numbers
When(/^I add (\d+) items to cart$/, async ({ page }, count: string) => {
  const quantity = parseInt(count, 10);
  for (let i = 0; i < quantity; i++) {
    await page.getByRole('button', { name: 'Add to Cart' }).click();
  }
});
```

### Custom Parameter Types

Define reusable parameter types:

```typescript
// steps/parameters.ts
import { defineParameterType } from 'playwright-bdd';

defineParameterType({
  name: 'color',
  regexp: /red|green|blue/,
  transformer: (s) => s,
});

defineParameterType({
  name: 'boolean',
  regexp: /true|false/,
  transformer: (s) => s === 'true',
});

defineParameterType({
  name: 'date',
  regexp: /\d{4}-\d{2}-\d{2}/,
  transformer: (s) => new Date(s),
});
```

Using custom parameters:

```typescript
// steps/ui.steps.ts
import { createBdd } from 'playwright-bdd';
import './parameters'; // Import parameter definitions

const { Given, When, Then } = createBdd();

When('I select the {color} theme', async ({ page }, color: string) => {
  await page.getByRole('button', { name: color }).click();
});

Then('dark mode is {boolean}', async ({ page }, enabled: boolean) => {
  if (enabled) {
    await expect(page.locator('body')).toHaveClass(/dark/);
  }
});
```

## Custom Fixtures

### Creating Custom Fixtures

```typescript
// steps/fixtures.ts
import { test as base, createBdd } from 'playwright-bdd';

// Define fixture types
type TestFixtures = {
  todoPage: TodoPage;
  apiClient: ApiClient;
};

// Extend base test with fixtures
export const test = base.extend<TestFixtures>({
  todoPage: async ({ page }, use) => {
    const todoPage = new TodoPage(page);
    await use(todoPage);
  },

  apiClient: async ({ request }, use) => {
    const client = new ApiClient(request);
    await use(client);
  },
});

// Create BDD functions with custom test
export const { Given, When, Then } = createBdd(test);
```

### Using Custom Fixtures in Steps

```typescript
// steps/todo.steps.ts
import { Given, When, Then } from './fixtures';

Given('I have an empty todo list', async ({ todoPage }) => {
  await todoPage.goto();
  await todoPage.clearAll();
});

When('I add a todo {string}', async ({ todoPage }, text: string) => {
  await todoPage.addTodo(text);
});

Then('I should see {int} todos', async ({ todoPage }, count: number) => {
  await todoPage.expectTodoCount(count);
});
```

### Fixture with Setup and Teardown

```typescript
// steps/fixtures.ts
import { test as base, createBdd } from 'playwright-bdd';

export const test = base.extend<{
  authenticatedPage: Page;
}>({
  authenticatedPage: async ({ page, context }, use) => {
    // Setup: Login before test
    await page.goto('/login');
    await page.getByLabel('Email').fill('test@example.com');
    await page.getByLabel('Password').fill('password');
    await page.getByRole('button', { name: 'Login' }).click();
    await page.waitForURL('/dashboard');

    // Use the authenticated page
    await use(page);

    // Teardown: Logout after test
    await page.goto('/logout');
  },
});

export const { Given, When, Then } = createBdd(test);
```

## Page Object Model

### Page Object Definition

```typescript
// pages/TodoPage.ts
import { Page, Locator, expect } from '@playwright/test';

export class TodoPage {
  readonly page: Page;
  readonly input: Locator;
  readonly list: Locator;
  readonly items: Locator;

  constructor(page: Page) {
    this.page = page;
    this.input = page.getByPlaceholder('What needs to be done?');
    this.list = page.getByRole('list');
    this.items = page.getByTestId('todo-item');
  }

  async goto() {
    await this.page.goto('/todos');
  }

  async addTodo(text: string) {
    await this.input.fill(text);
    await this.input.press('Enter');
  }

  async removeTodo(text: string) {
    const item = this.items.filter({ hasText: text });
    await item.hover();
    await item.getByRole('button', { name: 'Delete' }).click();
  }

  async toggleTodo(text: string) {
    const item = this.items.filter({ hasText: text });
    await item.getByRole('checkbox').click();
  }

  async expectTodoCount(count: number) {
    await expect(this.items).toHaveCount(count);
  }

  async expectTodoVisible(text: string) {
    await expect(this.items.filter({ hasText: text })).toBeVisible();
  }

  async clearAll() {
    const count = await this.items.count();
    for (let i = count - 1; i >= 0; i--) {
      await this.items.nth(i).hover();
      await this.items.nth(i).getByRole('button', { name: 'Delete' }).click();
    }
  }
}
```

### Integrating Page Objects with Steps

```typescript
// steps/fixtures.ts
import { test as base, createBdd } from 'playwright-bdd';
import { TodoPage } from '../pages/TodoPage';
import { LoginPage } from '../pages/LoginPage';

export const test = base.extend<{
  todoPage: TodoPage;
  loginPage: LoginPage;
}>({
  todoPage: async ({ page }, use) => {
    await use(new TodoPage(page));
  },
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));
  },
});

export const { Given, When, Then } = createBdd(test);
```

```typescript
// steps/todo.steps.ts
import { Given, When, Then } from './fixtures';

Given('I am on the todo page', async ({ todoPage }) => {
  await todoPage.goto();
});

When('I add {string} to my todos', async ({ todoPage }, text: string) => {
  await todoPage.addTodo(text);
});

When('I complete the todo {string}', async ({ todoPage }, text: string) => {
  await todoPage.toggleTodo(text);
});

When('I remove the todo {string}', async ({ todoPage }, text: string) => {
  await todoPage.removeTodo(text);
});

Then('I should see the todo {string}', async ({ todoPage }, text: string) => {
  await todoPage.expectTodoVisible(text);
});

Then('there should be {int} todos', async ({ todoPage }, count: number) => {
  await todoPage.expectTodoCount(count);
});
```

## Decorator-Based Steps

### Using Decorators with Classes

```typescript
// steps/TodoSteps.ts
import { Fixture, Given, When, Then } from 'playwright-bdd/decorators';
import { test } from './fixtures';

export
@Fixture<typeof test>('todoPage')
class TodoSteps {
  @Given('I am on the todo page')
  async gotoTodoPage() {
    await this.todoPage.goto();
  }

  @When('I add {string} to my todos')
  async addTodo(text: string) {
    await this.todoPage.addTodo(text);
  }

  @Then('I should see {int} todos')
  async checkTodoCount(count: number) {
    await this.todoPage.expectTodoCount(count);
  }
}
```

### Multiple Fixtures in Decorators

```typescript
// steps/AuthenticatedSteps.ts
import { Fixture, Given, When, Then } from 'playwright-bdd/decorators';
import { test } from './fixtures';

export
@Fixture<typeof test>('loginPage')
@Fixture<typeof test>('todoPage')
class AuthenticatedSteps {
  @Given('I am logged in')
  async login() {
    await this.loginPage.login('user@example.com', 'password');
  }

  @When('I visit my todos')
  async visitTodos() {
    await this.todoPage.goto();
  }
}
```

## Data Tables

### Simple Tables

```gherkin
When I add the following todos:
  | Buy milk  |
  | Buy bread |
  | Buy eggs  |
```

```typescript
import { DataTable } from '@cucumber/cucumber';

When('I add the following todos:', async ({ todoPage }, table: DataTable) => {
  const todos = table.raw().flat();
  for (const todo of todos) {
    await todoPage.addTodo(todo);
  }
});
```

### Tables with Headers

```gherkin
When I create users:
  | name  | email           | role  |
  | Alice | alice@test.com  | admin |
  | Bob   | bob@test.com    | user  |
```

```typescript
When('I create users:', async ({ page }, table: DataTable) => {
  const users = table.hashes(); // [{ name: 'Alice', email: '...', role: 'admin' }, ...]
  for (const user of users) {
    await page.getByLabel('Name').fill(user.name);
    await page.getByLabel('Email').fill(user.email);
    await page.getByLabel('Role').selectOption(user.role);
    await page.getByRole('button', { name: 'Create' }).click();
  }
});
```

### Vertical Tables

```gherkin
When I fill the form:
  | Name     | John Doe        |
  | Email    | john@example.com|
  | Password | secret123       |
```

```typescript
When('I fill the form:', async ({ page }, table: DataTable) => {
  const data = table.rowsHash(); // { Name: 'John Doe', Email: '...', Password: '...' }
  await page.getByLabel('Name').fill(data.Name);
  await page.getByLabel('Email').fill(data.Email);
  await page.getByLabel('Password').fill(data.Password);
});
```

## Doc Strings

### Multi-line Text Input

```gherkin
When I write the following review:
  """
  This product is amazing!
  I highly recommend it to everyone.
  Five stars!
  """
```

```typescript
When('I write the following review:', async ({ page }, docString: string) => {
  await page.getByRole('textbox', { name: 'Review' }).fill(docString);
});
```

### JSON Data

```gherkin
When I send the API request:
  """json
  {
    "name": "Test Product",
    "price": 29.99,
    "category": "electronics"
  }
  """
```

```typescript
When('I send the API request:', async ({ request }, docString: string) => {
  const data = JSON.parse(docString);
  await request.post('/api/products', { data });
});
```

## Sharing State Between Steps

### Using World/Context

```typescript
// steps/fixtures.ts
import { test as base, createBdd } from 'playwright-bdd';

type World = {
  currentUser?: { id: string; name: string };
  createdItems: string[];
};

export const test = base.extend<{ world: World }>({
  world: async ({}, use) => {
    await use({
      createdItems: [],
    });
  },
});

export const { Given, When, Then } = createBdd(test);
```

```typescript
// steps/user.steps.ts
import { Given, When, Then } from './fixtures';

Given('I am logged in as {string}', async ({ page, world }, name: string) => {
  world.currentUser = { id: '123', name };
  await page.goto('/login');
  // ... login steps
});

When('I create an item {string}', async ({ world }, item: string) => {
  world.createdItems.push(item);
  // ... create item
});

Then('I should see my items', async ({ page, world }) => {
  for (const item of world.createdItems) {
    await expect(page.getByText(item)).toBeVisible();
  }
});
```

## Error Handling

### Pending Steps

```typescript
Given('a feature not yet implemented', async ({}) => {
  throw new Error('Step not implemented');
});
```

### Skip Steps Conditionally

```typescript
Given('I am on a supported browser', async ({ browserName }) => {
  if (browserName === 'webkit') {
    test.skip(true, 'Feature not supported on WebKit');
  }
  // Continue with test
});
```

## Best Practices

### Step Reusability

Write generic steps that work across multiple scenarios:

```typescript
// Generic navigation step
Given('I am on the {string} page', async ({ page }, pageName: string) => {
  const routes: Record<string, string> = {
    home: '/',
    login: '/login',
    dashboard: '/dashboard',
    settings: '/settings',
  };
  await page.goto(routes[pageName] || `/${pageName}`);
});

// Generic form fill step
When('I fill in {string} with {string}', async ({ page }, label: string, value: string) => {
  await page.getByLabel(label).fill(value);
});

// Generic click step
When('I click {string}', async ({ page }, text: string) => {
  await page.getByRole('button', { name: text }).or(
    page.getByRole('link', { name: text })
  ).click();
});
```

### Step Organization

Organize steps by domain:

```
steps/
├── fixtures.ts          # Shared fixtures
├── parameters.ts        # Custom parameter types
├── common/
│   ├── navigation.steps.ts
│   └── forms.steps.ts
├── auth/
│   ├── login.steps.ts
│   └── logout.steps.ts
└── products/
    ├── catalog.steps.ts
    └── cart.steps.ts
```

### Assertions

Use Playwright's expect for assertions:

```typescript
import { expect } from '@playwright/test';

Then('I should see {string}', async ({ page }, text: string) => {
  await expect(page.getByText(text)).toBeVisible();
});

Then('the page title should be {string}', async ({ page }, title: string) => {
  await expect(page).toHaveTitle(title);
});

Then('the URL should contain {string}', async ({ page }, path: string) => {
  await expect(page).toHaveURL(new RegExp(path));
});
```

## When to Use This Skill

- Creating new step definitions
- Implementing Page Object Model with BDD
- Setting up custom fixtures
- Using data tables and doc strings
- Sharing state between steps
- Writing reusable generic steps
- Converting Cucumber steps to Playwright BDD
- Troubleshooting step matching issues
