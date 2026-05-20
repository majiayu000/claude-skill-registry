---
name: terra-webhooks
description: Terra API webhook handling for real-time health data. Use when setting up webhook endpoints, verifying signatures, handling events, or debugging webhook issues.
---

# Terra Webhooks

Handle real-time health data delivery from Terra API.

## Quick Start

```python
from flask import Flask, request
import hmac
import hashlib

app = Flask(__name__)

TERRA_SIGNING_SECRET = "your_signing_secret_from_dashboard"

@app.route("/webhooks/terra", methods=["POST"])
def handle_terra_webhook():
    # 1. Verify signature
    signature = request.headers.get("terra-signature")
    if not verify_signature(signature, request.get_data()):
        return "Invalid signature", 401

    # 2. Parse payload
    payload = request.get_json()
    event_type = payload.get("type")

    # 3. Handle event
    if event_type == "activity":
        handle_activity(payload)
    elif event_type == "sleep":
        handle_sleep(payload)
    elif event_type == "auth":
        handle_user_connected(payload)

    # 4. Respond immediately
    return "OK", 200

def verify_signature(header: str, body: bytes) -> bool:
    """Verify Terra webhook signature."""
    parts = dict(p.split("=") for p in header.split(","))
    timestamp = parts["t"]
    signature = parts["v1"]

    message = f"{timestamp}.{body.decode()}"
    expected = hmac.new(
        TERRA_SIGNING_SECRET.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected, signature)
```

## Webhook Event Types

### Authentication Events

| Event | Description |
|-------|-------------|
| `auth` | User successfully connected |
| `deauth` | User disconnected |
| `user_reauth` | User re-authenticated |
| `access_revoked` | Provider revoked access |
| `connection_error` | Connection failed |

### Data Events

| Event | Description |
|-------|-------------|
| `activity` | New workout/activity data |
| `sleep` | New sleep session data |
| `body` | Body metrics update |
| `daily` | Daily summary update |
| `nutrition` | Nutrition/meal data |
| `menstruation` | Cycle tracking data |
| `athlete` | User profile update |

### Processing Events

| Event | Description |
|-------|-------------|
| `processing` | Data is being processed |
| `large_request_processing` | Large request in progress |
| `large_request_sending` | Large request sending chunks |

## Event Payloads

### `auth` - User Connected
```json
{
  "type": "auth",
  "user": {
    "user_id": "terra_abc123",
    "provider": "FITBIT",
    "reference_id": "user_12345",
    "scopes": ["activity", "sleep", "body"]
  },
  "status": "authenticated"
}
```

### `activity` - Workout Data
```json
{
  "type": "activity",
  "user": {
    "user_id": "terra_abc123",
    "provider": "GARMIN",
    "reference_id": "user_12345"
  },
  "data": [{
    "metadata": {
      "start_time": "2025-12-05T07:00:00Z",
      "end_time": "2025-12-05T08:00:00Z",
      "type": "running"
    },
    "calories_data": {
      "total_burned_calories": 450
    },
    "heart_rate_data": {
      "summary": { "avg_hr_bpm": 145, "max_hr_bpm": 175 }
    },
    "distance_data": { "distance_meters": 8500 }
  }]
}
```

### `sleep` - Sleep Data
```json
{
  "type": "sleep",
  "user": {
    "user_id": "terra_abc123",
    "provider": "OURA"
  },
  "data": [{
    "metadata": {
      "start_time": "2025-12-04T22:30:00Z",
      "end_time": "2025-12-05T06:30:00Z"
    },
    "sleep_durations_data": {
      "sleep_efficiency": 0.92
    },
    "asleep": {
      "duration_deep_sleep_state_seconds": 5400,
      "duration_REM_sleep_state_seconds": 6600
    }
  }]
}
```

### `daily` - Daily Summary
```json
{
  "type": "daily",
  "user": {
    "user_id": "terra_abc123",
    "provider": "FITBIT"
  },
  "data": [{
    "metadata": {
      "start_time": "2025-12-05T00:00:00Z",
      "end_time": "2025-12-05T23:59:59Z"
    },
    "movement_data": { "steps_count": 10500 },
    "calories_data": { "total_burned_calories": 2400 }
  }]
}
```

### `deauth` - User Disconnected
```json
{
  "type": "deauth",
  "user": {
    "user_id": "terra_abc123",
    "provider": "FITBIT"
  },
  "status": "deauthenticated"
}
```

## Operations

### `setup-webhook-endpoint`
Create a production-ready webhook handler.

