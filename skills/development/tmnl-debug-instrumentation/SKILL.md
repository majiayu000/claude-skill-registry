---
name: tmnl-debug-instrumentation
description: DebugScope patterns, DebugScopeProvider, useDebugScope. Console logging via Effect.Console. Conditional debug activation.
triggers:
  - "debug"
  - "debug scope"
  - "instrumentation"
  - "debug logging"
  - "effect console"
---

# TMNL Debug Instrumentation Patterns

Canonical patterns for component instrumentation, lifecycle logging, and conditional debug activation using DebugScope and Effect.Console.

## Overview

TMNL's debug instrumentation system provides:
- **Per-component debug context** with conditional activation
- **Lifecycle event logging** (mount, unmount, update)
- **Dependency tracking** with diff detection
- **Rich metadata rendering** via Effect Console
- **Hierarchical scoping** (parent.child.grandchild)
- **No-op when disabled** (zero runtime cost)

**Location**: `src/lib/debug/DebugScope.tsx`

## Canonical Sources

**Primary Files**:
- `src/lib/debug/DebugScope.tsx` - Complete DebugScope implementation
- `src/lib/screensaver/__tests__/useScreensaver.test.tsx` - Test usage examples
- `src/components/testbed/ScreensaverTestbed.tsx` - Production usage

**Pattern Reference**:
- Provider pattern (`DebugScopeProvider`)
- Content pattern (`<DebugScope />`)
- Hook pattern (`useDebugScope()`)
- Context access (`useDebugScopeContext()`)

## Patterns

### 1. Provider Pattern (Wrap Component Subtree)

**When to Use**: Instrument a component tree with shared debug context.

**Implementation**:

```tsx
import { DebugScopeProvider } from "@/lib/debug/DebugScope"

function ScreensaverSystem({ debug }: { debug?: boolean }) {
  return (
    <DebugScopeProvider debug={debug} name="ScreensaverSystem">
      <ScreensaverOverlay />
      <IdleDetector />
      <AsciiRenderer />
    </DebugScopeProvider>
  )
}
```

**Features**:
- All children can access scope via `useDebugScopeContext()`
- Lifecycle logging for provider mount/unmount
- Metadata passed to all child scopes

**Lifecycle Output** (when `debug={true}`):
```
[ScreensaverSystem] PROVIDER MOUNT
[ScreensaverSystem] PROVIDER UNMOUNT { duration: "1234.56ms" }
```

### 2. Content Pattern (Render-Nothing Instrumentation)

**When to Use**: Instrument a component without wrapping it in a provider.

**Implementation**:

```tsx
import { DebugScope } from "@/lib/debug/DebugScope"

function Screensaver({ debug, isActive, timeRemaining }: ScreensaverProps) {
  return (
    <>
      <DebugScope
        debug={debug}
        name="Screensaver"
        watch={{ isActive, timeRemaining }}
      />
      {isActive && <AsciiScene />}
    </>
  )
}
```

**Features**:
- Renders `null` (no DOM output)
- Logs lifecycle events (mount, unmount)
- Tracks changes to `watch` object
- No provider wrapper needed

**Lifecycle Output**:
```
[Screensaver] MOUNT { watch: { isActive: false, timeRemaining: 300000 } }
[Screensaver] WATCH CHANGED { changes: { isActive: { from: false, to: true } } }
[Screensaver] UNMOUNT { duration: "2345.67ms" }
```

### 3. Hook Pattern (Imperative Logging)

**When to Use**: Need custom logging inside component logic.

**Implementation**:

```tsx
import { useDebugScope } from "@/lib/debug/DebugScope"

function MyComponent({ debug, count, status }: MyComponentProps) {
  const scope = useDebugScope({
    debug,
    name: "MyComponent",
    deps: [count, status],
    depLabels: ["count", "status"],
  })

  const handleClick = () => {
    scope.log("Button clicked", { count, status })
  }

  useEffect(() => {
    scope.log("Effect triggered", { reason: "count changed" })
  }, [count])

  return <button onClick={handleClick}>Click Me</button>
}
```

**Features**:
- Full control over logging
- Dependency change detection with labels
- Custom event logging
- Lifecycle logging automatic

**Output**:
```
[MyComponent] MOUNT { count: 0, status: "idle" }
[MyComponent] DEPS CHANGED { changes: [{ count: { from: 0, to: 1 } }] }
[MyComponent] Button clicked { count: 1, status: "idle" }
[MyComponent] Effect triggered { reason: "count changed" }
[MyComponent] UNMOUNT { duration: "456.78ms" }
```

### 4. Context Access Pattern (Child Scopes)

**When to Use**: Access parent DebugScopeProvider from child components.

