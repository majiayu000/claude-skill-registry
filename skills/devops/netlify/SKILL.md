---
name: netlify
description: Deploys applications to Netlify including functions, forms, redirects, and edge functions. Use when deploying static sites, JAMstack applications, or serverless functions.
---

# Netlify

The modern web development platform for deploying and hosting websites.

## Quick Start

**Install CLI:**
```bash
npm install -g netlify-cli
```

**Login:**
```bash
netlify login
```

**Deploy:**
```bash
netlify deploy
```

**Deploy to production:**
```bash
netlify deploy --prod
```

## Project Setup

### Connect Git Repository

1. Go to app.netlify.com
2. Add new site > Import from Git
3. Select repository
4. Configure build settings
5. Deploy

### Drag and Drop

Visit `https://app.netlify.com/drop` and drag your build folder.

### netlify.toml Configuration

```toml
[build]
  command = "npm run build"
  publish = "dist"
  functions = "netlify/functions"

[build.environment]
  NODE_VERSION = "18"

# Production context
[context.production]
  command = "npm run build:prod"

# Preview context (branch deploys)
[context.deploy-preview]
  command = "npm run build:preview"

# Branch-specific
[context.staging]
  command = "npm run build:staging"

# Dev settings
[dev]
  command = "npm run dev"
  port = 3000
  targetPort = 5173

# Headers
[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"

# Redirects
[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/:splat"
  status = 200

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

## Environment Variables

### Setting Variables

**Via Dashboard:**
Site settings > Environment variables > Add variable

**Via CLI:**
```bash
netlify env:set MY_VAR "value"
netlify env:list
netlify env:get MY_VAR
netlify env:unset MY_VAR
```

### Context-Specific Variables

```toml
# netlify.toml
[context.production.environment]
  API_URL = "https://api.example.com"

[context.deploy-preview.environment]
  API_URL = "https://staging-api.example.com"

[context.branch-deploy.environment]
  API_URL = "https://dev-api.example.com"
```

### Using Variables

```javascript
// In build process
const apiUrl = process.env.API_URL;

// In functions
export async function handler(event, context) {
  const secret = process.env.API_SECRET;
}
```

## Serverless Functions

### Basic Function

```javascript
// netlify/functions/hello.js
export async function handler(event, context) {
  return {
    statusCode: 200,
    body: JSON.stringify({ message: 'Hello, World!' }),
  };
}
```

### TypeScript Function

```typescript
// netlify/functions/users.ts
import type { Handler, HandlerEvent, HandlerContext } from '@netlify/functions';

interface User {
  id: string;
  name: string;
}

const handler: Handler = async (event: HandlerEvent, context: HandlerContext) => {
  const { httpMethod, body, queryStringParameters } = event;

  if (httpMethod === 'GET') {
    const users: User[] = await getUsers();
    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(users),
    };
  }

  if (httpMethod === 'POST') {
    const data = JSON.parse(body || '{}');
    const user = await createUser(data);
    return {
      statusCode: 201,
      body: JSON.stringify(user),
    };
  }

  return {
    statusCode: 405,
    body: 'Method Not Allowed',
  };
};

export { handler };
```

### Scheduled Functions

```typescript
// netlify/functions/scheduled.ts
import { schedule } from '@netlify/functions';

const handler = async () => {
  console.log('Running scheduled task');
  await runTask();
  return { statusCode: 200 };
};

// Run every day at midnight
export const handler = schedule('0 0 * * *', handler);
```

### Background Functions

```javascript
// netlify/functions/background-task-background.js
// Suffix with -background for async processing
export async function handler(event, context) {
  // Long-running task (up to 15 minutes)
  await processLargeDataset();

  return {
    statusCode: 200,
  };
}
```

## Edge Functions

### Basic Edge Function

```typescript
// netlify/edge-functions/geo.ts
import type { Context } from '@netlify/edge-functions';

export default async (request: Request, context: Context) => {
  const country = context.geo.country?.code ?? 'Unknown';
  const city = context.geo.city ?? 'Unknown';

  return new Response(
    JSON.stringify({
      message: `Hello from ${city}, ${country}!`,
    }),
    {
      headers: { 'Content-Type': 'application/json' },
    }
  );
};

export const config = { path: '/api/geo' };
```

### Edge Function with Middleware Pattern

```typescript
// netlify/edge-functions/auth.ts
import type { Context } from '@netlify/edge-functions';

