---
name: pen-code
description: Use when generating code from a Pencil (.pen) design, syncing code to a .pen file, or aligning an implementation with .pen changes.
---

# Pencil <> Code

Generate code from .pen designs or sync design changes into existing implementations. The core knowledge — how .pen properties map to React/Tailwind — is the same in both directions.

## The Cardinal Rule

**Pencil variables map 1:1 to Tailwind semantic utilities. Never use arbitrary values.**

```
WRONG                           RIGHT
─────                           ─────
bg-[#3b82f6]                    bg-primary
text-[var(--primary)]           text-primary
rounded-[6px]                   rounded-md
gap-[16px]                      gap-4
p-[24px]                        p-6
```

If a .pen variable exists for a value, there's a corresponding semantic Tailwind utility. Use it.

## Property Mapping

### Layout
```
.pen                            Tailwind
────                            ───────
layout: "vertical"              flex flex-col
layout: "horizontal"            flex (flex-row)
layout: "grid"                  grid
layout: "none"                  relative (children absolute)
alignItems: "center"            items-center
justifyContent: "space-between" justify-between
width: "fill_container"         w-full or flex-1
height: "fill_container"        h-full or flex-1
```

### Spacing (8-point grid)
```
gap/padding value    Tailwind
─────────────────    ───────
4                    1
8                    2
12                   3
16                   4
20                   5
24                   6
32                   8
```

Asymmetric padding: `[T,R,B,L]` → `py-T px-R` (when T=B and R=L) or explicit per-side.

### Typography
```
fontSize    Tailwind        fontWeight    Tailwind
────────    ───────         ──────────    ───────
12          text-xs         400           font-normal
14          text-sm         500           font-medium
16          text-base       600           font-semibold
18          text-lg         700           font-bold
20          text-xl
24          text-2xl
30          text-3xl
36          text-4xl
48          text-5xl
```

### Colors (via variables)
```
.pen variable       bg-*              text-*                border-*
─────────────       ────              ──────                ────────
primary             bg-primary        text-primary          border-primary
primary-foreground  —                 text-primary-foreground  —
background          bg-background     —                     —
foreground          —                 text-foreground       —
card                bg-card           —                     —
card-foreground     —                 text-card-foreground  —
muted               bg-muted          —                     —
muted-foreground    —                 text-muted-foreground —
border              —                 —                     border-border
destructive         bg-destructive    text-destructive      border-destructive
```

### Radius (via variables)
```
radius-sm → rounded-sm    radius-lg → rounded-lg
radius-md → rounded-md    radius-xl → rounded-xl
```

Asymmetric: `cornerRadius: [TL,TR,BR,BL]` → `rounded-tl-* rounded-tr-* rounded-br-* rounded-bl-*`

### Node Type → React Element
```
.pen node type      React output
──────────────      ────────────
frame + layout      <div className="flex ...">
frame + reusable    Extract as component
text (32px+ bold)   <h1>–<h3>
text (20-28px)      <h4>–<h6>
text (body)         <p>
text (label/inline) <span>
ref (instance)      <ComponentName />
rectangle           <div> with fill
ellipse             <div className="rounded-full">
image               <img> or background-image
```

### Icons (Material → Lucide)
```
search → <Search />         arrow_forward → <ArrowRight />
close → <X />               person → <User />
menu → <Menu />             settings → <Settings />
home → <Home />             notifications → <Bell />
add → <Plus />              check → <Check />
edit → <Pencil />           delete → <Trash2 />
chevron_right → <ChevronRight />  favorite → <Heart />
```

All Lucide icons accept `className` for sizing: `<Search className="size-4" />`

## Mode: Export (Full Code Generation)

Generate from scratch when no implementation exists.

1. Read design tokens: `get_variables` → generate `@theme` block with `--color-*` and `--radius-*` prefixes
2. Read design tree: `batch_get` with sufficient `readDepth`
3. Read reusable components: `batch_get` with `{ reusable: true }` → map to shadcn/ui components
4. Generate code using semantic Tailwind classes, TypeScript, React 19 patterns (no `forwardRef`)

### Theme Generation
```css
@import "tailwindcss";

@theme {
  --color-primary: oklch(...);     /* from .pen "primary" variable */
  --color-background: oklch(...);  /* from .pen "background" variable */
  --radius-md: 0.375rem;           /* from .pen "radius-md" variable */
}
```

