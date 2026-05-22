---
name: webhook-integration-patterns
description: Designs reliable webhook systems with proper delivery guarantees, retry logic, signature verification, and idempotent processing for event-driven integrations.
license: MIT
---

# Webhook Integration Patterns

This skill provides guidance for designing and implementing robust webhook systems—both as providers (sending webhooks) and consumers (receiving webhooks).

## Core Competencies

- **Delivery Guarantees**: At-least-once, exactly-once semantics
- **Security**: Signature verification, secret rotation
- **Reliability**: Retry strategies, dead letter handling
- **Scalability**: Queue-based processing, rate limiting

## Webhook Fundamentals

### What Webhooks Solve

```
Polling (inefficient):           Webhooks (efficient):
┌────────┐     ┌────────┐       ┌────────┐     ┌────────┐
│ Client │     │ Server │       │ Client │     │ Server │
└───┬────┘     └───┬────┘       └───┬────┘     └───┬────┘
    │ Any news?    │                │              │
    │─────────────▶│                │              │
    │    No        │                │   Event!     │
    │◀─────────────│                │◀─────────────│
    │ Any news?    │                │  POST /hook  │
    │─────────────▶│                │◀─────────────│
    │    No        │                │   200 OK     │
    │◀─────────────│                │─────────────▶│
    │ Any news?    │
    │─────────────▶│       Push-based notification
    │    YES!      │       instead of polling
    │◀─────────────│
```

### Webhook Anatomy

```http
POST /webhooks/payment HTTP/1.1
Host: your-app.com
Content-Type: application/json
X-Webhook-Signature: sha256=abc123...
X-Webhook-ID: evt_12345
X-Webhook-Timestamp: 1706616000

{
  "id": "evt_12345",
  "type": "payment.completed",
  "created_at": "2024-01-30T12:00:00Z",
  "data": {
    "payment_id": "pay_abc",
    "amount": 1000,
    "currency": "USD"
  }
}
```

Key headers:
- **Signature**: Cryptographic proof of authenticity
- **ID**: Unique event identifier for deduplication
- **Timestamp**: When the event occurred

## Webhook Provider Design

### Event Schema Design

```python
class WebhookEvent:
    """Standard webhook event structure"""

    def __init__(self, event_type, data, idempotency_key=None):
        self.id = self._generate_id()
        self.type = event_type
        self.created_at = datetime.utcnow().isoformat()
        self.api_version = "2024-01-30"
        self.data = data
        self.idempotency_key = idempotency_key or self.id

    def to_payload(self):
        return {
            "id": self.id,
            "type": self.type,
            "created_at": self.created_at,
            "api_version": self.api_version,
            "data": self.data
        }

# Event types follow resource.action pattern
EVENT_TYPES = [
    "payment.created",
    "payment.completed",
    "payment.failed",
    "subscription.created",
    "subscription.updated",
    "subscription.cancelled",
    "customer.created",
    "customer.deleted"
]
```

### Signature Generation

```python
import hmac
import hashlib
import time

class WebhookSigner:
    """Sign webhook payloads for verification"""

    def __init__(self, secret):  # allow-secret
        self.secret = secret.encode()  # allow-secret

    def sign(self, payload, timestamp=None):
        """Generate HMAC signature"""
        timestamp = timestamp or int(time.time())
        payload_str = json.dumps(payload, separators=(',', ':'))

        # Include timestamp to prevent replay attacks
        signed_payload = f"{timestamp}.{payload_str}"

        signature = hmac.new(
            self.secret,
            signed_payload.encode(),
            hashlib.sha256
        ).hexdigest()

        return {
            'signature': f"sha256={signature}",
            'timestamp': timestamp
        }

    def create_headers(self, payload):
        """Generate all webhook headers"""
        sign_data = self.sign(payload)
        return {
            'Content-Type': 'application/json',
            'X-Webhook-Signature': sign_data['signature'],
            'X-Webhook-Timestamp': str(sign_data['timestamp']),
            'X-Webhook-ID': payload['id']
        }
```

### Delivery System

