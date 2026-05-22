---
name: composio-connect
description: Universal fallback for executing actions across 1,000+ apps when no other skill is available. Use this skill ONLY when user requests an action on an app/service not covered by other skills (e.g., Notion, Asana, Trello, HubSpot, Airtable, Linear, Monday, Zendesk, Intercom, Stripe, Shopify, QuickBooks, Zoom, Microsoft 365, Dropbox, Box, Figma, Jira, Confluence, etc.). Do NOT use if another skill already handles the service. Triggers on requests to connect to external apps, execute actions on third-party services, or when user asks "can you actually do X" for an unsupported service.
---

# Composio Connect

## Overview

Universal action executor for 1,000+ apps. This is a **fallback skill** - only use when no other skill covers the requested service.

## When to Use This Skill

```
┌─────────────────────────────────────────────────────────────────┐
│ DECISION: Should I use Composio?                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 1. Does another skill already handle this service?              │
│    ├── Gmail/Drive/Calendar → google-workspace (USE THAT)       │
│    ├── Slack → slack-automation (USE THAT)                      │
│    ├── CRM (Attio) → attio-crm (USE THAT)                       │
│    ├── GitHub issues → Use gh CLI via Bash (USE THAT)           │
│    └── YouTube downloads → youtube-tools (USE THAT)             │
│                                                                 │
│ 2. Is the service NOT covered by other skills?                  │
│    ├── Notion, Asana, Trello, Monday → USE COMPOSIO             │
│    ├── HubSpot, Salesforce, Pipedrive → USE COMPOSIO            │
│    ├── Jira, Linear, Confluence → USE COMPOSIO                  │
│    ├── Airtable, Coda, ClickUp → USE COMPOSIO                   │
│    ├── Stripe, Shopify, QuickBooks → USE COMPOSIO               │
│    ├── Zendesk, Intercom, Freshdesk → USE COMPOSIO              │
│    ├── Microsoft 365, Teams, Outlook → USE COMPOSIO             │
│    ├── Dropbox, Box, OneDrive → USE COMPOSIO                    │
│    ├── Figma, Canva, Miro → USE COMPOSIO                        │
│    ├── Zoom, Webex, Google Meet → USE COMPOSIO                  │
│    └── 900+ other apps → USE COMPOSIO                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Environment Setup

```bash
# 1. Get free API key from https://platform.composio.dev
# 2. Add to .env file
COMPOSIO_API_KEY=your_api_key_here

# 3. Install SDK
pip install composio-core
```

## Quick Decision Tree

```
What do you want to do?
│
├── Execute a single action
│   └── python scripts/execute_action.py "Send email via Gmail to john@example.com"
│
├── List available apps
│   └── python scripts/execute_action.py --list-apps
│
├── List actions for an app
│   └── python scripts/execute_action.py --list-actions notion
│
├── Check connection status
│   └── python scripts/execute_action.py --check-connection notion
│
└── Connect to a new app
    └── python scripts/execute_action.py --connect notion
