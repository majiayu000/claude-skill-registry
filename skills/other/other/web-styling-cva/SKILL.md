---
name: web-styling-cva
description: Class Variance Authority - type-safe component variant styling with cva(), compound variants, and VariantProps
---

# CVA (Class Variance Authority) Patterns

> **Quick Guide:** Use CVA to define type-safe component variants with a declarative API. Define base classes, variant groups (size, intent, state), compound variants for combined conditions, and default values. Extract types with `VariantProps`. Works with any CSS approach (utility classes, CSS modules, plain CSS).

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
- Defining reusable styling patterns across components
- Implementing compound conditions (e.g., "large primary" has special styles)
- Sharing component styling across projects or frameworks

**When NOT to use:**

- Simple components with no variants (just use plain classes)
- One-off styling without pattern reuse
- Dynamic styles based on runtime values (use inline styles or CSS variables)
- Responsive styles that change based on viewport (use CSS media queries)

**Key patterns covered:**

- Basic variant definitions with `cva()`
- Multiple variant groups (size, intent, disabled)
- Boolean variants for toggle states
- Compound variants for combined conditions
- Default variants for initial state
- Type extraction with `VariantProps`
- Class merging with `cx()` and external utilities
- Multi-part component patterns
- Extending and composing variant definitions

**Detailed Resources:**

- For code examples:
  - [variants.md](examples/variants.md) - Basic variants, boolean states, default values
  - [compound-variants.md](examples/compound-variants.md) - Multi-condition styles and combinations
  - [composition.md](examples/composition.md) - VariantProps, class merging, component integration
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

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
// ❌ Manual approach: scattered logic, no type safety
function getButtonClasses(size: string, variant: string, disabled: boolean) {
  let classes = "btn";
  if (size === "sm") classes += " btn-sm";
  else if (size === "lg") classes += " btn-lg";
  if (variant === "primary") classes += " btn-primary";
  if (disabled) classes += " btn-disabled";
  return classes;
}

// ✅ CVA approach: declarative, type-safe, composable
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

Define component styles with base classes and variant options using `cva()`.

#### Basic Structure

```typescript
import { cva } from "class-variance-authority";

// ✅ Good Example - Clear variant structure
const buttonVariants = cva(
  // Base classes applied to all variants
  ["font-semibold", "border", "rounded", "transition-colors"],
  {
    variants: {
      intent: {
        primary: ["bg-blue-600", "text-white", "border-transparent"],
        secondary: ["bg-white", "text-gray-800", "border-gray-400"],
        danger: ["bg-red-600", "text-white", "border-transparent"],
      },
      size: {
        sm: ["text-sm", "py-1", "px-2"],
        md: ["text-base", "py-2", "px-4"],
        lg: ["text-lg", "py-3", "px-6"],
      },
    },
    defaultVariants: {
      intent: "primary",
      size: "md",
    },
  },
);

// Usage
buttonVariants(); // Uses defaults: primary + md
buttonVariants({ intent: "secondary" }); // secondary + md (size from default)
buttonVariants({ intent: "danger", size: "lg" }); // danger + lg
```

**Why good:** base classes shared across all variants, variant options are explicit and discoverable, defaultVariants ensure consistent initial state, TypeScript infers valid options

```typescript
// ❌ Bad Example - Missing defaults, magic strings
const buttonVariants = cva("font-semibold border rounded", {
  variants: {
    intent: {
      primary: "bg-blue-600 text-white",
      secondary: "bg-white text-gray-800",
    },
  },
  // No defaultVariants - relies on undefined behavior
});

// Caller must always specify intent or get empty classes
buttonVariants(); // No intent classes applied!
```

**Why bad:** no defaultVariants means caller must always specify all variants, string classes harder to read than arrays, missing variants return empty strings causing broken styling

---

### Pattern 2: Boolean Variants for Toggle States

Use boolean variants for binary states like disabled, loading, or active.

#### Boolean Keys

```typescript
import { cva } from "class-variance-authority";

// ✅ Good Example - Boolean variant with true/false keys
const inputVariants = cva(
  ["border", "rounded", "px-3", "py-2", "transition-colors"],
  {
    variants: {
      size: {
        sm: ["text-sm", "h-8"],
        md: ["text-base", "h-10"],
        lg: ["text-lg", "h-12"],
      },
      disabled: {
        false: ["bg-white", "cursor-text"],
        true: ["bg-gray-100", "cursor-not-allowed", "opacity-60"],
      },
      error: {
        false: ["border-gray-300", "focus:border-blue-500"],
        true: ["border-red-500", "focus:border-red-600"],
      },
    },
    defaultVariants: {
      size: "md",
      disabled: false,
      error: false,
    },
  },
);

// Usage
inputVariants({ disabled: true }); // disabled styles
inputVariants({ error: true, disabled: false }); // error state, enabled
```

