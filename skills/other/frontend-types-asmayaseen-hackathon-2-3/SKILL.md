# Frontend TypeScript Types Skill

**Purpose**: Guidance for creating TypeScript type definitions following existing patterns from `frontend/types/index.ts`.

## Overview

All TypeScript types are defined in `frontend/types/index.ts`. Types match backend API response structure and provide type safety across the frontend application.

## Type Patterns from `frontend/types/index.ts`

### 1. User Types

```typescript
export interface User {
  id: string;
  email: string;
  name: string;
  createdAt?: string;
  updatedAt?: string;
}

export interface UserCredentials {
  email: string;
  password: string;
}

export interface UserSignupData extends UserCredentials {
  name: string;
}
```

**Pattern**:
- Use `interface` for object types
- Mark optional fields with `?`
- Use `extends` for type inheritance
- Use camelCase for frontend types (even if backend uses snake_case)

### 2. Task Types

```typescript
export type TaskStatus = "pending" | "completed";
export type TaskPriority = "low" | "medium" | "high";

export interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: TaskPriority;
  due_date?: string;
  tags: string[];
  created_at: string;
  updated_at: string;
}

export interface TaskFormData {
  title: string;
  description?: string;
  priority?: TaskPriority;
  due_date?: string;
  tags?: string[];
}

export interface TaskQueryParams {
  status?: "all" | "pending" | "completed";
  sort?: "created" | "title" | "updated" | "priority" | "due_date";
  search?: string;
  page?: number;
  limit?: number;
}
```

**Pattern**:
- Use `type` for union types (string literals)
- Use `interface` for object types
- Match backend field names (snake_case for API fields like `user_id`, `due_date`, `created_at`)
- Create separate types for form data (all optional except required fields)
- Create separate types for query parameters (all optional)

### 3. API Response Types

```typescript
export interface ApiResponse<T = unknown> {
  data?: T;
  success: boolean;
  message?: string;
  error?: {
    code: string;
    message: string;
    details?: unknown;
  };
}

export interface PaginatedResponse<T> {
  data: T[];
  meta: {
    total: number;
    page: number;
    limit: number;
    totalPages: number;
  };
}
```

**Pattern**:
- Use generic types `<T>` for reusable structures
- Provide default type parameter (`<T = unknown>`)
- Include `success` boolean flag
- Include optional `data`, `message`, and `error` fields
- Create separate type for paginated responses with `meta` object

### 4. Authentication Types

```typescript
export interface AuthResponse {
  success: boolean;
  token: string;
  user: User;
}

export interface Session {
  user: User;
  token: string;
  expiresAt: number;
}
```

**Pattern**:
- Include `success` boolean
- Include `token` string
- Include `user` object (User type)
- Include `expiresAt` timestamp for session

### 5. Error Types

```typescript
export interface AppError {
  message: string;
  code?: string;
  statusCode?: number;
  field?: string;
}

export interface FormErrors {
  [key: string]: string | undefined;
}
```

**Pattern**:
- Use `interface` for error objects
- Mark optional fields with `?`
- Use index signature `[key: string]` for dynamic object types (FormErrors)

### 6. UI Types

```typescript
export type LoadingState = "idle" | "loading" | "success" | "error";

export type ToastType = "success" | "error" | "warning" | "info";

export interface ToastMessage {
  id: string;
  type: ToastType;
  message: string;
  duration?: number;
}
```

**Pattern**:
- Use `type` for union types (string literals)
- Use `interface` for object types
- Include `id` for unique identification
- Mark optional fields with `?`

### 7. Export/Import Types

```typescript
export type ExportFormat = "csv" | "json";

export interface ImportResult {
  imported: number;
  errors: number;
  errorDetails?: string[];
}
```

**Pattern**:
- Use `type` for union types (string literals)
- Use `interface` for result objects
- Include counts for success/error tracking
- Include optional error details array

## Type Naming Conventions

### Interfaces
- **PascalCase**: `User`, `Task`, `ApiResponse`
- **Descriptive names**: `TaskFormData`, `UserSignupData`

### Types (Union Types)
- **PascalCase**: `TaskStatus`, `TaskPriority`, `LoadingState`
- **Descriptive names**: `ToastType`, `ExportFormat`

### Props Types
- **ComponentName + Props**: `TaskItemProps`, `ProtectedRouteProps`
- **Example**: `interface TaskItemProps { task: Task; }`

### Form Data Types
- **EntityName + FormData**: `TaskFormData`, `UserSignupData`
- **Example**: `interface TaskFormData { title: string; description?: string; }`

