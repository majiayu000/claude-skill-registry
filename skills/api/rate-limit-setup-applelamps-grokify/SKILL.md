---
name: rate-limit-setup
description: Implement rate limiting for API endpoints. Use when user mentions "rate limit", "quota", "usage tracking", "throttle", or "limit requests".
---

# Rate Limiting Implementation

This project uses database-backed rate limiting via the `usage_tracking` table.

## Current Implementation

Located in `app/api/generate-image/route.ts`:
- **Limit**: 2 premium images per user per 24 hours
- **Identification**: SHA-256 hash of IP + User-Agent (anonymous)
- **Reset**: Automatic after 24 hours

## Instructions

1. **Create user identifier** (anonymous hash):
```typescript
const getUserIdentifier = async (req: NextRequest): Promise<string> => {
  const ip = req.headers.get('x-forwarded-for')?.split(',')[0]
    || req.headers.get('x-real-ip')
    || 'unknown';
  const userAgent = req.headers.get('user-agent') || 'unknown';

  const encoder = new TextEncoder();
  const data = encoder.encode(ip + userAgent);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map((b) => b.toString(16).padStart(2, '0')).join('');
};
```

2. **Check and update usage**:
```typescript
import { db, usageTracking } from '@/db';
import { eq } from 'drizzle-orm';

const checkUsage = async (identifier: string, limit: number) => {
  const existing = await db
    .select()
    .from(usageTracking)
    .where(eq(usageTracking.userIdentifier, identifier))
    .limit(1);

  let usage = existing[0] || null;
  const now = new Date();
  const resetNeeded = !usage ||
    now.getTime() - new Date(usage.lastResetAt!).getTime() > 24 * 60 * 60 * 1000;

  if (!usage) {
    const [inserted] = await db
      .insert(usageTracking)
      .values({ userIdentifier: identifier, premiumImagesCount: 0, lastResetAt: now })
      .returning();
    usage = inserted;
  } else if (resetNeeded) {
    const [updated] = await db
      .update(usageTracking)
      .set({ premiumImagesCount: 0, lastResetAt: now, updatedAt: now })
      .where(eq(usageTracking.userIdentifier, identifier))
      .returning();
    usage = updated;
  }

  const withinLimit = (usage?.premiumImagesCount || 0) < limit;
  return { withinLimit, usage };
};
```

3. **Increment counter after successful action**:
```typescript
await db
  .update(usageTracking)
  .set({
    premiumImagesCount: (usage?.premiumImagesCount || 0) + 1,
    updatedAt: new Date(),
  })
  .where(eq(usageTracking.userIdentifier, userIdentifier));
```

4. **Return appropriate response when limited**:
```typescript
if (!withinLimit) {
  return NextResponse.json(
    { error: 'Rate limit exceeded. Try again in 24 hours.' },
    { status: 429, headers: corsHeaders }
  );
}
```

## For New Rate-Limited Features

If tracking a different resource, add a new column to `usage_tracking` or create a new table:
```typescript
// In db/schema.ts
featureCount: integer('feature_count').default(0),
```

## Examples

- "Limit roasts to 5 per day" → Add `roastCount` column, apply pattern above
- "Add API request throttling" → Create new tracking table for general requests

## Guardrails

- Never expose user identifiers in responses
- Log usage counts, not full hashes
- Use 429 status code for rate limit responses
- Include reset time info in rate limit responses when possible
- Test reset logic carefully (24-hour boundary)
