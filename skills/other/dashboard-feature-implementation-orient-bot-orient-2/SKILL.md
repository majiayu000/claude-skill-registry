---
name: dashboard-feature-implementation
description: Guide for implementing dashboard features in the Orient monorepo. Use when adding new tabs, views, pages, or components to the dashboard. Covers backend services, API routes, frontend components, navigation, routing, and command palette integration. Applicable when asked to "add a dashboard feature", "create a new tab", "add a monitoring page", "create storage view", "add settings section", or any dashboard UI work requiring both backend and frontend changes.
---

# Dashboard Feature Implementation

Guide for adding features to the Orient dashboard across backend and frontend.

## Architecture Overview

```
packages/dashboard/                    # Backend
├── src/services/                      # Business logic
│   └── <feature>Service.ts           # Service with singleton pattern
└── src/server/routes/
    ├── <feature>.routes.ts           # Express routes
    └── index.ts                       # Route exports

packages/dashboard-frontend/           # Frontend
├── src/api.ts                         # API types and functions
├── src/routes.ts                      # Route definitions
├── src/App.tsx                        # Main app with routing
└── src/components/
    ├── Layout/Sidebar.tsx             # Navigation
    └── <FeatureName>Tab.tsx          # Tab component
        └── <FeatureName>/            # Sub-components
```

## Implementation Checklist

### Backend

1. Create service in `packages/dashboard/src/services/<feature>Service.ts`
2. Create routes in `packages/dashboard/src/server/routes/<feature>.routes.ts`
3. Export routes in `packages/dashboard/src/server/routes/index.ts`
4. Register routes in `packages/dashboard/src/server/routes.ts`

### Frontend

5. Add types and API functions in `packages/dashboard-frontend/src/api.ts`
6. Update `GlobalView` type and routes in `packages/dashboard-frontend/src/routes.ts`
7. Add navigation link in `packages/dashboard-frontend/src/components/Layout/Sidebar.tsx`
8. Add route rendering and command in `packages/dashboard-frontend/src/App.tsx`
9. Create main component `packages/dashboard-frontend/src/components/<Feature>Tab.tsx`
10. Create sub-components in `packages/dashboard-frontend/src/components/<Feature>/`

## Backend Patterns

### Service Pattern (Singleton)

```typescript
// packages/dashboard/src/services/featureService.ts
import { createServiceLogger } from '@orientbot/core';

const logger = createServiceLogger('feature-service');

export class FeatureService {
  constructor(private db: MessageDatabase) {}

  async getData(): Promise<FeatureData> {
    // Implementation
  }
}

let instance: FeatureService | null = null;

export function initFeatureService(db: MessageDatabase): FeatureService {
  instance = new FeatureService(db);
  return instance;
}

export function getFeatureService(): FeatureService {
  if (!instance) throw new Error('Service not initialized');
  return instance;
}
```

### Routes Pattern

```typescript
// packages/dashboard/src/server/routes/feature.routes.ts
import { Router, Request, Response } from 'express';
import { createServiceLogger } from '@orientbot/core';
import { getFeatureService } from '../../services/featureService.js';

const logger = createServiceLogger('feature-routes');

export function createFeatureRoutes(
  requireAuth: (req: Request, res: Response, next: () => void) => void
): Router {
  const router = Router();

  router.get('/data', requireAuth, async (_req: Request, res: Response) => {
    try {
      const service = getFeatureService();
      const data = await service.getData();
      res.json(data);
    } catch (error) {
      logger.error('Failed to get data', { error: String(error) });
      res.status(500).json({ error: 'Failed to get data' });
    }
  });

  return router;
}
```

### Register Routes

```typescript
// In routes/index.ts - add export
export { createFeatureRoutes } from './feature.routes.js';

// In routes.ts - import and register
import { createFeatureRoutes } from './routes/index.js';
import { initFeatureService } from '../services/featureService.js';

// In setupApiRoutes function:
initFeatureService(db);
router.use('/feature', createFeatureRoutes(requireAuth));
```

## Frontend Patterns

### API Types and Functions

```typescript
// In packages/dashboard-frontend/src/api.ts

export interface FeatureData {
  items: FeatureItem[];
  total: number;
}

export async function getFeatureData(): Promise<FeatureData> {
  return apiRequest('/feature/data');
}

export async function updateFeature(id: string, data: Partial<FeatureItem>): Promise<FeatureItem> {
  return apiRequest(`/feature/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}
```

### Route Configuration

```typescript
// In packages/dashboard-frontend/src/routes.ts

// 1. Add to GlobalView union type
export type GlobalView =
  | 'billing'
  | 'monitoring'
  | 'feature'  // Add here
  | 'settings';

// 2. Add to ROUTES constant
export const ROUTES = {
  BILLING: '/billing',
  MONITORING: '/monitoring',
  FEATURE: '/feature',  // Add here
  SETTINGS: '/settings',
} as const;

// 3. Add to getRouteState function
if (pathname.startsWith('/feature')) {
  return { ...defaultState, globalView: 'feature' };
}

