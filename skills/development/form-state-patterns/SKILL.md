---
name: form-state-patterns
description: React Hook Form v7 with Zod validation, React 19 useActionState, Server Actions, field arrays, and async validation. Use when building complex forms, validation flows, or server action forms.
tags: [react-hook-form, zod, forms, validation, server-actions, field-arrays, useActionState]
context: fork
agent: frontend-ui-developer
version: 1.0.0
allowed-tools: [Read, Write, Grep, Glob]
author: SkillForge
user-invocable: false
---

# Form State Patterns

Production form patterns with React Hook Form v7 + Zod - type-safe, performant, accessible.

## Overview

- Complex forms with validation
- Multi-step wizards
- Dynamic field arrays
- Server-side validation
- Async field validation
- Forms with file uploads

## Core Patterns

### 1. Basic Form with Zod Schema

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const userSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Min 8 characters'),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
});

type UserForm = z.infer<typeof userSchema>;

function SignupForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<UserForm>({
    resolver: zodResolver(userSchema),
    defaultValues: { email: '', password: '', confirmPassword: '' },
  });

  const onSubmit = async (data: UserForm) => {
    await api.signup(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} aria-invalid={!!errors.email} />
      {errors.email && <span role="alert">{errors.email.message}</span>}

      <input type="password" {...register('password')} />
      {errors.password && <span role="alert">{errors.password.message}</span>}

      <input type="password" {...register('confirmPassword')} />
      {errors.confirmPassword && <span role="alert">{errors.confirmPassword.message}</span>}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Submitting...' : 'Sign Up'}
      </button>
    </form>
  );
}
```

### 2. Field Arrays (Dynamic Fields)

```typescript
import { useFieldArray, useForm } from 'react-hook-form';

const orderSchema = z.object({
  items: z.array(z.object({
    productId: z.string().min(1),
    quantity: z.number().min(1).max(100),
  })).min(1, 'At least one item required'),
});

function OrderForm() {
  const { control, register, handleSubmit } = useForm({
    resolver: zodResolver(orderSchema),
    defaultValues: { items: [{ productId: '', quantity: 1 }] },
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'items',
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {fields.map((field, index) => (
        <div key={field.id}>
          <input {...register(`items.${index}.productId`)} />
          <input
            type="number"
            {...register(`items.${index}.quantity`, { valueAsNumber: true })}
          />
          <button type="button" onClick={() => remove(index)}>Remove</button>
        </div>
      ))}
      <button type="button" onClick={() => append({ productId: '', quantity: 1 })}>
        Add Item
      </button>
      <button type="submit">Submit Order</button>
    </form>
  );
}
```

### 3. Async Field Validation

```typescript
const usernameSchema = z.object({
  username: z.string()
    .min(3)
    .refine(async (value) => {
      const available = await checkUsernameAvailability(value);
      return available;
    }, 'Username already taken'),
});

// Or with mode: 'onBlur' for better UX
const { register } = useForm({
  resolver: zodResolver(usernameSchema),
  mode: 'onBlur', // Validate on blur, not on every keystroke
});
```

### 4. Server Actions (React 19 / Next.js)

```typescript
// actions.ts
'use server';
import { z } from 'zod';

const contactSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
  message: z.string().min(10),
});

export async function submitContact(formData: FormData) {
  const result = contactSchema.safeParse({
    name: formData.get('name'),
    email: formData.get('email'),
    message: formData.get('message'),
  });

  if (!result.success) {
    return { errors: result.error.flatten().fieldErrors };
  }

  await saveContact(result.data);
  return { success: true };
}

// Component
'use client';
import { useActionState } from 'react';
import { submitContact } from './actions';

function ContactForm() {
  const [state, formAction, isPending] = useActionState(submitContact, null);

  return (
    <form action={formAction}>
      <input name="name" />
      {state?.errors?.name && <span>{state.errors.name[0]}</span>}

      <input name="email" />
      {state?.errors?.email && <span>{state.errors.email[0]}</span>}

      <textarea name="message" />
      {state?.errors?.message && <span>{state.errors.message[0]}</span>}

      <button type="submit" disabled={isPending}>
        {isPending ? 'Sending...' : 'Send'}
      </button>
    </form>
  );
}
```

### 5. Multi-Step Wizard

```typescript
const steps = ['personal', 'address', 'payment'] as const;

