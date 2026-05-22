---
name: backend-error-handling
description: Backend typed error handling and boundary mapping
compatibility: opencode
license: MIT
metadata:
  stack: node-react-next
  style: solid-clean-code
---
## What I do

Je standardise une gestion d'erreurs **typée** et **composable** côté backend.

## Rules
- Domain errors : invariants.
- Application errors : orchestration/policies.
- Presentation : mapping vers HTTP.

## Template

```ts
export class NotFoundError extends Error {
  readonly code = 'NOT_FOUND';
}

export function toHttp(err: unknown) {
  if (err instanceof NotFoundError) return { status: 404, body: { message: err.message } };
  return { status: 500, body: { message: 'Internal error' } };
}
```

## When to use
- Chaque fois qu'un contrôleur commence à contenir des `if/else` d'erreurs.
