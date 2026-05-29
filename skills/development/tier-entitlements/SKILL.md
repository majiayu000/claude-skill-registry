---
name: tier-entitlements
description: Implement subscription tier-based feature gating and usage limits. Centralized tier configuration, database usage tracking, and clean APIs for checking limits.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: auth
  time: 3h
  source: drift-masterguide
---

# Tier-Based Entitlements

Gate features and track usage by subscription tier.

## When to Use This Skill

- Free users get limited features
- Pro users get unlimited access
- Need to track daily/monthly usage
- Want clean API for checking limits

## Core Concepts

1. **Tier config** - Single source of truth for all limits
2. **Usage tracking** - Database tracks consumption
3. **Atomic increments** - Prevent race conditions
4. **Rate limit headers** - Standard HTTP headers for clients

## TypeScript Implementation

### Tier Configuration

```typescript
// lib/tiers.ts

export const TIER_LIMITS = {
  free: {
    requestsPerDay: 10,
    storageGB: 1,
    historyDays: 7,
    exportEnabled: false,
    apiAccess: false,
    prioritySupport: false,
  },
  pro: {
    requestsPerDay: Infinity,
    storageGB: 100,
    historyDays: 365,
    exportEnabled: true,
    apiAccess: true,
    prioritySupport: false,
  },
  enterprise: {
    requestsPerDay: Infinity,
    storageGB: Infinity,
    historyDays: Infinity,
    exportEnabled: true,
    apiAccess: true,
    prioritySupport: true,
  },
} as const;

export type UserTier = keyof typeof TIER_LIMITS;
export type TierLimits = typeof TIER_LIMITS[UserTier];

export function getTierLimits(tier: UserTier): TierLimits {
  return TIER_LIMITS[tier] || TIER_LIMITS.free;
}
```

### Database Schema

```sql
-- migrations/001_user_profiles.sql

CREATE TABLE user_profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    subscription_tier VARCHAR(20) NOT NULL DEFAULT 'free',
    
    -- Usage tracking
    requests_today INTEGER DEFAULT 0,
    requests_date DATE DEFAULT CURRENT_DATE,
    storage_used_bytes BIGINT DEFAULT 0,
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Atomic increment function (prevents race conditions)
CREATE OR REPLACE FUNCTION increment_daily_usage(
    p_user_id UUID, 
    p_today DATE
)
RETURNS TABLE(new_count INTEGER, was_reset BOOLEAN) AS $$
DECLARE
    v_new_count INTEGER;
    v_was_reset BOOLEAN := FALSE;
BEGIN
    UPDATE user_profiles
    SET 
        requests_today = CASE 
            WHEN requests_date = p_today THEN requests_today + 1
            ELSE 1
        END,
        requests_date = p_today,
        updated_at = NOW()
    WHERE id = p_user_id
    RETURNING requests_today INTO v_new_count;
    
    -- Check if we reset (new day)
    v_was_reset := (SELECT requests_date != p_today FROM user_profiles WHERE id = p_user_id);
    
    RETURN QUERY SELECT v_new_count, v_was_reset;
END;
$$ LANGUAGE plpgsql;

-- Index for fast lookups
CREATE INDEX idx_user_profiles_tier ON user_profiles(subscription_tier);
```

### Rate Limit Functions

