---
name: angular-framework
description: "Develop enterprise-scale applications with Angular 18+ using dependency injection, RxJS, signals, and modular architecture. Master standalone components, services, directives, pipes, and reactive programming. Use for: building large-scale enterprise applications, implementing complex forms with reactive validation, managing application state with RxJS observables, creating reusable component libraries, integrating with REST APIs and GraphQL, implementing authentication and authorization, optimizing performance with change detection strategies, and deploying production-ready Angular applications."
---

# Angular Framework

Build enterprise-scale applications with Angular 18+ using TypeScript, RxJS, and modern architecture patterns.

## Overview

Angular is a comprehensive TypeScript-based framework for building scalable web applications. Angular 18 introduces standalone components as the default, improved dependency injection with the inject() function, signals for fine-grained reactivity, and enhanced developer experience with better tooling and performance.

## Standalone Components

### Component Structure

```typescript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-user-profile',
  standalone: true,
  imports: [CommonModule],
  template: \`
    <div class="profile">
      <h2>{{ user.name }}</h2>
      <p>{{ user.email }}</p>
    </div>
  \`,
  styles: [\`
    .profile {
      padding: 1rem;
      border: 1px solid #ccc;
    }
  \`]
})
export class UserProfileComponent {
  user = {
    name: 'John Doe',
    email: 'john@example.com'
  };
}
```

### Component Lifecycle

```typescript
import { Component, OnInit, OnDestroy, AfterViewInit } from '@angular/core';

@Component({
  selector: 'app-lifecycle',
  standalone: true,
  template: '<p>Lifecycle Demo</p>'
})
export class LifecycleComponent implements OnInit, OnDestroy, AfterViewInit {
  ngOnInit() {
    console.log('Component initialized');
  }

  ngAfterViewInit() {
    console.log('View initialized');
  }

  ngOnDestroy() {
    console.log('Component destroyed');
  }
}
```

## Dependency Injection

### Using inject() Function

```typescript
import { Component, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { UserService } from './user.service';

@Component({
  selector: 'app-users',
  standalone: true,
  template: '<div>Users</div>'
})
export class UsersComponent {
  private http = inject(HttpClient);
  private userService = inject(UserService);

  loadUsers() {
    this.userService.getUsers().subscribe(users => {
      console.log(users);
    });
  }
}
```

### Creating Services

```typescript
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private http = inject(HttpClient);
  private apiUrl = '/api/users';

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(this.apiUrl);
  }

  getUserById(id: string): Observable<User> {
    return this.http.get<User>(\`\${this.apiUrl}/\${id}\`);
  }

  createUser(user: User): Observable<User> {
    return this.http.post<User>(this.apiUrl, user);
  }
}
```

### Hierarchical Injectors

```typescript
// Root level
@Injectable({ providedIn: 'root' })
export class GlobalService {}

// Component level
@Component({
  selector: 'app-feature',
  standalone: true,
  providers: [FeatureService]
})
export class FeatureComponent {}
```

## Signals (New in Angular 16+)

### Signal Basics

```typescript
import { Component, signal, computed, effect } from '@angular/core';

@Component({
  selector: 'app-counter',
  standalone: true,
  template: \`
    <div>
      <p>Count: {{ count() }}</p>
      <p>Double: {{ doubleCount() }}</p>
      <button (click)="increment()">Increment</button>
    </div>
  \`
})
export class CounterComponent {
  count = signal(0);
  doubleCount = computed(() => this.count() * 2);

  constructor() {
    effect(() => {
      console.log(\`Count changed to \${this.count()}\`);
    });
  }

  increment() {
    this.count.update(value => value + 1);
  }
}
```

### Signal Arrays and Objects

```typescript
import { signal } from '@angular/core';

// Array signal
const items = signal<string[]>([]);

// Add item
items.update(current => [...current, 'new item']);

// Remove item
items.update(current => current.filter(item => item !== 'remove me'));

// Object signal
const user = signal({ name: 'John', age: 30 });

// Update property
user.update(current => ({ ...current, age: 31 }));
```

## Reactive Programming with RxJS

### Observable Patterns

```typescript
import { Component, inject, OnInit } from '@angular/core';
import { Observable, map, filter, debounceTime, switchMap } from 'rxjs';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'app-search',
  standalone: true,
  template: \`
    <input [formControl]="searchControl" placeholder="Search...">
    <div *ngFor="let result of results$ | async">
      {{ result.name }}
    </div>
  \`
})
export class SearchComponent implements OnInit {
  searchControl = new FormControl('');
  results$!: Observable<SearchResult[]>;

  ngOnInit() {
    this.results$ = this.searchControl.valueChanges.pipe(
      debounceTime(300),
      filter(query => query.length > 2),
      switchMap(query => this.searchService.search(query))
    );
  }
}
```

### Common RxJS Operators

