---
name: conform
description: Builds progressive enhancement forms with Conform using web standards, server validation, and framework integration. Use when building Remix/Next.js forms, implementing progressive enhancement, or needing accessible form validation.
---

# Conform

Type-safe form validation library with progressive enhancement for Remix and Next.js.

## Quick Start

```bash
npm install @conform-to/react @conform-to/zod zod
```

```tsx
import { useForm } from '@conform-to/react';
import { parseWithZod } from '@conform-to/zod';
import { z } from 'zod';

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

export default function LoginForm() {
  const [form, fields] = useForm({
    onValidate({ formData }) {
      return parseWithZod(formData, { schema });
    },
  });

  return (
    <form id={form.id} onSubmit={form.onSubmit}>
      <input
        name={fields.email.name}
        defaultValue={fields.email.initialValue}
      />
      <div>{fields.email.errors}</div>

      <input
        name={fields.password.name}
        type="password"
        defaultValue={fields.password.initialValue}
      />
      <div>{fields.password.errors}</div>

      <button>Submit</button>
    </form>
  );
}
```

## Remix Integration

### Action & Loader

```tsx
import { json, redirect } from '@remix-run/node';
import { useActionData } from '@remix-run/react';
import { useForm } from '@conform-to/react';
import { parseWithZod } from '@conform-to/zod';
import { z } from 'zod';

const schema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'At least 8 characters'),
});

export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData();
  const submission = parseWithZod(formData, { schema });

  if (submission.status !== 'success') {
    return json(submission.reply());
  }

  // Process valid data
  await createUser(submission.value);
  return redirect('/dashboard');
}

export default function SignUp() {
  const lastResult = useActionData<typeof action>();

  const [form, fields] = useForm({
    lastResult,
    onValidate({ formData }) {
      return parseWithZod(formData, { schema });
    },
    shouldValidate: 'onBlur',
    shouldRevalidate: 'onInput',
  });

  return (
    <form method="post" id={form.id} onSubmit={form.onSubmit}>
      <label>
        Email
        <input name={fields.email.name} />
        <div>{fields.email.errors}</div>
      </label>

      <label>
        Password
        <input name={fields.password.name} type="password" />
        <div>{fields.password.errors}</div>
      </label>

      <button>Sign Up</button>
    </form>
  );
}
```

## Next.js Integration (App Router)

### Server Action

```tsx
'use server';

import { parseWithZod } from '@conform-to/zod';
import { z } from 'zod';

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

export async function login(prevState: unknown, formData: FormData) {
  const submission = parseWithZod(formData, { schema });

  if (submission.status !== 'success') {
    return submission.reply();
  }

  // Authenticate user
  const user = await authenticate(submission.value);

  if (!user) {
    return submission.reply({
      formErrors: ['Invalid credentials'],
    });
  }

  redirect('/dashboard');
}
```

### Client Component

```tsx
'use client';

import { useFormState } from 'react-dom';
import { useForm } from '@conform-to/react';
import { parseWithZod } from '@conform-to/zod';
import { login } from './actions';

export function LoginForm() {
  const [lastResult, action] = useFormState(login, undefined);

  const [form, fields] = useForm({
    lastResult,
    onValidate({ formData }) {
      return parseWithZod(formData, { schema });
    },
  });

  return (
    <form id={form.id} action={action} onSubmit={form.onSubmit}>
      <input name={fields.email.name} />
      <div>{fields.email.errors}</div>

      <input name={fields.password.name} type="password" />
      <div>{fields.password.errors}</div>

      <button>Login</button>
    </form>
  );
}
```

## Form Configuration

### useForm Options

```tsx
const [form, fields] = useForm({
  // Last server result
  lastResult,

  // Client-side validation
  onValidate({ formData }) {
    return parseWithZod(formData, { schema });
  },

  // When to validate
  shouldValidate: 'onBlur',      // 'onSubmit' | 'onBlur' | 'onInput'
  shouldRevalidate: 'onInput',   // When to re-validate after error

  // Initial values
  defaultValue: {
    email: '',
    password: '',
  },

  // Constraint validation (HTML5)
  constraint: getZodConstraint(schema),
});
```

### Form Props

```tsx
<form
  id={form.id}
  onSubmit={form.onSubmit}
  noValidate  // Disable browser validation
>
  {/* Form errors */}
  {form.errors && <div>{form.errors}</div>}
</form>
```

## Field Helpers

### getInputProps

```tsx
import { getInputProps } from '@conform-to/react';

<input
  {...getInputProps(fields.email, {
    type: 'email',
    ariaAttributes: true,
  })}
/>

// Generates:
// name, id, defaultValue, aria-invalid, aria-describedby
```

### getTextareaProps

```tsx
import { getTextareaProps } from '@conform-to/react';

<textarea {...getTextareaProps(fields.message)} />
```

### getSelectProps

```tsx
import { getSelectProps } from '@conform-to/react';

<select {...getSelectProps(fields.country)}>
  <option value="">Select country</option>
  <option value="us">United States</option>
</select>
```

