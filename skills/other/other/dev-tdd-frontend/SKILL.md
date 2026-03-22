---
version: 1.1.0
name: dev-tdd-frontend
description: >
  Test-driven development workflow for Angular/TypeScript using Vitest,
  @testing-library/angular, Angular TestBed, and Playwright. Targets standalone
  components, signals, zoneless change detection, and modern Angular control flow.
  Invoked via /dev-tdd (unified entry point) — not directly.
disable-model-invocation: true
user-invocable: false
context: fork
argument-hint: "[feature description]"
---

# TDD Workflow — Frontend (Angular)

Write tests first, then implement. For Angular/TypeScript frontend code.

> **Stack:** Vitest, @testing-library/angular, Angular TestBed, Playwright

## When to Activate

- Writing new components, services, or pipes
- Fixing bugs (write a test that reproduces the bug first)
- Refactoring existing frontend code
- Adding new routes or form interactions

## Core Principles

1. **Tests BEFORE code** — always write the failing test first
2. **80%+ coverage** — unit + e2e combined
3. **Test behavior, not implementation** — tests should survive refactors
4. **Isolated tests** — each test sets up its own data, no shared state
5. **Zoneless** — projects use zoneless change detection (no zone.js); prefer signal-based assertions over manual `detectChanges()` calls

## TDD Cycle

```
RED → GREEN → REFACTOR → repeat
 │       │        │
 │       │        └─ Improve code while tests stay green
 │       └─ Write minimal code to pass
 └─ Write a failing test
```

## Component Under Test (Standalone, Signals, Inline Template)

```typescript
@Component({
  selector: 'app-order-list',
  standalone: true,
  imports: [RouterLink],
  template: `
    @if (error()) {
      <div data-testid="error-state">Failed to load orders</div>
    } @else if (orders().length > 0) {
      @for (order of orders(); track order.id) {
        <div data-testid="order-row">{{ order.status }} — {{ order.total | currency }}</div>
      }
    } @else {
      <p data-testid="empty-state">No orders found</p>
    }
  `,
  styles: [`
    :host { display: block; }
  `]
})
export class OrderListComponent {
  private readonly orderService = inject(OrderService);

  orders = signal<Order[]>([]);
  error = signal<string | null>(null);

  constructor() {
    this.orderService.getOrders().subscribe({
      next: (data) => this.orders.set(data),
      error: (err) => this.error.set(err.message),
    });
  }
}
```

## Component Unit Test (Vitest + TestBed)

```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of, throwError } from 'rxjs';

describe('OrderListComponent', () => {
  let component: OrderListComponent;
  let fixture: ComponentFixture<OrderListComponent>;
  let orderService: { getOrders: ReturnType<typeof vi.fn> };

  beforeEach(async () => {
    orderService = { getOrders: vi.fn().mockReturnValue(of([])) };

    await TestBed.configureTestingModule({
      imports: [OrderListComponent],  // standalone component imported directly
      providers: [
        { provide: OrderService, useValue: orderService }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(OrderListComponent);
    component = fixture.componentInstance;
  });

  it('should display orders when loaded', () => {
    orderService.getOrders.mockReturnValue(of([
      { id: '1', status: 'Placed', total: 19.98 }
    ]));

    fixture.detectChanges();

    const rows = fixture.nativeElement.querySelectorAll('[data-testid="order-row"]');
    expect(rows.length).toBe(1);
    expect(rows[0].textContent).toContain('19.98');
  });

  it('should show empty state when no orders', () => {
    orderService.getOrders.mockReturnValue(of([]));

    fixture.detectChanges();

    const empty = fixture.nativeElement.querySelector('[data-testid="empty-state"]');
    expect(empty).toBeTruthy();
  });

  it('should show error state on failure', () => {
    orderService.getOrders.mockReturnValue(throwError(() => new Error('Failed')));

    fixture.detectChanges();

    const error = fixture.nativeElement.querySelector('[data-testid="error-state"]');
    expect(error).toBeTruthy();
  });

  it('should expose orders via signal', () => {
    orderService.getOrders.mockReturnValue(of([
      { id: '1', status: 'Placed', total: 9.99 }
    ]));

    fixture.detectChanges();

    // Signal-based assertion — access with ()
    expect(component.orders()).toEqual([
      { id: '1', status: 'Placed', total: 9.99 }
    ]);
    expect(component.error()).toBeNull();
  });
});
```

