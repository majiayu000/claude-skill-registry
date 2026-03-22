---
name: web-styling-cva
description: Class Variance Authority - type-safe component variant styling with cva(), compound variants, and VariantProps
---

# CVA (Class Variance Authority) Patterns

> **Quick Guide:** Use CVA to define type-safe component variants with a declarative API. Define base classes, variant groups (size, intent, state), compound variants for combined conditions, and default values. Extract types with `VariantProps`. Works with any CSS approach (utility classes, CSS modules, plain CSS). Always set `defaultVariants`, always define both `true`/`false` for boolean variants, always use `VariantProps` for type extraction.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST define all variant options in the `variants` object - NEVER use conditional class logic outside cva)**

**(You MUST use `VariantProps` to extract types - NEVER manually define variant prop types)**

**(You MUST use `defaultVariants` for initial state - NEVER rely on undefined props for defaults)**

**(You MUST use `compoundVariants` for multi-condition styles - NEVER nest ternaries for combined states)**

</critical_requirements>

---

**Auto-detection:** cva, class-variance-authority, VariantProps, variants, compoundVariants, defaultVariants, component variants, type-safe styling, cx

**When to use:**

- Building components with multiple visual variants (size, intent, state)
- Creating design system components with type-safe props
- Implementing compound conditions (e.g., "large primary" has special styles)
- Sharing variant styling across projects or frameworks

**When NOT to use:**

- Simple components with no variants (just use plain classes)
- One-off styling without pattern reuse
- Dynamic styles based on runtime values (use inline styles or CSS variables)
- Responsive styles that change based on viewport (use CSS media queries)

**Key patterns covered:**

- Basic variant definitions with `cva()`
- Boolean variants for toggle states
- Compound variants for combined conditions
- Type extraction with `VariantProps`
- Class merging with `cx()` and external utilities
- Multi-part component patterns
- Composing and extending variant definitions

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Basic variants, boolean states, default values, required variants
- [examples/compound-variants.md](examples/compound-variants.md) - Multi-condition styles, array syntax, state combinations
- [examples/composition.md](examples/composition.md) - VariantProps, class merging, multi-part components, extending variants
- [reference.md](reference.md) - Decision frameworks, anti-patterns, quick reference

---

<philosophy>

## Philosophy

CVA treats component variants as a **type system for UI states**. Instead of scattering conditional class logic throughout components, CVA centralizes variant definitions in a single, typed configuration object.

**Core Principles:**

- **Declarative over imperative:** Define what each variant looks like, not how to compute classes
- **Type-safe variants:** TypeScript catches invalid variant values at compile time
- **Framework-agnostic:** Works with any UI framework and any CSS approach
- **Composition-friendly:** Variants can be combined, extended, and composed
- **Single source of truth:** Variant definitions live in one place, types are derived

**Why CVA over manual conditional classes:**

```typescript
// BAD: scattered logic, no type safety, hard to maintain
function getButtonClasses(size: string, variant: string, disabled: boolean) {
  let classes = "btn";
  if (size === "sm") classes += " btn-sm";
  else if (size === "lg") classes += " btn-lg";
  if (variant === "primary") classes += " btn-primary";
  if (disabled) classes += " btn-disabled";
  return classes;
}

// GOOD: declarative, type-safe, composable
const buttonVariants = cva("btn", {
  variants: {
    size: { sm: "btn-sm", lg: "btn-lg" },
    variant: { primary: "btn-primary" },
    disabled: { true: "btn-disabled" },
  },
});
```

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Basic Variant Definition

Define component styles with base classes and variant options. Use array syntax for readability, always set `defaultVariants`.

```typescript
import { cva } from "class-variance-authority";

const buttonVariants = cva(
  ["font-semibold", "border", "rounded"], // base classes as array
  {
    variants: {
      intent: {
        primary: ["bg-blue-600", "text-white"],
        secondary: ["bg-white", "text-gray-800"],
      },
      size: {
        sm: ["text-sm", "py-1", "px-2"],
        md: ["text-base", "py-2", "px-4"],
      },
    },
    defaultVariants: {
      intent: "primary",
      size: "md",
    },
  },
);

buttonVariants(); // defaults: primary + md
buttonVariants({ intent: "secondary" }); // secondary + md
```

