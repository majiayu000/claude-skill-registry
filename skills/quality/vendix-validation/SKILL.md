---
name: vendix-validation
description: Validation logic patterns.
metadata:
  scope: [root]
  auto_invoke: "Writing Validation Logic"
---
# Vendix Validation Pattern

> **Early Return Pattern** - Validación con retorno temprano para código limpio y legible.

## 🎯 Early Return Principle

**SIEMPRE usar early return para validaciones:**
- Retorna temprano si hay errores
- Reduce anidación de código
- Hace el código más legible
- Separa validación de lógica de negocio

---

## ✅ Backend Validation Pattern

### Service Layer Validation

```typescript
async createUser(create_user_dto: CreateUserDto, client_info: any) {
  // Early return for validation
  if (!create_user_dto.email) {
    throw new BadRequestException('Email is required');
  }

  if (!create_user_dto.email.includes('@')) {
    throw new BadRequestException('Invalid email format');
  }

  if (!create_user_dto.password || create_user_dto.password.length < 8) {
    throw new BadRequestException('Password must be at least 8 characters');
  }

  // Check if user exists
  const existing_user = await this.prisma.users.findUnique({
    where: { email: create_user_dto.email },
  });

  if (existing_user) {
    throw new ConflictException('User already exists');
  }

  // All validations passed - proceed with business logic
  try {
    const hashed_password = await bcrypt.hash(create_user_dto.password, 10);

    const user = await this.prisma.users.create({
      data: {
        ...create_user_dto,
        password: hashed_password,
        organization_id: this.context.organization_id,
      },
      select: {
        id: true,
        email: true,
        user_name: true,
        is_active: true,
      },
    });

    return this.response_service.success(user, 'User created successfully');

  } catch (error) {
    // Handle unexpected errors
    if (error.code === 'P2002') {
      throw new ConflictException('Email already exists');
    }

    throw new InternalServerErrorException('Error creating user');
  }
}
```

---

## 🎯 Validation Pattern Structure

### Standard Validation Flow

```typescript
async methodName(dto: DtoType) {
  // 1. Validate required fields
  if (!dto.required_field) {
    throw new BadRequestException('Field is required');
  }

  // 2. Validate format
  if (!this.isValidFormat(dto.field)) {
    throw new BadRequestException('Invalid format');
  }

  // 3. Check business rules
  if (!await this.meetsBusinessRule(dto.field)) {
    throw new BadRequestException('Business rule violation');
  }

  // 4. Check permissions
  if (!this.hasPermission()) {
    throw new ForbiddenException('Insufficient permissions');
  }

  // 5. Check existence
  const existing = await this.prisma.model.findUnique({
    where: { id: dto.id },
  });

  if (!existing) {
    throw new NotFoundException('Resource not found');
  }

  // All validations passed - execute business logic
  try {
    const result = await this.executeBusinessLogic(dto);
    return this.response_service.success(result);
  } catch (error) {
    // Handle errors
    throw new InternalServerErrorException('Operation failed');
  }
}
```

---

## 🔍 Validation Helpers

### Common Validation Methods

```typescript
// In a shared validation utility
export class ValidationHelper {
  static isValidEmail(email: string): boolean {
    const email_regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return email_regex.test(email);
  }

  static isValidPhone(phone: string): boolean {
    const phone_regex = /^\+?[\d\s-]+$/;
    return phone_regex.test(phone);
  }

  static isValidUrl(url: string): boolean {
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  }

  static isStrongPassword(password: string): boolean {
    // At least 8 characters, 1 uppercase, 1 lowercase, 1 number
    const password_regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
    return password_regex.test(password);
  }

  static isPositiveNumber(value: number): boolean {
    return value > 0;
  }

  static isFutureDate(date: Date): boolean {
    return date > new Date();
  }
}
```

---

## 🎨 DTO Validation with class-validator

### Create DTO

