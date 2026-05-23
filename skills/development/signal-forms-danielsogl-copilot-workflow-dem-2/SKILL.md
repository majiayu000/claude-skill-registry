---
name: signal-forms
description: Use when creating forms with validation in Angular. Triggers on requests involving "form", "validation", "input fields", "form validation", "schema validation", or when building user input forms.
---

# Angular Signal Forms Guide

Create type-safe forms using Angular Signal Forms with built-in schema validation.

**Note:** Signal Forms are experimental in Angular v21+. Use with awareness of potential API changes.

## Core Pattern

```typescript
import { Component, signal, ChangeDetectionStrategy } from "@angular/core";
import {
  form,
  schema,
  Field,
  required,
  email,
  minLength,
} from "@angular/forms/signals";

// 1. Define TypeScript interface
interface User {
  name: string;
  email: string;
}

// 2. Define validation schema
const userSchema = schema<User>((f) => {
  required(f.name, { message: "Name is required" });
  minLength(f.name, 3, { message: "Name must be at least 3 characters" });
  required(f.email, { message: "Email is required" });
  email(f.email, { message: "Enter a valid email address" });
});

// 3. Create component
@Component({
  selector: "app-user-form",
  imports: [Field],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <form (ngSubmit)="onSubmit()">
      <input type="text" placeholder="Name" [field]="userForm.name" />
      @if (userForm.name().touched() || userForm.name().dirty()) {
        @for (error of userForm.name().errors(); track error.kind) {
          <p class="error">{{ error.message }}</p>
        }
      }

      <input type="email" placeholder="Email" [field]="userForm.email" />
      @if (userForm.email().touched() || userForm.email().dirty()) {
        @for (error of userForm.email().errors(); track error.kind) {
          <p class="error">{{ error.message }}</p>
        }
      }

      <button type="submit" [disabled]="!userForm().valid()">Submit</button>
    </form>
  `,
})
export class UserForm {
  // Initialize state signal
  user = signal<User>({ name: "", email: "" });

  // Create form with validation
  userForm = form(this.user, userSchema);

  onSubmit(): void {
    if (this.userForm().valid()) {
      console.log("Valid data:", this.user());
    }
  }
}
```

## Built-in Validators

```typescript
import {
  schema,
  required,
  email,
  minLength,
  maxLength,
  min,
  max,
  pattern,
  validate,
  customError,
  applyEach,
} from "@angular/forms/signals";

const formSchema = schema<FormData>((f) => {
  // Required field
  required(f.name, { message: "Name is required" });

  // Email validation
  email(f.email, { message: "Invalid email format" });

  // String length
  minLength(f.password, 8, {
    message: "Password must be at least 8 characters",
  });
  maxLength(f.bio, 500, { message: "Bio cannot exceed 500 characters" });

  // Number range
  min(f.age, 18, { message: "Must be at least 18" });
  max(f.quantity, 100, { message: "Maximum 100 items" });

  // Regex pattern
  pattern(f.phone, /^\+?[1-9]\d{1,14}$/, { message: "Invalid phone number" });
  pattern(f.zip, /^\d{5}$/, { message: "ZIP must be 5 digits" });
});
```

## Custom Validation

```typescript
const formSchema = schema<User>((f) => {
  required(f.username);

  // Custom validation logic
  validate(f.username, (field) => {
    const value = field.value();
    if (value && !/^[a-zA-Z]/.test(value)) {
      return customError({
        kind: "pattern",
        message: "Username must start with a letter",
      });
    }
    return null;
  });

  // Password strength validation
  validate(f.password, (field) => {
    const value = field.value();
    if (!value) return null;

    if (value.length < 8) {
      return customError({
        kind: "minLength",
        message: "At least 8 characters",
      });
    }
    if (!/[A-Z]/.test(value)) {
      return customError({
        kind: "pattern",
        message: "Include an uppercase letter",
      });
    }
    if (!/[0-9]/.test(value)) {
      return customError({ kind: "pattern", message: "Include a number" });
    }
    return null;
  });
});
```

## Password Confirmation

```typescript
interface SignupForm {
  password: string;
  confirmPassword: string;
}

const signupSchema = schema<SignupForm>((f) => {
  required(f.password, { message: "Password is required" });
  minLength(f.password, 8, { message: "At least 8 characters" });
  required(f.confirmPassword, { message: "Please confirm password" });

  // Cross-field validation
  validate(f.confirmPassword, (field) => {
    const password = f.password.value();
    const confirm = field.value();

    if (confirm && password !== confirm) {
      return customError({
        kind: "passwordMismatch",
        message: "Passwords do not match",
      });
    }
    return null;
  });
});
```

## Nested Objects

```typescript
interface Address {
  street: string;
  city: string;
  zip: string;
}

interface User {
  name: string;
  address: Address;
}

