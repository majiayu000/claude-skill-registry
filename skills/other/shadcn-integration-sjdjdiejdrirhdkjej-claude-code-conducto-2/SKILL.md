---
name: shadcn-integration
description: Integration guide for shadcn/ui components with OKLCH design tokens. Use when setting up shadcn, customizing themes, or adding components to Next.js projects. Auto-trigger on /init --tokens --shadcn flag.
---

<objective>
The shadcn-integration skill bridges the Spec-Flow OKLCH design token system with shadcn/ui components. It preserves OKLCH's superior accessibility features while enabling seamless use of shadcn's battle-tested component library.

**Key Principle**: OKLCH tokens remain the source of truth. shadcn CSS variables are aliases that reference OKLCH tokens, not hardcoded values.

This skill is auto-invoked when:
- User runs `/init --tokens --shadcn`
- User asks to add shadcn components to a project
- Customizing shadcn theme colors or styles
- Setting up Next.js with shadcn/ui

**Benefits**:
- WCAG-compliant colors via OKLCH with perceptual uniformity
- Full shadcn component library compatibility
- 8 customization options without manual CSS editing
- Automatic dark mode support
- Menu-specific theming with variants
</objective>

<quick_start>
<trigger_pattern>
**Auto-invoke when**:
- `/init --tokens --shadcn` command is run
- User asks to "add shadcn" or "setup shadcn"
- User wants to customize theme colors
- Setting up new Next.js project with components
</trigger_pattern>

<basic_workflow>
**Step 1**: Run the questionnaire (8 questions)
```
/init --tokens --shadcn
```

**Step 2**: Review generated files
- `design/systems/shadcn-variables.css` - CSS variables
- `components.json` - shadcn CLI config
- `components/ui/menu-variants.ts` - Menu styling

**Step 3**: Import in globals.css
```css
@import '../design/systems/shadcn-variables.css';
```

**Step 4**: Add components
```bash
npx shadcn@latest add button card dropdown-menu
```
</basic_workflow>

<immediate_value>
**Before**:
- Manual theme.css editing with hardcoded HSL values
- Inconsistent color contrast
- No systematic menu theming
- Dark mode requires manual CSS duplication

**After**:
- 8 questions → complete theme system
- OKLCH ensures WCAG-compliant contrast
- Menu variants via tailwind-variants
- Automatic dark mode via CSS variables
</immediate_value>
</quick_start>

<workflow>
<step number="1">
**Ask 8 Customization Questions**

Use AskUserQuestion tool with these questions in sequence:

1. **Style Preset** → Determines shadcn style + density
2. **Base Color** → Generates OKLCH primary scale (11 shades)
3. **Theme Mode** → Configures light/dark/system preference
4. **Icon Library** → Sets package and components.json config
5. **Font Family** → Configures next/font
6. **Border Radius** → Sets --radius CSS variable
7. **Menu Color** → Generates menu background tokens
8. **Menu Accent** → Generates menu active state tokens
</step>

<step number="2">
**Generate Token Files**

Run the token generation script:
```bash
node .spec-flow/scripts/node/generate-shadcn-tokens.js --config answers.json
```

**Generated files**:
- `design/systems/shadcn-variables.css` - shadcn CSS variable aliases
- `design/systems/tokens.json` - Full token definitions
- `components.json` - shadcn CLI configuration
- `components/ui/menu-variants.ts` - Menu styling with tailwind-variants
</step>

<step number="3">
**Install Dependencies**

Based on questionnaire answers:
```bash
# Icon library (based on choice)
pnpm add lucide-react  # or @heroicons/react or @phosphor-icons/react

# shadcn dependencies
pnpm add tailwindcss-animate class-variance-authority clsx tailwind-merge

# For menu variants
pnpm add tailwind-variants
```
</step>

<step number="4">
**Configure Next.js Layout**

Update `app/layout.tsx` with font configuration:
```typescript
import { Inter } from 'next/font/google'

const fontSans = Inter({
  subsets: ['latin'],
  variable: '--font-sans',
})

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={fontSans.variable}>
      <body>{children}</body>
    </html>
  )
}
```
</step>

<step number="5">
**Add shadcn Components**

Now users can add components that automatically use the generated theme:
```bash
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add dropdown-menu
npx shadcn@latest add dialog
```

Components will use CSS variables from shadcn-variables.css.
</step>
</workflow>

<reference>
## OKLCH → shadcn Variable Mapping

| OKLCH Token | shadcn Variable | Usage |
|-------------|-----------------|-------|
| `--color-neutral-50` | `--background` | Page background |
| `--color-neutral-900` | `--foreground` | Primary text |
| `--color-primary-600` | `--primary` | Brand actions |
| `--color-neutral-50` | `--primary-foreground` | Text on primary |
| `--color-neutral-100` | `--muted` | Subtle backgrounds |
| `--color-neutral-500` | `--muted-foreground` | Secondary text |
| `--color-error-fg` | `--destructive` | Delete actions |
| `--color-neutral-200` | `--border` | Dividers, inputs |

## Menu Token System

