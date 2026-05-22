---
name: react-state-migration
description: Migration from useState to effect-atom. Pattern recognition for when useState is acceptable vs when atoms are required. Use for refactoring stateful components to service-scoped reactive state.
model_invoked: true
triggers:
  - "useState migration"
  - "effect-atom migration"
  - "state refactor"
  - "useState to atom"
  - "reactive state"
---

# React State Migration for TMNL

## Overview

TMNL enforces a strict separation: **useState for local UI state, effect-atom for shared/service-scoped state**. Migrating from useState to atoms eliminates prop drilling, enables reactive subscriptions, and integrates with Effect services.

**Critical Doctrine**: When React consumes Effect services via effect-atom, `Atom.make()` is the primary state mechanism—not `Effect.Ref`.

## Canonical Sources

### TMNL Implementations

- **DataManagerTestbed** — `/src/components/testbed/DataManagerTestbed.tsx` (BEFORE/AFTER example)
  - **BEFORE**: 4 useState hooks for results, status, stats, isIndexing
  - **AFTER**: All state via `useDataManager()` hook consuming atoms
  - Demonstrates progressive stream updates without setter soup

- **DataManager Service** — `/src/lib/data-manager/v1/DataManager.ts`
  - State lives in `Atom.make()` atoms, NOT `Effect.Ref`
  - Service methods mutate atoms directly via `Atom.set()`
  - React subscribes via `useAtomValue()`

- **SliderTestbed** — `/src/components/testbed/SliderTestbed.tsx`
  - useState acceptable for controlled slider value (local UI state)
  - Slider behavior injectable via runtime atoms

### Reference Documentation

