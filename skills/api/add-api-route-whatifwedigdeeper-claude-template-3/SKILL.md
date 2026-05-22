---
skill: add-api-route
description: Create Next.js API route with validation and error handling
arguments: route name and HTTP methods
---

# Add API Route: $ARGUMENTS

Create a Next.js API route with proper validation, error handling, and types.

## Process

### 1. Determine Route Structure

Parse arguments to determine:
- Route path (e.g., `users`, `posts/[id]`)
- HTTP methods (GET, POST, PUT, DELETE)
- Dynamic segments if any

### 2. Create Route File

**App Router (Next.js 13+):**
```
app/api/[route]/route.ts
```

**Pages Router:**
```
pages/api/[route].ts
```

### 3. Generate Route Handler

**App Router template:**

```typescript
import { NextRequest, NextResponse } from 'next/server';

// Types
interface RequestBody {
  // define expected body shape
}

interface ResponseData {
  // define response shape
}

// GET handler
export async function GET(request: NextRequest) {
  try {
    // Implementation
    return NextResponse.json({ data: [] });
  } catch (error) {
    console.error('GET error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

// POST handler
export async function POST(request: NextRequest) {
  try {
    const body: RequestBody = await request.json();

    // Validate
    if (!body.requiredField) {
      return NextResponse.json(
        { error: 'Missing required field' },
        { status: 400 }
      );
    }

    // Implementation
    return NextResponse.json({ success: true }, { status: 201 });
  } catch (error) {
    console.error('POST error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

### 4. Add Type Definitions

Add to `types/api.ts` or `types/index.ts`:

```typescript
export interface [Route]Request {
  // request body type
}

export interface [Route]Response {
  // response type
}
```

### 5. Create Tests

```typescript
// __tests__/api/[route].test.ts
describe('API /api/[route]', () => {
  test('GET returns data', async () => {
    const response = await fetch('/api/[route]');
    expect(response.status).toBe(200);
  });

  test('POST validates input', async () => {
    const response = await fetch('/api/[route]', {
      method: 'POST',
      body: JSON.stringify({}),
    });
    expect(response.status).toBe(400);
  });
});
```

### 6. Validate

```bash
npm run build
npm test
```

## Patterns

**Dynamic route:** `app/api/users/[id]/route.ts`

**Nested route:** `app/api/posts/[postId]/comments/route.ts`

**With middleware:** Add validation/auth in route or middleware.ts
