---
name: "TypeScript"
description: "Framework-focused TypeScript development with types, interfaces, generics, and utility types"
when_to_use: "When working with TypeScript codebases, defining type-safe APIs, implementing generic patterns, or needing utility types for type transformations"
---

# TypeScript Skill

## Quick Start

```typescript
// Basic type annotations
const name: string = "John";
const age: number = 25;
const isActive: boolean = true;

// Array types
const numbers: number[] = [1, 2, 3];
const users: Array<User> = [user1, user2];

// Object types
interface User {
  id: number;
  name: string;
  email?: string; // optional
}

// Function types
const greet = (name: string): string => `Hello, ${name}!`;
const add = (a: number, b: number): number => a + b;
```

## Common Patterns

### Interface Definitions

```typescript
// Basic interface
interface Product {
  id: string;
  name: string;
  price: number;
}

// Interface with optional properties
interface UserProfile {
  id: number;
  username: string;
  avatar?: string;
  bio?: string;
}

// Interface extending another
interface AdminUser extends UserProfile {
  permissions: string[];
  role: "admin" | "super_admin";
}

// Generic interface
interface ApiResponse<T> {
  data: T;
  status: number;
  message: string;
}

// Usage
const userResponse: ApiResponse<User> = {
  data: { id: 1, username: "john", email: "john@example.com" },
  status: 200,
  message: "Success",
};
```

### Generic Types and Functions

```typescript
// Generic function
function identity<T>(arg: T): T {
  return arg;
}

// Generic function with constraints
interface Lengthwise {
  length: number;
}

function getLength<T extends Lengthwise>(arg: T): number {
  return arg.length;
}

// Generic class
class Box<T> {
  private contents: T;

  constructor(value: T) {
    this.contents = value;
  }

  getValue(): T {
    return this.contents;
  }
}

// Generic utility function
function createApiResponse<T>(data: T, status = 200): ApiResponse<T> {
  return {
    data,
    status,
    message: status >= 400 ? "Error" : "Success",
  };
}
```

### Utility Types

```typescript
// Pick - select specific properties
type UserContactInfo = Pick<User, "email" | "phone">;

// Omit - remove specific properties
type CreateUserRequest = Omit<User, "id" | "createdAt">;

// Partial - make all properties optional
type PartialUser = Partial<User>;

// Required - make all properties required
type RequiredUser = Required<UserProfile>;

// Record - create object type with specific keys
type StatusMap = Record<"pending" | "approved" | "rejected", string>;

// Extract properties that match a condition
type StringProperties<T> = {
  [K in keyof T]: T[K] extends string ? K : never;
}[keyof T];

// Function property extraction
type FunctionPropertyNames<T> = {
  [K in keyof T]: T[K] extends Function ? K : never;
}[keyof T];

type FunctionProperties<T> = Pick<T, FunctionPropertyNames<T>>;
```

### Type Guards and Discriminated Unions

```typescript
// Discriminated union
interface LoadingState {
  status: "loading";
}

interface SuccessState<T> {
  status: "success";
  data: T;
}

interface ErrorState {
  status: "error";
  error: string;
}

type DataState<T> = LoadingState | SuccessState<T> | ErrorState;

// Type guard function
function isLoading<T>(state: DataState<T>): state is LoadingState {
  return state.status === "loading";
}

function isSuccess<T>(state: DataState<T>): state is SuccessState<T> {
  return state.status === "success";
}

// Usage
function handleDataState<T>(state: DataState<T>) {
  if (isLoading(state)) {
    console.log("Loading...");
  } else if (isSuccess(state)) {
    console.log("Data:", state.data);
  } else {
    console.log("Error:", state.error);
  }
}
```

### Advanced Type Patterns

```typescript
// Conditional types
type NonNullable<T> = T extends null | undefined ? never : T;

// Mapped types
type OptionalFields<T> = {
  [K in keyof T]?: T[K];
};

// Readonly mapped type
type ReadonlyUser = {
  readonly [K in keyof User]: User[K];
};

// Template literal types
type EventName = `on${Capitalize<string>}`;
type EventHandler = Record<EventName, Function>;

// Recursive utility types
type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};
```

### API Response Patterns

```typescript
// Standard API response
interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

// Error response
interface ApiError {
  code: string;
  message: string;
  details?: Record<string, any>;
}

// Union of success and error responses
type ApiResult<T> =
  | { success: true; data: T }
  | { success: false; error: ApiError };

// Type-safe API client
class ApiClient {
  async get<T>(url: string): Promise<ApiResult<T>> {
    try {
      const response = await fetch(url);
      const data = await response.json();
      return { success: true, data };
    } catch (error) {
      return {
        success: false,
        error: { code: "NETWORK_ERROR", message: error.message },
      };
    }
  }
}
```

### React/Component Patterns

```typescript
// Component props with generics
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
  keyExtractor: (item: T) => string;
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <div>
      {items.map(item => (
        <div key={keyExtractor(item)}>
          {renderItem(item)}
        </div>
      ))}
    </div>
  );
}

// Hook with generic state
interface State<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

function useApi<T>(url: string): State<T> {
  const [state, setState] = useState<State<T>>({
    data: null,
    loading: true,
    error: null
  });

  useEffect(() => {
    fetch(url)
      .then(res => res.json())
      .then(data => setState({ data, loading: false, error: null }))
      .catch(error => setState({ data: null, loading: false, error: error.message }));
  }, [url]);

  return state;
}
```

## Requirements

- TypeScript 4.5+ (for latest utility types and template literal types)
- Understanding of basic JavaScript concepts
- Familiarity with object-oriented programming concepts
- Knowledge of async/await patterns for API work

## Best Practices

1. **Use interface for object shapes** unless you need union types, then use type aliases
2. **Prefer generic types** over `any` for better type safety
3. **Use utility types** (Pick, Omit, Partial) to transform existing types
4. **Create type guards** for discriminated unions
5. **Leverage conditional types** for advanced type transformations
6. **Use readonly** for immutable data structures
7. **Prefer const assertions** for literal types and readonly arrays

## Common Gotchas

- `any` vs `unknown`: Use `unknown` when you need type checking before usage
- `[] as any[]`: Avoid, use proper typing instead
- Function overload ordering: Most specific signatures first
- Generic constraints: Use `extends` to limit generic types
- Type inference: Let TypeScript infer when possible, provide explicit types when needed
