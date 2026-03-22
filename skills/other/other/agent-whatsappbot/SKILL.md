---
name: agent-whatsappbot
description: Interact with WhatsApp using Cloud API credentials - send messages, manage templates
version: 1.15.0
allowed-tools: Bash(agent-whatsappbot:*)
metadata:
  openclaw:
    requires:
      bins:
        - agent-whatsappbot
    install:
      - kind: node
        package: agent-messenger
        bins: [agent-whatsappbot]
---

# Agent WhatsAppBot

A TypeScript CLI tool that enables AI agents and humans to send messages through WhatsApp Business Cloud API. Designed for customer notifications, transactional messaging, and CI/CD integrations using Phone Number ID + Access Token authentication.

## Key Concepts

Before diving in, a few things about WhatsApp Business Cloud API:

- **Send-only** — The Cloud API is webhook-only for inbound messages. This CLI cannot list or read received messages.
- **Template messages** — Outside the 24-hour customer service window, you must use pre-approved message templates. Free-form text only works within 24 hours of the customer's last message.
- **Phone Number ID** — Your WhatsApp Business phone number's unique identifier (not the phone number itself). Found in Meta Business Manager.
- **Access Token** — A permanent or temporary token from Meta Business Manager with `whatsapp_business_messaging` permission.
- **Meta Business Manager** — All setup (phone numbers, templates, verification) happens at [business.facebook.com](https://business.facebook.com).
- **Rate limits** — Tier 0-3: 80 messages per second. Tier 4: 1,000 messages per second. Tiers are based on business verification and messaging volume.

## Quick Start

```bash
# Set your API credentials
agent-whatsappbot auth set your-phone-number-id your-access-token

# Verify authentication
agent-whatsappbot auth status

# Send a text message (recipient must have messaged you within 24h)
agent-whatsappbot message send 15551234567 "Hello from the CLI!"

# List available message templates
agent-whatsappbot template list --pretty
```

## Authentication

### API Credential Setup

agent-whatsappbot uses Phone Number ID + Access Token pairs from Meta Business Manager:

```bash
# Set credentials (validates against WhatsApp Cloud API before saving)
agent-whatsappbot auth set your-phone-number-id your-access-token

# Check auth status
agent-whatsappbot auth status

# Clear stored credentials
agent-whatsappbot auth clear
```

### Multi-Account Management

```bash
# List stored accounts
agent-whatsappbot auth list

# Switch active account
agent-whatsappbot auth use <account-id>

# Remove a stored account
agent-whatsappbot auth remove <account-id>
```

## Memory

The agent maintains a `~/.config/agent-messenger/MEMORY.md` file as persistent memory across sessions. This is agent-managed, the CLI does not read or write this file. Use the `Read` and `Write` tools to manage your memory file.

### Reading Memory

At the **start of every task**, read `~/.config/agent-messenger/MEMORY.md` using the `Read` tool to load any previously discovered account IDs, template names, recipient numbers, and preferences.

- If the file doesn't exist yet, that's fine. Proceed without it and create it when you first have useful information to store.
- If the file can't be read (permissions, missing directory), proceed without memory. Don't error out.

### Writing Memory

After discovering useful information, update `~/.config/agent-messenger/MEMORY.md` using the `Write` tool. Write triggers include:

- After discovering account IDs and phone numbers (from `auth list`, `auth status`, etc.)
- After discovering template names and their parameters (from `template list`, `template get`, etc.)
- After the user gives you an alias or preference ("call this the notifications account", "my main template is X")

When writing, include the **complete file content**. The `Write` tool overwrites the entire file.

### What to Store

- Account IDs with phone numbers
- Template names with their required parameters
- Frequently used recipient numbers with context
- User-given aliases ("notifications account", "marketing number")
- Any user preference expressed during interaction

### What NOT to Store

Never store access tokens or any credentials. Never store full message content (just context). Never store personal user data.

### Handling Stale Data

If a memorized template returns an error (template not found, account invalid), remove it from `MEMORY.md`. Don't blindly trust memorized data. Verify when something seems off. Prefer re-listing over using a memorized value that might be stale.

### Format / Example

```markdown
# Agent Messenger Memory

## WhatsApp Accounts

- `112233445566` - Acme Notifications (Phone: +1 555 012 3456)

## Templates (Acme Notifications)

- `order_confirmation` - language: en_US, params: [customer_name, order_id]
- `shipping_update` - language: en_US, params: [customer_name, tracking_number]
- `appointment_reminder` - language: en_US, params: [customer_name, date, time]

## Frequent Recipients

- `15559876543` - Support escalation line
- `15551112222` - QA test number

## Aliases

- "notifications" -> `112233445566` (Acme Notifications)

## Notes

- order_confirmation template requires customer_name and order_id as components
- Business verified at Tier 2 (80 MPS limit)
```

> Memory lets you skip repeated `template list` calls. When you already know a template name from a previous session, use it directly.

## Commands

### Auth Commands

```bash
# Set account credentials (validates against API)
agent-whatsappbot auth set <phone-number-id> <access-token>

# Check auth status
agent-whatsappbot auth status
agent-whatsappbot auth status --account <account-id>

# List stored accounts
agent-whatsappbot auth list

# Switch active account
agent-whatsappbot auth use <account-id>

# Remove a stored account
agent-whatsappbot auth remove <account-id>

# Clear all credentials
agent-whatsappbot auth clear
```

### Message Commands

```bash
# Send a text message
agent-whatsappbot message send <to> <text>
agent-whatsappbot message send 15551234567 "Your order has shipped!"

# Send a template message
agent-whatsappbot message send-template <to> <template-name>
agent-whatsappbot message send-template 15551234567 order_confirmation --language en_US --components '[{"type":"body","parameters":[{"type":"text","text":"Alice"},{"type":"text","text":"ORD-9876"}]}]'

# Send a reaction to a message
agent-whatsappbot message send-reaction <to> <message-id> <emoji>
agent-whatsappbot message send-reaction 15551234567 wamid.abc123 "👍"

# Send an image
agent-whatsappbot message send-image <to> <url>
agent-whatsappbot message send-image 15551234567 "https://example.com/photo.jpg" --caption "Product photo"

# Send a document
agent-whatsappbot message send-document <to> <url>
agent-whatsappbot message send-document 15551234567 "https://example.com/invoice.pdf" --filename "invoice.pdf" --caption "Your invoice"
```

### Template Commands

```bash
# List message templates
agent-whatsappbot template list
agent-whatsappbot template list --limit 20

# Get template details
agent-whatsappbot template get <template-name>
agent-whatsappbot template get order_confirmation
```

## Output Format

### JSON (Default)

All commands output JSON by default for AI consumption:

```json
{
  "messaging_product": "whatsapp",
  "contacts": [{ "input": "15551234567", "wa_id": "15551234567" }],
  "messages": [{ "id": "wamid.HBgNMTU1NTEyMzQ1NjcVAgA..." }]
}
```

### Pretty (Human-Readable)

Use `--pretty` flag for formatted output:

```bash
agent-whatsappbot template list --pretty
```

## Global Options

| Option          | Description                                |
| --------------- | ------------------------------------------ |
| `--pretty`      | Human-readable output instead of JSON      |
| `--account <id>`| Use a specific account for this command     |

## Common Patterns

### Send a notification outside the 24h window

Template messages are required when the customer hasn't messaged you in the last 24 hours. Always check your available templates first:

```bash
# List templates to find the right one
agent-whatsappbot template list --pretty

# Get template details to see required parameters
agent-whatsappbot template get order_confirmation --pretty

# Send the template message
agent-whatsappbot message send-template 15551234567 order_confirmation \
  --language en_US \
  --components '[{"type":"body","parameters":[{"type":"text","text":"Alice"},{"type":"text","text":"ORD-9876"}]}]'
```

### Send a free-form reply within the 24h window

When a customer has messaged you within the last 24 hours, you can send any text:

```bash
agent-whatsappbot message send 15551234567 "Thanks for reaching out! We'll look into this right away."
```

### Send a document with a receipt

```bash
agent-whatsappbot message send-document 15551234567 "https://example.com/receipt.pdf" \
  --filename "receipt-2024-01.pdf" \
  --caption "Here's your receipt for January"
```

### CI/CD deployment notification

```bash
agent-whatsappbot message send-template 15559876543 deployment_alert \
  --language en_US \
  --components '[{"type":"body","parameters":[{"type":"text","text":"v2.1.0"},{"type":"text","text":"production"},{"type":"text","text":"success"}]}]'
```

## Error Handling

All commands return consistent error format:

```json
{
  "error": "No credentials. Run \"auth set <phone-number-id> <access-token>\" first."
}
```

Common errors: `No credentials`, `Account not found`, `Template not found`, `Invalid phone number format`, `Message failed to send (outside 24h window, use a template)`.

## Configuration

Credentials stored in `~/.config/agent-messenger/whatsappbot-credentials.json` (0600 permissions).

Config format:

```json
{
  "current": { "account_id": "112233445566" },
  "accounts": {
    "112233445566": {
      "account_id": "112233445566",
      "phone_number_id": "112233445566",
      "phone_number": "+1 555 012 3456",
      "access_token": "..."
    }
  }
}
```

## Limitations

- **Cannot list or read received messages** — WhatsApp Cloud API delivers inbound messages via webhooks only. This CLI is send-only.
- **Template messages required outside 24h window** — Free-form text only works within 24 hours of the customer's last message to you.
- **Business verification required for higher tiers** — Unverified businesses are limited in daily messaging volume.
- **Rate limits** — Tier 0-3: 80 messages per second. Tier 4: 1,000 messages per second.
- **No group chat support** — WhatsApp Cloud API does not support group messaging.
- **No real-time events / WebSocket connection** — Inbound messages require a separate webhook server.
- **No message editing or deletion**
- **No file upload from local disk** — Images and documents must be provided as URLs.
- **No voice or video calls**
- **Phone number must be registered with WhatsApp Business** — Personal WhatsApp numbers won't work.

## Troubleshooting

### `agent-whatsappbot: command not found`

**`agent-whatsappbot` is NOT the npm package name.** The npm package is `agent-messenger`.

If the package is installed globally, use `agent-whatsappbot` directly:

```bash
agent-whatsappbot message send 15551234567 "Hello"
```

If the package is NOT installed, run it directly with `npx -y`:

```bash
npx -y agent-messenger whatsappbot message send 15551234567 "Hello"
```

> **Note**: If the user prefers a different package runner (e.g., `bunx`, `pnpx`, `pnpm dlx`), use that instead.

**NEVER run `npx agent-whatsappbot`, `bunx agent-whatsappbot`, or `pnpm dlx agent-whatsappbot`**. It will fail or install a wrong package since `agent-whatsappbot` is not the npm package name.

### How to get API credentials

1. Go to [Meta Business Manager](https://business.facebook.com/)
2. Navigate to your WhatsApp Business Account
3. Open **WhatsApp Manager > Phone Numbers** to find your **Phone Number ID**
4. Go to **Business Settings > System Users** to create a system user and generate an **Access Token** with `whatsapp_business_messaging` permission
5. Run `agent-whatsappbot auth set <phone-number-id> <access-token>`

### Template messages not sending

- Verify the template exists: `agent-whatsappbot template get <name>`
- Check the template status is `APPROVED` (not `PENDING` or `REJECTED`)
- Ensure the `--language` matches the template's language code exactly
- Verify `--components` JSON matches the template's parameter structure

### Rate limiting

WhatsApp enforces rate limits based on your business tier. The CLI automatically retries on rate limit (429) responses. For bulk operations, add delays between requests to avoid hitting limits.

### Message not delivered

- Confirm the recipient's phone number is on WhatsApp
- Use full international format without `+` prefix (e.g., `15551234567` not `+1-555-123-4567`)
- If outside the 24h window, use `message send-template` instead of `message send`
- Check that your WhatsApp Business account is active and not restricted
