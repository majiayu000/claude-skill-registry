---
name: api-designer
description: This skill should be used when the user mentions "API design", "TypeScript API", "type-safe API", "endpoint design", "API validation", "Zod", discusses creating APIs, type safety, error handling, or API architecture. Addresses designing clean, type-safe APIs with validation, error handling, and documentation.
version: 1.0.0
---

# TypeScript API Design

Comprehensive guide to designing type-safe APIs with TypeScript. Covers type-safe contracts, validation with Zod, Result types for error handling, SvelteKit endpoints, middleware patterns, and API versioning.

---

## When This Skill Applies

Use this skill when:
- Designing API endpoints
- Creating type-safe API contracts
- Implementing validation
- Handling API errors
- Building SvelteKit API routes
- Creating reusable middleware
- Versioning APIs
- Questions about API design patterns

---

## Type-Safe Contracts

### Request/Response Types
```typescript
// types/api.ts
export interface CreateUserRequest {
	email: string;
	name: string;
	password: string;
}

export interface User {
	id: string;
	email: string;
	name: string;
	createdAt: string;
}

export interface ApiError {
	code: string;
	message: string;
	details?: Record<string, string[]>;
}
```

**Key principle**: Types ARE documentation. Well-named types with clear structure tell the story.

### Result Type Pattern
```typescript
// For expected failures (not found, validation, etc.)
export type Result<T, E = string> =
	| { success: true; data: T }
	| { success: false; error: E };

// Usage
function findUser(id: string): Result<User, 'not_found'> {
	const user = db.findUser(id);
	if (!user) {
		return { success: false, error: 'not_found' };
	}
	return { success: true, data: user };
}

// Consuming
const result = findUser('123');
if (result.success) {
	console.log(result.data.email); // Type-safe access
} else {
	console.error('Error:', result.error);
}
```

### API Response Format
```typescript
// Standard success response
export interface ApiSuccess<T> {
	success: true;
	data: T;
}

// Standard error response
export interface ApiError {
	success: false;
	error: {
		code: string;
		message: string;
		details?: Record<string, string[]>;
	};
}

export type ApiResponse<T> = ApiSuccess<T> | ApiError;
```

### Endpoint Type Map
```typescript
// Optional: Define all endpoints in one place
export interface ApiEndpoints {
	'POST /api/users': {
		request: CreateUserRequest;
		response: User;
	};
	'GET /api/users/:id': {
		params: { id: string };
		response: User;
	};
	'PATCH /api/users/:id': {
		params: { id: string };
		request: Partial<UpdateUserRequest>;
		response: User;
	};
	'DELETE /api/users/:id': {
		params: { id: string };
		response: null;
	};
}
```

---

## Validation with Zod

### Why Zod

- TypeScript-first (infers types from schemas)
- Works client/server/shared
- Composable schemas
- Excellent error messages
- Incremental adoption (add as needed)

### Basic Schema
```typescript
import { z } from 'zod';

export const CreateUserSchema = z.object({
	email: z.string().email(),
	name: z.string().min(2).max(100),
	password: z.string().min(8)
});

// Type automatically inferred!
export type CreateUserRequest = z.infer<typeof CreateUserSchema>;
```

### Complex Validation
```typescript
export const UpdateUserSchema = z.object({
	email: z.string().email().optional(),
	name: z.string().min(2).max(100).optional(),
	age: z.number().int().min(18).max(120).optional(),
	preferences: z.object({
		theme: z.enum(['light', 'dark']),
		notifications: z.boolean(),
		language: z.string().length(2) // ISO 639-1
	}).optional()
}).refine(
	(data) => Object.keys(data).length > 0,
	{ message: 'At least one field must be provided' }
);
```

### Custom Validation Rules
```typescript
export const PasswordSchema = z.string()
	.min(8, 'Password must be at least 8 characters')
	.regex(/[A-Z]/, 'Must contain uppercase letter')
	.regex(/[a-z]/, 'Must contain lowercase letter')
	.regex(/[0-9]/, 'Must contain number')
	.regex(/[^A-Za-z0-9]/, 'Must contain special character');

export const StrongPasswordSchema = z.object({
	password: PasswordSchema,
	confirmPassword: z.string()
}).refine(
	(data) => data.password === data.confirmPassword,
	{ message: 'Passwords must match', path: ['confirmPassword'] }
);
```

