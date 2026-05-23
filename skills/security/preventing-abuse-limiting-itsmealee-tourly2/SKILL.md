---
name: preventing-abuse-limiting
description: Implements rate limiting and abuse prevention measures. Use to protect sensitive endpoints like "Book Now" or "Contact Us".
---

# Rate Limiting and Abuse Prevention

## When to use this skill
- Protecting public-facing endpoints (Server Actions or Route Handlers).
- Preventing bot spam or brute-force attacks.

## Workflow
- [ ] Implement rate limiting in Next.js Middleware or Server Actions.
- [ ] Use an in-memory store (for simple cases) or Redis/Appwrite KV (for scaled apps).
- [ ] Return a `429 Too Many Requests` status code when exceeded.

## Code Pattern (Middleware)
```typescript
import { NextResponse } from 'next/server';

export function middleware(request: Request) {
    // Logic to check IP/Token against a limit
    if (isOverLimit(request)) {
        return NextResponse.json({ error: 'Too many requests' }, { status: 429 });
    }
}
```

## Instructions
- **Appwrite Built-in**: Use Appwrite's built-in rate limits where possible (e.g., authentication limits).
- **Graceful Failure**: Show a "Please wait a moment before trying again" message to the user.
