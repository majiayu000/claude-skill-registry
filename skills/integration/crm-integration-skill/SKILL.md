---
name: "crm-integration"
description: "CRM integration patterns for Close CRM, HubSpot, and Salesforce. Use when: Close CRM, HubSpot, Salesforce, CRM API, lead sync, deal sync, activity logging, CRM webhook, pipeline automation, contact enrichment."
---

<objective>
Integrate with CRM platforms for sales automation workflows:

1. **Close CRM** - Daily driver for SMB sales (simplest API, best value)
2. **HubSpot** - Marketing + Sales alignment with rich ecosystem
3. **Salesforce** - Enterprise requirements and complex workflows
4. **Cross-CRM Sync** - Bidirectional sync with conflict resolution

Key deliverables:
- API client setup with proper authentication
- CRUD operations for leads, contacts, deals, activities
- Webhook handlers for real-time sync
- Pipeline automation and reporting
</objective>

<quick_start>
**Close CRM (API Key Auth):**
```python
import httpx

class CloseClient:
    BASE_URL = "https://api.close.com/api/v1"

    def __init__(self, api_key: str):
        self.client = httpx.Client(
            base_url=self.BASE_URL,
            auth=(api_key, ""),  # Basic auth, password empty
            timeout=30.0,
        )

    def create_lead(self, data: dict) -> dict:
        response = self.client.post("/lead/", json=data)
        response.raise_for_status()
        return response.json()

    def search_leads(self, query: str) -> list:
        response = self.client.post("/data/search/", json={
            "query": {"type": "query_string", "value": query},
            "results_limit": 100
        })
        return response.json()["data"]

# Usage
close = CloseClient(os.environ["CLOSE_API_KEY"])
leads = close.search_leads("company:Coperniq")
```

**HubSpot (Python SDK):**
```python
from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInputForCreate

client = HubSpot(access_token=os.environ["HUBSPOT_ACCESS_TOKEN"])

# Create contact
contact = client.crm.contacts.basic_api.create(
    SimplePublicObjectInputForCreate(properties={
        "email": "user@example.com",
        "firstname": "Jane",
        "lastname": "Smith"
    })
)
print(f"Created: {contact.id}")
```

**Salesforce (JWT Bearer):**
```python
import jwt
from datetime import datetime, timedelta

class SalesforceClient:
    def __init__(self, client_id: str, username: str, private_key: str):
        self.auth_url = "https://login.salesforce.com"
        self._authenticate(client_id, username, private_key)

    def _authenticate(self, client_id, username, private_key):
        payload = {
            "iss": client_id,
            "sub": username,
            "aud": self.auth_url,
            "exp": int((datetime.utcnow() + timedelta(minutes=3)).timestamp())
        }
        assertion = jwt.encode(payload, private_key, algorithm="RS256")

        response = httpx.post(f"{self.auth_url}/services/oauth2/token", data={
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": assertion
        })
        self.access_token = response.json()["access_token"]
        self.instance_url = response.json()["instance_url"]
```
</quick_start>

<success_criteria>
A CRM integration is successful when:
- API authentication works without errors
- CRUD operations complete for all entity types
- Rate limits are respected (Close: 100 req/10s, HubSpot: varies by tier)
- Webhooks fire and process correctly
- Data syncs bidirectionally without duplicates
</success_criteria>

<crm_comparison>
## Platform Comparison

| Feature | Close | HubSpot | Salesforce |
|---------|-------|---------|------------|
| **Auth** | API Key | OAuth 2.0 / Private App | JWT Bearer |
| **Rate Limit** | 100 req/10s | 100-200 req/10s by tier | 100k req/day |
| **Best For** | SMB sales, simplicity | Marketing + Sales | Enterprise |
| **Starting Price** | $49/user/mo | Free (limited) | $25/user/mo |
| **API Access** | All plans | Starter+ ($45+) | All plans |
| **Webhooks** | All plans | Pro+ ($800+) | All plans |

## Entity Mapping

| Concept | Close | HubSpot | Salesforce |
|---------|-------|---------|------------|
| Company | `lead` | `company` | `Account` |
| Person | `contact` | `contact` | `Contact` / `Lead` |
| Deal | `opportunity` | `deal` | `Opportunity` |
| Activity | `activity` | `engagement` | `Task` / `Event` |
| Custom Field | `custom.cf_xxx` | `properties` | `Field__c` |

## Pipeline Stage Mapping

| Stage | Close | HubSpot | Salesforce |
|-------|-------|---------|------------|
| New | `Lead` | `appointmentscheduled` | `Prospecting` |
| Qualified | `Contacted` | `qualifiedtobuy` | `Qualification` |
| Demo | `Opportunity` | `presentationscheduled` | `Needs Analysis` |
| Proposal | `Proposal` | `decisionmakerboughtin` | `Proposal/Price Quote` |
| Won | `Won` | `closedwon` | `Closed Won` |
| Lost | `Lost` | `closedlost` | `Closed Lost` |
</crm_comparison>