### Nested Schemas
```typescript
const AddressSchema = z.object({
	street: z.string(),
	city: z.string(),
	country: z.string(),
	postalCode: z.string()
});

const UserSchema = z.object({
	name: z.string(),
	email: z.string().email(),
	address: AddressSchema,
	billingAddress: AddressSchema.optional()
});

type User = z.infer<typeof UserSchema>;
```

### Schema Composition
```typescript
// Base user fields
const BaseUserSchema = z.object({
	email: z.string().email(),
	name: z.string()
});

// Create adds password
const CreateUserSchema = BaseUserSchema.extend({
	password: PasswordSchema
});

// Update makes everything optional
const UpdateUserSchema = BaseUserSchema.partial();
```

---

## Error Handling Patterns

### Result Types (Expected Failures)
```typescript
// For operations that may legitimately fail
export type Result<T, E = string> =
	| { success: true; data: T }
	| { success: false; error: E };

// Usage in business logic
function findUser(id: string): Result<User, 'not_found' | 'invalid_id'> {
	if (!isValidId(id)) {
		return { success: false, error: 'invalid_id' };
	}

	const user = db.findUser(id);
	if (!user) {
		return { success: false, error: 'not_found' };
	}

	return { success: true, data: user };
}
```

### Error Classes (Unexpected Failures)
```typescript
// For exceptional cases that should be thrown
export class ApiError extends Error {
	constructor(
		public code: string,
		message: string,
		public statusCode: number = 500,
		public details?: Record<string, string[]>
	) {
		super(message);
		this.name = 'ApiError';
	}
}

export class ValidationError extends ApiError {
	constructor(details: Record<string, string[]>) {
		super('VALIDATION_ERROR', 'Validation failed', 400, details);
	}
}

export class NotFoundError extends ApiError {
	constructor(resource: string) {
		super('NOT_FOUND', `${resource} not found`, 404);
	}
}

export class UnauthorizedError extends ApiError {
	constructor(message = 'Authentication required') {
		super('UNAUTHORIZED', message, 401);
	}
}

export class ConflictError extends ApiError {
	constructor(message: string) {
		super('CONFLICT', message, 409);
	}
}
```

### When to Use Each

**Result Types** - Expected failures:
- User not found
- Validation failures
- Business rule violations
- Resource conflicts

**Error Classes** - Exceptional cases:
- Database connection failures
- Configuration errors
- Invalid application state
- Unexpected system errors

### Centralized Error Handler
```typescript
// lib/server/errors.ts
import { json } from '@sveltejs/kit';
import { ZodError } from 'zod';

export function handleApiError(error: unknown) {
	// Zod validation errors
	if (error instanceof ZodError) {
		return json({
			success: false,
			error: {
				code: 'VALIDATION_ERROR',
				message: 'Validation failed',
				details: error.flatten().fieldErrors
			}
		}, { status: 400 });
	}

	// Custom API errors
	if (error instanceof ApiError) {
		return json({
			success: false,
			error: {
				code: error.code,
				message: error.message,
				details: error.details
			}
		}, { status: error.statusCode });
	}

	// Unknown errors - don't expose details
	console.error('Unexpected error:', error);
	return json({
		success: false,
		error: {
			code: 'INTERNAL_ERROR',
			message: 'An unexpected error occurred'
		}
	}, { status: 500 });
}
```

---

## SvelteKit API Routes

### Basic GET Endpoint
```typescript
// src/routes/api/users/+server.ts
import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ url }) => {
	const limit = parseInt(url.searchParams.get('limit') || '10');
	const offset = parseInt(url.searchParams.get('offset') || '0');

	const users = await db.users.findMany(limit, offset);
	const total = await db.users.count();

	return json({
		success: true,
		data: {
			users,
			total,
			limit,
			offset
		}
	});
};
```