```typescript
// lib/rate-limits.ts
import type { SupabaseClient } from '@supabase/supabase-js';
import { TIER_LIMITS, type UserTier } from './tiers';

export interface RateLimitResult {
  allowed: boolean;
  limit: number;
  remaining: number;
  reset: number;  // Unix timestamp
  tier: UserTier;
}

export async function checkRateLimit(
  supabase: SupabaseClient,
  userId: string
): Promise<RateLimitResult> {
  const today = new Date().toISOString().split('T')[0];
  
  const { data: profile } = await supabase
    .from('user_profiles')
    .select('subscription_tier, requests_today, requests_date')
    .eq('id', userId)
    .single();

  if (!profile) {
    return {
      allowed: true,
      limit: TIER_LIMITS.free.requestsPerDay,
      remaining: TIER_LIMITS.free.requestsPerDay,
      reset: getResetTimestamp(),
      tier: 'free',
    };
  }

  const tier = (profile.subscription_tier as UserTier) || 'free';
  const limit = TIER_LIMITS[tier].requestsPerDay;

  // Unlimited tier
  if (limit === Infinity) {
    return {
      allowed: true,
      limit: -1,
      remaining: -1,
      reset: getResetTimestamp(),
      tier,
    };
  }

  // Check usage from today
  const used = profile.requests_date === today ? profile.requests_today : 0;
  const remaining = Math.max(0, limit - used);
  
  return {
    allowed: remaining > 0,
    limit,
    remaining,
    reset: getResetTimestamp(),
    tier,
  };
}

export async function incrementUsage(
  supabase: SupabaseClient,
  userId: string
): Promise<boolean> {
  const today = new Date().toISOString().split('T')[0];

  const { error } = await supabase.rpc('increment_daily_usage', {
    p_user_id: userId,
    p_today: today,
  });

  return !error;
}

function getResetTimestamp(): number {
  const tomorrow = new Date();
  tomorrow.setUTCDate(tomorrow.getUTCDate() + 1);
  tomorrow.setUTCHours(0, 0, 0, 0);
  return Math.floor(tomorrow.getTime() / 1000);
}

export function getRateLimitHeaders(result: RateLimitResult): Record<string, string> {
  const headers: Record<string, string> = {
    'X-RateLimit-Limit': result.limit === -1 ? 'unlimited' : String(result.limit),
    'X-RateLimit-Remaining': result.remaining === -1 ? 'unlimited' : String(result.remaining),
    'X-RateLimit-Reset': String(result.reset),
  };

  if (!result.allowed) {
    const retryAfter = result.reset - Math.floor(Date.now() / 1000);
    headers['Retry-After'] = String(Math.max(0, retryAfter));
  }

  return headers;
}

export function createRateLimitResponse(result: RateLimitResult): Response {
  return new Response(
    JSON.stringify({
      error: 'Rate limit exceeded',
      code: 'RATE_LIMIT_EXCEEDED',
      message: `You've used all ${result.limit} requests for today. Upgrade for unlimited access.`,
      reset: result.reset,
      upgradeUrl: '/pricing',
    }),
    {
      status: 429,
      headers: {
        'Content-Type': 'application/json',
        ...getRateLimitHeaders(result),
      },
    }
  );
}
```

### Using in API Routes

```typescript
// app/api/generate/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabaseClient } from '@/lib/supabase-server';
import { 
  checkRateLimit, 
  incrementUsage, 
  createRateLimitResponse,
  getRateLimitHeaders 
} from '@/lib/rate-limits';

export async function POST(request: NextRequest) {
  const userId = request.headers.get('x-user-id');
  
  if (!userId) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const supabase = await createServerSupabaseClient();
  
  // Check rate limit BEFORE expensive operation
  const rateLimit = await checkRateLimit(supabase, userId);
  
  if (!rateLimit.allowed) {
    return createRateLimitResponse(rateLimit);
  }

  // Process the request
  const body = await request.json();
  const result = await processRequest(body);

  // Increment usage AFTER successful operation
  await incrementUsage(supabase, userId);

  return NextResponse.json(
    { result },
    { headers: getRateLimitHeaders(rateLimit) }
  );
}
```

### Feature Gate Component

```typescript
// components/FeatureGate.tsx
'use client';

import { useUser } from '@/hooks/useUser';
import { TIER_LIMITS, type UserTier } from '@/lib/tiers';

