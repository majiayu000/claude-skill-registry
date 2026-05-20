---
name: webhook-development
description: Implement webhook systems for event-driven integration with retry logic, signature verification, and delivery guarantees. Use when creating event notification systems, integrating with external services, or building event-driven architectures.
---

# Webhook Development

## Overview

Build reliable webhook systems with event delivery, signature verification, retry logic, and dead-letter handling for asynchronous integrations.

## When to Use

- Sending real-time notifications to external systems
- Implementing event-driven architectures
- Integrating with third-party platforms
- Building audit trails and logging systems
- Triggering automated workflows
- Delivering payment or order notifications

## Instructions

### 1. **Webhook Event Schema**

```json
{
  "id": "evt_1234567890",
  "timestamp": "2025-01-15T10:30:00Z",
  "event": "order.created",
  "version": "1.0",
  "data": {
    "orderId": "ORD-123456",
    "customerId": "CUST-789",
    "amount": 99.99,
    "currency": "USD",
    "items": [
      {
        "productId": "PROD-001",
        "quantity": 2,
        "price": 49.99
      }
    ],
    "status": "pending"
  },
  "attempt": 1,
  "retryable": true
}
```

### 2. **Node.js Webhook Service**

```javascript
const express = require('express');
const crypto = require('crypto');
const axios = require('axios');
const Bull = require('bull');

const app = express();
app.use(express.json());

const WEBHOOK_SECRET = process.env.WEBHOOK_SECRET;
const webhookQueue = new Bull('webhooks', {
  redis: { host: 'localhost', port: 6379 }
});

// Register webhook subscription
app.post('/api/webhooks/subscribe', async (req, res) => {
  const { url, events, secret } = req.body;

  // Validate URL
  try {
    new URL(url);
  } catch {
    return res.status(400).json({ error: 'Invalid URL' });
  }

  const webhook = {
    id: crypto.randomBytes(16).toString('hex'),
    url,
    events,
    secret: secret || crypto.randomBytes(32).toString('hex'),
    active: true,
    createdAt: new Date(),
    failureCount: 0
  };

  // Save to database
  await WebhookSubscription.create(webhook);

  res.status(201).json({
    id: webhook.id,
    secret: webhook.secret,
    message: 'Webhook registered successfully'
  });
});

// Send webhook event
const sendWebhookEvent = async (eventType, data) => {
  const webhooks = await WebhookSubscription.find({
    events: eventType,
    active: true
  });

  for (const webhook of webhooks) {
    const event = {
      id: `evt_${Date.now()}`,
      timestamp: new Date().toISOString(),
      event: eventType,
      version: '1.0',
      data,
      attempt: 1,
      retryable: true
    };

    // Add to queue
    await webhookQueue.add(
      { webhook, event },
      {
        attempts: 5,
        backoff: {
          type: 'exponential',
          delay: 2000
        },
        removeOnComplete: true
      }
    );
  }
};

// Process webhook queue
webhookQueue.process(async (job) => {
  const { webhook, event } = job.data;

  try {
    const signature = generateSignature(event, webhook.secret);

    const response = await axios.post(webhook.url, event, {
      headers: {
        'Content-Type': 'application/json',
        'X-Webhook-Signature': signature,
        'X-Webhook-ID': event.id,
        'X-Webhook-Attempt': event.attempt
      },
      timeout: 10000
    });

    if (response.status >= 200 && response.status < 300) {
      // Success
      await WebhookDelivery.create({
        webhookId: webhook.id,
        eventId: event.id,
        status: 'delivered',
        statusCode: response.status,
        deliveredAt: new Date()
      });
      return;
    }

    throw new Error(`HTTP ${response.status}`);
  } catch (error) {
    // Retry or dead letter
    if (job.attemptsMade < 5) {
      throw error; // Retry
    } else {
      // Dead letter
      await DeadLetterQueue.create({
        webhookId: webhook.id,
        eventId: event.id,
        event,
        error: error.message,
        failedAt: new Date()
      });

      // Update failure count
      webhook.failureCount++;
      if (webhook.failureCount >= 10) {
        webhook.active = false;
      }
      await webhook.save();
    }
  }
});

// Webhook endpoint (receiving webhooks)
app.post('/webhooks/:id', async (req, res) => {
  const signature = req.headers['x-webhook-signature'];
  const webhookId = req.params.id;
  const event = req.body;

  try {
    const webhook = await WebhookSubscription.findOne({ id: webhookId });
    if (!webhook) {
      return res.status(404).json({ error: 'Webhook not found' });
    }

    // Verify signature
    const expectedSignature = generateSignature(event, webhook.secret);
    if (signature !== expectedSignature) {
      return res.status(401).json({ error: 'Invalid signature' });
    }

    // Process event
    console.log('Received webhook event:', event);

    res.status(200).json({ received: true });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Signature generation
const generateSignature = (payload, secret) => {
  const message = JSON.stringify(payload);
  return crypto.createHmac('sha256', secret).update(message).digest('hex');
};

// List webhook subscriptions
app.get('/api/webhooks', async (req, res) => {
  const webhooks = await WebhookSubscription.find({}, { secret: 0 });
  res.json(webhooks);
});

// Test webhook delivery
app.post('/api/webhooks/:id/test', async (req, res) => {
  const webhook = await WebhookSubscription.findOne({ id: req.params.id });

  const testEvent = {
    id: `evt_test_${Date.now()}`,
    timestamp: new Date().toISOString(),
    event: 'webhook.test',
    data: { message: 'Test event' }
  };

  await webhookQueue.add({ webhook, event: testEvent });

  res.json({ message: 'Test event queued' });
});

// Retry failed deliveries
app.post('/api/webhooks/deliveries/:id/retry', async (req, res) => {
  const delivery = await WebhookDelivery.findOne({ _id: req.params.id });
  if (!delivery) {
    return res.status(404).json({ error: 'Delivery not found' });
  }

  const webhook = await WebhookSubscription.findOne({ id: delivery.webhookId });
  const event = await Event.findOne({ id: delivery.eventId });

  await webhookQueue.add({ webhook, event });

  res.json({ message: 'Retry queued' });
});

// List webhook deliveries
app.get('/api/webhooks/:id/deliveries', async (req, res) => {
  const deliveries = await WebhookDelivery.find({
    webhookId: req.params.id
  }).limit(100);

  res.json(deliveries);
});

// Event trigger examples
app.post('/api/orders', async (req, res) => {
  const order = await Order.create(req.body);

  // Send webhook event
  await sendWebhookEvent('order.created', {
    orderId: order.id,
    customerId: order.customerId,
    amount: order.amount,
    status: order.status
  });

  res.status(201).json(order);
});

app.listen(3000, () => console.log('Server on port 3000'));
```

