---
name: web-framework-angular-standalone
description: Angular 17-19 standalone components, signals, control flow, dependency injection patterns
---

# Angular Standalone Components

> **Quick Guide:** Components are standalone by default in Angular 19. Use `signal()`, `computed()`, `effect()`, `linkedSignal()` for reactive state. Use `input()`, `output()`, `model()` for component communication. Use `@if`, `@for`, `@switch`, `@defer` for template control flow. Use `inject()` for dependency injection. Use `resource()` for async data fetching.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `standalone: true` on ALL components, directives, and pipes - it's the default in Angular 19 but be explicit for clarity)**

**(You MUST use `input()`, `output()`, `model()` functions instead of `@Input()`, `@Output()` decorators)**

**(You MUST use `inject()` function for dependency injection, NOT constructor injection)**

**(You MUST use `@if`, `@for`, `@switch` control flow blocks, NOT `*ngIf`, `*ngFor`, `*ngSwitch`)**

**(You MUST use `track` expression in ALL `@for` loops)**

**(You MUST use `linkedSignal()` instead of manual signal synchronization for dependent writable state)**

</critical_requirements>

---

**Auto-detection:** Angular component, standalone component, signal, computed, effect, linkedSignal, resource, rxResource, input(), output(), model(), @if, @for, @switch, @defer, inject(), provideRouter, afterRenderEffect

**When to use:**

- Building Angular 17-19 components with standalone architecture
- Implementing reactive state with signals
- Creating component communication with signal-based inputs/outputs
- Setting up routing with standalone components
- Lazy loading components with `@defer` or `loadComponent`
- Fetching async data with `resource()` or `rxResource()`

**Key patterns covered:**

- Standalone component architecture (default in Angular 19)
- Signals for reactive state (signal, computed, effect, linkedSignal)
- Resource API for async data (resource, rxResource) [experimental]
- Signal-based inputs and outputs (input, output, model)
- Control flow blocks (@if, @for, @switch, @defer)
- Dependency injection with inject()
- Routing with provideRouter and loadComponent
- DOM effects with afterRenderEffect()

**When NOT to use:**

- Legacy Angular projects that must use NgModules (consult migration guides)
- Simple scripts without Angular framework

**Detailed Resources:**

- For core code examples, see [examples/core.md](examples/core.md)
- For advanced patterns (@defer, DI config, model(), RxJS interop), see [examples/](examples/)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

Angular 17-19 embraces a standalone-first architecture that eliminates NgModule boilerplate. **In Angular 19, `standalone: true` is the default** - you only need to specify `standalone: false` for NgModule components. Signals provide synchronous, fine-grained reactivity for predictable state management. The new control flow syntax (`@if`, `@for`, `@switch`, `@defer`) is built into templates without imports, offering better type narrowing and smaller bundles. Components should be self-contained, lazy-loadable units that declare their own dependencies.

**Angular's Four Pillars (17-19):**

1. **Standalone by Default** - Components, directives, and pipes are standalone by default in v19
2. **Signal-Based Reactivity** - Synchronous, memoized, fine-grained change detection with `signal()`, `computed()`, `linkedSignal()`
3. **Built-In Control Flow** - Template syntax that requires no imports and optimizes at build time
4. **Resource API** - Experimental async data fetching that integrates with signals (`resource()`, `rxResource()`)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Standalone Component Structure

All Angular 17-19 components use `standalone: true` (the default in Angular 19) and declare their own imports.

```typescript
// user-card.component.ts
import { Component, input, output } from "@angular/core";
import { DatePipe } from "@angular/common";

export type User = {
  id: string;
  name: string;
  email: string;
  createdAt: Date;
};

@Component({
  selector: "app-user-card",
  standalone: true,
  imports: [DatePipe],
  template: `
    <article class="user-card">
      <h2>{{ user().name }}</h2>
      <p>{{ user().email }}</p>
      <time>Joined: {{ user().createdAt | date: "mediumDate" }}</time>
      <button (click)="edit.emit(user())">Edit</button>
    </article>
  `,
})
export class UserCardComponent {
  // Signal-based input (required)
  user = input.required<User>();

  // Signal-based output
  edit = output<User>();
}
```

