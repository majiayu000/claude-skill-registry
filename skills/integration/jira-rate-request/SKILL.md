# JIRA Rate Request Skill

---
name: jira-rate-request
description: Submit custom pricing requests to Sales/Pricing via JIRA Service Desk. Automates form filling, captures ticket number, and logs to HubSpot. Triggers on "submit JIRA", "rate request", "pricing request", "JIRA ticket", "submit to sales".
---

## Purpose

Automate the JIRA Service Desk rate request submission process for FirstMile custom pricing requests. This skill handles the entire workflow from form filling to HubSpot logging.

## Triggers

- "submit JIRA"
- "rate request"
- "pricing request"
- "JIRA ticket"
- "submit to sales"
- "create rate ticket"

## Prerequisites

1. **Chrome MCP Connected**: Browser automation requires Claude-in-Chrome extension
2. **JIRA Access**: User must be logged into FirstMile JIRA
3. **Deal Information**: Need customer details from Tier Tool or Brand Scout

## JIRA Form Structure

### Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| **Customer Name*** | Company name | Static Nails |
| **Product Type*** | Xparcel Domestic, UPS, etc. | Xparcel Domestic |
| **Weekly Volume*** | Packages per week | 1500 |
| **State*** | Ship-from state (dropdown) | TX |
| **Background and Goals*** | Customer context, requirements | See format below |
| **Requested Setup*** | Carrier list by service level | See format below |

### Optional Fields

| Field | Description |
|-------|-------------|
| **Attach the Tier Tool** | Upload Tier Tool Excel file |

## Field Formats

### Background and Goals Format

```
Hi Sales,

Please create rates for [CUSTOMER]. [LEAD STATUS] - [CURRENT CARRIER SITUATION].
[SPECIAL REQUIREMENTS - ORM-D, hazmat, etc.].

Ship from [CITY], [STATE] [ZIP].

[VOLUME]/day, [BOX SIZE] boxes, [WEIGHT PROFILE].

[INTEGRATION] integration.

[ADDITIONAL NOTES - Out Of Network pickup, etc.]
```

**Example:**
```
Hi Sales,

Please create rates for Static Nails. Hot lead - actively shopping carriers (currently on DHL).
ORM-D/Class 3 shipper (nail polish).

Ship from Fort Worth, TX 76106.

300 orders/day, 8x4x4 boxes, majority under 1 lb.

ShipStation integration.

Tier Tool shows "Out Of Network" pickup - needs Sales verification.
```

### Requested Setup Format (Bulleted)

```
XParcel Priority / Expedited Plus
  - DHL Max
  - USPS PM

XParcel Expedited
  - DHL Expedited
  - Amazon
  - USPS GA
  - ACI-D
  - ONT
  - UniUni
  - Veho

XParcel Ground
  - DHL Ground
  - Amazon
  - USPS GA
  - ACI-D
  - ACI-WS
  - ONT
  - UniUni
  - Veho
```

**For ORM-D/Hazmat accounts, add note:**
```
Note: ORM-D/Class 3 requires hazmat-capable carriers only (UPS Ground, FedEx Ground).
MSDS pending from customer.
```

## Workflow

### Step 1: Gather Deal Information

Before starting, collect:
- Customer name
- Product type (Xparcel Domestic, UPS, etc.)
- Weekly volume
- Ship-from state and ZIP
- Special requirements (hazmat, DG, etc.)
- Current carrier situation
- Integration platform
- Tier Tool file (if available)

### Step 2: Navigate to JIRA

```
URL: https://firstmile.atlassian.net/servicedesk/customer/portal/5
Click: "Submit a Custom Pricing Request"
```

### Step 3: Fill Form Fields

1. **Customer Name**: Enter company name
2. **Product Type**: Enter "Xparcel Domestic" (or UPS, etc.)
3. **Weekly Volume**: Enter number only (e.g., 1500)
4. **State**: Click dropdown, select state abbreviation
5. **Background and Goals**: Enter formatted text (see above)
6. **Requested Setup**: Enter bulleted carrier list (see above)
7. **Attach Tier Tool**: (Optional) Click Browse, upload file

### Step 4: Submit & Capture Ticket

1. Click **Send** button
2. Wait for confirmation page
3. Capture ticket number from URL: `RATE-XXXX`
4. Screenshot for verification

### Step 5: Log to HubSpot

Create note on deal with:
```
JIRA Rate Request Submitted: RATE-XXXX

Ticket Details:
- Customer: [NAME]
- Product Type: [TYPE]
- Weekly Volume: [VOLUME]
- State: [STATE] ([ZIP])
- [Special requirements]

Next Steps:
- Wait for Sales to [verify/create rates]
- [Pending items from customer]
```

## Chrome MCP Commands

```python
# Navigate to JIRA
mcp__claude-in-chrome__navigate(url="https://firstmile.atlassian.net/servicedesk/customer/portal/5", tabId=TAB_ID)

# Click Submit a Custom Pricing Request
mcp__claude-in-chrome__find(query="Submit a Custom Pricing Request", tabId=TAB_ID)
mcp__claude-in-chrome__computer(action="left_click", ref=REF_ID, tabId=TAB_ID)

# Fill text fields
mcp__claude-in-chrome__form_input(ref=REF_ID, value="VALUE", tabId=TAB_ID)

# Fill dropdown (State)
mcp__claude-in-chrome__computer(action="left_click", ref=STATE_REF, tabId=TAB_ID)
mcp__claude-in-chrome__find(query="TX option in dropdown", tabId=TAB_ID)
mcp__claude-in-chrome__computer(action="left_click", ref=OPTION_REF, tabId=TAB_ID)

# Submit
mcp__claude-in-chrome__find(query="Send button", tabId=TAB_ID)
mcp__claude-in-chrome__computer(action="left_click", ref=SEND_REF, tabId=TAB_ID)
```

## HubSpot Integration

```python
# Create note with JIRA ticket
note_payload = {
    'properties': {
        'hs_timestamp': str(int(datetime.now().timestamp() * 1000)),
        'hs_note_body': note_body
    }
}
requests.post('https://api.hubapi.com/crm/v3/objects/notes', headers=headers, json=note_payload)

# Associate with deal (type 214)
requests.put(f'https://api.hubapi.com/crm/v3/objects/notes/{note_id}/associations/deals/{deal_id}/214', headers=headers)
```

## Common Issues

| Issue | Solution |
|-------|----------|
| State dropdown not selecting | Click dropdown first, wait for options, then click state |
| Text appearing in wrong field | Use `read_page` to get correct element refs |
| Form not submitting | Scroll to bottom to ensure Send button visible |
| Garbled text | Take screenshot to verify, use Ctrl+A and retype if needed |

## Output

After successful submission:

| Field | Value |
|-------|-------|
| JIRA Ticket | RATE-XXXX |
| Status | Submitted |
| HubSpot Note | Created & Associated |
| Next Action | Wait for Sales response |

## Related Skills

- `/brand-scout` - Research before rate request
- `/deal-update` - Move deal stage after rates received
- `/create-followup` - Set follow-up task for rate response
