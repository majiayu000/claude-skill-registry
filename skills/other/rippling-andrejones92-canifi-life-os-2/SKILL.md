---
name: rippling
description: Manage workforce operations with Rippling's unified HR, IT, and Finance platform.
category: hr
---
# Rippling Skill

Manage workforce operations with Rippling's unified HR, IT, and Finance platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/rippling/install.sh | bash
```

Or manually:
```bash
cp -r skills/rippling ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set RIPPLING_API_KEY "your_api_key"
canifi-env set RIPPLING_COMPANY_ID "your_company_id"
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

1. **Employee Management**: Unified employee lifecycle management
2. **Payroll & Benefits**: Process payroll and manage benefits
3. **IT Provisioning**: Automatically provision apps and devices
4. **Time & Attendance**: Track time and manage schedules
5. **Workflow Automation**: Automate HR processes with custom workflows

## Usage Examples

### Onboard Employee
```
User: "Set up a new employee with laptop and app access"
Assistant: Creates employee and provisions IT
```

### Run Payroll
```
User: "Process next payroll run"
Assistant: Calculates and submits payroll
```

### Manage Apps
```
User: "Grant Slack access to the marketing team"
Assistant: Provisions Slack for team members
```

### Track Time
```
User: "Show me overtime hours this week"
Assistant: Returns time tracking summary
```

## Authentication Flow

1. Generate API key in Rippling admin
2. Note your company ID
3. Use API key for authentication
4. Scopes define access level

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify credentials |
| 403 Forbidden | No access | Check permissions |
| 404 Not Found | Resource not found | Verify ID |
| 429 Rate Limited | Too many requests | Wait and retry |

## Notes

- Unified HR, IT, Finance
- Device management included
- App provisioning automation
- Global payroll capability
- Custom workflows
- Modern platform
