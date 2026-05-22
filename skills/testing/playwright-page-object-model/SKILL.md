---
name: playwright-page-object-model
description: Use when creating page objects or refactoring Playwright tests for better maintainability with Page Object Model patterns.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Playwright Page Object Model

Master the Page Object Model (POM) pattern to create maintainable, reusable,
and scalable test automation code. This skill covers modern Playwright
patterns including component-based architecture, locator strategies, and
app actions.

## Core POM Principles

### Single Responsibility

Each page object should represent one page or component with a single,
well-defined responsibility.

### Encapsulation

Hide implementation details and expose only meaningful actions and
assertions.

### Reusability

Create reusable components that can be composed into larger page objects.

### Maintainability

When UI changes, update page objects in one place rather than across
multiple tests.

## Basic Page Object Pattern

### Simple Page Object

```typescript
// pages/login-page.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel('Email');
    this.passwordInput = page.getByLabel('Password');
    this.loginButton = page.getByRole('button', { name: 'Login' });
    this.errorMessage = page.getByRole('alert');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }

  async getErrorMessage() {
    return await this.errorMessage.textContent();
  }
}
```

### Using Page Object in Tests

```typescript
// tests/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/login-page';

test.describe('Login', () => {
  test('should login successfully', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('user@example.com', 'password123');

    await expect(page).toHaveURL('/dashboard');
  });

  test('should show error on invalid credentials', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('user@example.com', 'wrongpassword');

    const error = await loginPage.getErrorMessage();
    expect(error).toContain('Invalid credentials');
  });
});
```

## Locator Strategies

### Recommended Locator Priority

1. User-visible locators (getByRole, getByText, getByLabel)
2. Test IDs (getByTestId)
3. CSS/XPath (only as last resort)

### User-Visible Locators

```typescript
export class HomePage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  // By role (ARIA role)
  get searchButton() {
    return this.page.getByRole('button', { name: 'Search' });
  }

  // By label (form inputs)
  get searchInput() {
    return this.page.getByLabel('Search products');
  }

  // By text
  get welcomeMessage() {
    return this.page.getByText('Welcome back');
  }

  // By placeholder
  get emailInput() {
    return this.page.getByPlaceholder('Enter your email');
  }

  // By alt text (images)
  get logo() {
    return this.page.getByAltText('Company Logo');
  }

  // By title
  get helpIcon() {
    return this.page.getByTitle('Help');
  }
}
```

### Test ID Locators

```typescript
// Component with test IDs
// <button data-testid="submit-button">Submit</button>

export class FormPage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  get submitButton() {
    return this.page.getByTestId('submit-button');
  }

  get formContainer() {
    return this.page.getByTestId('form-container');
  }
}
```

### Locator Chaining

```typescript
export class ProductPage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  // Chain locators for specificity
  get priceInCart() {
    return this.page
      .getByTestId('shopping-cart')
      .getByRole('cell', { name: 'Price' });
  }

  // Filter locators
  getProductByName(name: string) {
    return this.page
      .getByRole('listitem')
      .filter({ hasText: name });
  }

  // Nth element
  get firstProduct() {
    return this.page.getByRole('article').nth(0);
  }
}
```

## Component-Based Architecture

### Reusable Component Objects

```typescript
// components/navigation.ts
export class Navigation {
  readonly page: Page;
  readonly homeLink: Locator;
  readonly productsLink: Locator;
  readonly cartLink: Locator;
  readonly profileMenu: Locator;

  constructor(page: Page) {
    this.page = page;
    this.homeLink = page.getByRole('link', { name: 'Home' });
    this.productsLink = page.getByRole('link', { name: 'Products' });
    this.cartLink = page.getByRole('link', { name: 'Cart' });
    this.profileMenu = page.getByRole('button', { name: 'Profile' });
  }

  async navigateToHome() {
    await this.homeLink.click();
  }

  async navigateToProducts() {
    await this.productsLink.click();
  }

  async navigateToCart() {
    await this.cartLink.click();
  }

  async openProfileMenu() {
    await this.profileMenu.click();
  }
}
```

### Composing Page Objects with Components

```typescript
// pages/base-page.ts
import { Page } from '@playwright/test';
import { Navigation } from '../components/navigation';
import { Footer } from '../components/footer';

export class BasePage {
  readonly page: Page;
  readonly navigation: Navigation;
  readonly footer: Footer;

  constructor(page: Page) {
    this.page = page;
    this.navigation = new Navigation(page);
    this.footer = new Footer(page);
  }
}
```

