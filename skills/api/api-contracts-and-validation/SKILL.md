---
name: api-contracts-and-validation
description: Define and validate API contracts using Zod
version: 1.1.0
tags: [api, zod, contracts, validation]
owner: platform
status: active
---

# API Contracts & Validation Skill

## Overview

Define Zod schemas as the source of truth for API contracts and validation.

## Usage

```
/api-contracts-and-validation
```

## Documentation Reference

- Use Ref tools to confirm Zod API details and best practices when needed.

## Identity
**Role**: API Designer
**Objective**: Create single-source-of-truth definitions for API structures using Zod schemas, shared between client and server.

## Standards

### 1. Zod First
Define the schema **before** the Typescript type.
```typescript
import { z } from 'zod';

// 1. Schema
export const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  role: z.enum(['ADMIN', 'USER']),
  meta: z.record(z.string()).optional()
});

// 2. Inference
export type User = z.infer<typeof UserSchema>;
```

### 2. Runtime Validation
**Server-Side**: All inputs (Req Body, Params, Query) MUST be parsed.
```typescript
app.post('/user', (req, res) => {
  const result = UserSchema.safeParse(req.body);
  if (!result.success) return res.status(400).json(result.error);
  // ...
});
```

### 3. Client-Side Safe Fetching
Validate responses from the API before using them in the UI to prevent "Undefined is not a function" crashes.

## Workflow

### Contract Creation
**Command**: `/make-contract <name>`
1.  **Define**: Create `src/contracts/<domain>.contract.ts`.
2.  **Schema**: Write Zod schema for Request, Response, and Errors.
3.  **Export**: Export inferred types.

### Code Gen (Optional)
If using tRPC or OpenAPI, update the generation scripts.

## Error Handling
- **Parse Errors**: Zod returns detailed error maps. Convert these to user-friendly messages for the frontend.
- **Strict Mode**: Schemas should use `.strict()` by default to strip unknown fields.

## Outputs

- Zod schemas and derived types for shared API contracts.

## Related Skills

- `/ts-strict-guardian` - Enforce strict TypeScript safety
