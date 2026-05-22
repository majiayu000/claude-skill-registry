---
name: sendinblue
description: Manage email, SMS, and chat marketing with Brevo's all-in-one platform.
category: marketing
---
# Brevo (Sendinblue) Skill

Manage email, SMS, and chat marketing with Brevo's all-in-one platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/sendinblue/install.sh | bash
```

Or manually:
```bash
cp -r skills/sendinblue ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set BREVO_API_KEY "your_api_key"
```

## Privacy & Authentication

**Your credentials, your choice.** Canifi LifeOS respects your privacy.

### Option 1: Manual Browser Login (Recommended)
If you prefer not to share credentials with Claude Code:
1. Complete the [Browser Automation Setup](/setup/automation) using CDP mode
2. Login to the service manually in the Playwright-controlled Chrome window
3. Claude will use your authenticated session without ever seeing your password

### Option 2: Environment Variables
If you're comfortable sharing credentials, you can store them locally:
```bash
canifi-env set SERVICE_EMAIL "your-email"
canifi-env set SERVICE_PASSWORD "your-password"
```

**Note**: Credentials stored in canifi-env are only accessible locally on your machine and are never transmitted.

## Capabilities

1. **Email Campaigns**: Create and send email marketing campaigns
2. **Transactional Email**: Send transactional emails via SMTP or API
3. **SMS Marketing**: Send SMS campaigns and notifications
4. **Contact Management**: Manage contacts with lists and attributes
5. **Automation**: Build automated marketing workflows

## Usage Examples

### Send Campaign
```
User: "Create an email campaign in Brevo for the sale announcement"
Assistant: Creates campaign with content and recipients
```

### Add Contact
```
User: "Add a subscriber to my newsletter list in Brevo"
Assistant: Creates contact with list assignment
```

### Send SMS
```
User: "Send an SMS notification about the order update"
Assistant: Sends SMS to customer phone number
```

### Create Automation
```
User: "Create a welcome email automation in Brevo"
Assistant: Sets up automation workflow with trigger
```

## Authentication Flow

1. Get API key from Brevo account settings
2. Use API key in request header
3. Single key for all operations
4. SMTP credentials available separately

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify API key |
| 400 Bad Request | Invalid data | Check request format |
| 404 Not Found | Resource not found | Verify ID |
| 429 Rate Limited | Too many requests | Wait and retry |

## Notes

- Formerly known as Sendinblue
- Free tier with 300 emails/day
- Transactional and marketing in one
- SMS and WhatsApp support
- Live chat included
- CRM features built-in
