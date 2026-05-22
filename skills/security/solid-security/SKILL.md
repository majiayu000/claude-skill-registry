---
name: solid-security
description: "SolidStart security: XSS prevention, CSP headers, CORS configuration, CSRF protection, input validation, server-side validation, environment variable security."
metadata:
  globs:
    - "**/middleware/**"
    - "**/*security*"
---

# SolidStart Security

Complete guide to securing SolidStart applications. Protect against XSS, CSRF, and other common attacks.

## XSS Prevention

Solid automatically escapes values in JSX to prevent XSS attacks.

### Automatic Escaping

```tsx
// ✅ Safe - automatically escaped
function Component() {
  const userInput = "<script>alert('xss')</script>";
  return <div>{userInput}</div>; // Rendered as text
}
```

### Dangerous: innerHTML

```tsx
// ❌ DANGEROUS - not escaped
function Component() {
  const userInput = "<script>alert('xss')</script>";
  return <div innerHTML={userInput} />; // Executes script!
}

// ✅ SAFE - sanitize first
import DOMPurify from "dompurify";

function Component() {
  const userInput = "<script>alert('xss')</script>";
  const sanitized = DOMPurify.sanitize(userInput);
  return <div innerHTML={sanitized} />;
}
```

### Best Practices

1. **Avoid innerHTML when possible**
2. **Sanitize user input** with DOMPurify
3. **Validate URLs** from user input:
   ```tsx
   function validateUrl(url: string) {
     const parsed = new URL(url);
     if (parsed.protocol === "javascript:") {
       throw new Error("Invalid URL");
     }
     return parsed;
   }
   ```
4. **Sanitize noscript content**

## Content Security Policy (CSP)

Configure CSP headers via middleware to restrict resource loading.

### With Nonce (Recommended)

```tsx
// src/middleware/index.ts
import { createMiddleware } from "@solidjs/start/middleware";
import { randomBytes } from "crypto";

export default createMiddleware({
  onRequest: (event) => {
    const nonce = randomBytes(16).toString("base64");
    event.locals.nonce = nonce;

    const csp = `
      default-src 'self';
      script-src 'nonce-${nonce}' 'strict-dynamic' 'unsafe-eval';
      object-src 'none';
      base-uri 'none';
      frame-ancestors 'none';
      form-action 'self';
    `.replace(/\s+/g, " ");

    event.response.headers.set("Content-Security-Policy", csp);
  },
});
```

```tsx
// src/entry-server.tsx
export default createHandler(
  () => <StartServer document={...} />,
  (event) => ({ nonce: event.locals.nonce })
);
```

### Without Nonce

```tsx
import { createMiddleware } from "@solidjs/start/middleware";

export default createMiddleware({
  onBeforeResponse: (event) => {
    const csp = `
      default-src 'self';
      font-src 'self';
      object-src 'none';
      base-uri 'none';
      frame-ancestors 'none';
      form-action 'self';
    `.replace(/\s+/g, " ");

    event.response.headers.set("Content-Security-Policy", csp);
  },
});
```

## CORS Configuration

Configure CORS headers for API endpoints.

```tsx
import { createMiddleware } from "@solidjs/start/middleware";
import { json } from "@solidjs/router";

const TRUSTED_ORIGINS = ["https://my-app.com", "https://another-app.com"];

export default createMiddleware({
  onBeforeResponse: (event) => {
    const { request, response } = event;

    response.headers.append("Vary", "Origin, Access-Control-Request-Method");

    const origin = request.headers.get("Origin");
    const requestUrl = new URL(request.url);
    const isApiRequest = requestUrl.pathname.startsWith("/api");

    if (isApiRequest && origin && TRUSTED_ORIGINS.includes(origin)) {
      // Handle preflight
      if (
        request.method === "OPTIONS" &&
        request.headers.get("Access-Control-Request-Method")
      ) {
        return json(null, {
          headers: {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Methods": "OPTIONS, POST, PUT, PATCH, DELETE",
            "Access-Control-Allow-Headers": "Authorization, Content-Type",
          },
        });
      }

      // Handle normal requests
      response.headers.set("Access-Control-Allow-Origin", origin);
    }
  },
});
```

