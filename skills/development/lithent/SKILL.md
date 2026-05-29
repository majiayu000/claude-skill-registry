---
name: lithent
title: Lithent Agent Skills
version: {{VERSION}}
description: AI agent skills for working with the Lithent library.
additional_materials:
  - constraints/
  - reference/
  - examples/
---

# Lithent Agent Skills

> Version: {{VERSION}}

This file provides AI agent skills for working with the Lithent library.

## Overview

Lithent is a lightweight (~4KB) JSX-based virtual DOM library with closure-based state management. It offers two component modes:
- **Manual Mode** (`mount`): Explicit control with `renew()` function
- **Light API Mode** (`lmount`): Auto-reactive with `lstate`/`lstore`

## Component Creation

### Manual Mode (mount)

```tsx
import { mount, render } from 'lithent';
import { state } from 'lithent/helper';

const Counter = mount<{ initial?: number }>((renew, props) => {
  const count = state(props.initial ?? 0, renew);

  return () => (
    <div>
      <p>Count: {count.value}</p>
      <button onClick={() => count.value++}>+1</button>
    </div>
  );
});

render(<Counter initial={10} />, document.getElementById('app')!);
```

### Light API Mode (lmount)

```tsx
import { lmount, render } from 'lithent';
import { lstate } from 'lithent/helper';

const Counter = lmount<{ initial?: number }>((props) => {
  const count = lstate(props.initial ?? 0);

  return () => (
    <div>
      <p>Count: {count.value}</p>
      <button onClick={() => count.value++}>+1</button>
    </div>
  );
});

render(<Counter initial={10} />, document.getElementById('app')!);
```

## State Management

### State (Manual Mode)

```tsx
import { mount } from 'lithent';
import { state, computed, effect } from 'lithent/helper';

const Component = mount((renew) => {
  const firstName = state('John', renew);
  const lastName = state('Doe', renew);

  // Derived value
  const fullName = computed(() => `${firstName.value} ${lastName.value}`);

  // Side effect
  effect(() => {
    console.log('Name changed:', fullName.value);
    return () => console.log('Cleanup');
  });

  return () => <p>{fullName.value}</p>;
});
```

### State (Light API Mode)

```tsx
import { lmount } from 'lithent';
import { lstate, computed, effect } from 'lithent/helper';

const Component = lmount(() => {
  const firstName = lstate('John');
  const lastName = lstate('Doe');

  const fullName = computed(() => `${firstName.value} ${lastName.value}`);

  effect(() => {
    console.log('Name changed:', fullName.value);
  });

  return () => <p>{fullName.value}</p>;
});
```

### Global Store

```tsx
// Manual Mode
import { store } from 'lithent/helper';
const userStore = store({ name: '', loggedIn: false });

const Component = mount((renew) => {
  const user = userStore(renew);
  return () => <p>{user.name}</p>;
});

// Light API Mode
import { lstore } from 'lithent/helper';
const userStore = lstore({ name: '', loggedIn: false });

const Component = lmount(() => {
  const user = userStore();
  return () => <p>{user.name}</p>;
});
```

## Lifecycle Hooks

```tsx
import { mount, mountCallback, updateCallback, mountReadyCallback } from 'lithent';

const Component = mount((renew) => {
  // After mount (return cleanup function for unmount)
  mountCallback(() => {
    console.log('Mounted');
    return () => console.log('Unmounted');
  });

  // Before each update
  updateCallback(() => {
    console.log('Will update');
  });

  // After initial render complete
  mountReadyCallback(() => {
    console.log('Initial render done');
  });

  return () => <div>Hello</div>;
});
```

## DOM References

```tsx
import { mount, ref } from 'lithent';

const Component = mount((renew) => {
  const inputRef = ref<HTMLInputElement>(null);

  const focusInput = () => inputRef.value?.focus();

  return () => (
    <div>
      <input ref={inputRef} type="text" />
      <button onClick={focusInput}>Focus</button>
    </div>
  );
});
```

## Context API

