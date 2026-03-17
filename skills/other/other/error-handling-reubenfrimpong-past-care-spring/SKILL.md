---
name: error-handling
description: Error handling and reporting patterns for both frontend and backend in PastCare
disable-model-invocation: true
argument-hint: [component or service to add error handling]
---

# Error Handling Skill

Implement error handling for: $ARGUMENTS

## Backend Error Response Format

### Standard Error Response
```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Map<String, Object>> handleValidationErrors(
            MethodArgumentNotValidException ex) {
        Map<String, List<String>> fieldErrors = new HashMap<>();

        ex.getBindingResult().getFieldErrors().forEach(error -> {
            fieldErrors.computeIfAbsent(error.getField(), k -> new ArrayList<>())
                .add(error.getDefaultMessage());
        });

        Map<String, Object> response = new HashMap<>();
        response.put("status", 400);
        response.put("error", "Validation Failed");
        response.put("timestamp", Instant.now());
        response.putAll(fieldErrors);  // Field errors at root level

        return ResponseEntity.badRequest().body(response);
    }
}
```

### Field-Level Error Format
```json
{
  "status": 400,
  "error": "Validation Failed",
  "timestamp": "2024-01-15T10:30:00Z",
  "email": ["Email is required", "Invalid email format"],
  "phone": ["Phone number must be 10 digits"]
}
```

### Business Logic Errors
```java
@ExceptionHandler(BusinessException.class)
public ResponseEntity<Map<String, Object>> handleBusinessError(BusinessException ex) {
    return ResponseEntity
        .status(ex.getStatus())
        .body(Map.of(
            "status", ex.getStatus().value(),
            "error", ex.getMessage(),
            "timestamp", Instant.now()
        ));
}
```

### Access Denied
```java
@ExceptionHandler(AccessDeniedException.class)
public ResponseEntity<Map<String, Object>> handleAccessDenied(AccessDeniedException ex) {
    return ResponseEntity
        .status(HttpStatus.FORBIDDEN)
        .body(Map.of(
            "status", 403,
            "error", "Access denied",
            "timestamp", Instant.now()
        ));
}
```

## Frontend Error Handling

### HTTP Error Interceptor
```typescript
@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
  constructor(
    private messageService: MessageService,
    private router: Router
  ) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(req).pipe(
      catchError((error: HttpErrorResponse) => {
        switch (error.status) {
          case 401:
            this.router.navigate(['/login']);
            break;
          case 403:
            this.messageService.add({
              severity: 'error',
              summary: 'Access Denied',
              detail: 'You do not have permission to perform this action'
            });
            break;
          case 404:
            this.messageService.add({
              severity: 'error',
              summary: 'Not Found',
              detail: 'The requested resource was not found'
            });
            break;
          case 500:
            this.messageService.add({
              severity: 'error',
              summary: 'Server Error',
              detail: 'An unexpected error occurred. Please try again.'
            });
            break;
        }
        return throwError(() => error);
      })
    );
  }
}
```

### Component-Level Error Handling
```typescript
export class MemberFormComponent {
  errorMessage = signal<string | null>(null);
  backendFieldErrors = signal<Record<string, string[]>>({});
  isLoading = signal(false);

  saveMember(): void {
    this.clearErrors();
    this.isLoading.set(true);

    this.memberService.save(this.form.value).subscribe({
      next: (result) => {
        this.isLoading.set(false);
        this.messageService.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Member saved successfully'
        });
        this.dialogRef.close(result);
      },
      error: (err: HttpErrorResponse) => {
        this.isLoading.set(false);
        this.handleError(err);
      }
    });
  }

  private handleError(error: HttpErrorResponse): void {
    // Parse field-level validation errors
    if (error.status === 400) {
      this.parseAndSetBackendFieldErrors(error);
    }

    // Set general error message
    const message = error.error?.error || error.error?.message || 'An error occurred';
    this.errorMessage.set(message);
  }

  private parseAndSetBackendFieldErrors(error: HttpErrorResponse): void {
    const fieldErrors: Record<string, string[]> = {};

    if (error.error && typeof error.error === 'object') {
      for (const key of Object.keys(error.error)) {
        // Skip non-field keys
        if (['message', 'status', 'timestamp', 'path', 'error'].includes(key)) {
          continue;
        }
        const value = error.error[key];
        if (Array.isArray(value) && value.length > 0 && typeof value[0] === 'string') {
          fieldErrors[key] = value;
        }
      }
    }

    this.backendFieldErrors.set(fieldErrors);
  }

  getBackendFieldErrors(fieldName: string): string[] {
    return this.backendFieldErrors()[fieldName] || [];
  }

  private clearErrors(): void {
    this.errorMessage.set(null);
    this.backendFieldErrors.set({});
  }
}
```

