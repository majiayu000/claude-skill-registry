---
name: web-artifacts-builder
description: >-
  Build multi-component React HTML artifacts for claude.ai using Vite, Tailwind
  CSS 3, and shadcn/ui. Use when the user requests interactive dashboards,
  multi-page apps, or any artifact needing state management, routing, or
  shadcn/ui components. Scaffolds the project, develops components, bundles to a
  single self-contained HTML file, and shares it in the conversation.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - WebFetch
metadata:
  version: "1.0.0"
  author: "platxa-skill-generator"
  tags:
    - builder
    - frontend
    - react
    - artifacts
  provenance:
    upstream_source: "web-artifacts-builder"
    upstream_sha: "2f2d0c426d23c3adf37ebe2b29e72df39bc5ea07"
    regenerated_at: "2026-02-04T18:00:00Z"
    generator_version: "1.0.0"
    intent_confidence: 0.58
---

# Web Artifacts Builder

Build elaborate, multi-component claude.ai HTML artifacts with React 18, TypeScript, Tailwind CSS, and shadcn/ui.

## Overview

This skill creates self-contained HTML artifacts from React projects. It scaffolds a Vite + React + TypeScript project with Tailwind CSS and 40+ pre-installed shadcn/ui components, develops the requested UI, bundles everything into a single HTML file via Parcel, and delivers it as a claude.ai artifact.

**What it creates:**
- Interactive dashboards with charts, tables, and filters
- Multi-step forms with validation (react-hook-form + zod)
- Data visualization apps with responsive layouts
- Landing pages with shadcn/ui component compositions
- Any complex frontend artifact requiring state management or routing

**Stack:** React 18 + TypeScript + Vite + Parcel (bundling) + Tailwind CSS 3.4 + shadcn/ui

**Prerequisites:**
- Node.js 18+ (`node -v` to verify)
- pnpm (`npm install -g pnpm` if missing)

## Workflow

### Step 1: Scaffold the Project

Run the init script to create a configured React + Vite project:

```bash
SKILL_DIR="<path-to-this-skill>"
bash "$SKILL_DIR/scripts/init-artifact.sh" my-artifact
cd my-artifact
```

The scaffold includes:
- React 18 + TypeScript via Vite with `@/` path aliases
- Tailwind CSS 3.4.1 with shadcn/ui HSL CSS variable theming
- 40+ shadcn/ui components (Accordion through Tooltip)
- All Radix UI primitives and utility libraries (clsx, tailwind-merge, lucide-react)
- Parcel bundler configuration with TypeScript path resolution

### Step 2: Develop the Artifact

Edit source files under `src/` to build the requested UI.

**Entry point:** `src/App.tsx` -- replace the default content with the artifact's root component.

**Component organization:**
```
src/
  App.tsx              # Root component
  components/
    ui/                # shadcn/ui primitives (pre-installed)
    feature-name.tsx   # Custom feature components
  lib/
    utils.ts           # cn() helper (pre-installed)
  hooks/
    use-feature.ts     # Custom hooks
```

**Import patterns:**
```tsx
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
```

**State management:** Use React built-in hooks (`useState`, `useReducer`, `useContext`) for artifact-scoped state. Avoid external state libraries -- the artifact must be self-contained.

### Step 3: Bundle to Single HTML

Bundle the entire React app into one self-contained HTML file:

```bash
bash "$SKILL_DIR/scripts/bundle-artifact.sh"
```

This produces `bundle.html` with all JavaScript, CSS, and dependencies inlined. The file works standalone in any browser with no external requests.

**How bundling works:**
1. Installs Parcel + html-inline as dev dependencies
2. Creates `.parcelrc` with `parcel-resolver-tspaths` for `@/` alias support
3. Runs `parcel build index.html --no-source-maps` to produce optimized dist/
4. Runs `html-inline dist/index.html` to inline all assets into `bundle.html`

### Step 4: Share the Artifact

Read `bundle.html` and present it to the user as a claude.ai artifact. The user can view and interact with it directly in the conversation.

### Step 5: Iterate (if needed)

If the user requests changes:
1. Edit the relevant `src/` files
2. Re-run `bash "$SKILL_DIR/scripts/bundle-artifact.sh"`
3. Share the updated `bundle.html`

For visual testing before sharing, open `bundle.html` in a browser or use Playwright.

## Design Guidelines

Avoid common AI-generated visual patterns ("AI slop"):