**Why good:** standalone: true eliminates NgModule boilerplate, imports array declares dependencies explicitly for tree-shaking, signal-based input() and output() provide type-safe reactive communication, template is colocated for readability

```typescript
// BAD - Legacy patterns
@Component({
  selector: "app-user-card",
  // Missing standalone: true
  template: `...`,
})
export class UserCardComponent {
  @Input() user!: User; // Legacy decorator
  @Output() edit = new EventEmitter<User>(); // Legacy EventEmitter
}
```

**Why bad:** requires NgModule declaration which adds boilerplate, @Input decorator lacks signal reactivity, EventEmitter is less type-safe than output(), non-null assertion (!) hides potential undefined errors

---

### Pattern 2: Signals for Reactive State

Use `signal()` for writable state, `computed()` for derived values, and `effect()` for side effects.

```typescript
// counter.component.ts
import { Component, signal, computed, effect } from "@angular/core";

const INCREMENT_STEP = 1;
const DOUBLE_MULTIPLIER = 2;

@Component({
  selector: "app-counter",
  standalone: true,
  template: `
    <div>
      <p>Count: {{ count() }}</p>
      <p>Double: {{ doubleCount() }}</p>
      <button (click)="increment()">+</button>
      <button (click)="decrement()">-</button>
      <button (click)="reset()">Reset</button>
    </div>
  `,
})
export class CounterComponent {
  // Writable signal with initial value
  count = signal(0);

  // Computed signal (read-only, memoized)
  doubleCount = computed(() => this.count() * DOUBLE_MULTIPLIER);

  constructor() {
    // Effect runs when dependencies change
    effect(() => {
      console.log(`Count changed to: ${this.count()}`);
    });
  }

  increment(): void {
    this.count.update((value) => value + INCREMENT_STEP);
  }

  decrement(): void {
    this.count.update((value) => value - INCREMENT_STEP);
  }

  reset(): void {
    this.count.set(0);
  }
}
```

**Why good:** signal() provides fine-grained reactivity with automatic change detection, computed() memoizes derived values and only recalculates when dependencies change, effect() handles side effects declaratively, named constants prevent magic numbers

```typescript
// BAD - Manual change detection
export class CounterComponent {
  count = 0;

  increment(): void {
    this.count++;
    this.cdr.detectChanges(); // Manual change detection
  }
}
```

**Why bad:** manual change detection is error-prone and inefficient, no automatic dependency tracking, computed values must be recalculated manually

---

### Pattern 3: Signal Inputs and Outputs

Use `input()`, `output()`, and `model()` functions for component communication.

```typescript
// search-input.component.ts
import { Component, input, output, model, computed } from "@angular/core";

const MIN_SEARCH_LENGTH = 3;

@Component({
  selector: "app-search-input",
  standalone: true,
  template: `
    <div class="search-input">
      <input
        [value]="query()"
        (input)="onInput($event)"
        [placeholder]="placeholder()"
      />
      @if (isValidSearch()) {
        <button (click)="search.emit(query())">Search</button>
      }
      @if (query()) {
        <button (click)="clear()">Clear</button>
      }
    </div>
  `,
})
export class SearchInputComponent {
  // Optional input with default value
  placeholder = input("Search...");

  // Required input
  minLength = input.required<number>();

  // Two-way binding with model()
  query = model("");

  // Output event
  search = output<string>();

  // Computed from inputs
  isValidSearch = computed(() => this.query().length >= this.minLength());

  onInput(event: Event): void {
    const target = event.target as HTMLInputElement;
    this.query.set(target.value);
  }

  clear(): void {
    this.query.set("");
  }
}
```

**Usage in parent:**

```html
<app-search-input
  [minLength]="3"
  [(query)]="searchQuery"
  (search)="onSearch($event)"
/>
```

**Why good:** input() and input.required() clearly distinguish optional vs required props, model() enables two-way binding with [(query)] syntax, computed() derives validation state reactively, output() provides type-safe event emission

---

### Pattern 4: Control Flow with @if, @for, @switch

Use built-in control flow blocks instead of structural directives.

