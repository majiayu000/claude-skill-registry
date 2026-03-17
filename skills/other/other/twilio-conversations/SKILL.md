---
name: twilio-conversations
cluster: twilio
description: "Unified: omnichannel SMS+WhatsApp+chat, conversation/participant/message management, webhooks"
tags: ["conversations","omnichannel","twilio"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "twilio conversations omnichannel sms whatsapp chat unified participant"
---

# twilio-conversations

## Purpose

Enable OpenClaw to implement and operate Twilio Conversations in production: create/manage conversations, participants, and messages across SMS/WhatsApp/chat; integrate webhooks for delivery/read/failure; enforce opt-out and compliance; and compose with Twilio Programmable Messaging/Voice/Verify/Studio/SendGrid patterns.

Concrete engineer value:

- Build a unified “thread” abstraction across channels (SMS, WhatsApp, in-app chat) with consistent participant/message APIs.
- Implement reliable webhook-driven state (delivery/read/failure) with idempotency, retries, and backpressure.
- Operate at scale: rate limits, pagination, cost controls (Messaging Services, geo-matching), and compliance (STOP, 10DLC, toll-free).
- Provide production-grade observability and incident response playbooks for Twilio error codes and webhook failures.

---

## Prerequisites

### Accounts & Twilio setup

- Twilio account with Conversations enabled.
- At least one of:
  - SMS-capable phone number (10DLC registered for US A2P where applicable)
  - WhatsApp sender (WhatsApp Business API via Twilio)
  - Messaging Service (recommended for scale/cost controls)
- Webhook endpoint reachable from Twilio (public HTTPS). For local dev: `ngrok` or `cloudflared`.

### Runtime versions (tested)

- Node.js: **20.11.1** (LTS)
- Python: **3.11.7**
- Twilio Node SDK: **4.23.0**
- Twilio Python SDK: **9.4.1**
- OpenSSL: **1.1.1w** or **3.0.13** (platform dependent)
- Docker: **25.0.3** (optional)
- PostgreSQL: **15.5** (optional, for webhook/event persistence)
- Redis: **7.2.4** (optional, for idempotency keys / rate limiting)

### OS support

- Ubuntu 22.04 LTS (x86_64, arm64)
- Fedora 39 (x86_64)
- macOS 14 Sonoma (Intel + Apple Silicon)

### Auth setup

Use Twilio API Key (recommended) instead of Account SID + Auth Token for production services.

1. Create API Key:
   - Twilio Console → Account → API keys & tokens → Create API key
2. Store:
   - `TWILIO_ACCOUNT_SID` (starts with `AC...`)
   - `TWILIO_API_KEY_SID` (starts with `SK...`)
   - `TWILIO_API_KEY_SECRET`

Environment variables (example):

```bash
export TWILIO_ACCOUNT_SID="YOUR_ACCOUNT_SID"
export TWILIO_API_KEY_SID="YOUR_API_KEY_SID"
export TWILIO_API_KEY_SECRET="YOUR_API_KEY_SECRET"
```

If you must use Auth Token (legacy):

```bash
export TWILIO_AUTH_TOKEN="your_auth_token"
```

### Network & firewall

- Allow outbound HTTPS to `api.twilio.com` and `conversations.twilio.com`.
- Inbound webhook endpoint must accept Twilio IP ranges (or validate signatures; prefer signature validation over IP allowlists).

---

## Core Concepts

### Conversations mental model

- **Conversation**: a thread container. Has a `sid` (`CH...`), `uniqueName`, attributes, timers, and state.
- **Participant**: an entity in a conversation. Types:
  - **Chat participant** (identity-based): `identity="user-123"`
  - **Messaging participant** (phone-based): `messagingBinding.address="+14155550100"` and `proxyAddress` (Twilio number or Messaging Service sender)
  - **WhatsApp participant**: address like `whatsapp:+14155550100`
- **Message**: content sent within a conversation. Has author, body, media, attributes, and delivery receipts (channel dependent).
- **Webhook events**: Twilio sends HTTP callbacks for conversation/message/participant lifecycle and delivery status.

### Architecture overview (production)

1. **Ingress**:
   - Inbound SMS/WhatsApp hits Programmable Messaging webhook.
   - In-app chat uses Conversations SDK (web/mobile) or REST API.
2. **Routing**:
   - Map inbound message to a Conversation (by phone number, identity, or business key).
   - Add/ensure participants.
3. **Egress**:
   - Send messages via Conversations API (preferred for unified thread) or Messaging API (for non-threaded blasts).
4. **State & observability**:
   - Persist webhook events (append-only) and derive state (delivery, read, failed).
   - Idempotency keys to handle Twilio retries.
5. **Compliance**:
   - STOP/START/HELP handling (Messaging compliance) and participant removal/blacklist.
   - 10DLC/toll-free verification for US traffic; WhatsApp template rules.

### Key identifiers

- Account SID: `AC...`
- Conversation SID: `CH...`
- Participant SID: `MB...` (varies)
- Message SID: `IM...`
- Service SID (Conversations Service): `IS...` (if using Services)
- Messaging Service SID: `MG...`

### Webhook signature validation

Twilio signs webhook requests with `X-Twilio-Signature`. Validate using the exact URL Twilio called (including query string) and the POST params.

---

## Installation & Setup

### Official Python SDK — Conversations

**Repository:** https://github.com/twilio/twilio-python  
**PyPI:** `pip install twilio` · **Supported:** Python 3.7–3.13

```python
from twilio.rest import Client
client = Client()

# Create conversation
conv = client.conversations.v1.conversations.create(
    friendly_name="Support Chat #123"
)

# Add participant (SMS)
p = client.conversations.v1.conversations(conv.sid) \
    .participants.create(
        messaging_binding_address="+15558675309",
        messaging_binding_proxy_address="+15017250604"
    )

# Send message
client.conversations.v1.conversations(conv.sid) \
    .messages.create(body="Welcome to support chat!", author="system")
```

Source: [twilio/twilio-python — conversations](https://github.com/twilio/twilio-python/blob/main/twilio/rest/conversations/)

### 1) System dependencies

#### Ubuntu 22.04

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg jq
```

Node.js 20.11.1 via NodeSource:

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
node -v  # v20.11.1 (or newer 20.x)
npm -v
```

Python 3.11:

```bash
sudo apt-get install -y python3.11 python3.11-venv python3-pip
python3.11 --version
```

#### Fedora 39

```bash
sudo dnf install -y jq curl ca-certificates
sudo dnf module install -y nodejs:20
node -v
sudo dnf install -y python3.11 python3.11-pip
python3.11 --version
```

#### macOS 14 (Intel/Apple Silicon)

Homebrew:

```bash
brew update
brew install jq node@20 python@3.11
node -v
python3.11 --version
```

### 2) Project dependencies

#### Node (recommended for webhook services)

```bash
mkdir -p twilio-conversations-service && cd twilio-conversations-service
npm init -y
npm install twilio@4.23.0 express@4.18.3 body-parser@1.20.2 pino@9.0.0 pino-http@9.0.0
npm install --save-dev typescript@5.3.3 ts-node@10.9.2 @types/express@4.17.21 @types/node@20.11.19
```

#### Python (batch jobs / admin tooling)

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip==24.0
pip install twilio==9.4.1 requests==2.31.0
```

### 3) Webhook endpoint (Express) with signature validation

Create `src/server.ts`:

```ts
import express from "express";
import bodyParser from "body-parser";
import pinoHttp from "pino-http";
import twilio from "twilio";

const app = express();
app.use(pinoHttp());

// Twilio signature validation requires the raw body for some frameworks.
// For Express with urlencoded, Twilio helper can validate using parsed params.
// Ensure you use the exact URL configured in Twilio Console.
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

const {
  TWILIO_AUTH_TOKEN,
  PUBLIC_WEBHOOK_BASE_URL,
} = process.env;

if (!TWILIO_AUTH_TOKEN) throw new Error("TWILIO_AUTH_TOKEN is required for webhook signature validation");
if (!PUBLIC_WEBHOOK_BASE_URL) throw new Error("PUBLIC_WEBHOOK_BASE_URL is required (e.g., https://example.com)");

app.post("/twilio/conversations/webhook", (req, res) => {
  const signature = req.header("X-Twilio-Signature") || "";
  const url = `${PUBLIC_WEBHOOK_BASE_URL}/twilio/conversations/webhook`;

  const isValid = twilio.validateRequest(
    TWILIO_AUTH_TOKEN,
    signature,
    url,
    req.body
  );

  if (!isValid) {
    req.log.warn({ signature }, "Invalid Twilio signature");
    return res.status(403).send("Forbidden");
  }

  // Idempotency: Twilio may retry. Use EventSid or MessageSid as a dedupe key.
  const eventType = req.body.EventType;
  const eventSid = req.body.EventSid;
  req.log.info({ eventType, eventSid, body: req.body }, "Twilio Conversations webhook");

  // TODO: enqueue to a worker; respond fast.
  res.status(200).send("ok");
});

const port = Number(process.env.PORT || 3000);
app.listen(port, () => {
  // eslint-disable-next-line no-console
  console.log(`listening on :${port}`);
});
```

Run:

```bash
npx ts-node src/server.ts
```

Expose with ngrok:

```bash
ngrok http 3000
# Set PUBLIC_WEBHOOK_BASE_URL to the https URL ngrok gives you
```

### 4) Configure Conversations webhooks

In Twilio Console:
- Conversations → Services → (your service) → Webhooks
- Configure:
  - **Pre-event Webhook** (optional; for authorization/routing decisions)
  - **Post-event Webhook** (recommended; for event ingestion)
- Point to:
  - `https://your-domain.example.com/twilio/conversations/webhook`

For inbound SMS/WhatsApp into Conversations, also configure Programmable Messaging inbound webhook to your app if you’re doing custom mapping, or use Conversations’ messaging bindings (preferred).

---

## Key Capabilities

### Create and manage Conversations

- Create conversation with `uniqueName` for idempotent lookup.
- Set `attributes` JSON for business metadata (tenantId, caseId, SLA).
- Control lifecycle: `state` (active/inactive/closed), timers, and cleanup.

### Add participants (chat + messaging + WhatsApp)

- Chat participants by `identity` (for SDK users).
- Messaging participants by `messagingBinding.address` and `proxyAddress` (Twilio sender).
- WhatsApp addresses use `whatsapp:+E164`.

Production patterns:
- Always ensure a deterministic mapping from business entity → conversation uniqueName.
- Enforce participant limits and blocklists before adding.

### Send messages with delivery tracking

- Send message with `author` and `body`.
- Attach `attributes` for correlation IDs.
- Track delivery via webhook events and/or message status callbacks (channel dependent).

### Webhooks: event ingestion, retries, idempotency

- Validate `X-Twilio-Signature`.
- Respond within 5 seconds; enqueue work.
- Dedupe by `EventSid` (preferred) or `(MessageSid, EventType, Timestamp)`.

### Compliance: STOP/START/HELP and opt-out

- For SMS/WhatsApp, STOP handling is primarily a Programmable Messaging concern.
- If you ingest inbound messages into Conversations, you must still respect opt-out:
  - Maintain a suppression list keyed by phone number.
  - On STOP, remove participant or mark as blocked; prevent outbound.

### Cost optimization with Messaging Services

- Use Messaging Service with:
  - Geo-matching
  - Sticky sender
  - Smart encoding
- For Conversations messaging participants, set `proxyAddress` to a Twilio number; for large scale, prefer Messaging Service where supported by your design (often via Messaging API for outbound, while keeping Conversations as system-of-record).

### Compose with Voice/Verify/Studio/SendGrid

- Escalate a conversation to Voice (Dial/Conference) and post call artifacts back into the conversation.
- Use Verify for step-up auth before adding a participant or revealing sensitive info.
- Trigger Studio flows on conversation events.
- Send SendGrid transactional emails and mirror them into the conversation as messages/attributes.

---

## Command Reference

This skill assumes OpenClaw can execute via:
- Twilio SDKs (Node/Python)
- Direct REST calls (curl)
- Twilio CLI (optional; limited Conversations coverage)

### REST API base

- Conversations API base: `https://conversations.twilio.com/v1`

Auth options:
- Basic auth with API Key:
  - username: `TWILIO_API_KEY_SID`
  - password: `TWILIO_API_KEY_SECRET`
- Or Account SID + Auth Token.

#### curl helper (API Key)

```bash
export TWILIO_API_KEY_SID="YOUR_API_KEY_SID"
export TWILIO_API_KEY_SECRET="YOUR_API_KEY_SECRET"
export TWILIO_ACCOUNT_SID="YOUR_ACCOUNT_SID"
```

### Conversations

#### Create conversation

Endpoint:
- `POST /v1/Conversations`

Flags/fields:
- `FriendlyName` (string)
- `UniqueName` (string; use for idempotency)
- `Attributes` (stringified JSON)
- `MessagingServiceSid` (string; optional)
- `State` (`active|inactive|closed`)
- `Timers.Inactive` (ISO-8601 duration string, e.g. `PT1H`) depending on API support

curl:

```bash
curl -sS -X POST "https://conversations.twilio.com/v1/Conversations" \
  -u "$TWILIO_API_KEY_SID:$TWILIO_API_KEY_SECRET" \
  --data-urlencode "FriendlyName=Support Case 10492" \
  --data-urlencode "UniqueName=case-10492" \
  --data-urlencode 'Attributes={"tenantId":"acme","caseId":10492,"priority":"p1"}'
```

Node:

```js
import twilio from "twilio";

const client = twilio(process.env.TWILIO_API_KEY_SID, process.env.TWILIO_API_KEY_SECRET, {
  accountSid: process.env.TWILIO_ACCOUNT_SID,
});

const conv = await client.conversations.v1.conversations.create({
  friendlyName: "Support Case 10492",
  uniqueName: "case-10492",
  attributes: JSON.stringify({ tenantId: "acme", caseId: 10492, priority: "p1" }),
});
console.log(conv.sid);
```

#### Fetch conversation

- `GET /v1/Conversations/{ConversationSid}`

```bash
curl -sS "https://conversations.twilio.com/v1/Conversations/CHXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" \
  -u "$TWILIO_API_KEY_SID:$TWILIO_API_KEY_SECRET"
```

#### List conversations (pagination)

- `GET /v1/Conversations?PageSize=50&PageToken=...`

Query params:
- `PageSize` (1–1000; practical: 50–200)
- `PageToken` (string)
- `State` filter may be available depending on API version

```bash
curl -sS "https://conversations.twilio.com/v1/Conversations?PageSize=50" \
  -u "$TWILIO_API_KEY_SID:$TWILIO_API_KEY_SECRET"
```

#### Update conversation

- `POST /v1/Conversations/{ConversationSid}`

Fields:
- `FriendlyName`
- `Attributes` (stringified JSON)
- `State`

```bash
curl -sS -X POST "https://conversations.twilio.com/v1/Conversations/CHXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" \
  -u "$TWILIO_API_KEY_SID:$TWILIO_API_KEY_SECRET" \
  --data-urlencode "State=closed" \
  --data-urlencode 'Attributes={"tenantId":"acme","caseId":10492,"priority":"p1","closedBy":"agent-7"}'
```

#### Delete conversation

- `DELETE /v1/Conversations/{ConversationSid}`

```bash
curl -sS -X DELETE "https://conversations.twilio.com/v1/Conversations/CHXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" \
  -u "$TWILIO_API_KEY_SID:$TWILIO_API_KEY_SECRET"
```

### Participants

#### Add chat participant (identity)

- `POST /v1/Conversations/{ConversationSid}/Participants`

Fields:
- `Identity` (string)
- `Attributes` (stringified JSON)

```bash
curl -sS -X POST "https://conversations.twilio.com/v1/Conversations/CH.../Participants" \
  -u "$TWILIO_API_KEY_SID:$TWILIO_API_KEY_SECRET" \
  --data-urlencode "Identity=user-123" \
  --data-urlencode 'Attributes={"role":"customer"}'
```

#### Add messaging participant (SMS)

Fields:
- `MessagingBinding.Address` (E.164, e.g. `+14155550100`)
- `MessagingBinding.ProxyAddress` (Twilio number in E.164, e.g. `+14155551234`)
- `Attributes`

```bash
curl -sS -X POST "https://conversations.twilio.com/v1/Conversations/CH.../Participants" \
  -u "$TWILIO_API_KEY_SID:$TWILIO_API_KEY_SECRET" \
  --data-urlencode "MessagingBinding.Address=+14155550100" \
  --data-urlencode "MessagingBinding.ProxyAddress=+14155551234" \
  --data-urlencode 'Attributes={"role":"customer","channel":"sms"}'
```

#### Add messaging participant (WhatsApp)

Use `whatsapp:` prefix:

```bash
curl -sS -X POST "https://conversations.twilio.com/v1/Conversations/CH.../Participants" \
  -u "$TWILIO_API_KEY_SID:$TWILIO_API_KEY_SECRET" \
  --data-urlencode "MessagingBinding.Address=whatsapp:+14155550100" \
  --data-urlencode "MessagingBinding.ProxyAddress=whatsapp:+14155559876" \
  --data-urlencode 'Attributes={"role":"customer","channel":"whatsapp"}'
```

#### List participants

- `GET /v1/Conversations/{ConversationSid}/Participants?PageSize=50`

```bash
curl -sS "https://conversations.twilio.com/v1/Conversations/CH.../Participants?PageSize=50" \
  -u "$TWILIO_API_KEY_SID:$TWILIO_API_KEY_SECRET"
```

#### Remove participant

- `DELETE /v1/Conversations/{ConversationSid}/Participants/{ParticipantSid}`

```bash
curl -sS -X DELETE "https://conversations.twilio.com/v1/Conversations/CH.../Participants/MB..." \
  -u "$TWILIO_API_KEY_SID:$TWILIO_API_KEY_SECRET"
```

### Messages

#### Send message

- `POST /v1/Conversations/{ConversationSid}/Messages`

Fields:
- `Author` (string; identity or system label)
- `Body` (string)
- `Attributes` (stringified JSON)
- `MediaSid` / media fields (if using media; depends on API)

```bash
curl -sS -X POST "https://conversations.twilio.com/v1/Conversations/CH.../Messages" \
  -u "$TWILIO_API_KEY_SID:$TWILIO_API_KEY_SECRET" \
  --data-urlencode "Author=agent-7" \
  --data-urlencode "Body=We’re looking into this now. ETA 15 minutes." \
  --data-urlencode 'Attributes={"correlationId":"req-01HPQ9K7Z9Y7J8V7Z0","visibility":"customer"}'
```

#### List messages

- `GET /v1/Conversations/{ConversationSid}/Messages?PageSize=50&Order=asc|desc`

```bash
curl -sS "https://conversations.twilio.com/v1/Conversations/CH.../Messages?PageSize=50&Order=desc" \
  -u "$TWILIO_API_KEY_SID:$TWILIO_API_KEY_SECRET"
```

#### Fetch message

- `GET /v1/Conversations/{ConversationSid}/Messages/{MessageSid}`

```bash
curl -sS "https://conversations.twilio.com/v1/Conversations/CH.../Messages/IM..." \
  -u "$TWILIO_API_KEY_SID:$TWILIO_API_KEY_SECRET"
```

#### Delete message (moderation)

- `DELETE /v1/Conversations/{ConversationSid}/Messages/{MessageSid}`

```bash
curl -sS -X DELETE "https://conversations.twilio.com/v1/Conversations/CH.../Messages/IM..." \
  -u "$TWILIO_API_KEY_SID:$TWILIO_API_KEY_SECRET"
```

### Webhooks (Conversations Service)

Conversations commonly uses a **Service** to configure defaults and webhooks.

- List services: `GET /v1/Services`
- Create service: `POST /v1/Services`
- Configure webhooks: `POST /v1/Services/{ServiceSid}/Configuration/Webhooks`

Key fields (vary by webhook type):
- `PostWebhookUrl`
- `PostWebhookMethod` (`GET|POST`)
- `Filters` (array of event types)
- `PreWebhookUrl`, `PreWebhookMethod`
- `WebhookTimeout` (seconds; if supported)

Because webhook configuration fields evolve, prefer SDK typing or console for initial setup; then export config into IaC (Terraform) where possible.

---

## Configuration Reference

### Environment variables

Recommended file: `/etc/openclaw/twilio-conversations.env` (Linux) or `~/.config/openclaw/twilio-conversations.env` (dev)

```bash
TWILIO_ACCOUNT_SID=YOUR_ACCOUNT_SID
TWILIO_API_KEY_SID=YOUR_API_KEY_SID
TWILIO_API_KEY_SECRET=replace_me
TWILIO_AUTH_TOKEN=replace_me_for_webhook_validation_only

PUBLIC_WEBHOOK_BASE_URL=https://conversations-webhooks.acme.example
TWILIO_CONVERSATIONS_SERVICE_SID=YOUR_IS_SID

DEFAULT_PROXY_ADDRESS=+14155551234
DEFAULT_WHATSAPP_PROXY=whatsapp:+14155559876

# Compliance / suppression
SUPPRESSION_REDIS_URL=redis://:redispass@redis-1.internal:6379/2
```

Load with systemd unit:

`/etc/systemd/system/openclaw-twilio-conversations.service`:

```ini
[Unit]
Description=OpenClaw Twilio Conversations Webhook Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
EnvironmentFile=/etc/openclaw/twilio-conversations.env
WorkingDirectory=/opt/openclaw/twilio-conversations
ExecStart=/usr/bin/node dist/server.js
Restart=on-failure
RestartSec=2
User=openclaw
Group=openclaw
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/lib/openclaw /var/log/openclaw

[Install]
WantedBy=multi-user.target
```

### OpenClaw skill config (example)

`/opt/openclaw/config/skills/twilio-conversations.toml`:

```toml
[twilio_conversations]
service_sid = "YOUR_IS_SID"
default_proxy_address = "+14155551234"
default_whatsapp_proxy = "whatsapp:+14155559876"

[twilio_conversations.webhooks]
public_base_url = "https://conversations-webhooks.acme.example"
path = "/twilio/conversations/webhook"
validate_signature = true
max_processing_ms = 2000

[twilio_conversations.idempotency]
backend = "redis"
redis_url = "redis://:redispass@redis-1.internal:6379/2"
ttl_seconds = 86400

[twilio_conversations.compliance]
enforce_stop = true
stop_keywords = ["STOP", "STOPALL", "UNSUBSCRIBE", "CANCEL", "END", "QUIT"]
start_keywords = ["START", "YES", "UNSTOP"]
help_keywords = ["HELP", "INFO"]
```

### NGINX reverse proxy

`/etc/nginx/conf.d/openclaw-twilio-conversations.conf`:

```nginx
server {
  listen 443 ssl http2;
  server_name conversations-webhooks.acme.example;

  ssl_certificate     /etc/letsencrypt/live/conversations-webhooks.acme.example/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/conversations-webhooks.acme.example/privkey.pem;

  client_max_body_size 1m;

  location /twilio/conversations/webhook {
    proxy_pass http://127.0.0.1:3000/twilio/conversations/webhook;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

    proxy_connect_timeout 2s;
    proxy_read_timeout 5s;
    proxy_send_timeout 5s;
  }
}
```

---

## Integration Patterns

### Pattern: Inbound SMS → map to Conversation → agent reply

Pipeline:

1. Programmable Messaging inbound webhook receives SMS.
2. Lookup/create conversation by `uniqueName = "sms:+14155550100"` (or tenant-scoped).
3. Ensure messaging participant exists with `MessagingBinding.Address` = sender.
4. Post inbound message into conversation (author = phone).
5. Agent replies via Conversations message API.

Key detail: inbound SMS already exists as a Messaging event; you’re mirroring into Conversations for unified thread. Ensure you don’t double-send outbound.

### Pattern: Conversations as system-of-record + Messaging Service for outbound

- Store all messages in Conversations for UI/history.
- For outbound SMS at scale, send via Messaging API using `MessagingServiceSid=MG...` for geo-matching and throughput.
- Mirror outbound message into Conversations with attributes linking to Messaging `MessageSid`.

This avoids sender management complexity while keeping a single thread.

### Pattern: Verify before adding a new phone participant

- User requests to add phone number to a conversation.
- Trigger Verify V2 SMS to that number.
- Only after successful verification, add as messaging participant.

### Pattern: Escalate to Voice and attach call recording/transcript

- When conversation hits escalation keyword, create a Voice call (TwiML Dial/Conference).
- Enable recording and transcription.
- Post recording URL/transcript back into conversation as a message or as conversation attributes.

### Pattern: Studio flow triggered by conversation events

- Post-event webhook ingests `onMessageAdded`.
- For certain intents, call Studio REST Trigger API to run a flow.
- Flow can send messages back via Conversations or Messaging.

---

## Error Handling & Troubleshooting

Handle Twilio errors by code + HTTP status + retryability. Always log:
- Twilio `X-Twilio-Request-Id`
- HTTP status
- error code/message
- relevant SIDs

### 1) Auth failure (20003)

Error (typical):

- HTTP 401
- Body includes:
  - `"code": 20003`
  - `"message": "Authenticate"`

Root cause:
- Wrong API key secret, wrong auth token, or using API key without `accountSid` in SDK config.

Fix:
- Verify `TWILIO_API_KEY_SID/SECRET`.
- In Node SDK, pass `{ accountSid: TWILIO_ACCOUNT_SID }` when using API keys.
- Rotate compromised keys.

### 2) Rate limiting (20429)

Error:

- HTTP 429
- `"code": 20429`
- `"message": "Too Many Requests"`

Root cause:
- Burst traffic exceeding Twilio API limits or your account’s concurrency.

Fix:
- Implement exponential backoff with jitter (e.g., base 250ms, max 5s).
- Queue writes; batch list operations; reduce `PageSize` if timeouts occur.
- Use worker concurrency caps per account/service.

### 3) Invalid phone number (21211)

Error:

- HTTP 400
- `"code": 21211`
- `"message": "The 'To' number +1415555 is not a valid phone number."`

Root cause:
- Non-E.164 formatting, missing country code, invalid characters.

Fix:
- Normalize to E.164 before adding messaging participants.
- Use libphonenumber in your app layer.
- Reject early with actionable error.

### 4) Messaging delivery failure (30003)

Error (Messaging status callback):

- `"ErrorCode": "30003"`
- `"MessageStatus": "undelivered"`
- `"ErrorMessage": "Unreachable destination handset."` (carrier-dependent)

Root cause:
- Carrier unreachable, handset off, blocked, or invalid route.

Fix:
- Mark participant as unreachable; fall back to alternate channel (WhatsApp/email/voice).
- Retry policy: limited retries; avoid infinite loops.
- For WhatsApp, ensure templates and opt-in.

### 5) Webhook signature validation failures

Log:

- `Invalid Twilio signature`

Root cause:
- `PUBLIC_WEBHOOK_BASE_URL` mismatch with actual URL Twilio calls (scheme/host/path).
- NGINX rewriting path or missing query string in validation URL.
- Using JSON body parsing when Twilio sends `application/x-www-form-urlencoded` (or vice versa).

Fix:
- Ensure the validation URL exactly matches Twilio configuration.
- Preserve original host/proto via `X-Forwarded-*` and reconstruct correctly.
- Confirm content-type and body parsing.

### 6) Participant already exists

Typical API error:

- HTTP 409
- Message similar to:
  - `"message": "Participant already exists"`

Root cause:
- Non-idempotent add participant calls under retries/concurrency.

Fix:
- Treat 409 as success if the participant matches desired binding.
- Use deterministic participant lookup before create (list participants and match by identity/address).
- Serialize participant creation per conversation.

### 7) Conversation not found

Error:

- HTTP 404
- `"message": "The requested resource /Conversations/CH... was not found"`

Root cause:
- Wrong SID, deleted conversation, or cross-account SID.

Fix:
- Validate SID prefix and length.
- Ensure correct account credentials.
- If using `uniqueName`, re-resolve by listing/filtering (or store mapping in DB).

### 8) Webhook timeouts and retries

Symptom:
- Twilio retries same event multiple times; your logs show duplicates.

Root cause:
- Your webhook handler exceeds Twilio timeout or returns non-2xx.
- Downstream dependencies (DB) slow.

Fix:
- Respond 200 immediately after enqueue.
- Use durable queue (SQS/Kafka/RabbitMQ) and process async.
- Implement idempotency with Redis keyed by `EventSid` TTL 24h+.

### 9) WhatsApp template / session issues (common)

Symptom:
- Outbound WhatsApp fails with policy-related error (varies by region/account).

Root cause:
- Attempting to send freeform message outside 24-hour session window; template required.

Fix:
- Use approved templates for re-engagement.
- Track last inbound timestamp per participant; enforce template usage.

### 10) Opt-out violations

Symptom:
- Carrier filtering, complaints, or Twilio compliance warnings.

Root cause:
- Sending SMS after STOP, or failing to honor opt-out across systems.

Fix:
- Central suppression list; check before every outbound.
- On STOP inbound, immediately suppress and confirm opt-out per policy.

---

## Security Hardening

### Secrets management

- Do not store `TWILIO_API_KEY_SECRET` in repo.
- Use:
  - AWS Secrets Manager / GCP Secret Manager / Vault
  - systemd `LoadCredential=` (systemd 252+) where available
- Rotate API keys quarterly; immediately on incident.

### Webhook verification

- Always validate `X-Twilio-Signature`.
- Enforce HTTPS only; redirect HTTP → HTTPS at edge.
- Reject requests with missing signature.

### Least privilege

- Use separate API keys per service (webhooks vs batch jobs).
- Restrict key usage by internal policy (Twilio keys are account-wide; enforce via network segmentation and secret distribution).

### Data minimization

- Avoid storing full message bodies if not required; store hashes/metadata.
- If storing bodies, encrypt at rest (Postgres TDE alternative: disk encryption + app-level envelope encryption).

### CIS-aligned host hardening (practical mapping)

- CIS Ubuntu Linux 22.04 LTS Benchmark:
  - Disable password SSH auth; enforce key-based.
  - Enable automatic security updates.
  - Restrict inbound ports to 443 only for webhook edge.
- Run service as non-root (`openclaw` user).
- systemd sandboxing:
  - `NoNewPrivileges=true`
  - `ProtectSystem=strict`
  - `ProtectHome=true`
  - `PrivateTmp=true`

### Audit logging

- Log all admin actions:
  - conversation create/close/delete
  - participant add/remove
  - outbound message send
- Include correlation IDs and actor identity.

---

## Performance Tuning

### Webhook ingestion latency

Goal: p95 webhook handler < 50ms, always < 500ms.

Optimizations:
- Parse and validate signature, then enqueue and return 200.
- Avoid synchronous DB writes in request thread.

Expected impact:
- Before: p95 800–1500ms under DB contention → Twilio retries.
- After: p95 10–30ms; retries near-zero.

### API rate limiting and batching

- Use `PageSize=200` for list operations to reduce round trips, but watch response size/timeouts.
- Cache conversation SID by `uniqueName` in Redis (TTL 1h) to avoid list/search calls.

Expected impact:
- Reduce Twilio API calls by 60–90% in high-traffic routing services.

### Participant lookup strategy

- Maintain your own mapping table:
  - `(tenantId, externalUserId) -> conversationSid`
  - `(tenantId, phoneE164) -> conversationSid`
- Avoid listing participants/messages to “discover” state.

Expected impact:
- Avoid O(n) scans; stable latency as conversation size grows.

### Message fanout control

If you add many participants (group chats), outbound message fanout can be expensive and slow.

- Enforce max participants per conversation (policy).
- For broadcast, use Messaging API + segmentation rather than a single conversation.

---

## Advanced Topics

### Pre-event webhooks for authorization

Use pre-event webhook to:
- Block participant additions from unknown identities.
- Enforce tenant boundaries (identity must match conversation attributes).
- Reject messages containing disallowed content (PII leakage) before they are accepted.

Implementation notes:
- Pre-event webhook must be highly available; failures can block message flow.
- Return explicit allow/deny per Twilio’s pre-event webhook contract.

### Idempotent conversation creation

Twilio doesn’t guarantee atomic “create if not exists by uniqueName” across concurrent callers.

Pattern:
1. Try create with `UniqueName`.
2. If conflict/duplicate occurs, fetch by `UniqueName` via your mapping DB (preferred) or list/filter (fallback).
3. Store mapping.

### Multi-tenant isolation

- Prefix `uniqueName` with tenant: `t_acme_case_10492`
- Store `tenantId` in `attributes`.
- Validate tenant on every webhook event before processing.

### Message ordering and eventual consistency

- Webhook events can arrive out of order.
- Use event timestamps and message index (if provided) to order.
- Treat webhooks as an event stream; build derived state with replay capability.

### Media handling

- Media messages may require separate retrieval and storage policies.
- Enforce content-type allowlist and size limits.
- Consider virus scanning for inbound media before exposing to internal users.

### Interop with Programmable Messaging status callbacks

You may receive:
- Conversations post-event webhooks (message added)
- Messaging status callbacks (delivered/failed)

Unify by correlating:
- Store Messaging `MessageSid` in Conversations message attributes when you send via Messaging API.
- On status callback, update your internal message state and optionally post a system message into the conversation (or update external UI).

---

## Usage Examples

### Scenario 1: Create conversation for a support case, add SMS customer + chat agent, send initial message

```bash
# 1) Create conversation
CONV_SID=$(curl -sS -X POST "https://conversations.twilio.com/v1/Conversations" \
  -u "$TWILIO_API_KEY_SID:$TWILIO_API_KEY_SECRET" \
  --data-urlencode "FriendlyName=Support Case 10492" \
  --data-urlencode "UniqueName=t_acme_case_10492" \
  --data-urlencode 'Attributes={"tenantId":"acme","caseId":10492,"priority":"p1"}' | jq -r .sid)

echo "$CONV_SID"

# 2) Add SMS participant (customer)
curl -sS -X POST "https://conversations.twilio.com/v1/Conversations/$CONV_SID/Participants" \
  -u "$TWILIO_API_KEY_SID:$TWILIO_API_KEY_SECRET" \
  --data-urlencode "MessagingBinding.Address=+14155550100" \
  --data-urlencode "MessagingBinding.ProxyAddress=+14155551234" \
  --data-urlencode 'Attributes={"role":"customer","channel":"sms"}' | jq .

# 3) Add chat participant (agent)
curl -sS -X POST "https://conversations.twilio.com/v1/Conversations/$CONV_SID/Participants" \
  -u "$TWILIO_API_KEY_SID:$TWILIO_API_KEY_SECRET" \
  --data-urlencode "Identity=agent-7" \
  --data-urlencode 'Attributes={"role":"agent"}' | jq .

# 4) Send message
curl -sS -X POST "https://conversations.twilio.com/v1/Conversations/$CONV_SID/Messages" \
  -u "$TWILIO_API_KEY_SID:$TWILIO_API_KEY_SECRET" \
  --data-urlencode "Author=agent-7" \
  --data-urlencode "Body=Hi—this is Acme Support. We’re on it." \
  --data-urlencode 'Attributes={"correlationId":"req-01HPQ9K7Z9Y7J8V7Z0"}' | jq .
```

### Scenario 2: Inbound STOP handling with suppression list (Redis) and participant removal

Python snippet to process inbound message webhook (from Messaging) and enforce STOP:

```python
import os
import redis
from twilio.rest import Client

STOP_WORDS = {"STOP", "STOPALL", "UNSUBSCRIBE", "CANCEL", "END", "QUIT"}
START_WORDS = {"START", "YES", "UNSTOP"}

r = redis.Redis.from_url(os.environ["SUPPRESSION_REDIS_URL"])
client = Client(os.environ["TWILIO_API_KEY_SID"], os.environ["TWILIO_API_KEY_SECRET"], os.environ["TWILIO_ACCOUNT_SID"])

def handle_inbound_sms(from_e164: str, body: str, conversation_sid: str, participant_sid: str):
    normalized = body.strip().upper()
    key = f"suppress:sms:{from_e164}"

    if normalized in STOP_WORDS:
        r.set(key, "1")
        # Remove participant to prevent further outbound via Conversations
        client.conversations.v1.conversations(conversation_sid).participants(participant_sid).delete()
        return {"action": "suppressed"}

    if normalized in START_WORDS:
        r.delete(key)
        return {"action": "unsuppressed"}

    if r.get(key):
        return {"action": "ignored_suppressed"}

    return {"action": "accepted"}
```

### Scenario 3: Webhook ingestion with idempotency (Redis) keyed by EventSid

Node snippet (core logic):

```js
import Redis from "ioredis";

const redis = new Redis(process.env.SUPPRESSION_REDIS_URL);

export async function dedupeEvent(eventSid) {
  const key = `twilio:event:${eventSid}`;
  const ok = await redis.set(key, "1", "NX", "EX", 86400);
  return ok === "OK"; // true if first time
}
```

In webhook handler:
- If `dedupeEvent(EventSid)` is false, return 200 immediately.

### Scenario 4: Escalate to Voice conference and post recording link back into conversation

High-level steps:
1. Create Voice conference via TwiML `<Dial><Conference record="record-from-start">case-10492</Conference></Dial>`
2. On `recording.completed` webhook, post message into conversation with recording URL.

Posting back:

```bash
curl -sS -X POST "https://conversations.twilio.com/v1/Conversations/CH.../Messages" \
  -u "$TWILIO_API_KEY_SID:$TWILIO_API_KEY_SECRET" \
  --data-urlencode "Author=system" \
  --data-urlencode "Body=Call recording available: https://api.twilio.com/2010-04-01/Accounts/AC.../Recordings/RE... .mp3" \
  --data-urlencode 'Attributes={"type":"call_recording","recordingSid":"RE0123456789abcdef0123456789abcdef"}'
```

### Scenario 5: WhatsApp re-engagement using templates + mirror into conversation

Pattern:
- If last inbound > 24h, send WhatsApp template via Messaging API (not freeform).
- Mirror template send into conversation with attributes.

Mirror message:

```bash
curl -sS -X POST "https://conversations.twilio.com/v1/Conversations/CH.../Messages" \
  -u "$TWILIO_API_KEY_SID:$TWILIO_API_KEY_SECRET" \
  --data-urlencode "Author=system" \
  --data-urlencode "Body=Sent WhatsApp template: order_update_v2" \
  --data-urlencode 'Attributes={"channel":"whatsapp","template":"order_update_v2","messagingMessageSid":"SM0123456789abcdef0123456789abcdef"}'
```

### Scenario 6: Bulk close inactive conversations safely

Python batch job:
- List conversations, filter by last activity (from your DB or Twilio fields if available), set `State=closed`.

```python
import os
from twilio.rest import Client

client = Client(os.environ["TWILIO_API_KEY_SID"], os.environ["TWILIO_API_KEY_SECRET"], os.environ["TWILIO_ACCOUNT_SID"])

for conv in client.conversations.v1.conversations.list(limit=200):
    # Prefer your own last_activity tracking; Twilio fields vary by API.
    if conv.state == "active" and conv.friendly_name.startswith("Support Case"):
        client.conversations.v1.conversations(conv.sid).update(state="closed")
        print("closed", conv.sid)
```

---

## Quick Reference

| Task | Endpoint / Command | Key fields / flags |
|---|---|---|
| Create conversation | `POST /v1/Conversations` | `FriendlyName`, `UniqueName`, `Attributes`, `State` |
| List conversations | `GET /v1/Conversations` | `PageSize`, `PageToken` |
| Update conversation | `POST /v1/Conversations/{CH}` | `State`, `Attributes`, `FriendlyName` |
| Delete conversation | `DELETE /v1/Conversations/{CH}` | n/a |
| Add chat participant | `POST /v1/Conversations/{CH}/Participants` | `Identity`, `Attributes` |
| Add SMS participant | same | `MessagingBinding.Address`, `MessagingBinding.ProxyAddress` |
| Add WhatsApp participant | same | `MessagingBinding.Address=whatsapp:+E164`, `ProxyAddress=whatsapp:+E164` |
| List participants | `GET /v1/Conversations/{CH}/Participants` | `PageSize`, `PageToken` |
| Remove participant | `DELETE /v1/Conversations/{CH}/Participants/{MB}` | n/a |
| Send message | `POST /v1/Conversations/{CH}/Messages` | `Author`, `Body`, `Attributes` |
| List messages | `GET /v1/Conversations/{CH}/Messages` | `PageSize`, `Order`, `PageToken` |
| Webhook validation | `X-Twilio-Signature` | Validate against exact URL + params |
| Retry handling | n/a | Dedupe by `EventSid`, backoff on `20429` |

---

## Graph Relationships

### DEPENDS_ON

- `twilio-core-auth` (API keys, token rotation, request signing validation patterns)
- `webhook-ingestion` (idempotency, queueing, backpressure, signature verification)
- `redis` (optional; idempotency/suppression)
- `postgres` (optional; event store / audit log)

### COMPOSES

- `twilio-programmable-messaging` (SMS/MMS/WhatsApp delivery callbacks, STOP handling, 10DLC/toll-free)
- `twilio-voice` (escalation, recordings, transcription, IVR state machines)
- `twilio-verify` (step-up verification before participant add / sensitive actions)
- `twilio-studio` (flow triggers based on conversation events)
- `sendgrid` (transactional email mirroring into conversation threads)

### SIMILAR_TO

- `slack-conversations` (thread + participant model, event-driven updates)
- `zendesk-ticketing` (case/ticket lifecycle mapped to conversation state)
- `intercom-messaging` (omnichannel messaging with identity + contact bindings)
