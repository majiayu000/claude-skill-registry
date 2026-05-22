---
name: solidstart-data-mutation
description: "SolidStart data mutation: form submissions with actions, validation, error handling, pending states, optimistic UI, redirects, database operations, programmatic triggers."
metadata:
  globs:
    - "**/routes/**/*"
    - "**/*action*"
    - "**/*mutation*"
    - "**/*form*"
---

# SolidStart Data Mutation

Complete guide to handling data mutations in SolidStart using actions, forms, validation, and error handling.

## Basic Form Submission

Actions handle form submissions. Forms must use `method="post"`:

```tsx
import { action } from "@solidjs/router";

const addPost = action(async (formData: FormData) => {
  const title = formData.get("title") as string;
  await fetch("https://my-api.com/posts", {
    method: "POST",
    body: JSON.stringify({ title }),
  });
}, "addPost");

export default function Page() {
  return (
    <form action={addPost} method="post">
      <input name="title" />
      <button>Add Post</button>
    </form>
  );
}
```

**Requirements:**
- Action must have unique name (second parameter)
- Form must use `method="post"`
- Action receives `FormData` as first parameter
- Use `FormData.get()` to extract field values

## Passing Additional Arguments

Use `.with()` to pass additional arguments to actions:

```tsx
const addPost = action(async (userId: number, formData: FormData) => {
  const title = formData.get("title") as string;
  await fetch("https://my-api.com/posts", {
    method: "POST",
    body: JSON.stringify({ userId, title }),
  });
}, "addPost");

export default function Page() {
  const userId = 1;
  return (
    <form action={addPost.with(userId)} method="post">
      <input name="title" />
      <button>Add Post</button>
    </form>
  );
}
```

## Showing Pending UI

Use `useSubmission` to track submission state and show pending UI:

```tsx
import { action, useSubmission } from "@solidjs/router";

const addPost = action(async (formData: FormData) => {
  const title = formData.get("title") as string;
  await fetch("https://my-api.com/posts", {
    method: "POST",
    body: JSON.stringify({ title }),
  });
}, "addPost");

export default function Page() {
  const submission = useSubmission(addPost);
  
  return (
    <form action={addPost} method="post">
      <input name="title" />
      <button disabled={submission.pending}>
        {submission.pending ? "Adding..." : "Add Post"}
      </button>
    </form>
  );
}
```

**Submission properties:**
- `pending` - Boolean indicating if action is running
- `result` - Successful return value
- `error` - Error thrown
- `input` - Reactive input data
- `clear()` - Clear submission state
- `retry()` - Re-execute with same input

## Handling Errors

Display errors from failed actions:

```tsx
import { Show } from "solid-js";
import { action, useSubmission } from "@solidjs/router";

const addPost = action(async (formData: FormData) => {
  const title = formData.get("title") as string;
  const response = await fetch("https://my-api.com/posts", {
    method: "POST",
    body: JSON.stringify({ title }),
  });
  
  if (!response.ok) {
    throw new Error("Failed to add post");
  }
}, "addPost");

export default function Page() {
  const submission = useSubmission(addPost);
  
  return (
    <form action={addPost} method="post">
      <Show when={submission.error}>
        <p class="error">{submission.error.message}</p>
        <button onClick={() => submission.retry()}>Retry</button>
      </Show>
      <input name="title" />
      <button>Add Post</button>
    </form>
  );
}
```

## Validating Form Fields

Return validation errors from actions and display them:

```tsx
import { Show } from "solid-js";
import { action, useSubmission } from "@solidjs/router";

const addPost = action(async (formData: FormData) => {
  const title = formData.get("title") as string;
  
  // Validate
  if (!title || title.length < 2) {
    return {
      error: "Title must be at least 2 characters",
    };
  }
  
  await fetch("https://my-api.com/posts", {
    method: "POST",
    body: JSON.stringify({ title }),
  });
  
  return { success: true };
}, "addPost");

export default function Page() {
  const submission = useSubmission(addPost);
  
  return (
    <form action={addPost} method="post">
      <input name="title" />
      <Show when={submission.result?.error}>
        <p class="error">{submission.result.error}</p>
      </Show>
      <button>Add Post</button>
    </form>
  );
}
```

