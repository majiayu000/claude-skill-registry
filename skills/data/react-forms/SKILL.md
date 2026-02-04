---
name: react-forms
description: Complete React forms system. PROACTIVELY activate for: (1) Controlled form patterns, (2) React Hook Form setup and validation, (3) Zod schema validation, (4) Dynamic fields with useFieldArray, (5) Server Actions with forms, (6) useOptimistic for optimistic updates, (7) File upload handling, (8) Multi-step form wizards. Provides: Form validation, error handling, field arrays, file drag-drop, form state management. Ensures robust form handling with proper validation and UX.
---

## Quick Reference

| Approach | Best For | Example |
|----------|----------|---------|
| Controlled | Simple forms | `value={state} onChange={...}` |
| React Hook Form | Complex forms | `useForm()` + `register()` |
| Server Actions | Next.js forms | `action={serverAction}` |

| React Hook Form | Usage |
|-----------------|-------|
| `register` | Connect input | `{...register('name')}` |
| `handleSubmit` | Form submission | `onSubmit={handleSubmit(fn)}` |
| `formState.errors` | Validation errors | `errors.name?.message` |
| `useFieldArray` | Dynamic fields | `fields.map(...)` |

| Validation | Setup |
|------------|-------|
| Inline | `register('email', { required: true })` |
| Zod | `resolver: zodResolver(schema)` |

## When to Use This Skill

Use for **React form implementation**:
- Building controlled forms with validation
- Setting up React Hook Form
- Adding Zod schema validation
- Creating dynamic form fields
- Handling file uploads with preview
- Building multi-step form wizards
- Using Server Actions for form submission

**For state management**: see `react-state-management`

---

# React Forms

## Controlled Forms

### Basic Controlled Form

```tsx
'use client';

import { useState, FormEvent, ChangeEvent } from 'react';

interface FormData {
  name: string;
  email: string;
  message: string;
}

function ContactForm() {
  const [formData, setFormData] = useState<FormData>({
    name: '',
    email: '',
    message: '',
  });

  const handleChange = (
    e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log('Form submitted:', formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="name">Name</label>
        <input
          id="name"
          name="name"
          type="text"
          value={formData.name}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label htmlFor="message">Message</label>
        <textarea
          id="message"
          name="message"
          value={formData.message}
          onChange={handleChange}
          required
        />
      </div>
      <button type="submit">Send</button>
    </form>
  );
}
```

### Form with Validation

```tsx
'use client';

import { useState, FormEvent, ChangeEvent } from 'react';

interface FormData {
  email: string;
  password: string;
  confirmPassword: string;
}

interface FormErrors {
  email?: string;
  password?: string;
  confirmPassword?: string;
}

function SignupForm() {
  const [formData, setFormData] = useState<FormData>({
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [touched, setTouched] = useState<Record<string, boolean>>({});

  const validate = (data: FormData): FormErrors => {
    const errors: FormErrors = {};

    if (!data.email) {
      errors.email = 'Email is required';
    } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(data.email)) {
      errors.email = 'Invalid email address';
    }

    if (!data.password) {
      errors.password = 'Password is required';
    } else if (data.password.length < 8) {
      errors.password = 'Password must be at least 8 characters';
    }

    if (data.password !== data.confirmPassword) {
      errors.confirmPassword = 'Passwords do not match';
    }

    return errors;
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    const newFormData = { ...formData, [name]: value };
    setFormData(newFormData);

    // Validate on change if field was touched
    if (touched[name]) {
      setErrors(validate(newFormData));
    }
  };

  const handleBlur = (e: ChangeEvent<HTMLInputElement>) => {
    const { name } = e.target;
    setTouched((prev) => ({ ...prev, [name]: true }));
    setErrors(validate(formData));
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const validationErrors = validate(formData);
    setErrors(validationErrors);
    setTouched({ email: true, password: true, confirmPassword: true });

    if (Object.keys(validationErrors).length === 0) {
      console.log('Form is valid:', formData);
    }
  };

  return (
    <form onSubmit={handleSubmit} noValidate>
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          onBlur={handleBlur}
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? 'email-error' : undefined}
        />
        {touched.email && errors.email && (
          <span id="email-error" className="error">{errors.email}</span>
        )}
      </div>

      <div>
        <label htmlFor="password">Password</label>
        <input
          id="password"
          name="password"
          type="password"
          value={formData.password}
          onChange={handleChange}
          onBlur={handleBlur}
          aria-invalid={!!errors.password}
        />
        {touched.password && errors.password && (
          <span className="error">{errors.password}</span>
        )}
      </div>

      <div>
        <label htmlFor="confirmPassword">Confirm Password</label>
        <input
          id="confirmPassword"
          name="confirmPassword"
          type="password"
          value={formData.confirmPassword}
          onChange={handleChange}
          onBlur={handleBlur}
          aria-invalid={!!errors.confirmPassword}
        />
        {touched.confirmPassword && errors.confirmPassword && (
          <span className="error">{errors.confirmPassword}</span>
        )}
      </div>

      <button type="submit">Sign Up</button>
    </form>
  );
}
```

