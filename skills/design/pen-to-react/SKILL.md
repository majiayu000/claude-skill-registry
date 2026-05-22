---
name: pen-to-react
description: >
  Convert .pen design files into React components for the Synnovator frontend.
  Two-phase workflow: (1) Extract reusable base UI components from .pen designs
  into frontend/components/ui/, (2) Compose full page components using those
  base components in frontend/components/pages/. Elements not worth extracting
  are inlined directly into the page component.
  Use when:
  (1) Converting a .pen design file into React page and UI components
  (2) Adding a new page component based on a .pen design
  (3) Updating existing components to match revised .pen designs
  (4) Extracting reusable UI patterns from .pen into shared components
---

# Pen to React

Convert Pencil (.pen) design files into production React components for the Synnovator platform.

## Prerequisites

- `.pen` design files in `specs/ui/components/` (one per page)
- Design system references in `specs/ui/style.pen` and `specs/ui/basic.pen`
- Frontend project at `frontend/` with Next.js 14, Tailwind v4, shadcn/ui

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Next.js 14 (App Router) |
| Language | TypeScript |
| Styling | Tailwind CSS v4 (`@import "tailwindcss"`) |
| UI Library | shadcn/ui (Radix UI primitives) |
| Icons | lucide-react |
| Fonts | Space Grotesk (heading), Inter (body), Poppins (mono), Noto Sans SC (Chinese) |
| Theme | Neon Forge dark theme |

## Theme Tokens (CSS Variables)

All colors MUST use CSS variables — never hardcode hex values in components.

```
--nf-lime: #BBFD3B        (primary accent)
--nf-surface: #00000E     (deepest background)
--nf-near-black: #181818  (page background)
--nf-card-bg: #222222     (card/panel background)
--nf-dark-bg: #333333     (borders, secondary background)
--nf-muted: #8E8E8E       (muted text, icons)
--nf-light-gray: #DCDCDC  (secondary text)
--nf-white: #FFFFFF        (primary text)
--nf-error: #FA541C       --nf-success: #74FFBB
--nf-warning: #FAAD14     --nf-cyan: #41FAF4
--nf-blue: #4C78FF        --nf-pink: #FF74A7
--nf-orange: #FB7A38
```

Font utility classes (defined in `globals.css` via `@theme inline`):
- `font-heading` → Space Grotesk
- `font-body` → Inter
- `font-mono` → Poppins
- `font-chinese` → Noto Sans SC

## Output Structure

```
frontend/components/
├── ui/             # Reusable base components (shadcn + custom extracted)
│   ├── button.tsx        # (existing shadcn)
│   ├── card.tsx          # (existing shadcn)
│   ├── avatar.tsx        # (existing shadcn)
│   ├── badge.tsx         # (existing shadcn)
│   ├── tabs.tsx          # (existing shadcn)
│   ├── ...               # other existing shadcn components
│   └── stat-card.tsx     # (example: newly extracted from .pen)
├── pages/          # Full page components composed from ui/ components
│   ├── home.tsx
│   ├── post-list.tsx
│   ├── post-detail.tsx
│   ├── proposal-list.tsx
│   ├── proposal-detail.tsx
│   ├── category-detail.tsx
│   ├── user-profile.tsx
│   ├── team.tsx
│   ├── assets.tsx
│   └── following-list.tsx
└── interactive/    # Client components for user interactions (future)
```

## Workflow

### Phase 1: Analyze the .pen Design

#### 1.1 Open and Read the Design

Use Pencil MCP tools to read the .pen file:

```
1. Open the document:
   open_document("specs/ui/components/{page-name}.pen")

2. Get editor state to understand structure:
   get_editor_state(include_schema=false)

3. Read the top-level frame and its full tree:
   batch_get(readDepth=10)

4. If the design has reusable components:
   batch_get(patterns=[{reusable: true}], readDepth=3, searchDepth=5)

5. Take a screenshot for visual reference:
   get_screenshot(nodeId="{top-frame-id}")
```

#### 1.2 Identify Extractable UI Components

