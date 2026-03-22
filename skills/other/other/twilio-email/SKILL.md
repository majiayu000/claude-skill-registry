---
name: twilio-email
cluster: twilio
description: "SendGrid: transactional email, templates Handlebars, event webhooks, suppression, SPF/DKIM/DMARC"
tags: ["email","sendgrid","twilio","transactional"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "sendgrid email transactional template webhook deliverability spf dkim dmarc"
---

# twilio-email

## Purpose

Enable OpenClaw to implement, operate, and troubleshoot SendGrid (Twilio) transactional email in production:

- Send transactional emails via SendGrid v3 API with correct auth, retries, idempotency, and observability.
- Use Dynamic Templates (Handlebars) safely (escaping, conditionals, loops), versioning templates, and rolling out changes.
- Process SendGrid Event Webhook (delivered/open/click/bounce/spamreport/dropped/deferred) with signature verification and replay protection.
- Manage suppressions (bounces, blocks, spam reports, unsubscribes) and implement list-unsubscribe correctly.
- Configure domain authentication (SPF/DKIM/DMARC), dedicated IPs, IP warming, and bounce/spam handling.
- Integrate with Twilio cluster patterns (rate limiting, webhook retry logic, error taxonomy, cost/throughput tradeoffs).

This skill is for engineers building reliable email delivery pipelines and maintaining them under real traffic, compliance constraints, and deliverability requirements.

---

## Prerequisites

### Accounts & Access

- Twilio SendGrid account with **Mail Send** enabled.
- API key with minimum scopes:
  - `mail.send` (required)
  - `templates.read`, `templates.write` (if managing templates)
  - `suppression.read`, `suppression.write` (if managing suppressions)
  - `eventwebhook.read`, `eventwebhook.write` (if managing webhook settings)
- Verified sender identity or authenticated domain.

### Runtime Versions (tested)

- Node.js **20.11.1** (LTS) + npm **10.2.4**
- Python **3.11.7** (or 3.12.1) + pip **23.3.2**
- Go **1.22.1** (if implementing webhook verifier or high-throughput sender)
- OpenSSL **3.0.2** (Ubuntu 22.04), **3.2.1** (macOS 14), **3.0.12** (Fedora 39)

### SDK / Libraries (recommended)

- Node: `@sendgrid/mail@8.1.3`, `@sendgrid/client@8.1.3`
- Python: `sendgrid==6.11.0`
- Webhook signature verification:
  - Node: `@sendgrid/eventwebhook@8.1.0` (or implement ECDSA verify manually)
  - Go: `github.com/sendgrid/sendgrid-go@3.16.0` (mail send), custom verifier for webhook

### Network / Infra

- Outbound HTTPS to `https://api.sendgrid.com` (TCP 443).
- Inbound HTTPS endpoint for Event Webhook (publicly reachable) with:
  - TLS 1.2+ (TLS 1.3 preferred)
  - Stable hostname
  - Ability to handle bursts (SendGrid batches events)

### Auth Setup (exact steps)

1. Create API key:
   - SendGrid Dashboard → Settings → API Keys → Create API Key
   - Name: `prod-mail-send-2026-02`
   - Permissions: **Restricted Access** → enable `Mail Send` (and others as needed)
2. Store secret in your secret manager:
   - AWS Secrets Manager: `prod/sendgrid/api_key`
   - GCP Secret Manager: `prod-sendgrid-api-key`
   - Vault: `secret/data/prod/sendgrid`
3. Export locally for testing (never commit):
   ```bash
   export SENDGRID_API_KEY='SG.xxxxxx.yyyyyy'
   ```

---

## Core Concepts

### Transactional vs Marketing

- **Transactional**: triggered by user/system actions (password reset, receipts, alerts). Must be timely, consistent, and typically exempt from marketing consent rules depending on jurisdiction and content.
- **Marketing**: campaigns, newsletters. Use SendGrid Marketing Campaigns; different compliance and suppression semantics.

This skill focuses on **transactional** via `/v3/mail/send` and Dynamic Templates.

### Message Model (SendGrid v3)

A send request is a JSON payload with:

- `from` (must be verified or domain-authenticated)
- `personalizations[]`:
  - `to[]`, `cc[]`, `bcc[]`
  - `dynamic_template_data` (for dynamic templates)
  - `custom_args` (for correlation IDs; appears in event webhook)
- `template_id` (dynamic template)
- `categories[]` (for analytics grouping)
- `asm` (unsubscribe groups)
- `mail_settings`, `tracking_settings`

### Dynamic Templates (Handlebars)

- Templates are stored in SendGrid; you reference `template_id`.
- Handlebars features:
  - `{{var}}` HTML-escaped by default
  - `{{{var}}}` unescaped (dangerous; avoid unless sanitized)
  - `{{#if}}`, `{{#each}}`, `{{else}}`
- Versioning: templates have versions; you can activate a version.

### Event Webhook

SendGrid posts batched JSON events to your endpoint, e.g.:

- `delivered`, `open`, `click`, `bounce`, `dropped`, `deferred`, `spamreport`, `unsubscribe`, `group_unsubscribe`, `group_resubscribe`, `processed`

Key production requirements:

- Verify signature (ECDSA) using SendGrid’s public key.
- Handle retries (SendGrid retries on non-2xx).
- Idempotency: events can be duplicated; dedupe by `(sg_event_id)` or `(sg_message_id, event, timestamp)`.

### Suppressions

Suppression lists prevent delivery:

- Global unsubscribes
- Group unsubscribes (ASM groups)
- Bounces
- Blocks
- Spam reports

Your system must:

- Respect unsubscribes (CAN-SPAM, GDPR/PECR depending on context).
- Provide list-unsubscribe headers for one-click where appropriate.
- Monitor bounce/spam rates; automatically stop sending to bad addresses.

### Deliverability: SPF/DKIM/DMARC

- SPF: authorizes sending IPs for your domain.
- DKIM: cryptographic signature; SendGrid provides CNAME records for domain authentication.
- DMARC: policy for alignment and reporting; start with `p=none`, move to `quarantine`/`reject`.

### Error Taxonomy (SendGrid API)

- 4xx: request/auth issues; do not blindly retry.
- 429: rate limiting; retry with backoff.
- 5xx: transient; retry with jitter.

---

## Installation & Setup

### Official Python SDK — Email (SendGrid)

**Repository:** https://github.com/twilio/twilio-python  
**PyPI:** `pip install twilio sendgrid` · **Supported:** Python 3.7–3.13

```python
# SendGrid is the email layer (separate package, same Twilio ecosystem)
import sendgrid
from sendgrid.helpers.mail import Mail
import os

sg = sendgrid.SendGridAPIClient(api_key=os.environ["SENDGRID_API_KEY"])

message = Mail(
    from_email="sender@example.com",
    to_emails="recipient@example.com",
    subject="Hello from Python!",
    html_content="<strong>Hello!</strong>"
)
response = sg.send(message)
print(response.status_code)  # 202 = queued
```

Source: [sendgrid/sendgrid-python](https://github.com/sendgrid/sendgrid-python) (official SendGrid Python SDK, part of the Twilio family)

### Ubuntu 22.04 / 24.04

Install Node 20, Python 3.11, and tools:

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg jq python3.11 python3.11-venv python3-pip

# NodeSource Node 20
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

node -v   # v20.11.1 (or later 20.x)
npm -v    # 10.2.4 (or later)
```

Project dependencies (Node):

```bash
mkdir -p services/email-sender
cd services/email-sender
npm init -y
npm install @sendgrid/mail@8.1.3 @sendgrid/client@8.1.3 pino@9.0.0 zod@3.22.4
```

Python venv:

```bash
mkdir -p services/email-worker
cd services/email-worker
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip==23.3.2
pip install sendgrid==6.11.0 fastapi==0.109.2 uvicorn==0.27.1 pydantic==2.6.1
```

### Fedora 39 / 40

```bash
sudo dnf install -y nodejs-20.11.1 npm jq python3.11 python3.11-pip python3.11-virtualenv openssl
node -v
python3.11 -V
```

### macOS 14 (Intel + Apple Silicon)

Using Homebrew:

```bash
brew update
brew install node@20 jq python@3.11 openssl@3
echo 'export PATH="/opt/homebrew/opt/node@20/bin:$PATH"' >> ~/.zshrc  # Apple Silicon
echo 'export PATH="/usr/local/opt/node@20/bin:$PATH"' >> ~/.zshrc     # Intel
source ~/.zshrc

node -v
python3.11 -V
```

### Environment Variables (local dev)

Create `.env` (do not commit):

Path: `services/email-sender/.env`

```dotenv
SENDGRID_API_KEY=SG.xxxxxx.yyyyyy
SENDGRID_FROM_EMAIL=notifications@mg.example.com
SENDGRID_FROM_NAME=Example Notifications
SENDGRID_TEMPLATE_PASSWORD_RESET=d-2f3c4b5a6d7e8f90123456789abcdeff
SENDGRID_TEMPLATE_RECEIPT=d-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
SENDGRID_EVENT_WEBHOOK_PUBLIC_KEY=MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE...
EMAIL_ENV=prod
```

Load it (bash):

```bash
set -a
source .env
set +a
```

---

## Key Capabilities

### Send Transactional Email (v3 Mail Send)

Requirements:

- Use dynamic templates for consistent rendering.
- Add correlation IDs via `custom_args`.
- Implement retry policy for 429/5xx only.
- Enforce per-recipient validation to reduce bounces.

Node example sender (production-safe skeleton):

Path: `services/email-sender/src/send.ts`

```ts
import sgMail from "@sendgrid/mail";
import { z } from "zod";
import pino from "pino";
import crypto from "crypto";

const log = pino({ level: process.env.LOG_LEVEL ?? "info" });

const Env = z.object({
  SENDGRID_API_KEY: z.string().min(20),
  SENDGRID_FROM_EMAIL: z.string().email(),
  SENDGRID_FROM_NAME: z.string().min(1),
  EMAIL_ENV: z.enum(["dev", "staging", "prod"]).default("prod"),
});
const env = Env.parse(process.env);

sgMail.setApiKey(env.SENDGRID_API_KEY);

export type SendTemplateEmailInput = {
  to: string;
  templateId: string;
  dynamicTemplateData: Record<string, unknown>;
  categories?: string[];
  customArgs?: Record<string, string>;
};

function makeIdempotencyKey(input: SendTemplateEmailInput): string {
  // Stable key for same logical send (avoid duplicates on retries)
  const h = crypto.createHash("sha256");
  h.update(input.to);
  h.update(input.templateId);
  h.update(JSON.stringify(input.dynamicTemplateData));
  return h.digest("hex");
}

export async function sendTemplateEmail(input: SendTemplateEmailInput) {
  const idempotencyKey = makeIdempotencyKey(input);

  const msg = {
    to: input.to,
    from: { email: env.SENDGRID_FROM_EMAIL, name: env.SENDGRID_FROM_NAME },
    templateId: input.templateId,
    dynamicTemplateData: input.dynamicTemplateData,
    categories: input.categories ?? ["transactional"],
    customArgs: {
      ...input.customArgs,
      idempotency_key: idempotencyKey,
      env: env.EMAIL_ENV,
    },
    mailSettings: {
      sandboxMode: { enable: env.EMAIL_ENV !== "prod" },
    },
  };

  // SendGrid does not support an explicit idempotency header for /mail/send.
  // You must implement idempotency in your app (e.g., outbox table).
  try {
    const [resp] = await sgMail.send(msg as any, false);
    log.info(
      { statusCode: resp.statusCode, headers: resp.headers, to: input.to, templateId: input.templateId },
      "sendgrid mail.send accepted"
    );
    return { accepted: true, statusCode: resp.statusCode, idempotencyKey };
  } catch (err: any) {
    const statusCode = err?.code ?? err?.response?.statusCode;
    const body = err?.response?.body;
    log.error({ err, statusCode, body, to: input.to, templateId: input.templateId }, "sendgrid mail.send failed");
    throw err;
  }
}
```

Operational notes:

- `mailSettings.sandboxMode.enable=true` prevents actual delivery (use in dev/staging).
- For real idempotency, use an **outbox table** keyed by `(idempotency_key)` and only send once.

### Dynamic Templates: Safe Handlebars Usage

Rules:

- Prefer `{{var}}` (escaped) for user-provided content.
- Avoid `{{{var}}}` unless content is sanitized HTML.
- Keep template logic minimal; compute complex values in code.

Example template data contract:

```json
{
  "app_name": "Example",
  "reset_url": "https://app.example.com/reset?token=9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "support_email": "support@example.com",
  "expires_minutes": 30
}
```

Handlebars snippet:

```handlebars
<p>Reset your {{app_name}} password:</p>
<p><a href="{{reset_url}}">Reset password</a></p>
<p>This link expires in {{expires_minutes}} minutes.</p>
```

### Event Webhook: Verification + Idempotent Processing

SendGrid Event Webhook uses ECDSA signatures:

- Headers:
  - `X-Twilio-Email-Event-Webhook-Signature`
  - `X-Twilio-Email-Event-Webhook-Timestamp`
- Verify signature over: `timestamp + payload` (raw request body)

FastAPI example (raw body + verify):

Path: `services/email-worker/app/webhook.py`

```python
import base64
import hashlib
from fastapi import APIRouter, Request, HTTPException
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature

router = APIRouter()

def verify_sendgrid_signature(public_key_pem: str, signature_b64: str, timestamp: str, payload: bytes) -> None:
    public_key = serialization.load_pem_public_key(public_key_pem.encode("utf-8"))
    if not isinstance(public_key, ec.EllipticCurvePublicKey):
        raise ValueError("public key is not EC")

    signed = timestamp.encode("utf-8") + payload
    sig = base64.b64decode(signature_b64)

    try:
        public_key.verify(sig, signed, ec.ECDSA(hashes.SHA256()))
    except InvalidSignature as e:
        raise

@router.post("/webhooks/sendgrid/events")
async def sendgrid_events(request: Request):
    sig = request.headers.get("X-Twilio-Email-Event-Webhook-Signature")
    ts = request.headers.get("X-Twilio-Email-Event-Webhook-Timestamp")
    if not sig or not ts:
        raise HTTPException(status_code=400, detail="missing signature headers")

    raw = await request.body()

    public_key_pem = request.app.state.sendgrid_event_public_key_pem
    try:
        verify_sendgrid_signature(public_key_pem, sig, ts, raw)
    except Exception:
        raise HTTPException(status_code=401, detail="invalid signature")

    events = await request.json()
    # events is a list of dicts
    # Idempotency: dedupe by sg_event_id
    # Persist first, then ack 2xx.
    return {"ok": True, "count": len(events)}
```

Replay protection:

- Reject timestamps older than e.g. 5 minutes:
  - Compare `ts` to current time; allow small skew.
- Store `(sg_event_id)` with unique constraint; ignore duplicates.

### Suppression Management

Use suppression endpoints to:

- Query if an address is suppressed before sending (optional; can be expensive).
- Remove from suppression only with explicit user action and compliance review.

Common endpoints:

- Global unsubscribes: `/v3/asm/suppressions/global`
- Group unsubscribes: `/v3/asm/groups/{group_id}/suppressions`
- Bounces: `/v3/suppression/bounces`
- Blocks: `/v3/suppression/blocks`
- Spam reports: `/v3/suppression/spam_reports`

### Domain Authentication (SPF/DKIM/DMARC)

Production baseline:

- Use SendGrid Domain Authentication (CNAME-based DKIM).
- SPF: include SendGrid if using their shared IPs; for dedicated IPs, follow SendGrid guidance.
- DMARC:
  - Start: `v=DMARC1; p=none; rua=mailto:dmarc-reports@example.com; ruf=mailto:dmarc-forensics@example.com; fo=1; adkim=s; aspf=s`
  - Move to `quarantine` then `reject` after monitoring.

### IP Warming (Dedicated IP)

If using dedicated IPs:

- Ramp volume gradually (days/weeks).
- Keep complaint rate low; avoid sudden spikes.
- Segment traffic: start with most engaged recipients.

---

## Command Reference

This section covers **SendGrid API via curl** (no official SendGrid CLI is assumed) and common operational commands.

### Authentication Header

All API calls:

- Header: `Authorization: Bearer $SENDGRID_API_KEY`
- Content-Type: `application/json`

### Send Email: `POST /v3/mail/send`

```bash
curl -sS -D /tmp/sg_headers.txt -o /tmp/sg_body.txt \
  -X POST "https://api.sendgrid.com/v3/mail/send" \
  -H "Authorization: Bearer ${SENDGRID_API_KEY}" \
  -H "Content-Type: application/json" \
  --data-binary @- <<'JSON'
{
  "from": { "email": "notifications@mg.example.com", "name": "Example Notifications" },
  "personalizations": [
    {
      "to": [{ "email": "alice@example.net", "name": "Alice" }],
      "dynamic_template_data": {
        "app_name": "Example",
        "reset_url": "https://app.example.com/reset?token=9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
        "expires_minutes": 30
      },
      "custom_args": {
        "user_id": "u_12345",
        "request_id": "req_01HPQ7ZK8Z7WQ2J9R8D2E6M3QK"
      }
    }
  ],
  "template_id": "d-2f3c4b5a6d7e8f90123456789abcdeff",
  "categories": ["password_reset", "transactional"],
  "tracking_settings": {
    "click_tracking": { "enable": true, "enable_text": true },
    "open_tracking": { "enable": true }
  }
}
JSON
```

Relevant behaviors:

- Success: HTTP `202 Accepted` with empty body.
- Failure: HTTP `4xx/5xx` with JSON error details.

### Templates

#### List templates: `GET /v3/templates`

Flags:
- `?generations=dynamic` filter (if supported in your account)
- `?page_size=...` pagination

```bash
curl -sS "https://api.sendgrid.com/v3/templates?generations=dynamic&page_size=50" \
  -H "Authorization: Bearer ${SENDGRID_API_KEY}" | jq .
```

#### Get template: `GET /v3/templates/{template_id}`

```bash
curl -sS "https://api.sendgrid.com/v3/templates/d-2f3c4b5a6d7e8f90123456789abcdeff" \
  -H "Authorization: Bearer ${SENDGRID_API_KEY}" | jq .
```

#### Create template: `POST /v3/templates`

```bash
curl -sS -X POST "https://api.sendgrid.com/v3/templates" \
  -H "Authorization: Bearer ${SENDGRID_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"name":"prod_password_reset","generation":"dynamic"}' | jq .
```

#### Add version: `POST /v3/templates/{template_id}/versions`

```bash
curl -sS -X POST "https://api.sendgrid.com/v3/templates/d-2f3c4b5a6d7e8f90123456789abcdeff/versions" \
  -H "Authorization: Bearer ${SENDGRID_API_KEY}" \
  -H "Content-Type: application/json" \
  -d @- <<'JSON' | jq .
{
  "active": 0,
  "name": "v2026-02-21",
  "subject": "Reset your password",
  "html_content": "<p>Reset your password: <a href=\"{{reset_url}}\">Reset</a></p>",
  "plain_content": "Reset your password: {{reset_url}}"
}
JSON
```

#### Activate version: `PATCH /v3/templates/{template_id}/versions/{version_id}`

```bash
curl -sS -X PATCH "https://api.sendgrid.com/v3/templates/d-2f3c4b5a6d7e8f90123456789abcdeff/versions/3c1b2a9d-0f2a-4c7b-9d2a-1a2b3c4d5e6f" \
  -H "Authorization: Bearer ${SENDGRID_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"active":1}' | jq .
```

### Event Webhook Configuration

#### Get settings: `GET /v3/user/webhooks/event/settings`

```bash
curl -sS "https://api.sendgrid.com/v3/user/webhooks/event/settings" \
  -H "Authorization: Bearer ${SENDGRID_API_KEY}" | jq .
```

#### Update settings: `PATCH /v3/user/webhooks/event/settings`

Key fields:
- `enabled` (boolean)
- `url` (string)
- `group_resubscribe`, `group_unsubscribe`, `spam_report`, `bounce`, `deferred`, `delivered`, `dropped`, `open`, `click`, `processed`, `unsubscribe` (booleans)
- `oauth_client_id`, `oauth_client_secret`, `oauth_token_url` (if using OAuth; uncommon)

```bash
curl -sS -X PATCH "https://api.sendgrid.com/v3/user/webhooks/event/settings" \
  -H "Authorization: Bearer ${SENDGRID_API_KEY}" \
  -H "Content-Type: application/json" \
  -d @- <<'JSON' | jq .
{
  "enabled": true,
  "url": "https://email-hooks.example.com/webhooks/sendgrid/events",
  "delivered": true,
  "bounce": true,
  "dropped": true,
  "deferred": true,
  "spam_report": true,
  "unsubscribe": true,
  "group_unsubscribe": true,
  "group_resubscribe": true,
  "open": true,
  "click": true,
  "processed": true
}
JSON
```

### Suppressions

#### Global unsubscribes: list: `GET /v3/asm/suppressions/global`

Pagination:
- `?offset=0&limit=500`

```bash
curl -sS "https://api.sendgrid.com/v3/asm/suppressions/global?offset=0&limit=500" \
  -H "Authorization: Bearer ${SENDGRID_API_KEY}" | jq .
```

#### Add global unsubscribe: `POST /v3/asm/suppressions/global`

```bash
curl -sS -X POST "https://api.sendgrid.com/v3/asm/suppressions/global" \
  -H "Authorization: Bearer ${SENDGRID_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"recipient_emails":["alice@example.net"]}' | jq .
```

#### Delete global unsubscribe: `DELETE /v3/asm/suppressions/global/{email}`

```bash
curl -sS -X DELETE "https://api.sendgrid.com/v3/asm/suppressions/global/alice%40example.net" \
  -H "Authorization: Bearer ${SENDGRID_API_KEY}" -i
```

#### Bounces: `GET /v3/suppression/bounces`

Filters:
- `?start_time=1708473600&end_time=1708560000` (unix seconds)
- `?email=alice@example.net`

```bash
curl -sS "https://api.sendgrid.com/v3/suppression/bounces?email=alice@example.net" \
  -H "Authorization: Bearer ${SENDGRID_API_KEY}" | jq .
```

#### Delete bounce: `DELETE /v3/suppression/bounces/{email}`

```bash
curl -sS -X DELETE "https://api.sendgrid.com/v3/suppression/bounces/alice%40example.net" \
  -H "Authorization: Bearer ${SENDGRID_API_KEY}" -i
```

### Diagnostics

#### Check DNS records (SPF/DKIM/DMARC)

```bash
dig +short TXT example.com
dig +short TXT _dmarc.example.com
dig +short CNAME s1._domainkey.mg.example.com
dig +short CNAME s2._domainkey.mg.example.com
```

#### TLS endpoint check (webhook receiver)

```bash
openssl s_client -connect email-hooks.example.com:443 -servername email-hooks.example.com -tls1_2 </dev/null 2>/dev/null | openssl x509 -noout -issuer -subject -dates
```

---

## Configuration Reference

### Node service config

Path: `services/email-sender/config/email.config.toml`

```toml
[sendgrid]
api_base_url = "https://api.sendgrid.com"
from_email = "notifications@mg.example.com"
from_name = "Example Notifications"

[templates]
password_reset = "d-2f3c4b5a6d7e8f90123456789abcdeff"
receipt = "d-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

[webhook]
event_public_key_pem_path = "/etc/email-sender/sendgrid_event_webhook_public_key.pem"

[delivery]
categories = ["transactional"]
sandbox_mode = false

[retry]
max_attempts = 5
base_delay_ms = 200
max_delay_ms = 5000
retry_on_status = [429, 500, 502, 503, 504]
```

### Systemd unit (Linux)

Path: `/etc/systemd/system/email-sender.service`

```ini
[Unit]
Description=Email Sender Service (SendGrid)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=email
Group=email
WorkingDirectory=/opt/email-sender
Environment=NODE_ENV=production
EnvironmentFile=/etc/email-sender/email-sender.env
ExecStart=/usr/bin/node /opt/email-sender/dist/index.js
Restart=on-failure
RestartSec=2
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/lib/email-sender
AmbientCapabilities=
CapabilityBoundingSet=
LockPersonality=true
MemoryDenyWriteExecute=true

[Install]
WantedBy=multi-user.target
```

Path: `/etc/email-sender/email-sender.env`

```dotenv
SENDGRID_API_KEY=SG.xxxxxx.yyyyyy
SENDGRID_FROM_EMAIL=notifications@mg.example.com
SENDGRID_FROM_NAME=Example Notifications
LOG_LEVEL=info
EMAIL_ENV=prod
```

### NGINX reverse proxy for webhook receiver

Path: `/etc/nginx/conf.d/sendgrid-webhook.conf`

```nginx
server {
  listen 443 ssl http2;
  server_name email-hooks.example.com;

  ssl_certificate     /etc/letsencrypt/live/email-hooks.example.com/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/email-hooks.example.com/privkey.pem;
  ssl_protocols TLSv1.2 TLSv1.3;
  ssl_ciphers HIGH:!aNULL:!MD5;

  client_max_body_size 2m;

  location /webhooks/sendgrid/events {
    proxy_pass http://127.0.0.1:8080/webhooks/sendgrid/events;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;

    proxy_connect_timeout 2s;
    proxy_read_timeout 5s;
    proxy_send_timeout 5s;
  }
}
```

---

## Integration Patterns

### Outbox Pattern (DB-backed idempotency)

Use when email sends are triggered by DB transactions.

Pattern:

1. In the same DB transaction as your business event, insert into `email_outbox`.
2. A worker reads pending rows, sends via SendGrid, marks sent with `sent_at` and stores `provider_response`.
3. Retries are safe because the outbox row is unique per logical email.

PostgreSQL schema:

```sql
CREATE TABLE email_outbox (
  id bigserial PRIMARY KEY,
  idempotency_key text NOT NULL UNIQUE,
  to_email text NOT NULL,
  template_id text NOT NULL,
  dynamic_template_data jsonb NOT NULL,
  categories text[] NOT NULL DEFAULT ARRAY['transactional'],
  created_at timestamptz NOT NULL DEFAULT now(),
  sent_at timestamptz,
  last_error text,
  attempt_count int NOT NULL DEFAULT 0
);

CREATE INDEX email_outbox_pending_idx ON email_outbox (created_at) WHERE sent_at IS NULL;
```

### Correlation IDs across Twilio cluster

- For SMS/Voice/Verify + Email, standardize:
  - `request_id` (ingress)
  - `user_id`
  - `notification_id` (logical notification)
- For SendGrid:
  - Put these into `custom_args` so they appear in Event Webhook payloads.

### Webhook ingestion pipeline

Recommended flow:

- Public endpoint receives webhook → verifies signature → enqueues raw events to Kafka/SQS/PubSub → async consumer updates DB/metrics.

Benefits:

- Avoids webhook timeouts.
- Allows replay and backfill.
- Centralizes dedupe.

Example SQS enqueue (pseudo):

- HTTP handler:
  - Validate signature
  - `SendMessageBatch` with raw JSON lines
  - Return 200 quickly

### CI/CD template promotion

Treat templates as code:

- Store template source in repo: `templates/sendgrid/password_reset/v2026-02-21.html`
- CI job:
  - Create new version via API
  - Run render tests (Handlebars compile + sample data)
  - Activate version after approval

---

## Error Handling & Troubleshooting

Include the exact error text and what to do.

1) **401 Unauthorized (bad API key)**  
Symptom (curl):

```text
HTTP/2 401
{"errors":[{"message":"Permission denied, wrong credentials","field":null,"help":null}]}
```

Root cause:
- `SENDGRID_API_KEY` invalid/revoked, or missing required scopes.

Fix:
- Regenerate API key with `mail.send`.
- Ensure your runtime is loading the correct secret (check env var source, secret mount).

2) **403 Forbidden (scope missing)**

```text
HTTP/2 403
{"errors":[{"message":"access forbidden","field":null,"help":null}]}
```

Root cause:
- API key lacks permission for endpoint (e.g., templates write).

Fix:
- Update API key permissions or create a separate key for template management.

3) **400 Bad Request: invalid email**  

```text
{"errors":[{"message":"The email address is invalid.","field":"personalizations.0.to.0.email","help":"http://sendgrid.com/docs/API_Reference/Web_API_v3/Mail/errors.html#message.personalizations.to.email"}]}
```

Root cause:
- Bad `to` address formatting.

Fix:
- Validate emails before enqueueing.
- If sourced from user input, require verification and normalization.

4) **400 Bad Request: template not found / wrong template id**

```text
{"errors":[{"message":"The template_id is not a valid template ID.","field":"template_id","help":"http://sendgrid.com/docs/API_Reference/Web_API_v3/Mail/errors.html"}]}
```

Root cause:
- Using a legacy template ID or wrong environment template.

Fix:
- Confirm template exists via `GET /v3/templates/{id}`.
- Ensure you’re using a **dynamic template** ID starting with `d-`.

5) **429 Too Many Requests**

```text
HTTP/2 429
{"errors":[{"message":"Too many requests","field":null,"help":null}]}
```

Root cause:
- Account or IP rate limit exceeded; burst traffic.

Fix:
- Implement exponential backoff with jitter.
- Batch sends where possible.
- If sustained, request higher limits or use multiple IPs (dedicated) with warming.

6) **413 Payload Too Large (webhook receiver)**

NGINX:

```text
413 Request Entity Too Large
```

Root cause:
- SendGrid batches events; payload exceeds `client_max_body_size`.

Fix:
- Increase `client_max_body_size` (e.g., 2m or 5m).
- Ensure app can parse large JSON arrays efficiently.

7) **401 invalid signature (your webhook verifier)**

Your service logs:

```text
HTTP 401 {"detail":"invalid signature"}
```

Root cause:
- Using parsed JSON instead of raw body for signature verification.
- Wrong public key (rotated or copied incorrectly).
- Timestamp mismatch if you include replay checks.

Fix:
- Verify against raw request bytes exactly as received.
- Fetch correct public key from SendGrid Event Webhook settings.
- Allow small clock skew; ensure NTP is working.

8) **Dropped events: suppressed address**

Event webhook includes:

```json
{
  "event":"dropped",
  "reason":"Bounced Address",
  "email":"alice@example.net"
}
```

Root cause:
- Recipient is on bounce/block/spam suppression list.

Fix:
- Stop sending to the address.
- Provide user remediation flow (update email, confirm address).
- Only remove suppression if you have a legitimate reason and user confirmation.

9) **550 5.1.1 bounce (mailbox does not exist)**

Event webhook bounce:

```json
{
  "event":"bounce",
  "status":"5.1.1",
  "reason":"550 5.1.1 The email account that you tried to reach does not exist."
}
```

Root cause:
- Recipient address invalid or deleted.

Fix:
- Mark address as invalid in your user DB.
- Require user to update email; do not retry.

10) **Deferred (temporary failure)**

```json
{
  "event":"deferred",
  "response":"451 4.7.1 Try again later",
  "attempt":"2"
}
```

Root cause:
- Temporary receiving server throttling.

Fix:
- No action required; SendGrid retries.
- If persistent for a domain, consider domain-specific throttling and content review.

---

## Security Hardening

### Secrets handling

- Store `SENDGRID_API_KEY` only in a secret manager; never in repo or container image.
- Rotate API keys quarterly (or per incident).
- Use separate keys per environment and per capability:
  - `prod-mail-send` (mail.send only)
  - `prod-templates-admin` (templates.* only, restricted to CI)

### Webhook endpoint hardening

- Require HTTPS; redirect HTTP to HTTPS.
- Verify ECDSA signature and timestamp.
- Enforce request size limits (but high enough for batches).
- Rate limit by IP (careful: SendGrid uses multiple IPs; allowlist is brittle).
- Log minimal PII; hash emails in logs where possible.

### OS / runtime hardening (CIS-aligned)

- Linux:
  - Run as non-root user (`User=email`).
  - `NoNewPrivileges=true`, `ProtectSystem=strict`, `ProtectHome=true` in systemd.
  - Keep base image minimal (distroless or slim) if containerized.
- TLS:
  - Disable TLS 1.0/1.1 (CIS recommends TLS 1.2+).
- Dependency hygiene:
  - Node: `npm audit` in CI; pin versions with lockfile.
  - Python: `pip-audit` and hash-locked requirements for prod.

### Email content security

- Never inject unsanitized HTML into templates.
- Avoid including secrets in URLs; use short-lived tokens.
- Use `List-Unsubscribe` where applicable; for transactional, still consider preference center.

---

## Performance Tuning

### Throughput: batching and connection reuse

- SendGrid `/v3/mail/send` supports multiple personalizations in one request.
- For high volume, batch recipients by template and payload shape.

Expected impact:
- Before: 1 request/email → high overhead, more 429s.
- After: 1 request/100 personalizations (where content allows) → fewer requests, lower latency variance.

Constraints:
- Personalization data differs per recipient; still can batch if template is same and data is per personalization.

### Worker concurrency

- Use bounded concurrency (e.g., 50 in-flight requests) to avoid self-induced 429.
- Adaptive backoff on 429.

### Webhook ingestion

- Parse JSON with streaming if payloads are large (language-dependent).
- Acknowledge quickly after enqueue; do not do heavy DB work inline.

### Deliverability performance

- Reduce bounces by validating addresses at capture time.
- Use domain authentication; improves inbox placement and reduces deferrals.

---

## Advanced Topics

### Handling “open” and “click” events

- Opens are unreliable (Apple Mail Privacy Protection, image proxying).
- Clicks are more reliable but still subject to bot scanning.
- Use events for aggregate analytics, not strict per-user state unless you have bot filtering.

### Custom Args vs Categories

- `custom_args`: key/value, appears in event webhook; best for correlation IDs.
- `categories`: array of strings; used for SendGrid stats/analytics grouping.

Production guidance:
- Keep categories low-cardinality (e.g., `password_reset`, `receipt`), not per-user.

### Inbound Parse Webhook (if receiving email)

If you use SendGrid Inbound Parse:

- Configure MX records to SendGrid parse host.
- Endpoint receives multipart form-data with fields like `from`, `to`, `subject`, `text`, `html`, `attachments`.

Hardening:
- Validate SPF/DKIM/DMARC results if provided; otherwise treat as untrusted input.
- Enforce attachment size/type limits.

### Multi-tenant sending

If sending on behalf of multiple brands/domains:

- Separate authenticated domains and from addresses.
- Consider subusers (SendGrid feature) for isolation.
- Ensure per-tenant suppression compliance.

### Dedicated IP pools and geo considerations

- If you operate in multiple regions, consider separate IP pools per region to isolate reputation.
- Warm each pool independently.

---

## Usage Examples

### 1) Password reset email (dynamic template + outbox)

1. API server writes outbox row:

```sql
INSERT INTO email_outbox (idempotency_key, to_email, template_id, dynamic_template_data, categories)
VALUES (
  'email:password_reset:u_12345:req_01HPQ7ZK8Z7WQ2J9R8D2E6M3QK',
  'alice@example.net',
  'd-2f3c4b5a6d7e8f90123456789abcdeff',
  '{"app_name":"Example","reset_url":"https://app.example.com/reset?token=9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d","expires_minutes":30}',
  ARRAY['password_reset','transactional']
);
```

2. Worker reads pending rows, calls `sendTemplateEmail`, marks sent.

3. Event webhook updates delivery status keyed by `custom_args.request_id`.

### 2) Receipt email with PDF attachment

SendGrid supports attachments (base64). Keep size small; large attachments hurt deliverability.

```bash
PDF_B64="$(base64 -w 0 receipt_2026-02-21.pdf)"
curl -sS -X POST "https://api.sendgrid.com/v3/mail/send" \
  -H "Authorization: Bearer ${SENDGRID_API_KEY}" \
  -H "Content-Type: application/json" \
  -d @- <<JSON
{
  "from": { "email": "billing@mg.example.com", "name": "Example Billing" },
  "personalizations": [
    {
      "to": [{ "email": "alice@example.net" }],
      "dynamic_template_data": {
        "amount": "49.00",
        "currency": "USD",
        "receipt_id": "rcpt_9f3a2c1d"
      },
      "custom_args": { "receipt_id": "rcpt_9f3a2c1d" }
    }
  ],
  "template_id": "d-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "attachments": [
    {
      "content": "${PDF_B64}",
      "type": "application/pdf",
      "filename": "receipt_rcpt_9f3a2c1d.pdf",
      "disposition": "attachment"
    }
  ],
  "categories": ["receipt","transactional"]
}
JSON
```

### 3) Webhook receiver with dedupe (Postgres unique constraint)

Schema:

```sql
CREATE TABLE sendgrid_events (
  sg_event_id text PRIMARY KEY,
  sg_message_id text,
  event text NOT NULL,
  email text NOT NULL,
  ts bigint NOT NULL,
  payload jsonb NOT NULL,
  received_at timestamptz NOT NULL DEFAULT now()
);
```

Insert with conflict ignore:

```sql
INSERT INTO sendgrid_events (sg_event_id, sg_message_id, event, email, ts, payload)
VALUES ($1, $2, $3, $4, $5, $6)
ON CONFLICT (sg_event_id) DO NOTHING;
```

### 4) Suppression-aware sending (pre-check for high-value emails)

For critical emails (e.g., legal notices), you may pre-check suppression:

```bash
curl -sS "https://api.sendgrid.com/v3/asm/suppressions/global/alice%40example.net" \
  -H "Authorization: Bearer ${SENDGRID_API_KEY}" -i
```

- If `200 OK`, user is globally unsubscribed → do not send.
- If `404 Not Found`, not suppressed globally → proceed (still could be bounced/blocked).

Use sparingly; it adds latency and API load.

### 5) Domain authentication verification checklist

1. Confirm DKIM CNAMEs resolve:

```bash
dig +short CNAME s1._domainkey.mg.example.com
dig +short CNAME s2._domainkey.mg.example.com
```

2. Confirm DMARC exists:

```bash
dig +short TXT _dmarc.example.com
```

3. Send test email to Gmail and inspect “Authentication-Results”:
- `spf=pass`
- `dkim=pass`
- `dmarc=pass`

### 6) Rate-limit resilient sender (retry policy)

Pseudo-policy:

- Retry on: 429, 500, 502, 503, 504
- Backoff: `min(max_delay, base * 2^attempt) + random(0, 100ms)`
- Max attempts: 5
- Do not retry on 400/401/403.

---

## Quick Reference

| Task | Command / Endpoint | Key flags / fields |
|---|---|---|
| Send email | `POST /v3/mail/send` | `template_id`, `personalizations[]`, `dynamic_template_data`, `custom_args`, `categories`, `mail_settings.sandboxMode` |
| List templates | `GET /v3/templates` | `generations=dynamic`, `page_size` |
| Create template | `POST /v3/templates` | `name`, `generation:"dynamic"` |
| Add template version | `POST /v3/templates/{id}/versions` | `name`, `subject`, `html_content`, `plain_content`, `active` |
| Activate version | `PATCH /v3/templates/{id}/versions/{vid}` | `active:1` |
| Get webhook settings | `GET /v3/user/webhooks/event/settings` | n/a |
| Update webhook settings | `PATCH /v3/user/webhooks/event/settings` | `enabled`, `url`, event toggles |
| List global unsub | `GET /v3/asm/suppressions/global` | `offset`, `limit` |
| Add global unsub | `POST /v3/asm/suppressions/global` | `recipient_emails[]` |
| Remove global unsub | `DELETE /v3/asm/suppressions/global/{email}` | URL-encode email |
| List bounces | `GET /v3/suppression/bounces` | `email`, `start_time`, `end_time` |
| Remove bounce | `DELETE /v3/suppression/bounces/{email}` | URL-encode email |
| DNS check | `dig` | `_dmarc`, `_domainkey`, SPF TXT |

---

## Graph Relationships

### DEPENDS_ON

- `twilio-email` DEPENDS_ON:
  - Secure secret storage (Vault/AWS Secrets Manager/GCP Secret Manager)
  - HTTPS ingress (NGINX/ALB/API Gateway) for webhooks
  - Persistent store for idempotency/dedupe (PostgreSQL/DynamoDB)
  - Observability stack (structured logs + metrics + tracing)

### COMPOSES

- `twilio-email` COMPOSES with:
  - `twilio-messaging` (SMS fallback when email bounces or is suppressed)
  - `twilio-verify` (email channel for OTP; verify + transactional email coordination)
  - `twilio-studio` (trigger flows that send email + SMS; webhook-driven orchestration)
  - Queue systems (SQS/Kafka/PubSub) for webhook ingestion and outbox workers

### SIMILAR_TO

- SIMILAR_TO:
  - AWS SES transactional email patterns (webhook/event-driven bounces/complaints)
  - Mailgun transactional email patterns (webhooks + suppression lists)
  - Postmark transactional email patterns (templates + message streams)
