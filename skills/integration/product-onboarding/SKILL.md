---
name: product-onboarding
description: Add a new Skill Recordings product to the support platform. Use when user says "add product", "new app", "onboard [product name]", or similar.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch
---

# Product Onboarding Skill

Add a new Skill Recordings product to the support platform.

## Prerequisites

- Product has a Front inbox
- Product has a Stripe account (for refund processing)
- Product codebase is accessible

## Step 1: Get Front Inbox ID

Front uses base-36 encoded IDs with prefixes. Convert the numeric URL ID to API ID.

From a Front URL like:
```
https://app.frontapp.com/inboxes/teams/folders/7256583/unassigned/...
```

The inbox ID (7256583) converts to:
```javascript
'inb_' + (7256583).toString(36)  // => "inb_4bj7r"
```

See `@.claude/skills/front-id-converter/SKILL.md` for full reference.

## Step 2: Generate App Config

Run the wizard or generate manually:

```bash
bun packages/cli/src/index.ts wizard
```

Or generate directly:
```javascript
const crypto = require('crypto')
const id = 'app_' + crypto.randomUUID().replace(/-/g, '').slice(0, 16)
const webhookSecret = crypto.randomBytes(32).toString('hex')
```

## Step 3: Insert into Database

```sql
INSERT INTO SUPPORT_apps (
  id, slug, name, front_inbox_id,
  integration_base_url, webhook_secret,
  capabilities, auto_approve_refund_days, auto_approve_transfer_days
)
VALUES (
  'app_xxxxxxxxxxxxxxxx',    -- Generated app ID
  'product-slug',            -- URL-friendly slug
  'Product Name',            -- Display name
  'inb_xxxxx',               -- Front inbox ID (base-36)
  'https://product.com/api/support',  -- SDK endpoint base URL
  'xxxxxxxx...',             -- 64-char hex webhook secret
  '["lookupUser","getPurchases","revokeAccess","transferPurchase","generateMagicLink"]',
  30,                        -- Auto-approve refunds within N days
  14                         -- Auto-approve transfers within N days
);
```

Or use Drizzle Studio: `bun run db:studio`

## Step 4: Connect Stripe via OAuth

After the app record exists, connect its Stripe account:

```
https://skill-support-agent-web.vercel.app/api/stripe/connect/authorize?appSlug=<slug>
```

This redirects to Stripe, authorizes the account, and stores `stripe_account_id` automatically.

## Step 5: Implement SDK in Product

### 5.1 Install SDK

```bash
# In product codebase
pnpm add @skillrecordings/sdk
# or
bun add @skillrecordings/sdk
```

### 5.2 Add Environment Variable

```bash
# .env.local
SUPPORT_WEBHOOK_SECRET=<webhook-secret-from-step-2>
```

### 5.3 Create Integration File

Create `app/api/support/integration.ts`:

```typescript
import type {
  ActionResult,
  Purchase,
  SupportIntegration,
  User,
} from '@skillrecordings/sdk/integration'

export const integration: SupportIntegration = {
  async lookupUser(email: string): Promise<User | null> {
    const user = await db.user.findUnique({ where: { email } })
    if (!user) return null
    return {
      id: user.id,
      email: user.email,
      name: user.name ?? undefined,
      createdAt: user.createdAt,
    }
  },

  async getPurchases(userId: string): Promise<Purchase[]> {
    const purchases = await db.purchase.findMany({
      where: { userId },
      include: { product: true },
    })
    return purchases.map((p) => ({
      id: p.id,
      productId: p.productId,
      productName: p.product.name,
      purchasedAt: p.createdAt,
      amount: p.totalAmount,  // in cents
      currency: 'USD',
      stripeChargeId: p.chargeIdentifier ?? undefined,
      status: p.status as 'active' | 'refunded' | 'transferred',
    }))
  },

  async revokeAccess({ purchaseId, reason, refundId }): Promise<ActionResult> {
    await db.purchase.update({
      where: { id: purchaseId },
      data: { status: 'refunded', refundReason: reason }
    })
    return { success: true }
  },

  async transferPurchase({ purchaseId, fromUserId, toEmail }): Promise<ActionResult> {
    let toUser = await db.user.findUnique({ where: { email: toEmail } })
    if (!toUser) {
      toUser = await db.user.create({ data: { email: toEmail } })
    }
    await db.purchase.update({
      where: { id: purchaseId },
      data: { userId: toUser.id }
    })
    return { success: true }
  },

  async generateMagicLink({ email, expiresIn }): Promise<{ url: string }> {
    const token = await createMagicLinkToken(email, expiresIn)
    return { url: `${process.env.NEXT_PUBLIC_URL}/api/auth/magic?token=${token}` }
  },

  // Optional methods:
  // async updateEmail({ userId, newEmail }): Promise<ActionResult>
  // async updateName({ userId, newName }): Promise<ActionResult>
  // async getSubscriptions(userId: string): Promise<Subscription[]>
  // async getClaimedSeats(bulkCouponId: string): Promise<ClaimedSeat[]>
}
```

