---
name: react-to-solid
description: Core transformation engine for React-to-SolidJS conversion. Contains React-to-SolidJS mapping tables, Base UI to Kobalte/Corvu mapping, and third-party dependency mapping. Provides transformation rules as reusable context.
---

# React-to-SolidJS Transformation Rules

Single source of truth for all React-to-SolidJS transformations in the Zaidan project. This is a KNOWLEDGE skill -- it provides transformation rules as reusable context. Agents reference these tables when converting React components to SolidJS equivalents.

**IMPORTANT**: This skill is a **knowledge resource**. It does NOT perform transformations itself. Instead, it provides the necessary rules and mappings that other transformation agents will reference when executing conversions. If user call it manually, explain what this skill covers and redirect user to the agents that will use this skill, then stop. 

## React-to-SolidJS Transformation Rules

| Aspect | React (shadcn) | SolidJS (Zaidan) |
|---|---|---|
| Class attribute | `className` | `class` |
| Class prop type | `className?: string` | `class?: string` |
| Props destructuring | `{ className, ...props }` | `splitProps(props, ["class"])` |
| Spread props | `{...props}` | `{...others}` after splitProps |
| Default props | Destructure defaults `{ x = 5 }` | `mergeProps({ x: 5 }, props)` |
| Conditional rendering | `{condition && <El />}` | `<Show when={condition}><El /></Show>` |
| List rendering | `{items.map(x => ...)}` | `<For each={items}>{x => ...}</For>` |
| Primitive library | `@base-ui/react-*` | `@kobalte/core/*` |
| Polymorphic | `asChild` prop | `as` prop with `PolymorphicProps` |
| Refs | `forwardRef` wrapper | Remove (not needed in SolidJS) |
| Children type | `React.ReactNode` | `JSX.Element` |
| Component type | `React.ComponentProps<"div">` | `ComponentProps<"div">` |
| Event target | `e.target.value` | `e.currentTarget.value` |
| Utils import | `@/registry/bases/base/lib/utils` | `@/lib/utils` |

### Import Transformations

```tsx
// REMOVE (React):
import * as React from "react"
import { Slot } from "base-ui"
import * as DialogPrimitive from "@base-ui/react/dialog"
import { cn } from "@/registry/bases/base/lib/utils"

// ADD (SolidJS):
import type { ComponentProps, JSX, ValidComponent } from "solid-js"
import { splitProps, mergeProps, Show, For } from "solid-js"
import * as DialogPrimitive from "@kobalte/core/dialog"
import type { PolymorphicProps } from "@kobalte/core/polymorphic"
import { cn } from "@/lib/utils"
```

## Advanced Transformation Patterns

### Component Part Patterns WITHOUT Kobalte/Corvu Primitive

When a component part does NOT use a Kobalte or Corvu primitive, use this pattern:

```tsx
type ComponentPartProps = ComponentProps<"<html_element>">

const ComponentPart = (props: ComponentPartProps) => {
  const mergedProps = mergeProps({ aProp: "default" } as ComponentPartProps, props);
  const [local, others] = splitProps(mergedProps, ["aProp"]);
  return <html_element aProp={local.aProp} {...others} />;
}
```

### Component Part Patterns WITH Kobalte/Corvu Primitive

When a component part uses a Kobalte or Corvu primitive, use polymorphic typing:

```tsx
import * as Primitive from "@kobalte/core/primitive";

type ComponentPartProps<T extends ValidComponent = "<html_element>"> =
  PolymorphicProps<T, Primitive.PrimitivePartProps<T>> &
  Pick<ComponentProps<"<html_element>">, "aProp">;

const ComponentPart = <T extends ValidComponent = "<html_element>">(
  props: ComponentPartProps<T>
) => {
  const mergedProps = mergeProps(
    { aProp: "default" } as ComponentPartProps<T>,
    props as ComponentPartProps<T>
  );
  const [local, others] = splitProps(mergedProps, ["aProp"]);
  return <Primitive.Root aProp={local.aProp} {...others} />;
}
```

### Reading Kobalte Documentation

When consulting Kobalte docs at `https://kobalte.dev/docs/core/components/<component-name>`:

- **Anatomy Section**: Lists all `ComponentPart` elements and how to combine them
- **Rendered Elements Section**: Check the "Default rendered element" column:
  - If starts with a capital letter -> no primitive used (e.g., a Kobalte sub-component)
  - If `none` -> no primitive used (wrapper/context provider)
  - Otherwise -> native HTML element (e.g., `div`, `button`, `h3`)
- **API Reference**: Props, data attributes, CSS variables for each part
- **CSS Variables**: Kobalte prefixes with `--kb-` (e.g., `--kb-accordion-content-height`)

### Reading Corvu Documentation

When consulting Corvu docs at `https://corvu.dev/docs/primitives/<component-name>`:

- **Anatomy Section**: Lists all `ComponentPart` elements with combination patterns
- **API Reference Section**: Rendered elements are specified in the Props table, under the `as` row
- **DynamicProps**: Corvu uses `DynamicProps` instead of Kobalte's `PolymorphicProps`
- **CSS Variables**: Corvu prefixes with `--corvu-` (e.g., `--corvu-disclosure-content-height`)
- **Data Attributes**: Corvu prefixes with `data-corvu-` (e.g., `data-corvu-accordion-trigger`)
- **Context Hooks**: `useContext()` and `useItemContext()` for accessing component state

## Documentation Resources

### Kobalte Core Components
- **URL Pattern**: `https://kobalte.dev/docs/core/components/<component-name>`
- **Content**: Anatomy, Rendered elements, API Reference, Props, Data Attributes, CSS Variables
- For detailed patterns, see [docs/kobalte-patterns.md](docs/kobalte-patterns.md)

### Corvu Primitives
- **URL Pattern**: `https://corvu.dev/docs/primitives/<component-name>`
- **Content**: Anatomy, API Reference with rendered elements in Props table
- For detailed patterns, see [docs/corvu-patterns.md](docs/corvu-patterns.md)

### Shadcn Registry
- **Components**: `https://raw.githubusercontent.com/shadcn-ui/ui/refs/heads/main/apps/v4/registry/bases/base/ui/<component-name>.tsx`
- **Examples**: `https://raw.githubusercontent.com/shadcn-ui/ui/refs/heads/main/apps/v4/registry/bases/base/examples/<component-name>-example.tsx`
- **Docs**: `https://raw.githubusercontent.com/shadcn-ui/ui/refs/heads/main/apps/v4/content/docs/components/<component-name>.mdx`
- **Schema**: `https://ui.shadcn.com/schema/registry.json`

## Supporting Documentation

- [docs/kobalte-patterns.md](docs/kobalte-patterns.md) -- Kobalte anatomy, rendered elements, props, data attributes, CSS variables
- [docs/corvu-patterns.md](docs/corvu-patterns.md) -- Corvu anatomy, API patterns, DynamicProps, context hooks
- [docs/base-ui-mapping.md](docs/base-ui-mapping.md) -- Complete Base UI to Kobalte/Corvu mapping reference
- [docs/third-party-deps.md](docs/third-party-deps.md) -- Detailed third-party React-to-SolidJS dependency mapping
