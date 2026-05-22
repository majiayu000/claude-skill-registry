---
name: vendix-frontend-state
description: State management patterns.
metadata:
  scope: [root]
  auto_invoke: "Managing State"
---
# Vendix Frontend State Management

> **Services, Toast & Notifications** - Estado reactivo, servicios HTTP y sistema de notificaciones.

## 🎯 State Management Principles

**Vendix usa un enfoque híbrido:**
- **Servicios con BehaviorSubject** para estado global
- **Señales (Angular 20)** para estado local de componentes
- **RxJS Observables** para operaciones asíncronas
- **ToastService** para notificaciones al usuario

---

## 📡 Service Pattern with BehaviorSubject

### Base Service Pattern

```typescript
import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { BehaviorSubject, Observable, throwError, takeUntil, Subject } from 'rxjs';
import { catchError, tap, shareReplay } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class {Module}Service {
  private http = inject(HttpClient);
  private toast_service = inject(ToastService);

  private api_url = '/api/{entities}';

  // Loading states
  private isLoading$$ = new BehaviorSubject<boolean>(false);
  isLoading$ = this.isLoading$$.asObservable();

  // Data states
  private entities$$ = new BehaviorSubject<{Entity}[]>([]);
  entities$ = this.entities$$.asObservable();

  // Error states
  private error$$ = new BehaviorSubject<string | null>(null);
  error$ = this.error$$.asObservable();

  // Cleanup
  private destroy$ = new Subject<void>();

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }

  // CRUD Operations
  getEntities(params?: any): Observable<{Entity}[]> {
    this.setLoading(true);
    this.setError(null);

    let http_params = new HttpParams();
    if (params) {
      Object.keys(params).forEach(key => {
        if (params[key] !== null && params[key] !== undefined) {
          http_params = http_params.set(key, params[key]);
        }
      });
    }

    return this.http.get<{Entity}[]>(this.api_url, { params: http_params }).pipe(
      tap(entities => {
        this.entities$$.next(entities);
        this.setLoading(false);
      }),
      catchError(error => {
        this.setError(error.message);
        this.setLoading(false);
        this.toast_service.show({
          variant: 'error',
          message: 'Error loading entities',
        });
        return throwError(() => error);
      }),
      takeUntil(this.destroy$),
    );
  }

  getEntity(id: number): Observable<{Entity}> {
    return this.http.get<{Entity}>(`${this.api_url}/${id}`).pipe(
      catchError(error => {
        this.toast_service.show({
          variant: 'error',
          message: 'Error loading entity',
        });
        return throwError(() => error);
      }),
    );
  }

  createEntity(dto: Create{Entity}Dto): Observable<{Entity}> {
    this.setLoading(true);

    return this.http.post<{Entity}>(this.api_url, dto).pipe(
      tap(entity => {
        const current_entities = this.entities$$.value;
        this.entities$$.next([...current_entities, entity]);
        this.setLoading(false);
        this.toast_service.show({
          variant: 'success',
          message: 'Entity created successfully',
        });
      }),
      catchError(error => {
        this.setLoading(false);
        this.toast_service.show({
          variant: 'error',
          message: 'Error creating entity',
        });
        return throwError(() => error);
      }),
    );
  }

  updateEntity(id: number, dto: Update{Entity}Dto): Observable<{Entity}> {
    this.setLoading(true);

    return this.http.put<{Entity}>(`${this.api_url}/${id}`, dto).pipe(
      tap(updated_entity => {
        const current_entities = this.entities$$.value;
        const updated_entities = current_entities.map(entity =>
          entity.id === id ? updated_entity : entity
        );
        this.entities$$.next(updated_entities);
        this.setLoading(false);
        this.toast_service.show({
          variant: 'success',
          message: 'Entity updated successfully',
        });
      }),
      catchError(error => {
        this.setLoading(false);
        this.toast_service.show({
          variant: 'error',
          message: 'Error updating entity',
        });
        return throwError(() => error);
      }),
    );
  }

  deleteEntity(id: number): Observable<void> {
    this.setLoading(true);

    return this.http.delete<void>(`${this.api_url}/${id}`).pipe(
      tap(() => {
        const current_entities = this.entities$$.value;
        const filtered_entities = current_entities.filter(entity => entity.id !== id);
        this.entities$$.next(filtered_entities);
        this.setLoading(false);
        this.toast_service.show({
          variant: 'success',
          message: 'Entity deleted successfully',
        });
      }),
      catchError(error => {
        this.setLoading(false);
        this.toast_service.show({
          variant: 'error',
          message: 'Error deleting entity',
        });
        return throwError(() => error);
      }),
    );
  }

  // State helpers
  private setLoading(is_loading: boolean) {
    this.isLoading$$.next(is_loading);
  }

  private setError(error: string | null) {
    this.error$$.next(error);
  }

  // Getters for current values
  get isLoading(): boolean {
    return this.isLoading$$.value;
  }

  get entities(): {Entity}[] {
    return this.entities$$.value;
  }

  get error(): string | null {
    return this.error$$.value;
  }
}
```