// 4. Add to getRoutePath function
case 'feature':
  return ROUTES.FEATURE;
```

### Sidebar Navigation

```typescript
// In Sidebar.tsx - add to GlobalView type and navigation links

// Add icon + link after existing items:
<Link
  to={ROUTES.FEATURE}
  className={`w-full flex items-center gap-2 px-3 py-2 text-sm font-medium rounded-md transition-colors ${
    isGlobalActive('feature')
      ? 'bg-primary text-primary-foreground'
      : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
  }`}
>
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    {/* Icon path */}
  </svg>
  Feature Name
</Link>
```

### App.tsx Integration

```typescript
// Import component
import FeatureTab from './components/FeatureTab';

// Add rendering
{globalView === 'feature' && <FeatureTab />}

// Add command palette entry
cmds.push({
  id: 'nav-feature',
  label: 'Feature Name',
  description: 'Feature description',
  category: 'navigation',
  keywords: ['keyword1', 'keyword2'],
  icon: (<svg>...</svg>),
  action: () => navigate(ROUTES.FEATURE),
});
```

### Tab Component Structure

```typescript
// packages/dashboard-frontend/src/components/FeatureTab.tsx
import { useState, useEffect, useCallback } from 'react';
import { getFeatureData, type FeatureData } from '../api';

export default function FeatureTab() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<FeatureData | null>(null);
  const [autoRefresh, setAutoRefresh] = useState(false);

  const fetchData = useCallback(async () => {
    try {
      setError(null);
      const result = await getFeatureData();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchData(); }, [fetchData]);

  // Auto-refresh effect
  useEffect(() => {
    if (!autoRefresh) return;
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, [autoRefresh, fetchData]);

  if (loading) return <LoadingState />;
  if (error) return <ErrorState error={error} onRetry={fetchData} />;

  return (
    <div className="space-y-6 animate-fade-in">
      <Header autoRefresh={autoRefresh} onAutoRefreshChange={setAutoRefresh} onRefresh={fetchData} />
      <SummaryCards data={data} />
      <DetailCards data={data} />
    </div>
  );
}
```

## UI Patterns

### Loading State

```tsx
<div className="flex items-center justify-center py-12">
  <div className="flex flex-col items-center gap-3">
    <div className="spinner" />
    <p className="text-sm text-muted-foreground">Loading...</p>
  </div>
</div>
```

### Error State

```tsx
<div className="card p-6">
  <div className="flex items-center gap-3 text-destructive">
    <svg>...</svg>
    <div>
      <p className="font-medium">Failed to load</p>
      <p className="text-sm text-muted-foreground">{error}</p>
    </div>
  </div>
  <button onClick={onRetry} className="btn btn-secondary mt-4">
    Try Again
  </button>
</div>
```

### Card Components

```tsx
<div className="card p-5">
  <div className="flex items-center gap-3 mb-4">
    <div className="w-8 h-8 rounded-lg bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
      <svg className="w-4 h-4 text-blue-600 dark:text-blue-400">...</svg>
    </div>
    <div>
      <h3 className="font-semibold">Card Title</h3>
      <p className="text-xs text-muted-foreground">Subtitle</p>
    </div>
  </div>
  {/* Card content */}
</div>
```

### Status Badges

```tsx
<span
  className={`px-2 py-1 text-xs font-medium rounded-full ${
    status === 'success'
      ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400'
      : status === 'error'
        ? 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
        : 'bg-gray-100 text-gray-700 dark:bg-gray-900/30 dark:text-gray-400'
  }`}
>
  {statusLabel}
</span>
```

## Common Sub-Tabs Pattern

For features with multiple views:

```typescript
// In routes.ts
export type FeatureView = 'overview' | 'details' | 'settings';

export const ROUTES = {
  FEATURE: '/feature',
  FEATURE_OVERVIEW: '/feature/overview',
  FEATURE_DETAILS: '/feature/details',
  FEATURE_SETTINGS: '/feature/settings',
};

// In App.tsx - render sub-tabs
{globalView === 'feature' && (
  <div className="flex gap-1 mb-6 p-1 bg-secondary rounded-lg w-fit border border-border">
    <Link to={ROUTES.FEATURE_OVERVIEW} className={...}>Overview</Link>
    <Link to={ROUTES.FEATURE_DETAILS} className={...}>Details</Link>
    <Link to={ROUTES.FEATURE_SETTINGS} className={...}>Settings</Link>
  </div>
)}
```

## Testing

1. **Type check**: `pnpm exec tsc --project packages/dashboard/tsconfig.json --noEmit`
2. **Lint**: `pnpm exec eslint packages/dashboard/src/... packages/dashboard-frontend/src/...`
3. **Manual test**:
   - Run backend: `pnpm --filter dashboard dev`
   - Run frontend: `pnpm --filter dashboard-frontend dev`
   - Test API: `curl http://localhost:3000/api/feature/data`
   - Navigate to `/dashboard/feature` in browser
