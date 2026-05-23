---
name: inboxzero
description: "Autonomous email triage powered by AI. Connects to any email provider via IMAP, auto-labels, archives, drafts replies, and surfaces only what matters. Use when: drowning in email, want smart filtering beyond Gmail filters, or need automated triage. NOT for: sending bulk email, newsletter management, or email marketing campaigns."
homepage: https://pawhub.ai/inboxzero
metadata:
  {
    "openpaw":
      {
        "emoji": "📬",
        "requires": { "bins": ["node"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "node",
              "package": "@pawhub/inboxzero",
              "bins": ["inboxzero"],
              "label": "Install InboxZero (npm)",
            },
          ],
      },
  }
---

# InboxZero 📬

Autonomous email triage that actually works. Connect any email account (Gmail, Outlook, IMAP), set your rules in plain language, and let Paw handle the noise.

## When to Use

✅ **USE this skill when:**

- Getting 100+ emails a day and drowning
- Want newsletters auto-archived but accessible
- Need email sorted by urgency/importance
- Want draft replies written while you sleep
- Trying to maintain actual inbox zero
- Need better filtering than Gmail's basic rules
- Want email handled autonomously (not just filtered)
- Managing multiple email accounts

## When NOT to Use

❌ **DON'T use this skill when:**

- Sending bulk email / newsletters → use Mailchimp, SendGrid, etc.
- Email marketing campaigns → use dedicated ESP
- Transactional email generation → use platform APIs
- Email deliverability testing → use specialized tools
- Building email lists → use proper CRM tools
- Legal/compliance email archiving → use enterprise solutions

## Setup

Install InboxZero:

```bash
npm install -g @pawhub/inboxzero
```

Connect your email account:

```bash
# Gmail (via IMAP)
inboxzero add gmail \
  --email your.email@gmail.com \
  --app-password your-app-password

# Outlook / Office 365
inboxzero add outlook \
  --email your.email@outlook.com \
  --password your-password

# Generic IMAP
inboxzero add imap \
  --email you@example.com \
  --host imap.example.com \
  --port 993 \
  --user you@example.com \
  --password your-password

# Verify connection
inboxzero status
```

## Example Interactions

### Initial Setup

**You:** Set up email triage for me

**Paw:** *settles in for configuration*

Alright, let's make email bearable again. First question:

**What email account should I watch?**

---

**You:** my.work.email@company.com (Gmail)

**Paw:** Got it. Gmail IMAP. You'll need an app password (not your regular password).

