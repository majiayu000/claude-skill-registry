---
name: interactor-webhooks
description: Receive real-time updates from Interactor via webhooks (push) or Server-Sent Events (pull). Use when building real-time UIs, monitoring credential changes, tracking workflow progress, or streaming AI chat responses.
author: Interactor Integration Guide
---

# Interactor Webhooks and Streaming Skill

Receive real-time updates from Interactor via webhooks (push to your server) or Server-Sent Events (pull from browser/client).

## When to Use

- **Credential Monitoring**: React to credential status changes (expired, revoked)
- **Workflow Notifications**: Get notified when workflows complete or need input
- **Real-time Chat**: Stream AI assistant responses to users
- **Live Dashboards**: Display real-time workflow progress
- **Event-Driven Architecture**: Trigger actions based on Interactor events

## Prerequisites

- Interactor authentication configured (see `interactor-auth` skill)
- HTTPS endpoint for webhooks (required for production)
- Understanding of webhook security (signature verification)

## Webhooks vs SSE: When to Use Each

| Use Case | Recommended | Reason |
|----------|-------------|--------|
| Backend notifications | **Webhooks** | Server-to-server, reliable delivery |
| Credential status changes | **Webhooks** | Background processing, no UI needed |
| Workflow completion | **Webhooks** | Trigger backend actions |
| Real-time chat UI | **SSE** | Low latency, browser-native |
| Live workflow progress | **SSE** | Visual feedback for users |
| Streaming AI responses | **SSE** | Token-by-token display |

**General Rule**: Use webhooks for backend-to-backend, SSE for frontend real-time updates.

---

## Webhooks

Webhooks push events to your server when things happen in Interactor.

### Available Event Types

```bash
curl https://core.interactor.com/api/v1/webhooks/event-types \
  -H "Authorization: Bearer <token>"
```

**Response:**
```json
{
  "data": {
    "event_types": [
      "credential.created",
      "credential.refreshed",
      "credential.expired",
      "credential.revoked",
      "workflow.instance.created",
      "workflow.instance.completed",
      "workflow.instance.failed",
      "workflow.instance.halted",
      "agent.room.message",
      "agent.room.closed"
    ]
  }
}
```

> **Note**: Additional events like `workflow.instance.resumed` and tool invocation events are available via SSE streams only. See the SSE section for details.

### Event Categories

| Category | Webhook Events | Description |
|----------|----------------|-------------|
| **Credentials** | `credential.created`, `credential.refreshed`, `credential.expired`, `credential.revoked` | OAuth token lifecycle |
| **Workflows** | `workflow.instance.created`, `workflow.instance.completed`, `workflow.instance.failed`, `workflow.instance.halted` | Workflow execution status |
| **Agents** | `agent.room.message`, `agent.room.closed` | AI chat events |

> **SSE-Only Events**: `workflow.instance.resumed`, `tool_use`, `tool_result` are available via Server-Sent Events streams only.

### Schema Versioning Policy

Interactor follows these principles for webhook payload changes:

| Change Type | Versioning | Example |
|-------------|------------|---------|
| **New optional fields** | Non-breaking, no version bump | Adding `metadata` field to events |
| **New event types** | Non-breaking, subscribe to receive | `credential.metadata_updated` |
| **Field type changes** | Breaking, announced 90 days ahead | `amount` from string to number |
| **Field removal** | Breaking, announced 90 days ahead | Removing deprecated fields |
| **Payload restructure** | New API version (v2) | Complete payload format change |

