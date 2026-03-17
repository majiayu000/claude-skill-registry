---
name: costar
description: Access commercial real estate data with CoStar's professional platform.
category: realestate
---
# CoStar Skill

Access commercial real estate data with CoStar's professional platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/costar/install.sh | bash
```

Or manually:
```bash
cp -r skills/costar ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set COSTAR_USERNAME "your_username"
canifi-env set COSTAR_PASSWORD "your_password"
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

1. **Property Search**: Search commercial properties for sale and lease
2. **Market Analytics**: Access commercial real estate analytics
3. **Comparable Sales**: View comparable property transactions
4. **Tenant Data**: Research tenant and lease information
5. **Property Reports**: Generate detailed property reports

## Usage Examples

### Search Properties
```
User: "Find office spaces for lease in Manhattan"
Assistant: Returns commercial listings
```

### Market Analysis
```
User: "What's the office vacancy rate in San Francisco?"
Assistant: Returns market analytics
```

### Find Comps
```
User: "Show me comparable sales for this property"
Assistant: Returns comparable transactions
```

### Generate Report
```
User: "Create a property report for 123 Business Ave"
Assistant: Generates detailed report
```

## Authentication Flow

1. CoStar requires subscription
2. Professional credentials needed
3. Browser-based authentication
4. Enterprise-level access

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Verify subscription |
| Access Denied | Subscription issue | Check account status |
| Data Unavailable | Market not covered | Try different area |
| Report Error | Generation failed | Retry |

## Notes

- Industry-leading CRE data
- Subscription required
- Professional platform
- Enterprise pricing
- No public API
- Research-grade data