```

## Common Usage

### Execute an Action (Natural Language)
```bash
# Let Composio figure out the right tool
python scripts/execute_action.py "Create a Notion page titled 'Meeting Notes' in my workspace"
python scripts/execute_action.py "Add a task to Asana: Review Q4 budget"
python scripts/execute_action.py "Create a Linear issue for bug in checkout flow"
python scripts/execute_action.py "Send a HubSpot email to lead@company.com"
```

### List Available Apps
```bash
python scripts/execute_action.py --list-apps
python scripts/execute_action.py --list-apps --category crm
python scripts/execute_action.py --list-apps --category productivity
```

### Connect to an App (First Time)
```bash
# This will provide an OAuth link to authorize
python scripts/execute_action.py --connect notion
python scripts/execute_action.py --connect hubspot
python scripts/execute_action.py --connect jira
```

### Execute Specific Action
```bash
python scripts/execute_action.py --app notion --action create_page --params '{"title": "My Page", "content": "Hello world"}'
```

## Supported Apps by Category

### Productivity & Docs
| App | Common Actions |
|-----|----------------|
| Notion | Create page, add database entry, search |
| Asana | Create task, update project, assign |
| Trello | Create card, move card, add comment |
| Monday | Create item, update column, notify |
| ClickUp | Create task, update status, add comment |
| Coda | Create doc, update table, run automation |
| Airtable | Create record, update field, query base |

### CRM & Sales
| App | Common Actions |
|-----|----------------|
| HubSpot | Create contact, update deal, send email |
| Salesforce | Create lead, update opportunity, log call |
| Pipedrive | Create deal, update person, add activity |
| Zoho CRM | Create record, update module, send email |
| Close | Create lead, log call, send email |

### Development & DevOps
| App | Common Actions |
|-----|----------------|
| Jira | Create issue, update status, add comment |
| Linear | Create issue, assign, update priority |
| Confluence | Create page, update space, add comment |
| GitLab | Create issue, merge request, pipeline |
| Bitbucket | Create PR, add comment, update issue |

### Customer Support
| App | Common Actions |
|-----|----------------|
| Zendesk | Create ticket, update status, add note |
| Intercom | Send message, create conversation, tag user |
| Freshdesk | Create ticket, reply, update priority |
| Help Scout | Create conversation, send reply, tag |

### Finance & E-commerce
| App | Common Actions |
|-----|----------------|
| Stripe | Create invoice, check payment, refund |
| Shopify | Create order, update product, check inventory |
| QuickBooks | Create invoice, record payment, add expense |
| Xero | Create invoice, reconcile, add contact |
| Square | Create payment, update catalog, send receipt |

### Communication
| App | Common Actions |
|-----|----------------|
| Microsoft Teams | Send message, create channel, schedule meeting |
| Zoom | Create meeting, send invite, get recording |
| Discord | Send message, create channel, manage roles |
| Twilio | Send SMS, make call, send WhatsApp |

### Design & Creative
| App | Common Actions |
|-----|----------------|
| Figma | Get file, export assets, add comment |
| Canva | Create design, export, share |
| Miro | Create board, add sticky, export |

### Storage & Files
| App | Common Actions |
|-----|----------------|
| Dropbox | Upload file, share link, create folder |
| Box | Upload, share, manage permissions |
| OneDrive | Upload, share, sync |

## First-Time Authentication Flow

When connecting to a new app for the first time:

1. **Run connect command:**
   ```bash
   python scripts/execute_action.py --connect notion
   ```

2. **You'll receive an OAuth URL:**
   ```
   Please authorize Composio to access Notion:
   https://app.composio.dev/authorize/notion?token=xxx
   ```

3. **Click the link and authorize in your browser**

4. **Confirm back in terminal:**
   ```
   Authorization complete? (y/n): y
   ```

5. **Connection is now saved** - future requests work automatically

## Cost

- **Composio API:** Free tier available (check platform.composio.dev for limits)
- **No per-action cost** for most operations
- **Premium apps** may require paid Composio plan

## Security Notes

### Credential Handling
- Store `COMPOSIO_API_KEY` in `.env` (never commit)
- OAuth tokens are stored securely by Composio
- Revoke access anytime via platform.composio.dev

### Permissions
- Each app requests only necessary OAuth scopes
- Review permissions before authorizing
- Connections can be removed individually

### Data Privacy
- Composio processes requests but doesn't store your data
- Actions execute directly with the connected service
- Review Composio's privacy policy for details

## Troubleshooting

### Issue: "App not connected"
**Solution:** Run `--connect <app>` and complete OAuth flow

### Issue: "Invalid API key"
**Solution:** Check COMPOSIO_API_KEY in .env, regenerate if needed

### Issue: "Action failed"
**Cause:** Missing permissions or invalid parameters
**Solution:** Check `--list-actions <app>` for correct action format

### Issue: "Rate limited"
**Solution:** Wait and retry, or upgrade Composio plan

## Integration with Other Skills

### Fallback Pattern
When user asks for something not in your skills:
1. Check if Composio supports the app
2. Use Composio to execute the action
3. Return results to user

### Chaining Actions
```bash
# Research → Create Notion summary
# 1. Use parallel-research for research
# 2. Use composio to create Notion page with results

# Scrape → Update CRM
# 1. Use apify-scrapers to get company data
# 2. Use composio to update HubSpot contact
```

## Resources

- **Composio Platform:** https://platform.composio.dev
- **API Documentation:** https://docs.composio.dev
- **Supported Apps List:** https://app.composio.dev/apps
- **references/apps-catalog.md** - Full list of 1,000+ supported apps
- **references/actions-guide.md** - Common actions by category
