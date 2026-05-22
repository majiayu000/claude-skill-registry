---
name: angular-dependency-injection
description: Use when building modular Angular applications requiring dependency injection with providers, injectors, and services.
allowed-tools:
  - Bash
  - Read
---

# Angular Dependency Injection

Master Angular's dependency injection system for building modular,
testable applications with proper service architecture.

## DI Fundamentals

Angular's DI is hierarchical and uses decorators and providers:

```typescript
import { Injectable } from '@angular/core';

// Service injectable at root level
@Injectable({
  providedIn: 'root'
})
export class UserService {
  private users: User[] = [];

  getUsers(): User[] {
    return this.users;
  }

  addUser(user: User): void {
    this.users.push(user);
  }
}

// Component injection
import { Component } from '@angular/core';

@Component({
  selector: 'app-user-list',
  template: `
    <div *ngFor="let user of users">
      {{ user.name }}
    </div>
  `
})
export class UserListComponent {
  users: User[];

  constructor(private userService: UserService) {
    this.users = this.userService.getUsers();
  }
}
```

## Provider Types

### useClass - Class Provider

```typescript
import { Injectable, Provider } from '@angular/core';

// Interface
interface Logger {
  log(message: string): void;
}

// Implementations
@Injectable()
export class ConsoleLogger implements Logger {
  log(message: string): void {
    console.log(message);
  }
}

@Injectable()
export class FileLogger implements Logger {
  log(message: string): void {
    // Write to file
  }
}

// Provider configuration
const loggerProvider: Provider = {
  provide: Logger,
  useClass: ConsoleLogger // or FileLogger based on env
};

// In module
@NgModule({
  providers: [loggerProvider]
})
export class AppModule {}

// Usage
export class MyComponent {
  constructor(private logger: Logger) {
    this.logger.log('Component initialized');
  }
}
```

### useValue - Value Provider

```typescript
import { InjectionToken } from '@angular/core';

// Configuration object
export interface AppConfig {
  apiUrl: string;
  timeout: number;
  retries: number;
}

export const APP_CONFIG = new InjectionToken<AppConfig>('app.config');

// Provider
const configProvider: Provider = {
  provide: APP_CONFIG,
  useValue: {
    apiUrl: 'https://api.example.com',
    timeout: 5000,
    retries: 3
  }
};

// Module
@NgModule({
  providers: [configProvider]
})
export class AppModule {}

// Usage
export class ApiService {
  constructor(@Inject(APP_CONFIG) private config: AppConfig) {
    console.log(this.config.apiUrl);
  }
}
```

### useFactory - Factory Provider

```typescript
import { Injectable, InjectionToken } from '@angular/core';

export const API_URL = new InjectionToken<string>('api.url');

// Factory function
export function apiUrlFactory(config: AppConfig): string {
  return config.production
    ? 'https://api.prod.example.com'
    : 'https://api.dev.example.com';
}

// Provider
const apiUrlProvider: Provider = {
  provide: API_URL,
  useFactory: apiUrlFactory,
  deps: [AppConfig] // Dependencies for factory
};

// Complex factory with multiple deps
export function httpClientFactory(
  handler: HttpHandler,
  config: AppConfig,
  logger: Logger
): HttpClient {
  logger.log('Creating HTTP client');
  return new HttpClient(handler);
}

const httpClientProvider: Provider = {
  provide: HttpClient,
  useFactory: httpClientFactory,
  deps: [HttpHandler, AppConfig, Logger]
};
```

### useExisting - Alias Provider

```typescript
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class NewLogger {
  log(message: string): void {
    console.log('[NEW]', message);
  }
}

// Alias old logger to new logger
const oldLoggerProvider: Provider = {
  provide: 'OldLogger',
  useExisting: NewLogger
};

// Usage
export class MyComponent {
  constructor(
    @Inject('OldLogger') private logger: NewLogger
  ) {
    this.logger.log('Using aliased logger');
  }
}
```

## Injection Tokens

### InjectionToken - Type-Safe Tokens

