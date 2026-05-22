---
name: design-system
description: Design system management for building and reusing UI components, tokens, and patterns. Use when working with component libraries, design tokens, style guides, or reusable UI patterns to ensure consistency and promote component reuse.
user-invocable: false
---

# Design System Skill

This skill automatically activates when working with design systems, component libraries, or reusable UI patterns. It ensures consistency and promotes component reuse across projects.

## Core Principle

**BUILD ONCE, USE EVERYWHERE**

```
❌ Duplicating UI code across components
✅ Building reusable, documented design system components
```

## Automatic Behaviors

When this skill activates, Claude will:

### 1. Identify Design System Opportunities

Automatically detect when code could benefit from design system patterns:

| Pattern | Detection | Recommendation |
|---------|-----------|----------------|
| Repeated styles | Same CSS in multiple places | Extract to design token |
| Similar components | Components with slight variations | Create variant system |
| Magic numbers | Hard-coded values (colors, spacing) | Replace with tokens |
| Inconsistent naming | Different names for same concept | Standardize naming |
| Missing documentation | Undocumented components | Add usage docs |

### 2. Design Token Architecture

```
DESIGN TOKEN STRUCTURE
════════════════════════════════════════════════════════════

PRIMITIVE TOKENS (Raw Values)
└── color.blue.500: "#3b82f6"
└── space.4: "16px"
└── font.size.base: "16px"

SEMANTIC TOKENS (Purpose-Based)
└── color.primary: "{color.blue.500}"
└── spacing.component: "{space.4}"
└── text.body: "{font.size.base}"

COMPONENT TOKENS (Component-Specific)
└── button.background: "{color.primary}"
└── button.padding: "{spacing.component}"
└── button.fontSize: "{text.body}"
```

### 3. Component Structure

```
COMPONENT ORGANIZATION (Atomic Design)
════════════════════════════════════════════════════════════

src/components/
├── atoms/                    # Smallest building blocks
│   ├── Button/
│   ├── Input/
│   ├── Icon/
│   └── Text/
│
├── molecules/                # Combinations of atoms
│   ├── FormField/
│   ├── SearchBox/
│   └── Card/
│
├── organisms/                # Complex UI sections
│   ├── Header/
│   ├── Sidebar/
│   └── DataTable/
│
└── templates/                # Page layouts
    ├── DashboardLayout/
    └── AuthLayout/
```

### 4. Component File Structure

```
Button/
├── Button.tsx           # Component implementation
├── Button.styles.ts     # Styles (CSS modules or styled)
├── Button.types.ts      # TypeScript interfaces
├── Button.test.tsx      # Unit tests
├── Button.stories.tsx   # Storybook documentation
└── index.ts             # Public exports
```

## Warning Triggers

Automatically warn user when:

1. **Hard-coded values detected**
   > "⚠️ DESIGN SYSTEM: Consider replacing hard-coded value with design token"

2. **Duplicate styles found**
   > "⚠️ DESIGN SYSTEM: This style exists in [component]. Consider extracting to shared token"

3. **Missing documentation**
   > "⚠️ DESIGN SYSTEM: Component missing Storybook story or usage documentation"

4. **Inconsistent naming**
   > "⚠️ DESIGN SYSTEM: Naming pattern differs from existing components"

5. **Component too complex**
   > "⚠️ DESIGN SYSTEM: Consider breaking this into smaller atomic components"

## Design System Checklist

```
📋 Design System Audit

□ TOKENS
  □ Color primitives defined
  □ Semantic color tokens exist
  □ Spacing scale consistent
  □ Typography scale defined

□ COMPONENTS
  □ Atomic structure followed
  □ Components are documented
  □ TypeScript types defined
  □ Accessibility tested

□ PATTERNS
  □ Layout patterns documented
  □ Form patterns standardized
  □ Error handling consistent
  □ Loading states defined
```
