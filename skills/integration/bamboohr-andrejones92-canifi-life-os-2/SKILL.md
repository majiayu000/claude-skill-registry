---
name: bamboohr
description: Manage small business HR with BambooHR's people management platform.
category: hr
---
# BambooHR Skill

Manage small business HR with BambooHR's people management platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/bamboohr/install.sh | bash
```

Or manually:
```bash
cp -r skills/bamboohr ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set BAMBOOHR_SUBDOMAIN "your_subdomain"
canifi-env set BAMBOOHR_API_KEY "your_api_key"
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

1. **Employee Database**: Maintain employee records and org chart
2. **Time Off**: Manage PTO requests and balances
3. **Onboarding**: Set up new hire onboarding workflows
4. **Performance**: Track goals and performance reviews
5. **Reporting**: Generate HR reports and analytics

## Usage Examples

### Add Employee
```
User: "Add a new employee to BambooHR"
Assistant: Creates employee record
```

### Request Time Off
```
User: "Submit a PTO request for next week"
Assistant: Creates time off request
```

### View Directory
```
User: "Show me the engineering team directory"
Assistant: Returns department employees
```

### Generate Report
```
User: "Create a report of employee anniversaries"
Assistant: Generates anniversary report
```

## Authentication Flow

1. Generate API key in BambooHR settings
2. Use Basic Auth with API key as password
3. Subdomain identifies your account
4. Use 'x' as username

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify credentials |
| 403 Forbidden | No access | Check user permissions |
| 404 Not Found | Employee not found | Verify employee ID |
| 429 Rate Limited | Too many requests | Wait and retry |

## Notes

- SMB-focused HRIS
- User-friendly interface
- Mobile app included
- ATS add-on available
- Benefits administration
- Affordable pricing
