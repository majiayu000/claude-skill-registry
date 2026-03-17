---
name: libweb
description: >
  libweb - Web extension utilities. authMiddleware validates JWT tokens.
  corsMiddleware handles cross-origin requests. validationMiddleware validates
  request bodies against JSON schema. createAuthMiddleware,
  createCorsMiddleware, createValidation are factories for customization. Use
  for securing HTTP APIs, request validation, and CORS handling with Hono
  framework.
---

# libweb Skill

## When to Use

- Adding authentication to HTTP endpoints
- Configuring CORS for API access
- Validating request payloads
- Building secure REST APIs with Hono

## Key Concepts

**authMiddleware**: Validates JWT tokens from Authorization header.

**corsMiddleware**: Handles preflight requests and CORS headers.

**validationMiddleware**: Validates request body against JSON schema.

## Usage Patterns

### Pattern 1: Secure endpoint

```javascript
import { authMiddleware, corsMiddleware } from "@copilot-ld/libweb";

app.use(corsMiddleware({ origins: ["http://localhost:3000"] }));
app.use("/api/*", authMiddleware(authConfig));
```

### Pattern 2: Validate requests

```javascript
import { validationMiddleware } from "@copilot-ld/libweb";

const schema = {
  type: "object",
  required: ["message"],
  properties: { message: { type: "string", maxLength: 1000 } },
};

app.post("/api/chat", validationMiddleware(schema), handler);
```

## Integration

Used by Web and API extensions. Works with Hono framework middleware pattern.
