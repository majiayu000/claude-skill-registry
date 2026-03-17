# Netlify Platform Skill

---
progressive_disclosure:
  entry_point:
    summary: "JAMstack deployment platform with serverless functions, forms, and identity"
    when_to_use:
      - "When deploying static sites and SPAs"
      - "When building JAMstack applications"
      - "When needing serverless functions"
      - "When requiring built-in forms and auth"
    quick_start:
      - "npm install -g netlify-cli"
      - "netlify login"
      - "netlify init"
      - "netlify deploy --prod"
  token_estimate:
    entry: 70-85
    full: 3800-4800
---

## Netlify Fundamentals

### Core Concepts
- **Sites**: Static sites deployed to Netlify's global CDN
- **Builds**: Automated build process triggered by Git commits
- **Deploy Contexts**: production, deploy-preview, branch-deploy
- **Atomic Deploys**: All-or-nothing deployments with instant rollback
- **Instant Cache Invalidation**: CDN cache cleared automatically

### Platform Benefits
- **Global CDN**: Built-in content delivery network
- **Continuous Deployment**: Auto-deploy from Git
- **HTTPS by Default**: Free SSL certificates
- **Deploy Previews**: Preview every pull request
- **Serverless Functions**: Backend logic without servers
- **Forms & Identity**: Built-in features for common needs

## Static Site Deployment

### Supported Frameworks
```bash
# React (Create React App, Vite)
Build command: npm run build
Publish directory: build (CRA) or dist (Vite)

# Next.js (Static Export)
Build command: npm run build && npm run export
Publish directory: out

# Vue.js
Build command: npm run build
Publish directory: dist

# Gatsby
Build command: gatsby build
Publish directory: public

# Hugo
Build command: hugo
Publish directory: public

# Svelte/SvelteKit
Build command: npm run build
Publish directory: build
```

### Manual Deployment
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Initialize site
netlify init

# Deploy draft (preview URL)
netlify deploy

# Deploy to production
netlify deploy --prod

# Deploy with build
netlify deploy --build --prod
```

## netlify.toml Configuration

### Basic Configuration
```toml
# netlify.toml
[build]
  # Build command
  command = "npm run build"

  # Publish directory
  publish = "dist"

  # Functions directory
  functions = "netlify/functions"

# Production context
[context.production]
  command = "npm run build:prod"

[context.production.environment]
  NODE_ENV = "production"
  API_URL = "https://api.example.com"

# Deploy Preview context
[context.deploy-preview]
  command = "npm run build:preview"

# Branch deploys
[context.branch-deploy]
  command = "npm run build"
```

### Build Settings
```toml
[build]
  command = "npm run build"
  publish = "dist"

  # Base directory for monorepos
  base = "packages/web"

  # Ignore builds on certain changes
  ignore = "git diff --quiet $CACHED_COMMIT_REF $COMMIT_REF packages/web"

[build.environment]
  NODE_VERSION = "18"
  NPM_VERSION = "9"
  RUBY_VERSION = "3.1"
```

### Advanced Build Configuration
```toml
[build]
  command = "npm run build"
  publish = "dist"

  # Build processing
  [build.processing]
    skip_processing = false
  [build.processing.css]
    bundle = true
    minify = true
  [build.processing.js]
    bundle = true
    minify = true
  [build.processing.images]
    compress = true
```

## Environment Variables

### Setting Variables
```bash
# Via CLI
netlify env:set API_KEY "secret-value"
netlify env:set NODE_ENV "production"

# List variables
netlify env:list

# Import from .env file
netlify env:import .env
```

### Variable Scopes
```toml
# netlify.toml
[context.production.environment]
  API_URL = "https://api.production.com"
  ENABLE_ANALYTICS = "true"

[context.deploy-preview.environment]
  API_URL = "https://api.staging.com"
  ENABLE_ANALYTICS = "false"

[context.branch-deploy.environment]
  API_URL = "https://api.dev.com"
```

### Accessing in Build
```javascript
// During build
const apiUrl = process.env.API_URL;

// Client-side (must be prefixed)
const publicKey = process.env.REACT_APP_PUBLIC_KEY;
```

## Serverless Functions

### Function Structure
```javascript
// netlify/functions/hello.js
exports.handler = async (event, context) => {
  return {
    statusCode: 200,
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: 'Hello from Netlify Function',
      path: event.path,
      method: event.httpMethod,
    }),
  };
};
```

### TypeScript Functions
```typescript
// netlify/functions/api.ts
import { Handler, HandlerEvent, HandlerContext } from '@netlify/functions';