## CSRF Protection

Protect against Cross-Site Request Forgery attacks.

```tsx
import { createMiddleware } from "@solidjs/start/middleware";
import { json } from "@solidjs/router";

const SAFE_METHODS = ["GET", "HEAD", "OPTIONS", "TRACE"];
const TRUSTED_ORIGINS = ["https://another-app.com"];

export default createMiddleware({
  onRequest: (event) => {
    const { request } = event;

    if (!SAFE_METHODS.includes(request.method)) {
      const requestUrl = new URL(request.url);
      const origin = request.headers.get("Origin");

      // Check Origin header
      if (origin) {
        const parsedOrigin = new URL(origin);

        if (
          parsedOrigin.origin !== requestUrl.origin &&
          !TRUSTED_ORIGINS.includes(parsedOrigin.host)
        ) {
          return json({ error: "origin invalid" }, { status: 403 });
        }
      }

      // Check Referer for HTTPS
      if (!origin && requestUrl.protocol === "https:") {
        const referer = request.headers.get("Referer");

        if (!referer) {
          return json({ error: "referer not supplied" }, { status: 403 });
        }

        const parsedReferer = new URL(referer);

        if (parsedReferer.protocol !== "https:") {
          return json({ error: "referer invalid" }, { status: 403 });
        }

        if (
          parsedReferer.host !== requestUrl.host &&
          !TRUSTED_ORIGINS.includes(parsedReferer.host)
        ) {
          return json({ error: "referer invalid" }, { status: 403 });
        }
      }
    }
  },
});
```

## Input Validation

### Server-Side Validation

```tsx
"use server";

import { action } from "@solidjs/router";
import { z } from "zod";

const userSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
});

export const createUser = action(async (formData: FormData) => {
  const data = {
    email: formData.get("email"),
    name: formData.get("name"),
  };

  // Validate
  const result = userSchema.safeParse(data);
  if (!result.success) {
    return { ok: false, errors: result.error.errors };
  }

  // Process validated data
  // ...
}, "createUser");
```

### Client-Side Validation

```tsx
import { createSignal } from "solid-js";

function Form() {
  const [email, setEmail] = createSignal("");
  const [error, setError] = createSignal("");

  const validateEmail = (value: string) => {
    if (!value.includes("@")) {
      setError("Invalid email");
      return false;
    }
    setError("");
    return true;
  };

  return (
    <form>
      <input
        value={email()}
        onInput={(e) => {
          setEmail(e.currentTarget.value);
          validateEmail(e.currentTarget.value);
        }}
      />
      <Show when={error()}>
        <span class="error">{error()}</span>
      </Show>
    </form>
  );
}
```

## Environment Variable Security

### Never Expose Secrets

```env
# ❌ WRONG - exposed to client
VITE_DB_PASSWORD=secret123

# ✅ CORRECT - server-only
DB_PASSWORD=secret123
```

### Access Control

```tsx
// ✅ Server-only access
"use server";

export async function getData() {
  const secret = process.env.API_SECRET_KEY; // Server-only
  // Use secret
}
```

## Best Practices

1. **Always validate input** on server
2. **Sanitize user content** before rendering
3. **Use CSP headers** to restrict resources
4. **Configure CORS** for API endpoints
5. **Protect against CSRF** for state-changing operations
6. **Never expose secrets** in client code
7. **Use HTTPS** in production
8. **Keep dependencies updated**

## Summary

- **XSS**: Avoid innerHTML, sanitize input
- **CSP**: Configure via middleware with nonces
- **CORS**: Restrict to trusted origins
- **CSRF**: Validate Origin/Referer headers
- **Validation**: Server-side is mandatory
- **Secrets**: Never use VITE_ prefix