**Why good:** boolean variants handle binary states cleanly, `false` case provides base styles instead of relying on absence, explicit defaults prevent undefined behavior

```typescript
// ❌ Bad Example - Only defining true case
const inputVariants = cva("border rounded px-3 py-2", {
  variants: {
    disabled: {
      true: "bg-gray-100 cursor-not-allowed opacity-60",
      // Missing false case - normal styles not applied
    },
  },
});
```

**Why bad:** missing `false` case means no styles applied when not disabled, must handle enabled state elsewhere, variant logic is incomplete

---

### Pattern 3: Compound Variants for Combined Conditions

Use `compoundVariants` when specific variant combinations need additional or different styles.

#### Compound Configuration

```typescript
import { cva } from "class-variance-authority";

// ✅ Good Example - Compound variants for special combinations
const buttonVariants = cva(
  ["font-semibold", "border", "rounded", "transition-colors"],
  {
    variants: {
      intent: {
        primary: ["bg-blue-600", "text-white", "border-transparent"],
        secondary: ["bg-white", "text-gray-800", "border-gray-400"],
      },
      size: {
        sm: ["text-sm", "py-1", "px-2"],
        lg: ["text-lg", "py-3", "px-6"],
      },
      disabled: {
        false: null,
        true: ["opacity-50", "cursor-not-allowed"],
      },
    },
    compoundVariants: [
      // Add hover styles only when NOT disabled
      {
        intent: "primary",
        disabled: false,
        class: ["hover:bg-blue-700"],
      },
      {
        intent: "secondary",
        disabled: false,
        class: ["hover:bg-gray-100"],
      },
      // Large primary gets uppercase
      {
        intent: "primary",
        size: "lg",
        class: ["uppercase", "tracking-wider"],
      },
    ],
    defaultVariants: {
      intent: "primary",
      size: "sm",
      disabled: false,
    },
  },
);
```

**Why good:** compound variants cleanly express "when X AND Y, also apply Z", hover states only added when enabled, special styling for specific combinations without nested conditionals

```typescript
// ❌ Bad Example - Nested ternaries instead of compoundVariants
const getButtonClasses = (intent: string, size: string, disabled: boolean) => {
  const base = "font-semibold border rounded";
  const intentClass = intent === "primary" ? "bg-blue-600" : "bg-white";
  const hoverClass = !disabled
    ? intent === "primary"
      ? "hover:bg-blue-700"
      : "hover:bg-gray-100"
    : "";
  const sizeClass = size === "lg" && intent === "primary" ? "uppercase" : "";
  return `${base} ${intentClass} ${hoverClass} ${sizeClass}`;
};
```

**Why bad:** complex nested ternaries are hard to read and maintain, no type safety, easy to miss edge cases, scattered logic across multiple conditionals

---

### Pattern 4: Array Syntax in Compound Variants

Match multiple variant values with array syntax for DRY compound definitions.

#### Array Matching

```typescript
import { cva } from "class-variance-authority";

// ✅ Good Example - Array syntax matches multiple values
const alertVariants = cva(["p-4", "rounded-lg", "border"], {
  variants: {
    intent: {
      info: ["bg-blue-50", "border-blue-200", "text-blue-800"],
      success: ["bg-green-50", "border-green-200", "text-green-800"],
      warning: ["bg-yellow-50", "border-yellow-200", "text-yellow-800"],
      error: ["bg-red-50", "border-red-200", "text-red-800"],
    },
    size: {
      sm: ["text-sm", "p-2"],
      md: ["text-base", "p-4"],
      lg: ["text-lg", "p-6"],
    },
  },
  compoundVariants: [
    // Array syntax: applies to BOTH info AND success intents
    {
      intent: ["info", "success"],
      size: "lg",
      class: ["shadow-lg"],
    },
    // Array syntax: applies to warning OR error when medium or large
    {
      intent: ["warning", "error"],
      size: ["md", "lg"],
      class: ["font-medium"],
    },
  ],
  defaultVariants: {
    intent: "info",
    size: "md",
  },
});
```

