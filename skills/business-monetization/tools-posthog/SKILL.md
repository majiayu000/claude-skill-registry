---
name: tools-posthog
description: Standard pattern for implementing freemium/pro features with PostHog feature flags, usage tracking, upgrade prompts, and Stripe-ready payment hooks. Use when adding any feature that will eventually be paid.
---

# Feature Gating Skill

Pattern for implementing freemium/pro features with per-user feature flags, usage measurement, and payment-ready architecture.

## When to Use

- Adding a feature that will eventually be paid/pro-only
- A/B testing feature availability
- Gradual rollouts to user segments
- Gating existing features for pro users
- Measuring demand before building paywall

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                     PostHog                              │
│  ┌─────────────────────────────────────────────────────┐│
│  │ Feature Flag: cloud-notes-sync                      ││
│  │ Targeting: plan = 'pro' OR beta-tester = true       ││
│  └─────────────────────────────────────────────────────┘│
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                    Client                                │
│  ┌─────────────────┐  ┌────────────────────────────────┐│
│  │ useProFeature() │──│ Feature Component              ││
│  │ - enabled       │  │ - Show feature if enabled      ││
│  │ - trackAttempt  │  │ - Show upgrade prompt if not   ││
│  └─────────────────┘  └────────────────────────────────┘│
└──────────────────────────────────────────────────────────┘
```

---

## Part 1: PostHog Feature Flags

### Naming Convention

Use descriptive, kebab-case names:

```
{feature-name}-enabled

Examples:
- cloud-notes-sync
- advanced-models
- export-features
- unlimited-messages
```

### Creating Flags in PostHog Dashboard

1. Go to **Feature Flags** → **New Feature Flag**
2. **Key**: `cloud-notes-sync`
3. **Rollout**: Start at 0% (disabled)
4. **Targeting** (when ready to enable):
   - Beta testers: `beta-tester` is `true`
   - Pro users: `plan` is `pro`
   - Percentage rollout: 10% → 50% → 100%

### PostHog User Properties (for targeting)

Set these properties when user state changes:

```typescript
// When user subscribes
posthog.setPersonProperties({ 
  plan: 'pro',
  subscribed_at: new Date().toISOString(),
})

// When user joins beta
posthog.setPersonProperties({ 
  'beta-tester': true,
})
```

---

## Part 2: Feature Flag Hooks

### Basic Hook

```typescript
// hooks/useFeatureFlags.ts

import { useEffect, useState, useCallback } from 'react'
import { posthog } from '@/lib/posthog'

export function useFeatureFlag(flagKey: string): boolean {
  const [enabled, setEnabled] = useState(false)
  
  useEffect(() => {
    if (typeof window === 'undefined') return
    
    const checkFlag = () => {
      const value = posthog.isFeatureEnabled(flagKey)
      setEnabled(value ?? false)
    }
    
    if (posthog.__loaded) checkFlag()
    posthog.onFeatureFlags(checkFlag)
  }, [flagKey])
  
  return enabled
}
```

### Pro Feature Hook (with tracking)

```typescript
export function useProFeature(flagKey: string): {
  enabled: boolean
  loading: boolean
  trackAttempt: () => void
  trackUpgradeShown: () => void
  trackUpgradeClicked: () => void
} {
  const [enabled, setEnabled] = useState(false)
  const [loading, setLoading] = useState(true)
  
  useEffect(() => {
    const checkFlag = () => {
      setEnabled(posthog.isFeatureEnabled(flagKey) ?? false)
      setLoading(false)
    }
    
    if (posthog.__loaded) checkFlag()
    posthog.onFeatureFlags(checkFlag)
  }, [flagKey])
  
  const trackAttempt = useCallback(() => {
    posthog.capture(`${flagKey}_attempted`)
  }, [flagKey])
  
  const trackUpgradeShown = useCallback(() => {
    posthog.capture(`${flagKey}_upgrade_shown`)
  }, [flagKey])
  
  const trackUpgradeClicked = useCallback(() => {
    posthog.capture(`${flagKey}_upgrade_clicked`)
  }, [flagKey])
  
  return { enabled, loading, trackAttempt, trackUpgradeShown, trackUpgradeClicked }
}
```

### Typed Convenience Hooks

Create specific hooks for each feature:

```typescript
export function useCloudNotesSync() {
  return useProFeature('cloud-notes-sync')
}

