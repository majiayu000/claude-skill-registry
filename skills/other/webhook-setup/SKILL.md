---
name: webhook-setup
description: Set up webhook receivers with signature verification, idempotent event processing, retry handling, and dead letter queues for reliable event-driven integrations. Use when the user requests webhook setup or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Webhook Setup

This skill enables an AI agent to build production-grade webhook receivers and configure webhook producers. The agent implements HTTP endpoints that accept event payloads, verify cryptographic signatures to authenticate senders, process events idempotently to handle retries safely, and route events by type to appropriate handlers. The result is a reliable event-driven integration that handles real-world failure modes including replay attacks, out-of-order delivery, and provider timeouts.

## Workflow

1. **Design the webhook endpoint:** Create an HTTP POST endpoint at a stable, non-guessable URL path (e.g., `/webhooks/stripe`, `/webhooks/github`). The endpoint must return a `200 OK` response quickly (within 5 seconds for most providers) to acknowledge receipt—long processing should be done asynchronously via a job queue. Use HTTPS exclusively; most providers reject plain HTTP endpoints.

2. **Implement signature verification:** Every webhook provider signs payloads using HMAC-SHA256, RSA, or a similar scheme. Before processing any event, verify the signature using the provider's signing secret. Compare signatures using a constant-time comparison function to prevent timing attacks. Reject requests with missing or invalid signatures immediately with a `401 Unauthorized` response. Read the raw request body for verification—parsed JSON may differ from the signed bytes.

3. **Parse and route events by type:** Parse the verified payload and extract the event type (e.g., `payment_intent.succeeded`, `push`). Route each event type to a dedicated handler function using a registry or switch statement. Log unrecognized event types at warning level and return `200 OK` to prevent the provider from retrying unhandled events indefinitely.

4. **Process events idempotently:** Providers retry webhook delivery when they don't receive a timely `200` response, which means your handler may receive the same event multiple times. Store processed event IDs in a database table and check for duplicates before processing. Use database transactions to atomically mark an event as processed and perform its side effects.

5. **Add async processing and dead letter queues:** For events that require heavy processing (sending emails, updating multiple records), acknowledge the webhook immediately and enqueue the event for background processing. Failed events that exhaust retries should be moved to a dead letter queue (DLQ) for manual inspection. Set up monitoring and alerts on DLQ depth.

6. **Configure the webhook on the provider side:** Register your endpoint URL with the webhook provider, select the event types you need (subscribe to the minimum set), and note the signing secret. Test the webhook using the provider's test/ping functionality. Set up monitoring for delivery failures on the provider dashboard.

## Supported Technologies

- **Web frameworks:** Express.js, Fastify, Flask, FastAPI, Django, Rails, Spring Boot
- **Queue systems:** Bull/BullMQ (Redis), Celery (Python), Sidekiq (Ruby), SQS, RabbitMQ
- **Providers:** Stripe, GitHub, Slack, Twilio, SendGrid, Shopify, PayPal, Paddle
- **Monitoring:** Svix (webhook infrastructure), Hookdeck, ngrok (local development)
- **Databases:** PostgreSQL, MySQL, Redis (for idempotency tracking)

## Usage

Provide the agent with the webhook provider (Stripe, GitHub, etc.), the events you want to handle, and your server framework. The agent will produce a complete webhook receiver with signature verification, event routing, idempotent processing, and error handling. For local development, the agent can set up ngrok or a similar tunnel for testing.

## Examples

### Example 1: Stripe Webhook Receiver (Express.js)