## React Hook Form

### Basic Setup

```tsx
'use client';

import { useForm, SubmitHandler } from 'react-hook-form';

interface FormInputs {
  firstName: string;
  lastName: string;
  email: string;
  age: number;
}

function BasicForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormInputs>();

  const onSubmit: SubmitHandler<FormInputs> = async (data) => {
    await new Promise((resolve) => setTimeout(resolve, 1000));
    console.log(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label>First Name</label>
        <input
          {...register('firstName', { required: 'First name is required' })}
        />
        {errors.firstName && <span>{errors.firstName.message}</span>}
      </div>

      <div>
        <label>Last Name</label>
        <input
          {...register('lastName', { required: 'Last name is required' })}
        />
        {errors.lastName && <span>{errors.lastName.message}</span>}
      </div>

      <div>
        <label>Email</label>
        <input
          type="email"
          {...register('email', {
            required: 'Email is required',
            pattern: {
              value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
              message: 'Invalid email address',
            },
          })}
        />
        {errors.email && <span>{errors.email.message}</span>}
      </div>

      <div>
        <label>Age</label>
        <input
          type="number"
          {...register('age', {
            required: 'Age is required',
            min: { value: 18, message: 'Must be at least 18' },
            max: { value: 120, message: 'Invalid age' },
          })}
        />
        {errors.age && <span>{errors.age.message}</span>}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  );
}
```

### With Zod Validation

```tsx
'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
  username: z
    .string()
    .min(3, 'Username must be at least 3 characters')
    .max(20, 'Username must be less than 20 characters')
    .regex(/^[a-z0-9_]+$/, 'Only lowercase letters, numbers, and underscores'),
  email: z.string().email('Invalid email address'),
  password: z
    .string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Must contain at least one uppercase letter')
    .regex(/[0-9]/, 'Must contain at least one number'),
  confirmPassword: z.string(),
  role: z.enum(['user', 'admin', 'moderator']),
  terms: z.literal(true, {
    errorMap: () => ({ message: 'You must accept the terms' }),
  }),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
});

type FormData = z.infer<typeof schema>;

function ZodForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      role: 'user',
    },
  });

  const onSubmit = async (data: FormData) => {
    await new Promise((resolve) => setTimeout(resolve, 1000));
    console.log(data);
    reset();
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label>Username</label>
        <input {...register('username')} />
        {errors.username && <span>{errors.username.message}</span>}
      </div>

      <div>
        <label>Email</label>
        <input type="email" {...register('email')} />
        {errors.email && <span>{errors.email.message}</span>}
      </div>

      <div>
        <label>Password</label>
        <input type="password" {...register('password')} />
        {errors.password && <span>{errors.password.message}</span>}
      </div>

      <div>
        <label>Confirm Password</label>
        <input type="password" {...register('confirmPassword')} />
        {errors.confirmPassword && <span>{errors.confirmPassword.message}</span>}
      </div>

      <div>
        <label>Role</label>
        <select {...register('role')}>
          <option value="user">User</option>
          <option value="admin">Admin</option>
          <option value="moderator">Moderator</option>
        </select>
        {errors.role && <span>{errors.role.message}</span>}
      </div>

      <div>
        <label>
          <input type="checkbox" {...register('terms')} />
          I accept the terms and conditions
        </label>
        {errors.terms && <span>{errors.terms.message}</span>}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  );
}
```

