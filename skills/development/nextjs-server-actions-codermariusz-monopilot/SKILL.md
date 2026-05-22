---
name: nextjs-server-actions
description: When handling form submissions, data mutations, or any action that modifies server-side data. **Version Context**: Next.js 16.0+ uses `useActionState` (replaces deprecated `useFormState`).
version: 1.1.0
tokens: ~550
confidence: high
sources:
  - https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations
  - https://react.dev/reference/rsc/server-actions
last_validated: 2025-12-10
next_review: 2025-12-24
tags: [nextjs, react, forms, server-actions, frontend]
---

## When to Use
When handling form submissions, data mutations, or any action that modifies server-side data.

**Version Context**: Next.js 16.0+ uses `useActionState` (replaces deprecated `useFormState`).

## Patterns

### Basic Server Action
```typescript
// app/actions.ts
'use server'

import { revalidatePath } from 'next/cache';

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;

  await db.insert({ title });

  revalidatePath('/posts'); // Refresh the page data
}
```

### Form with Server Action
```tsx
// app/page.tsx
import { createPost } from './actions';

export default function Page() {
  return (
    <form action={createPost}>
      <input name="title" required />
      <button type="submit">Create</button>
    </form>
  );
}
```

### With Validation (Zod)
```typescript
'use server'

import { z } from 'zod';
import { redirect } from 'next/navigation';

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

export async function register(formData: FormData) {
  const result = schema.safeParse({
    email: formData.get('email'),
    password: formData.get('password'),
  });

  if (!result.success) {
    return { error: result.error.flatten() };
  }

  // Process valid data
  await createUser(result.data);
  redirect('/dashboard');
}
```

### With useActionState (Next.js 16+)
```tsx
'use client'

import { useActionState } from 'react';
import { register } from './actions';

export function RegisterForm() {
  const [state, action, pending] = useActionState(register, null);

  return (
    <form action={action}>
      <input name="email" />
      {state?.error?.email && <p>{state.error.email}</p>}
      <button disabled={pending}>
        {pending ? 'Loading...' : 'Submit'}
      </button>
    </form>
  );
}
```

### Legacy: useFormState (Next.js 15 and earlier)
```tsx
'use client'

import { useFormState, useFormStatus } from 'react-dom';
import { register } from './actions';

function SubmitButton() {
  const { pending } = useFormStatus();
  return <button disabled={pending}>{pending ? 'Loading...' : 'Submit'}</button>;
}

export function RegisterForm() {
  const [state, formAction] = useFormState(register, null);

  return (
    <form action={formAction}>
      <input name="email" />
      {state?.error?.email && <p>{state.error.email}</p>}
      <SubmitButton />
    </form>
  );
}
```

### Event Handler with useTransition
```tsx
'use client'

import { useTransition } from 'react';
import { updateProfile } from './actions';

export function ProfileButton() {
  const [isPending, startTransition] = useTransition();

  return (
    <button onClick={() => startTransition(async () => {
      await updateProfile();
    })}>
      {isPending ? 'Saving...' : 'Update Profile'}
    </button>
  );
}
```

## Anti-Patterns
- Not validating input server-side
- Forgetting revalidatePath after mutation
- Missing error handling
- Using deprecated `useFormState` in Next.js 16+
- Not handling pending states

## Verification Checklist
- [ ] Input validated with Zod
- [ ] revalidatePath/revalidateTag after mutations
- [ ] Error handling with return values
- [ ] Using `useActionState` for Next.js 16+
- [ ] Pending states properly displayed