```tsx
// Manual Mode
import { mount } from 'lithent';
import { createContext } from 'lithent/helper';

const ThemeContext = createContext<{ theme: string }>();

const Provider = mount((renew, _props, children) => {
  return () => (
    <ThemeContext.Provider value={{ theme: 'dark' }}>
      {children}
    </ThemeContext.Provider>
  );
});

const Consumer = mount((renew) => {
  const { theme } = ThemeContext.useContext(renew);
  return () => <p>{theme}</p>;
});

// Light API Mode
import { lmount } from 'lithent';
import { createLContext } from 'lithent/helper';

const ThemeContext = createLContext<{ theme: string }>();

const Consumer = lmount(() => {
  const { theme } = ThemeContext.useContext();
  return () => <p>{theme}</p>;
});
```

## Portal

```tsx
import { mount, portal } from 'lithent';

const Modal = mount((renew, props: { onClose: () => void }) => {
  return () => portal(
    <div class="modal-overlay" onClick={props.onClose}>
      <div class="modal-content" onClick={(e) => e.stopPropagation()}>
        <h2>Modal</h2>
        <button onClick={props.onClose}>Close</button>
      </div>
    </div>,
    document.body
  );
});
```

## List Rendering

Always use `key` prop for lists:

```tsx
import { mount } from 'lithent';
import { state } from 'lithent/helper';

const TodoList = mount((renew) => {
  const todos = state([
    { id: 1, text: 'Learn Lithent', done: false },
    { id: 2, text: 'Build app', done: false },
  ], renew);

  const toggle = (id: number) => {
    todos.value = todos.value.map(t =>
      t.id === id ? { ...t, done: !t.done } : t
    );
  };

  return () => (
    <ul>
      {todos.value.map(todo => (
        <li key={todo.id} onClick={() => toggle(todo.id)}>
          {todo.text} {todo.done && '✓'}
        </li>
      ))}
    </ul>
  );
});
```

## SSR and Hydration

```tsx
// Server
import { renderToString } from 'lithent/ssr';
const html = renderToString(<App />);

// Client (hydrate existing DOM)
import { render } from 'lithent';
import { hydration } from 'lithent/ssr';
render(<App />, document.getElementById('app')!, hydration);
```

## FTags (No JSX)

```ts
import { fTags, fMount } from 'lithent/ftags';
import { state } from 'lithent/helper';

const { div, button, p } = fTags;

const Counter = fMount((renew) => {
  const count = state(0, renew);
  return () => div({},
    p({}, `Count: ${count.value}`),
    button({ onClick: () => count.value++ }, '+1')
  );
});
```

## HTM (Tagged Templates)

```ts
import { lTag } from 'lithent/tag';
import { mount } from 'lithent';
import { state } from 'lithent/helper';

const html = lTag;

const Counter = mount((renew) => {
  const count = state(0, renew);
  return () => html`
    <div>
      <p>Count: ${count.value}</p>
      <button onClick=${() => count.value++}>+1</button>
    </div>
  `;
});
```

## Performance

```tsx
import { cacheUpdate, nextTickRender } from 'lithent/helper';

// Batch multiple state updates into single render
cacheUpdate(() => {
  a.value = 1;
  b.value = 2;
  c.value = 3;
});

// Defer render to next tick
nextTickRender(() => {
  items.value = [...items.value, ...newItems];
});
```

## Children Handling

```tsx
import { mount } from 'lithent';
import { unwrapChildren } from 'lithent/helper';

const Card = mount((renew, props: { title: string }, children) => {
  return () => (
    <div class="card">
      <h3>{props.title}</h3>
      <div class="card-body">{unwrapChildren(children)}</div>
    </div>
  );
});

// Usage
<Card title="Title"><p>Content</p></Card>
```

## Import Reference

```tsx
// Core
import {
  mount, lmount, render, h, Fragment, portal,
  ref, nextTick, mountCallback, updateCallback, mountReadyCallback
} from 'lithent';

// Helper
import {
  state, lstate,                    // Reactive state
  computed, effect,                 // Derived values & side effects
  store, lstore,                    // Global state
  createContext, createLContext,   // Context API
  cacheUpdate, nextTickRender,     // Performance
  unwrapChildren                    // Utility
} from 'lithent/helper';

// SSR
import { renderToString, hydration } from 'lithent/ssr';

// FTags
import { fTags, fFragment, fMount } from 'lithent/ftags';

// HTM
import { lTag } from 'lithent/tag';
```

## Additional materials (optional)

- `constraints/` (rules, mistakes, troubleshooting)
- `reference/` (props types, children types, lstore inference)
- `examples/` (quick examples)
