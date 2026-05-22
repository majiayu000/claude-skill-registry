---
name: cold-email-outreach
description: >
  End-to-end cold email outreach orchestration. Handles goal alignment, lead
  selection from Supabase, sequence design, email generation (via email-drafting),
  campaign setup in the user's chosen outreach tool, and logging. Tool-agnostic —
  supports Smartlead (default), Instantly, Lemlist, Apollo, or manual CSV export.
tags: [outreach]
---

# Cold Email Outreach

The final mile of the outbound pipeline. Takes qualified leads from Supabase, builds email sequences using the `email-drafting` skill, loads campaigns into the user's chosen outreach tool, and logs everything back to Supabase.

**Tool-agnostic:** Asks the user which outreach platform they use. Defaults to Smartlead if they have MCP tools configured. Falls back to CSV export for any other tool or manual workflow.

## When to Auto-Load

Load this skill when:
- User says "launch a campaign", "send outreach", "email these leads", "set up cold email"
- An upstream skill connects with "create email campaign" or "passes: supabase-eligible-leads"
- User completes `lead-qualification` and wants to act on the results

## Supported Outreach Tools

This skill does NOT assume a specific tool. It asks first, then adapts.

| Tool | Integration | How It Works |
|------|------------|--------------|
| **Smartlead** (default) | MCP tools (`mcp__smartlead__*`) | Full automation: create campaign, add sequences, import leads, configure schedule, launch |
| **Instantly** | CSV import | Generate CSV matching Instantly's import format, user uploads manually |
| **Lemlist** | CSV import | Generate CSV with Lemlist-compatible columns |
| **Apollo** | CSV import | Generate CSV matching Apollo sequence import format |
| **Manual / Other** | CSV + instructions | Export leads + emails as generic CSV, provide setup instructions |

**Tool selection logic:**
1. Ask user in Phase 0: "Which outreach tool do you use?"
2. If **Smartlead** → use MCP tools for full automation
3. If **Instantly / Lemlist / Apollo** → generate tool-specific import CSV
4. If **Other or unknown** → generate generic CSV (`email`, `first_name`, `last_name`, `company`, `title`, `subject`, `body` per touch) and ask user for their tool's import requirements

## Prerequisites

### Supabase

People must be stored in Supabase with the schema from `tools/supabase/schema.sql`. The `people` and `outreach_log` tables must exist. Run `python3 tools/supabase/setup_database.py` if setting up fresh.

Environment variables in `.env`:
```
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJ...
```

### Outreach Tool

- **Smartlead:** MCP tools available via `mcp__smartlead__*`. No additional setup.
- **All others:** Just need CSV export — no API keys required.

## Phase 0: Intake

Ask all questions at once. Organize by category. Skip any already answered by an upstream skill.

### Campaign Goal
1. What's the objective? (book meetings, drive demo requests, get replies, nurture)
2. What's the outreach angle or hook? (hiring signal, competitor displacement, event-based, pain-based, cold database)
3. What should we name this campaign?

### Outreach Tool
4. Which outreach tool do you use? (Smartlead / Instantly / Lemlist / Apollo / Other / Just give me a CSV)

### Lead Selection
5. Which leads should we target? Options:
   - All leads for a specific `client_name`
   - Specific `icp_segment`
   - Title patterns (e.g., "VP Operations", "Director of Sales")
   - Industry or location filters
   - `qualification_score` above a threshold
   - Specific `source` (crustdata, apollo, linkedin, etc.)
   - Custom filter (describe what you want)
6. Any exclusions? (specific companies, recently contacted leads, certain titles)
7. Max campaign size? (default: 200)

### Sequence Design
8. How many touches? (default: 3)
9. Timing between touches? (default: Day 1 / Day 5 / Day 12)
10. Personalization tier? (Tier 1: merge fields only / Tier 2: segment-specific / Tier 3: unique per lead)

