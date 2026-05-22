---
name: api-spec-analyzer
description: Analyzes API documentation from OpenAPI specs to provide TypeScript interfaces, request/response formats, and implementation guidance. Use when implementing API integrations, debugging API errors (400, 401, 404), replacing mock APIs, verifying data types, or when user mentions endpoints, API calls, or backend integration.
---

# API Specification Analyzer

This Skill analyzes OpenAPI specifications to provide accurate API documentation, TypeScript interfaces, and implementation guidance for the caremaster-tenant-frontend project.

## When to use this Skill

Claude should invoke this Skill when:

- User is implementing a new API integration
- User encounters API errors (400 Bad Request, 401 Unauthorized, 404 Not Found, etc.)
- User wants to replace mock API with real backend
- User asks about data types, required fields, or API formats
- User mentions endpoints like "/api/users" or "/api/tenants"
- Before implementing any feature that requires API calls
- When debugging type mismatches between frontend and backend

## Instructions

### Step 1: Fetch API Documentation

Use the MCP server tools to get the OpenAPI specification:

```
mcp__Tenant_Management_Portal_API__read_project_oas_f4bjy4
```

If user requests fresh data or if documentation seems outdated:

```
mcp__Tenant_Management_Portal_API__refresh_project_oas_f4bjy4
```

For referenced schemas (when $ref is used):

```
mcp__Tenant_Management_Portal_API__read_project_oas_ref_resources_f4bjy4
```

### Step 2: Analyze the Specification

Extract the following information for each relevant endpoint:

1. **HTTP Method and Path**: GET /api/users, POST /api/tenants, etc.
2. **Authentication**: Bearer token, API key, etc.
3. **Request Parameters**:
   - Path parameters (e.g., `:id`)
   - Query parameters (e.g., `?page=1&limit=10`)
   - Request body schema
   - Required headers
4. **Response Specification**:
   - Success response structure (200, 201, etc.)
   - Error response formats (400, 401, 404, 500)
   - Status codes and their meanings
5. **Data Types**:
   - Exact types (string, number, boolean, array, object)
   - Format specifications (ISO 8601, UUID, email)
   - Required vs optional fields
   - Enum values and constraints
   - Default values

### Step 3: Generate TypeScript Interfaces

Create ready-to-use TypeScript interfaces that match the API specification exactly:

```typescript
/**
 * User creation input
 * Required fields: email, name, role
 */
export interface UserCreateInput {
	/** User's email address - must be unique */
	email: string
	/** Full name of the user (2-100 characters) */
	name: string
	/** User role - determines access permissions */
	role: "admin" | "manager" | "user"
	/** Account status - defaults to "active" */
	status?: "active" | "inactive"
}

/**
 * User entity returned from API
 */
export interface User {
	/** Unique identifier (UUID format) */
	id: string
	email: string
	name: string
	role: "admin" | "manager" | "user"
	status: "active" | "inactive"
	/** ISO 8601 timestamp */
	createdAt: string
	/** ISO 8601 timestamp */
	updatedAt: string
}
```

### Step 4: Provide Implementation Guidance

#### API Service Pattern

```typescript
// src/api/userApi.ts
export async function createUser(input: UserCreateInput): Promise<User> {
	const response = await fetch("/api/users", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			"Authorization": `Bearer ${getToken()}`,
		},
		body: JSON.stringify(input),
	})

	if (!response.ok) {
		const error = await response.json()
		throw new Error(error.message)
	}

	return response.json()
}
```

#### TanStack Query Hook Pattern

```typescript
// src/hooks/useCreateUser.ts
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { createUser } from "@/api/userApi"
import { userKeys } from "@/lib/queryKeys"
import { toast } from "sonner"

export function useCreateUser() {
	const queryClient = useQueryClient()

	return useMutation({
		mutationFn: createUser,
		onSuccess: (newUser) => {
			// Invalidate queries to refetch updated data
			queryClient.invalidateQueries({ queryKey: userKeys.all() })
			toast.success("User created successfully")
		},
		onError: (error) => {
			toast.error(`Failed to create user: ${error.message}`)
		},
	})
}
```

#### Query Key Pattern

```typescript
// src/lib/queryKeys.ts
export const userKeys = {
	all: () => ["users"] as const,
	lists: () => [...userKeys.all(), "list"] as const,
	list: (filters: UserFilters) => [...userKeys.lists(), filters] as const,
	details: () => [...userKeys.all(), "detail"] as const,
	detail: (id: string) => [...userKeys.details(), id] as const,
}
```

### Step 5: Document Security and Validation

- **OWASP Considerations**: SQL injection, XSS, CSRF protection
- **Input Validation**: Required field validation, format validation
- **Authentication**: Token handling, refresh logic
- **Error Handling**: Proper HTTP status code handling
- **Rate Limiting**: Retry logic, exponential backoff

### Step 6: Provide Test Recommendations

```typescript
// Example test cases based on API spec
describe("createUser", () => {
	it("should create user with valid data", async () => {
		// Test success case
	})

	it("should reject duplicate email", async () => {
		// Test 409 Conflict
	})

	it("should validate email format", async () => {
		// Test 400 Bad Request
	})

	it("should require authentication", async () => {
		// Test 401 Unauthorized
	})
})
```

## Output Format