export function useAdvancedModels() {
  return useProFeature('advanced-models')
}
```

---

## Part 3: Usage Tracking Events

Track feature usage to measure demand and conversion:

### Event Schema

| Event | When | Properties |
|-------|------|------------|
| `{feature}_attempted` | User tries to use gated feature | `{ feature }` |
| `{feature}_completed` | Feature used successfully | `{ feature, duration_ms? }` |
| `{feature}_upgrade_shown` | Upgrade prompt displayed | `{ feature, trigger }` |
| `{feature}_upgrade_clicked` | User clicked upgrade CTA | `{ feature }` |

### Implementation

```typescript
// Track when user tries to use feature
const handleFeatureClick = () => {
  if (!cloudSync.enabled) {
    cloudSync.trackAttempt()
    cloudSync.trackUpgradeShown()
    setShowUpgradeModal(true)
    return
  }
  // ... feature logic
}
```

---

## Part 4: Upgrade Prompt Patterns

### Modal Pattern

```tsx
function UpgradeModal({ feature, onClose }: { feature: string; onClose: () => void }) {
  const { trackUpgradeClicked } = useProFeature(feature)
  
  return (
    <Dialog open onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Upgrade to Pro</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <p>Get access to cloud sync and more for just $7/month.</p>
          <ul className="space-y-2">
            <li>✓ Sync notes across devices</li>
            <li>✓ Cloud backup</li>
            <li>✓ Export options</li>
          </ul>
          <Button 
            onClick={() => {
              trackUpgradeClicked()
              window.location.href = '/pricing'
            }}
          >
            Upgrade Now — $7/mo
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  )
}
```

### Inline Lock Pattern

```tsx
function FeatureLock({ 
  feature, 
  children 
}: { 
  feature: string
  children: React.ReactNode 
}) {
  const { enabled, loading, trackAttempt, trackUpgradeShown } = useProFeature(feature)
  
  if (loading) return <Skeleton />
  
  if (!enabled) {
    useEffect(() => {
      trackAttempt()
      trackUpgradeShown()
    }, [])
    
    return (
      <div className="relative">
        <div className="opacity-50 pointer-events-none blur-sm">
          {children}
        </div>
        <div className="absolute inset-0 flex items-center justify-center">
          <ProBadge />
          <span>Pro Feature</span>
        </div>
      </div>
    )
  }
  
  return <>{children}</>
}
```

---

## Part 5: Stripe-Ready Architecture

Structure code so payment integration is additive:

### Current (Pre-Stripe)

```typescript
// User properties are set manually or via feature flags
posthog.setPersonProperties({ plan: 'free' })
```

### Future (With Stripe)

```typescript
// After Stripe webhook confirms subscription
const handleSubscriptionCreated = async (subscription: Stripe.Subscription) => {
  const plan = subscription.items.data[0].price.lookup_key // 'pro' or 'free'
  
  // Update PostHog for feature flag targeting
  posthog.setPersonProperties({ 
    plan,
    stripe_customer_id: subscription.customer,
    subscribed_at: new Date().toISOString(),
  })
  
  // PostHog flag `cloud-notes-sync` targets `plan: 'pro'`
  // Features automatically unlock
}
```

### Pricing Page Structure

```tsx
// app/pricing/page.tsx
export default function PricingPage() {
  return (
    <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
      <PricingCard
        plan="Free"
        price="$0"
        features={[
          'Local notes storage',
          '50 AI messages/day',
          'Basic Bible reading',
        ]}
        cta="Current Plan"
        disabled
      />
      <PricingCard
        plan="Pro"
        price="$7"
        period="/month"
        features={[
          'Cloud sync across devices',
          'Unlimited AI messages',
          'Advanced AI models',
          'Export notes & highlights',
          'Priority support',
        ]}
        cta="Upgrade to Pro"
        highlighted
        onClick={() => {/* Stripe checkout */}}
      />
    </div>
  )
}
```

---

## Part 6: Implementation Checklist

When adding a new pro feature:

### Setup
- [ ] Create PostHog feature flag in dashboard
- [ ] Add typed hook in `useFeatureFlags.ts`
- [ ] Export from hooks barrel file

### Implementation
- [ ] Use hook in feature component
- [ ] Gate feature behind `enabled` check
- [ ] Show upgrade prompt when `!enabled`

### Tracking
- [ ] Track `_attempted` when user tries to use
- [ ] Track `_upgrade_shown` when prompt displays
- [ ] Track `_upgrade_clicked` when user clicks CTA
- [ ] Track `_completed` when feature is used successfully

### Documentation
- [ ] Add to TASKS.md if significant feature
- [ ] Document in this skill if pattern evolves

---

## Quick Reference

| Item | Pattern |
|------|---------|
| Flag naming | `{feature-name}` (kebab-case) |
| Hook | `useProFeature('flag-key')` |
| Tracking | `trackAttempt()`, `trackUpgradeShown()`, `trackUpgradeClicked()` |
| Targeting | Set `plan: 'pro'` in PostHog properties |
| Typical price | $5-15/month for indie SaaS |

---

## Example Use Cases

| Feature | Free | Pro |
|---------|------|-----|
| Cloud sync | Local storage only | Cross-device sync |
| API usage | 25 calls/day | Unlimited |
| AI models | GPT-4o-mini | Claude, GPT-4o, etc. |
| Export | None | PDF, Markdown |
| Support | Community | Priority |
