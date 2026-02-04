---
name: interactor-agents
description: Create LLM-powered AI assistants with tools and data sources through Interactor. Use when building conversational AI, chatbots, tool-calling assistants, or agents that need to query databases and external APIs.
author: Interactor Integration Guide
---

# Interactor AI Agents Skill

Build LLM-powered assistants that can have conversations, use tools, and access your data sources.

## When to Use

- **Conversational AI**: Building chat interfaces with AI assistants
- **Tool-Calling Agents**: Creating assistants that can invoke custom functions
- **Data-Connected AI**: Connecting AI to databases for natural language queries
- **Customer Support Bots**: Building support assistants with domain knowledge
- **Internal Tools**: Creating AI assistants for internal operations

## Prerequisites

- Interactor authentication configured (see `interactor-auth` skill)
- Understanding of LLM concepts (prompts, tools, context)
- Webhook endpoint for tool callbacks (optional, for custom tools)
- Database with network access from Interactor (optional, for data sources)
- `jq` command-line tool (for bash examples)

## Overview

The AI Agents system consists of:

| Component | Description |
|-----------|-------------|
| **Assistants** | Configured AI agents with specific behaviors and capabilities |
| **Rooms** | Chat sessions between users and assistants |
| **Messages** | Individual messages in a conversation |
| **Tools** | Custom functions that assistants can invoke |
| **Data Sources** | Databases and APIs that assistants can query |

---

## Quick Start

The typical implementation flow:

```
1. Create an Assistant    → Define behavior with instructions and model config
         ↓
2. Register Tools         → (Optional) Add custom functions the assistant can call
         ↓
3. Connect Data Sources   → (Optional) Connect databases for natural language queries
         ↓
4. Create a Room          → Start a conversation session for a user
         ↓
5. Send/Receive Messages  → Exchange messages, handle tool calls
         ↓
6. Close Room             → End the conversation when complete
```

**Minimal Example:**

> **Prerequisites**: This example requires `jq` for JSON parsing and a valid `$TOKEN`.
> See `interactor-auth` skill for authentication setup.

```bash
# Get your token first (see interactor-auth skill)
# export TOKEN="your_access_token_here"

# 1. Create assistant
ASSISTANT_ID=$(curl -s -X POST https://core.interactor.com/api/v1/agents/assistants \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "helper", "title": "Helper", "instructions": "You are a helpful assistant."}' \
  | jq -r '.data.id')

echo "Created assistant: $ASSISTANT_ID"

# 2. Create room
ROOM_ID=$(curl -s -X POST https://core.interactor.com/api/v1/agents/$ASSISTANT_ID/rooms \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"namespace": "user_123"}' \
  | jq -r '.data.id')

echo "Created room: $ROOM_ID"

# 3. Send message
curl -X POST https://core.interactor.com/api/v1/agents/rooms/$ROOM_ID/messages \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello!", "role": "user"}'
```

---

## Instructions

> **API Version Note**: This skill documents the standard AI Agents API. Some operations
> (DELETE endpoints, advanced pagination options) may vary by Interactor version.
> Always verify endpoint availability against your specific API documentation or test
> in a development environment first.

### Step 1: Create an Assistant

```bash
curl -X POST https://core.interactor.com/api/v1/agents/assistants \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "support_assistant",
    "title": "Support Assistant",
    "description": "Helps users with support questions",
    "model_config": {
      "provider": "openai",
      "model": "gpt-4o",
      "temperature": 0.7
    },
    "instructions": "You are a helpful support assistant. Be concise and friendly. Always try to resolve issues on the first response.",
    "enabled_tools": ["search_knowledge_base", "create_ticket"]
  }'
```

**Response:**
```json
{
  "data": {
    "id": "asst_abc",
    "name": "support_assistant",
    "title": "Support Assistant",
    "description": "Helps users with support questions",
    "model_config": {
      "provider": "openai",
      "model": "gpt-4o",
      "temperature": 0.7
    },
    "enabled_tools": ["search_knowledge_base", "create_ticket"],
    "created_at": "2026-01-20T12:00:00Z"
  }
}
```

### Assistant Configuration Options

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique identifier (lowercase, underscores only) |
| `title` | string | Yes | Display name for users |
| `description` | string | No | What the assistant does |
| `model_config.provider` | string | No | `openai` (default: `openai`) |
| `model_config.model` | string | No | Model identifier (default: `gpt-4o`) |
| `model_config.temperature` | number | No | Response randomness 0.0-1.0 (default: 0.7) |
| `instructions` | string | Yes | System prompt defining behavior |
| `enabled_tools` | array | No | Tool names the assistant can use |

### List Assistants

```bash
curl https://core.interactor.com/api/v1/agents/assistants \
  -H "Authorization: Bearer <token>"
```

### Get Assistant

```bash
curl https://core.interactor.com/api/v1/agents/assistants/asst_abc \
  -H "Authorization: Bearer <token>"
```

### Update Assistant

```bash
curl -X PUT https://core.interactor.com/api/v1/agents/assistants/asst_abc \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "instructions": "Updated instructions with more detail...",
    "model_config": {
      "temperature": 0.5
    }
  }'
```

### Delete Assistant

```bash
curl -X DELETE https://core.interactor.com/api/v1/agents/assistants/asst_abc \
  -H "Authorization: Bearer <token>"
```

---

## Chat Rooms

Rooms are conversations between a user and an assistant.

### Create a Room

```bash
curl -X POST https://core.interactor.com/api/v1/agents/asst_abc/rooms \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "namespace": "user_123",
    "metadata": {
      "user_name": "John",
      "context": "billing_question",
      "plan": "premium"
    }
  }'
```

**Response:**
```json
{
  "data": {
    "id": "room_xyz",
    "assistant_id": "asst_abc",
    "namespace": "user_123",
    "status": "active",
    "metadata": {
      "user_name": "John",
      "context": "billing_question",
      "plan": "premium"
    },
    "created_at": "2026-01-20T12:00:00Z"
  }
}
```

### List Rooms

```bash
curl https://core.interactor.com/api/v1/agents/rooms \
  -H "Authorization: Bearer <token>"
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `namespace` | string | Filter by namespace |
| `assistant_id` | string | Filter by assistant |
| `status` | string | `active` or `closed` |

**Example - List active rooms for a user:**
```bash
curl "https://core.interactor.com/api/v1/agents/rooms?namespace=user_123&status=active" \
  -H "Authorization: Bearer <token>"
```

### Get Room

```bash
curl https://core.interactor.com/api/v1/agents/rooms/room_xyz \
  -H "Authorization: Bearer <token>"
```

**Response includes conversation history:**
```json
{
  "data": {
    "id": "room_xyz",
    "assistant_id": "asst_abc",
    "status": "active",
    "metadata": {...},
    "message_count": 5,
    "created_at": "2026-01-20T12:00:00Z",
    "last_message_at": "2026-01-20T12:05:00Z"
  }
}
```

### Close Room

```bash
curl -X POST https://core.interactor.com/api/v1/agents/rooms/room_xyz/close \
  -H "Authorization: Bearer <token>"
```

---

## Messages

### Send a Message

```bash
curl -X POST https://core.interactor.com/api/v1/agents/rooms/room_xyz/messages \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "How do I update my billing information?",
    "role": "user"
  }'
```

**Response:**
```json
{
  "data": {
    "id": "msg_123",
    "role": "user",
    "content": "How do I update my billing information?",
    "created_at": "2026-01-20T12:00:00Z"
  }
}
```

The assistant's response is generated asynchronously. Use streaming or webhooks to receive it.

### List Messages

```bash
curl https://core.interactor.com/api/v1/agents/rooms/room_xyz/messages \
  -H "Authorization: Bearer <token>"
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | integer | Max messages to return (default: 50, max: 100) |
| `cursor` | string | Opaque cursor for pagination (from `next_cursor`) |
| `order` | string | Sort order: `asc` (oldest first) or `desc` (newest first, default) |

**Response:**
```json
{
  "data": {
    "messages": [
      {
        "id": "msg_123",
        "role": "user",
        "content": "How do I update my billing information?",
        "created_at": "2026-01-20T12:00:00Z"
      },
      {
        "id": "msg_124",
        "role": "assistant",
        "content": "To update your billing information, go to Settings > Billing...",
        "tool_calls": [],
        "created_at": "2026-01-20T12:00:05Z"
      }
    ],
    "has_more": true,
    "next_cursor": "eyJpZCI6Im1zZ18xMjQiLCJ0cyI6MTcwNTc1MjQwNX0="
  }
}
```

