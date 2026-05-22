---
name: api-new
description: "Create a new Next.js API route with validation, error handling, and TypeScript"
---

# Create New API Route

Create a new Next.js API route following modern best practices for solo developers.

## Requirements

API Endpoint: $ARGUMENTS

## Implementation Guidelines

### 1. **Next.js 15 App Router** (Recommended)
Use Route Handlers in `app/api/` directory with TypeScript

### 2. **Validation**
- Use Zod for runtime type validation
- Validate input early (before DB/API calls)
- Return clear validation error messages

### 3. **Error Handling**
- Global error handling with try/catch
- Consistent error response format
- Appropriate HTTP status codes
- Never expose sensitive error details

### 4. **TypeScript**
- Strict typing for requests/responses
- Shared type definitions
- No `any` types

### 5. **Security**
- Input sanitization
- CORS configuration if needed
- Rate limiting considerations
- Authentication/authorization checks

### 6. **Response Format**
```typescript
// Success
{ data: T, success: true }

// Error
{ error: string, details?: unknown, success: false }
```

## Code Structure

Create a complete API route with:

1. **Route Handler File** - `app/api/[route]/route.ts`
2. **Validation Schema** - Zod schemas for request/response
3. **Type Definitions** - Shared TypeScript types
4. **Error Handler** - Centralized error handling
5. **Example Usage** - Client-side fetch example

## Best Practices to Follow

- Early validation before expensive operations
- Proper HTTP status codes (200, 201, 400, 401, 404, 500)
- Consistent error response format
- TypeScript strict mode
- Minimal logic in routes (use services/utils)
- Environment variable validation
- Request/response logging for debugging
- No sensitive data in responses
- No database queries without validation
- No inline business logic (extract to services)

Generate production-ready code that I can immediately use in my Next.js project.
