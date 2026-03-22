---
name: amplemarket-org-chart
description: >
  Build a visual, interactive org chart for any target account using Amplemarket and HubSpot MCP data. Combines contact discovery, enrichment, outreach history, CRM deal context, and relationship signals into a single React-based visual. Use this skill whenever the user asks to map an org structure, visualize contacts at a company, understand outreach status across an account, build a stakeholder map, do account-based research, cross-reference with CRM, see account penetration with CRM data, or map a specific team. Trigger phrases include: "show me the org chart for [company]", "who do we know at [company]", "map the buying committee", "show me outreach status for [account]", "pull all contacts at [domain]", "account map", "stakeholder map", "account penetration", "engineering org chart for [company]", "map the product team at [company]", "deal context for [account]".
metadata:
  author: amplemarket
  version: "1.0.0"
  category: "Account Intelligence"
compatibility: Requires Amplemarket MCP server
---

# Amplemarket Account Org Chart Builder

Build an interactive, color-coded org chart for a target account that shows every contact, their outreach status, communication history, CRM deal context, and relationship signals -- all in a single visual.

## When to Use

- User wants to see who they know at a company
- User wants to map a buying committee or account org structure
- User asks about outreach status across an account
- User wants a stakeholder map before a meeting or deal review
- User wants to map a specific department or team (e.g., "engineering org chart", "map the product team")
- User wants to cross-reference account contacts with HubSpot CRM data
- User says "org chart", "account map", "who do we know at X", "map [company]"

## Prerequisites

The user must have the **Amplemarket MCP** connector enabled. If the tools aren't available, tell the user to enable the Amplemarket integration in their Claude settings.

**HubSpot MCP** is optional but recommended -- it enables CRM cross-referencing (deal context, lifecycle stage, ownership). If HubSpot tools aren't available, skip CRM steps and note it in the summary.

## Workflow

Follow these steps in order. Each step maps to specific MCP tools.

### Step 1: Identify the Account

Ask the user for a **company name or domain**. Then:

1. Call `Amplemarket:list_accounts` with `name` or `domain` to find the account in Amplemarket.
2. If found, call `Amplemarket:get_account` with the account ID to get account details, engagement stats, CRM data, tags, and AI insights.
3. Call `Amplemarket:enrich_company` with the domain to get firmographic data (industry, size, HQ, funding, tech stack).

**If the account isn't found**: Try `Amplemarket:search_companies` as a fallback. If that also returns nothing, fall back to `Amplemarket:enrich_company` with the domain to bootstrap firmographic data, then proceed with `search_people` only. Tell the user: "This account isn't tracked in Amplemarket yet, but I can still map contacts found in our database."

### Step 2: Scope the Search

Before pulling contacts, ask the user which departments or functions to focus on. Tailor the question based on company size (from Step 1 firmographics):

- **Small company (<200 employees)**: "I'll pull everyone -- should be manageable."
- **Medium company (200-2,000 employees)**: "Want me to focus on specific departments (e.g., Engineering, Sales, Marketing) or pull all?"
- **Large company (2,000+ employees)**: "This is a large company -- I'll need to focus. Which departments and seniority levels matter most?"

Use the answer to set `job_functions` and `person_seniorities` filters for the contact search in Step 3.

### Step 3: Discover Contacts

Pull contacts from multiple angles to maximize coverage, applying department/seniority filters from Step 2:

1. **Search by company domain**: Call `Amplemarket:search_people` with `company_domains: [domain]`, the scoped filters, and `full_output: true`. Start with `page_size: 50`. Paginate if needed.
2. **Search by seniority tiers** (if the first search returns too many results, or to ensure leadership coverage): Run separate searches filtering by `person_seniorities`:
   - `["C-Suite", "Founder", "Owner", "Partner"]`
   - `["VP", "Head", "Director"]`
   - `["Manager", "Senior"]`
3. **Check known contacts**: If the account data from Step 1 includes email addresses, call `Amplemarket:get_contacts` to pull their Amplemarket contact records with engagement history.

**Deduplication strategy** -- deduplicate using this priority:
1. **Primary key**: LinkedIn URL (exact match)
2. **Fallback**: Email address (exact match)
3. **Last resort**: Name + company + normalized title (strip "Sr."/"Senior"/"Jr."/"Junior"/"Lead"/"Staff" prefixes and compare)

### Step 4: Enrich Key Contacts + HubSpot Cross-Reference

**Enrichment**: For the most important contacts (C-suite, VPs, decision-makers), call `Amplemarket:enrich_person` to get:
- Full profile data (title, department, location, LinkedIn URL)
- Email (set `reveal_email: true` if the user wants contact info -- warn about credit cost)
- Phone (set `reveal_phone_numbers: true` only if explicitly requested)

