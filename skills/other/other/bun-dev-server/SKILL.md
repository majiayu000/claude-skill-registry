---
name: bun-dev-server
description: Set up high-performance development servers with Hot Module Replacement. Use when creating dev servers for web apps, setting up React Fast Refresh, or configuring API servers with live reload.
compatibility: Requires Bun 1.0+
allowed-tools: ["Bash", "Write", "Read"]
metadata:
  author: dale
  category: bun-runtime
  tags: [bun, dev-server, hmr, react, hot-reload]
---

# Bun Development Server Setup

You are assisting with setting up a high-performance development server using Bun.serve with Hot Module Replacement (HMR) and React Fast Refresh.

## Workflow

### 1. Determine Server Type

Ask the user what type of development server they need:

- **React/Frontend App**: SPA with React Fast Refresh
- **API Server**: REST/GraphQL API with auto-reload
- **Full-Stack App**: Frontend + API combined
- **Static Server**: File server with live reload

### 2. Check Prerequisites

```bash
# Verify Bun installation
bun --version

# Check if project has package.json
ls -la package.json
```

If no package.json exists, suggest running `bun init` first.

### 3. Install Dependencies

**For React Apps:**
```bash
bun add react react-dom
bun add -d @types/react @types/react-dom
```

**For API with Hono (recommended):**
```bash
bun add hono
```

**For Full-Stack:**
```bash
bun add react react-dom hono
bun add -d @types/react @types/react-dom
```

### 4. Create Server Configuration

#### React Development Server

Create `server.ts` in the project root:

```typescript
import type { ServerWebSocket } from "bun";

const clients = new Set<ServerWebSocket<unknown>>();

const server = Bun.serve({
  port: 3000,

  async fetch(request, server) {
    const url = new URL(request.url);

    // WebSocket for HMR
    if (url.pathname === "/_hmr") {
      const upgraded = server.upgrade(request);
      if (upgraded) return undefined;
      return new Response("WebSocket upgrade failed", { status: 500 });
    }

    // Serve index.html for SPA routing
    if (url.pathname === "/" || !url.pathname.includes(".")) {
      return new Response(
        Bun.file("public/index.html"),
        { headers: { "Content-Type": "text/html" } }
      );
    }

    // Serve static files
    const filePath = `public${url.pathname}`;
    const file = Bun.file(filePath);

    if (await file.exists()) {
      return new Response(file);
    }

    return new Response("Not Found", { status: 404 });
  },

  websocket: {
    open(ws) {
      clients.add(ws);
      console.log("HMR client connected");
    },

    close(ws) {
      clients.delete(ws);
      console.log("HMR client disconnected");
    },

    message(ws, message) {
      // Handle client messages if needed
    },
  },
});

console.log(`🚀 Dev server running at http://localhost:${server.port}`);

// Watch for file changes
const watcher = Bun.file.watch(import.meta.dir + "/src", {
  recursive: true,
});

for await (const event of watcher) {
  if (event.kind === "change" && event.path.endsWith(".tsx")) {
    console.log(`📝 File changed: ${event.path}`);

    // Notify all connected clients to reload
    for (const client of clients) {
      client.send(JSON.stringify({ type: "reload" }));
    }
  }
}
```

Create `public/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bun + React App</title>
</head>
<body>
  <div id="root"></div>
  <script type="module" src="/src/index.tsx"></script>

  <!-- HMR Client -->
  <script>
    const ws = new WebSocket('ws://localhost:3000/_hmr');

    ws.addEventListener('message', (event) => {
      const data = JSON.parse(event.data);

      if (data.type === 'reload') {
        console.log('🔄 Reloading...');
        window.location.reload();
      }
    });

    ws.addEventListener('close', () => {
      console.log('❌ HMR connection lost. Reconnecting...');
      setTimeout(() => window.location.reload(), 1000);
    });
  </script>
</body>
</html>
```

Create `src/index.tsx`:

```typescript
import { render } from 'react-dom';
import App from './App';

const root = document.getElementById('root');
render(<App />, root);
```

Create `src/App.tsx`:

```typescript
export default function App() {
  return (
    <div>
      <h1>Welcome to Bun + React!</h1>
      <p>Edit src/App.tsx to see HMR in action</p>
    </div>
  );
}
```

#### API Server with Hono

Create `server.ts`:

```typescript
import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { logger } from 'hono/logger';

const app = new Hono();

// Middleware
app.use('*', cors());
app.use('*', logger());

// Routes
app.get('/', (c) => {
  return c.json({ message: 'Welcome to Bun API' });
});

app.get('/api/health', (c) => {
  return c.json({ status: 'ok', timestamp: Date.now() });
});

// Example POST endpoint
app.post('/api/users', async (c) => {
  const body = await c.req.json();
  return c.json({ created: true, data: body }, 201);
});

// Start server
const server = Bun.serve({
  port: process.env.PORT || 3000,
  fetch: app.fetch,
});

console.log(`🚀 API server running at http://localhost:${server.port}`);
```

#### Full-Stack Server

Create `server.ts`:

```typescript
import { Hono } from 'hono';
import { serveStatic } from 'hono/bun';

const app = new Hono();

// API routes
const api = new Hono();

api.get('/health', (c) => c.json({ status: 'ok' }));
api.get('/users', (c) => c.json({ users: [] }));

app.route('/api', api);

// Serve static files
app.use('/*', serveStatic({ root: './public' }));

// SPA fallback
app.get('*', (c) => c.html(Bun.file('public/index.html')));

const server = Bun.serve({
  port: 3000,
  fetch: app.fetch,
});