| Avoid | Instead Use |
|-------|-------------|
| Centered everything | Asymmetric layouts, left-aligned content |
| Purple/blue gradients | Neutral palettes, single accent color |
| Uniform rounded corners | Mix sharp and rounded based on hierarchy |
| Inter font everywhere | System font stack or a single chosen typeface |
| Excessive drop shadows | Subtle borders, background contrast |
| Stock hero illustrations | Functional UI, real data patterns |

Use the shadcn/ui theming system (`--background`, `--foreground`, `--primary`, etc.) to maintain consistent color through CSS variables. See `references/design-patterns.md` for component composition recipes.

## Available Components

All 40+ shadcn/ui components are pre-installed. Commonly used:

| Component | Import Path | Use For |
|-----------|-------------|---------|
| Button | `@/components/ui/button` | Actions, CTAs |
| Card | `@/components/ui/card` | Content containers |
| Dialog | `@/components/ui/dialog` | Modal overlays |
| Form | `@/components/ui/form` | react-hook-form integration |
| Select | `@/components/ui/select` | Dropdown selection |
| Table | `@/components/ui/table` | Data display |
| Tabs | `@/components/ui/tabs` | Content organization |
| Toast/Sonner | `@/components/ui/sonner` | Notifications |
| Sheet | `@/components/ui/sheet` | Side panels |
| Command | `@/components/ui/command` | Command palette (cmdk) |

Full component list and props: `references/shadcn-components.md`

## Examples

### Example 1: Interactive Dashboard

```
User prompt: Build a sales dashboard with monthly revenue chart,
             top products table, and KPI cards

Steps taken:
  1. bash scripts/init-artifact.sh sales-dashboard
  2. Create src/components/kpi-card.tsx using Card + custom metrics
  3. Create src/components/revenue-chart.tsx with SVG bar chart
  4. Create src/components/products-table.tsx using Table component
  5. Wire everything in src/App.tsx with CSS grid layout
  6. bash scripts/bundle-artifact.sh
  7. Share bundle.html (142 KB)
```

### Example 2: Multi-step Form

```
User prompt: Create a job application form with personal info,
             experience, and review steps

Steps taken:
  1. bash scripts/init-artifact.sh job-form
  2. Create src/components/form-steps.tsx with useReducer for step state
  3. Use Form, Input, Select, Textarea from shadcn/ui
  4. Add zod schema validation per step
  5. bash scripts/bundle-artifact.sh
  6. Share bundle.html (98 KB)
```

### Example 3: Data Explorer

```
User prompt: Build a filterable data table with search, column sorting,
             and pagination

Steps taken:
  1. bash scripts/init-artifact.sh data-explorer
  2. Create src/hooks/use-table-state.ts for sort/filter/page state
  3. Create src/components/data-table.tsx using Table + Input + Select
  4. Add Command component for quick column search
  5. bash scripts/bundle-artifact.sh
  6. Share bundle.html (87 KB)
```

## Output Checklist

After each artifact build, verify:

- [ ] `bundle.html` exists and is non-empty
- [ ] File opens correctly in a browser (no blank page)
- [ ] All interactive elements respond to clicks and input
- [ ] Layout is responsive (resize browser to test)
- [ ] No console errors in browser DevTools
- [ ] Styling matches the design guidelines (no AI slop patterns)
- [ ] Dark mode works if theme toggle is included
- [ ] All shadcn/ui components render with correct theming
- [ ] Bundle size is reasonable (under 500 KB for most artifacts)
- [ ] No external network requests (fully self-contained)

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `pnpm: command not found` | Run `npm install -g pnpm` |
| Node.js version < 18 | Upgrade Node.js; Vite 6+ requires Node 20+ |
| Parcel build fails with path alias error | Verify `.parcelrc` includes `parcel-resolver-tspaths` |
| `bundle.html` shows blank page | Check browser console; likely a missing import or build error |
| Tailwind classes not applied | Verify `tailwind.config.js` content paths include `./src/**/*.{ts,tsx}` |
| shadcn/ui component missing | Components are in `src/components/ui/`; check import path uses `@/` |
| Bundle too large (> 1 MB) | Remove unused dependencies; check for accidentally bundled assets |
| TypeScript `@/` not resolving | Verify `tsconfig.json` has `baseUrl` and `paths` configured |
| Dark mode not working | Ensure `darkMode: ["class"]` in `tailwind.config.js` and ThemeProvider wraps App |