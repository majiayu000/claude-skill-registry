---
name: twilio-lookup
cluster: twilio
description: "Phone intelligence: number validation, carrier lookup, caller ID, line type mobile/landline/VoIP, CNAM"
tags: ["lookup","phone","validation","twilio"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "twilio lookup phone number carrier validation line type cnam ported"
---

# twilio-lookup

## Purpose

`twilio-lookup` enables production-grade phone intelligence workflows using Twilio Lookup: validating phone numbers, normalizing to E.164, retrieving carrier metadata, line type (mobile/landline/VoIP), and caller ID / CNAM (where supported). Engineers use this to:

- Reject invalid or unreachable numbers before sending SMS/WhatsApp/Voice (reduce 21211/30003 failures and cost).
- Route traffic by line type (e.g., avoid SMS to landlines; choose Voice fallback for VoIP-heavy regions).
- Enforce geo/region policy (e.g., block high-risk countries, require US/CA for 10DLC).
- Enrich user profiles with carrier + caller name for fraud scoring and support tooling.
- Build deterministic normalization pipelines (E.164 + country code) across services.

This guide assumes you are integrating Lookup into a larger Twilio production stack (Messaging/Voice/Verify/Studio/SendGrid), with strong error handling, rate limiting, and security controls.

---

## Prerequisites

### Accounts & API credentials

- Twilio Account SID (format `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)
- Twilio Auth Token
- Optional: Twilio API Key + Secret (recommended over Auth Token for production)
  - API Key SID format `SKxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

Create API Key:
- Twilio Console → **Account** → **API keys & tokens** → **Create API key**
- Store secrets in a secret manager (AWS Secrets Manager, GCP Secret Manager, Vault). Do not commit.

### Twilio Lookup API

- Lookup API v2 is the current recommended API surface.
- Some fields (e.g., caller name) may require add-ons or are region-dependent.

### Runtime versions (tested)

- Node.js: **20.11.1** (LTS)
- Python: **3.11.8**
- Java: **17.0.10** (Temurin)
- Go: **1.22.1**
- Twilio helper libraries:
  - twilio-node: **4.23.0**
  - twilio-python: **9.4.1**
- Twilio CLI (optional but useful): **5.19.0**

### OS support

- Ubuntu 22.04 LTS (x86_64)
- Fedora 39 (x86_64)
- macOS 14 Sonoma (Intel + Apple Silicon)

### Network & TLS

- Outbound HTTPS to `lookups.twilio.com` (and `api.twilio.com` for auth/other services).
- TLS inspection proxies must allow SNI and modern ciphers; otherwise expect intermittent `ECONNRESET`/handshake failures.

---

## Core Concepts

### Mental model: “Normalize → Enrich → Decide → Act”

1. **Normalize**: Convert user input to E.164 (e.g., `+14155552671`) and validate plausibility.
2. **Enrich**: Fetch metadata (carrier, line type, caller name).
3. **Decide**: Apply policy (allow/deny, route to SMS vs Voice, require Verify).
4. **Act**: Send message/call/verification; store enrichment for audit and future routing.

### Lookup API entities

- **Phone number**: input can be local/national; output should be E.164.
- **Fields**: optional expansions that increase cost/latency.
  - Common fields:
    - `line_type_intelligence` (line type + carrier)
    - `caller_name` (CNAM-like data where available)
- **Country code**: influences parsing when input is not E.164.

### Architecture overview

Typical production flow:

- Edge/API receives `phone` string.
- Service normalizes and validates using Lookup.
- Result stored in a user profile table with:
  - `e164`, `country_code`, `national_format`
  - `line_type`, `carrier_name`, `mobile_country_code`, `mobile_network_code`
  - `caller_name` (if used)
  - `lookup_timestamp`, `lookup_version`, `risk_flags`
- Downstream:
  - Messaging service chooses Messaging Service SID with geo-matching.
  - Verify uses normalized E.164.
  - Voice uses E.164 and optionally SIP routing.

### Cost and latency tradeoffs

- Basic number validation is cheaper than requesting additional fields.
- `fields=line_type_intelligence` adds extra lookup work; cache results.
- `fields=caller_name` can be slower and less reliable; use only when needed.

### Caching strategy

- Cache by E.164 for a TTL (e.g., 7–30 days) depending on your risk tolerance.
- Carrier and line type can change (porting). For high-risk flows, re-check on critical events (password reset, payout).

---

## Installation & Setup

### Official Python SDK — Lookup

**Repository:** https://github.com/twilio/twilio-python  
**PyPI:** `pip install twilio` · **Supported:** Python 3.7–3.13

```python
from twilio.rest import Client
client = Client()

# Basic lookup
phone = client.lookups.v2.phone_numbers("+15558675309").fetch()
print(phone.country_code, phone.phone_number)

# With add-ons
phone = client.lookups.v2.phone_numbers("+15558675309").fetch(
    fields=["line_type_intelligence", "caller_name", "sim_swap"]
)
print(phone.line_type_intelligence)  # {"type": "mobile", "error_code": null}
print(phone.caller_name)             # {"caller_name": "Alice", "error_code": null}
```

Source: [twilio/twilio-python — lookups](https://github.com/twilio/twilio-python/blob/main/twilio/rest/lookups/)

### 1) Install Twilio CLI (optional but recommended)

#### Ubuntu 22.04 (x86_64)

```bash
curl -sSL https://twilio-cli-prod.s3.amazonaws.com/twilio-cli-linux-x86_64.tar.gz -o /tmp/twilio.tar.gz
sudo tar -xzf /tmp/twilio.tar.gz -C /usr/local/bin twilio
twilio --version
```

#### Fedora 39 (x86_64)

```bash
curl -sSL https://twilio-cli-prod.s3.amazonaws.com/twilio-cli-linux-x86_64.tar.gz -o /tmp/twilio.tar.gz
sudo tar -xzf /tmp/twilio.tar.gz -C /usr/local/bin twilio
twilio --version
```

#### macOS (Intel + Apple Silicon) via Homebrew

```bash
brew update
brew install twilio/brew/twilio
twilio --version
```

### 2) Authenticate Twilio CLI

Preferred: API Key

```bash
twilio login --apikey YOUR_API_KEY_SID --apisecret 'your_api_key_secret' --profile prod
twilio profiles:list
```

Alternative: Account SID + Auth Token

```bash
twilio login --sid YOUR_ACCOUNT_SID --token 'your_auth_token' --profile prod
```

### 3) Install helper libraries

#### Node.js (20.11.1)

```bash
node --version
npm --version

mkdir -p twilio-lookup-demo-node && cd twilio-lookup-demo-node
npm init -y
npm install twilio@4.23.0 pino@9.0.0
```

#### Python (3.11.8)

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip==24.0
pip install twilio==9.4.1 httpx==0.27.0
```

### 4) Environment variables

Set in your shell (dev) or secret manager (prod):

```bash
export TWILIO_ACCOUNT_SID="YOUR_ACCOUNT_SID"
export TWILIO_AUTH_TOKEN="your_auth_token"
# or API key auth:
export TWILIO_API_KEY_SID="YOUR_API_KEY_SID"
export TWILIO_API_KEY_SECRET="your_api_key_secret"
```

### 5) Verify connectivity

```bash
curl -sS https://lookups.twilio.com/ -I | head
```

Expect `HTTP/2 404` or similar (root path not found is fine); the goal is TLS connectivity.

---

## Key Capabilities

### Number validation + E.164 normalization

- Accept user input in various formats.
- Use `countryCode` when input is not E.164.
- Persist normalized E.164 and derived country.

Key output fields:
- `phone_number` (E.164)
- `national_format`
- `country_code`
- `valid` (v1) / v2 semantics vary; treat as “lookup succeeded” + parse results.

### Carrier lookup + line type intelligence

Use `fields=line_type_intelligence` to retrieve:
- `line_type` (e.g., `mobile`, `landline`, `voip`, `nonFixedVoip`, `tollFree`)
- `carrier_name`
- `mobile_country_code` (MCC)
- `mobile_network_code` (MNC)
- `error_code` (carrier-specific issues)

Production uses:
- Route SMS only to `mobile`/`nonFixedVoip` depending on policy.
- Flag `voip` for fraud scoring (common in account takeovers).
- Detect toll-free and apply different messaging rules.

### Caller ID / CNAM (caller_name)

Use `fields=caller_name` (availability varies by country and number type).

Typical use:
- Support tooling (display “likely name”).
- Fraud heuristics (mismatch between claimed name and CNAM).

Do not treat CNAM as authoritative identity.

### Policy enforcement (geo + risk)

Combine Lookup results with:
- Country allow/deny lists
- Known high-risk carriers
- VoIP restrictions for sensitive actions
- 10DLC constraints (US A2P messaging requires registration; Lookup helps ensure US numbers are actually US)

### Pre-send gating for Messaging/Voice/Verify

- Messaging: reduce `21211` invalid To and `30003` unreachable.
- Voice: avoid calling invalid numbers; choose SIP trunk vs PSTN.
- Verify: normalize E.164; block VoIP if required by policy.

---

## Command Reference

### Twilio CLI: Lookup (if installed)

Twilio CLI command names can vary by version/plugins. In CLI 5.19.0, Lookup is typically available via the `api` surface.

#### Fetch a phone number (basic)

```bash
twilio api:lookups:v2:phone-numbers:fetch --phone-number "+14155552671" --profile prod
```

Flags:
- `--phone-number` (string, required): E.164 or raw input.
- `--profile` (string): Twilio CLI profile name.

#### Fetch with fields

```bash
twilio api:lookups:v2:phone-numbers:fetch \
  --phone-number "+14155552671" \
  --fields "line_type_intelligence,caller_name" \
  --profile prod
```

Flags:
- `--fields` (comma-separated): `line_type_intelligence`, `caller_name`

#### Fetch with country code (for non-E.164 input)

```bash
twilio api:lookups:v2:phone-numbers:fetch \
  --phone-number "4155552671" \
  --country-code "US" \
  --fields "line_type_intelligence" \
  --profile prod
```

Flags:
- `--country-code` (ISO-3166-1 alpha-2): e.g., `US`, `CA`, `GB`

If your CLI build does not expose `api:lookups:*`, use direct HTTPS (below) or helper libraries.

---

### Direct HTTPS (curl) — Lookup v2

Twilio Lookup v2 endpoint pattern:

- `GET https://lookups.twilio.com/v2/PhoneNumbers/{PhoneNumber}?Fields=...&CountryCode=...`

#### Basic lookup

```bash
curl -sS -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN" \
  "https://lookups.twilio.com/v2/PhoneNumbers/+14155552671" | jq
```

#### With fields

```bash
curl -sS -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN" \
  "https://lookups.twilio.com/v2/PhoneNumbers/+14155552671?Fields=line_type_intelligence,caller_name" | jq
```

#### With CountryCode for national input

```bash
curl -sS -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN" \
  "https://lookups.twilio.com/v2/PhoneNumbers/4155552671?CountryCode=US&Fields=line_type_intelligence" | jq
```

Notes:
- Use URL encoding for `+` if your tooling mishandles it (`%2B14155552671`).
- Prefer API Key auth in production by using `SK...:secret` basic auth.

---

### Node.js (twilio-node 4.23.0)

#### Basic lookup

```js
import twilio from "twilio";

const client = twilio(process.env.TWILIO_ACCOUNT_SID, process.env.TWILIO_AUTH_TOKEN);

const res = await client.lookups.v2
  .phoneNumbers("+14155552671")
  .fetch();

console.log(res.phoneNumber, res.countryCode, res.nationalFormat);
```

#### With fields

```js
import twilio from "twilio";

const client = twilio(process.env.TWILIO_ACCOUNT_SID, process.env.TWILIO_AUTH_TOKEN);

const res = await client.lookups.v2
  .phoneNumbers("+14155552671")
  .fetch({ fields: "line_type_intelligence,caller_name" });

console.log({
  e164: res.phoneNumber,
  lineType: res.lineTypeIntelligence?.type,
  carrier: res.lineTypeIntelligence?.carrier_name,
  callerName: res.callerName?.caller_name,
});
```

Flags/options:
- `fetch({ fields: "..." })`: comma-separated fields
- `fetch({ countryCode: "US" })`: for national input (if supported by helper version)

#### API Key auth (recommended)

```js
import twilio from "twilio";

const client = twilio(
  process.env.TWILIO_API_KEY_SID,
  process.env.TWILIO_API_KEY_SECRET,
  { accountSid: process.env.TWILIO_ACCOUNT_SID }
);
```

---

### Python (twilio-python 9.4.1)

#### Basic lookup

```python
import os
from twilio.rest import Client

client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])

res = client.lookups.v2.phone_numbers("+14155552671").fetch()
print(res.phone_number, res.country_code, res.national_format)
```

#### With fields

```python
import os
from twilio.rest import Client

client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])

res = client.lookups.v2.phone_numbers("+14155552671").fetch(
    fields="line_type_intelligence,caller_name"
)

print({
    "e164": res.phone_number,
    "line_type": getattr(res, "line_type_intelligence", None),
    "caller_name": getattr(res, "caller_name", None),
})
```

#### API Key auth

```python
import os
from twilio.rest import Client

client = Client(
    os.environ["TWILIO_API_KEY_SID"],
    os.environ["TWILIO_API_KEY_SECRET"],
    os.environ["TWILIO_ACCOUNT_SID"],
)
```

---

## Configuration Reference

### 1) Service configuration file (recommended)

Path (Linux):
- `/etc/openclaw/twilio/lookup.toml`

Path (macOS dev):
- `~/Library/Application Support/OpenClaw/twilio/lookup.toml`

Example:

```toml
# /etc/openclaw/twilio/lookup.toml

[twilio]
account_sid = "YOUR_ACCOUNT_SID"
auth_mode = "api_key" # "api_key" or "auth_token"

[twilio.api_key]
sid = "YOUR_API_KEY_SID"
secret_env = "TWILIO_API_KEY_SECRET" # secret is read from env at runtime

[lookup]
base_url = "https://lookups.twilio.com"
default_country_code = "US"
default_fields = ["line_type_intelligence"]
timeout_ms = 2500
max_retries = 2
retry_backoff_ms = 200
retry_jitter_ms = 100

[cache]
enabled = true
backend = "redis" # "redis" or "memory"
ttl_seconds = 604800 # 7 days
negative_ttl_seconds = 3600 # cache invalid numbers for 1 hour

[policy]
allow_countries = ["US", "CA"]
deny_line_types = ["landline"]
flag_line_types = ["voip", "nonFixedVoip"]
```

### 2) Environment variables

Production runtime should support:

- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN` (if using auth token)
- `TWILIO_API_KEY_SID`
- `TWILIO_API_KEY_SECRET`
- `OPENCLAW_TWILIO_LOOKUP_CONFIG=/etc/openclaw/twilio/lookup.toml`

Example systemd drop-in:

```ini
# /etc/systemd/system/openclaw.service.d/twilio-lookup.conf
[Service]
Environment="OPENCLAW_TWILIO_LOOKUP_CONFIG=/etc/openclaw/twilio/lookup.toml"
Environment="TWILIO_ACCOUNT_SID=YOUR_ACCOUNT_SID"
Environment="TWILIO_API_KEY_SID=YOUR_API_KEY_SID"
Environment="TWILIO_API_KEY_SECRET=/run/secrets/twilio_api_key_secret"
```

If `TWILIO_API_KEY_SECRET` points to a file path, your runtime should read file contents (common pattern). If not supported, store the secret directly in the env var via your secret injector.

### 3) Redis cache configuration (if used)

Path:
- `/etc/openclaw/redis.conf.d/lookup.conf`

```conf
# /etc/openclaw/redis.conf.d/lookup.conf
maxmemory 512mb
maxmemory-policy allkeys-lru
timeout 0
tcp-keepalive 300
```

Key format recommendation:
- `lookup:v2:{e164}:{fields_hash}:{country_code}`

---

## Integration Patterns

### Pattern: Pre-send gating for Messaging (SMS/WhatsApp)

Pipeline:

1. Lookup normalize + line type
2. If invalid → reject request (HTTP 400)
3. If landline → route to Voice or block
4. If mobile/voip → send via Messaging Service (geo-match)
5. Track message status webhooks; handle STOP

Example (pseudo):

```text
POST /send_sms
  -> lookup(+input, fields=line_type_intelligence)
  -> if line_type in deny: 422 "unsupported line type"
  -> send SMS via Messaging Service SID MGxxxxxxxx...
  -> store message SID + lookup snapshot
```

Compose with Twilio Messaging production patterns:
- Use Messaging Service with **geo-matching** to reduce cost and improve deliverability.
- Handle webhook retries and idempotency for status callbacks.
- Enforce opt-out: STOP/START/HELP keywords.

### Pattern: Verify enrollment with VoIP restriction

- Lookup first; if `voip` and your fraud policy disallows VoIP for MFA, require alternate channel (TOTP/email) via Verify custom channels.

### Pattern: Voice fallback for landlines

- If Lookup returns `landline`, skip SMS and place a Voice call using TwiML `<Say>` with Polly voice, or `<Dial>` to connect.

### Pattern: Studio Flow trigger with enrichment

- Use Lookup in your backend, then trigger Studio Flow via REST Trigger API with enriched parameters (`line_type`, `carrier`, `country`).
- Studio can branch on these parameters for IVR/SMS flows.

### Pattern: Data warehouse enrichment job

- Batch job reads new/changed phone numbers, runs Lookup with rate limiting, writes results to warehouse.
- Use caching and backoff to avoid `20429 Too Many Requests`.

---

## Error Handling & Troubleshooting

Handle errors as first-class: classify, retry safely, and surface actionable diagnostics.

### 1) Twilio error 20003 — authentication

**Message (common):**
- `Authenticate`
- Or JSON: `"code": 20003, "message": "Authenticate"`

**Root causes:**
- Wrong Auth Token / API Key secret
- Using API Key SID without `accountSid` in helper client
- Secret rotated but not deployed

**Fix:**
- Verify credentials in secret manager and runtime injection.
- For API Key auth in helper libs, set `accountSid`.
- Confirm you are hitting `lookups.twilio.com` with correct basic auth.

### 2) Twilio error 20429 — rate limiting

**Message:**
- `"code": 20429, "message": "Too Many Requests"`

**Root causes:**
- Burst traffic without client-side throttling
- Batch enrichment job too aggressive

**Fix:**
- Implement token bucket per account (and per region if needed).
- Exponential backoff with jitter; cap retries (e.g., 2–3).
- Cache results; avoid repeated lookups for same E.164.

### 3) Twilio error 21211 — invalid ‘To’ (downstream Messaging/Voice)

**Message:**
- `The 'To' number +1415555 is not a valid phone number.`

**Root causes:**
- Skipping Lookup normalization
- Accepting user input without country context
- Storing non-E.164 and reusing later

**Fix:**
- Always store E.164 from Lookup.
- Require `countryCode` for national inputs.
- Add validation at API boundary; reject ambiguous formats.

### 4) Twilio error 30003 — Unreachable destination handset (Messaging)

**Message:**
- `Unreachable destination handset`

**Root causes:**
- Number is valid but not reachable (inactive, roaming restrictions, blocked)
- Carrier filtering / destination restrictions

**Fix:**
- Use Lookup line type + carrier to detect problematic segments.
- Implement fallback channels (WhatsApp, Voice, email).
- Track delivery failures and suppress repeated sends.

### 5) HTTP 400 from Lookup — malformed request

**Message (typical):**
- `400 Bad Request`

**Root causes:**
- Invalid `Fields` value (typo)
- Bad URL encoding of `+` in phone number
- Unsupported `CountryCode` format (must be `US`, not `USA`)

**Fix:**
- Validate `fields` against allowlist: `line_type_intelligence`, `caller_name`.
- URL-encode phone numbers in raw HTTP clients.
- Enforce ISO alpha-2 country codes.

### 6) HTTP 404 from Lookup — number not found / invalid

**Message (common JSON):**
- `"status": 404, "message": "The requested resource /PhoneNumbers/... was not found"`

**Root causes:**
- Number is not parseable/valid for the given country context
- Missing `CountryCode` for national format input

**Fix:**
- Retry once with explicit `CountryCode` if you have user locale.
- Otherwise reject and request E.164.

### 7) Network errors: timeouts / TLS

**Messages:**
- Node: `ETIMEDOUT`, `ECONNRESET`
- Python httpx: `ReadTimeout`, `ConnectError`

**Root causes:**
- Egress firewall/proxy issues
- Too-low timeout under load
- DNS instability

**Fix:**
- Set timeout ~2–3s for Lookup; do not block critical paths indefinitely.
- Use retries only for network errors (not 4xx).
- Ensure DNS resolvers are stable; consider caching DNS at OS level.

### 8) JSON parsing / schema drift

**Message:**
- `TypeError: Cannot read properties of undefined (reading 'type')`
- Or Python: `AttributeError: 'PhoneNumberInstance' object has no attribute ...`

**Root causes:**
- Assuming fields exist when not requested
- Region does not support caller_name
- Helper library version mismatch

**Fix:**
- Treat optional expansions as nullable.
- Gate access: `res.lineTypeIntelligence?.type`.
- Pin helper library versions; add contract tests.

### 9) Twilio error 21614 / 21610 (opt-out) — downstream Messaging

**Message:**
- `21610: Message cannot be sent because the recipient has opted out of receiving messages from this number.`
- `21614: 'To' number is not a valid mobile number`

**Root causes:**
- Not honoring STOP lists
- Sending SMS to landline

**Fix:**
- Maintain opt-out suppression lists; handle inbound STOP/START.
- Use Lookup line type gating before sending.

---

## Security Hardening

### Credential handling

- Prefer API Key + Secret over Auth Token.
- Rotate API keys quarterly (or per policy).
- Store secrets in a secret manager; inject at runtime.
- Ensure logs never include:
  - Auth Token / API key secret
  - Full phone numbers in plaintext (mask or hash)

Masking recommendation:
- Log last 2–4 digits only: `+1415555****`
- Or store SHA-256 of E.164 for correlation.

### Least privilege and blast radius

- Use separate Twilio subaccounts for environments (dev/stage/prod).
- Use separate API keys per service (lookup-enricher vs messaging-sender).
- If using Twilio Console roles, restrict who can create/rotate keys.

### Transport security

- Enforce TLS 1.2+.
- If using corporate proxies, pin allowed domains:
  - `lookups.twilio.com`
  - `api.twilio.com`

### CIS-aligned host hardening (where applicable)

- CIS Ubuntu Linux 22.04 LTS Benchmark (v1.0.0) relevant controls:
  - Ensure secrets are not world-readable (`chmod 600` for config files with SIDs).
  - Restrict outbound traffic to required destinations (egress allowlist).
  - Centralize audit logs; protect log integrity.

### Webhook security (composed systems)

Lookup itself is outbound-only, but it composes with Messaging/Voice webhooks:
- Validate Twilio signatures (`X-Twilio-Signature`) on status callbacks.
- Implement idempotency keys for webhook processing.
- Apply retry-safe handlers (Twilio retries on non-2xx).

---

## Performance Tuning

### 1) Cache Lookup results (largest win)

Expected impact:
- 60–95% reduction in Lookup calls in steady state (depending on churn).
- Lower p95 latency for user-facing endpoints (cache hit ~1–5ms vs network 150–600ms).

Guidelines:
- TTL 7 days for general routing.
- TTL 1 day for high-risk flows if porting risk matters.
- Negative cache invalid numbers for 1 hour to reduce repeated abuse.

### 2) Request only required fields

Expected impact:
- Lower cost and latency.
- Avoid `caller_name` unless needed.

Example:
- Signup: `line_type_intelligence` only.
- Support agent view: `caller_name` on-demand.

### 3) Concurrency control + backpressure

- Implement a per-process semaphore (e.g., max 50 concurrent lookups).
- Add a global rate limiter (Redis-based) for batch jobs.

Expected impact:
- Fewer `20429` responses.
- More predictable latency under load.

### 4) Timeouts and retries

Recommended:
- Timeout: 2.5s
- Retries: 2 (network/5xx/20429 only)
- Backoff: 200ms, 400ms + jitter

Expected impact:
- Reduced tail latency amplification.
- Avoid retry storms.

---

## Advanced Topics

### Porting and carrier drift

- Carrier name and line type can change due to number porting.
- For critical actions (payouts, password resets), re-check Lookup if cached data is older than a threshold (e.g., 24h).

### Handling ambiguous national numbers

- If user enters `07700 900123`, you need country context (GB).
- Use:
  - User-selected country
  - GeoIP-derived country (with caution)
  - Account profile country
- If you guess wrong, you may normalize incorrectly; prefer explicit country selection in UX.

### VoIP nuance

- Some providers classify as `nonFixedVoip` vs `voip`.
- Decide policy explicitly:
  - Allow `nonFixedVoip` for low-risk notifications
  - Block for MFA if your threat model requires it

### Toll-free and short codes

- Lookup is for phone numbers; short codes are not standard E.164.
- For messaging, treat short codes separately; do not send them to Lookup.

### Internationalization and formatting

- Store E.164 as canonical.
- Store `national_format` for display only; do not use it for sending.

### Data retention

- Phone intelligence can be considered personal data.
- Apply retention policies:
  - Keep only what you need (line type, country) and for as long as needed.
  - Consider hashing E.164 for analytics.

---

## Usage Examples

### 1) API endpoint: validate + normalize + store

Node.js example with strict policy and caching stub:

```js
import twilio from "twilio";
import pino from "pino";

const log = pino();
const client = twilio(process.env.TWILIO_ACCOUNT_SID, process.env.TWILIO_AUTH_TOKEN);

const ALLOW_COUNTRIES = new Set(["US", "CA"]);
const DENY_LINE_TYPES = new Set(["landline"]);

export async function normalizePhone({ input, countryCode }) {
  const res = await client.lookups.v2
    .phoneNumbers(input)
    .fetch({ fields: "line_type_intelligence", countryCode });

  const e164 = res.phoneNumber;
  const cc = res.countryCode;
  const lineType = res.lineTypeIntelligence?.type ?? "unknown";

  if (!ALLOW_COUNTRIES.has(cc)) {
    throw Object.assign(new Error(`country_not_allowed: ${cc}`), { status: 422 });
  }
  if (DENY_LINE_TYPES.has(lineType)) {
    throw Object.assign(new Error(`line_type_not_supported: ${lineType}`), { status: 422 });
  }

  log.info({ e164, cc, lineType }, "phone_normalized");
  return { e164, countryCode: cc, lineType };
}
```

### 2) Pre-send gating for SMS with fallback to Voice

Decision logic:
- mobile/nonFixedVoip → SMS
- landline → Voice call
- voip → require Verify or alternate channel (policy)

Pseudo-implementation:

```python
from twilio.rest import Client
import os

client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])

def route_notification(phone: str):
    lookup = client.lookups.v2.phone_numbers(phone).fetch(fields="line_type_intelligence")
    e164 = lookup.phone_number
    lt = lookup.line_type_intelligence.get("type") if lookup.line_type_intelligence else "unknown"

    if lt in ("mobile", "nonFixedVoip"):
        msg = client.messages.create(
            to=e164,
            from_="+15005550006",
            body="Your package is arriving today."
        )
        return {"channel": "sms", "sid": msg.sid}

    if lt == "landline":
        call = client.calls.create(
            to=e164,
            from_="+15005550006",
            twiml="<Response><Say voice='Polly.Joanna'>Your package is arriving today.</Say></Response>"
        )
        return {"channel": "voice", "sid": call.sid}

    raise ValueError(f"unsupported_line_type: {lt}")
```

### 3) Batch enrichment job with rate limiting and caching

Shell + curl + jq example (simple; production should use a proper worker):

```bash
set -euo pipefail

INPUT_CSV="phones.csv" # one phone per line
FIELDS="line_type_intelligence"
COUNTRY="US"

while read -r phone; do
  # naive throttle: 5 req/s
  sleep 0.2

  curl -sS -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN" \
    "https://lookups.twilio.com/v2/PhoneNumbers/${phone}?CountryCode=${COUNTRY}&Fields=${FIELDS}" \
    | jq -c '{phone_number, country_code, line_type_intelligence}'
done < "$INPUT_CSV"
```

### 4) Studio Flow trigger with enriched params

Backend does Lookup, then triggers Studio:

```bash
curl -sS -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN" \
  -X POST "https://studio.twilio.com/v2/Flows/FW0123456789abcdef0123456789abcdef/Executions" \
  --data-urlencode "To=+14155552671" \
  --data-urlencode "From=+15005550006" \
  --data-urlencode "Parameters={\"line_type\":\"mobile\",\"carrier\":\"T-Mobile USA, Inc.\"}"
```

Studio can branch on `line_type` to choose SMS vs Voice.

### 5) Verify enrollment: block VoIP for MFA

Flow:
- Lookup with `line_type_intelligence`
- If `voip`/`nonFixedVoip` → require TOTP or email
- Else send Verify SMS

Python sketch:

```python
import os
from twilio.rest import Client

client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])

