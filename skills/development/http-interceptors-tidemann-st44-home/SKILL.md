---
name: http-interceptors
description: Angular 21+ functional HTTP interceptors for auth, error handling, loading states, retry logic, caching, and security best practices
allowed-tools: Read, Write, Edit, Glob, Grep
---

# HTTP Interceptors Skill

Expert in implementing Angular 21+ functional HTTP interceptors for cross-cutting concerns.

## When to Use This Skill

Use this skill when:

- Setting up authentication with automatic token injection
- Implementing global error handling
- Adding loading state management
- Configuring retry logic for failed requests
- Implementing request caching/deduplication
- Converting API services from Promises to Observables
- Implementing security best practices (JWT, CSRF protection)

## Angular 21 Functional Interceptors (2025)

### Why Functional Interceptors?

**Introduced in Angular v15+**, functional interceptors are now the **recommended approach** over class-based interceptors:

**Advantages**:

1. **Less Boilerplate**: Pure functions are simpler than classes
2. **Better Tree-Shaking**: Smaller bundle sizes
3. **Enhanced Developer Experience**: More readable and maintainable
4. **Composition**: Higher-order functions enable advanced patterns
5. **Predictable Behavior**: Especially in complex setups

**Note**: Class-based guard interfaces were deprecated in v16. While they still work for backward compatibility, **all new development should use functional interceptors**.

### Basic Structure

```typescript
import { HttpInterceptorFn } from '@angular/common/http';

export const myInterceptor: HttpInterceptorFn = (req, next) => {
  // Receive outgoing HttpRequest
  // 'next' represents the next processing step in chain

  // Process or modify request
  const modifiedReq = req.clone({
    /* ... */
  });

  // Pass to next interceptor or make request
  return next(modifiedReq);
};
```

### Configuration

Interceptors are chained together in the order listed via dependency injection:

```typescript
// app.config.ts
import { provideHttpClient, withInterceptors } from '@angular/common/http';

export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(
      withInterceptors([
        authInterceptor, // First
        retryInterceptor, // Second
        cacheInterceptor, // Third
        errorInterceptor, // Last (should always be last)
      ]),
    ),
  ],
};
```

**Order Matters**: Interceptors execute in the order provided. Error handling should typically be last.

## Core Principle

**NEVER manually handle these concerns in individual services**:

- ❌ Manual token injection in every request
- ❌ Per-service error handling
- ❌ Repetitive loading state management
- ❌ Manual retry logic

**ALWAYS use interceptors** for cross-cutting HTTP concerns.

## Required Interceptors

### 1. Auth Interceptor

Automatically adds authentication token to all requests.

```typescript
// interceptors/auth.interceptor.ts
import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { TokenService } from '../services/token.service';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const tokenService = inject(TokenService);
  const token = tokenService.getToken();

  // Skip auth for public endpoints
  if (req.url.includes('/auth/login') || req.url.includes('/auth/register')) {
    return next(req);
  }

  // Add token if available
  if (!token) {
    return next(req);
  }

  const authReq = req.clone({
    setHeaders: {
      Authorization: `Bearer ${token}`,
    },
  });

  return next(authReq);
};
```

### 2. Error Interceptor

Handles HTTP errors globally.

```typescript
// interceptors/error.interceptor.ts
import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, throwError } from 'rxjs';
import { Router } from '@angular/router';
import { NotificationService } from '../services/notification.service';

export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  const router = inject(Router);
  const notification = inject(NotificationService);

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      let errorMessage = 'An error occurred';

      if (error.error instanceof ErrorEvent) {
        // Client-side error
        errorMessage = error.error.message;
      } else {
        // Server-side error
        switch (error.status) {
          case 401:
            errorMessage = 'Unauthorized. Please login again.';
            router.navigate(['/auth/login']);
            break;
          case 403:
            errorMessage = 'Access forbidden.';
            break;
          case 404:
            errorMessage = 'Resource not found.';
            break;
          case 500:
            errorMessage = 'Server error. Please try again later.';
            break;
          default:
            errorMessage = error.error?.message || error.message;
        }
      }

      // Show notification
      notification.error(errorMessage);

      // Re-throw for component-level handling if needed
      return throwError(() => new Error(errorMessage));
    }),
  );
};
```

