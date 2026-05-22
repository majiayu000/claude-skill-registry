---
name: api-route-scaffold
description: Create new Next.js API routes following project patterns. Use when user mentions "new endpoint", "add API", "create route", or "POST/GET handler".
---

# Creating API Routes

This project uses Next.js 16 App Router with a consistent API pattern across all routes.

## Instructions

1. **Create route file**: `app/api/<endpoint-name>/route.ts`

2. **Use this template**:
```typescript
import { NextRequest, NextResponse } from 'next/server';

// CORS headers for cross-origin requests
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

export async function OPTIONS() {
  return NextResponse.json(null, { headers: corsHeaders });
}

export async function POST(req: NextRequest) {
  try {
    const { /* destructure fields */ } = await req.json();

    // Input validation
    if (!requiredField) {
      return NextResponse.json(
        { error: 'Field is required' },
        { status: 400, headers: corsHeaders }
      );
    }

    // Check required environment variables
    const apiKey = process.env.YOUR_API_KEY;
    if (!apiKey) {
      console.error('YOUR_API_KEY is not configured');
      return NextResponse.json(
        { error: 'YOUR_API_KEY is not configured' },
        { status: 500, headers: corsHeaders }
      );
    }

    // Business logic here
    const result = await doSomething();

    return NextResponse.json({ result }, { headers: corsHeaders });
  } catch (error) {
    console.error('Error in endpoint:', error);
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Unknown error' },
      { status: 500, headers: corsHeaders }
    );
  }
}
```

3. **For X handle validation** (if applicable):
```typescript
const HANDLE_REGEX = /^[a-zA-Z0-9_]{1,15}$/;
if (!handle || !HANDLE_REGEX.test(handle)) {
  return NextResponse.json(
    { error: 'Invalid X handle format.' },
    { status: 400, headers: corsHeaders }
  );
}
```

4. **For database operations**, import from `@/db`:
```typescript
import { db, tableName } from '@/db';
import { eq, gt, and } from 'drizzle-orm';
```

## Existing Endpoints Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/analyze-account` | POST | Analyze X account with Grok |
| `/api/generate-image` | POST | Generate images (rate-limited) |
| `/api/roast-account` | POST | Generate roast letter |
| `/api/fbi-profile` | POST | Generate FBI profile |

## Examples

- "Create an endpoint to fetch user stats" → Create `app/api/user-stats/route.ts`
- "Add a health check endpoint" → Create `app/api/health/route.ts` with GET handler

## Guardrails

- Always include CORS headers on all responses
- Always include OPTIONS handler for preflight requests
- Check environment variables exist before using
- Use try/catch with proper error responses
- Log errors with console.error for debugging
- Never expose API keys in responses
