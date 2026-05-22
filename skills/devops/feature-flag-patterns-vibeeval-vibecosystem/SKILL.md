---
name: feature-flag-patterns
description: Gradual rollout strategies, kill switches, A/B testing integration, flag lifecycle management, and technical debt prevention.
---

# Feature Flag Patterns

Feature flag strategies for safe deployments, experimentation, and operational control.

## Flag Types and Structure

```typescript
interface FeatureFlag {
  key: string
  type: 'boolean' | 'percentage' | 'variant' | 'segment'
  enabled: boolean
  description: string
  owner: string              // Team/person responsible
  createdAt: Date
  expiresAt?: Date           // Auto-cleanup reminder
  tags: string[]             // 'release', 'experiment', 'ops', 'permission'
}

// Flag categories by lifecycle
enum FlagCategory {
  RELEASE = 'release',       // Temporary: ship behind flag, remove after rollout
  EXPERIMENT = 'experiment', // Temporary: A/B test, remove after analysis
  OPS = 'ops',               // Long-lived: kill switches, circuit breakers
  PERMISSION = 'permission', // Long-lived: premium features, entitlements
}

// Flag configuration
const FLAGS: Record<string, FeatureFlag> = {
  'new-checkout-flow': {
    key: 'new-checkout-flow',
    type: 'percentage',
    enabled: true,
    description: 'Redesigned checkout with fewer steps',
    owner: 'checkout-team',
    createdAt: new Date('2025-01-15'),
    expiresAt: new Date('2025-04-15'),   // 3 month max
    tags: ['release'],
  },
  'emergency-read-only': {
    key: 'emergency-read-only',
    type: 'boolean',
    enabled: false,
    description: 'Kill switch: disable all write operations',
    owner: 'platform-team',
    createdAt: new Date('2024-06-01'),
    tags: ['ops'],
  },
}
```

## Gradual Rollout

```typescript
class FeatureFlagService {
  constructor(private store: FlagStore) {}

  // Percentage-based rollout using consistent hashing
  isEnabled(flagKey: string, userId: string): boolean {
    const flag = this.store.getFlag(flagKey)
    if (!flag || !flag.enabled) return false

    switch (flag.type) {
      case 'boolean':
        return flag.enabled

      case 'percentage': {
        // Consistent: same user always gets same result for same flag
        const hash = this.consistentHash(flagKey, userId)
        return hash < (flag.percentage ?? 0)
      }

      case 'segment':
        return this.isInSegment(userId, flag.segments ?? [])

      case 'variant':
        return true  // Use getVariant() instead
    }
  }

  // Deterministic hash: user always gets same bucket for same flag
  private consistentHash(flagKey: string, userId: string): number {
    const input = `${flagKey}:${userId}`
    let hash = 0
    for (let i = 0; i < input.length; i++) {
      const char = input.charCodeAt(i)
      hash = ((hash << 5) - hash) + char
      hash = hash & hash  // Convert to 32-bit integer
    }
    return Math.abs(hash) % 100  // 0-99
  }

  // Multi-variant for A/B/C testing
  getVariant(flagKey: string, userId: string): string {
    const flag = this.store.getFlag(flagKey)
    if (!flag?.enabled || !flag.variants) return 'control'

    const hash = this.consistentHash(flagKey, userId)
    let cumulative = 0
    for (const variant of flag.variants) {
      cumulative += variant.weight
      if (hash < cumulative) return variant.name
    }
    return 'control'
  }

  // Segment-based targeting
  private isInSegment(userId: string, segments: Segment[]): boolean {
    const user = this.store.getUser(userId)
    return segments.some(segment => {
      switch (segment.type) {
        case 'user_list': return segment.userIds.includes(userId)
        case 'attribute': return user?.[segment.attribute] === segment.value
        case 'percentage': return this.consistentHash(segment.id, userId) < segment.value
      }
    })
  }
}
```

## Kill Switch Pattern