```typescript
import { InjectionToken } from '@angular/core';

// Primitive token
export const MAX_RETRIES = new InjectionToken<number>('max.retries', {
  providedIn: 'root',
  factory: () => 3 // Default value
});

// Object token
export interface FeatureFlags {
  enableNewUI: boolean;
  enableBeta: boolean;
}

export const FEATURE_FLAGS = new InjectionToken<FeatureFlags>(
  'feature.flags',
  {
    providedIn: 'root',
    factory: () => ({
      enableNewUI: false,
      enableBeta: false
    })
  }
);

// Usage
@Injectable()
export class ApiService {
  constructor(
    @Inject(MAX_RETRIES) private maxRetries: number,
    @Inject(FEATURE_FLAGS) private flags: FeatureFlags
  ) {}
}
```

### String Tokens (Legacy)

```typescript
// Not type-safe, avoid when possible
const providers: Provider[] = [
  { provide: 'API_URL', useValue: 'https://api.example.com' },
  { provide: 'TIMEOUT', useValue: 5000 }
];

// Usage
export class MyService {
  constructor(
    @Inject('API_URL') private apiUrl: string,
    @Inject('TIMEOUT') private timeout: number
  ) {}
}
```

## Hierarchical Injectors

### Root Injector

```typescript
// Singleton across entire app
@Injectable({
  providedIn: 'root'
})
export class GlobalService {
  private state = {};
}

// Same instance everywhere
```

### Module Injector

```typescript
@Injectable()
export class ModuleService {
  // Service specific to module
}

@NgModule({
  providers: [ModuleService]
})
export class FeatureModule {}

// Different instance per module
```

### Component Injector

```typescript
@Injectable()
export class ComponentService {
  private data = [];
}

@Component({
  selector: 'app-my-component',
  template: '...',
  providers: [ComponentService] // New instance per component
})
export class MyComponent {
  constructor(private service: ComponentService) {}
}

// Each component instance gets its own service instance
```

### Element Injector

```typescript
@Directive({
  selector: '[appHighlight]',
  providers: [DirectiveService]
})
export class HighlightDirective {
  constructor(private service: DirectiveService) {}
}

// Each directive instance gets its own service
```

## ProvidedIn Options

```typescript
// Root - singleton
@Injectable({
  providedIn: 'root'
})
export class RootService {}

// Platform - shared across multiple apps
@Injectable({
  providedIn: 'platform'
})
export class PlatformService {}

// Any - new instance per module
@Injectable({
  providedIn: 'any'
})
export class AnyService {}

// Module - specific module
@Injectable({
  providedIn: FeatureModule
})
export class FeatureService {}
```

## Multi-Providers

```typescript
import { InjectionToken } from '@angular/core';

// Token for multiple providers
export const HTTP_INTERCEPTORS =
  new InjectionToken<HttpInterceptor[]>('http.interceptors');

// Multiple implementations
@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, next: HttpHandler) {
    // Add auth header
    return next.handle(req);
  }
}

@Injectable()
export class LoggingInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, next: HttpHandler) {
    // Log request
    return next.handle(req);
  }
}

// Register as multi-providers
const providers: Provider[] = [
  {
    provide: HTTP_INTERCEPTORS,
    useClass: AuthInterceptor,
    multi: true
  },
  {
    provide: HTTP_INTERCEPTORS,
    useClass: LoggingInterceptor,
    multi: true
  }
];

// Inject as array
export class HttpService {
  constructor(
    @Inject(HTTP_INTERCEPTORS) private interceptors: HttpInterceptor[]
  ) {
    // interceptors is array of all registered interceptors
  }
}
```

## Optional and Self Decorators

### @Optional - Allow Missing Dependencies

```typescript
import { Optional } from '@angular/core';

@Injectable()
export class MyService {
  constructor(
    @Optional() private logger?: Logger
  ) {
    // logger might be undefined
    this.logger?.log('Service created');
  }
}
```

### @Self - Only Current Injector

