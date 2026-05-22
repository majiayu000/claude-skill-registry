---
name: theatre-js
description: Use when implementing motion design, timeline animations, visual animation editors, animating Three.js/R3F scenes, creating keyframe animations, or using Theatre.js, @theatre/core, @theatre/studio, @theatre/r3f, theatric, or building animation tooling for the web.
---

# Theatre.js Best Practices

Motion design editor and animation library for the web. Provides a visual timeline editor (Studio) with programmatic control.

## Installation

```bash
# Core + Studio (development)
npm install @theatre/core@0.7 @theatre/studio@0.7

# React Three Fiber integration
npm install @theatre/r3f@0.7

# React utilities
npm install @theatre/react

# Theatric (simplified controls)
npm install theatric
```

## Quick Start

```tsx
import * as core from '@theatre/core'
import studio from '@theatre/studio'

// Initialize Studio (dev only)
if (import.meta.env.DEV) {
  studio.initialize()
}

// Create project → sheet → object
const project = core.getProject('My Project')
const sheet = project.sheet('Main')
const obj = sheet.object('Box', {
  position: { x: 0, y: 0 },
  opacity: 1
})

// Read values
console.log(obj.value.position.x)

// Listen to changes
obj.onValuesChange((values) => {
  element.style.opacity = values.opacity
  element.style.transform = `translate(${values.position.x}px, ${values.position.y}px)`
})

// Play animation
sheet.sequence.play({ iterationCount: Infinity })
```

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Project** | Container for all animation data; maps to exported JSON state |
| **Sheet** | A scene or component; contains objects and one sequence |
| **Object** | Animatable entity with typed props |
| **Sequence** | Timeline with keyframes; controls playback |
| **Props** | Typed values (number, compound, rgba, etc.) |

## Reference Index

| Reference | Use When |
|-----------|----------|
| `references/01-core.md` | Project setup, sheets, objects, sequences, playback control |
| `references/02-prop-types.md` | Defining props, custom types, compound props, constraints |
| `references/03-studio.md` | Studio UI, keyboard shortcuts, extensions, panels |
| `references/04-react-integration.md` | useVal, usePrism, @theatre/react hooks |
| `references/05-r3f-integration.md` | React Three Fiber, editable components, SheetProvider |
| `references/06-production.md` | Export state, assets, deployment, tree-shaking |

## Common Patterns

### Animate DOM Element

```tsx
const obj = sheet.object('Card', {
  x: 0,
  y: 0,
  rotation: 0,
  scale: 1,
  opacity: 1
})

obj.onValuesChange(({ x, y, rotation, scale, opacity }) => {
  element.style.transform = `translate(${x}px, ${y}px) rotate(${rotation}deg) scale(${scale})`
  element.style.opacity = opacity
})
```

### Sequence Playback Control

```tsx
const seq = sheet.sequence

// Play once
seq.play()

// Play with options
seq.play({
  iterationCount: Infinity,  // loop forever
  range: [0, 2],             // play seconds 0-2
  rate: 1.5,                 // 1.5x speed
  direction: 'alternate'     // ping-pong
})

// Pause and seek
seq.pause()
seq.position = 1.5  // jump to 1.5s

// Await completion
await seq.play({ iterationCount: 1 })
console.log('Animation complete')
```

### React Three Fiber Scene

```tsx
import { Canvas } from '@react-three/fiber'
import { editable as e, SheetProvider } from '@theatre/r3f'
import { getProject } from '@theatre/core'
import studio from '@theatre/studio'
import extension from '@theatre/r3f/dist/extension'

// Dev setup
if (import.meta.env.DEV) {
  studio.initialize()
  studio.extend(extension)
}

const sheet = getProject('R3F Demo').sheet('Scene')

function App() {
  return (
    <Canvas>
      <SheetProvider sheet={sheet}>
        <e.mesh theatreKey="Cube">
          <boxGeometry />
          <meshStandardMaterial color="orange" />
        </e.mesh>
        <e.pointLight theatreKey="Light" position={[10, 10, 10]} />
      </SheetProvider>
    </Canvas>
  )
}
```

### Theatric Controls (Simple)

```tsx
import { useControls, types } from 'theatric'

function Component() {
  const { color, intensity, position } = useControls({
    color: '#ff0000',
    intensity: types.number(1, { range: [0, 2] }),
    position: { x: 0, y: 0, z: 0 }
  })

  return <mesh position={[position.x, position.y, position.z]} />
}
```

## Critical Mistakes to Avoid

### 1. Studio in Production
```tsx
// ❌ Includes studio in bundle
import studio from '@theatre/studio'
studio.initialize()

// ✅ Dev-only initialization
if (import.meta.env.DEV) {
  studio.initialize()
}
```

### 2. Missing State in Production
```tsx
// ❌ No animations without state
const project = core.getProject('My Project')

// ✅ Load exported state
import state from './state.json'
const project = core.getProject('My Project', { state })
```

### 3. Object Key Collisions
```tsx
// ❌ Same key = same object (shared state)
sheet.object('Box', { x: 0 })
sheet.object('Box', { y: 0 })  // Overwrites!

// ✅ Unique keys per object
sheet.object('Box1', { x: 0 })
sheet.object('Box2', { y: 0 })
```

### 4. Missing R3F Extension
```tsx
// ❌ No 3D controls in Studio
studio.initialize()

// ✅ Extend with R3F extension
import extension from '@theatre/r3f/dist/extension'
studio.initialize()
studio.extend(extension)
```

### 5. Forgetting theatreKey
```tsx
// ❌ Not editable
<e.mesh>

// ✅ Requires theatreKey
<e.mesh theatreKey="MyCube">
```

## Quick Reference

| Task | Solution |
|------|----------|
| Create project | `getProject('Name', { state? })` |
| Create sheet | `project.sheet('Name')` |
| Create object | `sheet.object('Key', { props })` |
| Listen to values | `obj.onValuesChange(cb)` |
| Read value | `obj.value.propName` |
| Play animation | `sheet.sequence.play(opts?)` |
| Pause animation | `sheet.sequence.pause()` |
| Seek position | `sheet.sequence.position = 1.5` |
| R3F editable | `<e.mesh theatreKey="Key">` |
| React value hook | `useVal(obj.props.x)` |
| Export state | Studio → Project → Export (JSON) |
