---
name: react-tailwind-vigil-ui
description: React 18 + Vite + Tailwind CSS v4 frontend development for Vigil Guard v2.0.0 configuration interface. Use when building UI components, creating forms, implementing API integration for 3-branch detection, working with JWT authentication, managing routing, handling ETag-based concurrency control, implementing branch health monitoring, arbiter configuration, or fixing controlled component issues with getCurrentValue() pattern (CRITICAL for Select/Toggle components).
version: 2.0.0
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Vigil Guard Web UI Development (v2.0.0)

## Overview

Frontend development guidance for Vigil Guard's React-based configuration and monitoring interface, built with Vite, TypeScript, and Tailwind CSS v4, featuring JWT authentication, RBAC, 3-branch detection monitoring, arbiter configuration, and Grafana integration.

## When to Use This Skill

- Building new React components
- Creating configuration forms with validation
- Implementing API client integration
- Working with AuthContext and JWT tokens
- Setting up protected routes with RBAC
- Styling with Tailwind CSS Design System
- Managing state (AuthContext, form state)
- Handling ETag concurrency for config updates
- Integrating Grafana dashboards
- Building 3-branch health monitoring (v2.0.0)
- Creating arbiter configuration UI (v2.0.0)
- Debugging CORS or proxy issues

## v2.0.0 Architecture Integration

### 3-Branch Detection UI Components

The frontend can display and configure the 3-branch detection system:

```typescript
// Branch service information (v2.0.0)
const BRANCH_INFO = {
  A: { name: 'Heuristics', port: 5005, weight: 0.30, timeout: 1000 },
  B: { name: 'Semantic', port: 5006, weight: 0.35, timeout: 2000 },
  C: { name: 'LLM Guard', port: 8000, weight: 0.35, timeout: 3000 }
};
```

### Branch Health Monitor Component

```typescript
// src/components/BranchHealth.tsx
import { useState, useEffect } from 'react';
import api from '../lib/api';

interface BranchStatus {
  name: string;
  port: number;
  healthy: boolean;
}

interface BranchHealthResponse {
  branch_a: BranchStatus;
  branch_b: BranchStatus;
  branch_c: BranchStatus;
}

export default function BranchHealth() {
  const [health, setHealth] = useState<BranchHealthResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await api.get('/api/health/branches');
        setHealth(response.data);
      } catch (error) {
        console.error('Branch health check failed:', error);
      } finally {
        setLoading(false);
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 30000); // Refresh every 30s
    return () => clearInterval(interval);
  }, []);

  if (loading) return <div className="animate-pulse">Checking branches...</div>;

  return (
    <div className="grid grid-cols-3 gap-4">
      {health && Object.entries(health).map(([key, branch]) => (
        <div
          key={key}
          className={`p-4 rounded-lg border ${
            branch.healthy
              ? 'bg-green-900/20 border-green-600'
              : 'bg-red-900/20 border-red-600'
          }`}
        >
          <div className="flex items-center justify-between">
            <span className="text-text-primary font-semibold">{branch.name}</span>
            <span className={`w-3 h-3 rounded-full ${
              branch.healthy ? 'bg-green-500' : 'bg-red-500'
            }`} />
          </div>
          <div className="text-text-secondary text-sm mt-1">
            Port: {branch.port}
          </div>
        </div>
      ))}
    </div>
  );
}
```

### Arbiter Configuration Component

