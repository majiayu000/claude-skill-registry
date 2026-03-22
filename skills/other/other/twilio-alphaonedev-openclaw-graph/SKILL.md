---
name: twilio
cluster: twilio
description: "Twilio root: account management, API keys, sub-accounts, console, billing, rate limits, error codes"
tags: ["twilio","sms","voice","communications"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "twilio account api key sub-account billing rate limit"
---

# twilio

## Purpose

Enable OpenClaw to operate Twilio “root” production workflows end-to-end: account and subaccount management, API keys and auth, console/billing/rate limits, and the operational patterns that sit on top (Messaging/Voice/Verify/SendGrid/Studio). This skill is for engineers who need to:

- Provision and rotate credentials safely (API Keys, Auth Tokens, SendGrid keys), including per-environment isolation.
- Debug and remediate production incidents (webhook failures, carrier errors, rate limits, invalid numbers, auth errors).
- Implement production-grade Messaging/Voice/Verify flows with correct compliance (STOP handling, 10DLC, toll-free verification).
- Control cost and performance (messaging services with geo-matching, concurrency, retry/backoff, recording/transcription costs).
- Automate Twilio operations via CLI + REST APIs + IaC patterns.

## Prerequisites

### Accounts and access

- Twilio account with Console access: https://console.twilio.com/
- For Messaging in US:
  - A2P 10DLC brand + campaign registration (required for most US long-code messaging).
  - Toll-free verification if using toll-free numbers for A2P.
  - Short code approval if using short codes.
- For WhatsApp:
  - WhatsApp Business Account (WABA) and Twilio WhatsApp sender configured.
- For Voice:
  - A Twilio phone number with Voice capability.
  - If using SIP trunking: Twilio Elastic SIP Trunking enabled.
- For Verify:
  - Verify service created (Verify V2).
- For SendGrid:
  - SendGrid account (can be separate from Twilio login), API key with appropriate scopes.

### Local tooling (exact versions)

- Node.js **20.11.1** (LTS) or **18.19.1** (LTS)
- Python **3.11.8** or **3.12.2**
- curl **8.5.0+**
- jq **1.7+**
- OpenSSL **3.0.13+** (for signature verification tooling)
- Docker **25.0.3+** (optional, for local webhook receivers and integration tests)

### Twilio SDKs (recommended pinned versions)

- Node: `twilio` **4.23.0**
- Python: `twilio` **9.0.5**
- SendGrid Node: `@sendgrid/mail` **8.1.1**
- SendGrid Python: `sendgrid` **6.11.0**

### Auth setup (Twilio)

Twilio supports:
- **Account SID** (starts with `AC...`)
- **Auth Token** (secret)
- **API Key SID** (starts with `SK...`) + **API Key Secret** (preferred over Auth Token for apps/CI)
- **Subaccounts** (each has its own Account SID/Auth Token; API Keys can be created per account)

Minimum recommended production posture:
- Use **API Key** + **Secret** in apps/CI.
- Keep **Auth Token** only for break-glass and console use; rotate if exposed.
- Separate **subaccounts** per environment (prod/stage/dev) and/or per tenant.

### Twilio CLI (optional but strongly recommended)

Twilio CLI is useful for interactive operations; for automation prefer REST + IaC, but CLI is still valuable for incident response.

- Twilio CLI: `twilio-cli` **5.17.0**
- Plugins:
  - `@twilio-labs/plugin-serverless` **3.0.2** (for Twilio Functions/Assets)
  - `@twilio-labs/plugin-flex` **6.0.6** (if using Flex)

Install via npm (see Installation & Setup).

## Core Concepts

### Accounts, subaccounts, projects

- **Account**: top-level billing entity. Identified by `AccountSid` (`AC...`).
- **Subaccount**: child account with its own credentials, numbers, messaging services, etc. Useful for environment isolation and tenant isolation.
- **Project**: Twilio Console UI grouping; not a separate security boundary. Don’t confuse with subaccounts.

Production pattern:
- One parent account for billing.
- Subaccounts per environment: `prod`, `staging`, `dev`.
- Optionally subaccounts per customer/tenant if you need strict isolation and separate phone number pools.

### Credentials

- **Auth Token**: master secret for an account. High blast radius.
- **API Keys**: scoped to an account; can be revoked without rotating Auth Token.
- **Key rotation**: create new key, deploy, verify, revoke old key.

### Messaging architecture

- **From** can be:
  - A phone number (10DLC long code, toll-free, short code)
  - A **Messaging Service SID** (`MG...`) which selects an appropriate sender (pooling, geo-match, sticky sender)
- **Status callbacks**: message lifecycle events via webhook:
  - `queued`, `sent`, `delivered`, `undelivered`, `failed` (and sometimes `read` for channels that support it, e.g., WhatsApp)
- **STOP handling**:
  - Twilio has built-in opt-out handling for many channels; you must not override it incorrectly.
  - Your app should treat STOP as a compliance event and suppress future sends to that recipient unless they opt back in (e.g., START).

### Voice architecture

- **TwiML**: XML instructions returned by your webhook to control calls.
  - `<Dial>`, `<Conference>`, `<Record>`, `<Say>` (with Polly voices), `<Gather>` for IVR.
- **Call status callbacks**: webhooks for call events.
- **Recording**: can be enabled per call or per conference; transcription is separate and has cost/latency.
- **SIP trunking**: connect PBX/SBC to Twilio; requires careful auth and IP ACLs.

### Verify V2

- Verify Service (`VA...`) defines channel configuration and policies.
- Verify checks are rate-limited and fraud-protected; you must handle `429` and Verify-specific error codes.
- Custom channels: email/push/TOTP can be integrated; treat as separate trust and deliverability domains.

### SendGrid

- Transactional vs marketing:
  - Transactional: API-driven, low latency, templated.
  - Marketing: campaigns, list management, compliance.
- Dynamic templates use Handlebars.
- Inbound Parse: webhook that turns inbound email into HTTP POST.

### Studio

- Studio Flows are state machines managed in Twilio.
- REST Trigger API can start a flow execution.
- Export/import flows for version control; A/B testing via Split widgets.

### Rate limits and retries

- Twilio enforces per-account and per-resource rate limits; you will see `20429` and HTTP `429`.
- Webhooks are retried by Twilio on non-2xx responses; your endpoints must be idempotent.

## Installation & Setup

### Official Python SDK

**Repository:** https://github.com/twilio/twilio-python  
**PyPI:** https://pypi.org/project/twilio/ · **Supported:** Python 3.7–3.13

```shell
pip install twilio
```

```python
from twilio.rest import Client
import os

# Environment variables (recommended)
client = Client()  # reads TWILIO_ACCOUNT_SID + TWILIO_AUTH_TOKEN

# API Key auth (preferred for production)
client = Client(
    os.environ["TWILIO_API_KEY"],
    os.environ["TWILIO_API_SECRET"],
    os.environ["TWILIO_ACCOUNT_SID"]
)

# Regional edge routing
client = Client(region='au1', edge='sydney')
```

Source: [twilio/twilio-python — client auth](https://github.com/twilio/twilio-python/blob/main/README.md#api-credentials)

### Ubuntu 22.04 / 24.04 (x86_64)

Install dependencies:

```bash
sudo apt-get update
sudo apt-get install -y curl jq ca-certificates gnupg lsb-release openssl
```

Node.js 20.11.1 via NodeSource:

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
node -v  # expect v20.11.x
npm -v
```

Twilio CLI 5.17.0:

```bash
sudo npm install -g twilio-cli@5.17.0
twilio --version
```

Optional plugins:

```bash
twilio plugins:install @twilio-labs/plugin-serverless@3.0.2
twilio plugins:install @twilio-labs/plugin-flex@6.0.6
twilio plugins
```

Python 3.11 (if needed):

```bash
sudo apt-get install -y python3 python3-venv python3-pip
python3 --version
```

### Fedora 39 / 40 (x86_64)

```bash
sudo dnf install -y curl jq openssl nodejs npm python3 python3-pip
node -v
sudo npm install -g twilio-cli@5.17.0
twilio --version
```

### macOS 14 (Sonoma) Intel

Homebrew:

```bash
brew update
brew install node@20 jq openssl@3 python@3.12
brew link --force --overwrite node@20
node -v
```

Twilio CLI:

```bash
npm install -g twilio-cli@5.17.0
twilio --version
```

### macOS 14 (Sonoma) Apple Silicon (ARM64)

Same as Intel; ensure correct PATH:

```bash
brew install node@20 jq openssl@3 python@3.12
echo 'export PATH="/opt/homebrew/opt/node@20/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
node -v
npm install -g twilio-cli@5.17.0
twilio --version
```

### Twilio CLI authentication

Interactive login (stores token in local config):

```bash
twilio login
```

Non-interactive (CI) using env vars (preferred):

```bash
export TWILIO_ACCOUNT_SID="YOUR_ACCOUNT_SID"
export TWILIO_API_KEY="YOUR_API_KEY_SID"
export TWILIO_API_SECRET="your_api_key_secret_here"
```

If you must use Auth Token (not recommended for CI):

```bash
export TWILIO_AUTH_TOKEN="your_auth_token_here"
```

Verify auth:

```bash
twilio api:core:accounts:fetch --sid "$TWILIO_ACCOUNT_SID"
```

### SDK installation (Node)

```bash
mkdir -p twilio-app && cd twilio-app
npm init -y
npm install twilio@4.23.0
npm install @sendgrid/mail@8.1.1
```

### SDK installation (Python)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install twilio==9.0.5 sendgrid==6.11.0
```

## Key Capabilities

### Account management (root + subaccounts)

- List accounts/subaccounts, create/close subaccounts.
- Rotate API keys.
- Fetch usage and billing signals (where available via API).
- Enforce environment isolation via subaccounts.

### Programmable Messaging (SMS/MMS/WhatsApp)

- Send messages via `From` number or Messaging Service (`MessagingServiceSid`).
- Implement status callbacks and webhook verification.
- Handle STOP/START opt-out correctly.
- Support US compliance: 10DLC campaigns, toll-free verification, short codes.
- Cost optimization: geo-matching, sticky sender, sender pools.

### Voice (TwiML + SDK + SIP + IVR)

- TwiML endpoints for inbound/outbound call control.
- Conferences, recordings, transcription.
- IVR state machines with `<Gather>` and server-side session state.
- SIP trunking integration patterns and security.

### Verify V2

- Create Verify services, send verification codes, check codes.
- Custom channels (email/push/TOTP) patterns.
- Fraud guard and rate limiting handling.

### SendGrid

- Transactional email with dynamic templates.
- Inbound Parse webhook ingestion.
- Bounce/spam handling and suppression management.
- IP warming and deliverability monitoring patterns.

### Studio

- Trigger flows via REST.
- Export/import flows for version control.
- Split-based A/B testing patterns.

### Error handling and operational excellence

- Map common Twilio error codes to remediation steps.
- Implement webhook retry-safe endpoints.
- Rate limit backoff and idempotency keys.

## Command Reference

> Notes:
> - Twilio CLI command groups can vary slightly by CLI version and installed plugins. The commands below are validated against `twilio-cli@5.17.0` with default plugins.
> - For automation, prefer direct REST calls; CLI is best for interactive ops.

### Global Twilio CLI flags

Applies to most `twilio ...` commands:

- `-h, --help`: show help
- `-v, --version`: show CLI version
- `-l, --log-level <level>`: `debug|info|warn|error`
- `-o, --output <format>`: `json|tsv` (varies by command)
- `--profile <name>`: use a named profile from `~/.twilio-cli/config.json`

Examples:

```bash
twilio -l debug api:core:accounts:fetch --sid "$TWILIO_ACCOUNT_SID"
twilio --profile prod api:core:messages:list --limit 20 -o json
```

### Auth and profiles

Login:

```bash
twilio login
```

List profiles:

```bash
twilio profiles:list
```

Use a profile:

```bash
twilio --profile prod api:core:accounts:fetch --sid YOUR_ACCOUNT_SID
```

### Accounts (Core API)

Fetch account:

```bash
twilio api:core:accounts:fetch --sid YOUR_ACCOUNT_SID
```

List accounts (includes subaccounts):

```bash
twilio api:core:accounts:list --limit 50
```

Flags:
- `--limit <n>`: max records to return
- `--page-size <n>`: page size for API pagination
- `--friendly-name <name>`: filter by friendly name (where supported)

Create subaccount:

```bash
twilio api:core:accounts:create --friendly-name "prod-messaging"
```

Update account status (close subaccount):

```bash
twilio api:core:accounts:update --sid YOUR_ACCOUNT_SID --status closed
```

Flags:
- `--friendly-name <name>`
- `--status <status>`: `active|suspended|closed`

### API Keys (Core API)

List API keys:

```bash
twilio api:core:keys:list --limit 50
```

Create API key:

```bash
twilio api:core:keys:create --friendly-name "ci-prod-2026-02" --key-type standard
```

Flags:
- `--friendly-name <name>`
- `--key-type <type>`: `standard|restricted` (restricted requires additional configuration; prefer standard unless you have a clear policy model)

Fetch key:

```bash
twilio api:core:keys:fetch --sid YOUR_API_KEY_SID
```

Delete key (revoke):

```bash
twilio api:core:keys:remove --sid YOUR_API_KEY_SID
```

### Messaging (Core API)

Send SMS via `From`:

```bash
twilio api:core:messages:create \
  --from "+14155550100" \
  --to "+14155550199" \
  --body "prod smoke test 2026-02-21T18:42Z" \
  --status-callback "https://api.example.com/twilio/sms/status"
```

Send via Messaging Service:

```bash
twilio api:core:messages:create \
  --messaging-service-sid YOUR_MG_SID \
  --to "+14155550199" \
  --body "geo-match send via MG"
```

Important flags:
- `--from <E.164>`: sender number
- `--to <E.164>`: recipient
- `--body <text>`
- `--media-url <url>`: repeatable for MMS
- `--messaging-service-sid <MG...>`: use messaging service instead of `--from`
- `--status-callback <url>`: message status webhook
- `--max-price <decimal>`: cap price (channel-dependent)
- `--provide-feedback <boolean>`: request delivery feedback (where supported)
- `--validity-period <seconds>`: TTL for message
- `--force-delivery <boolean>`: attempt to force delivery (limited applicability)
- `--application-sid <AP...>`: messaging application (legacy patterns)
- `--smart-encoded <boolean>`: enable smart encoding

List messages:

```bash
twilio api:core:messages:list --limit 20
```

Filter list:

```bash
twilio api:core:messages:list --to "+14155550199" --date-sent 2026-02-21 --limit 50
```

Fetch message:

```bash
twilio api:core:messages:fetch --sid SM0123456789abcdef0123456789abcdef
```

### Incoming phone numbers

List numbers:

```bash
twilio api:core:incoming-phone-numbers:list --limit 50
```

Purchase a number (availability varies):

```bash
twilio api:core:available-phone-numbers:us:local:list --area-code 415 --limit 5
twilio api:core:incoming-phone-numbers:create --phone-number "+14155550100" --friendly-name "prod-sms-415-0100"
```

Configure webhook URLs on a number:

```bash
twilio api:core:incoming-phone-numbers:update \
  --sid PN0123456789abcdef0123456789abcdef \
  --sms-url "https://api.example.com/twilio/sms/inbound" \
  --sms-method POST \
  --voice-url "https://api.example.com/twilio/voice/inbound" \
  --voice-method POST
```

Flags (commonly used):
- `--sms-url <url>`, `--sms-method <GET|POST>`
- `--voice-url <url>`, `--voice-method <GET|POST>`
- `--status-callback <url>` (voice call status callback for the number, depending on resource)
- `--friendly-name <name>`

### Voice calls

Create outbound call:

```bash
twilio api:core:calls:create \
  --from "+14155550100" \
  --to "+14155550199" \
  --url "https://api.example.com/twilio/voice/twiml/outbound"
```

Flags:
- `--from`, `--to`
- `--url <twiml-webhook-url>`: TwiML instructions endpoint
- `--method <GET|POST>`
- `--status-callback <url>`
- `--status-callback-event <initiated|ringing|answered|completed>` (repeatable)
- `--status-callback-method <GET|POST>`
- `--timeout <seconds>`
- `--record <boolean>`
- `--recording-status-callback <url>`
- `--recording-status-callback-method <GET|POST>`

Fetch call:

```bash
twilio api:core:calls:fetch --sid YOUR_CA_SID
```

List calls:

```bash
twilio api:core:calls:list --from "+14155550100" --start-time 2026-02-21 --limit 50
```

### Verify V2 (REST-first; CLI coverage varies)

Verify is often easiest via REST calls. Example with curl:

Send verification:

```bash
curl -sS -X POST "https://verify.twilio.com/v2/Services/YOUR_VERIFY_SERVICE_SID/Verifications" \
  -u "$TWILIO_API_KEY:$TWILIO_API_SECRET" \
  --data-urlencode "To=+14155550199" \
  --data-urlencode "Channel=sms"
```

Check verification:

```bash
curl -sS -X POST "https://verify.twilio.com/v2/Services/YOUR_VERIFY_SERVICE_SID/VerificationCheck" \
  -u "$TWILIO_API_KEY:$TWILIO_API_SECRET" \
  --data-urlencode "To=+14155550199" \
  --data-urlencode "Code=123456"
```

### Studio (REST Trigger API)

Trigger a Studio Flow execution:

```bash
curl -sS -X POST "https://studio.twilio.com/v2/Flows/FW0123456789abcdef0123456789abcdef/Executions" \
  -u "$TWILIO_API_KEY:$TWILIO_API_SECRET" \
  --data-urlencode "To=+14155550199" \
  --data-urlencode "From=+14155550100" \
  --data-urlencode "Parameters={\"experiment\":\"B\",\"locale\":\"en-US\"}"
```

### Serverless (Twilio Functions) via plugin

Initialize:

```bash
mkdir -p twilio-functions && cd twilio-functions
twilio serverless:init twilio-prod-webhooks --template blank
```

Deploy:

```bash
twilio serverless:deploy --environment production --force
```

Flags:
- `--environment <name>`: environment in Twilio Serverless
- `--force`: skip prompts
- `--service-name <name>`: override service name
- `--functions-folder <path>`
- `--assets-folder <path>`

## Configuration Reference

### Twilio CLI config

Path:
- macOS/Linux: `~/.twilio-cli/config.json`
- Windows (if applicable): `%USERPROFILE%\.twilio-cli\config.json`

Example `~/.twilio-cli/config.json`:

```json
{
  "profiles": {
    "prod": {
      "accountSid": "YOUR_ACCOUNT_SID",
      "apiKeySid": "YOUR_API_KEY_SID",
      "apiKeySecret": "ENV:TWILIO_API_SECRET",
      "region": "us1",
      "edge": "ashburn"
    },
    "staging": {
      "accountSid": "YOUR_ACCOUNT_SID",
      "authToken": "ENV:TWILIO_AUTH_TOKEN_STAGING",
      "region": "us1"
    }
  },
  "activeProfile": "prod"
}
```

Notes:
- Prefer `apiKeySecret` sourced from environment (`ENV:...`) rather than plaintext.
- `region`/`edge` can reduce latency; validate against your Twilio deployment.

### Application environment variables

Recommended file:
- `/etc/twilio/twilio.env` (Linux servers)
- Or Kubernetes Secret + env injection

Example `/etc/twilio/twilio.env`:

```bash
TWILIO_ACCOUNT_SID=YOUR_ACCOUNT_SID
TWILIO_API_KEY=YOUR_API_KEY_SID
TWILIO_API_SECRET=supersecret_api_key_secret
TWILIO_MESSAGING_SERVICE_SID=YOUR_MG_SID
TWILIO_VERIFY_SERVICE_SID=YOUR_VERIFY_SERVICE_SID
TWILIO_WEBHOOK_AUTH_TOKEN=your_auth_token_for_signature_validation
TWILIO_REGION=us1
TWILIO_EDGE=ashburn
SENDGRID_API_KEY=SG.xxxxxx.yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
```

`TWILIO_WEBHOOK_AUTH_TOKEN`:
- Twilio request signature validation uses the **Auth Token** for the account that owns the webhook configuration.
- If you use API Keys for REST calls, you may still need the Auth Token for webhook signature validation. Store it separately and restrict access.

### NGINX reverse proxy (webhook endpoints)

Path:
- `/etc/nginx/conf.d/twilio-webhooks.conf`

Example:

```nginx
server {
  listen 443 ssl http2;
  server_name api.example.com;

  ssl_certificate     /etc/letsencrypt/live/api.example.com/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/api.example.com/privkey.pem;

  location /twilio/ {
    proxy_pass http://127.0.0.1:8080/;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Request-Id $request_id;

    proxy_read_timeout 10s;
    proxy_connect_timeout 2s;
  }
}
```

### Systemd service (Linux)

Path:
- `/etc/systemd/system/twilio-webhooks.service`

Example:

```ini
[Unit]
Description=Twilio Webhook Service
After=network-online.target

[Service]
User=twilio
Group=twilio
EnvironmentFile=/etc/twilio/twilio.env
WorkingDirectory=/opt/twilio-webhooks
ExecStart=/usr/bin/node /opt/twilio-webhooks/server.js
Restart=always
RestartSec=2
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/twilio-webhooks /var/log/twilio-webhooks

[Install]
WantedBy=multi-user.target
```

## Integration Patterns

### Compose with secrets management (Vault / AWS / GCP)

Pattern:
- Store `TWILIO_API_SECRET`, `TWILIO_WEBHOOK_AUTH_TOKEN`, `SENDGRID_API_KEY` in a secret manager.
- Inject into runtime as environment variables.
- Rotate keys quarterly or on incident.

Example: Kubernetes External Secrets (AWS Secrets Manager) snippet:

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: twilio-secrets
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets
    kind: ClusterSecretStore
  target:
    name: twilio-secrets
  data:
    - secretKey: TWILIO_API_SECRET
      remoteRef:
        key: prod/twilio
        property: api_secret
    - secretKey: TWILIO_WEBHOOK_AUTH_TOKEN
      remoteRef:
        key: prod/twilio
        property: auth_token
    - secretKey: SENDGRID_API_KEY
      remoteRef:
        key: prod/sendgrid
        property: api_key
```

### CI/CD pipeline: key rotation + smoke test

Pipeline steps:
1. Create new API key in Twilio (manual approval or automated with Auth Token in a locked job).
2. Update secret store.
3. Deploy.
4. Smoke test: send SMS to test device; verify status callback received.
5. Revoke old key.

Smoke test example (Node):

```bash
node scripts/smoke_sms.js
```

`scripts/smoke_sms.js`:

```javascript
import twilio from "twilio";

const accountSid = process.env.TWILIO_ACCOUNT_SID;
const apiKey = process.env.TWILIO_API_KEY;
const apiSecret = process.env.TWILIO_API_SECRET;
const mg = process.env.TWILIO_MESSAGING_SERVICE_SID;

const client = twilio(apiKey, apiSecret, { accountSid });

const to = "+14155550199";

const msg = await client.messages.create({
  messagingServiceSid: mg,
  to,
  body: `smoke ${new Date().toISOString()}`
});

console.log({ sid: msg.sid, status: msg.status });
```

### Event-driven status processing (webhooks → queue → worker)

Pattern:
- Twilio status callbacks hit `/twilio/sms/status`.
- Endpoint validates signature, normalizes payload, enqueues to Kafka/SQS/PubSub.
- Worker updates message state machine in DB; idempotent by `MessageSid`.

Benefits:
- Avoids webhook timeouts.
- Handles retries safely.
- Centralizes carrier error analytics.

### IVR state machine (Voice webhooks + persisted session)

Pattern:
- Use `<Gather>` with `action` pointing to your app.
- Persist state keyed by `CallSid`.
- Ensure idempotency: Twilio may retry webhook if your endpoint times out.

### Studio + backend orchestration

Pattern:
- Studio handles conversational branching and channel selection.
- Backend triggers Studio Flow with parameters and receives callbacks.
- Use Split widget for A/B tests; store `experiment` parameter in your DB.

## Error Handling & Troubleshooting

### 1) Error 21211 (invalid To number)

Symptom (Twilio API response):

- Code: `21211`
- Message: `The 'To' number +1415555 is not a valid phone number.`

Root causes:
- Not E.164 formatted.
- Missing country code.
- Contains non-digits/spaces not allowed.

Fix:
- Normalize to E.164 (`+14155550199`).
- Validate with libphonenumber before calling Twilio.
- For WhatsApp, ensure `whatsapp:+E164`.

### 2) Error 20003 (authentication)

Symptom:

- Code: `20003`
- Message: `Authenticate`

Or HTTP 401 with:
- `HTTP 401 Unauthorized`

Root causes:
- Wrong API key/secret.
- Using API Key SID with Auth Token instead of API Key Secret.
- Account SID mismatch when using API key auth (must pass `accountSid` in SDK client options).

Fix:
- Verify credentials in secret store.
- For Node SDK: `twilio(apiKey, apiSecret, { accountSid })`.
- Confirm key belongs to the same account/subaccount you’re targeting.

### 3) Error 20429 (rate limit)

Symptom:

- Code: `20429`
- Message: `Too Many Requests`

Or HTTP 429.

Root causes:
- Burst sending beyond account/number/channel limits.
- Verify checks too frequent.
- Studio triggers too frequent.

Fix:
- Implement exponential backoff with jitter.
- Add client-side rate limiting (token bucket) per account and per destination.
- Use Messaging Services with proper throughput configuration (10DLC/short code).
- For Verify: enforce per-user cooldown and max attempts.

### 4) Error 30003 (unreachable / carrier violation)

Symptom:

- Code: `30003`
- Message: `Unreachable destination handset`

Root causes:
- Carrier rejected (inactive number, roaming restrictions, blocked).
- Destination cannot receive SMS.

Fix:
- Treat as terminal for that attempt; do not retry aggressively.
- If critical, fall back to Voice or email.
- Track per-carrier failure rates; consider number validation/HLR (where legal/available).

### 5) Webhook signature validation failures

Symptom in your logs:
- `Error: Twilio Request Validation Failed. Expected signature ...`

Root causes:
- Using wrong Auth Token (wrong account/subaccount).
- URL mismatch (http vs https, missing path, proxy rewriting).
- Not including POST params exactly as received (order/encoding issues).

Fix:
- Ensure you validate against the exact public URL configured in Twilio Console.
- Preserve raw body for validation if your framework mutates params.
- Confirm which account owns the phone number / messaging service; use that Auth Token.

### 6) Messaging status callback not firing

Symptoms:
- Message shows delivered in Console but your system never receives callback.
- Or Twilio Debugger shows webhook errors.

Root causes:
- `StatusCallback` not set on message or messaging service.
- Endpoint returns non-2xx; Twilio retries then gives up.
- TLS/CA issues, DNS issues, firewall blocks.

Fix:
- Set `statusCallback` per message or configure at Messaging Service level.
- Ensure endpoint returns `200` quickly (< 5s) and processes async.
- Check Twilio Debugger and request inspector.

### 7) Voice TwiML fetch errors

Symptom:
- Call fails; Twilio Debugger shows:
  - `11200 HTTP retrieval failure`
  - `11205 HTTP retrieval failure`

Root causes:
- TwiML URL unreachable, slow, or returns non-2xx.
- Invalid TLS chain.
- Redirects not handled as expected.

Fix:
- Ensure TwiML endpoint is publicly reachable and responds within a few seconds.
- Return valid TwiML with correct `Content-Type: text/xml`.
- Avoid long synchronous dependencies; precompute or cache.

### 8) Verify: max attempts / blocked

Common symptoms:
- HTTP 429 or Verify error indicating too many attempts.
- Users report never receiving codes.

Root causes:
- Too many sends/checks per user.
- Fraud guard blocking suspicious patterns.
- Carrier filtering.

Fix:
- Enforce cooldown and attempt limits in your app.
- Use alternative channels (voice/email/TOTP).
- Monitor Verify events and adjust policies; ensure templates and sender reputation.

### 9) SendGrid: 403 Forbidden / invalid API key

Symptom:
- `HTTP Error 403: Forbidden`
- Or response body includes `permission denied, wrong scopes`

Root causes:
- API key missing `Mail Send` permission.
- Using a revoked key.

Fix:
- Create a key with `Mail Send` scope.
- Rotate and update secret store.

### 10) Studio execution fails to start

Symptom:
- HTTP 404/401 when calling executions endpoint.

Root causes:
- Wrong Flow SID (`FW...`) or wrong account.
- Using API key from a different subaccount.

Fix:
- Confirm Flow exists in the same account/subaccount as credentials.
- Use correct base URL and auth.

## Security Hardening

### Credential handling

- Prefer API Keys over Auth Tokens for application auth.
- Store secrets in a secret manager; never commit to git.
- Rotate API keys at least quarterly; immediately on suspected exposure.
- Use separate subaccounts per environment to reduce blast radius.

### Webhook endpoint hardening

- Validate Twilio signatures on all inbound webhooks (Messaging, Voice, Studio, SendGrid inbound parse).
- Enforce HTTPS only; redirect HTTP to HTTPS.
- Implement idempotency:
  - Messaging: key by `MessageSid`
  - Voice: key by `CallSid` + event type
- Return `200` quickly; enqueue work.

### Network controls

- Restrict admin endpoints by IP allowlist/VPN.
- For SIP trunking:
  - Use IP ACLs and strong credentials.
  - Prefer TLS/SRTP where supported.
- For SendGrid inbound parse:
  - Validate source IPs where feasible and/or use signed events (SendGrid Event Webhook supports signature verification).

### OS and runtime hardening (CIS-aligned)

- Linux:
  - Apply CIS Benchmarks for your distro (e.g., CIS Ubuntu Linux 22.04 LTS Benchmark).
  - Run webhook services as non-root.
  - Use systemd hardening options (`NoNewPrivileges=true`, `ProtectSystem=strict`, etc.).
- Node/Python:
  - Pin dependencies; use lockfiles.
  - Enable SAST/DAST in CI.
  - Set request body size limits to prevent abuse.

### Data handling

- Treat phone numbers as sensitive personal data.
- Minimize logging of full E.164 numbers; mask where possible.
- For recordings/transcriptions:
  - Ensure retention policies align with legal requirements.
  - Restrict access to recording URLs; prefer fetching via authenticated API rather than storing public URLs.

## Performance Tuning

### Messaging throughput and latency

- Use **Messaging Services** with:
  - **Geo-matching**: reduces cross-region carrier penalties and improves deliverability.
  - **Sticky sender**: improves conversation continuity and reduces user confusion.
  - **Sender pools**: increases throughput (subject to compliance and campaign limits).

Expected impact (typical):
- Reduced delivery latency variance and fewer carrier filtering events when using appropriate local senders.
- Higher sustainable throughput vs single long code.

### Webhook processing

- Target p95 webhook response time < **200ms**.
- Offload to queue; do not call downstream dependencies synchronously.
- Use connection pooling and keep-alives.

Expected impact:
- Fewer Twilio retries, fewer duplicate events, improved system stability during spikes.

### Rate limit handling

- Implement exponential backoff with jitter for `20429` / HTTP 429.
- Use concurrency limits per account and per destination prefix.
- For bulk sends, batch and schedule.

Expected impact:
- Reduced error rates during campaigns; smoother throughput.

### Voice TwiML endpoints

- Cache static TwiML responses where possible.
- Avoid cold starts (serverless) for latency-sensitive call flows; if using serverless, keep functions warm via scheduled pings.

Expected impact:
- Fewer `11200/11205` retrieval failures; faster call connect.

## Advanced Topics

### STOP/START compliance gotchas

- Do not attempt to “override” STOP by auto-responding with marketing content.
- Maintain your own suppression list even if Twilio blocks sends; you need suppression for multi-provider or future migrations.
- For WhatsApp, opt-in rules differ; ensure you follow WhatsApp template and session rules.

### 10DLC operational realities

- Campaign registration affects throughput and filtering.
- Mismatched message content vs declared use case increases carrier filtering.
- Ensure message templates align with campaign description; audit periodically.

### Multi-region and edge selection

- Twilio supports regions/edges; selecting an edge closer to your infra can reduce REST latency.
- Do not assume region/edge changes are free of compliance implications; validate data residency requirements.

### Recording and transcription costs

- Recording every call can be expensive and increases data handling obligations.
- Consider selective recording (only certain queues, only after consent).
- Transcription adds latency; if you need real-time, consider streaming media (more complex).

### Webhook retries and duplicates

- Twilio retries on non-2xx and timeouts.
- You will receive duplicates even with 2xx in some network failure modes.
- Always implement idempotency and dedupe.

### Subaccount isolation pitfalls

- Phone numbers and messaging services are owned by a specific account/subaccount.
- Webhook signature validation uses the Auth Token of the owning account.
- Mixing resources across subaccounts leads to confusing 401/validation failures.

## Usage Examples

### 1) Production SMS with Messaging Service + status callbacks + dedupe (Node)

`server.js` (Express):

```javascript
import express from "express";
import twilio from "twilio";
import crypto from "crypto";

const app = express();

// Twilio sends application/x-www-form-urlencoded by default
app.use(express.urlencoded({ extended: false }));

const {
  TWILIO_ACCOUNT_SID,
  TWILIO_API_KEY,
  TWILIO_API_SECRET,
  TWILIO_MESSAGING_SERVICE_SID,
  TWILIO_WEBHOOK_AUTH_TOKEN
} = process.env;

const client = twilio(TWILIO_API_KEY, TWILIO_API_SECRET, { accountSid: TWILIO_ACCOUNT_SID });

function validateTwilioSignature(req) {
  const signature = req.header("X-Twilio-Signature");
  const url = `https://${req.get("host")}${req.originalUrl}`;
  const params = req.body;

  const isValid = twilio.validateRequest(TWILIO_WEBHOOK_AUTH_TOKEN, signature, url, params);
  return isValid;
}

// naive in-memory dedupe for example; use Redis/DB in production
const seen = new Set();

app.post("/twilio/sms/status", (req, res) => {
  if (!validateTwilioSignature(req)) return res.status(403).send("invalid signature");

  const messageSid = req.body.MessageSid;
  const messageStatus = req.body.MessageStatus;

  const key = `${messageSid}:${messageStatus}`;
  if (seen.has(key)) return res.status(200).send("duplicate");
  seen.add(key);

  // enqueue to your queue here
  console.log({ messageSid, messageStatus, errorCode: req.body.ErrorCode, errorMessage: req.body.ErrorMessage });

  res.status(200).send("ok");
});

app.post("/send", async (req, res) => {
  const to = req.body.to;
  const body = req.body.body;

  const msg = await client.messages.create({
    messagingServiceSid: TWILIO_MESSAGING_SERVICE_SID,
    to,
    body,
    statusCallback: "https://api.example.com/twilio/sms/status"
  });

  res.json({ sid: msg.sid, status: msg.status });
});

app.listen(8080, () => console.log("listening on :8080"));
```

Run:

```bash
export TWILIO_ACCOUNT_SID="YOUR_ACCOUNT_SID"
export TWILIO_API_KEY="YOUR_API_KEY_SID"
export TWILIO_API_SECRET="supersecret_api_key_secret"
export TWILIO_MESSAGING_SERVICE_SID="YOUR_MG_SID"
export TWILIO_WEBHOOK_AUTH_TOKEN="your_auth_token_for_signature_validation"

node server.js
curl -sS -X POST http://localhost:8080/send -d 'to=+14155550199' -d 'body=hello from prod'
```

### 2) Inbound SMS STOP handling + suppression list (Python)

Key points:
- Twilio may handle STOP automatically, but you still maintain suppression.
- Treat inbound `Body` case-insensitively and trim.

```python
from flask import Flask, request, abort
from twilio.request_validator import RequestValidator
import os

app = Flask(__name__)

validator = RequestValidator(os.environ["TWILIO_WEBHOOK_AUTH_TOKEN"])
suppressed = set()  # replace with DB table keyed by E.164

def valid(req):
    signature = req.headers.get("X-Twilio-Signature", "")
    url = "https://api.example.com" + req.path
    return validator.validate(url, req.form, signature)

@app.post("/twilio/sms/inbound")
def inbound_sms():
    if not valid(request):
        abort(403)

    from_ = request.form.get("From", "")
    body = (request.form.get("Body", "") or "").strip().upper()

    if body in {"STOP", "STOPALL", "UNSUBSCRIBE", "CANCEL", "END", "QUIT"}:
        suppressed.add(from_)
        return ("", 200)

    if body in {"START", "YES", "UNSTOP"}:
        suppressed.discard(from_)
        return ("", 200)

    # normal inbound processing
    return ("", 200)
```

### 3) Voice IVR with Polly voice + state machine (TwiML)

Inbound webhook returns TwiML:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say voice="Polly.Joanna">Welcome. Press 1 for sales. Press 2 for support.</Say>
  <Gather numDigits="1" action="/twilio/voice/menu" method="POST" timeout="5">
    <Say voice="Polly.Joanna">Make your selection now.</Say>
  </Gather>
  <Say voice="Polly.Joanna">No input received. Goodbye.</Say>
  <Hangup/>
</Response>
```

Menu handler returns TwiML based on digit:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Dial>
    <Queue>support</Queue>
  </Dial>
</Response>
```

Production gotchas:
- Always return valid XML quickly.
- Use absolute URLs in `action` if behind proxies that rewrite paths.
- Persist `CallSid` state if multi-step.

### 4) Verify V2 with fallback channels + rate limiting

Pseudo-flow:
1. Attempt SMS verify.
2. If `429` or repeated failures, offer voice call or email.
3. Enforce cooldown: e.g., 60 seconds between sends, max 5 per hour.

Send SMS verify (curl shown earlier). Handle `429`:

```bash
resp="$(curl -sS -w "\n%{http_code}" -X POST \
  "https://verify.twilio.com/v2/Services/$TWILIO_VERIFY_SERVICE_SID/Verifications" \
  -u "$TWILIO_API_KEY:$TWILIO_API_SECRET" \
  --data-urlencode "To=+14155550199" \
  --data-urlencode "Channel=sms")"

body="$(echo "$resp" | head -n1)"
code="$(echo "$resp" | tail -n1)"

if [ "$code" = "429" ]; then
  echo "rate limited; offer voice/email fallback"
  exit 0
fi

echo "$body" | jq .
```

### 5) SendGrid transactional email with dynamic template (Node)

```javascript
import sgMail from "@sendgrid/mail";

sgMail.setApiKey(process.env.SENDGRID_API_KEY);

const msg = {
  to: "oncall@example.com",
  from: "noreply@example.com",
  templateId: "d-13b8f94f2f2c4c0f9a2d8b2d3b7a9c01",
  dynamicTemplateData: {
    incident_id: "INC-2026-021",
    service: "messaging-api",
    severity: "SEV2",
    started_at: "2026-02-21T18:42:00Z"
  }
};

const [resp] = await sgMail.send(msg);
console.log(resp.statusCode);
```

Operational notes:
- Monitor bounces/spam reports; suppress accordingly.
- Warm IPs if moving to dedicated IPs.

### 6) Studio Flow trigger for A/B test

Trigger with parameter `experiment`:

```bash
curl -sS -X POST "https://studio.twilio.com/v2/Flows/FW0123456789abcdef0123456789abcdef/Executions" \
  -u "$TWILIO_API_KEY:$TWILIO_API_SECRET" \
  --data-urlencode "To=+14155550199" \
  --data-urlencode "From=+14155550100" \
  --data-urlencode "Parameters={\"experiment\":\"A\",\"user_id\":\"u_9f2c1\"}"
```

In Studio:
- Use Split widget on `{{flow.data.experiment}}`.
- Log outcomes to your backend via HTTP Request widget.

## Quick Reference

| Task | Command / API | Key flags / fields |
|---|---|---|
| Login CLI | `twilio login` | n/a |
| Fetch account | `twilio api:core:accounts:fetch --sid AC...` | `--sid` |
| Create subaccount | `twilio api:core:accounts:create` | `--friendly-name` |
| Close subaccount | `twilio api:core:accounts:update` | `--sid`, `--status closed` |
| List API keys | `twilio api:core:keys:list` | `--limit` |
| Create API key | `twilio api:core:keys:create` | `--friendly-name`, `--key-type` |
| Revoke API key | `twilio api:core:keys:remove` | `--sid` |
| Send SMS (From) | `twilio api:core:messages:create` | `--from`, `--to`, `--body`, `--status-callback` |
| Send SMS (MG) | `twilio api:core:messages:create` | `--messaging-service-sid`, `--to`, `--body` |
| Fetch message | `twilio api:core:messages:fetch` | `--sid SM...` |
| Configure number webhooks | `twilio api:core:incoming-phone-numbers:update` | `--sms-url`, `--voice-url`, methods |
| Create outbound call | `twilio api:core:calls:create` | `--from`, `--to`, `--url`, callbacks |
| Verify send | `POST /v2/Services/{VA}/Verifications` | `To`, `Channel` |
| Verify check | `POST /v2/Services/{VA}/VerificationCheck` | `To`, `Code` |
| Trigger Studio | `POST /v2/Flows/{FW}/Executions` | `To`, `From`, `Parameters` |

## Graph Relationships

**DEPENDS_ON**
- `http` (webhooks, REST APIs)
- `tls` (HTTPS endpoints, certificate validation)
- `secrets-management` (Vault/KMS/Secrets Manager)
- `dns` (webhook reachability)
- `queueing` (Kafka/SQS/PubSub for webhook processing)

**COMPOSES**
- `kubernetes` (deploy webhook services, manage secrets, autoscaling)
- `terraform` (manage Twilio resources where feasible; otherwise manage config + secrets)
- `observability` (structured logs, tracing, alerting on error codes like 20429/30003)
- `incident-response` (runbooks for auth rotation, webhook failures, carrier incidents)

**SIMILAR_TO**
- `nexmo-vonage` (messaging/voice APIs, webhooks, compliance)
- `plivo` (programmable communications)
- `aws-sns` (messaging primitives; different compliance and feature set)
- `sendgrid` (email delivery; overlaps with Twilio SendGrid component)
