---
name: hubspot-crm-expert
description: |
  HubSpot CRM API expert with rate limiting, associations, timestamps, and batch operations.
  Use when: API calls, creating records, updating deals, associations, stage transitions
  Triggers on: "hubspot", "api call", "association", "create contact", "create deal",
               "update deal", "stage update", "batch", "rate limit", "timestamp"
---

# HubSpot CRM Expert

Production-tested HubSpot CRM API patterns for the FirstMile deals pipeline.

## Quick Reference

| Item | Value |
|------|-------|
| **Owner ID** | `699257003` (Brett Walker) |
| **Pipeline ID** | `8bd9336b-4767-4e67-9fe2-35dfcad7c8be` |
| **API Base** | `https://api.hubapi.com` |
| **Burst Limit** | 100 requests per 10 seconds |
| **Daily Limit** | 150,000 requests per 24 hours |

## Core Principles

1. **Always filter** by Owner ID + Pipeline ID (avoid pulling 3,000+ deals)
2. **Timestamps** = Unix milliseconds as STRING (`"1738281600000"`)
3. **Never hardcode** API keys - always use `.env`
4. **Division protection** - always check denominators before percentage calculations
5. **Windows encoding** - add UTF-8 wrapper to all scripts with emoji output

## Critical Association IDs

| Association | Type ID | Notes |
|-------------|---------|-------|
| CONTACT → COMPANY | 279 | Standard |
| DEAL → COMPANY | 341 | Standard |
| DEAL → CONTACT | 3 | Standard |
| NOTE → DEAL | 214 | Activity logging |
| TASK → DEAL | 216 | Follow-up tasks |
| LEAD → CONTACT | **578** | PRIMARY (required for creation) |
| LEAD → COMPANY | **580** | PRIMARY (required for creation) |

## Decision Rules Summary

### Record Creation Rules
```
IF creating Lead → MUST include PRIMARY associations (578, 580) inline
IF creating Contact → Associate to Company immediately after
IF creating Deal → Only after discovery call scheduled
IF creating Task → Use hs_timestamp for due date (NOT hs_task_due_date)
```

### API Call Rules
```
IF fetching deals → Always include Owner ID + Pipeline ID filters
IF setting dates → Use Unix milliseconds as STRING
IF bulk operation → Use batch endpoints (100 per batch max)
IF 429 response → Wait for Retry-After header, use exponential backoff
```

### Field Update Rules
```
IF setting notes_next_activity_date → CANNOT set directly, create task instead
IF setting Lead hs_lead_type → Use "NEW_BUSINESS" or "UPSELL" (NOT Outbound/Inbound)
IF setting Lead hs_lead_label → Use uppercase: "COLD", "WARM", "HOT"
IF counting tasks completed → Use hs_task_completion_date (NOT hs_timestamp)
```

## Reference Files

| File | Load When | Contents |
|------|-----------|----------|
| `00-decision-rules.md` | Always | IF-THEN rules for all HubSpot operations |
| `01-api-patterns.md` | API calls | Rate limiting, timestamps, headers, batch ops |
| `02-association-rules.md` | Associations | All type IDs with payloads and examples |
| `03-stage-properties.md` | Stage work | Pipeline stages, entry properties, mapping |
| `04-known-failures.md` | Before actions | Common errors and prevention patterns |

## Pipeline Stages (FM Pipeline)

| Stage | ID | Folder Name |
|-------|----|----|
| [01] Discovery Scheduled | `1090865183` | `[01-DISCOVERY-SCHEDULED]` |
| [02] Discovery Complete | `d2a08d6f-cc04-4423-9215-594fe682e538` | `[02-DISCOVERY-COMPLETE]` |
| [03] Rate Creation | `e1c4321e-afb6-4b29-97d4-2b2425488535` | `[03-RATE-CREATION]` |
| [04] Proposal Sent | `d607df25-2c6d-4a5d-9835-6ed1e4f4020a` | `[04-PROPOSAL-SENT]` |
| [05] Setup Docs Sent | `4e549d01-674b-4b31-8a90-91ec03122715` | `[05-SETUP-DOCS-SENT]` |
| [06] Implementation | `08d9c411-5e1b-487b-8732-9c2bcbbd0307` | `[06-IMPLEMENTATION]` |
| [07] Started Shipping | `3fd46d94-78b4-452b-8704-62a338a210fb` | `[07-STARTED-SHIPPING]` |
| [08] Closed Lost | `02d8a1d7-d0b3-41d9-adc6-44ab768a61b8` | `[08-CLOSED-LOST]` |

## Common Commands

| Command | Purpose |
|---------|---------|
| `/check-lead` | Search for existing contact/company before creating |
| `/add-lead` | Create company + contact + lead in HubSpot |
| `/create-deal` | Create deal after discovery scheduled |
| `/update-deal` | Update deal properties or stage |
| `/log-activity` | Create note associated with deal |
| `/create-followup` | Create task with due date |
| `/check-tasks` | Audit task count and hygiene |

## Lead Object Rules (Dec 2025)

**Lead creation REQUIRES inline PRIMARY associations** - cannot create then associate.

```python
# CORRECT - associations inline
lead_payload = {
    "properties": {
        "hs_lead_type": "NEW_BUSINESS",
        "hs_lead_label": "COLD",
        "hubspot_owner_id": "699257003"
    },
    "associations": [
        {"to": {"id": contact_id}, "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 578}]},
        {"to": {"id": company_id}, "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 580}]}
    ]
}
```

**Lead Pipeline Stages** (use string IDs):
- `new-stage-id`
- `attempting-stage-id` (default for outreach)
- `connected-stage-id`
- `qualified-stage-id`
- `unqualified-stage-id`

## Windows Encoding Fix

**Required at top of every Python script with emoji output:**

```python
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

**Subprocess calls:**
```python
result = subprocess.run(cmd, capture_output=True, encoding='utf-8')  # NOT text=True
```

## Integration Points

### Core Module
- `hubspot_sync_core.py` - HubSpotSyncManager class with rate limiting

### Related Skills
- `discovery-sales-expert` - Stage transitions, deal lifecycle
- `goal-tracking-expert` - Stage entry properties for metrics

### Commands
- 60+ commands in `.claude/commands/` for CRM operations

## Post-Action Learning

After any HubSpot API error:
1. Document the error pattern
2. Add to `04-known-failures.md` if new
3. Update `expertise.yaml` if pattern discovered
