---
name: posthog
description: >
  Implement PostHog analytics for PhotoVault with dual tracking (client + server).
  Use when working with event tracking, funnel analysis, user identification,
  TypeScript event schemas, ad-blocker-proof server-side tracking, or debugging
  missing analytics data. Includes PhotoVault event definitions and privacy defaults.
---

# ⚠️ MANDATORY WORKFLOW - DO NOT SKIP

**When this skill activates, you MUST follow the expert workflow before writing any code:**

1. **Spawn Domain Expert** using the Task tool with this prompt:
   ```
   Read the expert prompt at: C:\Users\natha\Stone-Fence-Brain\VENTURES\PhotoVault\claude\experts\posthog-expert.md

   Then research the codebase and write an implementation plan to: docs/claude/plans/posthog-[task-name]-plan.md

   Task: [describe the user's request]
   ```

2. **Spawn QA Critic** after expert returns, using Task tool:
   ```
   Read the QA critic prompt at: C:\Users\natha\Stone-Fence-Brain\VENTURES\PhotoVault\claude\experts\qa-critic-expert.md

   Review the plan at: docs/claude/plans/posthog-[task-name]-plan.md
   Write critique to: docs/claude/plans/posthog-[task-name]-critique.md
   ```

3. **Present BOTH plan and critique to user** - wait for approval before implementing

**DO NOT read files and start coding. DO NOT rationalize that "this is simple." Follow the workflow.**

---

# PostHog Analytics Integration

## Core Principles

### Dual Tracking is Non-Negotiable

Ad blockers block PostHog's client-side library in 30%+ of browsers. Critical funnel events MUST use server-side tracking.

```typescript
// CRITICAL EVENTS → Server-side (can't be blocked)
// - Signup, payment, churn, subscription changes
// - Anything that affects revenue attribution

// ENGAGEMENT EVENTS → Client-side (okay if some are blocked)
// - Page views, button clicks, gallery browsing
```

**Rule of thumb:** If losing 30% of this event would break your funnel analysis, it MUST be server-side.

### TypeScript Event Schemas Prevent Chaos

Without strict types, you'll end up with `gallery_id`, `galleryId`, `gallery-id`, and `GalleryId` in your data.

```typescript
// src/types/analytics.ts - EVERY event name and properties defined here
import { GalleryViewedEvent } from '@/types/analytics'
trackEvent<GalleryViewedEvent>('gallery_viewed', {
  gallery_id: '123',  // Type error if wrong name
})
```

### Identify Users Early and Consistently

```typescript
posthog.identify(user.id, {
  user_type: 'photographer' | 'client',
  signup_date: user.created_at,
})
```

## Anti-Patterns

**Only client-side tracking for critical events**
```typescript
// WRONG: 30%+ blocked by ad blockers
posthog.capture('payment_completed', { amount: 100 })

// RIGHT: Server-side for critical funnel events
await posthog.capture({
  distinctId: userId,
  event: 'payment_completed',
  properties: { amount: 100, $source: 'server' }
})
```

**Inconsistent property naming**
```typescript
// WRONG: Different properties in PostHog
{ gallery_id: '123' }
{ galleryId: '123' }
{ GalleryId: '123' }

// RIGHT: Use TypeScript types
trackEvent<GalleryViewedEvent>('gallery_viewed', { gallery_id: '123' })
```

**Forgetting to flush server-side events**
```typescript
// WRONG: Events lost if process exits
posthog.capture({ distinctId, event, properties })

// RIGHT: Flush in serverless
posthog.capture({ distinctId, event, properties })
await posthog.flush()
```

**Blocking user actions on analytics**
```typescript
// WRONG: User waits
await posthog.capture('form_submitted')
router.push('/success')

// RIGHT: Fire and forget
posthog.capture('form_submitted')
router.push('/success')
```

## Client-Side Setup

```typescript
// src/lib/analytics/client.ts
import posthog from 'posthog-js'

export function initPostHog() {
  if (typeof window === 'undefined') return

  posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY!, {
    api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST || 'https://app.posthog.com',
    capture_pageviews: true,
    respect_dnt: true,
    disable_session_recording: true,
    persistence: 'localStorage',
  })
}

export function identifyUser(userId: string, properties: Record<string, unknown>) {
  posthog.identify(userId, properties)
}

export function resetAnalytics() {
  posthog.reset()
}

export function trackEvent(eventName: string, properties?: Record<string, unknown>) {
  posthog.capture(eventName, properties)
}
```

## Server-Side Setup

```typescript
// src/lib/analytics/server.ts
import { PostHog } from 'posthog-node'

let posthogClient: PostHog | null = null

function getPostHogClient(): PostHog {
  if (!posthogClient) {
    posthogClient = new PostHog(process.env.POSTHOG_API_KEY!, {
      host: process.env.NEXT_PUBLIC_POSTHOG_HOST || 'https://app.posthog.com',
      flushAt: 1,
      flushInterval: 0,
    })
  }
  return posthogClient
}

export async function trackServerEvent(
  userId: string,
  eventName: string,
  properties?: Record<string, unknown>
) {
  const client = getPostHogClient()
  client.capture({
    distinctId: userId,
    event: eventName,
    properties: { ...properties, $source: 'server' },
  })
  await client.flush()
}
```

## usePageView Hook

```typescript
// src/hooks/useAnalytics.ts
'use client'

import { useEffect, useRef } from 'react'
import { trackEvent } from '@/lib/analytics/client'

export function usePageView(pageName: string, properties?: Record<string, unknown>) {
  const startTimeRef = useRef<number>(Date.now())
  const hasTrackedRef = useRef<boolean>(false)

  useEffect(() => {
    if (!hasTrackedRef.current) {
      trackEvent(`${pageName}_viewed`, properties)
      hasTrackedRef.current = true
      startTimeRef.current = Date.now()
    }

    return () => {
      const durationSeconds = Math.round((Date.now() - startTimeRef.current) / 1000)
      trackEvent(`${pageName}_left`, { ...properties, duration_seconds: durationSeconds })
    }
  }, [pageName])
}
```

## PhotoVault Configuration

### Critical Server-Side Events

| Event | Trigger | Why Critical |
|-------|---------|--------------|
| `photographer_signed_up` | Signup API | Top of funnel |
| `photographer_connected_stripe` | Connect callback | Conversion milestone |
| `client_payment_completed` | Stripe webhook | Revenue event |
| `client_payment_failed` | Stripe webhook | Churn risk signal |
| `photographer_churned` | Cancel subscription | Retention metric |

### Environment Variables

```bash
NEXT_PUBLIC_POSTHOG_KEY=phc_...
NEXT_PUBLIC_POSTHOG_HOST=https://app.posthog.com
POSTHOG_API_KEY=phc_...  # Same key, server-side
```

### Free Tier Limit

PostHog free tier: **1 million events/month**. Set alert at 800K.

## Debugging Checklist

1. Check PostHog Dashboard → Activity → Live Events
2. Verify user identification with `posthog.debug()` in dev
3. Check server-side events have `$source: 'server'` property
4. Verify flush is called in serverless functions
5. Test with ad blocker enabled (server events should still work)