### 3. Loading Interceptor

Manages global loading state.

```typescript
// interceptors/loading.interceptor.ts
import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { finalize } from 'rxjs';
import { LoadingService } from '../services/loading.service';

export const loadingInterceptor: HttpInterceptorFn = (req, next) => {
  const loadingService = inject(LoadingService);

  // Skip loading for certain requests
  if (req.headers.has('X-Skip-Loading')) {
    const newReq = req.clone({
      headers: req.headers.delete('X-Skip-Loading'),
    });
    return next(newReq);
  }

  loadingService.show();

  return next(req).pipe(
    finalize(() => {
      loadingService.hide();
    }),
  );
};
```

### 4. Retry Interceptor

Automatically retries failed requests with exponential backoff.

```typescript
// interceptors/retry.interceptor.ts
import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { retry, timer } from 'rxjs';

export const retryInterceptor: HttpInterceptorFn = (req, next) => {
  // Only retry GET requests and specific errors
  const shouldRetry = (error: unknown) => {
    if (!(error instanceof HttpErrorResponse)) return false;
    if (req.method !== 'GET') return false;

    // Retry on network errors or 5xx server errors
    return error.status === 0 || error.status >= 500;
  };

  return next(req).pipe(
    retry({
      count: 3,
      delay: (error, retryCount) => {
        if (!shouldRetry(error)) {
          throw error;
        }

        // Exponential backoff: 1s, 2s, 4s
        const delayMs = Math.pow(2, retryCount - 1) * 1000;
        return timer(delayMs);
      },
    }),
  );
};
```

### 5. Cache Interceptor

Caches GET requests to avoid duplicate calls.

```typescript
// interceptors/cache.interceptor.ts
import { HttpInterceptorFn, HttpResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { of, tap, share } from 'rxjs';
import { HttpCacheService } from '../services/http-cache.service';

export const cacheInterceptor: HttpInterceptorFn = (req, next) => {
  const cache = inject(HttpCacheService);

  // Only cache GET requests
  if (req.method !== 'GET') {
    return next(req);
  }

  // Check if cached
  const cachedResponse = cache.get(req.url);
  if (cachedResponse) {
    return of(cachedResponse);
  }

  // Make request and cache
  return next(req).pipe(
    tap((event) => {
      if (event instanceof HttpResponse) {
        cache.set(req.url, event);
      }
    }),
    share(), // Share to prevent duplicate in-flight requests
  );
};
```

## Supporting Services

### TokenService

```typescript
// services/token.service.ts
import { Injectable, inject } from '@angular/core';
import { StorageService, STORAGE_KEYS } from './storage.service';
import { z } from 'zod';

@Injectable({
  providedIn: 'root',
})
export class TokenService {
  private readonly storage = inject(StorageService);

  getToken(): string | null {
    return this.storage.get(STORAGE_KEYS.AUTH_TOKEN, z.string());
  }

  setToken(token: string): void {
    this.storage.set(STORAGE_KEYS.AUTH_TOKEN, token);
  }

  removeToken(): void {
    this.storage.remove(STORAGE_KEYS.AUTH_TOKEN);
  }

  hasToken(): boolean {
    return this.getToken() !== null;
  }
}
```

### NotificationService

