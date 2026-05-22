---
name: react-hoc-patterns
description: Higher-Order Component patterns for TMNL. Covers cross-cutting concerns, behavior injection, and composition. Use for patterns like withSliderDebug, withDraggable, withLayering.
model_invoked: true
triggers:
  - "HOC"
  - "Higher-Order Component"
  - "withSliderDebug"
  - "withDraggable"
  - "withLayering"
  - "behavior injection"
---

# React HOC Patterns for TMNL

## Overview

Higher-Order Components (HOCs) are functions that take a component and return a new component with enhanced behavior. In TMNL, HOCs inject cross-cutting concerns like debugging, drag-and-drop, and layering without modifying the original component.

**Key Insight**: HOCs add behavior, not UI. They wrap components to inject props, add side effects, or intercept renders.

## Canonical Sources

### TMNL Implementations

- **withSliderDebug** — `/src/lib/slider/v1/debug/withSliderDebug.tsx` (debug overlay injection)
  - Wraps any slider component
  - Adds debug panel with state visualization
  - Configurable position and default expanded state
  - Separate standalone panel export

- **withDraggable** — `/src/lib/floating/withDraggable.tsx` (drag + float behavior)
  - Adds @dnd-kit/sortable integration
  - Double-click to float capability
  - STX state management
  - Works with CSS Grid

- **withLayering** — `/src/lib/layers/withLayering.tsx` (layer system integration)
  - Auto-registration on mount
  - Auto-cleanup on unmount
  - Z-index and pointer-events injection

### Reference Documentation

