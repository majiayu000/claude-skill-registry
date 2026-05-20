---
name: af-integrate-posthog
description: Integrate PostHog for product analytics, feature flags, and session replay. Use when setting up the SDK, configuring feature flags, tracking events, or identifying users across sessions.

title: PostHog Expertise
created: 2026-02-08
updated: 2026-02-12
last_checked: 2026-02-12
tags: [skill, expertise, posthog, analytics, feature-flags, tracking]
parent: ../README.md
related:
  - ../../docs/guides/posthog-guide.md
  - ../af-setup-gaininsight-stack/SKILL.md
  - ../../docs/guides/gaininsight-standard/layer-3-ui-styling.md
  - ../../../.agentflow/adr/adr-010-posthog-analytics-feature-flags.md
---

# PostHog Expertise

## When to Use This Skill

Load this skill when you need to:
- Integrate PostHog into a new or existing project
- Set up feature flags for view or component gating
- Implement event tracking with standard naming conventions
- Manage PostHog credentials in Doppler and Bitwarden
- Debug feature flag loading or latency issues

## Quick Reference

| Concern | PostHog Feature |
|---------|----------------|
| Feature flags | `posthog.isFeatureEnabled()`, `useFeatureFlag` hook |
| Event tracking | `posthog.capture()`, typed event functions |
| User identity | `posthog.identify()` with auth provider ID |
| Session replay | PostHog autocapture (production only) |
| A/B testing | Feature flag multivariate support |

## PostHog Region

GainInsight projects use **PostHog EU** (`eu.posthog.com`) for GDPR compliance.

| Setting | Value |
|---------|-------|
| Dashboard | `https://eu.posthog.com` |
| Ingest host | `https://eu.i.posthog.com` |
| API host | `https://eu.posthog.com/api` |

## Credential Management

### Required Secrets (Doppler)

| Secret | Purpose | Where Used |
|--------|---------|------------|
| `VITE_POSTHOG_KEY` | Project API key (client-side, `phc_*`) | Vite build-time env var |
| `VITE_POSTHOG_HOST` | Ingest host URL | Vite build-time env var |
| `POSTHOG_PERSONAL_API_KEY` | Management API key (`phx_*`) | Server-side flag/API management |

### Bitwarden Entry

Store PostHog credentials in Bitwarden with:
- **Name**: `PostHog - {ProjectName}`
- **Username**: `{email}` (e.g., `admins+{project}-posthog@gaininsight.global`)
- **Password**: Account password
- **URI**: `https://eu.posthog.com`
- **Custom Fields**: Personal API Key, Project API Key, Project ID

### Account Registration

Use the `admins+{project}-posthog@gaininsight.global` email pattern for per-project PostHog accounts. This uses plus-addressing on the `admins@` Google Group so all team members receive notifications.

## SDK Setup Pattern

### File Structure

```
src/
  posthog/
    client.ts          # PostHog init, identify, reset, feature flag helpers, local overrides
    provider.tsx       # React provider for auth-aware identification
    events.ts          # Typed event tracking functions
    index.ts           # Barrel exports
  api/
    flags.ts           # API client for server-side flag management (fetchFlags, updateFlag)
  components/molecules/
    FeatureFlagPanel.tsx  # Admin UI for managing flags across tiers (Local/Dev/Prod)
server/src/api/routes/
  flags.ts             # Express route: GET/PATCH /api/flags — proxies PostHog API
```

### Initialization Order (Critical)

PostHog must initialize **at module load time**, not inside a React component, to minimize flag loading latency:

```typescript
// provider.tsx — init at module level
import { initPostHog } from "./client"
initPostHog()  // Runs when JS bundle loads, before auth

export function PostHogProvider({ children }) {
  // identify() happens here after auth succeeds
}
```

**Why:** Feature flags are fetched from the server on init. If init waits for auth, flags aren't ready when the sidebar renders, causing a flash of incorrect UI.

### Graceful Degradation

When `VITE_POSTHOG_KEY` is not set (local dev without Doppler):
- PostHog never initializes
- All feature flags return `true` (all features visible)
- No events are tracked
- No network requests to PostHog

This means `pnpm dev` works without any PostHog configuration.

### Flag Loading Behavior

When PostHog IS configured:
- Flags default to `false` (hidden) until PostHog responds
- Once flags load, enabled features appear
- Flags persist in `localStorage` so subsequent page loads are instant