**Why good:** array syntax avoids duplicating compound variant rules, clear expression of "any of these values" matching, easier to maintain when adding similar styles to multiple variants

---

### Pattern 5: Type Extraction with VariantProps

Use `VariantProps` to extract TypeScript types from variant definitions for component props.

#### Type Inference

```typescript
import { cva, type VariantProps } from "class-variance-authority";

// Define variants
const cardVariants = cva(["rounded-lg", "border", "p-4"], {
  variants: {
    elevation: {
      flat: ["shadow-none"],
      raised: ["shadow-md"],
      floating: ["shadow-xl"],
    },
    padding: {
      none: ["p-0"],
      sm: ["p-2"],
      md: ["p-4"],
      lg: ["p-8"],
    },
  },
  defaultVariants: {
    elevation: "flat",
    padding: "md",
  },
});

// ✅ Good Example - Extract types from cva definition
type CardVariants = VariantProps<typeof cardVariants>;
// { elevation?: "flat" | "raised" | "floating" | null; padding?: "none" | "sm" | "md" | "lg" | null }

// Use in component props (framework-agnostic example)
interface CardProps extends CardVariants {
  children: unknown;
  className?: string;
}

// Component implementation accesses typed variants
function createCardClasses(props: CardProps): string {
  const { elevation, padding, className } = props;
  return (
    cardVariants({ elevation, padding }) + (className ? ` ${className}` : "")
  );
}
```

**Why good:** VariantProps extracts exact types from cva definition, props always match available variants, IDE autocomplete works perfectly, invalid variant values caught at compile time

```typescript
// ❌ Bad Example - Manually defining variant types
type CardVariants = {
  elevation?: "flat" | "raised" | "floating";
  padding?: "none" | "sm" | "md" | "lg";
};

// Later add "xl" padding to cva but forget to update CardVariants type
const cardVariants = cva("rounded-lg border p-4", {
  variants: {
    padding: {
      none: "p-0",
      sm: "p-2",
      md: "p-4",
      lg: "p-8",
      xl: "p-12", // Added here but not in CardVariants!
    },
  },
});
```

**Why bad:** manual types drift from actual cva definition, "xl" padding exists but TypeScript doesn't know about it, defeats the purpose of type-safe variants

---

### Pattern 6: Required Variants with TypeScript

Enforce required variants (no defaults) using TypeScript utility types.

#### Required Props Pattern

```typescript
import { cva, type VariantProps } from "class-variance-authority";

// Variants without defaults
const badgeVariants = cva(
  ["inline-flex", "items-center", "rounded-full", "font-medium"],
  {
    variants: {
      color: {
        gray: ["bg-gray-100", "text-gray-800"],
        red: ["bg-red-100", "text-red-800"],
        green: ["bg-green-100", "text-green-800"],
        blue: ["bg-blue-100", "text-blue-800"],
      },
      size: {
        sm: ["text-xs", "px-2", "py-0.5"],
        md: ["text-sm", "px-2.5", "py-0.5"],
        lg: ["text-base", "px-3", "py-1"],
      },
    },
    // No defaultVariants - variants are required
  },
);

// ✅ Good Example - Make specific variants required
type BadgeVariantProps = VariantProps<typeof badgeVariants>;

// Color is required, size has a default
type BadgeProps = Omit<BadgeVariantProps, "color"> &
  Required<Pick<BadgeVariantProps, "color">> & {
    children: unknown;
  };

// Usage helper that enforces required variant
function createBadgeClasses(props: BadgeProps): string {
  const { color, size = "md" } = props; // size defaults in usage
  return badgeVariants({ color, size });
}

// Compile error if color not provided
// createBadgeClasses({ children: "Test" }); // Error: color is required
createBadgeClasses({ color: "green", children: "Test" }); // OK
```

**Why good:** TypeScript enforces that caller must provide color, size can still have a sensible default in usage code, VariantProps gives optional types that we make required selectively

---

### Pattern 7: Class Merging with cx() and Utilities

Use `cx()` for class concatenation and external utilities for conflict resolution.

#### Built-in cx() Function