Analyze the design tree and identify elements that should be extracted into `components/ui/`:

**Extract as reusable component IF:**
- The element appears 2+ times in this design OR across multiple pages
- It is marked as `reusable: true` in the .pen file
- It has a clear, generic purpose (card, stat display, avatar group, etc.)
- It maps to a recognizable UI pattern (list item, grid card, header section)

**Inline directly into page component IF:**
- The element appears only once and is page-specific
- It is a simple layout wrapper (section container, spacer)
- Extracting would create a component with too many props to be useful

#### 1.3 Check Existing Components

Before creating new components, check what already exists:

```
frontend/components/ui/
├── avatar.tsx    → Avatar, AvatarFallback (Radix-based)
├── badge.tsx     → Badge with variant support
├── button.tsx    → Button with size/variant (CVA-based)
├── card.tsx      → Card, CardHeader, CardContent, CardFooter, CardTitle, CardDescription
├── dropdown-menu.tsx → DropdownMenu (Radix-based)
├── input.tsx     → Input
├── scroll-area.tsx → ScrollArea (Radix-based)
├── separator.tsx → Separator
├── tabs.tsx      → Tabs, TabsList, TabsTrigger, TabsContent (Radix-based)
├── tooltip.tsx   → Tooltip (Radix-based)
```

If a design element maps to an existing shadcn component, USE the existing component — do not recreate it.

### Phase 2: Extract Base UI Components

For each element identified as extractable in Phase 1:

#### 2.1 Extract Component Definition from .pen

```
1. Read the component node with full depth:
   batch_get(nodeIds=["{component-id}"], readDepth=5)

2. If it contains path geometry (SVGs, icons):
   batch_get(nodeIds=["{component-id}"], includePathGeometry=true)

3. Take a screenshot for visual reference:
   get_screenshot(nodeId="{component-id}")
```

#### 2.2 Create the React Component

Follow these rules when translating .pen nodes to React:

**Node Type Mapping:**

| .pen node type | React element |
|---------------|--------------|
| `frame` (layout: horizontal) | `<div className="flex">` |
| `frame` (layout: vertical) | `<div className="flex flex-col">` |
| `frame` (layout: none) | `<div className="relative">` |
| `text` | `<span>` or `<p>` or `<h1>`-`<h6>` |
| `rectangle` | `<div>` with sizing and fill |
| `ellipse` | `<div className="rounded-full">` |
| `path` | `<svg><path d="..."/></svg>` |
| `icon_font` | `<IconName>` from lucide-react |
| `ref` (component instance) | `<ComponentName {...overrides}>` |

**Sizing Translation:**

| .pen value | Tailwind class |
|-----------|---------------|
| `width: "fill_container"` | `w-full` or `flex-1` (in flex context) |
| `height: "fill_container"` | `h-full` or `flex-1` (in flex context) |
| `width: "fit_content"` | `w-fit` |
| `height: "fit_content"` | `h-fit` |
| `width: N` (number) | `w-[Npx]` |
| `height: N` (number) | `h-[Npx]` |

**Color Translation:**
Always use CSS variables from the Neon Forge theme:

| .pen fill/color | Tailwind class |
|----------------|---------------|
| `#BBFD3B` | `bg-[var(--nf-lime)]` or `text-[var(--nf-lime)]` |
| `#181818` | `bg-[var(--nf-near-black)]` |
| `#222222` | `bg-[var(--nf-card-bg)]` |
| `#333333` | `bg-[var(--nf-dark-bg)]` or `border-[var(--nf-dark-bg)]` |
| `#8E8E8E` | `text-[var(--nf-muted)]` |
| `#DCDCDC` | `text-[var(--nf-light-gray)]` |
| `#FFFFFF` | `text-[var(--nf-white)]` |

**Typography Translation:**

| .pen font | Tailwind class |
|----------|---------------|
| Space Grotesk | `font-heading` |
| Inter | `font-body` |
| Poppins | `font-mono` |
| Noto Sans SC | `font-chinese` |
| `fontSize: N` | `text-[Npx]` |
| `fontWeight: "bold"` | `font-bold` |
| `fontWeight: "semibold"` | `font-semibold` |
| `fontWeight: "medium"` | `font-medium` |

