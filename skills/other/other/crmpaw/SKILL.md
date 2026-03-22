---
name: crmpaw
description: "Lightweight CRM inside your messaging app. Track conversations, set follow-ups, take notes, and manage relationships via Telegram. Use when: managing client relationships, tracking sales pipeline, or organizing networking contacts. NOT for: enterprise CRM (Salesforce replacement), marketing automation, or complex sales processes."
homepage: https://pawhub.ai/crmpaw
metadata:
  {
    "openpaw":
      {
        "emoji": "📋",
        "requires": { "bins": ["sqlite3"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "node",
              "package": "@pawhub/crmpaw",
              "bins": ["crmpaw"],
              "label": "Install CRMPaw (npm)",
            },
          ],
      },
  }
---

# CRMPaw 📋

Your CRM lives in Telegram. Track clients, set reminders, take notes, manage pipeline. Zero context switching. Maximum retention.

## When to Use

✅ **USE when:**

- Managing freelance clients
- Tracking sales conversations
- Organizing networking contacts
- Setting follow-up reminders
- Taking meeting notes
- Small business client management
- Consultant relationship tracking

## When NOT to Use

❌ **DON'T use when:**

- Enterprise sales teams → use Salesforce, HubSpot
- Complex deal workflows → need dedicated CRM
- Marketing automation → use dedicated tools
- Large teams (>10 people) → collaboration limits

## Example Interactions

**You:** Add client: Sarah Chen, sarah@startup.com, interested in Pro plan

**Paw:** ✅ **Client added:** Sarah Chen

**Details:**
- Email: sarah@startup.com
- Status: Lead
- Interest: Pro plan
- Added: Today

**Next steps:**
- Set follow-up reminder?
- Add notes from conversation?
- Move to pipeline stage?

What do you want to do? 📋

---

**You:** Set follow-up for Friday, send pricing

**Paw:** ✅ **Follow-up scheduled**

**Client:** Sarah Chen
**When:** Friday, 10 AM
**Action:** Send Pro plan pricing

**I'll remind you:**
- Friday morning (full reminder)
- Thursday evening (heads up)

**Want me to draft the pricing email now?** (I can save it for Friday)

---

**You:** Yes

**Paw:** *drafts email*

**Email draft saved:**

**To:** sarah@startup.com
**Subject:** Pro Plan Pricing — [Your Company]

---

Hi Sarah,

Great chatting with you yesterday about the Pro plan.

Here's the pricing breakdown:

**Pro Plan: $99/month**
- Feature 1
- Feature 2
- Feature 3
- Priority support

**Annual option:** $950/year (save $238)

Want to jump on a quick call to walk through the features? I'm free [your availability here].

Best,
[Your name]

---

**Status:** Draft saved, will remind you Friday to send.

Edit now or wait until Friday? ✉️

---

**Friday morning:**

**Paw:** 📅 **Reminder: Follow up with Sarah Chen**

**Task:** Send Pro plan pricing
**Client:** sarah@startup.com
**Context:** Interested in Pro plan, spoke Tuesday

**Draft email ready:**
[Shows email preview]

**Quick actions:**
- `/crm send` (send draft now)
- `/crm edit` (modify before sending)
- `/crm snooze 1d` (remind me tomorrow)
- `/crm done` (mark completed, no email)

What do you want to do? 🎯

---

**You:** `/crm send`

**Paw:** ✅ **Email sent** to sarah@startup.com

**Status updated:**
- Sarah Chen → "In negotiation"
- Last contact: Today
- Next action: Wait for response

**I'll track this:**
- If no response in 3 days, I'll remind you to follow up
- If she replies, I'll log it automatically

Want to add notes from your last conversation? 📝

---

**You:** Yes. Notes: She's comparing us to CompetitorX. Budget approved but needs to convince technical lead. Timeline: wants to decide by end of month.

**Paw:** ✅ **Notes saved**

**Client:** Sarah Chen
**Notes added:**
- Comparing vs CompetitorX
- Budget: ✅ approved
- Blocker: Technical lead buy-in needed
- Timeline: Decision by end of month

**Smart suggestions:**
- Schedule demo for technical lead?
- Send technical comparison doc?
- Set reminder for end-of-month check-in?

