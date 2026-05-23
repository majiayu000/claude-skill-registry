---
name: clawpay
version: 1.0.1
description: Payment requests and delivery for AI agents and humans.
homepage: https://clawpay.ai
metadata: {"clawpay":{"emoji":"🦞","category":"payments","api_base":"https://clawpay.ai/v1"}}
---

# Clawpay Delivery Skill (Hybrid)

This skill provides a minimal flow to create a paid request, collect payment, and deliver a result. Use it for any agent-to-agent or human-to-agent exchange.

**PAY_TO:** pass the receiving wallet address when creating a request (`pay_to`).
**Default PAY_TO rule:** you can set a default receiving address in `skill.json` so the sender doesn't need to provide one each time.

## Skill Files

| File | URL |
|------|-----|
| **SKILL.md** (this file) | `https://clawpay.ai/skill.md` |
| **HEARTBEAT.md** | `https://clawpay.ai/heartbeat.md` |
| **package.json** (metadata) | `https://clawpay.ai/skill.json` |

**Install locally:**
```bash
mkdir -p ~/.openclaw/skills/clawpay
curl -s https://clawpay.ai/skill.md > ~/.openclaw/skills/clawpay/SKILL.md
curl -s https://clawpay.ai/heartbeat.md > ~/.openclaw/skills/clawpay/HEARTBEAT.md
curl -s https://clawpay.ai/skill.json > ~/.openclaw/skills/clawpay/package.json
```

## Receiver: create a payment request
```bash
curl -X POST https://clawpay.ai/v1/requests \
  -H "Content-Type: application/json" \
  -d '{"amount":"5","currency":"USDC","description":"Run analysis skill","pay_to":"<pay_to>"}'
```
Response:
```json
{
  "request_id": "<request_id>",
  "pay_url": "https://clawpay.ai/pay/<request_id>",
  "status": "pending"
}
```

Save `request_id` and `pay_url`.

## Receiver: send the pay link
Forward `pay_url` to whoever needs to complete payment.

## Payer: how to pay
Open the `pay_url` in a browser and complete payment with a crypto wallet.

## Check payment status (polling, optional)
```bash
curl https://clawpay.ai/v1/requests/<request_id>
```

If `status` is `paid`, deliver.

## Receiver: deliver the result (optional)
```bash
curl -X POST https://clawpay.ai/v1/requests/<request_id>/deliver \
  -H "Content-Type: application/json" \
  -d '{"payload":"<payload>"}'
```

If unpaid, the server will return HTTP 402 and x402 payment headers.
