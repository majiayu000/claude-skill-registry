---
name: explanatory-playground
description: Build interactive debugging interfaces that reveal internal system behavior. Use when asked to "help me understand how this works", "show me what's happening", "visualize the state", "build a debug view", "I can't see what's going on", or any request to make opaque system behavior visible. Applies to state machines, data flow, event systems, algorithms, render cycles, animations, CSS calculations, or any mechanism with hidden internals.
---

# Explanatory Playground

Build dev-only visualizations that make invisible system behavior visible.

## Workflow

### 1. Clarify the target

Use AskUserQuestion to understand what needs visualization:

```
question: "What kind of system should the playground reveal?"
header: "System type"
options:
  - label: "State machine"
    description: "Finite states with transitions (auth flow, form wizard, game state)"
  - label: "Data flow"
    description: "Data transforming through a pipeline (API → transform → render)"
  - label: "Event system"
    description: "Publishers and subscribers, event propagation"
  - label: "Algorithm"
    description: "Step-by-step logic (sorting, pathfinding, search)"
```

Then ask what's confusing:

```
question: "What specifically is hard to understand?"
header: "Hidden aspect"
options:
  - label: "Current state"
    description: "I can't see what state the system is in right now"
  - label: "Why transitions happen"
    description: "I don't know what triggers changes or why"
  - label: "Data shape"
    description: "I can't see what the data looks like at each step"
  - label: "Timing/sequence"
    description: "Things happen too fast or in unclear order"
```

### 2. Identify what's hidden

Based on answers, determine what to surface:
- **State** — Values that change over time
- **Transitions** — Events that trigger changes
- **Relationships** — How parts communicate
- **Logic** — Conditions, thresholds, rules

### 3. Pick visualization approach

| System | Visualization | Library |
|--------|--------------|---------|
| State machines | Node-edge graph | react-flow |
| Data flow | Directed graph / Sankey | react-flow |
| Events | Timeline | custom or recharts |
| Algorithms | Step animation | custom |
| Render cycles | Component tree + diffs | custom |
| Animations | Timeline scrubber | custom |
| CSS/Layout | Box model overlay | custom |

See [references/patterns.md](references/patterns.md) for layouts, code, and implementation details.

### 4. Choose interactivity level

Ask if unclear:

```
question: "How interactive should the playground be?"
header: "Interactivity"
options:
  - label: "Just show me (Recommended)"
    description: "Real-time display of state and changes"
  - label: "Let me poke around"
    description: "Click/hover to inspect details and trace origins"
  - label: "Let me trigger things"
    description: "Fire events, modify state, inject test data"
  - label: "Time travel"
    description: "Record history, scrub through past states, replay"
```

| Level | Features | When |
|-------|----------|------|
| 1 - Observe | Real-time state display | Always |
| 2 - Inspect | Click/hover for details | Usually |
| 3 - Manipulate | Trigger events, modify state | Edge cases |
| 4 - Time travel | History scrubbing, replay | Race conditions |

Start with 1-2. Add 3-4 when needed.

### 6. Instrument minimally

**Prefer event emitters** (least invasive):
```typescript
const debugEmitter = new EventEmitter();
function transition(from, to, event) {
  debugEmitter.emit('transition', { from, to, event, timestamp: Date.now() });
  // existing logic...
}
```

**Use proxies** for third-party code:
```typescript
function observable<T extends object>(obj: T) {
  return new Proxy(obj, {
    set(target, prop, value) {
      window.dispatchEvent(new CustomEvent('state:change', {
        detail: { prop, old: target[prop], new: value }
      }));
      return Reflect.set(target, prop, value);
    }
  });
}
```

### 7. Create dev-only route

```
app/__dev/[system-name]/page.tsx
```

Guard against production:
```typescript
if (process.env.NODE_ENV !== 'development') {
  return notFound();
}
```

### 8. Document removal

Header in every created file:
```typescript
/**
 * EXPLANATORY-PLAYGROUND DEBUG TOOL
 * Remove when done:
 * 1. Delete: app/__dev/[name]/page.tsx
 * 2. Delete: src/lib/[system]-debug.ts
 * 3. Remove hooks from: src/lib/[system].ts (lines XX-YY)
 * Purpose: [what this debugs]
 */
```

## Cleanup

On removal request:
1. Delete `__dev/` route
2. Remove instrumentation (emitters, proxies)
3. Uninstall added deps if unused elsewhere
4. Search for `EXPLANATORY-PLAYGROUND` markers

Report what was removed.
