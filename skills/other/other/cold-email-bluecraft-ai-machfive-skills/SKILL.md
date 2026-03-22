---
name: cold-email
description: Generate hyper-personalized cold email sequences using AI. Turn lead data into high-converting outreach campaigns.
license: MIT
---

# MachFive - AI Cold Email Generator

Generate personalized cold email sequences from lead data. MachFive uses AI to research prospects and craft unique, relevant outreach - not templates.

## Setup

1. Get your API key at https://app.machfive.io/settings (Integrations → API Keys)
2. Set `MACHFIVE_API_KEY` in your environment

## Campaign ID

Every generate request needs a **campaign ID** in the URL: `/api/v1/campaigns/{campaign_id}/generate` (or `/generate-batch`).

- **If the user has not provided a campaign name or ID:** Call **GET /api/v1/campaigns** (see below) to list campaigns in their workspace, then ask them to pick one by name or ID before running generate.
- **Where to get it manually:** https://app.machfive.io/campaigns → open a campaign → copy the ID from the URL or settings.
- **No default:** The skill does not assume a campaign. The user (or agent config) must provide one. Agents can store a default campaign ID for the workspace if the user provides it (e.g. "use campaign X for my requests").

## Endpoints

### List Campaigns (discover before generate)

List campaigns in the workspace so the agent can ask the user which campaign to use when they haven't provided a name or ID.
```
GET https://app.machfive.io/api/v1/campaigns
Authorization: Bearer {MACHFIVE_API_KEY}
```
Or use `X-API-Key: {MACHFIVE_API_KEY}` header.

Optional query: `?q=search` or `?name=search` to filter by campaign name.

**Response (200):**
```json
{
  "campaigns": [
    { "id": "cb1bbb14-e576-4d8f-a8f3-6fa929076fd8", "name": "SaaS Q1 Outreach", "created_at": "2025-01-15T12:00:00Z" },
    { "id": "a1b2c3d4-...", "name": "Enterprise Leads", "created_at": "2025-01-10T08:00:00Z" }
  ]
}
```
If no campaign name or ID was given, call this first, then ask the user: "Which campaign should I use? [list names/IDs]."

### Single Lead (Sync)

Generate an email sequence for one lead (3–5 emails per lead). Waits for completion, returns the sequence directly. **The request can take 3–5 minutes** (AI research + generation); use a client timeout of at least **300 seconds (5 min)** or **600 seconds (10 min)**. Do not use a 120s timeout or the response will be cut off.
```
POST https://app.machfive.io/api/v1/campaigns/{campaign_id}/generate
Authorization: Bearer {MACHFIVE_API_KEY}
Content-Type: application/json
```

Or use `X-API-Key: {MACHFIVE_API_KEY}` header.
```json
{
  "lead": {
    "name": "John Smith",
    "title": "VP of Marketing",
    "company": "Acme Corp",
    "email": "john@acme.com",
    "company_website": "https://acme.com",
    "linkedin_url": "https://linkedin.com/in/johnsmith"
  },
  "options": {
    "list_name": "Q1 Outreach",
    "email_count": 3,
    "email_signature": "Best,\nYour Name",
    "approved_ctas": ["Direct Meeting CTA", "Lead Magnet CTA"]
  }
}
```

**Response (200):**
```json
{
  "lead_id": "lead_xyz789",
  "list_id": "uuid",
  "sequence": [
    { "step": 1, "subject": "...", "body": "..." },
    { "step": 2, "subject": "...", "body": "..." },
    { "step": 3, "subject": "...", "body": "..." }
  ],
  "credits_remaining": 94
}
```

**Recovery:** The response includes `list_id`. If the request times out or the response is truncated, you can still get the result: call **GET /api/v1/lists/{list_id}** to confirm status, then **GET /api/v1/lists/{list_id}/export?format=json** to retrieve the sequence.

### Batch (Async)

Generate email sequences for multiple leads (one list; each lead gets a sequence). **Returns immediately** (202) with `list_id`; processing runs in the background. To get results: poll list status, then call export.
```
POST https://app.machfive.io/api/v1/campaigns/{campaign_id}/generate-batch
Authorization: Bearer {MACHFIVE_API_KEY}
Content-Type: application/json
```

Or use `X-API-Key: {MACHFIVE_API_KEY}` header.
```json
{
  "leads": [
    { "name": "John Smith", "email": "john@acme.com", "company": "Acme Corp", "title": "VP Marketing" },
    { "name": "Jane Doe", "email": "jane@beta.com", "company": "Beta Inc", "title": "Director Sales" }
  ],
  "options": {
    "list_name": "Q1 Outreach Batch",
    "email_count": 3
  }
}
```

**Response (202):**
```json
{
  "list_id": "uuid",
  "status": "processing",
  "leads_count": 2,
  "message": "Batch accepted. Poll list status or open in UI."
}
```

### List lead lists

