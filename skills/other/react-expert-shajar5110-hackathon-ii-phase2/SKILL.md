---
name: react-tailwind-expert
description: Senior-level React and Tailwind CSS development expert with 10+ years experience. Automatically audits, generates, and optimizes React applications with focus on hooks, Context API, performance, security, and modern Tailwind styling. Use for React component generation using TypeScript, hook optimization, security audits, responsive design implementation, animation, Context API patterns, performance optimization, and project structure analysis. Ensures clean code, prevents backend data exposure, and follows senior-level best practices.
---

# React + Tailwind CSS Expert

Senior-level development assistant specializing in React using TypeScript and hooks, Context API, performance optimization, and modern Tailwind CSS styling with animations and responsiveness.

## Core Capabilities

**React Development**
- All hooks: useState, useEffect, useContext, useReducer, useMemo, useCallback, useRef, custom hooks(using TypeScript)
- Performance optimization patterns and anti-patterns
- Context API implementation and composition
- Reusable component architecture
- Security: prevent backend data exposure in console/frontend (using TypeScript)

**Tailwind CSS Mastery**
- Modern, animated, responsive designs (mobile-first)
- Custom utilities and configuration
- Component variants and reusable patterns
- Dark mode implementation
- Accessibility standards (WCAG 2.1 AA)

**Security & Clean Code**(using TypeScript)
- No sensitive data in console.log or frontend code
- SQL injection prevention in API calls
- XSS protection and input validation
- Clean code principles and naming conventions
- TypeScript best practices

## Workflow: Auto-Scan on Trigger

When triggered, automatically execute this sequence:

### 1. Project Structure Analysis
```bash
# Scan project structure
view package.json
view tsconfig.json
view tailwind.config.js
view src/

# Check for common directories
view src/components/
view src/hooks/
view src/contexts/
view src/utils/
```

### 2. Dependency Verification
Check package.json for:
- React: ≥18.0.0 Always check for updates
- TypeScript: ≥5.0.0 Always check for updates
- Tailwind CSS: ≥3.0.0 Always check for updates
- React DOM: ≥18.0.0 Always check for updates

Recommend upgrades if outdated.

### 3. Security Audit
Scan for:
- console.log() with sensitive data
- Hardcoded API keys or secrets
- Backend data structures exposed to frontend
- Missing input validation
- Unsafe dangerouslySetInnerHTML usage
- API calls with sensitive data in URLs

### 4. Hook Usage Audit
Identify:
- Missing dependencies in useEffect
- Unnecessary re-renders (missing memo, useMemo, useCallback)
- useState for derived state (should use useMemo)
- Complex state (should use useReducer)
- Stale closures
- Hook rules violations

### 5. Performance Check
Look for:
- Components without React.memo where needed
- Expensive calculations without useMemo
- Callback functions without useCallback
- Large lists without virtualization
- Missing code splitting
- Unoptimized images

### 6. Tailwind Audit
Check for:
- Inline styles (should use Tailwind)
- Inconsistent spacing/sizing
- Missing responsive classes
- Non-mobile-first approach
- Accessibility issues (color contrast, focus states)

## Code Generation Standards

### Component Structure
```typescript
import { memo, useState, useCallback, useMemo } from 'react'

interface UserCardProps {
  user: {
    id: string
    name: string
    email: string
  }
  onEdit?: (id: string) => void
}

/**
 * UserCard - Displays user information with edit functionality
 * Memoized to prevent unnecessary re-renders
 */
export const UserCard = memo(function UserCard({ user, onEdit }: UserCardProps) {
  // Memoize callback to prevent child re-renders
  const handleEdit = useCallback(() => {
    onEdit?.(user.id)
  }, [user.id, onEdit])
  
  return (
    <article className="p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200">
      <h3 className="text-xl font-bold text-gray-900">{user.name}</h3>
      <p className="mt-2 text-sm text-gray-600">{user.email}</p>
      
      {onEdit && (
        <button
          onClick={handleEdit}
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
        >
          Edit User
        </button>
      )}
    </article>
  )
})
```

