---
name: nextjs-server-actions
description: Complete Next.js Server Actions system (Next.js 15.5/16). PROACTIVELY activate for: (1) Defining Server Actions with 'use server', (2) Form handling with actions, (3) useActionState for form state, (4) useFormStatus for pending states, (5) Optimistic updates with useOptimistic, (6) Validation with Zod and next-safe-action, (7) Authorization in actions, (8) File uploads, (9) Revalidation after mutations, (10) Type-safe actions with next-safe-action library. Provides: Action patterns, form integration, validation, optimistic UI, error handling, next-safe-action integration. Ensures secure server mutations with proper validation and UX.
---

## Quick Reference

| Pattern | Code | Purpose |
|---------|------|---------|
| Inline action | `async function action() { 'use server'; }` | Define in component |
| Actions file | `'use server'` at file top | Dedicated actions file |
| Form action | `<form action={serverAction}>` | Native form integration |
| Bind args | `action.bind(null, id)` | Pass additional args |

| Hook | Import | Purpose |
|------|--------|---------|
| `useActionState` | `react` | Form state + pending |
| `useFormStatus` | `react-dom` | Pending state in children |
| `useOptimistic` | `react` | Optimistic UI updates |

| Revalidation | Function | Scope |
|--------------|----------|-------|
| `revalidatePath('/posts')` | Path-based | Specific route |
| `revalidateTag('posts')` | Tag-based | All tagged fetches |
| `redirect('/success')` | Navigation | After mutation |

## When to Use This Skill

Use for **server-side mutations**:
- Form submissions without API routes
- Database mutations (create, update, delete)
- File uploads to server
- Implementing optimistic updates
- Form validation with error display

**Related skills:**
- For data fetching: see `nextjs-data-fetching`
- For caching/revalidation: see `nextjs-caching`
- For authentication in actions: see `nextjs-authentication`

---

# Next.js Server Actions

## Defining Server Actions

### Inline Server Action

```tsx
// app/posts/page.tsx
export default function PostsPage() {
  async function createPost(formData: FormData) {
    'use server';

    const title = formData.get('title') as string;
    const content = formData.get('content') as string;

    await db.posts.create({
      data: { title, content },
    });

    revalidatePath('/posts');
  }

  return (
    <form action={createPost}>
      <input name="title" placeholder="Title" required />
      <textarea name="content" placeholder="Content" required />
      <button type="submit">Create Post</button>
    </form>
  );
}
```

### Separate Actions File

```tsx
// app/actions.ts
'use server';

import { revalidatePath, revalidateTag } from 'next/cache';
import { redirect } from 'next/navigation';
import { z } from 'zod';

const PostSchema = z.object({
  title: z.string().min(1, 'Title is required').max(100),
  content: z.string().min(1, 'Content is required'),
});

export async function createPost(formData: FormData) {
  const validatedFields = PostSchema.safeParse({
    title: formData.get('title'),
    content: formData.get('content'),
  });

  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
    };
  }

  try {
    await db.posts.create({
      data: validatedFields.data,
    });
  } catch (error) {
    return { error: 'Failed to create post' };
  }

  revalidatePath('/posts');
  redirect('/posts');
}

export async function deletePost(id: string) {
  await db.posts.delete({ where: { id } });
  revalidateTag('posts');
}

export async function updatePost(id: string, formData: FormData) {
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  await db.posts.update({
    where: { id },
    data: { title, content },
  });

  revalidatePath(`/posts/${id}`);
  return { success: true };
}
```

## Using Server Actions in Forms

### Basic Form

```tsx
// app/contact/page.tsx
import { submitContact } from './actions';

export default function ContactPage() {
  return (
    <form action={submitContact}>
      <input name="name" placeholder="Name" required />
      <input name="email" type="email" placeholder="Email" required />
      <textarea name="message" placeholder="Message" required />
      <button type="submit">Send</button>
    </form>
  );
}
```

### Form with useActionState

```tsx
// app/signup/page.tsx
'use client';

import { useActionState } from 'react';
import { signup } from './actions';

const initialState = {
  errors: {} as Record<string, string[]>,
  message: '',
};

export default function SignupPage() {
  const [state, formAction, isPending] = useActionState(signup, initialState);

  return (
    <form action={formAction}>
      <div>
        <input name="email" type="email" placeholder="Email" />
        {state.errors?.email && (
          <p className="error">{state.errors.email[0]}</p>
        )}
      </div>

      <div>
        <input name="password" type="password" placeholder="Password" />
        {state.errors?.password && (
          <p className="error">{state.errors.password[0]}</p>
        )}
      </div>

      {state.message && <p className="message">{state.message}</p>}

      <button type="submit" disabled={isPending}>
        {isPending ? 'Signing up...' : 'Sign Up'}
      </button>
    </form>
  );
}
```