### POST with Validation
```typescript
// src/routes/api/users/+server.ts
import { json } from '@sveltejs/kit';
import { CreateUserSchema } from '$lib/schemas';
import { handleApiError } from '$lib/server/errors';
import type { RequestHandler } from './$types';

export const POST: RequestHandler = async ({ request }) => {
	try {
		const body = await request.json();

		// Validate with Zod
		const data = CreateUserSchema.parse(body);

		// Business logic
		const user = await createUser(data);

		return json({
			success: true,
			data: user
		}, { status: 201 });

	} catch (error) {
		return handleApiError(error);
	}
};
```

### Dynamic Route Parameters
```typescript
// src/routes/api/users/[id]/+server.ts
import { json, error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ params }) => {
	const result = await findUser(params.id);

	if (!result.success) {
		throw error(404, 'User not found');
	}

	return json({
		success: true,
		data: result.data
	});
};

export const PATCH: RequestHandler = async ({ params, request }) => {
	try {
		const body = await request.json();
		const data = UpdateUserSchema.parse(body);

		const user = await updateUser(params.id, data);

		return json({
			success: true,
			data: user
		});

	} catch (error) {
		return handleApiError(error);
	}
};

export const DELETE: RequestHandler = async ({ params }) => {
	await deleteUser(params.id);

	return new Response(null, { status: 204 });
};
```

---

## Middleware Patterns

**Key principle**: Middleware are reusable functions for cross-cutting concerns.

### Authentication Middleware
```typescript
// lib/server/middleware/auth.ts
import { error } from '@sveltejs/kit';
import type { RequestEvent } from '@sveltejs/kit';

export async function requireAuth(event: RequestEvent): Promise<User> {
	const session = event.cookies.get('session');

	if (!session) {
		throw error(401, 'Authentication required');
	}

	const user = await verifySession(session);

	if (!user) {
		throw error(401, 'Invalid session');
	}

	return user;
}

// Usage
export const GET: RequestHandler = async (event) => {
	const user = await requireAuth(event);
	// Now we know user is authenticated
	const data = await getUserData(user.id);
	return json({ success: true, data });
};
```

### Validation Middleware
```typescript
// lib/server/middleware/validate.ts
import { type z } from 'zod';
import { handleApiError } from '$lib/server/errors';

export async function validateRequest<T extends z.ZodType>(
	request: Request,
	schema: T
): Promise<z.infer<T>> {
	const body = await request.json();
	return schema.parse(body); // Throws ZodError if invalid
}

// Usage
export const POST: RequestHandler = async ({ request }) => {
	try {
		const data = await validateRequest(request, CreateUserSchema);
		// data is fully typed as CreateUserRequest!

		const user = await createUser(data);
		return json({ success: true, data: user });

	} catch (error) {
		return handleApiError(error);
	}
};
```

### Rate Limiting Middleware

**Note**: Simple in-memory pattern for learning/development. Production apps should use Redis or external service.
```typescript
// lib/server/middleware/rateLimit.ts
const rateLimits = new Map<string, { count: number; resetAt: number }>();

export function checkRateLimit(
	key: string,
	maxRequests: number = 10,
	windowMs: number = 60000 // 1 minute
): boolean {
	const now = Date.now();
	const limit = rateLimits.get(key);

	if (!limit || now > limit.resetAt) {
		rateLimits.set(key, {
			count: 1,
			resetAt: now + windowMs
		});
		return true;
	}

	if (limit.count >= maxRequests) {
		return false;
	}

	limit.count++;
	return true;
}

// Usage
export const POST: RequestHandler = async ({ request, getClientAddress }) => {
	const ip = getClientAddress();

	if (!checkRateLimit(ip, 10, 60000)) {
		throw error(429, 'Too many requests');
	}

	// Continue with request
};
```

### Composing Middleware
```typescript
// lib/server/middleware/compose.ts
export async function withMiddleware<T>(
	event: RequestEvent,
	...middlewares: Array<(event: RequestEvent) => Promise<any>>
): Promise<T[]> {
	const results = [];
	for (const middleware of middlewares) {
		results.push(await middleware(event));
	}
	return results as T[];
}

// Usage
export const POST: RequestHandler = async (event) => {
	const [user, data] = await withMiddleware<[User, CreatePostRequest]>(
		event,
		requireAuth,
		(e) => validateRequest(e.request, CreatePostSchema)
	);

	const post = await createPost(user.id, data);
	return json({ success: true, data: post });
};
```

---

## Session Management Patterns

