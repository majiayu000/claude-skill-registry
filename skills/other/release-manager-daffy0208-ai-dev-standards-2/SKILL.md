---
name: release-manager
description: Ship features safely with progressive rollouts, feature flags, and canary deployments. Use when deploying risky features or need gradual rollouts.
license: Complete terms in LICENSE.txt
---

# Release Manager

Ship features safely with progressive rollouts.

## Progressive Rollout Strategy

```yaml
Phase 1 - Internal (Day 1):
  - 100% to internal team
  - Test thoroughly
  - Fix critical bugs

Phase 2 - Beta (Day 2-3):
  - 5% to beta users
  - Monitor errors/performance
  - Collect feedback

Phase 3 - Gradual (Day 4-7):
  - 25% of users
  - Watch metrics closely
  - 50% of users if good
  - 100% if still good

Phase 4 - Full Release:
  - 100% of users
  - Remove feature flag
  - Announce publicly
```

## Feature Flags

```typescript
// Feature flag implementation
const featureFlags = {
  newDashboard: {
    enabled: true,
    rollout: 0.25, // 25% of users
    userGroups: ['beta-testers'], // Always on for beta
  }
}

function isFeatureEnabled(feature, user) {
  const flag = featureFlags[feature]

  // Check user group
  if (user.groups.some(g => flag.userGroups.includes(g))) {
    return true
  }

  // Check rollout percentage
  const hash = hashUserId(user.id)
  return (hash % 100) < (flag.rollout * 100)
}

// Usage
{isFeatureEnabled('newDashboard', user) ? (
  <NewDashboard />
) : (
  <OldDashboard />
)}
```

## Deployment Strategies

### Blue-Green Deployment

```yaml
Process: 1. Deploy to "green" environment
  2. Test green thoroughly
  3. Switch traffic to green
  4. Keep blue as rollback

Pros: Instant rollback
Cons: 2x infrastructure cost
```

### Canary Deployment

```yaml
Process: 1. Deploy to 5% of servers
  2. Monitor for 1 hour
  3. If good, deploy to 25%
  4. Monitor for 1 hour
  5. If good, deploy to 100%

Pros: Gradual, safe
Cons: Slower rollout
```

## Rollback Plan

```yaml
Criteria for Rollback:
  - Error rate > 1%
  - Performance degradation > 20%
  - Critical bug discovered
  - Negative user feedback

Rollback Process: 1. Disable feature flag immediately
  2. Notify team
  3. Investigate issue
  4. Fix and redeploy
```

## Release Checklist

### Pre-Release

- [ ] Code reviewed
- [ ] Tests passing
- [ ] Staging tested
- [ ] Feature flag configured
- [ ] Rollback plan ready
- [ ] Monitoring alerts set

### During Release

- [ ] Deploy to 5% first
- [ ] Watch error rate
- [ ] Monitor performance
- [ ] Check user feedback
- [ ] Gradually increase

### Post-Release

- [ ] Monitor for 24 hours
- [ ] Collect feedback
- [ ] Remove feature flag
- [ ] Document learnings

## Monitoring

```yaml
Key Metrics During Release:
  - Error rate
  - Response time p95
  - CPU/memory usage
  - User-reported issues

Alerts:
  - Error rate > 1% → Pause rollout
  - Response time > 2s → Investigate
  - Memory spike > 90% → Rollback
```

## Communication

```yaml
Internal:
  - Slack announcement
  - Deploy log updated
  - Engineering team notified

External:
  - Changelog updated
  - Email to power users (if major)
  - Blog post (if significant)
```

## Summary

Safe releases:

- ✅ Start small (5%)
- ✅ Monitor closely
- ✅ Rollback readily
- ✅ Feature flags everywhere
- ✅ Document process