Be judicious with enrichment credits. Prioritize leadership and contacts in relevant departments.

**HubSpot cross-reference** (skip if HubSpot tools are unavailable): For contacts with email addresses, call `HubSpot:search_crm_objects` (type=contacts) searching by email to find matching CRM records. For matches, pull:
- Lifecycle stage, lead status, HubSpot owner
- Associated deals via `HubSpot:search_crm_objects` (type=deals) associated with those contacts -- capture deal stage, amount, and close date

This enriches the "Already in CRM" signal with actual deal context.

### Step 5: Get Outreach & Engagement History

Fire `Amplemarket:ask_analytics` to query outreach history. Ask questions like:
- `"Show me all outreach activity for contacts at [company domain]"`
- `"Which contacts at [domain] have replied to our sequences?"`

**While waiting for analytics**: Proceed immediately to Step 6 (signal identification) using data already gathered from Steps 3-4. Don't block on analytics.

Then poll with `Amplemarket:get_analytics_result` using this retry strategy:
1. Wait ~15 seconds, then call `get_analytics_result`.
2. If the result isn't ready, wait another 15 seconds and retry.
3. Max 3 retries. If all retries fail, proceed without analytics data -- mark affected contacts as "outreach status unknown" and tell the user: "Analytics data wasn't available. Outreach status is based on contact records only."

Also check `Amplemarket:get_contacts` for any contacts whose emails you already have -- the contact record may include sequence enrollment, email status, and reply data. This supplements analytics data.

Merge analytics data into signals when available; if not, contacts retain their "unknown" status with a note in the summary.

### Step 6: Identify Relationship Signals

From the data gathered, flag these signals for each contact:

- **Already in CRM**: Contact exists in Amplemarket with prior engagement
- **In CRM with deal**: Contact has an associated deal in HubSpot (show deal stage + amount)
- **HubSpot owner assigned**: A team member owns this contact in HubSpot
- **Replied**: Has responded to outreach (extract tone + key message)
- **In sequence**: Currently enrolled in an active sequence
- **Meeting booked**: Any meeting or demo scheduled
- **Connected**: A team member is connected on LinkedIn or has had prior communication
- **No outreach**: Not contacted yet

### Step 7: Build the Org Chart (React Artifact)

Create a React `.jsx` artifact that renders an interactive org chart. The visual approach depends on how many contacts were discovered.

#### Data Structure

```javascript
const orgData = {
  company: {
    name: "Acme Corp",
    domain: "acme.com",
    industry: "SaaS",
    size: "201-500",
    hq: "San Francisco, CA"
  },
  contacts: [
    {
      id: "1",
      name: "Jane Smith",
      title: "CEO",
      department: "Executive",
      seniority: "C-Suite",
      email: "jane@acme.com",
      linkedin: "https://linkedin.com/in/janesmith",
      status: "engaged",       // engaged | in_sequence | no_outreach | connected | unknown
      outreach: {
        reached: true,
        channel: "email",
        sequence: "Enterprise Outbound Q1",
        touchpoints: 3,
        replied: true,
        replySummary: "Positive -- asked for a demo next week",
        lastActivity: "2026-02-28"
      },
      relationships: {
        teamConnection: "Luis B. (LinkedIn)",
        inCRM: true
      },
      hubspot: {
        lifecycleStage: "opportunity",
        owner: "Maria G.",
        deal: {
          name: "Acme Corp - Enterprise",
          stage: "Contract Sent",
          amount: 85000,
          closeDate: "2026-04-15"
        }
      }
    },
    // ... more contacts
  ]
};
```

#### Layout Selection by Contact Count

**Small accounts (1-5 contacts) - Card Grid layout:**
Don't render a tree -- show a horizontal row of contact cards (or 2x3 grid) beneath the company header. Each card is larger with more detail visible by default: name, title, department, email, LinkedIn link, status badge, outreach summary, and deal info. No connector lines needed.

**Medium accounts (6-30 contacts) - Full Tree layout:**
This is the primary use case. Render the full interactive tree as described below.

**Large accounts (30+ contacts) - Collapsed Tree layout:**
Render the tree but collapse Director-level branches by default (show the Director card with a "+N reports" badge). User can click to expand any branch. Provide "Expand All" / "Collapse All" toggles. Group by department at the VP level.

#### Visual Design

Style after theorg.com: clean white cards, subtle shadows, thin gray connector lines, top-down vertical tree layout.

**Cards**: Initials avatar (colored by status), name, title, colored left-border stripe for status. Click a card to expand a detail panel showing outreach data, LinkedIn link, CRM deal info (stage, amount, close date), and relationship signals.

