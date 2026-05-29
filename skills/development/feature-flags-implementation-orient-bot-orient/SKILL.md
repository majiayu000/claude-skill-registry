---
name: feature-flags-implementation
description: Database-backed feature flag systems in the Orient. Use when implementing feature flags, debugging flag-related issues, or understanding the flag hierarchy. Covers schema design, API patterns, frontend hooks, ID format conversion, and ProtectedRoute integration.
---

# Feature Flags Implementation

## Quick Reference

```bash
# Check feature flags in database
sqlite3 "$SQLITE_DB_PATH" "SELECT id, name, enabled FROM feature_flags ORDER BY sort_order;"

# Test feature flag API
curl -X GET http://localhost:4098/api/feature-flags \
  -H "Authorization: Bearer $(cat ~/.dashboard_token)"
```

## Architecture Overview

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│   Database          │────▶│   Dashboard API     │────▶│   Frontend          │
│   (SQLite)          │     │   (Express)         │     │   (React)           │
│                     │     │                     │     │                     │
│ feature_flags table │     │ /api/feature-flags  │     │ useFeatureFlags()   │
│ snake_case IDs      │     │ JWT Authentication  │     │ camelCase IDs       │
│ dot.notation        │     │                     │     │ underscore_notation │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
```

## Database Schema

### Feature Flags Table

Located in `packages/database/src/schema/index.ts`:

```typescript
export const featureFlags = sqliteTable('feature_flags', {
  id: text('id').primaryKey(), // e.g., 'mini_apps', 'operations.billing'
  name: text('name').notNull(), // Display name
  description: text('description'),
  enabled: integer('enabled', { mode: 'boolean' }).default(true),
  category: text('category').default('ui'),
  sortOrder: integer('sort_order').default(0),
  createdAt: integer('created_at', { mode: 'timestamp' }),
  updatedAt: integer('updated_at', { mode: 'timestamp' }),
});
```

### ID Naming Convention

Database uses **snake_case with dot notation** for hierarchy:

```
mini_apps                           # Root flag
mini_apps.create                    # Child of mini_apps
mini_apps.edit_with_ai              # Child with multi-word name
operations                          # Root flag
operations.billing                  # Child of operations
operations.monitoring               # Child of operations
operations.monitoring.server_health # Nested child (grandchild)
```

## API Endpoints

Located in `packages/dashboard/src/server/routes/featureFlags.routes.ts`:

| Method | Endpoint                              | Description                          |
| ------ | ------------------------------------- | ------------------------------------ |
| GET    | `/api/feature-flags`                  | Get all flags with effective values  |
| GET    | `/api/feature-flags/list`             | Get detailed flag list               |
| GET    | `/api/feature-flags/effective`        | Get flat map of flag IDs to booleans |
| PUT    | `/api/feature-flags/:flagId`          | Update a flag                        |
| PUT    | `/api/feature-flags/:flagId/override` | Set user override                    |
| DELETE | `/api/feature-flags/:flagId/override` | Remove user override                 |

### API Response Format

```typescript
// GET /api/feature-flags returns:
{
  flags: [
    {
      id: 'mini_apps',
      name: 'Mini-Apps',
      description: 'Enable mini-apps feature',
      enabled: false,
      category: 'ui',
      sortOrder: 0,
      createdAt: '2024-01-15T10:00:00.000Z',
      updatedAt: '2024-01-15T10:00:00.000Z',
      userOverride: null,
      effectiveValue: false,
    },
    // ... more flags
  ];
}
```

## Frontend Implementation

### ID Format Conversion

**Database → Frontend**: `snake_case.dot` → `camelCase_underscore`

```typescript
// In useFeatureFlags.ts
// API returns: { id: 'mini_apps.edit_with_ai', ... }
// Frontend expects: 'miniApps_editWithAi'

const camelId = flag.id.replace(/_([a-z])/g, (_, c) => c.toUpperCase());
// 'mini_apps.edit_with_ai' → 'miniApps.editWithAi'