Colors MUST use `--color-*` prefix, radii MUST use `--radius-*` prefix — this is how Tailwind v4 auto-generates semantic utilities.

### Component Patterns
- Reusable .pen components with variants → CVA (`class-variance-authority`)
- Class merging → `cn()` from `@/lib/utils`
- Pencil component → shadcn/ui when a match exists (Button, Card, Input, Badge, Avatar, Dialog, Tabs, Table, etc.)
- Custom components when no shadcn/ui match → same CVA + cn() conventions

### Responsive (Multi-Artboard)
When .pen has artboards at multiple widths: generate mobile-first, add `md:`/`lg:` prefixes for larger breakpoints. Never hardcode artboard pixel widths.

## Mode: Sync (Incremental Updates)

Update existing code to match design changes. **The design is the source of truth.**

### Protected Code

These code regions have no design counterpart — never modify them during sync:
- Event handlers, React hooks, state management
- Conditional rendering logic, API calls, navigation
- Animation/transition code not represented in .pen

Only modify: JSX structure, `className` values, text content, asset references.

### Diff Systematically

Compare design and code in this order (most commonly missed first):

1. **Assets** — image format mismatches (`.jpg` vs `.png`), missing files, wrong paths
2. **Design tokens** — new, changed, or removed variables vs CSS custom properties
3. **Screen structure** — layout direction, alignment, gap, padding, typography, colors, icons, children count/order
4. **Cross-screen patterns** — shared components that changed, affecting multiple screens

### Report Before Editing

Output a structured diff report before making any changes:
```
## Design Sync Report
### Token Changes
- Added: --new-variable: #value
- Changed: --existing: #old → #new
### Screen: [Name]
- [file:line] property: old → new
- [file:line] added: new element
```

### Dead Code Cleanup

If the design removed something, the code must too:
- Deleted screens → remove component file + route
- Orphaned components → grep for imports, remove if zero
- Removed variables → remove CSS declaration, grep for `var()` references
- Unused imports → clean up after removing components

## Parallelization

For multi-screen projects, don't process sequentially — fan out after establishing shared context.

### Export: Parallel Code Generation

**Orchestrator setup** (sequential — shared dependencies):
1. Read design tokens (`get_variables`) → generate the `@theme` CSS block
2. Read reusable components (`batch_get` with `{ reusable: true }`) → identify shared component mappings (which Pencil components → which shadcn/ui components)
3. Read all screen frames (top-level `batch_get`)

**Then spawn a teammate per screen.** Each gets:
- The generated `@theme` block
- The component mapping table
- The property mapping reference (from this skill)
- Their specific screen's node tree (read with full depth)
- Target file path

Each teammate generates its screen component independently. The orchestrator reviews outputs and handles cross-screen deduplication (shared components that multiple teammates extracted).

### Sync: Parallel Diff + Apply

**Orchestrator setup** (sequential):
1. Read all design tokens — token changes affect everything
2. Identify which screens changed (or read all if unclear)
3. Read the existing code inventory

**Then spawn a teammate per modified screen.** Each gets:
- The token diff (new/changed/removed variables)
- Their screen's design tree (resolved)
- Their screen's current code file
- The protected code principle
- The property mapping reference

Each teammate produces a diff report and applies changes. The orchestrator consolidates reports and handles dead code cleanup (orphaned files, routes, imports) which requires cross-screen awareness.

### When to Parallelize

- **2+ screens** in export or sync → parallelize
- **Single screen** → not worth the overhead
- **Token-only changes** (no screen structure changes) → single agent, apply to CSS file directly
- **Tightly coupled screens** (shared state, navigation flow) → consider sequential for consistency

## Pencil-Specific Gotchas

- `fill` on text nodes → text color (`text-*`), not background (`bg-*`)
- `textGrowth: "fixed-width"` → set explicit width on the element
- `fill: "$variable"` → `bg-[var(--variable)]` (only when no semantic utility exists)
- `stroke.fill` + `stroke.thickness` → `border-[Npx] border-[var(--color)]`
- Padding arrays: `[T,R,B,L]` — watch the array length (1, 2, or 4 values)
- Image format: design references `.png`, code imports `.jpg` — always verify
- `cornerRadius: [3,24,24,24]` → needs explicit per-corner rounded syntax
