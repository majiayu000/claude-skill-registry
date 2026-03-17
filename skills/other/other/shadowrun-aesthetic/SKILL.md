---
name: shadowrun-aesthetic
description: Applies Shadowrun cyberpunk aesthetic to UI components. Use when building character sheets, creation cards, gear panels, modal dialogs, or any SR-themed interface elements. Combines systematic craft principles with the distinctive visual language of the Sixth World.
allowed-tools: Read, Grep, Glob
---

# Shadowrun UI Aesthetic

This skill guides the creation of distinctive, production-grade UI that captures the cyberpunk aesthetic of Shadowrun while maintaining the usability required for a character management tool.

## Design Philosophy

**The Sixth World aesthetic**: Corporate sleek meets street grit. Neon-lit interfaces emerging from darkness. Information density without visual clutter. Technology that feels both advanced and worn.

**Balance two forces:**

1. **Precision & Density** - Users spend hours in character creation; every pixel matters
2. **Cyberpunk Atmosphere** - The UI should feel like a runner's commlink interface

## Color System

### Primary Palette (Dark Mode Dominant)

```css
/* Backgrounds - layered darkness */
--bg-base: #09090b; /* zinc-950 - deepest layer */
--bg-elevated: #18181b; /* zinc-900 - cards, panels */
--bg-surface: #27272a; /* zinc-800 - interactive surfaces */
--bg-hover: #3f3f46; /* zinc-700 - hover states */

/* Text hierarchy */
--text-primary: #fafafa; /* zinc-50 - headings, important */
--text-secondary: #a1a1aa; /* zinc-400 - body text */
--text-muted: #71717a; /* zinc-500 - labels, hints */

/* Borders */
--border-subtle: #27272a; /* zinc-800 */
--border-default: #3f3f46; /* zinc-700 */
--border-emphasis: #52525b; /* zinc-600 */
```

### Accent Colors (Signature Shadowrun)

```css
/* Matrix Green - Primary accent for tech/positive */
--accent-matrix: #00ff41;
--accent-matrix-dim: #00cc34;
--accent-matrix-glow: rgba(0, 255, 65, 0.15);

/* Corp Blue - Secondary accent, professional */
--accent-corp: #0ea5e9; /* sky-500 */
--accent-corp-dim: #0284c7;

/* Warning/Danger */
--accent-warning: #f59e0b; /* amber-500 */
--accent-danger: #ef4444; /* red-500 */

/* Magic Purple - For awakened content */
--accent-magic: #a855f7; /* purple-500 */

/* Resonance Cyan - For technomancer content */
--accent-resonance: #22d3ee; /* cyan-400 */
```

### Usage Guidelines

- **Matrix green** for: success states, positive qualities, essence, magic rating
- **Corp blue** for: links, selected states, primary actions
- **Warning amber** for: budget overruns, caution states, negative qualities
- **Danger red** for: errors, forbidden items, damage
- **Magic purple** for: spells, rituals, foci, astral content
- **Resonance cyan** for: complex forms, sprites, matrix content

## Typography

### Font Stack

```css
/* Body/UI - Clean, technical */
font-family:
  ui-sans-serif,
  system-ui,
  -apple-system,
  sans-serif;

/* Stats & Numbers - ALWAYS monospace */
font-family: ui-monospace, "SF Mono", "Fira Code", monospace;
```

### Hierarchy Rules

1. **Card titles**: `text-lg font-semibold` - zinc-100
2. **Section headers**: `text-sm font-medium uppercase tracking-wide` - zinc-400
3. **Body text**: `text-sm` - zinc-300
4. **Labels**: `text-xs font-medium` - zinc-500
5. **Stats/Numbers**: `font-mono text-base font-bold` - zinc-100

### Critical Rule: Monospace for Data

All numerical data MUST use monospace:

- Attribute values (BOD: 4)
- Skill ratings
- Costs (nuyen, karma, essence)
- Dice pools
- Damage codes

## Spacing & Grid

### 4px Base Grid

All spacing uses multiples of 4px:

- `gap-1` (4px) - between inline elements
- `gap-2` (8px) - between related items
- `gap-3` (12px) - between sections within a card
- `gap-4` (16px) - between cards
- `p-4` (16px) - card padding
- `p-3` (12px) - compact card padding

### Card Patterns

```tsx
// Standard creation card
<div className="rounded-lg border border-zinc-800 bg-zinc-900 p-4">
  <div className="mb-3 flex items-center justify-between">
    <h3 className="text-lg font-semibold text-zinc-100">Card Title</h3>
    <button className="text-sky-400 hover:text-sky-300">Action</button>
  </div>
  {/* Content */}
</div>

// Elevated/modal surfaces
<div className="rounded-lg border border-zinc-700 bg-zinc-800 p-4 shadow-xl">
```

