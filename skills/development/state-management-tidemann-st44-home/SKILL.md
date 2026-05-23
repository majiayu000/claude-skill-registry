---
name: state-management
description: Angular 21+ state management with signals, NgRx SignalStore, resource APIs, AsyncState patterns, and localStorage abstraction for modern reactive applications
allowed-tools: Read, Write, Edit, Glob, Grep
---

# State Management Skill

Expert in Angular 21+ state management using signals, NgRx SignalStore, resource APIs, and modern reactive patterns.

## When to Use This Skill

Use this skill when:

- Implementing shared state across multiple components
- Setting up centralized state store (service-based or NgRx SignalStore)
- Migrating from component-level to centralized state
- Implementing AsyncState pattern or resource APIs for data loading
- Choosing between signals, RxJS, or combined approaches
- Abstracting localStorage access
- Debugging state synchronization issues

## Angular 21 State Management for 2025

### Modern Context

**Zoneless by Default**: Angular v21 uses signals for change detection with zone.js no longer included by default. Zoneless change detection reached stability in v20.2.

**Signals-First Development**: Signals are now the driving force for modern state management in Angular, providing synchronous reactive state and UI reactivity.

### Choose the Right Tool for Your Scope

**Small to Medium Apps** (1-5 developers):

- Use Angular Signals for local component state
- Use service-based stores for shared feature state
- Consider signal state or pure signals

**Large Enterprise Apps**:

- Use NgRx SignalStore for structured approach
- Break state into logical, feature-based stores (avoid monolithic store)
- Use composition with feature-specific stores

### Signals vs RxJS: When to Use Each

**Use Signals for**:

- Synchronous internal state
- UI reactivity and derived state
- Component-local state management
- When you need fine-grained reactivity

**Use RxJS Observables for**:

- Asynchronous data streams (HTTP, WebSockets)
- Complex operator-based data manipulation
- Event handling and timing operations
- When you need operators like debounce, throttle, retry

**Best Practice**: Use both together - Observables for async operations, convert to signals at UI boundary using `toSignal()`.

### Key Design Principles (2025)

1. **Immutability**: Always treat state as immutable. Use `patchState()` for updates in SignalStore.
2. **Feature-Based Stores**: Break down state into logical domains (tasks, users, settings), not one monolithic store.
3. **Separation of Concerns**: Store holds state and computed values. Service handles data operations (API calls).
4. **Type Safety**: Use `signalState()` for enhanced type safety over plain signals.
5. **Performance**: Computed signals prevent unnecessary recalculations - use them for derived state.

## Critical Decision: Shared vs Local State

### Shared State (Centralized Store)

**Use centralized store when**:

- Data is needed by multiple pages/components
- Data needs to be cached across navigation
- State must be synchronized across the app
- Examples: household, user, tasks, assignments, app settings

**Implementation**:

```typescript
// store/app.store.ts
import { Injectable, computed, signal } from '@angular/core';
import { Household, Task, Assignment, User } from '@st44/types/schemas';

@Injectable({ providedIn: 'root' })
export class AppStore {
  // Private writable signals
  private readonly householdSignal = signal<Household | null>(null);
  private readonly tasksSignal = signal<Task[]>([]);
  private readonly assignmentsSignal = signal<Assignment[]>([]);
  private readonly userSignal = signal<User | null>(null);

  // Public readonly access
  readonly household = this.householdSignal.asReadonly();
  readonly tasks = this.tasksSignal.asReadonly();
  readonly assignments = this.assignmentsSignal.asReadonly();
  readonly user = this.userSignal.asReadonly();

  // Computed/derived state
  readonly activeTasks = computed(() => this.tasksSignal().filter((t) => t.active));

  readonly pendingAssignments = computed(() =>
    this.assignmentsSignal().filter((a) => a.status === 'pending'),
  );

  // Actions
  setHousehold(household: Household | null): void {
    this.householdSignal.set(household);
  }

  setTasks(tasks: Task[]): void {
    this.tasksSignal.set(tasks);
  }

  updateTask(taskId: string, updates: Partial<Task>): void {
    this.tasksSignal.update((tasks) =>
      tasks.map((t) => (t.id === taskId ? { ...t, ...updates } : t)),
    );
  }

  addTask(task: Task): void {
    this.tasksSignal.update((tasks) => [...tasks, task]);
  }

  removeTask(taskId: string): void {
    this.tasksSignal.update((tasks) => tasks.filter((t) => t.id !== taskId));
  }

  clear(): void {
    this.householdSignal.set(null);
    this.tasksSignal.set([]);
    this.assignmentsSignal.set([]);
    this.userSignal.set(null);
  }
}
```