**Best practices for forward compatibility:**
- Ignore unknown fields (don't fail on extra properties)
- Use optional types for new fields: `metadata?: Record<string, unknown>`
- Subscribe to Interactor changelog for breaking change announcements
- Test against the `/webhooks/:id/test` endpoint after updates

### Complete Event Mapping Table

| Event | Trigger | Delivery | Typical Handler Action |
|-------|---------|----------|------------------------|
| `credential.created` | User completes OAuth flow | Webhook | Log for audit, update UI state |
| `credential.refreshed` | Token auto-refreshed | Webhook | Log for audit (usually no action needed) |
| `credential.expired` | Refresh token failed | Webhook | **Notify user to reconnect**, disable features |
| `credential.revoked` | User revoked via provider | Webhook | **Notify user to reconnect**, disable features |
| `workflow.instance.created` | Workflow started | Webhook | Track in analytics, show in dashboard |
| `workflow.instance.halted` | Workflow needs user input | Webhook | **Notify user**, show input form |
| `workflow.instance.completed` | Workflow finished successfully | Webhook | **Process results**, update records |
| `workflow.instance.failed` | Workflow error | Webhook | **Alert ops**, log error details |
| `agent.room.message` | AI sent complete message | Webhook | Forward to push notification or websocket |
| `agent.room.closed` | Chat session ended | Webhook | Log analytics, cleanup resources |
| `state_changed` | Workflow state transition | SSE | Update progress UI |
| `workflow_data_updated` | Workflow data modified | SSE | Refresh displayed data |
| `halted` | Workflow needs input | SSE | Show input form |
| `resumed` | User provided input | SSE | Update UI, show processing |
| `completed` | Workflow finished | SSE | Show completion, redirect |
| `message` | Complete message received | SSE | Display in chat |
| `message_start` | AI started responding | SSE | Show typing indicator |
| `message_delta` | Token received | SSE | Append to streaming message |
| `message_end` | AI finished message | SSE | Finalize message, enable input |
| `tool_use` | AI invoked a tool | SSE | Show tool activity indicator |
| `tool_result` | Tool returned result | SSE | Display tool result (optional) |
| `heartbeat` | Connection keepalive | SSE | Reset connection health timer |

### Permissions & RBAC

Webhook management requires specific permissions in Interactor:

| Action | Required Permission | Who Has It |
|--------|---------------------|------------|
| List webhooks | `webhooks:read` | Admin, Developer |
| Create webhook | `webhooks:write` | Admin, Developer |
| Update webhook | `webhooks:write` | Admin, Developer |
| Delete webhook | `webhooks:delete` | Admin only |
| Regenerate secret | `webhooks:write` | Admin, Developer |
| View delivery history | `webhooks:read` | Admin, Developer |

**API Token Scopes:**

When creating API tokens for webhook management, request these scopes:
- `webhooks` - Full webhook management (read + write + delete)
- `webhooks:read` - Read-only access to webhook configuration
- `webhooks:write` - Create and update (no delete)

```bash
# Token with full webhook access
curl -X POST https://core.interactor.com/api/v1/tokens \
  -H "Authorization: Bearer <admin_token>" \
  -d '{"name": "Webhook Manager", "scopes": ["webhooks"]}'
```

> **Security Note**: Webhook secrets are only shown once at creation and regeneration. Store them securely in environment variables or a secrets manager.

---

## Instructions

### Step 1: Create a Webhook

```bash
curl -X POST https://core.interactor.com/api/v1/webhooks \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://yourapp.com/webhooks/interactor",
    "events": [
      "credential.expired",
      "credential.revoked",
      "workflow.instance.completed",
      "workflow.instance.halted"
    ],
    "enabled": true
  }'
```

**Response:**
```json
{
  "data": {
    "id": "wh_abc",
    "url": "https://yourapp.com/webhooks/interactor",
    "secret": "whsec_xyz_SAVE_THIS",
    "events": [
      "credential.expired",
      "credential.revoked",
      "workflow.instance.completed",
      "workflow.instance.halted"
    ],
    "enabled": true,
    "created_at": "2026-01-20T12:00:00Z"
  }
}
```

> **CRITICAL**: Save the `secret` - you'll need it to verify webhook signatures. It's only shown once!

### Step 2: List Webhooks

```bash
curl https://core.interactor.com/api/v1/webhooks \
  -H "Authorization: Bearer <token>"
```

**Response:**
```json
{
  "data": {
    "webhooks": [
      {
        "id": "wh_abc",
        "url": "https://yourapp.com/webhooks/interactor",
        "events": ["credential.expired", "workflow.instance.completed"],
        "enabled": true,
        "created_at": "2026-01-20T12:00:00Z",
        "last_delivery_at": "2026-01-20T12:30:00Z",
        "last_delivery_status": "delivered"
      }
    ]
  }
}
```

### Step 3: Get Webhook Details

```bash
curl https://core.interactor.com/api/v1/webhooks/wh_abc \
  -H "Authorization: Bearer <token>"
```

### Step 4: Update Webhook

```bash
curl -X PUT https://core.interactor.com/api/v1/webhooks/wh_abc \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "events": ["credential.created", "credential.expired"],
    "url": "https://yourapp.com/webhooks/v2/interactor"
  }'
```

### Step 5: Toggle Webhook (Enable/Disable)

```bash
curl -X POST https://core.interactor.com/api/v1/webhooks/wh_abc/toggle \
  -H "Authorization: Bearer <token>"
```

### Step 6: Delete Webhook

```bash
curl -X DELETE https://core.interactor.com/api/v1/webhooks/wh_abc \
  -H "Authorization: Bearer <token>"
```

### Step 7: Regenerate Secret

If your secret is compromised:

```bash
curl -X POST https://core.interactor.com/api/v1/webhooks/wh_abc/regenerate-secret \
  -H "Authorization: Bearer <token>"
```

**Response:**
```json
{
  "data": {
    "id": "wh_abc",
    "secret": "whsec_NEW_SECRET_SAVE_THIS",
    "regenerated_at": "2026-01-20T12:00:00Z"
  }
}
```

> **CRITICAL**: The new secret is only shown once. Update your webhook handler immediately with the new secret.

### Step 8: View Recent Events

See delivery history and debug issues:

```bash
curl https://core.interactor.com/api/v1/webhooks/wh_abc/events \
  -H "Authorization: Bearer <token>"
```

**Response:**
```json
{
  "data": {
    "events": [
      {
        "id": "evt_123",
        "type": "workflow.instance.completed",
        "delivered_at": "2026-01-20T12:00:00Z",
        "status": "delivered",
        "response_code": 200,
        "response_time_ms": 145
      },
      {
        "id": "evt_122",
        "type": "credential.expired",
        "delivered_at": "2026-01-20T11:55:00Z",
        "status": "failed",
        "response_code": 500,
        "retry_count": 2
      }
    ]
  }
}
```

### Step 9: Test Webhook

Send a test event to verify your endpoint:

```bash
curl -X POST https://core.interactor.com/api/v1/webhooks/wh_abc/test \
  -H "Authorization: Bearer <token>"
```

---

## Webhook Payload Format

All webhook events follow this structure:

```json
{
  "id": "evt_abc123",
  "type": "workflow.instance.completed",
  "timestamp": "2026-01-20T12:00:00Z",
  "data": {
    "instance_id": "inst_xyz",
    "workflow_name": "approval_workflow",
    "namespace": "user_123",
    "status": "completed",
    "output": {
      "approved": true,
      "amount": 5000
    }
  }
}
```

### Event-Specific Payloads

**credential.created:**
```json
{
  "id": "evt_001",
  "type": "credential.created",
  "timestamp": "2026-01-20T12:00:00Z",
  "data": {
    "credential_id": "cred_abc",
    "service_id": "google_calendar",
    "service_name": "Google Calendar",
    "namespace": "user_123",
    "scopes": ["calendar.readonly", "calendar.events"]
  }
}
```

**credential.refreshed:**
```json
{
  "id": "evt_002",
  "type": "credential.refreshed",
  "timestamp": "2026-01-20T12:00:00Z",
  "data": {
    "credential_id": "cred_abc",
    "service_id": "google_calendar",
    "service_name": "Google Calendar",
    "namespace": "user_123",
    "expires_at": "2026-01-20T13:00:00Z"
  }
}
```

**credential.expired:**
```json
{
  "id": "evt_003",
  "type": "credential.expired",
  "timestamp": "2026-01-20T12:00:00Z",
  "data": {
    "credential_id": "cred_abc",
    "service_id": "google_calendar",
    "service_name": "Google Calendar",
    "namespace": "user_123",
    "reason": "refresh_token_invalid"
  }
}
```

**credential.revoked:**
```json
{
  "id": "evt_004",
  "type": "credential.revoked",
  "timestamp": "2026-01-20T12:00:00Z",
  "data": {
    "credential_id": "cred_abc",
    "service_id": "google_calendar",
    "service_name": "Google Calendar",
    "namespace": "user_123",
    "reason": "user_revoked_access"
  }
}
```

**workflow.instance.created:**
```json
{
  "id": "evt_005",
  "type": "workflow.instance.created",
  "timestamp": "2026-01-20T12:00:00Z",
  "data": {
    "instance_id": "inst_xyz",
    "workflow_name": "approval_workflow",
    "workflow_id": "wf_abc",
    "namespace": "user_123",
    "initial_input": {
      "request_id": "req_456",
      "amount": 5000
    }
  }
}
```

**workflow.instance.halted:**
```json
{
  "id": "evt_006",
  "type": "workflow.instance.halted",
  "timestamp": "2026-01-20T12:00:00Z",
  "data": {
    "instance_id": "inst_xyz",
    "workflow_name": "approval_workflow",
    "namespace": "user_123",
    "current_state": "await_approval",
    "halting_presentation": {
      "type": "form",
      "title": "Approval Required",
      "fields": [...]
    }
  }
}
```

**workflow.instance.completed:**
```json
{
  "id": "evt_007",
  "type": "workflow.instance.completed",
  "timestamp": "2026-01-20T12:00:00Z",
  "data": {
    "instance_id": "inst_xyz",
    "workflow_name": "approval_workflow",
    "namespace": "user_123",
    "final_state": "approved",
    "workflow_data": {
      "request_id": "req_456",
      "approved": true,
      "amount": 5000
    }
  }
}
```

**workflow.instance.failed:**
```json
{
  "id": "evt_008",
  "type": "workflow.instance.failed",
  "timestamp": "2026-01-20T12:00:00Z",
  "data": {
    "instance_id": "inst_xyz",
    "workflow_name": "approval_workflow",
    "namespace": "user_123",
    "failed_state": "process_payment",
    "error": {
      "code": "payment_declined",
      "message": "Card was declined by issuer"
    }
  }
}
```

**agent.room.message:**
```json
{
  "id": "evt_009",
  "type": "agent.room.message",
  "timestamp": "2026-01-20T12:00:00Z",
  "data": {
    "room_id": "room_xyz",
    "assistant_id": "asst_abc",
    "namespace": "user_123",
    "message_id": "msg_123",
    "role": "assistant",
    "content": "Here's what I found about your billing question..."
  }
}
```

**agent.room.closed:**
```json
{
  "id": "evt_010",
  "type": "agent.room.closed",
  "timestamp": "2026-01-20T12:00:00Z",
  "data": {
    "room_id": "room_xyz",
    "assistant_id": "asst_abc",
    "namespace": "user_123",
    "reason": "user_closed",
    "message_count": 15,
    "duration_seconds": 300
  }
}
```

> **Note**: Not all events require explicit handlers. For example, `credential.created` and `credential.refreshed` are often only logged for audit purposes, while `workflow.instance.created` may only need tracking in analytics systems.

---

## Verifying Webhook Signatures

**CRITICAL**: Always verify signatures to ensure webhooks came from Interactor.

### Signature Header Format

Webhooks include two headers for verification:

```
X-Interactor-Signature: sha256=<64 hex characters>
X-Interactor-Timestamp: 2026-01-20T12:00:00Z
```

**Example:**
```
X-Interactor-Signature: sha256=a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2
X-Interactor-Timestamp: 2026-01-20T12:00:00Z
```

> **Format validation**: The signature header MUST match the format `sha256=` followed by exactly 64 lowercase hexadecimal characters. Reject any other format.

### Preventing Replay Attacks

**CRITICAL**: Always validate the timestamp to prevent replay attacks.

1. Parse `X-Interactor-Timestamp` as ISO8601
2. Reject requests where `|now - timestamp| > allowed_skew` (recommended: 5 minutes)
3. Verify signature only after timestamp validation passes

```typescript
const MAX_TIMESTAMP_SKEW_SECONDS = 300; // 5 minutes

function validateTimestamp(timestampHeader: string | undefined): boolean {
  if (!timestampHeader) return false;

  const timestamp = new Date(timestampHeader);
  if (isNaN(timestamp.getTime())) return false;

  const now = Date.now();
  const diff = Math.abs(now - timestamp.getTime());

  return diff <= MAX_TIMESTAMP_SKEW_SECONDS * 1000;
}
```

### Key Rotation & Multiple Active Secrets

When rotating webhook secrets, you may have a period where both old and new secrets are valid:

```typescript
function verifyWithMultipleSecrets(
  payload: string,
  signatureHeader: string,
  secrets: string[]
): boolean {
  for (const secret of secrets) {
    if (isValidSignature(signatureHeader, Buffer.from(payload), secret)) {
      return true;
    }
  }
  return false;
}

// During rotation, configure both secrets:
const WEBHOOK_SECRETS = [
  process.env.INTERACTOR_WEBHOOK_SECRET!,           // Current secret
  process.env.INTERACTOR_WEBHOOK_SECRET_PREVIOUS!,  // Previous secret (optional)
].filter(Boolean);
```

**Rotation procedure:**
1. Generate new secret via `/regenerate-secret` endpoint
2. Deploy new secret to `INTERACTOR_WEBHOOK_SECRET`
3. Keep old secret in `INTERACTOR_WEBHOOK_SECRET_PREVIOUS` for 24-48 hours
4. Remove old secret after all in-flight events have been delivered

### TypeScript/Node.js Verification

```typescript
import crypto from 'crypto';
import express from 'express';

const app = express();

const MAX_TIMESTAMP_SKEW_MS = 5 * 60 * 1000; // 5 minutes

/**
 * Validates the X-Interactor-Timestamp header to prevent replay attacks.
 * Returns true if the timestamp is within the allowed skew window.
 */
function validateTimestamp(timestampHeader: string | undefined): boolean {
  if (!timestampHeader) return false;

  const timestamp = new Date(timestampHeader);
  if (isNaN(timestamp.getTime())) return false;

  const diff = Math.abs(Date.now() - timestamp.getTime());
  return diff <= MAX_TIMESTAMP_SKEW_MS;
}

/**
 * Validates and verifies the webhook signature using timing-safe comparison.
 * Properly handles the sha256= prefix and validates hex format.
 *
 * IMPORTANT: This function never throws - it returns false for any invalid input.
 */
function isValidSignature(
  signatureHeader: string | undefined,
  payload: Buffer,
  secret: string
): boolean {
  // Guard: header must exist
  if (!signatureHeader) return false;

  // Guard: header must match exact format sha256=<64 hex chars>
  const match = signatureHeader.match(/^sha256=([0-9a-f]{64})$/);
  if (!match) return false;

  const providedSignature = match[1];

  // Compute expected signature
  const expectedSignature = crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex');

  // Convert to buffers for timing-safe comparison
  // Both are now guaranteed to be 64 hex chars = 32 bytes when decoded
  const providedBuffer = Buffer.from(providedSignature, 'hex');
  const expectedBuffer = Buffer.from(expectedSignature, 'hex');

  // Length check (should always pass given regex, but defense in depth)
  if (providedBuffer.length !== expectedBuffer.length) return false;

  return crypto.timingSafeEqual(providedBuffer, expectedBuffer);
}

// IMPORTANT: Use raw body for signature verification
app.post(
  '/webhooks/interactor',
  express.raw({ type: 'application/json' }),
  (req, res) => {
    const signatureHeader = req.headers['x-interactor-signature'] as string;
    const timestampHeader = req.headers['x-interactor-timestamp'] as string;
    const payload = req.body; // Keep as Buffer

    // Step 1: Validate timestamp (prevent replay attacks)
    if (!validateTimestamp(timestampHeader)) {
      console.warn('Webhook rejected: invalid or stale timestamp');
      return res.status(401).json({ error: 'invalid_timestamp' });
    }

    // Step 2: Verify signature
    if (!isValidSignature(signatureHeader, payload, process.env.INTERACTOR_WEBHOOK_SECRET!)) {
      console.warn('Webhook rejected: invalid signature');
      return res.status(401).json({ error: 'invalid_signature' });
    }

    // Step 3: Parse and handle event
    let event: WebhookEvent;
    try {
      event = JSON.parse(payload.toString());
    } catch {
      return res.status(400).json({ error: 'invalid_json' });
    }

    console.log(`Received event: ${event.type} (${event.id})`);

    // Handle asynchronously - respond immediately
    handleWebhookEvent(event).catch((err) => {
      console.error(`Failed to process event ${event.id}:`, err);
    });

    // Always respond quickly (< 5 seconds)
    res.status(200).json({ received: true });
  }
);

async function handleWebhookEvent(event: WebhookEvent) {
  switch (event.type) {
    case 'credential.expired':
    case 'credential.revoked':
      // Notify user to reconnect their account
      await notifyUserToReconnect(
        event.data.namespace,
        event.data.service_name
      );
      break;

    case 'workflow.instance.halted':
      // Notify user they have a pending approval
      await notifyUserOfPendingApproval(
        event.data.namespace,
        event.data.instance_id,
        event.data.halting_presentation
      );
      break;

    case 'workflow.instance.completed':
      // Process completed workflow
      await processCompletedWorkflow(
        event.data.instance_id,
        event.data.workflow_data
      );
      break;

    case 'workflow.instance.failed':
      // Handle workflow failure
      await handleWorkflowFailure(
        event.data.namespace,
        event.data.instance_id,
        event.data.error,
        event.data.failed_state
      );
      break;

    case 'agent.room.message':
      // Forward message to real-time channel (if not using SSE)
      await forwardMessageToClient(
        event.data.namespace,
        event.data.room_id,
        event.data.message_id,
        event.data.content
      );
      break;
  }
}

// Webhook event types for type safety
type WebhookEventType =
  | 'credential.created'
  | 'credential.refreshed'
  | 'credential.expired'
  | 'credential.revoked'
  | 'workflow.instance.created'
  | 'workflow.instance.completed'
  | 'workflow.instance.failed'
  | 'workflow.instance.halted'
  | 'agent.room.message'
  | 'agent.room.closed';

// SSE-only event types (not available via webhooks)
type SSEEventType =
  | 'state_changed'
  | 'workflow_data_updated'
  | 'halted'
  | 'resumed'
  | 'completed'
  | 'message'
  | 'message_start'
  | 'message_delta'
  | 'message_end'
  | 'tool_use'
  | 'tool_result'
  | 'heartbeat';

interface WebhookEvent<T = Record<string, unknown>> {
  id: string;
  type: WebhookEventType;
  timestamp: string;
  data: T;
}

// Specific payload types for each event
interface CredentialEventData {
  credential_id: string;
  service_id: string;
  service_name?: string;
  namespace: string;
  reason?: string;
  scopes?: string[];
  expires_at?: string; // For credential.refreshed
}

interface WorkflowEventData {
  instance_id: string;
  workflow_name: string;
  workflow_id?: string;
  namespace: string;
  status?: 'created' | 'running' | 'halted' | 'completed' | 'failed';
  current_state?: string;
  final_state?: string;
  failed_state?: string;
  error?: { code: string; message: string };
  initial_input?: Record<string, unknown>;
  workflow_data?: Record<string, unknown>;
  output?: Record<string, unknown>;
  halting_presentation?: Record<string, unknown>;
}

interface AgentMessageEventData {
  room_id: string;
  assistant_id: string;
  namespace: string;
  message_id: string;
  role: 'user' | 'assistant';
  content: string;
}

interface AgentRoomClosedEventData {
  room_id: string;
  assistant_id: string;
  namespace: string;
  reason: 'user_closed' | 'timeout' | 'error';
  message_count: number;
  duration_seconds: number;
}
```

### Python/Flask Verification

```python
import hmac
import hashlib
import os
import re
from datetime import datetime, timezone, timedelta
from flask import Flask, request, jsonify

app = Flask(__name__)

MAX_TIMESTAMP_SKEW = timedelta(minutes=5)
SIGNATURE_PATTERN = re.compile(r'^sha256=([0-9a-f]{64})$')


def validate_timestamp(timestamp_header: str | None) -> bool:
    """Validate timestamp to prevent replay attacks."""
    if not timestamp_header:
        return False
    try:
        timestamp = datetime.fromisoformat(timestamp_header.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        return abs(now - timestamp) <= MAX_TIMESTAMP_SKEW
    except (ValueError, TypeError):
        return False


def is_valid_signature(signature_header: str | None, payload: bytes, secret: str) -> bool:
    """
    Validate and verify webhook signature with timing-safe comparison.
    Returns False for any invalid input - never raises exceptions.
    """
    if not signature_header:
        return False

    # Validate format: sha256=<64 hex chars>
    match = SIGNATURE_PATTERN.match(signature_header)
    if not match:
        return False

    provided_signature = match.group(1)
    expected_signature = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(provided_signature, expected_signature)


@app.route('/webhooks/interactor', methods=['POST'])
def handle_webhook():
    signature_header = request.headers.get('X-Interactor-Signature')
    timestamp_header = request.headers.get('X-Interactor-Timestamp')
    payload = request.get_data()

    # Step 1: Validate timestamp (prevent replay attacks)
    if not validate_timestamp(timestamp_header):
        print('Webhook rejected: invalid or stale timestamp')
        return jsonify({'error': 'invalid_timestamp'}), 401

    # Step 2: Verify signature
    if not is_valid_signature(signature_header, payload, os.environ['INTERACTOR_WEBHOOK_SECRET']):
        print('Webhook rejected: invalid signature')
        return jsonify({'error': 'invalid_signature'}), 401

    # Step 3: Parse and handle event
    try:
        event = request.get_json()
    except Exception:
        return jsonify({'error': 'invalid_json'}), 400

    print(f"Received event: {event['type']} ({event['id']})")

    # Handle asynchronously (use Celery, RQ, or similar in production)
    handle_webhook_event(event)

    # Always respond quickly (< 5 seconds)
    return jsonify({'received': True}), 200

def handle_webhook_event(event: dict):
    event_type = event['type']
    data = event['data']

    if event_type in ['credential.expired', 'credential.revoked']:
        notify_user_to_reconnect(data['namespace'], data.get('service_name'))

    elif event_type == 'workflow.instance.halted':
        notify_user_of_pending_approval(
            data['namespace'],
            data['instance_id'],
            data.get('halting_presentation')
        )

    elif event_type == 'workflow.instance.completed':
        process_completed_workflow(data['instance_id'], data.get('workflow_data'))

    elif event_type == 'workflow.instance.failed':
        handle_workflow_failure(
            data['namespace'],
            data['instance_id'],
            data.get('error'),
            data.get('failed_state')
        )

    elif event_type == 'agent.room.message':
        forward_message_to_client(
            data['namespace'],
            data['room_id'],
            data['message_id'],
            data['content']
        )
```

### Elixir/Phoenix Verification

```elixir
defmodule MyAppWeb.WebhookController do
  use MyAppWeb, :controller

  import Plug.Conn, only: [get_req_header: 2]

  # Maximum body size for webhooks (1MB should be plenty)
  @max_body_length 1_048_576
  # Maximum timestamp skew (5 minutes in seconds)
  @max_timestamp_skew 300
  # Regex to validate signature format: sha256=<64 hex chars>
  @signature_pattern ~r/^sha256=([0-9a-f]{64})$/

  def interactor(conn, _params) do
    signature_header = get_req_header(conn, "x-interactor-signature") |> List.first()
    timestamp_header = get_req_header(conn, "x-interactor-timestamp") |> List.first()

    with {:ok, payload, conn} <- read_body(conn, length: @max_body_length),
         :ok <- validate_timestamp(timestamp_header),
         secret <- Application.fetch_env!(:my_app, :interactor_webhook_secret),
         :ok <- verify_signature(payload, signature_header, secret),
         {:ok, event} <- Jason.decode(payload) do
      # Handle asynchronously to respond quickly
      Task.start(fn -> handle_event(event) end)

      conn
      |> put_status(200)
      |> json(%{received: true})
    else
      {:more, _partial, conn} ->
        conn
        |> put_status(413)
        |> json(%{error: "payload_too_large"})

      {:error, :invalid_timestamp} ->
        conn
        |> put_status(401)
        |> json(%{error: "invalid_timestamp"})

      {:error, :invalid_signature} ->
        conn
        |> put_status(401)
        |> json(%{error: "invalid_signature"})

      {:error, _reason} ->
        conn
        |> put_status(400)
        |> json(%{error: "invalid_json"})
    end
  end

  defp validate_timestamp(nil), do: {:error, :invalid_timestamp}

  defp validate_timestamp(timestamp_header) do
    case DateTime.from_iso8601(timestamp_header) do
      {:ok, timestamp, _offset} ->
        now = DateTime.utc_now()
        diff = abs(DateTime.diff(now, timestamp, :second))

        if diff <= @max_timestamp_skew do
          :ok
        else
          {:error, :invalid_timestamp}
        end

      {:error, _} ->
        {:error, :invalid_timestamp}
    end
  end

  defp verify_signature(_payload, nil, _secret), do: {:error, :invalid_signature}

  defp verify_signature(payload, signature_header, secret) do
    case Regex.run(@signature_pattern, signature_header) do
      [_, provided_hex] ->
        expected_hex =
          :crypto.mac(:hmac, :sha256, secret, payload)
          |> Base.encode16(case: :lower)

        if Plug.Crypto.secure_compare(provided_hex, expected_hex) do
          :ok
        else
          {:error, :invalid_signature}
        end

      _ ->
        {:error, :invalid_signature}
    end
  end

  defp handle_event(%{"type" => "credential.expired", "data" => data}) do
    MyApp.Notifications.notify_reconnect(data["namespace"], data["service_name"])
  end

  defp handle_event(%{"type" => "workflow.instance.halted", "data" => data}) do
    MyApp.Notifications.notify_pending_approval(
      data["namespace"],
      data["instance_id"],
      data["halting_presentation"]
    )
  end

  defp handle_event(%{"type" => "workflow.instance.completed", "data" => data}) do
    MyApp.Workflows.process_completed(data["instance_id"], data["workflow_data"])
  end

  defp handle_event(%{"type" => "workflow.instance.failed", "data" => data}) do
    MyApp.Workflows.handle_failure(
      data["namespace"],
      data["instance_id"],
      data["error"],
      data["failed_state"]
    )
  end

  defp handle_event(%{"type" => "agent.room.message", "data" => data}) do
    MyApp.Chat.forward_message(
      data["namespace"],
      data["room_id"],
      data["message_id"],
      data["content"]
    )
  end

  defp handle_event(_event), do: :ok
end
```

---

## Retry Policy

Interactor retries failed webhook deliveries with exponential backoff:

| Attempt | Delay | Total Time |
|---------|-------|------------|
| 1 | Immediate | 0 |
| 2 | 1 minute | 1 min |
| 3 | 5 minutes | 6 min |
| 4 | 30 minutes | 36 min |
| 5 | 2 hours | 2h 36min |

After 5 failed attempts, the webhook is **disabled**. Re-enable via the toggle endpoint.

### HTTP Response Semantics

Your webhook handler's HTTP response determines Interactor's retry behavior:

| HTTP Status | Interactor Behavior | Your Action |
|-------------|---------------------|-------------|
| `200-299` | ✅ Success - no retry | Event processed successfully |
| `400` | ❌ Permanent failure - no retry | Bad request, fix your handler |
| `401` | ❌ Permanent failure - no retry | Signature invalid, check secret |
| `403` | ❌ Permanent failure - no retry | Forbidden, check permissions |
| `404` | ❌ Permanent failure - no retry | Endpoint not found, check URL |
| `408` | 🔄 Retry with backoff | Request timeout, respond faster |
| `429` | 🔄 Retry with backoff | Rate limited, will retry later |
| `500` | 🔄 Retry with backoff | Server error, will retry |
| `502-504` | 🔄 Retry with backoff | Gateway/timeout, will retry |
| Timeout (>30s) | 🔄 Retry with backoff | No response received, will retry |
| Connection refused | 🔄 Retry with backoff | Server unreachable, will retry |

> **Important**: Return `200 OK` immediately, then process asynchronously. If you return `4xx` errors for transient issues, Interactor won't retry.

### Best Practices for Reliability

1. **Respond quickly** - Return 200 within 5 seconds
2. **Process asynchronously** - Queue events for background processing
3. **Be idempotent** - Handle duplicate deliveries gracefully
4. **Log event IDs** - Track which events you've processed

### Idempotent Event Processing

```typescript
// Example: Idempotent event processing with Redis
const IDEMPOTENCY_TTL = 7 * 24 * 60 * 60; // 7 days in seconds

async function handleWebhookEvent(event: WebhookEvent) {
  const idempotencyKey = `webhook:processed:${event.id}`;

  // Atomic check-and-set to prevent race conditions
  const wasSet = await redis.set(idempotencyKey, Date.now(), 'NX', 'EX', IDEMPOTENCY_TTL);

  if (!wasSet) {
    console.log(`Event ${event.id} already processed, skipping`);
    return;
  }

  try {
    await processEvent(event);
    console.log(`Successfully processed event ${event.id}`);
  } catch (error) {
    // Delete the key so retry can process it
    await redis.del(idempotencyKey);
    throw error;
  }
}
```

**Idempotency Storage Recommendations:**

| Storage | TTL | Use Case |
|---------|-----|----------|
| Redis | 7 days | High-throughput, distributed systems |
| PostgreSQL | 30 days | Audit trail needed, lower throughput |
| In-memory | Session | Development/testing only |

### Dead-Letter Queue (DLQ) Strategy

For events that repeatedly fail processing, implement a DLQ:

```typescript
const MAX_PROCESS_ATTEMPTS = 3;
const DLQ_KEY = 'webhook:dlq';

async function handleWebhookEvent(event: WebhookEvent) {
  const attemptKey = `webhook:attempts:${event.id}`;
  const attempts = await redis.incr(attemptKey);
  await redis.expire(attemptKey, 24 * 60 * 60); // 24 hour window

  try {
    await processEvent(event);
    await redis.del(attemptKey);
  } catch (error) {
    if (attempts >= MAX_PROCESS_ATTEMPTS) {
      // Move to DLQ for manual review
      await redis.rpush(DLQ_KEY, JSON.stringify({
        event,
        error: error.message,
        failedAt: new Date().toISOString(),
        attempts
      }));
      await redis.del(attemptKey);
      console.error(`Event ${event.id} moved to DLQ after ${attempts} attempts`);

      // Alert operations team
      await alertOps(`Webhook event ${event.id} failed ${attempts} times`);
    } else {
      console.warn(`Event ${event.id} failed (attempt ${attempts}/${MAX_PROCESS_ATTEMPTS})`);
      throw error; // Will be retried by Interactor
    }
  }
}

// Periodic DLQ processor (run via cron)
async function processDLQ() {
  while (true) {
    const item = await redis.lpop(DLQ_KEY);
    if (!item) break;

    const { event, error, failedAt } = JSON.parse(item);
    console.log(`DLQ item: ${event.id} failed at ${failedAt}: ${error}`);
    // Manual review or automated recovery logic
  }
}
```

### Monitoring & Observability

Track webhook health with these metrics:

**Prometheus Metrics Example:**

```typescript
import { Counter, Histogram, Gauge } from 'prom-client';

// Webhook metrics
const webhookReceived = new Counter({
  name: 'interactor_webhook_received_total',
  help: 'Total webhooks received',
  labelNames: ['event_type', 'status'] // status: success, invalid_signature, invalid_timestamp, processing_error
});

const webhookProcessingDuration = new Histogram({
  name: 'interactor_webhook_processing_duration_seconds',
  help: 'Webhook processing duration in seconds',
  labelNames: ['event_type'],
  buckets: [0.01, 0.05, 0.1, 0.5, 1, 2, 5]
});

const webhookDLQSize = new Gauge({
  name: 'interactor_webhook_dlq_size',
  help: 'Current size of the dead-letter queue'
});

// Usage in handler
app.post('/webhooks/interactor', async (req, res) => {
  const timer = webhookProcessingDuration.startTimer();

  try {
    // ... validation ...

    if (!isValidSignature(...)) {
      webhookReceived.inc({ event_type: 'unknown', status: 'invalid_signature' });
      return res.status(401).json({ error: 'invalid_signature' });
    }

    const event = JSON.parse(payload.toString());
    webhookReceived.inc({ event_type: event.type, status: 'success' });

    await handleWebhookEvent(event);
    timer({ event_type: event.type });

    res.status(200).json({ received: true });
  } catch (error) {
    webhookReceived.inc({ event_type: 'unknown', status: 'processing_error' });
    timer({ event_type: 'error' });
    throw error;
  }
});
```

**Key Metrics to Monitor:**

| Metric | Alert Threshold | Description |
|--------|-----------------|-------------|
| `webhook_received_total{status="invalid_signature"}` | >5 in 5min | Possible secret mismatch or attack |
| `webhook_processing_duration_seconds` | p99 >5s | Risk of timeout, scale handlers |
| `webhook_dlq_size` | >0 | Events need manual review |
| `webhook_received_total{status="processing_error"}` | >10 in 5min | Handler bugs, investigate logs |

---

## Server-Sent Events (SSE)

For real-time streaming in browsers and clients.

### Workflow Instance Stream

Stream updates for a specific workflow instance:

```bash
curl -N https://core.interactor.com/api/v1/workflows/instances/inst_xyz/stream \
  -H "Authorization: Bearer <token>" \
  -H "Accept: text/event-stream"
```

**Events:**
```
event: state_changed
data: {"state": "manager_approval", "previous_state": "submit", "thread_id": "thread_main"}

event: workflow_data_updated
data: {"key": "submitted_at", "value": "2026-01-20T12:00:00Z"}

event: halted
data: {"state": "manager_approval", "presentation": {...}}

event: resumed
data: {"state": "manager_approval", "input": {"approved": true}}

event: completed
data: {"status": "completed", "final_state": "approved", "output": {...}}
```

### Chat Room Stream

Stream messages in a chat room:

```bash
curl -N https://core.interactor.com/api/v1/agents/rooms/room_xyz/stream \
  -H "Authorization: Bearer <token>" \
  -H "Accept: text/event-stream"
```

**Events:**
```
event: message
data: {"id": "msg_1", "role": "user", "content": "Hello"}

event: message_start
data: {"id": "msg_2", "role": "assistant"}

event: message_delta
data: {"id": "msg_2", "delta": "Hi there! "}

event: message_delta
data: {"id": "msg_2", "delta": "How can I "}

event: message_delta
data: {"id": "msg_2", "delta": "help you today?"}

event: message_end
data: {"id": "msg_2", "role": "assistant", "content": "Hi there! How can I help you today?"}

event: tool_use
data: {"id": "call_1", "tool": "search_products", "parameters": {"query": "laptop"}}

event: tool_result
data: {"id": "call_1", "tool": "search_products", "result": {"products": [...]}}

event: heartbeat
data: {"timestamp": "2026-01-20T12:00:30Z"}
```

### SSE Security Best Practices

#### Short-Lived Tokens

Since EventSource doesn't support custom headers, tokens must be passed in the URL. Use short-lived tokens to minimize exposure:

```typescript
// Backend: Generate short-lived SSE token (5 minute expiry)
app.post('/api/sse-token', authenticate, async (req, res) => {
  const sseToken = jwt.sign(
    {
      sub: req.user.id,
      purpose: 'sse',
      roomId: req.body.roomId // Scope token to specific resource
    },
    process.env.SSE_TOKEN_SECRET,
    { expiresIn: '5m' }
  );

  res.json({ token: sseToken, expiresIn: 300 });
});

// Frontend: Request token before connecting
async function connectToSSE(roomId: string) {
  const { token } = await fetch('/api/sse-token', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${authToken}` },
    body: JSON.stringify({ roomId })
  }).then(r => r.json());

  return new EventSource(`/api/sse/rooms/${roomId}?token=${token}`);
}
```

#### Server-Side Proxy Pattern

Proxy SSE connections through your backend to avoid exposing Interactor tokens:

```typescript
// Your backend proxies SSE from Interactor
app.get('/api/sse/rooms/:roomId', authenticate, (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  // Connect to Interactor with server-side token
  const upstream = new EventSource(
    `https://core.interactor.com/api/v1/agents/rooms/${req.params.roomId}/stream`,
    { headers: { 'Authorization': `Bearer ${process.env.INTERACTOR_ACCESS_TOKEN}` } }
  );

  // Forward events to client
  upstream.onmessage = (event) => {
    res.write(`event: ${event.type}\ndata: ${event.data}\n\n`);
  };

  req.on('close', () => upstream.close());
});
```

#### CORS Configuration

If connecting directly to Interactor from the browser:

```typescript
// Ensure your domain is whitelisted in Interactor settings
// Interactor will include these headers:
// Access-Control-Allow-Origin: https://yourdomain.com
// Access-Control-Allow-Credentials: true