console.log(`🚀 Full-stack server at http://localhost:${server.port}`);
```

### 5. Configure React Fast Refresh (Advanced)

For true React Fast Refresh, create `hmr-runtime.ts`:

```typescript
// React Fast Refresh runtime
let timeout: Timer | null = null;

export function refresh() {
  if (timeout) clearTimeout(timeout);

  timeout = setTimeout(() => {
    // Re-import the App component
    import('./App.tsx?t=' + Date.now()).then((module) => {
      const { render } = require('react-dom');
      const root = document.getElementById('root');
      render(module.default(), root);
    });
  }, 100);
}

// Listen for HMR events
if (import.meta.hot) {
  import.meta.hot.accept(() => {
    refresh();
  });
}
```

### 6. Environment Configuration

Create `.env.development`:

```bash
# Server
PORT=3000
NODE_ENV=development

# API
API_URL=http://localhost:3000/api

# Features
ENABLE_HMR=true
```

Create `.env.production`:

```bash
# Server
PORT=8080
NODE_ENV=production

# API
API_URL=https://api.example.com

# Features
ENABLE_HMR=false
```

Load environment in `server.ts`:

```typescript
// Environment is loaded automatically by Bun
const isDev = process.env.NODE_ENV === 'development';
const port = process.env.PORT || 3000;
```

### 7. Update package.json Scripts

Add development scripts:

```json
{
  "scripts": {
    "dev": "bun run --hot server.ts",
    "dev:watch": "bun run --watch server.ts",
    "start": "NODE_ENV=production bun run server.ts",
    "build": "bun build src/index.tsx --outdir=dist --minify",
    "clean": "rm -rf dist"
  }
}
```

**Script explanations:**
- `dev`: Run with hot reload (restarts on file changes)
- `dev:watch`: Watch mode (faster, but doesn't reload on crash)
- `start`: Production mode
- `build`: Build frontend for production

### 8. Configure TypeScript

Update `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "types": ["bun-types"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "allowImportingTsExtensions": true,
    "noEmit": true,
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src/**/*", "server.ts"]
}
```

### 9. Create Project Structure

Generate complete project structure:

```
project/
├── server.ts              # Development server
├── src/
│   ├── index.tsx         # App entry point
│   ├── App.tsx           # Main component
│   ├── components/       # React components
│   └── styles/           # CSS files
├── public/
│   ├── index.html        # HTML template
│   └── assets/           # Static assets
├── .env.development
├── .env.production
├── package.json
├── tsconfig.json
└── README.md
```

### 10. Advanced: HTTPS for Local Development

For HTTPS support (needed for some browser APIs):

```typescript
import { readFileSync } from 'fs';

const server = Bun.serve({
  port: 3000,
  tls: {
    cert: readFileSync('./localhost.pem'),
    key: readFileSync('./localhost-key.pem'),
  },
  fetch: app.fetch,
});

console.log(`🔒 HTTPS server at https://localhost:${server.port}`);
```

Generate certificates with:
```bash
# Install mkcert first: brew install mkcert
mkcert -install
mkcert localhost 127.0.0.1 ::1
```

### 11. Proxy Configuration (for existing backends)

If user needs to proxy API requests to another server:

```typescript
const app = new Hono();

// Proxy /api requests to backend
app.all('/api/*', async (c) => {
  const url = new URL(c.req.url);
  const backendUrl = `http://localhost:8080${url.pathname}${url.search}`;

  const response = await fetch(backendUrl, {
    method: c.req.method,
    headers: c.req.raw.headers,
    body: c.req.method !== 'GET' ? await c.req.raw.text() : undefined,
  });

  return new Response(response.body, {
    status: response.status,
    headers: response.headers,
  });
});
```

## Testing the Setup

After creation, guide user to test:

```bash
# 1. Start dev server
bun run dev

# 2. Open browser
open http://localhost:3000

# 3. Make a change to src/App.tsx
# 4. Verify HMR reloads the page

# 5. Test API endpoints
curl http://localhost:3000/api/health
```

## Troubleshooting

### HMR not working

```typescript
// Check if WebSocket connection is established
// Open browser console and look for:
// "HMR client connected"

// If not, verify:
// 1. Port is correct
// 2. No firewall blocking WebSocket
// 3. Server is running with --hot flag
```

### Port already in use

```bash
# Find process using port 3000
lsof -ti:3000

# Kill the process
kill -9 $(lsof -ti:3000)

# Or use a different port
PORT=3001 bun run dev
```

### CORS issues

Add CORS headers to server:

```typescript
app.use('*', cors({
  origin: 'http://localhost:3000',
  credentials: true,
}));
```

## Performance Tips

1. **Use --hot for development**: Faster than --watch for most cases
2. **Minimize file watcher scope**: Watch only src/ directory
3. **Use HTTP/2**: Enable for faster parallel loading
4. **Cache static assets**: Add Cache-Control headers

```typescript
app.use('/assets/*', async (c, next) => {
  await next();
  c.header('Cache-Control', 'public, max-age=31536000');
});
```

## Completion Checklist

- ✅ Development server created
- ✅ HMR configured and tested
- ✅ Environment variables set up
- ✅ Package.json scripts added
- ✅ Project structure organized
- ✅ TypeScript configured
- ✅ Browser successfully connects
- ✅ File changes trigger reload

## Next Steps

Suggest to the user:
1. Add error boundaries for better error handling
2. Set up ESLint and Prettier
3. Configure path aliases in tsconfig.json
4. Add development vs production builds
5. Consider adding bun-test for testing
