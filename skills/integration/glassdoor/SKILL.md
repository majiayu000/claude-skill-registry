---
name: glassdoor
description: Manage employer brand and job listings on Glassdoor's review platform.
category: hr
---
# Glassdoor Skill

Manage employer brand and job listings on Glassdoor's review platform.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/glassdoor/install.sh | bash
```

Or manually:
```bash
cp -r skills/glassdoor ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GLASSDOOR_PARTNER_ID "your_partner_id"
canifi-env set GLASSDOOR_API_KEY "your_api_key"
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

1. **Company Profile**: Manage company profile and information
2. **Job Posting**: Post jobs and manage listings
3. **Review Management**: Monitor and respond to employee reviews
4. **Salary Insights**: Access salary data and benchmarks
5. **Analytics**: Track employer brand metrics

## Usage Examples

### View Reviews
```
User: "Show me our latest Glassdoor reviews"
Assistant: Returns recent employee reviews
```

### Post Job
```
User: "Post the Product Manager position on Glassdoor"
Assistant: Creates job listing
```

### Check Rating
```
User: "What's our current Glassdoor rating?"
Assistant: Returns company rating and trends
```

### Salary Benchmark
```
User: "What's the average salary for Software Engineers in NYC?"
Assistant: Returns salary data and ranges
```

## Authentication Flow

1. Apply for Glassdoor API partnership
2. Get Partner ID and API key
3. Use credentials in request headers
4. Limited API access for employers

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid credentials | Verify partner credentials |
| 403 Forbidden | No API access | Apply for partnership |
| 404 Not Found | Company not found | Verify company ID |
| 429 Rate Limited | Too many requests | Wait and retry |

## Notes

- Employee review platform
- Employer branding focus
- Salary data included
- API access limited
- Enhanced profile options
- Integration with job boards
