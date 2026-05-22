---
name: testing-infrastructure
description: Angular 21+ testing infrastructure with fixtures, ng-mocks, component harness, AAA pattern, and Jest best practices for eliminating duplication
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Testing Infrastructure Skill

Expert in creating shared testing infrastructure for Angular 21+ applications with modern best practices.

## When to Use This Skill

Use this skill when:

- Setting up shared test fixtures and factories
- Creating component test harness
- Building mock services with ng-mocks
- Eliminating duplicate test setup code
- Standardizing test patterns across the codebase
- Implementing AAA (Arrange-Act-Assert) pattern
- Migrating from Jasmine to Jest

## Angular Testing Best Practices (2025)

### AAA Pattern (Arrange-Act-Assert)

The **recommended default pattern** for Angular component tests:

```typescript
it('should update task status', () => {
  // Arrange - Set up test data and initial state
  const task = createMockTask({ status: 'pending' });
  component.task = task;
  fixture.detectChanges();

  // Act - Perform the action being tested
  component.completeTask();

  // Assert - Verify the expected outcome
  expect(component.task().status).toBe('completed');
});
```

**Benefits**: Clear structure, reduces false positives, easier to maintain.

### Testing Framework: Jest vs Jasmine

**Jest Recommended** for complex asynchronous flows:

- **Parallel test execution** - Faster feedback loops
- **Built-in mocks** - No need for spy libraries
- **Snapshot testing** - UI regression detection
- **Better developer experience** - Watch mode, clear output

**Migration**: Use `jest-preset-angular` for legacy Jasmine projects.

### ng-mocks Library (Essential for 2025)

**Why ng-mocks?** Drastically simplifies mocking Angular modules, components, and services.

**Benefits**:

- Eliminates boilerplate in TestBed setup
- Auto-mocks dependencies
- MockBuilder for easy configuration
- MockInstance for runtime customization
- MockRender for realistic component testing

**Installation**:

```bash
npm install ng-mocks --save-dev
```

### Global Configuration (src/test.ts)

```typescript
import { ngMocks } from 'ng-mocks';

// Auto-spy setup
ngMocks.autoSpy('jasmine'); // or 'jest'

// Default mock customization
ngMocks.defaultMock(HttpClient, () => ({
  get: () => of([]),
  post: () => of({}),
}));
```

## Problem Statement

**Current issues**:

- Every test file recreates mock data
- Duplicated mock service setup
- No component test harness
- Repetitive TestBed configuration
- Inconsistent test patterns

**Solution**: Centralized testing infrastructure + ng-mocks

## Folder Structure

```
apps/frontend/src/testing/
├── fixtures.ts              # Factory functions for test data
├── component-harness.ts     # Base component test harness
├── utils.ts                 # Test utilities
└── mocks/
    ├── api.service.mock.ts
    ├── auth.service.mock.ts
    ├── task.service.mock.ts
    ├── storage.service.mock.ts
    └── ... (other mocks)
```

## Test Fixtures

Factory functions for creating test data.

