---
description: Find 5-10 key decision makers per company with verified emails using Parallel, Apollo, and MillionVerifier APIs
---

# Lead Enrichment

Use this skill when: user asks to "enrich leads", "find decision makers", "get contacts for companies", "find emails", or any request to turn a company list into actionable contacts.

---

## Overview

This skill takes a list of companies and finds key decision makers with:
- Full name
- Job title
- Work email (verified)
- LinkedIn URL

Uses a 3-stage pipeline:
1. **Parallel API** - Primary contact discovery
2. **Apollo API** - Email enrichment fallback
3. **MillionVerifier** - Email verification

---

## Pre-flight Checks

### Required API Keys

Before running enrichment, verify these keys exist:

| Key | Service | Get it at |
|-----|---------|-----------|
| `PARALLEL_API_KEY` | Parallel (contact discovery) | platform.parallel.ai |
| `APOLLO_API_KEY` | Apollo (email enrichment) | app.apollo.io |
| `MILLIONVERIFIER_API_KEY` | MillionVerifier (verification) | app.millionverifier.com |

**If keys are missing:**
1. Ask user which keys they have
2. Guide them to sign up for missing services
3. Explain what each service does and approximate cost
4. Have them add keys to `.env` file

### Required Input

- **Company list**: CSV or JSON with at minimum:
  - Company name
  - Website (for domain extraction)
- **Optional**: ICP segment, priority score, target titles

---

## Stage 1: Contact Discovery (Parallel API)

### Purpose
Find 5-10 decision makers per company from public sources.

### Process
1. For each company, call Parallel Task API with:
   - Company name
   - Website domain
   - Target titles to find

2. Extract from results:
   - Person name
   - Title
   - Email (if public)
   - LinkedIn URL

### Target Titles (customize per ICP)

**Executive level:**
- Founder, CEO, President, Owner
- CTO, CIO, COO, CFO

**VP level:**
- VP Supply Chain, VP Procurement, VP Sourcing
- VP Operations, VP Product, VP Engineering

**Director level:**
- Director Supply Chain, Director Procurement
- Director Operations, Director Product

**Manager level:**
- Product Manager, Procurement Manager
- Merchandise Manager, Buyer

### Parallel API Call

```python
from parallel_web import Parallel

client = Parallel(api_key=os.getenv("PARALLEL_API_KEY"))

result = client.task.create(
    prompt=f"""Find up to 5 key decision makers at {company_name}.
    Website: {website}

    For each person, extract:
    - Full name
    - Job title
    - Work email (if available)
    - LinkedIn URL

    Target titles: {target_titles}
    """,
    processor="base"  # or "core", "pro"
)
```

### Output

```json
{
  "company": "Example Corp",
  "contacts": [
    {
      "name": "John Smith",
      "title": "VP Supply Chain",
      "email": "john.smith@example.com",
      "linkedin": "linkedin.com/in/johnsmith"
    }
  ]
}
```

---

## Stage 2: Email Enrichment (Apollo API)

### Purpose
Find emails for contacts that Parallel didn't return emails for.

### Process
1. Filter contacts where email is null/empty
2. For each contact, call Apollo People Match:
   - First name
   - Last name
   - Company domain (extracted from website)

3. Apollo returns:
   - Work email
   - LinkedIn URL (backup)
   - Verified title

### Apollo API Call

```python
import requests

def apollo_enrich(first_name, last_name, domain):
    url = "https://api.apollo.io/v1/people/match"
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "X-Api-Key": os.getenv("APOLLO_API_KEY")
    }
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "domain": domain
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()
```

### Rate Limits
- 0.5 sec between requests (be gentle)
- 60 sec wait on 429 errors
- Bulk endpoint available for up to 10 at once

---

## Stage 3: Email Verification (MillionVerifier)

### Purpose
Verify all discovered emails before outreach.

### Process
1. Collect all emails (from Parallel + Apollo)
2. Verify each with MillionVerifier API
3. Score quality: good, bad, risky, unknown

### MillionVerifier API Call

```python
import requests

def verify_email(email):
    url = f"https://api.millionverifier.com/api/v3/?api={api_key}&email={email}"
    response = requests.get(url)
    return response.json()
```

### Response Fields