// Your CSP should allow connections:
// connect-src 'self' https://core.interactor.com;
```

### Heartbeat & Connection Health

Interactor sends heartbeat events every **30 seconds**. Use them to detect stale connections:

```typescript
const HEARTBEAT_TIMEOUT_MS = 45_000; // 30s interval + 15s grace period
let lastHeartbeat = Date.now();
let healthCheckInterval: NodeJS.Timeout;

function setupHealthCheck(eventSource: EventSource, onStale: () => void) {
  eventSource.addEventListener('heartbeat', () => {
    lastHeartbeat = Date.now();
  });

  healthCheckInterval = setInterval(() => {
    const timeSinceHeartbeat = Date.now() - lastHeartbeat;
    if (timeSinceHeartbeat > HEARTBEAT_TIMEOUT_MS) {
      console.warn(`SSE connection stale (${timeSinceHeartbeat}ms since last heartbeat)`);
      onStale();
    }
  }, 10_000); // Check every 10 seconds
}

function cleanup() {
  clearInterval(healthCheckInterval);
  eventSource.close();
}
```

**Health Thresholds:**

| Condition | Threshold | Action |
|-----------|-----------|--------|
| Normal | Heartbeat within 30s | Connection healthy |
| Warning | 30-45s since heartbeat | Log warning, prepare reconnect |
| Stale | >45s since heartbeat | Force reconnect |
| Failed | 3 consecutive reconnect failures | Alert user, escalate to support |

---

## SSE Client Implementations

### Browser (Native EventSource)

```typescript
const token = 'your_access_token';
const roomId = 'room_xyz';