**Spacing Translation:**

| .pen property | Tailwind class |
|--------------|---------------|
| `gap: N` | `gap-[Npx]` (or `gap-N` if matches scale) |
| `padding: N` | `p-[Npx]` |
| `padding: [top, right, bottom, left]` | `pt-[] pr-[] pb-[] pl-[]` |
| `cornerRadius: [N,N,N,N]` | `rounded-[Npx]` |

#### 2.3 Component File Template

```typescript
// frontend/components/ui/{component-name}.tsx
import { cn } from "@/lib/utils"

interface {ComponentName}Props {
  // Props derived from .pen instance overrides
  className?: string
}

export function {ComponentName}({ className, ...props }: {ComponentName}Props) {
  return (
    <div className={cn(
      // Base styles from .pen component definition
      "...",
      className
    )}>
      {/* Children from .pen component tree */}
    </div>
  )
}
```

#### 2.4 Validate Component

After creating each component:

1. Compare the component's visual output against the .pen screenshot
2. Verify all CSS variables are correctly mapped
3. Ensure the component accepts the right props for all .pen instance overrides
4. Check that existing shadcn components are reused where applicable

### Phase 3: Compose Page Component

#### 3.1 Build the Full Page

Assemble the page component from:
- Extracted base components from Phase 2
- Existing shadcn/ui components
- Inlined elements (not worth extracting)
- lucide-react icons

**Page Component Template:**

```typescript
// frontend/components/pages/{page-name}.tsx
"use client"

import { /* icons */ } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
// ... other imports

// Mock data (to be replaced by API calls via openapi-to-components skill)
const mockData = [...]

export function {PageName}() {
  return (
    <div className="flex flex-col h-screen bg-[var(--nf-near-black)]">
      {/* Header */}
      <header className="flex items-center justify-between h-14 px-6 border-b border-[var(--nf-dark-bg)] bg-[var(--nf-near-black)]">
        {/* ... */}
      </header>

      {/* Body */}
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <aside className="w-[60px] bg-[var(--nf-near-black)] flex flex-col items-center pt-4 gap-4">
          {/* ... */}
        </aside>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto px-8 py-6 flex flex-col gap-6">
          {/* Page-specific content */}
        </main>
      </div>
    </div>
  )
}
```

#### 3.2 Shared Layout Elements

Every page shares these layout elements (translate from .pen consistently):

**Global Header:**
- Height: `h-14` (56px)
- Background: `bg-[var(--nf-near-black)]`
- Border bottom: `border-b border-[var(--nf-dark-bg)]`
- Contains: hamburger menu, logo text "协创者", search bar, action button, notifications, avatar

**Left Sidebar (Icon-only):**
- Width: `w-[60px]`
- Icons: Compass, Globe, Mountain (from lucide-react)
- Icon color: `text-[var(--nf-muted)]`

**Main Content Area:**
- `flex-1 overflow-y-auto`
- Padding: `px-8 py-6`
- Vertical layout: `flex flex-col gap-6`

#### 3.3 Mock Data Pattern

Page components initially use hardcoded mock data. Use `const` declarations at the top of the file:

```typescript
// Mock data — will be replaced by API integration
const cards = [
  { id: 1, title: "...", author: "..." },
  // ...
]
```

This mock data will later be replaced by real API calls when the `openapi-to-components` skill is applied.

### Phase 4: Visual Validation

After composing the page component:

1. **Screenshot Comparison:**
   ```
   get_screenshot(nodeId="{page-frame-id}")
   ```
   Compare design screenshot against the rendered React component.

