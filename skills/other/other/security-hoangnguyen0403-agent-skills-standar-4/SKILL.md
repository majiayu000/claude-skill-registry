---
name: Next.js Security
description: Core security standards for App Router and Server Actions.
metadata:
  labels: [nextjs, security, rsc, csrf, zod]
  triggers:
    files: ['app/**/actions.ts', 'middleware.ts']
    keywords: [action, boundary, sanitize, auth, jose]
---

# Next.js Security

## **Priority: P0 (CRITICAL)**

## Structure

```text
app/
├── lib/
│   └── validation.ts   # Shared Zod schemas
└── middleware.ts       # Auth & Headers
```

## Implementation Guidelines

- **Action Safety**: Validate all `FormData` or JSON input using **Zod**.
- **Data Boundaries**: Never pass whole DB objects to Client Components.
- **Server-Only**: Mark sensitive logic files with `'use server-only'`.
- **CSRF**: Modern Next.js manages this, but ensure unique session origins.
- **Middleware Guarding**: Use `middleware.ts` for global route protection.
- **Sanitization**: Sanitize HTML if bypassing default React escaping.

## Anti-Patterns

- **Raw Props**: **No leaking DB fields**: Use DTOs for client data.
- **Client Secrets**: **No process.env in client**: Mark as `NEXT_PUBLIC_` only if safe.
- **Unvalidated Actions**: **No raw JSON actions**: Always validate schema.
- **Logic in Layouts**: **No auth in shared Layouts**: Insecure; use Middleware.

## References

- [Secure App Router Patterns](references/implementation.md)