---

## 🔔 ToastService Pattern

**File:** `shared/components/toast/toast.service.ts`

```typescript
import { Injectable, signal, computed } from '@angular/core';

export interface Toast {
  id: string;
  variant: 'success' | 'error' | 'warning' | 'info';
  message: string;
  duration?: number;
  leaving?: boolean;
}

@Injectable({
  providedIn: 'root',
})
export class ToastService {
  private toasts_sig = signal<Toast[]>([]);
  toasts = this.toasts_sig.asReadonly();

  private default_duration = 3500;

  show(input: Partial<Toast> & { message: string }) {
    const toast: Toast = {
      id: Math.random().toString(36).slice(2),
      variant: input.variant ?? 'default',
      message: input.message,
      duration: input.duration ?? this.default_duration,
      leaving: false,
    };

    this.toasts_sig.update(toasts => [toast, ...toasts]);

    // Auto-remove after duration
    setTimeout(() => {
      this.remove(toast.id);
    }, toast.duration);
  }

  remove(id: string) {
    this.toasts_sig.update(toasts =>
      toasts.filter(toast => toast.id !== id)
    );
  }

  // Convenience methods
  success(message: string, duration?: number) {
    this.show({ variant: 'success', message, duration });
  }

  error(message: string, duration?: number) {
    this.show({ variant: 'error', message, duration });
  }

  warning(message: string, duration?: number) {
    this.show({ variant: 'warning', message, duration });
  }

  info(message: string, duration?: number) {
    this.show({ variant: 'info', message, duration });
  }
}
```

### Toast Component

**File:** `shared/components/toast/toast.component.ts`

```typescript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ToastService, Toast } from './toast.service';

@Component({
  selector: 'app-toast',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="toast-container">
      @for (toast of toasts(); track toast.id) {
        <div
          class="toast"
          [class.success]="toast.variant === 'success'"
          [class.error]="toast.variant === 'error'"
          [class.warning]="toast.variant === 'warning'"
          [class.info]="toast.variant === 'info'"
          [class.leaving]="toast.leaving">
          <div class="toast-content">
            <span>{{ toast.message }}</span>
            <button (click)="remove(toast.id)">×</button>
          </div>
        </div>
      }
    </div>
  `,
  styleUrls: ['./toast.component.scss'],
})
export class ToastComponent {
  toasts = this.toast_service.toasts;

  constructor(private toast_service: ToastService) {}

