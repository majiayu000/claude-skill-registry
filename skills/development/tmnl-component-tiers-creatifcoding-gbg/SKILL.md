---
name: tmnl-component-tiers
description: TMNL component organization system. Invoke when creating new components, refactoring file structures, or determining component placement. Defines the three-tier hierarchy - primitives, composites, testbeds, and pages.
model_invoked: true
triggers:
  - "component organization"
  - "primitives"
  - "composites"
  - "testbed"
  - "file structure"
  - "component location"
  - "where to put component"
---

# TMNL Component Tiers

## Overview

TMNL organizes components into a three-tier hierarchy based on complexity and composition. This system ensures clear dependencies, prevents circular imports, and maintains a predictable codebase structure.

**Key Principle**: Components can only import from their own tier or lower tiers. Never import upward in the hierarchy.

## Component Hierarchy

```
┌─────────────────────────────────────────┐
│            Pages / Routes               │ ← Tier 3: Composition
│  Full-page layouts, route components   │
└─────────────────────────────────────────┘
              ▲ imports from
┌─────────────────────────────────────────┐
│        Composites / Features            │ ← Tier 2: Business Logic
│  Domain-specific components, features  │
└─────────────────────────────────────────┘
              ▲ imports from
┌─────────────────────────────────────────┐
│           Primitives / UI               │ ← Tier 1: Foundation
│  Basic building blocks, no domain logic│
└─────────────────────────────────────────┘
              ▲ imports from
┌─────────────────────────────────────────┐
│          Tokens / Constants             │ ← Tier 0: Data
│  TMNL_TOKENS, VANTA_COLORS, etc.       │
└─────────────────────────────────────────┘
```

## Canonical Directory Structure

### Primitives (`src/lib/*/primitives/`, `src/components/primitives/`)

**Purpose**: Foundation UI components with no domain knowledge.

**Characteristics**:
- Single responsibility
- Token-driven styling
- Generic, reusable
- No business logic
- No domain-specific state

**Locations**:
- `src/lib/tmnl-ui/primitives/` - TMNL UI primitives (Badge, Button, Input, Label, Separator)
- `src/components/primitives/` - Shared primitives (card, button, badge, typography)
- `src/lib/primitives/` - Library-level primitives (TokenRegistry)

**Examples**:
- `src/lib/tmnl-ui/primitives/Badge.tsx`
- `src/lib/tmnl-ui/primitives/Button.tsx`
- `src/lib/tmnl-ui/primitives/Input.tsx`
- `src/lib/tmnl-ui/primitives/Label.tsx`
- `src/lib/tmnl-ui/primitives/Separator.tsx`
- `src/components/primitives/button.tsx`
- `src/components/primitives/card.tsx`
- `src/components/primitives/typography.tsx`

### Composites (`src/lib/*/components/`, `src/components/*/`)

**Purpose**: Domain-specific components that compose primitives.

**Characteristics**:
- Business logic
- Domain models
- Compose primitives
- Effect services integration
- State management

**Locations**:
- `src/lib/data-grid/components/` - DataGrid components (Header, Body, Title)
- `src/lib/charting/v1/components/` - Charting widgets
- `src/lib/slider/v2/components/` - Slider components
- `src/lib/minibuffer/v2/components/` - Minibuffer UI
- `src/components/portal/` - Vanta design system composites (VantaCard)

**Examples**:
- `src/lib/data-grid/components/Header.tsx`
- `src/lib/data-grid/components/Body.tsx`
- `src/components/portal/VantaCard.tsx`
- `src/lib/slider/v2/components/Slider.tsx`

### Testbeds (`src/components/testbed/`)

**Purpose**: Development environments for testing and validating components.

**Characteristics**:
- Hypothesis validation
- Integration testing
- Visual regression testing
- Performance benchmarking
- NOT production code

**Naming Convention**: `<Feature>Testbed.tsx`

**Examples**:
- `src/components/testbed/DataGridTestbed.tsx`
- `src/components/testbed/DataManagerTestbed.tsx`
- `src/components/testbed/AnimationTestbed.tsx`
- `src/components/testbed/SliderV2Testbed.tsx`
- `src/components/testbed/VantaCardTestbed.tsx`
- `src/components/testbed/HotkeyTestbed.tsx`

**Testbed Structure**:
```typescript
// Hypothesis-driven testbed structure
export function DataManagerTestbed() {
  return (
    <div className="p-8 space-y-8">
      <Header title="DataManager Testbed" />

      <Hypothesis
        id="H1"
        statement="effect-atom state flows correctly to AG-Grid rowData"
        status="validated"
      />

      <TestCase title="Progressive Stream Updates">
        {/* Test implementation */}
      </TestCase>

      <MetricsPanel>
        {/* Performance metrics */}
      </MetricsPanel>
    </div>
  )
}
```

**Canonical source**: `src/components/testbed/DataManagerTestbed.tsx`

### Pages (`src/pages/`, route components in `src/router.tsx`)

