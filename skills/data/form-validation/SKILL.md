---
name: form-validation
description: Implement form validation using React Hook Form, Formik, Vee-Validate, and custom validators. Use when building robust form handling with real-time validation.
---

# Form Validation

## Overview

Implement comprehensive form validation including client-side validation, server-side synchronization, and real-time error feedback with TypeScript type safety.

## When to Use

- User input validation
- Form submission handling
- Real-time error feedback
- Complex validation rules
- Multi-step forms

## Implementation Examples

### 1. **React Hook Form with TypeScript**

```typescript
// types/form.ts
export interface LoginFormData {
  email: string;
  password: string;
  rememberMe: boolean;
}

export interface RegisterFormData {
  email: string;
  password: string;
  confirmPassword: string;
  name: string;
  terms: boolean;
}

// components/LoginForm.tsx
import { useForm, SubmitHandler } from 'react-hook-form';
import { LoginFormData } from '../types/form';

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export const LoginForm: React.FC = () => {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    watch
  } = useForm<LoginFormData>({
    defaultValues: {
      email: '',
      password: '',
      rememberMe: false
    }
  });

  const onSubmit: SubmitHandler<LoginFormData> = async (data) => {
    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        body: JSON.stringify(data)
      });
      if (!response.ok) throw new Error('Login failed');
      // Handle success
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label>Email</label>
        <input
          type="email"
          {...register('email', {
            required: 'Email is required',
            pattern: {
              value: emailRegex,
              message: 'Invalid email format'
            }
          })}
        />
        {errors.email && <span className="error">{errors.email.message}</span>}
      </div>

      <div>
        <label>Password</label>
        <input
          type="password"
          {...register('password', {
            required: 'Password is required',
            minLength: {
              value: 8,
              message: 'Password must be at least 8 characters'
            }
          })}
        />
        {errors.password && <span className="error">{errors.password.message}</span>}
      </div>

      <div>
        <label>
          <input type="checkbox" {...register('rememberMe')} />
          Remember me
        </label>
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
};

// Custom validator
const usePasswordStrength = () => {
  return (password: string): boolean | string => {
    if (password.length < 8) return 'At least 8 characters';
    if (!/[A-Z]/.test(password)) return 'At least one uppercase letter';
    if (!/[0-9]/.test(password)) return 'At least one number';
    return true;
  };
};
```

### 2. **Formik with Yup Validation**

```typescript
// validationSchema.ts
import * as Yup from 'yup';

export const registerValidationSchema = Yup.object().shape({
  email: Yup.string()
    .email('Invalid email')
    .required('Email is required'),
  password: Yup.string()
    .min(8, 'Password must be at least 8 characters')
    .matches(/[A-Z]/, 'Must contain uppercase letter')
    .matches(/[0-9]/, 'Must contain number')
    .required('Password is required'),
  confirmPassword: Yup.string()
    .oneOf([Yup.ref('password')], 'Passwords must match')
    .required('Confirm password is required'),
  name: Yup.string()
    .min(2, 'Name too short')
    .required('Name is required'),
  terms: Yup.boolean()
    .oneOf([true], 'You must accept terms')
    .required()
});

// components/RegisterForm.tsx
import { Formik, Form, Field, ErrorMessage } from 'formik';
import { registerValidationSchema } from '../validationSchema';
import { RegisterFormData } from '../types/form';

export const RegisterForm: React.FC = () => {
  const initialValues: RegisterFormData = {
    email: '',
    password: '',
    confirmPassword: '',
    name: '',
    terms: false
  };

  const handleSubmit = async (
    values: RegisterFormData,
    { setSubmitting, setFieldError }: any
  ) => {
    try {
      const response = await fetch('/api/register', {
        method: 'POST',
        body: JSON.stringify(values)
      });

      if (!response.ok) {
        const error = await response.json();
        if (error.emailExists) {
          setFieldError('email', 'Email already registered');
        }
        throw new Error(error.message);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Formik
      initialValues={initialValues}
      validationSchema={registerValidationSchema}
      onSubmit={handleSubmit}
    >
      {({ isSubmitting, isValid }) => (
        <Form>
          <div>
            <label htmlFor="name">Name</label>
            <Field name="name" type="text" />
            <ErrorMessage name="name" component="span" className="error" />
          </div>

          <div>
            <label htmlFor="email">Email</label>
            <Field name="email" type="email" />
            <ErrorMessage name="email" component="span" className="error" />
          </div>

          <div>
            <label htmlFor="password">Password</label>
            <Field name="password" type="password" />
            <ErrorMessage name="password" component="span" className="error" />
          </div>

          <div>
            <label htmlFor="confirmPassword">Confirm Password</label>
            <Field name="confirmPassword" type="password" />
            <ErrorMessage name="confirmPassword" component="span" className="error" />
          </div>

          <div>
            <label>
              <Field name="terms" type="checkbox" />
              I agree to terms
            </label>
            <ErrorMessage name="terms" component="span" className="error" />
          </div>

          <button type="submit" disabled={isSubmitting || !isValid}>
            {isSubmitting ? 'Registering...' : 'Register'}
          </button>
        </Form>
      )}
    </Formik>
  );
};
```

