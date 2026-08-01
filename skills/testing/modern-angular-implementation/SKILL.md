---
name: modern-angular-implementation
description: 'Implement Angular 18+ features: Signals, standalone components, @defer
  blocks, SSR, zoneless change detection, new control flow syntax, and Material 3
  integration.'
---

---
name: modern-angular-implementation
description: Implement Angular 18+ features: Signals, standalone components, @defer blocks, SSR, zoneless change detection, new control flow syntax, and Material 3 integration.
sasmp_version: "1.3.0"
bonded_agent: 08-modern-angular
bond_type: PRIMARY_BOND
---

# Modern Angular Implementation Skill

## Angular Signals

### Basic Signals
```typescript
import { Component, signal, computed, effect } from '@angular/core';

@Component({
  selector: 'app-counter',
  standalone: true,
  template: `
    <button (click)="increment()">{{ count() }}</button>
    <p>Double: {{ double() }}</p>
  `
})
export class CounterComponent {
  // Writable signal
  count = signal(0);

  // Computed signal (auto-updates)
  double = computed(() => this.count() * 2);

  constructor() {
    // Effect (side effects)
    effect(() => {
      console.log('Count changed:', this.count());
    });
  }

  increment() {
    this.count.update(n => n + 1);
    // or: this.count.set(this.count() + 1);
  }
}
```

### Signal Store Pattern
```typescript
@Injectable({ providedIn: 'root' })
export class UserStore {
  // Private state signal
  private state = signal<{
    users: User[];
    loading: boolean;
    error: string | null;
  }>({
    users: [],
    loading: false,
    error: null
  });

  // Public computed selectors
  readonly users = computed(() => this.state().users);
  readonly loading = computed(() => this.state().loading);
  readonly error = computed(() => this.state().error);
  readonly userCount = computed(() => this.users().length);

  // Actions
  async loadUsers() {
    this.state.update(s => ({ ...s, loading: true }));
    try {
      const users = await this.http.get<User[]>('/api/users');
      this.state.update(s => ({ ...s, users, loading: false }));
    } catch (error) {
      this.state.update(s => ({
        ...s,
        error: error.message,
        loading: false
      }));
    }
  }

  addUser(user: User) {
    this.state.update(s => ({
      ...s,
      users: [...s.users, user]
    }));
  }
}
```

### Signals vs RxJS
```typescript
// ❌ OLD: RxJS BehaviorSubject
private userSubject = new BehaviorSubject<User | null>(null);
user$ = this.userSubject.asObservable();
userName$ = this.user$.pipe(map(u => u?.name ?? 'Guest'));

ngOnDestroy() {
  this.userSubject.complete();
}

// ✅ NEW: Angular Signals
user = signal<User | null>(null);
userName = computed(() => this.user()?.name ?? 'Guest');
// No cleanup needed!
```

## Standalone Components

### Basic Standalone Component
```typescript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],  // Import dependencies directly
  template: `
    <h1>Dashboard</h1>
    <router-outlet />
  `
})
export class DashboardComponent {}
```

### Standalone Bootstrap
```typescript
// main.ts
import { bootstrapApplication } from '@angular/platform-browser';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { AppComponent } from './app/app.component';
import { routes } from './app/app.routes';

bootstrapApplication(AppComponent, {
  providers: [
    provideRouter(routes),
    provideHttpClient(),
    // Add other providers
  ]
});
```

### Standalone Routes
```typescript
// app.routes.ts
import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./home/home.component').then(m => m.HomeComponent)
  },
  {
    path: 'users',
    loadChildren: () => import('./users/users.routes').then(m => m.USERS_ROUTES)
  }
];
```

### Migration Command
```bash
# Automated migration to standalone
ng generate @angular/core:standalone
```

## Deferrable Views (@defer)

### Basic @defer
```typescript
@defer {
  <app-heavy-component />
} @placeholder {
  <div class="loading-skeleton"></div>
}
```

### Defer with Triggers
```typescript
// On viewport (when visible)
@defer (on viewport) {
  <app-chart [data]="data" />
} @placeholder {
  <div class="chart-placeholder"></div>
}

// On interaction (click or keydown)
@defer (on interaction) {
  <app-advanced-editor />
} @placeholder {
  <button>Load Editor</button>
}

// On hover
@defer (on hover) {
  <app-tooltip [content]="tooltipContent" />
}

// On idle (browser idle)
@defer (on idle) {
  <app-analytics-dashboard />
}

// On timer
@defer (on timer(5s)) {
  <app-promotional-banner />
}
```

