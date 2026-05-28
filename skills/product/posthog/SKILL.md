---
name: posthog
description: >
  Comprehensive product analytics skill for PostHog implementation and management.
  Auto-triggers on phrases like "add analytics", "track event", "feature flag", "A/B test",
  "experiment", "session recording", "product analytics", "user tracking", "posthog",
  "conversion funnel", "user behavior", "engagement metrics", "rollout", "percentage rollout".
  Provides slash commands /kodo ph-event (event tracking setup), /kodo ph-flag (feature flag management),
  /kodo ph-experiment (A/B testing), /kodo ph-sync (Notion documentation sync).
  Ensures full instrumentation from Day 1 with autocapture, custom events, feature flags,
  experiments, and maintains comprehensive documentation in Notion.
---

# Kodo PostHog Analytics Skill

Ultimate product analytics assistant for PostHog implementation, event tracking, feature flags, experiments, and analytics documentation.

## Commands

All commands support inline context: `/kodo ph-event {event description}` or `/kodo ph-flag {feature context}`

| Command | Purpose |
|---------|---------|
| `/kodo ph-event [context]` | Plan and implement event tracking (autocapture + custom events) |
| `/kodo ph-flag [feature]` | Create, manage, and document feature flags |
| `/kodo ph-experiment [hypothesis]` | Design and implement A/B tests/experiments |
| `/kodo ph-sync [direction]` | Sync analytics documentation with Notion (push/pull/both) |
| `/kodo ph-dashboard [focus]` | Create and manage PostHog dashboards and insights |

## Workflow Overview

1. **Trigger detection** -> Identify analytics/tracking need
2. **Check config** -> Load `.kodo/config.json` for PostHog settings
3. **Discovery** -> Ask targeted questions about tracking requirements
4. **Implementation** -> Generate SDK code for frontend/backend
5. **Documentation** -> Create/update Notion docs with event catalog
6. **Validation** -> Verify instrumentation via PostHog MCP tools

## Project Configuration

Expects PostHog configuration in `.kodo/config.json`:

```json
{
  "stack": {
    "workspaces": {
      "server": {
        "analytics": {
          "provider": "posthog",
          "packages": {
            "server": "posthog-node",
            "client": "posthog-js"
          }
        }
      }
    }
  },
  "features": {
    "analytics": {
      "enabled": true,
      "provider": "posthog"
    }
  },
  "notion": {
    "teamspace": "MyTeamspace",
    "idPrefix": "KODO",
    "_populated_by_init": {
      "databases": {
        "events": { "dataSourceId": "collection://..." },
        "eventProperties": { "dataSourceId": "collection://..." },
        "featureFlags": { "dataSourceId": "collection://..." },
        "experiments": { "dataSourceId": "collection://..." },
        "dashboards": { "dataSourceId": "collection://..." }
      }
    }
  },
  "posthog": {
    "projectId": "",
    "organizationSlug": "",
    "environments": {
      "development": {
        "apiKey": "phc_dev_...",
        "host": "https://app.posthog.com"
      },
      "production": {
        "apiKey": "phc_prod_...",
        "host": "https://app.posthog.com"
      }
    }
  }
}
```

**Important:** Run `/kodo notion-init` first to create all Notion databases with proper Relations.

## Quick Decision Matrix

| Scenario | Approach |
|----------|----------|
| User actions (clicks, form submits) | Autocapture + semantic naming |
| Business events (purchase, signup) | Custom events with properties |
| Feature adoption tracking | Feature flag + usage events |
| Conversion optimization | Experiments with funnel metrics |
| Performance monitoring | Custom events with timing data |
| Error tracking | Custom events with error properties |
| User segmentation | Person properties + cohorts |
| Real-time metrics | PostHog dashboards |

## Event Tracking Strategy

### Autocapture vs Custom Events

**Use Autocapture for:**
```
- General user interactions (clicks, pageviews)
- Form interactions
- Link clicks and navigation
- Rapid prototyping/MVP analytics
```

**Use Custom Events for:**
```
- Business-critical actions (purchase, signup, subscription)
- Feature-specific tracking with custom properties
- Backend events (API calls, webhooks, jobs)
- Events requiring precise timing or context
- Cross-platform consistency
```

### Event Naming Convention

Follow snake_case naming with clear hierarchy:

```
{domain}_{action}_{object}

Examples:
- user_signed_up
- subscription_created
- payment_completed
- feature_flag_evaluated
- experiment_variant_assigned
- dashboard_viewed
- report_exported
```

### Standard Event Properties

Always include these properties where applicable:

```typescript
interface StandardEventProperties {
  // Identity
  $user_id?: string;
  $session_id?: string;

  // Context
  $current_url?: string;
  $pathname?: string;
  $referrer?: string;

  // Custom context
  feature_area?: string;
  component?: string;
  action_source?: 'button' | 'keyboard' | 'api' | 'automated';

  // Business context
  plan_type?: string;
  organization_id?: string;

  // Technical
  client_timestamp?: string;
  sdk_version?: string;
}
```