### Pattern 1: SvelteKit Cookies (Simple Apps)
```typescript
// lib/server/auth/cookies.ts
import type { Cookies } from '@sveltejs/kit';

export function createSession(cookies: Cookies, userId: string) {
	const sessionId = generateSessionId();

	cookies.set('session', sessionId, {
		path: '/',
		httpOnly: true,
		secure: true,
		sameSite: 'strict',
		maxAge: 60 * 60 * 24 * 7 // 1 week
	});

	// Store session in database
	await db.sessions.create({ sessionId, userId });
}

export async function getSession(cookies: Cookies): Promise<User | null> {
	const sessionId = cookies.get('session');
	if (!sessionId) return null;

	const session = await db.sessions.findUnique(sessionId);
	if (!session) return null;

	return await db.users.findUnique(session.userId);
}

export function clearSession(cookies: Cookies) {
	cookies.delete('session', { path: '/' });
}
```

**When to use**: Simple apps, server-rendered, no mobile apps.

### Pattern 2: JWT Tokens (Stateless APIs)
```typescript
// lib/server/auth/jwt.ts
import jwt from 'jsonwebtoken';

const SECRET = process.env.JWT_SECRET!;

export function createToken(userId: string): string {
	return jwt.sign(
		{ userId },
		SECRET,
		{ expiresIn: '7d' }
	);
}

export function verifyToken(token: string): { userId: string } | null {
	try {
		return jwt.verify(token, SECRET) as { userId: string };
	} catch {
		return null;
	}
}

// Middleware
export async function requireJwt(event: RequestEvent): Promise<User> {
	const auth = event.request.headers.get('Authorization');
	if (!auth?.startsWith('Bearer ')) {
		throw error(401, 'Missing token');
	}

	const token = auth.slice(7);
	const payload = verifyToken(token);

	if (!payload) {
		throw error(401, 'Invalid token');
	}

	const user = await db.users.findUnique(payload.userId);
	if (!user) {
		throw error(401, 'User not found');
	}

	return user;
}
```

**When to use**: Stateless APIs, mobile apps, microservices.

### Pattern 3: Supabase Auth (Full-Featured)
```typescript
// lib/server/auth/supabase.ts
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
	process.env.SUPABASE_URL!,
	process.env.SUPABASE_SERVICE_KEY!
);

export async function requireSupabaseAuth(event: RequestEvent): Promise<User> {
	const token = event.request.headers.get('Authorization')?.slice(7);

	if (!token) {
		throw error(401, 'Missing token');
	}

	const { data: { user }, error: authError } = await supabase.auth.getUser(token);

	if (authError || !user) {
		throw error(401, 'Invalid token');
	}

	return user;
}
```

**When to use**: Need OAuth, email verification, password reset, etc.

---

## Database Layer (Typed Wrappers)

**Principle**: No universal ORM for polyglot persistence. Use native clients with typed wrappers.

### PostgreSQL/Supabase Wrapper
```typescript
// lib/db/users.ts
import { supabase } from '$lib/server/supabase';

export interface CreateUserData {
	email: string;
	name: string;
	passwordHash: string;
}

export interface UpdateUserData {
	email?: string;
	name?: string;
}

export async function createUser(data: CreateUserData): Promise<User> {
	const { data: user, error } = await supabase
		.from('users')
		.insert(data)
		.select()
		.single();

	if (error) throw new Error(error.message);
	return user;
}

export async function findUser(id: string): Promise<User | null> {
	const { data: user } = await supabase
		.from('users')
		.select()
		.eq('id', id)
		.single();

	return user;
}

export async function updateUser(
	id: string,
	data: UpdateUserData
): Promise<User> {
	const { data: user, error } = await supabase
		.from('users')
		.update(data)
		.eq('id', id)
		.select()
		.single();

	if (error) throw new Error(error.message);
	return user;
}
```