```typescript
// src/components/ArbiterConfig.tsx
import { useState } from 'react';

interface ArbiterWeights {
  heuristics: number;  // Branch A
  semantic: number;    // Branch B
  llm_guard: number;   // Branch C
}

interface ArbiterThresholds {
  allow_max: number;
  sanitize_max: number;
  block_min: number;
}

export default function ArbiterConfig({
  weights,
  thresholds,
  onChange
}: {
  weights: ArbiterWeights;
  thresholds: ArbiterThresholds;
  onChange: (type: 'weights' | 'thresholds', values: any) => void;
}) {
  return (
    <div className="bg-surface-dark border border-border-subtle rounded-lg p-6">
      <h3 className="text-text-primary text-lg font-semibold mb-4">
        Arbiter v2 Configuration
      </h3>

      {/* Branch Weights */}
      <div className="mb-6">
        <h4 className="text-text-secondary mb-2">Branch Weights (must sum to 1.0)</h4>
        <div className="grid grid-cols-3 gap-4">
          <div>
            <label className="text-text-muted text-sm">Heuristics (A)</label>
            <input
              type="number"
              step="0.05"
              min="0"
              max="1"
              value={weights.heuristics}
              onChange={(e) => onChange('weights', {
                ...weights,
                heuristics: parseFloat(e.target.value)
              })}
              className="bg-surface-darker border border-border-subtle text-text-primary rounded-md px-3 py-2 w-full"
            />
          </div>
          <div>
            <label className="text-text-muted text-sm">Semantic (B)</label>
            <input
              type="number"
              step="0.05"
              min="0"
              max="1"
              value={weights.semantic}
              onChange={(e) => onChange('weights', {
                ...weights,
                semantic: parseFloat(e.target.value)
              })}
              className="bg-surface-darker border border-border-subtle text-text-primary rounded-md px-3 py-2 w-full"
            />
          </div>
          <div>
            <label className="text-text-muted text-sm">LLM Guard (C)</label>
            <input
              type="number"
              step="0.05"
              min="0"
              max="1"
              value={weights.llm_guard}
              onChange={(e) => onChange('weights', {
                ...weights,
                llm_guard: parseFloat(e.target.value)
              })}
              className="bg-surface-darker border border-border-subtle text-text-primary rounded-md px-3 py-2 w-full"
            />
          </div>
        </div>
      </div>

      {/* Decision Thresholds */}
      <div>
        <h4 className="text-text-secondary mb-2">Decision Thresholds</h4>
        <div className="grid grid-cols-3 gap-4">
          <div>
            <label className="text-text-muted text-sm">ALLOW Max</label>
            <input
              type="number"
              value={thresholds.allow_max}
              onChange={(e) => onChange('thresholds', {
                ...thresholds,
                allow_max: parseInt(e.target.value)
              })}
              className="bg-surface-darker border border-border-subtle text-text-primary rounded-md px-3 py-2 w-full"
            />
          </div>
          <div>
            <label className="text-text-muted text-sm">SANITIZE Max</label>
            <input
              type="number"
              value={thresholds.sanitize_max}
              onChange={(e) => onChange('thresholds', {
                ...thresholds,
                sanitize_max: parseInt(e.target.value)
              })}
              className="bg-surface-darker border border-border-subtle text-text-primary rounded-md px-3 py-2 w-full"
            />
          </div>
          <div>
            <label className="text-text-muted text-sm">BLOCK Min</label>
            <input
              type="number"
              value={thresholds.block_min}
              onChange={(e) => onChange('thresholds', {
                ...thresholds,
                block_min: parseInt(e.target.value)
              })}
              className="bg-surface-darker border border-border-subtle text-text-primary rounded-md px-3 py-2 w-full"
            />
          </div>
        </div>
      </div>
    </div>
  );
}
```

## Critical: Reverse Proxy Architecture

**PRODUCTION ACCESS**: All requests go through Caddy reverse proxy!

```
Client -> http://localhost/ui/
  |
Caddy (:80) strips /ui prefix
  |
Nginx (:80 internal) serves React SPA
  |
Vite build (base: "/ui/")
```