```typescript
export function isFeatureEnabled(flag: string): boolean {
  if (!POSTHOG_KEY) return true          // No key = show everything (dev)
  if (!flagsLoaded) return false         // Key set but loading = hide until ready
  return posthog.isFeatureEnabled(flag) ?? false
}
```

## Feature Flag Patterns

### View-Level Flags

Gate entire views/pages behind flags. Use plain, descriptive names matching the view ID:

```typescript
export const VIEW_FLAGS = {
  health: "health",
  sessions: "sessions",
  docs: "docs",
  canvas: "canvas",
} as const
```

**Sidebar integration:**
```typescript
// Sidebar accepts viewFlags prop
const filteredItems = navItems.filter(
  (item) => !viewFlags || viewFlags[item.id] !== false
)
```

### Component-Level Flags

Gate individual components within a view:

```typescript
function DashboardPage() {
  const showMetrics = useFeatureFlag("dashboard-metrics-panel")
  const showChart = useFeatureFlag("dashboard-chart")

  return (
    <div>
      <Header />
      {showMetrics && <MetricsPanel />}
      {showChart && <ActivityChart />}
    </div>
  )
}
```

### Flag Naming Convention

| Level | Pattern | Example |
|-------|---------|---------|
| View | `{view-id}` | `health`, `sessions`, `canvas` |
| Component | `{view}-{component}` | `health-services-panel`, `dashboard-chart` |
| Feature | `{feature-name}` | `dark-mode`, `export-csv` |

**Do NOT prefix with `feature-`** — use descriptive names and organize with PostHog groups/tags instead.

### Flag Grouping (Client-Side)

Flags are **flat** in PostHog (no dependencies) and **grouped client-side** in the FeatureFlagPanel. This avoids PostHog dependency chain complexity and keeps grouping logic in the UI where it can be changed without PostHog configuration.

#### Actual Flag Names (Agentview)

**Sidebar views:**
`my-tasks`, `projects`, `health`, `sessions`, `activity`, `costs`, `claude-usage`, `terminal`, `docs`, `canvas`, `settings`

**Task detail panels:**
`tasks-description`, `tasks-terminal`, `tasks-canvas`, `tasks-transcript`

**Project panels:**
`project-tasks-panel`, `project-costs-panel`, `project-activity-panel`, `project-docs-panel`, `project-settings-panel`

#### Client-Side Group Definitions

Groups are defined as static arrays in `FeatureFlagPanel.tsx`:

```typescript
// "By View" mode — mirrors sidebar navigation
const VIEW_GROUPS = [
  { id: 'tasks', label: 'Tasks', flags: ['my-tasks', 'tasks-description', ...] },
  { id: 'projects', label: 'Projects', flags: ['projects', 'project-tasks-panel', ...] },
  { id: 'views', label: 'Views', flags: ['health', 'sessions', 'activity', ...] },
  { id: 'tools', label: 'Tools', flags: ['terminal', 'docs', 'canvas'] },
]

// "By Feature" mode — groups same feature across views
const FEATURE_GROUPS = [
  { name: 'Tasks', flags: [{ flag: 'my-tasks', context: 'Sidebar' }, { flag: 'project-tasks-panel', context: 'Project panel' }] },
  { name: 'Canvas', flags: [{ flag: 'canvas', context: 'Sidebar' }, { flag: 'tasks-canvas', context: 'Task panel' }] },
  // ...
]
```

Group toggle switches flip all flags in a group at once (with parallel API calls).

### Local Overrides

Users can override any flag locally via `localStorage` without affecting other users. Local overrides take priority over PostHog SDK values.

```typescript
const OVERRIDES_KEY = "posthog_flag_overrides"

export function overrideFlag(flag: string, value: boolean | undefined) {
  // Save to localStorage
  // Apply to PostHog SDK via posthog.featureFlags.override()
  // Notify subscribed components
}

export function isFeatureEnabled(flag: string): boolean {
  const overrides = getFlagOverrides()
  if (flag in overrides) return overrides[flag]  // Local override wins
  if (!POSTHOG_KEY) return true                  // No key = show everything
  if (!flagsLoaded) return false                 // Loading = hide
  return posthog.isFeatureEnabled(flag) ?? false
}
```

Overrides are visually indicated with amber color in the FeatureFlagPanel. A "Reset" button clears all overrides.

## Environment Targeting (Dev vs Prod)

PostHog flags use **filter groups** with the `environment` person property to target dev and prod independently. The `environment` property is set as a super property during PostHog init (`"development"` or `"production"`).

