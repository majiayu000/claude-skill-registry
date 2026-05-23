---
name: tmnl-testbed-patterns
description: Creating testbed components at /testbed/*, adding cards to App.tsx portal, route registration. Testbed structure conventions.
triggers:
  - "testbed"
  - "create testbed"
  - "add testbed"
  - "testbed route"
---

# TMNL Testbed Patterns

Canonical patterns for creating, routing, and presenting testbed components in TMNL.

## Overview

Testbeds are isolated demonstration pages for features, patterns, and systems under development. They serve as:
- Living documentation
- Integration test surfaces
- Pattern exemplars
- Performance benchmarks

**Location**: `src/components/testbed/*`
**Routes**: `/testbed/*`
**Portal**: `src/App.tsx` card grid

## Canonical Sources

**Primary Files**:
- `src/router.tsx` - Route registration checklist and patterns
- `src/App.tsx` - Portal card data structure and rendering
- `src/components/testbed/DataManagerTestbed.tsx` - Exemplar testbed with antipattern documentation
- `src/components/testbed/SliderV2Testbed.tsx` - Trait-based testbed pattern

**Reference Testbeds**:
- `AnimationTestbed.tsx` - Animation system demonstration
- `EffectAtomTestbed.tsx` - Effect-atom integration patterns
- `OverlayTestbed.tsx` - Overlay system capabilities
- `ScadaOverlayTestbed.tsx` - Industrial overlay patterns

## Patterns

### 1. Testbed File Structure

**Template**:
```tsx
/**
 * [Feature] Testbed
 *
 * [Brief description of what this testbed demonstrates]
 *
 * Route: /testbed/[feature-name]
 *
 * HYPOTHESES (if experimental):
 * - H1: [Hypothesis to validate]
 * - H2: [Another hypothesis]
 * ...
 *
 * ANTIPATTERNS (if discovered):
 * - Document failure modes and fixes
 * - Provide root cause analysis
 * - Link to related testbeds with same issues
 */

import { useState } from 'react'
import { Link } from '@tanstack/react-router'
import { ArrowLeft } from 'lucide-react'

export function FeatureTestbed() {
  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-100 p-8">
      {/* Header with back link */}
      <div className="max-w-4xl mx-auto mb-8">
        <Link to="/" className="text-cyan-400 hover:underline text-sm mb-4 block">
          &larr; Back to Home
        </Link>
        <h1 className="text-3xl font-mono font-bold mb-2">[Feature] Testbed</h1>
        <p className="text-neutral-400">
          [Brief description]
        </p>
      </div>

      {/* Content sections */}
      <div className="max-w-4xl mx-auto grid gap-6">
        {/* Demo sections here */}
      </div>
    </div>
  )
}
```

**Naming Convention**: `[Feature]Testbed.tsx` (PascalCase, no spaces)

### 2. Route Registration (4-Step Checklist)

**From `src/router.tsx` header comment**:
```
CHECKLIST FOR NEW ROUTES:
1. Import the component at top of file
2. Create route constant (e.g., `const fooRoute = createRoute({ ... })`)
3. Add route to `routeTree.addChildren([...])` array
4. Add Link in App.tsx homepage navigation

DON'T FORGET STEP 4. THE LINK. IN APP.TSX. SERIOUSLY.
```

**Example Implementation**:

```tsx
// Step 1: Import
import { FeatureTestbed } from './components/testbed/FeatureTestbed'

// Step 2: Create route constant
const featureTestbedRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/testbed/feature',
  component: FeatureTestbed,
})

// Step 3: Add to routeTree.addChildren([...])
const router = createRouter({
  routeTree: rootRoute.addChildren([
    indexRoute,
    tmnlRoute,
    // ... other routes ...
    featureTestbedRoute, // ← Add here
  ]),
})
```

**Path Convention**:
- Basic: `/testbed/[feature-name]` (kebab-case)
- Versioned: `/testbed/[feature]/v1` or `/testbed/[feature]/v2`
- Nested: `/testbed/[category]/[feature]`

### 3. Portal Card Registration (App.tsx)

**Step 4 from checklist**: Add card to `CARDS` array in `src/App.tsx`.

**Card Definition Type**:
```tsx
interface CardDef {
  readonly title: string          // ALL CAPS by convention
  readonly body: string            // 1-2 sentences, technical detail
  readonly route: string           // Must match route path exactly
  readonly status?: IndicatorStatus // 'active' | 'idle' | 'warning' | 'error'
  readonly label?: string          // Badge text (e.g., 'NEW', 'v1', 'BETA')
  readonly glow?: GlowColor        // 'cyan' | 'rose' | 'amber' | 'emerald'
}
```

**Categories in CARDS Array**:
- Feature (Data Manager, AG-Grid, Overlays)
- Infrastructure (Effect-Atom, Animation, Streams)
- Controls (Slider, Hotkeys, Keybindings)
- Abstractions (Traits, Base Modal, Capabilities)

**Example Card**:
```tsx
const CARDS: readonly CardDef[] = [
  // Feature
  {
    title: 'FEATURE NAME',
    body: 'Effect.Service pattern with kernel architecture. FlexSearch and Linear drivers for progressive streaming.',
    route: '/testbed/feature',
    status: 'active',
    label: 'NEW',
    glow: 'cyan',
  },
  // ... more cards
]
```

**Glow Color Guidelines**:
- `cyan` - Data/infrastructure features
- `emerald` - New/experimental features
- `amber` - High-value integrations
- `rose` - Critical/system features

### 4. Demo Section Components

**Reusable Section Pattern**:
```tsx
function DemoSection({
  title,
  description,
  children,
}: {
  title: string
  description: string
  children: React.ReactNode
}) {
  return (
    <div className="p-4 bg-neutral-900/50 rounded-lg border border-neutral-800">
      <h3 className="text-lg font-mono font-bold text-neutral-100 mb-1">{title}</h3>
      <p className="text-sm text-neutral-400 mb-4">{description}</p>
      <div className="space-y-4">{children}</div>
    </div>
  )
}
```

**Usage**:
```tsx
<div className="max-w-4xl mx-auto grid gap-6">
  <DemoSection
    title="1. Basic Usage"
    description="Demonstrates the fundamental pattern"
  >
    {/* Demo content */}
  </DemoSection>

  <DemoSection
    title="2. Advanced Usage"
    description="Shows edge cases and configuration"
  >
    {/* Demo content */}
  </DemoSection>