### Pagination Pattern

The API uses **cursor-based pagination** for stable, consistent results:

```typescript
// Fetch all messages in a room
async function getAllMessages(roomId: string): Promise<Message[]> {
  const allMessages: Message[] = [];
  let cursor: string | undefined;

  do {
    const params = new URLSearchParams({ limit: '100' });
    if (cursor) params.set('cursor', cursor);

    const response = await fetch(
      `https://core.interactor.com/api/v1/agents/rooms/${roomId}/messages?${params}`,
      { headers: { 'Authorization': `Bearer ${token}` } }
    );

    const { data } = await response.json();
    allMessages.push(...data.messages);
    cursor = data.has_more ? data.next_cursor : undefined;

  } while (cursor);

  return allMessages;
}
```

**Pagination Best Practices:**
- Always use `next_cursor` from the response; never construct cursors manually
- Cursors are opaque and may change format between API versions
- Cursors expire after 24 hours; for long-running jobs, re-fetch from the beginning
- Results are stable within a cursor session (new messages won't appear mid-pagination)

### Message Roles

| Role | Description |
|------|-------------|
| `user` | Message from the user |
| `assistant` | Response from the AI assistant |
| `system` | System message (internal use) |
| `tool` | Tool execution result |

### Real-Time Responses

Assistant responses are generated asynchronously after you send a user message. To receive responses in real-time, you have three options:

> **API Note**: Verify streaming endpoint availability with your Interactor version.
> The SSE endpoint pattern shown below (`/rooms/{id}/stream`) is a common convention
> but may differ in your deployment. Check your API documentation or contact support.

**Option 1: Server-Sent Events (SSE)**

Subscribe to room events for streaming tokens as they're generated.

> **Note**: The standard browser `EventSource` API doesn't support custom headers.
> Use the `eventsource` npm package for Node.js, or pass the token as a query parameter
> if your API supports it.

**Node.js with `eventsource` package:**
```typescript
import EventSource from 'eventsource';

// Node.js: Use eventsource package which supports headers
const eventSource = new EventSource(
  `https://core.interactor.com/api/v1/agents/rooms/${roomId}/stream`,
  { headers: { 'Authorization': `Bearer ${token}` } }
);

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);

  if (data.type === 'token') {
    // Append token to response
    process.stdout.write(data.token);
  } else if (data.type === 'message_complete') {
    // Full message available
    console.log('\nComplete:', data.message);
  } else if (data.type === 'tool_call') {
    // Tool is being invoked
    console.log('Tool call:', data.tool_name);
  }
};

eventSource.onerror = (error) => {
  console.error('Stream error:', error);
  eventSource.close();
};
```

**Browser with Fetch API (alternative):**
```typescript
// Browser: Use fetch with ReadableStream for SSE with auth
async function streamMessages(roomId: string, token: string) {
  const response = await fetch(
    `https://core.interactor.com/api/v1/agents/rooms/${roomId}/stream`,
    { headers: { 'Authorization': `Bearer ${token}` } }
  );

  const reader = response.body?.getReader();
  const decoder = new TextDecoder();

  while (reader) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    // Parse SSE format: "data: {...}\n\n"
    const lines = chunk.split('\n');
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = JSON.parse(line.slice(6));
        console.log('Received:', data);
      }
    }
  }
}
```

**Option 2: Webhooks**

Configure a webhook to receive `agent.room.message` events at your endpoint. See the `interactor-webhooks` skill for complete webhook setup and payload handling.

**Option 3: Polling (Not Recommended)**

Poll the messages endpoint for new messages. Use only as a fallback:

```typescript
async function pollForResponse(roomId: string, lastKnownMessageId: string) {
  const maxAttempts = 30;
  const delayMs = 1000;

  for (let i = 0; i < maxAttempts; i++) {
    // Fetch recent messages and check for new assistant response
    const { messages } = await getMessages(roomId, { limit: 10 });
    const newMessages = messages.filter(m =>
      m.role === 'assistant' && m.id !== lastKnownMessageId
    );

    if (newMessages.length > 0) return newMessages[0];
    await new Promise(resolve => setTimeout(resolve, delayMs));
  }

  throw new Error('Response timeout');
}
```

---

## Tools

Tools are custom functions that assistants can invoke during conversations.

### Register a Tool

```bash
curl -X POST https://core.interactor.com/api/v1/tools \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "search_products",
    "description": "Search the product catalog by query and optional category",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "Search query for product names or descriptions"
        },
        "category": {
          "type": "string",
          "description": "Product category to filter by",
          "enum": ["electronics", "clothing", "home", "sports"]
        },
        "max_results": {
          "type": "integer",
          "description": "Maximum number of results to return",
          "default": 10
        }
      },
      "required": ["query"]
    },
    "callback_url": "https://yourapp.com/api/tools/search_products",
    "callback_secret": "your_webhook_secret_here"
  }'
```

**Response:**
```json
{
  "data": {
    "id": "tool_abc",
    "name": "search_products",
    "description": "Search the product catalog by query and optional category",
    "created_at": "2026-01-20T12:00:00Z"
  }
}
```

### Tool Callback

When the assistant invokes your tool, Interactor POSTs to your `callback_url`:

**Request Headers:**
```
POST /api/tools/search_products HTTP/1.1
Content-Type: application/json
X-Interactor-Signature: sha256=abc123def456...
X-Interactor-Timestamp: 2026-01-20T12:00:00Z
```

**Request Body:**
```json
{
  "tool_name": "search_products",
  "parameters": {
    "query": "laptop",
    "category": "electronics",
    "max_results": 5
  },
  "execution_id": "exec_xyz",
  "room_id": "room_xyz",
  "assistant_id": "asst_abc",
  "timestamp": "2026-01-20T12:00:00Z"
}
```

> **Security Note**: The `X-Interactor-Signature` header contains an HMAC-SHA256 signature
> of the raw request body, signed with your `callback_secret`. Always verify this signature
> before processing the request.

**Your response:**
```json
{
  "result": {
    "products": [
      {
        "id": "prod_1",
        "name": "MacBook Pro 14\"",
        "price": 1999,
        "in_stock": true
      },
      {
        "id": "prod_2",
        "name": "Dell XPS 15",
        "price": 1499,
        "in_stock": true
      }
    ],
    "total_count": 2
  }
}
```

The assistant will use this result to formulate its response.

### Verify Tool Callback Signature

Tool callbacks include three security headers for verification:

| Header | Description |
|--------|-------------|
| `X-Interactor-Signature` | HMAC-SHA256 signature of the raw request body |
| `X-Interactor-Timestamp` | ISO 8601 timestamp when request was signed |
| `X-Interactor-Request-Id` | Unique request ID (same as `execution_id` in body) |

**Security Requirements:**
1. Verify HMAC signature matches
2. Check timestamp is within acceptable window (recommended: 300 seconds)
3. Use `execution_id` as idempotency key to prevent replay attacks

**TypeScript (with replay protection):**
```typescript
import crypto from 'crypto';

interface VerificationResult {
  valid: boolean;
  error?: string;
}

function verifyToolCallback(
  payload: string,
  signature: string,
  timestamp: string,
  secret: string,
  maxAgeSeconds: number = 300
): VerificationResult {
  // 1. Check timestamp is not too old (replay protection)
  const requestTime = Date.parse(timestamp);
  const now = Date.now();
  const ageSeconds = Math.abs(now - requestTime) / 1000;

  if (ageSeconds > maxAgeSeconds) {
    return { valid: false, error: `Request too old: ${ageSeconds}s > ${maxAgeSeconds}s` };
  }

  // 2. Verify HMAC signature
  const expected = crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex');

  const signatureValid = crypto.timingSafeEqual(
    Buffer.from(signature.replace('sha256=', '')),
    Buffer.from(expected)
  );

  if (!signatureValid) {
    return { valid: false, error: 'Invalid signature' };
  }

  return { valid: true };
}

