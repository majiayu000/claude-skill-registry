---
name: twilio-admin
cluster: twilio
description: "Admin: sub-account lifecycle, usage monitoring, number management, compliance SHAKEN/STIR TCR, audit logs"
tags: ["admin","billing","compliance","twilio"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "twilio admin sub-account usage billing compliance numbers tcr shaken"
---

# twilio-admin

## Purpose

Enable reliable, auditable administration of Twilio accounts in production:

- Create, configure, suspend, and close subaccounts safely (with guardrails and rollback).
- Monitor usage/costs across parent + subaccounts; detect anomalies; enforce budgets.
- Manage phone numbers at scale (buy/release/port/assign to Messaging Services/Voice apps).
- Maintain compliance posture: SHAKEN/STIR, A2P 10DLC, Toll-Free verification, TrustHub bundles, audit logs.
- Provide repeatable operational workflows (CLI + API) suitable for CI/CD and on-call runbooks.

This skill is for engineers who need deterministic, scriptable control over Twilio admin surfaces without breaking production traffic.

---

## Prerequisites

### Twilio account + permissions

- A Twilio **parent account** with permission to:
  - Create/manage subaccounts
  - View usage records
  - Manage phone numbers
  - Access TrustHub / A2P / Toll-Free verification (as applicable)
- You must have:
  - `ACCOUNT_SID` (starts with `AC...`)
  - `AUTH_TOKEN`
- For subaccount operations, you need each subaccount SID (`AC...`) and (optionally) its auth token if using per-subaccount credentials.

### Supported tooling versions (pinned)

- **twilio-cli**: `5.6.0`
- **Node.js** (for twilio-cli runtime): `20.11.1` (LTS)
- **Python** (for admin scripts): `3.11.8`
- **twilio-python**: `9.4.1`
- **jq**: `1.7`
- **curl**: `8.5.0`
- **OpenSSL**: `3.0.13` (for TLS inspection / cert tooling)
- **Docker** (optional for hermetic runs): `25.0.3`

### OS support

- Ubuntu `22.04` / `24.04`
- Fedora `39` / `40`
- macOS `14` (Sonoma) on Intel + Apple Silicon

### Auth setup (recommended patterns)

1. **Local dev**: Twilio CLI profile + environment variables.
2. **CI**: short-lived secrets from a vault (AWS Secrets Manager / GCP Secret Manager / Vault) injected as env vars.
3. **Production automation**: separate Twilio API keys (where applicable) and strict scoping; avoid using the primary Auth Token in CI.

> Note: Twilio’s classic model uses Account SID + Auth Token. Some products support API Keys; for admin operations, you often still need Account SID + Auth Token. Treat Auth Token as a root secret.

---

## Core Concepts

### Parent account vs subaccounts

- **Parent account**: billing owner; can create/manage subaccounts; consolidated reporting.
- **Subaccount**: isolated resources (numbers, messaging services, apps) and usage; can be suspended/closed independently.

Operational model:
- Use subaccounts to isolate environments (prod/stage), tenants, or business units.
- Centralize billing and compliance at the parent where possible.

### Account lifecycle states

Twilio accounts have a `status` field:
- `active`: normal operation
- `suspended`: traffic blocked; resources retained
- `closed`: account closed; resources may be released; irreversible in practice

### Usage records vs billing

- **Usage Records API**: near-real-time usage events (minutes, messages, etc.) with categories.
- **Invoices**: monthly billing artifacts; not always suitable for alerting.
- For anomaly detection, prefer Usage Records with daily/hourly granularity.

### Phone number inventory

Twilio numbers are resources with:
- E.164 phone number
- capabilities: `sms`, `mms`, `voice`, `fax`
- configuration: Voice URL, Messaging webhook, status callback, emergency address (US), etc.

At scale:
- Use **Messaging Services** with **number pools** and **geo-matching** for cost/throughput optimization.
- Avoid binding application logic directly to a single number.

### Compliance surfaces (high-level)

- **A2P 10DLC (US)**: Brand + Campaign registration; required for many US A2P SMS use cases.
- **Toll-Free verification (US/CA)**: required for higher deliverability and throughput.
- **SHAKEN/STIR (Voice)**: caller ID attestation; impacts call completion and labeling.
- **TrustHub**: customer profiles, end-user profiles, supporting documents, bundles.

### Webhooks and auditability

- Messaging/Voice status callbacks are critical for delivery and debugging.
- Twilio Console provides audit events; programmatic access varies by product. Where APIs are limited, capture your own audit trail (who/what/when) in your automation.

---

## Installation & Setup

### Official Python SDK — Admin / Account Management

**Repository:** https://github.com/twilio/twilio-python  
**PyPI:** `pip install twilio` · **Supported:** Python 3.7–3.13

```python
from twilio.rest import Client
client = Client()

# List subaccounts
for acct in client.api.v2010.accounts.list():
    print(acct.sid, acct.friendly_name, acct.status)

# Create subaccount
sub = client.api.v2010.accounts.create(friendly_name="Staging Account")
sub_client = Client(client.username, client.password, sub.sid)

# Rotate auth token (master account key management)
keys = client.api.v2010.accounts(client.account_sid).keys.list()
for k in keys:
    print(k.sid, k.friendly_name, k.date_created)
```

Source: [twilio/twilio-python — accounts](https://github.com/twilio/twilio-python/blob/main/twilio/rest/api/v2010/account/__init__.py)

### Ubuntu 22.04/24.04

```bash
sudo apt-get update
sudo apt-get install -y curl jq python3.11 python3.11-venv python3-pip ca-certificates gnupg
```

Install Node.js 20.11.1 (NodeSource):

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
node --version   # expect v20.x
npm --version
```

Install Twilio CLI 5.6.0:

```bash
sudo npm install -g twilio-cli@5.6.0
twilio --version
```

Optional: install Twilio CLI plugins commonly used in admin workflows:

```bash
twilio plugins:install @twilio-labs/plugin-serverless@3.0.0
twilio plugins:install @twilio-labs/plugin-flex@6.0.4
twilio plugins:install @twilio-labs/plugin-verify@0.8.0
```

Python environment:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip==24.0
pip install twilio==9.4.1 requests==2.31.0 python-dateutil==2.9.0.post0
```

### Fedora 39/40

```bash
sudo dnf install -y curl jq python3.11 python3.11-pip python3.11-virtualenv ca-certificates
sudo dnf install -y nodejs npm
node --version
```

Install Twilio CLI:

```bash
sudo npm install -g twilio-cli@5.6.0
twilio --version
```

Python venv:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip==24.0
pip install twilio==9.4.1 requests==2.31.0 python-dateutil==2.9.0.post0
```

### macOS 14 (Intel + Apple Silicon)

Install Homebrew (if needed), then:

```bash
brew update
brew install jq python@3.11 node@20
```

Ensure Node 20 is active:

```bash
brew link --overwrite node@20
node --version
```

Install Twilio CLI:

```bash
npm install -g twilio-cli@5.6.0
twilio --version
```

Python venv:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip==24.0
pip install twilio==9.4.1 requests==2.31.0 python-dateutil==2.9.0.post0
```

### Twilio CLI authentication

Twilio CLI stores profiles under:

- macOS/Linux: `~/.twilio-cli/config.json`

Login interactively (writes profile):

```bash
twilio login
```

Non-interactive (CI) via env vars:

```bash
export TWILIO_ACCOUNT_SID="ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
export TWILIO_AUTH_TOKEN="your_auth_token"
```

Verify:

```bash
twilio api:core:accounts:fetch --sid "$TWILIO_ACCOUNT_SID"
```

---

## Key Capabilities

### Subaccount lifecycle management

Operations:
- Create subaccount with deterministic naming and metadata.
- Rotate credentials (where supported) and distribute secrets.
- Suspend subaccount during incident response.
- Close subaccount after resource cleanup.

Key production guardrails:
- Never close a subaccount until:
  - all phone numbers are released/ported
  - messaging services are drained
  - webhooks are disabled or pointed to a safe sink
  - Verify services and SendGrid integrations are detached (if used)

### Usage monitoring and anomaly detection

- Pull daily usage by category (SMS, MMS, Voice minutes, Verify, etc.).
- Aggregate across subaccounts.
- Compare against baseline (7-day moving average) and alert on deviations.
- Enforce budgets by suspending subaccounts or disabling messaging services.

### Phone number management at scale

- Search and buy numbers with required capabilities.
- Assign numbers to Messaging Services (pooling).
- Configure Voice URLs / Messaging webhooks.
- Release numbers safely (ensure no active dependencies).
- Track number inventory and ownership (tags via your CMDB; Twilio doesn’t provide arbitrary tags on numbers).

### Compliance: A2P 10DLC, Toll-Free, SHAKEN/STIR, TrustHub

- Validate that US A2P traffic is routed through registered campaigns.
- Ensure toll-free numbers are verified before production use.
- Confirm caller ID attestation posture (SHAKEN/STIR) and avoid spoofing patterns.
- Maintain TrustHub bundles and supporting documents for regulated regions.

### Audit logs and change tracking

- Twilio Console has audit events; API coverage varies.
- For production, implement **automation-level audit logs**:
  - record every admin action (who/what/when/why)
  - store request/response metadata (redact secrets)
  - correlate with incident tickets

---

## Command Reference

> Notes:
> - Twilio CLI command groups vary by installed plugins and CLI version.
> - When CLI coverage is incomplete, use direct REST API calls with `curl` or `twilio-python`.

### Twilio CLI global flags

Common flags (apply to most commands):

- `-o, --output [json|tsv|csv|human]`: output format
- `--properties <props>`: select fields (comma-separated)
- `--no-header`: suppress header (tsv/csv)
- `--limit <n>`: limit list results
- `--page-size <n>`: page size for list
- `--page-token <token>`: pagination token
- `--profile <name>`: use a named profile from `~/.twilio-cli/config.json`
- `--log-level [debug|info|warn|error]`: CLI logging verbosity

Examples:

```bash
twilio api:core:accounts:list -o json --limit 50
twilio api:core:incoming-phone-numbers:list --properties sid,phoneNumber,friendlyName -o tsv --no-header
```

### Accounts (parent + subaccounts)

List accounts:

```bash
twilio api:core:accounts:list --limit 200 -o json
```

Fetch account:

```bash
twilio api:core:accounts:fetch --sid ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX -o json
```

Create subaccount:

```bash
twilio api:core:accounts:create \
  --friendly-name "prod-tenant-acme" \
  -o json
```

Update account status (suspend/reactivate):

```bash
twilio api:core:accounts:update --sid ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX --status suspended -o json
twilio api:core:accounts:update --sid ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX --status active -o json
```

Close account:

```bash
twilio api:core:accounts:update --sid ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX --status closed -o json
```

> Production rule: closing is effectively irreversible. Prefer `suspended` first, then close after cleanup.

### Usage Records

List usage records (daily):

```bash
twilio api:core:usage:records:list \
  --category sms \
  --start-date 2026-02-01 \
  --end-date 2026-02-20 \
  --granularity daily \
  -o json
```

Flags (Usage Records list):
- `--category <string>`: e.g. `sms`, `mms`, `calls`, `phonenumbers`, `verify`, etc.
- `--start-date YYYY-MM-DD`
- `--end-date YYYY-MM-DD`
- `--granularity [daily|hourly|all]`

> Category names are Twilio-defined; enumerate by inspecting existing usage or Twilio docs for your account.

### Incoming Phone Numbers

List numbers:

```bash
twilio api:core:incoming-phone-numbers:list --limit 200 -o json
```

Fetch number by SID:

```bash
twilio api:core:incoming-phone-numbers:fetch --sid PNXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX -o json
```

Update number configuration:

```bash
twilio api:core:incoming-phone-numbers:update \
  --sid PNXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \
  --friendly-name "prod-sms-us-east-01" \
  --sms-url "https://api.example.com/twilio/sms/inbound" \
  --sms-method POST \
  --status-callback "https://api.example.com/twilio/sms/status" \
  --status-callback-method POST \
  --voice-url "https://api.example.com/twilio/voice/inbound" \
  --voice-method POST \
  -o json
```

Release number:

```bash
twilio api:core:incoming-phone-numbers:remove --sid PNXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### Available Phone Numbers (search + buy)

Search US local numbers with SMS+Voice:

```bash
twilio api:core:available-phone-numbers:local:list \
  --iso-country US \
  --in-region CA \
  --sms-enabled true \
  --voice-enabled true \
  --limit 20 \
  -o json
```

Buy a number:

```bash
twilio api:core:incoming-phone-numbers:create \
  --phone-number "+14155552671" \
  --friendly-name "prod-acme-us-ca-01" \
  -o json
```

### Messaging Services (pooling, geo-match, sticky sender)

List messaging services (requires messaging API group; CLI coverage may vary):

If CLI supports it:

```bash
twilio api:messaging:v1:services:list -o json --limit 200
```

Create service:

```bash
twilio api:messaging:v1:services:create \
  --friendly-name "prod-us-messaging" \
  --use-inbound-webhook-on-number true \
  --sticky-sender true \
  --smart-encoding true \
  -o json
```

Add a phone number to a service (phone number SID):

```bash
twilio api:messaging:v1:services:phone-numbers:create \
  --service-sid MGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \
  --phone-number-sid PNXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \
  -o json
```

Enable geo-match (where supported by service settings; may require API fields not exposed in CLI):
Use REST API via curl if needed.

### TrustHub / A2P / Toll-Free (API-first)

CLI support is inconsistent; use REST API with `curl` or `twilio-python`.

Base auth header:

```bash
export TWILIO_ACCOUNT_SID="ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
export TWILIO_AUTH_TOKEN="your_auth_token"
basic_auth="$(printf '%s:%s' "$TWILIO_ACCOUNT_SID" "$TWILIO_AUTH_TOKEN" | base64)"
```

Example: list TrustHub customer profiles (endpoint may vary by region/product availability):

```bash
curl -sS "https://trusthub.twilio.com/v1/CustomerProfiles" \
  -H "Authorization: Basic $basic_auth" | jq .
```

> If you receive 404, your account may not have TrustHub enabled or the endpoint differs for your product set. Confirm in Console and Twilio docs for your account.

### Audit events (Console vs API)

Twilio’s audit event API availability varies. If your account supports it, you may have endpoints under `https://accounts.twilio.com/v1/...` or similar. In many production setups, you should treat Twilio Console audit logs as a human-accessible source and implement your own automation audit logs.

---

## Configuration Reference

### Twilio CLI config

Path:
- `~/.twilio-cli/config.json`

Example (multiple profiles):

```json
{
  "profiles": {
    "prod-parent": {
      "accountSid": "YOUR_ACCOUNT_SID",
      "authToken": "prod_parent_auth_token",
      "region": "us1",
      "edge": "ashburn"
    },
    "stage-parent": {
      "accountSid": "YOUR_ACCOUNT_SID",
      "authToken": "stage_parent_auth_token",
      "region": "us1"
    }
  },
  "activeProfile": "prod-parent"
}
```

Operational guidance:
- Do not commit this file.
- On shared machines, enforce filesystem permissions:

```bash
chmod 600 ~/.twilio-cli/config.json
```

### OpenClaw skill config (recommended)

Path (repo-local):
- `./.openclaw/skills/twilio-admin.toml`

Example:

```toml
[twilio]
parent_account_sid = "YOUR_ACCOUNT_SID"
region = "us1"
edge = "ashburn"

[policy]
require_ticket_id = true
allowed_close_environments = ["dev", "sandbox"]
suspend_before_close = true
suspend_grace_period_hours = 24

[usage_alerts]
currency = "USD"
daily_spend_soft_limit = 250.00
daily_spend_hard_limit = 500.00
anomaly_multiplier = 2.5
lookback_days = 7

[number_management]
default_sms_url = "https://api.example.com/twilio/sms/inbound"
default_status_callback = "https://api.example.com/twilio/sms/status"
default_voice_url = "https://api.example.com/twilio/voice/inbound"
```

### Environment variables (CI-safe contract)

Path (CI system):
- GitHub Actions secrets / GitLab CI variables / Vault injection

Required:

```bash
export TWILIO_ACCOUNT_SID="YOUR_ACCOUNT_SID"
export TWILIO_AUTH_TOKEN="prod_parent_auth_token"
```

Optional (recommended for audit trail):

```bash
export CHANGE_TICKET_ID="INC-20481"
export CHANGE_ACTOR="oncall@company.com"
export CHANGE_REASON="Suspend tenant due to suspected SMS fraud"
```

---

## Integration Patterns

### Compose with incident response automation

Pattern:
1. Detect anomaly (usage spike, carrier failures, Verify fraud).
2. Automatically suspend subaccount or disable messaging service.
3. Page on-call with context and rollback steps.

Example pipeline (pseudo CI job):

```bash
python scripts/twilio_usage_anomaly.py --since 2026-02-20 --threshold-multiplier 3.0
python scripts/twilio_suspend_subaccount.py --subaccount AC333... --ticket INC-20481 --reason "SMS spike"
python scripts/post_to_pagerduty.py --incident-key twilio-ac333 --summary "Suspended Twilio subaccount AC333..."
```

### Compose with Terraform (infrastructure as code)

Twilio Terraform provider coverage is partial and changes over time. Use Terraform for stable resources (where supported) and use this skill for:
- emergency actions (suspend/close)
- number inventory operations
- compliance workflows that aren’t well-modeled in Terraform

Pattern:
- Terraform manages baseline apps/webhooks/messaging services.
- Admin scripts manage numbers and account lifecycle.

### Compose with data warehouse (cost + deliverability analytics)

Export usage records daily into BigQuery/Snowflake:
- `usage_records` table keyed by `account_sid`, `category`, `date`, `price`, `usage`.

Then join with:
- message status callbacks (delivered/failed)
- carrier error codes (e.g., `30003`)
- opt-out events (STOP)

### Compose with Twilio Messaging/Voice/Verify/SendGrid operational skills

- twilio-admin provides account/number/compliance primitives.
- Messaging skill handles:
  - status webhooks, STOP handling, 10DLC routing, toll-free verification checks
- Voice skill handles:
  - TwiML apps, SIP trunking, call recording/transcription, SHAKEN/STIR posture validation
- Verify skill handles:
  - Verify V2 services, rate limiting, Fraud Guard
- SendGrid skill handles:
  - templates, IP warming, bounce/spam suppression

---

## Error Handling & Troubleshooting

Include both CLI and API-level errors. For each: symptom, root cause, fix.

1) **Authentication failure**

Error:

```
Twilio could not authenticate the request. Please check your credentials. (20003)
```

Root causes:
- Wrong `TWILIO_AUTH_TOKEN`
- Using subaccount token with parent SID (or vice versa)
- Rotated token not updated in CI

Fix:
- Verify env vars and active CLI profile:
  ```bash
  twilio profiles:list
  twilio api:core:accounts:fetch --sid "$TWILIO_ACCOUNT_SID"
  ```
- Rotate secrets in vault and redeploy CI.

2) **Invalid phone number format**