**Using the Store**:

```typescript
import { inject } from '@angular/core';
import { AppStore } from '../store/app.store';

export class MyComponent {
  private readonly store = inject(AppStore);

  // Access state
  protected readonly household = this.store.household;
  protected readonly activeTasks = this.store.activeTasks;

  // Update state
  protected addNewTask(task: Task): void {
    this.store.addTask(task);
  }
}
```

### Local Component State

**Use local signals when**:

- State is specific to one component
- State doesn't need to be shared
- Examples: UI state (expanded, selected), form inputs, local toggles

```typescript
export class MyComponent {
  // Local state
  protected readonly expanded = signal(false);
  protected readonly selectedId = signal<string | null>(null);

  // Derived state
  protected readonly hasSelection = computed(() => this.selectedId() !== null);

  toggle(): void {
    this.expanded.update((v) => !v);
  }
}
```

## NgRx SignalStore (Enterprise Pattern)

NgRx SignalStore is recommended for larger applications (5+ developers) needing structured state management.

### Core Building Blocks

```typescript
import { signalStore, withState, withMethods, withComputed } from '@ngrx/signals';
import { inject } from '@angular/core';

export const TaskStore = signalStore(
  { providedIn: 'root' },

  // State
  withState({
    tasks: [] as Task[],
    loading: false,
    filter: 'all' as 'all' | 'active' | 'completed',
  }),

  // Computed
  withComputed(({ tasks, filter }) => ({
    filteredTasks: computed(() => {
      const allTasks = tasks();
      const currentFilter = filter();

      if (currentFilter === 'all') return allTasks;
      return allTasks.filter((t) => (currentFilter === 'active' ? t.active : !t.active));
    }),
  })),

  // Methods
  withMethods((store, taskService = inject(TaskService)) => ({
    async loadTasks() {
      patchState(store, { loading: true });
      try {
        const tasks = await taskService.getTasks();
        patchState(store, { tasks, loading: false });
      } catch (error) {
        patchState(store, { loading: false });
      }
    },

    // Optimistic update
    async updateTask(taskId: string, updates: Partial<Task>) {
      const previousTasks = store.tasks();

      // Optimistic update
      patchState(store, {
        tasks: previousTasks.map((t) => (t.id === taskId ? { ...t, ...updates } : t)),
      });

      try {
        await taskService.updateTask(taskId, updates);
      } catch (error) {
        // Rollback on error
        patchState(store, { tasks: previousTasks });
        throw error;
      }
    },
  })),
);
```

### When to Use SignalStore vs Service Store

**Use Service-Based Store when**:

- Simple to mid-size project (1-5 developers)
- Straightforward state needs
- Prefer lighter weight solution

**Use NgRx SignalStore when**:

- Large enterprise app (5+ developers)
- Need structured patterns and composition
- Want feature extraction and reusability
- Team familiar with NgRx patterns

### SignalStore Best Practices

1. **Separation of Concerns**: Store holds reactive state, Service handles data operations
2. **Feature Composition**: Extract reusable features that can be composed
3. **Optimistic Updates**: Update UI immediately, rollback on error
4. **Type Safety**: Let TypeScript inference handle types (minimal explicit typing needed)