// Express middleware with full security
app.post('/api/tools/search_products', express.raw({ type: 'application/json' }), async (req, res) => {
  const signature = req.headers['x-interactor-signature'] as string;
  const timestamp = req.headers['x-interactor-timestamp'] as string;
  const requestId = req.headers['x-interactor-request-id'] as string;
  const payload = req.body.toString();

  // Verify signature and timestamp
  const verification = verifyToolCallback(
    payload,
    signature,
    timestamp,
    process.env.TOOL_CALLBACK_SECRET!
  );

  if (!verification.valid) {
    console.error('Callback verification failed:', verification.error, { requestId });
    return res.status(401).json({ error: verification.error });
  }

  const data = JSON.parse(payload);

  // 3. Idempotency check - prevent duplicate processing
  const alreadyProcessed = await checkIdempotency(data.execution_id);
  if (alreadyProcessed) {
    console.log('Duplicate request ignored:', data.execution_id);
    return res.status(200).json({ result: await getCachedResult(data.execution_id) });
  }

  // Execute your tool logic
  const result = await searchProducts(data.parameters);

  // Store result for idempotency (retain for 7 days)
  await storeIdempotencyResult(data.execution_id, result, 7 * 24 * 60 * 60);

  res.json({ result });
});

// Idempotency helpers (implement with Redis, database, etc.)
async function checkIdempotency(executionId: string): Promise<boolean> {
  // Check if execution_id was already processed
  return false; // Implement with your storage
}

async function getCachedResult(executionId: string): Promise<any> {
  // Return cached result for duplicate request
  return null; // Implement with your storage
}

async function storeIdempotencyResult(executionId: string, result: any, ttlSeconds: number): Promise<void> {
  // Store result keyed by execution_id
  // Implement with your storage
}
```

**Python (with replay protection):**
```python
import os
import hmac
import hashlib
import time
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

def verify_tool_callback(
    payload: bytes,
    signature: str,
    timestamp: str,
    secret: str,
    max_age_seconds: int = 300
) -> tuple[bool, str | None]:
    """
    Verify callback with replay protection.
    Returns (is_valid, error_message).
    """
    # 1. Check timestamp is not too old
    try:
        request_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        age_seconds = abs((datetime.now(request_time.tzinfo) - request_time).total_seconds())

        if age_seconds > max_age_seconds:
            return False, f'Request too old: {age_seconds}s > {max_age_seconds}s'
    except ValueError as e:
        return False, f'Invalid timestamp: {e}'

    # 2. Verify HMAC signature
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    signature_value = signature.replace('sha256=', '')
    if not hmac.compare_digest(signature_value, expected):
        return False, 'Invalid signature'

    return True, None

@app.route('/api/tools/search_products', methods=['POST'])
def handle_tool_callback():
    signature = request.headers.get('X-Interactor-Signature', '')
    timestamp = request.headers.get('X-Interactor-Timestamp', '')
    request_id = request.headers.get('X-Interactor-Request-Id', '')
    payload = request.get_data()

    # Verify signature and timestamp
    is_valid, error = verify_tool_callback(
        payload,
        signature,
        timestamp,
        os.environ['TOOL_CALLBACK_SECRET']
    )

    if not is_valid:
        app.logger.error(f'Callback verification failed: {error}', extra={'request_id': request_id})
        return jsonify({'error': error}), 401

    data = request.get_json()

    # Idempotency check
    if is_duplicate_execution(data['execution_id']):
        return jsonify({'result': get_cached_result(data['execution_id'])}), 200

    # Execute your tool logic
    result = search_products(data['parameters'])

    # Store for idempotency
    store_execution_result(data['execution_id'], result)

    return jsonify({'result': result})
```

### List Tools

```bash
curl https://core.interactor.com/api/v1/tools \
  -H "Authorization: Bearer <token>"
```

### Get Tool

```bash
curl https://core.interactor.com/api/v1/tools/tool_abc \
  -H "Authorization: Bearer <token>"
```

### Update Tool

```bash
curl -X PUT https://core.interactor.com/api/v1/tools/tool_abc \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Updated description with more detail",
    "callback_url": "https://yourapp.com/api/v2/tools/search_products"
  }'
```

### Delete Tool

```bash
curl -X DELETE https://core.interactor.com/api/v1/tools/tool_abc \
  -H "Authorization: Bearer <token>"
```

---

## Webhook & Callback Contract

This section defines the canonical contract for all Interactor webhooks and tool callbacks.

### Request Headers

All webhook/callback requests include these headers:

| Header | Format | Description |
|--------|--------|-------------|
| `X-Interactor-Signature` | `sha256=<hex>` | HMAC-SHA256 of raw body |
| `X-Interactor-Timestamp` | ISO 8601 | When request was signed |
| `X-Interactor-Request-Id` | `exec_<id>` | Unique request identifier |
| `Content-Type` | `application/json` | Always JSON |

### Response Requirements

| Status | Meaning | Interactor Behavior |
|--------|---------|---------------------|
| `200` | Success | Process result, no retry |
| `201` | Created | Same as 200 |
| `202` | Accepted | Async processing (see below) |
| `400` | Bad Request | Permanent failure, no retry |
| `401` | Unauthorized | Permanent failure, no retry |
| `404` | Not Found | Permanent failure, no retry |
| `429` | Rate Limited | Retry with backoff |
| `500` | Server Error | Retry with backoff |
| `502-504` | Gateway Error | Retry with backoff |

**Expected Response Format:**
```json
{
  "result": { ... }
}
```

### Timeout Policy

| Operation | Timeout | Behavior on Timeout |
|-----------|---------|---------------------|
| Tool callback | 30 seconds | Retry with backoff |
| Webhook delivery | 10 seconds | Retry with backoff |
| Async callback (202) | 5 minutes | Poll for completion |

> **Important**: Your callback must respond within the timeout window. For long-running
> operations, return `202 Accepted` with a status URL, and Interactor will poll for completion.

### Retry Policy

When a callback fails (5xx, timeout, network error), Interactor retries with exponential backoff:

| Attempt | Delay | Cumulative Time |
|---------|-------|-----------------|
| 1 | Immediate | 0s |
| 2 | 1s | 1s |
| 3 | 2s | 3s |
| 4 | 4s | 7s |
| 5 | 8s | 15s |
| 6 (final) | 16s | 31s |

**After 6 failed attempts:**
- Request is marked as permanently failed
- `tool.callback.failed` event is emitted (if webhooks configured)
- Assistant receives an error and may retry or inform the user

### Idempotency Requirements

**You MUST implement idempotent handlers.** Use `execution_id` as the idempotency key.

**Idempotency Implementation:**

```typescript
// Redis-based idempotency example
import Redis from 'ioredis';
const redis = new Redis();

const IDEMPOTENCY_TTL = 7 * 24 * 60 * 60; // 7 days

