---
name: whatsapp
description: "Send WhatsApp messages and manage contacts via the WhatsApp Business Cloud API."
metadata: {"thinkfleetbot":{"emoji":"💬","requires":{"bins":["curl","jq"],"env":["WHATSAPP_ACCESS_TOKEN","WHATSAPP_PHONE_ID"]}}}
---

# WhatsApp Business

Send messages and manage contacts via the WhatsApp Business Cloud API.

## Environment Variables

- `WHATSAPP_ACCESS_TOKEN` - Access token
- `WHATSAPP_PHONE_ID` - Phone number ID

## Send text message

```bash
curl -s -X POST -H "Authorization: Bearer $WHATSAPP_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.facebook.com/v19.0/$WHATSAPP_PHONE_ID/messages" \
  -d '{"messaging_product":"whatsapp","to":"15551234567","type":"text","text":{"body":"Hello from ThinkFleetBot!"}}' | jq '{messages}'
```

## Send template message

```bash
curl -s -X POST -H "Authorization: Bearer $WHATSAPP_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.facebook.com/v19.0/$WHATSAPP_PHONE_ID/messages" \
  -d '{"messaging_product":"whatsapp","to":"15551234567","type":"template","template":{"name":"hello_world","language":{"code":"en_US"}}}' | jq '{messages}'
```

## Notes

- Phone numbers without + prefix.
- Always confirm before sending messages.