<close_patterns>
## Close CRM (Daily Driver)

### Query Language (for Smart Views)
```python
# Leads with no activity in 30 days
'sort:date_updated asc date_updated < "30 days ago"'

# High-value opportunities
'opportunities.value >= 50000 opportunities.status_type:active'

# Custom field filtering
'custom.cf_industry = "MEP Contractor"'

# Multiple trade types (your ICP)
'custom.cf_trades:HVAC OR custom.cf_trades:Electrical'
```

### Core Operations
```python
# Create lead with contacts
lead = close.create_lead({
    "name": "ABC Mechanical",
    "url": "https://abcmech.com",
    "contacts": [{
        "name": "John Smith",
        "title": "Owner",
        "emails": [{"email": "john@abcmech.com", "type": "office"}],
        "phones": [{"phone": "555-1234", "type": "office"}]
    }],
    "custom.cf_tier": "Gold",
    "custom.cf_source": "sales-agent"
})

# Create opportunity
opp = close._request("POST", "/opportunity/", json={
    "lead_id": lead["id"],
    "value": 50000,
    "confidence": 50,
    "status_id": "stat_xxx"  # Pipeline stage
})

# Log activity
close._request("POST", "/activity/note/", json={
    "lead_id": lead["id"],
    "note": "Initial discovery call - interested in demo"
})
```

### Rate Limit Headers (RFC-compliant)
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1704067200
```

> See `reference/close-deep-dive.md` for query language, Smart Views, sequences, and reporting.
</close_patterns>

<hubspot_patterns>
## HubSpot Integration

### Python SDK Pattern
```python
from hubspot import HubSpot
from hubspot.crm.deals import SimplePublicObjectInputForCreate
from hubspot.crm.contacts import PublicObjectSearchRequest

client = HubSpot(access_token=os.environ["HUBSPOT_ACCESS_TOKEN"])

# Create deal with association
deal = client.crm.deals.basic_api.create(
    SimplePublicObjectInputForCreate(properties={
        "dealname": "Enterprise Deal",
        "amount": "50000",
        "dealstage": "appointmentscheduled",
        "pipeline": "default"
    })
)

# Search contacts by email domain
search = PublicObjectSearchRequest(
    filter_groups=[{
        "filters": [{
            "propertyName": "email",
            "operator": "CONTAINS",
            "value": "@example.com"
        }]
    }],
    properties=["email", "firstname", "lastname"],
    limit=50
)
results = client.crm.contacts.search_api.do_search(search)
```

### Association Types
| From | To | Type ID |
|------|-----|---------|
| Contact | Company | 1 |
| Contact | Deal | 4 |
| Company | Deal | 6 |
| Deal | Contact | 3 |

> See `reference/hubspot-patterns.md` for batch operations, custom properties, and workflows.
</hubspot_patterns>

<salesforce_patterns>
## Salesforce Integration

### SOQL Query Patterns
```sql
-- Parent-child relationship (Contacts of Account)
SELECT Id, Name, (SELECT LastName, Email FROM Contacts)
FROM Account WHERE Industry = 'Technology'

-- Child-parent relationship
SELECT Id, FirstName, Account.Name, Account.Industry
FROM Contact WHERE Account.Industry = 'Technology'

-- Semi-join (Accounts with open Opportunities)
SELECT Id, Name FROM Account
WHERE Id IN (SELECT AccountId FROM Opportunity WHERE IsClosed = false)
```

### REST API v59.0
```python
def create_opportunity(self, data: dict) -> dict:
    """Required: Name, StageName, CloseDate."""
    response = self.client.post(
        f"{self.instance_url}/services/data/v59.0/sobjects/Opportunity/",
        headers={"Authorization": f"Bearer {self.access_token}"},
        json=data
    )
    return response.json()

# Composite API (batch up to 200 records)
def composite_create(self, records: list) -> dict:
    return self.client.post(
        f"{self.instance_url}/services/data/v59.0/composite/sobjects",
        json={"allOrNone": False, "records": records}
    )
```

> See `reference/salesforce-patterns.md` for JWT setup, Platform Events, and bulk API.
</salesforce_patterns>

<webhook_patterns>
## Webhook Handlers

### Close Webhook (FastAPI)
```python
from fastapi import FastAPI, Request, HTTPException
import hmac, hashlib

app = FastAPI()

@app.post("/webhooks/close")
async def close_webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("Close-Sig")

    expected = hmac.new(
        CLOSE_WEBHOOK_SECRET.encode(), body, hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature, expected):
        raise HTTPException(401, "Invalid signature")

    data = await request.json()
    event_type = data["event"]["event_type"]

    handlers = {
        "lead.created": handle_lead_created,
        "opportunity.status_changed": handle_opp_stage_change,
    }

    if handler := handlers.get(event_type):
        await handler(data["event"]["data"])

    return {"status": "ok"}
