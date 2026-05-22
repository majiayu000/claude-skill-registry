---
name: prototype-to-production
description: Convert design prototypes (HTML, CSS, Figma exports) into production-ready components. Analyzes prototype structure, extracts design tokens, identifies reusable patterns, and generates typed React components. Adapts to existing project tech stack with React + TypeScript as default.
version: 1.0.0
category: Design & Frontend
agents: [frontend-ui-developer, rapid-ui-designer, code-quality-reviewer]
keywords: [prototype, production, components, design, HTML, CSS, Figma, React, TypeScript, conversion, design-tokens, atomic-design]
---

# Prototype to Production Skill

Convert design prototypes into production-ready, typed components by analyzing structure, extracting patterns, and generating clean code.

## When to Use

- Converting HTML prototypes to React components
- Transforming super-design outputs (`.superdesign/design_iterations/*.html`) to production code
- Breaking down Figma exports into reusable components
- Extracting design tokens from prototype CSS/inline styles
- Productionizing a mockup or proof-of-concept UI

## Conversion Workflow

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│   Analyze   │──▶│   Detect    │──▶│  Decompose  │──▶│  Generate   │
│   Input     │   │  Tech Stack │   │  Components │   │    Code     │
└─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘
       │                 │                 │                 │
       ▼                 ▼                 ▼                 ▼
  Identify type    package.json      Atomic design     TypeScript
  & structure      scan + patterns   methodology       components
```

### Step 1: Analyze Input

**Detect prototype type and structure:**

| Input Type | Detection Method | Key Patterns |
|------------|------------------|--------------|
| Super-design | Path: `.superdesign/design_iterations/*.html` | Flowbite, Tailwind CDN, theme CSS references |
| Generic HTML | Any `.html` file | Standard HTML structure, inline/external CSS |
| Figma Export | Figma-specific class names | `figma-`, absolute positioning, frame naming |

**Super-design analysis:**
```
Read prototype file → Extract theme CSS reference →
Identify component regions (header, main, footer) →
Map flowbite components to equivalents
```

### Step 2: Detect Project Tech Stack

**Scan target project to determine output format:**

1. Check `package.json` for frameworks:
   - `react` / `react-dom` → React components
   - `vue` → Vue SFCs
   - `svelte` → Svelte components
   - `@angular/core` → Angular components

2. Check for TypeScript:
   - `tsconfig.json` exists → TypeScript output
   - `typescript` in dependencies → TypeScript output

3. Check styling approach:
   - `tailwindcss` → Tailwind classes
   - `styled-components` / `@emotion/react` → CSS-in-JS
   - CSS/SCSS files → Separate stylesheets

**Default**: React + TypeScript + Tailwind CSS

### Step 3: Component Decomposition

**Apply atomic design methodology:**

```
┌─────────────────────────────────────────────────────────┐
│ ORGANISMS (Complex compositions)                        │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ MOLECULES (Simple compositions)                     │ │
│ │ ┌─────────────────────────────────────────────────┐ │ │
│ │ │ ATOMS (Primitive elements)                      │ │ │
│ │ │ Button, Input, Label, Icon, Badge, Avatar       │ │ │
│ │ └─────────────────────────────────────────────────┘ │ │
│ │ FormField, SearchBar, Card, MenuItem               │ │
│ └─────────────────────────────────────────────────────┘ │
│ Header, Sidebar, ProductGrid, CommentThread            │
└─────────────────────────────────────────────────────────┘
```

**Component identification checklist:**
- [ ] Repeated patterns (2+ occurrences = extract)
- [ ] Logical groupings (header, nav, content sections)
- [ ] Interactive elements (buttons, forms, modals)
- [ ] Data display patterns (cards, lists, tables)

### Step 4: Extract Design Tokens

**Extract from prototype CSS/styles:**

```json
{
  "colors": {
    "primary": "extracted-from-buttons",
    "secondary": "extracted-from-secondary-elements",
    "background": "extracted-from-body/container",
    "text": "extracted-from-body-text"
  },
  "typography": {
    "fontFamily": "extracted-from-font-family",
    "fontSize": { "base": "16px", "lg": "18px", "xl": "20px" }
  },
  "spacing": {
    "derived-from-padding-margin-patterns": true
  },
  "borderRadius": "extracted-from-rounded-elements"
}
```

> See `templates/design-tokens-extract.json` for full template

### Step 5: Generate Components

**For each identified component:**

1. Create TypeScript interface for props
2. Apply forwardRef pattern for DOM access
3. Include accessibility attributes
4. Use project's styling approach
5. Add JSDoc documentation

> See `templates/component-base.tsx` and `templates/component-with-variants.tsx`

### Step 6: Integration Guidance

Provide clear instructions for:
- File placement in project structure
- Import statements needed
- Peer dependencies (if any)
- Usage examples

## Component Output Standards

### TypeScript Props Interface

```typescript
interface ComponentProps {
  /** Primary variant for emphasis */
  variant?: 'primary' | 'secondary' | 'outline';
  /** Size affects padding and font-size */
  size?: 'sm' | 'md' | 'lg';
  /** Disables interaction */
  disabled?: boolean;
  /** Additional CSS classes */
  className?: string;
  /** Content */
  children: React.ReactNode;
}
```

### Accessibility Requirements

Every component must include:
- Semantic HTML elements (use `<button>` not `<div>`)
- Keyboard navigation support
- ARIA attributes where needed
- Focus management

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Components | PascalCase | `ProductCard.tsx` |
| Props types | PascalCase + Props | `ProductCardProps` |
| CSS classes | kebab-case | `product-card-container` |
| Design tokens | camelCase | `primaryColor` |

## Conversion Patterns Reference

> See `references/conversion-patterns.md` for comprehensive HTML → React patterns

### Quick Reference

| HTML Pattern | React Equivalent |
|--------------|------------------|
| `class="..."` | `className="..."` |
| `onclick="..."` | `onClick={handler}` |
| `for="..."` | `htmlFor="..."` |
| `<input value="">` | `<input value="" onChange={...}>` |
| Inline styles | Tailwind classes or styled objects |

## Templates Reference

| Template | Purpose |
|----------|---------|
| `component-base.tsx` | Basic component with types and accessibility |
| `component-with-variants.tsx` | Component with variant/size system |
| `design-tokens-extract.json` | Token extraction structure |

## Example Conversion

**Input (super-design HTML):**
```html
<button class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
  Submit
</button>
```

**Output (React + TypeScript):**
```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary';
  children: React.ReactNode;
  onClick?: () => void;
}

export const Button = ({ variant = 'primary', children, onClick }: ButtonProps) => {
  return (
    <button
      className={cn(
        'px-4 py-2 rounded-lg transition-colors',
        variant === 'primary' && 'bg-blue-600 text-white hover:bg-blue-700'
      )}
      onClick={onClick}
    >
      {children}
    </button>
  );
};
```

## Integration with Super-Design

When converting super-design outputs:

1. **Read the theme CSS file** referenced in the HTML
2. **Map theme variables** to design tokens
3. **Preserve animations** defined in the prototype
4. **Maintain responsive breakpoints** from Tailwind classes

Super-design folder structure:
```
.superdesign/
└── design_iterations/
    ├── theme_1.css      # Theme tokens
    ├── chat_ui_1.html   # Prototype iteration 1
    └── chat_ui_2.html   # Prototype iteration 2
```
