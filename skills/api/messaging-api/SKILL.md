---
name: messaging-api
description: Comprehensive reference for LINE Messaging API — webhook setup, message sending, Flex Message design, Rich Menu management, audience targeting, insights, coupons, and channel access tokens. This skill should be used when the user asks to "build a LINE Bot", "set up a webhook", "send a push message", "design a Flex Message", "create a Rich Menu", "manage audience targeting", "get messaging insights", "create a coupon campaign", "debug webhook signature verification", or mentions LINE Messaging API, LINE OA chatbot, reply/push/multicast/narrowcast/broadcast, Flex Message JSON, Rich Menu, group chat bot, channel access token, or URL schemes. Always use this skill whenever the user mentions LINE bots, chatbots, LINE OA, or any messaging-related LINE integration, even if they don't explicitly say "Messaging API".
---

# LINE Messaging API

**Do not answer LINE API questions from memory — LINE updates APIs frequently and training data is unreliable. Always consult the references below.**

Reference for building, reviewing, and debugging LINE Bots and LINE Messaging API integrations.

## Workflow

### Build
1. Read [references/api-common.md](references/api-common.md) (rate limits, forward compatibility, error handling)
2. Load the relevant reference for the feature being implemented
3. For architecture or design choices, consult [references/experts.md](references/experts.md) for directional guidance
4. Write code following specs and constraints from references

### Review / Debug
1. Read [references/api-common.md](references/api-common.md) (rate limits, error codes)
2. Load relevant references for the code being reviewed
3. Cross-check code against specs (size limits, token expiry, counting rules, required fields)
4. For design pattern concerns, consult [references/experts.md](references/experts.md)
5. Report violations with reference to specific constraints

## Environment Variables

```
LINE_CHANNEL_ACCESS_TOKEN=Bot access token
LINE_CHANNEL_SECRET=Channel secret (webhook signature verification)
```

## Common Specifications

**Read [references/api-common.md](references/api-common.md) before writing any LINE bot code.** Contains rules that affect all API interactions: forward compatibility (don't use strict schemas — LINE adds fields without notice), rate limits, error handling, retry policy, and logging recommendations.

## Webhook

- Verification: `x-line-signature` header (HMAC-SHA256, base64, key = Channel Secret)
- Body: `{"destination": "U...", "events": [...]}`
- Bot server must return `200`

### Signature Verification (pseudocode)

```
channel_secret = ENV['LINE_CHANNEL_SECRET']
signature = request.headers['x-line-signature']
body = request.body   # raw bytes, do NOT parse/reformat before verification

digest = HMAC_SHA256(key = channel_secret, message = body)
expected = Base64.encode(digest)

if signature != expected:
    return 403  # reject — not from LINE

events = JSON.parse(body)['events']
for event in events:
    handle(event)
return 200
```

- Never deserialize or re-format the body before verification
- Use UTF-8 encoding exclusively
- Official SDKs handle this automatically — use them when possible

Full event types, properties, and webhook settings → **[references/webhook-events.md](references/webhook-events.md)**

## Message Sending

All require `Authorization: Bearer {channel access token}`:

| Mode | Endpoint | Purpose |
|------|----------|---------|
| Reply | `POST /v2/bot/message/reply` | Reply to user (requires one-time replyToken) |
| Push | `POST /v2/bot/message/push` | Send to a specific user/group at any time |
| Multicast | `POST /v2/bot/message/multicast` | Send to multiple users (max 500) |
| Broadcast | `POST /v2/bot/message/broadcast` | Send to all friends |

- Max 5 messages per request
- Domain: `api.line.me` (general) / `api-data.line.me` (content upload)

Message objects → **[references/message-objects.md](references/message-objects.md)**
Full sending API (Narrowcast, statistics, validation, etc.) → **[references/message-sending.md](references/message-sending.md)**

## Flex Message

Three-layer structure:

```
Container (Bubble / Carousel)
  └── Block (Header / Hero / Body / Footer)
       └── Component (Box / Button / Image / Video / Icon / Text / Span / Separator)
```

Minimal Flex Message:
```json
{
  "type": "flex", "altText": "Notification",
  "contents": {
    "type": "bubble",
    "body": {
      "type": "box", "layout": "vertical",
      "contents": [{"type": "text", "text": "Hello Flex!", "weight": "bold"}]
    }
  }
}
```

Full component specs, layout, video → **[references/flex-message.md](references/flex-message.md)**
Official Flex Message Simulator examples → `assets/examples/`

## Reference Index

| File | Topic |
|------|-------|
| [references/api-common.md](references/api-common.md) | **Read first.** Rate limits, error handling, forward compatibility |
| [references/webhook-events.md](references/webhook-events.md) | Webhook event types and JSON structure |
| [references/message-objects.md](references/message-objects.md) | Message objects, Quick Reply, sender customization |
| [references/action-objects.md](references/action-objects.md) | Action objects (postback, URI, datetimepicker, etc.) |
| [references/message-sending.md](references/message-sending.md) | Reply/Push/Multicast/Narrowcast/Broadcast, statistics |
| [references/flex-message.md](references/flex-message.md) | Flex Message components, layout, styles |
| [references/rich-menu.md](references/rich-menu.md) | Rich Menu CRUD, tab switching, display priority |
| [references/user.md](references/user.md) | User profile, follower IDs, account link |
| [references/group-chat.md](references/group-chat.md) | Group/Room messaging and member APIs |
| [references/audience.md](references/audience.md) | Audience management (create/add/get/delete) |
| [references/insights.md](references/insights.md) | Delivery, follower, and interaction insights |
| [references/channel-token.md](references/channel-token.md) | Channel access token lifecycle |
| [references/coupon.md](references/coupon.md) | Coupon CRUD, reward types, sending |
| [references/url-schemes.md](references/url-schemes.md) | LINE URL schemes for deep linking |
| [references/experts.md](references/experts.md) | Expert domain routing and 17 specialist profiles |
| assets/examples/ | Flex Message JSON examples (11 showcases) |

## SDK

Official SDKs: [Python](https://github.com/line/line-bot-sdk-python) | [Node.js](https://github.com/line/line-bot-sdk-nodejs) | [Go](https://github.com/line/line-bot-sdk-go) | [Java](https://github.com/line/line-bot-sdk-java) | [PHP](https://github.com/line/line-bot-sdk-php) | [Ruby](https://github.com/line/line-bot-sdk-ruby)

Other languages: use [LINE OpenAPI specs](https://developers.line.biz/en/docs/messaging-api/line-bot-sdk/) with OpenAPI Generator.