### Neo4j Wrapper
```typescript
// lib/db/graph.ts
import { neo4j } from '$lib/server/neo4j';

export async function createFollowRelationship(
	followerId: string,
	followedId: string
): Promise<void> {
	await neo4j.run(`
		MATCH (a:User {id: $followerId})
		MATCH (b:User {id: $followedId})
		MERGE (a)-[:FOLLOWS {since: datetime()}]->(b)
	`, { followerId, followedId });
}

export async function getFollowers(userId: string): Promise<User[]> {
	const result = await neo4j.run(`
		MATCH (follower:User)-[:FOLLOWS]->(u:User {id: $userId})
		RETURN follower
	`, { userId });

	return result.records.map(r => r.get('follower').properties);
}

export async function getSuggestedFollows(
	userId: string,
	limit: number = 10
): Promise<User[]> {
	const result = await neo4j.run(`
		MATCH (u:User {id: $userId})-[:FOLLOWS]->()-[:FOLLOWS]->(suggestion:User)
		WHERE NOT (u)-[:FOLLOWS]->(suggestion)
		  AND u <> suggestion
		RETURN DISTINCT suggestion
		LIMIT $limit
	`, { userId, limit });

	return result.records.map(r => r.get('suggestion').properties);
}
```

---

## API Versioning

**Recommended approach**: URL-based versioning

### Directory Structure
```
src/routes/api/
├── v1/
│   ├── users/
│   │   └── +server.ts
│   └── posts/
│       └── +server.ts
└── v2/
    ├── users/
    │   ├── +server.ts
    │   └── [id]/+server.ts
    └── posts/
        └── +server.ts
```

### Version-Specific Types
```typescript
// types/api/v1.ts
export interface UserV1 {
	id: string;
	name: string;
}

// types/api/v2.ts
export interface UserV2 {
	id: string;
	name: string;
	email: string;      // Added in v2
	createdAt: string;  // Added in v2
}
```

### Shared Business Logic
```typescript
// lib/services/users.ts
import type { UserV1, UserV2 } from '$lib/types/api';

export async function getUserById(id: string): Promise<User> {
	// Single source of truth
	return await db.users.findUnique(id);
}

// Transform for v1
export function toUserV1(user: User): UserV1 {
	return {
		id: user.id,
		name: user.name
	};
}

// Transform for v2
export function toUserV2(user: User): UserV2 {
	return {
		id: user.id,
		name: user.name,
		email: user.email,
		createdAt: user.createdAt
	};
}
```

### Version-Specific Endpoints
```typescript
// src/routes/api/v1/users/[id]/+server.ts
import { toUserV1 } from '$lib/services/users';

export const GET: RequestHandler = async ({ params }) => {
	const user = await getUserById(params.id);
	return json({
		success: true,
		data: toUserV1(user) // v1 format
	});
};

// src/routes/api/v2/users/[id]/+server.ts
import { toUserV2 } from '$lib/services/users';

export const GET: RequestHandler = async ({ params }) => {
	const user = await getUserById(params.id);
	return json({
		success: true,
		data: toUserV2(user) // v2 format
	});
};
```

### When to Version

**Create new version when**:
- Breaking changes to existing endpoints
- Removing fields
- Changing field types
- Changing behavior significantly

**Don't version for**:
- Adding optional fields (backward compatible)
- New endpoints
- Bug fixes
- Performance improvements

---

## Type-Safe API Client

**Pattern**: Create typed wrapper functions for consuming your API.

### Basic Client
```typescript
// lib/api/client.ts
export class ApiClient {
	constructor(private baseUrl: string = '') {}

	private async request<T>(
		method: string,
		endpoint: string,
		data?: any
	): Promise<T> {
		const response = await fetch(`${this.baseUrl}${endpoint}`, {
			method,
			headers: {
				'Content-Type': 'application/json'
			},
			body: data ? JSON.stringify(data) : undefined
		});

		const json = await response.json();

		if (!json.success) {
			throw new ApiError(
				json.error.code,
				json.error.message,
				response.status,
				json.error.details
			);
		}

		return json.data;
	}

	get<T>(endpoint: string): Promise<T> {
		return this.request<T>('GET', endpoint);
	}

	post<T>(endpoint: string, data: any): Promise<T> {
		return this.request<T>('POST', endpoint, data);
	}

	patch<T>(endpoint: string, data: any): Promise<T> {
		return this.request<T>('PATCH', endpoint, data);
	}

	delete(endpoint: string): Promise<void> {
		return this.request<void>('DELETE', endpoint);
	}
}
```

