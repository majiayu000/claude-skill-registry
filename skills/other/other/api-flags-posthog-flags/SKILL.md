---
name: api-flags-posthog-flags
description: PostHog feature flags, rollouts, A/B testing. Use when implementing gradual rollouts, A/B tests, kill switches, remote configuration, beta features, or user targeting with PostHog.
---

# Feature Flags with PostHog

> **Quick Guide:** Use PostHog feature flags for gradual rollouts, A/B testing, and remote configuration. Client-side: `useFeatureFlagEnabled` hook. Server-side: `posthog-node` with local evaluation. Always pair `useFeatureFlagPayload` with `useFeatureFlagEnabled` for experiments. Handle the `undefined` loading state on every flag check.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST always pair `useFeatureFlagPayload` with `useFeatureFlagEnabled` or `useFeatureFlagVariantKey` for experiments - payload hooks don't send exposure events)**

**(You MUST use the feature flags secure API key (phs\_\*) for server-side local evaluation - personal API keys are deprecated for this use)**

**(You MUST handle the `undefined` state when flags are loading - never assume a flag is immediately available)**

**(You MUST include flag owner and expiry date in flag metadata - flags without owners become orphaned debt)**

**(You MUST wrap flag usage in a single function when used in multiple places - prevents orphaned flag code on cleanup)**

</critical_requirements>

---

**Auto-detection:** PostHog feature flags, useFeatureFlagEnabled, useFeatureFlagPayload, useFeatureFlagVariantKey, PostHogFeature, isFeatureEnabled, getFeatureFlag, gradual rollout, A/B test, experiment, multivariate flag

**When to use:**

- Gradual rollouts (deploy to 10% users, then 50%, then 100%)
- A/B testing with experiments (measure impact of changes)
- Kill switches (instantly disable features without deploy)
- Remote configuration (change behavior without code changes)
- Beta features opt-in (let users try new features)
- User targeting (show features to specific cohorts)

**When NOT to use:**

- Simple on/off switches that never change (use environment variables)
- Configuration that must be compile-time (use build flags)
- Secrets or sensitive data (use secret management)
- Features that should always be on (just ship the code)

**Key patterns covered:**

- Client-side flag evaluation with React hooks
- Server-side local evaluation for performance
- Boolean vs multivariate flags
- Gradual rollouts with percentage targeting
- A/B testing and experiments
- Payloads for remote configuration
- Local development overrides
- Flag cleanup and lifecycle management

---

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Boolean flags, multivariate flags, PostHogFeature component, payloads, experiments, rollouts, lifecycle management
- [examples/server-side.md](examples/server-side.md) - Server-side evaluation, local evaluation setup, distributed environments
- [examples/development.md](examples/development.md) - Local overrides, bootstrapping, onFeatureFlags callback
- [reference.md](reference.md) - Decision frameworks and anti-patterns

---

<philosophy>

## Philosophy

Feature flags decouple deployment from release. You can ship code to production but control who sees it and when. This enables:

1. **Safe releases** - Roll out to 1% first, monitor, then expand
2. **Fast rollback** - Toggle off instantly without deploying
3. **Data-driven decisions** - A/B test to measure impact
4. **Progressive delivery** - Beta users first, then everyone

**Core principles:**

- Flags are temporary - plan for cleanup from day one
- Flags have owners - someone is responsible for each flag
- Simple flags are better - percentage rollouts over complex conditions
- Handle undefined - flags load asynchronously

**When to use feature flags:**

- Risky features that need gradual rollout
- Features requiring A/B testing for validation
- Features that may need instant rollback
- Beta programs with user opt-in

**When NOT to use feature flags:**

- Every feature (creates maintenance burden)
- Permanent configuration (use config files)
- Features that are ready for 100% release

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Client-Side Boolean Flags

Use `useFeatureFlagEnabled` for simple on/off features. Always handle the `undefined` loading state -- treating it as `false` causes a flash of wrong UI.

```typescript
const isNewCheckout = useFeatureFlagEnabled(FLAG_NEW_CHECKOUT);

if (isNewCheckout === undefined) return <Skeleton />;   // Loading
if (isNewCheckout) return <NewCheckout />;               // Enabled
return <LegacyCheckout />;                               // Disabled
```

Store flag keys as named constants in `lib/feature-flags.ts` to prevent typos and enable cleanup-by-grep.

