---
name: coding-standards
description: Universal coding standards, best practices, and patterns for TypeScript, JavaScript, React, and Node.js development.
---

# Coding Standards & Best Practices

Universal coding standards applicable across all projects.

## Code Quality Principles

- **Readability First**: Clear names, self-documenting code
- **KISS**: Simplest solution, avoid over-engineering
- **DRY**: Extract common logic, reusable components
- **YAGNI**: Build only what's needed

## TypeScript/JavaScript Standards

### Immutability Pattern (CRITICAL)

```typescript
// ✅ Spread operator
const updated = { ...user, name: 'New' }
const items = [...list, newItem]

// ❌ Direct mutation
user.name = 'New'
items.push(newItem)
```

### Error Handling

```typescript
async function fetchData(url: string) {
  try {
    const response = await fetch(url)
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    return await response.json()
  } catch (error) {
    throw new Error('Failed to fetch')
  }
}
```

### Async/Await & Type Safety

```typescript
// ✅ Parallel execution
const [users, markets] = await Promise.all([fetchUsers(), fetchMarkets()])

// ✅ Proper types
interface Market { id: string; status: 'active' | 'resolved' }

// ❌ Using 'any' or sequential when unnecessary
```

## React Best Practices

### Component Structure

```typescript
interface ButtonProps {
  children: React.ReactNode
  onClick: () => void
  disabled?: boolean
}

export function Button({ children, onClick, disabled = false }: ButtonProps) {
  return <button onClick={onClick} disabled={disabled}>{children}</button>
}
```

### Custom Hooks & State

```typescript
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value)
  useEffect(() => {
    const handler = setTimeout(() => setDebouncedValue(value), delay)
    return () => clearTimeout(handler)
  }, [value, delay])
  return debouncedValue
}

// ✅ Functional update | ❌ Direct reference (stale)
setCount(prev => prev + 1) | setCount(count + 1)
```

## API Design Standards

### REST API Conventions

```
GET/POST/PUT/PATCH/DELETE /api/markets/:id
```

### Response Format & Validation

```typescript
interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
}

import { z } from 'zod'
const Schema = z.object({ name: z.string().min(1) })
const validated = Schema.parse(body)
```

## File Organization

```
src/
├── app/          # Next.js App Router
├── components/   # React components (PascalCase.tsx)
├── hooks/        # Custom hooks (use*.ts)
├── lib/          # Utilities (camelCase.ts)
├── types/        # TypeScript types (*.types.ts)
└── styles/       # Global styles
```

## Code Smell Detection

- **Long Functions**: >50 lines → split
- **Deep Nesting**: >3 levels → early returns
- **Magic Numbers**: unexplained → named constants

## Testing Standards (AAA)

```typescript
test('returns empty array when no match', () => {
  const result = search(query)
  expect(result).toEqual([])
})
```

## Further Reading

**Internal**: @.claude/skills/coding-standards/REFERENCE.md - Advanced patterns, hooks library, API design, testing strategies | @.claude/skills/vibe-coding/SKILL.md - Code quality limits

**External**: [TypeScript Handbook](https://www.typescriptlang.org/docs/) | [React Docs](https://react.dev/)
