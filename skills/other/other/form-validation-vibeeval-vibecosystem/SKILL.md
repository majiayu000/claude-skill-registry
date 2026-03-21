---
name: form-validation
description: React Hook Form + Zod integration, multi-step forms, optimistic validation, server-side error mapping, and file upload patterns.
---

# Form Validation

React Hook Form + Zod patterns for robust, accessible forms.

## React Hook Form + Zod Setup

```typescript
// Install: npm install react-hook-form zod @hookform/resolvers

import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

// 1. Define schema
const TaskSchema = z.object({
  title:       z.string().min(1, 'Title is required').max(200),
  description: z.string().max(2000).optional(),
  priority:    z.enum(['low', 'medium', 'high']),
  dueDate:     z.string().date('Invalid date').optional(),
})

type TaskFormData = z.infer<typeof TaskSchema>

// 2. Use in component
export function TaskForm({ onSubmit }: { onSubmit: (data: TaskFormData) => Promise<void> }) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting, isDirty },
    setError,
    reset,
  } = useForm<TaskFormData>({
    resolver: zodResolver(TaskSchema),
    defaultValues: { priority: 'medium' },
  })

  const submit = handleSubmit(async (data) => {
    try {
      await onSubmit(data)
      reset()
    } catch (err) {
      // Map server errors to fields (see Server-Side Error Mapping)
      setError('title', { message: 'A task with this title already exists' })
    }
  })

  return (
    <form onSubmit={submit} noValidate>
      <div>
        <label htmlFor="title">Title *</label>
        <input
          id="title"
          {...register('title')}
          aria-invalid={!!errors.title}
          aria-describedby={errors.title ? 'title-error' : undefined}
        />
        {errors.title && (
          <p id="title-error" role="alert" className="text-red-600 text-sm">
            {errors.title.message}
          </p>
        )}
      </div>

      <button type="submit" disabled={isSubmitting || !isDirty}>
        {isSubmitting ? 'Saving...' : 'Save Task'}
      </button>
    </form>
  )
}
```

## Form Schema Definition with Zod

```typescript
import { z } from 'zod'

// Common field patterns
const emailField = z.string().email('Invalid email address').toLowerCase()
const passwordField = z.string()
  .min(8, 'At least 8 characters')
  .regex(/[A-Z]/, 'Must contain uppercase letter')
  .regex(/[0-9]/, 'Must contain a number')

const urlField = z.string().url('Must be a valid URL').optional().or(z.literal(''))

const phoneField = z.string()
  .regex(/^\+?[1-9]\d{1,14}$/, 'Invalid phone number')
  .optional()

// Cross-field validation (refine)
const PasswordChangeSchema = z
  .object({
    password:        passwordField,
    confirmPassword: z.string(),
  })
  .refine(data => data.password === data.confirmPassword, {
    message: 'Passwords do not match',
    path: ['confirmPassword'],   // error attached to confirmPassword field
  })

// Conditional fields (superRefine)
const EventSchema = z
  .object({
    type:      z.enum(['online', 'in-person']),
    url:       z.string().url().optional(),
    address:   z.string().optional(),
  })
  .superRefine((data, ctx) => {
    if (data.type === 'online' && !data.url) {
      ctx.addIssue({ code: 'custom', message: 'URL required for online events', path: ['url'] })
    }
    if (data.type === 'in-person' && !data.address) {
      ctx.addIssue({ code: 'custom', message: 'Address required', path: ['address'] })
    }
  })
```

## Multi-Step Form State Management