```typescript
// testing/fixtures.ts
import { Task, Assignment, Child, Household, User } from '@st44/types/schemas';

// Base factory with overrides pattern
export const createMockTask = (overrides?: Partial<Task>): Task => ({
  id: 'test-task-1',
  householdId: 'test-household-1',
  name: 'Test Task',
  description: 'A test task description',
  points: 10,
  active: true,
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
  ...overrides,
});

export const createMockAssignment = (overrides?: Partial<Assignment>): Assignment => ({
  id: 'test-assignment-1',
  taskId: 'test-task-1',
  childId: 'test-child-1',
  householdId: 'test-household-1',
  status: 'pending',
  dueDate: new Date().toISOString(),
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
  ...overrides,
});

export const createMockChild = (overrides?: Partial<Child>): Child => ({
  id: 'test-child-1',
  userId: 'test-user-1',
  householdId: 'test-household-1',
  firstName: 'Test',
  lastName: 'Child',
  dateOfBirth: '2015-01-01',
  points: 0,
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
  ...overrides,
});

export const createMockHousehold = (overrides?: Partial<Household>): Household => ({
  id: 'test-household-1',
  name: 'Test Household',
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
  ...overrides,
});

export const createMockUser = (overrides?: Partial<User>): User => ({
  id: 'test-user-1',
  email: 'test@example.com',
  firstName: 'Test',
  lastName: 'User',
  role: 'parent',
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
  ...overrides,
});

// Array factory helpers
export const createMockTasks = (count: number): Task[] => {
  return Array.from({ length: count }, (_, i) =>
    createMockTask({
      id: `test-task-${i + 1}`,
      name: `Task ${i + 1}`,
    }),
  );
};

export const createMockAssignments = (count: number): Assignment[] => {
  return Array.from({ length: count }, (_, i) =>
    createMockAssignment({
      id: `test-assignment-${i + 1}`,
    }),
  );
};

// Relationship helpers
export const createTaskWithAssignments = (
  taskOverrides?: Partial<Task>,
  assignmentCount = 3,
): { task: Task; assignments: Assignment[] } => {
  const task = createMockTask(taskOverrides);
  const assignments = Array.from({ length: assignmentCount }, (_, i) =>
    createMockAssignment({
      id: `assignment-${i + 1}`,
      taskId: task.id,
    }),
  );

  return { task, assignments };
};
```

## Component Test Harness

Base class for component testing with common utilities.

```typescript
// testing/component-harness.ts
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Type, DebugElement } from '@angular/core';
import { By } from '@angular/platform-browser';

export class ComponentTestHarness<T> {
  fixture: ComponentFixture<T>;
  component: T;
  nativeElement: HTMLElement;

  constructor(componentClass: Type<T>, providers: unknown[] = []) {
    TestBed.configureTestingModule({
      imports: [componentClass],
      providers,
    });

    this.fixture = TestBed.createComponent(componentClass);
    this.component = this.fixture.componentInstance;
    this.nativeElement = this.fixture.nativeElement;
  }

  /**
   * Trigger change detection
   */
  detectChanges(): void {
    this.fixture.detectChanges();
  }

  /**
   * Query single element by CSS selector
   */
  query<E extends HTMLElement = HTMLElement>(selector: string): E | null {
    return this.nativeElement.querySelector<E>(selector);
  }

  /**
   * Query all elements by CSS selector
   */
  queryAll<E extends HTMLElement = HTMLElement>(selector: string): E[] {
    return Array.from(this.nativeElement.querySelectorAll<E>(selector));
  }

  /**
   * Query by DebugElement
   */
  queryDebug(selector: string): DebugElement | null {
    return this.fixture.debugElement.query(By.css(selector));
  }

  /**
   * Query all by DebugElement
   */
  queryAllDebug(selector: string): DebugElement[] {
    return this.fixture.debugElement.queryAll(By.css(selector));
  }

  /**
   * Get text content of element
   */
  getText(selector: string): string {
    const element = this.query(selector);
    return element?.textContent?.trim() || '';
  }

  /**
   * Click element
   */
  click(selector: string): void {
    const element = this.query(selector);
    if (!element) {
      throw new Error(`Element not found: ${selector}`);
    }
    element.click();
    this.detectChanges();
  }

  /**
   * Set input value
   */
  setInputValue(selector: string, value: string): void {
    const input = this.query<HTMLInputElement>(selector);
    if (!input) {
      throw new Error(`Input not found: ${selector}`);
    }
    input.value = value;
    input.dispatchEvent(new Event('input'));
    this.detectChanges();
  }

  /**
   * Check if element exists
   */
  exists(selector: string): boolean {
    return this.query(selector) !== null;
  }

  /**
   * Check if element has class
   */
  hasClass(selector: string, className: string): boolean {
    const element = this.query(selector);
    return element?.classList.contains(className) || false;
  }

  /**
   * Wait for async operations
   */
  async waitForAsync(): Promise<void> {
    this.fixture.detectChanges();
    await this.fixture.whenStable();
  }

  /**
   * Destroy fixture
   */
  destroy(): void {
    this.fixture.destroy();
  }
}
```

