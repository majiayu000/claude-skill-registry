---
name: assembling-components
description: Assembles component outputs from AI Design Components skills into unified, production-ready component systems with validated token integration, proper import chains, and framework-specific scaffolding. Use as the capstone skill after running theming, layout, dashboard, data-viz, or feedback skills to wire components into working React/Next.js, Python, or Rust projects.
---

# Assembling Components

## Purpose

This skill transforms the outputs of AI Design Components skills into production-ready applications. It provides library-specific context for our token system, component patterns, and skill chain workflow - knowledge that generic assembly patterns cannot provide. The skill validates token integration, generates proper scaffolding, and wires components together correctly.

## When to Use

Activate this skill when:
- Completing a skill chain workflow (theming → layout → dashboards → data-viz → feedback)
- Generating new project scaffolding for React/Vite, Next.js, FastAPI, Flask, or Rust/Axum
- Validating that all generated CSS uses design tokens (not hardcoded values)
- Creating barrel exports and wiring component imports correctly
- Assembling components from multiple skills into a unified application
- Debugging integration issues (missing entry points, broken imports, theme not switching)
- Preparing generated code for production deployment

## Skill Chain Context

This skill understands the output of every AI Design Components skill:

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ theming-         │────▶│ designing-       │────▶│ creating-        │
│ components       │     │ layouts          │     │ dashboards       │
└──────────────────┘     └──────────────────┘     └──────────────────┘
        │                        │                        │
        ▼                        ▼                        ▼
    tokens.css               Layout.tsx             Dashboard.tsx
    theme-provider.tsx       Header.tsx             KPICard.tsx
        │                        │                        │
        └────────────────────────┴────────────────────────┘
                                 │
                                 ▼
                    ┌──────────────────────┐
                    │ visualizing-data     │
                    │ providing-feedback   │
                    └──────────────────────┘
                                 │
                                 ▼
                         DonutChart.tsx
                         Toast.tsx, Spinner.tsx
                                 │
                                 ▼
                    ┌──────────────────────┐
                    │ ASSEMBLING-          │
                    │ COMPONENTS           │
                    │ (THIS SKILL)         │
                    └──────────────────────┘
                                 │
                                 ▼
                       WORKING COMPONENT SYSTEM
```

### Expected Outputs by Skill

| Skill | Primary Outputs | Token Dependencies |
|-------|-----------------|-------------------|
| `theming-components` | tokens.css, theme-provider.tsx | Foundation |
| `designing-layouts` | Layout.tsx, Header.tsx, Sidebar.tsx | --spacing-*, --color-border-* |
| `creating-dashboards` | Dashboard.tsx, KPICard.tsx | All layout + chart tokens |
| `visualizing-data` | Chart components, legends | --chart-color-*, --font-size-* |
| `building-forms` | Form inputs, validation | --spacing-*, --radius-*, --color-error |
| `building-tables` | Table, pagination | --color-*, --spacing-* |
| `providing-feedback` | Toast, Spinner, EmptyState | --color-success/error/warning |

## Token Validation

### Run Validation Script (Token-Free Execution)

```bash
# Basic validation
python scripts/validate_tokens.py src/styles

# Strict mode with fix suggestions
python scripts/validate_tokens.py src --strict --fix-suggestions

# JSON output for CI/CD
python scripts/validate_tokens.py src --json
```

### Our Token Naming Conventions

```css
/* Colors - semantic naming */
--color-primary: #FA582D;          /* Brand primary */
--color-success: #00CC66;          /* Positive states */
--color-warning: #FFCB06;          /* Caution states */
--color-error: #C84727;            /* Error states */
--color-info: #00C0E8;             /* Informational */

--color-bg-primary: #FFFFFF;       /* Main background */
--color-bg-secondary: #F8FAFC;     /* Elevated surfaces */
--color-text-primary: #1E293B;     /* Body text */
--color-text-secondary: #64748B;   /* Muted text */

