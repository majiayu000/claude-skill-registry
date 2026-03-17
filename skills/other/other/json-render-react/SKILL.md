---
name: json-render-react
description: React renderer for json-render that turns JSON specs into React components. Use when working with @json-render/react, building React UIs from JSON, creating component catalogs, or rendering AI-generated specs.
---

# @json-render/react

React renderer that converts JSON specs into React component trees.

## Quick Start

```typescript
import { defineRegistry, Renderer } from "@json-render/react";
import { catalog } from "./catalog";

const { registry } = defineRegistry(catalog, {
  components: {
    Card: ({ props, children }) => <div>{props.title}{children}</div>,
  },
});

function App({ spec }) {
  return <Renderer spec={spec} registry={registry} />;
}
```

## Creating a Catalog

```typescript
import { defineCatalog } from "@json-render/core";
import { schema, defineRegistry } from "@json-render/react";
import { z } from "zod";

// Create catalog with props schemas
export const catalog = defineCatalog(schema, {
  components: {
    Button: {
      props: z.object({
        label: z.string(),
        variant: z.enum(["primary", "secondary"]).nullable(),
      }),
      description: "Clickable button",
    },
    Card: {
      props: z.object({ title: z.string() }),
      description: "Card container with title",
    },
  },
});

// Define component implementations with type-safe props
const { registry } = defineRegistry(catalog, {
  components: {
    Button: ({ props }) => (
      <button className={props.variant}>{props.label}</button>
    ),
    Card: ({ props, children }) => (
      <div className="card">
        <h2>{props.title}</h2>
        {children}
      </div>
    ),
  },
});
```

## Spec Structure (Element Tree)

The React schema uses an element tree format:

```json
{
  "root": {
    "type": "Card",
    "props": { "title": "Hello" },
    "children": [
      { "type": "Button", "props": { "label": "Click me" } }
    ]
  }
}
```

## Providers

| Provider | Purpose |
|----------|---------|
| `StateProvider` | Share state across components (JSON Pointer paths) |
| `ActionProvider` | Handle actions dispatched via the event system |
| `VisibilityProvider` | Enable conditional rendering based on state |
| `ValidationProvider` | Form field validation |

## Dynamic Prop Expressions

Any prop value can be a data-driven expression resolved by the renderer before components receive props:

- **`{ "$path": "/state/key" }`** - reads from data model
- **`{ "$cond": <condition>, "$then": <value>, "$else": <value> }`** - conditional value

```json
{
  "color": {
    "$cond": { "eq": [{ "path": "/status" }, "active"] },
    "$then": "green",
    "$else": "gray"
  }
}
```

Components receive already-resolved props. No changes needed to component implementations.

## Event System

Components use `emit` to fire named events. The element's `on` field maps events to action bindings:

```tsx
// Component emits a named event
Button: ({ props, emit }) => (
  <button onClick={() => emit?.("press")}>{props.label}</button>
),
```

```json
{
  "type": "Button",
  "props": { "label": "Submit" },
  "on": { "press": { "action": "submit" } }
}
```

## Built-in Actions

The `setState` action is handled automatically by `ActionProvider` and updates the state model directly, which re-evaluates visibility conditions and dynamic prop expressions:

```json
{ "action": "setState", "actionParams": { "path": "/activeTab", "value": "home" } }
```

## Key Exports

| Export | Purpose |
|--------|---------|
| `defineRegistry` | Create a type-safe component registry from a catalog |
| `Renderer` | Render a spec using a registry |
| `schema` | Element tree schema |
| `useStateStore` | Access state context |
| `useStateValue` | Get single value from state |
| `useStateBinding` | Two-way state binding |
| `useActions` | Access actions context |
| `useAction` | Get a single action dispatch function |
| `useUIStream` | Stream specs from an API endpoint |