// Note: EventSource doesn't support custom headers
// Pass token as query parameter
const eventSource = new EventSource(
  `https://core.interactor.com/api/v1/agents/rooms/${roomId}/stream?token=${token}`
);

// ⚠️ SECURITY NOTE: Token in URL may appear in server access logs.
// For enhanced security, use short-lived tokens specifically for SSE connections.
// Consider using a dedicated SSE token endpoint that issues time-limited tokens.

// Handle different event types
eventSource.addEventListener('message', (event) => {
  const data = JSON.parse(event.data);
  displayMessage(data);
});

eventSource.addEventListener('message_start', (event) => {
  const data = JSON.parse(event.data);
  startStreamingMessage(data.id);
});

eventSource.addEventListener('message_delta', (event) => {
  const data = JSON.parse(event.data);
  appendToStreamingMessage(data.id, data.delta);
});

eventSource.addEventListener('message_end', (event) => {
  const data = JSON.parse(event.data);
  finalizeStreamingMessage(data.id, data.content);
});

eventSource.addEventListener('tool_use', (event) => {
  const data = JSON.parse(event.data);
  showToolUsage(data.tool, data.parameters);
});

eventSource.addEventListener('tool_result', (event) => {
  const data = JSON.parse(event.data);
  showToolResult(data.tool, data.result);
});

