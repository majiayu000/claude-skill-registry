---
name: typescript-dry-principle
description: Apply DRY principle to eliminate code duplication in TypeScript projects with comprehensive refactoring patterns
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: code-refactoring
---

## What I do

I help you eliminate code duplication in TypeScript projects by applying the DRY (Don't Repeat Yourself) principle:

1. **Analyze Codebase**: Scan TypeScript files to identify repeated code patterns, logic, types, and configurations
2. **Identify Duplication Patterns**: Detect common anti-patterns including:
   - Duplicate logic across multiple functions/components
   - Repeated type definitions
   - Copy-pasted code blocks
   - Similar functions with slight variations
   - Scattered configuration values
3. **Extract Common Logic**: Refactor duplicated code into reusable utility functions and modules
4. **Consolidate Type Definitions**: Merge duplicate types into shared interfaces and type utilities
5. **Create Generic Solutions**: Build type-safe reusable components using TypeScript generics
6. **Organize Folder Structure**: Restructure code into logical directories (types/, utils/, constants/, hooks/, services/)
7. **Replace Duplicated Code**: Update files to import from shared modules instead of duplicating code
8. **Verify Refactoring**: Ensure code compiles and tests pass after changes

## When to use me

Use this workflow when:
- You notice similar code blocks across multiple TypeScript files
- You're copy-pasting code between modules or components
- Type definitions are duplicated or repeated across files
- Business logic appears in multiple places with slight variations
- Configuration values are scattered across multiple files
- Tests contain repeated setup/teardown logic
- You want to improve code maintainability and reduce technical debt
- Preparing for a code review to address technical debt
- Setting up a new TypeScript project with proper code organization

Ask clarifying questions if the scope of refactoring is unclear or if you want to focus on specific areas.

## Prerequisites

- TypeScript project with source code (.ts, .tsx files)
- File permissions to read and modify TypeScript files
- TypeScript compiler installed and configured
- (Optional) Test suite to verify refactoring doesn't break functionality
- (Optional) Git repository to commit refactoring changes

## Steps

### Step 1: Analyze Codebase for Duplication Patterns

Scan TypeScript files to identify duplication:
```bash
# Find TypeScript files
find . -name "*.ts" -o -name "*.tsx" -not -path "*/node_modules/*" -not -path "*/dist/*" -not -path "*/build/*"

# Analyze files for common patterns
# Look for:
# - Similar function names with variations (getUserData, getUserInfo, getUserDetails)
# - Repeated API calls or data fetching logic
# - Duplicate type definitions across files
# - Similar component structures with slight differences
```

**Common Duplication Indicators:**
- Functions with similar names (getUser vs getUserData vs getUserInfo)
- Nearly identical code blocks with slight variations
- Same type interfaces defined in multiple files
- Repeated validation or transformation logic
- Similar component structures with different props

### Step 2: Categorize Duplication Types

Identify the type of duplication to apply appropriate refactoring pattern:

| Duplication Type | Description | Refactoring Approach |
|------------------|-------------|----------------------|
| **Logic Duplication** | Same business logic in multiple functions | Extract to shared utility functions |
| **Type Duplication** | Duplicate interfaces/types across files | Consolidate into shared types/ directory |
| **Component Duplication** | Similar components with minor variations | Create generic components using TypeScript generics |
| **Configuration Duplication** | Same config values in multiple files | Create constants/ directory |
| **API Call Duplication** | Repeated API calls with similar logic | Create API service layer |
| **Validation Duplication** | Same validation logic in multiple places | Create shared validators |
| **Template Duplication** | Similar code patterns that could be templated | Create higher-order functions or components |

### Step 3: Extract Common Logic to Utility Functions

Refactor duplicate logic into shared utility functions:

**Example 1: Data Transformation Logic**

Before (duplicated across multiple files):
```typescript
// In file1.ts
function formatUserName(firstName: string, lastName: string): string {
  return `${firstName.charAt(0).toUpperCase()}${firstName.slice(1).toLowerCase()} ${lastName.charAt(0).toUpperCase()}${lastName.slice(1).toLowerCase()}`
}

// In file2.ts
function formatAuthorName(firstName: string, lastName: string): string {
  return `${firstName.charAt(0).toUpperCase()}${firstName.slice(1).toLowerCase()} ${lastName.charAt(0).toUpperCase()}${lastName.slice(1).toLowerCase()}`
}
```

After (refactored to shared utility):
```typescript
// In utils/stringUtils.ts
export function capitalizeFirstLetter(word: string): string {
  if (!word) return ''
  return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
}

export function formatFullName(firstName: string, lastName: string): string {
  return `${capitalizeFirstLetter(firstName)} ${capitalizeFirstLetter(lastName)}`
}

// In file1.ts
import { formatFullName } from '../utils/stringUtils'

function formatUserName(firstName: string, lastName: string): string {
  return formatFullName(firstName, lastName)
}

// In file2.ts
import { formatFullName } from '../utils/stringUtils'

function formatAuthorName(firstName: string, lastName: string): string {
  return formatFullName(firstName, lastName)
}
```

**Example 2: API Call Duplication**

Before (duplicated across multiple components):
```typescript
// In component1.ts
async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`)
  if (!response.ok) throw new Error('Failed to fetch user')
  return response.json()
}

