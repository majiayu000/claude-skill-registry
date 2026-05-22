---
name: sdk-adapter
description: Create SDK adapters for new app integrations. Use when onboarding a new Skill Recordings product, implementing the SupportIntegration interface, or scaffolding a new app.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# SDK + Adapter Pattern

Adding a new app should be **"a `skill init` away"**. Each app implements the `SupportIntegration` interface.

## Architecture Overview

```
Support Platform                          App Integration
┌─────────────────┐                      ┌─────────────────┐
│ Agent Tool      │  HTTPS + HMAC-SHA256 │ createSupport-  │
│ (lookupUser,    │─────────────────────►│ Handler         │
│  processRefund) │  x-signature header  │ (verifies sig)  │
└────────┬────────┘                      └────────┬────────┘
         │                                        │
         ▼                                        ▼
┌─────────────────┐                      ┌─────────────────┐
│ IntegrationClient│                     │ SupportIntegration
│ (signs requests) │                     │ (your impl)     │
└─────────────────┘                      └─────────────────┘
```

## SupportIntegration Interface

Import from `@skillrecordings/sdk/integration`:

```typescript
import type { SupportIntegration } from '@skillrecordings/sdk/integration'

export interface SupportIntegration {
  // Required: User lookup
  lookupUser(email: string): Promise<User | null>
  getPurchases(userId: string): Promise<Purchase[]>

  // Optional: Subscriptions
  getSubscriptions?(userId: string): Promise<Subscription[]>

  // Required: Access management
  revokeAccess(params: {
    purchaseId: string
    reason: string
    refundId: string
  }): Promise<ActionResult>

  transferPurchase(params: {
    purchaseId: string
    fromUserId: string
    toEmail: string
  }): Promise<ActionResult>

  // Required: Auth
  generateMagicLink(params: {
    email: string
    expiresIn: number
  }): Promise<{ url: string }>

  // Optional: Profile updates
  updateEmail?(params: { userId: string; newEmail: string }): Promise<ActionResult>
  updateName?(params: { userId: string; newName: string }): Promise<ActionResult>

  // Optional: Team features
  getClaimedSeats?(bulkCouponId: string): Promise<ClaimedSeat[]>
}
```

## Type Definitions

Import from `@skillrecordings/sdk/types`:

```typescript
export interface User {
  id: string
  email: string
  name?: string
  createdAt?: Date
}

export interface Purchase {
  id: string
  userId: string
  productId: string
  productName?: string
  purchasedAt: Date
  amount: number
  currency?: string
  stripeChargeId?: string
  status: 'active' | 'refunded' | 'transferred'
}

export interface Subscription {
  id: string
  userId: string
  productId: string
  status: 'active' | 'canceled' | 'past_due' | 'trialing'
  currentPeriodEnd: Date
  cancelAtPeriodEnd: boolean
}

export interface ActionResult {
  success: boolean
  message?: string
}
```

## HMAC Signature Verification

Requests from the support platform include an `x-signature` header:

```
x-signature: timestamp=1737163200,v1=<hex_signature>
```

**Payload to sign:** `${timestamp}.${JSON.stringify(body)}`

The handler verifies:
1. Signature matches HMAC-SHA256(payload, webhook_secret)
2. Timestamp is within 5 minutes (replay protection)

## Next.js Route Handler

```typescript
// app/api/support/route.ts
import { createSupportHandler } from '@skillrecordings/sdk/handler'
import type { SupportIntegration } from '@skillrecordings/sdk/integration'

const integration: SupportIntegration = {
  async lookupUser(email) {
    return db.user.findUnique({ where: { email } })
  },
  async getPurchases(userId) {
    return db.purchase.findMany({ where: { userId } })
  },
  async revokeAccess({ purchaseId, reason, refundId }) {
    await db.purchase.update({
      where: { id: purchaseId },
      data: { status: 'refunded', refundReason: reason, stripeRefundId: refundId }
    })
    return { success: true }
  },
  async transferPurchase({ purchaseId, fromUserId, toEmail }) {
    const toUser = await db.user.findUnique({ where: { email: toEmail } })
    await db.purchase.update({
      where: { id: purchaseId },
      data: { userId: toUser.id, status: 'transferred' }
    })
    return { success: true }
  },
  async generateMagicLink({ email, expiresIn }) {
    const token = await createMagicToken(email, expiresIn)
    return { url: `${APP_URL}/auth/magic?token=${token}` }
  },
}

// Create handler - handles signature verification automatically
const handler = createSupportHandler(integration, {
  webhookSecret: process.env.SUPPORT_WEBHOOK_SECRET!,
})

export async function POST(request: Request) {
  return handler(request)
}
```

## App Registration

Each app needs an entry in the `apps` table:

```typescript
{
  slug: 'total-typescript',
  name: 'Total TypeScript',
  front_inbox_id: 'inb_xxx',
  stripe_account_id: 'acct_xxx',
  integration_base_url: 'https://totaltypescript.com/api/support',
  webhook_secret: 'whsec_xxx',  // Shared secret for HMAC signing
  capabilities: ['refund', 'transfer', 'magic_link'],
  auto_approve_refund_days: 30,
  auto_approve_transfer_days: 14,
  escalation_slack_channel: 'C0XXXXXXX',
}
```

## File Locations

| File | Purpose |
|------|---------|
| `packages/sdk/src/types.ts` | User, Purchase, Subscription, ActionResult types |
| `packages/sdk/src/integration.ts` | SupportIntegration interface |
| `packages/sdk/src/handler.ts` | createSupportHandler factory |
| `packages/sdk/src/client.ts` | IntegrationClient (used by core) |
| `packages/core/src/services/app-registry.ts` | App config lookup with 5-min TTL cache |

## Package Exports

```typescript
// Types
import type { User, Purchase, ActionResult } from '@skillrecordings/sdk/types'

// Interface
import type { SupportIntegration } from '@skillrecordings/sdk/integration'

// Handler (for app implementations)
import { createSupportHandler } from '@skillrecordings/sdk/handler'

// Client (used internally by core)
import { IntegrationClient } from '@skillrecordings/sdk/client'
```

## Reference Docs

For full details, see:
- `docs/support-app-prd/67-sdk.md`
- `docs/ARCHITECTURE.md` (SDK Integration Flow section)