```typescript
// services/notification.service.ts
import { Injectable, signal } from '@angular/core';

export interface Notification {
  id: string;
  type: 'success' | 'error' | 'info' | 'warning';
  message: string;
  duration?: number;
}

@Injectable({
  providedIn: 'root',
})
export class NotificationService {
  private readonly notificationsSignal = signal<Notification[]>([]);
  readonly notifications = this.notificationsSignal.asReadonly();

  private idCounter = 0;

  private show(type: Notification['type'], message: string, duration = 5000): void {
    const notification: Notification = {
      id: `notification-${this.idCounter++}`,
      type,
      message,
      duration,
    };

    this.notificationsSignal.update((notifications) => [...notifications, notification]);

    if (duration > 0) {
      setTimeout(() => {
        this.dismiss(notification.id);
      }, duration);
    }
  }

  success(message: string, duration?: number): void {
    this.show('success', message, duration);
  }

  error(message: string, duration?: number): void {
    this.show('error', message, duration);
  }

  info(message: string, duration?: number): void {
    this.show('info', message, duration);
  }

  warning(message: string, duration?: number): void {
    this.show('warning', message, duration);
  }

  dismiss(id: string): void {
    this.notificationsSignal.update((notifications) => notifications.filter((n) => n.id !== id));
  }

  clear(): void {
    this.notificationsSignal.set([]);
  }
}
```

### LoadingService

```typescript
// services/loading.service.ts
import { Injectable, signal, computed } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class LoadingService {
  private readonly countSignal = signal(0);
  readonly isLoading = computed(() => this.countSignal() > 0);

  show(): void {
    this.countSignal.update((count) => count + 1);
  }

  hide(): void {
    this.countSignal.update((count) => Math.max(0, count - 1));
  }

  reset(): void {
    this.countSignal.set(0);
  }
}
```

### HttpCacheService

```typescript
// services/http-cache.service.ts
import { Injectable } from '@angular/core';
import { HttpResponse } from '@angular/common/http';

interface CacheEntry {
  response: HttpResponse<unknown>;
  timestamp: number;
}

@Injectable({
  providedIn: 'root',
})
export class HttpCacheService {
  private cache = new Map<string, CacheEntry>();
  private readonly defaultTTL = 5 * 60 * 1000; // 5 minutes

  get(url: string): HttpResponse<unknown> | null {
    const entry = this.cache.get(url);
    if (!entry) return null;

    // Check if expired
    if (Date.now() - entry.timestamp > this.defaultTTL) {
      this.cache.delete(url);
      return null;
    }

    return entry.response;
  }

  set(url: string, response: HttpResponse<unknown>): void {
    this.cache.set(url, {
      response,
      timestamp: Date.now(),
    });
  }

  clear(url?: string): void {
    if (url) {
      this.cache.delete(url);
    } else {
      this.cache.clear();
    }
  }

  clearPattern(pattern: RegExp): void {
    for (const key of this.cache.keys()) {
      if (pattern.test(key)) {
        this.cache.delete(key);
      }
    }
  }
}
```

## Configuration

### Register Interceptors in App Config

```typescript
// app.config.ts
import { ApplicationConfig } from '@angular/core';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { authInterceptor } from './interceptors/auth.interceptor';
import { errorInterceptor } from './interceptors/error.interceptor';
import { loadingInterceptor } from './interceptors/loading.interceptor';
import { retryInterceptor } from './interceptors/retry.interceptor';
import { cacheInterceptor } from './interceptors/cache.interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(
      withInterceptors([
        authInterceptor,
        retryInterceptor,
        cacheInterceptor,
        loadingInterceptor,
        errorInterceptor, // Error should be last
      ]),
    ),
    // ... other providers
  ],
};
```

**Order matters**: Interceptors run in the order provided.

## Advanced Caching Patterns (2025 Best Practices)

### Common Caching Pitfalls to Avoid

**1. Infinite Cache Growth**

- Problem: In-memory cache grows indefinitely
- Solution: Implement size limits or LRU eviction

**2. In-Flight Request Duplication**

- Problem: Multiple parallel requests to same URL before cache populates
- Solution: Store in-flight observable in cache with `shareReplay`

**3. Stale Data**