async function handleWithIdempotency(
  executionId: string,
  handler: () => Promise<any>
): Promise<{ result: any; isDuplicate: boolean }> {
  const cacheKey = `idempotency:${executionId}`;

  // Check for existing result
  const cached = await redis.get(cacheKey);
  if (cached) {
    return { result: JSON.parse(cached), isDuplicate: true };
  }

  // Execute handler
  const result = await handler();

  // Store result with TTL
  await redis.setex(cacheKey, IDEMPOTENCY_TTL, JSON.stringify(result));

  return { result, isDuplicate: false };
}
```

**Recommended idempotency window:** 7 days minimum. This covers retry scenarios and
delayed processing.

### Dead Letter Handling

If all retries are exhausted:

1. Interactor emits a `tool.callback.dead_letter` event (if webhooks configured)
2. The failed request is logged in your Interactor dashboard
3. You can manually retry from the dashboard or via API

**Dead Letter Event Payload:**
```json
{
  "event": "tool.callback.dead_letter",
  "data": {
    "execution_id": "exec_xyz",
    "tool_name": "search_products",
    "assistant_id": "asst_abc",
    "room_id": "room_xyz",
    "attempts": 6,
    "last_error": "Connection timeout",
    "first_attempt_at": "2026-01-20T12:00:00Z",
    "last_attempt_at": "2026-01-20T12:00:31Z"
  }
}
```

---

## Streaming Contract

This section defines the canonical contract for Server-Sent Events (SSE) streaming.

### Event Types

The streaming endpoint emits these event types:

| Event Type | Description | When Emitted |
|------------|-------------|--------------|
| `token` | Incremental response token | During response generation |
| `message_complete` | Full message available | When response finishes |
| `tool_call` | Tool is being invoked | When assistant calls a tool |
| `tool_result` | Tool execution completed | After tool callback returns |
| `error` | Error occurred | On any error |
| `done` | Stream complete | End of stream |

### Event Schemas

**`token` Event:**
```json
{
  "type": "token",
  "token": "Hello",
  "index": 0,
  "message_id": "msg_123"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Always `"token"` |
| `token` | string | The text token (1-4 characters typically) |
| `index` | integer | Token position in the response |
| `message_id` | string | ID of the message being generated |

**`message_complete` Event:**
```json
{
  "type": "message_complete",
  "message": {
    "id": "msg_123",
    "role": "assistant",
    "content": "Hello! How can I help you today?",
    "tool_calls": [],
    "created_at": "2026-01-20T12:00:05Z"
  }
}
```

**`tool_call` Event:**
```json
{
  "type": "tool_call",
  "tool_call": {
    "id": "tc_456",
    "tool_name": "search_products",
    "parameters": {
      "query": "laptop"
    },
    "status": "pending"
  },
  "message_id": "msg_123"
}
```

**`tool_result` Event:**
```json
{
  "type": "tool_result",
  "tool_call": {
    "id": "tc_456",
    "tool_name": "search_products",
    "status": "completed",
    "result": {
      "products": [...]
    }
  },
  "message_id": "msg_123"
}
```

**`error` Event:**
```json
{
  "type": "error",
  "error": {
    "code": "tool_callback_failed",
    "message": "Tool callback timed out",
    "tool_call_id": "tc_456"
  },
  "message_id": "msg_123"
}
```

**`done` Event:**
```json
{
  "type": "done",
  "message_id": "msg_123"
}
```

### SSE Wire Format

Events follow the standard SSE format:

```
event: token
data: {"type":"token","token":"Hello","index":0,"message_id":"msg_123"}

event: token
data: {"type":"token","token":" world","index":1,"message_id":"msg_123"}

event: message_complete
data: {"type":"message_complete","message":{...}}

event: done
data: {"type":"done","message_id":"msg_123"}

```

**Important**: Each event has an `event:` line followed by a `data:` line, then a blank line.

### Authentication for Streaming

The standard browser `EventSource` API does not support custom headers. Use one of these approaches:

**Option 1: Short-Lived Token in Query Parameter (Recommended for Browsers)**

```typescript
// 1. Get a short-lived streaming token (valid 60 seconds)
const { streaming_token } = await fetch('/api/v1/agents/rooms/{room_id}/stream-token', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${accessToken}` }
}).then(r => r.json());

// 2. Connect with token in query string
const eventSource = new EventSource(
  `https://core.interactor.com/api/v1/agents/rooms/${roomId}/stream?token=${streaming_token}`
);
```

**Option 2: Fetch API with ReadableStream**

```typescript
async function streamWithAuth(roomId: string, accessToken: string) {
  const response = await fetch(
    `https://core.interactor.com/api/v1/agents/rooms/${roomId}/stream`,
    {
      headers: { 'Authorization': `Bearer ${accessToken}` }
    }
  );

  const reader = response.body?.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  while (reader) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });

    // Parse complete events from buffer
    const events = buffer.split('\n\n');
    buffer = events.pop() || ''; // Keep incomplete event in buffer

    for (const eventBlock of events) {
      if (!eventBlock.trim()) continue;

      const lines = eventBlock.split('\n');
      let eventType = 'message';
      let data = '';

      for (const line of lines) {
        if (line.startsWith('event: ')) {
          eventType = line.slice(7);
        } else if (line.startsWith('data: ')) {
          data = line.slice(6);
        }
      }

      if (data) {
        const parsed = JSON.parse(data);
        handleStreamEvent(eventType, parsed);
      }
    }
  }
}

function handleStreamEvent(eventType: string, data: any) {
  switch (data.type) {
    case 'token':
      process.stdout.write(data.token);
      break;
    case 'message_complete':
      console.log('\n[Complete]', data.message.content);
      break;
    case 'tool_call':
      console.log('[Tool]', data.tool_call.tool_name);
      break;
    case 'error':
      console.error('[Error]', data.error.message);
      break;
    case 'done':
      console.log('[Stream ended]');
      break;
  }
}
```

**Option 3: Node.js with `eventsource` Package**

```typescript
import EventSource from 'eventsource';

const eventSource = new EventSource(
  `https://core.interactor.com/api/v1/agents/rooms/${roomId}/stream`,
  { headers: { 'Authorization': `Bearer ${accessToken}` } }
);

eventSource.addEventListener('token', (e) => {
  const data = JSON.parse(e.data);
  process.stdout.write(data.token);
});

eventSource.addEventListener('error', (e) => {
  console.error('Stream error:', e);
  eventSource.close();
});
```

### Reconnection Handling

If the stream disconnects, reconnect with a `Last-Event-ID` header (if supported):

```typescript
let lastEventId: string | null = null;

eventSource.onmessage = (e) => {
  lastEventId = e.lastEventId;
  // ... handle event
};

eventSource.onerror = () => {
  eventSource.close();

  // Reconnect after delay
  setTimeout(() => {
    const newSource = new EventSource(
      `${streamUrl}?last_event_id=${lastEventId}`,
      { headers: { 'Authorization': `Bearer ${token}` } }
    );
    // ... set up handlers
  }, 1000);
};
```

---

## Data Sources

Connect databases and APIs that assistants can query directly using natural language.

### Register a Data Source

```bash
curl -X POST https://core.interactor.com/api/v1/data-sources \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "sales_database",
    "type": "postgresql",
    "connection": {
      "host": "db.yourcompany.com",
      "port": 5432,
      "database": "sales",
      "username": "readonly_user",
      "password": "secure_password"
    },
    "description": "Sales and customer data including orders, products, and customer information"
  }'
```

**Response:**
```json
{
  "data": {
    "id": "ds_abc",
    "name": "sales_database",
    "type": "postgresql",
    "status": "connected",
    "schema_status": "extracting",
    "created_at": "2026-01-20T12:00:00Z"
  }
}
```

Interactor automatically extracts the database schema for the assistant to understand.

### Supported Data Source Types

| Type | Description |
|------|-------------|
| `postgresql` | PostgreSQL database |
| `mysql` | MySQL database |
| `mssql` | Microsoft SQL Server |
| `mongodb` | MongoDB database |
| `rest_api` | REST API endpoint |

### List Data Sources

```bash
curl https://core.interactor.com/api/v1/data-sources \
  -H "Authorization: Bearer <token>"
```

### Get Data Source

```bash
curl https://core.interactor.com/api/v1/data-sources/ds_abc \
  -H "Authorization: Bearer <token>"
```

**Response includes schema information:**
```json
{
  "data": {
    "id": "ds_abc",
    "name": "sales_database",
    "type": "postgresql",
    "status": "connected",
    "schema_status": "ready",
    "tables": [
      {
        "name": "customers",
        "columns": [
          {"name": "id", "type": "uuid", "nullable": false},
          {"name": "email", "type": "varchar", "nullable": false},
          {"name": "name", "type": "varchar", "nullable": true},
          {"name": "created_at", "type": "timestamp", "nullable": false}
        ]
      },
      {
        "name": "orders",
        "columns": [...]
      }
    ]
  }
}
```

### Update Data Source

```bash
curl -X PUT https://core.interactor.com/api/v1/data-sources/ds_abc \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Updated description with more context"
  }'
```

### Delete Data Source

```bash
curl -X DELETE https://core.interactor.com/api/v1/data-sources/ds_abc \
  -H "Authorization: Bearer <token>"
```

### Refresh Schema

Re-extract the schema if your database structure changed:

```bash
curl -X POST https://core.interactor.com/api/v1/data-sources/ds_abc/refresh-schema \
  -H "Authorization: Bearer <token>"
```

### Execute Query

Run a query directly against the data source:

```bash
curl -X POST https://core.interactor.com/api/v1/data-sources/ds_abc/query \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "SELECT * FROM customers WHERE created_at > $1 LIMIT 10",
    "parameters": ["2026-01-01"]
  }'