eventSource.addEventListener('heartbeat', (event) => {
  // Connection is alive
  updateLastHeartbeat();
});

eventSource.onerror = (error) => {
  console.error('SSE error:', error);
  // Implement reconnection logic
  if (eventSource.readyState === EventSource.CLOSED) {
    setTimeout(() => reconnect(), 5000);
  }
};

// Clean up when done
function cleanup() {
  eventSource.close();
}
```

### React Hook for Chat Streaming

```tsx
import { useEffect, useState, useRef, useCallback } from 'react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  isStreaming?: boolean;
}

interface UseChatStreamOptions {
  roomId: string;
  token: string;
  onError?: (error: Error) => void;
}

export function useChatStream({ roomId, token, onError }: UseChatStreamOptions) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const eventSourceRef = useRef<EventSource | null>(null);
  const streamingContentRef = useRef<Map<string, string>>(new Map());

  // Use ref for onError to prevent infinite re-renders
  // when onError is an inline function
  const onErrorRef = useRef(onError);
  useEffect(() => {
    onErrorRef.current = onError;
  }, [onError]);

  const connect = useCallback(() => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }

    const url = `https://core.interactor.com/api/v1/agents/rooms/${roomId}/stream?token=${token}`;
    const eventSource = new EventSource(url);
    eventSourceRef.current = eventSource;

    eventSource.onopen = () => {
      setIsConnected(true);
    };

    eventSource.addEventListener('message', (event) => {
      const data = JSON.parse(event.data);
      setMessages(prev => [...prev, data]);
    });

    eventSource.addEventListener('message_start', (event) => {
      const data = JSON.parse(event.data);
      setIsStreaming(true);
      streamingContentRef.current.set(data.id, '');
      setMessages(prev => [...prev, {
        id: data.id,
        role: 'assistant',
        content: '',
        isStreaming: true
      }]);
    });

    eventSource.addEventListener('message_delta', (event) => {
      const data = JSON.parse(event.data);
      const currentContent = streamingContentRef.current.get(data.id) || '';
      const newContent = currentContent + data.delta;
      streamingContentRef.current.set(data.id, newContent);

      setMessages(prev => prev.map(msg =>
        msg.id === data.id
          ? { ...msg, content: newContent }
          : msg
      ));
    });

    eventSource.addEventListener('message_end', (event) => {
      const data = JSON.parse(event.data);
      setIsStreaming(false);
      streamingContentRef.current.delete(data.id);

      setMessages(prev => prev.map(msg =>
        msg.id === data.id
          ? { ...msg, content: data.content, isStreaming: false }
          : msg
      ));
    });

    eventSource.onerror = () => {
      setIsConnected(false);
      onErrorRef.current?.(new Error('SSE connection error'));

      // Auto-reconnect after 5 seconds
      setTimeout(() => {
        if (eventSourceRef.current?.readyState === EventSource.CLOSED) {
          connect();
        }
      }, 5000);
    };
  }, [roomId, token]); // Note: onError removed, using ref instead

  const disconnect = useCallback(() => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }
    // Clean up streaming content map to prevent memory leaks
    streamingContentRef.current.clear();
    setIsConnected(false);
    setIsStreaming(false);
  }, []);

  useEffect(() => {
    connect();
    return () => disconnect();
  }, [connect, disconnect]);

  return {
    messages,
    isConnected,
    isStreaming,
    reconnect: connect,
    disconnect
  };
}