## Angular Resource APIs (Modern Data Fetching)

Angular 19.2+ provides specialized APIs for declarative async data loading.

### httpResource (Recommended for HTTP)

```typescript
import { httpResource } from '@angular/core';
import { inject } from '@angular/core';

export class TaskListComponent {
  private http = inject(HttpClient);

  // Reactive data fetching with signals
  protected tasksResource = httpResource({
    url: () => `/api/tasks`,
    loader: ({ abortSignal }) =>
      this.http.get<Task[]>('/api/tasks', {
        context: new HttpContext().set(ABORT_SIGNAL, abortSignal),
      }),
  });

  // Access as signals
  protected tasks = this.tasksResource.value;
  protected isLoading = this.tasksResource.isLoading;
  protected error = this.tasksResource.error;

  // Reload data
  protected reload() {
    this.tasksResource.reload();
  }
}
```

### rxResource (For RxJS Integration)

```typescript
import { rxResource } from '@angular/core/rxjs-interop';
import { inject, signal } from '@angular/core';

export class TaskListComponent {
  private taskService = inject(TaskService);
  private filter = signal<'all' | 'active'>('all');

  // rxResource for observable-based data
  protected tasksResource = rxResource({
    request: () => ({ filter: this.filter() }),
    loader: ({ request }) => this.taskService.getTasks(request.filter),
  });

  // Previous data remains visible while loading
  protected tasks = this.tasksResource.value;
  protected isLoading = this.tasksResource.isLoading;
}
```

### Best Practices for Resource APIs

1. **Use httpResource first** for HTTP requests - simpler than resource/rxResource
2. **Keep previous data visible**: Don't collapse UI while loading new data
3. **Handle experimental status**: APIs are experimental in v20, may change
4. **Combine with signals**: Use computed() for derived state from resource values
5. **AbortSignal support**: Always pass abortSignal to prevent memory leaks

## AsyncState Utility Pattern

**Problem**: Every component has repetitive loading/error/data pattern

**Solution**: Use AsyncState utility class

### Implementation

```typescript
// utils/async-state.ts
import { signal, computed } from '@angular/core';

export class AsyncState<T> {
  readonly state = signal<
    | { status: 'idle' }
    | { status: 'loading' }
    | { status: 'error'; error: string }
    | { status: 'success'; data: T }
  >({ status: 'idle' });

  // Computed helpers
  readonly isLoading = computed(() => this.state().status === 'loading');
  readonly isSuccess = computed(() => this.state().status === 'success');
  readonly isError = computed(() => this.state().status === 'error');
  readonly isIdle = computed(() => this.state().status === 'idle');

  readonly error = computed(() => (this.state().status === 'error' ? this.state().error : null));

  readonly data = computed(() => (this.state().status === 'success' ? this.state().data : null));

  async execute(fn: () => Promise<T>): Promise<void> {
    this.state.set({ status: 'loading' });
    try {
      const data = await fn();
      this.state.set({ status: 'success', data });
    } catch (error) {
      this.state.set({
        status: 'error',
        error: error instanceof Error ? error.message : String(error),
      });
    }
  }

  reset(): void {
    this.state.set({ status: 'idle' });
  }
}
```

### Usage in Components

```typescript
import { AsyncState } from '../utils/async-state';

export class MyComponent {
  private readonly taskService = inject(TaskService);

  // Create AsyncState instance
  protected readonly tasksState = new AsyncState<Task[]>();

  // Use computed helpers
  protected readonly isLoading = this.tasksState.isLoading;
  protected readonly error = this.tasksState.error;
  protected readonly tasks = this.tasksState.data;

  async ngOnInit(): Promise<void> {
    await this.loadTasks();
  }

  async loadTasks(): Promise<void> {
    await this.tasksState.execute(async () => {
      return this.taskService.getTasks();
    });
  }
}
```

### Template Usage

