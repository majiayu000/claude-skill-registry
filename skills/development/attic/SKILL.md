---
name: coding-standards
description: Universal coding standards and best practices for TypeScript, JavaScript, React, and Node.js. Use when: writing code, reviewing code quality, establishing conventions. Focuses on modern patterns, explicit conventions, and rationale for best practices.
---

# Coding Standards & Best Practices

Modern coding standards applicable across TypeScript, JavaScript, React, and Node.js projects.

---

## Quick Navigation

| If you need... | MANDATORY READ WHEN... | File |
|---------------|------------------------|------|
| Type patterns | WRITING TYPES | `references/type-patterns.md` |
| React patterns | WRITING COMPONENTS | `references/react-patterns.md` |
| API patterns | DESIGNING APIS | `references/api-patterns.md` |
| Testing patterns | WRITING TESTS | `references/testing-patterns.md` |

---

## Core Principles

### 1. Readability First

**WHY**: Code is read 10x more than written. Optimize for the reader.

**Practices**:
- Self-documenting code preferred over comments
- Descriptive variable and function names
- Consistent formatting (use linter/formatter)
- Clear intent over clever tricks

**Recognition**: "Would a new team member understand this without explanation?"

### 2. Immutability Pattern (CRITICAL)

**WHY**: Prevents stale closures, makes state predictable, enables React optimizations.

**✅ ALWAYS use spread operator**:
```typescript
const updatedUser = { ...user, name: 'New Name' }
const updatedArray = [...items, newItem]
```

**❌ NEVER mutate directly**:
```typescript
user.name = 'New Name'  // BAD - causes bugs
items.push(newItem)     // BAD - breaks React optimizations
```

**Best practice**: Use Lodash (cloneDeep), Immer, or structuredClone for deep objects.

### 3. Functional Updates for State

**WHY**: Prevents stale closure bugs in async scenarios.

**✅ GOOD** (functional update):
```typescript
setCount(prev => prev + 1)
setData(prev => ({ ...prev, field: value }))
```

**❌ BAD** (direct reference - can be stale):
```typescript
setCount(count + 1)     // May use stale value
setData({ ...data, field: value })  // Can miss updates
```

### 4. Comprehensive Error Handling

**WHY**: Unhandled errors crash processes, cause bad UX, make debugging impossible.

**✅ GOOD pattern**:
```typescript
async function fetchData(url: string) {
  try {
    const response = await fetch(url)
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
    return await response.json()
  } catch (error) {
    console.error('Fetch failed:', error)
    throw new Error('Failed to fetch data')
  }
}
```

**❌ BAD** (no error handling):
```typescript
async function fetchData(url) {
  const response = await fetch(url)
  return response.json()  // Crashes on network failure
}
```

### 5. Parallel Async Execution

**WHY**: Sequential awaits waste time. Parallel execution is faster.

**✅ GOOD** (parallel when possible):
```typescript
const [users, markets, stats] = await Promise.all([
  fetchUsers(),
  fetchMarkets(),
  fetchStats()
])
```

**❌ BAD** (sequential when unnecessary):
```typescript
const users = await fetchUsers()    // Waits 100ms
const markets = await fetchMarkets() // Waits 100ms (total: 200ms)
const stats = await fetchStats()     // Waits 100ms (total: 300ms)
```

**Recognition**: "Can these operations run in parallel?" → Use Promise.all

### 6. Type Safety Over Convenience

**WHY**: Types catch bugs at compile-time, serve as documentation, enable refactoring.

**✅ GOOD** (proper types):
```typescript
interface Market {
  id: string
  name: string
  status: 'active' | 'resolved' | 'closed'
}

function getMarket(id: string): Promise<Market> { }
```

**❌ BAD** (using `any`):
```typescript
function getMarket(id: any): Promise<any> { }
```

**Recognition**: "Could I use a more specific type?" → Always prefer specificity

---

## Naming Conventions

### Variables and Functions

**✅ GOOD** (descriptive, camelCase):
```typescript
const marketSearchQuery = 'election'
const isUserAuthenticated = true
const totalRevenue = 1000

async function fetchMarketData(marketId: string) { }
function calculateSimilarity(a: number[], b: number[]) { }
```

**❌ BAD** (unclear, abbreviated):
```typescript
const q = 'election'
const flag = true
const x = 1000

async function market(id: string) { }
function similarity(a, b) { }
```

### Boolean Variables