### Advanced @defer with States
```typescript
@defer (on interaction; prefetch on idle) {
  <app-video-player [src]="videoUrl" />
} @loading (minimum 500ms; after 100ms) {
  <app-spinner />
} @placeholder (minimum 1s) {
  <button>Load Video Player</button>
} @error {
  <p>Failed to load video player</p>
}
```

### Strategic Deferment
```typescript
<div class="page">
  <!-- Critical content loads immediately -->
  <app-header />
  <app-hero-section />

  <!-- Defer below-the-fold content -->
  @defer (on viewport) {
    <app-features-section />
  }

  @defer (on viewport) {
    <app-testimonials />
  }

  <!-- Defer interactive widgets -->
  @defer (on interaction; prefetch on idle) {
    <app-chat-widget />
  } @placeholder {
    <button class="chat-trigger">Chat with us</button>
  }
</div>
```

## New Control Flow

### @if (replaces *ngIf)
```typescript
// OLD
<div *ngIf="user">{{ user.name }}</div>
<div *ngIf="user; else loading">{{ user.name }}</div>

// NEW
@if (user) {
  <div>{{ user.name }}</div>
}

@if (user) {
  <div>{{ user.name }}</div>
} @else {
  <div>Loading...</div>
}
```

### @for (replaces *ngFor)
```typescript
// OLD
<div *ngFor="let item of items; trackBy: trackById">
  {{ item.name }}
</div>

// NEW
@for (item of items; track item.id) {
  <div>{{ item.name }}</div>
} @empty {
  <p>No items found</p>
}
```

### @switch (replaces *ngSwitch)
```typescript
// OLD
<div [ngSwitch]="status">
  <p *ngSwitchCase="'loading'">Loading...</p>
  <p *ngSwitchCase="'error'">Error occurred</p>
  <p *ngSwitchDefault>Success</p>
</div>

// NEW
@switch (status) {
  @case ('loading') {
    <p>Loading...</p>
  }
  @case ('error') {
    <p>Error occurred</p>
  }
  @default {
    <p>Success</p>
  }
}
```

### Combined Control Flow
```typescript
@if (users.length > 0) {
  <ul>
    @for (user of users; track user.id) {
      <li>
        {{ user.name }}
        @if (user.isAdmin) {
          <span class="badge">Admin</span>
        }
      </li>
    } @empty {
      <li>No users found</li>
    }
  </ul>
} @else {
  <p>Loading users...</p>
}
```

## Server-Side Rendering (SSR)

### Enable SSR
```bash
# Add SSR to existing project
ng add @angular/ssr

# Or create new project with SSR
ng new my-app --ssr
```

### SSR Configuration
```typescript
// app.config.ts
import { ApplicationConfig } from '@angular/core';
import { provideClientHydration } from '@angular/platform-browser';

export const appConfig: ApplicationConfig = {
  providers: [
    provideClientHydration()  // Enable hydration
  ]
};
```

### SSR-Safe Code
```typescript
import { Component, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';

@Component({...})
export class MapComponent {
  constructor(@Inject(PLATFORM_ID) private platformId: Object) {}

  ngOnInit() {
    // Only run in browser
    if (isPlatformBrowser(this.platformId)) {
      this.initializeMap();
      this.loadGoogleMapsAPI();
    }
  }

  private initializeMap() {
    // Browser-specific code
    const map = new google.maps.Map(document.getElementById('map'));
  }
}
```

### Transfer State (Avoid Duplicate Requests)
```typescript
import { Component, makeStateKey, TransferState } from '@angular/core';

const USERS_KEY = makeStateKey<User[]>('users');

@Component({...})
export class UsersComponent {
  constructor(
    private http: HttpClient,
    private transferState: TransferState
  ) {}

  loadUsers() {
    // Check if data exists in transfer state (from SSR)
    const users = this.transferState.get(USERS_KEY, null);

    if (users) {
      // Use cached data from SSR
      return of(users);
    }

    // Fetch from API and cache for hydration
    return this.http.get<User[]>('/api/users').pipe(
      tap(users => this.transferState.set(USERS_KEY, users))
    );
  }
}
```