### 5.4 Create Route Handler

Create `app/api/support/[...action]/route.ts`:

```typescript
import { createSupportHandler } from '@skillrecordings/sdk/handler'
import { integration } from '../integration'

const handler = createSupportHandler({
  integration,
  webhookSecret: process.env.SUPPORT_WEBHOOK_SECRET!,
})

export { handler as POST }
```

### 5.5 Add to Env Schema (if using t3-env or similar)

```typescript
// env.mjs
server: {
  // ...existing vars
  SUPPORT_WEBHOOK_SECRET: z.string().optional(),
},
runtimeEnv: {
  // ...existing vars
  SUPPORT_WEBHOOK_SECRET: process.env.SUPPORT_WEBHOOK_SECRET,
},
```

### 5.6 Add to turbo.json (Turborepo monorepos)

For Turborepo monorepos, add the env var to the build task's `env` array:

```json
{
  "tasks": {
    "build": {
      "env": [
        "...existing vars...",
        "SUPPORT_WEBHOOK_SECRET"
      ]
    }
  }
}
```

Without this, Turbo won't pass the env var to the build and you'll get warnings.

## Step 6: Verify Integration

Test the endpoint is reachable:
```bash
curl -X POST https://product.com/api/support/health
```

Or use the CLI:
```bash
bun packages/cli/src/index.ts health --app product-slug
```

## Course-Builder Apps

For apps built on course-builder (like AI Hero), **always use `courseBuilderAdapter`** instead of direct database queries. The adapter handles organization setup, proper relations, and maintains consistency.

### Import Pattern

```typescript
import { courseBuilderAdapter } from '@/db'
import { env } from '@/env.mjs'
```

**Do NOT import `db` or schema tables directly** - use adapter methods.

### Adapter Methods Reference

| Operation | Adapter Method |
|-----------|----------------|
| Find user by email | `courseBuilderAdapter.getUserByEmail(email)` |
| Find user by ID | `courseBuilderAdapter.getUserById(userId)` |
| Find or create user | `courseBuilderAdapter.findOrCreateUser(email)` |
| Get user's purchases | `courseBuilderAdapter.getPurchasesForUser(userId)` |
| Get single purchase | `courseBuilderAdapter.getPurchase(purchaseId)` |
| Update purchase status | `courseBuilderAdapter.updatePurchaseStatusForCharge(chargeId, status)` |
| Transfer purchase | `courseBuilderAdapter.transferPurchaseToUser({ purchaseId, sourceUserId, targetUserId })` |
| Update user | `courseBuilderAdapter.updateUser({ id, ...fields })` |
| Create verification token | `courseBuilderAdapter.createVerificationToken({ identifier, token, expires })` |

### Full Integration Example (Course-Builder)

