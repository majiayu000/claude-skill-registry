---
name: frontend-web-dev
description: Use when building Angular applications, creating TypeScript components, implementing reactive forms, managing state, working with RxJS observables, or developing modern web UI with TypeScript.
---

# Frontend Web Development Expert

## Overview

Expert guidance for building modern web applications with Angular 20+, TypeScript, Signals, and RxJS. Focused on standalone components, signal-based reactivity, and type-safe development.

## When to Use

- Creating Angular components, services, or standalone features
- Implementing reactive forms or template-driven forms
- Working with Signals for state management
- Working with RxJS observables for async streams
- Implementing HTTP clients and API integration
- Creating reusable UI components
- Implementing routing and navigation
- Working with Angular dependency injection

## Angular 20+ Core Patterns

### Standalone Component with Signals (Preferred)

```typescript
// Good: Modern Angular 20 component with signals and OnPush
import {
  Component,
  ChangeDetectionStrategy,
  input,
  output,
  computed
} from '@angular/core';

interface User {
  readonly id: number;
  readonly name: string;
  readonly email: string;
}

@Component({
  selector: 'app-user-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './user-card.component.html',
  styleUrl: './user-card.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class UserCardComponent {
  // Signal-based inputs (Angular 17+)
  user = input.required<User>();

  // Signal-based outputs
  userSelected = output<User>();

  // Computed signals for derived state
  displayName = computed(() => this.user().name.toUpperCase());

  onSelect(): void {
    this.userSelected.emit(this.user());
  }
}
```

```typescript
// Bad: Outdated patterns
@Component({
  selector: 'user-card',
  template: `<div>{{user.name}}</div>`
  // Missing: standalone, OnPush, proper typing
})
export class UserCard {
  user: any;  // No type safety!
  @Output() selected: any;  // Old decorator syntax + any type
}
```

### Service with Signals for State

```typescript
// Good: Modern service using signals for state management
import { Injectable, signal, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';

interface User {
  readonly id: number;
  readonly name: string;
  readonly email: string;
  readonly active: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private readonly apiUrl = '/api/users';

  // Signal-based state
  private readonly usersState = signal<User[]>([]);
  private readonly loadingState = signal(false);
  private readonly errorState = signal<string | null>(null);

  // Public readonly computed signals
  readonly users = this.usersState.asReadonly();
  readonly loading = this.loadingState.asReadonly();
  readonly error = this.errorState.asReadonly();

  // Computed derived state
  readonly activeUsers = computed(() =>
    this.usersState().filter(u => u.active)
  );
  readonly userCount = computed(() => this.usersState().length);

  constructor(private http: HttpClient) {}

  loadUsers(): void {
    this.loadingState.set(true);
    this.errorState.set(null);

    this.http.get<User[]>(this.apiUrl).subscribe({
      next: (users) => {
        this.usersState.set(users);
        this.loadingState.set(false);
      },
      error: (err) => {
        this.errorState.set(err.message);
        this.loadingState.set(false);
      }
    });
  }

  addUser(user: User): void {
    // Immutable update
    this.usersState.update(users => [...users, user]);
  }
}
```

### Reactive Forms with Typed FormGroup

```typescript
// Good: Strongly-typed reactive forms (Angular 14+)
import { Component, ChangeDetectionStrategy } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';

interface UserFormValue {
  email: string;
  name: string;
  age: number | null;
}

@Component({
  selector: 'app-user-form',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './user-form.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class UserFormComponent {
  // Typed form group
  userForm = this.fb.nonNullable.group({
    email: ['', [Validators.required, Validators.email]],
    name: ['', [Validators.required, Validators.minLength(2)]],
    age: [null as number | null, [Validators.min(0), Validators.max(150)]]
  });

  constructor(private fb: FormBuilder) {}

  onSubmit(): void {
    if (this.userForm.valid) {
      const userData: UserFormValue = this.userForm.getRawValue();
      // Process typed form data
    }
  }
}
```

## Quick Reference: Angular 20+ Best Practices

| Pattern | Recommendation |
|---------|---------------|
| Components | Standalone with `standalone: true` |
| Change Detection | Always use `OnPush` for performance |
| State (local) | Signals: `signal()`, `computed()` |
| State (shared) | Services with signals |
| Async streams | RxJS for HTTP, events, WebSockets |
| Inputs | `input()` / `input.required()` (signal-based) |
| Outputs | `output()` (signal-based) |
| Forms | Typed reactive forms with `fb.nonNullable.group()` |
| Type Safety | Strict TypeScript, interfaces for all data |

## Change Detection: OnPush Explained

Angular checks components for changes to update the DOM. There are two strategies:

**Default:** Check this component on EVERY change detection cycle (expensive)

