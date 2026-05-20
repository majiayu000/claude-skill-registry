---
name: frontend-design
description: Enforce a precise, minimal design system for Battery's dashboard UI. Use this skill when building admin interfaces, deployment management screens, or any dashboard components. Inspired by Linear, Notion, and Stripe - clean, modern, enterprise-grade with Jony Ive-level precision.
---

# Frontend Design Principles

## Design Direction

Battery is an enterprise deployment platform. The aesthetic should communicate:
- **Trust & Sophistication**: Cool tones, layered depth, professional
- **Data & Analysis**: Numbers-first, monospace for IDs and timestamps
- **Utility & Function**: Dense but readable, efficient use of space

### Color Foundation

- **Primary**: Cool grays with blue undertones
- **Accent**: Electric blue for primary actions, success states
- **Semantic**: Green (deployed), Yellow (pending), Red (error/revoked)
- **Mode**: Support both light and dark themes

## Core Craft Principles

### 4px Grid System

All spacing uses multiples of 4px:
- `4px` - Tight inline spacing
- `8px` - Related elements
- `12px` - Default padding
- `16px` - Section gaps
- `24px` - Major separations
- `32px` - Page-level spacing

### Symmetrical Padding

Top/Left/Bottom/Right must match. Never asymmetric padding.

```tsx
// Correct
<div className="p-4">
<div className="px-4 py-3">

// Incorrect - asymmetric
<div className="pt-2 pb-4 pl-3 pr-5">
```

### Border Radius Consistency

Use one system throughout:
- `rounded-none` - Tables, code blocks
- `rounded` (4px) - Buttons, inputs, cards
- `rounded-lg` (8px) - Modals, large containers

### Depth & Elevation

Prefer borders over shadows for structure:
```tsx
// Preferred - border-based depth
<div className="border border-gray-200 dark:border-gray-800">

// Use shadows sparingly for floating elements only
<div className="shadow-lg"> // Dropdowns, modals only
```

### Typography Hierarchy

- **Headings**: System font, semibold (600)
- **Body**: System font, regular (400)
- **Data**: Monospace for IDs, timestamps, counts, URLs

```tsx
// Data should use monospace
<span className="font-mono text-sm">deploy_abc123</span>
<span className="font-mono tabular-nums">1,234</span>
```

### Iconography

Use Phosphor Icons (regular weight) throughout:
```tsx
import { Rocket, Shield, Database } from '@phosphor-icons/react'

<Rocket size={20} />
```

### Color for Meaning Only

- Gray builds structure
- Color communicates status/action
- Never decorative gradients

```tsx
// Status colors
<Badge variant="success">Deployed</Badge>  // Green
<Badge variant="warning">Pending</Badge>   // Yellow
<Badge variant="error">Failed</Badge>      // Red
<Badge variant="default">Draft</Badge>     // Gray
```

## Navigation & Layout

### Sidebar Pattern

- Fixed left sidebar (240px)
- Logo top-left
- Primary nav with icons + labels
- User/org switcher bottom

### Content Area

- Max width 1200px for readability
- Consistent page header pattern
- Breadcrumbs for deep navigation

## Dark Mode

- Borders become more prominent than shadows
- Backgrounds: gray-900, gray-950
- Text: gray-100 (primary), gray-400 (secondary)
- Maintain same spacing and structure

## Anti-Patterns

Never use:
- Drop shadows for depth (use borders)
- Border radius > 8px
- Asymmetric padding
- Decorative gradients
- Multiple font families
- Colorful backgrounds (except status indicators)
- Rounded-full on non-avatar elements

Always question:
- Is this spacing a multiple of 4?
- Is this color communicating meaning?
- Would this look correct in dark mode?
- Is data displayed in monospace?