## Component Patterns

### Stat Blocks

```tsx
// Attribute display - grid-based, monospace values
<div className="grid grid-cols-3 gap-2">
  <div className="rounded border border-zinc-700 bg-zinc-800 p-2 text-center">
    <div className="text-xs font-medium uppercase text-zinc-500">BOD</div>
    <div className="font-mono text-xl font-bold text-zinc-100">4</div>
  </div>
</div>
```

### Budget/Progress Bars

```tsx
// Essence/Karma/Nuyen tracking
<div className="rounded-lg border border-zinc-700 bg-zinc-800 p-3">
  <div className="flex justify-between text-sm">
    <span className="text-zinc-400">Essence</span>
    <span className="font-mono font-bold text-emerald-400">5.4 / 6.0</span>
  </div>
  <div className="mt-2 h-2 overflow-hidden rounded-full bg-zinc-700">
    <div className="h-full bg-emerald-500" style={{ width: '90%' }} />
  </div>
</div>

// Over-budget state
<div className="rounded-lg border border-amber-800 bg-amber-900/20 p-3">
  <span className="font-mono font-bold text-amber-400">-15 Karma</span>
</div>
```

### List Items (Skills, Gear, Qualities)

```tsx
// Compact list row
<div className="flex items-center justify-between rounded px-2 py-1.5 hover:bg-zinc-800">
  <div className="flex items-center gap-2">
    <span className="text-sm text-zinc-200">Firearms</span>
    <span className="text-xs text-zinc-500">(Pistols)</span>
  </div>
  <span className="font-mono text-sm font-bold text-zinc-100">6</span>
</div>

// With rating controls
<div className="flex items-center gap-2">
  <button className="rounded p-1 text-zinc-400 hover:bg-zinc-700 hover:text-zinc-200">
    <Minus className="h-4 w-4" />
  </button>
  <span className="w-8 text-center font-mono font-bold">4</span>
  <button className="rounded p-1 text-zinc-400 hover:bg-zinc-700 hover:text-zinc-200">
    <Plus className="h-4 w-4" />
  </button>
</div>
```

### Modals

```tsx
// Modal overlay - use React Aria for accessibility
<div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm">
  <div className="max-h-[85vh] w-full max-w-2xl overflow-hidden rounded-lg border border-zinc-700 bg-zinc-900 shadow-2xl">
    {/* Header */}
    <div className="flex items-center justify-between border-b border-zinc-800 p-4">
      <h2 className="text-lg font-semibold text-zinc-100">Modal Title</h2>
      <button className="rounded p-1 text-zinc-400 hover:bg-zinc-800 hover:text-zinc-200">
        <X className="h-5 w-5" />
      </button>
    </div>
    {/* Content */}
    <div className="max-h-[60vh] overflow-y-auto p-4">{/* Scrollable content */}</div>
    {/* Footer */}
    <div className="flex justify-end gap-2 border-t border-zinc-800 p-4">
      <button className="rounded-lg bg-zinc-700 px-4 py-2 text-sm font-medium text-zinc-200 hover:bg-zinc-600">
        Cancel
      </button>
      <button className="rounded-lg bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-500">
        Confirm
      </button>
    </div>
  </div>
</div>
```

### Category Tabs

```tsx
// Gear/Equipment category selection
<div className="flex gap-1 rounded-lg border border-zinc-700 bg-zinc-800 p-1">
  <button className="rounded-md bg-sky-600 px-3 py-1.5 text-sm font-medium text-white">
    Weapons
  </button>
  <button className="rounded-md px-3 py-1.5 text-sm font-medium text-zinc-400 hover:bg-zinc-700 hover:text-zinc-200">
    Armor
  </button>
  <button className="rounded-md px-3 py-1.5 text-sm font-medium text-zinc-400 hover:bg-zinc-700 hover:text-zinc-200">
    Cyberware
  </button>
</div>
```

## Cyberpunk Accents (Use Sparingly)

### Subtle Glow Effects

```tsx
// For selected/active states only
<div className="border-sky-500 shadow-[0_0_10px_rgba(14,165,233,0.3)]">

// For important values (essence, magic)
<span className="text-emerald-400 drop-shadow-[0_0_4px_rgba(52,211,153,0.5)]">
```

### Tech Panel Borders

```tsx
// Accent corner for "high-tech" feel
<div className="relative rounded-lg border border-zinc-700 bg-zinc-900">
  <div className="absolute -top-px left-4 h-px w-8 bg-sky-500" />
  <div className="absolute -left-px top-4 h-8 w-px bg-sky-500" />
  {/* Content */}
</div>
```

## Neon Card System (Dashboard & Lists)

The neon card system provides archetype-based visual identity with automatic light/dark mode adaptation. Defined in `app/globals.css`.

