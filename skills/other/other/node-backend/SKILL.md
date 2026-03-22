---
name: node-backend
description: Build Node.js backends for BigCommerce apps — Express/Fastify servers, OAuth handling, JWT verification, API proxy, webhook processing, session management, and deployment. Use when building the server-side component of BigCommerce apps.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# Node.js Backend for BigCommerce Apps

## Before writing code

**Fetch live docs**:
1. Web-search `site:developer.bigcommerce.com apps guide` for app development patterns
2. Fetch `https://expressjs.com/` or `https://fastify.dev/` for framework docs
3. Web-search `bigcommerce node sample app github` for official sample apps

## App Server Architecture

### Typical Stack

```
BigCommerce Admin (iframe)
    ↓ OAuth flow / Load callback
Your Node.js Server (Express/Fastify)
    ↓ API calls
BigCommerce REST/GraphQL APIs
    ↓ Webhooks
Your Webhook Handler
```

### Project Structure

```
bc-app/
├── src/
│   ├── index.ts              # Server entry point
│   ├── routes/
│   │   ├── auth.ts           # OAuth callbacks (install, load, uninstall)
│   │   ├── api.ts            # App API routes
│   │   └── webhooks.ts       # Webhook handlers
│   ├── services/
│   │   ├── bigcommerce.ts    # BigCommerce API client
│   │   └── store.ts          # Store/token management
│   ├── middleware/
│   │   ├── auth.ts           # Authentication middleware
│   │   └── verify.ts         # JWT/webhook verification
│   └── lib/
│       ├── jwt.ts            # JWT utilities
│       └── db.ts             # Database connection
├── .env                      # Environment variables
├── package.json
└── tsconfig.json
```

## OAuth Implementation

### Install Callback

```typescript
// routes/auth.ts
app.get('/auth/install', async (req, res) => {
  const { code, scope, context } = req.query;

  // Exchange code for permanent token
  const tokenResponse = await fetch('https://login.bigcommerce.com/oauth2/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      client_id: process.env.BC_CLIENT_ID,
      client_secret: process.env.BC_CLIENT_SECRET,
      code,
      scope,
      grant_type: 'authorization_code',
      redirect_uri: process.env.BC_AUTH_CALLBACK,
      context,
    }),
  });

  const { access_token, user, context: storeContext } = await tokenResponse.json();
  const storeHash = storeContext.split('/')[1];

  // Store token securely
  await saveStoreToken(storeHash, access_token, user);

  // Return app UI
  res.send('<html>App installed successfully!</html>');
});
```

### Load Callback

```typescript
app.get('/auth/load', async (req, res) => {
  const signedPayload = req.query.signed_payload_jwt as string;

  // Verify JWT
  const decoded = verifyJwt(signedPayload, process.env.BC_CLIENT_SECRET!);
  const storeHash = decoded.sub.split('/')[1];
  const userId = decoded.user.id;

  // Load store token
  const token = await getStoreToken(storeHash);

  // Render app UI
  res.send(renderApp(storeHash, userId));
});
```

### Uninstall Callback

```typescript
app.get('/auth/uninstall', async (req, res) => {
  const signedPayload = req.query.signed_payload_jwt as string;
  const decoded = verifyJwt(signedPayload, process.env.BC_CLIENT_SECRET!);
  const storeHash = decoded.sub.split('/')[1];

  // Clean up stored data
  await deleteStoreData(storeHash);

  res.status(200).send('OK');
});
```

## JWT Verification

```typescript
import jwt from 'jsonwebtoken';

function verifyJwt(token: string, secret: string) {
  return jwt.verify(token, secret, {
    algorithms: ['HS256'],
    audience: process.env.BC_CLIENT_ID,
  });
}
```

## BigCommerce API Client

### Typed HTTP Client

```typescript
class BigCommerceClient {
  constructor(
    private storeHash: string,
    private accessToken: string,
  ) {}

  private async request<T>(path: string, options?: RequestInit): Promise<T> {
    const url = `https://api.bigcommerce.com/stores/${this.storeHash}${path}`;
    const response = await fetch(url, {
      ...options,
      headers: {
        'X-Auth-Token': this.accessToken,
        'Content-Type': 'application/json',
        Accept: 'application/json',
        ...options?.headers,
      },
    });

    if (response.status === 429) {
      const retryAfter = response.headers.get('X-Rate-Limit-Time-Reset-Ms');
      // Implement backoff
    }

    if (!response.ok) {
      throw new ApiError(response.status, await response.text());
    }

    return response.json();
  }

  async getProducts(params?: Record<string, string>) {
    const query = new URLSearchParams(params).toString();
    return this.request(`/v3/catalog/products?${query}`);
  }

  async getOrder(orderId: number) {
    return this.request(`/v2/orders/${orderId}`);
  }
}
```

## Webhook Handling

```typescript
app.post('/webhooks/orders', async (req, res) => {
  // Verify webhook (check custom header)
  const secret = req.headers['x-webhook-secret'];
  if (secret !== process.env.WEBHOOK_SECRET) {
    return res.status(401).send('Unauthorized');
  }

  // Acknowledge immediately
  res.status(200).send('OK');

  // Process asynchronously
  const { scope, data, store_id } = req.body;
  await processOrderEvent(store_id, data.id, scope);
});
```

## Session Management

### For Multi-Store Apps

Store sessions with store hash context:
- Use Redis or database-backed sessions
- Associate session with `storeHash` and `userId`
- Validate session on every request

### Cookie Security

```typescript
app.use(session({
  secret: process.env.SESSION_SECRET!,
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: true,        // HTTPS only
    httpOnly: true,      // No JS access
    sameSite: 'none',    // Required for iframe embedding
    maxAge: 24 * 60 * 60 * 1000,
  },
}));
```

Note: `sameSite: 'none'` is required because BigCommerce apps load in an iframe.

## Error Handling

```typescript
// Global error handler
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  console.error('Unhandled error:', err);
  res.status(500).json({ error: 'Internal server error' });
});

// API error class
class ApiError extends Error {
  constructor(public statusCode: number, message: string) {
    super(message);
  }
}
```

## Deployment

### Platform Options

| Platform | Pros | Setup |
|----------|------|-------|
| Vercel | Easy, auto-scaling, edge functions | `vercel deploy` |
| Railway | Simple, DB support | `railway deploy` |
| Render | Free tier, managed services | Git push |
| AWS Lambda | Serverless, pay-per-use | SAM/CDK |
| Heroku | Classic PaaS | `git push heroku` |

### Environment Variables

Always set via platform's secret management — never in code:
```
BC_CLIENT_ID=xxx
BC_CLIENT_SECRET=xxx
BC_AUTH_CALLBACK=https://your-app.com/auth/install
BC_LOAD_CALLBACK=https://your-app.com/auth/load
BC_UNINSTALL_CALLBACK=https://your-app.com/auth/uninstall
SESSION_SECRET=xxx
WEBHOOK_SECRET=xxx
DATABASE_URL=xxx
```

## Best Practices

- Use TypeScript for type safety across API interactions
- Verify JWTs on every callback — never trust unsigned payloads
- Store tokens encrypted in database, not in memory or sessions
- Handle rate limits with exponential backoff
- Process webhooks asynchronously — acknowledge with 200 immediately
- Use `sameSite: 'none'` + `secure: true` cookies for iframe embedding
- Implement health check endpoints for monitoring
- Log API errors but never log tokens or secrets
- Use connection pooling for database connections

Fetch the BigCommerce app development guide and Node.js framework docs for exact callback parameters, JWT structure, and deployment patterns before implementing.
