---
name: line-notification-message
description: Reference for LINE Notification Messages — phone-number-based messaging to non-friends, template type (premade layouts) and flexible type (custom Flex Message), delivery completion webhooks, user consent flow, SMS authentication, and billing. Use when the user asks to "send a notification message via phone number", "hash a phone number for PNP", "handle delivery completion webhook", "set up template or flexible notification", "check notification message count", "integrate LON", or mentions LINE notification messages, LINE Official Notification (LON), PNP push, phone-number-based delivery, hashed phone number, notification template, delivery completion event, consent states, or SMS authentication for notifications. Always use this skill whenever the user mentions LINE notification messages, PNP, LON, LINE Official Notification, LINE 通知型訊息, or phone-based LINE messaging to non-friends, even if they don't explicitly say "notification message".
---

# LINE Notification Messages

**Do not answer LINE Notification Messages questions from memory — LINE updates APIs frequently and training data is unreliable. Always consult the references below.**

LINE Notification Messages allow sending messages to users by specifying their phone number (SHA256-hashed E.164 format), even if they haven't added the LINE Official Account as a friend. Corporate-only service available in **Japan, Thailand, and Taiwan**. Not for advertising or commercial purposes.

## Workflow

### Build
1. Read [references/api-common.md](references/api-common.md) (rate limits, forward compatibility, error handling)
2. Load the relevant reference for the feature being implemented
3. For architecture or design choices, consult [references/experts.md](references/experts.md) for directional guidance
4. Write code following specs and constraints from references

### Review / Debug
1. Read [references/api-common.md](references/api-common.md) (rate limits, error codes)
2. Load relevant references for the code being reviewed
3. Cross-check code against specs (phone hashing format, sending conditions, consent states, billing rules, IP restriction warnings)
4. For design pattern concerns, consult [references/experts.md](references/experts.md)
5. Report violations with reference to specific constraints

## Environment Variables

```
LINE_CHANNEL_ACCESS_TOKEN=Bot access token (Messaging API channel)
LINE_CHANNEL_SECRET=Channel secret (webhook signature verification)
```

## Common Specifications