**Key rules:** always provide `defaultVariants` (calling without props returns incomplete classes otherwise), use arrays over space-separated strings for readability.

> See [examples/core.md](examples/core.md) for complete button, badge, and icon button examples.

---

### Pattern 2: Boolean Variants

Use `true`/`false` keys for binary states. Always define both sides.

```typescript
const inputVariants = cva(["border", "rounded", "px-3", "py-2"], {
  variants: {
    disabled: {
      false: ["bg-white", "cursor-text"], // normal state
      true: ["bg-gray-100", "cursor-not-allowed"], // disabled state
    },
    error: {
      false: ["border-gray-300"],
      true: ["border-red-500"],
    },
  },
  defaultVariants: { disabled: false, error: false },
});
```

**Key rule:** missing `false` case means no styles applied in normal state -- variant logic becomes incomplete.

> See [examples/core.md](examples/core.md) for boolean variant patterns with loading, disabled, and error states.

---

### Pattern 3: Compound Variants

Use `compoundVariants` when specific variant combinations need special styles. Array syntax matches multiple values.

```typescript
const buttonVariants = cva(["font-semibold", "rounded"], {
  variants: {
    intent: {
      primary: ["bg-blue-600", "text-white"],
      secondary: ["bg-white", "text-gray-800"],
    },
    disabled: {
      false: null,
      true: ["opacity-50", "cursor-not-allowed"],
    },
  },
  compoundVariants: [
    // Hover only when enabled
    { intent: "primary", disabled: false, class: ["hover:bg-blue-700"] },
    { intent: "secondary", disabled: false, class: ["hover:bg-gray-100"] },
    // Array syntax: matches multiple values
    {
      intent: ["primary", "secondary"],
      disabled: true,
      class: ["pointer-events-none"],
    },
  ],
  defaultVariants: { intent: "primary", disabled: false },
});
```

**Key rules:** compound variants express "when X AND Y, also apply Z", array syntax avoids duplicating rules across similar variants.

> See [examples/compound-variants.md](examples/compound-variants.md) for hover states, loading overrides, state matrices, and multi-part compounds.

---

### Pattern 4: Type Extraction with VariantProps

Always use `VariantProps` to extract types from cva definitions -- never manually define variant types.

```typescript
import { cva, type VariantProps } from "class-variance-authority";

const cardVariants = cva(["rounded-lg", "border"], {
  variants: {
    elevation: { flat: ["shadow-none"], raised: ["shadow-md"] },
    padding: { none: ["p-0"], sm: ["p-2"], md: ["p-4"] },
  },
  defaultVariants: { elevation: "flat", padding: "md" },
});

// Extract types -- always in sync with cva definition
type CardVariants = VariantProps<typeof cardVariants>;
// { elevation?: "flat" | "raised" | null; padding?: "none" | "sm" | "md" | null }

interface CardProps extends CardVariants {
  children: unknown;
  className?: string;
}
```

**Key rule:** manual types drift when you add/remove variants. `VariantProps` is always in sync.

To make specific variants required (no default):

```typescript
type BadgeProps = Omit<BadgeVariants, "color"> &
  Required<Pick<BadgeVariants, "color">>;
```

> See [examples/composition.md](examples/composition.md) for complete type extraction and required variant patterns.

---

### Pattern 5: Class Merging with cx()

Use `cx()` (built-in, alias for clsx) for class concatenation. Use an external merge utility for class conflict resolution.

```typescript
import { cva, cx } from "class-variance-authority";

// cx() concatenates and filters falsy values
cx(buttonVariants({ intent: "primary" }), highlighted && "ring-2", className);

// For conflict resolution (e.g., caller overriding variant padding),
// use a class-merging utility wrapper
function button(variants: ButtonVariants, className?: string): string {
  return cn(buttonVariants(variants), className); // cn() resolves conflicts
}
```