Error:

```
The 'To' number +1415555 is not a valid phone number. (21211)
```

Root causes:
- Not E.164
- Missing country code
- Non-dialable test data in production

Fix:
- Normalize to E.164 in application layer.
- Add validation before sending; reject non-E.164.

3) **Rate limiting**

Error:

```
Rate limit exceeded (20429)
```

Root causes:
- Bulk admin operations without backoff
- Parallel scripts across many subaccounts

Fix:
- Implement exponential backoff with jitter.
- Reduce concurrency; batch operations.
- For CLI loops, add sleeps:
  ```bash
  for sid in $(cat subaccounts.txt); do
    twilio api:core:accounts:fetch --sid "$sid" -o json
    sleep 0.3
  done
  ```

4) **Carrier delivery failure**

Error (messaging status callback / logs):

```
Message Delivery - Error Code 30003: Unreachable destination handset
```

Root causes:
- Subscriber unreachable/offline
- Carrier filtering
- Invalid/ported number edge cases

Fix:
- Treat as non-retryable after limited attempts.
- Track per-carrier failure rates; consider alternate routes (Messaging Service, verified sender types).
- Ensure compliance (10DLC/toll-free verification) to reduce filtering.

5) **Permission / resource not found due to wrong account context**

Error:

```
The requested resource /IncomingPhoneNumbers/PNXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX was not found (20404)
```