```

**Response:**
```json
{
  "data": {
    "columns": ["id", "email", "name", "created_at"],
    "rows": [
      ["uuid-1", "john@example.com", "John Doe", "2026-01-15T10:00:00Z"],
      ["uuid-2", "jane@example.com", "Jane Smith", "2026-01-16T11:00:00Z"]
    ],
    "row_count": 2,
    "execution_time_ms": 45
  }
}
```

### Semantic Mappings

Add synonyms and descriptions to help the assistant understand your schema better:

```bash
curl -X PATCH https://core.interactor.com/api/v1/data-sources/ds_abc/semantic-mappings \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "mappings": {
      "customers": {
        "description": "Customer accounts and profiles",
        "synonyms": ["users", "clients", "accounts", "members"]
      },
      "customers.created_at": {
        "description": "When the customer signed up",
        "synonyms": ["signup date", "registration date", "joined date"]
      },
      "orders": {
        "description": "Customer purchase orders",
        "synonyms": ["purchases", "transactions", "sales"]
      },
      "orders.total_amount": {
        "description": "Total order value in USD",
        "synonyms": ["order total", "purchase amount", "sale value"]
      }
    }
  }'
```

This helps the assistant translate natural language questions like:
- "How many users signed up last month?" → `SELECT COUNT(*) FROM customers WHERE created_at >= '2026-01-01'`
- "What's the total sales this week?" → `SELECT SUM(total_amount) FROM orders WHERE created_at >= '2026-01-14'`

---

## Knowledge Base Search

Search for external services that assistants can connect to:

### Search Services

```bash
curl -X POST https://core.interactor.com/api/v1/knowledge-base/services/search \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "calendar scheduling",
    "limit": 5
  }'
```

**Response:**
```json
{
  "data": {
    "services": [
      {
        "id": "google_calendar",
        "name": "Google Calendar",
        "description": "Calendar and scheduling service",
        "auth_type": "oauth2",
        "capabilities": ["create_event", "list_events", "update_event", "delete_event"]
      },
      {
        "id": "microsoft_calendar",
        "name": "Microsoft Outlook Calendar",
        "description": "Microsoft 365 calendar service",
        "auth_type": "oauth2",
        "capabilities": ["create_event", "list_events", "update_event"]
      }
    ]
  }
}
```

### Lookup Service

```bash
curl -X POST https://core.interactor.com/api/v1/knowledge-base/services/lookup \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"service_id": "google_calendar"}'
```

### Get Service Details

```bash
curl https://core.interactor.com/api/v1/knowledge-base/services/google_calendar \
  -H "Authorization: Bearer <token>"
```

### Get Service OAuth Config

```bash
curl https://core.interactor.com/api/v1/knowledge-base/services/google_calendar/oauth \
  -H "Authorization: Bearer <token>"
```

---

## Complete Implementation Example

### TypeScript Implementation

```typescript
import { InteractorClient } from './interactor-client';

export class AgentManager {
  private client: InteractorClient;

  constructor(client: InteractorClient) {
    this.client = client;
  }

  // ============ Assistants ============

  async createAssistant(config: {
    name: string;
    title: string;
    description?: string;
    instructions: string;
    modelConfig?: {
      provider?: 'openai';
      model?: string;
      temperature?: number;
    };
    enabledTools?: string[];
  }): Promise<Assistant> {
    return this.client.request('POST', '/agents/assistants', {
      name: config.name,
      title: config.title,
      description: config.description,
      instructions: config.instructions,
      model_config: config.modelConfig,
      enabled_tools: config.enabledTools
    });
  }

  async listAssistants(): Promise<Assistant[]> {
    const result = await this.client.request<{ assistants: Assistant[] }>(
      'GET',
      '/agents/assistants'
    );
    return result.assistants;
  }

  async getAssistant(id: string): Promise<Assistant> {
    return this.client.request('GET', `/agents/assistants/${id}`);
  }

  async updateAssistant(id: string, updates: Partial<AssistantConfig>): Promise<Assistant> {
    return this.client.request('PUT', `/agents/assistants/${id}`, updates);
  }

  async deleteAssistant(id: string): Promise<void> {
    await this.client.request('DELETE', `/agents/assistants/${id}`);
  }

  // ============ Rooms ============

  async createRoom(
    assistantId: string,
    userId: string,
    metadata?: Record<string, any>
  ): Promise<Room> {
    return this.client.request('POST', `/agents/${assistantId}/rooms`, {
      namespace: `user_${userId}`,
      metadata
    });
  }

  async listRooms(filters?: {
    userId?: string;
    assistantId?: string;
    status?: 'active' | 'closed';
  }): Promise<Room[]> {
    const params = new URLSearchParams();
    if (filters?.userId) params.set('namespace', `user_${filters.userId}`);
    if (filters?.assistantId) params.set('assistant_id', filters.assistantId);
    if (filters?.status) params.set('status', filters.status);

    const query = params.toString();
    const result = await this.client.request<{ rooms: Room[] }>(
      'GET',
      `/agents/rooms${query ? '?' + query : ''}`
    );
    return result.rooms;
  }

  async getRoom(roomId: string): Promise<Room> {
    return this.client.request('GET', `/agents/rooms/${roomId}`);
  }

  async closeRoom(roomId: string): Promise<void> {
    await this.client.request('POST', `/agents/rooms/${roomId}/close`);
  }

  // ============ Messages ============

  async sendMessage(roomId: string, content: string): Promise<Message> {
    return this.client.request('POST', `/agents/rooms/${roomId}/messages`, {
      content,
      role: 'user'
    });
  }

  async getMessages(roomId: string, options?: {
    limit?: number;
    before?: string;
  }): Promise<{ messages: Message[]; has_more: boolean }> {
    const params = new URLSearchParams();
    if (options?.limit) params.set('limit', options.limit.toString());
    if (options?.before) params.set('before', options.before);

    const query = params.toString();
    return this.client.request(
      'GET',
      `/agents/rooms/${roomId}/messages${query ? '?' + query : ''}`
    );
  }

  // ============ Tools ============

  async registerTool(tool: {
    name: string;
    description: string;
    parameters: Record<string, any>;
    callbackUrl: string;
    callbackSecret: string;
  }): Promise<Tool> {
    return this.client.request('POST', '/tools', {
      name: tool.name,
      description: tool.description,
      parameters: tool.parameters,
      callback_url: tool.callbackUrl,
      callback_secret: tool.callbackSecret
    });
  }

  async listTools(): Promise<Tool[]> {
    const result = await this.client.request<{ tools: Tool[] }>('GET', '/tools');
    return result.tools;
  }

  async deleteTool(id: string): Promise<void> {
    await this.client.request('DELETE', `/tools/${id}`);
  }

  // ============ Data Sources ============

  async registerDataSource(config: {
    name: string;
    type: 'postgresql' | 'mysql' | 'mssql' | 'mongodb' | 'rest_api';
    connection: Record<string, any>;
    description?: string;
  }): Promise<DataSource> {
    return this.client.request('POST', '/data-sources', config);
  }

  async listDataSources(): Promise<DataSource[]> {
    const result = await this.client.request<{ data_sources: DataSource[] }>(
      'GET',
      '/data-sources'
    );
    return result.data_sources;
  }

  async getDataSource(id: string): Promise<DataSource> {
    return this.client.request('GET', `/data-sources/${id}`);
  }

  async refreshSchema(id: string): Promise<void> {
    await this.client.request('POST', `/data-sources/${id}/refresh-schema`);
  }

  async executeQuery(
    id: string,
    query: string,
    parameters?: any[]
  ): Promise<QueryResult> {
    return this.client.request('POST', `/data-sources/${id}/query`, {
      query,
      parameters
    });
  }

  async updateSemanticMappings(
    id: string,
    mappings: Record<string, { description?: string; synonyms?: string[] }>
  ): Promise<void> {
    await this.client.request('PATCH', `/data-sources/${id}/semantic-mappings`, {
      mappings
    });
  }
}

// Types
interface Assistant {
  id: string;
  name: string;
  title: string;
  description?: string;
  model_config: {
    provider: string;
    model: string;
    temperature: number;
  };
  enabled_tools: string[];
  created_at: string;
}

interface AssistantConfig {
  title?: string;
  description?: string;
  instructions?: string;
  model_config?: {
    provider?: string;
    model?: string;
    temperature?: number;
  };
  enabled_tools?: string[];
}

interface Room {
  id: string;
  assistant_id: string;
  namespace: string;
  status: 'active' | 'closed';
  metadata?: Record<string, any>;
  message_count: number;
  created_at: string;
  last_message_at?: string;
}

interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system' | 'tool';
  content: string;
  tool_calls?: ToolCall[];
  created_at: string;
}

interface ToolCall {
  id: string;
  tool_name: string;
  parameters: Record<string, any>;
  result?: any;
}

