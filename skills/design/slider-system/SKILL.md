---
name: slider-system
description: DAW-grade slider system for TMNL. Invoke when implementing sliders, precision controls, behavior curves, or audio-style UI. Provides Effect.Service patterns, trait composition, and debug overlays.
model_invoked: true
triggers:
  - "slider"
  - "DAW slider"
  - "precision control"
  - "SliderBehavior"
  - "decibel"
  - "logarithmic"
  - "sensitivity"
  - "modifier keys"
  - "Shift+drag"
  - "fine control"
---

# Slider System for TMNL

## Overview

A DAW-grade slider system with:
- **Runtime-swappable behaviors** via Effect.Service (linear, log, decibel, exp, stepped)
- **Precision modifiers** (Shift=0.1x, Ctrl=0.01x, Alt=snap)
- **Debug overlays** via HOC pattern
- **Two versions**: v1 (Effect.Service), v2 (Trait-based)

## Canonical Sources

### TMNL Implementations

| File | Purpose | Pattern |
|------|---------|---------|
| `src/lib/slider/index.ts` | Barrel export, v1/v2 routing | Version switching |
| `src/lib/slider/v1/services/SliderBehavior.ts` | Effect.Service behaviors | Context.Tag strategy |
| `src/lib/slider/v1/types.ts` | Core types (SliderState, SliderConfig) | Schema candidates |
| `src/lib/slider/v1/atoms/index.ts` | effect-atom integration | Atom.runtime pattern |
| `src/lib/slider/v1/hooks/useSlider.ts` | Primary React hook | useReducer + Effect |
| `src/lib/slider/v2/traits/` | Trait-based composition | Trait injection |
| `src/lib/slider/v2/effects/` | Effect-ified animations | Overshoot, emanation |

### Testbeds

- **SliderTestbed**: `/testbed/slider` — v1 DAW-grade demonstration
- **SliderV2Testbed**: `/testbed/slider-v2` — v2 trait-based demonstration

---

## Pattern 1: SliderBehavior Service — STRATEGY PATTERN

**When:** Implementing a slider with swappable value transformation curves.

The SliderBehavior service uses `Context.Tag` (not `Effect.Service<>()`) because it has **multiple swappable implementations**.

```typescript
import { Context, Layer } from 'effect'
import type { ModifierKeys, SliderBehaviorShape, SliderConfig } from '../types'

// Tag definition (strategy interface)
export class SliderBehavior extends Context.Tag('tmnl/slider/SliderBehavior')<
  SliderBehavior,
  SliderBehaviorShape
>() {}

// Interface shape
interface SliderBehaviorShape {
  readonly id: string
  readonly name: string
  normalize(value: number, min: number, max: number): number
  denormalize(normalized: number, min: number, max: number): number
  getSensitivity(modifiers: ModifierKeys, config: SliderConfig): number
  snap(value: number, step: number | null, min: number, max: number): number
  format(value: number, precision: number, unit: string): string
  getTicks(min: number, max: number, count: number): number[]
}

// Implementation (Linear)
const linearBehavior: SliderBehaviorShape = {
  id: 'linear',
  name: 'Linear',
  normalize: (value, min, max) => (value - min) / (max - min),
  denormalize: (normalized, min, max) => min + normalized * (max - min),
  // ... other methods
}

// Export BOTH Layer AND shape
export const LinearBehavior = {
  Default: Layer.succeed(SliderBehavior, linearBehavior),
  shape: linearBehavior,  // ← Direct access without Layer
}
```

**Key Pattern**: Export `.Default` (Layer) AND `.shape` (direct object).

**TMNL Location**: `src/lib/slider/v1/services/SliderBehavior.ts:15`

---

## Pattern 2: Built-in Behaviors — THE FIVE CURVES

### Linear (Default)

Uniform distribution. Best for percentage values.

```typescript
import { LinearBehavior } from '@/lib/slider'

<Slider behavior={LinearBehavior.shape} config={{ min: 0, max: 100 }} />
```

### Logarithmic

For frequency (Hz) and gain. More resolution at lower values.

```typescript
import { LogarithmicBehavior } from '@/lib/slider'

// Default base 10
<Slider behavior={LogarithmicBehavior.shape(10)} config={{ min: 20, max: 20000, unit: 'Hz' }} />
```

**Formatting**: Smart k-suffix (20000 → "20kHz")

### Decibel

Audio gain with 0dB reference. Non-linear curve gives more resolution near unity.

```typescript
import { DecibelBehavior } from '@/lib/slider'

<Slider behavior={DecibelBehavior.shape} config={{ min: -48, max: 12, unit: 'dB' }} />
```

**Formatting**: Sign prefix (+3.0dB, -12.0dB)

**Ticks**: Standard dB stops (-48, -24, -12, -6, -3, 0, +3, +6)

### Exponential

For time constants (attack, release). More resolution at lower values.

```typescript
import { ExponentialBehavior } from '@/lib/slider'

// Exponent 2 (default)
<Slider behavior={ExponentialBehavior.shape(2)} config={{ min: 0, max: 5000, unit: 'ms' }} />
```