```typescript
// pages/product-page.ts
import { BasePage } from './base-page';
import { Page } from '@playwright/test';

export class ProductPage extends BasePage {
  readonly addToCartButton: Locator;
  readonly productTitle: Locator;
  readonly productPrice: Locator;

  constructor(page: Page) {
    super(page);
    this.addToCartButton = page.getByRole('button', { name: 'Add to Cart' });
    this.productTitle = page.getByRole('heading', { level: 1 });
    this.productPrice = page.getByTestId('product-price');
  }

  async goto(productId: string) {
    await this.page.goto(`/products/${productId}`);
  }

  async addToCart() {
    await this.addToCartButton.click();
    // Wait for cart update
    await this.page.waitForResponse(
      (response) => response.url().includes('/api/cart')
    );
  }

  async getProductTitle() {
    return await this.productTitle.textContent();
  }

  async getProductPrice() {
    const text = await this.productPrice.textContent();
    return parseFloat(text?.replace('$', '') || '0');
  }
}
```

### Modal and Dialog Components

```typescript
// components/modal.ts
export class Modal {
  readonly page: Page;
  readonly container: Locator;
  readonly closeButton: Locator;
  readonly title: Locator;

  constructor(page: Page) {
    this.page = page;
    this.container = page.getByRole('dialog');
    this.closeButton = this.container.getByRole('button', { name: 'Close' });
    this.title = this.container.getByRole('heading');
  }

  async isVisible() {
    return await this.container.isVisible();
  }

  async getTitle() {
    return await this.title.textContent();
  }

  async close() {
    await this.closeButton.click();
    await this.container.waitFor({ state: 'hidden' });
  }
}
```

```typescript
// components/confirmation-modal.ts
import { Modal } from './modal';
import { Page } from '@playwright/test';

export class ConfirmationModal extends Modal {
  readonly confirmButton: Locator;
  readonly cancelButton: Locator;
  readonly message: Locator;

  constructor(page: Page) {
    super(page);
    this.confirmButton = this.container.getByRole('button', {
      name: 'Confirm',
    });
    this.cancelButton = this.container.getByRole('button', {
      name: 'Cancel',
    });
    this.message = this.container.getByTestId('modal-message');
  }

  async confirm() {
    await this.confirmButton.click();
    await this.container.waitFor({ state: 'hidden' });
  }

  async cancel() {
    await this.cancelButton.click();
    await this.container.waitFor({ state: 'hidden' });
  }

  async getMessage() {
    return await this.message.textContent();
  }
}
```

## App Actions Pattern

### High-Level Actions

```typescript
// pages/app-actions.ts
import { Page } from '@playwright/test';
import { LoginPage } from './login-page';
import { ProductPage } from './product-page';

export class AppActions {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async login(email: string, password: string) {
    const loginPage = new LoginPage(this.page);
    await loginPage.goto();
    await loginPage.login(email, password);
    await this.page.waitForURL('/dashboard');
  }

  async addProductToCart(productId: string) {
    const productPage = new ProductPage(this.page);
    await productPage.goto(productId);
    await productPage.addToCart();
  }

  async completeCheckout(paymentDetails: PaymentDetails) {
    await this.page.goto('/checkout');
    await this.fillShippingInfo(paymentDetails.shipping);
    await this.fillPaymentInfo(paymentDetails.payment);
    await this.page.getByRole('button', { name: 'Place Order' }).click();
    await this.page.waitForURL('/order-confirmation');
  }

  private async fillShippingInfo(shipping: ShippingInfo) {
    await this.page.getByLabel('Full Name').fill(shipping.name);
    await this.page.getByLabel('Address').fill(shipping.address);
    await this.page.getByLabel('City').fill(shipping.city);
    await this.page.getByLabel('Postal Code').fill(shipping.postalCode);
  }

  private async fillPaymentInfo(payment: PaymentInfo) {
    await this.page.getByLabel('Card Number').fill(payment.cardNumber);
    await this.page.getByLabel('Expiry Date').fill(payment.expiry);
    await this.page.getByLabel('CVV').fill(payment.cvv);
  }
}

interface PaymentDetails {
  shipping: ShippingInfo;
  payment: PaymentInfo;
}

interface ShippingInfo {
  name: string;
  address: string;
  city: string;
  postalCode: string;
}

interface PaymentInfo {
  cardNumber: string;
  expiry: string;
  cvv: string;
}
```

### Using App Actions in Tests