Root causes:
- Number belongs to a different subaccount than the credentials used
- Using parent credentials but querying subaccount-scoped resource incorrectly (or vice versa)

Fix:
- Determine owning account by listing numbers in each subaccount (or maintain inventory mapping).
- Use correct credentials/profile for that account.

6) **Attempting to close account with active resources**

Symptom:
- Account closes but numbers remain billed until released, or closure fails in internal workflows.

Root causes:
- Closing doesn’t automatically release all resources immediately.
- Numbers may remain in “owned” state until explicitly released.

Fix:
- Pre-close checklist:
  - list and remove incoming phone numbers
  - detach messaging services
  - disable webhooks
- Automate cleanup before closure.

7) **Webhook retry storms due to non-2xx responses**

Symptom:
- Repeated webhook deliveries; increased load; duplicated events.

Root causes:
- Your webhook endpoint returns 500/timeout.
- Slow downstream dependencies.

Fix:
- Ensure webhook endpoints return 2xx quickly; enqueue work async.
- Idempotency keys: use `MessageSid` / `CallSid`.
- Add circuit breakers and shed load.

8) **TLS / certificate issues on webhook endpoints**

Symptom (Twilio debugger / logs):
- Webhook errors indicating TLS handshake failure.

Root causes:
- Expired certificate
- Incomplete chain
- Unsupported cipher suite