interface RequestBody {
  name: string;
  email: string;
}

export const handler: Handler = async (
  event: HandlerEvent,
  context: HandlerContext
) => {
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      body: 'Method Not Allowed',
    };
  }

  const { name, email }: RequestBody = JSON.parse(event.body || '{}');

  return {
    statusCode: 200,
    body: JSON.stringify({
      message: `Hello ${name}`,
      email,
    }),
  };
};
```

### Advanced Function Patterns
```javascript
// netlify/functions/database.js
const { MongoClient } = require('mongodb');

let cachedDb = null;

async function connectToDatabase() {
  if (cachedDb) return cachedDb;

  const client = await MongoClient.connect(process.env.MONGODB_URI);
  cachedDb = client.db();
  return cachedDb;
}

exports.handler = async (event) => {
  const db = await connectToDatabase();
  const users = await db.collection('users').find({}).toArray();

  return {
    statusCode: 200,
    body: JSON.stringify(users),
  };
};
```

### Scheduled Functions
```javascript
// netlify/functions/scheduled.js
const { schedule } = require('@netlify/functions');

const handler = async () => {
  console.log('Running scheduled task');

  // Your scheduled logic
  await performBackup();

  return {
    statusCode: 200,
  };
};

// Run every day at midnight
exports.handler = schedule('0 0 * * *', handler);
```

### Background Functions
```javascript
// netlify/functions/background-task.js
// Auto-runs in background if response is 200 within 10s
exports.handler = async (event) => {
  // Long-running task
  await processLargeDataset();

  return {
    statusCode: 200,
  };
};

// Invoke: POST to /.netlify/functions/background-task
```

## Netlify Forms

### HTML Form
```html
<!-- Contact form -->
<form name="contact" method="POST" data-netlify="true">
  <input type="hidden" name="form-name" value="contact" />

  <label>Name: <input type="text" name="name" required /></label>
  <label>Email: <input type="email" name="email" required /></label>
  <label>Message: <textarea name="message" required></textarea></label>

  <button type="submit">Send</button>
</form>
```

### React Form
```jsx
// ContactForm.jsx
import { useState } from 'react';

export default function ContactForm() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: '',
  });

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch('/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        'form-name': 'contact',
        ...formData,
      }).toString(),
    });

    if (response.ok) {
      alert('Thank you for your message!');
    }
  };

  return (
    <form name="contact" onSubmit={handleSubmit} data-netlify="true">
      <input type="hidden" name="form-name" value="contact" />
      {/* Form fields */}
    </form>
  );
}
```

### Form Features
```html
<!-- Spam filtering with honeypot -->
<form name="contact" method="POST" data-netlify="true" data-netlify-honeypot="bot-field">
  <input type="hidden" name="form-name" value="contact" />
  <p class="hidden">
    <label>Don't fill this out: <input name="bot-field" /></label>
  </p>
  <!-- Form fields -->
</form>

<!-- reCAPTCHA v2 -->
<form name="contact" method="POST" data-netlify="true" data-netlify-recaptcha="true">
  <div data-netlify-recaptcha="true"></div>
  <button type="submit">Submit</button>
</form>

<!-- File uploads -->
<form name="file-upload" method="POST" data-netlify="true" enctype="multipart/form-data">
  <input type="file" name="file" />
  <button type="submit">Upload</button>
</form>
```

### Form Notifications
```toml
# netlify.toml
[[plugins]]
  package = "@netlify/plugin-emails"

  [plugins.inputs]
    formName = "contact"
    to = "admin@example.com"
    subject = "New contact form submission"
```

## Netlify Identity

### Enable Identity
```javascript
// Add to HTML
<script src="https://identity.netlify.com/v1/netlify-identity-widget.js"></script>

// Initialize
if (window.netlifyIdentity) {
  window.netlifyIdentity.on('init', user => {
    if (!user) {
      window.netlifyIdentity.on('login', () => {
        document.location.href = '/admin/';
      });
    }
  });
}
```

### React Integration
```jsx
// useNetlifyIdentity.js
import { useEffect, useState } from 'react';

