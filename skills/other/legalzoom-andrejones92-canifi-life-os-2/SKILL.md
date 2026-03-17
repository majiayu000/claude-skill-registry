---
name: legalzoom
description: Access legal documents and business formation services with LegalZoom.
category: communication
---
# LegalZoom Skill

Access legal documents and business formation services with LegalZoom.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/legalzoom/install.sh | bash
```

Or manually:
```bash
cp -r skills/legalzoom ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set LEGALZOOM_EMAIL "your_email"
canifi-env set LEGALZOOM_PASSWORD "your_password"
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

1. **Business Formation**: Form LLCs, corporations, and nonprofits
2. **Legal Documents**: Access and create legal documents
3. **Registered Agent**: Manage registered agent services
4. **Trademark**: File and manage trademark applications
5. **Compliance**: Stay compliant with annual reports

## Usage Examples

### Check Formation Status
```
User: "What's the status of my LLC formation?"
Assistant: Returns formation progress
```

### Order Document
```
User: "Order a will template from LegalZoom"
Assistant: Initiates document order
```

### View Filings
```
User: "Show me my upcoming compliance deadlines"
Assistant: Returns compliance calendar
```

### Registered Agent
```
User: "Update my registered agent address"
Assistant: Initiates address change
```

## Authentication Flow

1. LegalZoom uses account authentication
2. No official public API
3. Browser automation for access
4. Session-based authentication

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Verify email and password |
| Session Expired | Timeout | Re-authenticate |
| Service Error | System issue | Retry later |
| Order Failed | Payment issue | Check payment method |

## Notes

- Consumer legal services
- Business formation leader
- Attorney consultations available
- Ongoing compliance services
- No official API
- Consumer-focused platform