See [examples/core.md](examples/core.md#pattern-1-client-side-boolean-flags) for full good/bad examples.

---

### Pattern 2: Multivariate Flags and Variants

Use `useFeatureFlagVariantKey` for A/B tests with multiple variants. Define variant constants alongside the flag key. Switch on variants with a default fallback to `control`.

```typescript
const variant = useFeatureFlagVariantKey(FLAG_PRICING_PAGE);
if (variant === undefined) return <Skeleton />;

switch (variant) {
  case VARIANT_SIMPLE: return <SimplePricing />;
  case VARIANT_DETAILED: return <DetailedPricing />;
  default: return <ControlPricing />;
}
```

See [examples/core.md](examples/core.md#pattern-2-multivariate-flags-and-variants) for full example.

---

### Pattern 3: PostHogFeature Component

The `PostHogFeature` component provides automatic exposure tracking and built-in fallback handling with less boilerplate. Use `match={true}` for boolean flags or `match={VARIANT_KEY}` for specific variants.

```typescript
<PostHogFeature flag={FLAG_BETA} match={true} fallback={<Legacy />}>
  <NewFeature />
</PostHogFeature>
```

See [examples/core.md](examples/core.md#pattern-3-posthogfeature-component) for boolean and variant examples.

---

### Pattern 4: Payloads for Remote Configuration

Use `useFeatureFlagPayload` for dynamic JSON configuration. **Always pair with `useFeatureFlagEnabled`** -- the payload hook alone does NOT send exposure events, breaking experiment tracking.

```typescript
const isEnabled = useFeatureFlagEnabled(FLAG_BANNER); // Sends exposure event
const payload = useFeatureFlagPayload(FLAG_BANNER); // Gets config
const config = payload ?? DEFAULT_BANNER_CONFIG;
```

See [examples/core.md](examples/core.md#pattern-4-feature-flag-payloads-for-remote-configuration) for full good/bad examples.

---

### Pattern 5: Server-Side Flag Evaluation

Use `posthog-node` with the Feature Flags Secure API Key (`phs_*`) for local evaluation. This reduces latency from ~500ms (network call) to ~10-50ms (local). The `personalApiKey` config option takes the `phs_*` key despite its legacy name.

```typescript
export const posthog = new PostHog(process.env.POSTHOG_API_KEY!, {
  host: process.env.POSTHOG_HOST || "https://us.i.posthog.com",
  personalApiKey: process.env.POSTHOG_FEATURE_FLAGS_KEY, // phs_* key
  featureFlagsPollingInterval: POSTHOG_POLL_INTERVAL_MS, // default 5 min
});
```

See [examples/server-side.md](examples/server-side.md) for API handler usage, local-only evaluation, and distributed/serverless environments.

---

### Pattern 6: Flag Lifecycle and Cleanup

Every flag needs an owner, a creation date, and an expected removal date. Wrap flag checks in a single helper function so cleanup is a one-file change.

```typescript
/**
 * Owner: @john-doe | Created: 2025-01-15 | Remove by: 2025-02-15
 */
export const FLAG_NEW_CHECKOUT = "new-checkout-flow";

export function isNewCheckoutEnabled(flag: boolean | undefined): boolean {
  return flag === true; // When removing: change to `return true;`
}
```

See [examples/core.md](examples/core.md#pattern-7-flag-cleanup-and-lifecycle-management) for full documentation patterns and stale flag detection.

</patterns>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using `useFeatureFlagPayload` alone for experiments (no exposure tracking)
- Exposing Feature Flags Secure API key (`phs_*`) on client (security violation)
- No loading state handling (causes UI flash)
- Flags without owners or expiry dates (becomes permanent debt)

**Medium Priority Issues:**

- Magic string flag keys instead of constants (typos, hard to grep)
- Complex targeting rules on high-traffic flags (performance hit)
- Local evaluation in serverless/edge without external cache (cold start issues)
- Not using PostHog toolbar for local testing (harder debugging)

**Common Mistakes:**

- Checking flag in multiple places instead of wrapper function
- Not bootstrapping flags for SSR (content flash on hydration)
- Running experiments without defined primary metric
- Peeking at experiment results before completion
- Rolling out to 100% without cleanup plan

**Gotchas & Edge Cases:**

- PostHog uses deterministic hashing - same user always gets same variant
- Decreasing rollout percentage can remove users who were previously included
- Local evaluation requires Feature Flags Secure API Key (`phs_*`) - personal API keys are deprecated
- Flags load asynchronously - first render always has undefined
- GeoIP targeting uses server IP by default in posthog-node v3+
- Experiments need minimum 50 exposures per variant for results
- Stale flag = 100% rollout + not evaluated in 30 days
- `onFeatureFlags` callback receives `{ errorsLoading?: boolean }` as second parameter
- External cache providers (Redis, KV) are experimental - Node.js/Python SDKs only

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST always pair `useFeatureFlagPayload` with `useFeatureFlagEnabled` or `useFeatureFlagVariantKey` for experiments - payload hooks don't send exposure events)**

**(You MUST use the feature flags secure API key (phs\_\*) for server-side local evaluation - personal API keys are deprecated for this use)**

**(You MUST handle the `undefined` state when flags are loading - never assume a flag is immediately available)**

**(You MUST include flag owner and expiry date in flag metadata - flags without owners become orphaned debt)**

**(You MUST wrap flag usage in a single function when used in multiple places - prevents orphaned flag code on cleanup)**

**Failure to follow these rules will cause incorrect experiment results, security vulnerabilities, UI flashing, and technical debt.**

</critical_reminders>

---

## Sources

- [PostHog React Integration](https://posthog.com/docs/libraries/react)
- [PostHog Feature Flags](https://posthog.com/docs/feature-flags)
- [PostHog Feature Flag Best Practices](https://posthog.com/docs/feature-flags/best-practices)
- [PostHog Server-Side Local Evaluation](https://posthog.com/docs/feature-flags/local-evaluation)
- [PostHog Creating Feature Flags](https://posthog.com/docs/feature-flags/creating-feature-flags)
- [PostHog How to Do a Phased Rollout](https://posthog.com/tutorials/phased-rollout)
- [PostHog Feature Flag Testing](https://posthog.com/docs/feature-flags/testing)
- [PostHog Experiments](https://posthog.com/ab-testing)
- [PostHog Feature Flag Overrides](https://posthog.com/docs/toolbar/override-feature-flags)
- [Don't Make These Feature Flag Mistakes](https://posthog.com/newsletter/feature-flag-mistakes)
