---
name: coding-guidelines
description: 'Comprehensive React component coding guidelines, refactoring principles,
  and architectural patterns. **CRITICAL**: Focuses on patterns AI commonly fails
  to implement correctly, especially testability,'
---

---
name: coding-guidelines
description: Comprehensive React component coding guidelines, refactoring principles, and architectural patterns. **CRITICAL**: Focuses on patterns AI commonly fails to implement correctly, especially testability, props control, and component responsibility separation. Reference this skill when implementing or refactoring React components during Phase 2.
---

# Coding Guidelines - What AI Gets Wrong

This skill focuses on patterns AI commonly fails to implement correctly. Trust AI for syntax and structure, but scrutinize these critical areas where AI consistently makes mistakes.

## ⚠️ Critical: AI's Common Failures

### 1. Lack of Testability (Most Critical)

**Pattern AI ALWAYS gets wrong**: Creating components that control UI branches with internal state

```typescript
// ❌ Typical AI pattern (untestable)
function UserProfile({ userId }: { userId: string }) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<Error | null>(null)
  const [user, setUser] = useState<User | null>(null)

  // Problem 1: To test loading state, you must actually trigger fetch to set loading=true
  // Problem 2: To test error state, you must make fetch fail
  // Problem 3: Cannot test each state independently

  if (loading) return <Spinner />
  if (error) return <ErrorMessage error={error} />
  if (!user) return <div>Not found</div>

  return <div>{user.name}</div>
}
```

**Why is this untestable?**:
- Depends on **internal state** (`loading`, `error`, `user`)
- To test each state, you must **actually trigger** those states
- Mocks and stubs become complex, tests become brittle

**Correct pattern**: Convert internal state to props, separate components by state

```typescript
// ✅ Testable pattern
type UserProfileProps = {
  user: User | null
}

function UserProfile({ user }: UserProfileProps) {
  if (!user) return <div>Not found</div>
  return <div>{user.name}</div>
}

// Easy to test
test('displays Not found when user is null', () => {
  render(<UserProfile user={null} />)
  expect(screen.getByText('Not found')).toBeInTheDocument()
})

test('displays user name', () => {
  const user = { name: 'Taro', id: '1' }
  render(<UserProfile user={user} />)
  expect(screen.getByText('Taro')).toBeInTheDocument()
})
```

**Same applies to functions**:
```typescript
// ❌ AI writes: depends on internal state
function validateUser() {
  const user = getCurrentUser() // depends on global state
  if (!user.email) return false
  return true
}

// ✅ Correct: controllable via arguments
function validateUser(user: User): boolean {
  if (!user.email) return false
  return true
}
```

---

### 2. Insufficient Props Control

**Pattern AI ALWAYS gets wrong**: Components hold internal state that cannot be controlled externally

```typescript
// ❌ AI writes: trapped in internal state
function UserCard({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null)

  useEffect(() => {
    fetchUser(userId).then(setUser)
  }, [userId])

  // Problem: Cannot control loading/error states from parent
  // Problem: Cannot use Suspense
  // Problem: Actual fetch runs during tests

  return user ? <div>{user.name}</div> : <div>Loading...</div>
}

// Cannot control loading state from parent
<UserCard userId="123" />  // Cannot change Loading display
```

**Correct pattern**: Make everything controllable via props

```typescript
// ✅ Correct: everything controlled via props
type UserCardProps = {
  user: User | null
  isLoading?: boolean
  error?: Error | null
}

function UserCard({ user, isLoading, error }: UserCardProps) {
  if (isLoading) return <Spinner />
  if (error) return <ErrorMessage error={error} />
  if (!user) return <div>Not found</div>

  return <div>{user.name}</div>
}

// Fully controllable from parent
function UserPage() {
  const { user, isLoading, error } = useUser('123')

  return <UserCard user={user} isLoading={isLoading} error={error} />
}

// Easy to test
test('loading state', () => {
  render(<UserCard user={null} isLoading={true} />)
  expect(screen.getByTestId('spinner')).toBeInTheDocument()
})
```

---

### 3. Insufficient Conditional Branch Extraction

**Pattern AI ALWAYS gets wrong**: Cramming multiple conditional branches into one component

