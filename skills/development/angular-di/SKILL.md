---
name: angular-di
description: Implement dependency injection in Angular v20+ using inject(), injection tokens, and provider configuration. Use for service architecture, providing dependencies at different levels, creating injectable tokens, and managing singleton vs scoped services. Triggers on service creation, configuring providers, using injection tokens, or understanding DI hierarchy.
---

# Angular Dependency Injection

Configure and use dependency injection in Angular v20+ with `inject()` and providers.

## Basic Injection

### Using inject()

Prefer `inject()` over constructor injection:

```typescript
import { Component, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { UserService } from './user.service';

@Component({
  selector: 'app-user-list',
  template: `...`,
})
export class UserListComponent {
  // Inject dependencies
  private http = inject(HttpClient);
  private userService = inject(UserService);
  
  // Can use immediately
  users = this.userService.getUsers();
}
```

### Injectable Services

```typescript
import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root', // Singleton at root level
})
export class UserService {
  private http = inject(HttpClient);
  
  private users = signal<User[]>([]);
  readonly users$ = this.users.asReadonly();
  
  async loadUsers() {
    const users = await firstValueFrom(
      this.http.get<User[]>('/api/users')
    );
    this.users.set(users);
  }
}
```

## Provider Scopes

### Root Level (Singleton)

```typescript
// Recommended: providedIn
@Injectable({
  providedIn: 'root',
})
export class AuthService {}

// Alternative: in app.config.ts
export const appConfig: ApplicationConfig = {
  providers: [
    AuthService,
  ],
};
```

### Component Level (Instance per Component)

```typescript
@Component({
  selector: 'app-editor',
  providers: [EditorStateService], // New instance for each component
  template: `...`,
})
export class EditorComponent {
  private editorState = inject(EditorStateService);
}
```

### Route Level

```typescript
export const routes: Routes = [
  {
    path: 'admin',
    providers: [AdminService], // Shared within this route tree
    children: [
      { path: '', component: AdminDashboardComponent },
      { path: 'users', component: AdminUsersComponent },
    ],
  },
];
```

## Injection Tokens

### Creating Tokens

```typescript
import { InjectionToken } from '@angular/core';

// Simple value token
export const API_URL = new InjectionToken<string>('API_URL');

// Object token
export interface AppConfig {
  apiUrl: string;
  features: {
    darkMode: boolean;
    analytics: boolean;
  };
}

export const APP_CONFIG = new InjectionToken<AppConfig>('APP_CONFIG');

// Token with factory (self-providing)
export const WINDOW = new InjectionToken<Window>('Window', {
  providedIn: 'root',
  factory: () => window,
});

export const LOCAL_STORAGE = new InjectionToken<Storage>('LocalStorage', {
  providedIn: 'root',
  factory: () => localStorage,
});
```

### Providing Token Values

```typescript
// app.config.ts
export const appConfig: ApplicationConfig = {
  providers: [
    { provide: API_URL, useValue: 'https://api.example.com' },
    {
      provide: APP_CONFIG,
      useValue: {
        apiUrl: 'https://api.example.com',
        features: { darkMode: true, analytics: true },
      },
    },
  ],
};
```

### Injecting Tokens

```typescript
@Injectable({ providedIn: 'root' })
export class ApiService {
  private apiUrl = inject(API_URL);
  private config = inject(APP_CONFIG);
  private window = inject(WINDOW);
  
  getBaseUrl(): string {
    return this.apiUrl;
  }
}
```

## Provider Types

### useClass

```typescript
// Provide implementation
{ provide: LoggerService, useClass: ConsoleLoggerService }

// Conditional implementation
{
  provide: LoggerService,
  useClass: environment.production 
    ? ProductionLoggerService 
    : ConsoleLoggerService,
}
```

### useValue

```typescript
// Static values
{ provide: API_URL, useValue: 'https://api.example.com' }

// Configuration objects
{ provide: APP_CONFIG, useValue: { theme: 'dark', language: 'en' } }
```