Fix:
- Validate with:
  ```bash
  openssl s_client -connect api.example.com:443 -servername api.example.com -showcerts
  ```
- Renew cert; ensure full chain; prefer modern TLS configs.

9) **Messaging compliance enforcement (10DLC / toll-free)**

Symptom:
- Sudden throughput reduction, increased filtering, or messages failing with policy-related errors.

Root causes:
- Unregistered A2P campaign for US traffic
- Toll-free not verified
- Mismatch between use case and content

Fix:
- Confirm registration status in Console/TrustHub.
- Route US A2P via registered campaign numbers/services.
- Update templates and opt-in flows.

10) **Voice caller ID attestation issues (SHAKEN/STIR)**

Symptom:
- Calls labeled “Spam Likely” or reduced answer rates.

Root causes:
- Using unverified caller ID
- Mismatched origination identity
- Low attestation due to configuration

Fix:
- Use Twilio numbers you own as caller ID.
- Avoid spoofing; ensure consistent origination.
- Review SHAKEN/STIR guidance and your call flows.

---

## Security Hardening

### Secrets management

- Store `TWILIO_AUTH_TOKEN` only in a secrets manager.
- Never log auth tokens; redact in structured logs.
- Rotate Auth Token on incident or staff departure.

Local filesystem:
- `~/.twilio-cli/config.json` must be `0600`.
- On macOS, prefer Keychain-backed secret storage for automation where possible.

