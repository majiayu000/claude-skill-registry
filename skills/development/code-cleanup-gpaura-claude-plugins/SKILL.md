---
name: code-cleanup
description: "Refactor and clean up code following best practices for readability and maintainability"
---

# Code Cleanup

Clean up and refactor the following code to improve readability, maintainability, and follow best practices.

## Code to Clean

$ARGUMENTS

## Cleanup Checklist for Solo Developers

### 1. **Code Smells to Fix**

**Naming**
- Descriptive variable/function names
- Consistent naming conventions (camelCase, PascalCase)
- Avoid abbreviations unless obvious
- Boolean names start with is/has/can

**Functions**
- Single responsibility per function
- Keep functions small (<50 lines)
- Reduce parameters (max 3-4)
- Extract complex logic
- Avoid side effects where possible

**DRY (Don't Repeat Yourself)**
- Extract repeated code to utilities
- Create reusable components
- Use TypeScript generics for type reuse
- Centralize constants/configuration

**Complexity**
- Reduce nested if statements
- Replace complex conditions with functions
- Use early returns
- Simplify boolean logic

**TypeScript**
- Remove `any` types
- Add proper type annotations
- Use interfaces for object shapes
- Leverage utility types (Pick, Omit, Partial)

### 2. **Modern Patterns to Apply**

**JavaScript/TypeScript**
```typescript
// Use optional chaining
const value = obj?.prop?.nested

// Use nullish coalescing
const result = value ?? defaultValue

// Use destructuring
const { name, email } = user

// Use template literals
const message = `Hello, ${name}!`

// Use array methods
const filtered = arr.filter(x => x.active)
```

**React**
```typescript
// Extract custom hooks
const useUserData = () => {
  // logic here
}

// Use proper TypeScript types
interface Props {
  user: User
  onUpdate: (user: User) => void
}

// Avoid prop drilling with composition
<Provider value={data}>
  <Component />
</Provider>
```

### 3. **Refactoring Techniques**

**Extract Function**
```typescript
// Before
const process = () => {
  // 50 lines of code
}

// After
const validate = () => { /* ... */ }
const transform = () => { /* ... */ }
const save = () => { /* ... */ }

const process = () => {
  validate()
  const data = transform()
  save(data)
}
```

**Replace Conditional with Polymorphism**
```typescript
// Before
if (type === 'A') return processA()
if (type === 'B') return processB()

// After
const processors = {
  A: processA,
  B: processB
}
return processors[type]()
```

**Introduce Parameter Object**
```typescript
// Before
function create(name, email, age, address)

// After
interface UserData {
  name: string
  email: string
  age: number
  address: string
}
function create(userData: UserData)
```

### 4. **Common Cleanup Tasks**

**Remove Dead Code**
- Unused imports
- Unreachable code
- Commented out code
- Unused variables

**Improve Error Handling**
```typescript
// Before
try { doSomething() } catch (e) { console.log(e) }

// After
try {
  doSomething()
} catch (error) {
  if (error instanceof ValidationError) {
    // Handle validation
  } else {
    logger.error('Unexpected error', { error })
    throw error
  }
}
```

**Consistent Formatting**
- Proper indentation
- Consistent quotes
- Line length (<100 characters)
- Organized imports

**Better Comments**
- Remove obvious comments
- Add why, not what
- Document complex logic
- Update outdated comments

### 5. **Next.js/React Specific**

**Server vs Client Components**
```typescript
// Move state to client component
'use client'
function Interactive() {
  const [state, setState] = useState()
}

// Keep data fetching in server component
async function Page() {
  const data = await fetchData()
}
```

**Proper Data Fetching**
```typescript
// Use SWR/React Query for client
const { data } = useSWR('/api/user')

// Use direct fetch in server components
const data = await fetch('/api/user').then(r => r.json())
```

## Output Format

1. **Issues Found** - List of code smells and problems
2. **Cleaned Code** - Refactored version
3. **Explanations** - What changed and why
4. **Before/After Comparison** - Side-by-side if helpful
5. **Further Improvements** - Optional enhancements

Focus on practical improvements that make code more maintainable without over-engineering. Balance clean code with pragmatism.