**Menu Color Options**:
| Choice | Effect |
|--------|--------|
| `background` | Uses page background |
| `surface` | Elevated card with shadow |
| `primaryTint` | 5% primary color wash |
| `glass` | Transparent + blur |

**Menu Accent Options**:
| Choice | Effect |
|--------|--------|
| `border` | 3px left border on active |
| `background` | Full background highlight |
| `iconTint` | Only icon changes color |
| `combined` | Border + subtle background |

## Border Radius Scale

| Choice | Value | Effect |
|--------|-------|--------|
| None | `0` | Sharp corners |
| Small | `0.25rem` | Minimal |
| Medium | `0.5rem` | Modern (default) |
| Large | `0.75rem` | Soft |
| Full | `9999px` | Pills |

## Icon Library Integration

| Choice | Package | Import |
|--------|---------|--------|
| Lucide | `lucide-react` | `import { Icon } from 'lucide-react'` |
| Heroicons | `@heroicons/react` | `import { Icon } from '@heroicons/react/24/outline'` |
| Phosphor | `@phosphor-icons/react` | `import { Icon } from '@phosphor-icons/react'` |
</reference>

<quality_gates>
**FAIL (block next phase)**:
- `components.json` missing after --shadcn flag
- Icon library package not installed
- shadcn CSS variable aliases missing from tokens.css
- tailwindcss-animate not installed

**WARN (non-blocking)**:
- Font not configured in layout.tsx
- Dark mode class not on html element
- Menu variants file missing

**Validation commands**:
```bash
# Check components.json exists
test -f components.json && echo "✓ components.json"

# Check shadcn variables
grep -q "shadcn/ui CSS Variable Aliases" design/systems/shadcn-variables.css && echo "✓ shadcn variables"

# Check icon library
pnpm list lucide-react 2>/dev/null || pnpm list @heroicons/react 2>/dev/null && echo "✓ icon library"
```
</quality_gates>

<examples>
<example name="Full Integration Flow">
```bash
# 1. Run questionnaire
/init --tokens --shadcn

# Answer 8 questions...
# Style: Default
# Color: Blue
# Theme: System preference
# Icons: Lucide
# Font: Inter
# Radius: Medium
# Menu Color: Background
# Menu Accent: Left border

# 2. Files generated automatically

# 3. Import in globals.css
# @import '../design/systems/shadcn-variables.css';

# 4. Install icon library
pnpm add lucide-react

# 5. Add components
npx shadcn@latest add button card dropdown-menu

# 6. Use in components
import { Button } from '@/components/ui/button'
<Button variant="default">Click me</Button>
```
</example>

<example name="Custom Primary Color">
When user selects "Custom" for base color:

```typescript
// AskUserQuestion for custom hue
{
  question: "Enter OKLCH hue value (0-360)",
  header: "Custom Hue",
  options: [
    { label: "Teal (175)", description: "Modern, tech-forward" },
    { label: "Coral (15)", description: "Warm, energetic" },
    { label: "Other", description: "Enter exact value" }
  ]
}

// Result: Full 11-shade scale generated from hue
// oklch(98% 0.045 175) → oklch(14% 0.045 175)
```
</example>

<example name="Menu Theming in Action">
```tsx
// components/sidebar.tsx
import { menuStyles } from '@/components/ui/menu-variants'

export function Sidebar() {
  const styles = menuStyles({ menuColor: 'background', menuAccent: 'border' })

  return (
    <nav className={styles.root()}>
      <a href="/" data-active={true} className={styles.item()}>
        <HomeIcon className={styles.icon()} />
        <span className={styles.label()}>Home</span>
      </a>
      <a href="/settings" className={styles.item()}>
        <SettingsIcon className={styles.icon()} />
        <span className={styles.label()}>Settings</span>
      </a>
    </nav>
  )
}
```
</example>
</examples>

<troubleshooting>
## Common Issues

**Colors not applying**:
- Verify `@import '../design/systems/shadcn-variables.css'` in globals.css
- Check import order (shadcn-variables before @tailwind directives)
- Ensure Tailwind config has `cssVariables: true`

**Dark mode not working**:
- Add `className="dark"` to html element for class-based dark mode
- Or use `suppressHydrationWarning` with next-themes
- Verify `.dark` CSS block exists in shadcn-variables.css

**Menu variants not found**:
- Install tailwind-variants: `pnpm add tailwind-variants`
- Check `components/ui/menu-variants.ts` exists
- Verify import path in your component

**Icons not loading**:
- Verify correct package installed based on questionnaire choice
- Check import syntax matches package (lucide vs heroicons)
- Ensure tree-shaking is enabled in bundler

**Radius not applying**:
- Check `--radius` variable in :root
- Verify Tailwind config has borderRadius extension
- Some components use `calc(var(--radius) - 2px)` for nested elements
</troubleshooting>

<related_skills>
- `design-tokens` - Core OKLCH token system (this skill extends it)
- `theme-consistency` - Enforces token usage in prototypes
- `mockup-extraction` - Extracts component patterns from mockups
- `frontend-dev` - Uses generated tokens in implementation
</related_skills>