### Network controls

- Webhook endpoints:
  - enforce HTTPS only
  - validate Twilio signatures (X-Twilio-Signature) for inbound webhooks
  - rate-limit and WAF protect endpoints
- If you terminate TLS at a load balancer, ensure end-to-end integrity and correct host headers.

### Change control

- Require `CHANGE_TICKET_ID` for destructive actions (suspend/close/release numbers).
- Implement two-person review for:
  - closing accounts
  - releasing high-value numbers
  - changing messaging/voice webhooks in production

### CIS benchmarks (where applicable)

- CIS Ubuntu Linux Benchmark v2.0.1:
  - ensure least privilege on config files (`chmod 600`)
  - audit logging enabled for admin scripts execution
- CIS Docker Benchmark v1.5.0 (if running admin tooling in containers):
  - do not bake secrets into images
  - run as non-root
  - read-only filesystem where feasible

### API request integrity

- Use idempotency patterns in your own automation:
  - before creating resources, check if they exist
  - store mapping (subaccount name → SID) in a durable store
- For webhooks, verify signatures and enforce strict parsing.

---

## Performance Tuning

### Reduce API calls with bulk listing + local joins

Before:
- For each subaccount, list numbers, usage, services separately (N×M calls).

After:
- Cache account list once; parallelize with bounded concurrency; reuse HTTP sessions.