### Dynamic Fields with useFieldArray

```tsx
'use client';

import { useForm, useFieldArray, SubmitHandler } from 'react-hook-form';

interface FormValues {
  teamName: string;
  members: {
    name: string;
    email: string;
    role: string;
  }[];
}

function DynamicFieldsForm() {
  const {
    register,
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<FormValues>({
    defaultValues: {
      teamName: '',
      members: [{ name: '', email: '', role: '' }],
    },
  });

  const { fields, append, remove, move } = useFieldArray({
    control,
    name: 'members',
  });

  const onSubmit: SubmitHandler<FormValues> = (data) => {
    console.log(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label>Team Name</label>
        <input {...register('teamName', { required: 'Team name is required' })} />
        {errors.teamName && <span>{errors.teamName.message}</span>}
      </div>

      <h3>Team Members</h3>
      {fields.map((field, index) => (
        <div key={field.id} className="member-row">
          <input
            placeholder="Name"
            {...register(`members.${index}.name` as const, {
              required: 'Name is required',
            })}
          />
          {errors.members?.[index]?.name && (
            <span>{errors.members[index]?.name?.message}</span>
          )}

          <input
            placeholder="Email"
            type="email"
            {...register(`members.${index}.email` as const, {
              required: 'Email is required',
            })}
          />

          <select {...register(`members.${index}.role` as const)}>
            <option value="">Select role</option>
            <option value="developer">Developer</option>
            <option value="designer">Designer</option>
            <option value="manager">Manager</option>
          </select>

          <button type="button" onClick={() => remove(index)}>
            Remove
          </button>
          {index > 0 && (
            <button type="button" onClick={() => move(index, index - 1)}>
              Move Up
            </button>
          )}
        </div>
      ))}

      <button
        type="button"
        onClick={() => append({ name: '', email: '', role: '' })}
      >
        Add Member
      </button>

      <button type="submit">Submit Team</button>
    </form>
  );
}
```

### Form with Watch and Conditional Fields

```tsx
'use client';

import { useForm, useWatch } from 'react-hook-form';

interface FormData {
  accountType: 'personal' | 'business';
  name: string;
  companyName?: string;
  taxId?: string;
  employeeCount?: string;
}

function ConditionalForm() {
  const { register, handleSubmit, control, formState: { errors } } = useForm<FormData>({
    defaultValues: {
      accountType: 'personal',
    },
  });

  const accountType = useWatch({
    control,
    name: 'accountType',
  });

  const onSubmit = (data: FormData) => {
    console.log(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label>Account Type</label>
        <select {...register('accountType')}>
          <option value="personal">Personal</option>
          <option value="business">Business</option>
        </select>
      </div>

      <div>
        <label>Name</label>
        <input {...register('name', { required: 'Name is required' })} />
        {errors.name && <span>{errors.name.message}</span>}
      </div>

      {accountType === 'business' && (
        <>
          <div>
            <label>Company Name</label>
            <input
              {...register('companyName', {
                required: accountType === 'business' ? 'Company name is required' : false,
              })}
            />
            {errors.companyName && <span>{errors.companyName.message}</span>}
          </div>

          <div>
            <label>Tax ID</label>
            <input
              {...register('taxId', {
                required: accountType === 'business' ? 'Tax ID is required' : false,
                pattern: {
                  value: /^\d{2}-\d{7}$/,
                  message: 'Format: XX-XXXXXXX',
                },
              })}
            />
            {errors.taxId && <span>{errors.taxId.message}</span>}
          </div>

          <div>
            <label>Number of Employees</label>
            <select {...register('employeeCount')}>
              <option value="1-10">1-10</option>
              <option value="11-50">11-50</option>
              <option value="51-200">51-200</option>
              <option value="200+">200+</option>
            </select>
          </div>
        </>
      )}

      <button type="submit">Submit</button>
    </form>
  );
}
```

## Server Actions with Forms

### Basic Server Action Form

```tsx
// actions.ts
'use server';

import { revalidatePath } from 'next/cache';

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  // Validate
  if (!title || title.length < 3) {
    return { error: 'Title must be at least 3 characters' };
  }

  // Save to database
  await db.posts.create({ data: { title, content } });

  revalidatePath('/posts');
  return { success: true };
}
```