```typescript
// Operational flags: immediately disable features under load
class KillSwitch {
  private cache = new Map<string, { value: boolean; expiry: number }>()
  private pollInterval: NodeJS.Timeout

  constructor(private store: FlagStore, pollMs: number = 5000) {
    // Poll every 5s for kill switch changes (fast response)
    this.pollInterval = setInterval(() => this.refresh(), pollMs)
  }

  isKilled(switchKey: string): boolean {
    const cached = this.cache.get(switchKey)
    if (cached && cached.expiry > Date.now()) {
      return cached.value
    }
    // Fallback: if cache miss, assume NOT killed (fail open)
    return false
  }

  private async refresh(): Promise<void> {
    try {
      const switches = await this.store.getKillSwitches()
      for (const [key, value] of Object.entries(switches)) {
        this.cache.set(key, { value, expiry: Date.now() + 10_000 })
      }
    } catch {
      // On error, extend existing cache TTL (don't flip switches on failure)
    }
  }

  destroy(): void {
    clearInterval(this.pollInterval)
  }
}

// Usage in request handler
async function handleCheckout(req: Request, res: Response) {
  if (killSwitch.isKilled('checkout-disabled')) {
    return res.status(503).json({
      error: 'Checkout temporarily unavailable',
      retryAfter: 300,
    })
  }
  // ... normal checkout logic
}
```

## A/B Testing Integration

```typescript
// Track experiment exposure and outcomes
interface ExperimentEvent {
  experimentKey: string
  variant: string
  userId: string
  timestamp: Date
  eventType: 'exposure' | 'conversion'
  metadata?: Record<string, unknown>
}

class ExperimentTracker {
  constructor(private analytics: AnalyticsClient) {}

  trackExposure(flagKey: string, variant: string, userId: string): void {
    this.analytics.track({
      experimentKey: flagKey,
      variant,
      userId,
      timestamp: new Date(),
      eventType: 'exposure',
    })
  }

  trackConversion(flagKey: string, userId: string, value?: number): void {
    this.analytics.track({
      experimentKey: flagKey,
      variant: featureFlags.getVariant(flagKey, userId),
      userId,
      timestamp: new Date(),
      eventType: 'conversion',
      metadata: { value },
    })
  }
}

// Usage: checkout experiment
function CheckoutPage({ user }: { user: User }) {
  const variant = featureFlags.getVariant('checkout-redesign', user.id)
  experimentTracker.trackExposure('checkout-redesign', variant, user.id)

  if (variant === 'new') {
    return <NewCheckout onComplete={() => {
      experimentTracker.trackConversion('checkout-redesign', user.id)
    }} />
  }
  return <OldCheckout onComplete={() => {
    experimentTracker.trackConversion('checkout-redesign', user.id)
  }} />
}
```

## Flag Lifecycle and Cleanup

```typescript
// Prevent flag debt: enforce expiration dates
async function auditFlags(): Promise<FlagAuditReport> {
  const flags = await flagStore.getAllFlags()
  const now = new Date()

  const report: FlagAuditReport = {
    total: flags.length,
    expired: [],
    noOwner: [],
    stale: [],
    permanent: [],
  }

  for (const flag of flags) {
    // Expired flags: should have been removed
    if (flag.expiresAt && flag.expiresAt < now) {
      report.expired.push(flag.key)
    }

    // No owner: nobody responsible for cleanup
    if (!flag.owner) {
      report.noOwner.push(flag.key)
    }

    // Stale: 100% rollout for > 2 weeks (just remove the flag)
    if (flag.type === 'percentage' && flag.percentage === 100) {
      const twoWeeksAgo = new Date(now.getTime() - 14 * 24 * 60 * 60 * 1000)
      if (flag.lastModified && flag.lastModified < twoWeeksAgo) {
        report.stale.push(flag.key)
      }
    }

    // Permanent flags without ops/permission tag
    if (!flag.expiresAt && !flag.tags.includes('ops') && !flag.tags.includes('permission')) {
      report.permanent.push(flag.key)
    }
  }

  return report
}

// Run weekly: flag cleanup report
// Slack alert for expired/stale flags
```

## Checklist

- [ ] Every release flag has an expiration date (max 3 months)
- [ ] Every flag has an owner (team or person)
- [ ] Consistent hashing for percentage rollout (same user, same result)
- [ ] Kill switches poll every 5-10 seconds (fast disable)
- [ ] A/B test exposure tracked before showing variant
- [ ] Flag audit runs weekly (detect expired, stale, ownerless flags)
- [ ] Remove flag code after full rollout (not just set to 100%)
- [ ] Default to safe value when flag service is unavailable (fail open/closed per flag)

## Anti-Patterns

- Flags without expiration dates: accumulate as permanent technical debt
- Nested flag checks: `if flagA && flagB && !flagC` becomes unmaintainable
- Flag evaluation in hot loops: cache the result per request
- Not tracking experiment exposure: biased results, no statistical power
- Removing flag from config but leaving dead code branches
- Using flags for authorization (use proper RBAC/permissions instead)