interface Tool {
  id: string;
  name: string;
  description: string;
  parameters: Record<string, any>;
  callback_url: string;
  created_at: string;
}

interface DataSource {
  id: string;
  name: string;
  type: string;
  status: 'connected' | 'disconnected' | 'error';
  schema_status: 'extracting' | 'ready' | 'error';
  tables?: TableSchema[];
  created_at: string;
}

interface TableSchema {
  name: string;
  columns: ColumnSchema[];
}

interface ColumnSchema {
  name: string;
  type: string;
  nullable: boolean;
}

interface QueryResult {
  columns: string[];
  rows: any[][];
  row_count: number;
  execution_time_ms: number;
}
```

### Chat Interface Example

```typescript
// Example: Building a chat interface
async function chat(userId: string, assistantId: string) {
  const agentManager = new AgentManager(interactorClient);

  // Get or create a room for this user
  let rooms = await agentManager.listRooms({
    userId,
    assistantId,
    status: 'active'
  });

  let room: Room;
  if (rooms.length > 0) {
    room = rooms[0];
  } else {
    room = await agentManager.createRoom(assistantId, userId, {
      user_name: 'John',
      context: 'general_support'
    });
  }

  // Send a message
  await agentManager.sendMessage(room.id, 'How do I reset my password?');

  // Wait for response (in real app, use streaming)
  await new Promise(resolve => setTimeout(resolve, 3000));

  // Get messages
  const { messages } = await agentManager.getMessages(room.id);

  // Display conversation
  for (const msg of messages) {
    console.log(`${msg.role}: ${msg.content}`);
  }
}
```

---

## Webhook Events

Subscribe to agent events for real-time updates:

| Event | Description |
|-------|-------------|
| `agent.room.message` | New message in a room |
| `agent.room.closed` | Room was closed |

> **Note**: Additional events like `agent.tool.invoked` may be available depending on
> your Interactor version. Check the `interactor-webhooks` skill or your API documentation
> for the complete list of available events.

See `interactor-webhooks` skill for webhook setup and SSE streaming.

---

## Best Practices

### DO

- **Keep instructions focused** - Clear, specific instructions produce better results
- **Use semantic mappings** - Help assistants understand your data schema
- **Secure tool callbacks** - Always verify signatures on tool callbacks
- **Use read-only database users** - Limit data source connections to read-only access
- **Monitor tool usage** - Track which tools are being called and their success rates
- **Test conversations** - Verify assistant behavior before deploying to users
- **Use metadata** - Pass user context (name, plan, etc.) to personalize responses

### DON'T

- **Don't expose sensitive data** - Be careful what tools can access
- **Don't use write access** - Keep data sources read-only
- **Don't skip signature verification** - Always verify tool callback signatures
- **Don't overload with tools** - Only enable tools the assistant actually needs
- **Don't use vague instructions** - Specific instructions produce better results

---

## Error Handling

### Agent-Specific Errors

Common error patterns you may encounter:

| Error Code | HTTP Status | Description | Resolution |
|------------|-------------|-------------|------------|
| `assistant_not_found` | 404 | Assistant doesn't exist | Check assistant ID |
| `room_not_found` | 404 | Room doesn't exist | Check room ID |
| `room_closed` | 400 | Room is already closed | Create a new room |
| `tool_not_found` | 404 | Tool doesn't exist | Check tool ID |
| `tool_callback_failed` | 500 | Tool callback returned error | Check your callback endpoint |
| `data_source_disconnected` | 400 | Database connection failed | Check connection settings |
| `query_execution_failed` | 400 | SQL query failed | Check query syntax |

> **Note**: Error codes and formats may vary. Always check the response body for
> detailed error messages. Standard HTTP status codes apply (4xx for client errors,
> 5xx for server errors).

---

## Rate Limiting

The AI Agents API uses rate limiting to ensure fair usage and system stability.

### Rate Limit Headers

Every API response includes these headers:

| Header | Type | Description |
|--------|------|-------------|
| `X-RateLimit-Limit` | integer | Max requests allowed in window |
| `X-RateLimit-Remaining` | integer | Requests remaining in current window |
| `X-RateLimit-Reset` | integer | Unix timestamp (UTC) when window resets |
| `X-RateLimit-Resource` | string | Which limit bucket this applies to |

**Example Response Headers:**
```
HTTP/1.1 200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1705752000
X-RateLimit-Resource: agents:messages
```

### Default Rate Limits

Limits vary by plan. Typical defaults:

| Resource | Free | Pro | Enterprise |
|----------|------|-----|------------|
| Assistants (create) | 10/min | 60/min | 300/min |
| Rooms (create) | 100/min | 600/min | 3000/min |
| Messages (send) | 60/min/room | 300/min/room | 1000/min/room |
| Tool registrations | 20/min | 100/min | 500/min |
| Data source queries | 100/min | 500/min | 2000/min |
| API calls (global) | 1000/min | 10000/min | 100000/min |

> **Check Your Limits**: View your actual limits in the Interactor dashboard under
> Settings → API → Rate Limits, or call `GET /api/v1/account/limits`.

### Rate Limit Response (HTTP 429)

When rate limited:

```http
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1705752000
Retry-After: 30
Content-Type: application/json

{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "Rate limit exceeded for agents:messages",
    "resource": "agents:messages",
    "retry_after": 30
  }
}
```

### Handling Rate Limits

**Implementation with proper header parsing:**

```typescript
interface RateLimitInfo {
  limit: number;
  remaining: number;
  resetAt: Date;
  resource: string;
}

function parseRateLimitHeaders(headers: Headers): RateLimitInfo {
  return {
    limit: parseInt(headers.get('X-RateLimit-Limit') || '0'),
    remaining: parseInt(headers.get('X-RateLimit-Remaining') || '0'),
    resetAt: new Date(parseInt(headers.get('X-RateLimit-Reset') || '0') * 1000),
    resource: headers.get('X-RateLimit-Resource') || 'unknown'
  };
}

async function withRateLimitHandling<T>(
  fn: () => Promise<Response>,
  maxRetries: number = 3
): Promise<T> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    const response = await fn();
    const rateLimit = parseRateLimitHeaders(response.headers);

    // Log rate limit status for monitoring
    console.log(`Rate limit: ${rateLimit.remaining}/${rateLimit.limit} for ${rateLimit.resource}`);

    if (response.ok) {
      return response.json();
    }

    if (response.status === 429) {
      const retryAfter = parseInt(response.headers.get('Retry-After') || '1');
      console.warn(`Rate limited. Waiting ${retryAfter}s before retry ${attempt + 1}/${maxRetries}`);
      await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
      continue;
    }

    // Non-retryable error
    throw new Error(`API error: ${response.status}`);
  }

  throw new Error('Max retries exceeded due to rate limiting');
}