## SDK Implementation Patterns

### Frontend (React + posthog-js)

```typescript
// lib/posthog.ts
import posthog from 'posthog-js';

const POSTHOG_KEY = import.meta.env.VITE_POSTHOG_KEY;
const POSTHOG_HOST = import.meta.env.VITE_POSTHOG_HOST || 'https://app.posthog.com';

export function initPostHog() {
  if (typeof window !== 'undefined' && POSTHOG_KEY) {
    posthog.init(POSTHOG_KEY, {
      api_host: POSTHOG_HOST,
      capture_pageview: true,
      capture_pageleave: true,
      autocapture: true,
      persistence: 'localStorage+cookie',

      // Session recording
      session_recording: {
        maskAllInputs: true,
        maskTextSelector: '[data-mask]',
      },

      // Performance
      loaded: (posthog) => {
        if (import.meta.env.DEV) {
          posthog.debug();
        }
      },
    });
  }
}

// Custom event helper with type safety
export function trackEvent<T extends Record<string, unknown>>(
  eventName: string,
  properties?: T
) {
  posthog.capture(eventName, {
    ...properties,
    client_timestamp: new Date().toISOString(),
  });
}

// Feature flag helper
export function isFeatureEnabled(flagKey: string): boolean {
  return posthog.isFeatureEnabled(flagKey) ?? false;
}

// Get feature flag payload
export function getFeatureFlagPayload<T>(flagKey: string): T | undefined {
  return posthog.getFeatureFlagPayload(flagKey) as T | undefined;
}

// Identify user
export function identifyUser(
  userId: string,
  properties?: Record<string, unknown>
) {
  posthog.identify(userId, properties);
}

// Reset on logout
export function resetAnalytics() {
  posthog.reset();
}
```

### Backend (Node.js + posthog-node)

```typescript
// lib/posthog-server.ts
import { PostHog } from 'posthog-node';

const client = new PostHog(process.env.POSTHOG_API_KEY!, {
  host: process.env.POSTHOG_HOST || 'https://app.posthog.com',
  flushAt: 20,
  flushInterval: 10000,
});

// Graceful shutdown
process.on('SIGTERM', async () => {
  await client.shutdown();
});

export function trackServerEvent(
  distinctId: string,
  eventName: string,
  properties?: Record<string, unknown>
) {
  client.capture({
    distinctId,
    event: eventName,
    properties: {
      ...properties,
      $lib: 'posthog-node',
      server_timestamp: new Date().toISOString(),
    },
  });
}

export function identifyServerUser(
  distinctId: string,
  properties: Record<string, unknown>
) {
  client.identify({
    distinctId,
    properties,
  });
}

export async function getFeatureFlag(
  flagKey: string,
  distinctId: string,
  options?: {
    personProperties?: Record<string, unknown>;
    groupProperties?: Record<string, Record<string, unknown>>;
  }
): Promise<boolean | string | undefined> {
  return client.getFeatureFlag(flagKey, distinctId, options);
}

export async function getAllFlags(
  distinctId: string
): Promise<Record<string, boolean | string>> {
  return client.getAllFlags(distinctId);
}

export { client as posthog };
```

## Feature Flag Patterns

### Flag Naming Convention

```
{scope}_{feature}_{variant_type}

Examples:
- release_new_dashboard_enabled
- experiment_pricing_page_variant
- ops_maintenance_mode_enabled
- beta_ai_assistant_enabled
```

### Flag Types and Use Cases

| Type | Use Case | Example |
|------|----------|---------|
| Boolean | Simple on/off | `release_dark_mode_enabled` |
| Multivariate | A/B/n testing | `experiment_checkout_flow_variant` |
| Percentage rollout | Gradual release | `release_new_editor_rollout` |
| User targeting | Beta users | `beta_advanced_analytics_enabled` |

### Implementation Pattern

```typescript
// hooks/useFeatureFlag.ts
import { useEffect, useState } from 'react';
import { isFeatureEnabled, getFeatureFlagPayload } from '@/lib/posthog';

export function useFeatureFlag(flagKey: string): boolean {
  const [enabled, setEnabled] = useState(false);

  useEffect(() => {
    setEnabled(isFeatureEnabled(flagKey));
  }, [flagKey]);

  return enabled;
}

export function useFeatureFlagPayload<T>(flagKey: string): T | undefined {
  const [payload, setPayload] = useState<T | undefined>();

  useEffect(() => {
    setPayload(getFeatureFlagPayload<T>(flagKey));
  }, [flagKey]);

  return payload;
}

// Usage
function MyComponent() {
  const showNewFeature = useFeatureFlag('release_new_feature_enabled');
  const experimentVariant = useFeatureFlagPayload<{ variant: 'A' | 'B' }>('experiment_checkout');

  if (!showNewFeature) return <LegacyComponent />;

  return experimentVariant?.variant === 'B'
    ? <NewCheckoutB />
    : <NewCheckoutA />;
}
```

