---
name: angular-api-service
description: Use when creating API services for backend communication with proper patterns for caching, error handling, and type safety.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Angular API Service Development Workflow

## When to Use This Skill

- Creating new API service for backend communication
- Adding caching to API calls
- Implementing file upload/download
- Adding custom headers or interceptors

## Pre-Flight Checklist

- [ ] Identify backend API base URL
- [ ] **Read the design system docs** for the target application (see below)
- [ ] List all endpoints to implement
- [ ] Determine caching requirements
- [ ] Search existing services: `grep "{Feature}ApiService" --include="*.ts"`

## 🎨 Design System Documentation (MANDATORY)

**Before creating any API service, read the design system documentation for your target application:**

| Application                       | Design System Location                           |
| --------------------------------- | ------------------------------------------------ |
| **WebV2 Apps**                    | `docs/design-system/`                            |
| **TextSnippetClient**             | `src/PlatformExampleAppWeb/apps/playground-text-snippet/docs/design-system/` |

**Key docs to read:**

- `README.md` - Component overview, base classes, library summary
- `07-technical-guide.md` - Implementation checklist, best practices
- `06-state-management.md` - State management and API integration patterns

## File Location

```
src/PlatformExampleAppWeb/libs/apps-domains/src/lib/
└── {domain}/
    └── services/
        └── {feature}-api.service.ts
```

## Pattern 1: Basic CRUD API Service

```typescript
// {feature}-api.service.ts
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { PlatformApiService } from '@libs/platform-core';
import { environment } from '@env/environment';

// ═══════════════════════════════════════════════════════════════════════════
// DTOs (can be in separate file)
// ═══════════════════════════════════════════════════════════════════════════

export interface FeatureDto {
    id: string;
    name: string;
    code: string;
    status: FeatureStatus;
    createdDate: Date;
}

export interface FeatureListQuery {
    searchText?: string;
    statuses?: FeatureStatus[];
    skipCount?: number;
    maxResultCount?: number;
}

export interface PagedResult<T> {
    items: T[];
    totalCount: number;
}

export interface SaveFeatureCommand {
    id?: string;
    name: string;
    code: string;
    status: FeatureStatus;
}

// ═══════════════════════════════════════════════════════════════════════════
// API SERVICE
// ═══════════════════════════════════════════════════════════════════════════

@Injectable({ providedIn: 'root' })
export class FeatureApiService extends PlatformApiService {
    // ─────────────────────────────────────────────────────────────────────────
    // CONFIGURATION
    // ─────────────────────────────────────────────────────────────────────────

    protected get apiUrl(): string {
        return environment.apiUrl + '/api/Feature';
    }

    // ─────────────────────────────────────────────────────────────────────────
    // QUERY METHODS
    // ─────────────────────────────────────────────────────────────────────────

    getList(query?: FeatureListQuery): Observable<PagedResult<FeatureDto>> {
        return this.get<PagedResult<FeatureDto>>('', query);
    }

    getById(id: string): Observable<FeatureDto> {
        return this.get<FeatureDto>(`/${id}`);
    }

    getByCode(code: string): Observable<FeatureDto> {
        return this.get<FeatureDto>('/by-code', { code });
    }

    // ─────────────────────────────────────────────────────────────────────────
    // COMMAND METHODS
    // ─────────────────────────────────────────────────────────────────────────

    save(command: SaveFeatureCommand): Observable<FeatureDto> {
        return this.post<FeatureDto>('', command);
    }

    update(id: string, command: Partial<SaveFeatureCommand>): Observable<FeatureDto> {
        return this.put<FeatureDto>(`/${id}`, command);
    }

    delete(id: string): Observable<void> {
        return this.deleteRequest<void>(`/${id}`);
    }

    // ─────────────────────────────────────────────────────────────────────────
    // VALIDATION METHODS
    // ─────────────────────────────────────────────────────────────────────────

    checkCodeExists(code: string, excludeId?: string): Observable<boolean> {
        return this.get<boolean>('/check-code-exists', { code, excludeId });
    }
}
```

## Pattern 2: API Service with Caching