Expected impact:
- 3–10× faster for fleets of 100+ subaccounts.
- Lower chance of `20429 Rate limit exceeded`.

Python pattern (requests session + bounded concurrency):

```python
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from twilio.rest import Client

client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])

def fetch_usage(acct_sid: str):
    sub = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"], account_sid=acct_sid)
    recs = sub.usage.records.list(category="sms", granularity="daily", limit=30)
    return acct_sid, sum(float(r.price or 0) for r in recs)

accounts = client.api.accounts.list(limit=200)

with ThreadPoolExecutor(max_workers=8) as ex:
    futs = [ex.submit(fetch_usage, a.sid) for a in accounts]
    for f in as_completed(futs):
        sid, total = f.result()
        print(sid, total)
        time.sleep(0.05)
```

### Use Messaging Services with geo-matching and pooling

- Consolidate numbers into a Messaging Service.
- Enable geo-matching to reduce cross-region carrier penalties.
- Use sticky sender to improve deliverability for conversational flows.

Expected impact:
- Lower per-message costs in some regions.
- Higher throughput and better deliverability vs single-number sending.

### Webhook handling: fast ACK + async processing

- Return HTTP 204/200 within <200ms.
- Enqueue to Kafka/SQS/PubSub; process asynchronously.

Expected impact:
- Prevent webhook retries and duplicate processing.
- Stabilize under traffic spikes.