```typescript
import { useState } from 'react'
import { useForm, FormProvider } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'

const steps = ['Personal', 'Details', 'Review'] as const
type Step = (typeof steps)[number]

// Each step has its own schema
const Step1Schema = z.object({ name: z.string().min(1), email: emailField })
const Step2Schema = z.object({ company: z.string().min(1), role: z.string().min(1) })
const FullSchema = Step1Schema.merge(Step2Schema)

type FormData = z.infer<typeof FullSchema>

export function MultiStepForm() {
  const [currentStep, setCurrentStep] = useState(0)

  const methods = useForm<FormData>({
    resolver: zodResolver(FullSchema),
    mode: 'onTouched',
  })

  const stepSchemas = [Step1Schema, Step2Schema]

  const next = async () => {
    // Validate only current step's fields
    const fieldsToValidate = Object.keys(stepSchemas[currentStep].shape) as (keyof FormData)[]
    const valid = await methods.trigger(fieldsToValidate)
    if (valid) setCurrentStep(s => s + 1)
  }

  const submit = methods.handleSubmit(async (data) => {
    await createUser(data)
  })

  return (
    <FormProvider {...methods}>
      {/* Progress indicator */}
      <nav aria-label="Form steps">
        {steps.map((step, i) => (
          <span key={step} aria-current={i === currentStep ? 'step' : undefined}>
            {step}
          </span>
        ))}
      </nav>

      <form onSubmit={submit}>
        {currentStep === 0 && <Step1Fields />}
        {currentStep === 1 && <Step2Fields />}
        {currentStep === 2 && <ReviewStep />}

        <div className="flex gap-2">
          {currentStep > 0 && (
            <button type="button" onClick={() => setCurrentStep(s => s - 1)}>Back</button>
          )}
          {currentStep < steps.length - 1 ? (
            <button type="button" onClick={next}>Next</button>
          ) : (
            <button type="submit">Submit</button>
          )}
        </div>
      </form>
    </FormProvider>
  )
}
```

## Server-Side Validation Error Mapping

```typescript
import { useForm } from 'react-hook-form'

// API returns: { errors: { field: string[] } }
interface ApiError {
  errors?: Record<string, string[]>
  message?: string
}

export function RegistrationForm() {
  const { register, handleSubmit, setError, formState: { errors } } = useForm<FormData>()

  const submit = handleSubmit(async (data) => {
    try {
      await registerUser(data)
    } catch (err) {
      const apiError = err as ApiError

      if (apiError.errors) {
        // Map each server field error to react-hook-form
        Object.entries(apiError.errors).forEach(([field, messages]) => {
          setError(field as keyof FormData, {
            type: 'server',
            message: messages[0],
          })
        })
      } else {
        // Non-field error — show at form root
        setError('root', { message: apiError.message ?? 'Registration failed' })
      }
    }
  })

  return (
    <form onSubmit={submit}>
      {errors.root && <div role="alert" className="text-red-600">{errors.root.message}</div>}
      {/* fields */}
    </form>
  )
}
```

## Optimistic Validation (Real-time Feedback)

```typescript
import { useForm } from 'react-hook-form'
import { useCallback } from 'react'
import { useDebouncedCallback } from 'use-debounce'

export function UsernameField() {
  const { register, setError, clearErrors, formState: { errors } } = useForm()

  const checkUsername = useDebouncedCallback(async (username: string) => {
    if (username.length < 3) return
    try {
      const available = await fetch(`/api/check-username?u=${username}`)
        .then(r => r.json())
        .then(d => d.available)

      if (!available) {
        setError('username', { message: `"${username}" is already taken` })
      } else {
        clearErrors('username')
      }
    } catch {
      // network error — don't block the form
    }
  }, 400)

  return (
    <div>
      <input
        {...register('username', { onChange: (e) => checkUsername(e.target.value) })}
        aria-invalid={!!errors.username}
      />
      {errors.username && <p role="alert">{errors.username.message}</p>}
    </div>
  )
}
```

## File Upload with Preview