### Filter Group Structure

Each flag has one or two filter groups:

```
Same state in dev & prod:
  [{ properties: [], rollout_percentage: 100 }]   ← single catch-all

Different state:
  [
    { properties: [{ key: "environment", value: ["development"] }], rollout_percentage: 100 },  ← dev group
    { properties: [], rollout_percentage: 0 }                                                    ← prod catch-all
  ]
```

The server-side `/api/flags` route parses these groups into simple `{ devEnabled, prodEnabled }` booleans and rebuilds them on PATCH.

### Server-Side Flag Proxy (`/api/flags`)

The Express API proxies PostHog's Management API so the Personal API Key stays server-side:

```
GET  /api/flags          → List all flags with parsed dev/prod state
PATCH /api/flags/:key    → Update a flag's dev and/or prod targeting
```

**GET response:**
```json
{ "flags": [{ "id": 141447, "key": "my-tasks", "active": true, "devEnabled": true, "prodEnabled": true }] }
```

**PATCH body:**
```json
{ "devEnabled": false }
```

The PATCH handler: (1) fetches current flag from PostHog, (2) merges the update, (3) builds new filter groups, (4) PATCHes PostHog, (5) returns parsed result.

## FeatureFlagPanel (Admin UI)

A slide-out Sheet component for managing flags. Three tiers, two grouping modes.

### Three Tiers

| Tier | Color | Behavior |
|------|-------|----------|
| **Local** (amber) | Browser-only overrides via `localStorage` | Instant, affects only this browser |
| **Dev** (blue) | Shared dev flags via PostHog API proxy | PATCHes PostHog, affects all dev users |
| **Prod** (emerald) | Production PostHog values | **Read-only** in the panel |

### Two Slice Modes

- **By View**: Groups flags by sidebar nav structure (Tasks, Projects, Views, Tools)
- **By Feature**: Groups the same feature across all views it appears in

### Optimistic Updates with Race Prevention

Dev tier uses optimistic updates so switches respond instantly despite the 2-round-trip API call (GET all flags + PATCH specific flag):

```typescript
const requestCounter = useRef<Map<string, number>>(new Map())

const handleToggle = (flag, currentValue) => {
  const reqId = (requestCounter.current.get(flag) ?? 0) + 1
  requestCounter.current.set(flag, reqId)

  // Flip immediately
  setPosthogFlags(prev => prev.map(f => f.key === flag ? { ...f, devEnabled: !currentValue } : f))

  updateFlag(flag, { devEnabled: !currentValue })
    .then(updated => {
      // Only apply if no newer request exists (prevents stale responses overwriting)
      if (requestCounter.current.get(flag) === reqId) {
        setPosthogFlags(prev => prev.map(f => f.key === flag ? updated : f))
      }
    })
    .catch(() => { /* revert if reqId is still current */ })
}
```

**Key pattern**: Never replace a Switch with a loading spinner — always keep it in the DOM. Show the spinner alongside the switch so it remains clickable during API calls.

### PostHog Dashboard Organization

- Group related flags by feature area using PostHog tags
- Link to Linear issues in flag descriptions
- Use filter groups for environment targeting, not separate flags per environment

## Event Tracking Conventions

### Standard Event Names

Use `snake_case` for all event names:

| Event | When | Properties |
|-------|------|------------|
| `view_changed` | User navigates to a view | `view`, `previous_view` |
| `login_completed` | Auth succeeds | `user_id`, `github_login` |
| `login_failed` | Auth fails | `error` |
| `logout` | User logs out | — |
| `{feature}_triggered` | User initiates action | `manual: boolean` |
| `{feature}_result` | Action completes | `status`, `error?` |

### Typed Event Functions

Create typed wrappers to prevent typos and ensure consistent properties:

```typescript
// events.ts
export function trackViewChanged(view: View, previousView?: View) {
  trackEvent("view_changed", { view, previous_view: previousView })
}

export function trackLoginCompleted(userId: string, login: string) {
  trackEvent("login_completed", { user_id: userId, github_login: login })
}
```

### Super Properties

Set once at init, attached to every event automatically:

| Property | Values | Purpose |
|----------|--------|---------|
| `platform` | `"tauri"` / `"browser"` | Filter by deployment target |
| `environment` | `"development"` / `"production"` | Filter dev vs prod traffic |

