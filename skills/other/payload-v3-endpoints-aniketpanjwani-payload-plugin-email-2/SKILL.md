---
name: payload-v3-endpoints
description: Provides correct Payload CMS v3 endpoint patterns and logger API usage. Use when writing or fixing REST API endpoints, custom handlers, or when encountering TypeScript errors with req.data, req.cookies, or logger calls.
---

<objective>
Ensure all Payload v3 endpoints and logger calls follow the correct patterns to avoid runtime errors and TypeScript issues.
</objective>

<critical_patterns>

<pattern name="request-body-access">
**WRONG (Payload v2 pattern):**
```typescript
handler: async (req, res) => {
  const data = req.data  // undefined in v3!
  res.status(200).json({ success: true })
}
```

**CORRECT (Payload v3 pattern):**
```typescript
handler: async (req) => {
  const data = await req.json()
  return Response.json({ success: true }, { status: 200 })
}
```

Alternative using helper:
```typescript
import { addDataAndFileToRequest } from 'payload'

handler: async (req) => {
  await addDataAndFileToRequest(req)
  const data = req.data  // now available
  return Response.json({ success: true })
}
```
</pattern>

<pattern name="response-format">
**WRONG:**
```typescript
res.status(200).json({ message: 'success' })
res.json({ message: 'success' })
```

**CORRECT:**
```typescript
return Response.json({ message: 'success' }, { status: 200 })
return Response.json({ message: 'success' })  // defaults to 200
```

Error responses:
```typescript
return Response.json({ error: 'Not found' }, { status: 404 })
return Response.json({ error: 'Unauthorized' }, { status: 401 })
```
</pattern>

<pattern name="cookie-access">
**WRONG:**
```typescript
const token = req.cookies.token  // undefined in v3!
```

**CORRECT:**
```typescript
const cookieHeader = req.headers.get('cookie')
const cookies = parseCookies(cookieHeader)
const token = cookies.token
```
</pattern>

<pattern name="handler-signature">
**WRONG:**
```typescript
handler: async (req, res) => { ... }
```

**CORRECT:**
```typescript
handler: async (req) => { ... }
// or with PayloadRequest type
handler: async (req: PayloadRequest) => { ... }
```
</pattern>

<pattern name="logger-api">
Payload uses pino logger. The signature is: `logger.info(object, message)` NOT `logger.info(message, object)`

**WRONG:**
```typescript
req.payload.logger.info('User created', { userId: 123 })
req.payload.logger.error('Failed to save:', error)
```

**CORRECT:**
```typescript
req.payload.logger.info({ userId: 123 }, 'User created')
req.payload.logger.error({ error: String(error) }, 'Failed to save')
```

For simple messages (no object):
```typescript
req.payload.logger.info('Operation completed')  // This is fine
```
</pattern>

<pattern name="endpoint-definition">
Complete endpoint example:
```typescript
import type { Endpoint, PayloadRequest } from 'payload'

export const myEndpoint: Endpoint = {
  path: '/my-endpoint',
  method: 'post',
  handler: async (req: PayloadRequest) => {
    try {
      const data = await req.json()

      // Access payload
      const result = await req.payload.find({
        collection: 'users',
        where: { email: { equals: data.email } }
      })

      req.payload.logger.info({ count: result.totalDocs }, 'Found users')

      return Response.json({
        success: true,
        data: result
      })
    } catch (error) {
      req.payload.logger.error({ error: String(error) }, 'Endpoint failed')
      return Response.json({ error: 'Internal error' }, { status: 500 })
    }
  }
}
```
</pattern>

</critical_patterns>

<common_errors>
| Error | Cause | Fix |
|-------|-------|-----|
| `req.data is undefined` | Using v2 pattern | Use `await req.json()` |
| `req.cookies is undefined` | Using v2 pattern | Parse from `req.headers.get('cookie')` |
| `res.json is not a function` | Handler has wrong signature | Return `Response.json()` |
| `TS2769: No overload matches` on logger | Wrong argument order | Put object first, message second |
| `Type 'string \| string[]' not assignable` | relationTo can be array | Use `Array.isArray(x) ? x[0] : x` |
</common_errors>

<quick_reference>
```typescript
// Request body
const data = await req.json()

// Response
return Response.json({ data }, { status: 200 })

// Logger
req.payload.logger.info({ key: value }, 'Message')
req.payload.logger.error({ error: String(e) }, 'Error message')

// Handler signature
handler: async (req: PayloadRequest) => { ... }
```
</quick_reference>

<success_criteria>
- All endpoints use `await req.json()` for body access
- All responses use `Response.json()`
- All logger calls have object first, message second
- Handler signature is `(req)` not `(req, res)`
- TypeScript compiles without errors
</success_criteria>