```typescript
// user-list.component.ts
import { Component, input, output } from "@angular/core";
import type { User } from "./user.types";

type LoadingState = "idle" | "loading" | "error" | "success";

@Component({
  selector: "app-user-list",
  standalone: true,
  template: `
    @switch (state()) {
      @case ("loading") {
        <div class="loading">Loading users...</div>
      }
      @case ("error") {
        <div class="error">
          <p>Failed to load users</p>
          <button (click)="retry.emit()">Retry</button>
        </div>
      }
      @case ("success") {
        @if (users().length > 0) {
          <ul class="user-list">
            @for (
              user of users();
              track user.id;
              let i = $index, first = $first, last = $last
            ) {
              <li [class.first]="first" [class.last]="last">
                <span class="index">{{ i + 1 }}.</span>
                <span class="name">{{ user.name }}</span>
                <span class="email">{{ user.email }}</span>
              </li>
            } @empty {
              <li class="empty">No users found</li>
            }
          </ul>
        } @else {
          <p>No users available</p>
        }
      }
      @default {
        <p>Ready to load users</p>
      }
    }
  `,
})
export class UserListComponent {
  users = input.required<User[]>();
  state = input<LoadingState>("idle");
  retry = output<void>();
}
```

**Why good:** @switch provides clear multi-branch logic, @for with track enables efficient DOM updates, @empty handles empty collections elegantly, $index/$first/$last provide iteration context without extra code, no CommonModule import required

```typescript
// BAD - Legacy structural directives
@Component({
  imports: [CommonModule], // Extra import needed
  template: `
    <div *ngIf="loading; else content">Loading...</div>
    <ng-template #content>
      <ul>
        <li *ngFor="let user of users; trackBy: trackByFn; let i = index">
          {{ user.name }}
        </li>
      </ul>
    </ng-template>
  `,
})
export class UserListComponent {
  trackByFn(index: number, user: User): string {
    return user.id; // Separate function needed
  }
}
```

**Why bad:** requires CommonModule import, trackBy requires separate function, ng-template syntax is verbose, less optimal type narrowing

---

### Pattern 5: Deferred Loading with @defer

Use `@defer` for lazy loading components and improving initial bundle size.

```typescript
// dashboard.component.ts
import { Component, signal } from "@angular/core";

@Component({
  selector: "app-dashboard",
  standalone: true,
  template: `
    <h1>Dashboard</h1>

    <!-- Defer loading until viewport -->
    @defer (on viewport) {
      <app-heavy-chart />
    } @placeholder (minimum 200ms) {
      <div class="chart-skeleton">Chart loading...</div>
    } @loading (after 100ms; minimum 500ms) {
      <div class="spinner">Loading chart...</div>
    } @error {
      <div class="error">Failed to load chart</div>
    }

    <!-- Defer loading on interaction -->
    @defer (on interaction) {
      <app-comments-section />
    } @placeholder {
      <button>Load Comments</button>
    }

    <!-- Defer with condition -->
    @defer (when showAdvanced()) {
      <app-advanced-settings />
    } @placeholder {
      <p>Advanced settings will load when enabled</p>
    }

    <!-- Prefetch for faster navigation -->
    @defer (on idle; prefetch on hover) {
      <app-related-items />
    } @placeholder {
      <div class="related-skeleton">Related items</div>
    }
  `,
})
export class DashboardComponent {
  showAdvanced = signal(false);
}
```

**Why good:** @defer reduces initial bundle size by lazy-loading components, @placeholder prevents layout shift during load, @loading shows progress after delay to avoid flicker, @error handles failures gracefully, prefetch optimizes perceived performance

**When to use @defer:**

- Heavy components below the fold (charts, data tables)
- Features triggered by user interaction (comments, modals)
- Conditional features that may never be needed
- Components that can be prefetched on idle/hover

**When NOT to use @defer:**

- Components visible on initial load (above the fold)
- Critical UI that users need immediately
- Components that would cause layout shift when loaded

---

### Pattern 6: Dependency Injection with inject()

Use `inject()` function instead of constructor injection for cleaner, more flexible DI.