// Proactive rate limit avoidance
async function sendMessageWithBackpressure(roomId: string, content: string): Promise<Message> {
  const response = await fetch(`/api/v1/agents/rooms/${roomId}/messages`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ content, role: 'user' })
  });

  const rateLimit = parseRateLimitHeaders(response.headers);

  // If getting close to limit, slow down proactively
  if (rateLimit.remaining < rateLimit.limit * 0.1) {
    const waitTime = Math.ceil((rateLimit.resetAt.getTime() - Date.now()) / 1000);
    console.warn(`Approaching rate limit. Consider slowing down. Resets in ${waitTime}s`);
  }

  return response.json();
}
```

---

## Troubleshooting

### Common Issues

#### Tool Callback Not Receiving Requests

**Symptoms**: Assistant says it's calling a tool, but your callback endpoint never receives the request.

**Checklist**:
1. ✓ Verify `callback_url` is publicly accessible (not localhost)
2. ✓ Check firewall/security group allows inbound HTTPS
3. ✓ Ensure endpoint returns 200 status within 30 seconds
4. ✓ Verify SSL certificate is valid (no self-signed in production)

**Debug**: Check Interactor dashboard for tool execution logs.

#### Tool Callback Signature Verification Failing

**Symptoms**: All tool callbacks return 401 Unauthorized.

**Checklist**:
1. ✓ Verify `callback_secret` matches what you registered
2. ✓ Ensure you're reading raw request body (not parsed JSON)
3. ✓ Check signature header name: `X-Interactor-Signature`
4. ✓ Verify HMAC algorithm is SHA256

**Debug**:
```typescript
// Log for debugging (remove in production)
console.log('Received signature:', signature);
console.log('Payload:', payload);
console.log('Expected:', `sha256=${crypto.createHmac('sha256', secret).update(payload).digest('hex')}`);
```

#### Data Source Connection Failed

**Symptoms**: Data source status shows "disconnected" or "error".

**Checklist**:
1. ✓ Verify database host is reachable from Interactor's servers
2. ✓ Check credentials are correct
3. ✓ Ensure database user has SELECT permissions
4. ✓ Verify SSL/TLS settings match your database configuration
5. ✓ Check if IP allowlisting is required

**Common Fixes**:
```sql
-- Grant read-only access to Interactor user
GRANT SELECT ON ALL TABLES IN SCHEMA public TO interactor_readonly;
GRANT USAGE ON SCHEMA public TO interactor_readonly;
```

#### Assistant Not Using Tools

**Symptoms**: Assistant responds without using available tools when it should.

**Checklist**:
1. ✓ Verify tool is in `enabled_tools` array for the assistant
2. ✓ Check tool description is clear about when to use it
3. ✓ Ensure instructions mention when to use tools
4. ✓ Verify tool parameters schema is valid JSON Schema

**Fix**: Update assistant instructions to be explicit:
```
"When users ask about products, ALWAYS use the search_products tool to find current information."
```

#### Messages Not Appearing in Room

**Symptoms**: Sent messages don't show up when listing messages.

**Checklist**:
1. ✓ Verify room status is "active" (not "closed")
2. ✓ Check message was acknowledged (201 response)
3. ✓ Ensure you're querying the correct room ID
4. ✓ Wait for async processing (use streaming for real-time)

#### High Latency on Responses

**Symptoms**: Assistant takes a long time to respond.

**Possible Causes**:
1. Tool callbacks taking too long → Optimize your callback endpoints
2. Large context window → Close old rooms, start fresh conversations
3. Complex instructions → Simplify system prompt
4. Data source queries slow → Add indexes, optimize queries

**Monitor**:
```typescript
const start = Date.now();
await sendMessage(roomId, content);
console.log(`Message sent in ${Date.now() - start}ms`);
```

---

## Security & Compliance

### Data Retention

| Data Type | Default Retention | Configurable |
|-----------|-------------------|--------------|
| Messages | 90 days | Yes (30-365 days) |
| Room metadata | Until room deleted | N/A |
| Tool execution logs | 30 days | Yes (7-90 days) |
| Assistant configurations | Indefinite | N/A |

> **Enterprise**: Contact support for custom retention policies and data residency requirements.

Configure retention in your Interactor dashboard under Settings → Data Management → Retention Policies.

### Data Deletion (GDPR/CCPA)

To delete user data for compliance with GDPR "Right to Erasure" or CCPA:

**Delete all rooms for a user:**
```bash
# 1. List all rooms for the user
curl "https://core.interactor.com/api/v1/agents/rooms?namespace=user_123" \
  -H "Authorization: Bearer <token>"

# 2. Delete each room (also deletes messages)
curl -X DELETE "https://core.interactor.com/api/v1/agents/rooms/room_xyz" \
  -H "Authorization: Bearer <token>"
```

**Bulk deletion via API:**
```bash
curl -X POST https://core.interactor.com/api/v1/data/delete-user-data \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "namespace": "user_123",
    "include_messages": true,
    "include_tool_logs": true,
    "confirmation": "DELETE_ALL_DATA_FOR_user_123"
  }'
```

**Response:**
```json
{
  "data": {
    "deletion_id": "del_abc123",
    "status": "processing",
    "estimated_completion": "2026-01-20T13:00:00Z",
    "items_to_delete": {
      "rooms": 5,
      "messages": 142,
      "tool_logs": 23
    }
  }
}
```

> **Important**: Data deletion is asynchronous. Poll the deletion status endpoint to confirm completion
> before responding to user deletion requests.

### Secret Rotation

Rotate `callback_secret` for tools without downtime:

**Step 1: Add new secret (dual-secret mode):**
```bash
curl -X PATCH https://core.interactor.com/api/v1/tools/tool_abc/secrets \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "add_secret": "new_secret_value_here",
    "deprecate_old_after_hours": 24
  }'
```

**Step 2: Update your callback handler to accept both secrets:**
```typescript
function verifyWithRotation(
  payload: string,
  signature: string,
  secrets: string[]
): boolean {
  const signatureValue = signature.replace('sha256=', '');

  for (const secret of secrets) {
    const expected = crypto
      .createHmac('sha256', secret)
      .update(payload)
      .digest('hex');

    if (crypto.timingSafeEqual(
      Buffer.from(signatureValue),
      Buffer.from(expected)
    )) {
      return true;
    }
  }

  return false;
}

// Use both secrets during rotation
const SECRETS = [
  process.env.TOOL_CALLBACK_SECRET_NEW!,
  process.env.TOOL_CALLBACK_SECRET_OLD!
];

const isValid = verifyWithRotation(payload, signature, SECRETS);
```

**Step 3: After transition period, remove old secret:**
```bash
curl -X PATCH https://core.interactor.com/api/v1/tools/tool_abc/secrets \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "remove_deprecated": true
  }'
```

### PII Handling

**Do NOT include PII in:**
- Tool names or descriptions
- Assistant names
- Log messages

**DO use:**
- Namespaces for user identification (e.g., `user_123`)
- Encrypted metadata for sensitive context
- Room metadata (encrypted at rest) for PII when necessary

```typescript
// Bad - PII in tool parameters
{ "user_email": "john@example.com" }