```typescript
@Injectable({ providedIn: 'root' })
export class LookupApiService extends PlatformApiService {
    protected get apiUrl(): string {
        return environment.apiUrl + '/api/Lookup';
    }

    // ─────────────────────────────────────────────────────────────────────────
    // CACHED METHODS
    // ─────────────────────────────────────────────────────────────────────────

    getCountries(): Observable<CountryDto[]> {
        return this.get<CountryDto[]>('/countries', null, {
            enableCache: true,
            cacheKey: 'countries',
            cacheDurationMs: 60 * 60 * 1000 // 1 hour
        });
    }

    getCurrencies(): Observable<CurrencyDto[]> {
        return this.get<CurrencyDto[]>('/currencies', null, {
            enableCache: true,
            cacheKey: 'currencies'
        });
    }

    getTimezones(): Observable<TimezoneDto[]> {
        return this.get<TimezoneDto[]>('/timezones', null, {
            enableCache: true
        });
    }

    // ─────────────────────────────────────────────────────────────────────────
    // CACHE INVALIDATION
    // ─────────────────────────────────────────────────────────────────────────

    invalidateCountriesCache(): void {
        this.clearCache('countries');
    }

    invalidateAllCache(): void {
        this.clearAllCache();
    }
}
```

## Pattern 3: File Upload/Download

```typescript
@Injectable({ providedIn: 'root' })
export class DocumentApiService extends PlatformApiService {
    protected get apiUrl(): string {
        return environment.apiUrl + '/api/Document';
    }

    // ─────────────────────────────────────────────────────────────────────────
    // FILE UPLOAD
    // ─────────────────────────────────────────────────────────────────────────

    upload(file: File, metadata?: DocumentMetadata): Observable<DocumentDto> {
        const formData = new FormData();
        formData.append('file', file, file.name);

        if (metadata) {
            formData.append('metadata', JSON.stringify(metadata));
        }

        return this.postFormData<DocumentDto>('/upload', formData);
    }

    uploadMultiple(files: File[]): Observable<DocumentDto[]> {
        const formData = new FormData();
        files.forEach((file, index) => {
            formData.append(`files[${index}]`, file, file.name);
        });

        return this.postFormData<DocumentDto[]>('/upload-multiple', formData);
    }

    // ─────────────────────────────────────────────────────────────────────────
    // FILE DOWNLOAD
    // ─────────────────────────────────────────────────────────────────────────

    download(id: string): Observable<Blob> {
        return this.getBlob(`/${id}/download`);
    }

    downloadAsBase64(id: string): Observable<string> {
        return this.get<string>(`/${id}/base64`);
    }

    // ─────────────────────────────────────────────────────────────────────────
    // HELPER: Trigger browser download
    // ─────────────────────────────────────────────────────────────────────────

    downloadAndSave(id: string, fileName: string): Observable<void> {
        return this.download(id).pipe(
            tap(blob => {
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.download = fileName;
                link.click();
                window.URL.revokeObjectURL(url);
            }),
            map(() => void 0)
        );
    }
}
```

## Pattern 4: API Service with Custom Headers

```typescript
@Injectable({ providedIn: 'root' })
export class ExternalApiService extends PlatformApiService {
    protected get apiUrl(): string {
        return environment.externalApiUrl;
    }

    // Override to add custom headers
    protected override getDefaultHeaders(): HttpHeaders {
        return super.getDefaultHeaders().set('X-Api-Key', environment.externalApiKey).set('X-Request-Id', this.generateRequestId());
    }

    // Method with custom headers
    getWithCustomHeaders(endpoint: string): Observable<any> {
        return this.get(endpoint, null, {
            headers: {
                'X-Custom-Header': 'custom-value'
            }
        });
    }

    private generateRequestId(): string {
        return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    }
}
```

## Pattern 5: Search/Autocomplete API

