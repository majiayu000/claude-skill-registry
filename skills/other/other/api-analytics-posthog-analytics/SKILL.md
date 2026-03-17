---
name: api-analytics-posthog-analytics
description: PostHog event tracking, user identification, group analytics for B2B, GDPR consent patterns. Use when implementing product analytics, tracking user behavior, setting up funnels, or configuring privacy-compliant tracking.
---

# PostHog Analytics Patterns

> **Quick Guide:** Use PostHog for product analytics with structured event naming (category:object_action), server-side tracking for reliability, and proper user identification integrated with your authentication flow. Client-side for UI interactions, server-side for business events.

**Detailed Resources:**

- For code examples, see [examples/core.md](examples/core.md) (start here)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST call `posthog.identify()` ONLY when a user signs up or logs in - never on every page load)**

**(You MUST include the user's database ID as `distinct_id` in ALL server-side events)**

**(You MUST call `posthog.reset()` when a user logs out to unlink future events)**

**(You MUST use the `category:object_action` naming convention for all custom events)**

**(You MUST NEVER include PII (email, name, phone) in event properties - use user IDs only)**

</critical_requirements>

---

**Auto-detection:** PostHog, posthog-js, posthog-node, usePostHog, PostHogProvider, capture, identify, group analytics, product analytics, event tracking, funnel analysis

**When to use:**

- Tracking user behavior and product analytics
- Setting up conversion funnels and retention analysis
- Implementing group analytics for B2B multi-tenant apps
- Understanding feature adoption and user journeys
- A/B testing analysis (in conjunction with feature flags)

**When NOT to use:**

- Feature flag implementation (use `backend/feature-flags.md` skill)
- PostHog setup and installation (use `setup/posthog.md` skill)
- Error tracking and logging (use dedicated error tracking tools)
- Infrastructure monitoring (use observability tools)

**Key patterns covered:**

- Event naming conventions (category:object_action)
- Property naming patterns (object*adjective, is*/has\_ booleans)
- User identification with authentication flow integration
- Client-side tracking with React hooks
- Server-side tracking with posthog-node
- Group analytics for B2B organizations
- Privacy and GDPR consent patterns
- Funnel and cohort setup
- TypeScript patterns for type-safe events

---

<philosophy>

## Philosophy

PostHog analytics follows a **structured taxonomy** approach: consistent naming conventions, meaningful properties, and strategic placement (client vs server). Track what matters for product decisions, not everything.

**Core principles:**

1. **Server-side for business events** - User signups, purchases, subscriptions (reliable, not blocked)
2. **Client-side for UI interactions** - Button clicks, page views, form interactions
3. **Identify once per session** - Not on every page load
4. **Structured naming** - Makes querying and analysis possible at scale

**When to use PostHog analytics:**

- Product decisions need data (feature adoption, conversion funnels)
- B2B apps needing organization-level metrics
- User journey analysis and retention tracking
- A/B test result analysis

**When NOT to use analytics:**

- Debug logging (use structured logs instead)
- Error tracking (use Sentry or similar)
- Infrastructure metrics (use observability tools)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Event Naming Conventions

Use the **category:object_action** framework for consistent, queryable event names.

**Format:** `category:object_action`

- **category**: Context (signup_flow, settings, dashboard)
- **object**: Component/location (password_button, pricing_page)
- **action**: Present-tense verb (click, submit, view)

**Examples:**

```typescript
// Signup flow events
"signup_flow:email_form_submit";
"signup_flow:google_oauth_click";
"signup_flow:verification_email_sent";

// Dashboard events
"dashboard:project_create";
"dashboard:invite_member_click";

// Alternative format: object_verb (simpler, still good)
"project_created";
"user_signed_up";
```

**Why good:** Category prefix groups related events in PostHog UI, enables wildcard queries like `signup_flow:*`, consistent naming makes analysis possible at scale.

**Property Naming Conventions:**

- `object_adjective`: `project_id`, `plan_name`, `item_count`
- `is_` or `has_` for booleans: `is_first_purchase`, `has_completed_onboarding`
- `_date` or `_timestamp` suffix: `trial_end_date`, `last_login_timestamp`

For complete code examples, see [examples/core.md](examples/core.md#pattern-1-event-naming-conventions).

---

### Pattern 2: User Identification with Authentication

Integrate PostHog identification with your authentication flow.

**Key Rules:**

1. Call `identify()` only on auth state change (not every render)
2. Check `_isIdentified()` to prevent duplicate calls
3. Use database user ID as `distinct_id` (not email)
4. Call `reset()` on logout to unlink future events

**Client-Side Flow:**

```typescript
// In useAnalyticsIdentify hook
useEffect(() => {
  if (session?.user && !posthog._isIdentified()) {
    posthog.identify(session.user.id, {
      plan: session.user.plan ?? "free",
      created_at: session.user.createdAt,
      is_verified: session.user.emailVerified ?? false,
    });
  }
}, [session?.user]);
```

**Logout Reset:**

```typescript
const handleLogout = async () => {
  posthog?.capture("user_logged_out");
  posthog?.reset(); // Unlink future events
  await authClient.signOut();
};
```

For complete implementation with constants and hooks, see [examples/core.md](examples/core.md#pattern-2-user-identification-with-authentication).

---

### Pattern 3: Server-Side Tracking

Track business events reliably from your backend with posthog-node.

**Key Rules:**

1. Always include `distinctId` (user's database ID)
2. Use `captureImmediate()` for serverless (guarantees HTTP completion)
3. Always call `shutdown()` before returning in serverless
4. Configure `flushAt: 1` and `flushInterval: 0` for serverless

**Server Client Setup:**

```typescript
export const posthogServer = new PostHog(POSTHOG_KEY, {
  host: POSTHOG_HOST,
  flushAt: 1, // Flush after 1 event (serverless)
  flushInterval: 0, // Don't batch (serverless)
});
```

**Tracking in API Routes:**

```typescript
posthogServer.capture({
  distinctId: user.id, // REQUIRED
  event: "project_created",
  properties: {
    project_id: project.id,
    is_first_project: user.projectCount === 0,
  },
});
await posthogServer.shutdown(); // REQUIRED for serverless
```

For complete Hono route examples, see [examples/server-tracking.md](examples/server-tracking.md).

</patterns>

---

<performance>

## Performance Optimization

**Web Apps (default batching):**

```typescript
posthog.init(POSTHOG_KEY, {
  api_host: "/ingest",
  // Default batching is efficient - don't override
});
```

**Serverless (immediate delivery):**

```typescript
const posthogServer = new PostHog(POSTHOG_KEY, {
  flushAt: 1, // Flush after 1 event
  flushInterval: 0, // No interval batching
});

// Option 1: Use captureImmediate (preferred - guarantees completion)
await posthogServer.captureImmediate({ distinctId, event, properties });

// Option 2: Use capture + shutdown
posthogServer.capture({ distinctId, event, properties });
await posthogServer.shutdown(); // Ensures all events sent before termination
```

**Reducing Costs:**

```typescript
posthog.init(POSTHOG_KEY, {
  person_profiles: "identified_only", // Anonymous events 4x cheaper
  autocapture: false, // Optional: disable for high-traffic
});
```

</performance>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST call `posthog.identify()` ONLY when a user signs up or logs in - never on every page load)**

**(You MUST include the user's database ID as `distinct_id` in ALL server-side events)**

**(You MUST call `posthog.reset()` when a user logs out to unlink future events)**

**(You MUST use the `category:object_action` naming convention for all custom events)**

**(You MUST NEVER include PII (email, name, phone) in event properties - use user IDs only)**

**Failure to follow these rules will cause analytics data quality issues, privacy violations, or lost events.**

</critical_reminders>

---

## Sources

- [PostHog Event Tracking Guide](https://posthog.com/tutorials/event-tracking-guide)
- [PostHog Best Practices](https://posthog.com/docs/product-analytics/best-practices)
- [PostHog User Identification](https://posthog.com/docs/getting-started/identify-users)
- [PostHog Group Analytics](https://posthog.com/docs/product-analytics/group-analytics)
- [PostHog GDPR Compliance](https://posthog.com/docs/privacy/gdpr-compliance)
- [PostHog Node.js SDK](https://posthog.com/docs/libraries/node)
- [PostHog Next.js Integration](https://posthog.com/docs/libraries/next-js)
- [PostHog React Integration](https://posthog.com/docs/libraries/react)