```typescript
posthog.register({
  platform: isTauri ? "tauri" : "browser",
  environment: isDev ? "development" : "production",
})
```

### Autocapture

- **Production**: Enabled (captures clicks, page views, form submissions)
- **Development**: Disabled (reduces noise)

```typescript
posthog.init(key, { autocapture: !isDev })
```

## User Identification

Use the auth provider's user ID as PostHog's distinct ID:

```typescript
// On login
identifyUser(String(user.id), {
  github_login: user.login,
  name: user.name,
  avatar_url: user.avatar_url,
})

// On logout
posthog.reset()
```

**Important:** Call `identify()` AFTER `init()`, not during. Init happens at module load; identify happens when auth state changes.

## Integration Points

### GainInsight Standard

PostHog fits into the GI Standard stack as a **cross-cutting concern** applied after Layer 1:

| When | Action |
|------|--------|
| Layer 1 complete | Register PostHog account, add secrets to Doppler |
| Layer 3 (UI) | Add `posthog-js`, create `src/posthog/` module |
| Layer 4 (CI/CD) | Ensure Doppler injects `VITE_POSTHOG_KEY` in builds |

### Brownfield Integration

For existing projects without PostHog:
1. Install `posthog-js` via package manager
2. Create `src/posthog/` module (client, provider, events, flags, index)
3. Wrap app with `PostHogProvider`
4. Add `VITE_POSTHOG_KEY` and `VITE_POSTHOG_HOST` to Doppler
5. Create feature flags in PostHog dashboard (or via API with personal key)
6. Store credentials in Bitwarden

### PostHog API (Server-Side)

For programmatic flag management, use the personal API key:

```bash
# List flags with dev/prod state
POSTHOG_KEY=$(doppler run --project agentview --config prd -- printenv POSTHOG_PERSONAL_API_KEY)
curl -H "Authorization: Bearer $POSTHOG_KEY" \
  "https://eu.posthog.com/api/projects/$PROJECT_ID/feature_flags/?limit=100"

# Create a flag (on for everyone)
curl -X POST -H "Authorization: Bearer $POSTHOG_KEY" -H "Content-Type: application/json" \
  "https://eu.posthog.com/api/projects/$PROJECT_ID/feature_flags/" \
  -d '{"key":"my-flag","name":"My Flag","active":true,"filters":{"groups":[{"properties":[],"rollout_percentage":100}]}}'

# Set flag to dev=ON, prod=OFF
curl -X PATCH -H "Authorization: Bearer $POSTHOG_KEY" -H "Content-Type: application/json" \
  "https://eu.posthog.com/api/projects/$PROJECT_ID/feature_flags/$FLAG_ID/" \
  -d '{"active":true,"filters":{"groups":[{"properties":[{"key":"environment","value":["development"],"operator":"exact","type":"person"}],"rollout_percentage":100},{"properties":[],"rollout_percentage":0}]}}'
```

**Note:** `POSTHOG_PERSONAL_API_KEY` is stored in Doppler `prd` config only (not `dev`).

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| All views flash before flags load | Init too late (inside component) | Move `initPostHog()` to module level |
| Flags always return true | `VITE_POSTHOG_KEY` not set | Check Doppler config, ensure `doppler run` in build |
| Flags never update | `onFeatureFlags` callback not firing | Check PostHog console for init errors |
| Events not appearing in dashboard | Wrong API host | Use `eu.i.posthog.com` for EU region |
| User not identified | `identify()` called before `init()` | Ensure init completes before identify |
| Switch unclickable during API call | Switch replaced by spinner | Keep Switch in DOM, show spinner alongside |
| Switch flips back after toggle | Stale API response overwrites optimistic update | Use request counter ref to discard stale responses |
| Dev flags return 503 | `POSTHOG_PERSONAL_API_KEY` missing | API server must run with Doppler `prd` config |

## Flutter / Mobile (Future)

PostHog has a Flutter SDK (`posthog_flutter`). When mobile arrives:
- Same PostHog project, same feature flags
- Use platform super property (`"flutter"`) to distinguish
- Share flag naming conventions across web and mobile
- Session replay not yet supported in Flutter SDK

## Essential Reading

- [PostHog Integration Guide](../../docs/guides/posthog-guide.md)
- [GainInsight Standard Skill](../af-setup-gaininsight-stack/SKILL.md)
- [PostHog JS Docs](https://posthog.com/docs/libraries/js)
- [PostHog Feature Flags](https://posthog.com/docs/feature-flags)