```typescript
// tests/checkout.spec.ts
import { test, expect } from '@playwright/test';
import { AppActions } from '../pages/app-actions';

test('should complete checkout flow', async ({ page }) => {
  const app = new AppActions(page);

  await app.login('user@example.com', 'password123');
  await app.addProductToCart('product-123');
  await app.completeCheckout({
    shipping: {
      name: 'John Doe',
      address: '123 Main St',
      city: 'New York',
      postalCode: '10001',
    },
    payment: {
      cardNumber: '4111111111111111',
      expiry: '12/25',
      cvv: '123',
    },
  });

  await expect(page.getByText('Order confirmed')).toBeVisible();
});
```

## Advanced Patterns

### Generic Table Component

```typescript
// components/table.ts
export class Table {
  readonly page: Page;
  readonly container: Locator;

  constructor(page: Page, testId?: string) {
    this.page = page;
    this.container = testId
      ? page.getByTestId(testId)
      : page.getByRole('table');
  }

  async getHeaders() {
    const headers = await this.container
      .getByRole('columnheader')
      .allTextContents();
    return headers;
  }

  async getRowCount() {
    return await this.container.getByRole('row').count() - 1; // Exclude header
  }

  async getRow(index: number) {
    return this.container.getByRole('row').nth(index + 1); // Skip header
  }

  async getCellValue(row: number, column: number) {
    const rowLocator = await this.getRow(row);
    const cell = rowLocator.getByRole('cell').nth(column);
    return await cell.textContent();
  }

  async getCellByColumnName(row: number, columnName: string) {
    const headers = await this.getHeaders();
    const columnIndex = headers.indexOf(columnName);
    if (columnIndex === -1) {
      throw new Error(`Column "${columnName}" not found`);
    }
    return await this.getCellValue(row, columnIndex);
  }

  async findRowByValue(columnName: string, value: string) {
    const headers = await this.getHeaders();
    const columnIndex = headers.indexOf(columnName);
    const rowCount = await this.getRowCount();

    for (let i = 0; i < rowCount; i++) {
      const cellValue = await this.getCellValue(i, columnIndex);
      if (cellValue === value) {
        return await this.getRow(i);
      }
    }

    return null;
  }
}
```

### Form Component with Validation

```typescript
// components/form.ts
export class Form {
  readonly page: Page;
  readonly container: Locator;
  readonly submitButton: Locator;

  constructor(page: Page, formTestId: string) {
    this.page = page;
    this.container = page.getByTestId(formTestId);
    this.submitButton = this.container.getByRole('button', {
      name: /submit|save|create/i,
    });
  }

  async fillField(label: string, value: string) {
    await this.container.getByLabel(label).fill(value);
  }

  async selectOption(label: string, value: string) {
    await this.container.getByLabel(label).selectOption(value);
  }

  async checkCheckbox(label: string) {
    await this.container.getByLabel(label).check();
  }

  async uncheckCheckbox(label: string) {
    await this.container.getByLabel(label).uncheck();
  }

  async submit() {
    await this.submitButton.click();
  }

  async getFieldError(label: string) {
    const field = this.container.getByLabel(label);
    const fieldId = await field.getAttribute('id');
    const error = this.container.locator(`[aria-describedby="${fieldId}"]`);
    return await error.textContent();
  }

  async hasError(label: string) {
    const error = await this.getFieldError(label);
    return error !== null && error.trim() !== '';
  }

  async getFormErrors() {
    const errors = await this.container
      .locator('[role="alert"]')
      .allTextContents();
    return errors.filter((e) => e.trim() !== '');
  }
}
```

### Waiting Strategies in Page Objects

```typescript
export class DashboardPage {
  readonly page: Page;
  readonly loadingSpinner: Locator;
  readonly dataTable: Locator;

  constructor(page: Page) {
    this.page = page;
    this.loadingSpinner = page.getByTestId('loading-spinner');
    this.dataTable = page.getByRole('table');
  }

  async goto() {
    await this.page.goto('/dashboard');
    await this.waitForPageLoad();
  }

  async waitForPageLoad() {
    // Wait for loading spinner to disappear
    await this.loadingSpinner.waitFor({ state: 'hidden' });

    // Wait for data to load
    await this.dataTable.waitFor({ state: 'visible' });

    // Wait for network idle
    await this.page.waitForLoadState('networkidle');
  }

  async refreshData() {
    const refreshButton = this.page.getByRole('button', { name: 'Refresh' });
    await refreshButton.click();

    // Wait for API response
    await this.page.waitForResponse(
      (response) =>
        response.url().includes('/api/dashboard') && response.status() === 200
    );

    await this.waitForPageLoad();
  }
}
```

## Handling Dynamic Content

### Lists and Collections