[Generate one here](https://myaccount.google.com/apppasswords)

Once you have it, run:
```bash
inboxzero add gmail --email my.work.email@company.com --app-password YOUR_APP_PASSWORD
```

Then come back and we'll set up your triage rules. ✉️

---

**You:** Done. Now what?

**Paw:** *stretches and opens the rule configurator*

Perfect. Now let's teach me how to handle your inbox.

**Quick setup or custom rules?**

Quick setup = I make smart guesses based on patterns
Custom rules = you tell me exactly what to do

Most people start with quick setup, then tweak later. What sounds good?

---

**You:** Quick setup

**Paw:** *starts analyzing your inbox*

Scanning your last 500 emails to learn patterns...

*30 seconds later*

Okay, here's what I found:

**Newsletters (42% of volume):**
- Substack digests
- Marketing emails from vendors
- Automated reports

**Action needed (18%):**
- Client requests
- Meeting invitations
- PR reviews
- Calendar items

**FYI / CC'd (31%):**
- Group threads where you're CC'd
- Status updates
- Announcements

**Social (9%):**
- LinkedIn notifications
- Twitter alerts
- GitHub notifications

**Proposed rules:**
1. Archive newsletters (but keep searchable)
2. Priority flag: client emails, PRs, meeting invites
3. Auto-label FYI emails (don't clutter inbox)
4. Snooze social notifications until evening batch

Sound good? (yes/no/customize)

---

**You:** Yes, but don't archive newsletters — I actually read some

**Paw:** *nods in approval*

Smart. Newsletters modified:
- Label as "Newsletter" ✅
- Leave in inbox ✅
- Mark as read after 3 days if unopened ✅

Everything else approved. Activating triage rules now...

**Status:**
- ✅ Connected to IMAP
- ✅ Rules active
- ✅ Processing backlog (500 emails)
- ⏳ Will check every 5 minutes

You'll get a summary of actions taken. Check back in 10 minutes. 🐾

---

### Daily Usage

**You:** What did you do to my email overnight?

**Paw:** *reports with satisfaction*

**InboxZero Summary (Last 12 Hours)**

📬 **Processed:** 87 emails

**Actions taken:**
- 🗃️ Archived 42 emails (newsletters, FYI)
- 🏷️ Labeled 19 emails (categorized)
- ⭐ Flagged 8 as priority (need your attention)
- 💤 Snoozed 12 until tomorrow
- ✍️ Drafted 6 replies (ready for your review)

**Current inbox:** 8 emails (all priority)

**Your move:**
1. Check the 8 flagged items
2. Review drafted replies (or let me send them)
3. Relax — everything else is handled

Want details on any category? 📊

---

**You:** Show me the drafted replies

**Paw:** *pulls up the drafts*

**Drafted Replies (6):**

**1. From: sarah@client.com**
Subject: "Q4 timeline check-in"

*Draft:*
> Hi Sarah,
>
> Timeline is on track. We're finishing QA this week, deployment scheduled for Oct 15.
>
> I'll send the staging link by EOD Thursday for your team to preview.
>
> Best,
> [Your name]

✅ Send now | ✏️ Edit | 🗑️ Delete draft

---

**2. From: vendor-support@tool.com**
Subject: "Account renewal reminder"

*Draft:*
> Hi,
>
> Thanks for the reminder. I'll review this with the team and get back to you by end of week.

✅ Send | ✏️ Edit | 🗑️ Delete

---

**Want to review all 6 or should I just send them?** (Drafts are conservative — I only auto-send if you enable "confident mode")

---

**You:** Send 1, 2, 3, 5. Hold 4 and 6 for me to review.

**Paw:** *clicks send on the approved emails*

✅ Sent 4 emails
📝 Holding 2 drafts for your review (marked in your Drafts folder)

Anything else? Or should I go back to monitoring your inbox quietly? 😺

---

### Advanced Triage

**You:** Create a rule: if John from engineering emails me with "urgent" in the subject, text me immediately

**Paw:** Got it. Adding VIP rule:

```
Trigger: Email from john@company.com
Condition: Subject contains "urgent"
Action: Send Telegram notification immediately
Priority: High
```

Testing... *sends test notification*

Did you get the test ping? (yes/no)

---

**You:** Yes

**Paw:** Perfect. Rule is live. John's urgent emails now bypass the queue and ping you directly.

**Pro tip:** If John sends too many "urgent" emails that aren't actually urgent, I'll learn that and downgrade the priority automatically after 3 false alarms. 🎯

---

### Weekly Cleanup

**You:** How's my email hygiene this week?

**Paw:** *pulls weekly report*

**InboxZero Weekly Report**

📬 **Processed:** 412 emails

**Breakdown:**
- Priority handled: 34 (8%)
- Auto-archived: 287 (70%)
- Labeled for later: 61 (15%)
- Snoozed: 30 (7%)

**Time saved:** ~4.2 hours
(Avg 6 mins per priority email × 42 emails handled autonomously)

**Inbox status:**
- Start of week: 127 unread
- End of week: 4 unread
- Current state: Inbox Zero ✅

**Top senders:**
1. newsletters@substack.com — 87 emails (auto-archived)
2. github.com — 52 notifications (labeled)
3. sarah@client.com — 14 emails (8 handled, 6 flagged)

**Recommendations:**
- Unsubscribe from "MarketingTool Weekly" (12 emails, 0 opens)
- Create filter for "deploy success" notifications (GitHub)
- Consider VIP rule for sarah@client.com (high reply rate)

Want me to make these changes? 🐾

## Commands

### Account Management

```bash
# Add email account
inboxzero add gmail --email you@gmail.com --app-password ABC123

# List connected accounts
inboxzero accounts list

# Remove account
inboxzero accounts remove you@gmail.com

# Test connection
inboxzero accounts test you@gmail.com
```

### Triage Rules

```bash
# Quick setup (AI learns patterns)
inboxzero setup quick --account you@gmail.com

# Create custom rule
inboxzero rule create \
  --from "newsletter@example.com" \
  --action archive \
  --label "Newsletter"

# List active rules
inboxzero rule list

# Disable a rule temporarily
inboxzero rule disable <rule-id>

# Edit existing rule
inboxzero rule edit <rule-id>
```

### Manual Actions

```bash
# Process inbox now (don't wait for schedule)
inboxzero process --account you@gmail.com

# Generate reply draft for specific email
inboxzero draft-reply --email-id ABC123

# Bulk archive by sender
inboxzero bulk-archive --from "sender@example.com" --older-than 30d

# Unsubscribe helper (finds unsubscribe links)
inboxzero unsubscribe --from "sender@example.com"
```

### Reports

```bash
# Daily summary
inboxzero report daily

# Weekly digest
inboxzero report weekly

# Show inbox statistics
inboxzero stats

# Email hygiene score
inboxzero score
```

### Smart Features

```bash
# Enable draft replies
inboxzero config set draft-replies true

# Enable confident mode (auto-send safe replies)
inboxzero config set confident-mode false

# Set Telegram notifications
inboxzero config set telegram-notify true

# VIP sender (always notify)
inboxzero vip add sarah@client.com
```

## Rule Syntax

### Simple Rules

```bash
# Archive all newsletters
inboxzero rule create --subject-contains "newsletter" --action archive

# Flag client emails as priority
inboxzero rule create --from "@client.com" --action flag --priority high

# Auto-label GitHub notifications
inboxzero rule create --from "notifications@github.com" --action label --label "GitHub"
```

### Advanced Rules

```bash
# Combine conditions
inboxzero rule create \
  --from "boss@company.com" \
  --subject-contains "urgent" \
  --action notify-telegram \
  --priority critical

# Time-based snoozing
inboxzero rule create \
  --from "@social-network.com" \
  --action snooze \
  --until "18:00" \
  --label "Social"

# Draft reply with template
inboxzero rule create \
  --from "vendor@example.com" \
  --subject-contains "renewal" \
  --action draft-reply \
  --template "vendor-renewal"
```

## Draft Reply Templates

Create custom templates for common replies:

```bash
# Create template
inboxzero template create vendor-renewal "
Thanks for the reminder. I'll review this with the team and get back to you by end of week.

Best,
{sender_name}
"

# Use template in rule
inboxzero rule create \
  --from "@vendor.com" \
  --action draft-reply \
  --template vendor-renewal
```

## Telegram Integration

Once connected to OpenPaw + Telegram:

**Paw:** 📬 **3 new priority emails**
1. sarah@client.com: "Q4 timeline check-in"
2. john@eng: "Prod issue - need review"
3. security@company: "2FA reminder"

Reply with:
`/email 2` to read
`/email draft 1` to draft reply
`/email done` to mark handled

---

**You:** `/email 2`

**Paw:** *sends full email content*

```
From: john@engineering.com
Subject: Prod issue - need review
Time: 2:14 PM

Hey, seeing elevated error rates on /api/users endpoint.
Can you take a look? Nothing critical yet but trending up.

Logs: [link]
```

Quick actions:
`/email reply 2` - Draft reply
`/email done 2` - Mark handled
`/email forward 2 @sarah` - Forward to someone

## Configuration

```bash
# Show current config
inboxzero config show

# Processing frequency
inboxzero config set check-interval "5m"

# Max emails to process per run
inboxzero config set batch-size 50

# Draft reply tone
inboxzero config set reply-tone "professional" # casual, professional, brief

# Auto-send confidence threshold
inboxzero config set auto-send-confidence 0.95

# Enable learning mode (improves over time)
inboxzero config set learning-mode true
```

## Learning Mode

InboxZero gets smarter over time:

- Learns which emails you actually read
- Adjusts priority based on your reply patterns
- Improves draft quality by learning your writing style
- Suggests new rules based on recurring patterns

```bash
# View learning insights
inboxzero insights

# Example output:
# - You never open emails from "newsletter@example.com" → Suggest: auto-archive
# - You always reply to sarah@client.com within 2 hours → Suggest: VIP rule
# - Emails with "invoice" in subject get forwarded to accounting → Suggest: auto-forward rule
```

## Tips from Paw

> "Start with quick setup, let me learn for a week, then refine the rules. Don't over-engineer on day one."

> "Draft mode is safer than confident mode. I'll write replies but you hit send. Confident mode is for when you trust me blindly (rare)."

> "The VIP list is powerful. Use it for people where you need instant notifications, not just priority flagging."

> "Check the weekly report. It'll show you patterns you didn't know existed. Then unsubscribe ruthlessly."

> "I never delete emails. Everything is archived, labeled, and searchable. Inbox Zero ≠ Email Deletion."

## Pricing

- **Free tier:** 1 email account, 100 emails/day, basic rules
- **Pro:** $12/month — 3 accounts, unlimited emails, draft replies, learning mode
- **Team:** $39/month — 10 accounts, shared rules, team insights, Slack integration

Install from PawHub or [pawhub.ai/inboxzero](https://pawhub.ai/inboxzero)

## Security & Privacy

- Your email credentials are encrypted at rest using AES-256
- Email content is processed locally on your OpenPaw gateway
- Draft replies are generated via Claude API (opt-in)
- No email content is stored permanently; everything is ephemeral processing
- You can disable cloud AI and use local models for draft generation
- Full audit log of all actions taken on your behalf

## Notes

- IMAP is read-only until you enable "confident mode" (write actions)
- Draft replies use Claude Sonnet by default; configurable to Haiku or local models
- Processing runs every 5 minutes by default; adjustable down to 1 minute
- Supports Gmail, Outlook, FastMail, ProtonMail (via bridge), and any IMAP provider
- Works with multiple email accounts simultaneously
- No message limits on Pro tier (unlike Gmail filters which max out)

---

Built for people who want their inbox managed, not just filtered. 📬🐾