Want me to do any of these? 🎯

---

**Pipeline view:**

**You:** Show pipeline

**Paw:** **Your Pipeline:**

**🌱 Leads (3):**
- Alex Johnson (product interest)
- Mike Torres (cold outreach)
- Lisa Park (referral)

**💬 In Negotiation (2):**
- Sarah Chen (Pro plan, $99/mo)
- David Kim (Enterprise, $499/mo)

**✅ Won (5):**
- [Recent wins...]

**❌ Lost (2):**
- [Recent losses...]

**Pipeline value:** $3,576/mo potential MRR

**This month:**
- Deals won: 2 ($1,188/mo)
- Deals lost: 1
- Win rate: 67%

**Action items:**
- Sarah Chen: waiting for reply (sent Friday)
- David Kim: demo scheduled tomorrow
- Alex Johnson: follow up overdue (3 days)

Want details on any of these? 📊

---

**You:** Show Alex Johnson

**Paw:** **Client:** Alex Johnson

**Status:** Lead (3 days since last contact ⚠️)
**Email:** alex@company.com
**Phone:** (555) 123-4567
**Interest:** Pro plan

**Timeline:**
- Mar 18: Added (cold outreach)
- Mar 19: Sent intro email
- Mar 20: No response
- Mar 21: Follow-up sent
- Mar 22: Still no response

**Notes:**
- Works at TechCorp
- Saw our Product Hunt launch
- Interested in API access

**Recommended action:** One more follow-up, then mark as inactive.

Want me to draft the follow-up? ✍️

## Commands

```bash
# Add client
crmpaw add "Name" --email "email@example.com" --status lead

# Set follow-up
crmpaw remind "Name" --when "Friday 10am" --action "Send pricing"

# Add notes
crmpaw note "Name" "Notes here"

# Update status
crmpaw status "Name" --stage negotiation

# Show pipeline
crmpaw pipeline

# Search clients
crmpaw search "keyword"

# Show client details
crmpaw show "Name"

# Export data
crmpaw export --format csv
```

## Telegram Integration

**Quick add:**

**You:** `/crm add Sarah Chen sarah@startup.com Pro plan`

**Paw:** ✅ Added. Set follow-up? (Reply "Friday" or "3 days")

---

**Pipeline:**

**You:** `/crm pipeline`

**Paw:** 
🌱 Leads: 3
💬 Negotiating: 2
✅ Won: 5

React for details or `/crm show Name` for specific client.

---

**Daily digest:**

**Paw:** ☀️ **CRM Daily Digest**

**Today's actions:**
- 📅 Follow up: Sarah Chen (send pricing)
- 📞 Demo: David Kim at 2 PM

**Overdue:**
- Alex Johnson (3 days, no response)

**This week:**
- New leads: 2
- Deals closed: 1 ($99/mo)
- Pipeline: $3,576/mo

Have a productive day! 📋🐾

## Features

### Auto-tracking

- Email replies logged automatically
- Meeting notes captured from calendar
- Follow-ups suggested based on patterns
- Pipeline stages updated smartly

### Smart Reminders

- Overdue follow-ups flagged
- Dead leads identified (no response >14 days)
- Hot leads highlighted (high engagement)
- Win probability calculated

### Integrations

```bash
# Connect email
crmpaw connect email --provider gmail

# Connect calendar
crmpaw connect calendar --provider google

# Connect Telegram
crmpaw connect telegram

# Sync contacts
crmpaw sync contacts
```

## Configuration

```bash
# Set default follow-up delay
crmpaw config set default-follow-up 3d

# Configure pipeline stages
crmpaw config stages "Lead,Negotiation,Won,Lost"

# Set reminder times
crmpaw config reminders 10:00 # daily at 10 AM

# Auto-archive old leads
crmpaw config auto-archive 30d # no activity for 30 days
```

## Pricing

- **Free tier:** 25 contacts, basic CRM
- **Pro:** $15/month — unlimited contacts, email integration, analytics

Install: [pawhub.ai/crmpaw](https://pawhub.ai/crmpaw)

---

Stop losing deals because you forgot to follow up. 📋🐾