## Mock Services

### Mock API Service

```typescript
// testing/mocks/api.service.mock.ts
import { Observable, of, throwError } from 'rxjs';

export class MockApiService {
  private responses = new Map<string, unknown>();
  private errors = new Map<string, Error>();

  /**
   * Set mock response for URL
   */
  setResponse(url: string, data: unknown): void {
    this.responses.set(url, data);
    this.errors.delete(url);
  }

  /**
   * Set mock error for URL
   */
  setError(url: string, error: Error): void {
    this.errors.set(url, error);
    this.responses.delete(url);
  }

  get<T>(url: string): Observable<T> {
    if (this.errors.has(url)) {
      return throwError(() => this.errors.get(url));
    }
    return of(this.responses.get(url) as T);
  }

  post<T>(url: string, _body: unknown): Observable<T> {
    if (this.errors.has(url)) {
      return throwError(() => this.errors.get(url));
    }
    return of(this.responses.get(url) as T);
  }

  put<T>(url: string, _body: unknown): Observable<T> {
    if (this.errors.has(url)) {
      return throwError(() => this.errors.get(url));
    }
    return of(this.responses.get(url) as T);
  }

  delete<T>(url: string): Observable<T> {
    if (this.errors.has(url)) {
      return throwError(() => this.errors.get(url));
    }
    return of(this.responses.get(url) as T);
  }

  reset(): void {
    this.responses.clear();
    this.errors.clear();
  }
}
```

### Mock Storage Service

```typescript
// testing/mocks/storage.service.mock.ts
import { z } from 'zod';

export class MockStorageService {
  private storage = new Map<string, unknown>();

  get<T>(key: string, _schema: z.ZodType<T>): T | null {
    return (this.storage.get(key) as T) || null;
  }

  set<T>(key: string, value: T): void {
    this.storage.set(key, value);
  }

  remove(key: string): void {
    this.storage.delete(key);
  }

  clear(): void {
    this.storage.clear();
  }

  has(key: string): boolean {
    return this.storage.has(key);
  }
}
```

### Mock Auth Service

```typescript
// testing/mocks/auth.service.mock.ts
import { signal } from '@angular/core';
import { User } from '@st44/types/schemas';
import { createMockUser } from '../fixtures';

export class MockAuthService {
  private currentUserSignal = signal<User | null>(null);
  readonly currentUser = this.currentUserSignal.asReadonly();

  private isAuthenticatedSignal = signal(false);
  readonly isAuthenticated = this.isAuthenticatedSignal.asReadonly();

  setUser(user: User | null): void {
    this.currentUserSignal.set(user);
    this.isAuthenticatedSignal.set(user !== null);
  }

  login(): void {
    this.setUser(createMockUser());
  }

  logout(): void {
    this.setUser(null);
  }

  reset(): void {
    this.logout();
  }
}
```

## Test Utilities

```typescript
// testing/utils.ts

/**
 * Wait for specified milliseconds
 */
export const wait = (ms: number): Promise<void> => {
  return new Promise((resolve) => setTimeout(resolve, ms));
};

/**
 * Trigger input event on element
 */
export const triggerInput = (element: HTMLElement, value: string): void => {
  if (element instanceof HTMLInputElement) {
    element.value = value;
    element.dispatchEvent(new Event('input', { bubbles: true }));
  }
};

/**
 * Trigger click event
 */
export const triggerClick = (element: HTMLElement): void => {
  element.click();
  element.dispatchEvent(new MouseEvent('click', { bubbles: true }));
};

/**
 * Find element by data-testid attribute
 */
export const getByTestId = (container: HTMLElement, testId: string): HTMLElement | null => {
  return container.querySelector(`[data-testid="${testId}"]`);
};

/**
 * Find all elements by data-testid attribute
 */
export const getAllByTestId = (container: HTMLElement, testId: string): HTMLElement[] => {
  return Array.from(container.querySelectorAll(`[data-testid="${testId}"]`));
};
```

## ng-mocks Patterns (2025)

