---
name: form-validation
description: Form validation patterns for both frontend (Angular) and backend (Spring) in PastCare
disable-model-invocation: true
argument-hint: [form or entity to add validation]
---

# Form Validation Skill

Implement validation for: $ARGUMENTS

## Backend Validation (Spring Boot)

### Entity/DTO Validation Annotations
```java
public class MemberRequest {

    @NotBlank(message = "First name is required")
    @Size(min = 2, max = 100, message = "First name must be 2-100 characters")
    private String firstName;

    @NotBlank(message = "Last name is required")
    @Size(min = 2, max = 100, message = "Last name must be 2-100 characters")
    private String lastName;

    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    private String email;

    @Pattern(regexp = "^[0-9]{10}$", message = "Phone must be 10 digits")
    private String phone;

    @NotNull(message = "Date of birth is required")
    @Past(message = "Date of birth must be in the past")
    private LocalDate dateOfBirth;

    @Min(value = 0, message = "Amount cannot be negative")
    @Max(value = 1000000, message = "Amount exceeds maximum")
    private BigDecimal amount;

    @NotNull(message = "Fellowship is required")
    private Long fellowshipId;
}
```

### Common Validation Annotations
| Annotation | Use Case |
|------------|----------|
| `@NotNull` | Field must not be null |
| `@NotBlank` | String must not be null/empty/whitespace |
| `@NotEmpty` | Collection/String must not be null/empty |
| `@Size(min, max)` | String/Collection length |
| `@Min` / `@Max` | Numeric range |
| `@Email` | Email format |
| `@Pattern` | Regex pattern |
| `@Past` / `@Future` | Date constraints |
| `@Positive` / `@PositiveOrZero` | Positive numbers |

### Controller Validation
```java
@PostMapping("/members")
public ResponseEntity<MemberResponse> createMember(
        @Valid @RequestBody MemberRequest request) {
    // @Valid triggers validation
    return ResponseEntity.ok(memberService.create(request));
}
```

### Custom Validator
```java
@Target({ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = UniqueEmailValidator.class)
public @interface UniqueEmail {
    String message() default "Email already exists";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}

@Component
public class UniqueEmailValidator implements ConstraintValidator<UniqueEmail, String> {

    @Autowired
    private MemberRepository memberRepository;

    @Override
    public boolean isValid(String email, ConstraintValidatorContext context) {
        if (email == null) return true;  // @NotBlank handles null
        return !memberRepository.existsByEmail(email);
    }
}
```

### Cross-Field Validation
```java
@Target({ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = DateRangeValidator.class)
public @interface ValidDateRange {
    String message() default "End date must be after start date";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}

@ValidDateRange
public class EventRequest {
    private LocalDate startDate;
    private LocalDate endDate;
}
```

### Service-Level Validation
```java
public MemberResponse create(MemberRequest request) {
    // Business logic validation
    if (memberRepository.existsByEmailAndChurchId(request.getEmail(), churchId)) {
        throw new BusinessException("A member with this email already exists");
    }

    Fellowship fellowship = fellowshipRepository.findById(request.getFellowshipId())
        .orElseThrow(() -> new BusinessException("Fellowship not found"));

    // Percentage validation - always cap at 100%
    double rate = total > 0 ? Math.min((count * 100.0 / total), 100.0) : 0.0;

    // ... create member
}
```

## Frontend Validation (Angular)

### Reactive Form Setup
```typescript
export class MemberFormComponent implements OnInit {
  form: FormGroup;
  backendFieldErrors = signal<Record<string, string[]>>({});

  constructor(private fb: FormBuilder) {}

  ngOnInit(): void {
    this.form = this.fb.group({
      firstName: ['', [
        Validators.required,
        Validators.minLength(2),
        Validators.maxLength(100)
      ]],
      lastName: ['', [
        Validators.required,
        Validators.minLength(2),
        Validators.maxLength(100)
      ]],
      email: ['', [
        Validators.required,
        Validators.email
      ]],
      phone: ['', [
        Validators.pattern(/^[0-9]{10}$/)
      ]],
      dateOfBirth: [null, [
        Validators.required,
        this.pastDateValidator
      ]],
      fellowshipId: [null, Validators.required]
    });
  }

  // Custom validator
  pastDateValidator(control: AbstractControl): ValidationErrors | null {
    if (!control.value) return null;
    const date = new Date(control.value);
    return date < new Date() ? null : { futureDate: true };
  }
}
```

