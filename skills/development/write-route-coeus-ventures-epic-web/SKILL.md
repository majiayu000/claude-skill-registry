---
name: write-route
description: Write routes following the Epic architecture patterns. Use when creating HTTP endpoints for behaviors, webhooks, or streaming. Triggers on "create a route", "add a webhook", or "write a route for".
---

# Write Route

## Overview

This skill creates routes that follow the Epic three-layer architecture. Routes belong to the **Backend layer** and provide HTTP endpoints for behaviors that need HTTP semantics, streaming, or external access.

A behavior has either an action OR a route, not both.

## Architecture Context

```
Frontend: Hook (via fetch or fetchEventSource)
              |
              v (HTTP)
Backend: Route (request/response or streaming)
              |
              v
Infrastructure: Models + Integrations
```

Routes:
- Live inside behavior folders
- Handle HTTP requests (GET, POST, etc.)
- Support streaming via SSE (optional)
- Can serve as webhooks for external integrations
- NEVER accessed directly by components

## When to Use Routes

| Use Route | Use Action |
|-----------|------------|
| Streaming/SSE needed | Most behaviors |
| Webhooks (Stripe, etc.) | Direct function calls |
| Need HTTP headers/status | Simpler mental model |
| External client access | Internal operations |

## Route Location

```
app/[page]/behaviors/[behavior-name]/
  route.ts                    # HTTP endpoint
  use-[behavior-name].ts      # Hook that consumes it
```

The route URL follows the folder path:
```
app/(app)/projects/behaviors/generate-spec/route.ts
-> POST /projects/behaviors/generate-spec
```

---

## Non-Streaming Route Pattern

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { getUser } from '@/lib/auth';
import { z } from 'zod';

const InputSchema = z.object({
  name: z.string().min(1),
});

export async function POST(request: NextRequest) {
  // 1. Check authentication
  const user = await getUser();
  if (!user) {
    return NextResponse.json(
      { success: false, error: 'Unauthorized' },
      { status: 401 }
    );
  }

  // 2. Validate input
  const body = await request.json();
  const result = InputSchema.safeParse(body);
  if (!result.success) {
    return NextResponse.json(
      { success: false, error: result.error.errors[0].message },
      { status: 400 }
    );
  }

  // 3. Execute logic
  const data = await someIntegration.process(result.data);

  return NextResponse.json({ success: true, data });
}
```

---

## Streaming Route Pattern (SSE)

```typescript
import { NextRequest } from 'next/server';
import { getUser } from '@/lib/auth';
import { z } from 'zod';

const InputSchema = z.object({
  prompt: z.string().min(1),
});

export async function POST(request: NextRequest) {
  // 1. Check authentication
  const user = await getUser();
  if (!user) {
    return new Response('Unauthorized', { status: 401 });
  }

  // 2. Validate input
  const body = await request.json();
  const result = InputSchema.safeParse(body);
  if (!result.success) {
    return new Response(result.error.errors[0].message, { status: 400 });
  }

  // 3. Create streaming response
  const stream = new TransformStream();
  const writer = stream.writable.getWriter();
  const encoder = new TextEncoder();

  const sendEvent = async (event: string, data: string) => {
    await writer.write(
      encoder.encode(`event: ${event}\ndata: ${data}\n\n`)
    );
  };

  // 4. Start async processing
  (async () => {
    try {
      for await (const chunk of generateContent(result.data.prompt)) {
        await sendEvent('token', chunk);
      }
      await sendEvent('complete', '');
    } catch (error) {
      await sendEvent('error', error instanceof Error ? error.message : 'Unknown error');
    } finally {
      await writer.close();
    }
  })();

  return new Response(stream.readable, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  });
}
```

---

## Webhook Pattern

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { stripe } from '@/shared/integrations/stripe';

export async function POST(request: NextRequest) {
  const body = await request.text();
  const signature = request.headers.get('stripe-signature');

  if (!signature) {
    return NextResponse.json(
      { success: false, error: 'Missing signature' },
      { status: 400 }
    );
  }

  try {
    const event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    );

    switch (event.type) {
      case 'checkout.session.completed':
        // Handle event
        break;
    }

    return NextResponse.json({ received: true });
  } catch (error) {
    console.error('Webhook error:', error);
    return NextResponse.json(
      { success: false, error: 'Webhook failed' },
      { status: 400 }
    );
  }
}
```

---

## Specification Format

### Non-Streaming Route Spec

```markdown
# Process Data Route

**Method:** POST
**Path:** /projects/behaviors/process-data

## Description

Processes uploaded data and returns results.

## Input

- fileId: string - ID of the uploaded file

## Returns

- success: boolean
- data: ProcessedResult

## Examples

### Process successfully

#### Input
fileId: "file-123"

#### Response
{ success: true, data: { ... } }
```

### Streaming Route Spec

```markdown
# Generate Specification Route

**Method:** POST
**Path:** /projects/behaviors/generate-spec

## Description

Generates a project specification incrementally.

## Behavior

- Implements: Generate Specification

## Input

- prompt: string - user description of the project

## Emitted Events

- token - partial generated text
- complete - generation finished

## Completion

- Success: emits `complete`, then closes stream
- Error: emits `error`, then closes stream

## Examples

### Generate specification successfully

#### Input
prompt: "Project management app"

#### Stream
* Emit: token - "# Project Management App"
* Emit: token - "\n## Pages"
* Emit: complete - ""
```

---

## Constraints

- NEVER import React, Jotai, or frontend code
- NEVER access database directly - use models/integrations
- ALWAYS check authentication (except webhooks with signature verification)
- ALWAYS validate input with Zod
- ALWAYS handle errors gracefully
- ALWAYS close streams when done (for SSE)
- Event names are route-specific, not prescribed globally