// Good - Use references
{ "user_id": "user_123" }  // Look up email in your backend
```

---

## Observability & Correlation IDs

### Request Correlation

Every API request returns a correlation ID for tracing:

**Response Headers:**
```
X-Request-Id: req_abc123xyz
X-Trace-Id: trace_789def
```

Include these in support requests and logging:

```typescript
async function apiRequest(path: string, options: RequestInit = {}) {
  const response = await fetch(`https://core.interactor.com/api/v1${path}`, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${token}`,
      'X-Client-Request-Id': crypto.randomUUID() // Your own correlation ID
    }
  });

  const requestId = response.headers.get('X-Request-Id');
  const traceId = response.headers.get('X-Trace-Id');

  // Log for debugging
  console.log(`[${path}] Request: ${requestId}, Trace: ${traceId}`);

  return { response, requestId, traceId };
}
```

### Logging Recommendations

```typescript
import { Logger } from 'your-logging-library';

const logger = new Logger({
  service: 'my-app',
  version: process.env.APP_VERSION
});

// Include correlation IDs in all agent-related logs
async function sendMessageWithLogging(roomId: string, content: string) {
  const correlationId = crypto.randomUUID();

  logger.info('Sending message to AI agent', {
    correlationId,
    roomId,
    contentLength: content.length
  });

  try {
    const { response, requestId } = await apiRequest(
      `/agents/rooms/${roomId}/messages`,
      {
        method: 'POST',
        body: JSON.stringify({ content, role: 'user' })
      }
    );

    if (!response.ok) {
      logger.error('Message send failed', {
        correlationId,
        requestId,
        status: response.status
      });
      throw new Error(`API error: ${response.status}`);
    }

    const data = await response.json();

    logger.info('Message sent successfully', {
      correlationId,
      requestId,
      messageId: data.data.id
    });

    return data;
  } catch (error) {
    logger.error('Message send exception', {
      correlationId,
      error: error.message
    });
    throw error;
  }
}
```

### Metrics to Track

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `agent.messages.sent` | Messages sent to assistants | N/A (volume) |
| `agent.messages.latency_ms` | Time to first token | > 5000ms |
| `agent.tool_calls.total` | Tool invocations | N/A (volume) |
| `agent.tool_calls.errors` | Failed tool callbacks | > 5% error rate |
| `agent.tool_calls.latency_ms` | Tool callback duration | > 10000ms |
| `agent.rooms.active` | Currently active rooms | Depends on scale |
| `agent.rate_limits.hits` | 429 responses received | > 10/min |

### Dashboard Integration

Export metrics to your monitoring system:

```typescript
import { metrics } from 'your-metrics-library';

// Track message latency
const sendStart = Date.now();
await sendMessage(roomId, content);
metrics.histogram('agent.messages.latency_ms', Date.now() - sendStart, {
  assistant_id: assistantId
});

// Track tool callback performance
app.post('/api/tools/:toolName', async (req, res) => {
  const start = Date.now();
  try {
    const result = await handleToolCallback(req);
    metrics.increment('agent.tool_calls.total', { tool: req.params.toolName, status: 'success' });
    res.json({ result });
  } catch (error) {
    metrics.increment('agent.tool_calls.errors', { tool: req.params.toolName });
    throw error;
  } finally {
    metrics.histogram('agent.tool_calls.latency_ms', Date.now() - start, {
      tool: req.params.toolName
    });
  }
});
```

---

## Message Limits & Attachments

### Message Size Limits

| Content Type | Max Size | Notes |
|--------------|----------|-------|
| Text message | 32 KB | UTF-8 encoded |
| Metadata object | 16 KB | JSON serialized |
| Tool result | 64 KB | JSON serialized |
| Total request | 128 KB | Including headers |

Messages exceeding these limits return `413 Payload Too Large`.

### Handling Large Content

For content that may exceed limits:

```typescript
const MAX_MESSAGE_SIZE = 32 * 1024; // 32 KB

function truncateForAssistant(content: string): string {
  if (content.length <= MAX_MESSAGE_SIZE) {
    return content;
  }

  // Truncate with indicator
  const truncated = content.slice(0, MAX_MESSAGE_SIZE - 100);
  return truncated + '\n\n[Content truncated. Full content available via reference ID: ref_xxx]';
}

// For large documents, summarize or chunk
async function sendLargeDocument(roomId: string, document: string) {
  if (document.length <= MAX_MESSAGE_SIZE) {
    return sendMessage(roomId, document);
  }

  // Store full document and send reference
  const docId = await storeDocument(document);

  return sendMessage(roomId,
    `I have a document to analyze (${document.length} characters). ` +
    `Key sections:\n${extractKeySections(document)}\n\n` +
    `Use the get_document tool with id="${docId}" to retrieve specific sections.`
  );
}
```

### Attachment Support

> **API Note**: File attachment support varies by Interactor version. Check your API documentation
> or contact support for availability.

**If supported, the typical pattern:**

```bash
# 1. Upload attachment
curl -X POST https://core.interactor.com/api/v1/attachments \
  -H "Authorization: Bearer <token>" \
  -F "file=@document.pdf" \
  -F "purpose=message_attachment"

# Response:
# { "data": { "id": "att_xyz", "url": "https://...", "expires_at": "..." } }

# 2. Reference in message
curl -X POST https://core.interactor.com/api/v1/agents/rooms/room_xyz/messages \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Please analyze this document",
    "role": "user",
    "attachments": ["att_xyz"]
  }'
```

**Supported file types (when available):**
- Documents: PDF, DOCX, TXT, MD
- Images: PNG, JPG, GIF, WEBP
- Data: CSV, JSON, XML

**Max file size:** 10 MB per file, 25 MB total per message.

---

## API Reference & Testing

### OpenAPI Specification

The AI Agents API follows OpenAPI 3.0 specification. Access the spec at:

```
https://core.interactor.com/api/v1/openapi.json
https://core.interactor.com/api/v1/openapi.yaml
```

**Generate Client Libraries:**

```bash
# TypeScript
npx openapi-typescript-codegen \
  --input https://core.interactor.com/api/v1/openapi.json \
  --output ./generated/interactor-client

# Python
pip install openapi-python-client
openapi-python-client generate \
  --url https://core.interactor.com/api/v1/openapi.json
```

### Testing Your Integration

**1. Use the Sandbox Environment:**

```bash
# Sandbox base URL
export INTERACTOR_URL="https://sandbox.interactor.com"

# Sandbox credentials (from dashboard)
export INTERACTOR_SANDBOX_TOKEN="sandbox_token_here"
```

**2. Test Tool Callbacks Locally:**

Use a tunnel service to expose your local endpoint:

```bash
# Using ngrok
ngrok http 3000

# Register tool with ngrok URL
curl -X POST https://sandbox.interactor.com/api/v1/tools \
  -H "Authorization: Bearer $INTERACTOR_SANDBOX_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test_tool",
    "description": "Test tool for development",
    "parameters": {"type": "object", "properties": {}},
    "callback_url": "https://abc123.ngrok.io/api/tools/test"
  }'
```

**3. Verify Webhook Signatures in Tests:**

```typescript
import { describe, it, expect } from 'vitest';
import crypto from 'crypto';

describe('Tool Callback Verification', () => {
  const SECRET = 'test_secret';

  it('should verify valid signature', () => {
    const payload = JSON.stringify({ tool_name: 'test', parameters: {} });
    const signature = 'sha256=' + crypto
      .createHmac('sha256', SECRET)
      .update(payload)
      .digest('hex');

    const result = verifyToolCallback(payload, signature, SECRET);
    expect(result.valid).toBe(true);
  });

  it('should reject invalid signature', () => {
    const payload = JSON.stringify({ tool_name: 'test', parameters: {} });
    const signature = 'sha256=invalid';

    const result = verifyToolCallback(payload, signature, SECRET);
    expect(result.valid).toBe(false);
  });

  it('should reject expired timestamp', () => {
    const payload = JSON.stringify({ tool_name: 'test', parameters: {} });
    const oldTimestamp = new Date(Date.now() - 400000).toISOString(); // 400 seconds old
    const signature = 'sha256=' + crypto
      .createHmac('sha256', SECRET)
      .update(payload)
      .digest('hex');

    const result = verifyToolCallback(payload, signature, oldTimestamp, SECRET, 300);
    expect(result.valid).toBe(false);
    expect(result.error).toContain('too old');
  });
});
```

**4. Integration Test Example:**

```typescript
import { describe, it, expect, beforeAll, afterAll } from 'vitest';

describe('AI Agents Integration', () => {
  let assistantId: string;
  let roomId: string;

  beforeAll(async () => {
    // Create test assistant
    const assistant = await createAssistant({
      name: `test_${Date.now()}`,
      title: 'Test Assistant',
      instructions: 'You are a test assistant. Always respond with "Test OK".'
    });
    assistantId = assistant.id;
  });

  afterAll(async () => {
    // Cleanup
    if (roomId) await closeRoom(roomId);
    if (assistantId) await deleteAssistant(assistantId);
  });

  it('should create a room and exchange messages', async () => {
    // Create room
    const room = await createRoom(assistantId, 'test_user');
    roomId = room.id;
    expect(room.status).toBe('active');

    // Send message
    const sent = await sendMessage(roomId, 'Hello');
    expect(sent.role).toBe('user');

    // Wait for response (in real test, use streaming or webhooks)
    await new Promise(r => setTimeout(r, 3000));

    // Get messages
    const { messages } = await getMessages(roomId);
    expect(messages.length).toBeGreaterThanOrEqual(2);

    const assistantMessage = messages.find(m => m.role === 'assistant');
    expect(assistantMessage).toBeDefined();
    expect(assistantMessage?.content).toContain('Test OK');
  });
});
```

---

## Output Format

When implementing AI agents, provide this summary:

```markdown
## AI Agent Implementation Report

**Date**: YYYY-MM-DD
**Assistant**: support_assistant

### Configuration
| Setting | Value |
|---------|-------|
| Model | gpt-4o |
| Temperature | 0.7 |
| Tools | search_products, create_ticket |

### Tools Registered
| Tool | Callback URL | Status |
|------|--------------|--------|
| search_products | https://app.com/api/tools/search | ✓ Active |
| create_ticket | https://app.com/api/tools/ticket | ✓ Active |

### Data Sources Connected
| Name | Type | Status |
|------|------|--------|
| sales_database | PostgreSQL | ✓ Connected |

### Implementation Checklist
- [ ] Assistant created with instructions
- [ ] Tools registered with callbacks
- [ ] Tool callback signature verification
- [ ] Data sources connected
- [ ] Semantic mappings configured
- [ ] Room management implemented
- [ ] Message streaming setup
- [ ] Error handling implemented

### Next Steps
1. Test conversations with sample queries
2. Set up webhooks for real-time updates (see `interactor-webhooks` skill)
3. Implement streaming for real-time responses
```

---

## Related Skills

- **interactor-auth**: Setup authentication (prerequisite)
- **interactor-sdk**: TypeScript/JavaScript SDK for API integration
- **interactor-credentials**: Agents can use credentials to access external services
- **interactor-workflows**: Combine AI agents with automated workflows
- **interactor-webhooks**: Real-time message streaming and event subscriptions