```typescript
import {
  IsString,
  IsEmail,
  MinLength,
  IsOptional,
  IsBoolean,
  IsNumber,
  Min,
  Max,
  IsEnum,
  IsDate,
  IsNotEmpty,
} from 'class-validator';

export class CreateUserDto {
  @IsString()
  @IsNotEmpty()
  @MinLength(3)
  user_name: string;

  @IsEmail()
  @IsNotEmpty()
  email: string;

  @IsString()
  @IsNotEmpty()
  @MinLength(8)
  password: string;

  @IsOptional()
  @IsString()
  phone_number?: string;

  @IsOptional()
  @IsBoolean()
  is_active?: boolean = true;
}

export class CreateProductDto {
  @IsString()
  @IsNotEmpty()
  name: string;

  @IsString()
  @IsNotEmpty()
  description: string;

  @IsNumber()
  @Min(0)
  base_price: number;

  @IsEnum(['active', 'inactive', 'draft'])
  status: 'active' | 'inactive' | 'draft';

  @IsDate()
  @IsOptional()
  available_from?: Date;
}
```

### Update DTO (Partial)

```typescript
import { PartialType } from '@nestjs/mapped-types';
import { CreateUserDto } from './create-user.dto';

export class UpdateUserDto extends PartialType(CreateUserDto) {}
```

---

## 🚫 Frontend Validation Pattern

### Reactive Forms Validation

```typescript
import { Component, inject } from '@angular/core';
import { FormBuilder, Validators, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-user-form',
  standalone: true,
  imports: [ReactiveFormsModule],
})
export class UserFormComponent {
  private fb = inject(FormBuilder);

  userForm = this.fb.group({
    user_name: [
      '',
      [
        Validators.required,
        Validators.minLength(3),
        Validators.maxLength(50),
      ],
    ],
    email: [
      '',
      [
        Validators.required,
        Validators.email,
      ],
    ],
    phone_number: [
      '',
      [
        Validators.pattern(/^[+]?[\d\s-]+$/),
      ],
    ],
    password: [
      '',
      [
        Validators.required,
        Validators.minLength(8),
        Validators.pattern(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/),
      ],
    ],
    is_active: [true],
  });

  onSubmit() {
    if (this.userForm.invalid) {
      // Mark all fields as touched to show validation errors
      Object.keys(this.userForm.controls).forEach(key => {
        this.userForm.get(key)?.markAsTouched();
      });
      return;  // Early return
    }

    // Form is valid - proceed
    const form_data = this.userForm.value;
    this.userService.createUser(form_data).subscribe();
  }

  // Validation getters for template
  get user_name() {
    return this.userForm.get('user_name');
  }

  get email() {
    return this.userForm.get('email');
  }
}
```

### Template with Validation Messages

```html
<form [formGroup]="userForm" (ngSubmit)="onSubmit()">
  <div [class.error]="user_name.invalid && user_name.touched">
    <label>User Name</label>
    <input formControlName="user_name" />
    @if (user_name.invalid && user_name.touched) {
      @if (user_name.errors?.['required']) {
        <small>User name is required</small>
      }
      @if (user_name.errors?.['minlength']) {
        <small>Must be at least 3 characters</small>
      }
    }
  </div>

  <div [class.error]="email.invalid && email.touched">
    <label>Email</label>
    <input formControlName="email" type="email" />
    @if (email.invalid && email.touched) {
      @if (email.errors?.['required']) {
        <small>Email is required</small>
      }
      @if (email.errors?.['email']) {
        <small>Invalid email format</small>
      }
    }
  </div>

  <button [disabled]="userForm.invalid">Submit</button>
</form>
```

---

## 🎯 Custom Validators

### Async Validator

```typescript
import { AbstractControl, ValidationErrors, AsyncValidator } from '@angular/core';
import { Observable, of } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { UserService } from '@/app/services/user.service';

export class UniqueEmailValidator implements AsyncValidator {
  constructor(private user_service: UserService) {}

  validate(
    control: AbstractControl,
  ): Observable<ValidationErrors | null> {
    return this.user_service.checkEmailExists(control.value).pipe(
      map(exists => (exists ? { emailExists: true } : null)),
      catchError(() => of(null)),
    );
  }
}

// Usage in component
this.form = this.fb.group({
  email: [
    '',
    {
      validators: [Validators.required, Validators.email],
      asyncValidators: [new UniqueEmailValidator(this.user_service).validate],
    },
  ],
});
```

---

## 🔍 Key Files Reference

| File | Purpose |
|------|---------|
| Backend DTOs | `*/dto/*.dto.ts` |
| Frontend Forms | Component `.ts` files |
| Validation Utils | `common/utils/validation.helper.ts` |

---

## Related Skills

- `vendix-backend-api` - API response patterns
- `vendix-frontend-module` - Form handling in modules
- `vendix-naming-conventions` - Naming conventions (CRITICAL)