```typescript
import { cva, cx } from "class-variance-authority";

const buttonVariants = cva(["font-semibold", "rounded"], {
  variants: {
    intent: {
      primary: ["bg-blue-600", "text-white"],
      secondary: ["bg-white", "text-gray-800"],
    },
  },
  defaultVariants: {
    intent: "primary",
  },
});

// ✅ Good Example - Combine with cx()
function getButtonClasses(
  variants: VariantProps<typeof buttonVariants>,
  additionalClasses?: string,
  conditionalClasses?: Record<string, boolean>,
): string {
  return cx(buttonVariants(variants), additionalClasses, conditionalClasses);
}

// Usage
getButtonClasses({ intent: "primary" }, "custom-class", { "is-loading": true });
// "font-semibold rounded bg-blue-600 text-white custom-class is-loading"
```

**Why good:** cx() handles class concatenation cleanly, supports conditional class objects, avoids manual string concatenation

#### Conflict Resolution with External Utilities

```typescript
import { cva, type VariantProps } from "class-variance-authority";
// Example with a class-merging utility (e.g., clsx + tailwind-merge wrapper)
import { cn } from "./utils"; // Your utility that merges and dedupes

const buttonVariants = cva(["px-4", "py-2", "rounded"], {
  variants: {
    size: {
      sm: ["px-2", "py-1", "text-sm"],
      lg: ["px-6", "py-3", "text-lg"],
    },
  },
  defaultVariants: {
    size: "sm",
  },
});

// ✅ Good Example - Wrapper for conflict resolution
function button(
  variants: VariantProps<typeof buttonVariants>,
  className?: string,
): string {
  return cn(buttonVariants(variants), className);
}

// When caller passes "px-8", cn() resolves conflict with variant's px
button({ size: "sm" }, "px-8"); // "py-1 text-sm rounded px-8" (px-8 wins)
```

**Why good:** external className prop can override variant styles cleanly, cn() utility handles class conflicts, caller has escape hatch for customization

---

### Pattern 8: Multi-Part Component Patterns

Define variants for components with multiple styled parts (e.g., input with label and helper text).

#### Multiple CVA Definitions

```typescript
import { cva, type VariantProps } from "class-variance-authority";

// ✅ Good Example - Separate cva for each part
const formFieldVariants = {
  label: cva(["block", "font-medium"], {
    variants: {
      size: {
        sm: ["text-sm", "mb-1"],
        md: ["text-base", "mb-1.5"],
        lg: ["text-lg", "mb-2"],
      },
      required: {
        false: null,
        true: ["after:content-['*']", "after:ml-0.5", "after:text-red-500"],
      },
    },
    defaultVariants: {
      size: "md",
      required: false,
    },
  }),

  input: cva(["w-full", "border", "rounded", "transition-colors"], {
    variants: {
      size: {
        sm: ["text-sm", "px-2", "py-1"],
        md: ["text-base", "px-3", "py-2"],
        lg: ["text-lg", "px-4", "py-3"],
      },
      error: {
        false: ["border-gray-300", "focus:border-blue-500"],
        true: ["border-red-500", "focus:border-red-600"],
      },
    },
    defaultVariants: {
      size: "md",
      error: false,
    },
  }),

  helper: cva(["mt-1"], {
    variants: {
      size: {
        sm: ["text-xs"],
        md: ["text-sm"],
        lg: ["text-base"],
      },
      error: {
        false: ["text-gray-500"],
        true: ["text-red-600"],
      },
    },
    defaultVariants: {
      size: "md",
      error: false,
    },
  }),
};

// Shared type for consistent sizing across parts
type FormFieldSize = NonNullable<
  VariantProps<typeof formFieldVariants.input>["size"]
>;

// Usage
function getFormFieldClasses(
  size: FormFieldSize,
  hasError: boolean,
  isRequired: boolean,
) {
  return {
    label: formFieldVariants.label({ size, required: isRequired }),
    input: formFieldVariants.input({ size, error: hasError }),
    helper: formFieldVariants.helper({ size, error: hasError }),
  };
}
```

**Why good:** each part has its own cva definition for clear separation, shared size values ensure visual consistency, error state propagates to input and helper but not label

---

### Pattern 9: Composing and Extending Variants

Extend base variants for specialized components using composition.

#### Composition with cx()