Provide analysis in this structure:

```markdown
# API Analysis: [Endpoint Name]

## Endpoint Summary
- **Method**: POST
- **Path**: /api/users
- **Authentication**: Bearer token required

## Request Specification

### Path Parameters
None

### Query Parameters
None

### Request Body
[TypeScript interface]

### Required Headers
- Content-Type: application/json
- Authorization: Bearer {token}

## Response Specification

### Success Response (201)
[TypeScript interface]

### Error Responses
- 400: Validation error (duplicate email, invalid format)
- 401: Unauthorized (missing/invalid token)
- 403: Forbidden (insufficient permissions)
- 500: Server error

## Data Type Details
- **email**: string, required, must be valid email format, unique
- **name**: string, required, 2-100 characters
- **role**: enum ["admin", "manager", "user"], required
- **status**: enum ["active", "inactive"], optional, defaults to "active"

## TypeScript Interfaces
[Complete interfaces with JSDoc comments]

## Implementation Guide
[API service + TanStack Query hook examples]

## Security Notes
- Validate email format on client and server
- Hash passwords if handling credentials
- Use HTTPS for all requests
- Store tokens securely (httpOnly cookies recommended)

## Integration Checklist
- [ ] Add types to src/types/
- [ ] Create API service in src/api/
- [ ] Add query keys to src/lib/queryKeys.ts
- [ ] Create hooks in src/hooks/
- [ ] Add error handling with toast notifications
- [ ] Test with Vitest
```

## Project Conventions

### Path Aliases
Always use `@/` path alias:
```typescript
import { User } from "@/types/user"
import { createUser } from "@/api/userApi"
```

### Code Style (Biome)
- Tabs for indentation
- Double quotes
- Semicolons optional (only when needed)
- Line width: 100 characters

### File Organization
```
src/
├── types/           # Domain types
│   └── user.ts
├── api/             # API service functions
│   └── userApi.ts
├── hooks/           # TanStack Query hooks
│   └── useUsers.ts
└── lib/
    └── queryKeys.ts # Query key factories
```

## Common Patterns

### Optimistic Updates
```typescript
onMutate: async (newUser) => {
	// Cancel outgoing queries
	await queryClient.cancelQueries({ queryKey: userKeys.lists() })

	// Snapshot previous value
	const previous = queryClient.getQueryData(userKeys.lists())

	// Optimistically update cache
	queryClient.setQueryData(userKeys.lists(), (old) => [...old, newUser])

	return { previous }
},
onError: (err, newUser, context) => {
	// Rollback on error
	queryClient.setQueryData(userKeys.lists(), context.previous)
},
```

### Pagination
```typescript
export const userKeys = {
	list: (page: number, limit: number) =>
		[...userKeys.lists(), { page, limit }] as const,
}
```

### Search and Filters
```typescript
export interface UserFilters {
	search?: string
	role?: UserRole
	status?: UserStatus
	sortBy?: "name" | "email" | "createdAt"
	sortOrder?: "asc" | "desc"
}

export const userKeys = {
	list: (filters: UserFilters) => [...userKeys.lists(), filters] as const,
}
```

## Error Handling Patterns

### API Service
```typescript
if (!response.ok) {
	const error = await response.json()
	throw new ApiError(error.message, response.status, error.details)
}
```

### Custom Hook
```typescript
onError: (error: ApiError) => {
	if (error.status === 409) {
		toast.error("Email already exists")
	} else if (error.status === 400) {
		toast.error("Invalid data: " + error.details)
	} else {
		toast.error("An error occurred. Please try again.")
	}
}
```

## Quality Checklist

Before providing analysis, ensure:
- ✅ Fetched latest OpenAPI specification
- ✅ Extracted all required/optional fields
- ✅ Documented all possible status codes
- ✅ Created complete TypeScript interfaces
- ✅ Provided working code examples
- ✅ Noted security considerations
- ✅ Aligned with project conventions
- ✅ Included error handling patterns

## Examples

### Example 1: User asks to implement user creation

```
User: "I need to implement user creation"

Claude: [Invokes api-spec-analyzer Skill]
1. Fetches OpenAPI spec for POST /api/users
2. Extracts request/response schemas
3. Generates TypeScript interfaces
4. Provides API service implementation
5. Shows TanStack Query hook example
6. Lists validation requirements
```

### Example 2: User gets 400 error

```
User: "I'm getting a 400 error when creating a tenant"

Claude: [Invokes api-spec-analyzer Skill]
1. Fetches POST /api/tenants specification
2. Identifies required fields and formats
3. Compares user's implementation with spec
4. Points out data type mismatches
5. Provides corrected implementation
```

### Example 3: Replacing mock API

```
User: "Replace mockUserApi with real backend"

Claude: [Invokes api-spec-analyzer Skill]
1. Fetches all /api/users/* endpoints
2. Generates interfaces for all CRUD operations
3. Shows how to implement each API function
4. Maintains same interface as mock API
5. Provides migration checklist
```

## Notes

- Always fetch fresh documentation when user reports API issues
- Quote directly from OpenAPI spec when documenting requirements
- Flag ambiguities or missing information in documentation
- Prioritize type safety - use strict TypeScript types
- Follow existing patterns in the codebase
- Consider OWASP security guidelines
- Provide actionable, copy-paste-ready code
