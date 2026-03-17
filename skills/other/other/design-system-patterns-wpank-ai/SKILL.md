---
name: design-system-patterns
model: standard
description: Foundational design system architecture — token hierarchies, theming infrastructure, token pipelines, and governance. Use when creating design tokens, implementing theme switching, setting up Style Dictionary, or establishing multi-brand theming. Triggers on design tokens, theme provider, Style Dictionary, token pipeline, multi-brand theming, CSS custom properties architecture.
---

# Design System Patterns

Foundational architecture for scalable design systems: token hierarchies, theming infrastructure, token pipelines, and governance patterns.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install design-system-patterns
```


---

## When to Use

- Defining token architecture (primitive → semantic → component layers)
- Implementing light/dark/system theme switching with React
- Setting up Style Dictionary or Figma-to-code token pipelines
- Building multi-brand theming systems
- Establishing token naming conventions and governance
- Preventing flash of unstyled content (FOUC) in SSR

---

## Pattern 1: Token Hierarchy

Three-layer token architecture separates raw values from meaning from usage.

```css
/* Layer 1: Primitive tokens — raw values, never used directly in components */
:root {
  --color-blue-500: #3b82f6;
  --color-blue-600: #2563eb;
  --color-gray-50: #fafafa;
  --color-gray-900: #171717;

  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-4: 1rem;

  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
}

/* Layer 2: Semantic tokens — contextual meaning, theme-aware */
:root {
  --text-primary: var(--color-gray-900);
  --text-secondary: var(--color-gray-600);
  --surface-default: white;
  --surface-elevated: var(--color-gray-50);
  --border-default: var(--color-gray-200);
  --interactive-primary: var(--color-blue-500);
  --interactive-primary-hover: var(--color-blue-600);
}

/* Layer 3: Component tokens — specific usage, optional */
:root {
  --button-bg: var(--interactive-primary);
  --button-bg-hover: var(--interactive-primary-hover);
  --button-text: white;
  --button-radius: var(--radius-md);
  --button-padding-x: var(--space-4);
  --button-padding-y: var(--space-2);
}
```

> Semantic tokens are the most important layer — they enable theming. Component tokens are optional and useful for complex component libraries.

---

## Pattern 2: Theme Switching with React

Key capabilities: `theme` (user selection), `resolvedTheme` (actual light/dark), `setTheme`, system preference detection, localStorage persistence, DOM attribute application.

```tsx
type Theme = "light" | "dark" | "system";

