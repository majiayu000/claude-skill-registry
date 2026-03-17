---
name: api-flags-posthog-flags
description: PostHog feature flags, rollouts, A/B testing. Use when implementing gradual rollouts, A/B tests, kill switches, remote configuration, beta features, or user targeting with PostHog.
---

# Feature Flags with PostHog

> **Quick Guide:** Use PostHog feature flags for gradual rollouts, A/B testing, and remote configuration. Client-side: `useFeatureFlagEnabled` hook. Server-side: `posthog-node` with local evaluation. Always pair `useFeatureFlagPayload` with `useFeatureFlagEnabled` for experiments.

---

**Detailed Resources:**

- For code examples, see [examples/core.md](examples/core.md)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

**Topic-Specific Examples:**

- [examples/payloads.md](examples/payloads.md) - Remote configuration with JSON payloads
- [examples/server-side.md](examples/server-side.md) - Server-side evaluation with posthog-node
- [examples/rollouts.md](examples/rollouts.md) - Gradual rollouts and user targeting
- [examples/experiments.md](examples/experiments.md) - A/B testing with experiments
- [examples/development.md](examples/development.md) - Local development overrides
- [examples/lifecycle.md](examples/lifecycle.md) - Flag cleanup and lifecycle management

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
- User and cohort targeting
- A/B testing and experiments
- Payloads for remote configuration
- Local development overrides
- Flag cleanup and lifecycle management

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

Use `useFeatureFlagEnabled` for simple on/off features. Handle the `undefined` loading state.

#### Constants

```typescript
// lib/feature-flags.ts
export const FLAG_NEW_CHECKOUT = "new-checkout-flow";
export const FLAG_DARK_MODE = "dark-mode-enabled";
export const FLAG_BETA_DASHBOARD = "beta-dashboard";
```

#### Implementation

```typescript
// components/checkout-button.tsx
import { useFeatureFlagEnabled } from "posthog-js/react";

import { FLAG_NEW_CHECKOUT } from "@/lib/feature-flags";

// Good Example - Handle undefined state
export const CheckoutButton = () => {
  const isNewCheckout = useFeatureFlagEnabled(FLAG_NEW_CHECKOUT);

  // Flag is loading - show nothing or skeleton
  if (isNewCheckout === undefined) {
    return <ButtonSkeleton />;
  }

  // Flag resolved - render appropriate UI
  if (isNewCheckout) {
    return <NewCheckoutButton />;
  }

  return <LegacyCheckoutButton />;
};
```

**Why good:** Named constant prevents typos, undefined check prevents flash of wrong content, explicit handling of all states

For more examples including bad patterns, see [examples/core.md](examples/core.md#pattern-1-client-side-boolean-flags).

---

### Pattern 2: Multivariate Flags and Variants

Use `useFeatureFlagVariantKey` for A/B tests with multiple variants.

#### Constants

```typescript
// lib/feature-flags.ts
export const FLAG_PRICING_PAGE = "pricing-page-experiment";

// Variant constants prevent typos
export const VARIANT_CONTROL = "control";
export const VARIANT_SIMPLE = "simple";
export const VARIANT_DETAILED = "detailed";
```

#### Implementation

```typescript
// components/pricing-page.tsx
import { useFeatureFlagVariantKey } from "posthog-js/react";

import {
  FLAG_PRICING_PAGE,
  VARIANT_CONTROL,
  VARIANT_SIMPLE,
  VARIANT_DETAILED,
} from "@/lib/feature-flags";

// Good Example - Multivariate flag with loading state
export const PricingPage = () => {
  const variant = useFeatureFlagVariantKey(FLAG_PRICING_PAGE);

  // Loading state
  if (variant === undefined) {
    return <PricingPageSkeleton />;
  }

  // Render based on variant
  switch (variant) {
    case VARIANT_SIMPLE:
      return <SimplePricing />;
    case VARIANT_DETAILED:
      return <DetailedPricing />;
    case VARIANT_CONTROL:
    default:
      return <ControlPricing />;
  }
};
```

**Why good:** Variant constants prevent typos, switch statement handles all cases, default fallback to control variant, loading state prevents flash

For more examples, see [examples/core.md](examples/core.md#pattern-2-multivariate-flags-and-variants).

---

### Pattern 3: Server-Side Flag Evaluation

Use `posthog-node` for server-side evaluation. Use local evaluation for performance.

#### Setup

```typescript
// lib/posthog-server.ts
import { PostHog } from "posthog-node";

const POSTHOG_POLL_INTERVAL_MS = 30000; // 30 seconds
const FLAG_REQUEST_TIMEOUT_MS = 3000; // 3 seconds (default)

// Initialize with local evaluation
// Use the Feature Flags Secure API Key (phs_*) from project settings
// Personal API keys are deprecated for local evaluation
export const posthog = new PostHog(process.env.POSTHOG_API_KEY!, {
  host: process.env.POSTHOG_HOST || "https://us.i.posthog.com",
  // Enable local evaluation with feature flags secure key (phs_*)
  personalApiKey: process.env.POSTHOG_FEATURE_FLAGS_KEY,
  // Poll for flag definition updates
  featureFlagsPollingInterval: POSTHOG_POLL_INTERVAL_MS,
  // Timeout for flag evaluation requests
  featureFlagsRequestTimeoutMs: FLAG_REQUEST_TIMEOUT_MS,
});

// Named export
export { posthog };
```

#### API Route Usage

```typescript
// app/api/dashboard/route.ts
import { NextRequest, NextResponse } from "next/server";

import { posthog } from "@/lib/posthog-server";
import { FLAG_BETA_DASHBOARD } from "@/lib/feature-flags";

// Good Example - Server-side flag evaluation
export async function GET(request: NextRequest) {
  const userId = request.headers.get("x-user-id");

  if (!userId) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  // Evaluate flag server-side with user context
  const isBetaDashboard = await posthog.isFeatureEnabled(
    FLAG_BETA_DASHBOARD,
    userId,
    {
      // Provide person properties for targeting rules
      personProperties: {
        email: request.headers.get("x-user-email"),
        plan: request.headers.get("x-user-plan"),
      },
    }
  );

  if (isBetaDashboard) {
    return NextResponse.json({ dashboard: "beta", features: [...] });
  }

  return NextResponse.json({ dashboard: "stable", features: [...] });
}
```

**Why good:** Local evaluation reduces latency (500ms to 10-50ms), personProperties enable targeting, server-side prevents client manipulation

For more examples including bad patterns, local-only evaluation, and distributed environments, see [examples/server-side.md](examples/server-side.md).

</patterns>

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