List lead lists in the workspace. Optional query: `campaign_id`, `status` (`pending` | `processing` | `completed` | `failed`), `limit` (default 50, max 100), `offset`.
```
GET https://app.machfive.io/api/v1/lists
GET https://app.machfive.io/api/v1/lists?campaign_id={campaign_id}&status=completed&limit=20
Authorization: Bearer {MACHFIVE_API_KEY}
```

**Response (200):** `{ "lists": [ { "id", "campaign_id", "custom_name", "processing_status", "created_at", "completed_at" }, ... ] }`. Order is `created_at` desc.

### List status (poll)

Poll until the list is done. Use the `list_id` from generate or generate-batch.
```
GET https://app.machfive.io/api/v1/lists/{list_id}
Authorization: Bearer {MACHFIVE_API_KEY}
```

**Response (200):** `id`, `campaign_id`, `custom_name`, `processing_status` (`pending` | `processing` | `completed` | `failed`), `created_at`, `updated_at`. When `processing_status === 'completed'`: `leads_count`, `emails_created`, `completed_at`. When `failed`: `failed_at`. **404** if list not found or not in workspace.

Poll every 10–30 seconds until `processing_status === 'completed'` or `failed`. If `failed`, the list cannot be exported; retry by submitting a new batch.

### List export (get results)

After status is `completed`, fetch the processed output. **CSV** (default) or **JSON**.
```
GET https://app.machfive.io/api/v1/lists/{list_id}/export?format=csv
GET https://app.machfive.io/api/v1/lists/{list_id}/export?format=json
Authorization: Bearer {MACHFIVE_API_KEY}
```

- **format=csv** (default): Returns the processed CSV (same as UI download), with `Content-Disposition: attachment; filename="MachFive-{list_id}.csv"`.
- **format=json**: Returns `{ "leads": [ { "email": "...", "sequence": [ { "step": 1, "subject": "...", "body": "..." }, ... ] }, ... ] }`. Each lead may include optional `name`, `company`, `title` when present, e.g. `{ "email": "john@acme.com", "name": "John Smith", "company": "Acme Corp", "title": "VP Marketing", "sequence": [ ... ] }`.
- **409** if list is not yet completed (poll GET /lists/:id first). **404** if list not found or not in workspace.

**Batch flow:** POST generate-batch → 202 + list_id → poll GET /lists/:id until `processing_status === 'completed'` → GET /lists/:id/export?format=csv or json → return result to user.

## Lead Fields

Each lead must include a valid **`email`**; it is used to map the lead through processing and to match generated sequences back to the lead in exports (same as the app UI). All other fields are optional but improve personalization.

| Field | Required | Description |
|-------|----------|-------------|
| `email` | **Yes** | Lead's email address; used to map the lead through processing and in exports |
| `name` | No | Full name or first name (improves personalization) |
| `company` | No | Company name (improves personalization) |
| `title` | No | Job title (improves personalization) |
| `company_website` | No | Company URL for research |
| `linkedin_url` | No | LinkedIn profile for deeper personalization |

## Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `list_name` | string | Auto | Display name for this list in MachFive UI |
| `email_count` | number | 3 | Emails per lead (1-5) |
| `email_signature` | string | None | Signature appended to emails |
| `campaign_angle` | string | None | Context for personalization |
| `approved_ctas` | array | From campaign | CTAs to use (omit to use campaign defaults) |

## Limits

- **Single lead (sync):** Request can take 5–10 minutes; use a client timeout of at least 300s (5 min) or 600s (10 min).
- **Batch (async):** Returns 202 immediately; poll **GET /api/v1/lists/{list_id}** every 10–30s until `processing_status` is `completed` or `failed`. Workspaces have a concurrent batch limit; if you get **429**, retry later.
- **List lists:** Query param `limit` default 50, max 100; `offset` for pagination.

## Errors

| Code | Error | Description |
|------|-------|-------------|
| 400 | BAD_REQUEST | Invalid JSON, missing `lead`/`leads`, or missing/invalid lead `email`; or campaign has no vector store |
| 401 | UNAUTHORIZED | Invalid or missing API key |
| 402 | INSUFFICIENT_CREDITS | Out of credits |
| 403 | FORBIDDEN | Campaign not in your workspace |
| 404 | NOT_FOUND | Campaign or list doesn't exist |
| 409 | NOT_READY | Export called before list completed (poll GET /lists/:id first) |
| 429 | WORKSPACE_LIMIT | Too many concurrent batch jobs; try again later |

## Usage Examples

"Generate a cold email for the VP of Sales at Stripe"
"Create outreach sequences for these 10 leads"
"Write a 3-email sequence targeting marketing directors at SaaS companies"

## Pricing

- Free: 100 credits/month
- Starter: 2,000 credits/month
- Growth: 5,000 credits/month
- Enterprise: Custom credits/month
- 1 credit = 1 lead processed

Get started: https://machfive.io