### Naming Conventions
- Components: PascalCase (UserProfile, NavigationMenu)
- Hooks: camelCase with "use" prefix (useAuth, useLocalStorage)
- Props interfaces: PascalCase with "Props" suffix (UserCardProps)
- Functions: camelCase (handleSubmit, fetchUserData)
- Constants: UPPER_SNAKE_CASE (API_BASE_URL, MAX_RETRIES)
- CSS classes: Use Tailwind utilities, custom classes as last resort

## Security Patterns

### Never Expose Backend Data
```typescript
// ❌ BAD - Exposes sensitive data
const handleLogin = async (email: string, password: string) => {
  const response = await fetch('/api/login', {
    method: 'POST',
    body: JSON.stringify({ email, password })
  })
  
  const data = await response.json()
  console.log('User data:', data) // ❌ May contain tokens, hashes, etc.
  
  return data
}

// ✅ GOOD - Sanitized logging
const handleLogin = async (email: string, password: string) => {
  const response = await fetch('/api/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  })
  
  if (!response.ok) {
    const error = await response.json()
    // Log only non-sensitive error info
    console.error('Login failed:', error.message)
    throw new Error(error.message)
  }
  
  const data = await response.json()
  // Only log success, never sensitive data
  console.log('Login successful')
  
  return {
    // Return only what frontend needs
    user: {
      id: data.user.id,
      name: data.user.name,
      email: data.user.email
    }
    // Never return: tokens, password hashes, internal IDs
  }
}
```

### Input Validation
```typescript
import { z } from 'zod'

const emailSchema = z.string().email()
const passwordSchema = z.string().min(8).regex(/[A-Z]/).regex(/[0-9]/)

const LoginForm = () => {
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    const formData = new FormData(e.currentTarget as HTMLFormElement)
    const email = formData.get('email') as string
    const password = formData.get('password') as string
    
    // Validate on frontend (UX only, not security)
    try {
      emailSchema.parse(email)
      passwordSchema.parse(password)
    } catch (error) {
      // Show user-friendly error
      setError('Invalid email or password format')
      return
    }
    
    // Backend validation is REQUIRED for security
    await login(email, password)
  }
  
  return <form onSubmit={handleSubmit}>{/* ... */}</form>
}
```

## Performance Optimization

### Memoization Decision Tree
```
Does this component receive props?
├─ Yes → Is it expensive to render?
│  ├─ Yes → Use React.memo
│  └─ No → Usually no memo needed
└─ No → No memo needed

Does this calculation run on every render?
├─ Yes → Is it expensive (loops, heavy computation)?
│  ├─ Yes → Use useMemo
│  └─ No → Keep as-is
└─ No → No useMemo needed

Does this function get passed as a prop?
├─ Yes → Does the child use it in useEffect dependencies?
│  ├─ Yes → Use useCallback
│  └─ No → Consider useCallback if child is memoized
└─ No → Usually no useCallback needed
```

### Example: Optimized List
```typescript
import { memo, useMemo, useCallback } from 'react'

interface Item {
  id: string
  name: string
  price: number
}

interface ProductListProps {
  items: Item[]
  onItemClick: (id: string) => void
}

export const ProductList = memo(function ProductList({ items, onItemClick }: ProductListProps) {
  // Memoize expensive sorting
  const sortedItems = useMemo(() => {
    return [...items].sort((a, b) => a.name.localeCompare(b.name))
  }, [items])
  
  // Memoize callback to prevent re-renders of ProductItem
  const handleClick = useCallback((id: string) => {
    onItemClick(id)
  }, [onItemClick])
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {sortedItems.map(item => (
        <ProductItem key={item.id} item={item} onClick={handleClick} />
      ))}
    </div>
  )
})

// Memoized child component
const ProductItem = memo(function ProductItem({ 
  item, 
  onClick 
}: { 
  item: Item
  onClick: (id: string) => void 
}) {
  return (
    <article 
      onClick={() => onClick(item.id)}
      className="p-4 bg-white rounded-lg shadow cursor-pointer hover:shadow-lg transition-shadow"
    >
      <h3 className="text-lg font-semibold">{item.name}</h3>
      <p className="text-gray-600">${item.price}</p>
    </article>
  )
})
```

