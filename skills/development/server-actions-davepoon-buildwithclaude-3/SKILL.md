---
name: server-actions
description: This skill should be used when the user asks about "Server Actions", "form handling in Next.js", "mutations", "useFormState", "useFormStatus", "revalidatePath", "revalidateTag", or needs guidance on data mutations and form submissions in Next.js App Router.
version: 1.0.0
---

# Next.js Server Actions

## Overview

Server Actions are asynchronous functions that execute on the server. They can be called from Client and Server Components for data mutations, form submissions, and other server-side operations.

## Defining Server Actions

### In Server Components

Use the `'use server'` directive inside an async function:

```tsx
// app/page.tsx (Server Component)
export default function Page() {
  async function createPost(formData: FormData) {
    'use server'
    const title = formData.get('title') as string
    await db.post.create({ data: { title } })
  }

  return (
    <form action={createPost}>
      <input name="title" />
      <button type="submit">Create</button>
    </form>
  )
}
```

### In Separate Files

Mark the entire file with `'use server'`:

```tsx
// app/actions.ts
'use server'

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string
  await db.post.create({ data: { title } })
}

export async function deletePost(id: string) {
  await db.post.delete({ where: { id } })
}
```

## Form Handling

### Basic Form

```tsx
// app/actions.ts
'use server'

export async function submitContact(formData: FormData) {
  const name = formData.get('name') as string
  const email = formData.get('email') as string
  const message = formData.get('message') as string

  await db.contact.create({
    data: { name, email, message }
  })
}

// app/contact/page.tsx
import { submitContact } from '@/app/actions'

export default function ContactPage() {
  return (
    <form action={submitContact}>
      <input name="name" required />
      <input name="email" type="email" required />
      <textarea name="message" required />
      <button type="submit">Send</button>
    </form>
  )
}
```

### With Validation (Zod)

```tsx
// app/actions.ts
'use server'

import { z } from 'zod'

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})

export async function signup(formData: FormData) {
  const parsed = schema.safeParse({
    email: formData.get('email'),
    password: formData.get('password'),
  })

  if (!parsed.success) {
    return { error: parsed.error.flatten() }
  }

  await createUser(parsed.data)
  return { success: true }
}
```

## useFormState Hook

Handle form state and errors:

```tsx
// app/signup/page.tsx
'use client'

import { useFormState } from 'react-dom'
import { signup } from '@/app/actions'

const initialState = {
  error: null,
  success: false,
}

export default function SignupPage() {
  const [state, formAction] = useFormState(signup, initialState)

  return (
    <form action={formAction}>
      <input name="email" type="email" />
      <input name="password" type="password" />
      {state.error && (
        <p className="text-red-500">{state.error}</p>
      )}
      <button type="submit">Sign Up</button>
    </form>
  )
}

// app/actions.ts
'use server'

export async function signup(prevState: any, formData: FormData) {
  const email = formData.get('email') as string

  if (!email.includes('@')) {
    return { error: 'Invalid email', success: false }
  }

  await createUser({ email })
  return { error: null, success: true }
}
```

## useFormStatus Hook

Show loading states during submission:

```tsx
// components/submit-button.tsx
'use client'

import { useFormStatus } from 'react-dom'

export function SubmitButton() {
  const { pending } = useFormStatus()

  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Submitting...' : 'Submit'}
    </button>
  )
}

// Usage in form
import { SubmitButton } from '@/components/submit-button'

export default function Form() {
  return (
    <form action={submitAction}>
      <input name="title" />
      <SubmitButton />
    </form>
  )
}
```

## Revalidation

### revalidatePath

Revalidate a specific path:

```tsx
'use server'

import { revalidatePath } from 'next/cache'

export async function createPost(formData: FormData) {
  await db.post.create({ data: { ... } })

  // Revalidate the posts list page
  revalidatePath('/posts')

  // Revalidate a dynamic route
  revalidatePath('/posts/[slug]', 'page')

  // Revalidate all paths under /posts
  revalidatePath('/posts', 'layout')
}
```

### revalidateTag

Revalidate by cache tag:

```tsx
// Fetching with tags
const posts = await fetch('https://api.example.com/posts', {
  next: { tags: ['posts'] }
})

// Server Action
'use server'

import { revalidateTag } from 'next/cache'

export async function createPost(formData: FormData) {
  await db.post.create({ data: { ... } })
  revalidateTag('posts')
}
```

## Redirects After Actions

```tsx
'use server'

import { redirect } from 'next/navigation'

export async function createPost(formData: FormData) {
  const post = await db.post.create({ data: { ... } })

  // Redirect to the new post
  redirect(`/posts/${post.slug}`)
}
```

## Optimistic Updates

Update UI immediately while action completes:

```tsx
'use client'

import { useOptimistic } from 'react'
import { addTodo } from '@/app/actions'

export function TodoList({ todos }: { todos: Todo[] }) {
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    todos,
    (state, newTodo: string) => [
      ...state,
      { id: 'temp', title: newTodo, completed: false }
    ]
  )

  async function handleSubmit(formData: FormData) {
    const title = formData.get('title') as string
    addOptimisticTodo(title) // Update UI immediately
    await addTodo(formData)  // Server action
  }

  return (
    <>
      <form action={handleSubmit}>
        <input name="title" />
        <button>Add</button>
      </form>
      <ul>
        {optimisticTodos.map(todo => (
          <li key={todo.id}>{todo.title}</li>
        ))}
      </ul>
    </>
  )
}
```

## Non-Form Usage

Call Server Actions programmatically:

```tsx
'use client'

import { deletePost } from '@/app/actions'

export function DeleteButton({ id }: { id: string }) {
  return (
    <button onClick={() => deletePost(id)}>
      Delete
    </button>
  )
}
```

## Error Handling

```tsx
'use server'

export async function createPost(formData: FormData) {
  try {
    await db.post.create({ data: { ... } })
    return { success: true }
  } catch (error) {
    if (error instanceof PrismaClientKnownRequestError) {
      if (error.code === 'P2002') {
        return { error: 'A post with this title already exists' }
      }
    }
    return { error: 'Failed to create post' }
  }
}
```

## Security Considerations

1. **Always validate input** - Never trust client data
2. **Check authentication** - Verify user is authorized
3. **Use CSRF protection** - Built-in with Server Actions
4. **Sanitize output** - Prevent XSS attacks

```tsx
'use server'

import { auth } from '@/lib/auth'

export async function deletePost(id: string) {
  const session = await auth()

  if (!session) {
    throw new Error('Unauthorized')
  }

  const post = await db.post.findUnique({ where: { id } })

  if (post.authorId !== session.user.id) {
    throw new Error('Forbidden')
  }

  await db.post.delete({ where: { id } })
}
```

## Resources

For detailed patterns, see:
- `references/form-handling.md` - Advanced form patterns
- `references/revalidation.md` - Cache revalidation strategies
- `examples/mutation-patterns.md` - Complete mutation examples