### Type-Safe API Methods
```typescript
// lib/api/users.ts
import { ApiClient } from './client';
import type { CreateUserRequest, User, UpdateUserRequest } from '$lib/types/api';

export class UsersApi {
	constructor(private client: ApiClient) {}

	create(data: CreateUserRequest): Promise<User> {
		return this.client.post<User>('/api/users', data);
	}

	get(id: string): Promise<User> {
		return this.client.get<User>(`/api/users/${id}`);
	}

	update(id: string, data: UpdateUserRequest): Promise<User> {
		return this.client.patch<User>(`/api/users/${id}`, data);
	}

	delete(id: string): Promise<void> {
		return this.client.delete(`/api/users/${id}`);
	}

	list(params: { limit?: number; offset?: number } = {}): Promise<User[]> {
		const query = new URLSearchParams(
			Object.entries(params)
				.filter(([_, v]) => v !== undefined)
				.map(([k, v]) => [k, String(v)])
		);

		return this.client.get<User[]>(`/api/users?${query}`);
	}
}

// Main API object
export const api = {
	users: new UsersApi(new ApiClient())
};
```

### Usage (Fully Typed!)
```typescript
import { api } from '$lib/api';

// TypeScript knows CreateUserRequest shape
const user = await api.users.create({
	email: 'alice@example.com',
	name: 'Alice',
	password: 'secure123'
});

// TypeScript knows user is User type
console.log(user.email); // ✓ Type-safe
console.log(user.invalidField); // ✗ TypeScript error

// List users with typed params
const users = await api.users.list({ limit: 10, offset: 0 });
```

---

## Optional: OpenAPI Generation

**Using zod-to-openapi** (much easier than manual Swagger)

### Setup
```bash
npm install zod-openapi @asteasolutions/zod-to-openapi
```

### Extend Schemas with OpenAPI Metadata
```typescript
// lib/schemas/users.ts
import { z } from 'zod';
import { extendZodWithOpenApi } from '@asteasolutions/zod-to-openapi';

extendZodWithOpenApi(z);

export const CreateUserSchema = z.object({
	email: z.string().email().openapi({
		example: 'alice@example.com',
		description: 'User email address'
	}),
	name: z.string().min(2).openapi({
		example: 'Alice Smith'
	}),
	password: z.string().min(8).openapi({
		example: 'SecurePass123!',
		description: 'Minimum 8 characters'
	})
}).openapi('CreateUserRequest');

export const UserSchema = z.object({
	id: z.string().uuid(),
	email: z.string().email(),
	name: z.string(),
	createdAt: z.string().datetime()
}).openapi('User');
```

### Generate OpenAPI Spec
```typescript
// scripts/generateOpenApi.ts
import { OpenAPIRegistry, OpenApiGeneratorV3 } from '@asteasolutions/zod-to-openapi';
import { CreateUserSchema, UserSchema } from '../src/lib/schemas/users';

const registry = new OpenAPIRegistry();

// Register schemas
registry.register('CreateUserRequest', CreateUserSchema);
registry.register('User', UserSchema);

// Register paths
registry.registerPath({
	method: 'post',
	path: '/api/users',
	request: {
		body: {
			content: {
				'application/json': {
					schema: CreateUserSchema
				}
			}
		}
	},
	responses: {
		201: {
			description: 'User created',
			content: {
				'application/json': {
					schema: UserSchema
				}
			}
		}
	}
});

const generator = new OpenApiGeneratorV3(registry.definitions);

const docs = generator.generateDocument({
	openapi: '3.0.0',
	info: {
		title: 'My API',
		version: '1.0.0'
	}
});

console.log(JSON.stringify(docs, null, 2));
```

---

## Testing APIs

