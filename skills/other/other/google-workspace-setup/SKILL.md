---
name: google-workspace-setup
description: Connect Google Workspace (Gmail, Calendar, Docs) to Dex for email-aware planning and meeting prep
integration:
  id: google-workspace
  name: Google Workspace
  auth: oauth2
  mcp_server: google-workspace-mcp
  category: communication
  sync_direction: bidirectional
---

# Google Workspace Setup

Connect your Google Workspace to Dex so your daily plans, meeting prep, and weekly reviews get richer context from email, Google Calendar, and Docs.

## What This Enables

Once connected, Dex can:

**Read:**
- Search emails by sender, subject, or keyword
- Surface unread emails from priority senders
- Pull email threads for meeting attendees
- Access Google Calendar events (if not using Apple Calendar)
- Search Google Docs and Sheets

**Write (always with your confirmation):**
- Send emails (Dex will always show you the draft and ask before sending)
- Create calendar events
- Create or update Google Docs

**Skill Enhancements:**
- **Daily Plan** (`/daily-plan`) gets an email digest -- unread count, threads needing reply, emails from today's meeting contacts
- **Meeting Prep** (`/meeting-prep`) shows recent email threads with each attendee
- **Week Review** (`/week-review`) includes email stats -- sent/received, response time, top correspondents
- **Draft Messages** (if configured) can send via Gmail with confirmation

**New Capabilities:**
- **Email Follow-Up Detection:** During `/daily-plan`, Dex checks for emails awaiting replies for more than 48 hours and surfaces them: "Sarah hasn't replied to your pricing email from 3 days ago. Draft a nudge?"

## Privacy

Dex reads your email **on demand** -- nothing is stored permanently. Emails are fetched, summarized, and discarded after the session. Only YOUR account is accessible (scoped to your OAuth login). The OAuth token stays local on your machine and is gitignored.

## When to Run

- User types `/google-workspace-setup`
- User asks about connecting Gmail or Google Workspace
- User wants email context in daily plans or meeting prep
- During `/integrate-mcp` if Gmail or Google Workspace is mentioned

---

## Setup Flow

### Step 1: Check if Already Connected

1. Check `System/integrations/config.yaml` for `google-workspace.enabled: true`
2. If enabled, try a test query via Google Workspace MCP (e.g., search for a recent email)
3. If healthy and responding, skip to **Step 5** (Configure Labels)
4. If the tool is not available or errors, continue to Step 2

### Step 2: Explain What We're Setting Up

Say:

```
**Let's connect Google Workspace to Dex.**

This uses an open-source MCP bridge that connects to your Google account via OAuth.
You'll authorize Dex once, and it remembers your login locally.

**What you'll need:**
- A Google account (Gmail, Workspace, or personal)
- About 3 minutes for the OAuth flow

**What Dex will be able to do:**
- Read your emails (search, unread, threads)
- Read Google Calendar, Docs, and Sheets
- Send emails and create events (always with your confirmation first)

**Ready to go?**
```

Wait for confirmation.

### Step 3: Add the Google Workspace MCP Server

Check the user's MCP configuration. If `google-workspace-mcp` is not listed:

1. Explain what we're adding:

```
I need to add the Google Workspace connector to your Dex configuration.

This is an open-source bridge (github.com/taylorwilsdon/google_workspace_mcp)
that connects to Google's APIs via OAuth. Your credentials stay on your machine.
```

2. Add to the user's `.mcp.json` (use the `/dex-add-mcp` skill or manual edit):

```json
{
  "google-workspace-mcp": {
    "command": "npx",
    "args": ["-y", "google-workspace-mcp"],
    "env": {}
  }
}
```

3. Tell the user the MCP server needs to restart for changes to take effect.

### Step 4: Authenticate via OAuth

1. Run `npx google-workspace-mcp` -- this starts the OAuth flow
2. A browser window opens for Google sign-in
3. The user authorizes the requested scopes (Gmail read/send, Calendar, Docs)
4. The token is saved locally to `System/.gmail-oauth-token.json`

**If OAuth succeeds:**
```
Connected! I can see your Google Workspace account.
```

**If it fails:**
```
The OAuth flow didn't complete. A few things to check:

1. **Did the browser open?** If not, try copying the URL from the terminal output
2. **Did you approve all permissions?** Dex needs Gmail, Calendar, and Docs access
3. **Firewall or proxy?** Corporate networks sometimes block OAuth redirects

Want to retry?
```

Retry up to 2 times, then offer to skip and come back later.

### Step 5: Configure Labels and Write Preferences

Once connected, ask:

```
**Which Gmail labels matter most for your work?**

I'll prioritize these when building your email digest.

Common choices:
- INBOX (always included)
- IMPORTANT
- STARRED
- Custom labels (e.g., "Deals", "Follow-Up")

**Which labels should I watch?** (Just list names, or say "show me what's available")
```