const wizardSchema = z.object({
  personal: z.object({
    firstName: z.string().min(1),
    lastName: z.string().min(1),
  }),
  address: z.object({
    street: z.string().min(1),
    city: z.string().min(1),
  }),
  payment: z.object({
    cardNumber: z.string().length(16),
  }),
});

function WizardForm() {
  const [step, setStep] = useState(0);
  const methods = useForm({
    resolver: zodResolver(wizardSchema),
    mode: 'onTouched',
  });

  const nextStep = async () => {
    const stepKey = steps[step];
    const isValid = await methods.trigger(stepKey);
    if (isValid) setStep((s) => Math.min(s + 1, steps.length - 1));
  };

  return (
    <FormProvider {...methods}>
      <form onSubmit={methods.handleSubmit(onSubmit)}>
        {step === 0 && <PersonalStep />}
        {step === 1 && <AddressStep />}
        {step === 2 && <PaymentStep />}

        <div>
          {step > 0 && <button type="button" onClick={() => setStep(s => s - 1)}>Back</button>}
          {step < steps.length - 1 && <button type="button" onClick={nextStep}>Next</button>}
          {step === steps.length - 1 && <button type="submit">Submit</button>}
        </div>
      </form>
    </FormProvider>
  );
}
```

### 6. File Upload with Preview

```typescript
const fileSchema = z.object({
  avatar: z
    .instanceof(FileList)
    .refine((files) => files.length === 1, 'File required')
    .refine((files) => files[0]?.size <= 5_000_000, 'Max 5MB')
    .refine(
      (files) => ['image/jpeg', 'image/png'].includes(files[0]?.type),
      'Only JPEG/PNG'
    ),
});

function AvatarUpload() {
  const [preview, setPreview] = useState<string | null>(null);
  const { register, watch } = useForm({ resolver: zodResolver(fileSchema) });

  const avatar = watch('avatar');
  useEffect(() => {
    if (avatar?.[0]) {
      setPreview(URL.createObjectURL(avatar[0]));
    }
  }, [avatar]);

  return (
    <>
      {preview && <img src={preview} alt="Preview" />}
      <input type="file" accept="image/*" {...register('avatar')} />
    </>
  );
}
```

### 7. Controlled Components Integration

```typescript
import { Controller } from 'react-hook-form';
import { DatePicker } from '@/components/ui/date-picker';

function EventForm() {
  const { control } = useForm();

  return (
    <Controller
      name="eventDate"
      control={control}
      render={({ field, fieldState }) => (
        <DatePicker
          value={field.value}
          onChange={field.onChange}
          onBlur={field.onBlur}
          error={fieldState.error?.message}
        />
      )}
    />
  );
}
```

## Performance Optimizations

```typescript
// Isolate re-renders with Controller
<Controller name="email" control={control} render={...} />

// Use mode: 'onBlur' instead of 'onChange'
useForm({ mode: 'onBlur' });

// Avoid watching entire form
const email = watch('email'); // Good: specific field
const form = watch(); // Bad: entire form triggers re-render
```

## Accessibility Checklist

- [ ] All inputs have associated labels
- [ ] Error messages use `role="alert"`
- [ ] Invalid inputs have `aria-invalid="true"`
- [ ] Submit button shows loading state
- [ ] Focus management on error

## Quick Reference

```typescript
// ✅ Basic form setup with Zod resolver
const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<FormData>({
  resolver: zodResolver(schema),
  defaultValues: { name: '', email: '' },
  mode: 'onBlur', // Validate on blur, not every keystroke
});

// ✅ Register inputs with accessibility
<input
  {...register('email')}
  aria-invalid={!!errors.email}
  aria-describedby={errors.email ? 'email-error' : undefined}
/>
{errors.email && <p id="email-error" role="alert">{errors.email.message}</p>}

// ✅ Controller for third-party components
<Controller
  name="date"
  control={control}
  render={({ field, fieldState }) => (
    <DatePicker value={field.value} onChange={field.onChange} error={fieldState.error} />
  )}
/>