```typescript
import { of, from, interval } from 'rxjs';
import { map, filter, take, mergeMap, catchError } from 'rxjs/operators';

// map - transform values
of(1, 2, 3).pipe(
  map(x => x * 2)
).subscribe(console.log); // 2, 4, 6

// filter - filter values
of(1, 2, 3, 4).pipe(
  filter(x => x % 2 === 0)
).subscribe(console.log); // 2, 4

// mergeMap - flatten inner observables
of('user1', 'user2').pipe(
  mergeMap(id => this.userService.getUser(id))
).subscribe(console.log);

// catchError - handle errors
this.http.get('/api/data').pipe(
  catchError(error => of({ error: true }))
).subscribe();
```

## Forms

### Reactive Forms

```typescript
import { Component, inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-user-form',
  standalone: true,
  imports: [ReactiveFormsModule],
  template: \`
    <form [formGroup]="userForm" (ngSubmit)="onSubmit()">
      <input formControlName="name" placeholder="Name">
      <div *ngIf="userForm.get('name')?.invalid && userForm.get('name')?.touched">
        Name is required
      </div>

      <input formControlName="email" type="email" placeholder="Email">
      <div *ngIf="userForm.get('email')?.invalid && userForm.get('email')?.touched">
        Valid email required
      </div>

      <button type="submit" [disabled]="userForm.invalid">Submit</button>
    </form>
  \`
})
export class UserFormComponent {
  private fb = inject(FormBuilder);

  userForm: FormGroup = this.fb.group({
    name: ['', Validators.required],
    email: ['', [Validators.required, Validators.email]],
    age: [null, [Validators.min(0), Validators.max(120)]]
  });

  onSubmit() {
    if (this.userForm.valid) {
      console.log(this.userForm.value);
    }
  }
}
```

### Custom Validators

```typescript
import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';

export function passwordMatchValidator(): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    const password = control.get('password');
    const confirmPassword = control.get('confirmPassword');

    if (!password || !confirmPassword) {
      return null;
    }

    return password.value === confirmPassword.value
      ? null
      : { passwordMismatch: true };
  };
}

// Usage
this.form = this.fb.group({
  password: ['', Validators.required],
  confirmPassword: ['', Validators.required]
}, { validators: passwordMatchValidator() });
```

## Directives

### Structural Directives

```typescript
import { Directive, Input, TemplateRef, ViewContainerRef } from '@angular/core';

@Directive({
  selector: '[appUnless]',
  standalone: true
})
export class UnlessDirective {
  constructor(
    private templateRef: TemplateRef<any>,
    private viewContainer: ViewContainerRef
  ) {}

  @Input() set appUnless(condition: boolean) {
    if (!condition) {
      this.viewContainer.createEmbeddedView(this.templateRef);
    } else {
      this.viewContainer.clear();
    }
  }
}

// Usage
<div *appUnless="isHidden">Content</div>
```

### Attribute Directives

```typescript
import { Directive, ElementRef, HostListener, Input } from '@angular/core';

@Directive({
  selector: '[appHighlight]',
  standalone: true
})
export class HighlightDirective {
  @Input() appHighlight = 'yellow';

  constructor(private el: ElementRef) {}

  @HostListener('mouseenter') onMouseEnter() {
    this.highlight(this.appHighlight);
  }

  @HostListener('mouseleave') onMouseLeave() {
    this.highlight('');
  }

  private highlight(color: string) {
    this.el.nativeElement.style.backgroundColor = color;
  }
}

// Usage
<p appHighlight="lightblue">Hover me</p>
```

## Pipes

### Built-in Pipes

```typescript
// Template
{{ value | date:'short' }}
{{ price | currency:'USD' }}
{{ text | uppercase }}
{{ items | json }}
{{ data | async }}
```

### Custom Pipes

```typescript
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'truncate',
  standalone: true
})
export class TruncatePipe implements PipeTransform {
  transform(value: string, limit: number = 50): string {
    return value.length > limit
      ? value.substring(0, limit) + '...'
      : value;
  }
}

// Usage
{{ longText | truncate:100 }}
```

## Change Detection

### OnPush Strategy

```typescript
import { Component, ChangeDetectionStrategy, Input } from '@angular/core';

@Component({
  selector: 'app-optimized',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: '<div>{{ data }}</div>'
})
export class OptimizedComponent {
  @Input() data!: string;
}
```

## Routing

```typescript
import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'users/:id', component: UserDetailComponent },
  {
    path: 'admin',
    loadComponent: () => import('./admin/admin.component').then(m => m.AdminComponent),
    canActivate: [authGuard]
  }
];

// Guard
export const authGuard: CanActivateFn = (route, state) => {
  const authService = inject(AuthService);
  return authService.isAuthenticated();
};
```

## Using the Reference Files

### When to Read Each Reference

**`/references/dependency-injection.md`** — Read when implementing advanced DI patterns, custom providers, or hierarchical injectors.

**`/references/rxjs-patterns.md`** — Read when working with complex observable streams, error handling, or state management.

**`/references/forms-validation.md`** — Read when building complex forms, custom validators, or dynamic form controls.

**`/references/performance-optimization.md`** — Read when optimizing change detection, lazy loading, or bundle size.