```typescript
// user.service.ts
import { Injectable, inject } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import type { User } from "./user.types";

const API_BASE_URL = "/api";

@Injectable({ providedIn: "root" })
export class UserService {
  private http = inject(HttpClient);

  getUsers() {
    return this.http.get<User[]>(`${API_BASE_URL}/users`);
  }

  getUser(id: string) {
    return this.http.get<User>(`${API_BASE_URL}/users/${id}`);
  }
}
```

```typescript
// user-profile.component.ts
import { Component, inject, signal, computed, effect } from "@angular/core";
import { ActivatedRoute } from "@angular/router";
import { toSignal } from "@angular/core/rxjs-interop";
import { UserService } from "./user.service";
import type { User } from "./user.types";

@Component({
  selector: "app-user-profile",
  standalone: true,
  template: `
    @if (user(); as user) {
      <h1>{{ user.name }}</h1>
      <p>{{ user.email }}</p>
    } @else {
      <p>Loading user...</p>
    }
  `,
})
export class UserProfileComponent {
  private route = inject(ActivatedRoute);
  private userService = inject(UserService);

  // Convert route params to signal
  private userId = toSignal(this.route.params, { initialValue: { id: "" } });

  // Derived signal for user ID
  private currentUserId = computed(() => this.userId()["id"]);

  user = signal<User | null>(null);

  constructor() {
    // Effect to fetch user when ID changes
    effect(() => {
      const id = this.currentUserId();
      if (id) {
        this.userService.getUser(id).subscribe((user) => {
          this.user.set(user);
        });
      }
    });
  }
}
```

**Why good:** inject() provides cleaner syntax without constructor boilerplate, works in field initializers for simpler code, supports injection flags via options object, enables DI in standalone functions

```typescript
// BAD - Constructor injection (legacy)
export class UserProfileComponent {
  constructor(
    private route: ActivatedRoute,
    private userService: UserService,
  ) {}
}
```

**Why bad:** constructor injection requires boilerplate, doesn't work in field initializers, less flexible for conditional injection

**inject() with options:**

```typescript
// Optional injection
private optionalService = inject(OptionalService, { optional: true });

// Skip self (look in parent injectors)
private parentService = inject(ParentService, { skipSelf: true });

// Self only (don't look in parent injectors)
private selfService = inject(SelfService, { self: true });
```

---

### Pattern 7: Routing with Standalone Components

Configure routing using `provideRouter` and lazy load with `loadComponent`.

```typescript
// app.config.ts
import { ApplicationConfig } from "@angular/core";
import {
  provideRouter,
  withComponentInputBinding,
  withPreloading,
  PreloadAllModules,
} from "@angular/router";
import { provideHttpClient } from "@angular/common/http";
import { routes } from "./app.routes";

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(
      routes,
      withComponentInputBinding(), // Bind route params to inputs
      withPreloading(PreloadAllModules), // Preload lazy routes
    ),
    provideHttpClient(),
  ],
};
```

```typescript
// app.routes.ts
import type { Routes } from "@angular/router";

export const routes: Routes = [
  {
    path: "",
    loadComponent: () =>
      import("./home/home.component").then((m) => m.HomeComponent),
  },
  {
    path: "users",
    loadComponent: () =>
      import("./users/user-list.component").then((m) => m.UserListComponent),
  },
  {
    path: "users/:id",
    loadComponent: () =>
      import("./users/user-detail.component").then(
        (m) => m.UserDetailComponent,
      ),
  },
  {
    path: "admin",
    loadComponent: () =>
      import("./admin/admin.component").then((m) => m.AdminComponent),
    canActivate: [authGuard],
  },
  {
    path: "**",
    loadComponent: () =>
      import("./not-found/not-found.component").then(
        (m) => m.NotFoundComponent,
      ),
  },
];
```

```typescript
// user-detail.component.ts - Using withComponentInputBinding
import { Component, input } from "@angular/core";

@Component({
  selector: "app-user-detail",
  standalone: true,
  template: `
    <h1>User {{ id() }}</h1>
    @if (tab()) {
      <p>Active tab: {{ tab() }}</p>
    }
  `,
})
export class UserDetailComponent {
  // Route param :id bound automatically with withComponentInputBinding
  id = input.required<string>();

  // Query param ?tab bound automatically
  tab = input<string | undefined>();
}
```

