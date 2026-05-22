---
name: kapso-api
description: Kapso Platform API for customer onboarding, setup links, phone number provisioning, and connection detection. Use when working with multi-tenant WhatsApp integrations, embedded signup, or customer management.
---

# Kapso Platform API

## When to use

Use this skill for Platform API operations: creating customers, generating setup links, provisioning phone numbers, or detecting WhatsApp connections.

## Setup

Base host: `https://api.kapso.ai` (scripts append `/platform/v1`)

Auth header:
```
X-API-Key: <api_key>
```

## How to

### Onboard a customer

1. Create customer: `POST /customers`
2. Generate setup link: `POST /customers/:id/setup_links`
3. Customer completes embedded signup
4. Use `phone_number_id` to send messages

### Detect connection

Option A: Project webhook `whatsapp.phone_number.created`

Option B: Success redirect URL query params

Use both for best UX and backend reliability.

### Provision phone numbers

When creating a setup link, set:

```json
{
  "setup_link": {
    "provision_phone_number": true,
    "phone_number_country_isos": ["US"]
  }
}
```

## Notes

- Platform API base: `/platform/v1`
- Meta proxy base: `/meta/whatsapp/v24.0` (use for messaging and templates)
- Use `phone_number_id` as the primary WhatsApp identifier

## References

- [references/platform-api-reference.md](references/platform-api-reference.md) - Full endpoint reference
- [references/getting-started.md](references/getting-started.md) - Initial setup guide
- [references/setup-links.md](references/setup-links.md) - Setup link configuration
- [references/detecting-whatsapp-connection.md](references/detecting-whatsapp-connection.md) - Connection detection methods

## Related skills

- `kapso-automation` - Workflow automation
- `whatsapp-messaging` - WhatsApp messaging and templates
- `whatsapp-flows` - WhatsApp Flows
- `kapso-ops` - Operations and webhooks