const uiId = camelId.replace(/\./g, '_');
// 'miniApps.editWithAi' → 'miniApps_editWithAi'
```

**Frontend → Database**: `camelCase_underscore` → `snake_case.dot`

```typescript
// In FeatureFlagsPage.tsx
const toDbId = (uiId: string): string => {
  const parts = uiId.split('_');
  const dbParts = parts.map((part) =>
    part
      .replace(/([A-Z])/g, '_$1')
      .toLowerCase()
      .replace(/^_/, '')
  );
  return dbParts.join('.');
};

// 'miniApps_editWithAi' → 'mini_apps.edit_with_ai'
```

### useFeatureFlags Hook

Located in `packages/dashboard-frontend/src/hooks/useFeatureFlags.ts`:

```typescript
import { getFeatureFlags } from '../api'; // MUST use authenticated API

export function useFeatureFlags(): UseFeatureFlagsReturn {
  const [flags, setFlags] = useState<Record<string, FeatureFlagDefinition>>(PRE_LAUNCH_DEFAULTS);

  const loadFlags = useCallback(async () => {
    try {
      // Use authenticated API function, NOT raw fetch
      const data = await getFeatureFlags();

      // Transform API format to UI format
      const flagsFromApi: Record<string, FeatureFlagDefinition> = {};
      for (const flag of data.flags) {
        const uiId = convertToUiId(flag.id);
        flagsFromApi[uiId] = {
          enabled: flag.effectiveValue ?? flag.enabled ?? false,
          uiStrategy: 'hide',
          parentFlag: extractParentFlag(flag.id),
        };
      }

      setFlags({ ...PRE_LAUNCH_DEFAULTS, ...flagsFromApi });
    } catch (err) {
      // Fallback to defaults on error
      setFlags(PRE_LAUNCH_DEFAULTS);
    }
  }, []);

  // ... isEnabled, shouldHide, shouldNotify helpers
}
```

### PRE_LAUNCH_DEFAULTS

Safe defaults when API is unavailable:

```typescript
const PRE_LAUNCH_DEFAULTS: Record<string, FeatureFlagDefinition> = {
  // Disabled by default (new/experimental features)
  miniApps: { enabled: false, uiStrategy: 'hide', route: '/apps' },
  miniApps_create: { enabled: false, parentFlag: 'miniApps', uiStrategy: 'hide' },

  // Enabled by default (core features)
  agentRegistry: { enabled: true, uiStrategy: 'hide', route: '/agents' },
  operations: { enabled: true, uiStrategy: 'hide', route: '/operations' },
  operations_billing: { enabled: true, parentFlag: 'operations', uiStrategy: 'hide' },
};
```

### FeatureFlagsPage Component

Located in `packages/dashboard-frontend/src/components/Settings/FeatureFlagsPage.tsx`:

```typescript
import { setFeatureFlagOverride } from '../../api'; // MUST use authenticated API

const updateFlag = async (flagId: string, updates: Partial<FeatureFlagDefinition>) => {
  try {
    const dbId = toDbId(flagId); // Convert UI ID to database ID
    await setFeatureFlagOverride(dbId, updates.enabled ?? false);
    await refresh(); // Reload flags
  } catch (error) {
    alert('Failed to update feature flag');
  }
};
```

## ProtectedRoute Integration

Located in `packages/dashboard-frontend/src/components/ProtectedRoute.tsx`:

```typescript
function ProtectedRoute({ flagId, children }: Props) {
  const { isEnabled, shouldHide, shouldNotify } = useFeatureFlags();

  if (shouldHide(flagId)) {
    return <Navigate to="/" replace />;
  }

  if (shouldNotify(flagId)) {
    return <FeatureDisabledOverlay />;
  }

  return children;
}

// Usage in routes
<Route
  path="/apps"
  element={
    <ProtectedRoute flagId="miniApps">
      <AppsPage />
    </ProtectedRoute>
  }