```html
@if (isLoading()) {
<div>Loading...</div>
} @if (error()) {
<div class="error">{{ error() }}</div>
} @if (tasks()) { @for (task of tasks(); track task.id) {
<app-task-card [task]="task" />
} }
```

**Benefits**:

- Eliminates 15+ lines of boilerplate per component
- Type-safe discriminated unions
- Consistent error handling
- Automatic loading state management
- Easier to test

## StorageService Pattern

**Problem**: 9+ files directly access localStorage without type safety

**Solution**: Centralized, type-safe StorageService

### Implementation

```typescript
// services/storage.service.ts
import { Injectable } from '@angular/core';
import { z } from 'zod';

export const STORAGE_KEYS = {
  ACTIVE_HOUSEHOLD_ID: 'activeHouseholdId',
  TASKS_FILTER: 'tasksFilter',
  USER_PREFERENCES: 'userPreferences',
} as const;

@Injectable({
  providedIn: 'root',
})
export class StorageService {
  get<T>(key: string, schema: z.ZodType<T>): T | null {
    const value = localStorage.getItem(key);
    if (!value) return null;

    try {
      const parsed = JSON.parse(value);
      return schema.parse(parsed);
    } catch {
      // Invalid data, remove it
      this.remove(key);
      return null;
    }
  }

  set<T>(key: string, value: T): void {
    localStorage.setItem(key, JSON.stringify(value));
  }

  setWithTTL<T>(key: string, value: T, ttlMs: number): void {
    const item = {
      value,
      expiry: Date.now() + ttlMs,
    };
    localStorage.setItem(key, JSON.stringify(item));
  }

  getWithTTL<T>(key: string, schema: z.ZodType<T>): T | null {
    const value = localStorage.getItem(key);
    if (!value) return null;

    try {
      const parsed = JSON.parse(value);
      if (parsed.expiry && Date.now() > parsed.expiry) {
        this.remove(key);
        return null;
      }
      return schema.parse(parsed.value);
    } catch {
      this.remove(key);
      return null;
    }
  }

  remove(key: string): void {
    localStorage.removeItem(key);
  }

  clear(): void {
    localStorage.clear();
  }

  has(key: string): boolean {
    return localStorage.getItem(key) !== null;
  }
}
```

### Usage

```typescript
import { inject } from '@angular/core';
import { z } from 'zod';
import { StorageService, STORAGE_KEYS } from '../services/storage.service';

export class MyComponent {
  private readonly storage = inject(StorageService);

  // Define schema
  private readonly filterSchema = z.object({
    status: z.enum(['all', 'pending', 'completed']),
    sortBy: z.string(),
  });

  // Load with type safety
  loadFilter(): void {
    const filter = this.storage.get(STORAGE_KEYS.TASKS_FILTER, this.filterSchema);
    if (filter) {
      this.applyFilter(filter);
    }
  }

  // Save
  saveFilter(filter: { status: string; sortBy: string }): void {
    this.storage.set(STORAGE_KEYS.TASKS_FILTER, filter);
  }

  // With TTL (expires after 1 hour)
  saveTemporaryData(data: unknown): void {
    this.storage.setWithTTL('tempData', data, 60 * 60 * 1000);
  }
}
```

**Benefits**:

- Type safety with Zod validation
- Centralized key management
- TTL support for cached data
- Automatic cleanup of invalid data
- Easy to mock for testing
- No direct localStorage coupling

## Migration Guide

### Migrating to Centralized Store

**Before** (component-level state):

```typescript
// home.component.ts
export class Home {
  private readonly householdService = inject(HouseholdService);
  protected household = signal<Household | null>(null);

  async ngOnInit(): Promise<void> {
    this.household.set(await this.householdService.getActive());
  }
}

// tasks.component.ts
export class Tasks {
  private readonly householdService = inject(HouseholdService);
  protected household = signal<Household | null>(null);

  async ngOnInit(): Promise<void> {
    // DUPLICATE API CALL!
    this.household.set(await this.householdService.getActive());
  }
}
```