</div>
```

### 5. Shared Components

**Import from shared module**:
```tsx
import { SectionLabel } from '@/components/testbed/shared'
```

**Available Shared Components** (in `src/components/testbed/shared.tsx`):
- `SectionLabel` - Standardized section headers
- Render tracking utilities (for performance analysis)

### 6. Version Switching Pattern

**For multi-version features** (e.g., DataGrid V1/V2):

```tsx
// Component: DataGridTestbedSwitch.tsx
export function DataGridTestbedSwitch() {
  const [version, setVersion] = useState<'v1' | 'v2'>('v2')

  return (
    <div>
      <VersionToggle value={version} onChange={setVersion} />
      {version === 'v1' ? <DataGridTestbed /> : <DataGridTestbedV2 />}
    </div>
  )
}
```

**Route**: Single route `/testbed/data-grid` with internal switching.

### 7. Hypothesis Validation Pattern

**When conducting experiments** (EPOCH-style):

```tsx
/**
 * HYPOTHESES:
 * - H1: Search results flow correctly to AG-Grid rowData
 * - H2: Progressive stream updates trigger grid re-renders without flicker
 * - H3: Stream-first search provides clean DX
 * - H4: Real-time metrics (throughput, items/sec)
 * - H5: Driver switching (flex/linear) is seamless
 */

export function ExperimentalTestbed() {
  const [hypotheses, setHypotheses] = useState({
    h1: false,
    h2: false,
    h3: false,
    h4: false,
    h5: false,
  })

  // Verify actual outcomes, not just function calls
  const validateH1 = () => {
    setHypotheses(prev => ({ ...prev, h1: gridData.length > 0 })) // ✓ Correct
    // NOT: setHypotheses(prev => ({ ...prev, h1: true })) after setGridData() // ✗ Wrong
  }

  // Display validation status
  return (
    <div>
      <HypothesisPanel hypotheses={hypotheses} />
      {/* Testbed content */}
    </div>
  )
}
```

**Antipattern Fix (from DataManagerTestbed.tsx)**:
- Verify **outcomes** (e.g., `gridData.length > 0`)
- NOT **function calls** (e.g., "setGridData was called")

### 8. Antipattern Documentation

**When discovering antipatterns**, document them prominently:

```tsx
/**
 * ═══════════════════════════════════════════════════════════════════════════════
 * ANTIPATTERN DISCOVERED: [Title]
 * ═══════════════════════════════════════════════════════════════════════════════
 *
 * ROOT CAUSE: [Why it failed]
 *
 * FAILURE SCENARIO:
 *   1. [Step 1]
 *   2. [Step 2]
 *   3. [Outcome]
 *
 * SYMPTOM: [Observable behavior]
 *
 * FIX: [Solution]
 *
 * See also: [Related testbed] for similar antipattern documentation.
 * ═══════════════════════════════════════════════════════════════════════════════
 */
```

**Reference**: `DataManagerTestbed.tsx` for canonical antipattern documentation format.

## Examples

### Example 1: Simple Testbed

```tsx
/**
 * Slider Testbed
 *
 * Demonstrates DAW-grade slider with Effect.Service behaviors.
 *
 * Route: /testbed/slider
 */

import { useState } from 'react'
import { Link } from '@tanstack/react-router'
import { Slider, LinearBehavior } from '@/lib/slider'