// In component2.ts
async function fetchUserProfile(id: string): Promise<UserProfile> {
  const response = await fetch(`/api/users/${id}/profile`)
  if (!response.ok) throw new Error('Failed to fetch user profile')
  return response.json()
}
```

After (refactored to shared service):
```typescript
// In services/apiService.ts
class ApiService {
  private baseUrl: string = '/api'

  async fetch<T>(endpoint: string): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`)
    if (!response.ok) throw new Error(`Failed to fetch ${endpoint}`)
    return response.json()
  }

  async getUser(id: string): Promise<User> {
    return this.fetch<User>(`/users/${id}`)
  }

  async getUserProfile(id: string): Promise<UserProfile> {
    return this.fetch<UserProfile>(`/users/${id}/profile`)
  }
}

export const apiService = new ApiService()

// In component1.ts
import { apiService } from '../services/apiService'

async function fetchUser(id: string): Promise<User> {
  return apiService.getUser(id)
}

// In component2.ts
import { apiService } from '../services/apiService'

async function fetchUserProfile(id: string): Promise<UserProfile> {
  return apiService.getUserProfile(id)
}
```

### Step 4: Consolidate Type Definitions

Merge duplicate type definitions into shared interfaces:

**Before (duplicated types in multiple files):**
```typescript
// In file1.ts
interface UserData {
  id: string
  name: string
  email: string
}

// In file2.ts
interface UserInfo {
  id: string
  fullName: string
  emailAddress: string
}

// In file3.ts
interface UserProfile {
  userId: string
  displayName: string
  contactEmail: string
}
```

After (consolidated in shared types file):
```typescript
// In types/user.ts
export interface User {
  id: string
  name: string
  email: string
}

// In file1.ts
import type { User } from '../types/user'
const userData: User = { /* ... */ }

// In file2.ts
import type { User } from '../types/user'
const userInfo: User = { /* ... */ }

// In file3.ts
import type { User } from '../types/user'
const userProfile: User = { /* ... */ }
```

**Advanced Type Consolidation (using utility types):**
```typescript
// In types/api.ts
export type ApiResponse<T> = {
  data: T
  error: string | null
  status: 'success' | 'error'
}

export type PaginatedResponse<T> = {
  items: T[]
  total: number
  page: number
  pageSize: number
}

// In types/common.ts
export type Optional<T> = T | null | undefined
export type Nullable<T> = T | null

export type DeepPartial<T> = {
  [P in keyof T]?: T[P]
}
```

### Step 5: Create Generic Components with TypeScript Generics

Refactor similar components into generic reusable components:

**Example 1: Generic List Component**

Before (duplicated list components):
```typescript
// In UserList.tsx
interface UserListProps {
  users: User[]
  onSelectUser: (user: User) => void
}

export function UserList({ users, onSelectUser }: UserListProps) {
  return (
    <ul>
      {users.map(user => (
        <li key={user.id} onClick={() => onSelectUser(user)}>
          {user.name}
        </li>
      ))}
    </ul>
  )
}

// In ProductList.tsx
interface ProductListProps {
  products: Product[]
  onSelectProduct: (product: Product) => void
}

export function ProductList({ products, onSelectProduct }: ProductListProps) {
  return (
    <ul>
      {products.map(product => (
        <li key={product.id} onClick={() => onSelectProduct(product)}>
          {product.name}
        </li>
      ))}
    </ul>
  )
}
```

After (refactored to generic component):
```typescript
// In components/GenericList.tsx
interface GenericListProps<T> {
  items: T[]
  key: keyof T
  renderItem: (item: T) => React.ReactNode
  onSelectItem: (item: T) => void
}

export function GenericList<T>({ items, key, renderItem, onSelectItem }: GenericListProps<T>) {
  return (
    <ul>
      {items.map(item => (
        <li key={String(item[key])} onClick={() => onSelectItem(item)}>
          {renderItem(item)}
        </li>
      ))}
    </ul>
  )
}

// In UserList.tsx
import { GenericList } from './GenericList'
import type { User } from '../types/user'

export function UserList({ users, onSelectUser }: { users: User[]; onSelectUser: (user: User) => void }) {
  return (
    <GenericList
      items={users}
      key="id"
      renderItem={(user) => <span>{user.name}</span>}
      onSelectItem={onSelectUser}
    />
  )
}

// In ProductList.tsx
import { GenericList } from './GenericList'
import type { Product } from '../types/product'

export function ProductList({ products, onSelectProduct }: { products: Product[]; onSelectProduct: (product: Product) => void }) {
  return (
    <GenericList
      items={products}
      key="id"
      renderItem={(product) => <span>{product.name}</span>}
      onSelectItem={onSelectProduct}
    />
  )
}
```

**Example 2: Generic Data Fetching Hook**

Before (duplicated fetching logic in multiple components):
```typescript
// In useUserData.ts
export function useUserData(userId: string) {
  const [data, setData] = useState<User | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchData() {
      setLoading(true)
      setError(null)
      try {
        const response = await fetch(`/api/users/${userId}`)
        const result = await response.json()
        setData(result)
      } catch (err) {
        setError('Failed to fetch user')
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [userId])

  return { data, loading, error }
}
```

After (refactored to generic hook):
```typescript
// In hooks/useApiData.ts
interface UseApiDataOptions {
  immediate?: boolean
}

export function useApiData<T>(url: string, options: UseApiDataOptions = {}) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchData() {
      setLoading(true)
      setError(null)
      try {
        const response = await fetch(url)
        const result = await response.json()
        setData(result)
      } catch (err) {
        setError('Failed to fetch data')
      } finally {
        setLoading(false)
      }
    }

    if (options.immediate !== false) {
      fetchData()
    }
  }, [url, options.immediate])

  return { data, loading, error, refetch: () => fetchData() }
}

// In useUserData.ts
export function useUserData(userId: string) {
  return useApiData<User>(`/api/users/${userId}`)
}
```

### Step 6: Create Constants Directory

Extract scattered configuration values into shared constants:

**Before (configuration scattered across files):**
```typescript
// In component1.tsx
const API_BASE_URL = 'https://api.example.com/v1'
const MAX_RETRIES = 3
const TIMEOUT = 5000

// In component2.tsx
const API_BASE_URL = 'https://api.example.com/v1'
const MAX_RETRIES = 3
const TIMEOUT = 5000

// In service.ts
const API_BASE_URL = 'https://api.example.com/v1'
const MAX_RETRIES = 3
const TIMEOUT = 5000
```

After (consolidated in constants):**
```typescript
// In constants/api.ts
export const API_CONFIG = {
  BASE_URL: 'https://api.example.com/v1',
  MAX_RETRIES: 3,
  TIMEOUT: 5000,
  ENDPOINTS: {
    USERS: '/users',
    PRODUCTS: '/products',
    ORDERS: '/orders'
  } as const
} as const

export const UI_CONFIG = {
  ANIMATION_DURATION: 300,
  DEBOUNCE_DELAY: 500,
  TOAST_DURATION: 3000
} as const

// In component1.tsx
import { API_CONFIG } from '../constants/api'

async function fetchData() {
  const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.USERS}`)
  // ...
}