// Usage in component
function ChatRoom({ roomId, token }: { roomId: string; token: string }) {
  const { messages, isConnected, isStreaming } = useChatStream({
    roomId,
    token,
    onError: (error) => console.error('Chat error:', error)
  });

  return (
    <div className="chat-room">
      <div className="status">
        {isConnected ? '🟢 Connected' : '🔴 Disconnected'}
        {isStreaming && ' (typing...)'}
      </div>

      <div className="messages">
        {messages.map((msg) => (
          <div key={msg.id} className={`message ${msg.role}`}>
            <div className="content">
              {msg.content}
              {msg.isStreaming && <span className="cursor">▊</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
```

### Node.js SSE Client

```typescript
import EventSource from 'eventsource';

class InteractorSSEClient {
  private eventSource: EventSource | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;

  constructor(
    private baseUrl: string,
    private token: string
  ) {}

  connectToRoom(roomId: string, handlers: {
    onMessage?: (message: any) => void;
    onMessageStart?: (data: any) => void;
    onMessageDelta?: (data: any) => void;
    onMessageEnd?: (data: any) => void;
    onToolUse?: (data: any) => void;
    onToolResult?: (data: any) => void;
    onHeartbeat?: (data: any) => void;
    onError?: (error: Error) => void;
  }) {
    const url = `${this.baseUrl}/agents/rooms/${roomId}/stream`;

    this.eventSource = new EventSource(url, {
      headers: {
        'Authorization': `Bearer ${this.token}`
      }
    });

    this.eventSource.onopen = () => {
      console.log('SSE connected to room:', roomId);
      this.reconnectAttempts = 0;
    };

    if (handlers.onMessage) {
      this.eventSource.addEventListener('message', (event) => {
        handlers.onMessage!(JSON.parse(event.data));
      });
    }

    if (handlers.onMessageStart) {
      this.eventSource.addEventListener('message_start', (event) => {
        handlers.onMessageStart!(JSON.parse(event.data));
      });
    }

    if (handlers.onMessageDelta) {
      this.eventSource.addEventListener('message_delta', (event) => {
        handlers.onMessageDelta!(JSON.parse(event.data));
      });
    }

    if (handlers.onMessageEnd) {
      this.eventSource.addEventListener('message_end', (event) => {
        handlers.onMessageEnd!(JSON.parse(event.data));
      });
    }

    if (handlers.onToolUse) {
      this.eventSource.addEventListener('tool_use', (event) => {
        handlers.onToolUse!(JSON.parse(event.data));
      });
    }

    if (handlers.onToolResult) {
      this.eventSource.addEventListener('tool_result', (event) => {
        handlers.onToolResult!(JSON.parse(event.data));
      });
    }

    if (handlers.onHeartbeat) {
      this.eventSource.addEventListener('heartbeat', (event) => {
        handlers.onHeartbeat!(JSON.parse(event.data));
      });
    }

    this.eventSource.onerror = (error) => {
      console.error('SSE error:', error);
      handlers.onError?.(new Error('SSE connection error'));

      // Auto-reconnect with backoff
      if (this.reconnectAttempts < this.maxReconnectAttempts) {
        const delay = Math.pow(2, this.reconnectAttempts) * 1000;
        this.reconnectAttempts++;
        setTimeout(() => this.connectToRoom(roomId, handlers), delay);
      }
    };

    return this;
  }

  connectToWorkflow(instanceId: string, handlers: {
    onStateChanged?: (data: any) => void;
    onWorkflowDataUpdated?: (data: any) => void;
    onHalted?: (data: any) => void;
    onResumed?: (data: any) => void;
    onCompleted?: (data: any) => void;
    onHeartbeat?: (data: any) => void;
    onError?: (error: Error) => void;
  }) {
    const url = `${this.baseUrl}/workflows/instances/${instanceId}/stream`;

    this.eventSource = new EventSource(url, {
      headers: {
        'Authorization': `Bearer ${this.token}`
      }
    });

    this.eventSource.onopen = () => {
      console.log('SSE connected to workflow:', instanceId);
      this.reconnectAttempts = 0;
    };

    if (handlers.onStateChanged) {
      this.eventSource.addEventListener('state_changed', (event) => {
        handlers.onStateChanged!(JSON.parse(event.data));
      });
    }

    if (handlers.onWorkflowDataUpdated) {
      this.eventSource.addEventListener('workflow_data_updated', (event) => {
        handlers.onWorkflowDataUpdated!(JSON.parse(event.data));
      });
    }

    if (handlers.onHalted) {
      this.eventSource.addEventListener('halted', (event) => {
        handlers.onHalted!(JSON.parse(event.data));
      });
    }

    if (handlers.onResumed) {
      this.eventSource.addEventListener('resumed', (event) => {
        handlers.onResumed!(JSON.parse(event.data));
      });
    }

    if (handlers.onCompleted) {
      this.eventSource.addEventListener('completed', (event) => {
        handlers.onCompleted!(JSON.parse(event.data));
      });
    }

    if (handlers.onHeartbeat) {
      this.eventSource.addEventListener('heartbeat', (event) => {
        handlers.onHeartbeat!(JSON.parse(event.data));
      });
    }

    this.eventSource.onerror = (error) => {
      console.error('SSE error:', error);
      handlers.onError?.(new Error('SSE connection error'));

      // Auto-reconnect with backoff (same as room connection)
      if (this.reconnectAttempts < this.maxReconnectAttempts) {
        const delay = Math.pow(2, this.reconnectAttempts) * 1000;
        this.reconnectAttempts++;
        setTimeout(() => this.connectToWorkflow(instanceId, handlers), delay);
      }
    };

    return this;
  }

  disconnect() {
    if (this.eventSource) {
      this.eventSource.close();
      this.eventSource = null;
    }
  }
}

// Usage
const sseClient = new InteractorSSEClient(
  'https://core.interactor.com/api/v1',
  process.env.INTERACTOR_ACCESS_TOKEN!
);

sseClient.connectToRoom('room_xyz', {
  onMessageDelta: (data) => {
    process.stdout.write(data.delta);
  },
  onMessageEnd: (data) => {
    console.log('\n--- Message complete ---');
  },
  onError: (error) => {
    console.error('Error:', error);
  }
});
```

---

## Rate Limits

| Resource | Limit |
|----------|-------|
| Webhooks per account | 50 |
| SSE connections per account | 10 concurrent |
| Events per webhook | Unlimited |

---

## Best Practices

### Webhooks

1. **Always verify signatures** - Reject requests with invalid signatures
2. **Respond quickly** - Return 200 within 5 seconds, process asynchronously
3. **Handle duplicates** - Events may be delivered more than once
4. **Use idempotent processing** - Track event IDs to prevent double-processing
5. **Monitor delivery** - Check webhook events list for failures
6. **Use HTTPS** - Required for production webhooks

### SSE

1. **Handle reconnection** - SSE connections may drop; implement auto-reconnect
2. **Watch for heartbeats** - Detect stale connections
3. **Close when done** - Close connections when leaving pages/screens
4. **Limit connections** - Max 10 concurrent SSE connections per account
5. **Use for frontend only** - For backend, prefer webhooks

---

## Local Development & Testing

### Testing Webhooks Locally

Webhooks require a publicly accessible URL. For local development:

**Option 1: ngrok (Recommended)**
```bash
# Install ngrok: https://ngrok.com/download
ngrok http 4000  # For Phoenix default port

# Use the generated URL for your webhook
# Example: https://abc123.ngrok.io/webhooks/interactor
```

**Option 2: localtunnel**
```bash
npm install -g localtunnel
lt --port 4000

# Use the generated URL for your webhook
```

**Option 3: Cloudflare Tunnel**
```bash
cloudflared tunnel --url http://localhost:4000
```

### Testing Webhook Signature Verification

Create a test script to verify your signature implementation:

```typescript
// test-webhook-signature.ts
import crypto from 'crypto';

const secret = 'whsec_your_test_secret';
const payload = JSON.stringify({
  id: 'evt_test',
  type: 'workflow.instance.completed',
  timestamp: new Date().toISOString(),
  data: { instance_id: 'inst_test' }
});

const signature = 'sha256=' + crypto
  .createHmac('sha256', secret)
  .update(payload)
  .digest('hex');

console.log('Test payload:', payload);
console.log('Test signature:', signature);

// Use curl to test:
// curl -X POST http://localhost:4000/webhooks/interactor \
//   -H "Content-Type: application/json" \
//   -H "X-Interactor-Signature: ${signature}" \
//   -d '${payload}'
```

### Use the Test Endpoint

Interactor provides a test endpoint to send sample events:

```bash
curl -X POST https://core.interactor.com/api/v1/webhooks/wh_abc/test \
  -H "Authorization: Bearer <token>"
```

This sends a test event to your webhook URL to verify it's working.

### Postman Collection

Import this collection to test webhook handling:

```json
{
  "info": { "name": "Interactor Webhooks", "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json" },
  "variable": [
    { "key": "webhook_secret", "value": "whsec_your_test_secret" },
    { "key": "webhook_url", "value": "http://localhost:4000/webhooks/interactor" }
  ],
  "item": [
    {
      "name": "Test Webhook - Credential Expired",
      "request": {
        "method": "POST",
        "url": "{{webhook_url}}",
        "header": [
          { "key": "Content-Type", "value": "application/json" },
          { "key": "X-Interactor-Signature", "value": "sha256={{signature}}" },
          { "key": "X-Interactor-Timestamp", "value": "{{timestamp}}" }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\"id\":\"evt_test_001\",\"type\":\"credential.expired\",\"timestamp\":\"{{timestamp}}\",\"data\":{\"credential_id\":\"cred_test\",\"service_id\":\"google_calendar\",\"namespace\":\"user_123\",\"reason\":\"refresh_token_invalid\"}}"
        }
      }
    }
  ]
}
```

**Pre-request script to generate signature:**
```javascript
const crypto = require('crypto-js');
const timestamp = new Date().toISOString();
const payload = pm.request.body.raw.replace(/\{\{timestamp\}\}/g, timestamp);
const signature = crypto.HmacSHA256(payload, pm.variables.get('webhook_secret')).toString();

pm.variables.set('timestamp', timestamp);
pm.variables.set('signature', signature);
pm.request.body.raw = payload;
```

### Unit Test Template (TypeScript/Jest)

```typescript
import crypto from 'crypto';
import request from 'supertest';
import app from '../app'; // Your Express app

describe('Webhook Handler', () => {
  const WEBHOOK_SECRET = 'whsec_test_secret_123';

  beforeAll(() => {
    process.env.INTERACTOR_WEBHOOK_SECRET = WEBHOOK_SECRET;
  });

  function generateSignature(payload: string): string {
    return 'sha256=' + crypto.createHmac('sha256', WEBHOOK_SECRET).update(payload).digest('hex');
  }

  function generateTimestamp(offsetMs = 0): string {
    return new Date(Date.now() + offsetMs).toISOString();
  }

  it('accepts valid webhook', async () => {
    const payload = JSON.stringify({
      id: 'evt_test_001',
      type: 'workflow.instance.completed',
      timestamp: generateTimestamp(),
      data: { instance_id: 'inst_123' }
    });

    const res = await request(app)
      .post('/webhooks/interactor')
      .set('Content-Type', 'application/json')
      .set('X-Interactor-Signature', generateSignature(payload))
      .set('X-Interactor-Timestamp', generateTimestamp())
      .send(payload);

    expect(res.status).toBe(200);
    expect(res.body.received).toBe(true);
  });

  it('rejects invalid signature', async () => {
    const payload = JSON.stringify({ id: 'evt_test', type: 'test' });

    const res = await request(app)
      .post('/webhooks/interactor')
      .set('Content-Type', 'application/json')
      .set('X-Interactor-Signature', 'sha256=invalid')
      .set('X-Interactor-Timestamp', generateTimestamp())
      .send(payload);

    expect(res.status).toBe(401);
    expect(res.body.error).toBe('invalid_signature');
  });

  it('rejects malformed signature header', async () => {
    const payload = JSON.stringify({ id: 'evt_test', type: 'test' });

    const res = await request(app)
      .post('/webhooks/interactor')
      .set('Content-Type', 'application/json')
      .set('X-Interactor-Signature', 'not_sha256_format')
      .set('X-Interactor-Timestamp', generateTimestamp())
      .send(payload);

    expect(res.status).toBe(401);
  });

  it('rejects stale timestamp (replay attack)', async () => {
    const payload = JSON.stringify({ id: 'evt_test', type: 'test' });
    const staleTimestamp = generateTimestamp(-10 * 60 * 1000); // 10 minutes ago

    const res = await request(app)
      .post('/webhooks/interactor')
      .set('Content-Type', 'application/json')
      .set('X-Interactor-Signature', generateSignature(payload))
      .set('X-Interactor-Timestamp', staleTimestamp)
      .send(payload);

    expect(res.status).toBe(401);
    expect(res.body.error).toBe('invalid_timestamp');
  });

  it('handles duplicate events idempotently', async () => {
    const eventId = 'evt_duplicate_test';
    const payload = JSON.stringify({
      id: eventId,
      type: 'workflow.instance.completed',
      timestamp: generateTimestamp(),
      data: { instance_id: 'inst_123' }
    });

    // First request
    await request(app)
      .post('/webhooks/interactor')
      .set('Content-Type', 'application/json')
      .set('X-Interactor-Signature', generateSignature(payload))
      .set('X-Interactor-Timestamp', generateTimestamp())
      .send(payload);

    // Second request (duplicate)
    const res = await request(app)
      .post('/webhooks/interactor')
      .set('Content-Type', 'application/json')
      .set('X-Interactor-Signature', generateSignature(payload))
      .set('X-Interactor-Timestamp', generateTimestamp())
      .send(payload);

    expect(res.status).toBe(200); // Should still succeed, just skip processing
  });
});
```

### Event Replay Script

Replay historical events for debugging or recovery:

```typescript
#!/usr/bin/env npx ts-node
// scripts/replay-webhook-events.ts
import crypto from 'crypto';
import fetch from 'node-fetch';

interface ReplayOptions {
  webhookUrl: string;
  webhookSecret: string;
  events: Array<{ id: string; type: string; data: unknown }>;
  delayMs?: number;
}

async function replayEvents({ webhookUrl, webhookSecret, events, delayMs = 100 }: ReplayOptions) {
  for (const event of events) {
    const timestamp = new Date().toISOString();
    const payload = JSON.stringify({
      ...event,
      timestamp,
      _replayed: true, // Mark as replayed for debugging
      _originalTimestamp: event.timestamp
    });

    const signature = 'sha256=' + crypto
      .createHmac('sha256', webhookSecret)
      .update(payload)
      .digest('hex');

    try {
      const res = await fetch(webhookUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Interactor-Signature': signature,
          'X-Interactor-Timestamp': timestamp
        },
        body: payload
      });

      console.log(`[${event.id}] ${event.type}: ${res.status} ${res.statusText}`);
    } catch (error) {
      console.error(`[${event.id}] FAILED:`, error);
    }

    await new Promise(r => setTimeout(r, delayMs));
  }
}

// Usage: Fetch events from Interactor and replay locally
const events = [
  { id: 'evt_001', type: 'credential.expired', data: { credential_id: 'cred_abc', namespace: 'user_123' } },
  { id: 'evt_002', type: 'workflow.instance.completed', data: { instance_id: 'inst_xyz' } }
];

replayEvents({
  webhookUrl: 'http://localhost:4000/webhooks/interactor',
  webhookSecret: process.env.INTERACTOR_WEBHOOK_SECRET!,
  events
});
```

---

## Error Handling

### Webhook API Errors

| Error Code | HTTP Status | Description | Resolution |
|------------|-------------|-------------|------------|
| `webhook_not_found` | 404 | Webhook ID doesn't exist | Verify webhook ID, may have been deleted |
| `invalid_url` | 400 | URL not valid HTTPS | Use `https://` URL (HTTP only in dev) |
| `invalid_events` | 400 | Unknown event types in subscription | Check `/event-types` for valid events |
| `webhook_disabled` | 400 | Webhook disabled after failures | Fix endpoint issues, then toggle to re-enable |
| `max_webhooks_exceeded` | 400 | Account webhook limit reached | Delete unused webhooks or contact support |
| `url_unreachable` | 400 | Cannot reach webhook URL | Ensure URL is publicly accessible |
| `invalid_secret_format` | 500 | Internal error generating secret | Retry request, contact support if persists |
| `rate_limited` | 429 | Too many API requests | Wait and retry with exponential backoff |
| `unauthorized` | 401 | Invalid or expired token | Refresh authentication token |
| `forbidden` | 403 | Insufficient permissions | Check API token scopes |

### Webhook Delivery Errors

Your endpoint may receive these error scenarios:

| Scenario | Your Response | Interactor Behavior |
|----------|---------------|---------------------|
| Signature mismatch | Return `401` | Logged as authentication failure |
| Timestamp too old | Return `401` | Logged as authentication failure |
| Unknown event type | Return `200` | Treated as success (forward compatible) |
| Processing error (recoverable) | Return `500` | Retried with backoff |
| Processing error (permanent) | Return `400` | Not retried, logged as permanent failure |
| Timeout (no response) | N/A | Retried with backoff |

### SSE Errors

| Error | HTTP Status | Cause | Resolution |
|-------|-------------|-------|------------|
| Connection refused | 401 | Invalid or expired token | Refresh token and reconnect |
| Connection refused | 403 | No access to resource | Check permissions for room/workflow |
| Resource not found | 404 | Invalid room_id or instance_id | Verify resource exists |
| Connection dropped | N/A | Network issues | Implement auto-reconnect with backoff |
| Rate limited | 429 | Too many connections | Close unused connections, respect limits |
| Server error | 500 | Interactor service issue | Retry with backoff, check status page |

### Rate Limit Exceeded Behavior

When you exceed rate limits, Interactor returns:

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 60
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1706176800

{
  "error": "rate_limited",
  "message": "Too many requests. Please retry after 60 seconds.",
  "retry_after": 60
}
```

**Rate limit headers:**
- `X-RateLimit-Limit`: Maximum requests per window
- `X-RateLimit-Remaining`: Requests remaining in current window
- `X-RateLimit-Reset`: Unix timestamp when the window resets
- `Retry-After`: Seconds to wait before retrying

**Handling rate limits:**

```typescript
async function callInteractorAPI(endpoint: string, options: RequestInit) {
  const response = await fetch(`https://core.interactor.com/api/v1${endpoint}`, options);

  if (response.status === 429) {
    const retryAfter = parseInt(response.headers.get('Retry-After') || '60', 10);
    console.warn(`Rate limited. Retrying after ${retryAfter}s`);
    await new Promise(r => setTimeout(r, retryAfter * 1000));
    return callInteractorAPI(endpoint, options); // Retry once
  }

  return response;
}
```

---

## Output Format

When implementing webhooks/streaming, provide this summary:

```markdown
## Webhooks & Streaming Implementation Report

**Date**: YYYY-MM-DD

### Webhooks Configured
| Webhook ID | URL | Events | Status |
|------------|-----|--------|--------|
| wh_abc | https://app.com/webhooks | credential.*, workflow.* | ✓ Active |

### Event Handlers
| Event | Handler | Status |
|-------|---------|--------|
| credential.expired | notifyUserToReconnect() | ✓ Implemented |
| credential.revoked | notifyUserToReconnect() | ✓ Implemented |
| workflow.instance.halted | notifyPendingApproval() | ✓ Implemented |
| workflow.instance.completed | processWorkflowResult() | ✓ Implemented |
| workflow.instance.failed | handleWorkflowFailure() | ✓ Implemented |
| agent.room.message | forwardToRealtime() | ✓ Implemented |

### SSE Streams
| Stream | Purpose | Status |
|--------|---------|--------|
| Room stream | Real-time chat UI | ✓ Implemented |
| Workflow stream | Progress tracking | ✓ Implemented |

### Implementation Checklist

**Security**
- [ ] Webhook endpoint uses HTTPS (required for production)
- [ ] Signature verification with timing-safe comparison
- [ ] Signature header format validated (`sha256=` + 64 hex chars)
- [ ] Timestamp validation to prevent replay attacks (5 min window)
- [ ] Webhook secret stored in environment variable (not in code)
- [ ] Key rotation procedure documented and tested
- [ ] SSE tokens are short-lived (5 min) or proxied through backend

**Reliability**
- [ ] Respond to webhooks within 5 seconds
- [ ] Async processing with background job queue
- [ ] Idempotent processing (track event IDs in Redis/DB)
- [ ] Dead-letter queue for failed events
- [ ] Event handlers for all subscribed events
- [ ] Unknown event types handled gracefully (ignore, don't fail)

**Observability**
- [ ] Webhook received counter (by event_type, status)
- [ ] Processing duration histogram
- [ ] DLQ size gauge
- [ ] Error rate alerting configured
- [ ] Signature validation failure alerting

**SSE**
- [ ] Auto-reconnect with exponential backoff
- [ ] Heartbeat monitoring (45s timeout)
- [ ] Connection cleanup on component unmount
- [ ] Connection health indicator in UI
- [ ] Max reconnect attempts with user notification

**Testing**
- [ ] Unit tests for signature verification
- [ ] Unit tests for timestamp validation
- [ ] Integration tests with test webhook endpoint
- [ ] Replay script available for debugging
```

---

## Related Skills

- **interactor-auth**: Setup authentication (prerequisite)
- **interactor-credentials**: Credential events to monitor
- **interactor-agents**: Chat streaming events
- **interactor-workflows**: Workflow status events