**Formatting**: Smart time conversion (5000ms → "5.00s")

### Stepped

Discrete values only. Perfect for quantized presets.

```typescript
import { SteppedBehavior } from '@/lib/slider'

const presets = [0, 25, 50, 75, 100]
<Slider behavior={SteppedBehavior.shape(presets)} config={{ min: 0, max: 100 }} />
```

**Behavior**: Always snaps to nearest preset value.

---

## Pattern 3: Precision Modifiers — DAW CONTROL

**Modifier key sensitivity multipliers for fine-grained control.**

| Modifier | Sensitivity | Use Case |
|----------|-------------|----------|
| None | 1.0x | Normal dragging |
| Shift | 0.1x | Fine adjustment |
| Ctrl | 0.01x | Ultra-fine (sub-dB precision) |
| Alt | Snap | Force snap to step |

### Configuration

```typescript
const config: SliderConfig = {
  min: -48,
  max: 12,
  step: 0.5,

  // Sensitivity multipliers
  baseSensitivity: 1,
  shiftSensitivity: 0.1,
  ctrlSensitivity: 0.01,
  altSnap: true,  // Force snap when Alt pressed
}
```

### Implementation in Behavior

```typescript
getSensitivity(modifiers: ModifierKeys, config: SliderConfig): number {
  if (modifiers.ctrl) return config.ctrlSensitivity  // 0.01x
  if (modifiers.shift) return config.shiftSensitivity  // 0.1x
  return config.baseSensitivity  // 1.0x
}
```

**TMNL Location**: `src/lib/slider/v1/services/SliderBehavior.ts:36`

---

## Pattern 4: useSlider Hook — REACT INTEGRATION

**When:** Building a slider component with full state management.

```typescript
import { useSlider, LinearBehavior } from '@/lib/slider'

function MySlider({ value, onChange }) {
  const slider = useSlider({
    value,
    onChange,
    behavior: LinearBehavior.shape,
    config: { min: 0, max: 100, step: 1 },
    debug: true,  // Enable debug overlay
  })

  return (
    <div
      ref={slider.containerRef}
      className={cn('slider', slider.state.isDragging && 'dragging')}
      onPointerDown={slider.handlePointerDown}
      onKeyDown={slider.handleKeyDown}
      onWheel={slider.handleWheel}
      onDoubleClick={slider.handleDoubleClick}
      tabIndex={0}
    >
      <div
        className="track"
        style={{ '--progress': `${slider.state.normalizedValue * 100}%` }}
      />
      <div
        className="thumb"
        style={{ left: `${slider.state.normalizedValue * 100}%` }}
      />
      <span className="value">{slider.displayValue}</span>

      {slider.debug && (
        <SliderDebugPanel debugInfo={slider.debugInfo} />
      )}
    </div>
  )
}
```

### Hook Return Shape

```typescript
interface UseSliderReturn {
  // State
  state: SliderState
  displayValue: string
  ticks: number[]

  // Refs
  containerRef: React.RefObject<HTMLDivElement>

  // Event handlers
  handlePointerDown: (e: React.PointerEvent) => void
  handleKeyDown: (e: React.KeyboardEvent) => void
  handleWheel: (e: React.WheelEvent) => void
  handleDoubleClick: () => void

  // Debug
  debug: boolean
  debugInfo: SliderDebugInfo | null
}
```

**TMNL Location**: `src/lib/slider/v1/hooks/useSlider.ts`

---

## Pattern 5: Debug Overlay HOC — withSliderDebug

**When:** Adding debug overlays to any slider component.

```typescript
import { Slider, withSliderDebug } from '@/lib/slider'

// Wrap any slider component
const DebugSlider = withSliderDebug(Slider, { defaultExpanded: true })

<DebugSlider
  value={value}
  onChange={onChange}
  behavior={LinearBehavior.shape}
  config={{ min: 0, max: 100 }}
/>
```

### Debug Panel Information

| Field | Description |
|-------|-------------|
| behaviorId | "linear", "decibel", etc. |
| rawValue | Actual numeric value |
| normalizedValue | 0-1 position |
| displayValue | Formatted string ("50.0%") |
| activeSensitivity | Current multiplier |
| activeModifiers | ["Shift"], ["Ctrl"], etc. |
| isDragging | Interaction state |
| lastUpdateMs | Performance metric |

**TMNL Location**: `src/lib/slider/v1/debug/withSliderDebug.tsx`

---

## Pattern 6: Slider V2 — TRAIT-BASED COMPOSITION

**When:** Using the newer trait-based slider (experimental).

V2 uses trait injection instead of Effect.Service for composition.

```typescript
import { v2 } from '@/lib/slider'

<v2.Slider
  value={value}
  onChange={onChange}
  traits={[
    v2.CurveTrait.logarithmic(10),
    v2.PrecisionTrait.daw(),
    v2.OvershootTrait.elastic(),
  ]}
  config={{ min: 20, max: 20000 }}
/>
```