**Validation pattern:**
- Return error object from action (don't throw)
- Check `submission.result?.error` in UI
- Action continues execution if validation passes

## Optimistic UI

Show expected result immediately before server responds. See `solidstart-optimistic-ui` rule for detailed patterns.

Basic pattern with `useSubmission`:

```tsx
import { For, Show } from "solid-js";
import { action, useSubmission, query, createAsync } from "@solidjs/router";

const getPosts = query(async () => {
  const posts = await fetch("https://my-api.com/blog");
  return await posts.json();
}, "posts");

const addPost = action(async (formData: FormData) => {
  const title = formData.get("title") as string;
  await fetch("https://my-api.com/posts", {
    method: "POST",
    body: JSON.stringify({ title }),
  });
}, "addPost");

export default function Page() {
  const posts = createAsync(() => getPosts());
  const submission = useSubmission(addPost);
  
  return (
    <main>
      <form action={addPost} method="post">
        <input name="title" />
        <button>Add Post</button>
      </form>
      <ul>
        <For each={posts()}>{(post) => <li>{post.title}</li>}</For>
        <Show when={submission.pending}>
          <li>{submission.input?.[0]?.get("title")?.toString()} (pending)</li>
        </Show>
      </ul>
    </main>
  );
}
```

For multiple concurrent submissions, use `useSubmissions` (see `solidstart-optimistic-ui` rule).

## Redirecting After Mutation

Redirect users after successful mutation:

```tsx
import { action, redirect } from "@solidjs/router";

const addPost = action(async (formData: FormData) => {
  const title = formData.get("title") as string;
  const response = await fetch("https://my-api.com/posts", {
    method: "POST",
    body: JSON.stringify({ title }),
  });
  const post = await response.json();
  
  // Throw redirect to navigate
  throw redirect(`/posts/${post.id}`);
}, "addPost");
```

**Important:** Must `throw redirect()`, not return it.

## Using Database or ORM

Mark actions with `"use server"` to safely access database:

```tsx
import { action } from "@solidjs/router";
import { db } from "~/lib/db";

const addPost = action(async (formData: FormData) => {
  "use server";
  const title = formData.get("title") as string;
  await db.insert("posts").values({ title });
}, "addPost");
```

**Best practices:**
- Always use `"use server"` for database operations
- Keeps API keys and database credentials secure
- Runs exclusively on server
- Can be called from client (automatically transformed to RPC)

## Programmatic Action Triggers

Use `useAction` to trigger actions programmatically (not just from forms):

```tsx
import { createSignal } from "solid-js";
import { action, useAction } from "@solidjs/router";

const addPost = action(async (title: string) => {
  await fetch("https://my-api.com/posts", {
    method: "POST",
    body: JSON.stringify({ title }),
  });
}, "addPost");

export default function Page() {
  const [title, setTitle] = createSignal("");
  const addPostAction = useAction(addPost);
  
  const handleSubmit = async () => {
    await addPostAction(title());
    setTitle(""); // Clear input
  };
  
  return (
    <div>
      <input 
        value={title()} 
        onInput={(e) => setTitle(e.target.value)} 
      />
      <button onClick={handleSubmit}>Add Post</button>
    </div>
  );
}
```

**Use cases:**
- Custom form handling (not using native `<form>`)
- Button clicks that trigger mutations
- Complex validation before submission
- Multiple actions in sequence

## Complete Example: Form with Validation and Error Handling

```tsx
import { Show } from "solid-js";
import { action, useSubmission, redirect } from "@solidjs/router";

const createUser = action(async (formData: FormData) => {
  "use server";
  const email = formData.get("email") as string;
  const name = formData.get("name") as string;
  
  // Validation
  if (!email || !email.includes("@")) {
    return { error: "Invalid email address" };
  }
  
  if (!name || name.length < 2) {
    return { error: "Name must be at least 2 characters" };
  }
  
  // Database operation
  const user = await db.users.create({ email, name });
  
  // Redirect on success
  throw redirect(`/users/${user.id}`);
}, "createUser");

export default function CreateUserPage() {
  const submission = useSubmission(createUser);
  
  return (
    <form action={createUser} method="post">
      <input name="email" type="email" />
      <input name="name" />
      
      <Show when={submission.result?.error}>
        <p class="error">{submission.result.error}</p>
      </Show>
      
      <Show when={submission.error}>
        <p class="error">Error: {submission.error.message}</p>
        <button onClick={() => submission.retry()}>Retry</button>
      </Show>
      
      <button disabled={submission.pending}>
        {submission.pending ? "Creating..." : "Create User"}
      </button>
    </form>
  );
}
```

## Best Practices

1. **Always name actions**: Second parameter to `action()` must be unique
2. **Use `"use server"` for database**: Keeps credentials secure
3. **Track submissions**: Use `useSubmission` for better UX (pending, errors)
4. **Validate in actions**: Return error objects, don't throw for validation errors
5. **Handle errors**: Show error messages and provide retry options
6. **Use `.with()` for additional args**: When forms need extra context
7. **Throw redirects**: Must throw, not return, redirect responses
8. **Optimistic UI**: Use `useSubmissions` for multiple concurrent mutations
9. **Programmatic triggers**: Use `useAction` when not using native forms

## Common Patterns

### File Uploads

```tsx
const uploadFile = action(async (formData: FormData) => {
  "use server";
  const file = formData.get("file") as File;
  // Handle file upload
}, "uploadFile");

<form action={uploadFile} method="post" enctype="multipart/form-data">
  <input name="file" type="file" />
  <button>Upload</button>
</form>
```

### Multiple Actions in Sequence

```tsx
const saveDraft = useAction(saveDraftAction);
const publish = useAction(publishAction);

const handlePublish = async () => {
  await saveDraft(data);
  await publish(data.id);
};
```

### Conditional Redirects

```tsx
const updatePost = action(async (formData: FormData) => {
  "use server";
  const post = await db.posts.update(formData);
  
  if (post.published) {
    throw redirect(`/posts/${post.id}`);
  } else {
    throw redirect(`/posts/${post.id}/edit`);
  }
}, "updatePost");
```