### MockBuilder (Easiest Way to Mock)

Replace repetitive TestBed configuration with MockBuilder:

```typescript
import { MockBuilder, MockRender } from 'ng-mocks';
import { TaskListComponent } from './task-list.component';
import { TaskService } from '../services/task.service';

describe('TaskListComponent with MockBuilder', () => {
  beforeEach(() => {
    // Mock everything except the component being tested
    return MockBuilder(TaskListComponent).mock(TaskService, {
      getTasks: () => of([createMockTask()]),
    });
  });

  it('should display tasks', () => {
    const fixture = MockRender(TaskListComponent);
    expect(fixture.nativeElement.textContent).toContain('Test Task');
  });
});
```

### MockInstance (Runtime Configuration)

Configure mocks before initialization:

```typescript
import { MockBuilder, MockInstance, MockRender } from 'ng-mocks';

describe('TaskComponent with MockInstance', () => {
  beforeEach(() => MockBuilder(TaskComponent));

  beforeAll(() => {
    // Global mock configuration
    MockInstance(TaskService, () => ({
      getTasks: () => of([]),
      createTask: jasmine.createSpy(),
    }));
  });

  afterAll(MockInstance.restore); // Clean up

  it('should use mocked service', () => {
    const fixture = MockRender(TaskComponent);
    const service = fixture.point.injector.get(TaskService);
    expect(service.getTasks).toBeDefined();
  });
});
```

### MockRender (Advanced Component Testing)

Respects all lifecycle hooks and OnPush change detection:

```typescript
import { MockBuilder, MockRender } from 'ng-mocks';

describe('TaskCardComponent', () => {
  beforeEach(() => MockBuilder(TaskCardComponent));

  it('should display task with input', () => {
    const task = createMockTask({ name: 'My Task' });

    // MockRender creates wrapper component and respects all hooks
    const fixture = MockRender(TaskCardComponent, {
      task, // Pass input
    });

    expect(fixture.nativeElement.textContent).toContain('My Task');
  });

  it('should emit output event', () => {
    const onComplete = jasmine.createSpy();
    const fixture = MockRender(
      `<app-task-card [task]="task" (complete)="onComplete($event)"></app-task-card>`,
      {
        task: createMockTask(),
        onComplete,
      },
    );

    // Trigger complete
    fixture.point.componentInstance.complete.emit('task-1');
    expect(onComplete).toHaveBeenCalledWith('task-1');
  });
});
```

### Mock Components and Directives

```typescript
import { MockBuilder, MockComponents } from 'ng-mocks';

describe('ParentComponent', () => {
  beforeEach(
    () =>
      MockBuilder(ParentComponent)
        .mock(ChildComponent) // Auto-mock child
        .mock(SomeDirective), // Auto-mock directive
  );

  it('should render with mocked children', () => {
    const fixture = MockRender(ParentComponent);
    // Child components are mocked, no need to set up their dependencies
    expect(fixture.nativeElement).toBeTruthy();
  });
});
```

### ng-mocks Best Practices

1. **Use MockBuilder** instead of TestBed.configureTestingModule
2. **Use MockRender** instead of TestBed.createComponent
3. **Configure globally** with MockInstance for repeated mocks
4. **Clean up** with MockInstance.restore() in afterAll
5. **Mock components** to avoid dependency chains

## Usage Examples

### Using Fixtures

```typescript
import { createMockTask, createMockTasks } from '../testing/fixtures';

describe('TaskCardComponent', () => {
  it('should display task name', () => {
    const task = createMockTask({ name: 'Custom Task Name' });
    // ... test with task
  });

  it('should handle multiple tasks', () => {
    const tasks = createMockTasks(5);
    expect(tasks).toHaveLength(5);
  });
});
```

### Using Component Harness