## Component Test with @testing-library/angular

```typescript
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/angular';
import { of } from 'rxjs';

describe('OrderListComponent (testing-library)', () => {
  it('should render orders', async () => {
    const orderService = { getOrders: vi.fn().mockReturnValue(of([
      { id: '1', status: 'Placed', total: 19.98 }
    ])) };

    await render(OrderListComponent, {
      providers: [
        { provide: OrderService, useValue: orderService }
      ]
    });

    expect(screen.getByTestId('order-row')).toHaveTextContent('19.98');
  });

  it('should show empty state', async () => {
    const orderService = { getOrders: vi.fn().mockReturnValue(of([])) };

    await render(OrderListComponent, {
      providers: [
        { provide: OrderService, useValue: orderService }
      ]
    });

    expect(screen.getByTestId('empty-state')).toBeInTheDocument();
  });
});
```

## Service Unit Test (HttpTestingController + firstValueFrom)

```typescript
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { firstValueFrom } from 'rxjs';

describe('OrderService', () => {
  let service: OrderService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        OrderService
      ]
    });

    service = TestBed.inject(OrderService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => httpMock.verify());

  it('should fetch orders', async () => {
    const mockOrders = [{ id: '1', status: 'Placed' }];

    const promise = firstValueFrom(service.getOrders());
    const req = httpMock.expectOne('/api/orders');
    expect(req.request.method).toBe('GET');
    req.flush(mockOrders);

    const result = await promise;
    expect(result).toEqual(mockOrders);
  });
});
```

## Functional Guard Test

```typescript
import { describe, it, expect, vi } from 'vitest';
import { TestBed } from '@angular/core/testing';
import { ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';

// Functional guard (CanActivateFn)
export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  return authService.isAuthenticated() || inject(Router).createUrlTree(['/login']);
};

describe('authGuard', () => {
  it('should allow access when authenticated', () => {
    TestBed.configureTestingModule({
      providers: [
        { provide: AuthService, useValue: { isAuthenticated: () => true } }
      ]
    });

    const result = TestBed.runInInjectionContext(() =>
      authGuard({} as ActivatedRouteSnapshot, {} as RouterStateSnapshot)
    );

    expect(result).toBe(true);
  });

  it('should redirect to login when not authenticated', () => {
    TestBed.configureTestingModule({
      providers: [
        { provide: AuthService, useValue: { isAuthenticated: () => false } },
        { provide: Router, useValue: { createUrlTree: vi.fn().mockReturnValue('/login') } }
      ]
    });

    const result = TestBed.runInInjectionContext(() =>
      authGuard({} as ActivatedRouteSnapshot, {} as RouterStateSnapshot)
    );

    expect(result).toBe('/login');
  });
});
```

## Template-Driven Form Test

```typescript
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/angular';
import userEvent from '@testing-library/user-event';
import { FormsModule } from '@angular/forms';

// Component uses template-driven forms with [(ngModel)]
@Component({
  selector: 'app-order-form',
  standalone: true,
  imports: [FormsModule],
  template: `
    <form #orderForm="ngForm" (ngSubmit)="onSubmit()">
      <input data-testid="sku-input" [(ngModel)]="order.sku" name="sku" required />
      <input data-testid="quantity-input" [(ngModel)]="order.quantity" name="quantity"
             type="number" required min="1" />
      <button data-testid="submit-button" type="submit"
              [disabled]="orderForm.invalid">Place Order</button>
    </form>
  `,
  styles: [`:host { display: block; }`]
})
export class OrderFormComponent {
  order = { sku: '', quantity: 1 };
  onSubmit = vi.fn();
}

describe('OrderFormComponent', () => {
  it('should bind input values via ngModel', async () => {
    const user = userEvent.setup();
    await render(OrderFormComponent, { imports: [FormsModule] });

    await user.clear(screen.getByTestId('sku-input'));
    await user.type(screen.getByTestId('sku-input'), 'SKU-001');

    expect(screen.getByTestId('sku-input')).toHaveValue('SKU-001');
  });
});
```