### Error Display in Templates
```html
<!-- General error banner -->
@if (errorMessage()) {
  <div class="error-banner">
    <i class="pi pi-exclamation-circle"></i>
    <span>{{ errorMessage() }}</span>
    <button (click)="errorMessage.set(null)" class="close-btn">
      <i class="pi pi-times"></i>
    </button>
  </div>
}

<!-- Field-level errors -->
<div class="form-field">
  <label for="email">Email <span class="required">*</span></label>
  <input id="email" formControlName="email" pInputText>

  <!-- Frontend validation errors -->
  @if (form.get('email')?.invalid && form.get('email')?.touched) {
    @if (form.get('email')?.errors?.['required']) {
      <div class="error-message">Email is required</div>
    }
    @if (form.get('email')?.errors?.['email']) {
      <div class="error-message">Invalid email format</div>
    }
  }

  <!-- Backend validation errors -->
  @for (error of getBackendFieldErrors('email'); track error) {
    <div class="error-message backend-error">{{ error }}</div>
  }
</div>
```

## Error Styling

### Error Message
```css
.error-message {
  color: #dc2626;
  font-size: 0.75rem;
  margin-top: 0.25rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.error-message::before {
  content: '\e936'; /* pi-exclamation-circle */
  font-family: 'primeicons';
}
```

### Backend Error (Distinguished)
```css
.error-message.backend-error {
  color: #dc2626;
  background: #fef2f2;
  padding: 0.375rem 0.625rem;
  border-radius: 0.375rem;
  border: 1px solid #fee2e2;
  margin-top: 0.375rem;
}
```

### Error Banner
```css
.error-banner {
  background: #fef2f2;
  border: 1px solid #fee2e2;
  border-radius: 0.75rem;
  padding: 1rem;
  color: #dc2626;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.error-banner i {
  font-size: 1.25rem;
}

.error-banner .close-btn {
  margin-left: auto;
  background: none;
  border: none;
  color: #dc2626;
  cursor: pointer;
}
```

### Input Error State
```css
input.ng-invalid.ng-touched,
.has-error input {
  border-color: #ef4444;
}

input.ng-invalid.ng-touched:focus {
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}
```

## Error Scenarios

### Network Errors
```typescript
catchError((error) => {
  if (error.status === 0) {
    this.messageService.add({
      severity: 'error',
      summary: 'Connection Error',
      detail: 'Unable to connect to server. Check your internet connection.'
    });
  }
  return throwError(() => error);
})
```

### Timeout Errors
```typescript
this.http.get('/api/data').pipe(
  timeout(30000),
  catchError((error) => {
    if (error.name === 'TimeoutError') {
      this.messageService.add({
        severity: 'warn',
        summary: 'Request Timeout',
        detail: 'The request took too long. Please try again.'
      });
    }
    return throwError(() => error);
  })
);
```

### Optimistic Update Rollback
```typescript
// Save original state
const originalData = [...this.members()];

// Optimistically update
this.members.update(m => m.filter(x => x.id !== id));

// If error, rollback
this.memberService.delete(id).subscribe({
  error: () => {
    this.members.set(originalData);
    this.messageService.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to delete. Changes reverted.'
    });
  }
});
```

## Best Practices

### DO:
- Always show user-friendly error messages
- Log detailed errors to console for debugging
- Preserve form input when errors occur
- Clear errors when user starts fixing
- Provide actionable guidance when possible

### DON'T:
- Show stack traces to users
- Use generic "Something went wrong" without context
- Clear form data on validation errors
- Ignore 401/403 errors (handle auth properly)
- Swallow errors silently