  remove(id: string) {
    this.toast_service.remove(id);
  }
}
```

---

## 🔌 HTTP Client with Interceptors

### Auth Interceptor

**File:** `core/interceptors/auth.interceptor.ts`

```typescript
import { Injectable } from '@angular/core';
import {
  HttpInterceptor,
  HttpRequest,
  HttpHandler,
  HttpEvent,
} from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from '@/app/core/services/auth.service';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private auth_service: AuthService) {}

  intercept(
    request: HttpRequest<any>,
    next: HttpHandler,
  ): Observable<HttpEvent<any>> {
    const token = this.auth_service.getToken();

    if (token) {
      request = request.clone({
        setHeaders: {
          Authorization: `Bearer ${token}`,
        },
      });
    }

    return next.handle(request);
  }
}
```

### Error Interceptor

**File:** `core/interceptors/error.interceptor.ts`

```typescript
import { Injectable } from '@angular/core';
import {
  HttpInterceptor,
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpErrorResponse,
} from '@angular/common/http';
import { Observable, throwError, catchError } from 'rxjs';
import { Router } from '@angular/router';
import { ToastService } from '@/app/shared/components/toast/toast.service';

@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
  constructor(
    private router: Router,
    private toast_service: ToastService,
  ) {}

  intercept(
    request: HttpRequest<any>,
    next: HttpHandler,
  ): Observable<HttpEvent<any>> {
    return next.handle(request).pipe(
      catchError((error: HttpErrorResponse) => {
        if (error.status === 401) {
          // Unauthorized - redirect to login
          this.router.navigate(['/auth/login']);
          this.toast_service.error('Session expired. Please login again.');
        } else if (error.status === 403) {
          // Forbidden
          this.toast_service.error('You do not have permission to perform this action.');
        } else if (error.status === 404) {
          // Not found
          this.toast_service.error('Resource not found.');
        } else if (error.status >= 500) {
          // Server error
          this.toast_service.error('Server error. Please try again later.');
        } else {
          // Other errors
          this.toast_service.error(error.error?.message || 'An error occurred');
        }

        return throwError(() => error);
      }),
    );
  }
}
```

---

## 🎯 Using Services in Components

### Component with Service

```typescript
import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { {Module}Service } from './services/{module}.service';
import { {Entity} } from './interfaces/{module}.interface';

@Component({
  selector: 'app-{module}',
  standalone: true,
  imports: [CommonModule],
  template: `
    @if (isLoading()) {
      <div>Loading...</div>
    } @else if (error()) {
      <div class="error">{{ error() }}</div>
    } @else {
      <div *ngFor="let entity of entities()">
        {{ entity.name }}
      </div>
    }
  `,
})
export class {Module}Component implements OnInit {
  private {module}_service = inject({Module}Service);

  // Using signals for local state (Angular 20)
  isLoading = toSignal(this.{module}_service.isLoading$, { initialValue: false });
  error = toSignal(this.{module}_service.error$, { initialValue: null });
  entities = toSignal(this.{module}_service.entities$, { initialValue: [] });

  ngOnInit() {
    this.{module}_service.getEntities().subscribe();
  }

  onDelete(entity: {Entity}) {
    this.{module}_service.deleteEntity(entity.id).subscribe();
  }
}
```

---

## 🔄 Async Pipe Usage

### Template with Async Pipe

```typescript
@Component({
  template: `
    @if (entities$ | async; as entities) {
      <div *ngFor="let entity of entities">
        {{ entity.name }}
      </div>
    }

    @if (isLoading$ | async) {
      <div>Loading...</div>
    }
  `,
})
export class MyComponent {
  entities$ = this.service.entities$;
  isLoading$ = this.service.isLoading$;
}
```

---

## 🔍 Key Files Reference

| File | Purpose |
|------|---------|
| `shared/components/toast/toast.service.ts` | Notification system |
| `core/interceptors/auth.interceptor.ts` | JWT injection |
| `core/interceptors/error.interceptor.ts` | Global error handling |
| `*/services/*.service.ts` | Business logic and API |

---

## Related Skills

- `vendix-frontend-module` - Module structure with services
- `vendix-frontend-component` - Component patterns
- `vendix-naming-conventions` - Naming conventions (CRITICAL)