**After** (centralized store):

```typescript
// app.store.ts
@Injectable({ providedIn: 'root' })
export class AppStore {
  private readonly householdSignal = signal<Household | null>(null);
  readonly household = this.householdSignal.asReadonly();

  setHousehold(household: Household): void {
    this.householdSignal.set(household);
  }
}

// app initialization (app.component.ts or guard)
export class AppComponent {
  private readonly store = inject(AppStore);
  private readonly householdService = inject(HouseholdService);

  async ngOnInit(): Promise<void> {
    // Load once at app initialization
    const household = await this.householdService.getActive();
    this.store.setHousehold(household);
  }
}

// home.component.ts
export class Home {
  private readonly store = inject(AppStore);
  protected readonly household = this.store.household; // No API call
}

// tasks.component.ts
export class Tasks {
  private readonly store = inject(AppStore);
  protected readonly household = this.store.household; // No API call
}
```

### Migrating to AsyncState

**Before**:

```typescript
export class MyComponent {
  protected loading = signal(false);
  protected error = signal<string | null>(null);
  protected data = signal<Task[]>([]);

  async loadData(): Promise<void> {
    try {
      this.loading.set(true);
      this.error.set(null);
      const result = await this.service.getData();
      this.data.set(result);
    } catch (err) {
      this.error.set('Failed to load data');
    } finally {
      this.loading.set(false);
    }
  }
}
```

**After**:

```typescript
export class MyComponent {
  protected readonly dataState = new AsyncState<Task[]>();

  async loadData(): Promise<void> {
    await this.dataState.execute(() => this.service.getData());
  }
}
```

### Migrating from localStorage

**Before**:

```typescript
// Multiple files accessing localStorage directly
const id = localStorage.getItem('activeHouseholdId');
localStorage.setItem('activeHouseholdId', newId);
```

**After**:

```typescript
// Centralized access through StorageService
const id = this.storage.get(STORAGE_KEYS.ACTIVE_HOUSEHOLD_ID, z.string());
this.storage.set(STORAGE_KEYS.ACTIVE_HOUSEHOLD_ID, newId);
```

## Testing State Management

### Testing Centralized Store

```typescript
import { TestBed } from '@angular/core/testing';
import { AppStore } from './app.store';

describe('AppStore', () => {
  let store: AppStore;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [AppStore],
    });
    store = TestBed.inject(AppStore);
  });

  it('should update tasks', () => {
    const tasks = [{ id: '1', name: 'Test' }];
    store.setTasks(tasks);
    expect(store.tasks()).toEqual(tasks);
  });

  it('should compute active tasks', () => {
    store.setTasks([
      { id: '1', active: true },
      { id: '2', active: false },
    ]);
    expect(store.activeTasks().length).toBe(1);
  });
});
```

### Testing AsyncState

```typescript
import { AsyncState } from './async-state';

describe('AsyncState', () => {
  it('should handle successful execution', async () => {
    const state = new AsyncState<string>();
    await state.execute(async () => 'success');

    expect(state.isSuccess()).toBe(true);
    expect(state.data()).toBe('success');
  });

  it('should handle errors', async () => {
    const state = new AsyncState<string>();
    await state.execute(async () => {
      throw new Error('Failed');
    });

    expect(state.isError()).toBe(true);
    expect(state.error()).toBe('Failed');
  });
});
```

### Testing with StorageService

```typescript
import { TestBed } from '@angular/core/testing';
import { StorageService } from './storage.service';

describe('Component with StorageService', () => {
  let storage: StorageService;

  beforeEach(() => {
    // Clear localStorage before each test
    localStorage.clear();

    TestBed.configureTestingModule({
      providers: [StorageService],
    });
    storage = TestBed.inject(StorageService);
  });

  it('should save and retrieve data', () => {
    const data = { test: 'value' };
    storage.set('key', data);

    const retrieved = storage.get('key', z.object({ test: z.string() }));
    expect(retrieved).toEqual(data);
  });
});
```