**Read [references/api-common.md](references/api-common.md) before writing any notification message code.** Contains rules that affect all API interactions: forward compatibility (don't use strict schemas — LINE adds fields without notice), rate limits, error handling, and logging recommendations.

## Two Message Types

| Type | Description | UX Review | Send Endpoint |
|------|-------------|-----------|---------------|
| **Template** | Predefined layout with templateKey, itemKey, buttonKey. Easy to set up. | Not required | `POST /v2/bot/message/pnp/templated/push` |
| **Flexible** | Free-form message objects (Flex Message, text, etc.). Greater design freedom. | **Required** | `POST /bot/pnp/push` |

- Template type added June 2025 — simpler, no UX review needed
- Flexible type (formerly just "LINE notification messages") — allows custom message objects but requires prior UX review
- Both types: no images, video, or audio allowed

Full type comparison → **[references/sending-api.md](references/sending-api.md)**

## Minimal Flow (pseudocode)

```
# 1. Hash phone number (E.164 → SHA256)
phone = "+818000001234"                    # E.164 format, no hyphens
hashed = SHA256(phone.encode()).hexdigest() # 64-char lowercase hex

# 2a. Send via template type
POST https://api.line.me/v2/bot/message/pnp/templated/push
Authorization: Bearer {channel_access_token}
X-Line-Delivery-Tag: {optional_tracking_tag}
{
  "to": hashed,
  "templateKey": "shipment_completed_ja",
  "body": {
    "emphasizedItem": {"itemKey": "date_002_ja", "content": "August 10"},
    "items": [{"itemKey": "number_001_ja", "content": "1234567"}],
    "buttons": [{"buttonKey": "contact_ja", "url": "https://example.com"}]
  }
}
# → Response: 202 Accepted

# 2b. OR send via flexible type
POST https://api.line.me/bot/pnp/push
Authorization: Bearer {channel_access_token}
{
  "to": hashed,
  "messages": [{"type": "text", "text": "Your order has shipped"}]
}
# → Response: 200 OK

# 3. IMPORTANT: 200/202 does NOT guarantee delivery
#    User may be blocked, consent not given, SMS auth expired, etc.

# 4. Delivery confirmation arrives via webhook
#    event.type = "delivery", delivery.data = hashed phone or delivery tag
```

## API Endpoint Summary

| Operation | Endpoint | Response |
|-----------|----------|----------|
| Send (Template) | `POST /v2/bot/message/pnp/templated/push` | 202 |
| Send (Flexible) | `POST /bot/pnp/push` | 200 |
| Count (Template) | `GET /v2/bot/message/delivery/pnp/templated?date=yyyyMMdd` | 200 |
| Count (Flexible) | `GET /v2/bot/message/delivery/pnp?date=yyyyMMdd` | 200 |

- Domain: `api.line.me`
- Rate limit: 2,000 req/sec for all endpoints
- `X-Line-Retry-Key` is **NOT supported** — do not use retry keys
- Do **NOT** restrict server IP in channel Security Settings — may cause sending failure

Full API specs, parameters, error codes → **[references/sending-api.md](references/sending-api.md)**

## Key Concepts

### Phone Number Hashing
1. Normalize to **E.164** format (country code, no hyphens): `+818000001234`
2. Hash with **SHA256**: `hashlib.sha256("+818000001234".encode()).hexdigest()`
3. Result: 64-char lowercase hex string

### Sending Conditions (ALL must be met)
1. Phone number matches user's LINE account
2. Phone number is valid (SMS authenticated)
3. User agrees to receive LINE notification messages
4. User has **not** blocked the LINE Official Account
5. Phone number issued in Japan, Thailand, or Taiwan
6. User has agreed to LINE's Privacy Policy (revised March 2022)

### User Consent States
| State | Behavior |
|-------|----------|
| **Agree (on)** | Message delivered normally |
| **Reject (off)** | Message deleted, not delivered |
| **Not set** | User receives consent prompt; 24 hours to agree or message is deleted |

- Consent is **comprehensive** — once agreed, applies to ALL LINE Official Accounts

### SMS Authentication
- Required once every **180 days**
- Not required within 180 days of account creation or phone number change

### Delivery Confirmation
- API response `200`/`202` does **NOT** guarantee delivery
- Use **delivery completion webhook** (`type: "delivery"`) to confirm actual delivery
- No webhook within 24 hours = message was not delivered

Full technical specs → **[references/technical-specs.md](references/technical-specs.md)**
Template system details → **[references/template-system.md](references/template-system.md)**
Webhook details → **[references/delivery-webhook.md](references/delivery-webhook.md)**

## Reference Index

| File | Topic |
|------|-------|
| [references/api-common.md](references/api-common.md) | **Read first.** Rate limits, status codes, error handling, forward compatibility |
| [references/sending-api.md](references/sending-api.md) | Send APIs (template + flexible), count APIs, request/response specs, error codes |
| [references/template-system.md](references/template-system.md) | Template structure: templateKey, itemKey, buttonKey, field limits, country suffixes |
| [references/technical-specs.md](references/technical-specs.md) | Phone hashing, sending conditions, consent flow, SMS auth, billing, IP restrictions |
| [references/delivery-webhook.md](references/delivery-webhook.md) | Delivery completion event, X-Line-Delivery-Tag, user consent flows, non-friend behavior |
| [references/experts.md](references/experts.md) | LINE Notification Messages domain experts for architecture guidance |

## SDK

Official SDKs: [Python](https://github.com/line/line-bot-sdk-python) | [Node.js](https://github.com/line/line-bot-sdk-nodejs) | [Go](https://github.com/line/line-bot-sdk-go) | [Java](https://github.com/line/line-bot-sdk-java) | [PHP](https://github.com/line/line-bot-sdk-php) | [Ruby](https://github.com/line/line-bot-sdk-ruby)

Other languages: use [LINE OpenAPI specs](https://developers.line.biz/en/docs/messaging-api/line-bot-sdk/) with OpenAPI Generator.