Then ask about write operations:

```
**For sending emails and creating events:**

Would you prefer:
1. **Auto-draft** -- I'll compose messages and show them for your approval before sending
2. **Ask each time** -- I'll ask before even drafting anything

(You can change this anytime by re-running /google-workspace-setup)
```

Save their preference. Map choice 1 to `draft_and_send: true`, choice 2 to `draft_and_send: false`.

### Step 6: Test the Connection

Run a quick test to confirm everything works:

1. Search for a recent email (e.g., from the last 24 hours)
2. Verify calendar access (list today's events)

Show a brief summary:

```
**Quick test results:**
- Email search: Working (found [N] recent emails)
- Calendar: Working (found [N] events today)

Everything looks good!
```

If either fails, troubleshoot before proceeding.

### Step 7: Save Configuration

Write to `System/integrations/config.yaml` -- update the google-workspace section:

```yaml
google-workspace:
  enabled: true
  configured_at: YYYY-MM-DD
  mcp_server: google-workspace-mcp
  auth_type: oauth2
  account: user@example.com
  labels:
    - INBOX
    - IMPORTANT
  features:
    email_digest: true
    email_followup: true
    draft_and_send: true   # or false based on user preference
```

If the file already exists, only update the `google-workspace:` section. Preserve other integration configs.

### Step 8: Confirm with Capability Cascade

```
**Google Workspace is connected!**

Here's what just got enhanced:

- **Daily Plan** (`/daily-plan`) now includes an email digest:
  - Unread count from priority senders
  - Threads needing reply (> 24h)
  - Emails from today's meeting attendees
  - Follow-up detection ("Sarah hasn't replied in 3 days")

- **Meeting Prep** (`/meeting-prep`) now shows email context:
  - Recent email threads with each attendee
  - Last email date and topic
  - Unanswered emails to flag

- **Week Review** (`/week-review`) now includes email stats:
  - Emails sent/received this week
  - Average response time
  - Top senders and recipients

You can adjust settings anytime by running `/google-workspace-setup` again.
```

---

## New Capabilities

### Email Follow-Up Detection

During `/daily-plan`, Dex checks for stale email threads:

1. Search for sent emails from the last 7 days
2. For each sent email, check if there's a reply
3. If no reply after 48 hours, surface it:

```
**Emails awaiting reply:**
- Sarah Chen hasn't replied to your pricing email (sent 3 days ago). Draft a nudge?
- Mike Ross hasn't replied to the proposal follow-up (sent 2 days ago).
```

**Rules:**
- Only check emails YOU sent (not inbound)
- 48-hour threshold (skip weekends in the count)
- Limit to 5 items max (don't overwhelm)
- Only runs if `google-workspace.features.email_followup: true` in config
- Surfaces during the email digest step of `/daily-plan`

---

## Troubleshooting

### OAuth Token Expired

Google OAuth tokens typically last 1 hour, but refresh tokens are longer-lived. If you see auth errors:

1. Run `/google-workspace-setup` to trigger a token refresh
2. If the refresh token is also expired, you'll need to re-authorize through the browser
3. This is rare -- usually happens after 6+ months or if you revoked access in Google settings

### "Google Workspace MCP not found"

The server might not be in your configuration. Re-run `/google-workspace-setup` and it will detect and fix this.

### Permission Errors

If certain features don't work (e.g., can't send emails):

1. The OAuth scopes might be incomplete
2. Run `/google-workspace-setup` to re-authorize with full scopes
3. Make sure you approved ALL permissions in the Google consent screen

### Rate Limiting

Google APIs have generous limits for personal use. If you see rate errors:

1. Wait 60 seconds and retry
2. If persistent, you may be hitting a Workspace admin quota
3. Contact your IT team if you're on a managed Workspace account

### Corporate Workspace Restrictions

Some organizations restrict OAuth access for third-party apps:

1. Check with your IT admin if OAuth is allowed
2. They may need to whitelist the google-workspace-mcp client ID
3. Alternative: Use a personal Gmail account for now

---

## Reconfiguration

If the user runs `/google-workspace-setup` when already configured:

1. Check current status via a test query
2. Show current config from `System/integrations/config.yaml`
3. Offer options:
   - Update watched labels
   - Change write preferences (auto-draft vs ask each time)
   - Re-authenticate (if token expired)
   - Disconnect Gmail

### Disconnect Flow

If user wants to disconnect:

1. Update `System/integrations/config.yaml`:
   ```yaml
   google-workspace:
     enabled: false
   ```
2. Confirm: "Google Workspace is disconnected. Your daily plans, meeting prep, and reviews will no longer include email context. Run `/google-workspace-setup` anytime to reconnect."