```tsx
// app/signup/actions.ts
'use server';

import { z } from 'zod';

const SignupSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

export async function signup(prevState: any, formData: FormData) {
  const validatedFields = SignupSchema.safeParse({
    email: formData.get('email'),
    password: formData.get('password'),
  });

  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
      message: '',
    };
  }

  try {
    await createUser(validatedFields.data);
    return { errors: {}, message: 'Account created successfully!' };
  } catch (error) {
    return { errors: {}, message: 'Failed to create account' };
  }
}
```

### useFormStatus for Pending State

```tsx
// components/SubmitButton.tsx
'use client';

import { useFormStatus } from 'react-dom';

export function SubmitButton({ children }: { children: React.ReactNode }) {
  const { pending } = useFormStatus();

  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Submitting...' : children}
    </button>
  );
}
```

```tsx
// Usage in form
import { SubmitButton } from '@/components/SubmitButton';

export default function Form() {
  return (
    <form action={submitForm}>
      <input name="title" />
      <SubmitButton>Submit</SubmitButton>
    </form>
  );
}
```

## Optimistic Updates

### useOptimistic Hook

```tsx
// app/posts/[id]/comments.tsx
'use client';

import { useOptimistic, useTransition } from 'react';
import { addComment } from './actions';

interface Comment {
  id: string;
  text: string;
  pending?: boolean;
}

export function Comments({ initialComments }: { initialComments: Comment[] }) {
  const [isPending, startTransition] = useTransition();
  const [optimisticComments, addOptimisticComment] = useOptimistic(
    initialComments,
    (state, newComment: Comment) => [...state, { ...newComment, pending: true }]
  );

  async function handleSubmit(formData: FormData) {
    const text = formData.get('text') as string;

    startTransition(async () => {
      addOptimisticComment({
        id: `temp-${Date.now()}`,
        text,
      });

      await addComment(formData);
    });
  }

  return (
    <div>
      <ul>
        {optimisticComments.map((comment) => (
          <li
            key={comment.id}
            style={{ opacity: comment.pending ? 0.5 : 1 }}
          >
            {comment.text}
            {comment.pending && ' (posting...)'}
          </li>
        ))}
      </ul>

      <form action={handleSubmit}>
        <input name="text" placeholder="Add comment" required />
        <button type="submit" disabled={isPending}>
          Add
        </button>
      </form>
    </div>
  );
}
```

### Optimistic Like Button

```tsx
// components/LikeButton.tsx
'use client';

import { useOptimistic, useTransition } from 'react';
import { toggleLike } from '@/app/actions';

interface LikeButtonProps {
  postId: string;
  initialLiked: boolean;
  initialCount: number;
}

export function LikeButton({
  postId,
  initialLiked,
  initialCount,
}: LikeButtonProps) {
  const [isPending, startTransition] = useTransition();
  const [optimistic, setOptimistic] = useOptimistic(
    { liked: initialLiked, count: initialCount },
    (state, liked: boolean) => ({
      liked,
      count: liked ? state.count + 1 : state.count - 1,
    })
  );

  const handleClick = () => {
    startTransition(async () => {
      setOptimistic(!optimistic.liked);
      await toggleLike(postId);
    });
  };

  return (
    <button onClick={handleClick} disabled={isPending}>
      {optimistic.liked ? '❤️' : '🤍'} {optimistic.count}
    </button>
  );
}
```

## Bound Arguments

### Passing Arguments with bind

```tsx
// components/DeleteButton.tsx
'use client';

import { deletePost } from '@/app/actions';

export function DeleteButton({ postId }: { postId: string }) {
  const deletePostWithId = deletePost.bind(null, postId);

  return (
    <form action={deletePostWithId}>
      <button type="submit">Delete</button>
    </form>
  );
}
```

```tsx
// app/actions.ts
'use server';

export async function deletePost(postId: string, formData: FormData) {
  await db.posts.delete({ where: { id: postId } });
  revalidatePath('/posts');
}
```

### Hidden Input Alternative

```tsx
// components/EditForm.tsx
export function EditForm({ post }: { post: Post }) {
  return (
    <form action={updatePost}>
      <input type="hidden" name="id" value={post.id} />
      <input name="title" defaultValue={post.title} />
      <textarea name="content" defaultValue={post.content} />
      <button type="submit">Update</button>
    </form>
  );
}
```

## Non-Form Invocation

### Button Click

