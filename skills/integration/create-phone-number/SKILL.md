---
name: create-phone-number
description: Set up and manage phone numbers in Vapi for inbound and outbound voice AI calls. Use when importing Twilio, Vonage, or Telnyx numbers, buying Vapi numbers, or configuring phone numbers for assistants.
license: MIT
compatibility: Requires internet access and a Vapi API key (VAPI_API_KEY).
metadata:
  author: vapi
  version: "1.0"
---

# Vapi Phone Number Setup

Import phone numbers from Twilio, Vonage, or Telnyx, or use Vapi's built-in numbers to connect voice assistants to real phone calls.

> **Setup:** Ensure `VAPI_API_KEY` is set. See the `setup-api-key` skill if needed.

## Quick Start — Buy a Vapi Number

Vapi provides free phone numbers for testing with daily call limits.

```bash
curl -X POST https://api.vapi.ai/phone-number \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "vapi",
    "assistantId": "your-assistant-id",
    "name": "Main Support Line"
  }'
```

## Import from Twilio

```bash
curl -X POST https://api.vapi.ai/phone-number \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "twilio",
    "number": "+11234567890",
    "twilioAccountSid": "your-twilio-account-sid",
    "twilioAuthToken": "your-twilio-auth-token",
    "assistantId": "your-assistant-id",
    "name": "Twilio Support Line"
  }'
```

## Import from Vonage

```bash
curl -X POST https://api.vapi.ai/phone-number \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "vonage",
    "number": "+11234567890",
    "credentialId": "your-vonage-credential-id",
    "assistantId": "your-assistant-id",
    "name": "Vonage Support Line"
  }'
```

## Import from Telnyx

```bash
curl -X POST https://api.vapi.ai/phone-number \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "telnyx",
    "number": "+11234567890",
    "credentialId": "your-telnyx-credential-id",
    "assistantId": "your-assistant-id",
    "name": "Telnyx Support Line"
  }'
```

## Assign an Assistant

Every phone number can be linked to an assistant or squad for inbound calls:

```bash
curl -X PATCH https://api.vapi.ai/phone-number/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "assistantId": "your-assistant-id"
  }'
```

Or assign a squad:
```bash
curl -X PATCH https://api.vapi.ai/phone-number/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "squadId": "your-squad-id"
  }'
```

## Phone Number Hooks

Configure automated actions when calls come in:

```json
{
  "hooks": [
    {
      "on": "call.ringing",
      "do": [
        {
          "type": "say",
          "exact": "Please hold while we connect you."
        }
      ]
    }
  ]
}
```

## Managing Phone Numbers

```bash
# List all phone numbers
curl https://api.vapi.ai/phone-number \
  -H "Authorization: Bearer $VAPI_API_KEY"

# Get a phone number
curl https://api.vapi.ai/phone-number/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY"

# Update a phone number
curl -X PATCH https://api.vapi.ai/phone-number/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Name"}'

# Delete a phone number
curl -X DELETE https://api.vapi.ai/phone-number/{id} \
  -H "Authorization: Bearer $VAPI_API_KEY"
```

## Inbound Call Flow

1. Caller dials your Vapi phone number
2. Vapi routes the call to the assigned assistant or squad
3. The assistant speaks its `firstMessage`
4. The conversation proceeds with the configured model, voice, and tools

## Outbound Call Flow

1. Create a call via `POST /call` with `phoneNumberId` and `customer.number`
2. Vapi dials the customer from your phone number
3. When answered, the assistant begins the conversation

## Free Number Limitations

- Cannot make international calls
- Daily call limits apply
- For production use, import your own Twilio/Vonage/Telnyx numbers

## References

- [Vapi Phone Numbers Docs](https://docs.vapi.ai/phone-numbers/import-twilio)
- [Free Telephony](https://docs.vapi.ai/free-telephony)
- [Phone Number Hooks](https://docs.vapi.ai/phone-numbers/phone-number-hooks)

## Additional Resources

This skills repository includes a **Vapi documentation MCP server** (`vapi-docs`) that gives your AI agent access to the full Vapi knowledge base. Use the `searchDocs` tool to look up anything beyond what this skill covers — advanced configuration, troubleshooting, SDK details, and more.

**Auto-configured:** If you cloned or installed these skills, the MCP server is already configured via `.mcp.json` (Claude Code), `.cursor/mcp.json` (Cursor), or `.vscode/mcp.json` (VS Code Copilot).

**Manual setup:** If your agent doesn't auto-detect the config, run:
```bash
claude mcp add vapi-docs -- npx -y mcp-remote https://docs.vapi.ai/_mcp/server
```

See the [README](../README.md#vapi-documentation-server-mcp) for full setup instructions across all supported agents.