- [CLAUDE.md: useState → effect-atom Migration Protocol](/home/getbygenius/getbyzenbook/projects/gbg/assets/code/repos/gbg/packages/tmnl/CLAUDE.md#usestate--effect-atom-migration-protocol)
- [Effect-Atom Patterns Skill](/.claude/skills/effect-patterns/SKILL.md)

## Pattern Recognition

### When useState Is ACCEPTABLE

Use useState for:

1. **Pure UI state** — Input bindings, hover states, toggle visibility
2. **Single-component scope** — State used only within one component
3. **No async dependencies** — Simple synchronous state
4. **Controlled component values** — Parent controls value, component notifies via onChange

```tsx
// ✅ ACCEPTABLE - Local toggle
function Accordion() {
  const [isOpen, setIsOpen] = useState(false)
  return <div onClick={() => setIsOpen(!isOpen)}>...</div>
}

// ✅ ACCEPTABLE - Input binding
function SearchBox({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState('')
  return (
    <input
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      onKeyDown={(e) => e.key === 'Enter' && onSearch(query)}
    />
  )
}

// ✅ ACCEPTABLE - Controlled slider value
function VolumeControl() {
  const [volume, setVolume] = useState(75)
  return <Slider value={volume} onChange={setVolume} />
}
```

### When Atoms Are REQUIRED

Use effect-atom when:

1. **Crosses component boundaries** — Shared state between sibling/distant components
2. **Derives from async operations** — API calls, streams, Effects
3. **Needs reactive subscriptions** — Multiple consumers of same state
4. **Benefits from service scoping** — Lifecycle tied to a service, not component mount
5. **Integrates with Effect services** — DataManager, SearchKernel, etc.

```tsx
// ❌ BANNED - useState for cross-component state
function SearchResults() {
  const [results, setResults] = useState<SearchResult[]>([])
  const [status, setStatus] = useState<'idle' | 'loading' | 'complete'>('idle')
  // Other components can't access this!
}

// ✅ CORRECT - Atoms for shared state
const resultsAtom = Atom.make<SearchResult[]>([])
const statusAtom = Atom.make<'idle' | 'loading' | 'complete'>('idle')

function SearchResults() {
  const results = useAtomValue(resultsAtom)
  const status = useAtomValue(statusAtom)
  // Other components can subscribe to same atoms
}
```

## Migration Patterns

### Pattern 1: Simple State Migration

**BEFORE (useState pollution)**:

```tsx
function SearchUI() {
  const [results, setResults] = useState<SearchResult[]>([])
  const [status, setStatus] = useState<'idle' | 'loading' | 'complete'>('idle')
  const [isIndexing, setIsIndexing] = useState(false)

  const handleSearch = async (query: string) => {
    setStatus('loading')
    setResults([])

    const newResults = await fetchResults(query)

    setResults(newResults)
    setStatus('complete')
  }

  return (
    <div>
      {status === 'loading' && <Spinner />}
      {results.map((r) => <Result key={r.id} result={r} />)}
    </div>
  )
}
```

**AFTER (effect-atom)**:

```tsx
// In atoms/index.ts
export const resultsAtom = Atom.make<SearchResult[]>([])
export const statusAtom = Atom.make<'idle' | 'loading' | 'complete'>('idle')
export const isIndexingAtom = Atom.make<boolean>(false)

// In hooks/useDataManager.ts
export function useDataManager() {
  const results = useAtomValue(resultsAtom)
  const status = useAtomValue(statusAtom)
  const isIndexing = useAtomValue(isIndexingAtom)

  const search = useCallback(async (query: string) => {
    Atom.set(statusAtom, 'loading')
    Atom.set(resultsAtom, [])

    const newResults = await fetchResults(query)

    Atom.set(resultsAtom, newResults)
    Atom.set(statusAtom, 'complete')
  }, [])

  return { results, status, isIndexing, search }
}

// In component
function SearchUI() {
  const { results, status, search } = useDataManager()

  return (
    <div>
      {status === 'loading' && <Spinner />}
      {results.map((r) => <Result key={r.id} result={r} />)}
    </div>
  )
}
```

**Canonical source**: `src/components/testbed/DataManagerTestbed.tsx:463-638`

### Pattern 2: Setter Soup → Service Methods

**BEFORE (setter soup in callbacks)**:

```tsx
function StreamingSearch() {
  const [results, setResults] = useState<SearchResult[]>([])
  const [status, setStatus] = useState<StreamStatus>('idle')
  const [stats, setStats] = useState<StreamStats>({ chunks: 0, items: 0, ms: 0 })

  const handleSearch = async (query: string) => {
    setStatus('streaming')
    setResults([])
    setStats({ chunks: 0, items: 0, ms: 0 })

    for await (const chunk of searchStream(query)) {
      setResults((prev) => [...prev, ...chunk.results])
      setStats((prev) => ({
        chunks: prev.chunks + 1,
        items: prev.items + chunk.results.length,
        ms: Date.now() - startTime,
      }))
    }

    setStatus('complete')
  }

  // 20 lines of setter calls scattered across component
}
```

**AFTER (service-scoped atoms)**:

```tsx
// In DataManager.ts (Effect service)
class DataManager extends Effect.Service<DataManager>()("tmnl/DataManager", {
  effect: Effect.gen(function* () {
    const search = (query: SearchQuery) =>
      Effect.gen(function* () {
        // Service mutates atoms directly
        Atom.set(statusAtom, 'streaming')
        Atom.set(resultsAtom, [])
        Atom.set(statsAtom, { chunks: 0, items: 0, ms: 0 })

        for await (const chunk of searchStream(query)) {
          Atom.set(resultsAtom, (prev) => [...prev, ...chunk.results])
          Atom.set(statsAtom, (prev) => ({
            chunks: prev.chunks + 1,
            items: prev.items + chunk.results.length,
            ms: Date.now() - startTime,
          }))
        }

        Atom.set(statusAtom, 'complete')
      }).pipe(Effect.withSpan('DataManager.search'))

    return { search } as const
  }),
}) {}

// In component
function StreamingSearch() {
  const { results, status, stats, search } = useDataManager()

  const handleSearch = async (query: string) => {
    await search({ query, limit: 100 })
    // Atoms update automatically via service
  }

  return <div>...</div>
}
```

**Canonical source**: `src/lib/data-manager/v1/DataManager.ts:73-200`

### Pattern 3: Derived State Migration

**BEFORE (useState + useEffect for derived values)**:

```tsx
function SearchMetrics() {
  const [results, setResults] = useState<SearchResult[]>([])
  const [resultCount, setResultCount] = useState(0)
  const [hasResults, setHasResults] = useState(false)

  // Derived state in useEffect
  useEffect(() => {
    setResultCount(results.length)
    setHasResults(results.length > 0)
  }, [results])

  // Now have 3 state hooks for 1 source of truth!
}
```

**AFTER (derived atoms)**:

```tsx
// In atoms/index.ts
export const resultsAtom = Atom.make<SearchResult[]>([])

export const resultCountAtom = Atom.make((get) => {
  const results = get(resultsAtom)
  return results.length
})

export const hasResultsAtom = Atom.make((get) => {
  const count = get(resultCountAtom)
  return count > 0
})

// In component
function SearchMetrics() {
  const results = useAtomValue(resultsAtom)
  const resultCount = useAtomValue(resultCountAtom)
  const hasResults = useAtomValue(hasResultsAtom)

  // No useEffect needed - atoms auto-derive!
}
```

**Canonical source**: `src/lib/data-manager/v1/atoms/index.ts:82-104`

### Pattern 4: Progressive Stream Updates

**BEFORE (flicker from array recreation)**:

```tsx
function ProgressiveResults() {
  const [results, setResults] = useState<SearchResult[]>([])

  useEffect(() => {
    const stream = searchStream(query)

    for await (const chunk of stream) {
      // Creates new array on every chunk - causes grid flicker!
      setResults((prev) => [...prev, ...chunk.results])
    }
  }, [query])

  return <AgGridReact rowData={results} />
}
```

**AFTER (atom updates with transaction batching)**:

```tsx
// In DataManager service
const search = (query: SearchQuery) =>
  Effect.gen(function* () {
    const stream = yield* searchKernel.queryStream(query)

    for await (const chunk of stream) {
      // Atom update batches efficiently
      Atom.set(resultsAtom, (prev) => [...prev, ...chunk.results])
    }
  })

// In component
function ProgressiveResults() {
  const { results, search } = useDataManager()

  useEffect(() => {
    search({ query, limit: 100 })
  }, [query, search])

  return <AgGridReact rowData={results} />
  // No flicker - AG-Grid receives stable updates
}
```

**Canonical source**: `src/components/testbed/DataManagerTestbed.tsx:536-638`

## Decision Tree

```
Need state in React component?
│
├─ State used only in this component?
│  │
│  ├─ Pure UI state (toggle, hover, input)?
│  │  └─ Use: useState
│  │
│  └─ Derives from async operation?
│     └─ Use: effect-atom
│
├─ State shared across components?
│  └─ Use: effect-atom
│
├─ State integrates with Effect service?
│  └─ Use: effect-atom (Atom.make, NOT Effect.Ref)
│
└─ Derived from other state?
   └─ Use: Derived atom (Atom.make with getter)
```

## Migration Checklist

When migrating from useState to atoms:

- [ ] **Identify shared state** — Find useState that crosses component boundaries
- [ ] **Create atoms** — Define atoms in `atoms/index.ts` with `Atom.make()`
- [ ] **Update service** — Service methods use `Atom.set()`, not `Effect.Ref`
- [ ] **Create hook** — Wrap atoms in custom hook (e.g., `useDataManager()`)
- [ ] **Migrate components** — Replace useState with `useAtomValue()` subscriptions
- [ ] **Remove setters** — Delete setState calls, let service handle mutations
- [ ] **Add derived atoms** — Replace useEffect derivations with derived atoms
- [ ] **Test reactivity** — Verify subscriptions update correctly

## Anti-Patterns (BANNED)

### Effect.Ref for React State

```tsx
// BANNED - Effect.Ref creates bridge complexity
class DataManager extends Effect.Service<DataManager>()("tmnl/DataManager", {
  effect: Effect.gen(function* () {
    const stateRef = yield* Ref.make<State>(initial) // ← WRONG!

    // Now need polling, SubscriptionRef, streams-to-consume-streams...
  }),
}) {}

// CORRECT - Atom.make as primary state
const resultsAtom = Atom.make<SearchResult[]>([])

class DataManager extends Effect.Service<DataManager>()("tmnl/DataManager", {
  effect: Effect.gen(function* () {
    const search = () => Effect.gen(function* () {
      Atom.set(resultsAtom, newResults) // ← Direct mutation
    })
    return { search } as const
  }),
}) {}
```

### useState for Cross-Component State

```tsx
// BANNED - Prop drilling for shared state
function Parent() {
  const [results, setResults] = useState([])
  return <Child results={results} setResults={setResults} />
}

function Child({ results, setResults }) {
  return <GrandChild results={results} setResults={setResults} />
}

// CORRECT - Atoms for shared state
const resultsAtom = Atom.make([])

function Parent() {
  return <Child />
}

function Child() {
  const results = useAtomValue(resultsAtom)
  // No props needed
}
```

### Derived useState + useEffect

```tsx
// BANNED - Manual derived state
const [results, setResults] = useState([])
const [count, setCount] = useState(0)

useEffect(() => {
  setCount(results.length) // ← Fragile, extra render
}, [results])

// CORRECT - Derived atom
const resultsAtom = Atom.make([])
const countAtom = Atom.make((get) => get(resultsAtom).length)
```

### Mixing useState and Atoms

```tsx
// BANNED - State split across useState and atoms
function Component() {
  const [localResults, setLocalResults] = useState([])
  const atomResults = useAtomValue(resultsAtom)

  // Which is the source of truth?
}

// CORRECT - Pick one pattern
function Component() {
  const results = useAtomValue(resultsAtom)
  // Single source of truth
}
```

## Examples

### Example 1: DataManagerTestbed Migration

Full migration from 4 useState hooks to service-scoped atoms.

**BEFORE**:
```tsx
const [results, setResults] = useState<SearchResult[]>([])
const [status, setStatus] = useState<StreamStatus>('idle')
const [stats, setStats] = useState<StreamStats>({ chunks: 0, items: 0, ms: 0 })
const [isIndexing, setIsIndexing] = useState(false)

const handleSearch = async () => {
  setStatus('streaming')
  setResults([])
  // ... 30 more lines of setter soup
}
```

**AFTER**:
```tsx
const {
  results,
  status,
  stats,
  isIndexing,
  search,
} = useDataManager<MovieItem>()

const handleSearch = async () => {
  await search({ query, limit: 100 })
  // Atoms update automatically
}
```

**Canonical source**: `src/components/testbed/DataManagerTestbed.tsx:54-638`

### Example 2: Slider Acceptable useState

Local UI state for controlled component.

```tsx
function VolumeControl() {
  const [volume, setVolume] = useState(75)

  return (
    <Slider
      value={volume}
      onChange={setVolume}
      behavior={LinearBehavior.shape}
      config={{ min: 0, max: 100 }}
    />
  )
}
```

**Canonical source**: `src/components/testbed/SliderTestbed.tsx`

## Related Patterns

- **effect-patterns** — Atom-as-State doctrine (NO Effect.Ref)
- **react-hook-composition** — Hooks wrap atoms for ergonomic API
- **react-performance-patterns** — Atoms enable fine-grained subscriptions

## Filing New Patterns

When you discover a new migration pattern:

1. Document BEFORE/AFTER in testbed
2. Update this skill with canonical source references
3. Add to `.edin/EFFECT_PATTERNS.md` registry
4. Create migration guide in project docs