```typescript
// ❌ AI writes: scattered conditional branches
function Dashboard() {
  const { user, subscription, notifications } = useData()

  return (
    <div>
      {/* Problem 1: user conditional branch */}
      {user ? (
        <div>
          <h1>{user.name}</h1>
          {/* Problem 2: subscription conditional branch */}
          {subscription?.isPremium ? (
            <PremiumBadge />
          ) : (
            <FreeBadge />
          )}
        </div>
      ) : (
        <LoginPrompt />
      )}

      {/* Problem 3: notifications conditional branch */}
      {notifications.length > 0 ? (
        <NotificationList items={notifications} />
      ) : (
        <EmptyState />
      )}
    </div>
  )
}

// Problems with this design:
// - Cannot test each conditional branch independently
// - To test PremiumBadge display, need user + subscription.isPremium=true
// - Combination of multiple states = test cases explode
```

**Correct pattern**: Separate components for each conditional branch

```typescript
// ✅ Correct: extract conditional branches into separate components
type UserSectionProps = {
  user: User | null
  subscription: Subscription | null
}

function UserSection({ user, subscription }: UserSectionProps) {
  if (!user) return <LoginPrompt />

  return (
    <div>
      <h1>{user.name}</h1>
      <SubscriptionBadge subscription={subscription} />
    </div>
  )
}

type SubscriptionBadgeProps = {
  subscription: Subscription | null
}

function SubscriptionBadge({ subscription }: SubscriptionBadgeProps) {
  if (subscription?.isPremium) return <PremiumBadge />
  return <FreeBadge />
}

type NotificationSectionProps = {
  notifications: Notification[]
}

function NotificationSection({ notifications }: NotificationSectionProps) {
  if (notifications.length === 0) return <EmptyState />
  return <NotificationList items={notifications} />
}

// Easy to test
test('displays premium badge', () => {
  const subscription = { isPremium: true }
  render(<SubscriptionBadge subscription={subscription} />)
  expect(screen.getByTestId('premium-badge')).toBeInTheDocument()
})

test('displays free badge', () => {
  render(<SubscriptionBadge subscription={null} />)
  expect(screen.getByTestId('free-badge')).toBeInTheDocument()
})
```

---

### 4. Mixing Data Fetching with UI Display

**Pattern AI ALWAYS gets wrong**: Data fetching with useEffect

```typescript
// ❌ AI writes: data fetching with useEffect
'use client'

function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then(res => res.json())
      .then(data => {
        setUser(data)
        setLoading(false)
      })
  }, [userId])

  // Problem 1: Cannot use Suspense
  // Problem 2: Cannot SSR (becomes Client Component)
  // Problem 3: Cannot control loading state from parent
  // Problem 4: Must mock fetch during tests

  if (loading) return <Spinner />
  return <div>{user?.name}</div>
}
```

**Correct pattern**: Data fetching in Server Component, display in Presentational Component

```typescript
// ✅ Correct: Data fetching in Server Component
async function UserProfileServer({ userId }: { userId: string }) {
  const user = await fetchUser(userId)  // Direct async/await
  return <UserProfile user={user} />
}

// Presentational Component
type UserProfileProps = {
  user: User
}

function UserProfile({ user }: UserProfileProps) {
  return <div>{user.name}</div>
}

// Usage: Loading management with Suspense
<Suspense fallback={<Spinner />}>
  <UserProfileServer userId="123" />
</Suspense>

// Easy to test (data fetching and display separated)
test('displays user name', () => {
  const user = { name: 'Taro', id: '1' }
  render(<UserProfile user={user} />)
  expect(screen.getByText('Taro')).toBeInTheDocument()
})
```

---

## Refactoring Principles

Eight core principles guide component refactoring:

1. **Logic Extraction** - Separate non-UI logic into utility files
2. **Presenter Pattern** - Consolidate conditional text in presenter.ts
3. **Conditional UI Extraction** - Extract conditional branches to components (CRITICAL)
4. **Naming and Structure** - Use kebab-case directories, PascalCase files
5. **Props Control** - All rendering controllable via props (CRITICAL)
6. **Avoid useEffect for Data** - Use Server Components with async/await
7. **Avoid Over-Abstraction** - Don't create unnecessary wrappers
8. **Promise Handling** - Prefer .then().catch() over try-catch

**CRITICAL** marked principles are areas where AI ALWAYS makes mistakes.

---

## Component Directory Structure

### Key Rules

**Directory Naming**:
- Root: `kebab-case` matching component name
- Entry point: `PascalCase` file directly inside root
- Example: `read-only-editor/ReadOnlyEditor.tsx`

**Parent-Child Hierarchy**:
- Child components in subdirectories under parent
- Clear ownership: `parent-component/child-component/grandchild-component/`
- Import paths reflect relationships

**Export Strategy**:
- Root entry point is public API
- Re-export other files for external use
- Direct imports of subdirectory files limited to internal use

