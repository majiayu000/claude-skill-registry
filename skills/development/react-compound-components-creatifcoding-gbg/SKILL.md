---
name: react-compound-components
description: Compound component patterns for TMNL. Covers context-based composition, slot patterns, and Object.assign exports. Use for building composable component APIs like VantaCard.Header, Modal.Content, etc.
model_invoked: true
triggers:
  - "compound component"
  - "VantaCard"
  - "slot pattern"
  - "Object.assign"
  - "context composition"
---

# React Compound Components for TMNL

## Overview

Compound components provide a flexible, composable API where a parent component shares implicit state with child components via React Context. This pattern enables expressive, self-documenting component APIs without prop drilling.

**Key Insight**: Compound components trade explicit props for implicit context, creating component families that share state while maintaining composition flexibility.

## Canonical Sources

### TMNL Implementations

- **VantaCard** — `/src/components/portal/VantaCard.tsx` (comprehensive example)
  - Context-based variant sharing
  - Typography token presets
  - Status indicators with visual tokens
  - `Object.assign` export pattern

- **DataGrid** — `/src/components/data-grid/DataGrid.tsx`
  - Header, Body, CornerDecorations composition
  - Context-free compound (stateless slots)

- **shadcn/ui primitives** — `/src/components/ui/card.tsx`, `/src/components/ui/dialog.tsx`
  - React.forwardRef pattern for compound children
  - Minimal context, slot-based composition

### Reference Documentation

