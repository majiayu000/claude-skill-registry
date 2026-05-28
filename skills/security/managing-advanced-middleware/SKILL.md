---
name: managing-advanced-middleware
description: Advanced middleware logic for security and routing. Use for global rate limiting, security headers, and protection of admin routes.
---

# Advanced Middleware and Security Logic

## When to use this skill
- Implementing site-wide security measures.
- Protecting sensitive routes like `/admin/*` or `/dashboard/*`.
- Injecting nonces or CSP headers.

## Workflow
- [ ] Create `middleware.ts` in the root (Next.js 15).
- [ ] Define `config.matcher` to specify target routes.
- [ ] Implement checks (Auth check, Rate limit, CSP).

## Code Pattern (CSP Header)
```typescript
import { NextResponse } from 'next/server';

export function middleware(request: Request) {
    const nonce = Buffer.from(crypto.randomUUID()).toString('base64');
    const csp = `default-src 'self'; script-src 'self' 'nonce-${nonce}';`;
    
    const response = NextResponse.next();
    response.headers.set('Content-Security-Policy', csp);
    return response;
}
```

## Instructions
- **Performance**: Keep middleware logic lightweight to avoid slowing down every request.
- **Auth**: Appwrite sessions are stored in cookies; middleware can check for the presence of these cookies for simple protection.