```typescript
import { Self } from '@angular/core';

@Component({
  selector: 'app-my-component',
  providers: [LocalService]
})
export class MyComponent {
  constructor(
    @Self() private local: LocalService // Only from this component
  ) {}
}
```

### @SkipSelf - Skip Current Injector

```typescript
import { SkipSelf } from '@angular/core';

@Component({
  selector: 'app-child',
  providers: [SharedService]
})
export class ChildComponent {
  constructor(
    @SkipSelf() private parent: SharedService // From parent, not self
  ) {}
}
```

### @Host - Host Element Injector

```typescript
import { Host } from '@angular/core';

@Directive({
  selector: '[appChild]'
})
export class ChildDirective {
  constructor(
    @Host() private parent: ParentComponent // From host component
  ) {}
}
```

## ForRoot and ForChild Patterns

```typescript
import { NgModule, ModuleWithProviders } from '@angular/core';

@NgModule({})
export class SharedModule {
  // For root module - configures services
  static forRoot(config: SharedConfig): ModuleWithProviders<SharedModule> {
    return {
      ngModule: SharedModule,
      providers: [
        SharedService,
        {
          provide: SHARED_CONFIG,
          useValue: config
        }
      ]
    };
  }

  // For feature modules - no service providers
  static forChild(): ModuleWithProviders<SharedModule> {
    return {
      ngModule: SharedModule,
      providers: [] // No providers, use root services
    };
  }
}

// Usage in AppModule
@NgModule({
  imports: [
    SharedModule.forRoot({ apiUrl: 'https://api.example.com' })
  ]
})
export class AppModule {}

// Usage in feature module
@NgModule({
  imports: [
    SharedModule.forChild()
  ]
})
export class FeatureModule {}
```

## Tree-Shakable Providers

```typescript
// Traditional (not tree-shakable)
@Injectable()
export class OldService {}

@NgModule({
  providers: [OldService]
})
export class AppModule {}

// Tree-shakable (preferred)
@Injectable({
  providedIn: 'root'
})
export class NewService {}

// No need to register in module
// Service is removed if never injected
```

## Testing with DI

### TestBed Provider Overrides

```typescript
import { TestBed } from '@angular/core/testing';

describe('MyComponent', () => {
  let mockUserService: jasmine.SpyObj<UserService>;

  beforeEach(() => {
    mockUserService = jasmine.createSpyObj('UserService', ['getUsers']);

    TestBed.configureTestingModule({
      declarations: [MyComponent],
      providers: [
        { provide: UserService, useValue: mockUserService }
      ]
    });
  });

  it('should get users', () => {
    mockUserService.getUsers.and.returnValue([]);
    const fixture = TestBed.createComponent(MyComponent);
    // Test component with mock
  });
});
```

### Spy on Dependencies

```typescript
import { TestBed } from '@angular/core/testing';

describe('UserService', () => {
  let service: UserService;
  let httpMock: jasmine.SpyObj<HttpClient>;

  beforeEach(() => {
    httpMock = jasmine.createSpyObj('HttpClient', ['get', 'post']);

    TestBed.configureTestingModule({
      providers: [
        UserService,
        { provide: HttpClient, useValue: httpMock }
      ]
    });

    service = TestBed.inject(UserService);
  });

  it('should fetch users', () => {
    httpMock.get.and.returnValue(of([]));
    service.getUsers().subscribe();
    expect(httpMock.get).toHaveBeenCalled();
  });
});
```

## When to Use This Skill

Use angular-dependency-injection when building modern, production-ready
applications that require:

- Modular service architecture
- Testable components and services
- Configuration management
- Plugin/extension systems
- Multi-provider patterns (interceptors, validators)
- Complex service hierarchies
- Lazy-loaded module isolation
- Tree-shakable code

## Angular DI Best Practices

