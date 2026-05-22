---
name: backend-dev-ops
description: Backend development, API design, and business logic implementation. Use for Node.js, Express, Next.js API routes, Supabase Edge Functions, authentication flows, database queries, third-party integrations, webhooks, and server-side logic. Triggers on queries like "build the API", "create endpoints", "implement auth", "add business logic", "integrate with [service]", or any backend development task.
---

# Backend Development Operations

Build production-quality backend services, APIs, and business logic.

## Tech Stack Defaults

| Use Case | Stack |
|----------|-------|
| Full-stack app | Next.js API Routes + Supabase |
| Standalone API | Express + TypeScript + Prisma |
| Serverless | Supabase Edge Functions (Deno) |
| Background jobs | Node.js + BullMQ |

## Standard Structure

### Next.js API Routes
```
src/app/api/
├── auth/
│   ├── login/route.ts
│   ├── logout/route.ts
│   └── register/route.ts
├── users/
│   ├── route.ts              # GET all, POST create
│   └── [id]/route.ts         # GET one, PUT, DELETE
├── webhooks/
│   └── stripe/route.ts
└── _lib/                     # Shared utilities
    ├── auth.ts
    ├── db.ts
    └── errors.ts
```

### Express API
```
src/
├── routes/
│   ├── auth.routes.ts
│   ├── users.routes.ts
│   └── index.ts
├── controllers/
│   ├── auth.controller.ts
│   └── users.controller.ts
├── services/
│   ├── auth.service.ts
│   └── users.service.ts
├── middleware/
│   ├── auth.middleware.ts
│   ├── error.middleware.ts
│   └── validate.middleware.ts
├── lib/
│   ├── db.ts
│   └── utils.ts
├── types/
│   └── index.ts
└── index.ts
```

## API Route Patterns

### Next.js Route Handler
```typescript
// app/api/items/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@/lib/supabase/server';

export async function GET(request: NextRequest) {
  try {
    const supabase = createClient();
    const { data, error } = await supabase
      .from('items')
      .select('*')
      .order('created_at', { ascending: false });
    
    if (error) throw error;
    
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch items' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const supabase = createClient();
    
    const { data, error } = await supabase
      .from('items')
      .insert(body)
      .select()
      .single();
    
    if (error) throw error;
    
    return NextResponse.json(data, { status: 201 });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create item' },
      { status: 500 }
    );
  }
}
```

### Dynamic Route
```typescript
// app/api/items/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const { id } = params;
  // ... fetch by id
}

export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const { id } = params;
  const body = await request.json();
  // ... update by id
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const { id } = params;
  // ... delete by id
}
```

## Authentication

### Supabase Auth (Next.js)
```typescript
// lib/supabase/server.ts
import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';

export function createClient() {
  const cookieStore = cookies();
  
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) =>
            cookieStore.set(name, value, options)
          );
        },
      },
    }
  );
}
```

### Protected Route Middleware
```typescript
// middleware.ts
import { createServerClient } from '@supabase/ssr';
import { NextResponse, type NextRequest } from 'next/server';

export async function middleware(request: NextRequest) {
  const response = NextResponse.next();
  
  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    { cookies: { /* cookie handlers */ } }
  );
  
  const { data: { user } } = await supabase.auth.getUser();
  
  if (!user && request.nextUrl.pathname.startsWith('/api/protected')) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }
  
  return response;
}
```

## Database Queries

### Supabase Query Patterns
```typescript
// SELECT with filters
const { data } = await supabase
  .from('items')
  .select('*, category:categories(name)')
  .eq('user_id', userId)
  .gte('price', minPrice)
  .order('created_at', { ascending: false })
  .range(0, 9);

// INSERT with return
const { data } = await supabase
  .from('items')
  .insert({ name, price, user_id: userId })
  .select()
  .single();

// UPDATE
const { data } = await supabase
  .from('items')
  .update({ name, price })
  .eq('id', id)
  .select()
  .single();

// DELETE
const { error } = await supabase
  .from('items')
  .delete()
  .eq('id', id);

// RPC (stored procedure)
const { data } = await supabase
  .rpc('get_user_stats', { user_id: userId });
```

## Error Handling

### Standard Error Response
```typescript
// lib/errors.ts
export class APIError extends Error {
  constructor(
    public statusCode: number,
    message: string,
    public code?: string
  ) {
    super(message);
  }
}

export function handleError(error: unknown) {
  if (error instanceof APIError) {
    return NextResponse.json(
      { error: error.message, code: error.code },
      { status: error.statusCode }
    );
  }
  
  console.error('Unexpected error:', error);
  return NextResponse.json(
    { error: 'Internal server error' },
    { status: 500 }
  );
}
```

### Usage
```typescript
export async function GET() {
  try {
    // ... logic
  } catch (error) {
    return handleError(error);
  }
}
```

## Validation

### Zod Schema Validation
```typescript
import { z } from 'zod';

const CreateItemSchema = z.object({
  name: z.string().min(1).max(100),
  price: z.number().positive(),
  category_id: z.string().uuid().optional(),
});

export async function POST(request: NextRequest) {
  const body = await request.json();
  
  const result = CreateItemSchema.safeParse(body);
  if (!result.success) {
    return NextResponse.json(
      { error: 'Validation failed', details: result.error.flatten() },
      { status: 400 }
    );
  }
  
  const validated = result.data;
  // ... proceed with validated data
}
```

## Third-Party Integrations

### Stripe Webhook
```typescript
// app/api/webhooks/stripe/route.ts
import Stripe from 'stripe';
import { headers } from 'next/headers';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function POST(request: NextRequest) {
  const body = await request.text();
  const signature = headers().get('stripe-signature')!;
  
  let event: Stripe.Event;
  
  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    );
  } catch (err) {
    return NextResponse.json({ error: 'Invalid signature' }, { status: 400 });
  }
  
  switch (event.type) {
    case 'payment_intent.succeeded':
      await handlePaymentSuccess(event.data.object);
      break;
    case 'customer.subscription.updated':
      await handleSubscriptionUpdate(event.data.object);
      break;
  }
  
  return NextResponse.json({ received: true });
}
```

### External API Client
```typescript
// services/external-api.ts
export class ExternalAPIClient {
  private baseUrl: string;
  private apiKey: string;
  
  constructor() {
    this.baseUrl = process.env.EXTERNAL_API_URL!;
    this.apiKey = process.env.EXTERNAL_API_KEY!;
  }
  
  async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const res = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });
    
    if (!res.ok) {
      throw new APIError(res.status, `External API error: ${res.statusText}`);
    }
    
    return res.json();
  }
}
```

## Environment Variables

### Required Variables
```env
# Database
DATABASE_URL=
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# Auth
NEXTAUTH_SECRET=
NEXTAUTH_URL=

# External Services (as needed)
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
OPENAI_API_KEY=
```

## Quality Checklist

Before marking backend task complete:
- [ ] All endpoints return proper status codes
- [ ] Input validation on all POST/PUT routes
- [ ] Authentication on protected routes
- [ ] Error handling with meaningful messages
- [ ] No secrets in code (use env vars)
- [ ] Database queries optimized (indexes, limits)
- [ ] Webhook signature verification
- [ ] TypeScript: proper types, no `any`
- [ ] Build passes without errors