**OnPush:** Only check this component when:
1. An `@Input()` or `input()` reference changes
2. An event originates from this component or its children
3. A signal used in the template updates
4. Manually triggered via `ChangeDetectorRef`

```typescript
// ALWAYS use OnPush - it's a free performance win
@Component({
  // ...
  changeDetection: ChangeDetectionStrategy.OnPush
})
```

**With signals, OnPush becomes even more efficient** - Angular knows exactly which signal changed and only updates the affected DOM nodes.

## Signals vs RxJS: When to Use Each

| Use Case | Use Signals | Use RxJS |
|----------|-------------|----------|
| Component state | ✅ `signal()` | ❌ |
| Derived/computed values | ✅ `computed()` | ❌ |
| Service state | ✅ `signal()` | ⚠️ BehaviorSubject (legacy) |
| HTTP requests | ❌ | ✅ `HttpClient` returns Observable |
| Event streams | ❌ | ✅ Multiple values over time |
| Debounce/throttle | ❌ | ✅ RxJS operators |
| Combining async sources | ⚠️ Limited | ✅ `combineLatest`, `forkJoin` |

```typescript
// Signals: Synchronous state
const count = signal(0);
const doubled = computed(() => count() * 2);

// RxJS: Async streams (HTTP, events, WebSockets)
this.http.get<User[]>('/api/users').pipe(
  catchError(err => of([]))
).subscribe(users => this.usersState.set(users));
```

## Common Mistakes

**Forgetting OnPush:**
```typescript
// Bad: Missing OnPush (checks every cycle)
@Component({ selector: 'app-foo', ... })

// Good: Always include OnPush
@Component({
  selector: 'app-foo',
  changeDetection: ChangeDetectionStrategy.OnPush,
  ...
})
```

**Mutating state directly:**
```typescript
// Bad: Direct mutation (won't trigger change detection with OnPush)
this.users.push(newUser);
this.usersSignal().push(newUser);  // Also bad!

// Good: Immutable update
this.users = [...this.users, newUser];
this.usersSignal.update(users => [...users, newUser]);
```

**Not typing data structures:**
```typescript
// Bad: Lose type safety
const data: any = response;
navItems = signal([{ label: 'Home', icon: 'home' }]);  // Inline, no interface

// Good: Define interfaces
interface NavItem {
  readonly label: string;
  readonly icon: string;
  readonly route: string;
}
const navItems = signal<NavItem[]>([...]);
```

**Memory leaks with RxJS (still relevant for HTTP/events):**
```typescript
// Bad: Subscription leak
ngOnInit() {
  this.service.getData().subscribe(data => {
    this.data = data;
  });
}

// Good: Use takeUntilDestroyed (Angular 16+)
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

export class MyComponent {
  private destroyRef = inject(DestroyRef);

  ngOnInit() {
    this.service.getData()
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe(data => this.dataSignal.set(data));
  }
}

// Better: Convert to signal with toSignal()
import { toSignal } from '@angular/core/rxjs-interop';

export class MyComponent {
  data = toSignal(this.service.getData(), { initialValue: [] });
}
```

## TypeScript Best Practices

```typescript
// Good: Strict interfaces with readonly properties
interface User {
  readonly id: number;
  readonly email: string;
  readonly name: string;
  readonly createdAt: Date;
}

// Good: Utility types for variations
type UserCreate = Omit<User, 'id' | 'createdAt'>;
type UserUpdate = Partial<UserCreate>;

// Good: Discriminated unions for state
type LoadingState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: string };
```

## Testing Patterns

```typescript
// Good: Testing standalone component with signals
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('UserCardComponent', () => {
  let component: UserCardComponent;
  let fixture: ComponentFixture<UserCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UserCardComponent]  // Standalone: import the component itself
    }).compileComponents();

    fixture = TestBed.createComponent(UserCardComponent);
    component = fixture.componentInstance;
  });

  it('should emit userSelected when clicked', () => {
    const user: User = { id: 1, name: 'Test', email: 'test@example.com' };

    // Set signal input using componentRef
    fixture.componentRef.setInput('user', user);
    fixture.detectChanges();

    let emittedUser: User | undefined;
    component.userSelected.subscribe(u => emittedUser = u);

    component.onSelect();

    expect(emittedUser).toEqual(user);
  });
});
```

## Key Principles

1. **Standalone components**: Always use `standalone: true`
2. **OnPush always**: Free performance optimization
3. **Signals for state**: Simpler than RxJS for synchronous state
4. **RxJS for streams**: HTTP calls, events, WebSockets
5. **Type everything**: Interfaces for all data structures
6. **Immutable updates**: Never mutate, always create new references
7. **Modern inputs/outputs**: Use `input()` and `output()` functions