> See [examples/composition.md](examples/composition.md) for class merging patterns and conflict resolution.

---

### Pattern 6: Multi-Part Components

Define separate cva for each styled part of a component (label, input, helper text). Share variant values for visual consistency.

```typescript
const formFieldVariants = {
  label: cva(["block", "font-medium"], {
    variants: { size: { sm: ["text-sm"], md: ["text-base"] } },
    defaultVariants: { size: "md" },
  }),
  input: cva(["w-full", "border", "rounded"], {
    variants: {
      size: { sm: ["text-sm", "px-2"], md: ["text-base", "px-3"] },
      error: { false: ["border-gray-300"], true: ["border-red-500"] },
    },
    defaultVariants: { size: "md", error: false },
  }),
  helper: cva(["mt-1"], {
    variants: {
      size: { sm: ["text-xs"], md: ["text-sm"] },
      error: { false: ["text-gray-500"], true: ["text-red-600"] },
    },
    defaultVariants: { size: "md", error: false },
  }),
};
```

> See [examples/composition.md](examples/composition.md) for multi-part and extending/composing variant patterns.

---

### Pattern 7: Composing and Extending Variants

Combine multiple cva definitions with `cx()` for shared base + specialized variants.

```typescript
const interactiveVariants = cva(["transition-colors", "focus:ring-2"], {
  variants: { focusRing: { blue: ["focus:ring-blue-500"] } },
  defaultVariants: { focusRing: "blue" },
});

const buttonVariants = cva(["font-semibold", "rounded"], {
  variants: { intent: { primary: ["bg-blue-600"] } },
  defaultVariants: { intent: "primary" },
});

// Compose with cx()
type ButtonProps = VariantProps<typeof interactiveVariants> &
  VariantProps<typeof buttonVariants>;

function button(props: ButtonProps): string {
  return cx(
    interactiveVariants({ focusRing: props.focusRing }),
    buttonVariants({ intent: props.intent }),
  );
}
```

> See [examples/composition.md](examples/composition.md) for composition and extension patterns.

</patterns>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- **Manual variant type definitions** -- Types drift from cva definition, defeating type safety. Always use `VariantProps<typeof variants>`.
- **Conditional class logic outside cva** -- Defeats purpose of centralized variant definitions. Add the condition as a variant.
- **Missing `defaultVariants`** -- Calling without props returns incomplete classes. Always set defaults.
- **Nested ternaries for combined states** -- Use `compoundVariants` instead.
- **Only defining `true` for boolean variants** -- `false` case should provide base/normal styles.

**Medium Priority Issues:**

- Space-separated class strings instead of arrays -- arrays are more readable and maintainable
- Not using `cx()` for class merging -- manual concatenation is error-prone
- Duplicating variant styles across components -- compose from shared base variants
- Putting complex responsive logic in cva -- keep cva simple, handle responsiveness in CSS

**Gotchas & Edge Cases:**

- `VariantProps` makes all variants optional (nullable) -- use TypeScript utilities (`Required<Pick<>>`) to make specific ones required
- `compoundVariants` are applied AFTER regular variants -- order matters for class specificity
- Empty variant values (`null` or empty string) are valid -- useful for "no additional styles" case
- Base classes are always applied -- you cannot conditionally remove them via variants
- Both `class` and `className` work in `compoundVariants` config -- pick one and be consistent (`class` in non-React contexts, `className` if you prefer React conventions)
- Don't forget `import type` for `VariantProps`: `import { cva, type VariantProps }`

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST define all variant options in the `variants` object - NEVER use conditional class logic outside cva)**

**(You MUST use `VariantProps` to extract types - NEVER manually define variant prop types)**

**(You MUST use `defaultVariants` for initial state - NEVER rely on undefined props for defaults)**

**(You MUST use `compoundVariants` for multi-condition styles - NEVER nest ternaries for combined states)**

**Failure to follow these rules will break type safety, create inconsistent styling, and defeat the purpose of using CVA.**

</critical_reminders>