// In component2.tsx
import { API_CONFIG } from '../constants/api'

async function fetchData() {
  const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.PRODUCTS}`)
  // ...
}
```

### Step 7: Create Validator Utilities

Extract duplicate validation logic into shared validators:

**Example: Email Validation**

Before (duplicate validation in multiple places):
```typescript
// In component1.tsx
function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

// In component2.tsx
function checkEmail(email: string): boolean {
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailPattern.test(email)
}

// In form.tsx
function isEmailValid(email: string): boolean {
  const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return pattern.test(email)
}
```

After (consolidated in validators):**
```typescript
// In utils/validators.ts
export class Validators {
  private static emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

  static email(email: string): boolean {
    return this.emailRegex.test(email)
  }

  static minLength(value: string, min: number): boolean {
    return value.length >= min
  }

  static maxLength(value: string, max: number): boolean {
    return value.length <= max
  }

  static required(value: string): boolean {
    return value.trim().length > 0
  }

  static pattern(value: string, pattern: RegExp): boolean {
    return pattern.test(value)
  }

  static phone(value: string): boolean {
    const phoneRegex = /^\+?[\d\s-()]+$/
    return phoneRegex.test(value)
  }
}

// In component1.tsx
import { Validators } from '../utils/validators'

function validateEmail(email: string): boolean {
  return Validators.email(email)
}

// In form.tsx
import { Validators } from '../utils/validators'

function checkEmail(email: string): boolean {
  return Validators.email(email)
}
```