---

## Advanced Topics

### Safe subaccount closure playbook (production)

1. Suspend subaccount (`status=suspended`).
2. Snapshot inventory:
   - numbers
   - messaging services + phone number pools
   - voice apps / webhook URLs
3. Drain traffic:
   - disable sending in your app
   - ensure no scheduled jobs target the subaccount
4. Release numbers (or port out).
5. Confirm usage drops to near-zero for 24h.
6. Close subaccount.

### Number release dependencies

Before releasing a number:
- Remove from Messaging Service pool.
- Ensure it’s not configured as caller ID in Voice apps.
- Ensure it’s not referenced in Verify (if used as a custom channel sender).
- Ensure no compliance bundle requires it (region-specific).

### Multi-region Twilio edges

Twilio supports regions/edges; CLI profile can set `region` and `edge`.
- Use consistent region/edge for latency-sensitive operations.
- For admin operations, region mismatch usually isn’t fatal, but can complicate debugging.

### Handling STOP/opt-out at admin level

- STOP handling is primarily application-level and Messaging Service configuration.
- Admin responsibility:
  - ensure inbound webhooks are configured and reachable
  - ensure opt-out keywords are not overridden incorrectly
  - ensure compliance logs are retained

### SHAKEN/STIR gotchas

- Using a Twilio number you own as caller ID is necessary but not always sufficient for high attestation.
- Avoid dynamically setting caller ID to numbers you don’t control.
- Monitor answer rates and spam labeling; correlate with carrier analytics where available.

### SendGrid cross-product considerations

If your org uses SendGrid:
- Keep Twilio subaccounts and SendGrid subusers aligned by tenant/environment.
- Ensure bounce/spam handling doesn’t break transactional mail.
- Maintain separate IP pools for marketing vs transactional; warm IPs gradually.

---

## Usage Examples

### 1) Create a subaccount, attach baseline webhooks, and record in inventory

Create subaccount:

```bash
twilio api:core:accounts:create --friendly-name "prod-tenant-acme" -o json | jq -r '.sid'
```

Store mapping (example local file):
- `./inventory/twilio_subaccounts.json`

```bash
mkdir -p inventory
twilio api:core:accounts:list -o json --limit 200 > inventory/twilio_subaccounts.json
```

Buy a number and configure webhooks:

```bash
twilio api:core:incoming-phone-numbers:create \
  --phone-number "+14155552671" \
  --friendly-name "prod-acme-primary" \
  --sms-url "https://api.example.com/twilio/sms/inbound" \
  --sms-method POST \
  --status-callback "https://api.example.com/twilio/sms/status" \
  --status-callback-method POST \
  --voice-url "https://api.example.com/twilio/voice/inbound" \
  --voice-method POST \
  -o json
```

### 2) Suspend a subaccount during suspected fraud (with ticket enforcement)

Suspend:

```bash
export CHANGE_TICKET_ID="INC-20481"
export CHANGE_REASON="Suspected SMS pumping; usage spike 4x baseline"
twilio api:core:accounts:update --sid YOUR_ACCOUNT_SID --status suspended -o json
```

Verify status:

```bash
twilio api:core:accounts:fetch --sid YOUR_ACCOUNT_SID -o json | jq -r '.status'
```

### 3) Daily usage rollup across subaccounts (JSON → CSV)

