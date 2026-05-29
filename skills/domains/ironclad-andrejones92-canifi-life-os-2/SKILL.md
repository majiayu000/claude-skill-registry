---
name: ironclad
description: Manage enterprise contracts with Ironclad's digital contracting platform.
category: legal
---
# Ironclad Skill

Manage enterprise contracts with Ironclad's digital contracting platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/ironclad/install.sh | bash
```

Or manually:
```bash
cp -r skills/ironclad ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set IRONCLAD_API_KEY "your_api_key"
canifi-env set IRONCLAD_SUBDOMAIN "your_subdomain"
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

1. **Contract Workflow**: Build and manage contract approval workflows
2. **Clause Library**: Access and insert approved legal clauses
3. **AI Review**: Use AI to review and analyze contracts
4. **Repository**: Central repository for all contracts
5. **Reporting**: Track contract metrics and bottlenecks

## Usage Examples

### Launch Workflow
```
User: "Start a new vendor agreement workflow"
Assistant: Initiates contract workflow
```

### Review Contract
```
User: "Analyze this contract for risk"
Assistant: Returns AI-powered risk analysis
```

### Search Repository
```
User: "Find all contracts with TechCorp"
Assistant: Returns matching contracts
```

### Track Workflow
```
User: "Where is the sales agreement in the approval process?"
Assistant: Returns workflow status
```

## Authentication Flow

1. Generate API key in Ironclad admin
2. Note your subdomain
3. Use API key for authentication
4. Scoped by workspace

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify credentials |
| 403 Forbidden | No access | Check permissions |
| 404 Not Found | Resource not found | Verify ID |
| 429 Rate Limited | Too many requests | Wait and retry |

## Notes

- Enterprise CLM platform
- AI-powered features
- Advanced workflows
- Legal team focused
- Salesforce integration
- Premium pricing