const userSchema = schema<User>((f) => {
  required(f.name, { message: "Name is required" });

  // Nested validation
  required(f.address.street, { message: "Street is required" });
  required(f.address.city, { message: "City is required" });
  required(f.address.zip, { message: "ZIP is required" });
  pattern(f.address.zip, /^\d{5}$/, { message: "ZIP must be 5 digits" });
});

// Template
`
<input [field]="userForm.name" placeholder="Name" />
<input [field]="userForm.address.street" placeholder="Street" />
<input [field]="userForm.address.city" placeholder="City" />
<input [field]="userForm.address.zip" placeholder="ZIP" />
`;
```

## Dynamic Arrays

```typescript
interface Hobby {
  name: string;
  years: number;
}

interface User {
  name: string;
  hobbies: Hobby[];
}

const userSchema = schema<User>((f) => {
  required(f.name);

  // Validate each array item
  applyEach(f.hobbies, (hobby) => {
    required(hobby.name, { message: "Hobby name is required" });
    min(hobby.years, 0, { message: "Years must be positive" });
  });
});

@Component({
  template: `
    @for (hobby of userForm.hobbies; track hobby; let i = $index) {
      <div class="hobby-row">
        <input [field]="hobby.name" placeholder="Hobby" />
        <input [field]="hobby.years" type="number" placeholder="Years" />
        <button type="button" (click)="removeHobby(i)">Remove</button>
      </div>
    } @empty {
      <p>No hobbies added</p>
    }
    <button type="button" (click)="addHobby()">Add Hobby</button>
  `,
})
export class HobbyForm {
  user = signal<User>({ name: "", hobbies: [] });
  userForm = form(this.user, userSchema);

  addHobby(): void {
    this.user.update((u) => ({
      ...u,
      hobbies: [...u.hobbies, { name: "", years: 0 }],
    }));
  }

  removeHobby(index: number): void {
    this.user.update((u) => ({
      ...u,
      hobbies: u.hobbies.filter((_, i) => i !== index),
    }));
  }
}
```

## Field State Properties

```typescript
// Access field state
const field = userForm.name();

field.value(); // Current value (may be debounced)
field.controlValue(); // Non-debounced value
field.valid(); // Is valid
field.invalid(); // Is invalid
field.errors(); // Array of { kind, message }
field.touched(); // User has blurred
field.dirty(); // Value has changed
field.pending(); // Async validation in progress
field.disabled(); // Is disabled
field.hidden(); // Is hidden
field.readonly(); // Is read-only

// Methods
field.reset(); // Mark pristine and untouched
field.markAsTouched(); // Mark as touched
field.markAsDirty(); // Mark as dirty
```

## Form State with Computed Signals

```typescript
@Component({
  template: `
    <form (ngSubmit)="onSubmit()">
      <!-- fields -->
      <button type="submit" [disabled]="!canSubmit()">Submit</button>
      <p>Form valid: {{ isValid() }}</p>
      <p>Has changes: {{ isDirty() }}</p>
    </form>
  `,
})
export class Form {
  user = signal<User>({ name: "", email: "" });
  userForm = form(this.user, userSchema);

  readonly isValid = computed(() => this.userForm().valid());
  readonly isDirty = computed(
    () => this.userForm.name().dirty() || this.userForm.email().dirty(),
  );
  readonly canSubmit = computed(() => this.isValid() && this.isDirty());
}
```

## With Material Form Fields

```typescript
@Component({
  imports: [Field, MatFormFieldModule, MatInputModule],
  template: `
    <mat-form-field appearance="outline">
      <mat-label>Email</mat-label>
      <input matInput [field]="userForm.email" type="email" />
      @if (userForm.email().touched()) {
        @for (error of userForm.email().errors(); track error.kind) {
          <mat-error>{{ error.message }}</mat-error>
        }
      }
    </mat-form-field>
  `,
})
```

## Schema Organization

```typescript
// src/app/domain/data/models/user.validation.ts

import {
  schema,
  required,
  email,
  min,
  max,
  pattern,
} from "@angular/forms/signals";

export interface User {
  name: string;
  email: string;
  age: number;
}

// Export reusable schema
export const userValidation = schema<User>((f) => {
  required(f.name, { message: "Name is required" });
  required(f.email, { message: "Email is required" });
  email(f.email, { message: "Invalid email" });
  min(f.age, 18, { message: "Must be 18 or older" });
  max(f.age, 120, { message: "Invalid age" });
});

// Usage in component
import { userValidation } from "../data/models/user.validation";

userForm = form(this.user, userValidation);
```

## Checklist

- [ ] Define TypeScript interface for form data
- [ ] Create schema with validation rules
- [ ] Use `signal()` for form state
- [ ] Use `form()` to create reactive form
- [ ] Import `Field` directive for bindings
- [ ] Show errors only when `touched()` or `dirty()`
- [ ] Track errors by `error.kind`
- [ ] Use `userForm().valid()` for submit button
- [ ] Use OnPush change detection