---

## Quality Requirements

### Non-Negotiable Standards

- **Preserve external contracts** - Don't change public APIs or behavior
- **Run checks after all work** - `bun run check:fix` and `bun run typecheck`
- **No new `any`** - Solve issues fundamentally, document when unavoidable
- **No new ignores** - No `@ts-ignore` or `// biome-ignore` without reason
- **Resolve warnings** - Fix ESLint/Biome warnings, remove unnecessary ignores
- **Improve type safety** - Produce self-explanatory code (comments only for exceptional cases)

---

## AI Weakness Checklist

Before considering implementation complete, verify AI didn't fall into these traps:

### Testability ⚠️ (Most Critical)
- [ ] All UI states controlled via props (not internal state)
- [ ] Each conditional branch extracted to separate component
- [ ] No internal state that can't be controlled from parent
- [ ] Functions take arguments (not relying on closures/globals)
- [ ] Easy to test each state independently

### Props Control ⚠️
- [ ] Loading states controllable from parent
- [ ] Error states controllable from parent
- [ ] All display variations controllable via props
- [ ] No useEffect for data fetching in presentational components

### Component Responsibility
- [ ] Data fetching in Server Components (not useEffect)
- [ ] Display logic in presenter.ts (not embedded in JSX)
- [ ] Validation logic in utility files (not in components)
- [ ] One responsibility per component

### Over-Abstraction
- [ ] No wrapper components without added value
- [ ] No single-use abstractions
- [ ] Direct rendering when no logic needed

### Type Safety
- [ ] No `any` types
- [ ] Explicit type annotations on all props
- [ ] Type guards for runtime checks

---

## Code Examples

### Quick Reference

**Testable Component Pattern**:
```typescript
// ✅ Props control all states
type ComponentProps = {
  data: Data | null
  isLoading?: boolean
  error?: Error | null
}

function Component({ data, isLoading, error }: ComponentProps) {
  if (isLoading) return <Spinner />
  if (error) return <ErrorMessage error={error} />
  if (!data) return <EmptyState />

  return <Content data={data} />
}
```

**Logic Extraction**:
```typescript
// Extract to userValidation.ts
export const validateEmail = (email: string): boolean => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}
```

**Presenter Pattern**:
```typescript
// presenter.ts
export const getUserStatusText = (status: string): string => {
  switch (status) {
    case "active": return "Active"
    case "inactive": return "Inactive"
    default: return "Unknown"
  }
}
```

---

## Integration with Development Workflow

This skill is primarily referenced during **Phase 2 (Implementation)** when:
- Implementing new React components
- Refactoring existing components
- Extracting logic from components
- Organizing component directory structure
- Ensuring code quality standards

After implementation, code undergoes review in Phase 2 (Code Review) using Codex MCP.

---

## Common Patterns

### Server Component Pattern
```typescript
// Server Component (async)
export async function UserProfileServer({ userId }: { userId: string }) {
  const user = await fetchUser(userId)  // Direct async/await
  return <UserProfile user={user} />
}

// Usage with Suspense
<Suspense fallback={<Spinner />}>
  <UserProfileServer userId={userId} />
</Suspense>
```

### Presenter Pattern
```typescript
// presenter.ts - Pure functions for display logic
export const getUserStatusText = (status: string): string => { /* ... */ }
export const getUserStatusColor = (status: string): string => { /* ... */ }

// Component uses presenter
<Badge color={getUserStatusColor(status)}>
  {getUserStatusText(status)}
</Badge>
```

### Conditional UI Extraction
```typescript
// Extract conditional branches to separate components
// Instead of: {isLoading ? <Spinner /> : <Content />}
// Create: <LoadingState /> and <ContentState /> components with props
```

---

## Summary: What to Watch For

AI will confidently write code that:
1. **Looks clean** but is **impossible to test** (internal state dependencies)
2. **Works** but **can't be controlled** from parent (no props control)
3. **Compiles** but **violates separation of concerns** (data fetching + UI mixed)
4. **Is abstract** but **has no benefit** (unnecessary wrappers)

**Trust AI for**:
- Syntax and TypeScript basics
- Import/export statements
- Basic component structure

**Scrutinize AI for**:
- Testability (internal state vs props)
- Component responsibility (one thing per component)
- Props control (can parent control all states?)
- Conditional branch extraction (separate components?)

When in doubt, ask: **"Can I easily test this component's different states?"**

If the answer is no, refactor until you can pass props to control each state independently.