**Implementation**:

```tsx
import { useDebugScopeContext } from "@/lib/debug/DebugScope"

function ChildComponent() {
  const parentScope = useDebugScopeContext()

  // Create child scope
  const childScope = parentScope.child("ChildComponent")

  const handleEvent = () => {
    childScope.log("Event handled")
  }

  return <div onClick={handleEvent}>Child</div>
}
```

**Features**:
- Inherits parent's debug state (enabled/disabled)
- Hierarchical naming: `[Parent.ChildComponent]`
- No-op if no parent provider

**Output** (with parent named "System"):
```
[System.ChildComponent] Event handled
```

### 5. Effect.Console Integration

**Pattern**: Use `Effect.Console` for rich metadata logging.

**Why Effect.Console**:
- Structured logging (not just strings)
- Metadata objects rendered beautifully
- Integration with Effect runtime spans/traces
- Consistent with TMNL's Effect-first architecture

**Implementation** (from DebugScope.tsx):

```tsx
import { Effect, Console } from "effect"

const log = (message: string, data?: Record<string, unknown>) => {
  if (!enabled) return
  const payload = { ...metadata, ...data }
  if (Object.keys(payload).length > 0) {
    Effect.runSync(Console.log(`${prefix} ${message}`, payload))
  } else {
    Effect.runSync(Console.log(`${prefix} ${message}`))
  }
}
```

**Usage**:

```tsx
scope.log("Animation started", {
  duration: 300,
  easing: "power2.out",
  targets: ["#logo", "#tagline"],
})
```

**Output**:
```
[AnimationSequence] Animation started {
  duration: 300,
  easing: "power2.out",
  targets: ["#logo", "#tagline"]
}
```

### 6. Conditional Debug Activation

**Pattern**: Pass `debug` prop to control instrumentation at runtime.

**Three Activation Strategies**:

#### A. Environment Variable

```tsx
// In component
const debug = import.meta.env.DEV && import.meta.env.VITE_DEBUG === "true"

<DebugScopeProvider debug={debug} name="MyComponent">
  ...
</DebugScopeProvider>
```

#### B. URL Query Parameter

```tsx
import { useSearchParams } from "@tanstack/react-router"

function MyComponent() {
  const searchParams = useSearchParams()
  const debug = searchParams.debug === "true"

  return (
    <DebugScopeProvider debug={debug} name="MyComponent">
      ...
    </DebugScopeProvider>
  )
}
```

**Usage**: Navigate to `/testbed/feature?debug=true`

#### C. Testbed Prop

```tsx
export function FeatureTestbed() {
  const [debug, setDebug] = useState(false)

  return (
    <div>
      <label>
        <input type="checkbox" checked={debug} onChange={(e) => setDebug(e.target.checked)} />
        Enable Debug
      </label>
      <DebugScopeProvider debug={debug} name="FeatureTestbed">
        <MyFeature />
      </DebugScopeProvider>
    </div>
  )
}
```

**Key Insight**: All three patterns use same `debug` boolean prop.

### 7. Dependency Change Detection

**Pattern**: Track dependency changes with labeled diffs.

**Implementation**:

```tsx
import { useDebugScope } from "@/lib/debug/DebugScope"

function DataGrid({ query, filters, sortBy }: DataGridProps) {
  const scope = useDebugScope({
    debug: true,
    name: "DataGrid",
    deps: [query, filters, sortBy],
    depLabels: ["query", "filters", "sortBy"],
  })

  // ... component logic
}
```

**Output** (when `filters` changes):
```
[DataGrid] DEPS CHANGED {
  changes: [
    { filters: { from: { status: "active" }, to: { status: "all" } } }
  ]
}
```

**Unlabeled Deps** (falls back to indices):
```tsx
const scope = useDebugScope({
  debug: true,
  name: "MyComponent",
  deps: [a, b, c], // No depLabels
})
```

**Output**:
```
[MyComponent] DEPS CHANGED {
  changes: [
    { dep[0]: { from: 1, to: 2 } },
    { dep[2]: { from: "foo", to: "bar" } }
  ]
}
```

### 8. Watch Value Change Detection

**Pattern**: Track arbitrary object changes (like `useEffect` deps but for DebugScope).

**Implementation**:

```tsx
import { DebugScope } from "@/lib/debug/DebugScope"

function SearchResults({ results, status, stats }: SearchResultsProps) {
  return (
    <>
      <DebugScope
        debug={true}
        name="SearchResults"
        watch={{ results: results.length, status, stats }}
      />
      {/* Render results */}
    </>
  )
}
```