```javascript
const express = require("express");
const crypto = require("crypto");
const { Queue } = require("bullmq");

const app = express();
const eventQueue = new Queue("webhook-events", { connection: { host: "localhost" } });

// CRITICAL: Use raw body for signature verification — must be before json parser
app.post("/webhooks/stripe", express.raw({ type: "application/json" }), async (req, res) => {
  const signature = req.headers["stripe-signature"];
  const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;

  // Step 1: Verify signature
  let event;
  try {
    event = verifyStripeSignature(req.body, signature, webhookSecret);
  } catch (err) {
    console.error(`Signature verification failed: ${err.message}`);
    return res.status(401).json({ error: "Invalid signature" });
  }

  // Step 2: Idempotency check — skip if already processed
  const alreadyProcessed = await checkIdempotency(event.id);
  if (alreadyProcessed) {
    console.log(`Event ${event.id} already processed, skipping`);
    return res.status(200).json({ received: true, deduplicated: true });
  }

  // Step 3: Acknowledge immediately, process async
  try {
    await eventQueue.add(event.type, {
      eventId: event.id,
      type: event.type,
      data: event.data.object,
      created: event.created,
    });
    await markEventReceived(event.id);
    res.status(200).json({ received: true });
  } catch (err) {
    console.error(`Failed to enqueue event ${event.id}:`, err);
    res.status(500).json({ error: "Processing failed" });
  }
});

// Stripe signature verification (manual implementation)
function verifyStripeSignature(payload, signatureHeader, secret) {
  const elements = signatureHeader.split(",").reduce((acc, part) => {
    const [key, value] = part.split("=");
    acc[key.trim()] = value;
    return acc;
  }, {});

  const timestamp = elements["t"];
  const expectedSig = elements["v1"];

  // Protect against replay attacks: reject events older than 5 minutes
  const tolerance = 300; // 5 minutes
  const currentTime = Math.floor(Date.now() / 1000);
  if (currentTime - parseInt(timestamp) > tolerance) {
    throw new Error("Webhook timestamp too old — possible replay attack");
  }

  // Compute expected signature
  const signedPayload = `${timestamp}.${payload}`;
  const computedSig = crypto
    .createHmac("sha256", secret)
    .update(signedPayload)
    .digest("hex");

  // Constant-time comparison to prevent timing attacks
  if (!crypto.timingSafeEqual(Buffer.from(expectedSig), Buffer.from(computedSig))) {
    throw new Error("Signature mismatch");
  }

  return JSON.parse(payload);
}

// Idempotency tracking with PostgreSQL
const { Pool } = require("pg");
const db = new Pool();

async function checkIdempotency(eventId) {
  const result = await db.query(
    "SELECT 1 FROM processed_webhook_events WHERE event_id = $1",
    [eventId]
  );
  return result.rows.length > 0;
}

async function markEventReceived(eventId) {
  await db.query(
    "INSERT INTO processed_webhook_events (event_id, received_at) VALUES ($1, NOW()) ON CONFLICT (event_id) DO NOTHING",
    [eventId]
  );
}

// Event handler workers (BullMQ)
const { Worker } = require("bullmq");

const worker = new Worker("webhook-events", async (job) => {
  const { eventId, type, data } = job.data;

  const handlers = {
    "payment_intent.succeeded": handlePaymentSucceeded,
    "payment_intent.payment_failed": handlePaymentFailed,
    "customer.subscription.deleted": handleSubscriptionCanceled,
    "invoice.payment_failed": handleInvoicePaymentFailed,
  };

  const handler = handlers[type];
  if (!handler) {
    console.log(`Unhandled event type: ${type}`);
    return;
  }

  await handler(data, eventId);
  await db.query("UPDATE processed_webhook_events SET processed_at = NOW() WHERE event_id = $1", [eventId]);
}, { connection: { host: "localhost" } });

async function handlePaymentSucceeded(paymentIntent, eventId) {
  const orderId = paymentIntent.metadata.order_id;
  await db.query("UPDATE orders SET status = 'paid', payment_id = $1 WHERE id = $2", [
    paymentIntent.id, orderId,
  ]);
  console.log(`Order ${orderId} marked as paid (event: ${eventId})`);
}

async function handlePaymentFailed(paymentIntent, eventId) {
  const orderId = paymentIntent.metadata.order_id;
  await db.query("UPDATE orders SET status = 'payment_failed' WHERE id = $1", [orderId]);
  // Trigger customer notification
  console.log(`Payment failed for order ${orderId} (event: ${eventId})`);
}

async function handleSubscriptionCanceled(subscription, eventId) {
  await db.query("UPDATE users SET subscription_status = 'canceled' WHERE stripe_customer_id = $1", [
    subscription.customer,
  ]);
}

async function handleInvoicePaymentFailed(invoice, eventId) {
  console.log(`Invoice ${invoice.id} payment failed, attempt ${invoice.attempt_count}`);
}

app.listen(3000, () => console.log("Webhook receiver listening on port 3000"));
```