export function ThemeProvider({ children, defaultTheme = "system", storageKey = "theme",
  attribute = "data-theme" }: { children: React.ReactNode; defaultTheme?: Theme;
  storageKey?: string; attribute?: "class" | "data-theme" }) {
  const [theme, setThemeState] = useState<Theme>(() =>
    typeof window === "undefined" ? defaultTheme
      : (localStorage.getItem(storageKey) as Theme) || defaultTheme);
  const [resolvedTheme, setResolvedTheme] = useState<"light" | "dark">("light");

  const getSystem = useCallback(() =>
    matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light" as const, []);

  const apply = useCallback((r: "light" | "dark") => {
    const root = document.documentElement;
    attribute === "class"
      ? (root.classList.remove("light", "dark"), root.classList.add(r))
      : root.setAttribute(attribute, r);
    root.style.colorScheme = r;
    setResolvedTheme(r);
  }, [attribute]);

  useEffect(() => { apply(theme === "system" ? getSystem() : theme); }, [theme, apply, getSystem]);

  useEffect(() => {  // Listen for system preference changes
    if (theme !== "system") return;
    const mq = matchMedia("(prefers-color-scheme: dark)");
    const handler = () => apply(getSystem());
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, [theme, apply, getSystem]);

  const setTheme = useCallback((t: Theme) => {
    localStorage.setItem(storageKey, t); setThemeState(t);
  }, [storageKey]);

  return <ThemeContext.Provider value={{ theme, resolvedTheme, setTheme }}>
    {children}
  </ThemeContext.Provider>;
}
```

Full implementation with `toggleTheme`, `disableTransitionOnChange`, and testing patterns in [references/theming-architecture.md](references/theming-architecture.md).

### Preventing FOUC in SSR (Next.js)

Inline script in `<head>` runs before paint:

```tsx
const themeScript = `(function(){
  var t=localStorage.getItem('theme')||'system';
  var d=t==='dark'||(t==='system'&&matchMedia('(prefers-color-scheme:dark)').matches);
  document.documentElement.setAttribute('data-theme',d?'dark':'light');
  document.documentElement.style.colorScheme=d?'dark':'light';
})()`;

// In layout.tsx
<html lang="en" suppressHydrationWarning>
  <head>
    <script dangerouslySetInnerHTML={{ __html: themeScript }} />
  </head>
  <body><ThemeProvider>{children}</ThemeProvider></body>
</html>
```

---

## Pattern 3: Multi-Brand Theming

Layer brand tokens on top of semantic tokens for white-label products:

```css
[data-brand="corporate"] {
  --brand-primary: #0066cc;
  --brand-primary-hover: #0052a3;
  --brand-font-heading: "Helvetica Neue", sans-serif;
  --brand-radius: 0.25rem;
}

[data-brand="startup"] {
  --brand-primary: #7c3aed;
  --brand-primary-hover: #6d28d9;
  --brand-font-heading: "Poppins", sans-serif;
  --brand-radius: 1rem;
}

/* Map brand tokens into semantic tokens */
:root {
  --interactive-primary: var(--brand-primary);
  --interactive-primary-hover: var(--brand-primary-hover);
}
```

---

## Pattern 4: Style Dictionary Pipeline

Multi-platform token generation from a single JSON source:

```javascript
// style-dictionary.config.js — generates CSS, iOS Swift, and Android XML
module.exports = {
  source: ["tokens/**/*.json"],
  platforms: {
    css: {
      transformGroup: "css", buildPath: "dist/css/",
      files: [{ destination: "variables.css", format: "css/variables",
        options: { outputReferences: true } }],
    },
    ios: {
      transformGroup: "ios-swift", buildPath: "dist/ios/",
      files: [{ destination: "DesignTokens.swift", format: "ios-swift/class.swift",
        className: "DesignTokens" }],
    },
    android: {
      transformGroup: "android", buildPath: "dist/android/",
      files: [{ destination: "colors.xml", format: "android/colors",
        filter: { attributes: { category: "color" } } }],
    },
  },
};
```

See [references/design-tokens.md](references/design-tokens.md) for token category definitions, custom transforms, and platform-specific output examples.

---

## Pattern 5: Accessibility Tokens

```css
@media (prefers-reduced-motion: reduce) {
  :root {
    --duration-fast: 0ms;
    --duration-normal: 0ms;
    --duration-slow: 0ms;
  }
}

@media (prefers-contrast: high) {
  :root {
    --text-primary: #000000;
    --surface-default: #ffffff;
    --border-default: #000000;
    --interactive-primary: #0000ee;
  }
}

@media (forced-colors: active) {
  .button { border: 2px solid currentColor; }
  .card { border: 1px solid CanvasText; }
}
```

---

## Token Naming Conventions

Format: `[category]-[property]-[variant]-[state]` (e.g. `color-border-input-focus`)

1. **kebab-case** — `text-primary` not `textPrimary`
2. **Semantic names** — `danger` not `red`
3. **State suffixes** — `-hover`, `-focus`, `-active`, `-disabled`
4. **Scale indicators** — `spacing-4`, `font-size-lg`

---

## Token Governance

Change management: **Propose** → **Review** (design + eng) → **Test** (all platforms/themes) → **Deprecate** (with migration path) → **Remove** (after deprecation period).

```json
{
  "color.primary": {
    "value": "{color.primitive.blue.500}",
    "deprecated": true,
    "deprecatedMessage": "Use semantic.accent.default instead",
    "replacedBy": "semantic.accent.default"
  }
}
```

---

## Best Practices

1. **Name tokens by purpose** — semantic names, not visual descriptions
2. **Maintain the hierarchy** — primitives → semantic → component
3. **Version tokens** — treat token changes as API changes with semver
4. **Test all theme combinations** — every theme must work with every component
5. **Automate the pipeline** — CI/CD for Figma-to-code synchronization
6. **Provide migration paths** — deprecate gradually with clear alternatives
7. **Validate contrast** — automated WCAG AA/AAA checks on token pairs

---

## Common Pitfalls

- **Token sprawl** — too many tokens without clear hierarchy
- **Inconsistent naming** — mixing camelCase and kebab-case
- **Hardcoded values** — using raw hex/rem instead of token references
- **Circular references** — tokens referencing each other in loops
- **Platform gaps** — tokens defined for web but missing for mobile
- **Missing dark mode** — semantic tokens that don't adapt to themes

---

## Related Skills

- [design-system-components](../design-system-components/) — CVA variant patterns and Surface primitives
- [distinctive-design-systems](../distinctive-design-systems/) — Aesthetic documentation and visual identity
- [theme-factory](../theme-factory/) — Pre-built theme palettes for artifacts

---

## References

- [references/design-tokens.md](references/design-tokens.md) — Complete token category definitions
- [references/theming-architecture.md](references/theming-architecture.md) — Detailed theming implementation
- [references/component-architecture.md](references/component-architecture.md) — Compound, polymorphic, and headless patterns