**Output** (when `status` and `stats.items` change):
```
[SearchResults] WATCH CHANGED {
  changes: {
    status: { from: "streaming", to: "complete" },
    stats: { from: { items: 10 }, to: { items: 100 } }
  }
}
```

**Key Difference from Deps**:
- `deps` → Array with positional tracking
- `watch` → Object with named keys

### 9. Log Levels (log, warn, error)

**Pattern**: Use appropriate log level for message severity.

**Implementation**:

```tsx
const scope = useDebugScope({ debug: true, name: "MyComponent" })

// Informational
scope.log("User action", { action: "click", target: "button" })

// Warning
scope.warn("Deprecated API used", { api: "oldMethod", replacement: "newMethod" })

// Error
scope.error("Failed to fetch data", { url, status: 404 })
```

**Effect.Console Mapping**:
- `scope.log()` → `Effect.runSync(Console.log(...))`
- `scope.warn()` → `Effect.runSync(Console.warn(...))`
- `scope.error()` → `Effect.runSync(Console.error(...))`

**Console Output Styling**:
- `log` → Default console style
- `warn` → Yellow/orange in browser console
- `error` → Red in browser console

### 10. No-Op When Disabled

**Pattern**: Zero runtime cost when `debug={false}`.

**Implementation** (from DebugScope.tsx):

```tsx
const log = (message: string, data?: Record<string, unknown>) => {
  if (!enabled) return // Early exit, no Effect execution
  Effect.runSync(Console.log(`${prefix} ${message}`, data))
}
```

**Key Insight**: All logging functions check `enabled` first, avoiding:
- Effect execution
- String formatting
- Object serialization
- Console API calls

**Performance**: Production builds with `debug={false}` have zero logging overhead.

## Examples

### Example 1: Basic Component Instrumentation

```tsx
import { DebugScope } from "@/lib/debug/DebugScope"

function Counter({ debug }: { debug?: boolean }) {
  const [count, setCount] = useState(0)

  return (
    <>
      <DebugScope debug={debug} name="Counter" watch={{ count }} />
      <div>
        <p>Count: {count}</p>
        <button onClick={() => setCount(count + 1)}>Increment</button>
      </div>
    </>
  )
}
```

**Output**:
```
[Counter] MOUNT { watch: { count: 0 } }
[Counter] WATCH CHANGED { changes: { count: { from: 0, to: 1 } } }
[Counter] WATCH CHANGED { changes: { count: { from: 1, to: 2 } } }
```

### Example 2: Custom Event Logging

```tsx
import { useDebugScope } from "@/lib/debug/DebugScope"

function SearchBar({ debug }: { debug?: boolean }) {
  const [query, setQuery] = useState("")
  const scope = useDebugScope({ debug, name: "SearchBar" })

  const handleSearch = () => {
    scope.log("Search initiated", { query, timestamp: Date.now() })
    // ... perform search
  }

  const handleClear = () => {
    scope.log("Search cleared")
    setQuery("")
  }

  return (
    <div>
      <input value={query} onChange={(e) => setQuery(e.target.value)} />
      <button onClick={handleSearch}>Search</button>
      <button onClick={handleClear}>Clear</button>
    </div>
  )
}
```

**Output**:
```
[SearchBar] MOUNT
[SearchBar] Search initiated { query: "effect-ts", timestamp: 1701234567890 }
[SearchBar] Search cleared
```

### Example 3: Hierarchical Scopes

```tsx
import { DebugScopeProvider, useDebugScopeContext } from "@/lib/debug/DebugScope"

function ParentComponent({ debug }: { debug?: boolean }) {
  return (
    <DebugScopeProvider debug={debug} name="Parent">
      <ChildA />
      <ChildB />
    </DebugScopeProvider>
  )
}

function ChildA() {
  const parent = useDebugScopeContext()
  const scope = parent.child("ChildA")

  const handleClick = () => {
    scope.log("Child A clicked")
  }

  return <button onClick={handleClick}>A</button>
}

function ChildB() {
  const parent = useDebugScopeContext()
  const scope = parent.child("ChildB")

  const handleClick = () => {
    scope.log("Child B clicked")
  }

  return <button onClick={handleClick}>B</button>
}
```

**Output**:
```
[Parent] PROVIDER MOUNT
[Parent.ChildA] Child A clicked
[Parent.ChildB] Child B clicked
[Parent] PROVIDER UNMOUNT { duration: "1234.56ms" }
```

### Example 4: Dependency Tracking

```tsx
import { useDebugScope } from "@/lib/debug/DebugScope"

function DataFetcher({ url, method, headers }: DataFetcherProps) {
  const scope = useDebugScope({
    debug: true,
    name: "DataFetcher",
    deps: [url, method, headers],
    depLabels: ["url", "method", "headers"],
  })

  useEffect(() => {
    scope.log("Fetching data", { url, method })
    // ... fetch logic
  }, [url, method, headers])

  return <div>Loading...</div>
}
```