- [React Context API](https://react.dev/learn/passing-data-deeply-with-context)
- [Compound Components Pattern](https://kentcdodds.com/blog/compound-components-with-react-hooks)

## Pattern Variants

### Pattern 1: Context-Based Compound Components (Stateful)

Use when child components need shared state from parent.

```tsx
import { createContext, useContext, forwardRef, type ReactNode } from 'react'

// ─────────────────────────────────────────────────────────────────────────
// 1. Define Context
// ─────────────────────────────────────────────────────────────────────────

interface CardContextValue {
  variant: 'default' | 'elevated' | 'glass'
}

const CardContext = createContext<CardContextValue>({ variant: 'default' })

const useCard = () => useContext(CardContext)

// ─────────────────────────────────────────────────────────────────────────
// 2. Root Component (Provider)
// ─────────────────────────────────────────────────────────────────────────

interface CardProps {
  children: ReactNode
  variant?: 'default' | 'elevated' | 'glass'
  className?: string
}

const CardRoot = forwardRef<HTMLDivElement, CardProps>(
  ({ children, variant = 'default', className = '' }, ref) => {
    return (
      <CardContext.Provider value={{ variant }}>
        <div ref={ref} className={`card card-${variant} ${className}`}>
          {children}
        </div>
      </CardContext.Provider>
    )
  }
)

CardRoot.displayName = 'Card'

// ─────────────────────────────────────────────────────────────────────────
// 3. Child Components (Consumers)
// ─────────────────────────────────────────────────────────────────────────

interface HeaderProps {
  children: ReactNode
  className?: string
}

function Header({ children, className = '' }: HeaderProps) {
  const { variant } = useCard() // ← Accesses parent context

  return (
    <div className={`card-header card-header-${variant} ${className}`}>
      {children}
    </div>
  )
}

function Title({ children, className = '' }: { children: ReactNode; className?: string }) {
  const { variant } = useCard()

  return (
    <h3 className={`card-title card-title-${variant} ${className}`}>
      {children}
    </h3>
  )
}

function Body({ children, className = '' }: { children: ReactNode; className?: string }) {
  return <div className={`card-body ${className}`}>{children}</div>
}

// ─────────────────────────────────────────────────────────────────────────
// 4. Compound Export
// ─────────────────────────────────────────────────────────────────────────

export const Card = Object.assign(CardRoot, {
  Header,
  Title,
  Body,
})

// ─────────────────────────────────────────────────────────────────────────
// Usage
// ─────────────────────────────────────────────────────────────────────────

function Example() {
  return (
    <Card variant="elevated">
      <Card.Header>
        <Card.Title>System Status</Card.Title>
      </Card.Header>
      <Card.Body>
        All systems operational
      </Card.Body>
    </Card>
  )
}
```

**Canonical source**: `src/components/portal/VantaCard.tsx:40-552`

### Pattern 2: Slot-Based Compound Components (Stateless)

Use when child components are pure slots without shared state.

```tsx
import { forwardRef, type ReactNode } from 'react'

// ─────────────────────────────────────────────────────────────────────────
// Root Component (no context)
// ─────────────────────────────────────────────────────────────────────────

const ModalRoot = forwardRef<HTMLDivElement, { children: ReactNode }>(
  ({ children }, ref) => {
    return (
      <div ref={ref} className="modal">
        {children}
      </div>
    )
  }
)

ModalRoot.displayName = 'Modal'

// ─────────────────────────────────────────────────────────────────────────
// Slots (no context access)
// ─────────────────────────────────────────────────────────────────────────

function Header({ children }: { children: ReactNode }) {
  return <div className="modal-header">{children}</div>
}

function Content({ children }: { children: ReactNode }) {
  return <div className="modal-content">{children}</div>
}

function Footer({ children }: { children: ReactNode }) {
  return <div className="modal-footer">{children}</div>
}

// ─────────────────────────────────────────────────────────────────────────
// Compound Export
// ─────────────────────────────────────────────────────────────────────────

export const Modal = Object.assign(ModalRoot, {
  Header,
  Content,
  Footer,
})
```

**Canonical source**: `src/components/ui/card.tsx`

### Pattern 3: Context with Design Tokens

Use when child components need token-driven styling based on parent variant.

```tsx
import { createContext, useContext, forwardRef, type ReactNode, type CSSProperties } from 'react'
import { VANTA_COLORS, VANTA_TYPOGRAPHY, VANTA_SPACING } from './tokens'

// ─────────────────────────────────────────────────────────────────────────
// Context
// ─────────────────────────────────────────────────────────────────────────

interface VantaCardContextValue {
  variant: 'default' | 'elevated' | 'glass'
}

const VantaCardContext = createContext<VantaCardContextValue>({ variant: 'default' })

const useVantaCard = () => useContext(VantaCardContext)

// ─────────────────────────────────────────────────────────────────────────
// Root with Token-Based Styling
// ─────────────────────────────────────────────────────────────────────────

const VANTA_CARD_VARIANTS = {
  default: {
    background: VANTA_COLORS.surface.bg,
    border: `1px solid ${VANTA_COLORS.surface.border}`,
    padding: VANTA_SPACING['4'],
  },
  elevated: {
    background: VANTA_COLORS.surface.bgElevated,
    border: `1px solid ${VANTA_COLORS.surface.borderHighlight}`,
    padding: VANTA_SPACING['5'],
  },
  glass: {
    background: VANTA_COLORS.surface.bgGlass,
    border: `1px solid ${VANTA_COLORS.surface.borderGlass}`,
    padding: VANTA_SPACING['4'],
  },
}

const VantaCardRoot = forwardRef<HTMLDivElement, { children: ReactNode; variant?: 'default' | 'elevated' | 'glass' }>(
  ({ children, variant = 'default' }, ref) => {
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

VantaCardRoot.displayName = 'VantaCard'

// ─────────────────────────────────────────────────────────────────────────
// Children with Token-Based Styling
// ─────────────────────────────────────────────────────────────────────────

function Title({ children }: { children: ReactNode }) {
  return (
    <h3
      style={{
        color: VANTA_COLORS.text.primary,
        ...VANTA_TYPOGRAPHY.preset.cardTitle,
      }}
    >
      {children}
    </h3>
  )
}

function Body({ children }: { children: ReactNode }) {
  return (
    <div
      style={{
        color: VANTA_COLORS.text.secondary,
        ...VANTA_TYPOGRAPHY.preset.cardBody,
      }}
    >
      {children}
    </div>
  )
}

export const VantaCard = Object.assign(VantaCardRoot, {
  Title,
  Body,
})
```

**Canonical source**: `src/components/portal/VantaCard.tsx:65-149`

## Decision Tree

```
Need composable component API?
│
├─ Child components need shared state from parent?
│  └─ Use: Context-Based Compound Components
│     (e.g., VantaCard with variant context)
│
├─ Child components are pure layout slots?
│  └─ Use: Slot-Based Compound Components
│     (e.g., Modal.Header, Modal.Content)
│
└─ Styling driven by design tokens + parent state?
   └─ Use: Context + Token Pattern
      (e.g., VantaCard with VANTA_COLORS)
```

## Examples

### Example 1: VantaCard with All Features

Full-featured compound component with context, tokens, and multiple child variants.

```tsx
<VantaCard variant="elevated" corners glow glowColor="cyan">
  <VantaCard.Header>
    <VantaCard.Title>SYSTEM STATUS</VantaCard.Title>
    <VantaCard.Indicator status="active" label="Online" pulse />
  </VantaCard.Header>

  <VantaCard.Subtitle>Last updated 2 minutes ago</VantaCard.Subtitle>

  <VantaCard.Body>
    All systems operational. No incidents reported.
  </VantaCard.Body>

  <VantaCard.Divider />

  <div className="grid grid-cols-3 gap-4">
    <VantaCard.LabelValue label="Uptime" value="99.98%" accent="emerald" />
    <VantaCard.LabelValue label="Requests" value="1.2M" accent="cyan" />
    <VantaCard.LabelValue label="Latency" value="45ms" accent="amber" />
  </div>

  <VantaCard.Actions>
    <VantaCard.Action variant="primary" onClick={() => {}}>View Details</VantaCard.Action>
    <VantaCard.Action variant="ghost" onClick={() => {}}>Dismiss</VantaCard.Action>
  </VantaCard.Actions>
</VantaCard>
```

**Canonical source**: `src/components/testbed/VantaCardTestbed.tsx:23-100`

### Example 2: DataGrid Slots (Context-Free)

Stateless slot composition for structured layout.

```tsx
<DataGrid>
  <DataGrid.Header>
    <DataGrid.Title>Search Results</DataGrid.Title>
  </DataGrid.Header>
  <DataGrid.Body>
    <AgGridReact {...gridOptions} />
  </DataGrid.Body>
  <DataGrid.CornerDecorations />
</DataGrid>
```

**Canonical source**: `src/components/data-grid/DataGrid.tsx`

## Anti-Patterns (BANNED)

### Prop Drilling Through Compound Children

```tsx
// BANNED - Defeats the purpose of compound components
<Card variant="elevated">
  <Card.Header variant="elevated"> {/* ← Redundant prop drilling */}
    <Card.Title variant="elevated"> {/* ← Even worse */}
      Title
    </Card.Title>
  </Card.Header>
</Card>

// CORRECT - Context provides variant implicitly
<Card variant="elevated">
  <Card.Header>
    <Card.Title>Title</Card.Title>
  </Card.Header>
</Card>
```

### Using Children Props Instead of Slots

```tsx
// BANNED - Loses composability
<Card
  header={<div>Header</div>}
  body={<div>Body</div>}
  footer={<div>Footer</div>}
/>

// CORRECT - Compound children for flexibility
<Card>
  <Card.Header>Header</Card.Header>
  <Card.Body>Body</Card.Body>
  <Card.Footer>Footer</Card.Footer>
</Card>
```

### Exporting Children Separately

```tsx
// BANNED - Breaks compound API
export { Card }
export { CardHeader }
export { CardTitle }

// Usage is awkward
import { Card, CardHeader, CardTitle } from './Card'

// CORRECT - Object.assign for compound export
export const Card = Object.assign(CardRoot, {
  Header,
  Title,
  Body,
})

// Usage is clean
import { Card } from './Card'
<Card.Header><Card.Title /></Card.Header>
```

## Implementation Checklist

When creating a compound component:

- [ ] **Context**: Create context if children need shared state
- [ ] **Root Component**: Wrap children with context provider
- [ ] **Child Components**: Define slot components
- [ ] **displayName**: Set `displayName` on root for DevTools
- [ ] **forwardRef**: Use `forwardRef` if refs are needed
- [ ] **Object.assign**: Export as compound with `Object.assign(Root, { Child1, Child2 })`
- [ ] **TypeScript**: Export root props interface
- [ ] **Tokens**: Use design tokens for styling, not hardcoded values

## Related Patterns

- **effect-patterns** — Use `Atom.make()` if compound state is reactive
- **react-hook-composition** — Compound context often pairs with custom hooks
- **react-hoc-patterns** — HOCs can enhance compound components

## Filing New Patterns

When you discover a new compound component pattern:

1. Implement in `src/components/` with full TypeScript types
2. Add testbed example at `/testbed/<component-name>`
3. Update this skill with canonical source references
4. Document context usage and token integration