**Why good:** provideRouter replaces RouterModule.forRoot(), loadComponent lazy loads individual components without wrapper modules, withComponentInputBinding eliminates ActivatedRoute boilerplate, preloading improves navigation performance

---

### Pattern 8: Lifecycle Hooks with Signals

Replace traditional lifecycle hooks with signal-based patterns.

```typescript
// resize-observer.component.ts
import {
  Component,
  ElementRef,
  signal,
  inject,
  afterNextRender,
  afterRender,
  DestroyRef,
} from "@angular/core";

const DEBOUNCE_MS = 100;

@Component({
  selector: "app-resize-observer",
  standalone: true,
  template: `
    <div #container class="container">
      <p>Width: {{ width() }}px</p>
      <p>Height: {{ height() }}px</p>
    </div>
  `,
})
export class ResizeObserverComponent {
  private elementRef = inject(ElementRef);
  private destroyRef = inject(DestroyRef);

  width = signal(0);
  height = signal(0);

  constructor() {
    // Run once after first render (replaces ngAfterViewInit for DOM setup)
    afterNextRender(() => {
      this.setupResizeObserver();
    });

    // Run after every render (use sparingly)
    afterRender(() => {
      console.log("Component rendered");
    });
  }

  private setupResizeObserver(): void {
    const element = this.elementRef.nativeElement;
    const observer = new ResizeObserver((entries) => {
      for (const entry of entries) {
        this.width.set(entry.contentRect.width);
        this.height.set(entry.contentRect.height);
      }
    });

    observer.observe(element);

    // Cleanup on destroy (replaces ngOnDestroy)
    this.destroyRef.onDestroy(() => {
      observer.disconnect();
    });
  }
}
```

**Why good:** afterNextRender runs after first render for DOM setup, afterRender provides per-render hooks, DestroyRef.onDestroy handles cleanup without implementing OnDestroy, signals automatically trigger change detection

**Lifecycle hook mapping:**

| Legacy Hook        | Signal-Based Alternative          |
| ------------------ | --------------------------------- |
| ngOnInit           | constructor + effect()            |
| ngOnChanges        | effect() watching input() signals |
| ngAfterViewInit    | afterNextRender()                 |
| ngAfterViewChecked | afterRender()                     |
| ngOnDestroy        | DestroyRef.onDestroy()            |

</patterns>

---

<integration>

## Integration Guide

**Angular standalone architecture is self-contained.** Components declare their own imports and providers. Routing uses `provideRouter`. Services use `providedIn: "root"` or component-level providers.

**Bootstrapping:**

```typescript
// main.ts
import { bootstrapApplication } from "@angular/platform-browser";
import { AppComponent } from "./app/app.component";
import { appConfig } from "./app/app.config";

bootstrapApplication(AppComponent, appConfig).catch((err) =>
  console.error(err),
);
```

**Component Communication:**

- Parent to child: `input()` and `input.required()`
- Child to parent: `output()` with `.emit()`
- Two-way binding: `model()` with `[()]` syntax
- Across tree: Services with `inject()`

**RxJS Interop:**

```typescript
import { toSignal, toObservable } from "@angular/core/rxjs-interop";

// Observable to Signal
const users = toSignal(this.userService.getUsers(), { initialValue: [] });

// Signal to Observable
const count$ = toObservable(this.count);
```

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use `standalone: true` on ALL components, directives, and pipes - it's the default in Angular 19 but be explicit for clarity)**

**(You MUST use `input()`, `output()`, `model()` functions instead of `@Input()`, `@Output()` decorators)**

**(You MUST use `inject()` function for dependency injection, NOT constructor injection)**

**(You MUST use `@if`, `@for`, `@switch` control flow blocks, NOT `*ngIf`, `*ngFor`, `*ngSwitch`)**

**(You MUST use `track` expression in ALL `@for` loops)**

**(You MUST use `linkedSignal()` instead of manual signal synchronization for dependent writable state)**

**Failure to follow these rules will produce legacy Angular code that misses performance optimizations and modern reactivity benefits.**

</critical_reminders>