export function useNetlifyIdentity() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const netlifyIdentity = window.netlifyIdentity;

    netlifyIdentity.on('init', user => setUser(user));
    netlifyIdentity.on('login', user => setUser(user));
    netlifyIdentity.on('logout', () => setUser(null));

    netlifyIdentity.init();
  }, []);

  return {
    user,
    login: () => window.netlifyIdentity.open('login'),
    logout: () => window.netlifyIdentity.logout(),
    signup: () => window.netlifyIdentity.open('signup'),
  };
}
```

### Protected Functions
```javascript
// netlify/functions/protected.js
exports.handler = async (event, context) => {
  const { user } = context.clientContext;

  if (!user) {
    return {
      statusCode: 401,
      body: 'Unauthorized',
    };
  }

  return {
    statusCode: 200,
    body: JSON.stringify({
      message: 'Protected data',
      user: user.email,
    }),
  };
};
```

## Redirects and Rewrites

### _redirects File
```text
# _redirects file in publish directory

# Redirect with status code
/old-path  /new-path  301

# Rewrite (proxy)
/api/*  https://api.example.com/:splat  200

# SPA fallback
/*  /index.html  200

# Force HTTPS
http://example.com/*  https://example.com/:splat  301!

# Conditional redirects
/news/*  /blog/:splat  302  Country=us

# Role-based redirects
/admin/*  /admin/dashboard  200!  Role=admin
/admin/*  /unauthorized  401
```

### netlify.toml Redirects
```toml
[[redirects]]
  from = "/old-path"
  to = "/new-path"
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

[[redirects]]
  from = "/admin/*"
  to = "/admin/dashboard"
  status = 200
  conditions = {Role = ["admin"]}

# Proxy with headers
[[redirects]]
  from = "/proxy/*"
  to = "https://backend.com/:splat"
  status = 200
  force = true
  [redirects.headers]
    X-From = "Netlify"
```

### Custom Headers
```toml
[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    Content-Security-Policy = "default-src 'self'"

[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
```

## Deploy Previews

### Automatic Preview URLs
```toml
# netlify.toml
[context.deploy-preview]
  command = "npm run build:preview"

[context.deploy-preview.environment]
  NODE_ENV = "preview"
  API_URL = "https://api-staging.example.com"
```

### Branch Deploys
```toml
# Deploy specific branches
[context.staging]
  command = "npm run build:staging"

[context.staging.environment]
  API_URL = "https://api-staging.example.com"

# Branch pattern matching
[context.branch-deploy]
  command = "npm run build"
```

### Deploy Notifications
```bash
# GitHub PR comments
# Slack notifications
# Email notifications
# Configured in Netlify UI
```

## Split Testing (A/B Testing)

### Configuration
```toml
# netlify.toml
[[redirects]]
  from = "/*"
  to = "/version-a/:splat"
  status = 200
  conditions = {Cookie = ["ab_test=a"]}
  force = true

[[redirects]]
  from = "/*"
  to = "/version-b/:splat"
  status = 200
  conditions = {Cookie = ["ab_test=b"]}
  force = true

# 50/50 split
[[redirects]]
  from = "/*"
  to = "/version-a/:splat"
  status = 200!
  percentage = 50

[[redirects]]
  from = "/*"
  to = "/version-b/:splat"
  status = 200!
```

## Edge Functions

### Deno Runtime
```typescript
// netlify/edge-functions/hello.ts
import type { Context } from "https://edge.netlify.com";

export default async (request: Request, context: Context) => {
  const url = new URL(request.url);

  return new Response(`Hello from ${url.pathname}`, {
    headers: { "content-type": "text/html" },
  });
};

export const config = { path: "/hello" };
```

### Geolocation
```typescript
// netlify/edge-functions/geo.ts
import type { Context } from "https://edge.netlify.com";

export default async (request: Request, context: Context) => {
  const { city, country } = context.geo;

  return Response.json({
    location: `${city}, ${country}`,
  });
};
```

### Transform Response
```typescript
// netlify/edge-functions/transform.ts
import type { Context } from "https://edge.netlify.com";

export default async (request: Request, context: Context) => {
  const response = await context.next();
  const text = await response.text();

  // Modify HTML
  const modified = text.replace(
    '</body>',
    '<script>console.log("Injected by edge");</script></body>'
  );

  return new Response(modified, response);
};

export const config = { path: "/*" };
```

## Custom Domains and SSL

### Add Custom Domain
```bash
# Via CLI
netlify domains:add example.com

# DNS Configuration
# A record: 75.2.60.5
# CNAME: <site-name>.netlify.app

# Verify domain
netlify domains:verify example.com
```

### SSL Certificates
```toml
# Automatic HTTPS (default)
# Free Let's Encrypt certificates
# Auto-renewal

# Force HTTPS redirect
[[redirects]]
  from = "http://example.com/*"
  to = "https://example.com/:splat"
  status = 301
  force = true
```

## Analytics

### Netlify Analytics
```html
<!-- Automatically injected, no code needed -->
<!-- Server-side analytics, no client-side JS -->
```

### Custom Analytics
```javascript
// Track custom events
function trackEvent(eventName, data) {
  fetch('/.netlify/functions/analytics', {
    method: 'POST',
    body: JSON.stringify({ event: eventName, ...data }),
  });
}

trackEvent('button_click', { button: 'signup' });
```

## CLI Advanced Usage

### Development Server
```bash
# Run functions locally
netlify dev

# Specific port
netlify dev --port 3000

# Live session sharing
netlify dev --live

# Functions only
netlify functions:serve
```

### Site Management
```bash
# Link existing site
netlify link

# Create new site
netlify sites:create

# List sites
netlify sites:list

# Site info
netlify status

# Open site in browser
netlify open
```

### Deploy Management
```bash
# List deploys
netlify deploy:list

# Rollback to previous deploy
netlify rollback

# Cancel deploy
netlify deploy:cancel <deploy-id>
```

## Git Integration

### Continuous Deployment
```toml
# netlify.toml
[build]
  command = "npm run build"
  publish = "dist"

# Auto-publish on Git push
# Production: main/master branch
# Previews: all pull requests
# Branch deploys: configured branches
```

### Deploy Hooks
```bash
# Trigger builds via webhook
curl -X POST -d {} https://api.netlify.com/build_hooks/<hook-id>

# Scheduled builds (use external cron + webhook)
```

## Best Practices

### Performance Optimization
```toml
# Enable processing
[build.processing]
  skip_processing = false

[build.processing.css]
  bundle = true
  minify = true

[build.processing.js]
  bundle = true
  minify = true

[build.processing.images]
  compress = true

# Asset optimization
[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
```

### Security Headers
```toml
[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    X-XSS-Protection = "1; mode=block"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Permissions-Policy = "geolocation=(), microphone=(), camera=()"
    Content-Security-Policy = """
      default-src 'self';
      script-src 'self' 'unsafe-inline';
      style-src 'self' 'unsafe-inline';
      img-src 'self' data: https:;
      font-src 'self' data:;
    """
```

### Function Best Practices
```javascript
// Keep functions lightweight
// Use connection pooling
// Cache external API responses
// Set appropriate timeouts
// Handle errors gracefully

exports.handler = async (event) => {
  try {
    // Set timeout
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 8000);

    const response = await fetch(API_URL, {
      signal: controller.signal,
    });

    clearTimeout(timeout);

    return {
      statusCode: 200,
      body: JSON.stringify(await response.json()),
    };
  } catch (error) {
    console.error('Function error:', error);

    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Internal server error' }),
    };
  }
};
```

### Build Optimization
```toml
[build]
  command = "npm run build"
  publish = "dist"

  # Skip builds when not needed
  ignore = """
    git diff --quiet $CACHED_COMMIT_REF $COMMIT_REF -- . ':(exclude)docs/' ':(exclude)*.md'
  """

# Cache dependencies
[build.environment]
  NPM_FLAGS = "--legacy-peer-deps"
  NODE_OPTIONS = "--max-old-space-size=4096"
```

### Monorepo Support
```toml
# netlify.toml
[build]
  base = "packages/web"
  command = "npm run build"
  publish = "dist"

  # Only build when package changes
  ignore = "git diff --quiet $CACHED_COMMIT_REF $COMMIT_REF packages/web"
```

## Common Patterns

### SPA with API Proxy
```toml
[build]
  command = "npm run build"
  publish = "build"
  functions = "netlify/functions"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/:splat"
  status = 200

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Microsite with Subfolder
```toml
[[redirects]]
  from = "/blog/*"
  to = "https://blog.example.com/:splat"
  status = 200
  force = true
```

### Authentication Gateway
```toml
[[redirects]]
  from = "/app/*"
  to = "/app/dashboard"
  status = 200
  conditions = {Role = ["user"]}

[[redirects]]
  from = "/app/*"
  to = "/login"
  status = 302
```

---

**Summary**: Netlify provides a complete JAMstack platform with static hosting, serverless functions, forms, and identity management. Key strengths include atomic deploys, instant cache invalidation, deploy previews, and built-in CDN. Configure via netlify.toml for builds, redirects, headers, and environment-specific settings. Leverage serverless functions for backend logic, forms for user input, and Edge Functions for edge computing. Best practices include performance optimization, security headers, and efficient build configurations.