## Zoneless Change Detection

### Enable Zoneless
```typescript
// app.config.ts
import { ApplicationConfig } from '@angular/core';
import { provideExperimentalZonelessChangeDetection } from '@angular/core';

export const appConfig: ApplicationConfig = {
  providers: [
    provideExperimentalZonelessChangeDetection()
  ]
};
```

### Zoneless-Compatible Code
```typescript
@Component({...})
export class MyComponent {
  count = signal(0);  // Signals work great with zoneless!

  // Manual change detection when needed
  constructor(private cdr: ChangeDetectorRef) {}

  onManualUpdate() {
    this.legacyProperty = 'new value';
    this.cdr.markForCheck();  // Trigger change detection manually
  }
}
```

## Material 3

### Install Material 3
```bash
ng add @angular/material
```

### Material 3 Theme
```scss
// styles.scss
@use '@angular/material' as mat;

$my-theme: mat.define-theme((
  color: (
    theme-type: light,
    primary: mat.$azure-palette,
  ),
));

html {
  @include mat.all-component-themes($my-theme);
}

// Dark mode
html.dark-theme {
  $dark-theme: mat.define-theme((
    color: (
      theme-type: dark,
      primary: mat.$azure-palette,
    ),
  ));

  @include mat.all-component-colors($dark-theme);
}
```

### Material 3 Components
```typescript
import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';

@Component({
  standalone: true,
  imports: [MatButtonModule, MatCardModule, MatIconModule],
  template: `
    <mat-card appearance="outlined">
      <mat-card-header>
        <mat-card-title>Material 3 Card</mat-card-title>
      </mat-card-header>
      <mat-card-content>
        <p>Beautiful Material Design 3 components</p>
      </mat-card-content>
      <mat-card-actions>
        <button mat-button>Action</button>
        <button mat-raised-button color="primary">
          <mat-icon>favorite</mat-icon>
          Primary
        </button>
      </mat-card-actions>
    </mat-card>
  `
})
export class MaterialCardComponent {}
```

## Migration Patterns

### NgModule → Standalone
```typescript
// BEFORE: NgModule
@NgModule({
  declarations: [UserComponent, UserListComponent],
  imports: [CommonModule, RouterModule],
  exports: [UserComponent]
})
export class UserModule {}

// AFTER: Standalone
export const USER_ROUTES: Routes = [{
  path: '',
  loadComponent: () => import('./user.component').then(m => m.UserComponent)
}];

@Component({
  standalone: true,
  imports: [CommonModule, RouterModule]
})
export class UserComponent {}
```

### RxJS → Signals
```typescript
// BEFORE: RxJS
class UserService {
  private usersSubject = new BehaviorSubject<User[]>([]);
  users$ = this.usersSubject.asObservable();

  addUser(user: User) {
    const current = this.usersSubject.value;
    this.usersSubject.next([...current, user]);
  }
}

// AFTER: Signals
class UserService {
  users = signal<User[]>([]);

  addUser(user: User) {
    this.users.update(users => [...users, user]);
  }
}
```

## Performance Optimization

### Bundle Size Reduction with @defer
```typescript
// Can reduce initial bundle by 40-60%!
@defer (on viewport) {
  <app-heavy-chart-library />
}
```

### Zoneless Performance Gains
```typescript
// 20-30% performance improvement
provideExperimentalZonelessChangeDetection()
```

### SSR Core Web Vitals
```typescript
// Dramatically improves LCP, FCP, TTFB
provideClientHydration()
```

## Best Practices

1. **Use Signals for Simple State** - Perfect for component-local reactive state
2. **Keep RxJS for Complex Async** - Still best for HTTP, WebSockets, complex operators
3. **Strategic @defer** - Don't defer critical content, be strategic
4. **Gradual Migration** - Migrate to standalone incrementally
5. **SSR-Safe Guards** - Always check isPlatformBrowser for DOM access
6. **Zoneless-Ready** - Use Signals and OnPush to prepare for zoneless future

## Resources

- [Signals Documentation](https://angular.dev/guide/signals)
- [Standalone Migration](https://angular.dev/reference/migrations/standalone)
- [@defer Guide](https://angular.dev/guide/templates/defer)
- [SSR Guide](https://angular.dev/guide/ssr)
- [Material 3](https://material.angular.io)