### 3. **Vue Vee-Validate**

```typescript
// validationRules.ts
import { defineRule } from 'vee-validate';
import { email, required, min, confirmed } from '@vee-validate/rules';

defineRule('required', required);
defineRule('email', email);
defineRule('min', min);
defineRule('confirmed', confirmed);
defineRule('password-strength', (value: string) => {
  if (value.length < 8) return 'Password must be at least 8 characters';
  if (!/[A-Z]/.test(value)) return 'Must contain uppercase letter';
  if (!/[0-9]/.test(value)) return 'Must contain number';
  return true;
});

// components/LoginForm.vue
<template>
  <Form @submit="onSubmit" :validation-schema="validationSchema">
    <div class="form-group">
      <label for="email">Email</label>
      <Field name="email" type="email" as="input" class="form-control" />
      <ErrorMessage name="email" class="error" />
    </div>

    <div class="form-group">
      <label for="password">Password</label>
      <Field name="password" type="password" as="input" class="form-control" />
      <ErrorMessage name="password" class="error" />
    </div>

    <button type="submit" :disabled="isSubmitting">
      {{ isSubmitting ? 'Logging in...' : 'Login' }}
    </button>
  </Form>
</template>

<script setup lang="ts">
import { Form, Field, ErrorMessage } from 'vee-validate';
import { object, string } from 'yup';
import { ref } from 'vue';

const isSubmitting = ref(false);

const validationSchema = object({
  email: string().email('Invalid email').required('Email is required'),
  password: string().required('Password is required')
});

const onSubmit = async (values: any) => {
  isSubmitting.value = true;
  try {
    const response = await fetch('/api/login', {
      method: 'POST',
      body: JSON.stringify(values)
    });
    if (!response.ok) throw new Error('Login failed');
  } catch (error) {
    console.error(error);
  } finally {
    isSubmitting.value = false;
  }
};
</script>
```

### 4. **Custom Validator Hook**

```typescript
// hooks/useFieldValidator.ts
import { useState, useCallback } from 'react';

export interface ValidationRule {
  validate: (value: any) => boolean | string;
  message: string;
}

export interface FieldError {
  isValid: boolean;
  message: string | null;
}

export const useFieldValidator = (rules: ValidationRule[] = []) => {
  const [error, setError] = useState<FieldError>({
    isValid: true,
    message: null
  });

  const validate = useCallback((value: any) => {
    for (const rule of rules) {
      const result = rule.validate(value);
      if (result !== true) {
        setError({
          isValid: false,
          message: typeof result === 'string' ? result : rule.message
        });
        return false;
      }
    }

    setError({
      isValid: true,
      message: null
    });
    return true;
  }, [rules]);

  const clearError = useCallback(() => {
    setError({
      isValid: true,
      message: null
    });
  }, []);

  return { error, validate, clearError };
};

// Usage
const { error: emailError, validate: validateEmail } = useFieldValidator([
  {
    validate: (v) => v.length > 0,
    message: 'Email is required'
  },
  {
    validate: (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v),
    message: 'Invalid email format'
  }
]);
```

### 5. **Server-Side Validation Integration**

```typescript
// Async server validation
const useAsyncValidation = () => {
  const validateEmail = async (email: string) => {
    const response = await fetch(`/api/validate/email?email=${email}`);
    const { available } = await response.json();
    return available ? true : 'Email already registered';
  };

  const validateUsername = async (username: string) => {
    const response = await fetch(`/api/validate/username?username=${username}`);
    const { available } = await response.json();
    return available ? true : 'Username taken';
  };

  return { validateEmail, validateUsername };
};

// React Hook Form with async validation
const { validateEmail } = useAsyncValidation();

register('email', {
  required: 'Email required',
  validate: async (value) => {
    return await validateEmail(value);
  }
});
```

## Best Practices

- Validate on both client and server
- Provide real-time feedback
- Use TypeScript for type safety
- Implement custom validators for complex rules
- Handle async validation properly
- Show clear error messages
- Preserve user input on validation failure
- Test validation rules thoroughly
- Use schema validation (Yup, Zod)

## Resources

- [React Hook Form](https://react-hook-form.com/)
- [Formik Documentation](https://formik.org/)
- [Vee-Validate](https://vee-validate.logaretm.com/)
- [Yup Validation](https://github.com/jquense/yup)
- [Zod Schema Validation](https://zod.dev/)