### Query Parameter Types
- **EntityName + QueryParams**: `TaskQueryParams`
- **Example**: `interface TaskQueryParams { status?: "all" | "pending" | "completed"; }`

## Matching Backend Schema

### Field Name Mapping

**Backend (snake_case)** → **Frontend (camelCase for form data, snake_case for API response)**

```typescript
// Backend API response (matches backend exactly)
export interface Task {
  id: number;
  user_id: string;        // snake_case from backend
  title: string;
  due_date?: string;     // snake_case from backend
  created_at: string;    // snake_case from backend
  updated_at: string;    // snake_case from backend
}

// Frontend form data (camelCase for easier use)
export interface TaskFormData {
  title: string;
  dueDate?: string;      // camelCase for frontend
  tags?: string[];
}
```

**Pattern**:
- API response types match backend exactly (snake_case)
- Form data types use camelCase for easier frontend usage
- Convert between formats when sending/receiving from API

### Required vs Optional Fields

```typescript
// Backend API response (all fields from backend)
export interface Task {
  id: number;              // Required (from backend)
  user_id: string;         // Required (from backend)
  title: string;           // Required (from backend)
  description?: string;    // Optional (from backend)
  completed: boolean;      // Required (from backend)
  priority: TaskPriority;  // Required (from backend)
  due_date?: string;       // Optional (from backend)
  tags: string[];          // Required (from backend, can be empty array)
  created_at: string;      // Required (from backend)
  updated_at: string;      // Required (from backend)
}

// Frontend form data (only fields user can edit)
export interface TaskFormData {
  title: string;           // Required (user must provide)
  description?: string;    // Optional
  priority?: TaskPriority;  // Optional (has default)
  due_date?: string;       // Optional
  tags?: string[];         // Optional (can be empty array)
}
```

**Pattern**:
- API response types include all fields from backend
- Form data types only include fields user can edit
- Mark optional fields with `?`
- Required fields don't have `?`

## Type Structure Patterns

### 1. Use `interface` for Objects

```typescript
export interface User {
  id: string;
  email: string;
}
```

**When to use**: Object types with properties

### 2. Use `type` for Unions, Intersections, or Aliases

```typescript
export type TaskStatus = "pending" | "completed";
export type TaskPriority = "low" | "medium" | "high";
```

**When to use**: Union types, intersections, or type aliases

### 3. Use Generic Types for Reusable Structures

```typescript
export interface ApiResponse<T = unknown> {
  data?: T;
  success: boolean;
}
```

**When to use**: Reusable structures that work with different types

### 4. Mark Optional Properties with `?`

```typescript
export interface Task {
  title: string;        // Required
  description?: string; // Optional
}
```

**When to use**: Fields that may not exist

## Complete Example: Adding New Types

### Step 1: Define Entity Type (matches backend)

```typescript
export interface Category {
  id: number;
  user_id: string;
  name: string;
  color?: string;
  created_at: string;
  updated_at: string;
}
```

### Step 2: Define Form Data Type (for user input)

```typescript
export interface CategoryFormData {
  name: string;
  color?: string;
}
```

### Step 3: Define Query Parameters Type (for API queries)

```typescript
export interface CategoryQueryParams {
  search?: string;
  page?: number;
  limit?: number;
}
```

### Step 4: Use in API Client

```typescript
async getCategories(
  userId: string,
  queryParams?: CategoryQueryParams
): Promise<ApiResponse<PaginatedResponse<Category>>> {
  // Implementation
}
```

## Constitution Requirements

- **FR-030**: Typed TypeScript interfaces for all API calls ✅
- **FR-037**: TypeScript strict mode ✅

## References

- **Specification**: `specs/002-frontend-todo-app/spec.md` - Entity definitions
- **Plan**: `specs/002-frontend-todo-app/plan.md` - API contracts with types
- **Types File**: `frontend/types/index.ts` - Complete type definitions

## Common Patterns Summary

1. ✅ Use `interface` for object types
2. ✅ Use `type` for union types (string literals)
3. ✅ Use generic types `<T>` for reusable structures
4. ✅ Mark optional fields with `?`
5. ✅ Match backend field names (snake_case for API responses)
6. ✅ Use camelCase for form data types
7. ✅ Create separate types for form data and query parameters
8. ✅ Use descriptive names (EntityFormData, EntityQueryParams)
9. ✅ Include all required fields from backend
10. ✅ Provide default type parameters for generics (`<T = unknown>`)