**Status Color Coding:**
- Green = Engaged (replied positively or meeting booked)
- Yellow = In sequence (reached out, awaiting reply)
- Red = No outreach yet (gap in coverage)
- Blue = Warm relationship (connected, internal champion)
- Gray = Unknown (analytics unavailable, status couldn't be determined)

**Tree Hierarchy Construction:**
Since Amplemarket doesn't store reporting lines, infer hierarchy from seniority and department:
- Level 0: C-Suite / Founders
- Level 1: VPs / Heads of Department (grouped by department)
- Level 2: Directors (under their department's VP)
- Level 3: Managers / Senior ICs

If the user scoped the search to a specific department in Step 2, make that department's VP/Head the root instead of CEO.

Group children by department or region when a parent has many reports. If a node has >8 direct reports, show first 4-5 and a "+N more" expandable badge.

**Responsive**: Horizontally scrollable for wide trees.

**Company Header:**
Above the tree. Company name, domain, industry, size, and key engagement stats (emails sent, replies, meetings, account score) in a row of stat badges.

**Controls Bar:**
Below header, above tree: search input, status filter pills (All, Engaged, In Sequence, No Outreach, Warm -- each with a count), and expand-all toggle.

**Legend:**
Fixed bottom-right corner: small floating card with color dot + label for each status.

### Step 8: Present and Summarize

After rendering the org chart, provide a brief text summary:

- **Account overview**: Company, industry, size
- **Coverage stats**: X of Y contacts reached, Z replied, N gaps
- **Key insight**: Who's the most engaged? Where are the biggest gaps? Which department has no coverage?
- **CRM context** (if HubSpot data available): Active deals, total pipeline value, contacts with HubSpot owners
- **Suggested next steps**: Recommend who to reach out to next (senior people in uncovered departments)

If analytics data was unavailable (Step 5 failed), note this in the summary and suggest re-running later.
If HubSpot data was unavailable, note that CRM cross-referencing was skipped.

### Step 9: Optional -- Create Lead List

After presenting the chart, offer: "Want me to create an Amplemarket lead list with the uncovered contacts (no outreach yet)?"

If the user says yes:
1. Call `Amplemarket:create_lead_list` with a name like "[Company] - Org Chart Gaps - [Date]"
2. Call `Amplemarket:add_leads_to_lead_list` with only contacts whose status is "no_outreach" or "unknown"

This gives the sales team a ready-made list of gaps to fill.

## Tool Reference Quick Guide

| Goal | Tool | Key Params |
|------|------|-----------|
| Find account | `Amplemarket:list_accounts` | `name`, `domain` |
| Account details | `Amplemarket:get_account` | `id` |
| Company firmographics | `Amplemarket:enrich_company` | `domain` |
| Find contacts | `Amplemarket:search_people` | `company_domains`, `person_seniorities`, `job_functions`, `full_output: true` |
| Contact records | `Amplemarket:get_contacts` | `emails` |
| Enrich a person | `Amplemarket:enrich_person` | `linkedin_url` or `name` + `company_domain` |
| Outreach history | `Amplemarket:ask_analytics` + `Amplemarket:get_analytics_result` | natural language question |
| CRM contacts | `HubSpot:search_crm_objects` | `objectType: "contacts"`, filter by email |
| CRM deals | `HubSpot:search_crm_objects` | `objectType: "deals"`, associated contact |
| Create lead list | `Amplemarket:create_lead_list` | `name` |
| Add to lead list | `Amplemarket:add_leads_to_lead_list` | `lead_list_id`, `leads` |

## Important Notes

- **Credit awareness**: `enrich_person` costs 0.5 credits per call. `reveal_email` and `reveal_phone_numbers` cost additional credits. Always warn the user before batch-enriching. For large accounts (50+ people), suggest enriching only leadership first.
- **Rate limits**: Space out `enrich_person` calls. Don't fire 50 enrichments simultaneously.
- **Data freshness**: Amplemarket data is cached for 24h after enrichment. Mention this if the user asks about accuracy.
- **Hierarchy inference**: Amplemarket doesn't store explicit reporting lines. The skill infers hierarchy from seniority level and department. Call this out to the user -- it's a best-guess org chart, not a verified reporting structure.
- **Graceful degradation**: If any data source fails (analytics, enrichment, contact search, HubSpot), proceed with what you have. An incomplete org chart with clear labels about what's missing is more useful than no chart at all.
- **HubSpot is optional**: If HubSpot tools aren't available or the user doesn't have HubSpot connected, skip all CRM cross-referencing steps and note it in the summary. The org chart is fully functional without CRM data.