## E2E Test (Playwright)

```typescript
import { test, expect } from '@playwright/test';

test('user can place an order', async ({ page }) => {
  await page.goto('/orders/new');

  await page.getByTestId('sku-input').fill('SKU-001');
  await page.getByTestId('quantity-input').fill('2');
  await page.getByTestId('add-item-button').click();

  await page.getByTestId('place-order-button').click();

  await expect(page.getByTestId('order-confirmation'))
    .toContainText('Order placed');
});

test('shows validation error for empty order', async ({ page }) => {
  await page.goto('/orders/new');

  await page.getByTestId('place-order-button').click();

  await expect(page.getByTestId('validation-error'))
    .toContainText('at least one item');
});
```

## Test File Organization

```
src/
├── app/
│   ├── orders/
│   │   ├── order-list/
│   │   │   ├── order-list.component.ts
│   │   │   └── order-list.component.spec.ts
│   │   └── services/
│   │       ├── order.service.ts
│   │       └── order.service.spec.ts
└── e2e/
    └── orders.spec.ts
```

## Running Tests

```bash
# Unit tests (single run)
npx vitest run

# Unit tests (watch mode for TDD)
npx vitest

# Unit tests with coverage
npx vitest run --coverage

# Playwright E2E
npx playwright test

# Playwright with UI
npx playwright test --ui
```

## Aspire Runtime Verification (Optional)

After tests pass (GREEN phase), if the Aspire AppHost is running, check for runtime errors that Vitest and Playwright won't catch:

```
mcp__aspire__list_console_logs  resourceName: "site"
```

Look for:
- **Angular runtime errors** — `NullInjectorError` (missing provider), `NG0` errors (template/change detection issues)
- **Chunk load failures** — lazy-loaded routes that fail to resolve after refactoring
- **API contract mismatches** — check the API resource logs for 4xx/5xx errors triggered by frontend requests:
  ```
  mcp__aspire__list_structured_logs  resourceName: "api"
  ```

These catch issues where the app compiles and unit tests pass, but the running app has runtime failures — especially common after changing service signatures, route structures, or API contracts.

Skip if Aspire is not running or the project doesn't use Aspire.

## Coverage Thresholds

Target 80%+. Configure in `vitest.config.ts`:

```typescript
export default defineConfig({
  test: {
    coverage: {
      thresholds: {
        branches: 80,
        functions: 80,
        lines: 80,
        statements: 80,
      }
    }
  }
});
```

## Common Mistakes to Avoid

- **Testing implementation details** — test what the user sees, not component internals
- **Brittle selectors** — use `[data-testid]` or `getByTestId()`, not CSS classes or tag names
- **Shared test state** — each test sets up its own data via `beforeEach`
- **Skipping error paths** — test error states and loading states, not just happy paths
- **Forgetting zoneless** — don't rely on zone.js triggering change detection; use signals and `fixture.detectChanges()` explicitly when needed
- **Using `*ngIf`/`*ngFor`** — use `@if`/`@for` control flow instead
- **Class-based guards/interceptors** — use functional `CanActivateFn`, `HttpInterceptorFn` etc.
- **Not verifying HTTP mocks** — always call `httpMock.verify()` in `afterEach`
- **Subscribe-in-test pattern** — prefer `firstValueFrom()` with async/await over `.subscribe()` in tests
