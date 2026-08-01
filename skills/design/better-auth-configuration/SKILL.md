---
name: better-auth-configuration
description: 'Creates Better Auth configuration for frontend and backend: handlers,
  providers, middleware, session/token options. Uses Context7 MCP to retrieve Better
  Auth docs.'
---

---
name: Better Auth Configuration
description: Creates Better Auth configuration for frontend and backend: handlers, providers, middleware, session/token options. Uses Context7 MCP to retrieve Better Auth docs.
---

# Better Auth Configuration

## Instructions

1. Create Better Auth configuration:
   - Set up main auth instance with appropriate options
   - Configure OAuth providers (Google, GitHub, etc.)
   - Define session management settings
   - Configure cookie settings and security options
   - Set up email/password authentication if needed

2. Follow Better Auth documentation:
   - Retrieve latest official documentation via Context7 MCP
   - Follow recommended security practices
   - Use proper TypeScript configuration
   - Include proper error handling

3. Configure frontend integration:
   - Set up client-side configuration
   - Configure authentication hooks
   - Set up provider wrappers
   - Include proper type definitions

4. Configure backend integration:
   - Set up server-side configuration
   - Define middleware for protected routes
   - Configure API route protection
   - Include proper session validation

5. Security considerations:
   - Use secure cookie settings
   - Configure proper CORS settings
   - Set up rate limiting if needed
   - Include proper error handling

## Examples

Input: "Configure Better Auth with Google OAuth and JWT sessions"
Output: Creates configuration with:
```typescript
import { betterAuth } from 'better-auth'

export const auth = betterAuth({
  database: {
    provider: 'drizzle',
    url: process.env.DATABASE_URL!,
  },
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  },
  session: {
    expires: 7 * 24 * 60 * 60 * 1000, // 7 days
    generateId: () => crypto.randomUUID(),
  },
})
```