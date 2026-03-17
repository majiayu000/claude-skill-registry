---
name: agent-tool
description: Define tools for the support agent. Use when adding new capabilities like refund processing, license transfer, knowledge lookup, or any agent action.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Agent Tool Definition

Tools are the agent's hands. Every action the agent can take is a tool with defined parameters, approval requirements, and execution logic.

## Agent Core (Mastra)

```typescript
import { Agent } from '@mastra/core'
import { supportTools } from './tools'

export const supportAgent = new Agent({
  name: 'support-agent',
  instructions: `
    You are a support agent for Skill Recordings products.
    Your goal is to resolve customer issues quickly and empathetically.

    ## Authority Levels

    AUTO-APPROVE (do immediately):
    - Magic link requests
    - Password reset requests
    - Refunds within 30 days of purchase
    - Transfers within 14 days of purchase
    - Email/name updates

    REQUIRE-APPROVAL (draft action, wait for human):
    - Refunds 30-45 days after purchase
    - Transfers after 14 days
    - Bulk seat management
    - Account deletions

    ALWAYS-ESCALATE (flag for human, do not act):
    - Angry/frustrated customers (detect sentiment)
    - Legal language (lawsuit, lawyer, etc.)
    - Repeated failed interactions
    - Anything you're uncertain about

    ## Response Style
    - Be personal, use first names
    - Be concise, not verbose
    - Don't apologize excessively
    - Focus on resolution, not explanation
  `,
  model: { provider: 'anthropic', name: 'claude-sonnet-4-[PHONE]' },
  tools: supportTools,
})
```

## Tool Definition Pattern

```typescript
import { createTool } from './create-tool'
import { z } from 'zod'
import { getApp } from '@skillrecordings/core/services/app-registry'
import { IntegrationClient } from '@skillrecordings/sdk/client'

export const processRefund = createTool({
  name: 'process_refund',
  description: 'Process a refund for a purchase. Use only within policy.',

  // Zod schema for parameters
  parameters: z.object({
    purchaseId: z.string(),
    appId: z.string(),
    reason: z.string(),
  }),

  // Dynamic approval requirement based on context
  requiresApproval: (params, context) => {
    const purchase = context.purchases.find(p => p.id === params.purchaseId)
    const daysSincePurchase = daysBetween(purchase.purchasedAt, new Date())
    return daysSincePurchase > 30  // Auto-approve within 30 days
  },

  // Execution logic - THROW errors, don't return {success: false}
  execute: async ({ purchaseId, appId, reason }, context) => {
    // Get app config from registry (5-min TTL cache)
    const app = await getApp(appId)
    if (!app) {
      throw new Error(`App not found: ${appId}`)  // ← THROW, don't return error
    }

    // Process via Stripe Connect
    const stripeRefund = await stripe.refunds.create({
      charge: purchase.stripeChargeId,
    }, {
      stripeAccount: app.stripe_account_id,
    })

    // Revoke access via IntegrationClient (signed request)
    const client = new IntegrationClient({
      baseUrl: app.integration_base_url,
      webhookSecret: app.webhook_secret,
    })

    const revokeResult = await client.revokeAccess({
      purchaseId,
      reason,
      refundId: stripeRefund.id,
    })

    if (!revokeResult.success) {
      throw new Error(revokeResult.message || 'Failed to revoke access')
    }

    // Return data only - wrapper adds {success: true, data: ...}
    return { refundId: stripeRefund.id, amountRefunded: stripeRefund.amount }
  },
})
```

## Error Handling Pattern

**CRITICAL**: The `createTool` wrapper handles success/error wrapping automatically.

```typescript
// ❌ WRONG - Don't return success/error objects
execute: async (params) => {
  if (!app) {
    return { success: false, error: 'App not found' }  // BAD
  }
  return { success: true, data: result }  // BAD
}

// ✅ CORRECT - Throw errors, return plain data
execute: async (params) => {
  if (!app) {
    throw new Error('App not found')  // GOOD - wrapper catches this
  }
  return { refundId, amount }  // GOOD - wrapper wraps as {success: true, data: ...}
}
```

The wrapper produces:
- Success: `{ success: true, data: <your return value> }`
- Error: `{ success: false, error: { code: 'EXECUTION_ERROR', message: '...' } }`
```

## Standard Tools

| Tool | Description | Approval |
|------|-------------|----------|
| `lookup_user` | Get user details and purchase history | Never |
| `process_refund` | Issue a refund via Stripe Connect | >30 days |
| `generate_magic_link` | Create login link for user | Never |
| `transfer_purchase` | Move purchase to another user | >14 days |
| `draft_response` | Create draft reply in Front | Never |
| `escalate_to_human` | Flag for human review | Never |

## Tool Examples

### Lookup User (No Approval)
```typescript
import { getApp } from '@skillrecordings/core/services/app-registry'
import { IntegrationClient } from '@skillrecordings/sdk/client'

export const lookupUser = createTool({
  name: 'lookup_user',
  description: 'Look up a user by email to get their account details and purchase history',
  parameters: z.object({
    email: z.string().email(),
    appId: z.string(),
  }),
  execute: async ({ email, appId }) => {
    const app = await getApp(appId)
    if (!app) {
      return { found: false, error: `App not found: ${appId}` }
    }

    const client = new IntegrationClient({
      baseUrl: app.integration_base_url,
      webhookSecret: app.webhook_secret,
    })

    const user = await client.lookupUser(email)
    if (!user) {
      return { found: false, user: null, purchases: [] }
    }

    const purchases = await client.getPurchases(user.id)
    return { found: true, user, purchases }
  },
})
```

### Escalate to Human
```typescript
export const escalateToHuman = createTool({
  name: 'escalate_to_human',
  description: 'Escalate this conversation to a human support agent',
  parameters: z.object({
    conversationId: z.string(),
    reason: z.string(),
    urgency: z.enum(['low', 'medium', 'high']),
  }),
  execute: async ({ conversationId, reason, urgency }) => {
    await front.conversations.addTag(conversationId, 'needs-human')

    await slack.postMessage({
      channel: SUPPORT_CHANNEL,
      text: `Escalation needed`,
      blocks: [
        {
          type: 'section',
          text: { type: 'mrkdwn', text: `*Reason:* ${reason}\n*Urgency:* ${urgency}` },
        },
        {
          type: 'actions',
          elements: [
            { type: 'button', text: { type: 'plain_text', text: 'Open in Front' }, url: frontConversationUrl },
          ],
        },
      ],
    })

    return { escalated: true }
  },
})
```

## File Locations

| File | Purpose |
|------|---------|
| `packages/core/src/agent/config.ts` | Agent definition with tool bindings |
| `packages/core/src/tools/` | Individual tool implementations |
| `packages/core/src/tools/create-tool.ts` | Tool factory with success/error wrapping |
| `packages/core/src/services/app-registry.ts` | App config lookup (5-min TTL cache) |
| `packages/sdk/src/client.ts` | IntegrationClient for SDK calls |

## Reference Docs

For full details, see:
- `docs/support-app-prd/64-agent-tools.md`