```typescript
import { courseBuilderAdapter } from '@/db'
import { env } from '@/env.mjs'
import type {
  ActionResult,
  Purchase,
  SupportIntegration,
  User,
} from '@skillrecordings/sdk/integration'
import { v4 as uuidv4 } from 'uuid'

export const integration: SupportIntegration = {
  async lookupUser(email: string): Promise<User | null> {
    const user = await courseBuilderAdapter.getUserByEmail?.(email)
    if (!user) return null
    return {
      id: user.id,
      email: user.email,
      name: user.name ?? undefined,
      createdAt: new Date(),
    }
  },

  async getPurchases(userId: string): Promise<Purchase[]> {
    const purchases = await courseBuilderAdapter.getPurchasesForUser(userId)
    return purchases.map((p) => ({
      id: p.id,
      productId: p.productId,
      productName: p.product?.name ?? 'Unknown Product',
      purchasedAt: p.createdAt,
      amount: Math.round(Number(p.totalAmount) * 100),
      currency: 'USD',
      stripeChargeId: p.merchantChargeId ?? undefined,
      status: mapPurchaseStatus(p.status ?? 'Valid'),
    }))
  },

  async revokeAccess({ purchaseId }): Promise<ActionResult> {
    const purchase = await courseBuilderAdapter.getPurchase(purchaseId)
    if (!purchase?.merchantChargeId) {
      return { success: false, error: 'No charge ID' }
    }
    await courseBuilderAdapter.updatePurchaseStatusForCharge(
      purchase.merchantChargeId,
      'Refunded',
    )
    return { success: true }
  },

  async transferPurchase({ purchaseId, fromUserId, toEmail }): Promise<ActionResult> {
    const { user: toUser } = await courseBuilderAdapter.findOrCreateUser(toEmail)
    if (!toUser) return { success: false, error: 'User creation failed' }

    await courseBuilderAdapter.transferPurchaseToUser({
      purchaseId,
      sourceUserId: fromUserId,
      targetUserId: toUser.id,
    })
    return { success: true }
  },

  async generateMagicLink({ email, expiresIn }): Promise<{ url: string }> {
    const token = uuidv4()
    await courseBuilderAdapter.createVerificationToken?.({
      identifier: email,
      token,
      expires: new Date(Date.now() + expiresIn * 1000),
    })
    const baseUrl = env.NEXT_PUBLIC_URL
    return {
      url: `${baseUrl}/api/auth/callback/email?callbackUrl=${encodeURIComponent(baseUrl)}&token=${token}&email=${encodeURIComponent(email)}`,
    }
  },

  async updateEmail({ userId, newEmail }): Promise<ActionResult> {
    const existing = await courseBuilderAdapter.getUserByEmail?.(newEmail)
    if (existing && existing.id !== userId) {
      return { success: false, error: 'Email in use' }
    }
    await courseBuilderAdapter.updateUser?.({ id: userId, email: newEmail })
    return { success: true }
  },

  async updateName({ userId, newName }): Promise<ActionResult> {
    await courseBuilderAdapter.updateUser?.({ id: userId, name: newName })
    return { success: true }
  },
}

function mapPurchaseStatus(status: string): 'active' | 'refunded' | 'transferred' {
  switch (status) {
    case 'Refunded': return 'refunded'
    case 'Transferred': return 'transferred'
    default: return 'active'
  }
}
```

### Route Handler (Request-Time Check)

**IMPORTANT**: Check the env var at request time, not module load time. Top-level throws break the build.

```typescript
import { NextRequest, NextResponse } from 'next/server'
import { env } from '@/env.mjs'
import { createSupportHandler } from '@skillrecordings/sdk/handler'
import { integration } from '../integration'

export async function POST(request: NextRequest) {
  // Check at request time, not build time
  if (!env.SUPPORT_WEBHOOK_SECRET) {
    return NextResponse.json(
      { error: 'Support integration not configured' },
      { status: 503 },
    )
  }

  const handler = createSupportHandler({
    integration,
    webhookSecret: env.SUPPORT_WEBHOOK_SECRET,
  })

  return handler(request)
}
```

## Checklist

- [ ] Front inbox ID converted (base-36)
- [ ] App record inserted in SUPPORT_apps
- [ ] Stripe Connect OAuth completed
- [ ] SDK installed in product
- [ ] SUPPORT_WEBHOOK_SECRET in product's .env
- [ ] Integration file implements required methods
- [ ] Route handler created at `/api/support/[...action]`
- [ ] Env schema updated (if applicable)
- [ ] Endpoint tested

## Production URLs

| App | URL |
|-----|-----|
| Web (dashboard, Stripe) | https://skill-support-agent-web.vercel.app |
| Front Plugin | https://skill-support-agent-front.vercel.app |
| Slack Bot | https://skill-support-agent-slack.vercel.app |