/* Spacing - 4px base unit */
--spacing-xs: 0.25rem;   /* 4px */
--spacing-sm: 0.5rem;    /* 8px */
--spacing-md: 1rem;      /* 16px */
--spacing-lg: 1.5rem;    /* 24px */
--spacing-xl: 2rem;      /* 32px */

/* Typography */
--font-size-xs: 0.75rem;   /* 12px */
--font-size-sm: 0.875rem;  /* 14px */
--font-size-base: 1rem;    /* 16px */
--font-size-lg: 1.125rem;  /* 18px */

/* Component sizes */
--icon-size-sm: 1rem;      /* 16px */
--icon-size-md: 1.5rem;    /* 24px */
--radius-sm: 4px;
--radius-md: 8px;
--shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
```

### Validation Rules

| Must Use Tokens (Errors) | Example Fix |
|--------------------------|-------------|
| Colors | `#FA582D` → `var(--color-primary)` |
| Spacing (≥4px) | `16px` → `var(--spacing-md)` |
| Font sizes | `14px` → `var(--font-size-sm)` |

| Should Use Tokens (Warnings) | Example Fix |
|------------------------------|-------------|
| Border radius | `8px` → `var(--radius-md)` |
| Shadows | `0 4px...` → `var(--shadow-md)` |
| Z-index (≥100) | `1000` → `var(--z-dropdown)` |

## Framework Selection

### React/TypeScript

**Choose Vite + React when:**
- Building single-page applications
- Lightweight, fast development builds
- Maximum control over configuration
- No server-side rendering needed

**Choose Next.js 14/15 when:**
- Need server-side rendering or static generation
- Building full-stack with API routes
- SEO is important
- Using React Server Components

### Python

**Choose FastAPI when:**
- Building modern async APIs
- Need automatic OpenAPI documentation
- High performance is required
- Using Pydantic for validation

**Choose Flask when:**
- Simpler, more flexible setup
- Familiar with Flask ecosystem
- Template rendering (Jinja2)
- Smaller applications

### Rust

**Choose Axum when:**
- Modern tower-based architecture
- Type-safe extractors
- Async-first design
- Growing ecosystem

**Choose Actix Web when:**
- Maximum performance required
- Actor model benefits your use case
- More mature ecosystem

## Implementation Approach

### 1. Validate Token Integration

Before assembly, check all CSS uses tokens:

```bash
python scripts/validate_tokens.py <component-directory>
```

Fix any violations before proceeding.

### 2. Generate Project Scaffolding

**React/Vite:**
```tsx
// src/main.tsx - Entry point
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { ThemeProvider } from '@/context/theme-provider'
import App from './App'
import './styles/tokens.css'   // FIRST - token definitions
import './styles/globals.css'  // SECOND - global resets

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ThemeProvider>
      <App />
    </ThemeProvider>
  </StrictMode>,
)
```

**index.html:**
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{{PROJECT_TITLE}}</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

### 3. Wire Components Together

**Theme Provider:**
```tsx
// src/context/theme-provider.tsx
import { createContext, useContext, useEffect, useState } from 'react'

type Theme = 'light' | 'dark' | 'system'

const ThemeContext = createContext<{
  theme: Theme
  setTheme: (theme: Theme) => void
} | undefined>(undefined)

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>('system')

  useEffect(() => {
    const root = document.documentElement
    const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark' : 'light'
    root.setAttribute('data-theme', theme === 'system' ? systemTheme : theme)
    localStorage.setItem('theme', theme)
  }, [theme])

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export const useTheme = () => {
  const context = useContext(ThemeContext)
  if (!context) throw new Error('useTheme must be used within ThemeProvider')
  return context
}
```

**Barrel Exports:**
```tsx
// src/components/ui/index.ts
export { Button } from './button'
export { Card } from './card'

// src/components/features/dashboard/index.ts
export { KPICard } from './kpi-card'
export { DonutChart } from './donut-chart'
export { Dashboard } from './dashboard'
```