1. **Use `providedIn: 'root'`** - Tree-shakable and singleton
2. **Use InjectionToken** - Type-safe over string tokens
3. **Favor composition** - Inject small, focused services
4. **Use factories for complex creation** - useFactory for dynamic values
5. **Test with mocks** - Override providers in TestBed
6. **Follow forRoot/forChild pattern** - For shared modules
7. **Use @Optional sparingly** - Prefer defaults or required deps
8. **Document multi-providers** - Clear contract for extensions
9. **Avoid circular dependencies** - Refactor to common service
10. **Use providedIn module** - For module-specific services

## DI Pitfalls and Gotchas

1. **Circular dependencies** - A depends on B, B depends on A
2. **Providing in component** - Creates new instance per component
3. **Missing providers** - Runtime error if not provided
4. **Wrong injector level** - Service not found in hierarchy
5. **Forgetting multi: true** - Overrides instead of adding
6. **String token collisions** - Use InjectionToken instead
7. **Not using forRoot** - Multiple service instances
8. **Providing eagerly** - Use providedIn for tree-shaking
9. **Testing without mocks** - Real dependencies in tests
10. **Complex factory deps** - Hard to test and maintain

## Advanced DI Patterns

### Service with Configuration

```typescript
import { Injectable, Inject, InjectionToken } from '@angular/core';

export interface ApiConfig {
  baseUrl: string;
  timeout: number;
}

export const API_CONFIG = new InjectionToken<ApiConfig>('api.config');

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  constructor(@Inject(API_CONFIG) private config: ApiConfig) {}

  get(endpoint: string) {
    return fetch(`${this.config.baseUrl}/${endpoint}`, {
      signal: AbortSignal.timeout(this.config.timeout)
    });
  }
}

// Module
@NgModule({
  providers: [
    {
      provide: API_CONFIG,
      useValue: {
        baseUrl: 'https://api.example.com',
        timeout: 5000
      }
    }
  ]
})
export class AppModule {}
```

### Abstract Class Provider

```typescript
import { Injectable } from '@angular/core';

// Abstract class
export abstract class DataService<T> {
  abstract get(id: string): Observable<T>;
  abstract save(item: T): Observable<T>;
}

// Implementation
@Injectable()
export class UserDataService implements DataService<User> {
  get(id: string): Observable<User> {
    // Implementation
  }

  save(user: User): Observable<User> {
    // Implementation
  }
}

// Provider
@NgModule({
  providers: [
    { provide: DataService, useClass: UserDataService }
  ]
})
export class FeatureModule {}

// Usage
export class MyComponent {
  constructor(private dataService: DataService<User>) {}
}
```

### Conditional Provider

```typescript
import { Injectable, InjectionToken } from '@angular/core';
import { environment } from './environments/environment';

@Injectable()
export class DevLogger {
  log(message: string) {
    console.log('[DEV]', message);
  }
}

@Injectable()
export class ProdLogger {
  log(message: string) {
    // Send to logging service
  }
}

// Factory chooses implementation
export function loggerFactory(): Logger {
  return environment.production
    ? new ProdLogger()
    : new DevLogger();
}

const loggerProvider: Provider = {
  provide: Logger,
  useFactory: loggerFactory
};
```

### Scope Isolation

```typescript
// Parent service
@Injectable({
  providedIn: 'root'
})
export class GlobalState {
  count = 0;
}

// Child service (isolated)
@Injectable()
export class LocalState {
  count = 0; // Independent per component
}

@Component({
  selector: 'app-counter',
  providers: [LocalState] // New instance per component
})
export class CounterComponent {
  constructor(
    public global: GlobalState,
    public local: LocalState
  ) {}

  incrementGlobal() {
    this.global.count++; // Affects all components
  }

  incrementLocal() {
    this.local.count++; // Only this component
  }
}
```

## Resources

- [Angular Dependency Injection Guide](https://angular.io/guide/dependency-injection)
- [Hierarchical Injectors](https://angular.io/guide/hierarchical-dependency-injection)
- [DI in Action](https://angular.io/guide/dependency-injection-in-action)
- [Injectable Services](https://angular.io/guide/creating-injectable-service)
- [Providers](https://angular.io/guide/providers)
- [Testing with DI](https://angular.io/guide/testing-services)
