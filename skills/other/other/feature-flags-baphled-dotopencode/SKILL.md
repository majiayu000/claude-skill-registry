---
name: feature-flags
description: Safe feature rollouts using feature flags, gradual releases, and A/B testing
category: DevOps & Operations
---

# Skill: feature-flags

## What I do

I provide expertise in decoupling deployment from release. I enable runtime control of feature availability, gradual rollouts (1% → 100%), A/B testing, and operational kill-switches without new code deployments.

## When to use me

- Releasing new features gradually to mitigate risk
- A/B testing different implementations/UI variants
- Trunk-based development with incomplete features
- Emergency feature disablement (kill switches)
- User segment targeting (e.g., beta testers only)

## Core principles

1. **Decouple Deploy from Release** — Deploy code continuously; release features through configuration.
2. **Short-Lived by Default** — Release flags are temporary; remove them once 100% rolled out to avoid debt.
3. **Fail Safe** — If flag evaluation fails, always default to the "safe" (usually legacy/disabled) state.
4. **Gradual Rollout** — Progressively increase exposure (1% → 5% → 25% → 100%) and monitor metrics.
5. **Fast Toggle** — Changes must take effect in seconds without application restart.

## Patterns & examples

**Release Toggle Pattern (Go):**
```go
if features.IsEnabled("new-checkout-flow") {
    return newCheckoutFlow(ctx, order)
}
return legacyCheckoutFlow(ctx, order)
```

**Percentage-Based Rollout (Go):**
```go
func (f *FlagStore) IsEnabledForUser(flagName, userID string) bool {
    // ... hash userID and check against rollout percentage
    hash := hashString(userID)
    bucket := hash % 100
    return bucket < uint32(f.flags[flagName].RolloutPercentage)
}
```

**Experiment Variants:**
```go
variant := features.GetVariant("button-color")
switch variant {
case "red":   return renderRedButton()
case "green": return renderGreenButton()
default:      return renderBlueButton()
}
```

## Anti-patterns to avoid

- ❌ **Flag Sprawl** — Accumulating hundreds of old flags; implement a "cleanup" task after 100% rollout.
- ❌ **Testing only one path** — Always test both the flag-enabled AND the fallback path.
- ❌ **200 for everything** — Ensure your flag system failures don't return 200 OK with broken UI.
- ❌ **Ignoring Metrics** — Increasing rollout percentage without checking error rates/latency.
- ❌ **Hardcoding Defaults** — Use a central configuration source rather than scattered hardcoded checks.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Delivery/Feature Flags.md`

## Related skills

- `devops` — Pipelines that deploy flagged code
- `monitoring` — Observability during gradual rollouts
- `configuration-management` — Managing secrets and environment-specific flags
- `breaking-changes` — Using flags to manage risky API or schema transitions