List subaccounts:

```bash
twilio api:core:accounts:list -o json --limit 200 > /tmp/accounts.json
```

Extract SIDs:

```bash
jq -r '.[].sid' /tmp/accounts.json > /tmp/account_sids.txt
```

Loop usage (daily SMS) and emit CSV:

```bash
echo "account_sid,total_price_usd" > /tmp/sms_usage.csv
while read -r sid; do
  total="$(twilio api:core:usage:records:list --category sms --start-date 2026-02-20 --end-date 2026-02-20 --granularity daily -o json \
    | jq '[.[].price | tonumber] | add // 0')"
  echo "$sid,$total" >> /tmp/sms_usage.csv
  sleep 0.2
done < /tmp/account_sids.txt
```

### 4) Migrate numbers into a Messaging Service pool

Create service:

```bash
twilio api:messaging:v1:services:create \
  --friendly-name "prod-us-messaging" \
  --sticky-sender true \
  --smart-encoding true \
  -o json | jq -r '.sid'
```

Add numbers:

```bash
export MG_SID="YOUR_MG_SID"
for pn in PNaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa PNbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb; do
  twilio api:messaging:v1:services:phone-numbers:create \
    --service-sid "$MG_SID" \
    --phone-number-sid "$pn" \
    -o json
done
```

### 5) Release unused numbers safely (pre-check + remove)

List numbers with friendly name filter (client-side):

```bash
twilio api:core:incoming-phone-numbers:list -o json --limit 200 \
  | jq -r '.[] | select(.friendlyName | test("deprecated")) | .sid + " " + .phoneNumber'
```

Remove:

```bash
twilio api:core:incoming-phone-numbers:remove --sid PNXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### 6) Validate webhook endpoints quickly (TLS + HTTP)

TLS check:

```bash
openssl s_client -connect api.example.com:443 -servername api.example.com </dev/null 2>/dev/null | openssl x509 -noout -dates -issuer -subject
```

HTTP health:

```bash
curl -sS -o /dev/null -w "%{http_code}\n" https://api.example.com/twilio/sms/status/health
```

---

## Quick Reference

| Task | Command | Key flags |
|---|---|---|
| List subaccounts | `twilio api:core:accounts:list` | `--limit`, `-o json` |
| Create subaccount | `twilio api:core:accounts:create` | `--friendly-name` |
| Suspend/reactivate | `twilio api:core:accounts:update` | `--sid`, `--status suspended|active` |
| Close account | `twilio api:core:accounts:update` | `--status closed` |
| Daily usage | `twilio api:core:usage:records:list` | `--category`, `--start-date`, `--end-date`, `--granularity` |
| List numbers | `twilio api:core:incoming-phone-numbers:list` | `--limit`, `--properties` |
| Buy number | `twilio api:core:incoming-phone-numbers:create` | `--phone-number`, `--friendly-name` |
| Update number webhooks | `twilio api:core:incoming-phone-numbers:update` | `--sms-url`, `--status-callback`, `--voice-url` |
| Release number | `twilio api:core:incoming-phone-numbers:remove` | `--sid` |
| Search available numbers | `twilio api:core:available-phone-numbers:local:list` | `--iso-country`, `--in-region`, `--sms-enabled`, `--voice-enabled` |

---

## Graph Relationships

### DEPENDS_ON

- `twilio-cli@5.6.0`
- `node@20.11.1`
- `python@3.11.8`
- `twilio-python@9.4.1`
- `jq@1.7`
- Secure secret storage (Vault/ASM/GSM)

### COMPOSES

- `twilio-messaging` (status callbacks, STOP handling, 10DLC, toll-free verification)
- `twilio-voice` (TwiML apps, SIP trunking, recordings/transcriptions, IVR state machines)
- `twilio-verify` (Verify V2, Fraud Guard, rate limiting)
- `sendgrid-admin` (templates, inbound parse, IP warming, bounce/spam handling)
- `studio-admin` (Flow export/import, REST Trigger API, A/B testing)

### SIMILAR_TO

- `aws-organizations-admin` (account lifecycle + guardrails)
- `gcp-resource-manager-admin`
- `stripe-admin` (billing/usage monitoring patterns)
- `okta-admin` (audit/change control patterns)