### useFactory

```typescript
// Factory with dependencies
{
  provide: UserService,
  useFactory: (http: HttpClient, config: AppConfig) => {
    return new UserService(http, config.apiUrl);
  },
  deps: [HttpClient, APP_CONFIG],
}

// Async factory (not recommended - use provideAppInitializer)
{
  provide: CONFIG,
  useFactory: () => fetch('/config.json').then(r => r.json()),
}
```

### useExisting

```typescript
// Alias to existing provider
{ provide: AbstractLogger, useExisting: ConsoleLoggerService }

// Multiple tokens pointing to same instance
providers: [
  ConsoleLoggerService,
  { provide: Logger, useExisting: ConsoleLoggerService },
  { provide: ErrorLogger, useExisting: ConsoleLoggerService },
]
```

## Injection Options

### Optional Injection

```typescript
@Component({...})
export class MyComponent {
  // Returns null if not provided
  private analytics = inject(AnalyticsService, { optional: true });
  
  trackEvent(name: string) {
    this.analytics?.track(name);
  }
}
```

### Self, SkipSelf, Host

```typescript
@Component({
  providers: [LocalService],
})
export class ParentComponent {
  // Only look in this component's injector
  private local = inject(LocalService, { self: true });
}

@Component({...})
export class ChildComponent {
  // Skip this component, look in parent
  private parentService = inject(ParentService, { skipSelf: true });
  
  // Only look up to host component
  private hostService = inject(HostService, { host: true });
}
```

## Multi Providers

Collect multiple values for same token:

```typescript
// Token for multiple validators
export const VALIDATORS = new InjectionToken<Validator[]>('Validators');

// Provide multiple values
providers: [
  { provide: VALIDATORS, useClass: RequiredValidator, multi: true },
  { provide: VALIDATORS, useClass: EmailValidator, multi: true },
  { provide: VALIDATORS, useClass: MinLengthValidator, multi: true },
]

// Inject as array
@Injectable()
export class ValidationService {
  private validators = inject(VALIDATORS); // Validator[]
  
  validate(value: string): ValidationError[] {
    return this.validators
      .map(v => v.validate(value))
      .filter(Boolean);
  }
}
```

### HTTP Interceptors (Multi Provider)

```typescript
// Interceptors use multi providers internally
export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(
      withInterceptors([
        authInterceptor,
        loggingInterceptor,
        errorInterceptor,
      ])
    ),
  ],
};
```

## App Initializers

Run async code before app starts using `provideAppInitializer`:

```typescript
import { provideAppInitializer, inject } from '@angular/core';

export const appConfig: ApplicationConfig = {
  providers: [
    ConfigService,
    provideAppInitializer(() => {
      const configService = inject(ConfigService);
      return configService.loadConfig();
    }),
  ],
};
```

### Multiple Initializers

```typescript
providers: [
  provideAppInitializer(() => {
    const config = inject(ConfigService);
    return config.load();
  }),
  provideAppInitializer(() => {
    const auth = inject(AuthService);
    return auth.checkSession();
  }),
]
```

## Environment Injector

Create injectors programmatically:

```typescript
import { createEnvironmentInjector, EnvironmentInjector, inject } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class PluginService {
  private parentInjector = inject(EnvironmentInjector);
  
  loadPlugin(providers: Provider[]): EnvironmentInjector {
    return createEnvironmentInjector(providers, this.parentInjector);
  }
}
```

## runInInjectionContext

Run code with injection context:

```typescript
import { runInInjectionContext, EnvironmentInjector, inject } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class UtilityService {
  private injector = inject(EnvironmentInjector);
  
  executeWithDI<T>(fn: () => T): T {
    return runInInjectionContext(this.injector, fn);
  }
}

// Usage
utilityService.executeWithDI(() => {
  const http = inject(HttpClient);
  // Use http...
});
```

For advanced patterns, see [references/di-patterns.md](references/di-patterns.md).