### 3. **Python Webhook Handler**

```python
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import hmac
import hashlib
import requests
import json
from celery import Celery
from sqlalchemy import Column, String, Boolean, DateTime, Integer

app = Flask(__name__)
celery = Celery(app.name, broker='redis://localhost:6379')

class WebhookSubscription:
    id = Column(String(100), primary_key=True)
    url = Column(String(500))
    events = Column(String(500))
    secret = Column(String(256))
    active = Column(Boolean, default=True)
    failure_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

def generate_signature(payload, secret):
    message = json.dumps(payload, sort_keys=True)
    return hmac.new(
        secret.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

@app.route('/api/webhooks/subscribe', methods=['POST'])
def subscribe_webhook():
    data = request.get_json()
    url = data.get('url')
    events = data.get('events', [])
    secret = data.get('secret', os.urandom(32).hex())

    webhook = WebhookSubscription(
        id=f"wh_{secrets.token_hex(8)}",
        url=url,
        events=','.join(events),
        secret=secret,
        active=True
    )

    db.session.add(webhook)
    db.session.commit()

    return jsonify({
        'id': webhook.id,
        'secret': webhook.secret,
        'message': 'Webhook registered'
    }), 201

@celery.task(bind=True, max_retries=5)
def deliver_webhook(self, webhook_id, event):
    webhook = WebhookSubscription.query.get(webhook_id)
    if not webhook:
        return

    signature = generate_signature(event, webhook.secret)

    try:
        response = requests.post(
            webhook.url,
            json=event,
            headers={
                'Content-Type': 'application/json',
                'X-Webhook-Signature': signature,
                'X-Webhook-ID': event['id'],
                'X-Webhook-Attempt': str(event.get('attempt', 1))
            },
            timeout=10
        )

        if 200 <= response.status_code < 300:
            WebhookDelivery.create(
                webhook_id=webhook_id,
                event_id=event['id'],
                status='delivered',
                status_code=response.status_code
            )
            return

        raise Exception(f"HTTP {response.status_code}")

    except Exception as exc:
        retry_delay = 2 ** self.request.retries
        raise self.retry(exc=exc, countdown=retry_delay)

@app.route('/webhooks/<webhook_id>', methods=['POST'])
def receive_webhook(webhook_id):
    signature = request.headers.get('X-Webhook-Signature')
    event = request.get_json()

    webhook = WebhookSubscription.query.get(webhook_id)
    if not webhook:
        return jsonify({'error': 'Not found'}), 404

    expected_signature = generate_signature(event, webhook.secret)
    if signature != expected_signature:
        return jsonify({'error': 'Invalid signature'}), 401

    return jsonify({'received': True}), 200

@app.route('/api/orders', methods=['POST'])
def create_order():
    order = Order.create(request.get_json())

    # Queue webhook delivery
    event = {
        'id': f"evt_{datetime.utcnow().timestamp()}",
        'timestamp': datetime.utcnow().isoformat(),
        'event': 'order.created',
        'data': order.to_dict()
    }

    webhooks = WebhookSubscription.query.filter(
        WebhookSubscription.events.contains('order.created'),
        WebhookSubscription.active == True
    ).all()

    for webhook in webhooks:
        deliver_webhook.delay(webhook.id, event)

    return jsonify(order.to_dict()), 201

if __name__ == '__main__':
    app.run(debug=False, port=3000)
```