**Purpose**: Full-page layouts and route components.

**Characteristics**:
- Top-level composition
- Route definitions
- Layout orchestration
- Feature integration

**Examples**:
```typescript
// Route definition in router.tsx
{
  path: '/testbed/data-manager',
  element: <DataManagerTestbed />,
}

// Page component
export function DashboardPage() {
  return (
    <PageLayout>
      <Sidebar />
      <MainContent>
        <DataGrid />
        <ChartPanel />
      </MainContent>
    </PageLayout>
  )
}
```

## Naming Conventions

### Primitives

- **File**: lowercase with hyphens - `badge.tsx`, `button.tsx`, `input.tsx`
- **Component**: PascalCase - `Badge`, `Button`, `Input`
- **Export**: Named export - `export function Badge() { ... }`

```typescript
// src/lib/tmnl-ui/primitives/Badge.tsx
export function Badge({ children, variant = 'default' }: BadgeProps) {
  return <span className={...}>{children}</span>
}
```

### Composites

- **File**: PascalCase - `VantaCard.tsx`, `DataGrid.tsx`, `Header.tsx`
- **Component**: PascalCase - `VantaCard`, `DataGrid`, `Header`
- **Export**: Named or compound export

```typescript
// src/components/portal/VantaCard.tsx
export const VantaCard = Object.assign(VantaCardRoot, {
  Header,
  Title,
  Subtitle,
  Body,
})
```

### Testbeds

- **File**: `<Feature>Testbed.tsx` - `DataGridTestbed.tsx`, `AnimationTestbed.tsx`
- **Component**: `<Feature>Testbed` - `DataGridTestbed`, `AnimationTestbed`
- **Route**: `/testbed/<feature>` - `/testbed/data-grid`, `/testbed/animation`

```typescript
// src/components/testbed/DataManagerTestbed.tsx
export function DataManagerTestbed() {
  // Hypothesis-driven test structure
}
```

## Patterns

### Pattern 1: Primitive Component Structure

Single-responsibility UI building blocks.

```typescript
/**
 * TMNL Badge Component
 *
 * CEW-styled status badges.
 */

import type { ReactNode } from 'react'
import { cn } from '../utils/cn'
import { TMNL_FONT_SIZE, TMNL_TOKENS } from '../tokens'

interface BadgeProps {
  children: ReactNode
  className?: string
  variant?: 'default' | 'success' | 'warning' | 'error' | 'info'
}

const variants = {
  default: 'bg-neutral-800 text-neutral-400 border-neutral-700',
  success: 'bg-emerald-950 text-emerald-400 border-emerald-800',
  warning: 'bg-amber-950 text-amber-400 border-amber-800',
  error: 'bg-red-950 text-red-400 border-red-800',
  info: 'bg-cyan-950 text-cyan-400 border-cyan-800',
}

export function Badge({ children, className, variant = 'default' }: BadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center px-2 py-0.5 rounded border',
        TMNL_TOKENS.typography.label,
        variants[variant],
        className
      )}
      style={{ fontSize: TMNL_FONT_SIZE.xs }}
    >
      {children}
    </span>
  )
}
```

**Canonical source**: `src/lib/tmnl-ui/primitives/Badge.tsx`

### Pattern 2: Composite Component (Compound Pattern)

Domain components that compose primitives.

```typescript
import { VANTA_COLORS, VANTA_TYPOGRAPHY, VANTA_SPACING } from './tokens'

// Root component
const VantaCardRoot = forwardRef<HTMLDivElement, VantaCardProps>(
  ({ children, variant = 'default', glow = false }, ref) => {
    const variantTokens = VANTA_CARD_VARIANTS[variant]

    return (
      <VantaCardContext.Provider value={{ variant }}>
        <div ref={ref} style={variantTokens}>
          {children}
        </div>
      </VantaCardContext.Provider>
    )
  }
)

// Subcomponents
function Title({ children }: TitleProps) {
  return (
    <h3 style={{ ...VANTA_TYPOGRAPHY.preset.cardTitle }}>
      {children}
    </h3>
  )
}

function Indicator({ status }: IndicatorProps) {
  return (
    <div style={{ display: 'flex', alignItems: 'center' }}>
      <div style={{ backgroundColor: statusColors[status].dot }} />
      <span>{status}</span>
    </div>
  )
}

// Compound export
export const VantaCard = Object.assign(VantaCardRoot, {
  Header,
  Title,
  Subtitle,
  Body,
  Indicator,
  Actions,
})
```

**Canonical source**: `src/components/portal/VantaCard.tsx`

### Pattern 3: Testbed Structure

Hypothesis-driven development environment.