```typescript
import { ComponentTestHarness } from '../testing/component-harness';
import { TaskCardComponent } from './task-card.component';

describe('TaskCardComponent', () => {
  let harness: ComponentTestHarness<TaskCardComponent>;

  beforeEach(() => {
    harness = new ComponentTestHarness(TaskCardComponent);
  });

  afterEach(() => {
    harness.destroy();
  });

  it('should render task name', () => {
    harness.component.task = createMockTask({ name: 'Test Task' });
    harness.detectChanges();

    expect(harness.getText('.task-name')).toBe('Test Task');
  });

  it('should emit complete event on button click', () => {
    const spy = jasmine.createSpy('complete');
    harness.component.complete.subscribe(spy);

    harness.click('.complete-button');

    expect(spy).toHaveBeenCalled();
  });
});
```

### Using Mock Services

```typescript
import { MockApiService } from '../testing/mocks/api.service.mock';
import { createMockTasks } from '../testing/fixtures';

describe('TaskService', () => {
  let service: TaskService;
  let mockApi: MockApiService;

  beforeEach(() => {
    mockApi = new MockApiService();

    TestBed.configureTestingModule({
      providers: [TaskService, { provide: ApiService, useValue: mockApi }],
    });

    service = TestBed.inject(TaskService);
  });

  it('should fetch tasks', async () => {
    const mockTasks = createMockTasks(3);
    mockApi.setResponse('/api/tasks', mockTasks);

    const tasks = await service.getTasks();

    expect(tasks).toEqual(mockTasks);
  });

  it('should handle errors', async () => {
    mockApi.setError('/api/tasks', new Error('Network error'));

    await expectAsync(service.getTasks()).toBeRejected();
  });
});
```

### Integration Test Example

```typescript
import { ComponentTestHarness } from '../testing/component-harness';
import { MockApiService } from '../testing/mocks/api.service.mock';
import { createMockTasks } from '../testing/fixtures';

describe('TaskListComponent Integration', () => {
  let harness: ComponentTestHarness<TaskListComponent>;
  let mockApi: MockApiService;

  beforeEach(() => {
    mockApi = new MockApiService();

    harness = new ComponentTestHarness(TaskListComponent, [
      { provide: ApiService, useValue: mockApi },
    ]);
  });

  it('should load and display tasks', async () => {
    const tasks = createMockTasks(3);
    mockApi.setResponse('/api/tasks', tasks);

    await harness.component.ngOnInit();
    await harness.waitForAsync();

    const taskCards = harness.queryAll('.task-card');
    expect(taskCards).toHaveLength(3);
  });

  it('should show error on failure', async () => {
    mockApi.setError('/api/tasks', new Error('Failed'));

    await harness.component.ngOnInit();
    await harness.waitForAsync();

    expect(harness.exists('.error-message')).toBe(true);
  });
});
```

## Best Practices

### 1. Use Fixtures for All Test Data

```typescript
// ❌ BAD - Inline test data
const task = {
  id: '1',
  name: 'Task',
  points: 10,
  // ... many properties
};

// ✅ GOOD - Use fixture
const task = createMockTask({ name: 'Task', points: 10 });
```

### 2. Use Harness for Component Tests

```typescript
// ❌ BAD - Manual setup
let fixture: ComponentFixture<MyComponent>;
let component: MyComponent;

beforeEach(() => {
  TestBed.configureTestingModule({ imports: [MyComponent] });
  fixture = TestBed.createComponent(MyComponent);
  component = fixture.componentInstance;
});

// ✅ GOOD - Use harness
let harness: ComponentTestHarness<MyComponent>;

beforeEach(() => {
  harness = new ComponentTestHarness(MyComponent);
});
```

### 3. Use data-testid for Selectors

```html
<!-- component.html -->
<button data-testid="submit-button">Submit</button>

<!-- test -->
<script>
  const button = getByTestId(harness.nativeElement, 'submit-button');
</script>
```

### 4. Reset Mocks Between Tests

```typescript
afterEach(() => {
  mockApi.reset();
  mockStorage.clear();
  mockAuth.reset();
});
```

## Migration Guide

### Before (Duplicated Setup)

