---
name: web-styling-scss-modules
description: SCSS Modules, cva, design tokens
---

# Styling & Design System

> **Quick Guide:** Two-tier token system (Core primitives -> Semantic tokens). Foreground/background color pairs. Components use semantic tokens only. SCSS Modules + CSS Cascade Layers. HSL format. Dark mode via `.dark` class with mixin. Data-attributes for state. Self-contained (no external dependencies).

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST wrap ALL UI package component styles in `@layer components {}` for proper cascade precedence)**

**(You MUST use semantic tokens ONLY in components - NEVER use core tokens directly)**

**(You MUST use HSL format for colors with CSS color functions - NO Sass color functions like darken/lighten)**

**(You MUST use data-attributes for state styling - NOT className toggling)**

**(You MUST use `#### SubsectionName` markdown headers within patterns - NOT separator comments)**

**(You MUST use `@use` for imports - `@import` is deprecated and will be removed in Dart Sass 3.0.0)**

</critical_requirements>

---

**Auto-detection:** UI components, styling patterns, design tokens, SCSS modules, CSS Cascade Layers, dark mode theming

**When to use:**

- Implementing design tokens and theming
- Building component styles with SCSS Modules
- Ensuring visual consistency across applications
- Working with colors, spacing, typography
- Implementing dark mode with class-based theming
- Setting up CSS Cascade Layers for predictable style precedence

**Key patterns covered:**

- Two-tier token system (Core -> Semantic)
- SCSS Module patterns with CSS Cascade Layers
- Color system (HSL format, semantic naming, foreground/background pairs)
- Spacing and typography systems
- Dark mode implementation (`.dark` class with mixin pattern)
- Component structure and organization

**When NOT to use:**

- One-off prototypes without design system needs (use inline styles or basic CSS)
- External component libraries with their own theming (Material-UI, Chakra)
- Projects requiring comprehensive utility classes (use Tailwind CSS instead)

**Detailed Resources:**

- For code examples, see [examples/core.md](examples/core.md)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

The design system follows a **self-contained, two-tier token architecture** where core primitives (raw HSL values, base sizes) map to semantic tokens (purpose-driven names). Components consume only semantic tokens, enabling theme changes without component modifications.

**Core Principles:**

- **Self-contained:** No external dependencies (no Open Props, no Tailwind for tokens)
- **Two-tier system:** Core tokens provide raw values, semantic tokens provide meaning
- **HSL-first:** Use modern CSS color functions, not Sass color manipulation
- **Layer-based:** CSS Cascade Layers ensure predictable style precedence across monorepo
- **Theme-agnostic components:** Components use semantic tokens and adapt automatically to light/dark mode

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Two-Tier Token System

The design system uses a two-tier token architecture: **Tier 1 (Core tokens)** provides raw values, **Tier 2 (Semantic tokens)** references core tokens with purpose-driven names.

#### Token Architecture

**Location:** `packages/ui/src/styles/design-tokens.scss`

**Tier 1: Core tokens** - Raw HSL values, base sizes, primitives

```scss
--color-white: 0 0% 100%;
--color-gray-900: 222 47% 11%;
--color-red-500: 0 84% 60%;
--space-unit: 0.2rem;
```

**Tier 2: Semantic tokens** - Reference core tokens with purpose-driven names

```scss
--color-background-base: var(--color-white);
--color-text-default: var(--color-gray-500);
--color-primary: var(--color-gray-900);
--color-primary-foreground: var(--color-white);
--color-destructive: var(--color-red-500);
```

**Why this matters:** Semantic tokens make purpose clear (what the token is for), theme changes only update token values (not component code), components remain theme-agnostic.