```python
import asyncio
from datetime import datetime, timedelta

class WebhookDeliverySystem:
    """Reliable webhook delivery with retries"""

    RETRY_SCHEDULE = [
        timedelta(seconds=10),
        timedelta(minutes=1),
        timedelta(minutes=5),
        timedelta(minutes=30),
        timedelta(hours=1),
        timedelta(hours=6),
        timedelta(hours=24)
    ]

    def __init__(self, signer, http_client):
        self.signer = signer
        self.http = http_client
        self.delivery_log = []

    async def deliver(self, endpoint, event, attempt=0):
        """Attempt webhook delivery"""
        payload = event.to_payload()
        headers = self.signer.create_headers(payload)

        try:
            response = await self.http.post(
                endpoint.url,
                json=payload,
                headers=headers,
                timeout=30
            )

            self._log_attempt(endpoint, event, attempt, response)

            if response.status_code in (200, 201, 202, 204):
                return {'status': 'delivered', 'attempts': attempt + 1}

            # Non-success status - schedule retry
            return await self._schedule_retry(endpoint, event, attempt)

        except Exception as e:
            self._log_attempt(endpoint, event, attempt, error=e)
            return await self._schedule_retry(endpoint, event, attempt)

    async def _schedule_retry(self, endpoint, event, attempt):
        """Schedule next retry or give up"""
        if attempt >= len(self.RETRY_SCHEDULE):
            self._move_to_dead_letter(endpoint, event)
            return {'status': 'failed', 'attempts': attempt + 1}

        delay = self.RETRY_SCHEDULE[attempt]
        # In production: use job queue with delayed execution
        await asyncio.sleep(delay.total_seconds())
        return await self.deliver(endpoint, event, attempt + 1)

    def _move_to_dead_letter(self, endpoint, event):
        """Store failed webhook for manual review"""
        # Store in dead letter queue/table
        pass
```

### Endpoint Management

```python
class WebhookEndpoint:
    """Subscriber endpoint configuration"""

    def __init__(self, url, events, secret=None):  # allow-secret
        self.id = generate_id()
        self.url = url
        self.events = events  # List of subscribed event types
        self.secret = secret or generate_secret()  # allow-secret
        self.status = 'active'
        self.created_at = datetime.utcnow()

        # Health tracking
        self.consecutive_failures = 0
        self.last_success = None
        self.last_failure = None

    def should_receive(self, event_type):
        """Check if endpoint subscribes to this event"""
        if '*' in self.events:
            return True
        return event_type in self.events

    def record_success(self):
        self.consecutive_failures = 0
        self.last_success = datetime.utcnow()
        if self.status == 'disabled':
            self.status = 'active'

    def record_failure(self):
        self.consecutive_failures += 1
        self.last_failure = datetime.utcnow()

        # Auto-disable after too many failures
        if self.consecutive_failures >= 10:
            self.status = 'disabled'
```

## Webhook Consumer Design

### Signature Verification

```python
class WebhookVerifier:
    """Verify incoming webhook signatures"""

    TIMESTAMP_TOLERANCE = 300  # 5 minutes

    def __init__(self, secret):  # allow-secret
        self.secret = secret.encode()  # allow-secret

    def verify(self, payload, signature, timestamp):
        """Verify webhook authenticity"""
        # Check timestamp freshness
        current_time = int(time.time())
        if abs(current_time - int(timestamp)) > self.TIMESTAMP_TOLERANCE:
            raise WebhookVerificationError("Timestamp too old")

        # Compute expected signature
        signed_payload = f"{timestamp}.{payload}"
        expected = hmac.new(
            self.secret,
            signed_payload.encode(),
            hashlib.sha256
        ).hexdigest()

        expected_sig = f"sha256={expected}"

        # Constant-time comparison to prevent timing attacks
        if not hmac.compare_digest(signature, expected_sig):
            raise WebhookVerificationError("Invalid signature")

        return True


# Flask endpoint example
@app.route('/webhooks/provider', methods=['POST'])
def handle_webhook():
    verifier = WebhookVerifier(WEBHOOK_SECRET)

    try:
        verifier.verify(
            request.data.decode(),
            request.headers.get('X-Webhook-Signature'),
            request.headers.get('X-Webhook-Timestamp')
        )
    except WebhookVerificationError:
        return 'Invalid signature', 401

    event = request.json
    process_webhook(event)

    return 'OK', 200
```

### Idempotent Processing

```python
class IdempotentWebhookProcessor:
    """Process webhooks exactly once"""

    def __init__(self, storage):
        self.storage = storage  # Redis, database, etc.
        self.lock_ttl = 300  # 5 minute lock

    async def process(self, event):
        """Process webhook idempotently"""
        event_id = event['id']

        # Check if already processed
        if await self.storage.exists(f"webhook:processed:{event_id}"):
            return {'status': 'duplicate', 'event_id': event_id}

        # Acquire lock to prevent concurrent processing
        lock_key = f"webhook:lock:{event_id}"
        if not await self.storage.set_nx(lock_key, "1", ex=self.lock_ttl):
            return {'status': 'processing', 'event_id': event_id}

        try:
            # Process the event
            result = await self._handle_event(event)

            # Mark as processed (with long TTL for deduplication)
            await self.storage.set(
                f"webhook:processed:{event_id}",
                json.dumps(result),
                ex=86400 * 7  # Keep for 7 days
            )

            return {'status': 'processed', 'event_id': event_id}

        finally:
            await self.storage.delete(lock_key)

    async def _handle_event(self, event):
        """Route event to appropriate handler"""
        handlers = {
            'payment.completed': self._handle_payment_completed,
            'subscription.cancelled': self._handle_subscription_cancelled,
            # ... more handlers
        }
        handler = handlers.get(event['type'])
        if handler:
            return await handler(event['data'])
        return {'skipped': True, 'reason': 'unknown_event_type'}
```