**Prefix with `is`, `has`, `should`, `can`**:
```typescript
const isLoading = true
const hasPermission = false
const shouldRetry = true
const canEdit = true
```

### Constants

**Use UPPER_SNAKE_CASE** for true constants (never reassigned):
```typescript
const MAX_RETRIES = 3
const DEFAULT_TIMEOUT_MS = 5000
const API_BASE_URL = 'https://api.example.com'
```

---

## Code Organization

### File Structure Preference

```
src/
├── components/         # React components
│   ├── ui/            # Generic, reusable
│   └── features/      # Feature-specific
├── hooks/             # Custom React hooks
├── lib/               # Utilities and helpers
│   ├── api/          # API clients
│   ├── utils/        # Helper functions
│   └── constants/    # Constants
├── types/             # TypeScript types
└── styles/            # Global styles
```

### File Naming

| Type | Pattern | Example |
|------|---------|---------|
| Components | PascalCase | `Button.tsx`, `MarketCard.tsx` |
| Hooks | camelCase with `use` prefix | `useAuth.ts`, `useDebounce.ts` |
| Utilities | camelCase | `formatDate.ts`, `calculateTotal.ts` |
| Types | camelCase with `.types` suffix | `market.types.ts` |
| Constants | camelCase with `constants` suffix | `api.constants.ts` |

---

## Common Anti-Patterns

### Anti-Pattern 1: Magic Numbers

**❌ BAD**:
```typescript
if (retryCount > 3) { }
setTimeout(callback, 500)
```

**✅ GOOD**:
```typescript
const MAX_RETRIES = 3
const DEBOUNCE_DELAY_MS = 500

if (retryCount > MAX_RETRIES) { }
setTimeout(callback, DEBOUNCE_DELAY_MS)
```

### Anti-Pattern 2: Deep Nesting

**❌ BAD** (5+ levels):
```typescript
if (user) {
  if (user.isAdmin) {
    if (market) {
      if (market.isActive) {
        if (hasPermission) {
          // Do something
        }
      }
    }
  }
}
```

**✅ GOOD** (early returns):
```typescript
if (!user) return
if (!user.isAdmin) return
if (!market) return
if (!market.isActive) return
if (!hasPermission) return

// Do something
```

### Anti-Pattern 3: Console.log in Production

**❌ BAD**:
```typescript
console.log('User logged in', user)
console.error('Error occurred', error)
```

**✅ GOOD**:
```typescript
// Use proper logging library
logger.info('User logged in', { userId: user.id })
logger.error('Error occurred', { error, context })
```

### Anti-Pattern 4: Ignoring Type Errors

**❌ BAD**:
```typescript
// @ts-ignore
const data = JSON.parse uncertain
```

**✅ GOOD**:
```typescript
const data = JSON.parse uncertain as unknown as ExpectedType
// Or use zod/joi for validation
```

---

## Performance Best Practices

### Memoization

**Use for**:
- Expensive computations (`useMemo`)
- Functions passed to children (`useCallback`)
- Pure components (`React.memo`)

```typescript
const sortedMarkets = useMemo(() => {
  return markets.sort((a, b) => b.volume - a.volume)
}, [markets])

const handleSearch = useCallback((query: string) => {
  setSearchQuery(query)
}, [])
```

### Lazy Loading

**Use for**:
- Heavy components (`lazy`, `Suspense`)
- Route-based code splitting
- Non-critical features

```typescript
const HeavyChart = lazy(() => import('./HeavyChart'))

<Suspense fallback={<ChartSkeleton />}>
  <HeavyChart data={data} />
</Suspense>
```

---

## Verification Checklist

Before considering code complete:

- [ ] Immutability pattern used (spread operators)
- [ ] Functional state updates (prev => pattern)
- [ ] Comprehensive error handling
- [ ] Type-safe (no `any` without justification)
- [ ] Parallel async execution where possible
- [ ] Descriptive naming (self-documenting)
- [ ] No console.log in production code
- [ ] No magic numbers (use constants)
- [ ] Early returns over deep nesting
- [ ] Performance optimizations applied

---

## Integration with Other Skills

This skill integrates with:
- `frontend-patterns` - React/Next.js specific patterns
- `backend-patterns` - API and database patterns
- `tdd-workflow` - Testing standards
- `verify` - Quality gate verification

**Recognition**: "Am I following WHY-based best practices?" → If you're doing something "because that's how it's done," you're missing the rationale.