**Key Points:**
- Vite config: `base: "/ui/"` (assets have /ui/ prefix in HTML)
- Caddy strips `/ui` before proxying to nginx
- Nginx receives requests WITHOUT /ui/ prefix
- Keep nginx config simple: `try_files $uri $uri/ /index.html`
- **Never add nginx location blocks for /ui/**

## Tech Stack

- React 18.3.1
- Vite 6.0.1 (build tool, dev server)
- TypeScript 5.6.3
- Tailwind CSS v4.0 (Design System)
- React Router 7.1.1
- JWT authentication + localStorage

## Project Structure

```
services/web-ui/frontend/
├── src/
│   ├── components/           # React components
│   │   ├── Login.tsx        # Auth form
│   │   ├── UserManagement.tsx  # Admin panel
│   │   ├── ConfigEditor.tsx    # Config UI
│   │   ├── ConfigSection.tsx   # Variable group UI
│   │   ├── BranchHealth.tsx    # v2.0.0: Branch monitoring
│   │   ├── ArbiterConfig.tsx   # v2.0.0: Arbiter settings
│   │   ├── PIISettings.tsx     # PII detection config
│   │   ├── GrafanaEmbed.tsx    # Monitoring
│   │   └── TopBar.tsx          # Nav header
│   ├── contexts/
│   │   └── AuthContext.tsx  # Global auth state
│   ├── lib/
│   │   └── api.ts           # Backend API client
│   ├── spec/
│   │   └── variables.json   # Config variable specs
│   ├── App.tsx              # Main app + routing
│   └── main.tsx             # Entry point
├── public/
│   └── docs/                # GUI help system
├── vite.config.ts           # Vite configuration
├── tailwind.config.ts       # Design System
└── nginx.conf               # Production server
```

## Common Tasks

### Create New Component

```typescript
// src/components/MyComponent.tsx
import { useState } from 'react';

interface MyComponentProps {
  title: string;
  onAction?: () => void;
}

export default function MyComponent({ title, onAction }: MyComponentProps) {
  const [state, setState] = useState<string>('');

  return (
    <div className="bg-surface-base border border-border-subtle rounded-lg p-4">
      <h2 className="text-text-primary text-lg font-semibold">{title}</h2>
      <button
        onClick={onAction}
        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md"
      >
        Action
      </button>
    </div>
  );
}
```

### Add Protected Route

```typescript
// src/App.tsx
import { useAuth } from './contexts/AuthContext';

function App() {
  const { user } = useAuth();

  return (
    <Routes>
      <Route path="/login" element={<Login />} />

      {/* Protected route with permission check */}
      <Route
        path="/config"
        element={
          user?.permissions.can_view_configuration ?
            <ConfigEditor /> :
            <Navigate to="/" />
        }
      />

      {/* v2.0.0: Branch monitoring route */}
      <Route
        path="/branches"
        element={
          user?.permissions.can_view_monitoring ?
            <BranchHealth /> :
            <Navigate to="/" />
        }
      />
    </Routes>
  );
}
```

### API Integration

```typescript
// Use API client from lib/api.ts
import api from '../lib/api';

async function fetchConfigFiles() {
  try {
    const response = await api.get('/api/files');
    return response.data;
  } catch (error) {
    if (error.response?.status === 401) {
      // Token expired, redirect to login
      window.location.href = '/login';
    }
    throw error;
  }
}

// v2.0.0: Fetch branch health
async function fetchBranchHealth() {
  const response = await api.get('/api/health/branches');
  return response.data;
}

// v2.0.0: Test heuristics service
async function testHeuristics(text: string) {
  const response = await api.post('/api/analyze/heuristics', {
    text,
    request_id: `test-${Date.now()}`
  });
  return response.data;
}
```

### ETag Concurrency Control

```typescript
// Optimistic locking for config saves
const [etag, setEtag] = useState<string>('');

// 1. Fetch with ETag
const response = await api.get('/api/parse/unified_config.json');
setEtag(response.headers['etag']);
setData(response.data);

// 2. Save with ETag validation
try {
  await api.post('/api/save', {
    name: 'unified_config.json',
    content: updatedData,
    etag: etag,
    username: user.username
  });
} catch (error) {
  if (error.response?.status === 412) {
    alert('File was modified by another user. Please refresh.');
  }
}
```

## Design System (Tailwind CSS v4)

### Semantic Color Tokens

```css
/* Background colors */
bg-surface-base        /* Main background #0F1419 */
bg-surface-dark        /* Cards, panels #131A21 */
bg-surface-darker      /* Sidebar #0C1117 */