- Problem: Cached responses return outdated data
- Solution: Implement TTL (Time-To-Live) and cache invalidation

### LRU (Least Recently Used) Cache

```typescript
// services/lru-cache.service.ts
import { Injectable } from '@angular/core';
import { HttpResponse } from '@angular/common/http';

interface CacheEntry {
  response: HttpResponse<unknown>;
  timestamp: number;
}

@Injectable({
  providedIn: 'root',
})
export class LRUCacheService {
  private cache = new Map<string, CacheEntry>();
  private readonly maxSize = 100;
  private readonly defaultTTL = 5 * 60 * 1000; // 5 minutes

  get(url: string): HttpResponse<unknown> | null {
    const entry = this.cache.get(url);
    if (!entry) return null;

    // Check TTL
    if (Date.now() - entry.timestamp > this.defaultTTL) {
      this.cache.delete(url);
      return null;
    }

    // Move to end (most recently used)
    this.cache.delete(url);
    this.cache.set(url, entry);

    return entry.response;
  }

  set(url: string, response: HttpResponse<unknown>): void {
    // Remove oldest if at capacity
    if (this.cache.size >= this.maxSize) {
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }

    this.cache.set(url, {
      response,
      timestamp: Date.now(),
    });
  }
}
```

### In-Flight Request Deduplication

Prevents duplicate parallel requests using `shareReplay`:

```typescript
// services/request-deduplication.service.ts
import { Injectable } from '@angular/core';
import { Observable, share } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class RequestDeduplicationService {
  private inFlightRequests = new Map<string, Observable<unknown>>();

  deduplicate<T>(key: string, request: () => Observable<T>): Observable<T> {
    // Return existing request if in-flight
    if (this.inFlightRequests.has(key)) {
      return this.inFlightRequests.get(key) as Observable<T>;
    }

    // Create new request with share operator
    const sharedRequest = request().pipe(
      share({
        // Remove from map when complete
        resetOnComplete: () => {
          this.inFlightRequests.delete(key);
        },
      }),
    );

    this.inFlightRequests.set(key, sharedRequest);
    return sharedRequest;
  }
}
```

**Usage in Interceptor**:

```typescript
export const deduplicationInterceptor: HttpInterceptorFn = (req, next) => {
  const dedup = inject(RequestDeduplicationService);

  // Only deduplicate GET requests
  if (req.method !== 'GET') {
    return next(req);
  }

  return dedup.deduplicate(req.urlWithParams, () => next(req));
};
```

### Cache Invalidation on Mutations

```typescript
export class TaskService {
  private http = inject(HttpClient);
  private cache = inject(HttpCacheService);

  createTask(task: CreateTaskRequest): Observable<Task> {
    return this.http.post<Task>('/api/tasks', task).pipe(
      tap(() => {
        // Invalidate all task-related caches
        this.cache.clearPattern(/\/api\/tasks/);
      }),
    );
  }

  updateTask(id: string, updates: Partial<Task>): Observable<Task> {
    return this.http.put<Task>(`/api/tasks/${id}`, updates).pipe(
      tap(() => {
        // Invalidate specific task and list caches
        this.cache.clear(`/api/tasks/${id}`);
        this.cache.clearPattern(/\/api\/tasks($|\?)/);
      }),
    );
  }
}
```

### Conditional Caching with HttpContext

Control caching per-request using HttpContext:

```typescript
// Define context token
export const CACHE_ENABLED = new HttpContextToken<boolean>(() => true);
export const CACHE_TTL = new HttpContextToken<number>(() => 5 * 60 * 1000);

// Use in interceptor
export const cacheInterceptor: HttpInterceptorFn = (req, next) => {
  const cache = inject(HttpCacheService);

  // Check if caching is enabled for this request
  if (!req.context.get(CACHE_ENABLED) || req.method !== 'GET') {
    return next(req);
  }

  // Get custom TTL if provided
  const ttl = req.context.get(CACHE_TTL);

  // Check cache
  const cached = cache.getWithTTL(req.urlWithParams, ttl);
  if (cached) {
    return of(cached);
  }

  // Make request and cache
  return next(req).pipe(
    tap((event) => {
      if (event instanceof HttpResponse) {
        cache.setWithTTL(req.urlWithParams, event, ttl);
      }
    }),
  );
};

// Disable caching for specific request
this.http.get('/api/tasks', {
  context: new HttpContext().set(CACHE_ENABLED, false),
});

// Custom TTL for request
this.http.get('/api/stats', {
  context: new HttpContext().set(CACHE_TTL, 60000), // 1 minute
});
```

## Security Best Practices

### JWT Token Handling

```typescript
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const tokenService = inject(TokenService);
  const router = inject(Router);

  // Get token
  const token = tokenService.getToken();
  if (!token) {
    return next(req);
  }

  // Check token expiration
  if (tokenService.isTokenExpired(token)) {
    tokenService.removeToken();
    router.navigate(['/auth/login']);
    return throwError(() => new Error('Token expired'));
  }

  // Add token to request
  const authReq = req.clone({
    setHeaders: { Authorization: `Bearer ${token}` },
  });

  return next(authReq);
};
```

### CSRF Protection

```typescript
export const csrfInterceptor: HttpInterceptorFn = (req, next) => {
  // Skip for GET, HEAD, OPTIONS
  if (['GET', 'HEAD', 'OPTIONS'].includes(req.method)) {
    return next(req);
  }

  // Get CSRF token from cookie or meta tag
  const csrfToken = getCsrfToken();

  if (csrfToken) {
    const secureReq = req.clone({
      setHeaders: { 'X-CSRF-TOKEN': csrfToken },
    });
    return next(secureReq);
  }

  return next(req);
};
```

### 401 Error Handling and Redirect

```typescript
export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  const router = inject(Router);
  const tokenService = inject(TokenService);
  const notification = inject(NotificationService);

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401) {
        // Clear token and redirect to login
        tokenService.removeToken();
        router.navigate(['/auth/login']);
        notification.error('Session expired. Please login again.');
      }

      return throwError(() => error);
    }),
  );
};
```

## Service Migration: Promises to Observables

### Before (Promises)

```typescript
// api.service.ts
@Injectable({ providedIn: 'root' })
export class ApiService {
  private http = inject(HttpClient);

  async get<T>(url: string): Promise<T> {
    return firstValueFrom(this.http.get<T>(url));
  }

  async post<T>(url: string, body: unknown): Promise<T> {
    const token = localStorage.getItem('token'); // Manual token
    return firstValueFrom(
      this.http.post<T>(url, body, {
        headers: { Authorization: `Bearer ${token}` },
      }),
    );
  }
}
```

### After (Observables)

```typescript
// api.service.ts
@Injectable({ providedIn: 'root' })
export class ApiService {
  private http = inject(HttpClient);

  get<T>(url: string): Observable<T> {
    return this.http.get<T>(url);
    // Auth token added by interceptor
    // Errors handled by interceptor
    // Loading state managed by interceptor
  }

  post<T>(url: string, body: unknown): Observable<T> {
    return this.http.post<T>(url, body);
    // All cross-cutting concerns handled by interceptors
  }
}
```

### Component Usage

```typescript
export class MyComponent {
  private api = inject(ApiService);
  protected dataState = new AsyncState<Data[]>();

  async loadData(): Promise<void> {
    await this.dataState.execute(async () => {
      // Convert Observable to Promise
      return firstValueFrom(this.api.get<Data[]>('/api/data'));
    });
  }

  // Or use Observable directly
  protected data$ = this.api.get<Data[]>('/api/data');
}
```

## Advanced Patterns

### Request Deduplication