### Step 8: Organize Folder Structure

Restructure code into logical directories:

```
src/
├── types/              # Shared type definitions
│   ├── index.ts        # Type exports
│   ├── user.ts         # User-related types
│   ├── api.ts          # API response types
│   └── common.ts       # Common utility types
├── utils/              # Reusable utility functions
│   ├── stringUtils.ts  # String manipulation
│   ├── dateUtils.ts    # Date formatting
│   ├── validators.ts    # Validation logic
│   └── apiHelpers.ts   # API helper functions
├── constants/          # Configuration values
│   ├── api.ts          # API endpoints and config
│   └── ui.ts           # UI configuration
├── services/           # API and business logic services
│   └── apiService.ts  # API service layer
├── components/          # Reusable UI components
│   ├── generic/         # Generic components
│   └── specific/       # Domain-specific components
├── hooks/              # Custom React hooks
│   ├── useApiData.ts   # API data fetching hook
│   └── useAuth.ts      # Authentication hook
└── pages/              # Page components
```

### Step 9: Replace Duplicated Code with Imports

Update files to use shared modules instead of duplicated code:

```typescript
// Before - duplicated logic
function calculateTotal(items: any[]): number {
  let total = 0
  for (const item of items) {
    total += item.price
  }
  return total
}

function calculateSum(items: any[]): number {
  let sum = 0
  for (const item of items) {
    sum += item.amount
  }
  return sum
}

function calculateAverage(items: any[]): number {
  let sum = 0
  for (const item of items) {
    sum += item.value
  }
  return sum / items.length
}

// After - extracted to shared utility
import { calculateArraySum } from '../utils/arrayUtils'

function calculateTotal(items: any[]): number {
  return calculateArraySum(items, 'price')
}

function calculateSum(items: any[]): number {
  return calculateArraySum(items, 'amount')
}

function calculateAverage(items: any[]): number {
  return calculateArraySum(items, 'value') / items.length
}
```