```typescript
import { cva, cx, type VariantProps } from "class-variance-authority";

// Base interactive element variants
const interactiveVariants = cva(
  [
    "transition-colors",
    "focus:outline-none",
    "focus:ring-2",
    "focus:ring-offset-2",
  ],
  {
    variants: {
      focusRing: {
        blue: ["focus:ring-blue-500"],
        green: ["focus:ring-green-500"],
        red: ["focus:ring-red-500"],
      },
    },
    defaultVariants: {
      focusRing: "blue",
    },
  },
);

// Button extends interactive with its own variants
const buttonVariants = cva(["font-semibold", "rounded"], {
  variants: {
    intent: {
      primary: ["bg-blue-600", "text-white"],
      secondary: ["bg-gray-200", "text-gray-800"],
    },
    size: {
      sm: ["text-sm", "px-2", "py-1"],
      md: ["text-base", "px-4", "py-2"],
    },
  },
  defaultVariants: {
    intent: "primary",
    size: "md",
  },
});

// ✅ Good Example - Compose with cx()
type ButtonProps = VariantProps<typeof buttonVariants> &
  VariantProps<typeof interactiveVariants>;

function button(props: ButtonProps): string {
  const { intent, size, focusRing } = props;
  return cx(
    interactiveVariants({ focusRing }),
    buttonVariants({ intent, size }),
  );
}

// Usage
button({ intent: "primary", size: "md", focusRing: "blue" });
```

**Why good:** base styles shared via composition, specialized component adds its own variants, cx() combines classes from multiple cva instances

---

### Pattern 10: Responsive Variant Patterns

Handle responsive styling by combining CVA with CSS or passing breakpoint-aware values.

#### CSS-Based Responsiveness

```typescript
import { cva } from "class-variance-authority";

// ✅ Good Example - Responsive classes in variants (utility-class approach)
const containerVariants = cva(["w-full", "mx-auto", "px-4"], {
  variants: {
    maxWidth: {
      sm: ["max-w-screen-sm"],
      md: ["max-w-screen-md"],
      lg: ["max-w-screen-lg"],
      xl: ["max-w-screen-xl"],
      full: ["max-w-full"],
    },
    // Responsive padding using utility classes
    padding: {
      none: ["px-0"],
      sm: ["px-2", "sm:px-4"],
      md: ["px-4", "sm:px-6", "lg:px-8"],
      lg: ["px-6", "sm:px-8", "lg:px-12"],
    },
  },
  defaultVariants: {
    maxWidth: "lg",
    padding: "md",
  },
});
```

**Why good:** responsive breakpoint classes defined in variant values, single variant prop controls all breakpoint styles, CSS handles actual responsive behavior

#### Runtime Responsive Values

```typescript
import { cva, type VariantProps } from "class-variance-authority";

// For dynamic responsive behavior, accept breakpoint-aware props
type ResponsiveValue<T> = T | { base: T; sm?: T; md?: T; lg?: T };

const textVariants = cva([], {
  variants: {
    size: {
      sm: ["text-sm"],
      md: ["text-base"],
      lg: ["text-lg"],
      xl: ["text-xl"],
    },
  },
  defaultVariants: {
    size: "md",
  },
});

type TextSize = NonNullable<VariantProps<typeof textVariants>["size"]>;

// ✅ Helper to resolve responsive value to classes
function getResponsiveTextClasses(size: ResponsiveValue<TextSize>): string {
  if (typeof size === "string") {
    return textVariants({ size });
  }

  // Build responsive class string
  const classes: string[] = [];
  if (size.base) classes.push(textVariants({ size: size.base }));
  if (size.sm) classes.push(`sm:${textVariants({ size: size.sm }).trim()}`);
  if (size.md) classes.push(`md:${textVariants({ size: size.md }).trim()}`);
  if (size.lg) classes.push(`lg:${textVariants({ size: size.lg }).trim()}`);
  return classes.join(" ");
}

// Usage
getResponsiveTextClasses("lg"); // "text-lg"
getResponsiveTextClasses({ base: "sm", md: "lg" }); // "text-sm md:text-lg"
```

**Why good:** accepts either simple value or responsive object, helper generates appropriate breakpoint-prefixed classes, keeps cva definition simple while enabling responsive behavior

</patterns>

---

<integration>

## Integration Guide

**CVA is a standalone class generation utility.** It generates class strings from variant configurations. How you use those classes depends on your UI framework and CSS approach.

**Integration points:**

- **UI Frameworks:** Pass generated classes to your framework's className/class prop
- **CSS approaches:** CVA works with utility classes, CSS modules, BEM classes, or any class naming convention
- **Class utilities:** Combine with clsx, classnames, or tailwind-merge for conditional classes and conflict resolution
- **Type systems:** Use `VariantProps` to integrate with your component prop types

**CVA generates classes only.** For actual styling, component structure, or framework-specific patterns, use the appropriate skill.

</integration>

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
