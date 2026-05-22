---
name: twilio-whatsapp
cluster: twilio
description: "WhatsApp Business: template messages, session messages, media, webhooks, opt-in management"
tags: ["whatsapp","twilio","messaging"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "twilio whatsapp business template session message webhook media"
---

# twilio-whatsapp

## Purpose

Enable OpenClaw to implement and operate Twilio WhatsApp Business messaging in production:

- Send **template messages** (pre-approved) and **session messages** (24-hour customer care window).
- Attach **media** (images/docs/audio) with correct MIME types and size constraints.
- Receive and validate **webhooks** (incoming messages + message status callbacks).
- Implement **opt-in/opt-out** and compliance controls (STOP handling, consent logging, regional constraints).
- Operate reliably under Twilio production constraints: rate limits, retries, idempotency, error codes, and cost controls via Messaging Services.

Concrete value to an engineer: ship a WhatsApp messaging subsystem that is observable, compliant, resilient to webhook retries, and safe to run at scale with predictable failure modes.

---

## Prerequisites

### Accounts & Twilio-side setup

- Twilio account with WhatsApp sender enabled:
  - Either **Twilio Sandbox for WhatsApp** (dev only) or a **WhatsApp Business Profile** connected to Twilio (prod).
- A Twilio **Messaging Service** (recommended for production) with:
  - WhatsApp sender(s) attached (e.g., `whatsapp:+14155238886` or your approved WA number).
  - Status callback URL configured (optional but recommended).
- WhatsApp templates approved in Meta Business Manager (via Twilio Console template manager).

### Local tooling versions (pinned)

- Node.js **20.11.1** (LTS) or **18.19.1** (LTS)
- Python **3.11.8** or **3.12.2**
- Twilio helper libraries:
  - `twilio` (Node) **4.23.0**
  - `twilio` (Python) **9.0.5**
- Twilio CLI **5.16.0** (for diagnostics; not required at runtime)
- ngrok **3.13.1** (local webhook testing)

### Auth & secrets

Use one of:

1. **API Key (recommended)**:
   - `TWILIO_API_KEY_SID` (starts with `SK...`)
   - `TWILIO_API_KEY_SECRET`
   - `TWILIO_ACCOUNT_SID` (starts with `AC...`)

2. **Account SID + Auth Token**:
   - `TWILIO_ACCOUNT_SID`
   - `TWILIO_AUTH_TOKEN`

Store secrets in:
- Kubernetes: `Secret` + mounted env vars
- AWS: Secrets Manager + IRSA
- GCP: Secret Manager + Workload Identity
- Local dev: `.env` (never commit)

### Network & webhook requirements

- Public HTTPS endpoint for webhooks (Twilio requires HTTPS in most production contexts).
- Allow inbound from Twilio webhook IPs is not stable; validate using **X-Twilio-Signature** instead of IP allowlists.
- Ensure your endpoint can handle retries and out-of-order delivery.

---

## Core Concepts

### WhatsApp message types (Twilio perspective)

1. **Template message** (outside 24-hour window):
   - Must use a pre-approved template.
   - Used for notifications, OTP, shipping updates, etc.
   - In Twilio, templates are typically sent via the **Content API** (preferred) or via template integration depending on account configuration.

2. **Session message** (inside 24-hour window):
   - Free-form text/media allowed (subject to WhatsApp policies).
   - The 24-hour window starts when the user messages you.

3. **Media message**:
   - WhatsApp supports images, documents, audio, video with constraints.
   - Twilio sends media via `MediaUrl` (publicly accessible URL) or via Twilio-hosted media in some flows.

### Identifiers and addressing

- WhatsApp addresses in Twilio use `whatsapp:` prefix:
  - `From`: `whatsapp:+14155238886`
  - `To`: `whatsapp:+14155550123`
- Messaging Service SID: `MGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- Message SID: `SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Webhooks

Two primary webhook categories:

1. **Incoming message webhook** (when user sends you a message):
   - Twilio sends an HTTP request with form-encoded parameters like `From`, `To`, `Body`, `NumMedia`, `MediaUrl0`, etc.

2. **Message status callback** (delivery lifecycle):
   - Status values: `queued`, `sent`, `delivered`, `read`, `failed`, `undelivered`
   - Twilio retries on non-2xx responses with backoff.

### Idempotency and retries

- Twilio may retry webhooks; your handler must be idempotent.
- Status callbacks can arrive out of order (e.g., `delivered` then `read`, or `failed` after transient states).
- Use `MessageSid` + `MessageStatus` + timestamp to dedupe.

### Compliance: opt-in/opt-out

- WhatsApp requires user opt-in; you must store consent evidence.
- STOP handling:
  - For SMS, Twilio has built-in STOP.
  - For WhatsApp, you must implement opt-out keywords and respect them (e.g., “STOP”, “UNSUBSCRIBE”).
- Maintain a suppression list keyed by E.164 phone number.

---

## Installation & Setup

### Official Python SDK — WhatsApp

**Repository:** https://github.com/twilio/twilio-python  
**PyPI:** `pip install twilio` · **Supported:** Python 3.7–3.13

```python
from twilio.rest import Client
client = Client()

# Send WhatsApp message (Sandbox: from_ = 'whatsapp:+14155238886')
msg = client.messages.create(
    body="Your order is confirmed!",
    from_="whatsapp:+14155238886",
    to="whatsapp:+15558675309"
)

# Send template message (approved HSM)
msg = client.messages.create(
    from_="whatsapp:+14155238886",
    to="whatsapp:+15558675309",
    content_sid="HX...",          # pre-approved template SID
    content_variables='{"1":"Alice","2":"12345"}'
)
```

Source: [twilio/twilio-python — messages](https://github.com/twilio/twilio-python/blob/main/twilio/rest/api/v2010/account/message/__init__.py)

### Ubuntu 22.04 LTS (x86_64)

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg jq
```

Node.js 20.11.1 via NodeSource:

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
node -v
npm -v
```

Python 3.11:

```bash
sudo apt-get install -y python3.11 python3.11-venv python3-pip
python3.11 --version
```

Twilio CLI 5.16.0:

```bash
npm install -g twilio-cli@5.16.0
twilio --version
```

ngrok 3.13.1:

```bash
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
  | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
  | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt-get update && sudo apt-get install -y ngrok
ngrok version
```

### Fedora 39 (x86_64)

```bash
sudo dnf install -y curl jq nodejs python3 python3-virtualenv
node -v
python3 --version
```

Twilio CLI:

```bash
sudo npm install -g twilio-cli@5.16.0
twilio --version
```

ngrok:

```bash
sudo dnf install -y ngrok
ngrok version
```

### macOS 14 (Sonoma) — Intel + Apple Silicon

Homebrew:

```bash
brew update
brew install node@20 python@3.12 jq ngrok/ngrok/ngrok
node -v
python3 --version
ngrok version
```

Twilio CLI:

```bash
npm install -g twilio-cli@5.16.0
twilio --version
```

### Auth setup (CLI + env)

Twilio CLI login (writes to `~/.twilio-cli/config.json`):

```bash
twilio login
```

Runtime env vars (recommended: API Key):

```bash
export TWILIO_ACCOUNT_SID="AC2f7b9c2b0f1d2e3a4b5c6d7e8f9a0b1"
export TWILIO_API_KEY_SID="SK3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8"
export TWILIO_API_KEY_SECRET="a_very_long_secret_value"
export TWILIO_MESSAGING_SERVICE_SID="MG0c3d2e1f4a5b6c7d8e9f0a1b2c3d4e5"
```

Local `.env` (example path: `/srv/whatsapp/.env`):

```dotenv
TWILIO_ACCOUNT_SID=AC2f7b9c2b0f1d2e3a4b5c6d7e8f9a0b1
TWILIO_API_KEY_SID=SK3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8
TWILIO_API_KEY_SECRET=a_very_long_secret_value
TWILIO_MESSAGING_SERVICE_SID=MG0c3d2e1f4a5b6c7d8e9f0a1b2c3d4e5
PUBLIC_BASE_URL=https://wa.example.com
```

---

## Key Capabilities

### Send session messages (text + media)

- Use Twilio Programmable Messaging `Messages` API.
- Ensure `To` and `From` include `whatsapp:` prefix.
- Prefer `MessagingServiceSid` over hardcoding `From` for routing and future sender expansion.

Node (twilio 4.23.0):

```javascript
import twilio from "twilio";

const client = twilio(
  process.env.TWILIO_API_KEY_SID,
  process.env.TWILIO_API_KEY_SECRET,
  { accountSid: process.env.TWILIO_ACCOUNT_SID }
);

export async function sendSessionText(toE164, body) {
  const msg = await client.messages.create({
    to: `whatsapp:${toE164}`,
    messagingServiceSid: process.env.TWILIO_MESSAGING_SERVICE_SID,
    body,
    statusCallback: `${process.env.PUBLIC_BASE_URL}/twilio/status`
  });
  return msg.sid;
}
```

Python (twilio 9.0.5):

```python
import os
from twilio.rest import Client

client = Client(
    os.environ["TWILIO_API_KEY_SID"],
    os.environ["TWILIO_API_KEY_SECRET"],
    os.environ["TWILIO_ACCOUNT_SID"],
)

def send_session_media(to_e164: str, body: str, media_url: str) -> str:
    msg = client.messages.create(
        to=f"whatsapp:{to_e164}",
        messaging_service_sid=os.environ["TWILIO_MESSAGING_SERVICE_SID"],
        body=body,
        media_url=[media_url],
        status_callback=f"{os.environ['PUBLIC_BASE_URL']}/twilio/status",
    )
    return msg.sid
```

Operational constraints:
- Media URLs must be publicly reachable by Twilio (no private S3 URL unless presigned).
- If you send media, validate content-type and size before sending to reduce failures.

### Send template messages (outside session window)

Production recommendation: use Twilio **Content API** (aka “Content Templates”) when available in your account. This decouples template definition from code and supports localization/variables.

#### Content API send (Messages API with `contentSid`)

Node:

```javascript
export async function sendTemplate(toE164) {
  const msg = await client.messages.create({
    to: `whatsapp:${toE164}`,
    messagingServiceSid: process.env.TWILIO_MESSAGING_SERVICE_SID,
    contentSid: "HXb5b62575e6e4ff6129ad7c8efe1f983e",
    contentVariables: JSON.stringify({
      "1": "Ava",
      "2": "Order #18473",
      "3": "2026-02-21"
    }),
    statusCallback: `${process.env.PUBLIC_BASE_URL}/twilio/status`
  });
  return msg.sid;
}
```

Python:

```python
import json

def send_template(to_e164: str) -> str:
    msg = client.messages.create(
        to=f"whatsapp:{to_e164}",
        messaging_service_sid=os.environ["TWILIO_MESSAGING_SERVICE_SID"],
        content_sid="HXb5b62575e6e4ff6129ad7c8efe1f983e",
        content_variables=json.dumps({"1": "Ava", "2": "Order #18473", "3": "2026-02-21"}),
        status_callback=f"{os.environ['PUBLIC_BASE_URL']}/twilio/status",
    )
    return msg.sid
```

Notes:
- `contentVariables` keys are strings `"1"`, `"2"`, etc. per Twilio Content variable indexing.
- Template approval and category (utility/marketing/authentication) affects deliverability and policy compliance.

### Receive inbound WhatsApp messages (webhook handler)

Twilio sends `application/x-www-form-urlencoded` by default.

Express (Node):

```javascript
import express from "express";
import twilio from "twilio";

const app = express();
app.use(express.urlencoded({ extended: false }));

app.post("/twilio/inbound", (req, res) => {
  const signature = req.header("X-Twilio-Signature") || "";
  const url = `${process.env.PUBLIC_BASE_URL}/twilio/inbound`;

  const isValid = twilio.validateRequest(
    process.env.TWILIO_AUTH_TOKEN, // validateRequest requires Auth Token, not API key secret
    signature,
    url,
    req.body
  );

  if (!isValid) return res.status(403).send("invalid signature");

  const from = req.body.From; // e.g. "whatsapp:+14155550123"
  const body = req.body.Body || "";
  const numMedia = parseInt(req.body.NumMedia || "0", 10);

  // Idempotency: inbound messages have MessageSid
  const messageSid = req.body.MessageSid;

  // TODO: persist inbound event, dedupe by MessageSid
  // TODO: implement opt-out keywords

  res.type("text/xml").send("<Response></Response>");
});

app.listen(3000);
```

Important: `validateRequest` requires `TWILIO_AUTH_TOKEN`. If you use API Keys for REST calls, you still need Auth Token for webhook signature validation. Store it separately and restrict access.

FastAPI (Python):

```python
import os
from fastapi import FastAPI, Request, Response
from twilio.request_validator import RequestValidator

app = FastAPI()
validator = RequestValidator(os.environ["TWILIO_AUTH_TOKEN"])

@app.post("/twilio/inbound")
async def inbound(request: Request):
    form = await request.form()
    signature = request.headers.get("X-Twilio-Signature", "")
    url = f"{os.environ['PUBLIC_BASE_URL']}/twilio/inbound"

    if not validator.validate(url, dict(form), signature):
        return Response(content="invalid signature", status_code=403)

    message_sid = form.get("MessageSid")
    from_ = form.get("From")
    body = form.get("Body", "")

    return Response(content="<Response></Response>", media_type="text/xml")
```

### Message status callbacks (delivered/read/failed)

Configure `statusCallback` per message or at Messaging Service level.

Twilio will POST fields including:
- `MessageSid`, `MessageStatus`, `To`, `From`, `ErrorCode`, `ErrorMessage`

Handler requirements:
- Always return 2xx quickly (under ~2 seconds).
- Enqueue processing to a job queue (SQS, Pub/Sub, Kafka).
- Dedupe by `(MessageSid, MessageStatus)`.

Example (Express):

```javascript
app.post("/twilio/status", (req, res) => {
  // Validate signature same as inbound
  const { MessageSid, MessageStatus, ErrorCode, ErrorMessage } = req.body;

  // Persist status transition; do not assume ordering
  // If failed/undelivered, capture ErrorCode + ErrorMessage for triage

  res.sendStatus(204);
});
```

### Opt-in management and suppression

Implement:
- Consent capture (timestamp, source, IP/user agent if applicable, proof text).
- Suppression list:
  - If user sends “STOP”, “UNSUBSCRIBE”, “CANCEL”, “END”, “QUIT” → mark suppressed.
  - If user sends “START”, “UNSTOP”, “SUBSCRIBE” → unsuppress (only if policy allows).

Example keyword parsing:

```python
STOP_WORDS = {"stop", "unsubscribe", "cancel", "end", "quit"}
START_WORDS = {"start", "unstop", "subscribe"}

def classify_opt(body: str) -> str | None:
    t = body.strip().lower()
    if t in STOP_WORDS:
        return "STOP"
    if t in START_WORDS:
        return "START"
    return None
```

Enforcement:
- Before sending any outbound message, check suppression list.
- For template messages, also check consent freshness and region-specific rules.

### Media handling (upload, validation, and delivery)

Twilio requires `MediaUrl` accessible by Twilio. Common pattern:
- Store media in S3 with short-lived presigned URL (e.g., 15 minutes).
- Validate MIME type and size before generating URL.

Constraints vary; enforce conservative limits:
- Images: <= 5 MB
- Documents: <= 100 MB (PDF), but enforce smaller for reliability
- Audio/video: enforce <= 16 MB unless you have confirmed limits for your account/region

Example: generate presigned URL (AWS SDK v3, Node):

```javascript
import { S3Client, GetObjectCommand } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

const s3 = new S3Client({ region: "us-east-1" });

export async function presign(bucket, key) {
  const cmd = new GetObjectCommand({ Bucket: bucket, Key: key });
  return await getSignedUrl(s3, cmd, { expiresIn: 900 });
}
```

### Webhook replay protection and idempotency

Store processed webhook IDs:
- Inbound: `MessageSid`
- Status: `MessageSid + ":" + MessageStatus`

Use a fast store (Redis) with TTL (e.g., 7 days) to prevent duplicate processing.

Redis example (pseudo):

```text
SETNX twilio:inbound:SM... 1 EX 604800
SETNX twilio:status:SM...:delivered 1 EX 604800
```

---

## Command Reference

### Twilio CLI (5.16.0)

#### Authenticate

```bash
twilio login
```

Flags:
- `--profile <name>`: store credentials under a named profile
- `--username <AC...>`: account SID
- `--password <auth_token>`: auth token (interactive if omitted)

#### List messages

```bash
twilio api:core:messages:list
```

Relevant flags:
- `--to <string>`: filter by To (e.g., `whatsapp:+14155550123`)
- `--from <string>`: filter by From
- `--date-sent <YYYY-MM-DD>`: filter by date
- `--page-size <int>`: default 50
- `--limit <int>`: max records to return
- `--properties <csv>`: select fields (CLI dependent)
- `--output json|tsv|csv`: output format (CLI dependent)

Example:

```bash
twilio api:core:messages:list --to "whatsapp:+14155550123" --limit 20 --output json | jq .
```

#### Fetch a message

```bash
twilio api:core:messages:fetch --sid SMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

Flags:
- `--sid <SM...>`: required

#### Create a message (session or template via Content API)

```bash
twilio api:core:messages:create \
  --to "whatsapp:+14155550123" \
  --messaging-service-sid MG0c3d2e1f4a5b6c7d8e9f0a1b2c3d4e5 \
  --body "Hello from production"
```

All relevant flags (commonly supported by API/CLI; availability may vary by CLI version):
- `--to <string>`: required
- `--from <string>`: optional if using Messaging Service
- `--messaging-service-sid <MG...>`: recommended
- `--body <string>`: message text
- `--media-url <url>`: repeatable for multiple media
- `--status-callback <url>`: status webhook
- `--max-price <decimal>`: price cap (channel-dependent)
- `--provide-feedback <boolean>`: request delivery feedback (carrier dependent)
- `--attempt <int>` / `--validity-period <int>`: channel dependent; may not apply to WhatsApp
- `--content-sid <HX...>`: Content API template identifier
- `--content-variables <json>`: JSON string of variables

Example template send:

```bash
twilio api:core:messages:create \
  --to "whatsapp:+14155550123" \
  --messaging-service-sid MG0c3d2e1f4a5b6c7d8e9f0a1b2c3d4e5 \
  --content-sid HXb5b62575e6e4ff6129ad7c8efe1f983e \
  --content-variables '{"1":"Ava","2":"Order #18473","3":"2026-02-21"}'
```

#### Debug webhooks locally with ngrok

```bash
ngrok http 3000
```

Copy the HTTPS forwarding URL into:
- Twilio Console → Messaging → WhatsApp Sender / Messaging Service → Inbound webhook
- Status callback URL

---

## Configuration Reference

### Node service config

**Path:** `/srv/whatsapp/config/whatsapp.production.toml`

```toml
[twilio]
account_sid = "AC2f7b9c2b0f1d2e3a4b5c6d7e8f9a0b1"
messaging_service_sid = "MG0c3d2e1f4a5b6c7d8e9f0a1b2c3d4e5"
public_base_url = "https://wa.example.com"

[webhooks]
inbound_path = "/twilio/inbound"
status_path = "/twilio/status"
validate_signatures = true
signature_auth_token_env = "TWILIO_AUTH_TOKEN"

[opt]
stop_keywords = ["stop","unsubscribe","cancel","end","quit"]
start_keywords = ["start","unstop","subscribe"]
suppression_ttl_days = 3650

[media]
max_image_bytes = 5242880
max_doc_bytes = 26214400
presign_ttl_seconds = 900
allowed_mime_prefixes = ["image/","application/pdf"]
```

**Path:** `/srv/whatsapp/.env` (permissions `0600`)

```dotenv
TWILIO_ACCOUNT_SID=AC2f7b9c2b0f1d2e3a4b5c6d7e8f9a0b1
TWILIO_API_KEY_SID=SK3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8
TWILIO_API_KEY_SECRET=a_very_long_secret_value
TWILIO_AUTH_TOKEN=your_auth_token_for_signature_validation
TWILIO_MESSAGING_SERVICE_SID=MG0c3d2e1f4a5b6c7d8e9f0a1b2c3d4e5
PUBLIC_BASE_URL=https://wa.example.com
```

### systemd unit (Linux)

**Path:** `/etc/systemd/system/whatsapp.service`

```ini
[Unit]
Description=WhatsApp Messaging Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=whatsapp
Group=whatsapp
WorkingDirectory=/srv/whatsapp
EnvironmentFile=/srv/whatsapp/.env
ExecStart=/usr/bin/node /srv/whatsapp/dist/server.js
Restart=on-failure
RestartSec=2
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/srv/whatsapp /var/log/whatsapp
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
```

### Kubernetes deployment snippet

**Path:** `/srv/whatsapp/deploy/k8s/deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: whatsapp
  namespace: messaging
spec:
  replicas: 6
  selector:
    matchLabels:
      app: whatsapp
  template:
    metadata:
      labels:
        app: whatsapp
    spec:
      containers:
        - name: whatsapp
          image: ghcr.io/acme/whatsapp:2026.02.21
          ports:
            - containerPort: 3000
          env:
            - name: TWILIO_ACCOUNT_SID
              valueFrom:
                secretKeyRef:
                  name: twilio
                  key: account_sid
            - name: TWILIO_API_KEY_SID
              valueFrom:
                secretKeyRef:
                  name: twilio
                  key: api_key_sid
            - name: TWILIO_API_KEY_SECRET
              valueFrom:
                secretKeyRef:
                  name: twilio
                  key: api_key_secret
            - name: TWILIO_AUTH_TOKEN
              valueFrom:
                secretKeyRef:
                  name: twilio
                  key: auth_token
            - name: TWILIO_MESSAGING_SERVICE_SID
              valueFrom:
                secretKeyRef:
                  name: twilio
                  key: messaging_service_sid
            - name: PUBLIC_BASE_URL
              value: "https://wa.example.com"
          readinessProbe:
            httpGet:
              path: /healthz
              port: 3000
            initialDelaySeconds: 3
            periodSeconds: 5
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "1"
              memory: "1Gi"
```

---

## Integration Patterns

### Pattern: API service + queue for webhook processing

- Webhook handler validates signature and enqueues event.
- Worker consumes events and updates DB, triggers downstream actions.

Example pipeline:
1. Twilio → `POST /twilio/inbound`
2. API → publish to Kafka topic `twilio.inbound.v1`
3. Worker → parse, apply opt-out, route to conversation service
4. Conversation service → decides response → sends via Twilio Messages API

Kafka message schema (JSON):

```json
{
  "event_type": "twilio_inbound",
  "received_at": "2026-02-21T18:22:11.123Z",
  "message_sid": "SMd2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7",
  "from": "whatsapp:+14155550123",
  "to": "whatsapp:+14155238886",
  "body": "Where is my order?",
  "num_media": 0,
  "raw": { "Body": "Where is my order?", "ProfileName": "Ava" }
}
```

### Pattern: Compose with Twilio Verify (OTP over WhatsApp)

- Use Verify V2 with WhatsApp channel where supported.
- Fallback to SMS if WhatsApp fails.

Flow:
- Attempt Verify via WhatsApp
- If error indicates channel unavailable, fallback to SMS

Key operational note: Verify has its own rate limiting and fraud controls; do not DIY OTP over session messages unless you accept the compliance and abuse risk.

### Pattern: Compose with SendGrid for email fallback

- If WhatsApp template fails with `63016` (outside window / template required) or user opted out:
  - Send transactional email via SendGrid dynamic template.
- Keep a unified notification log with channel attempts and outcomes.

### Pattern: Studio for rapid iteration, API for core flows

- Use Twilio Studio for low-risk flows (FAQ, routing).
- Use REST Trigger API to start Studio flows from your backend.
- Keep WhatsApp sending in code for high-volume, audited flows.

---

## Error Handling & Troubleshooting

Handle Twilio errors at two layers:
- REST API errors when sending
- Webhook status callbacks with `ErrorCode`/`ErrorMessage`

At minimum, log:
- `MessageSid`, `To`, `From`, `MessagingServiceSid`, `ErrorCode`, `ErrorMessage`, HTTP status, Twilio request ID (`X-Twilio-Request-Id` if present)

### 1) 21211 — invalid To number

Error text (common):

```
TwilioRestException: The 'To' number +1415555012 is not a valid phone number.
```

Root cause:
- Not E.164, missing digits, or missing `whatsapp:` prefix.

Fix:
- Normalize to E.164 and prefix: `To=whatsapp:+14155550123`.
- Validate with libphonenumber before calling Twilio.

### 2) 20003 — authentication failure

Error text:

```
Authenticate
The AccountSid and AuthToken combination you have provided is invalid.
```

Root cause:
- Wrong credentials, mixing API key secret with auth token, wrong account SID.

Fix:
- For REST calls with API keys: use `(apiKeySid, apiKeySecret, accountSid)`.
- For webhook validation: use `TWILIO_AUTH_TOKEN`.
- Rotate compromised credentials; verify environment injection.

### 3) 20429 — rate limit exceeded

Error text:

```
Too Many Requests
Rate limit exceeded
```

Root cause:
- Bursting sends, too many concurrent API calls, or account-level limits.

Fix:
- Implement client-side rate limiting (token bucket).
- Batch sends and use a queue with concurrency control.
- Prefer Messaging Service and distribute across senders if applicable.

### 4) 30003 — Unreachable destination / carrier violation (often SMS, can surface in mixed services)

Error text:

```
Message Delivery - Carrier violation
```

Root cause:
- Carrier filtering, invalid destination, or blocked route.

Fix:
- For WhatsApp, ensure destination is WhatsApp-capable and opted in.
- Verify sender is approved for the destination region.
- Check status callback `ErrorCode` and Twilio Console logs.

### 5) 63016 — WhatsApp template required / outside session window

Common status callback error message:

```
63016: Failed to send message because you are outside the allowed window.
```

Root cause:
- Attempted free-form session message outside 24-hour window.

Fix:
- Use an approved template (Content API) to re-open conversation.
- Track last inbound user message timestamp per user.

### 6) 63018 — Template not found / not approved / mismatch

Common error:

```
63018: Content template not found or not approved for use.
```

Root cause:
- Wrong `contentSid`, template not approved, or not enabled for WhatsApp sender.

Fix:
- Verify template approval status in Twilio Console.
- Ensure template is associated with the correct WhatsApp sender / business.
- Deploy template changes before code rollout.

### 7) 21610 — user opted out (more typical for SMS; still handle suppression uniformly)

Error text:

```
Attempt to send to unsubscribed recipient
```

Root cause:
- Recipient opted out (Twilio-managed for SMS) or your own suppression list for WhatsApp.

Fix:
- For WhatsApp: enforce your suppression list before sending.
- Provide a re-subscribe path and record consent.

### 8) Webhook signature validation failures

Your service logs:

```
invalid signature
```

Root cause:
- `PUBLIC_BASE_URL` mismatch (ngrok URL changed), wrong auth token, proxy rewriting URL, missing form parsing.

Fix:
- Ensure the exact URL used in validation matches Twilio’s requested URL (scheme/host/path).
- In Express, use `express.urlencoded({ extended: false })` before handler.
- If behind a reverse proxy, ensure `PUBLIC_BASE_URL` matches external URL, not internal.

### 9) Media fetch failures

Status callback may show:

```
30007: Carrier violation
```

or Twilio console indicates media fetch error.

Root cause:
- Media URL not publicly accessible, expired presigned URL, blocked by WAF, wrong TLS config.

Fix:
- Presign with sufficient TTL (>= 10 minutes).
- Allow Twilio user agent through WAF or bypass for media bucket.
- Ensure correct `Content-Type` and `Content-Length`.

### 10) 11200 — HTTP retrieval failure (webhook endpoint)

Twilio debugger shows:

```
11200 - HTTP retrieval failure
```

Root cause:
- Your webhook endpoint timed out, returned 5xx, DNS/TLS issues.

Fix:
- Return 2xx quickly; enqueue work.
- Increase server timeouts; ensure TLS chain is correct.
- Add health checks and autoscaling.

---

## Security Hardening

### Webhook validation (mandatory)

- Validate `X-Twilio-Signature` on every inbound and status webhook.
- Keep `TWILIO_AUTH_TOKEN` in a restricted secret store; do not expose to app logs.
- If using API keys for REST, still store Auth Token for validation.

### Least privilege credentials

- Prefer API Keys over Auth Token for REST calls.
- Rotate API keys quarterly; rotate immediately on suspected compromise.
- Separate keys per environment (dev/stage/prod) and per service.

### Transport security

- Enforce TLS 1.2+ on public endpoints.
- Use HSTS on your domain.
- Do not accept plaintext HTTP for webhooks.

### Data minimization

- Store only required message content; consider hashing or redacting:
  - OTP codes
  - Payment details (should never be sent)
  - Sensitive PII
- Apply retention policies (e.g., 30–90 days for message bodies, longer for metadata).

### Access controls and audit

- Restrict Twilio Console access via SSO and MFA.
- Log all template changes and sender changes.
- Use separate subaccounts for isolation if your org structure supports it.

### CIS-aligned host hardening (Linux)

Reference: CIS Ubuntu Linux 22.04 LTS Benchmark (where applicable).

- Run service as non-root user (`whatsapp`).
- systemd hardening:
  - `NoNewPrivileges=true`
  - `ProtectSystem=strict`
  - `ProtectHome=true`
  - `PrivateTmp=true`
- File permissions:
  - `/srv/whatsapp/.env` mode `0600`, owned by service user.
- Disable shell access for service user:
  - `/usr/sbin/nologin`

### WAF / reverse proxy considerations

- Do not IP-allowlist Twilio; validate signatures instead.
- Ensure proxy preserves request body exactly; signature validation is sensitive to parameter changes.
- If you must transform requests, validate at the edge before transformation.

---

## Performance Tuning

### 1) Webhook latency: enqueue + 204

Target:
- p95 webhook handler latency < 50ms (excluding network)
- Always respond within 1s

Expected impact:
- Reduces Twilio retries and duplicate deliveries.
- Stabilizes under burst traffic.

Implementation:
- Parse + validate signature
- Write minimal event record
- Enqueue job
- Return `204 No Content`

### 2) Outbound throughput: concurrency control

Problem:
- Unbounded concurrency triggers `20429` and increases tail latency.

Solution:
- Token bucket per sender or per Messaging Service.
- Start with concurrency 20–50 per pod; tune based on observed 20429 rate.

Expected impact:
- Fewer rate-limit errors; higher sustained throughput.

### 3) Connection reuse

- Use HTTP keep-alive agent (Node) for Twilio REST calls.
- In Python, reuse client and avoid creating per-request.

Expected impact:
- Lower CPU and latency under high send volume.

### 4) Dedupe storage

- Use Redis with `SETNX` and TTL for webhook dedupe.
- Keep TTL aligned with your maximum replay window (7–14 days).

Expected impact:
- Prevents duplicate downstream actions (double replies, double refunds, etc.).

### 5) Cost optimization via Messaging Service

- Use Messaging Service for sender pooling and routing.
- For mixed channels (SMS/WhatsApp), configure geo-matching and fallback rules carefully.

Expected impact:
- Lower operational overhead; fewer misroutes; potential cost savings depending on routing.

---

## Advanced Topics

### Handling out-of-order status transitions

Do not model status as a simple state machine with strict ordering. Instead:
- Store all status events with timestamps.
- Derive “current status” as the max-precedence terminal state:
  - `failed`/`undelivered` terminal negative
  - `read` terminal positive
  - `delivered` positive
  - `sent`/`queued` transient

### Multi-tenant / subaccount architecture

If you serve multiple customers:
- Use Twilio subaccounts per tenant for isolation.
- Store per-tenant `AccountSid` and API key.
- Ensure webhook validation uses the correct Auth Token per tenant (map by `To` number or `AccountSid` if provided).

### Template localization

- Use Content API with localized variants.
- Choose locale based on user profile; fallback to `en_US`.
- Keep template variables stable across locales.

### Media privacy and compliance

- Presigned URLs leak access if forwarded; keep TTL short.
- Consider proxying media through your domain with auth if policy requires, but ensure Twilio can fetch it.

### Disaster recovery

- If webhook processing is down, Twilio will retry for a limited period.
- Persist raw webhook payloads to durable storage (S3/GCS) for replay.
- Provide a replay tool that re-enqueues events by `MessageSid`.

### Testing strategy

- Unit test:
  - Signature validation (known-good fixtures)
  - Opt-out keyword parsing
  - E.164 normalization
- Integration test:
  - Send message to sandbox number
  - Verify status callback receipt
- Load test:
  - Simulate webhook bursts (e.g., 500 RPS) and ensure 2xx responses

---

## Usage Examples

### 1) Production: send a template for shipping update, then handle replies

Steps:
1. User opts in on website checkout.
2. Send template “shipping_update”.
3. User replies “Where is my package?”
4. Respond with session message.

Node (end-to-end sketch):

```javascript
// 1) consent stored elsewhere
const to = "+14155550123";

// 2) template send
const templateSid = "HXb5b62575e6e4ff6129ad7c8efe1f983e";
await client.messages.create({
  to: `whatsapp:${to}`,
  messagingServiceSid: process.env.TWILIO_MESSAGING_SERVICE_SID,
  contentSid: templateSid,
  contentVariables: JSON.stringify({ "1": "Ava", "2": "18473", "3": "UPS" }),
  statusCallback: `${process.env.PUBLIC_BASE_URL}/twilio/status`
});

// 3/4) inbound webhook routes to agent/bot and responds within 24h window
```

### 2) Media: send invoice PDF with presigned URL

Python:

```python
pdf_url = "https://files.example.com/presigned/invoices/18473.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=..."
sid = client.messages.create(
    to="whatsapp:+14155550123",
    messaging_service_sid=os.environ["TWILIO_MESSAGING_SERVICE_SID"],
    body="Invoice for Order #18473",
    media_url=[pdf_url],
    status_callback=f"{os.environ['PUBLIC_BASE_URL']}/twilio/status",
).sid
print(sid)
```

### 3) Opt-out: user sends STOP, enforce suppression

Inbound handler logic:
- If body is STOP keyword:
  - Mark suppressed
  - Reply confirmation (session message allowed because user initiated)

Example response (TwiML empty is fine; you can also send outbound message via REST):

```xml
<Response></Response>
```

Then send confirmation via REST:

```bash
twilio api:core:messages:create \
  --to "whatsapp:+14155550123" \
  --messaging-service-sid MG0c3d2e1f4a5b6c7d8e9f0a1b2c3d4e5 \
  --body "You are opted out. Reply START to re-subscribe."
```

### 4) Status-driven retry: transient failure handling

Policy:
- Do not blindly retry WhatsApp sends on `failed` without inspecting error code.
- Retry only on known transient conditions (e.g., 20429 rate limit) with backoff.

Pseudo:
- If REST call returns 429 or error 20429:
  - retry with exponential backoff + jitter
- If status callback returns 63016:
  - switch to template message or alternate channel

### 5) Local dev: ngrok + sandbox

1. Start server on port 3000.
2. Start ngrok:

```bash
ngrok http 3000
```

3. Set `PUBLIC_BASE_URL` to ngrok HTTPS URL.
4. Configure Twilio sandbox inbound webhook to:
   - `https://<id>.ngrok-free.app/twilio/inbound`
5. Send WhatsApp message to sandbox number; verify inbound handler logs.

### 6) Multi-region: route by user locale and sender

- Maintain mapping:
  - `country_code -> messaging_service_sid`
- Choose Messaging Service based on `To` country.

Example mapping file:

**Path:** `/srv/whatsapp/config/routing.yaml`

```yaml
default_messaging_service_sid: MG0c3d2e1f4a5b6c7d8e9f0a1b2c3d4e5
by_country:
  US: MG0c3d2e1f4a5b6c7d8e9f0a1b2c3d4e5
  GB: YOUR_MG_SID
  DE: YOUR_MG_SID
```

---

## Quick Reference

| Task | Command / API | Key flags/fields |
|---|---|---|
| Send session text | `twilio api:core:messages:create` | `--to`, `--messaging-service-sid`, `--body`, `--status-callback` |
| Send media | `messages.create` | `media_url[]` / `--media-url` |
| Send template (Content API) | `messages.create` | `contentSid`, `contentVariables` |
| List messages | `twilio api:core:messages:list` | `--to`, `--from`, `--date-sent`, `--limit` |
| Fetch message | `twilio api:core:messages:fetch` | `--sid` |
| Validate webhook | SDK validator | `X-Twilio-Signature`, exact URL, `TWILIO_AUTH_TOKEN` |
| Handle opt-out | inbound parsing | STOP/START keywords + suppression list |
| Diagnose webhook failures | Twilio Console Debugger | error `11200`, request/response details |

---

## Graph Relationships

### DEPENDS_ON

- `twilio-core` (Twilio REST API fundamentals: auth, subaccounts, API keys)
- `twilio-messaging` (Programmable Messaging patterns: Messaging Services, status callbacks)
- `webhook-security` (signature validation, replay protection)
- `queueing` (Kafka/SQS/PubSub patterns for async processing)
- `secrets-management` (KMS, Vault, cloud secret managers)

### COMPOSES

- `twilio-verify` (OTP via WhatsApp where supported; fallback strategies)
- `sendgrid-transactional` (email fallback when WhatsApp fails or user opted out)
- `twilio-studio` (rapid flow prototyping; REST trigger integration)
- `observability` (structured logs, tracing, metrics, alerting on failure rates)

### SIMILAR_TO

- `twilio-sms` (similar send/status patterns; different compliance and STOP semantics)
- `meta-whatsapp-cloud-api` (direct Meta API; Twilio abstracts some concerns but adds its own constraints)
- `twilio-conversations` (higher-level conversation orchestration; different primitives than raw Messages API)