```python
from flask import Flask, request
from celery import Celery
import hmac
import hashlib
import logging

app = Flask(__name__)
celery = Celery()
logger = logging.getLogger(__name__)

TERRA_SIGNING_SECRET = "your_signing_secret"

# Terra webhook source IPs (for additional security)
TERRA_IPS = [
    "18.133.218.210", "18.169.82.189", "18.132.162.19",
    "18.130.218.186", "13.43.183.154", "3.11.208.36",
    "35.214.201.105", "35.214.230.71", "35.214.252.53", "35.214.229.114"
]

@app.route("/webhooks/terra", methods=["POST"])
def terra_webhook():
    # Optional: IP whitelist check
    client_ip = request.remote_addr
    if client_ip not in TERRA_IPS:
        logger.warning(f"Webhook from unknown IP: {client_ip}")
        # Consider: return "Forbidden", 403

    # Verify signature
    signature = request.headers.get("terra-signature")
    raw_body = request.get_data()

    if not signature or not verify_signature(signature, raw_body):
        logger.error("Invalid webhook signature")
        return "Invalid signature", 401

    # Parse and queue for async processing
    payload = request.get_json()
    process_webhook.delay(payload)

    # Respond immediately (within 5 seconds)
    return "OK", 200

def verify_signature(header: str, body: bytes) -> bool:
    """HMAC-SHA256 signature verification."""
    try:
        parts = dict(p.split("=") for p in header.split(","))
        timestamp = parts["t"]
        signature = parts["v1"]

        message = f"{timestamp}.{body.decode()}"
        expected = hmac.new(
            TERRA_SIGNING_SECRET.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()

        # Constant-time comparison to prevent timing attacks
        return hmac.compare_digest(expected, signature)
    except Exception as e:
        logger.error(f"Signature verification error: {e}")
        return False

@celery.task
def process_webhook(payload: dict):
    """Async webhook processing."""
    event_type = payload.get("type")
    user = payload.get("user", {})

    logger.info(f"Processing {event_type} for user {user.get('user_id')}")

    handlers = {
        "auth": handle_auth,
        "deauth": handle_deauth,
        "activity": handle_activity,
        "sleep": handle_sleep,
        "body": handle_body,
        "daily": handle_daily,
        "nutrition": handle_nutrition,
    }

    handler = handlers.get(event_type)
    if handler:
        handler(payload)
    else:
        logger.warning(f"Unknown event type: {event_type}")
```

### `handle-data-events`
Process incoming health data.

```python
def handle_activity(payload: dict):
    """Handle activity/workout data."""
    user_id = payload["user"]["user_id"]

    for activity in payload.get("data", []):
        metadata = activity["metadata"]
        unique_key = f"{user_id}:{metadata['start_time']}:{metadata['end_time']}"

        # Insert if not exists (activities are unique sessions)
        db.activities.update_one(
            {"_id": unique_key},
            {"$setOnInsert": activity},
            upsert=True
        )

        logger.info(f"Processed activity: {metadata['type']}")

def handle_daily(payload: dict):
    """Handle daily summary data."""
    user_id = payload["user"]["user_id"]

    for daily in payload.get("data", []):
        date = daily["metadata"]["start_time"][:10]  # YYYY-MM-DD

        # UPSERT - daily data updates multiple times per day
        db.daily.update_one(
            {"user_id": user_id, "date": date},
            {"$set": daily},
            upsert=True
        )

        logger.info(f"Updated daily for {date}")

def handle_sleep(payload: dict):
    """Handle sleep data."""
    user_id = payload["user"]["user_id"]

    for sleep in payload.get("data", []):
        metadata = sleep["metadata"]
        unique_key = f"{user_id}:{metadata['start_time']}:{metadata['end_time']}"

        db.sleep.update_one(
            {"_id": unique_key},
            {"$setOnInsert": sleep},
            upsert=True
        )

def handle_body(payload: dict):
    """Handle body metrics data."""
    user_id = payload["user"]["user_id"]

    for body in payload.get("data", []):
        date = body["metadata"]["start_time"][:10]

        # UPSERT - body data updates multiple times per day
        db.body.update_one(
            {"user_id": user_id, "date": date},
            {"$set": body},
            upsert=True
        )
```

### `handle-auth-events`
Process connection lifecycle events.

```python
def handle_auth(payload: dict):
    """Handle new user connection."""
    user = payload["user"]

    # Store Terra user mapping
    db.terra_users.insert_one({
        "terra_user_id": user["user_id"],
        "provider": user["provider"],
        "reference_id": user["reference_id"],
        "scopes": user.get("scopes", []),
        "connected_at": datetime.now(),
        "status": "active"
    })

    # Trigger historical data backfill
    trigger_backfill.delay(user["user_id"])

    logger.info(f"User connected: {user['user_id']} via {user['provider']}")

def handle_deauth(payload: dict):
    """Handle user disconnection."""
    user = payload["user"]

    # Mark as disconnected
    db.terra_users.update_one(
        {"terra_user_id": user["user_id"]},
        {"$set": {"status": "disconnected", "disconnected_at": datetime.now()}}
    )

    logger.info(f"User disconnected: {user['user_id']}")
```