export function SliderTestbed() {
  const [value, setValue] = useState(50)

  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-100 p-8">
      <div className="max-w-4xl mx-auto mb-8">
        <Link to="/" className="text-cyan-400 hover:underline text-sm mb-4 block">
          &larr; Back to Home
        </Link>
        <h1 className="text-3xl font-mono font-bold mb-2">Slider Testbed</h1>
        <p className="text-neutral-400">
          DAW-grade slider with runtime-swappable behaviors
        </p>
      </div>

      <div className="max-w-4xl mx-auto">
        <Slider
          value={value}
          onChange={setValue}
          behavior={LinearBehavior.shape}
          config={{ min: 0, max: 100 }}
        />
      </div>
    </div>
  )
}
```

**Route Registration**:
```tsx
// router.tsx
import { SliderTestbed } from './components/testbed/SliderTestbed'

const sliderTestbedRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/testbed/slider',
  component: SliderTestbed,
})
```

**Card Registration**:
```tsx
// App.tsx CARDS array
{
  title: 'SLIDER V1',
  body: 'DAW-grade slider with Effect.Service behaviors. Runtime-swappable linear, log, decibel curves.',
  route: '/testbed/slider',
  status: 'idle',
}
```

### Example 2: Complex Testbed with Sections

```tsx
/**
 * Data Manager Testbed
 *
 * Route: /testbed/data-manager
 */

import { useState } from 'react'
import { Link } from '@tanstack/react-router'
import { DataGrid } from '@/components/data-grid'
import { SectionLabel } from '@/components/testbed/shared'

function DemoSection({
  title,
  description,
  children,
}: {
  title: string
  description: string
  children: React.ReactNode
}) {
  return (
    <div className="p-4 bg-neutral-900/50 rounded-lg border border-neutral-800">
      <h3 className="text-lg font-mono font-bold text-neutral-100 mb-1">{title}</h3>
      <p className="text-sm text-neutral-400 mb-4">{description}</p>
      <div className="space-y-4">{children}</div>
    </div>
  )
}

export function DataManagerTestbed() {
  const [gridData, setGridData] = useState([])

  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-100 p-8">
      <div className="max-w-4xl mx-auto mb-8">
        <Link to="/" className="text-cyan-400 hover:underline text-sm mb-4 block">
          &larr; Back to Home
        </Link>
        <h1 className="text-3xl font-mono font-bold mb-2">Data Manager Testbed</h1>
        <p className="text-neutral-400">
          Effect.Service pattern with kernel architecture
        </p>
      </div>

      <div className="max-w-4xl mx-auto grid gap-6">
        <DemoSection
          title="1. Search Integration"
          description="Progressive streaming search with AG-Grid"
        >
          <DataGrid rowData={gridData} />
        </DemoSection>

        <DemoSection
          title="2. Driver Switching"
          description="FlexSearch vs Linear comparison"
        >
          {/* Driver switching controls */}
        </DemoSection>
      </div>
    </div>
  )
}
```

## Anti-Patterns

### Don't: Forget Step 4 (Portal Card)

```tsx
// ✗ BAD - Route works but card missing from homepage
// User can't discover testbed without directly typing URL
```

**Fix**: Always add card to `App.tsx` CARDS array.

### Don't: Use Inconsistent Naming

```tsx
// ✗ BAD
export function sliderTestbedComponent() { }  // lowercase
export function Slider_Testbed() { }         // snake_case
export function testbedSlider() { }          // inverted order
```

**Fix**: Use `[Feature]Testbed` pattern (PascalCase).

### Don't: Create Routes Without Comments

```tsx
// ✗ BAD
const foo = createRoute({ path: '/testbed/foo', component: Foo })
```

**Fix**: Add descriptive comment.
```tsx
// ✓ GOOD
// Create slider testbed route
const sliderTestbedRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/testbed/slider',
  component: SliderTestbed,
})
```

### Don't: Skip Hypothesis Validation

```tsx
// ✗ BAD - Tracking function calls, not outcomes
setHypotheses(prev => ({ ...prev, h1: true })) // Called setGridData

// ✓ GOOD - Verifying actual outcomes
setHypotheses(prev => ({ ...prev, h1: gridData.length > 0 }))
```

### Don't: Hardcode Paths in Components

```tsx
// ✗ BAD
<Link to="/testbed/slider">...</Link>

// ✓ GOOD - Use card definition route
<Link to={cardDef.route}>...</Link>
```

## Quick Reference

**Create New Testbed Checklist**:
1. Create file: `src/components/testbed/[Feature]Testbed.tsx`
2. Import in `src/router.tsx`
3. Create route constant: `[feature]TestbedRoute`
4. Add to `routeTree.addChildren([...])`
5. Add card to `App.tsx` CARDS array
6. Test route navigation
7. Verify card appears on homepage

**File Template Locations**:
- Basic testbed: `SliderTestbed.tsx`
- Section-based: `DataManagerTestbed.tsx`
- Trait-based: `SliderV2Testbed.tsx`
- Versioned: `DataGridTestbedSwitch.tsx`

**Portal Card Categories**:
- Feature (new capabilities)
- Infrastructure (foundational systems)
- Controls (UI components)
- Abstractions (patterns/DSLs)