### Checkbox/Radio

```tsx
import { getInputProps } from '@conform-to/react';

<input
  {...getInputProps(fields.remember, { type: 'checkbox' })}
/>

<input
  {...getInputProps(fields.plan, { type: 'radio', value: 'free' })}
/>
<input
  {...getInputProps(fields.plan, { type: 'radio', value: 'pro' })}
/>
```

## Nested Objects

```tsx
const schema = z.object({
  user: z.object({
    name: z.string(),
    email: z.string().email(),
  }),
  address: z.object({
    street: z.string(),
    city: z.string(),
  }),
});

function Form() {
  const [form, fields] = useForm({
    onValidate({ formData }) {
      return parseWithZod(formData, { schema });
    },
  });

  const user = fields.user.getFieldset();
  const address = fields.address.getFieldset();

  return (
    <form>
      <input name={user.name.name} />
      <input name={user.email.name} />

      <input name={address.street.name} />
      <input name={address.city.name} />
    </form>
  );
}
```

## Field Arrays

```tsx
import { useForm, useFieldList, insert, remove } from '@conform-to/react';

const schema = z.object({
  tasks: z.array(z.object({
    title: z.string(),
    done: z.boolean().default(false),
  })),
});

function TaskForm() {
  const [form, fields] = useForm({
    onValidate({ formData }) {
      return parseWithZod(formData, { schema });
    },
    defaultValue: {
      tasks: [{ title: '', done: false }],
    },
  });

  const tasks = fields.tasks.getFieldList();

  return (
    <form id={form.id} onSubmit={form.onSubmit}>
      {tasks.map((task, index) => {
        const taskFields = task.getFieldset();

        return (
          <div key={task.key}>
            <input name={taskFields.title.name} />
            <input
              type="checkbox"
              name={taskFields.done.name}
              value="true"
            />
            <button
              {...form.remove.getButtonProps({
                name: fields.tasks.name,
                index,
              })}
            >
              Remove
            </button>
          </div>
        );
      })}

      <button
        {...form.insert.getButtonProps({
          name: fields.tasks.name,
          defaultValue: { title: '', done: false },
        })}
      >
        Add Task
      </button>

      <button>Submit</button>
    </form>
  );
}
```

## Intent Buttons

Handle different submit actions:

```tsx
<form>
  <button name="intent" value="save">
    Save Draft
  </button>
  <button name="intent" value="publish">
    Publish
  </button>
</form>
```

```tsx
// In action
export async function action({ request }) {
  const formData = await request.formData();
  const intent = formData.get('intent');

  if (intent === 'save') {
    // Save draft
  } else if (intent === 'publish') {
    // Publish
  }
}
```

## File Uploads

```tsx
const schema = z.object({
  avatar: z.instanceof(File)
    .refine((file) => file.size < 5_000_000, 'Max 5MB'),
});

function AvatarForm() {
  const [form, fields] = useForm({
    onValidate({ formData }) {
      return parseWithZod(formData, { schema });
    },
  });

  return (
    <form method="post" encType="multipart/form-data">
      <input type="file" name={fields.avatar.name} accept="image/*" />
      <div>{fields.avatar.errors}</div>
    </form>
  );
}
```

## Accessibility

Conform automatically handles accessibility:

```tsx
// Using getInputProps with ariaAttributes
<input
  {...getInputProps(fields.email, {
    type: 'email',
    ariaAttributes: true,
  })}
/>

// Generates:
// aria-invalid="true" when has errors
// aria-describedby pointing to error element

// Error element
<div id={fields.email.errorId}>{fields.email.errors}</div>
```

## Validation Schemas

### With Zod

```tsx
import { parseWithZod, getZodConstraint } from '@conform-to/zod';

const [form, fields] = useForm({
  constraint: getZodConstraint(schema),
  onValidate({ formData }) {
    return parseWithZod(formData, { schema });
  },
});
```

### With Yup

```tsx
import { parseWithYup, getYupConstraint } from '@conform-to/yup';

const [form, fields] = useForm({
  constraint: getYupConstraint(schema),
  onValidate({ formData }) {
    return parseWithYup(formData, { schema });
  },
});
```

### With Valibot

```tsx
import { parseWithValibot, getValibotConstraint } from '@conform-to/valibot';

const [form, fields] = useForm({
  constraint: getValibotConstraint(schema),
  onValidate({ formData }) {
    return parseWithValibot(formData, { schema });
  },
});
```

## Error Handling

### Field Errors

```tsx
{fields.email.errors?.map((error, i) => (
  <div key={i} className="error">{error}</div>
))}
```

### Form Errors

```tsx
{form.errors?.map((error, i) => (
  <div key={i} className="form-error">{error}</div>
))}
```

### Custom Server Errors

```tsx
// In action
return submission.reply({
  fieldErrors: {
    email: ['Email already registered'],
  },
  formErrors: ['Something went wrong'],
});
```

See [references/api.md](references/api.md) for complete API reference.