### Archetype Colors (CSS Variables)

```css
/* Available in :root and .dark with different intensities */
--accent-mage: #8b5cf6; /* Purple - full mages, aspected mages */
--accent-sam: #10b981; /* Green - street samurai, mundane */
--accent-rigger: #06b6d4; /* Cyan - riggers */
--accent-decker: #3b82f6; /* Blue - deckers, technomancers */
--accent-face: #f59e0b; /* Amber - faces, adepts */
--accent-campaign: #6366f1; /* Indigo - campaigns */
```

### Neon Card Classes

```tsx
// Base neon card - includes ::before accent bar
<div className="neon-card">
  {/* Content */}
</div>

// Archetype-specific cards (add glow effect)
<div className="neon-card neon-card-mage">   {/* Purple glow */}
<div className="neon-card neon-card-sam">    {/* Green glow */}
<div className="neon-card neon-card-rigger"> {/* Cyan glow */}
<div className="neon-card neon-card-decker"> {/* Blue glow */}
<div className="neon-card neon-card-face">   {/* Amber glow */}
<div className="neon-card neon-card-campaign">{/* Indigo glow */}
```

### Archetype Detection Helper

```typescript
import { Character } from "@/lib/types";

function getArchetypeCardClass(character: Character): string {
  const path = character.magicalPath;
  // Awakened - mage glow
  if (path === "full-mage" || path === "aspected-mage" || path === "explorer") {
    return "neon-card-mage";
  }
  // Adept - face/amber glow
  if (path === "adept") {
    return "neon-card-face";
  }
  // Technomancer - decker/blue glow
  if (path === "technomancer") {
    return "neon-card-decker";
  }
  // Mundane - sam/green glow (default)
  return "neon-card-sam";
}

// Usage
<div className={`neon-card ${getArchetypeCardClass(character)}`}>
```

### Visual Dividers

```tsx
// Neon divider with diamond center
<div className="neon-divider" />

// Section title with accent underline
<h2 className="section-title-accent">My Characters</h2>

// Alert banner with accent top bar
<div className="alert-banner-accent">
  Important message here
</div>
```

### Grid Background

```tsx
// Subtle tech grid overlay (use on containers)
<div className="bg-grid">{/* Dashboard content */}</div>
```

### Stat Value Colors

```tsx
<span className="stat-karma">25</span>    {/* Purple karma values */}
<span className="stat-nuyen">5,000¥</span> {/* Green nuyen values */}
<span className="stat-essence">5.4</span>  {/* Cyan essence values */}
```

### Light vs Dark Mode Behavior

- **Light mode**: Subtle shadows, muted accent bars, professional appearance
- **Dark mode**: Full neon glow effects, vibrant accent colors, cyberpunk atmosphere

The CSS variables automatically adjust intensity based on theme.

## Anti-Patterns (AVOID)

1. **Generic Bootstrap/Material look** - No default rounded buttons with solid colors
2. **Excessive glow/neon** - Reserve for key interactive moments
3. **Light mode defaults** - Dark mode is primary; light mode should still feel "tech"
4. **Sans-serif for numbers** - ALWAYS use monospace for stats
5. **Fantasy RPG styling** - No parchment textures, serif fonts, or medieval iconography
6. **Cluttered dense layouts** - Use whitespace strategically
7. **Asymmetric padding** - Maintain consistent internal spacing
8. **Multiple accent colors at once** - One accent per component

## File Reference

Key existing patterns to follow:

- `app/globals.css` - **Neon card system, archetype colors, glow effects, grid patterns**
- `app/page.tsx` - Dashboard with neon cards and archetype detection
- `components/creation/shared/CreationCard.tsx` - Card wrapper pattern
- `components/creation/SkillsCard.tsx` - Modal-based editing
- `components/creation/AugmentationsCard.tsx` - Category tabs + list
- `app/characters/create/sheet/components/SheetCreationLayout.tsx` - Three-column layout

## Quick Reference: Tailwind Classes

```
Backgrounds:  bg-zinc-950, bg-zinc-900, bg-zinc-800, bg-grid
Borders:      border-zinc-800, border-zinc-700
Text:         text-zinc-100, text-zinc-300, text-zinc-400, text-zinc-500
Accents:      text-sky-400, text-emerald-400, text-amber-400, text-purple-400
Hover:        hover:bg-zinc-800, hover:bg-zinc-700
Focus:        focus:ring-2 focus:ring-sky-500 focus:ring-offset-2 focus:ring-offset-zinc-900

Neon Cards:   neon-card, neon-card-mage, neon-card-sam, neon-card-rigger,
              neon-card-decker, neon-card-face, neon-card-campaign
Dividers:     neon-divider, section-title-accent, alert-banner-accent
Stats:        stat-karma, stat-nuyen, stat-essence
```