### Example 2: GitHub Webhook for CI Triggers (Python/FastAPI)

```python
import hashlib
import hmac
import os
import logging
from datetime import datetime, timezone
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from pydantic import BaseModel

app = FastAPI()
logger = logging.getLogger(__name__)

GITHUB_WEBHOOK_SECRET = os.environ["GITHUB_WEBHOOK_SECRET"]

# In-memory idempotency store (use Redis or PostgreSQL in production)
processed_deliveries: set[str] = set()


def verify_github_signature(payload_body: bytes, signature_header: str | None) -> None:
    """Verify the GitHub webhook signature using HMAC-SHA256."""
    if not signature_header:
        raise HTTPException(status_code=401, detail="Missing X-Hub-Signature-256 header")

    expected_signature = "sha256=" + hmac.new(
        GITHUB_WEBHOOK_SECRET.encode(),
        payload_body,
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, signature_header):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")


@app.post("/webhooks/github")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    # Step 1: Read raw body and verify signature
    body = await request.body()
    signature = request.headers.get("X-Hub-Signature-256")
    verify_github_signature(body, signature)

    # Step 2: Idempotency check using delivery ID
    delivery_id = request.headers.get("X-GitHub-Delivery")
    if delivery_id in processed_deliveries:
        logger.info(f"Duplicate delivery {delivery_id}, skipping")
        return {"status": "duplicate", "delivery_id": delivery_id}

    # Step 3: Parse event and route
    event_type = request.headers.get("X-GitHub-Event")
    payload = await request.json()

    logger.info(f"Received GitHub event: {event_type} (delivery: {delivery_id})")

    # Acknowledge immediately, process in background
    processed_deliveries.add(delivery_id)
    background_tasks.add_task(process_github_event, event_type, payload, delivery_id)

    return {"status": "accepted", "event": event_type, "delivery_id": delivery_id}


async def process_github_event(event_type: str, payload: dict, delivery_id: str):
    """Route and process GitHub webhook events."""
    handlers = {
        "push": handle_push,
        "pull_request": handle_pull_request,
        "issues": handle_issue,
        "ping": handle_ping,
    }

    handler = handlers.get(event_type)
    if not handler:
        logger.warning(f"Unhandled GitHub event type: {event_type}")
        return

    try:
        await handler(payload)
        logger.info(f"Successfully processed {event_type} (delivery: {delivery_id})")
    except Exception as e:
        logger.error(f"Failed to process {event_type} (delivery: {delivery_id}): {e}")
        # In production, move to dead letter queue for retry
        raise


async def handle_push(payload: dict):
    """Trigger CI pipeline on push to main branch."""
    ref = payload.get("ref", "")
    repo = payload["repository"]["full_name"]
    commits = payload.get("commits", [])

    if ref != "refs/heads/main":
        logger.info(f"Ignoring push to {ref} on {repo}")
        return

    commit_messages = [c["message"].split("\n")[0] for c in commits]
    logger.info(f"Push to main on {repo}: {len(commits)} commits")

    # Check if any commits modify CI-relevant files
    changed_files = set()
    for commit in commits:
        changed_files.update(commit.get("added", []))
        changed_files.update(commit.get("modified", []))

    # Trigger appropriate CI jobs
    if any(f.startswith("src/") for f in changed_files):
        await trigger_ci_pipeline(repo, "build-and-test", payload["after"])
    if any(f.startswith("infrastructure/") for f in changed_files):
        await trigger_ci_pipeline(repo, "infrastructure-plan", payload["after"])

    logger.info(f"CI pipelines triggered for {repo}@{payload['after'][:8]}")


async def handle_pull_request(payload: dict):
    """Run checks on pull request events."""
    action = payload["action"]
    pr = payload["pull_request"]
    repo = payload["repository"]["full_name"]

    if action in ("opened", "synchronize"):
        logger.info(f"PR #{pr['number']} {action} on {repo}: {pr['title']}")
        await trigger_ci_pipeline(repo, "pr-checks", pr["head"]["sha"])
    elif action == "closed" and pr.get("merged"):
        logger.info(f"PR #{pr['number']} merged on {repo}")
        await trigger_ci_pipeline(repo, "deploy-staging", pr["merge_commit_sha"])


async def handle_issue(payload: dict):
    """Log issue events."""
    action = payload["action"]
    issue = payload["issue"]
    logger.info(f"Issue #{issue['number']} {action}: {issue['title']}")


async def handle_ping(payload: dict):
    """Respond to GitHub's test ping."""
    logger.info(f"Ping received. Hook ID: {payload.get('hook_id')}, Zen: {payload.get('zen')}")


async def trigger_ci_pipeline(repo: str, pipeline: str, commit_sha: str):
    """Trigger a CI pipeline (stub — replace with actual CI API call)."""
    logger.info(f"Triggering {pipeline} for {repo}@{commit_sha[:8]}")
    # In production: POST to Jenkins, GitHub Actions, CircleCI, etc.
```