interface FeatureGateProps {
  feature: keyof typeof TIER_LIMITS.free;
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export function FeatureGate({ feature, children, fallback }: FeatureGateProps) {
  const { tier, isLoading } = useUser();
  
  if (isLoading) return null;
  
  const limits = TIER_LIMITS[tier as UserTier];
  const hasAccess = limits[feature] === true || limits[feature] === Infinity;
  
  if (!hasAccess) {
    return fallback ?? (
      <div className="p-4 bg-gray-100 rounded text-center">
        <p className="text-gray-600">This feature requires Pro</p>
        <a href="/pricing" className="text-blue-600 hover:underline">
          Upgrade now
        </a>
      </div>
    );
  }
  
  return <>{children}</>;
}

// Usage
<FeatureGate feature="exportEnabled">
  <ExportButton />
</FeatureGate>

<FeatureGate 
  feature="apiAccess" 
  fallback={<ApiAccessUpsell />}
>
  <ApiKeyManager />
</FeatureGate>
```

### Usage Display Component

```typescript
// components/UsageDisplay.tsx
'use client';

import { useUser } from '@/hooks/useUser';
import { TIER_LIMITS } from '@/lib/tiers';

export function UsageDisplay() {
  const { tier, profile } = useUser();
  const limits = TIER_LIMITS[tier];
  
  if (limits.requestsPerDay === Infinity) {
    return <span className="text-green-600">Unlimited</span>;
  }
  
  const used = profile?.requests_today ?? 0;
  const remaining = Math.max(0, limits.requestsPerDay - used);
  const percentage = (used / limits.requestsPerDay) * 100;
  
  return (
    <div className="space-y-2">
      <div className="flex justify-between text-sm">
        <span>{remaining} remaining today</span>
        <span>{used} / {limits.requestsPerDay}</span>
      </div>
      <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
        <div 
          className={`h-full ${percentage > 80 ? 'bg-red-500' : 'bg-blue-500'}`}
          style={{ width: `${Math.min(100, percentage)}%` }}
        />
      </div>
      {remaining === 0 && (
        <a href="/pricing" className="text-blue-600 text-sm">
          Upgrade for unlimited
        </a>
      )}
    </div>
  );
}
```

## Python Implementation

```python
# lib/tiers.py
from dataclasses import dataclass
from typing import Literal
import math

TierName = Literal["free", "pro", "enterprise"]

@dataclass(frozen=True)
class TierLimits:
    requests_per_day: float  # Use math.inf for unlimited
    storage_gb: float
    history_days: int
    export_enabled: bool
    api_access: bool

TIER_LIMITS: dict[TierName, TierLimits] = {
    "free": TierLimits(
        requests_per_day=10,
        storage_gb=1,
        history_days=7,
        export_enabled=False,
        api_access=False,
    ),
    "pro": TierLimits(
        requests_per_day=math.inf,
        storage_gb=100,
        history_days=365,
        export_enabled=True,
        api_access=True,
    ),
}

def get_tier_limits(tier: TierName) -> TierLimits:
    return TIER_LIMITS.get(tier, TIER_LIMITS["free"])
```

```python
# lib/rate_limits.py
from datetime import datetime, timezone
from dataclasses import dataclass

@dataclass
class RateLimitResult:
    allowed: bool
    limit: int
    remaining: int
    reset: int
    tier: str

async def check_rate_limit(db, user_id: str) -> RateLimitResult:
    today = datetime.now(timezone.utc).date().isoformat()
    
    profile = await db.get_user_profile(user_id)
    tier = profile.subscription_tier if profile else "free"
    limits = get_tier_limits(tier)
    
    if limits.requests_per_day == math.inf:
        return RateLimitResult(
            allowed=True,
            limit=-1,
            remaining=-1,
            reset=get_reset_timestamp(),
            tier=tier,
        )
    
    used = profile.requests_today if profile.requests_date == today else 0
    remaining = max(0, int(limits.requests_per_day) - used)
    
    return RateLimitResult(
        allowed=remaining > 0,
        limit=int(limits.requests_per_day),
        remaining=remaining,
        reset=get_reset_timestamp(),
        tier=tier,
    )
```

## Response Headers

```
X-RateLimit-Limit: 10         # Max requests allowed
X-RateLimit-Remaining: 3      # Requests remaining
X-RateLimit-Reset: 1705363200 # Unix timestamp when limit resets
Retry-After: 3600             # Seconds until reset (only on 429)
```

## Best Practices

1. **Check before work** - Verify limits before expensive operations
2. **Increment after success** - Only count successful requests
3. **Atomic increments** - Use database functions to prevent races
4. **Include upgrade CTA** - 429 responses should help users upgrade
5. **Show remaining** - Display usage in UI

## Common Mistakes

- Incrementing before the operation completes
- Race conditions with non-atomic increments
- Not resetting counters on new day
- Missing rate limit headers on responses
- Blocking unlimited tier users

## Related Skills

- [Rate Limiting](../rate-limiting/)
- [Stripe Integration](../stripe-integration/)
- [Supabase Auth](../supabase-auth/)
