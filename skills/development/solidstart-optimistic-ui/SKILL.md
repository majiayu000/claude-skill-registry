---
name: solidstart-optimistic-ui
description: "SolidStart optimistic UI: use useSubmissions to show pending data immediately, combine server data with pending submissions, filter by pending state, handle rollback on errors."
metadata:
  globs:
    - "**/routes/**/*"
    - "**/*action*"
    - "**/*mutation*"
---

# SolidStart Optimistic UI

Optimistic UI shows the expected result immediately without waiting for the server response. If the request fails, the UI rolls back to the previous state.

## Core Concept

Use `useSubmissions` to track pending action submissions and combine them with server data to create an optimistic view.

## Basic Pattern

```tsx
import {
  action,
  createAsync,
  query,
  useAction,
  useSubmissions,
} from "@solidjs/router";
import { For } from "solid-js";

// Server data
const getServerTodos = query(async () => {
  "use server";
  return todos;
}, "serverTodos");

// Mutation action
const addTodo = action(async (title: string) => {
  "use server";
  await new Promise(r => setTimeout(r, 2000));
  todos.push({ title });
}, "add-todo");

export default function Home() {
  const serverTodos = createAsync(() => getServerTodos());
  const addTodoAction = useAction(addTodo);
  const todoSubmissions = useSubmissions(addTodo);

  // Extract pending todos from submissions
  const pendingTodos = () =>
    todoSubmissions
      .filter(submission => submission.pending)
      .map(submission => ({
        title: submission.input[0] + " (pending)",
      }));

  // Combine server data with pending items
  const todos = () =>
    serverTodos() ? [...serverTodos(), ...pendingTodos()] : [];

  return (
    <main>
      <h1>Todos</h1>
      <button onClick={() => addTodoAction("Todo 3")}>Add Todo</button>
      <For each={todos()}>
        {(todo) => <h3>{todo.title}</h3>}
      </For>
    </main>
  );
}
```

## Key Steps

1. **Get submissions**: Use `useSubmissions(action)` to track all submissions for an action
2. **Filter pending**: Use `.filter(submission => submission.pending)` to only show in-flight requests
3. **Map to data shape**: Transform `submission.input` into the same shape as server data
4. **Combine**: Merge server data with pending items: `[...serverData, ...pendingItems]`

## Important Notes

### Accessing Submissions Values

`useSubmissions` returns a reactive array (with a `.pending` boolean). Use it directly:

```tsx
// ✅ Correct
const pendingTodos = () =>
  todoSubmissions.filter(submission => submission.pending);

// ✅ Also valid
const pendingTodos = () => [...todoSubmissions];
```

### Filter by Pending State

Only include pending submissions to avoid duplicates. Once a submission completes, the server data will include it:

```tsx
const pendingTodos = () =>
  todoSubmissions
    .filter(submission => submission.pending) // Only pending ones!
    .map(submission => ({ title: submission.input[0] }));
```

### Accessing Action Input

The `submission.input` array contains the arguments passed to the action:

```tsx
// Action with single argument
const addTodo = action(async (title: string) => { ... }, "add-todo");
// submission.input[0] is the title

// Action with multiple arguments
const updateTodo = action(async (id: string, title: string) => { ... }, "update-todo");
// submission.input[0] is id, submission.input[1] is title

// Action with FormData
const addPost = action(async (formData: FormData) => { ... }, "add-post");
// submission.input[0] is FormData
const title = submission.input[0].get("title");
```

## Complete Example with FormData

```tsx
import {
  action,
  createAsync,
  query,
  useSubmissions,
} from "@solidjs/router";
import { For } from "solid-js";

const getPosts = query(async () => {
  "use server";
  return posts;
}, "posts");

const addPost = action(async (formData: FormData) => {
  "use server";
  const title = formData.get("title") as string;
  await new Promise(r => setTimeout(r, 1500));
  posts.push({ title });
}, "add-post");

export default function Home() {
  const serverPosts = createAsync(() => getPosts());
  const postSubmissions = useSubmissions(addPost);

  const pendingPosts = () =>
    postSubmissions
      .filter(submission => submission.pending)
      .map(submission => {
        const formData = submission.input[0] as FormData;
        return {
          title: formData.get("title") + " (pending)",
        };
      });

  const posts = () =>
    serverPosts() ? [...serverPosts(), ...pendingPosts()] : [];

  return (
    <main>
      <form action={addPost} method="post">
        <input name="title" />
        <button>Add Post</button>
      </form>
      <For each={posts()}>
        {(post) => <article>{post.title}</article>}
      </For>
    </main>
  );
}
```

## With Multiple Arguments

```tsx
const updateTodo = action(async (id: string, title: string, completed: boolean) => {
  "use server";
  await updateTodoInDB(id, { title, completed });
}, "update-todo");

export default function TodoList() {
  const todos = createAsync(() => getTodos());
  const submissions = useSubmissions(updateTodo);

  const pendingUpdates = () =>
    submissions
      .filter(submission => submission.pending)
      .map(submission => ({
        id: submission.input[0],      // id
        title: submission.input[1],   // title
        completed: submission.input[2], // completed
        pending: true,
      }));

  // Merge: replace existing todos with pending updates, then add new ones
  const todosWithPending = () => {
    const serverData = todos() || [];
    const pending = pendingUpdates();
    
    return serverData.map(todo => {
      const pendingUpdate = pending.find(p => p.id === todo.id);
      return pendingUpdate || todo;
    }).concat(
      pending.filter(p => !serverData.some(t => t.id === p.id))
    );
  };

  return <For each={todosWithPending()}>...</For>;
}
```

## Benefits

1. **Instant feedback**: Users see changes immediately
2. **Better UX**: No waiting for network requests
3. **Automatic cleanup**: When submission completes, it's no longer pending, so it disappears from the optimistic list and appears in server data
4. **No manual state management**: Solid's reactivity handles updates automatically

## Best Practices

1. **Filter by pending**: Always filter to only show pending submissions to avoid duplicates
2. **Match data shape**: Ensure optimistic items match the shape of server data
3. **Visual indicators**: Consider adding visual indicators (e.g., "(pending)") to distinguish optimistic items
4. **Handle errors**: If an action fails, the submission will no longer be pending, so it automatically disappears from the optimistic list
5. **Use with server actions**: This pattern works best with SolidStart actions, not just client-side state

## When to Use

- Adding items to a list
- Updating item properties
- Toggling boolean states (like, favorite, completed)
- Any mutation where you can predict the result

## When NOT to Use

- When the server response contains data you can't predict (e.g., generated IDs, timestamps)
- When operations are likely to fail validation
- When immediate consistency is critical
