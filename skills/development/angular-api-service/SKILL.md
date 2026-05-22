---
name: angular-api-service
description: Use when creating API services for backend communication with proper patterns for caching, error handling, and type safety.
---

# Angular API Service Development

## Required Reading

**For comprehensive TypeScript/Angular patterns, you MUST read:**

- **`docs/claude/frontend-typescript-complete-guide.md`** - Complete patterns for API services, HTTP patterns, error handling

---

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

## API Service Pattern

```typescript
@Injectable({ providedIn: 'root' })
export class EmployeeApiService extends PlatformApiService {
    protected get apiUrl(): string {
        return environment.apiUrl + '/api/Employee';
    }

    // GET list
    getEmployees(query?: GetEmployeeListQuery): Observable<PagedResult<EmployeeDto>> {
        return this.get<PagedResult<EmployeeDto>>('', query);
    }

    // GET single
    getEmployee(id: string): Observable<EmployeeDto> {
        return this.get<EmployeeDto>(`/${id}`);
    }

    // POST command
    saveEmployee(command: SaveEmployeeCommand): Observable<SaveEmployeeCommandResult> {
        return this.post<SaveEmployeeCommandResult>('', command);
    }

    // POST with caching
    searchEmployees(criteria: SearchCriteria): Observable<EmployeeDto[]> {
        return this.post<EmployeeDto[]>('/search', criteria, {
            enableCache: true
        });
    }

    // DELETE
    deleteEmployee(id: string): Observable<void> {
        return this.delete(`/${id}`);
    }

    // File upload
    uploadDocument(id: string, file: File): Observable<DocumentDto> {
        const formData = new FormData();
        formData.append('file', file);
        return this.post<DocumentDto>(`/${id}/documents`, formData);
    }
}
```

## Service Location

```
src/PlatformExampleAppWeb/libs/apps-domains/src/lib/
├── growth/
│   └── employee/
│       ├── employee-api.service.ts
│       ├── employee.model.ts
│       └── employee.validators.ts
├── talents/
│   └── candidate/
│       ├── candidate-api.service.ts
│       └── candidate.model.ts
```

## Usage in Component/Store

```typescript
// In store
public loadEmployees = this.effectSimple(
  (query: GetEmployeeListQuery) => this.employeeApi.getEmployees(query).pipe(
    this.tapResponse(result => this.updateState({
      employees: result.items,
      totalCount: result.totalCount
    }))
  ),
  'loadEmployees'
);

// In component
this.employeeApi.saveEmployee(command)
  .pipe(
    this.observerLoadingErrorState('save'),
    this.tapResponse(
      result => this.router.navigate(['/employees', result.id]),
      error => this.showError(error)
    ),
    this.untilDestroyed()
  )
  .subscribe();
```

## Key APIs

| Method                       | Purpose             |
| ---------------------------- | ------------------- |
| `get<T>(path, params?)`      | HTTP GET request    |
| `post<T>(path, body, opts?)` | HTTP POST request   |
| `put<T>(path, body)`         | HTTP PUT request    |
| `delete(path)`               | HTTP DELETE request |

## Request/Response Types

```typescript
// Query DTO (matches backend)
export interface GetEmployeeListQuery {
    skipCount?: number;
    maxResultCount?: number;
    searchText?: string;
    statuses?: EmployeeStatus[];
}

// Command DTO
export interface SaveEmployeeCommand {
    id?: string;
    firstName: string;
    lastName: string;
    email: string;
}

// Paged result
export interface PagedResult<T> {
    items: T[];
    totalCount: number;
}
```

## Anti-Patterns

- Using `HttpClient` directly instead of `PlatformApiService`
- Hardcoding API URLs (use `apiUrl` property)
- Not using type parameters for responses
- Manual error handling (use `tapResponse`)