**Shared utility function:**
```typescript
// In utils/arrayUtils.ts
export function calculateArraySum<T>(items: T[], key: keyof T): number {
  return items.reduce((sum, item) => sum + (item[key] as number), 0)
}

export function calculateArrayAverage<T>(items: T[], key: keyof T): number {
  if (items.length === 0) return 0
  const sum = calculateArraySum(items, key)
  return sum / items.length
}
```

### Step 10: Verify Refactoring

Ensure code compiles and tests pass after refactoring:

```bash
# Check TypeScript compilation
npx tsc --noEmit

# Run tests
npm run test

# Build project
npm run build

# Run linting
npm run lint
```

**Refactoring Verification Checklist:**
- [ ] No TypeScript compilation errors
- [ ] All tests pass
- [ ] No new linting errors introduced
- [ ] Removed all identified duplicate code
- [ ] Shared modules are properly exported
- [ ] Imports use correct relative/absolute paths
- [ ] Folder structure is logical and organized

## Best Practices

**DRY Principles:**
- **Single Responsibility**: Each function/module should have one clear purpose
- **Composition over Inheritance**: Prefer composition for code reuse
- **Immutability**: Use immutable data structures where possible
- **Type Safety**: Leverage TypeScript's type system to prevent runtime errors
- **Extract Early**: Refactor duplication as soon as you identify it
- **Utility-First**: Create reusable utilities before business logic

**TypeScript-Specific Best Practices:**
- **Interfaces Over Types**: Use interfaces for object shapes, types for unions/primitives
- **Utility Types**: Use Pick, Omit, Partial, Record for type transformations
- **Generics**: Use generics for reusable components and functions
- **Type Guards**: Use type guards for runtime type checking
- **Never Types**: Avoid `any` - use proper type definitions
- **Readonly**: Mark properties as readonly where appropriate

**Code Organization:**
- **Feature-Based Folders**: Group related files in feature directories
- **Shared Resources**: Keep shared utilities in dedicated directories
- **Index Files**: Use index.ts files for clean imports
- **Barrel Exports**: Export related items from single index file
- **Separation of Concerns**: Keep UI, business logic, and data separate

**Refactoring Workflow:**
- **Analyze First**: Identify all duplication before making changes
- **Small Steps**: Refactor incrementally, test after each change
- **Test Coverage**: Ensure tests exist for refactored code
- **Git Commits**: Commit refactoring in logical chunks
- **Backward Compatibility**: Maintain existing public APIs

## Common Issues

### Breaking Changes After Refactoring

**Issue**: Refactoring breaks existing code that imports refactored modules

**Solution:**
- Use git bisect to identify which commit broke functionality
- Check import paths and ensure they're correct
- Verify exported interfaces match what consumers expect
- Add index.ts files with proper re-exports
- Run tests frequently during refactoring

### Circular Dependencies

**Issue**: Extracted utilities create circular dependencies

**Solution:**
- Analyze dependency graph before extraction
- Split utilities into smaller, more focused modules
- Use dependency injection where appropriate
- Consider merging closely related utilities
- Move shared types to separate types/ directory

### Type Errors After Consolidation

**Issue**: Merged types cause TypeScript compilation errors

**Solution:**
- Use intersection types when combining similar interfaces
- Use utility types (Pick, Omit, Partial) to transform types
- Add proper type guards for runtime type checking
- Review generic constraints and type parameters
- Use `satisfies` keyword for complex type constraints

### Over-Engineering

**Issue**: Creating overly complex generic abstractions

**Solution:**
- Start with concrete implementations, extract abstractions later
- Prefer composition over complex inheritance
- Keep generics simple with clear constraints
- Use type assertions sparingly and only when necessary
- Focus on actual duplication, not theoretical abstraction

## Advanced Refactoring Patterns

### Higher-Order Components

