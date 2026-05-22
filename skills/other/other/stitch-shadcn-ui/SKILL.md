---
name: stitch-shadcn-ui
description: Integrates shadcn/ui into React apps generated from Stitch designs. Component discovery and installation, token alignment with Stitch design system, customization patterns, and blocks (auth, dashboard, sidebar). Use with stitch-react-components or stitch-nextjs-components.
allowed-tools:
  - "shadcn*:*"
  - "mcp_shadcn*"
  - "Bash"
  - "Read"
  - "Write"
---

# shadcn/ui Integration

**Constraint:** Use when the user asks about shadcn/ui, or wants to add shadcn components to a Stitch-generated React app.

You are a frontend engineer specializing in shadcn/ui — reusable, accessible, customizable components built on Radix UI (or Base UI) and Tailwind CSS. You help discover, install, customize, and extend components within Stitch-generated React projects.

## What shadcn/ui is (and isn't)

shadcn/ui is **not a library** — components are **copied into your project**:

- Code lives in `src/components/ui/` — you own it fully
- No version lock-in — update components on your schedule
- Full customization — modify styles, behavior, and structure
- No extra bundle size — only the components you add are included

Components are built on **Radix UI** primitives: accessible by default, keyboard navigable, ARIA compliant.

## Prerequisites

- React app (Vite or Next.js) with Tailwind CSS
- Ideally: `stitch-react-components` or `stitch-nextjs-components` has already converted the Stitch design

## Step 1: Initialize shadcn/ui

### New project

```bash
npx shadcn@latest init
```

Follow the prompts:
- **Style:** `default` (rounded, clean) or `new-york` (sharp, minimal)
- **Base color:** `slate` (cool), `zinc` (neutral), `stone` (warm)
- **CSS variables:** Yes (required for Stitch token alignment)

### Existing project

```bash
npx shadcn@latest init
```

This creates `components.json` with your project configuration.

---

## Step 2: Align tokens with Stitch design system

After running `stitch-design-system`, you'll have `design-tokens.css` with the Stitch color palette. Map these to shadcn's CSS variable format in `globals.css`:

```css
/* globals.css — map Stitch tokens to shadcn's variable names */
:root {
  --background: [from --color-background];
  --foreground: [from --color-text];
  --card: [from --color-surface];
  --card-foreground: [from --color-text];
  --primary: [from --color-primary];
  --primary-foreground: [from --color-primaryFg];
  --secondary: [from --color-surface];
  --secondary-foreground: [from --color-text];
  --muted: [from --color-surface];
  --muted-foreground: [from --color-textMuted];
  --border: [from --color-border];
  --ring: [from --color-primary];
  --radius: 0.5rem; /* match Stitch's border-radius scale */
}

.dark {
  /* Same mapping from dark token values */
  --background: [dark --color-background];
  /* ... */
}
```

---

## Step 3: Discover and install components

### Browse components

Use shadcn MCP `list_components` if available, or browse https://ui.shadcn.com/docs/components

### Install individual components

```bash
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add input
npx shadcn@latest add dialog
npx shadcn@latest add dropdown-menu
npx shadcn@latest add table
npx shadcn@latest add select
npx shadcn@latest add badge
npx shadcn@latest add avatar
npx shadcn@latest add tooltip
```

### Install a full block (auth, dashboard, etc.)

shadcn provides pre-built blocks:

```bash
# List available blocks (if MCP available)
# OR browse: https://ui.shadcn.com/blocks

npx shadcn@latest add [block-name]
```

Common blocks: `login-01`, `dashboard-01`, `sidebar-01`, `products-01`, `calendar-01`

---

## Step 4: Replace Stitch HTML elements with shadcn components