```tsx
// CreatePostForm.tsx
'use client';

import { useActionState } from 'react';
import { createPost } from './actions';

const initialState = { error: null as string | null, success: false };

function CreatePostForm() {
  const [state, formAction, isPending] = useActionState(createPost, initialState);

  return (
    <form action={formAction}>
      {state.error && <div className="error">{state.error}</div>}
      {state.success && <div className="success">Post created!</div>}

      <div>
        <label htmlFor="title">Title</label>
        <input id="title" name="title" required />
      </div>

      <div>
        <label htmlFor="content">Content</label>
        <textarea id="content" name="content" required />
      </div>

      <button type="submit" disabled={isPending}>
        {isPending ? 'Creating...' : 'Create Post'}
      </button>
    </form>
  );
}
```

### Optimistic Updates with useOptimistic

```tsx
'use client';

import { useOptimistic, useTransition } from 'react';
import { addComment } from './actions';

interface Comment {
  id: string;
  text: string;
  author: string;
  pending?: boolean;
}

function CommentSection({ initialComments }: { initialComments: Comment[] }) {
  const [isPending, startTransition] = useTransition();
  const [optimisticComments, addOptimisticComment] = useOptimistic(
    initialComments,
    (state, newComment: Comment) => [...state, { ...newComment, pending: true }]
  );

  async function handleSubmit(formData: FormData) {
    const text = formData.get('text') as string;
    const tempId = `temp-${Date.now()}`;

    startTransition(async () => {
      // Optimistically add comment
      addOptimisticComment({
        id: tempId,
        text,
        author: 'Current User',
      });

      // Actually add comment
      await addComment(formData);
    });
  }

  return (
    <div>
      <ul>
        {optimisticComments.map((comment) => (
          <li key={comment.id} style={{ opacity: comment.pending ? 0.5 : 1 }}>
            <strong>{comment.author}</strong>: {comment.text}
            {comment.pending && <span> (posting...)</span>}
          </li>
        ))}
      </ul>

      <form action={handleSubmit}>
        <input name="text" placeholder="Add a comment" required />
        <button type="submit" disabled={isPending}>
          {isPending ? 'Posting...' : 'Post'}
        </button>
      </form>
    </div>
  );
}
```

### Form with useFormStatus

```tsx
'use client';

import { useFormStatus } from 'react-dom';

function SubmitButton() {
  const { pending, data, method, action } = useFormStatus();

  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Submitting...' : 'Submit'}
    </button>
  );
}

function ContactForm() {
  return (
    <form action={submitContactForm}>
      <input name="name" placeholder="Name" required />
      <input name="email" type="email" placeholder="Email" required />
      <textarea name="message" placeholder="Message" required />
      <SubmitButton />
    </form>
  );
}
```

## Custom Form Components

### Reusable Input Component

```tsx
import { forwardRef, InputHTMLAttributes } from 'react';
import { UseFormRegister, FieldError } from 'react-hook-form';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  name: string;
  error?: FieldError;
  register?: UseFormRegister<any>;
  validation?: object;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, name, error, register, validation, className, ...props }, ref) => {
    const inputProps = register ? register(name, validation) : { name, ref };

    return (
      <div className="form-field">
        <label htmlFor={name}>{label}</label>
        <input
          id={name}
          className={`input ${error ? 'input-error' : ''} ${className || ''}`}
          aria-invalid={!!error}
          aria-describedby={error ? `${name}-error` : undefined}
          {...inputProps}
          {...props}
        />
        {error && (
          <span id={`${name}-error`} className="error-message" role="alert">
            {error.message}
          </span>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';

export { Input };
```

### Select Component

