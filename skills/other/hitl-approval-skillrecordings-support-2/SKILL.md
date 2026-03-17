---
name: hitl-approval
description: Implement human-in-the-loop approval flows. Use when adding Slack approvals, dashboard review queues, action gating, or trust-based auto-approval.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Human-in-the-Loop Approval

Core differentiator: **agent proposes, human approves**. Every sensitive action requires human approval until trust is established.

## Architecture Overview

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Agent Tool     │ ──▶ │ requestApproval  │ ──▶ │  Slack Message  │
│  proposes       │     │ workflow         │     │  with buttons   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                                          │
                                                          ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Action         │ ◀── │ executeApproved  │ ◀── │  Interactions   │
│  executed       │     │ Action workflow  │     │  handler        │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

## Approval Surfaces

| Surface | Use Case | Capabilities |
|---------|----------|--------------|
| **Slack** | Real-time push notifications | Approve/reject buttons, rejection reason modal |
| **Dashboard** | Bulk review, audit trail | Queue view, search, bulk actions |
| **Front Plugin** | In-context approval | View customer data, quick actions |

## Inngest Events

| Event | Trigger | Data |
|-------|---------|------|
| `support/approval.requested` | Agent proposes action | actionId, conversationId, appId, action, agentReasoning |
| `support/approval.decided` | Human clicks button | **actionId**, decision, decidedBy, decidedAt |
| `support/action.approved` | Human approves | actionId, approvedBy, approvedAt |
| `support/action.rejected` | Human rejects | actionId, rejectedBy, rejectedAt, reason? |

**IMPORTANT**: The `waitForEvent` match uses `data.actionId` - ensure all events use `actionId` consistently (not `approvalId`).

## Slack Block Kit Builder

Build approval messages with `buildApprovalBlocks`:

```typescript
import { buildApprovalBlocks } from '@skillrecordings/core/slack/approval-blocks'

const blocks = buildApprovalBlocks({
  actionId: 'action-123',
  conversationId: 'conv-456',
  appId: 'total-typescript',
  actionType: 'issue_refund',
  parameters: { orderId: 'order-789', amount: 99.00 },
  agentReasoning: 'Customer within 30-day refund window',
})
// Returns: header, reasoning section, parameters, approve/reject buttons
```

Button metadata structure (embedded in value):
```typescript
{ actionId, conversationId, appId }
```

## Slack Client (Lazy Init)

```typescript
import { postApprovalMessage, updateApprovalMessage } from '@skillrecordings/core/slack/client'

// Post approval message to channel
const { ts, channel } = await postApprovalMessage(
  process.env.SLACK_APPROVAL_CHANNEL,
  blocks,
  'Approval needed for Issue Refund'
)

// Update message after decision
await updateApprovalMessage(channel, ts, updatedBlocks, 'Approved')
```

## Slack Interactions Handler (Next.js App Router)

```typescript
// apps/slack/app/api/slack/interactions/route.ts
import { verifySlackSignature } from '../../../../lib/verify-signature'
import { inngest, SUPPORT_APPROVAL_DECIDED, SUPPORT_ACTION_APPROVED } from '@skillrecordings/core/inngest'

export async function POST(request: Request) {
  const body = await request.text()
  const signature = request.headers.get('x-slack-signature') ?? ''
  const timestamp = request.headers.get('x-slack-request-timestamp') ?? ''

  // Verify signature (HMAC-SHA256, 5-min replay protection)
  if (!verifySlackSignature({ signature, timestamp, body })) {
    return new Response('Invalid signature', { status: 401 })
  }

  // Parse URL-encoded payload
  const params = new URLSearchParams(body)
  const payload = JSON.parse(params.get('payload') ?? '{}')

  if (payload.type === 'block_actions') {
    const action = payload.actions[0]
    const metadata = JSON.parse(action.value)

    if (action.action_id === 'approve_action') {
      await inngest.send([
        { name: SUPPORT_APPROVAL_DECIDED, data: { approvalId: metadata.actionId, decision: 'approved', ... } },
        { name: SUPPORT_ACTION_APPROVED, data: { actionId: metadata.actionId, ... } },
      ])
    }
  }

  return new Response('OK', { status: 200 }) // Slack requires quick 200
}
```

## Signature Verification

```typescript
import { verifySlackSignature } from 'apps/slack/lib/verify-signature'

// Returns true if valid, false if invalid/expired
// Throws if SLACK_SIGNING_SECRET missing
const isValid = verifySlackSignature({
  signature: request.headers.get('x-slack-signature'),
  timestamp: request.headers.get('x-slack-request-timestamp'),
  body: rawRequestBody,
  // secret defaults to process.env.SLACK_SIGNING_SECRET
})
```

Key features:
- HMAC-SHA256 with timing-safe comparison (prevents timing attacks)
- 5-minute replay protection
- Validates v0= signature prefix

## Authority Levels

```typescript
// AUTO-APPROVE (execute immediately)
- Magic link requests
- Password reset requests
- Refunds within 30 days of purchase
- Transfers within 14 days of purchase
- Email/name updates

// REQUIRE-APPROVAL (draft action, wait for human)
- Refunds 30-45 days after purchase
- Transfers after 14 days
- Bulk seat management
- Account deletions

// ALWAYS-ESCALATE (flag for human, do not act)
- Angry/frustrated customers (sentiment detection)
- Legal language (lawsuit, lawyer, etc.)
- Repeated failed interactions
- Anything uncertain
```

## Draft Comparison (HITL Scoring)

Track how much humans modify agent drafts to build trust:

```typescript
function diffScore(draft: string, sent: string): 'unmodified' | 'edited' | 'rewritten' {
  const draftTokens = new Set(tokenize(draft))
  const sentTokens = new Set(tokenize(sent))
  const intersection = [...draftTokens].filter(t => sentTokens.has(t))
  const overlap = intersection.length / Math.max(draftTokens.size, sentTokens.size)

  if (overlap > 0.95) return 'unmodified'  // Trust++
  if (overlap > 0.50) return 'edited'       // Trust neutral
  return 'rewritten'                         // Trust--
}
```

## Trust Decay

Trust score uses exponential decay with 30-day half-life. High-trust agents can auto-send drafts.

## File Locations

| File | Purpose |
|------|---------|
| `packages/core/src/slack/approval-blocks.ts` | Block Kit message builder |
| `packages/core/src/slack/client.ts` | Slack WebClient singleton (lazy init) |
| `packages/core/src/inngest/workflows/request-approval.ts` | Approval request workflow |
| `packages/core/src/inngest/workflows/execute-approved-action.ts` | Execute after approval |
| `apps/slack/app/api/slack/interactions/route.ts` | Button click handler |
| `apps/slack/lib/verify-signature.ts` | HMAC signature verification |
| `packages/database/src/schema.ts` | ApprovalRequestsTable, ActionsTable |

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `SLACK_BOT_TOKEN` | Slack WebClient authentication |
| `SLACK_SIGNING_SECRET` | Request signature verification |
| `SLACK_APPROVAL_CHANNEL` | Channel ID for posting approvals |

## Reference Docs

For full details, see:
- `docs/support-app-prd/66-hitl.md`