## Common Patterns

### Optimistic Updates

```typescript
@Injectable({ providedIn: 'root' })
export class AppStore {
  private tasksSignal = signal<Task[]>([]);
  readonly tasks = this.tasksSignal.asReadonly();

  async updateTaskOptimistic(
    taskId: string,
    updates: Partial<Task>,
    apiCall: () => Promise<Task>,
  ): Promise<void> {
    // Save current state for rollback
    const previousTasks = this.tasksSignal();

    // Optimistic update
    this.tasksSignal.update((tasks) =>
      tasks.map((t) => (t.id === taskId ? { ...t, ...updates } : t)),
    );

    try {
      // Make API call
      await apiCall();
    } catch (error) {
      // Rollback on error
      this.tasksSignal.set(previousTasks);
      throw error;
    }
  }
}
```

### Loading with Store

```typescript
@Injectable({ providedIn: 'root' })
export class AppStore {
  private readonly loadingSignal = signal(false);
  readonly isLoading = this.loadingSignal.asReadonly();

  async loadWithIndicator<T>(fn: () => Promise<T>): Promise<T> {
    this.loadingSignal.set(true);
    try {
      return await fn();
    } finally {
      this.loadingSignal.set(false);
    }
  }
}
```

## Success Criteria

Before implementing state management:

- [ ] Identified shared vs local state correctly
- [ ] Centralized store for multi-component data
- [ ] AsyncState used for async operations
- [ ] StorageService used instead of localStorage
- [ ] No duplicate API calls
- [ ] Proper error handling
- [ ] Tests for store logic
- [ ] Optimistic updates where appropriate

## References

### Project-Specific

- GitHub Issue #255: State Management
- GitHub Issue #258: Eliminate Code Duplication (AsyncState)
- GitHub Issue #259: Abstract localStorage
- `.claude/agents/agent-frontend.md`: Complete frontend patterns

### Angular 21 State Management (2025)

- [Angular State Management for 2025 | Nx Blog](https://nx.dev/blog/angular-state-management-2025)
- [Signals Overview • Angular](https://angular.dev/guide/signals)
- [Best Practices for Using Angular Signals in 2025 | Medium](https://medium.com/@AmnaJavaid/best-practices-for-using-angular-signals-in-2025-2f4d4088a1d2)
- [Application State Management with Angular Signals | Medium](https://medium.com/@eugeniyoz/application-state-management-with-angular-signals-b9c8b3a3afd7)
- [Practical Guide: State Management Angular Services + Signals | Telerik](https://www.telerik.com/blogs/practical-guide-state-management-using-angular-services-signals)

### NgRx SignalStore

- [NgRx SignalStore Official Docs](https://ngrx.io/guide/signals/signal-store)
- [NgRx Signal Store vs Signal State vs Simple Signal | Medium](https://medium.com/multitude-it-labs/ngrx-signal-store-vs-signal-state-vs-simple-signal-33ceb2f5ee1d)
- [Using NgRx Signal Store for State Management | DEV Community](https://dev.to/dimeloper/using-ngrx-signal-store-for-scalable-state-management-in-angular-2ne5)
- [Modern Angular State Management with NgRx Signals | Medium](https://medium.com/@mlglobtech/modern-angular-state-management-with-ngrx-signals-complete-crud-store-guide-a20ad4afa20e)

### Resource APIs

- [Angular Resource and rxResource | Telerik](https://www.telerik.com/blogs/angular-resource-rxresource)
- [Reactive data fetching with httpResource • Angular](https://angular.dev/guide/http/http-resource)
- [Angular's Resource APIs - Let's Fix Them! | Angular.Schule](https://angular.schule/blog/2025-10-rx-resource-is-broken/)
- [Improve UX with (rx)resource | Tim Deschryver](https://timdeschryver.dev/blog/improve-the-user-experience-of-your-application-using-rxresource)