/* Text colors */
text-text-primary      /* Main text #E6EDF3 */
text-text-secondary    /* Muted text #8B949E */
text-text-muted        /* Disabled text #57606A */

/* Border colors */
border-border-subtle   /* Dividers #30363D */
border-border-muted    /* Inactive borders #21262D */

/* Accent colors */
bg-blue-600           /* Primary actions */
bg-green-600          /* Success states */
bg-red-600            /* Danger/errors */
bg-yellow-600         /* Warnings */
```

### Reusable Components

```typescript
// Button component
<button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md transition-colors">
  Save Changes
</button>

// Card container
<div className="bg-surface-dark border border-border-subtle rounded-lg p-6">
  Content
</div>

// Form input
<input
  type="text"
  className="bg-surface-darker border border-border-subtle text-text-primary rounded-md px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
/>

// v2.0.0: Branch status indicator
<span className={`w-3 h-3 rounded-full ${healthy ? 'bg-green-500' : 'bg-red-500'}`} />
```

## Authentication Flow

### JWT Token Management

```typescript
// AuthContext provides:
const { user, login, logout, loading } = useAuth();

// Login
await login(username, password);
// Sets token in localStorage
// Updates AuthContext.user

// Logout
logout();
// Removes token from localStorage
// Clears AuthContext.user
// Redirects to /login
```

### Permission Checks

```typescript
// Component-level
{user?.permissions.can_manage_users && (
  <UserManagement />
)}

// Route-level (see Add Protected Route above)
```

### API Token Injection

```typescript
// api.ts automatically adds JWT to headers
const token = localStorage.getItem('token');
if (token) {
  config.headers.Authorization = `Bearer ${token}`;
}
```

## Configuration Forms

### Variable Groups (from spec/variables.json)

1. Quick Settings - Test mode, logging
2. Detection Tuning - Thresholds, scoring, arbiter weights (v2.0.0)
3. Performance - Timeouts, limits, branch timeouts (v2.0.0)
4. Advanced - Normalization, sanitization
5. PII Detection - Presidio configuration
6. Branch Configuration - 3-branch settings (v2.0.0)

### CRITICAL: Controlled vs Uncontrolled Components

**Problem:** ConfigSection uses TWO separate state arrays:
- `resolveOut` - Original values from server (`/api/resolve`)
- `changes` - Pending user changes (not yet saved)

**Why This Matters:**

1. **Select components (boolean/enum)** are **controlled** - use `value` prop
2. **Input/textarea components** are **uncontrolled** - use `defaultValue` prop

**WRONG (Bug):**
```typescript
// Select always shows original value, ignoring user changes!
<Select value={resolveOut[i].value} onChange={handleChange} />
```

**CORRECT:**
```typescript
// Helper function to merge original + changes
function getCurrentValue(file: string, mapping: any, originalValue: any) {
  const fileChanges = changes.find(c => c.file === file);
  if (!fileChanges) return originalValue;

  const change = fileChanges.updates.find(u =>
    mapping.path ? u.path === mapping.path :
    u.key === mapping.key && (u.section ?? null) === (mapping.section ?? null)
  );

  return change ? change.value : originalValue;
}

// Use merged value in Select
<Select value={getCurrentValue(file, mapping, resolveOut[i].value)} />
```

**Symptoms of Missing getCurrentValue():**
- Boolean toggles don't switch visually when clicked
- Dropdown selections revert to original value
- User sees old value even though onChange fires
- Changes ARE tracked in state but UI doesn't reflect them

**Implementation Reference:** See `services/web-ui/frontend/src/components/ConfigSection.tsx` lines 59-72

### Form Pattern

```typescript
const [resolveOut, setResolveOut] = useState<any[]>([]); // Original values
const [changes, setChanges] = useState<Chg[]>([]);       // Pending changes

// Fetch current values
const loadConfig = async () => {
  const response = await api.get('/api/resolve');
  setResolveOut(response.data);
};

