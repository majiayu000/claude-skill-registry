---
name: solid-router-actions
description: "Solid Router actions: action() for mutations, useAction for programmatic calls, useSubmission/useSubmissions for tracking state, form submissions with FormData."
metadata:
  globs:
    - "**/*router*"
    - "**/routes/**/*"
---

# Solid Router Actions & Submissions

## Defining Actions

Actions handle mutations and form submissions:

```tsx
import { action } from "@solidjs/router";

const createTicketAction = action(async (subject: string) => {
  const response = await fetch("/api/tickets", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ subject })
  });
  
  if (!response.ok) {
    const error = await response.json();
    return { ok: false, message: error.message };
  }
  
  return { ok: true };
}, "createTicket");
```

## Using Actions with Forms

```tsx
import { action } from "@solidjs/router";

const submitFeedbackAction = action(async (formData: FormData) => {
  const message = formData.get("message")?.toString();
  // Process form data
  return { success: true };
}, "submitFeedback");

function FeedbackForm() {
  return (
    <form action={submitFeedbackAction} method="post">
      <textarea name="message" placeholder="Message" />
      <button type="submit">Send feedback</button>
    </form>
  );
}
```

**Form requirements:**
- Must have `method="post"`
- Action receives `FormData` as first parameter
- For file uploads, add `enctype="multipart/form-data"`

## Using Actions Programmatically

```tsx
import { useAction } from "@solidjs/router";

function EditUser({ userId }: { userId: string }) {
  const updateUser = useAction(updateUserAction);
  
  const handleSubmit = async (event: SubmitEvent) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget as HTMLFormElement);
    await updateUser(userId, formData);
  };
  
  return <form onSubmit={handleSubmit}>...</form>;
}
```

## Action with Multiple Arguments

```tsx
const updateUserAction = action(async (userId: string, formData: FormData) => {
  // ...
}, "updateUser");

// Use with .with() helper
<form action={updateUserAction.with(userId)} method="post">
  <input name="name" />
  <button type="submit">Update</button>
</form>
```

## Submissions

### useSubmission

Track single form submission state:

```tsx
import { useSubmission, Show } from "@solidjs/router";

function AddTodoForm() {
  const submission = useSubmission(addTodoAction);
  
  return (
    <form action={addTodoAction} method="post">
      <input name="name" />
      <button type="submit" disabled={submission.pending}>
        {submission.pending ? "Adding..." : "Add"}
      </button>
      <Show when={submission.result?.ok === false}>
        <div>{submission.result.message}</div>
        <button onClick={() => submission.retry()}>Retry</button>
      </Show>
    </form>
  );
}
```

**Submission properties:**
- `input` - Reactive input data
- `result` - Successful return value
- `error` - Error thrown
- `pending` - Boolean indicating if running
- `clear()` - Clear submission state
- `retry()` - Re-execute with same input

### useSubmissions

Track multiple submissions (useful for optimistic UI, lists):

```tsx
import { useSubmissions, For } from "@solidjs/router";

function AddTodoForm() {
  const submissions = useSubmissions(addTodoAction);
  
  return (
    <div>
      <form action={addTodoAction} method="post">
        <input name="name" />
        <button type="submit">Add</button>
      </form>
      <For each={submissions}>
        {(submission) => (
          <div>
            <span>Adding "{submission.input[0].get("name")}"</span>
            <Show when={submission.pending}> (pending...)</Show>
            <Show when={submission.result?.ok}> (completed)</Show>
            <Show when={submission.error}>
              Error: {submission.error.message}
              <button onClick={() => submission.retry()}>Retry</button>
            </Show>
          </div>
        )}
      </For>
    </div>
  );
}
```

### Filtering Submissions

```tsx
const failedSubmissions = useSubmissions(
  addTodoAction,
  ([formData]: [FormData]) => {
    const name = formData.get("name")?.toString() ?? "";
    return name.length <= 2; // Filter for failed validations
  }
);
```

## Optimistic Updates

```tsx
const updateTodoAction = action(async (id: string, completed: boolean) => {
  await api.updateTodo(id, { completed });
  return { id, completed };
}, "updateTodo");

function Todo({ todo }) {
  const update = useAction(updateTodoAction);
  
  const handleToggle = async () => {
    // Optimistically update UI
    setTodo({ ...todo, completed: !todo.completed });
    
    try {
      await update(todo.id, !todo.completed);
    } catch (error) {
      // Revert on error
      setTodo(todo);
    }
  };
  
  return <input type="checkbox" checked={todo.completed} onChange={handleToggle} />;
}
```

## Best Practices

1. Track submissions for better UX (pending, error states)
2. Use `useSubmission` for single form feedback
3. Use `useSubmissions` for optimistic UI and lists
4. Handle errors properly in actions
5. Use `.with()` helper for multiple arguments in forms