```tsx
// components/LogoutButton.tsx
'use client';

import { logout } from '@/app/actions';

export function LogoutButton() {
  return (
    <button onClick={() => logout()}>
      Log Out
    </button>
  );
}
```

### Event Handler

```tsx
// components/TodoItem.tsx
'use client';

import { toggleTodo, deleteTodo } from '@/app/actions';

export function TodoItem({ todo }: { todo: Todo }) {
  return (
    <li>
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => toggleTodo(todo.id)}
      />
      <span>{todo.title}</span>
      <button onClick={() => deleteTodo(todo.id)}>Delete</button>
    </li>
  );
}
```

## Validation

### Zod Schema Validation

```tsx
// app/actions.ts
'use server';

import { z } from 'zod';

const CreateUserSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  age: z.coerce.number().min(18, 'Must be at least 18 years old'),
});

export type CreateUserState = {
  errors?: {
    name?: string[];
    email?: string[];
    age?: string[];
  };
  message?: string;
};

export async function createUser(
  prevState: CreateUserState,
  formData: FormData
): Promise<CreateUserState> {
  const validatedFields = CreateUserSchema.safeParse({
    name: formData.get('name'),
    email: formData.get('email'),
    age: formData.get('age'),
  });

  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
    };
  }

  try {
    await db.users.create({ data: validatedFields.data });
    return { message: 'User created successfully!' };
  } catch (error) {
    return { message: 'Database error: Failed to create user.' };
  }
}
```

## Authorization

### Checking User Permissions

```tsx
// app/actions.ts
'use server';

import { auth } from '@/lib/auth';
import { forbidden, unauthorized } from 'next/navigation';

export async function deletePost(postId: string) {
  const session = await auth();

  if (!session) {
    unauthorized();
  }

  const post = await db.posts.findUnique({ where: { id: postId } });

  if (post?.authorId !== session.user.id && session.user.role !== 'admin') {
    forbidden();
  }

  await db.posts.delete({ where: { id: postId } });
  revalidatePath('/posts');
}
```

### Role-Based Access

```tsx
// app/actions.ts
'use server';

import { auth } from '@/lib/auth';

export async function updateSettings(formData: FormData) {
  const session = await auth();

  if (!session) {
    return { error: 'Not authenticated' };
  }

  if (session.user.role !== 'admin') {
    return { error: 'Not authorized' };
  }

  // Update settings
  await updateSystemSettings(formData);

  revalidatePath('/settings');
  return { success: true };
}
```

## Error Handling

### Try-Catch Pattern

```tsx
// app/actions.ts
'use server';

export async function createPost(formData: FormData) {
  try {
    const title = formData.get('title') as string;
    const content = formData.get('content') as string;

    await db.posts.create({ data: { title, content } });

    revalidatePath('/posts');
    return { success: true };
  } catch (error) {
    console.error('Failed to create post:', error);
    return { error: 'Failed to create post. Please try again.' };
  }
}
```

### Redirect After Action

```tsx
// app/actions.ts
'use server';

import { redirect } from 'next/navigation';

export async function createPost(formData: FormData) {
  const post = await db.posts.create({
    data: {
      title: formData.get('title') as string,
      content: formData.get('content') as string,
    },
  });

  revalidatePath('/posts');
  redirect(`/posts/${post.slug}`);
}
```

## File Uploads

### Basic File Upload

```tsx
// app/upload/page.tsx
import { uploadFile } from './actions';

export default function UploadPage() {
  return (
    <form action={uploadFile}>
      <input type="file" name="file" accept="image/*" required />
      <button type="submit">Upload</button>
    </form>
  );
}
```

```tsx
// app/upload/actions.ts
'use server';

import { writeFile } from 'fs/promises';
import { join } from 'path';

export async function uploadFile(formData: FormData) {
  const file = formData.get('file') as File;

  if (!file || file.size === 0) {
    return { error: 'No file provided' };
  }

  const bytes = await file.arrayBuffer();
  const buffer = Buffer.from(bytes);

  const filename = `${Date.now()}-${file.name}`;
  const path = join(process.cwd(), 'public/uploads', filename);

  await writeFile(path, buffer);

  return { success: true, path: `/uploads/${filename}` };
}
```

## Best Practices

| Practice | Description |
|----------|-------------|
| Validate all inputs | Use Zod or similar for validation |
| Check authorization | Verify user permissions in each action |
| Handle errors gracefully | Return error messages, don't throw |
| Use optimistic updates | Better UX for mutations |
| Revalidate properly | Use revalidatePath or revalidateTag |
| Keep actions focused | One action per mutation |
| Type return values | Define state types for useActionState |