/>
```

## Database Migrations

### Adding a New Feature Flag

Create migration in `data/migrations/`:

```sql
-- XXXX_add_my_feature_flag.sql
INSERT INTO feature_flags (id, name, description, enabled, category, sort_order)
VALUES
  ('my_feature', 'My Feature', 'Description of feature', false, 'ui', 100),
  ('my_feature.sub_feature', 'Sub Feature', 'A sub-feature', false, 'ui', 101)
ON CONFLICT (id) DO NOTHING;
```

### Adding Child Flags

```sql
-- Add child flags under existing parent
INSERT INTO feature_flags (id, name, description, enabled, category, sort_order)
VALUES
  ('operations.new_child', 'New Child', 'Under operations', true, 'ui', 50)
ON CONFLICT (id) DO NOTHING;
```

## Common Issues

### Issue: 401 Unauthorized on Flag Updates

**Cause**: Using raw `fetch()` instead of authenticated API functions.

**Fix**: Import and use functions from `api.ts`:

```typescript
// BAD
const response = await fetch(`/api/feature-flags/${id}`, {
  method: 'PUT',
  credentials: 'include',
  body: JSON.stringify({ enabled }),
});

// GOOD
import { setFeatureFlagOverride } from '../api';
await setFeatureFlagOverride(id, enabled);
```

### Issue: Flag Shows in UI but Not in Database

**Cause**: Flag is defined in PRE_LAUNCH_DEFAULTS but missing from database.

**Fix**: Add migration to create the flag in database, or remove from defaults if not needed.

### Issue: Child Flag Accessible When Parent Disabled

**Cause**: `isEnabled` doesn't check parent chain, or parent flag ID is wrong.

**Fix**: Ensure `parentFlag` is set correctly in both database parent extraction and defaults:

```typescript
// The isEnabled function checks parent chain
const isEnabled = (flagId: string): boolean => {
  const flag = flags[flagId];
  if (!flag?.enabled) return false;
  if (flag.parentFlag) {
    return isEnabled(flag.parentFlag); // Recursive check
  }
  return true;
};
```

### Issue: ID Conversion Mismatch

**Symptoms**: Flag exists in DB but not showing in UI, or updates go to wrong flag.

**Debug**:

```typescript
console.log('UI ID:', uiId);
console.log('DB ID:', toDbId(uiId));
// Verify they match expected values
```

## Checklist for New Feature Flags

- [ ] Add flag to database migration
- [ ] Run migration: `./run.sh dev` (auto-runs migrations)
- [ ] Add to PRE_LAUNCH_DEFAULTS in `useFeatureFlags.ts` (if needs default)
- [ ] Export from `@orientbot/database` if queried server-side
- [ ] Add ProtectedRoute wrapper if flag controls route access
- [ ] Update navigation to conditionally show/hide based on flag
- [ ] Test toggle in UI persists to database
- [ ] Test parent/child relationships work correctly

## Testing Feature Flags

### Manual Testing

1. Navigate to Settings → Feature Flags
2. Toggle a flag
3. Verify database updated:
   ```bash
   sqlite3 "$SQLITE_DB_PATH" "SELECT id, enabled FROM feature_flags WHERE id = 'mini_apps';"
   ```
4. Verify UI reflects change (navigation item appears/disappears)

### Automated Testing

```typescript
// In a test file
import { describe, it, expect, vi } from 'vitest';
import { renderHook } from '@testing-library/react';
import { useFeatureFlags } from '../hooks/useFeatureFlags';

describe('useFeatureFlags', () => {
  it('should return defaults when API fails', async () => {
    vi.mock('../api', () => ({
      getFeatureFlags: vi.fn().mockRejectedValue(new Error('Network error')),
    }));

    const { result } = renderHook(() => useFeatureFlags());

    // Should use PRE_LAUNCH_DEFAULTS
    expect(result.current.isEnabled('miniApps')).toBe(false);
    expect(result.current.isEnabled('agentRegistry')).toBe(true);
  });
});
```