### 4. Configure Build System

**vite.config.ts:**
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
```

**tsconfig.json:**
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "baseUrl": ".",
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["src"]
}
```

## Cross-Skill Integration

### Using Theming Components

```tsx
// Import tokens first, components inherit token values
import './styles/tokens.css'

// Use ThemeProvider at root
<ThemeProvider>
  <App />
</ThemeProvider>
```

### Using Dashboard Components

```tsx
// Components from creating-dashboards skill
import { Dashboard, KPICard } from '@/components/features/dashboard'

// Wire with data
<Dashboard>
  <KPICard
    label="Total Threats"
    value={1234}
    severity="critical"
    trend={{ value: 15.3, direction: 'up' }}
  />
</Dashboard>
```

### Using Data Visualization

```tsx
// Charts from visualizing-data skill
import { DonutChart } from '@/components/charts'

// Charts use --chart-color-* tokens automatically
<DonutChart
  data={threatData}
  title="Threats by Severity"
/>
```

### Using Feedback Components

```tsx
// From providing-feedback skill
import { Toast, Spinner, EmptyState } from '@/components/feedback'

// Wire toast notifications
<ToastProvider>
  <App />
</ToastProvider>

// Use spinner for loading states
{isLoading ? <Spinner /> : <Dashboard />}
```

## Integration Checklist

Before delivery, verify:

- [ ] **Token file exists** (`tokens.css`) with all 7 categories
- [ ] **Token import order** correct (tokens.css → globals.css → components)
- [ ] **No hardcoded values** (run `validate_tokens.py`)
- [ ] **Theme toggle works** (`data-theme` attribute switches)
- [ ] **Reduced motion** supported (`@media (prefers-reduced-motion)`)
- [ ] **Build completes** without errors
- [ ] **Types pass** (TypeScript compiles)
- [ ] **Imports resolve** (no missing modules)
- [ ] **Barrel exports** exist for each component directory

## Bundled Resources

### Scripts (Token-Free Execution)
- `scripts/validate_tokens.py` - Validate CSS uses design tokens
- `scripts/generate_scaffold.py` - Generate project boilerplate
- `scripts/check_imports.py` - Validate import chains
- `scripts/generate_exports.py` - Create barrel export files

Run scripts directly without loading into context:
```bash
python scripts/validate_tokens.py demo/examples --fix-suggestions
```

### References (Detailed Patterns)
- `references/library-context.md` - AI Design Components library awareness
- `references/react-vite-template.md` - Full Vite + React setup
- `references/nextjs-template.md` - Next.js 14/15 patterns
- `references/python-fastapi-template.md` - FastAPI project structure
- `references/rust-axum-template.md` - Rust/Axum project structure
- `references/token-validation-rules.md` - Complete validation rules

### Examples (Complete Implementations)
- `examples/react-dashboard/` - Full Vite + React dashboard
- `examples/nextjs-dashboard/` - Next.js App Router dashboard
- `examples/fastapi-dashboard/` - Python FastAPI dashboard
- `examples/rust-axum-dashboard/` - Rust Axum dashboard

### Assets (Templates)
- `assets/templates/react/` - React project templates
- `assets/templates/python/` - Python project templates
- `assets/templates/rust/` - Rust project templates

## Application Assembly Workflow

1. **Validate Components**: Run `validate_tokens.py` on all generated CSS
2. **Choose Framework**: React/Vite, Next.js, FastAPI, or Rust based on requirements
3. **Generate Scaffolding**: Create project structure and configuration
4. **Wire Imports**: Set up entry point, import chain, barrel exports
5. **Add Providers**: ThemeProvider, ToastProvider at root
6. **Connect Components**: Import and compose feature components
7. **Configure Build**: vite.config, tsconfig, package.json
8. **Final Validation**: Build, type-check, lint
9. **Document**: README with setup and usage instructions

For library-specific patterns and complete context, see `references/library-context.md`.