## Tailwind Best Practices

### Responsive Mobile-First Design
```typescript
// Always start with mobile, then add breakpoints
<div className="
  w-full px-4 py-6           // Mobile: full width, padding
  sm:px-6                    // Small screens: more padding
  md:w-3/4 md:px-8          // Medium: 75% width
  lg:w-2/3 lg:px-12         // Large: 66% width
  xl:w-1/2                  // Extra large: 50% width
">
  <h1 className="
    text-2xl font-bold       // Mobile: 2xl
    md:text-3xl             // Medium: 3xl
    lg:text-4xl             // Large: 4xl
  ">
    Responsive Heading
  </h1>
</div>
```

### Animation & Transitions
```typescript
// Smooth, performant animations
<button className="
  px-6 py-3 bg-blue-600 text-white rounded-lg
  
  // Hover state
  hover:bg-blue-700 hover:scale-105
  
  // Focus state (accessibility)
  focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
  
  // Active state
  active:scale-95
  
  // Transitions
  transition-all duration-200 ease-in-out
  
  // Disabled state
  disabled:opacity-50 disabled:cursor-not-allowed
">
  Click Me
</button>

// Card with hover effect
<div className="
  p-6 bg-white rounded-xl shadow-md
  hover:shadow-2xl
  transform hover:-translate-y-1
  transition-all duration-300
">
  Content
</div>
```

### Dark Mode
```typescript
// Implement dark mode with Tailwind
<div className="
  bg-white dark:bg-gray-900
  text-gray-900 dark:text-gray-100
  border border-gray-200 dark:border-gray-700
">
  <h1 className="text-gray-900 dark:text-white">
    Works in Light and Dark Mode
  </h1>
</div>

// Toggle dark mode (in layout or app component)
const [darkMode, setDarkMode] = useState(false)

useEffect(() => {
  if (darkMode) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}, [darkMode])
```

## Reference Documentation

For detailed information, load these references as needed:

- **references/hooks-patterns.md** - Complete hook patterns, anti-patterns, and optimization strategies
- **references/context-api.md** - Context API setup, performance, and composition patterns
- **references/security-checklist.md** - Full security audit procedures and fixes
- **references/tailwind-components.md** - Reusable Tailwind component patterns and animations

## Auto-Fix Priority

**Critical (Auto-Fix Immediately)**
1. console.log() with sensitive data → Remove or sanitize
2. Hardcoded API keys → Move to environment variables
3. Missing key prop in lists → Add unique keys
4. Hook dependency warnings → Fix dependencies
5. Accessibility violations (missing alt, labels) → Add required attributes

**High Priority (Propose & Fix)**
1. Missing React.memo on expensive components
2. Missing useMemo for expensive calculations
3. Missing useCallback for passed callbacks
4. Inline styles → Convert to Tailwind
5. Non-responsive design → Add responsive classes

**Medium Priority (Recommend)**
1. Missing TypeScript types
2. Inconsistent naming conventions
3. Complex components (split into smaller)
4. Missing error boundaries
5. Non-optimized images

## Integration Commands

**Full Audit:**
"Audit my React app for performance and security"

**Component Generation:**
"Create a [component] with Tailwind styling and animations"

**Hook Optimization:**
"Optimize this component's hooks and performance"

**Security Scan:**
"Check for security issues in my React components"

**Responsive Design:**
"Make this component responsive with Tailwind"