---
name: inngest-workflow
description: Create Inngest workflows for durable execution. Use when building agent workflows, approval flows, scheduled tasks, or any multi-step async process.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Inngest Workflow Patterns

Inngest is the **only workflow engine** for this platform. All durable execution goes through Inngest.

## Core Pattern: Inbound Message Handler

```typescript
import { inngest } from './client'

export const handleInboundMessage = inngest.createFunction(
  {
    id: 'handle-inbound-message',
    // Throttle prevents duplicate processing
    throttle: {
      key: 'event.data.conversationId',
      limit: 1,
      period: '10s',
    },
  },
  { event: 'front/inbound_received' },
  async ({ event, step }) => {
    const { conversationId, appId, senderEmail } = event.data

    // Step 1: Gather context (retriable)
    const context = await step.run('gather-context', async () => {
      const [user, messages, app] = await Promise.all([
        appRegistry.get(appId).integration.lookupUser(senderEmail),
        front.conversations.listMessages(conversationId),
        appRegistry.get(appId),
      ])
      return { user, messages, app }
    })

    // Step 2: Agent reasoning (retriable)
    const agentResult = await step.run('agent-reasoning', async () => {
      return supportAgent.run({
        messages: [{ role: 'user', content: buildPrompt(context) }],
        context,
      })
    })

    // Step 3: Handle approval or execute
    if (agentResult.action?.requiresApproval) {
      await step.run('request-approval', async () => {
        await requestApproval({
          action: agentResult.action,
          conversationId,
          appId,
          agentReasoning: agentResult.reasoning,
        })
      })
    } else if (agentResult.action) {
      await step.run('execute-action', async () => {
        await executeAction(agentResult.action)
      })
    }

    // Step 4: Create draft response
    if (agentResult.draftResponse) {
      await step.run('create-draft', async () => {
        await front.conversations.createDraft(conversationId, {
          body: agentResult.draftResponse,
        })
      })
    }

    return { processed: true, action: agentResult.action }
  }
)
```

## Key Inngest Patterns

### Throttling (Dedupe)
```typescript
throttle: {
  key: 'event.data.conversationId',
  limit: 1,
  period: '10s',
}
```

### Wait for Event (Approval Flow)

**⚠️ CRITICAL: Match Field Alignment**

The `match` field MUST align with the field name in BOTH the triggering event AND the awaited event:

```typescript
// Triggering workflow sends:
await inngest.send({
  name: 'support/approval.requested',
  data: { actionId: 'abc123', ... }  // ← Field is "actionId"
})

// waitForEvent MUST use the same field:
const approval = await step.waitForEvent('approval-received', {
  event: 'support/approval.decided',
  match: 'data.actionId',  // ✅ Matches triggering event's field name
  timeout: '24h',
})

// Decision event MUST also use the same field:
await inngest.send({
  name: 'support/approval.decided',
  data: { actionId: 'abc123', approved: true }  // ✅ Same field name
})
```

**Common mistake:**
```typescript
// ❌ WRONG - field name mismatch
// Trigger has: data.actionId
// waitForEvent uses: match: 'data.approvalId'  ← Never matches!
// Decision has: data.approvalId
```

```typescript
const approval = await step.waitForEvent('approval-received', {
  event: 'action/approved',
  match: 'data.actionId',
  timeout: '24h',
})
if (!approval) {
  await step.run('handle-timeout', () => expireAction(actionId))
}
```

### Sleep (Scheduled Tasks)
```typescript
await step.sleep('wait-for-send', '5m')
await step.run('auto-send', () => sendDraft(draftId))
```

### Invoke (Sub-workflows)
```typescript
await step.invoke('process-refund', {
  function: processRefundWorkflow,
  data: { purchaseId, reason },
})
```

## Event Naming Convention

```
{source}/{entity}.{action}

Examples:
- front/inbound_received
- front/outbound_sent
- action/approved
- action/rejected
- stripe/refund.completed
```

## Database Access in Workflows

**CRITICAL**: Use lazy initialization, not the singleton.

```typescript
// ❌ BAD - singleton creates pool at import time, fails in serverless
import { database, ActionsTable } from '@skillrecordings/database'

// ✅ GOOD - lazy init inside step function
import { getDb, ActionsTable } from '@skillrecordings/database'

await step.run('create-action', async () => {
  const db = getDb()  // Pool created here, at runtime
  await db.insert(ActionsTable).values({ ... })
})
```

Why: The `database` singleton calls `mysql.createPool()` at import time. In serverless/Turbopack builds, this fails because DATABASE_URL isn't available during static analysis.

## Vercel Cron for Inngest Registration

Keep Inngest functions registered on Vercel serverless:

```typescript
// app/api/cron/route.ts
import { headers } from 'next/headers'

export const dynamic = 'force-dynamic'

export async function GET() {
  await headers()
  const baseUrl = process.env.VERCEL_URL
    ? `https://${process.env.VERCEL_URL}`
    : 'http://localhost:3000'

  await fetch(`${baseUrl}/api/inngest`, { method: 'PUT' })
  return new Response(null, { status: 200 })
}
```

```json
// vercel.json
{
  "crons": [{ "path": "/api/cron", "schedule": "*/5 * * * *" }]
}
```

## External API Fallback Pattern

When fetching from external APIs (Front, Stripe), always provide fallback:

```typescript
const context = await step.run('get-context', async () => {
  const fallback = {
    body: event.data.messageBody || '',
    senderEmail: event.data.customerEmail || '',
  }

  try {
    const data = await externalApi.fetch(id)
    return data
  } catch (error) {
    console.warn('[workflow] API error, using fallback:', error)
    return fallback
  }
})
```

## File Locations

- Inngest client: `packages/core/src/inngest/client.ts`
- Workflow definitions: `packages/core/src/inngest/workflows/`
- Event types: `packages/core/src/inngest/events.ts`
- Cron endpoint: `apps/front/app/api/cron/route.ts`

## Reference Docs

For full details, see:
- `docs/support-app-prd/65-workflows.md`