```typescript
export class ProductListPage {
  readonly page: Page;
  readonly productCards: Locator;

  constructor(page: Page) {
    this.page = page;
    this.productCards = page.getByTestId('product-card');
  }

  async goto() {
    await this.page.goto('/products');
  }

  async getProductCount() {
    return await this.productCards.count();
  }

  async getProductCard(index: number) {
    return this.productCards.nth(index);
  }

  async getProductCardByName(name: string) {
    return this.productCards.filter({ hasText: name }).first();
  }

  async getAllProductNames() {
    const names = await this.productCards
      .locator('h3')
      .allTextContents();
    return names;
  }

  async clickProduct(name: string) {
    const card = await this.getProductCardByName(name);
    await card.click();
  }

  async addToCartByName(name: string) {
    const card = await this.getProductCardByName(name);
    await card.getByRole('button', { name: 'Add to Cart' }).click();
  }
}
```

### Search and Filter

```typescript
export class SearchPage {
  readonly page: Page;
  readonly searchInput: Locator;
  readonly searchButton: Locator;
  readonly results: Locator;
  readonly filters: Locator;

  constructor(page: Page) {
    this.page = page;
    this.searchInput = page.getByRole('searchbox');
    this.searchButton = page.getByRole('button', { name: 'Search' });
    this.results = page.getByTestId('search-results');
    this.filters = page.getByTestId('filters');
  }

  async search(query: string) {
    await this.searchInput.fill(query);
    await this.searchButton.click();
    await this.waitForResults();
  }

  async applyFilter(filterName: string, value: string) {
    await this.filters
      .getByRole('button', { name: filterName })
      .click();
    await this.page
      .getByRole('checkbox', { name: value })
      .check();
    await this.waitForResults();
  }

  async getResultCount() {
    const countText = await this.results
      .getByTestId('result-count')
      .textContent();
    return parseInt(countText?.match(/\d+/)?.[0] || '0');
  }

  private async waitForResults() {
    await this.page.waitForResponse(
      (response) => response.url().includes('/api/search')
    );
    await this.results.getByTestId('result-item').first().waitFor();
  }
}
```

## Type-Safe Page Objects

### Using TypeScript Interfaces

```typescript
// types/user.ts
export interface User {
  email: string;
  password: string;
  firstName?: string;
  lastName?: string;
}

export interface Product {
  id: string;
  name: string;
  price: number;
  description?: string;
}
```

```typescript
// pages/registration-page.ts
import { User } from '../types/user';

export class RegistrationPage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async goto() {
    await this.page.goto('/register');
  }

  async register(user: User) {
    await this.page.getByLabel('Email').fill(user.email);
    await this.page.getByLabel('Password').fill(user.password);

    if (user.firstName) {
      await this.page.getByLabel('First Name').fill(user.firstName);
    }

    if (user.lastName) {
      await this.page.getByLabel('Last Name').fill(user.lastName);
    }

    await this.page.getByRole('button', { name: 'Register' }).click();
  }
}
```

### Builder Pattern for Test Data

```typescript
// builders/user-builder.ts
import { User } from '../types/user';

export class UserBuilder {
  private user: Partial<User> = {};

  withEmail(email: string): this {
    this.user.email = email;
    return this;
  }

  withPassword(password: string): this {
    this.user.password = password;
    return this;
  }

  withName(firstName: string, lastName: string): this {
    this.user.firstName = firstName;
    this.user.lastName = lastName;
    return this;
  }

  build(): User {
    if (!this.user.email || !this.user.password) {
      throw new Error('Email and password are required');
    }
    return this.user as User;
  }
}
```

```typescript
// tests/registration.spec.ts
import { UserBuilder } from '../builders/user-builder';
import { RegistrationPage } from '../pages/registration-page';

test('should register new user', async ({ page }) => {
  const user = new UserBuilder()
    .withEmail('newuser@example.com')
    .withPassword('SecurePass123!')
    .withName('John', 'Doe')
    .build();

  const registrationPage = new RegistrationPage(page);
  await registrationPage.goto();
  await registrationPage.register(user);

  await expect(page).toHaveURL('/welcome');
});
```

## When to Use This Skill

- Creating new page objects for test automation
- Refactoring existing tests to use Page Object Model
- Building reusable component libraries for tests
- Implementing app actions for complex user flows
- Standardizing locator strategies across a test suite
- Creating type-safe page objects with TypeScript
- Designing maintainable test architecture
- Handling dynamic content and complex UI interactions
- Building form and table abstractions
- Establishing page object patterns for a team

## Resources

- Playwright Locators: <https://playwright.dev/docs/locators>
- Playwright Page Object Models: <https://playwright.dev/docs/pom>
- Playwright Best Practices: <https://playwright.dev/docs/best-practices>