For complete implementation examples, see [examples/core.md](examples/core.md#pattern-1-two-tier-token-system).

---

### Pattern 2: HSL Color Format with CSS Color Functions

Store HSL values without the `hsl()` wrapper in tokens, apply `hsl()` wrapper when using tokens, and use modern CSS color functions for transparency and color mixing.

#### Color Format Rules

- Store HSL values without `hsl()` wrapper: `--color-gray-900: 222 47% 11%;`
- Use `hsl()` wrapper when applying: `background-color: hsl(var(--color-primary))`
- Use CSS color functions for derived colors:
  - Transparency: `hsl(var(--color-primary) / 0.5)` (append alpha to HSL components)
  - Color mixing: `color-mix(in srgb, hsl(var(--color-primary)), white 10%)`
  - Channel manipulation: `hsl(from hsl(var(--color-primary)) h s calc(l * 0.8))` (wrap origin in `hsl()` first)
- **NEVER use Sass color functions:** No `darken()`, `lighten()`, `transparentize()`
- Always use semantic color tokens (not raw HSL in components)

**Why HSL:** HSL format eliminates Sass dependencies, CSS color functions work natively in browsers, semantic naming clarifies purpose (not just value), theme changes update token values without touching components.

For complete implementation examples, see [examples/core.md](examples/core.md#pattern-2-hsl-color-format-with-css-color-functions).

---

### Pattern 3: CSS Cascade Layers for Predictable Precedence

Use CSS Cascade Layers to control style precedence across the monorepo, ensuring UI package components have lower priority than app-specific overrides.

#### Layer Hierarchy (lowest -> highest priority)

1. `@layer reset` - Browser resets and normalizations
2. `@layer components` - Design system component styles (UI package)
3. Unlayered styles - App-specific overrides (highest priority)

#### Key Rules

- **UI package components:** Always wrap in `@layer components {}`
- **App-specific styles:** Never wrap in layers (unlayered = highest priority)
- **Layer declaration:** Import `layers.scss` first to declare layer order

**Why layers:** Wrapping in `@layer components {}` ensures app styles can override without specificity wars, loading order becomes irrelevant, predictable precedence across monorepo.

For complete implementation examples, see [examples/core.md](examples/core.md#pattern-3-css-cascade-layers-for-predictable-precedence).

---

### Pattern 4: Dark Mode with `.dark` Class and Mixin

Implement dark mode by adding `.dark` class to root element, which overrides semantic tokens. Use mixin pattern for organization.

#### Key Principles

- Components remain **theme-agnostic** (no theme logic in component code)
- Semantic tokens provide indirection between theme and components
- Only override **Tier 2 semantic tokens** in `.dark` class, never Tier 1 core tokens
- Theme switching is instant (just CSS variable changes)

For complete implementation examples, see [examples/theming.md](examples/theming.md#pattern-4-dark-mode-with-dark-class-and-mixin).

---

### Additional Patterns

The following patterns are documented with full examples in the examples/ folder:

- **Pattern 5:** SCSS Module Structure with Cascade Layers - [examples/patterns.md](examples/patterns.md#pattern-5-scss-module-structure-with-cascade-layers)
- **Pattern 6:** Spacing System with Semantic Tokens - [examples/tokens.md](examples/tokens.md#pattern-6-spacing-system-with-semantic-tokens)
- **Pattern 7:** Typography System with REM-Based Sizing - [examples/tokens.md](examples/tokens.md#pattern-7-typography-system-with-rem-based-sizing)
- **Pattern 8:** Data-Attributes for State Styling - [examples/patterns.md](examples/patterns.md#pattern-8-data-attributes-for-state-styling)
- **Pattern 9:** SCSS Mixins for Reusable Patterns - [examples/patterns.md](examples/patterns.md#pattern-9-scss-mixins-for-reusable-patterns)
- **Pattern 10:** Global Styles Organization - [examples/patterns.md](examples/patterns.md#pattern-10-global-styles-organization)
- **Pattern 11:** Icon Styling - [examples/patterns.md](examples/patterns.md#pattern-11-icon-styling)
- **Pattern 12:** cva Integration - [examples/cva.md](examples/cva.md#pattern-12-cva-class-variance-authority-integration)
- **Pattern 13:** Advanced CSS Features - [examples/advanced.md](examples/advanced.md#pattern-13-advanced-css-features)
- **Pattern 14:** Sass Module System (@use and @forward) - [examples/modules.md](examples/modules.md#pattern-14-sass-module-system-use-and-forward)

</patterns>

---

<red_flags>

## RED FLAGS

For complete anti-patterns and red flags, see [reference.md](reference.md#red-flags).

**High Priority Issues:**

- Using core tokens directly in components (use semantic tokens)
- Component styles not wrapped in `@layer components {}`
- Using Sass color functions (`darken()`, `lighten()`)
- Hardcoded color/spacing values
- Theme logic in components
- Using `@import` instead of `@use` (deprecated in Dart Sass 1.80.0, removed in 3.0.0)
- Using `/` for division instead of `math.div()` (deprecated)

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST wrap ALL UI package component styles in `@layer components {}` for proper cascade precedence)**

**(You MUST use semantic tokens ONLY in components - NEVER use core tokens directly)**

**(You MUST use HSL format for colors with CSS color functions - NO Sass color functions like darken/lighten)**

**(You MUST use data-attributes for state styling - NOT className toggling)**

**(You MUST use `#### SubsectionName` markdown headers within patterns - NOT separator comments)**

**(You MUST use `@use` for imports - `@import` is deprecated and will be removed in Dart Sass 3.0.0)**

**Failure to follow these rules will break theming, create cascade precedence issues, and violate design system conventions.**

</critical_reminders>