def start_mfa(phone: str):
    lookup = client.lookups.v2.phone_numbers(phone).fetch(fields="line_type_intelligence")
    e164 = lookup.phone_number
    lt = lookup.line_type_intelligence.get("type") if lookup.line_type_intelligence else "unknown"

    if lt in ("voip", "nonFixedVoip"):
        return {"action": "require_totp", "reason": f"line_type={lt}"}

    verification = client.verify.v2.services("YOUR_VERIFY_SERVICE_SID") \
        .verifications.create(to=e164, channel="sms")

    return {"action": "verify_sms", "sid": verification.sid, "status": verification.status}
```

### 6) Support tool: on-demand caller name lookup

Only fetch `caller_name` when an agent opens a profile:

```bash
curl -sS -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN" \
  "https://lookups.twilio.com/v2/PhoneNumbers/+14155552671?Fields=caller_name" | jq '.caller_name'
```

---

## Quick Reference

| Task | Command / API | Key flags / params |
|---|---|---|
| Basic lookup | `GET /v2/PhoneNumbers/{num}` | none |
| Lookup with line type + carrier | `GET ...?Fields=line_type_intelligence` | `Fields` |
| Lookup with caller name | `GET ...?Fields=caller_name` | `Fields` |
| National input parsing | `.../{num}?CountryCode=US` | `CountryCode` |
| CLI fetch | `twilio api:lookups:v2:phone-numbers:fetch` | `--phone-number`, `--fields`, `--country-code`, `--profile` |
| Node fetch | `client.lookups.v2.phoneNumbers(num).fetch()` | `{ fields, countryCode }` |
| Python fetch | `client.lookups.v2.phone_numbers(num).fetch()` | `fields=...` |

---

## Graph Relationships

### DEPENDS_ON

- `twilio-core-auth` (Account SID/Auth Token or API Key auth patterns)
- `twilio-cli` (optional; for debugging and ops workflows)
- `secrets-management` (Vault/AWS/GCP secret injection)
- `redis` (optional; caching and rate limiting)

### COMPOSES

- `twilio-messaging` (pre-send gating, geo-matching Messaging Services, STOP handling, status webhooks)
- `twilio-voice` (fallback routing, TwiML generation, call recording/transcription)
- `twilio-verify` (E.164 normalization, VoIP restrictions, fraud guard)
- `twilio-studio` (Flow branching based on lookup enrichment)
- `sendgrid-email` (fallback channel when phone is invalid/unreachable)

### SIMILAR_TO

- `libphonenumber` (local parsing/formatting; not authoritative for reachability/carrier)
- `numverify` / other phone intelligence providers (feature overlap; different coverage/cost)
- `HLR lookup` services (carrier/reachability in some regions; different semantics and legality constraints)