```

### Close Webhook Events
```
lead.created, lead.updated, lead.deleted, lead.status_changed
contact.created, contact.updated
opportunity.created, opportunity.status_changed
activity.note.created, activity.call.created, activity.email.created
unsubscribed_email.created
```
</webhook_patterns>

<sync_architecture>
## Cross-CRM Sync

### Architecture
```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Close     │────▶│  Sync Layer  │◀────│  HubSpot    │
│  (Primary)  │◀────│  (Postgres)  │────▶│  (Marketing)│
└─────────────┘     └──────────────┘     └─────────────┘
```

### Sync Record Schema
```sql
CREATE TABLE crm_sync_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type VARCHAR(50) NOT NULL,
    close_id VARCHAR(100) UNIQUE,
    hubspot_id VARCHAR(100) UNIQUE,
    salesforce_id VARCHAR(100) UNIQUE,
    email VARCHAR(255),
    company_name VARCHAR(255),
    last_synced_at TIMESTAMPTZ,
    sync_source VARCHAR(50),
    sync_hash VARCHAR(64)
);

CREATE INDEX idx_sync_email ON crm_sync_records(email);
```

### Conflict Resolution
```python
from enum import Enum

class ConflictStrategy(Enum):
    CLOSE_WINS = "close"      # Close is source of truth
    LAST_WRITE_WINS = "lww"   # Most recent update wins

def resolve_conflict(close_record, hubspot_record, strategy):
    if strategy == ConflictStrategy.CLOSE_WINS:
        merged = close_record.copy()
        for key, value in hubspot_record.items():
            if key not in merged or not merged[key]:
                merged[key] = value
        return merged
```

> See `reference/sync-patterns.md` for deduplication, migration scripts, and bulk sync.
</sync_architecture>

<file_locations>
## Reference Files

**CRM-Specific:**
- `reference/close-deep-dive.md` - Query language, Smart Views, sequences, reporting
- `reference/hubspot-patterns.md` - SDK patterns, batch operations, workflows
- `reference/salesforce-patterns.md` - JWT auth, SOQL, Platform Events, bulk API

**Operations:**
- `reference/sync-patterns.md` - Cross-CRM sync, deduplication, migration
- `reference/automation.md` - Webhook setup, sequences, workflows

**Templates:**
- `templates/close-client.py` - Full Close API client
- `templates/hubspot-client.py` - HubSpot SDK wrapper
- `templates/sync-service.py` - Cross-CRM sync service
</file_locations>

<routing>
## Request Routing

**User wants CRM integration:**
→ Ask which CRM (Close recommended for simplicity)
→ Provide auth setup + basic CRUD

**User wants Close CRM:**
→ Provide API key setup, query language
→ Reference: `reference/close-deep-dive.md`

**User wants HubSpot:**
→ Provide SDK setup, search patterns
→ Reference: `reference/hubspot-patterns.md`

**User wants Salesforce:**
→ Provide JWT auth, SOQL patterns
→ Reference: `reference/salesforce-patterns.md`

**User wants sync between CRMs:**
→ Provide sync architecture, conflict resolution
→ Reference: `reference/sync-patterns.md`

**User wants webhooks:**
→ Provide handler pattern for specified CRM
→ Include signature verification
</routing>

<env_setup>
## Environment Variables

```bash
# Close CRM
export CLOSE_API_KEY="api_xxx"
export CLOSE_WEBHOOK_SECRET="whsec_xxx"

# HubSpot
export HUBSPOT_ACCESS_TOKEN="pat-xxx"

# Salesforce
export SF_CLIENT_ID="xxx"
export SF_USERNAME="user@company.com"
export SF_PRIVATE_KEY_PATH="./salesforce.key"
export SF_INSTANCE_URL="https://yourorg.my.salesforce.com"
```

```bash
# Install dependencies
pip install httpx pyjwt hubspot-api-client python-dotenv
```
</env_setup>

<example_session>
## Example Session

**User:** "I need to push enriched leads from my sales-agent to Close CRM"

**Claude:**
1. Here's the pattern for pushing enriched data to Close:
```python
async def push_to_close(close_client, enriched_data: dict) -> str:
    lead_data = {
        "name": enriched_data["company_name"],
        "url": enriched_data.get("website"),
        "custom.cf_tier": enriched_data["tier"],
        "custom.cf_source": "sales-agent",
        "contacts": [{
            "name": c["name"],
            "title": c.get("title"),
            "emails": [{"email": c["email"]}] if c.get("email") else []
        } for c in enriched_data.get("contacts", [])]
    }

    result = close_client.create_lead(lead_data)
    return result["id"]
```

2. Make sure you have these custom fields in Close:
   - `cf_tier` (choices: Gold, Silver, Bronze)
   - `cf_source` (choices: sales-agent, inbound, referral)

3. Rate limit: 100 requests per 10 seconds. Add `asyncio.sleep(0.1)` between requests for bulk imports.
</example_session>