2. **Checklist:**
   - [ ] All text content matches the .pen labels exactly (including Chinese text)
   - [ ] All icons match (lucide-react equivalents)
   - [ ] Colors use CSS variables, not hardcoded hex
   - [ ] Spacing (gap, padding) matches .pen values
   - [ ] Border radius matches .pen cornerRadius
   - [ ] Typography (font family, size, weight) matches
   - [ ] Layout structure (flex direction, alignment) matches
   - [ ] Responsive behavior: `fill_container` → `flex-1`/`w-full`/`h-full`
   - [ ] No inline styles — all styling via Tailwind classes
   - [ ] Existing shadcn components used where applicable

3. **TypeScript Verification:**
   ```bash
   cd frontend && npx tsc --noEmit
   ```

## Component-to-Page Mapping

| .pen Design File | Page Component | Key UI Components Used |
|-----------------|---------------|----------------------|
| `home.pen` | `home.tsx` | Card, Badge, Avatar, Tabs |
| `post-list.pen` | `post-list.tsx` | Card, Badge, Tabs |
| `post-detail.pen` | `post-detail.tsx` | Card, Badge, Avatar, ScrollArea |
| `proposal-list.pen` | `proposal-list.tsx` | Card, Badge, Tabs |
| `proposal-detail.pen` | `proposal-detail.tsx` | Card, Badge, Avatar, Tabs |
| `category-detail.pen` | `category-detail.tsx` | Card, Badge, Tabs |
| `user-profile.pen` | `user-profile.tsx` | Card, Avatar, Badge, Tabs |
| `team.pen` | `team.tsx` | Card, Avatar, Badge, Tabs |
| `assets.pen` | `assets.tsx` | Card, Badge, DropdownMenu |
| `following-list.pen` | `following-list.tsx` | Card, Avatar, Badge |

## Conventions

### Naming

- Component files: `kebab-case.tsx` (e.g., `stat-card.tsx`)
- Component exports: `PascalCase` (e.g., `StatCard`)
- Props interfaces: `{ComponentName}Props`
- CSS variable references: `var(--nf-{token-name})`

### Imports

```typescript
// 1. React/Next.js imports
import { useState } from "react"

// 2. Icon imports
import { Menu, Search, Zap } from "lucide-react"

// 3. UI component imports (shadcn)
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"

// 4. Custom UI component imports
import { StatCard } from "@/components/ui/stat-card"

// 5. Type imports
import type { Post } from "@/lib/types"
```

### Decision Tree: Extract vs Inline

```
Is the element used in 2+ pages?
├─ YES → Extract to components/ui/
└─ NO
   ├─ Is it a recognizable UI pattern (card variant, stat display, etc.)?
   │  ├─ YES → Extract to components/ui/ (likely reusable later)
   │  └─ NO
   │     ├─ Is it a complex sub-section with its own layout?
   │     │  ├─ YES → Consider extraction for readability
   │     │  └─ NO → Inline in page component
   │     └─ Is the element a simple wrapper or spacer?
   │        └─ YES → Inline in page component
   └─ Is the element already available as shadcn/ui component?
      └─ YES → Use existing shadcn component directly
```

## SVG and Path Handling

When a .pen design contains `path` nodes (custom shapes, logos):

1. Extract exact geometry using `batch_get` with `includePathGeometry=true`
2. Use the `geometry` string directly as the SVG `d` attribute
3. Set `viewBox="0 0 {width} {height}"` from the node dimensions
4. Apply fill/stroke via Tailwind: `fill-[var(--nf-lime)]`, `stroke-[var(--nf-dark-bg)]`
5. Never approximate or simplify path data

```tsx
<svg className="w-6 h-6" viewBox="0 0 24 24">
  <path
    d="{exact geometry from .pen}"
    className="fill-[var(--nf-lime)]"
  />
</svg>
```

## Integration with Other Skills

This skill generates **initial component code with mock data**. After running this skill:

1. **`openapi-to-components`** replaces mock data with real API calls:
   - Converts `"use client"` pages to async Server Components
   - Adds API fetch functions from `lib/api/*.ts`
   - Extracts interactive elements to `components/interactive/`

2. **`synnovator`** manages the underlying data model that the API serves

The recommended order is:
```
pen-to-react → openapi-to-components → (deploy)
```