// ✅ useActionState for React 19 Server Actions
const [state, formAction, isPending] = useActionState(serverAction, initialState);

// ❌ NEVER watch entire form (causes full re-render)
const allValues = watch(); // BAD

// ❌ NEVER use index as key in field arrays
fields.map((field, index) => <div key={index}>...</div>) // BAD - use field.id
```

## Key Decisions

| Decision | Option A | Option B | Recommendation |
|----------|----------|----------|----------------|
| Validation library | Yup | Zod | **Zod** - better TypeScript inference, smaller bundle |
| Validation mode | onChange | onBlur | **onBlur** - better performance, less noise |
| Complex components | register | Controller | **Controller** - for non-native inputs |
| Server validation | Client-only | Server Actions | **Server Actions** - for mutations with React 19 |
| Form state lib | Formik | React Hook Form | **RHF** - better performance, less re-renders |
| Field arrays | Manual state | useFieldArray | **useFieldArray** - built-in add/remove/swap |

## Anti-Patterns (FORBIDDEN)

```typescript
// ❌ FORBIDDEN: Watching entire form
const form = watch();  // Re-renders on EVERY change to ANY field

// ❌ FORBIDDEN: Using index as key in field arrays
{fields.map((field, index) => (
  <div key={index}>  // WRONG - will cause bugs on reorder/remove
    <input {...register(`items.${index}.name`)} />
  </div>
))}
// ✅ CORRECT: Use field.id
{fields.map((field, index) => (
  <div key={field.id}>
    <input {...register(`items.${index}.name`)} />
  </div>
))}

// ❌ FORBIDDEN: Missing defaultValues for all fields
useForm({
  resolver: zodResolver(schema),
  // Missing defaultValues causes uncontrolled->controlled warning
});

// ❌ FORBIDDEN: Using native validation with Zod
<input type="email" required {...register('email')} /> // Conflicts with Zod
// ✅ CORRECT: Disable native validation
<form onSubmit={handleSubmit(onSubmit)} noValidate>

// ❌ FORBIDDEN: setError without manual clearErrors
const onSubmit = async (data) => {
  const result = await api.submit(data);
  if (!result.success) {
    setError('email', { message: 'Email taken' });
    // Missing clearErrors on next submit!
  }
};

// ❌ FORBIDDEN: Async validation on every keystroke
const schema = z.object({
  username: z.string().refine(async (val) => {
    return await checkAvailable(val);  // Fires on every character!
  }),
});
// ✅ CORRECT: Use mode: 'onBlur' or debounce
useForm({ mode: 'onBlur' });

// ❌ FORBIDDEN: Missing error messages in Zod
const schema = z.object({
  email: z.string().email(),  // Generic "Invalid" error
});
// ✅ CORRECT: Custom error messages
const schema = z.object({
  email: z.string().email('Please enter a valid email address'),
});
```

## Related Skills

- `tanstack-query-advanced` - Combine form mutations with TanStack Query
- `zustand-patterns` - Form wizard state with multi-step persistence
- `input-validation` - Server-side validation and sanitization
- `accessibility-specialist` - WCAG compliance for forms

## Capability Details

### zod-validation
**Keywords**: zod, schema, validation, refine, transform, parse
**Solves**: Type-safe validation with automatic TypeScript inference

### field-arrays
**Keywords**: useFieldArray, dynamic, add, remove, append, swap, move
**Solves**: Dynamic forms with add/remove items like invoices, surveys

### server-actions
**Keywords**: useActionState, Server Actions, 'use server', formData
**Solves**: React 19 progressive enhancement with server-side validation

### multi-step-wizard
**Keywords**: wizard, steps, trigger, FormProvider, partial validation
**Solves**: Complex multi-page forms with step-by-step validation

### async-validation
**Keywords**: async, refine, debounce, username, availability
**Solves**: Server-side validation during input (e.g., username availability)

### file-upload
**Keywords**: FileList, File, upload, preview, drag-drop, validation
**Solves**: File input validation with size, type, and preview handling

## References

- `references/validation-patterns.md` - Advanced Zod patterns
- `templates/form-template.tsx` - Production form template
- `checklists/form-checklist.md` - Implementation checklist
- `examples/form-examples.md` - Real-world form examples