```typescript
@Injectable({ providedIn: 'root' })
export class EmployeeApiService extends PlatformApiService {

  protected get apiUrl(): string {
    return environment.apiUrl + '/api/Employee';
  }

  // ─────────────────────────────────────────────────────────────────────────
  // SEARCH WITH DEBOUNCE (use in component)
  // ─────────────────────────────────────────────────────────────────────────

  search(term: string): Observable<EmployeeDto[]> {
    if (!term || term.length < 2) {
      return of([]);
    }

    return this.get<EmployeeDto[]>('/search', {
      searchText: term,
      maxResultCount: 10
    });
  }

  // ─────────────────────────────────────────────────────────────────────────
  // AUTOCOMPLETE WITH CACHING
  // ─────────────────────────────────────────────────────────────────────────

  autocomplete(prefix: string): Observable<AutocompleteItem[]> {
    return this.get<AutocompleteItem[]>('/autocomplete', { prefix }, {
      enableCache: true,
      cacheKey: `autocomplete-${prefix}`,
      cacheDurationMs: 30 * 1000  // 30 seconds
    });
  }
}

// Usage in component with debounce:
@Component({...})
export class EmployeeSearchComponent {
  private searchSubject = new Subject<string>();

  search$ = this.searchSubject.pipe(
    debounceTime(300),
    distinctUntilChanged(),
    switchMap(term => this.employeeApi.search(term))
  );

  onSearchInput(term: string): void {
    this.searchSubject.next(term);
  }
}
```

## Base PlatformApiService Methods

| Method               | Purpose              | Example                                  |
| -------------------- | -------------------- | ---------------------------------------- |
| `get<T>()`           | GET request          | `this.get<User>('/users/1')`             |
| `post<T>()`          | POST request         | `this.post<User>('/users', data)`        |
| `put<T>()`           | PUT request          | `this.put<User>('/users/1', data)`       |
| `patch<T>()`         | PATCH request        | `this.patch<User>('/users/1', partial)`  |
| `deleteRequest<T>()` | DELETE request       | `this.deleteRequest('/users/1')`         |
| `postFormData<T>()`  | POST with FormData   | `this.postFormData('/upload', formData)` |
| `getBlob()`          | GET binary data      | `this.getBlob('/file/download')`         |
| `clearCache()`       | Clear specific cache | `this.clearCache('cacheKey')`            |
| `clearAllCache()`    | Clear all cache      | `this.clearAllCache()`                   |

## Request Options

```typescript
interface RequestOptions {
    // Caching
    enableCache?: boolean;
    cacheKey?: string;
    cacheDurationMs?: number;

    // Headers
    headers?: { [key: string]: string };

    // Response handling
    responseType?: 'json' | 'text' | 'blob' | 'arraybuffer';

    // Progress tracking
    reportProgress?: boolean;
    observe?: 'body' | 'events' | 'response';
}
```

## Anti-Patterns to AVOID

:x: **Using HttpClient directly**

```typescript
// WRONG - bypasses platform features
constructor(private http: HttpClient) { }

// CORRECT - extend PlatformApiService
export class MyApiService extends PlatformApiService { }
```

:x: **Hardcoding URLs**

```typescript
// WRONG
return this.get('https://api.example.com/users');

// CORRECT - use environment
protected get apiUrl() { return environment.apiUrl + '/api/User'; }
```

:x: **Not handling errors in service**

```typescript
// WRONG - let errors propagate unhandled
return this.get('/users');

// CORRECT - component handles via tapResponse
this.userApi.getUsers().pipe(
    this.tapResponse(
        users => {
            /* success */
        },
        error => {
            /* handle error */
        }
    )
);
```

:x: **Missing type safety**

```typescript
// WRONG - returns any
getUser(id: string) {
  return this.get(`/users/${id}`);
}

// CORRECT - typed response
getUser(id: string): Observable<UserDto> {
  return this.get<UserDto>(`/users/${id}`);
}
```

## Verification Checklist

- [ ] Extends `PlatformApiService`
- [ ] `apiUrl` getter returns correct base URL
- [ ] All methods have return type annotations
- [ ] DTOs defined for request/response
- [ ] Caching configured for appropriate endpoints
- [ ] File operations use `postFormData`/`getBlob`
- [ ] Validation endpoints return `boolean`
- [ ] `@Injectable({ providedIn: 'root' })` for singleton