```typescript
import { Hypothesis, TestCase, MetricsPanel } from '@/components/testbed/shared'

export function DataManagerTestbed() {
  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold">DataManager Testbed</h1>
        <p className="text-muted">Service-scoped data orchestration validation</p>
      </div>

      {/* Hypotheses */}
      <section>
        <h2 className="text-lg font-semibold mb-4">Hypotheses</h2>
        <Hypothesis
          id="H1"
          statement="effect-atom state flows correctly to AG-Grid rowData"
          status="validated"
        />
        <Hypothesis
          id="H2"
          statement="Progressive stream updates trigger grid re-renders without flicker"
          status="in-progress"
        />
      </section>

      {/* Test Cases */}
      <section>
        <h2 className="text-lg font-semibold mb-4">Test Cases</h2>
        <TestCase title="Search with Progressive Updates">
          <SearchInput />
          <DataGrid />
        </TestCase>
      </section>

      {/* Metrics */}
      <MetricsPanel>
        <Metric label="Throughput" value={throughput} unit="docs/s" />
        <Metric label="Latency" value={latency} unit="ms" />
      </MetricsPanel>
    </div>
  )
}
```

**Canonical source**: `src/components/testbed/DataManagerTestbed.tsx`

### Pattern 4: Library-Level Organization

Feature-specific component hierarchies.

```
src/lib/slider/v2/
├── index.ts              # Public exports
├── types.ts              # Shared types
├── services/
│   └── SliderBehavior.ts # Effect services
├── atoms/
│   └── index.ts          # Atom definitions
├── hooks/
│   └── useSlider.ts      # React hooks
├── components/
│   └── Slider.tsx        # UI components
└── debug/
    └── withSliderDebug.tsx # Debug tools
```

**Canonical source**: `src/lib/slider/`

### Pattern 5: Shared Testbed Utilities

Reusable testbed components in `src/components/testbed/shared/`.

```typescript
// src/components/testbed/shared/hypothesis.tsx
export function Hypothesis({ id, statement, status }: HypothesisProps) {
  return (
    <div className="border rounded p-4">
      <div className="flex items-center gap-2">
        <Badge variant={statusVariant[status]}>{id}</Badge>
        <StatusIndicator status={status} />
      </div>
      <p className="mt-2">{statement}</p>
    </div>
  )
}
```

**Canonical source**: `src/components/testbed/shared/hypothesis.tsx`

## Component Placement Decision Tree

```
Is it reusable across domains?
  ├─ YES → Is it a basic UI element?
  │         ├─ YES → src/lib/tmnl-ui/primitives/
  │         └─ NO  → src/components/primitives/
  └─ NO  → Does it belong to a specific library?
            ├─ YES → src/lib/<library>/components/
            └─ NO  → Is it a testbed?
                      ├─ YES → src/components/testbed/
                      └─ NO  → src/components/<feature>/
```

## Import Direction Rules

**ALLOWED** (downward or lateral):
```typescript
// Page imports composite
import { VantaCard } from '@/components/portal/VantaCard'

// Composite imports primitive
import { Badge } from '@/lib/tmnl-ui/primitives/Badge'

// Testbed imports composite
import { DataGrid } from '@/lib/data-grid'

// All import tokens
import { VANTA_COLORS } from '@/components/portal/tokens'
```

**BANNED** (upward):
```typescript
// BANNED - primitive importing composite
import { VantaCard } from '@/components/portal/VantaCard' // in Badge.tsx

// BANNED - primitive importing page
import { DashboardPage } from '@/pages/Dashboard' // in Button.tsx

// BANNED - composite importing page
import { SettingsPage } from '@/pages/Settings' // in VantaCard.tsx
```

## Anti-Patterns (BANNED)

### God Components

```typescript
// BANNED - single component doing too much
export function MegaWidget() {
  // Has primitives, composites, business logic, AND page layout
  // Impossible to reuse or test
}

// CORRECT - separated concerns
export function WidgetPrimitive() { /* UI only */ }
export function Widget() { /* Composes primitives */ }
export function WidgetPage() { /* Page layout */ }
```

### Circular Imports

```typescript
// BANNED - circular dependency
// VantaCard.tsx imports Badge
// Badge.tsx imports VantaCard

// CORRECT - unidirectional
// VantaCard.tsx imports Badge
// Badge.tsx imports only tokens
```

### Testbeds in Production

```typescript
// BANNED - importing testbed in production code
import { DataManagerTestbed } from '@/components/testbed/DataManagerTestbed'

// CORRECT - testbeds only in router.tsx
{
  path: '/testbed/data-manager',
  element: <DataManagerTestbed />,
}
```

### Hardcoded Domain Logic in Primitives

```typescript
// BANNED - domain logic in primitive
export function Badge({ userId }: BadgeProps) {
  const user = useUser(userId) // DOMAIN LOGIC
  return <span>{user.role}</span>
}

// CORRECT - primitive is generic
export function Badge({ children }: BadgeProps) {
  return <span>{children}</span>
}
```

## Related Skills

- **tmnl-design-tokens** - Token consumption in components
- **tmnl-typography-discipline** - Typography in primitives
- **tmnl-color-system** - Color token usage across tiers