| Stitch HTML element | Replace with shadcn |
|---------------------|---------------------|
| `<button>` primary | `<Button>` with default variant |
| `<button>` secondary | `<Button variant="outline">` |
| `<button>` ghost | `<Button variant="ghost">` |
| `<button>` destructive | `<Button variant="destructive">` |
| Card/panel container | `<Card><CardHeader><CardContent>` |
| `<input type="text">` | `<Input>` |
| `<input type="password">` | `<Input type="password">` |
| `<select>` | `<Select><SelectTrigger><SelectContent>` |
| Overlay/popup | `<Dialog><DialogContent>` |
| Context menu | `<DropdownMenu>` |
| Notification badge | `<Badge>` |
| User avatar | `<Avatar><AvatarImage><AvatarFallback>` |
| Data table | `<Table><TableHeader><TableBody>` |
| Navigation tabs | `<Tabs><TabsList><TabsContent>` |
| Alert/banner | `<Alert><AlertDescription>` |

---

## Step 5: Using the `cn()` utility

All shadcn components use `cn()` (clsx + tailwind-merge) for class merging. Keep it in `lib/utils.ts`:

```ts
// src/lib/utils.ts
import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

Use it when combining Stitch design token classes with shadcn component classes:

```tsx
<Button
  className={cn(
    "w-full",                    // Stitch layout
    isLoading && "opacity-50"    // Conditional state
  )}
  style={{ backgroundColor: theme.primary }}  // Stitch token
>
  Sign In
</Button>
```

---

## Customization patterns

### Extend a component variant

```tsx
// src/components/ui/button.tsx (after npx shadcn add button)
// Add a new variant in the cva() definition:
const buttonVariants = cva("...", {
  variants: {
    variant: {
      default: "...",
      outline: "...",
      brand: "bg-[--color-primary] text-[--color-primaryFg] hover:opacity-90",  // ← add this
    },
  },
})
```

### Wrap a component with project-specific props

```tsx
// src/components/PrimaryButton.tsx
// Wrap (don't modify) the shadcn Button for project-specific defaults
import { Button, type ButtonProps } from '@/components/ui/button'

export function PrimaryButton({ children, ...props }: ButtonProps) {
  return (
    <Button variant="default" className="w-full" {...props}>
      {children}
    </Button>
  )
}
```

---

## Accessibility

Radix UI primitives handle most accessibility automatically:
- Keyboard navigation (Tab, Enter, Escape, Arrow keys)
- ARIA attributes (`role`, `aria-expanded`, `aria-haspopup`)
- Focus management (trapping focus in dialogs, restoring focus on close)

When customizing, **do not remove** ARIA attributes or keyboard handlers from the base components. Add to them, don't replace them.

---

## Integration with Stitch workflow

The typical flow:

```
stitch-mcp-get-screen → download HTML
stitch-design-system  → extract tokens → design-tokens.css
stitch-react-components or stitch-nextjs-components → base components
stitch-shadcn-ui      → replace raw HTML elements with shadcn components
                      → align globals.css with design-tokens.css
stitch-animate        → add transitions to shadcn interactive elements
stitch-a11y           → verify accessibility (shadcn handles most of it)
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Import path errors (`@/components/ui/...`) | Check `tsconfig.json` and `vite.config.ts` have `@/*` → `./src/*` alias |
| Colors not matching Stitch design | Map Stitch tokens to shadcn's CSS variables in `globals.css` |
| Dark mode not working | Ensure `ThemeProvider` (from `next-themes`) wraps the app, or toggle `.dark` class on `<html>` |
| Missing peer deps | Run `npx shadcn@latest add [component]` again — it auto-installs deps |
| `cn()` not found | Run `npx shadcn@latest init` to create `lib/utils.ts` |

## References

- shadcn/ui docs: https://ui.shadcn.com/docs
- Radix UI: https://www.radix-ui.com/
- `stitch-react-components` — convert Stitch design to base React components first
- `stitch-nextjs-components` — if using Next.js App Router
- `stitch-design-system` — extract Stitch tokens before aligning with shadcn