```tsx
import { forwardRef, SelectHTMLAttributes } from 'react';
import { UseFormRegister, FieldError } from 'react-hook-form';

interface Option {
  value: string;
  label: string;
}

interface SelectProps extends SelectHTMLAttributes<HTMLSelectElement> {
  label: string;
  name: string;
  options: Option[];
  error?: FieldError;
  register?: UseFormRegister<any>;
  validation?: object;
  placeholder?: string;
}

const Select = forwardRef<HTMLSelectElement, SelectProps>(
  (
    { label, name, options, error, register, validation, placeholder, ...props },
    ref
  ) => {
    const selectProps = register ? register(name, validation) : { name, ref };

    return (
      <div className="form-field">
        <label htmlFor={name}>{label}</label>
        <select
          id={name}
          className={`select ${error ? 'select-error' : ''}`}
          aria-invalid={!!error}
          {...selectProps}
          {...props}
        >
          {placeholder && (
            <option value="" disabled>
              {placeholder}
            </option>
          )}
          {options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
        {error && <span className="error-message">{error.message}</span>}
      </div>
    );
  }
);

Select.displayName = 'Select';

export { Select };
```

### Checkbox Group

```tsx
import { UseFormRegister, FieldError } from 'react-hook-form';

interface CheckboxOption {
  value: string;
  label: string;
}

interface CheckboxGroupProps {
  name: string;
  label: string;
  options: CheckboxOption[];
  error?: FieldError;
  register: UseFormRegister<any>;
  validation?: object;
}

function CheckboxGroup({
  name,
  label,
  options,
  error,
  register,
  validation,
}: CheckboxGroupProps) {
  return (
    <fieldset className="form-field">
      <legend>{label}</legend>
      <div className="checkbox-group">
        {options.map((option) => (
          <label key={option.value} className="checkbox-label">
            <input
              type="checkbox"
              value={option.value}
              {...register(name, validation)}
            />
            {option.label}
          </label>
        ))}
      </div>
      {error && <span className="error-message">{error.message}</span>}
    </fieldset>
  );
}

export { CheckboxGroup };
```

## File Upload Forms

### Single File Upload

```tsx
'use client';

import { useState, ChangeEvent, FormEvent } from 'react';

function FileUploadForm() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);

      // Create preview for images
      if (selectedFile.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onloadend = () => {
          setPreview(reader.result as string);
        };
        reader.readAsDataURL(selectedFile);
      }
    }
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Upload failed');

      const result = await response.json();
      console.log('Upload successful:', result);
    } catch (error) {
      console.error('Upload error:', error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="file">Select File</label>
        <input
          id="file"
          type="file"
          accept="image/*,.pdf"
          onChange={handleFileChange}
        />
      </div>

      {preview && (
        <div className="preview">
          <img src={preview} alt="Preview" style={{ maxWidth: 200 }} />
        </div>
      )}

      {file && (
        <div className="file-info">
          <p>Name: {file.name}</p>
          <p>Size: {(file.size / 1024).toFixed(2)} KB</p>
          <p>Type: {file.type}</p>
        </div>
      )}

      <button type="submit" disabled={!file || uploading}>
        {uploading ? 'Uploading...' : 'Upload'}
      </button>
    </form>
  );
}
```

### Drag and Drop Upload

```tsx
'use client';

import { useState, DragEvent, useRef } from 'react';

function DragDropUpload() {
  const [files, setFiles] = useState<File[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDrag = (e: DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDragIn = (e: DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragOut = (e: DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDrop = (e: DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const droppedFiles = Array.from(e.dataTransfer.files);
    setFiles((prev) => [...prev, ...droppedFiles]);
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const selectedFiles = Array.from(e.target.files);
      setFiles((prev) => [...prev, ...selectedFiles]);
    }
  };

  const removeFile = (index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  };

  return (
    <div>
      <div
        className={`dropzone ${isDragging ? 'dragging' : ''}`}
        onDrag={handleDrag}
        onDragEnter={handleDragIn}
        onDragLeave={handleDragOut}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
      >
        <input
          ref={inputRef}
          type="file"
          multiple
          onChange={handleFileSelect}
          style={{ display: 'none' }}
        />
        <p>Drag files here or click to select</p>
      </div>

      {files.length > 0 && (
        <ul className="file-list">
          {files.map((file, index) => (
            <li key={`${file.name}-${index}`}>
              <span>{file.name}</span>
              <span>{(file.size / 1024).toFixed(2)} KB</span>
              <button onClick={() => removeFile(index)}>Remove</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

## Multi-Step Forms

```tsx
'use client';

import { useState } from 'react';
import { useForm, FormProvider, useFormContext } from 'react-hook-form';