### Testing Endpoints
```typescript
// src/routes/api/users/+server.test.ts
import { describe, it, expect, vi } from 'vitest';
import { POST } from './+server';

describe('POST /api/users', () => {
	it('should create user with valid data', async () => {
		const request = new Request('http://localhost/api/users', {
			method: 'POST',
			body: JSON.stringify({
				email: 'test@example.com',
				name: 'Test User',
				password: 'password123'
			})
		});

		const response = await POST({ request } as any);
		const data = await response.json();

		expect(response.status).toBe(201);
		expect(data.success).toBe(true);
		expect(data.data).toHaveProperty('id');
		expect(data.data.email).toBe('test@example.com');
	});

	it('should reject invalid email', async () => {
		const request = new Request('http://localhost/api/users', {
			method: 'POST',
			body: JSON.stringify({
				email: 'invalid-email',
				name: 'Test',
				password: 'password123'
			})
		});

		const response = await POST({ request } as any);
		const data = await response.json();

		expect(response.status).toBe(400);
		expect(data.success).toBe(false);
		expect(data.error.code).toBe('VALIDATION_ERROR');
	});

	it('should reject short password', async () => {
		const request = new Request('http://localhost/api/users', {
			method: 'POST',
			body: JSON.stringify({
				email: 'test@example.com',
				name: 'Test',
				password: '123'
			})
		});

		const response = await POST({ request } as any);
		const data = await response.json();

		expect(response.status).toBe(400);
		expect(data.error.details).toHaveProperty('password');
	});
});
```

### Testing Business Logic
```typescript
// lib/services/users.test.ts
import { describe, it, expect } from 'vitest';
import { createUser, findUser } from './users';

describe('createUser', () => {
	it('should create user successfully', async () => {
		const data = {
			email: 'test@example.com',
			name: 'Test User',
			passwordHash: 'hashed'
		};

		const user = await createUser(data);

		expect(user).toHaveProperty('id');
		expect(user.email).toBe(data.email);
		expect(user.name).toBe(data.name);
	});
});

describe('findUser', () => {
	it('should return null for non-existent user', async () => {
		const user = await findUser('non-existent-id');
		expect(user).toBeNull();
	});

	it('should return user when exists', async () => {
		const created = await createUser({
			email: 'test@example.com',
			name: 'Test',
			passwordHash: 'hashed'
		});

		const found = await findUser(created.id);
		expect(found).not.toBeNull();
		expect(found?.id).toBe(created.id);
	});
});
```

---

## Best Practices

### 1. Always Validate Input
```typescript
// ✓ Good - validate with Zod
const data = CreateUserSchema.parse(input);
const user = await createUser(data);

// ✗ Bad - trusting client input
const user = await createUser(input);
```

### 2. Use Result Types for Expected Failures
```typescript
// ✓ Good - Result type for expected failure
function findUser(id: string): Result<User, 'not_found'> {
	const user = db.findUser(id);
	if (!user) {
		return { success: false, error: 'not_found' };
	}
	return { success: true, data: user };
}

// ✗ Bad - throwing for expected case
function findUser(id: string): User {
	const user = db.findUser(id);
	if (!user) throw new Error('Not found');
	return user;
}
```

### 3. Throw Error Classes for Unexpected Failures
```typescript
// ✓ Good - throw for exceptional case
async function connectDatabase(): Promise<Database> {
	try {
		return await connect();
	} catch (error) {
		throw new DatabaseError('Failed to connect');
	}
}

// ✗ Bad - Result type for exceptional case
async function connectDatabase(): Result<Database, string> {
	// Database connection should succeed or crash
}
```

### 4. Type Everything Explicitly
```typescript
// ✓ Good - explicit types
interface CreateUserRequest {
	email: string;
	name: string;
}

async function createUser(data: CreateUserRequest): Promise<User> {
	// ...
}

// ✗ Bad - implicit any
async function createUser(data): Promise<any> {
	// ...
}
```

### 5. Separate Concerns (Layered Architecture)
```typescript
// ✓ Good - separated layers

// Handler (thin, delegates to service)
export const POST: RequestHandler = async ({ request }) => {
	const data = await validateRequest(request, CreateUserSchema);
	const user = await createUser(data);
	return json({ success: true, data: user }, { status: 201 });
};

// Service (business logic)
async function createUser(data: CreateUserRequest): Promise<User> {
	const passwordHash = await hashPassword(data.password);
	return await db.users.create({ ...data, passwordHash });
}

// ✗ Bad - everything in handler
export const POST: RequestHandler = async ({ request }) => {
	const body = await request.json();
	// validation, hashing, database, all mixed together
};
```