export default async (request: Request, context: Context) => {
  const token = request.headers.get('Authorization');

  if (!token) {
    return new Response('Unauthorized', { status: 401 });
  }

  // Validate token
  const user = await validateToken(token);

  if (!user) {
    return new Response('Invalid token', { status: 403 });
  }

  // Continue to origin
  return context.next();
};

export const config = { path: '/api/*' };
```

### Edge Function Declaration

```toml
# netlify.toml
[[edge_functions]]
  path = "/api/geo"
  function = "geo"

[[edge_functions]]
  path = "/api/*"
  function = "auth"
```

## Redirects & Rewrites

### _redirects File

```
# Simple redirect
/old-page /new-page 301

# Wildcard redirect
/blog/* /posts/:splat 301

# Rewrite (proxy)
/api/* /.netlify/functions/:splat 200

# SPA fallback
/* /index.html 200

# Conditional redirect
/country/* /us/:splat 200 Country=us
/country/* /uk/:splat 200 Country=gb
```

### netlify.toml Redirects

```toml
[[redirects]]
  from = "/old"
  to = "/new"
  status = 301

[[redirects]]
  from = "/api/*"
  to = "https://api.example.com/:splat"
  status = 200
  force = true

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
  conditions = { Role = ["admin"] }
```

## Forms

### HTML Form

```html
<form name="contact" method="POST" data-netlify="true">
  <input type="hidden" name="form-name" value="contact" />
  <input type="text" name="name" required />
  <input type="email" name="email" required />
  <textarea name="message" required></textarea>
  <button type="submit">Send</button>
</form>
```

### React Form

```tsx
function ContactForm() {
  const [status, setStatus] = useState('');

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget;
    const formData = new FormData(form);

    try {
      await fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(formData as any).toString(),
      });
      setStatus('success');
    } catch (error) {
      setStatus('error');
    }
  };

  return (
    <form
      name="contact"
      method="POST"
      data-netlify="true"
      onSubmit={handleSubmit}
    >
      <input type="hidden" name="form-name" value="contact" />
      <input type="text" name="name" required />
      <input type="email" name="email" required />
      <button type="submit">Send</button>
    </form>
  );
}
```

### Form Notifications

Configure in Dashboard: Forms > [Form Name] > Settings > Notifications

## Identity (Auth)

### Setup

```html
<!-- Add to HTML -->
<script src="https://identity.netlify.com/v1/netlify-identity-widget.js"></script>
```

### JavaScript API

```javascript
import netlifyIdentity from 'netlify-identity-widget';

netlifyIdentity.init();

// Open modal
netlifyIdentity.open();

// Login
netlifyIdentity.on('login', user => {
  console.log('Logged in:', user);
});

// Logout
netlifyIdentity.on('logout', () => {
  console.log('Logged out');
});

// Get current user
const user = netlifyIdentity.currentUser();
```

## Large Media (Git LFS)

```bash
# Install
netlify lm:install

# Setup
netlify lm:setup

# Track files
git lfs track "*.jpg" "*.png" "*.gif"
```

## Blobs (Storage)

```typescript
// netlify/functions/upload.ts
import { getStore } from '@netlify/blobs';

export async function handler(event) {
  const store = getStore('uploads');

  // Store blob
  await store.set('file-key', event.body, {
    metadata: { contentType: 'image/png' },
  });

  // Get blob
  const blob = await store.get('file-key');

  // Delete blob
  await store.delete('file-key');

  return { statusCode: 200 };
}
```

## Local Development

```bash
# Start dev server
netlify dev

# Start with specific port
netlify dev --port 3000

# Link to site
netlify link

# Pull environment variables
netlify env:pull
```

## Best Practices

1. **Use netlify.toml** - Version control your config
2. **Set up branch deploys** - Preview before production
3. **Use context-specific vars** - Different values per environment
4. **Enable form spam filtering** - Protect forms
5. **Use edge functions** - For low-latency operations

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing form-name input | Add hidden input with form name |
| Wrong publish directory | Check framework output folder |
| Functions not found | Use netlify/functions directory |
| Redirects not working | Check order (first match wins) |
| Build failures | Check build logs, Node version |

## Reference Files

- [references/functions.md](references/functions.md) - Function patterns
- [references/forms.md](references/forms.md) - Form handling
- [references/edge.md](references/edge.md) - Edge functions