**Output** (when `url` changes from `/api/v1` to `/api/v2`):
```
[DataFetcher] MOUNT
[DataFetcher] Fetching data { url: "/api/v1", method: "GET" }
[DataFetcher] DEPS CHANGED { changes: [{ url: { from: "/api/v1", to: "/api/v2" } }] }
[DataFetcher] Fetching data { url: "/api/v2", method: "GET" }
```

### Example 5: Conditional Activation via URL

```tsx
import { useSearchParams } from "@tanstack/react-router"
import { DebugScopeProvider } from "@/lib/debug/DebugScope"

export function FeatureTestbed() {
  const searchParams = useSearchParams()
  const debug = searchParams.debug === "true"

  return (
    <div>
      <p>Debug Mode: {debug ? "ON" : "OFF"}</p>
      <DebugScopeProvider debug={debug} name="FeatureTestbed">
        <MyFeature />
      </DebugScopeProvider>
    </div>
  )
}
```

**Usage**:
- `/testbed/feature` → Debug OFF (no logs)
- `/testbed/feature?debug=true` → Debug ON (logs enabled)

## Anti-Patterns

### Don't: Use console.log Directly

```tsx
// ✗ BAD - No structure, can't disable, no metadata
console.log("Component mounted")
console.log("Count changed:", count)

// ✓ GOOD - Structured, conditional, rich metadata
scope.log("Component mounted")
scope.log("Count changed", { count, previousCount })
```

### Don't: Forget to Pass debug Prop

```tsx
// ✗ BAD - Always enabled (production performance hit)
<DebugScopeProvider name="MyComponent">
  ...
</DebugScopeProvider>

// ✓ GOOD - Controlled activation
<DebugScopeProvider debug={debug} name="MyComponent">
  ...
</DebugScopeProvider>
```

### Don't: Create Scopes Inside Loops

```tsx
// ✗ BAD - Creates scope on every render
function MyComponent({ items, debug }) {
  return items.map((item) => {
    const scope = useDebugScope({ debug, name: "Item" }) // BAD!
    return <div>{item.name}</div>
  })
}

// ✓ GOOD - Single scope outside loop
function MyComponent({ items, debug }) {
  const scope = useDebugScope({ debug, name: "MyComponent" })

  return items.map((item) => <div key={item.id}>{item.name}</div>)
}
```

### Don't: Log Sensitive Data

```tsx
// ✗ BAD - Exposes credentials
scope.log("Login attempt", { username, password }) // BAD!

// ✓ GOOD - Sanitize sensitive fields
scope.log("Login attempt", { username, password: "[REDACTED]" })
```

### Don't: Use DebugScope for Production Metrics

```tsx
// ✗ BAD - Debug scope is for development only
<DebugScope debug={true} name="ProductionMetrics" watch={{ revenue, users }} />

// ✓ GOOD - Use analytics/observability service
useEffect(() => {
  analytics.track("metrics", { revenue, users })
}, [revenue, users])
```

### Don't: Ignore Dependency Labels

```tsx
// ✗ BAD - Unlabeled deps hard to debug
const scope = useDebugScope({
  debug: true,
  name: "MyComponent",
  deps: [a, b, c, d, e], // Which one changed?
})

// ✓ GOOD - Labeled deps for clarity
const scope = useDebugScope({
  debug: true,
  name: "MyComponent",
  deps: [query, filters, sortBy, page, limit],
  depLabels: ["query", "filters", "sortBy", "page", "limit"],
})
```

## Quick Reference

**Three Patterns**:
- `<DebugScopeProvider>` → Wrap subtree with shared context
- `<DebugScope />` → Render-nothing instrumentation
- `useDebugScope()` → Imperative logging hook

**Logging Methods**:
- `scope.log(message, data?)` → Info
- `scope.warn(message, data?)` → Warning
- `scope.error(message, data?)` → Error
- `scope.child(name)` → Create child scope

**Lifecycle Events**:
- `MOUNT` → Component mounted
- `UNMOUNT` → Component unmounted (with duration)
- `DEPS CHANGED` → Dependencies changed (with diff)
- `WATCH CHANGED` → Watch values changed (with diff)

**Conditional Activation**:
- Environment: `import.meta.env.VITE_DEBUG === "true"`
- URL param: `searchParams.debug === "true"`
- Testbed toggle: `useState(false)` + checkbox

**Performance**:
- `debug={false}` → Zero runtime cost
- `debug={true}` → Full instrumentation
- No production impact when disabled
