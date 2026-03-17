---
name: mitosis
description: |
    Use when writing cross-framework UI components with Mitosis (Builder.io). Write components once in a JSX subset, compile to React, Vue, Angular, Svelte, Solid, Qwik, and more.
    USE FOR: Mitosis component authoring, cross-framework component compilation, multi-framework design system components, Mitosis JSX syntax, mitosis.config.js
    DO NOT USE FOR: single-framework components (use the framework's own skill), design token management (use design-tokens or style-dictionary), component documentation (use storybook)
license: MIT
metadata:
  displayName: "Mitosis"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "Mitosis — GitHub Repository (Builder.io)"
    url: "https://github.com/BuilderIO/mitosis"
  - title: "Mitosis Documentation"
    url: "https://mitosis.builder.io/"
---

# Mitosis — Write Once, Compile Everywhere

## Overview
Mitosis (by Builder.io) is a compile-time framework that lets you write UI components in a static JSX subset, then compile them to React, Vue, Angular, Svelte, Solid, Qwik, React Native, Web Components, and more. It's the key intermediary format for design systems that need to ship components to multiple frameworks from a single source.

## How It Works
```
Mitosis JSX (.lite.tsx)
        │
        ▼
   ┌──────────┐
   │  Parse    │  JSX → Mitosis JSON (intermediate AST)
   └────┬─────┘
        ▼
   ┌──────────┐
   │ Compile   │  JSON → Target framework code
   └────┬─────┘
        ▼
React, Vue, Angular, Svelte, Solid, Qwik, Lit, Stencil, RN, ...
```

## Supported Targets
| Target | Output |
|--------|--------|
| React | `.tsx` with hooks |
| Vue (3) | `.vue` SFC with Composition API |
| Angular | `.component.ts` with decorators |
| Svelte | `.svelte` SFC |
| Solid | `.tsx` with signals |
| Qwik | `.tsx` with `$` closures |
| React Native | `.tsx` with RN primitives |
| Lit | `.ts` with LitElement |
| Stencil | `.tsx` Web Components |
| Web Components | Vanilla custom elements |
| Swift (beta) | SwiftUI views |

## Getting Started
```bash
# Create a new Mitosis project
npm create @builder.io/mitosis@latest

# Or add to an existing project
npm install @builder.io/mitosis-cli @builder.io/mitosis
```

## Component Syntax
Mitosis uses a **static subset of JSX** — no arbitrary JS expressions, hooks, or closures. This constraint enables reliable compilation to any target.

### Basic Component
```tsx
// Button.lite.tsx
import { useStore } from "@builder.io/mitosis";

export default function Button(props) {
  const state = useStore({
    count: 0,
  });

  return (
    <button
      class={`btn btn-${props.variant}`}
      onClick={() => (state.count = state.count + 1)}
    >
      {props.children} ({state.count})
    </button>
  );
}
```

### Props
Props are received as the function argument and accessed via `props.name`:
```tsx
export default function Avatar(props) {
  return (
    <img
      src={props.src}
      alt={props.alt}
      class={`avatar avatar-${props.size || "md"}`}
    />
  );
}
```

### State (`useStore`)
`useStore` creates a reactive state object. Mutate properties directly:
```tsx
const state = useStore({
  isOpen: false,
  items: [],
});

// Toggle
state.isOpen = !state.isOpen;

// Update array (replace, don't push)
state.items = [...state.items, newItem];
```

### Conditional Rendering
Use the `<Show>` component (not ternaries in JSX):
```tsx
import { Show } from "@builder.io/mitosis";

export default function Alert(props) {
  return (
    <Show when={props.visible}>
      <div class="alert">{props.message}</div>
    </Show>
  );
}
```

### Loops
Use the `<For>` component (not `.map()`):
```tsx
import { For } from "@builder.io/mitosis";

export default function List(props) {
  return (
    <ul>
      <For each={props.items}>
        {(item) => <li key={item.id}>{item.name}</li>}
      </For>
    </ul>
  );
}
```

### Event Handlers
Inline arrow functions only — no function references:
```tsx
<button onClick={() => (state.count = state.count + 1)}>+</button>
<input onInput={(event) => (state.query = event.target.value)} />
```

### Styles
Use the `<style>` JSX element or `css` prop:
```tsx
export default function Card(props) {
  return (
    <>
      <div class="card">{props.children}</div>
      <style>{`
        .card {
          padding: 1rem;
          border-radius: 8px;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
      `}</style>
    </>
  );
}
```

### Refs
```tsx
import { useRef } from "@builder.io/mitosis";

export default function Input(props) {
  const inputRef = useRef(null);

  function focusInput() {
    inputRef.focus();
  }

  return <input ref={inputRef} />;
}
```

## Intermediate JSON
Mitosis parses JSX into a framework-agnostic JSON AST:
```json
{
  "@type": "@builder.io/mitosis/component",
  "state": {
    "count": 0
  },
  "children": [
    {
      "@type": "@builder.io/mitosis/node",
      "name": "button",
      "bindings": {
        "onClick": "state.count = state.count + 1"
      },
      "children": [{ "@type": "@builder.io/mitosis/text", "text": "Click" }]
    }
  ]
}
```

This JSON is the intermediary format — custom compilers can consume it to generate output for any target.

## Configuration
```js
// mitosis.config.js
module.exports = {
  files: "src/**/*.lite.tsx",
  targets: ["react", "vue", "svelte", "angular"],
  dest: "output",
  options: {
    react: {
      typescript: true,
      stylesType: "style-tag",
    },
    vue: {
      api: "composition",
      typescript: true,
    },
    angular: {
      standalone: true,
    },
    svelte: {
      typescript: true,
    },
  },
};
```

## CLI Commands
```bash
# Compile all components to all targets
npx mitosis compile

# Compile to a specific target
npx mitosis compile --to=react

# Watch mode
npx mitosis compile --watch
```

## JSX Subset Rules
Mitosis enforces a static JSX subset for reliable cross-compilation:

| Allowed | Not Allowed |
|---------|-------------|
| `useStore` for state | React hooks (`useState`, `useEffect`) |
| `<Show when={}>` | Ternary in JSX (`{x ? a : b}`) |
| `<For each={}>` | `.map()` in JSX |
| Inline arrow event handlers | Function references as handlers |
| `props.name` access | Destructured props |
| Direct state mutation | Immutable update patterns |

## Figma Integration
Mitosis integrates with Figma to convert designs into `.lite.tsx` components:
- Import Figma frames as Mitosis components
- Map Figma variants to component props
- Keep design and code in sync

## Best Practices
- Use the `.lite.tsx` extension for Mitosis components to distinguish them from framework-specific files.
- Use `<Show>` and `<For>` instead of ternaries and `.map()` — these are the only control flow patterns that compile reliably to all targets.
- Keep state mutations simple — assign directly to `state.property`, avoid complex expressions.
- Use the Mitosis Playground (mitosis.builder.io/playground) to verify compilation output before committing.
- Configure per-target options in `mitosis.config.js` for framework-specific needs (TypeScript, composition API, standalone components).
- Pair with Style Dictionary to inject design tokens — Mitosis handles components, Style Dictionary handles tokens.
- Test the compiled output in each target framework's Storybook, not just the Mitosis source.