### Sending Config (skip if CSV export)
11. Which email accounts should send? (list accounts or "use all available")
12. Sending schedule? (default: Mon-Fri 8am-5pm in recipient's timezone)
13. Daily send limit per account? (default: 30/day)
14. Track opens and clicks? (default: opens yes, clicks no)

## Phase 1: Lead Selection from Supabase

### Connect

Use the shared Supabase client:

```python
import sys, os
sys.path.insert(0, os.path.join("tools", "supabase"))
from supabase_client import SupabaseClient

client = SupabaseClient(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_ROLE_KEY"])
```

### Build Filters

Map user criteria to PostgREST query parameters on the `people` table:

| User Says | PostgREST Filter |
|-----------|-----------------|
| "VP Operations" | `title=ilike.*VP Operations*` |
| Client "happy-robot" | `client_name=eq.happy-robot` |
| Score > 7 | `qualification_score=gte.7` |
| Has verified email | `email_verified=eq.true` |
| Industry "logistics" | `industry=ilike.*logistics*` |
| Location "San Francisco" | `location=ilike.*San Francisco*` |
| Source "crustdata" | `source=eq.crustdata` |
| Not contacted in 84 days | `or=(last_contacted.is.null,last_contacted.lt.{84_days_ago})` |

### Cooldown Filter (Mandatory)

**Always** exclude people contacted within 84 days (12 weeks). This is not optional.

Use the shared client's `check_cooldown()` method:
```python
in_cooldown = client.check_cooldown(client_name="happy-robot", cooldown_days=84)
# Returns set of person_id strings still in cooldown
```

Or query directly:
1. Query `outreach_log` for `person_id`s with `sent_date` in the last 84 days:
   ```
   GET /rest/v1/outreach_log?select=person_id&sent_date=gte.{84_days_ago}&status=neq.bounced&client_name=eq.{client}
   ```
2. Collect those `person_id`s into an exclusion set
3. Add `id=not.in.({excluded_ids})` to the people query

### Present & Confirm

Show a sample table (10-15 leads) with:
- Name, Title, Company, Industry, Score, Email, Last Contacted

Tell user: total eligible leads, how many excluded by cooldown, how many have verified emails.

Ask user to confirm or adjust filters before proceeding.

## Phase 2: Sequence Design

Present the sequence plan as a table before writing any copy:

| Touch | Day | Email Type | Framework | CTA |
|-------|-----|-----------|-----------|-----|
| 1 | 1 | Cold intro | Signal-Proof-Ask | 15-min call |
| 2 | 5 | New angle / asset | PAS | Resource offer |
| 3 | 12 | Social proof | BAB | Open to chat? |

Get user approval on the structure before generating copy in Phase 3.

## Phase 3: Email Generation

Load the `email-drafting` skill and pass it:
- Campaign context (goal, angle, product, proof points)
- Sequence structure from Phase 2
- 3-5 sample leads from the selected list
- Personalization tier
- Tone preference

### By Personalization Tier

**Tier 1 (Generic):** Generate one template per touch with merge fields (`{first_name}`, `{company}`, `{title}`). Same template for all leads.

**Tier 2 (Segment):** Generate one template per segment per touch. Segments are defined by role, industry, or signal type. Swap pain points and proof points between segments.

**Tier 3 (Deep):** Generate unique email per lead per touch. Cap at 50 leads — recommend Tier 2 above that volume.

### Review Loop

1. Generate sample emails for 3-5 leads first
2. Present to user for review
3. Iterate until approved (max 3 rounds)
4. Generate remaining emails after approval

## Phase 4: Campaign Setup

### If Smartlead (MCP Automation)

Full automation via MCP tools. Execute in this order:

**Step 1: List email accounts**
```
mcp__smartlead__get_email_accounts
```
Present available accounts. User selects which to use.

**Step 2: Create campaign**
```
mcp__smartlead__create_campaign
  name: {campaign_name}
```
Save the returned `campaign_id`.

**Step 3: Add sequence steps**
```
mcp__smartlead__save_campaign_sequences
  campaign_id: {campaign_id}
  sequences: [
    { seq_number: 1, subject: "...", email_body: "...", seq_delay_details: { delay_in_days: 0 } },
    { seq_number: 2, subject: "...", email_body: "...", seq_delay_details: { delay_in_days: 4 } },
    { seq_number: 3, subject: "...", email_body: "...", seq_delay_details: { delay_in_days: 7 } }
  ]
```

**Merge variable mapping:** Convert `{first_name}` → `{{first_name}}`, `{company}` → `{{company}}` (Smartlead uses double-brace syntax).

**Step 4: Import leads (batch 100)**
```
mcp__smartlead__add_leads_to_campaign
  campaign_id: {campaign_id}
  lead_list: [{ email: "...", first_name: "...", last_name: "...", company_name: "...", ... }]
```
Batch in groups of 100 if more than 100 leads.

**Step 5: Assign sending accounts**
```
mcp__smartlead__add_email_accounts_to_campaign
  campaign_id: {campaign_id}
  email_account_ids: [...]
```

**Step 6: Set schedule**
```
mcp__smartlead__update_campaign_schedule
  campaign_id: {campaign_id}
  schedule: { ... }
```

**Step 7: Configure settings**
```
mcp__smartlead__update_campaign_settings
  campaign_id: {campaign_id}
  settings: { track_opens: true, track_clicks: false, stop_on_reply: true }
```

### If CSV-Based Tool (Instantly, Lemlist, Apollo, Other)

**Step 1: Generate CSV**

Columns depend on personalization tier:

**Tier 1 (same template for all):**
- CSV columns: `email`, `first_name`, `last_name`, `company`, `title`, `custom_field_1` (signal/hook)
- Separate file with sequence templates (subjects + bodies with merge fields)

**Tier 2/3 (per-segment or per-lead emails):**
- CSV columns: `email`, `first_name`, `last_name`, `company`, `title`, `touch_1_subject`, `touch_1_body`, `touch_2_subject`, `touch_2_body`, `touch_3_subject`, `touch_3_body`

**Step 2: Save file**
```
skills/cold-email-outreach/output/{campaign-name}-{YYYY-MM-DD}.csv
```

**Step 3: Provide tool-specific import instructions**

**Instantly:**
- Upload CSV → Sequences → Create new sequence
- Map columns: Email → email, First Name → first_name, etc.
- Paste sequence templates into each step
- Set delays between steps

**Lemlist:**
- People → Import → Upload CSV
- Map custom variables to columns
- Create campaign → add email steps → insert variables

**Apollo:**
- Sequences → Create Sequence → add email steps
- Contacts → Import → Upload CSV
- Add imported contacts to sequence

**Other / Manual:**
- Provide the CSV path and explain the column structure
- Ask user what format their tool expects, adjust if needed

## Phase 5: Review & Launch

Present campaign summary:

```
Campaign: {name}
Leads: {count}
Sequence: {touches} touches over {days} days
Sending: {accounts} accounts × {daily_limit}/day = {daily_volume} emails/day
Estimated completion: {date}
Tool: {smartlead/instantly/etc.}
```

### Hard Approval Gate

**Do NOT activate the campaign without explicit user confirmation.** Present the summary, then ask: "Ready to launch? Type 'yes' to activate."

- **Smartlead:** `mcp__smartlead__update_campaign_status` → set to active
- **CSV tools:** Tell user the file is ready for import, provide the file path

## Phase 6: Tracking & Logging

### Database Write Policy

**All database writes in this phase require the user's prior approval from the launch gate in Phase 5.** The Phase 5 approval ("Ready to launch?") covers both the campaign activation AND the subsequent logging. However, if the campaign was exported as CSV (not launched via Smartlead), confirm with the user before logging — they may not have actually imported/sent yet.

### Log to Supabase

After launch (or export), insert records into `outreach_log`:

```
POST /rest/v1/outreach_log
Prefer: return=minimal

[
  {
    "person_id": "{person_uuid}",
    "campaign_name": "{campaign_name}",
    "external_campaign_id": "{smartlead_campaign_id or null}",
    "channel": "email",
    "tool": "{smartlead/instantly/lemlist/apollo/manual}",
    "sent_date": "{ISO timestamp}",
    "status": "sent",
    "client_name": "{client_name}"
  },
  ...
]
```

Or use the shared client:
```python
client.log_outreach(entries)
```

**For CSV-based tools:** Log with `status` = `"exported"`. It changes to `"sent"` when user confirms they launched the campaign in their tool.

### Update People Records

Update `last_contacted` on the people table for all people in this campaign:

```
PATCH /rest/v1/people?id=in.({person_ids})
{ "last_contacted": "{ISO timestamp}" }
```

### Present Summary

```
{count} people logged to outreach_log
last_contacted updated for {count} people
Campaign ID: {id}
Cooldown active until: {date + 84 days}
Next eligible re-contact: {date}
```

## Cooldown Enforcement Rules

Reference section for cooldown logic used throughout this skill.

| Rule | Detail |
|------|--------|
| **Default cooldown** | 84 days (12 weeks) from `sent_date` |
| **Bounced leads** | Exempt from cooldown — email never reached them. Filter: `status=neq.bounced` when checking cooldown |
| **Active campaign leads** | Always ineligible — if a lead is in an active campaign (status = "sent", no reply/bounce), they cannot be added to another campaign |
| **User override** | User can explicitly override cooldown for specific leads — ask for confirmation before allowing |
| **Null last_contacted** | Leads never contacted are always eligible |

## Output Directory

Campaign exports are saved to:
```
skills/cold-email-outreach/output/
```

Create this directory if it doesn't exist. Files are named `{campaign-name}-{YYYY-MM-DD}.csv`.
