---
name: solid-core-stores
description: "SolidJS stores: createStore for complex state, direct property access, path syntax for updates, produce for immutable mutations, reconcile for diffing, createMutable for proxy-based stores, unwrap for raw data."
metadata:
  globs:
    - "**/*store*"
    - "**/*state*"
---

# SolidJS Store Utilities

Complete guide to managing complex state with SolidJS stores. Stores provide fine-grained reactivity for objects and arrays, making them ideal for complex state management.

## createStore Basics

Stores manage complex data structures (objects, arrays) with fine-grained reactivity. Access properties directly - no getter functions needed.

```tsx
import { createStore } from "solid-js/store";

// Initialize store
const [store, setStore] = createStore({
  userCount: 3,
  users: [
    { id: 0, username: "felix909", location: "England", loggedIn: false },
    { id: 1, username: "tracy634", location: "Canada", loggedIn: true },
  ],
});

// Access properties directly (not store.users())
return <div>Users: {store.userCount}</div>;
```

**Key differences from signals:**
- Direct property access: `store.users` not `store.users()`
- Nested reactivity: changes to nested properties trigger updates automatically
- Path syntax: update specific nested paths with setter

## Store Getters

Stores support getters for derived values:

```tsx
const [state, setState] = createStore({
  user: {
    firstName: "John",
    lastName: "Smith",
    get fullName() {
      return `${this.firstName} ${this.lastName}`;
    },
  },
});

// Access getter
return <div>{state.user.fullName}</div>;
```

## Store Setters

Use path syntax to update stores. Objects are shallowly merged. Set to `undefined` to delete properties.

```tsx
// Shallow merge
setStore({ firstName: "Johnny", middleName: "Lee" });
// Result: { firstName: 'Johnny', middleName: 'Lee', lastName: 'Miller' }

// Function form
setStore((state) => ({ 
  preferredName: state.firstName, 
  lastName: "Milner" 
}));

// Path syntax for nested updates
setStore("users", 0, "loggedIn", true);

// Delete property
setStore("middleName", undefined);
// In TypeScript: setStore("middleName", undefined!);
```

## Path Syntax

Path syntax provides flexible ways to update nested structures:

```tsx
// Update array element by index
setStore("users", 0, { loggedIn: true });

// Update with function
setStore("users", 3, "loggedIn", (loggedIn) => !loggedIn);

// Filter and update
setStore("users", (user) => user.username.startsWith("t"), "loggedIn", false);

// Add to array
setStore("tasks", state.tasks.length, {
  id: state.tasks.length,
  text: "New task",
  completed: false,
});
```

## produce - Immutable Mutations

Use `produce` for Immer-style mutations. Simplifies complex nested updates:

```tsx
import { produce } from "solid-js/store";

const [state, setState] = createStore({
  user: { name: "John", age: 30 },
  list: ["book", "pen"],
});

// Mutate inside produce
setState(
  produce((state) => {
    state.user.name = "Jane";
    state.list.push("pencil");
  })
);
```

**Benefits:**
- Familiar mutation syntax
- Multiple property updates in one call
- Better readability for complex updates

## reconcile - Data Diffing

Use `reconcile` to efficiently diff and merge data changes. Perfect for API responses or immutable data:

```tsx
import { reconcile } from "solid-js/store";

// Subscribe to observable
const unsubscribe = store.subscribe(({ todos }) => {
  setState("todos", reconcile(todos));
});
onCleanup(() => unsubscribe());

// With options
setState(
  "todos",
  reconcile(newTodos, {
    key: "id",      // Match items by id
    merge: false,   // Replace non-matching items
  })
);
```

**Options:**
- `key`: Property to match items (default: `"id"`)
- `merge`: When `true`, morphs previous data to new value. When `false`, replaces non-matching items.

## createMutable - Proxy-Based Stores

Create mutable proxy stores for MobX/Vue compatibility or external system integration:

```tsx
import { createMutable } from "solid-js/store";

const state = createMutable({
  someValue: 0,
  list: [],
});

// Direct mutation
state.someValue = 5;
state.list.push(anotherValue);

// Getters and setters
const user = createMutable({
  firstName: "John",
  lastName: "Smith",
  get fullName() {
    return `${this.firstName} ${this.lastName}`;
  },
  set setFullName(value) {
    [this.firstName, this.lastName] = value.split(" ");
  },
});
```

**Note:** Prefer `createStore` for better unidirectional flow. Use `createMutable` only when needed for compatibility.

## modifyMutable - Batch Mutable Updates

Batch multiple mutable store changes to trigger a single update:

```tsx
import { modifyMutable, reconcile, produce } from "solid-js/store";

const state = createMutable({
  user: { firstName: "John", lastName: "Smith" },
});

// Multiple updates trigger multiple renders
state.user.firstName = "Jane";
state.user.lastName = "Doe";

// Batch with reconcile
modifyMutable(
  state.user,
  reconcile({
    firstName: "Jane",
    lastName: "Doe",
  })
);

// Batch with produce
modifyMutable(
  state,
  produce((state) => {
    state.user.firstName = "Jane";
    state.user.lastName = "Doe";
  })
);
```

**Benefits:**
- Single render cycle for multiple changes
- Works with `reconcile` and `produce`
- Better performance for complex updates

## unwrap - Extract Raw Data

Get underlying data without proxy wrapping:

```tsx
import { unwrap } from "solid-js/store";

const rawData = unwrap(store);
// Use for debugging, serialization, or third-party integrations
```

## Best Practices

1. **Use stores for complex state:**
   - Objects and arrays
   - Multiple related values
   - Nested data structures

2. **Use signals for simple state:**
   - Single primitive values
   - Simple counters
   - Toggle flags

3. **Prefer `createStore` over `createMutable`:**
   - Better unidirectional flow
   - More predictable updates
   - Use `produce` for mutation-style syntax

4. **Use `produce` for complex updates:**
   - Multiple property changes
   - Array manipulations
   - Nested object updates

5. **Use `reconcile` for external data:**
   - API responses
   - Observable subscriptions
   - Immutable data updates

6. **Access properties in tracking scopes:**
   - Properties accessed outside tracking scopes won't be reactive
   - Use `createEffect` to establish tracking

```tsx
// Not reactive
setState("numberOfTasks", state.tasks.length);

// Reactive
createEffect(() => {
  setState("numberOfTasks", state.tasks.length);
});
```

## Common Patterns

### Task List with Stores

```tsx
import { createStore } from "solid-js/store";
import { For } from "solid-js";

function TaskList() {
  const [state, setState] = createStore({
    tasks: [],
    numberOfTasks: 0,
  });

  const addTask = (text) => {
    setState("tasks", state.tasks.length, {
      id: state.tasks.length,
      text,
      completed: false,
    });
    setState("numberOfTasks", state.tasks.length + 1);
  };

  const toggleTask = (id) => {
    setState(
      "tasks",
      (task) => task.id === id,
      "completed",
      (completed) => !completed
    );
  };

  return (
    <>
      <h1>My Task List</h1>
      <span>You have {state.numberOfTasks} task(s) today!</span>
      <For each={state.tasks}>
        {(task) => (
          <div>
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => toggleTask(task.id)}
            />
            <span>{task.text}</span>
          </div>
        )}
      </For>
    </>
  );
}
```

### Using produce for Complex Updates

```tsx
const toggleTask = (id) => {
  setState(
    produce((state) => {
      const task = state.tasks.find((t) => t.id === id);
      if (task) {
        task.completed = !task.completed;
      }
    })
  );
};
```
