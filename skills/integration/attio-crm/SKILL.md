---
name: attio-crm
description: Attio CRM operations for companies, contacts, and notes management. Use this skill when interacting with Attio CRM, searching companies, creating contacts, adding notes, or managing deal records. Triggers on CRM operations, company lookup, contact management, or Attio-related requests.
---

# Attio CRM

## Overview

Interact with Attio CRM to manage companies, contacts, notes, and deals programmatically.

## Quick Decision Tree

```
What do you need?
│
├── Get/search companies
│   └── references/api-guide.md
│   └── Script: scripts/attio_api.py get-company / search-companies
│
├── Create/update company
│   └── Script: scripts/attio_api.py create-company / update-company
│
├── Create/link contacts
│   └── Script: scripts/attio_api.py create-person
│
├── Add notes to records
│   └── Script: scripts/attio_api.py create-note
│
└── Parse Attio URLs
    └── Script: scripts/attio_api.py parse-url
```

## Environment Setup

```bash
# Required in .env
ATTIO_API_KEY=your_api_key_here
```

Get your API key: Attio Settings → Developers → API Keys

## Required Scopes

| Scope | Operations |
|-------|------------|
| `record:read` | Get/search companies and people |
| `record:write` | Create/update companies and people |
| `note:read` | List and get notes |
| `note:write` | Create and delete notes |

## Common Usage

### Search Companies
```bash
python scripts/attio_api.py search-companies "Acme Corp" --limit 10
```

### Get Company
```bash
python scripts/attio_api.py get-company <record_id>
```

### Create Company
```bash
python scripts/attio_api.py create-company "Microsoft" --domain "microsoft.com"
```

### Create Contact
```bash
python scripts/attio_api.py create-person "john@acme.com" --first-name "John" --last-name "Smith"
```

### Add Note
```bash
python scripts/attio_api.py create-note <record_id> "Meeting Notes" "Discussion summary..."
```

## Rate Limits
- 100 requests per minute
- Automatic retry with exponential backoff

## Cost
Free - Attio API has generous free tier.

## Security Notes

### Credential Handling
- Store `ATTIO_API_KEY` in `.env` file (never commit to git)
- Generate keys in Attio: Settings > Developers > API Keys
- Rotate keys periodically or if compromised
- Never log or print API keys in script output

### Data Privacy
- CRM contains sensitive customer and prospect information
- Company records include business details and contact info
- People records contain PII (names, emails, phone numbers)
- Notes may contain confidential meeting discussions
- Avoid exporting full CRM data unnecessarily

### Access Scopes
- Request minimum required scopes:
  - `record:read` - Read companies and people (read-only)
  - `record:write` - Create/update records (write access)
  - `note:read` - Read notes (read-only)
  - `note:write` - Create notes (write access)
- API keys can be scoped to specific permissions

### Compliance Considerations
- **PII Protection**: Customer data is subject to privacy regulations
- **GDPR**: EU customer data requires GDPR compliance
- **Data Minimization**: Only access/export data you need
- **Audit Trail**: Log CRM operations for compliance auditing
- **Data Retention**: Follow organizational data retention policies
- **Access Control**: Limit API key distribution to authorized users
- **Customer Consent**: Ensure proper consent for data processing

## Troubleshooting

### Common Issues

#### Issue: Invalid field ID / slug
**Symptoms:** "Field not found" or "Invalid attribute" error
**Cause:** Field slug doesn't match Attio workspace configuration
**Solution:**
- Check field slugs in Attio: Settings > Objects > Fields
- Field slugs are case-sensitive (e.g., `company_name` not `Company_Name`)
- Custom fields have unique slugs - verify exact spelling
- Use API to list available fields if unsure

#### Issue: Rate limited
**Symptoms:** 429 status code or "rate limit exceeded"
**Cause:** Exceeding 100 requests per minute limit
**Solution:**
- Implement exponential backoff between requests
- Batch multiple operations into single requests where possible
- Add delays (600ms+) between consecutive requests
- Queue requests and process gradually

#### Issue: Record not found
**Symptoms:** "Record not found" error with known record
**Cause:** Invalid record ID, deleted record, or wrong object type
**Solution:**
- Verify record ID from Attio URL or previous API response
- Check if record was deleted or merged
- Ensure using correct object type (companies vs people)
- Use search endpoint to find record by name/email

#### Issue: API key invalid
**Symptoms:** 401 Unauthorized or "invalid API key"
**Cause:** Key expired, revoked, or incorrectly configured
**Solution:**
- Regenerate API key in Attio: Settings > Developers > API Keys
- Verify `ATTIO_API_KEY` is correctly set in `.env`
- Check for leading/trailing whitespace in key
- Ensure key has required scopes for operation

#### Issue: Insufficient permissions
**Symptoms:** "Forbidden" error or missing data
**Cause:** API key missing required scopes
**Solution:**
- Review key scopes in Attio: Settings > Developers > API Keys
- Create new key with required scopes (`record:read`, `record:write`, etc.)
- For notes: ensure `note:read` and `note:write` scopes
- Workspace admin may need to grant additional permissions

#### Issue: Duplicate record created
**Symptoms:** Same company/person appears multiple times
**Cause:** No deduplication on create, or different field values
**Solution:**
- Search before creating to check for existing records
- Use primary identifier (domain for companies, email for people)
- Consider using update-or-create pattern
- Merge duplicates manually in Attio UI

## Resources

- **references/api-guide.md** - Complete API documentation
- **references/integration.md** - CRM integration patterns

## Integration Patterns

### Meeting Notes to CRM
**Skills:** transcript-search → attio-crm
**Use case:** Add meeting summaries to company records
**Flow:**
1. Search transcript-search for client meetings
2. Extract key points, action items, and summary
3. Create note on Attio company record with meeting details

### Research to CRM
**Skills:** parallel-research → attio-crm
**Use case:** Enrich CRM records with research data
**Flow:**
1. Run parallel-research on company for latest info
2. Extract funding, team size, tech stack, news
3. Update Attio company record with enriched fields

### Voice Agent to CRM
**Skills:** voice-agents → attio-crm
**Use case:** Log AI call summaries to CRM
**Flow:**
1. Voice agent completes discovery or feedback call
2. Extract call summary and key insights
3. Add note to Attio record with call summary and next steps
