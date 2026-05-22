---
name: instantly
description: Instantly.ai cold email outreach API - manage campaigns, leads, accounts, and analytics. Use for cold email automation, lead management, campaign creation/monitoring, and email account warmup.
metadata: {"clawdbot": {"emoji": "📧", "requires": {"env": ["INSTANTLY_API_KEY"]}, "primaryEnv": "INSTANTLY_API_KEY"}}
---

# Instantly.ai Skill

Manage cold email outreach via the Instantly.ai API V2. This skill provides full access to campaigns, leads, email accounts, analytics, and more.

## Setup

1. Get your API key from Instantly Dashboard → Settings → API Key
2. Set the environment variable:
   ```bash
   export INSTANTLY_API_KEY="your-api-key-here"
   ```
   Or add to your shell profile / Clawdbot config.

**Note:** API access requires Hypergrowth plan or above.

## Usage

Use the CLI script for all operations:

```bash
# List campaigns
<skill>/scripts/instantly.py campaigns list

# Get campaign details
<skill>/scripts/instantly.py campaigns get <campaign_id>

# List leads in a campaign
<skill>/scripts/instantly.py leads list --campaign <campaign_id>

# Add a lead
<skill>/scripts/instantly.py leads create --campaign <campaign_id> --email "john@example.com" --first-name "John"

# List email accounts
<skill>/scripts/instantly.py accounts list

# Get analytics
<skill>/scripts/instantly.py analytics summary --campaign <campaign_id>
```

## Commands Reference

### Campaigns

| Command | Description |
|---------|-------------|
| `campaigns list` | List all campaigns |
| `campaigns get <id>` | Get campaign details |
| `campaigns create --name "..." --schedule "..."` | Create new campaign |
| `campaigns update <id> --name "..."` | Update campaign |
| `campaigns launch <id>` | Launch/activate campaign |
| `campaigns pause <id>` | Pause campaign |

### Leads

| Command | Description |
|---------|-------------|
| `leads list --campaign <id>` | List leads in campaign |
| `leads get <id>` | Get lead details |
| `leads create --campaign <id> --email "..."` | Add lead to campaign |
| `leads update <id> --status <n>` | Update lead status |
| `leads delete <id>` | Delete lead |
| `leads bulk-add --campaign <id> --file <csv>` | Bulk add leads from CSV |

**Lead Status Codes:**
- 1 = Active
- 2 = Paused
- 3 = Completed
- -1 = Bounced
- -2 = Unsubscribed
- -3 = Skipped

**Interest Status:**
- 1 = Interested
- 2 = Meeting Booked
- 3 = Meeting Completed
- 4 = Won
- 0 = Out of Office
- -1 = Not Interested
- -2 = Wrong Person
- -3 = Lost
- -4 = No Show

### Accounts (Email Sending Accounts)

| Command | Description |
|---------|-------------|
| `accounts list` | List all email accounts |
| `accounts get <email>` | Get account details |
| `accounts create --email "..." --imap-host "..." ...` | Add email account |
| `accounts update <email> --daily-limit 50` | Update account settings |
| `accounts warmup-start <email>` | Start warmup |
| `accounts warmup-pause <email>` | Pause warmup |

**Account Status:**
- 1 = Active
- 2 = Paused
- -1 = Connection Error
- -2 = Soft Bounce Error
- -3 = Sending Error

### Analytics

| Command | Description |
|---------|-------------|
| `analytics summary --campaign <id>` | Campaign summary stats |
| `analytics daily --campaign <id> --days 7` | Daily breakdown |

### Lead Lists

| Command | Description |
|---------|-------------|
| `lists list` | List all lead lists |
| `lists get <id>` | Get list details |
| `lists create --name "..."` | Create lead list |

### Emails (Unibox)

| Command | Description |
|---------|-------------|
| `emails list --campaign <id>` | List emails in campaign |
| `emails get <id>` | Get email details |
| `emails reply <id> --message "..."` | Send reply |

### Webhooks

| Command | Description |
|---------|-------------|
| `webhooks list` | List webhooks |
| `webhooks create --url "..." --event "..."` | Create webhook |
| `webhooks delete <id>` | Delete webhook |

**Webhook Events:**
- `lead_interested`
- `email_sent`
- `email_opened`
- `email_clicked`
- `email_replied`
- `lead_unsubscribed`

## Common Workflows

### Check Campaign Health

```bash
# See all campaigns with status
<skill>/scripts/instantly.py campaigns list

# Get detailed analytics for underperforming campaign
<skill>/scripts/instantly.py analytics summary --campaign <id>

# Check account health
<skill>/scripts/instantly.py accounts list
```

### Add Leads to Running Campaign

```bash
# Single lead
<skill>/scripts/instantly.py leads create \
  --campaign <campaign_id> \
  --email "prospect@company.com" \
  --first-name "Jane" \
  --last-name "Doe" \
  --company "ACME Inc"

# Bulk from CSV (email,first_name,last_name,company_name columns)
<skill>/scripts/instantly.py leads bulk-add \
  --campaign <campaign_id> \
  --file /path/to/leads.csv
```

### Monitor Replies

```bash
# List recent replies
<skill>/scripts/instantly.py emails list --campaign <id> --type reply

# Get conversation thread
<skill>/scripts/instantly.py emails get <email_id>
```

## Output Formats

All commands support `--format` option:
- `table` (default) - Human-readable table
- `json` - Full JSON response
- `csv` - CSV for spreadsheets

Example:
```bash
<skill>/scripts/instantly.py leads list --campaign <id> --format csv > leads.csv
```

## Error Handling

The script returns standard exit codes:
- 0 = Success
- 1 = API error (check message)
- 2 = Invalid arguments

API errors include the Instantly error message in stderr.

## Rate Limits

Instantly API has rate limits. The script handles 429 responses with automatic retry and exponential backoff.

## API Reference

Full API docs: https://developer.instantly.ai/api/v2

Base URL: `https://api.instantly.ai/api/v2/`
Authentication: Bearer token in Authorization header