interface FormData {
  // Step 1
  firstName: string;
  lastName: string;
  email: string;
  // Step 2
  address: string;
  city: string;
  zipCode: string;
  // Step 3
  cardNumber: string;
  expiryDate: string;
  cvv: string;
}

function Step1() {
  const { register, formState: { errors } } = useFormContext<FormData>();

  return (
    <div>
      <h2>Personal Information</h2>
      <input {...register('firstName', { required: 'Required' })} placeholder="First Name" />
      {errors.firstName && <span>{errors.firstName.message}</span>}

      <input {...register('lastName', { required: 'Required' })} placeholder="Last Name" />
      {errors.lastName && <span>{errors.lastName.message}</span>}

      <input {...register('email', { required: 'Required' })} placeholder="Email" type="email" />
      {errors.email && <span>{errors.email.message}</span>}
    </div>
  );
}

function Step2() {
  const { register, formState: { errors } } = useFormContext<FormData>();

  return (
    <div>
      <h2>Shipping Address</h2>
      <input {...register('address', { required: 'Required' })} placeholder="Address" />
      {errors.address && <span>{errors.address.message}</span>}

      <input {...register('city', { required: 'Required' })} placeholder="City" />
      {errors.city && <span>{errors.city.message}</span>}

      <input {...register('zipCode', { required: 'Required' })} placeholder="ZIP Code" />
      {errors.zipCode && <span>{errors.zipCode.message}</span>}
    </div>
  );
}

function Step3() {
  const { register, formState: { errors } } = useFormContext<FormData>();

  return (
    <div>
      <h2>Payment</h2>
      <input {...register('cardNumber', { required: 'Required' })} placeholder="Card Number" />
      {errors.cardNumber && <span>{errors.cardNumber.message}</span>}

      <input {...register('expiryDate', { required: 'Required' })} placeholder="MM/YY" />
      {errors.expiryDate && <span>{errors.expiryDate.message}</span>}

      <input {...register('cvv', { required: 'Required' })} placeholder="CVV" />
      {errors.cvv && <span>{errors.cvv.message}</span>}
    </div>
  );
}

const steps = [Step1, Step2, Step3];
const stepFields: (keyof FormData)[][] = [
  ['firstName', 'lastName', 'email'],
  ['address', 'city', 'zipCode'],
  ['cardNumber', 'expiryDate', 'cvv'],
];

function MultiStepForm() {
  const [currentStep, setCurrentStep] = useState(0);
  const methods = useForm<FormData>({ mode: 'onChange' });

  const StepComponent = steps[currentStep];

  const handleNext = async () => {
    const fields = stepFields[currentStep];
    const isValid = await methods.trigger(fields);

    if (isValid) {
      setCurrentStep((prev) => Math.min(prev + 1, steps.length - 1));
    }
  };

  const handlePrev = () => {
    setCurrentStep((prev) => Math.max(prev - 1, 0));
  };

  const onSubmit = (data: FormData) => {
    console.log('Form submitted:', data);
  };

  return (
    <FormProvider {...methods}>
      <form onSubmit={methods.handleSubmit(onSubmit)}>
        {/* Progress indicator */}
        <div className="progress">
          {steps.map((_, index) => (
            <div
              key={index}
              className={`step ${index <= currentStep ? 'active' : ''}`}
            >
              {index + 1}
            </div>
          ))}
        </div>

        <StepComponent />

        <div className="buttons">
          {currentStep > 0 && (
            <button type="button" onClick={handlePrev}>
              Previous
            </button>
          )}
          {currentStep < steps.length - 1 ? (
            <button type="button" onClick={handleNext}>
              Next
            </button>
          ) : (
            <button type="submit">Submit</button>
          )}
        </div>
      </form>
    </FormProvider>
  );
}
```

## Best Practices

| Practice | Description |
|----------|-------------|
| Use controlled inputs | Better predictability and React state sync |
| Validate on blur | Balance between UX and validation feedback |
| Show errors near inputs | Improves form accessibility |
| Disable submit while loading | Prevents duplicate submissions |
| Use proper input types | `email`, `tel`, `number` for better UX |
| Add aria attributes | `aria-invalid`, `aria-describedby` |
| Clear form on success | Reset state after successful submission |
| Handle server errors | Display API validation errors |