### Queue-Based Processing

```python
class QueuedWebhookHandler:
    """Decouple receipt from processing"""

    def __init__(self, queue):
        self.queue = queue  # Redis, SQS, RabbitMQ, etc.

    async def receive(self, event):
        """Acknowledge receipt quickly, process async"""
        # Validate immediately
        self._validate_event_structure(event)

        # Queue for processing
        await self.queue.enqueue(
            'webhook_processing',
            event,
            deduplication_id=event['id']
        )

        # Return 200 immediately (don't make sender wait)
        return {'status': 'accepted'}

    async def process_queue(self):
        """Worker that processes queued webhooks"""
        while True:
            event = await self.queue.dequeue('webhook_processing')
            if event:
                try:
                    await self._process_event(event)
                    await self.queue.ack(event)
                except Exception as e:
                    await self.queue.nack(event, requeue=True)
                    logging.error(f"Webhook processing failed: {e}")
```

## Security Patterns

### Secret Rotation

```python
class SecretRotation:
    """Support rolling secret updates"""

    def __init__(self):
        self.current_secret = None
        self.previous_secret = None
        self.rotation_timestamp = None

    def rotate(self, new_secret):
        """Rotate to new secret while supporting old"""
        self.previous_secret = self.current_secret
        self.current_secret = new_secret
        self.rotation_timestamp = datetime.utcnow()

    def get_verification_secrets(self):
        """Return secrets to try for verification"""
        secrets = [self.current_secret]

        # Accept previous secret for grace period
        if self.previous_secret and self.rotation_timestamp:
            grace_period = timedelta(hours=24)
            if datetime.utcnow() - self.rotation_timestamp < grace_period:
                secrets.append(self.previous_secret)

        return secrets
```

### IP Allowlisting

```python
ALLOWED_IPS = {
    'stripe': ['3.18.12.63', '3.130.192.231', ...],
    'github': ['192.30.252.0/22', '185.199.108.0/22', ...],
    'twilio': ['54.172.60.0/23', '54.244.51.0/24', ...]
}

def verify_source_ip(request, provider):
    """Verify webhook comes from expected IP"""
    client_ip = request.remote_addr

    allowed = ALLOWED_IPS.get(provider, [])
    for allowed_range in allowed:
        if ip_in_range(client_ip, allowed_range):
            return True

    return False
```

## Error Handling

### Response Codes

| Code | Meaning | Provider Action |
|------|---------|-----------------|
| 200-204 | Success | Mark delivered |
| 400 | Bad request | Don't retry (your bug) |
| 401/403 | Auth failed | Disable endpoint |
| 404 | Not found | Disable endpoint |
| 429 | Rate limited | Retry with backoff |
| 500+ | Server error | Retry |
| Timeout | No response | Retry |

### Dead Letter Queue

```python
class DeadLetterQueue:
    """Store and manage failed webhooks"""

    async def add(self, endpoint, event, failure_reason, attempts):
        """Add failed webhook to DLQ"""
        await self.storage.add({
            'id': generate_id(),
            'endpoint_id': endpoint.id,
            'endpoint_url': endpoint.url,
            'event': event.to_payload(),
            'failure_reason': str(failure_reason),
            'attempts': attempts,
            'added_at': datetime.utcnow().isoformat()
        })

    async def retry(self, dlq_item_id):
        """Manually retry a DLQ item"""
        item = await self.storage.get(dlq_item_id)
        endpoint = await self.get_endpoint(item['endpoint_id'])
        event = WebhookEvent.from_payload(item['event'])

        result = await self.delivery_system.deliver(endpoint, event)

        if result['status'] == 'delivered':
            await self.storage.remove(dlq_item_id)

        return result

    async def purge_old(self, days=30):
        """Clean up old DLQ items"""
        cutoff = datetime.utcnow() - timedelta(days=days)
        await self.storage.delete_before(cutoff)
```

## Best Practices

### For Providers

1. **Include event ID** for consumer deduplication
2. **Sign payloads** with HMAC-SHA256 minimum
3. **Include timestamps** to prevent replay
4. **Retry with exponential backoff** (5 attempts minimum)
5. **Provide webhook logs** in your dashboard
6. **Support event filtering** by type
7. **Version your payloads** for backward compatibility

### For Consumers

1. **Verify signatures** before processing
2. **Respond quickly** (< 5 seconds)
3. **Process asynchronously** via queue
4. **Implement idempotency** using event ID
5. **Log everything** for debugging
6. **Monitor for failures** proactively

## References

- `references/webhook-security.md` - Detailed security implementation
- `references/provider-examples.md` - Stripe, GitHub, Twilio patterns
- `references/testing-webhooks.md` - Local development and testing