```typescript
import { useForm, Controller } from 'react-hook-form'
import { useState, useCallback } from 'react'

const UploadSchema = z.object({
  avatar: z
    .instanceof(File)
    .refine(f => f.size < 5 * 1024 * 1024, 'Max 5 MB')
    .refine(f => ['image/jpeg', 'image/png', 'image/webp'].includes(f.type), 'JPEG, PNG or WebP only'),
})

export function AvatarUpload() {
  const { control, handleSubmit } = useForm<z.infer<typeof UploadSchema>>({
    resolver: zodResolver(UploadSchema),
  })
  const [preview, setPreview] = useState<string | null>(null)

  return (
    <form onSubmit={handleSubmit(async ({ avatar }) => {
      const fd = new FormData()
      fd.append('avatar', avatar)
      await fetch('/api/avatar', { method: 'POST', body: fd })
    })}>
      <Controller
        name="avatar"
        control={control}
        render={({ field, fieldState }) => (
          <div>
            <input
              type="file"
              accept="image/jpeg,image/png,image/webp"
              onChange={e => {
                const file = e.target.files?.[0]
                if (!file) return
                field.onChange(file)
                setPreview(URL.createObjectURL(file))
              }}
            />
            {preview && <img src={preview} alt="Avatar preview" className="size-24 rounded-full object-cover" />}
            {fieldState.error && <p role="alert">{fieldState.error.message}</p>}
          </div>
        )}
      />
      <button type="submit">Upload</button>
    </form>
  )
}
```

## Dynamic Form Fields (Arrays, Conditional)

```typescript
import { useForm, useFieldArray, useWatch } from 'react-hook-form'

const LinksSchema = z.object({
  links: z.array(z.object({
    url:   z.string().url('Invalid URL'),
    label: z.string().min(1),
  })).min(1),
  hasExpiry: z.boolean(),
  expiryDate: z.string().optional(),
}).superRefine((data, ctx) => {
  if (data.hasExpiry && !data.expiryDate) {
    ctx.addIssue({ code: 'custom', message: 'Expiry date required', path: ['expiryDate'] })
  }
})

export function LinksForm() {
  const { register, control, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(LinksSchema),
    defaultValues: { links: [{ url: '', label: '' }], hasExpiry: false },
  })

  const { fields, append, remove } = useFieldArray({ control, name: 'links' })
  const hasExpiry = useWatch({ control, name: 'hasExpiry' })

  return (
    <form onSubmit={handleSubmit(console.log)}>
      {fields.map((field, i) => (
        <div key={field.id} className="flex gap-2">
          <input {...register(`links.${i}.url`)} placeholder="https://..." />
          <input {...register(`links.${i}.label`)} placeholder="Label" />
          <button type="button" onClick={() => remove(i)} disabled={fields.length === 1}>
            Remove
          </button>
          {errors.links?.[i]?.url && <p>{errors.links[i].url.message}</p>}
        </div>
      ))}
      <button type="button" onClick={() => append({ url: '', label: '' })}>Add Link</button>

      {/* Conditional field */}
      <label>
        <input type="checkbox" {...register('hasExpiry')} /> Set expiry date
      </label>
      {hasExpiry && <input type="date" {...register('expiryDate')} />}

      <button type="submit">Save</button>
    </form>
  )
}
```

## Form Submission States

```typescript
type FormStatus = 'idle' | 'submitting' | 'success' | 'error'

export function ContactForm() {
  const [status, setStatus] = useState<FormStatus>('idle')
  const { register, handleSubmit, reset } = useForm()

  const submit = handleSubmit(async (data) => {
    setStatus('submitting')
    try {
      await sendMessage(data)
      setStatus('success')
      reset()
      setTimeout(() => setStatus('idle'), 3000)
    } catch {
      setStatus('error')
    }
  })

  return (
    <form onSubmit={submit}>
      {/* fields */}
      {status === 'success' && (
        <div role="status" className="text-green-600">Message sent!</div>
      )}
      {status === 'error' && (
        <div role="alert" className="text-red-600">Failed to send. Try again.</div>
      )}
      <button type="submit" disabled={status === 'submitting'}>
        {status === 'submitting' ? 'Sending...' : 'Send'}
      </button>
    </form>
  )
}
```