```typescript
// task-list.component.spec.ts
describe('TaskListComponent', () => {
  let fixture: ComponentFixture<TaskListComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [TaskListComponent],
    });
    fixture = TestBed.createComponent(TaskListComponent);
  });

  it('test 1', () => {
    const task = { id: '1', name: 'Task' /* ... */ };
    // ... test
  });
});

// task-card.component.spec.ts - SAME setup repeated
describe('TaskCardComponent', () => {
  let fixture: ComponentFixture<TaskCardComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [TaskCardComponent],
    });
    fixture = TestBed.createComponent(TaskCardComponent);
  });

  it('test 1', () => {
    const task = { id: '1', name: 'Task' /* ... */ };
    // ... test
  });
});
```

### After (Shared Infrastructure)

```typescript
// task-list.component.spec.ts
describe('TaskListComponent', () => {
  let harness: ComponentTestHarness<TaskListComponent>;

  beforeEach(() => {
    harness = new ComponentTestHarness(TaskListComponent);
  });

  it('test 1', () => {
    const task = createMockTask();
    // ... test
  });
});

// task-card.component.spec.ts
describe('TaskCardComponent', () => {
  let harness: ComponentTestHarness<TaskCardComponent>;

  beforeEach(() => {
    harness = new ComponentTestHarness(TaskCardComponent);
  });

  it('test 1', () => {
    const task = createMockTask();
    // ... test
  });
});
```

## Success Criteria

Before marking testing infrastructure complete:

- [ ] Fixtures created for all domain models
- [ ] ComponentTestHarness implemented
- [ ] Mock services created for all injectable services
- [ ] Test utilities documented
- [ ] Existing tests migrated to use shared infrastructure
- [ ] No duplicated mock data in test files
- [ ] No duplicated TestBed setup
- [ ] All tests pass with new infrastructure

## References

### Project-Specific

- GitHub Issue #261: Testing Infrastructure
- `.claude/agents/agent-frontend.md`: Complete frontend patterns
- `.claude/skills/state-management/SKILL.md`: State patterns for testing
- `.claude/skills/http-interceptors/SKILL.md`: HTTP mocking patterns

### Angular Testing (2025)

**Official Documentation:**

- [Angular Testing Guide](https://angular.dev/guide/testing) - Official testing documentation
- [Angular Testing Components](https://angular.dev/guide/testing/components) - Component testing guide
- [Angular Testing Services](https://angular.dev/guide/testing/services) - Service testing patterns

**ng-mocks Library:**

- [ng-mocks Documentation](https://ng-mocks.sudo.eu/) - Official ng-mocks docs
- [ng-mocks GitHub](https://github.com/help-me-mom/ng-mocks) - Source code and examples
- [MockBuilder API](https://ng-mocks.sudo.eu/api/MockBuilder) - Simplified test configuration
- [MockRender API](https://ng-mocks.sudo.eu/api/MockRender) - Advanced component rendering
- [MockInstance API](https://ng-mocks.sudo.eu/api/MockInstance) - Runtime mock configuration

**Jest Migration:**

- [Jest Official Docs](https://jestjs.io/docs/getting-started) - Jest documentation
- [Angular Jest Setup](https://thymikee.github.io/jest-preset-angular/) - jest-preset-angular
- [Jest vs Jasmine](https://blog.angular.dev/moving-angular-cli-to-jest-and-web-test-runner-ef85ef69ceca) - Angular team on Jest adoption

**Testing Best Practices:**

- [AAA Pattern in Testing](https://automationpanda.com/2020/07/07/arrange-act-assert-a-pattern-for-writing-good-tests/) - Arrange-Act-Assert explained
- [Component Harness Pattern](https://material.angular.io/cdk/test-harnesses/overview) - Angular CDK Test Harnesses
- [Testing Asynchronous Code](https://angular.dev/guide/testing/async) - Async testing patterns

**Advanced Topics:**

- [Test Doubles](https://martinfowler.com/bliki/TestDouble.html) - Martin Fowler on mocks, stubs, fakes
- [Testing Best Practices](https://testingjavascript.com/) - Testing JavaScript applications
- [Component Testing Strategies](https://angular.dev/guide/testing/components-scenarios) - Common testing scenarios