## Best Practices

- **Respond quickly, process later.** Return `200 OK` within 3-5 seconds. Most providers time out at 10-30 seconds and will retry, causing duplicate processing. Enqueue events into a background job queue for actual processing.
- **Always verify signatures** before processing any webhook payload. Use the provider's signing secret and a constant-time comparison function. Never skip verification, even in development.
- **Implement idempotency with event IDs.** Store the provider's delivery/event ID in a database and check for duplicates before processing. Use `INSERT ... ON CONFLICT DO NOTHING` for atomic deduplication.
- **Use a dead letter queue** for events that fail processing after all retries. Monitor DLQ depth and set up alerts. Provide tooling to replay events from the DLQ after fixing bugs.
- **Subscribe only to events you handle.** Receiving events you don't process wastes bandwidth and creates noise in logs. Most providers let you select specific event types during webhook configuration.
- **Protect against replay attacks** by checking the event timestamp. Reject events older than 5 minutes (configurable based on your tolerance). Stripe, GitHub, and most providers include a timestamp in the signature header for this purpose.

## Edge Cases

- **Out-of-order delivery:** Webhooks can arrive out of order (e.g., `invoice.paid` before `invoice.created`). Use event timestamps and the resource's current state (fetched via API) to make decisions rather than assuming sequential delivery.
- **Provider retries during deployments:** If your server is down during a deployment, the provider will retry. Ensure your idempotency logic handles receiving the same event after your server recovers. Use rolling deployments so at least one instance is always available.
- **Payload size limits:** Some providers send large payloads (especially for diff-heavy GitHub push events). Set appropriate body size limits on your endpoint (e.g., 10MB) and handle `413 Payload Too Large` gracefully.
- **Secret rotation:** When rotating webhook signing secrets, support both the old and new secrets during the transition period. Verify against the new secret first, falling back to the old secret. Remove the old secret after confirming all deliveries use the new one.
- **Endpoint URL changes:** If you need to change your webhook URL, register the new URL before deregistering the old one. Run both endpoints in parallel until the provider confirms deliveries to the new URL succeed.
- **Testing locally:** Use ngrok, Cloudflare Tunnel, or the provider's CLI (e.g., `stripe listen --forward-to localhost:3000/webhooks/stripe`) to forward webhooks to your local development server.