### Available V2 Traits

| Trait | Purpose |
|-------|---------|
| `CurveTrait` | Value transformation (linear, log, exp) |
| `PrecisionTrait` | Modifier key sensitivity |
| `OvershootTrait` | Overshoot boundary animation |

### V2 Effects (anime.js v4)

| Effect | Purpose |
|--------|---------|
| `OvershootEffect` | Elastic bounce on boundary hit |
| `EmanationEffect` | Radial glow on value change |
| `SettleEffect` | Smooth settle after drag end |

**TMNL Location**: `src/lib/slider/v2/`

---

## Pattern 7: SliderState Reducer — EFFECT-ATOM INTEGRATION

**When:** Understanding the state machine for slider interactions.

```typescript
import { Atom } from '@effect-rx/rx-react'

// Reducer handles all state transitions
type SliderAction =
  | { type: 'SET_VALUE'; value: number }
  | { type: 'DRAG_START'; x: number; y: number }
  | { type: 'DRAG_MOVE'; x: number; y: number }
  | { type: 'DRAG_END' }
  | { type: 'MODIFIER_CHANGE'; modifiers: Partial<ModifierKeys> }
  | { type: 'RESET' }

const sliderReducer = (
  state: SliderState,
  action: SliderAction,
  behavior: SliderBehaviorShape,
  config: SliderConfig
): SliderState => {
  switch (action.type) {
    case 'DRAG_START':
      return {
        ...state,
        isDragging: true,
        dragStartValue: state.value,
        dragStartX: action.x,
        dragStartY: action.y,
      }
    case 'DRAG_MOVE': {
      const sensitivity = behavior.getSensitivity(state.modifiers, config)
      const delta = (state.dragStartY! - action.y) * sensitivity
      const newNormalized = state.normalizedValue + delta / 100
      const clamped = Math.max(0, Math.min(1, newNormalized))
      const newValue = behavior.denormalize(clamped, config.min, config.max)
      const snapped = behavior.snap(newValue, config.step, config.min, config.max)

      return {
        ...state,
        value: snapped,
        normalizedValue: behavior.normalize(snapped, config.min, config.max),
        activeSensitivity: sensitivity,
      }
    }
    // ... other cases
  }
}
```

**TMNL Location**: `src/lib/slider/v1/atoms/index.ts`

---

## Decision Tree: Which Behavior?

```
What are you controlling?
│
├─ Percentage (0-100)?
│  └─ LinearBehavior
│
├─ Frequency (Hz)?
│  └─ LogarithmicBehavior(10)
│
├─ Audio gain (dB)?
│  └─ DecibelBehavior
│
├─ Time constant (ms)?
│  └─ ExponentialBehavior(2)
│
├─ Discrete presets?
│  └─ SteppedBehavior([...values])
│
└─ Custom curve?
   └─ Implement SliderBehaviorShape interface
```

---

## Anti-Patterns

### Don't: Use useState for slider value when crossing boundaries

```typescript
// BANNED - loses precision, no behavior integration
const [value, setValue] = useState(50)
<input type="range" value={value} onChange={e => setValue(e.target.value)} />

// CORRECT - use useSlider hook
const slider = useSlider({ value, onChange, behavior: LinearBehavior.shape })
```

### Don't: Hardcode sensitivity values

```typescript
// BANNED - ignores configuration
const delta = (startY - currentY) * 0.5

// CORRECT - use behavior.getSensitivity
const sensitivity = behavior.getSensitivity(modifiers, config)
const delta = (startY - currentY) * sensitivity
```

### Don't: Skip the snap step

```typescript
// BANNED - may produce invalid values
const newValue = behavior.denormalize(normalized, min, max)
onChange(newValue)

// CORRECT - always snap
const newValue = behavior.denormalize(normalized, min, max)
const snapped = behavior.snap(newValue, config.step, min, max)
onChange(snapped)
```

---

## Integration Points

**Depends on:**
- `effect-patterns` — Context.Tag, Layer.succeed
- `effect-atom-integration` — Atom.make, useAtomValue
- `react-hook-composition` — Custom hook patterns

**Used by:**
- `ag-grid-patterns` — Slider cell editors
- `tmnl-animation-tokens` — Slider value animations
- `ux-interaction-patterns` — DAW-grade controls

---

## Quick Reference

| Task | Pattern | File |
|------|---------|------|
| Create linear slider | `LinearBehavior.shape` | v1/services/SliderBehavior.ts:67 |
| Create dB slider | `DecibelBehavior.shape` | v1/services/SliderBehavior.ts:201 |
| Add debug overlay | `withSliderDebug(Slider)` | v1/debug/withSliderDebug.tsx |
| Use precision modifiers | Configure `shiftSensitivity`, `ctrlSensitivity` | v1/types.ts:84 |
| Implement custom behavior | Implement `SliderBehaviorShape` | v1/types.ts:130 |
| Use trait-based slider | `v2.Slider` with `traits` prop | v2/index.ts |