### Template with Validation Messages
```html
<form [formGroup]="form" (ngSubmit)="onSubmit()">

  <!-- First Name -->
  <div class="form-field">
    <label for="firstName">
      First Name <span class="required">*</span>
    </label>
    <input
      id="firstName"
      formControlName="firstName"
      pInputText
      [class.ng-invalid]="form.get('firstName')?.invalid && form.get('firstName')?.touched">

    <!-- Frontend validation errors -->
    @if (form.get('firstName')?.touched && form.get('firstName')?.invalid) {
      @if (form.get('firstName')?.errors?.['required']) {
        <div class="error-message">First name is required</div>
      }
      @if (form.get('firstName')?.errors?.['minlength']) {
        <div class="error-message">First name must be at least 2 characters</div>
      }
      @if (form.get('firstName')?.errors?.['maxlength']) {
        <div class="error-message">First name cannot exceed 100 characters</div>
      }
    }

    <!-- Backend validation errors -->
    @for (error of getBackendFieldErrors('firstName'); track error) {
      <div class="error-message backend-error">{{ error }}</div>
    }
  </div>

  <!-- Email -->
  <div class="form-field">
    <label for="email">
      Email <span class="required">*</span>
    </label>
    <input
      id="email"
      formControlName="email"
      pInputText
      type="email">

    @if (form.get('email')?.touched && form.get('email')?.invalid) {
      @if (form.get('email')?.errors?.['required']) {
        <div class="error-message">Email is required</div>
      }
      @if (form.get('email')?.errors?.['email']) {
        <div class="error-message">Please enter a valid email</div>
      }
    }

    @for (error of getBackendFieldErrors('email'); track error) {
      <div class="error-message backend-error">{{ error }}</div>
    }
  </div>

  <!-- Phone (Optional) -->
  <div class="form-field">
    <label for="phone">Phone</label>
    <input
      id="phone"
      formControlName="phone"
      pInputText>

    @if (form.get('phone')?.touched && form.get('phone')?.errors?.['pattern']) {
      <div class="error-message">Phone must be 10 digits</div>
    }

    @for (error of getBackendFieldErrors('phone'); track error) {
      <div class="error-message backend-error">{{ error }}</div>
    }
  </div>

  <!-- Submit -->
  <div class="form-actions">
    <button
      type="submit"
      class="btn-primary"
      [disabled]="form.invalid || isSubmitting()">
      @if (isSubmitting()) {
        <i class="pi pi-spin pi-spinner"></i>
      }
      Save
    </button>
  </div>
</form>
```

### Backend Error Integration
```typescript
// Parse and display backend field errors
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

clearBackendFieldErrors(): void {
  this.backendFieldErrors.set({});
}

// Call on submit
onSubmit(): void {
  this.clearBackendFieldErrors();

  if (this.form.invalid) {
    this.form.markAllAsTouched();
    return;
  }

  this.isSubmitting.set(true);

  this.memberService.save(this.form.value).subscribe({
    next: (result) => {
      this.isSubmitting.set(false);
      this.dialogRef.close(result);
    },
    error: (err) => {
      this.isSubmitting.set(false);
      if (err.status === 400) {
        this.parseAndSetBackendFieldErrors(err);
      }
    }
  });
}

// Clear errors when dialog closes
onDialogHide(): void {
  this.clearBackendFieldErrors();
  this.form.reset();
}
```

## Validation Styling

```css
/* Error message */
.error-message {
  color: #dc2626;
  font-size: 0.75rem;
  margin-top: 0.25rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.error-message::before {
  content: '\e936';
  font-family: 'primeicons';
  font-size: 0.75rem;
}

/* Backend error - distinguished styling */
.error-message.backend-error {
  background: #fef2f2;
  padding: 0.375rem 0.625rem;
  border-radius: 0.375rem;
  border: 1px solid #fee2e2;
  margin-top: 0.375rem;
}

/* Invalid input border */
input.ng-invalid.ng-touched,
textarea.ng-invalid.ng-touched,
p-dropdown.ng-invalid.ng-touched ::ng-deep .p-dropdown {
  border-color: #ef4444 !important;
}

/* Required marker */
.required {
  color: #ef4444;
  margin-left: 0.125rem;
}

/* Form field container */
.form-field {
  margin-bottom: 1.25rem;
}

.form-field label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
}
```

## Security Considerations

### DO NOT rely on frontend validation alone
```java
// Backend MUST validate even if frontend validates
@PostMapping("/members")
public ResponseEntity<MemberResponse> createMember(
        @Valid @RequestBody MemberRequest request) {
    // Validation happens here regardless of frontend
}
```

### Login/Register Forms - Security Exception
```typescript
// DON'T show field-specific errors for auth forms
// This prevents attackers from discovering valid usernames/emails

// ❌ DON'T
if (error.status === 401) {
  this.emailError.set('Email not found');  // Reveals valid emails!
}

// ✅ DO
if (error.status === 401) {
  this.errorMessage.set('Invalid email or password');
}
```

## Best Practices

1. **Validate on both frontend AND backend** - Never trust client input
2. **Show errors immediately** - Don't wait for form submission
3. **Clear backend errors** - When user starts editing field
4. **Preserve input** - Don't clear form on validation errors
5. **Use proper field names** - Backend error keys must match frontend field names
6. **Be specific** - "Email is required" not "Field is required"
7. **Be helpful** - "Password must be 8+ characters" not just "Invalid"