| Field | Values | Meaning |
|-------|--------|---------|
| `quality` | good, bad, risky, unknown | Overall quality |
| `result` | ok, catch_all, unknown, invalid | Specific result |
| `resultcode` | 1, 2, 3, 6 | Numeric code |
| `role` | true/false | Is it a role address (info@, sales@) |
| `free` | true/false | Is it a free email provider |

### Quality Interpretation

| Quality | Action |
|---------|--------|
| **good** | Safe to send |
| **risky** | Send with caution, may bounce |
| **bad** | Do not send |
| **unknown** | Manual review |

### Flag Role Addresses

Role addresses (info@, sales@, support@) have lower response rates. Flag them:
- Still usable but deprioritize
- Look for personal emails instead
- Note in output for campaign decisions

---

## Progress Tracking

### Resume Capability

Store progress in JSONL files for resumability:

```
leads/progress/
  parallel.jsonl    - Company + contacts + status
  apollo.jsonl      - Contact + email + status
  millionverifier.jsonl - Email + quality + status
```

### JSONL Format

```jsonl
{"company": "Example Corp", "status": "done", "contacts": [...]}
{"company": "Another Inc", "status": "done", "contacts": [...]}
```

### Resume Logic

Before processing:
1. Load existing progress file
2. Build set of already-processed items
3. Skip items in the set
4. Append new results to progress file

---

## Output Format

### Final CSV

```csv
company,segment,website,person1_name,person1_title,person1_email,person1_linkedin,person2_name,person2_title,person2_email,person2_linkedin,...
```

Up to 5 contacts per company (person1 through person5).

### Final JSON

```json
{
  "company": "Example Corp",
  "segment": "Tier1_Gloves",
  "website": "example.com",
  "contacts": [
    {
      "name": "John Smith",
      "title": "VP Supply Chain",
      "email": "john.smith@example.com",
      "email_quality": "good",
      "linkedin": "linkedin.com/in/johnsmith"
    }
  ]
}
```

---

## Execution Flow

### Option A: Use Existing Scripts

If `pga-2026/scripts/enrichment/` exists with:
- `enrich_contacts_parallel.py`
- `enrich_emails_apollo.py`
- `verify_emails_millionverifier.py`

Run them in sequence:
```bash
uv run pga-2026/scripts/enrichment/enrich_contacts_parallel.py
uv run pga-2026/scripts/enrichment/enrich_emails_apollo.py
uv run pga-2026/scripts/enrichment/verify_emails_millionverifier.py
```

### Option B: Manual Enrichment

For small lists (under 10 companies):
1. Use Parallel MCP tool directly for contact discovery
2. Use Apollo API calls for missing emails
3. Use MillionVerifier for verification

### Option C: Create New Scripts

For new campaigns without existing scripts:
1. Create script directory: `[campaign]/scripts/enrichment/`
2. Create 3 stage scripts based on templates
3. Create progress tracking directory
4. Run pipeline

---

## Error Handling

### API Failures

| Error | Action |
|-------|--------|
| 401 Unauthorized | Check API key is valid |
| 429 Rate Limited | Wait 60 sec, retry |
| 500 Server Error | Wait, retry up to 3 times |
| Timeout | Retry with longer timeout |

### Missing Data

| Issue | Fallback |
|-------|----------|
| No contacts found (Parallel) | Manual web search |
| No email found (Apollo) | Try LinkedIn outreach |
| Bad email (MillionVerifier) | Remove from list |

---

## Quality Checklist

Before delivering enriched list:

- [ ] All companies processed (check progress files)
- [ ] Emails verified (good/risky/bad flagged)
- [ ] Role addresses flagged (info@, sales@)
- [ ] LinkedIn URLs present for contacts
- [ ] Output format matches user request (CSV or JSON)
- [ ] No duplicate contacts across companies

---

## Cost Awareness

Approximate costs (check current pricing):

| Service | Cost |
|---------|------|
| Parallel | ~$0.01-0.05 per task |
| Apollo | Credits-based, varies by plan |
| MillionVerifier | ~$0.0003 per email |

For 100 companies with 5 contacts each:
- Parallel: 100 tasks
- Apollo: ~200 email lookups (assuming 40% need enrichment)
- MillionVerifier: ~500 verifications

---

*This skill is generic - works for any campaign, not just Performance Leather.*