### `verify-signature`
Signature verification utility.

```python
import hmac
import hashlib

def verify_terra_signature(
    signature_header: str,
    raw_body: bytes,
    signing_secret: str
) -> bool:
    """
    Verify Terra webhook signature.

    Header format: terra-signature: t=1234567890,v1=abc123...

    Args:
        signature_header: The terra-signature header value
        raw_body: Raw request body (bytes)
        signing_secret: Your signing secret from Terra dashboard

    Returns:
        bool: True if signature is valid
    """
    try:
        # Parse header
        parts = {}
        for part in signature_header.split(","):
            key, value = part.split("=", 1)
            parts[key] = value

        timestamp = parts["t"]
        signature = parts["v1"]

        # Compute expected signature
        message = f"{timestamp}.{raw_body.decode()}"
        expected = hmac.new(
            signing_secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()

        # Constant-time comparison
        return hmac.compare_digest(expected, signature)

    except Exception:
        return False
```

## Retry Logic

Terra retries failed webhooks:

| Attempt | Delay |
|---------|-------|
| 1 | Immediate |
| 2 | ~30 seconds |
| 3 | ~2 minutes |
| 4 | ~10 minutes |
| 5 | ~30 minutes |
| 6 | ~2 hours |
| 7 | ~8 hours |
| 8 | ~24 hours |

**Total**: ~8 retries over 24+ hours

**Failure conditions**:
- Non-2XX response
- Timeout (>5 seconds recommended)
- Connection error

## Idempotency

Handle duplicate webhooks safely:

```python
def handle_webhook_idempotent(payload: dict):
    """Process webhook with idempotency."""

    # Generate idempotency key
    user_id = payload["user"]["user_id"]
    event_type = payload["type"]

    if event_type in ["activity", "sleep"]:
        # Session-based: use start+end time
        data = payload["data"][0]
        key = f"{user_id}:{data['metadata']['start_time']}:{data['metadata']['end_time']}"
    elif event_type in ["daily", "body"]:
        # Date-based: use date
        data = payload["data"][0]
        key = f"{user_id}:{data['metadata']['start_time'][:10]}"
    else:
        # Auth events: use user_id + type + timestamp
        key = f"{user_id}:{event_type}:{datetime.now().isoformat()}"

    # Check if already processed
    if db.processed_webhooks.find_one({"_id": key}):
        logger.info(f"Duplicate webhook skipped: {key}")
        return

    # Process and mark as done
    process_event(payload)
    db.processed_webhooks.insert_one({"_id": key, "processed_at": datetime.now()})
```

## Testing Webhooks

### Local Development with ngrok

```bash
# Install ngrok
npm install -g ngrok

# Start your server
python app.py  # Running on localhost:5000

# Expose with ngrok
ngrok http 5000

# Use ngrok URL in Terra dashboard
# https://abc123.ngrok.io/webhooks/terra
```

### Testing with curl

```bash
# Simulate webhook (without signature)
curl -X POST http://localhost:5000/webhooks/terra \
  -H "Content-Type: application/json" \
  -d '{
    "type": "activity",
    "user": {"user_id": "test123", "provider": "FITBIT"},
    "data": [{"metadata": {"type": "running"}}]
  }'
```

### Webhook.site Testing

1. Go to https://webhook.site
2. Copy your unique URL
3. Add to Terra dashboard as webhook destination
4. Connect a test user and observe payloads

## IP Whitelisting

Terra webhooks come from these IPs:

```python
TERRA_IPS = [
    "18.133.218.210",
    "18.169.82.189",
    "18.132.162.19",
    "18.130.218.186",
    "13.43.183.154",
    "3.11.208.36",
    "35.214.201.105",
    "35.214.230.71",
    "35.214.252.53",
    "35.214.229.114"
]
```

## Dashboard Configuration

1. Go to Terra Dashboard → Destinations → Webhooks
2. Add your webhook URL (must be HTTPS in production)
3. Copy the signing secret for signature verification
4. Select which events to receive

## Related Skills

- **terra-auth**: Get signing secret
- **terra-connections**: Handle auth/deauth events
- **terra-data**: Data schema reference
- **terra-troubleshooting**: Debug webhook issues