```typescript
// services/request-deduplication.service.ts
import { Injectable } from '@angular/core';
import { Observable, share } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class RequestDeduplicationService {
  private inFlightRequests = new Map<string, Observable<unknown>>();

  deduplicate<T>(key: string, request: () => Observable<T>): Observable<T> {
    if (this.inFlightRequests.has(key)) {
      return this.inFlightRequests.get(key) as Observable<T>;
    }

    const sharedRequest = request().pipe(
      share({
        resetOnComplete: () => {
          this.inFlightRequests.delete(key);
        },
      }),
    );

    this.inFlightRequests.set(key, sharedRequest);
    return sharedRequest;
  }
}
```

### Conditional Loading Indicator

```typescript
// Skip loading for background requests
this.http.get('/api/data', {
  headers: new HttpHeaders({ 'X-Skip-Loading': 'true' }),
});
```

### Cache Invalidation

```typescript
// Clear cache after mutation
export class TaskService {
  private http = inject(HttpClient);
  private cache = inject(HttpCacheService);

  createTask(task: CreateTaskRequest): Observable<Task> {
    return this.http.post<Task>('/api/tasks', task).pipe(
      tap(() => {
        // Invalidate tasks list cache
        this.cache.clearPattern(/\/api\/tasks/);
      }),
    );
  }
}
```

## Testing

### Testing with Interceptors

```typescript
import { TestBed } from '@angular/core/testing';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { authInterceptor } from './auth.interceptor';

describe('AuthInterceptor', () => {
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(withInterceptors([authInterceptor])),
        provideHttpClientTesting(),
      ],
    });

    httpMock = TestBed.inject(HttpTestingController);
  });

  it('should add auth token', () => {
    // Test implementation
  });
});
```

## Success Criteria

Before marking HTTP layer implementation complete:

- [ ] Auth interceptor configured (no manual token injection)
- [ ] Error interceptor handles all HTTP errors
- [ ] Loading interceptor manages global state
- [ ] Retry logic configured for transient failures
- [ ] Cache interceptor prevents duplicate requests
- [ ] All services return Observables (not Promises)
- [ ] TokenService abstracts token management
- [ ] NotificationService replaces console.log
- [ ] LoadingService provides global loading state
- [ ] Tests cover interceptor logic

## References

### Project-Specific

- GitHub Issue #257: HTTP Layer Improvements
- `.claude/agents/agent-frontend.md`: Complete frontend patterns

### Angular Functional Interceptors (2025)

- [Intercepting requests and responses • Angular](https://angular.dev/guide/http/interceptors)
- [Functional Approach for HTTP Interceptors | JavaScript in Plain English](https://javascript.plainenglish.io/adopting-a-functional-approach-for-http-interceptors-in-angular-c5109d87f2b2)
- [Mastering Modern Angular: Functional Route Guards & Interceptors | Medium](https://manishboge.medium.com/mastering-modern-angular-functional-route-guards-interceptors-explained-492d0f9dc86e)
- [HTTP interceptors in Angular (2025 update) | Angular Training](https://blog.angulartraining.com/http-interceptors-in-angular-61dcf80b6bdd)

### Caching Strategies

- [Client Side Caching With Interceptors | DEV Community](https://dev.to/this-is-angular/client-side-caching-with-interceptors-ii)
- [Caching with HttpInterceptor in Angular | LogRocket](https://blog.logrocket.com/caching-with-httpinterceptor-in-angular/)
- [Angular: Caching service using Http Interceptor | Medium](https://medium.com/geekculture/angular-caching-service-using-http-interceptor-ce713f421c3b)
- [Optimizing Angular Performance with HttpInterceptor Caching | OpenReplay](https://blog.openreplay.com/optimizing-angular-performance-with-httpinterceptor-caching/)

### Security Best Practices

- [Angular Security Best Practices 2025 | Security Articles](https://hub.corgea.com/articles/angular-security-best-practices)
- [Angular v15 introduces functional HTTP interceptors | HeroDevs](https://www.herodevs.com/blog-posts/angular-15-introduces-functional-http-interceptors)