### 6. Use Middleware for Cross-Cutting Concerns
```typescript
// ✓ Good - reusable middleware
export const POST: RequestHandler = async (event) => {
	const user = await requireAuth(event);
	const data = await validateRequest(event.request, CreatePostSchema);
	const post = await createPost(user.id, data);
	return json({ success: true, data: post });
};

// ✗ Bad - repeating auth/validation everywhere
export const POST: RequestHandler = async ({ request, cookies }) => {
	// Repeated auth code
	const session = cookies.get('session');
	if (!session) throw error(401);
	const user = await verifySession(session);

	// Repeated validation code
	const body = await request.json();
	if (!body.title) throw error(400);
	// ...
};
```

### 7. Document with Types, Not Comments
```typescript
// ✓ Good - type tells the story
interface CreateUserRequest {
	email: string;          // Type is clear
	name: string;           // Type is clear
	password: string;       // Min 8 chars (Zod enforces)
}

// ✗ Bad - relying on comments
interface CreateUserRequest {
	email: string;          // Must be valid email
	name: string;           // Required, 2-100 chars
	password: string;       // Min 8, uppercase, lowercase, number, special
}
// Comments get out of sync with code!
```

---

## Privacy-by-Default Patterns

### Principle

APIs should collect, expose, and store the minimum data needed. Privacy is a design constraint, not an afterthought.

### Response Filtering
```typescript
// ✗ Bad: Returning everything from the database
export const GET: RequestHandler = async ({ params }) => {
	const user = await db.users.findUnique(params.id);
	return json({ success: true, data: user }); // Exposes internal fields
};

// ✓ Good: Explicit response shaping
export const GET: RequestHandler = async ({ params }) => {
	const user = await db.users.findUnique(params.id);
	return json({
		success: true,
		data: {
			id: user.id,
			name: user.name,
			avatarUrl: user.avatarUrl
			// No email, no internal IDs, no metadata
		}
	});
};
```

### Request Minimisation
```typescript
// ✗ Bad: Collecting data you don't need
const SignupSchema = z.object({
	email: z.string().email(),
	name: z.string(),
	phone: z.string(),        // Do you actually need this?
	dateOfBirth: z.string(),   // Do you actually need this?
	address: z.string(),       // Do you actually need this?
});

// ✓ Good: Collect only what's required for the feature
const SignupSchema = z.object({
	email: z.string().email(),
	name: z.string(),
});
```

### Sensitive Data Handling
```typescript
// Never log sensitive data
function logApiRequest(req: Request, body: unknown) {
	const sanitised = { ...body };
	delete sanitised.password;
	delete sanitised.token;
	delete sanitised.creditCard;
	console.log('API request:', sanitised);
}

// Never expose internal IDs unnecessarily
// Use public-facing slugs or UUIDs, not sequential database IDs
```

### Auth Scoping
```typescript
// ✗ Bad: Endpoint returns all users' data
export const GET: RequestHandler = async () => {
	const users = await db.users.findMany();
	return json({ success: true, data: users });
};

// ✓ Good: Scoped to authenticated user's data
export const GET: RequestHandler = async (event) => {
	const user = await requireAuth(event);
	const data = await db.users.findByOrganisation(user.organisationId);
	return json({ success: true, data });
};
```

### Data Deletion
```typescript
// Provide clear deletion endpoints
export const DELETE: RequestHandler = async (event) => {
	const user = await requireAuth(event);

	// Delete user data across all stores
	await db.users.delete(user.id);
	await neo4j.run('MATCH (u:User {id: $id}) DETACH DELETE u', { id: user.id });
	await mongo.collection('preferences').deleteOne({ _id: user.id });

	return new Response(null, { status: 204 });
};
```

---

## Success Criteria

API design is well-structured when:
- All requests/responses explicitly typed
- Input validated with Zod schemas
- Expected failures use Result types
- Unexpected failures throw Error classes
- Endpoints follow REST conventions
- Middleware reusable and composable
- Database layer has typed wrappers
- Authentication consistent across endpoints
- Errors have standardised format
- Type-safe client available for consumption
- Tests cover happy path and error cases
- Code is maintainable and follows patterns
- Responses expose minimum necessary data (privacy-by-default)
- No sensitive data logged or leaked
- Auth scoping prevents cross-user data access
- Data deletion is supported and complete