### 4. **Best Practices**

```
✅ DO:
- Sign all webhooks with HMAC
- Implement exponential backoff retries
- Use message queues for reliable delivery
- Track webhook deliveries for debugging
- Provide webhook test endpoints
- Document supported event types
- Use unique event IDs for deduplication
- Set appropriate timeouts (10s)
- Implement dead-letter queues
- Return 2xx quickly, process async

❌ DON'T:
- Send sensitive data without encryption
- Use weak signatures
- Synchronous webhook delivery
- Ignore signature verification
- Expose webhook URLs publicly
- Retry indefinitely
- Log webhook payloads with secrets
- Skip webhook authentication
- Forget to handle idempotency
- Send duplicate events
```

### 5. **Webhook Events**

```
Standard Event Types:
- order.created
- order.updated
- order.cancelled
- payment.succeeded
- payment.failed
- user.registered
- user.updated
- invoice.issued
- shipment.created
- refund.processed
```

## Monitoring

```javascript
app.get('/api/webhooks/metrics', async (req, res) => {
  const total = await WebhookDelivery.countDocuments();
  const delivered = await WebhookDelivery.countDocuments({ status: 'delivered' });
  const failed = await WebhookDelivery.countDocuments({ status: 'failed' });
  const avgLatency = await WebhookDelivery.aggregate([
    { $group: { _id: null, avg: { $avg: '$latency' } } }
  ]);

  res.json({
    total,
    delivered,
    failed,
    successRate: (delivered / total * 100).toFixed(2),
    averageLatency: avgLatency[0]?.avg || 0
  });
});
```