## Experiment Design

### Experiment Workflow

1. **Hypothesis** -> Define what you're testing and expected outcome
2. **Metrics** -> Choose primary and secondary metrics
3. **Variants** -> Design control and treatment(s)
4. **Targeting** -> Define user segments
5. **Duration** -> Calculate required sample size
6. **Implementation** -> Code the variants
7. **Analysis** -> Evaluate results with statistical significance

### Metric Types

| Type | Use For | Example |
|------|---------|---------|
| Funnel | Conversion flows | Signup -> Activation -> Purchase |
| Trend | Engagement metrics | Daily active users |
| Retention | Long-term impact | Week 1 retention |
| Mean | Quantitative measures | Average session duration |

### Creating Experiments via MCP

Use PostHog MCP tools for experiment management:

```
# List existing experiments
mcp__posthog__experiment-get-all

# Create new experiment
mcp__posthog__experiment-create with:
- name: Descriptive experiment name
- feature_flag_key: experiment_feature_key
- primary_metrics: [{ metric_type: 'funnel', event_name: 'purchase_completed' }]
- variants: [{ key: 'control', rollout_percentage: 50 }, { key: 'test', rollout_percentage: 50 }]

# Get experiment results
mcp__posthog__experiment-results-get with experimentId
```

## Dashboard Management

### Standard Dashboards to Create

1. **Product Overview**
   - DAU/WAU/MAU
   - Core feature usage
   - Conversion funnels
   - Retention cohorts

2. **Feature Adoption**
   - Feature flag usage
   - New feature engagement
   - Feature discovery metrics

3. **Experiments**
   - Active experiments status
   - Historical results
   - Statistical significance tracking

4. **Technical Health**
   - Error rates by feature
   - Performance metrics
   - SDK versions in use

### Creating Dashboards via MCP

```
# List dashboards
mcp__posthog__dashboards-get-all

# Create dashboard
mcp__posthog__dashboard-create with:
- name: Dashboard name
- description: Purpose and audience
- pinned: true/false

# Add insights to dashboard
mcp__posthog__add-insight-to-dashboard with:
- insightId: ID from insight creation
- dashboardId: Target dashboard ID
```

## Notion Documentation Sync

### Documentation Structure

All analytics databases are created by `/kodo notion-init` under a centralized "Docs Hub" page:

1. **Event Properties** (`notion._populated_by_init.databases.eventProperties`)
   - Shared property definitions across events
   - Type, required flag, validation rules
   - Bidirectional relation to Events

2. **Events Catalog** (`notion._populated_by_init.databases.events`)
   - Event name, description, implementation status
   - Properties captured (relation to Event Properties)
   - Relation to Features, Feature Flags

3. **Feature Flags** (`notion._populated_by_init.databases.featureFlags`)
   - Flag key, type, status, rollout %
   - Targeting rules documentation
   - Relation to Features, Events, Experiments

4. **Experiments** (`notion._populated_by_init.databases.experiments`)
   - Hypothesis, primary/secondary metrics
   - Start/end dates, results
   - Relation to Features, Feature Flags

5. **Dashboards** (`notion._populated_by_init.databases.dashboards`)
   - Dashboard name, purpose, category
   - PostHog ID and direct URL
   - Relation to Features

### Sync Workflow

**Prerequisites:**
- Run `/kodo notion-init` to create databases with proper Relations
- Config contains dataSourceIds for all databases

See [references/notion-sync.md](references/notion-sync.md) for detailed sync patterns.

## Reference Documentation

- **Event Tracking**: See [references/events.md](references/events.md) for event schemas, naming, properties
- **Feature Flags**: See [references/feature-flags.md](references/feature-flags.md) for flag patterns, targeting
- **Experiments**: See [references/experiments.md](references/experiments.md) for A/B testing methodology
- **Dashboards**: See [references/dashboards.md](references/dashboards.md) for insight types, dashboard design
- **Session Recording**: See [references/session-recording.md](references/session-recording.md) for privacy, masking
- **Notion Sync**: See [references/notion-sync.md](references/notion-sync.md) for documentation sync

## Integration with OpenKodo

Before implementing analytics:
```bash
kodo query "analytics events"
kodo query "feature flags"
```

After implementation:
```bash
kodo reflect  # Capture tracking decisions as learnings
```

## Key Principles

1. **Instrument early** -> Set up tracking before features ship
2. **Name consistently** -> Follow naming conventions strictly
3. **Document everything** -> Keep Notion docs in sync
4. **Test tracking** -> Verify events in PostHog before deploy
5. **Privacy first** -> Mask sensitive data, respect consent
6. **Measure what matters** -> Focus on actionable metrics
7. **Iterate experiments** -> Use data to drive product decisions
8. **Automate sync** -> Keep documentation current via MCP tools