Wrap components with additional behavior:
```typescript
// In components/withLoading.tsx
interface WithLoadingProps {
  isLoading: boolean
  loadingText?: string
}

export function withLoading<P>(
  Component: React.ComponentType<P>,
  props: P & WithLoadingProps
) {
  if (props.isLoading) {
    return (
      <div>
        <Component {...props} disabled={true} />
        <div className="loading-overlay">
          {props.loadingText || 'Loading...'}
        </div>
      </div>
    )
  }
  return <Component {...props} />
}

// Usage
export function UserList({ users, loading }: UserListProps) {
  return (
    <div>
      <GenericList
        items={users}
        renderItem={(user) => <span>{user.name}</span>}
        onSelectItem={onSelectUser}
      />
    </div>
  )
}

export function LoadingUserList({ users, loading }: UserListProps) {
  return (
    <div>
      <GenericList
        items={users}
        renderItem={(user) => <span>{user.name}</span>}
        onSelectItem={onSelectUser}
      />
    </div>
  )
}
```

### Factory Pattern

Create objects without specifying exact classes:
```typescript
// In utils/dataFetcher.ts
interface DataFetcher<T> {
  fetch(id: string): Promise<T>
}

class UserDataFetcher implements DataFetcher<User> {
  async fetch(id: string): Promise<User> {
    const response = await fetch(`/api/users/${id}`)
    return response.json()
  }
}

class ProductDataFetcher implements DataFetcher<Product> {
  async fetch(id: string): Promise<Product> {
    const response = await fetch(`/api/products/${id}`)
    return response.json()
  }
}

// Factory function
export function createDataFetcher<T>(type: 'user' | 'product'): DataFetcher<T> {
  switch (type) {
    case 'user':
      return new UserDataFetcher() as DataFetcher<T>
    case 'product':
      return new ProductDataFetcher() as DataFetcher<T>
  }
}

// Usage
const userFetcher = createDataFetcher<User>('user')
const productFetcher = createDataFetcher<Product>('product')

const user = await userFetcher.fetch('123')
const product = await productFetcher.fetch('456')
```

### Repository Pattern

Centralize data access logic:
```typescript
// In repositories/UserRepository.ts
class UserRepository {
  private apiUrl: string = '/api/users'

  async findById(id: string): Promise<User> {
    const response = await fetch(`${this.apiUrl}/${id}`)
    return response.json()
  }

  async findAll(): Promise<User[]> {
    const response = await fetch(this.apiUrl)
    return response.json()
  }

  async create(user: Omit<User, 'id'>): Promise<User> {
    const response = await fetch(this.apiUrl, {
      method: 'POST',
      body: JSON.stringify(user)
    })
    return response.json()
  }

  async update(id: string, user: Partial<User>): Promise<User> {
    const response = await fetch(`${this.apiUrl}/${id}`, {
      method: 'PUT',
      body: JSON.stringify(user)
    })
    return response.json()
  }

  async delete(id: string): Promise<void> {
    await fetch(`${this.apiUrl}/${id}`, { method: 'DELETE' })
  }
}

export const userRepository = new UserRepository()

// Usage in components
import { userRepository } from '../repositories/UserRepository'

const user = await userRepository.findById('123')
const allUsers = await userRepository.findAll()
await userRepository.create({ name: 'John', email: 'john@example.com' })
```

## Troubleshooting Checklist

Before refactoring:
- [ ] Codebase has been analyzed for duplication patterns
- [ ] Duplication types have been categorized
- [ ] Target files/modules for refactoring identified
- [ ] Tests exist for code to be refactored

During refactoring:
- [ ] Each step is tested before moving to next
- [ ] No TypeScript compilation errors introduced
- [ ] Existing tests still pass
- [ ] Code is committed in logical chunks
- [ ] Import paths are verified after each change

After refactoring:
- [ ] All identified duplication has been eliminated
- [ ] Code compiles without errors
- [ ] All tests pass
- [ ] No new linting errors
- [ ] Folder structure is organized and logical
- [ ] Shared modules are properly exported
- [ ] Documentation is updated if needed

## Related Skills

- `nextjs-standard-setup`: For creating standardized Next.js 16 applications with proper component architecture
- `linting-workflow`: Ensure code quality during refactoring
- `docstring-generator`: Add documentation to refactored code
- `typescript-dry-principle`: This skill
- `nextjs-pr-workflow`: Create PR after completing refactoring
- `test-generator-framework`: Generate tests for refactored code