// Update value (tracks in changes, NOT resolveOut)
const handleChange = (varName: string, file: string, update: any) => {
  setChanges(prev => {
    const idx = prev.findIndex(c => c.file === file);
    if (idx === -1) return [...prev, { file, updates: [update] }];
    const merged = { ...prev[idx] };
    merged.updates = mergeUpdates(merged.updates, update);
    const clone = [...prev]; clone[idx] = merged; return clone;
  });
};

// Save with validation
const handleSave = async () => {
  await api.post('/api/save', {
    changes: changes,
    changeTag: user.username
  });
  setChanges([]); // Clear pending changes
  await loadConfig(); // Reload from server
};
```

## Grafana Integration

### Embed Panel

```typescript
<iframe
  src={`http://localhost:3001/d/vigil-guard/dashboard?panelId=1&orgId=1&theme=dark&kiosk`}
  className="w-full h-96 border-0"
  title="Grafana Dashboard"
/>
```

**Requirements:**
- Grafana config: `GF_SECURITY_ALLOW_EMBEDDING=true`
- Use `kiosk` mode to hide Grafana UI
- Add `theme=dark` for consistency

### v2.0.0 Branch Metrics Dashboard

```typescript
// Embed branch comparison panel
<iframe
  src={`http://localhost:3001/d/vigil-guard/dashboard?panelId=branch-scores&orgId=1&theme=dark&kiosk`}
  className="w-full h-96 border-0"
  title="Branch Score Comparison"
/>
```

## Development Workflow

### Local Development

```bash
cd services/web-ui/frontend

# Install dependencies
npm install

# Start dev server (http://localhost:5173)
npm run dev

# TypeScript type checking
npx tsc --noEmit

# Build for production
npm run build
```

### Docker Build

```bash
# Build frontend image
docker-compose build web-ui-frontend

# Or full stack
docker-compose up --build
```

## Troubleshooting

### CORS Errors

```typescript
// Backend (services/web-ui/backend/src/server.ts)
app.use(cors({
  origin: /^http:\/\/localhost(:\d+)?$/, // Any localhost port
  credentials: true
}));
```

### Proxy 404 Errors

```typescript
// Check Vite config
export default {
  base: "/ui/", // Must match Caddy route
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8787' // Backend dev server
    }
  }
}
```

### Token Expired

```typescript
// api.ts interceptor handles 401
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

## Best Practices

1. **Use Design System** - Semantic color tokens only
2. **Type everything** - Leverage TypeScript
3. **Handle errors** - User-friendly messages
4. **Validate forms** - Client-side validation
5. **Loading states** - Show spinners during API calls
6. **Responsive design** - Mobile-first approach
7. **Accessibility** - ARIA labels, keyboard navigation
8. **ETag always** - Prevent concurrent edit conflicts
9. **Controlled Components** - ALWAYS use getCurrentValue() helper for Select components that display config values with pending changes (see Configuration Forms section)
10. **State Separation** - Keep original server values (resolveOut) separate from pending changes (changes array)
11. **Branch Health Polling** - Refresh branch status every 30 seconds (v2.0.0)

## Related Skills

- `n8n-vigil-workflow` - Understanding what the UI configures
- `clickhouse-grafana-monitoring` - Grafana dashboard integration
- `docker-vigil-orchestration` - Deployment and nginx configuration
- `express-api-developer` - Backend API integration

## References

- Frontend code: `services/web-ui/frontend/src/`
- API client: `services/web-ui/frontend/src/lib/api.ts`
- Variable specs: `services/web-ui/frontend/src/spec/variables.json`
- Design system: `services/web-ui/frontend/tailwind.config.ts`
- Web UI CLAUDE.md: `services/web-ui/CLAUDE.md`
- unified_config.json: `services/workflow/config/unified_config.json` (303 lines, v5.0.0)

---

**Last Updated:** 2025-12-09
**Frontend Version:** v2.0.0
**Components:** 15+ React components (including branch monitoring)

## Version History

- **v2.0.0** (Current): Branch health monitoring, arbiter configuration UI, 3-branch detection components
- **v1.6.11**: Initial React setup, config forms, getCurrentValue() pattern
