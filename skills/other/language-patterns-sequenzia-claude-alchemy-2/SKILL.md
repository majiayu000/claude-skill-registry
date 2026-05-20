---
name: language-patterns
description: Provides language-specific patterns for TypeScript, Python, and React including idioms, best practices, and common patterns. Use when implementing features in these languages.
model: inherit
user-invocable: false
disable-model-invocation: false
---

# Language Patterns

This skill provides language-specific patterns and best practices. Apply patterns that match the project's language and framework.

---

## TypeScript Patterns

### Type Safety

**Use strict types over `any`:**
```typescript
// Bad
function process(data: any): any {
  return data.value;
}

// Good
interface DataItem {
  value: string;
  count: number;
}

function process(data: DataItem): string {
  return data.value;
}
```

**Use discriminated unions for variants:**
```typescript
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: Error };

function handleResult<T>(result: Result<T>) {
  if (result.success) {
    // TypeScript knows result.data exists
    console.log(result.data);
  } else {
    // TypeScript knows result.error exists
    console.error(result.error);
  }
}
```

**Use `unknown` over `any` for external data:**
```typescript
async function fetchData(): Promise<unknown> {
  const response = await fetch('/api/data');
  return response.json();
}

// Then validate/parse
const data = await fetchData();
if (isValidData(data)) {
  // Now safely typed
}
```

### Null Handling

**Use optional chaining and nullish coalescing:**
```typescript
// Optional chaining
const userName = user?.profile?.name;

// Nullish coalescing (only for null/undefined)
const displayName = userName ?? 'Anonymous';

// Combine them
const city = user?.address?.city ?? 'Unknown';
```

**Use type guards:**
```typescript
function isUser(obj: unknown): obj is User {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj &&
    'email' in obj
  );
}
```

### Async Patterns

**Prefer async/await over raw promises:**
```typescript
// Good
async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch user: ${response.status}`);
  }
  return response.json();
}
```

**Handle errors properly:**
```typescript
async function safeOperation(): Promise<Result<Data>> {
  try {
    const data = await riskyOperation();
    return { success: true, data };
  } catch (error) {
    return { success: false, error: error as Error };
  }
}
```

**Parallel operations:**
```typescript
// Run in parallel
const [users, posts] = await Promise.all([
  fetchUsers(),
  fetchPosts()
]);

// With error handling
const results = await Promise.allSettled([
  fetchUsers(),
  fetchPosts()
]);
```

---

## Python Patterns

### Type Hints

**Use type hints for clarity:**
```python
from typing import Optional, List, Dict

def process_users(
    users: List[dict],
    filter_active: bool = True
) -> List[str]:
    """Process users and return their names."""
    result: List[str] = []
    for user in users:
        if filter_active and not user.get("active"):
            continue
        result.append(user["name"])
    return result
```

**Use dataclasses for data containers:**
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: int
    email: str
    name: str
    active: bool = True
    profile: Optional[dict] = None
```

**Use Pydantic for validation:**
```python
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    age: int

    class Config:
        extra = "forbid"  # Reject unknown fields
```

### Pythonic Patterns

**Use comprehensions:**
```python
# List comprehension
names = [user.name for user in users if user.active]

# Dict comprehension
user_map = {user.id: user for user in users}

# Generator for large data
active_users = (user for user in users if user.active)
```

**Context managers for resources:**
```python
# File handling
with open("file.txt", "r") as f:
    content = f.read()

# Database connections
with get_db_connection() as conn:
    conn.execute(query)

# Custom context manager
from contextlib import contextmanager

@contextmanager
def timer(name: str):
    start = time.time()
    yield
    print(f"{name}: {time.time() - start:.2f}s")
```

**Use `pathlib` for paths:**
```python
from pathlib import Path

config_path = Path(__file__).parent / "config" / "settings.yaml"
if config_path.exists():
    content = config_path.read_text()
```

### Error Handling

```python
class ValidationError(Exception):
    """Raised when input validation fails."""
    pass

class NotFoundError(Exception):
    """Raised when a resource is not found."""
    pass

def get_user(user_id: int) -> User:
    user = db.query(User).get(user_id)
    if user is None:
        raise NotFoundError(f"User {user_id} not found")
    return user
```

---

## React Patterns

### Component Patterns

**Functional components with hooks:**
```tsx
interface UserCardProps {
  user: User;
  onEdit: (user: User) => void;
}

function UserCard({ user, onEdit }: UserCardProps) {
  const handleClick = useCallback(() => {
    onEdit(user);
  }, [user, onEdit]);

  return (
    <div className="user-card">
      <h3>{user.name}</h3>
      <button onClick={handleClick}>Edit</button>
    </div>
  );
}
```

**Custom hooks for logic reuse:**
```tsx
function useUser(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    setLoading(true);
    fetchUser(userId)
      .then(setUser)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [userId]);

  return { user, loading, error };
}
```

### State Management

**Use appropriate state level:**
```tsx
// Local state - component only
const [isOpen, setIsOpen] = useState(false);

// Lifted state - shared between siblings
// Put in common parent

// Context - deeply nested sharing
const ThemeContext = createContext<Theme>("light");

// External store - complex app state
// Use Redux, Zustand, or similar
```

**Derive state when possible:**
```tsx
// Bad: redundant state
const [items, setItems] = useState<Item[]>([]);
const [totalCount, setTotalCount] = useState(0);

// Good: derive from source of truth
const [items, setItems] = useState<Item[]>([]);
const totalCount = items.length;
```

### Performance

**Memoization:**
```tsx
// Memoize expensive computations
const sortedItems = useMemo(
  () => items.sort((a, b) => a.name.localeCompare(b.name)),
  [items]
);

// Memoize callbacks passed to children
const handleClick = useCallback(() => {
  doSomething(id);
}, [id]);

// Memoize components
const MemoizedChild = memo(ChildComponent);
```

**Lazy loading:**
```tsx
const HeavyComponent = lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <HeavyComponent />
    </Suspense>
  );
}
```

### Error Boundaries

```tsx
class ErrorBoundary extends Component<Props, State> {
  state = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    logError(error, info);
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback error={this.state.error} />;
    }
    return this.props.children;
  }
}
```

---

## General Best Practices

### Naming Conventions

| Language | Variables | Functions | Classes | Constants |
|----------|-----------|-----------|---------|-----------|
| TypeScript | camelCase | camelCase | PascalCase | UPPER_SNAKE |
| Python | snake_case | snake_case | PascalCase | UPPER_SNAKE |
| React | camelCase | camelCase/use* | PascalCase | UPPER_SNAKE |

### File Organization

**TypeScript/React:**
```
src/
  components/
    Button/
      Button.tsx
      Button.test.tsx
      index.ts
  hooks/
  utils/
  types/
```

**Python:**
```
src/
  package/
    __init__.py
    models.py
    services.py
    utils.py
  tests/
    test_models.py
    test_services.py
```

### Import Organization

**TypeScript:**
```typescript
// 1. External packages
import React from 'react';
import { useState } from 'react';

// 2. Internal modules (absolute)
import { Button } from '@/components';
import { useAuth } from '@/hooks';

// 3. Relative imports
import { helper } from './utils';
import type { Props } from './types';
```

**Python:**
```python
# 1. Standard library
import os
from pathlib import Path

# 2. Third-party packages
import requests
from pydantic import BaseModel

# 3. Local imports
from .models import User
from .utils import helper
```