- [React HOC Documentation](https://react.dev/learn/reusing-logic-with-custom-hooks#higher-order-components)
- [HOC vs Hooks](https://kentcdodds.com/blog/when-to-use-higher-order-components)

## Pattern Variants

### Pattern 1: Behavior Injection HOC

Use when adding cross-cutting behavior that doesn't require render interception.

```tsx
import { useCallback, forwardRef, type ComponentType, type ReactNode } from 'react'
import { useSortable } from '@dnd-kit/sortable'
import { CSS } from '@dnd-kit/utilities'

// ─────────────────────────────────────────────────────────────────────────
// Config Type
// ─────────────────────────────────────────────────────────────────────────

export interface DraggableConfig {
  /** Enable float on double-click */
  float?: boolean
  /** Float dimensions */
  floatDimensions?: { width: number; height: number }
}

// ─────────────────────────────────────────────────────────────────────────
// Injected Props Type
// ─────────────────────────────────────────────────────────────────────────

export interface DraggableInjectedProps {
  sortableRef: (node: HTMLElement | null) => void
  sortableAttributes: Record<string, unknown>
  sortableListeners: Record<string, unknown> | undefined
  sortableStyle: CSSProperties
  isDragging: boolean
  isFloating: boolean
  onDoubleClickToFloat: () => void
}

// ─────────────────────────────────────────────────────────────────────────
// Base Props Required
// ─────────────────────────────────────────────────────────────────────────

export interface DraggableProps {
  id: string
  children?: ReactNode
  className?: string
  style?: CSSProperties
}

// ─────────────────────────────────────────────────────────────────────────
// HOC Implementation
// ─────────────────────────────────────────────────────────────────────────

export function withDraggable<P extends object>(
  WrappedComponent: ComponentType<P>,
  config: DraggableConfig = {}
) {
  const { float = false, floatDimensions = { width: 400, height: 300 } } = config

  function DraggableComponent({
    id,
    children,
    className = '',
    style,
    ...restProps
  }: DraggableProps & Omit<P, keyof DraggableProps>) {
    // @dnd-kit sortable hook
    const {
      attributes,
      listeners,
      setNodeRef,
      transform,
      transition,
      isDragging,
    } = useSortable({ id })

    // Sortable style
    const sortableStyle: CSSProperties = {
      transform: CSS.Transform.toString(transform),
      transition,
      opacity: isDragging ? 0.4 : 1,
      cursor: isDragging ? 'grabbing' : 'grab',
      ...style,
    }

    // Double-click handler
    const handleDoubleClick = useCallback(() => {
      if (!float) return
      // Float logic here
    }, [id, float])

    return (
      <div
        ref={setNodeRef}
        style={sortableStyle}
        className={className}
        onDoubleClick={handleDoubleClick}
        {...attributes}
        {...listeners}
      >
        <WrappedComponent {...(restProps as P)}>
          {children}
        </WrappedComponent>
      </div>
    )
  }

  DraggableComponent.displayName = `withDraggable(${WrappedComponent.displayName || WrappedComponent.name || 'Component'})`

  return DraggableComponent
}
```

**Canonical source**: `src/lib/floating/withDraggable.tsx:93-212`

**Key patterns**:
- Config object parameter for HOC options
- Injected props interface for type safety
- `displayName` for React DevTools
- Props spreading with TypeScript generics

### Pattern 2: Render Interception HOC (Debug Overlay)

Use when adding UI elements around the wrapped component.

```tsx
import React, { useState, useCallback } from 'react'
import type { ComponentType } from 'react'
import { useSlider } from '../hooks/useSlider'
import type { SliderProps, SliderDebugInfo } from '../types'

// ─────────────────────────────────────────────────────────────────────────
// HOC Options
// ─────────────────────────────────────────────────────────────────────────

export interface WithSliderDebugOptions {
  /** Initial expanded state */
  defaultExpanded?: boolean
  /** Position of debug overlay */
  position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left'
}

// ─────────────────────────────────────────────────────────────────────────
// Debug Overlay Component
// ─────────────────────────────────────────────────────────────────────────

function DebugOverlay({
  debugInfo,
  isExpanded,
  onToggle,
}: {
  debugInfo: SliderDebugInfo
  isExpanded: boolean
  onToggle: () => void
}) {
  return (
    <div className={`debug-overlay ${isExpanded ? 'expanded' : 'collapsed'}`}>
      {/* Debug UI */}
      <button onClick={onToggle}>{isExpanded ? '×' : '🔍'}</button>
      {isExpanded && (
        <div>
          <div>behavior: {debugInfo.behaviorName}</div>
          <div>value: {debugInfo.rawValue.toFixed(4)}</div>
          <div>normalized: {debugInfo.normalizedValue.toFixed(4)}</div>
        </div>
      )}
    </div>
  )
}

// ─────────────────────────────────────────────────────────────────────────
// HOC Implementation
// ─────────────────────────────────────────────────────────────────────────

export function withSliderDebug<P extends SliderProps>(
  SliderComponent: ComponentType<P>,
  options: WithSliderDebugOptions = {}
) {
  const { defaultExpanded = false, position = 'top-right' } = options

  return function DebugSliderWrapper(props: P) {
    const [isExpanded, setIsExpanded] = useState(defaultExpanded)

    // Intercept slider to get debug info
    const slider = useSlider({
      value: props.value,
      onChange: props.onChange,
      config: props.config,
      behavior: props.behavior,
      debug: true, // ← Enable debug mode
    })

    const toggleExpanded = useCallback(() => setIsExpanded((e) => !e), [])

    return (
      <div className="relative">
        {/* Original component */}
        <SliderComponent {...props} />

        {/* Debug overlay */}
        {slider.debugInfo && (
          <div className={`absolute ${position}`}>
            <DebugOverlay
              debugInfo={slider.debugInfo}
              isExpanded={isExpanded}
              onToggle={toggleExpanded}
            />
          </div>
        )}
      </div>
    )
  }
}
```

**Canonical source**: `src/lib/slider/v1/debug/withSliderDebug.tsx:177-243`

**Key patterns**:
- Render interception with wrapper `<div>`
- Duplicate hook call to access internal state
- Conditional overlay rendering
- Position configuration

### Pattern 3: Lifecycle HOC (Auto-Registration)

Use when adding mount/unmount side effects.

```tsx
import { useEffect, forwardRef, type ComponentType, type ReactNode } from 'react'
import { layerOpsAtom } from '../atoms'
import type { LayerConfig } from '../types'

// ─────────────────────────────────────────────────────────────────────────
// HOC Config
// ─────────────────────────────────────────────────────────────────────────

export interface LayeringConfig {
  name: string
  zIndex: number
  pointerEvents?: 'auto' | 'none' | 'pass-through'
}

// ─────────────────────────────────────────────────────────────────────────
// HOC Implementation
// ─────────────────────────────────────────────────────────────────────────

export function withLayering<P extends object>(
  Component: ComponentType<P>,
  config: LayeringConfig
) {
  return function LayeredComponent(props: P) {
    // Auto-register on mount
    useEffect(() => {
      const layer = {
        id: `layer-${config.name}`,
        name: config.name,
        zIndex: config.zIndex,
        visible: true,
        pointerEvents: config.pointerEvents ?? 'auto',
      }

      // Register
      layerOpsAtom.addLayer(layer)

      // Cleanup on unmount
      return () => {
        layerOpsAtom.removeLayer(layer.id)
      }
    }, [])

    return (
      <div
        data-layer-id={`layer-${config.name}`}
        data-layer-name={config.name}
        style={{
          zIndex: config.zIndex,
          pointerEvents: config.pointerEvents ?? 'auto',
        }}
      >
        <Component {...props} />
      </div>
    )
  }
}

// ─────────────────────────────────────────────────────────────────────────
// Usage
// ─────────────────────────────────────────────────────────────────────────

const BackgroundLayer = withLayering(HoundstoothGOL, {
  name: 'background',
  zIndex: -10,
  pointerEvents: 'auto',
})

<BackgroundLayer />
```

**Key patterns**:
- `useEffect` with cleanup for registration/deregistration
- Data attributes for debugging
- Style injection for z-index and pointer-events

## Decision Tree

```
Need to add behavior to components?
│
├─ Adding cross-cutting concern (drag, debug, layers)?
│  └─ Use: HOC
│     (e.g., withDraggable, withSliderDebug)
│
├─ Behavior is component-specific?
│  └─ Use: Custom Hook instead
│     (e.g., useSlider, useDataManager)
│
├─ Adding UI wrapper around component?
│  └─ Use: Render Interception HOC
│     (e.g., withSliderDebug with overlay)
│
└─ Need mount/unmount side effects?
   └─ Use: Lifecycle HOC
      (e.g., withLayering for auto-registration)
```

## When to Use HOC vs Hooks

| Scenario | Use HOC | Use Hook |
|----------|---------|----------|
| Cross-cutting concern | ✅ Yes | ❌ No |
| Component-specific logic | ❌ No | ✅ Yes |
| Wrapping multiple components | ✅ Yes | ⚠️ Awkward |
| Accessing context | ⚠️ Possible | ✅ Yes |
| Type safety with generics | ⚠️ Complex | ✅ Simple |
| DevTools debugging | ⚠️ Nested | ✅ Flat |

**General rule**: Prefer hooks for new code. Use HOCs when wrapping behavior applies to multiple unrelated components.

## Examples

### Example 1: withSliderDebug Usage

```tsx
import { Slider } from '@/lib/slider'
import { withSliderDebug } from '@/lib/slider/debug'

// Create debug-enhanced slider
const DebugSlider = withSliderDebug(Slider, {
  defaultExpanded: true,
  position: 'top-right',
})

// Use like normal slider
function SliderTestbed() {
  const [value, setValue] = useState(0)

  return (
    <DebugSlider
      value={value}
      onChange={setValue}
      behavior={DecibelBehavior.shape}
      config={{ min: -48, max: 12, step: 0.5 }}
    />
  )
}
```

**Canonical source**: `src/components/testbed/SliderTestbed.tsx`

### Example 2: withDraggable with Sortable Grid

```tsx
import { withDraggable } from '@/lib/floating'
import { TestCard } from '@/components/testbed/shared'

// Wrap card with draggable behavior
const DraggableCard = withDraggable(TestCard, {
  float: { enabled: true, title: 'My Card' },
  floatDimensions: { width: 400, height: 300 },
})

// Use in sortable grid
function GridLayout() {
  const [items, setItems] = useState(['card-1', 'card-2', 'card-3'])

  return (
    <SortableContext items={items}>
      <div className="grid grid-cols-3 gap-4">
        {items.map((id) => (
          <DraggableCard key={id} id={id} title={`Card ${id}`}>
            Content
          </DraggableCard>
        ))}
      </div>
    </SortableContext>
  )
}
```

**Canonical source**: `src/lib/floating/withDraggable.tsx:15-23`

### Example 3: Standalone Debug Panel

Separate export for when you want debug panel decoupled from HOC.

```tsx
import { SliderDebugPanel } from '@/lib/slider/debug'

function CustomSlider() {
  const slider = useSlider({ value: 0.5, debug: true })

  return (
    <div className="grid grid-cols-2">
      {/* Slider UI */}
      <div ref={slider.containerRef} onPointerDown={slider.handlePointerDown}>
        <div style={{ width: `${slider.normalizedValue * 100}%` }} />
      </div>

      {/* Debug panel in separate column */}
      <SliderDebugPanel debugInfo={slider.debugInfo} />
    </div>
  )
}
```

**Canonical source**: `src/lib/slider/v1/debug/withSliderDebug.tsx:249-369`

## Anti-Patterns (BANNED)

### Mutating Props

```tsx
// BANNED - Never mutate props
function withBad<P>(Component: ComponentType<P>) {
  return function Bad(props: P) {
    props.className = 'mutated' // ← WRONG!
    return <Component {...props} />
  }
}

// CORRECT - Spread and override
function withGood<P extends { className?: string }>(Component: ComponentType<P>) {
  return function Good(props: P) {
    return <Component {...props} className={`${props.className} enhanced`} />
  }
}
```

### Nested HOCs Without displayName

```tsx
// BANNED - DevTools shows "Component" x5
const Enhanced = withA(withB(withC(withD(withE(MyComponent)))))

// CORRECT - Each HOC sets displayName
function withA<P>(Component: ComponentType<P>) {
  function WithA(props: P) { /* ... */ }
  WithA.displayName = `withA(${Component.displayName || Component.name})`
  return WithA
}
```

### HOC for Component-Specific Logic

```tsx
// BANNED - Use hook instead
function withSliderValue<P>(Component: ComponentType<P>) {
  return function WithSlider(props: P) {
    const [value, setValue] = useState(0)
    return <Component {...props} value={value} onChange={setValue} />
  }
}

// CORRECT - Use hook
function useSliderValue() {
  const [value, setValue] = useState(0)
  return { value, setValue }
}
```

### Static Property Loss

```tsx
// BANNED - Loses static properties
function withEnhance<P>(Component: ComponentType<P>) {
  return function Enhanced(props: P) {
    return <Component {...props} />
  }
}

MyComponent.staticMethod = () => {}
const Enhanced = withEnhance(MyComponent)
Enhanced.staticMethod // ← undefined!

// CORRECT - Use hoist-non-react-statics or manual copy
import hoistNonReactStatics from 'hoist-non-react-statics'

function withEnhance<P>(Component: ComponentType<P>) {
  function Enhanced(props: P) {
    return <Component {...props} />
  }
  return hoistNonReactStatics(Enhanced, Component)
}
```

## Implementation Checklist

When creating a HOC:

- [ ] **Name**: Prefix with `with` (e.g., `withDraggable`)
- [ ] **displayName**: Set for DevTools visibility
- [ ] **Config**: Accept options object for configurability
- [ ] **Generics**: Use `<P extends object>` for type safety
- [ ] **Props**: Define injected props interface
- [ ] **Spread**: Use rest/spread for prop forwarding
- [ ] **TypeScript**: Export HOC config and injected props types
- [ ] **Documentation**: Add JSDoc with usage example
- [ ] **Cleanup**: Return cleanup functions from useEffect if needed

## Composition Patterns

### Composing Multiple HOCs

```tsx
// Sequential composition
const Enhanced = withA(withB(withC(Component)))

// Compose helper
function compose(...hocs) {
  return (Component) => hocs.reduceRight((acc, hoc) => hoc(acc), Component)
}

const Enhanced = compose(
  withA,
  withB,
  withC
)(Component)
```

### HOC with Hook Integration

```tsx
function withDataManager<P extends object>(Component: ComponentType<P>) {
  return function WithDataManager(props: P) {
    const dataManager = useDataManager()

    return <Component {...props} dataManager={dataManager} />
  }
}
```

## Related Patterns

- **react-hook-composition** — HOCs often wrap hooks internally
- **react-compound-components** — HOCs can enhance compound components
- **effect-patterns** — HOCs can inject Effect service atoms

## Filing New Patterns

When you discover a new HOC pattern:

1. Implement in `src/lib/<domain>/` with full TypeScript types
2. Add usage example in testbed
3. Update this skill with canonical source references
4. Document config options and injected props
