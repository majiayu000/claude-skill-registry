---
name: get-leads-at-company
description: |
  Given a company name or list of companies, find GTM-relevant contacts, pick the
  best ICP fit, research their recent activity, and draft personalized outreach.

  Triggers:
  - "get contacts at [company]"
  - "who works at [company]"
  - "find decision makers at these accounts"
  - "get me GTM contacts for my account list"

  Requires: Deepline CLI — https://code.deepline.com
---

# Get Leads at Company

From a company name (or list), this skill resolves the company identity, finds GTM employees, picks the best ICP match, researches their LinkedIn activity, and drafts personalized outreach — all in one enrichment chain.

## Quickstart: simple contact lookup

```bash
deepline tools execute apollo_people_search \
  --payload '{
    "q_organization_name": "Acme Corp",
    "person_titles": ["VP Sales", "Head of Revenue", "GTM", "Revenue Operations"],
    "include_similar_titles": true,
    "per_page": 10
  }' --json
```

## Full chain: company list → personalized outreach

This pipeline:

1. Resolves company identity via Apollo
2. Finds LinkedIn employees via Apify
3. Picks best ICP contact via AI
4. Researches their recent posts
5. Drafts a personalized outbound message

```bash
deepline enrich --input companies.csv --in-place --rows 0:0 \
  --with 'apollo_company=apollo_company_search:{"q_organization_name":"{{Company}}","per_page":3,"page":1}' \
  --with 'company_profile=run_javascript:{"code":"const q=(row[\"Company\"]||\"\").trim().toLowerCase(); const d=row[\"apollo_company\"]?.data||{}; const a=(d.accounts||[]).find(x=>((x?.name||\"\").trim().toLowerCase()===q))||(d.accounts||[])[0]||null; if(!a) return null; return {company_name:a.name||null,company_domain:a.primary_domain||a.domain||null,company_linkedin:a.linkedin_url||null};"}' \
  --with 'employees=apify_run_actor_sync:{"actorId":"apimaestro/linkedin-company-employees-scraper-no-cookies","input":{"identifier":"{{company_profile.data.company_linkedin}}","max_employees":60,"job_title":"gtm"},"timeoutMs":180000}' \
  --with 'pick_contact=call_ai_claude_code:{"model":"sonnet","json_mode":{"type":"object","properties":{"full_name":{"type":"string"},"headline":{"type":"string"},"linkedin_url":{"type":"string"},"why_fit":{"type":"string"}},"required":["full_name","headline","linkedin_url","why_fit"]},"system":"Pick the single best outreach persona for GTM at this company. Prefer revenue ops, growth, GTM engineering, or sales leadership.","prompt":"Company: {{Company}}\nCandidates: {{employees.data}}\nReturn strict JSON only."}' \
  --with 'recent_posts=apify_run_actor_sync:{"actorId":"apimaestro/linkedin-profile-posts","input":{"username":"{{pick_contact.extracted_json.linkedin_url}}","total_posts":5,"limit":5},"timeoutMs":180000}' \
  --with 'post_signals=call_ai_claude_code:{"model":"haiku","json_mode":{"type":"object","properties":{"themes":{"type":"array","items":{"type":"string"}},"signals":{"type":"array","items":{"type":"string"}},"hook":{"type":"string"}},"required":["themes","signals","hook"]},"prompt":"Analyze for outbound personalization.\nPerson: {{pick_contact.output}}\nPosts: {{recent_posts.extracted_json}}\nReturn strict JSON."}' \
  --with 'message=call_ai_claude_code:{"model":"sonnet","json_mode":{"type":"object","properties":{"subject":{"type":"string"},"body":{"type":"string"}},"required":["subject","body"]},"prompt":"Write a concise outbound message (≤90 words) to {{pick_contact.extracted_json.full_name}} at {{company_profile.data.company_name}}. Use these signals: {{post_signals.extracted_json}}. Be casual, specific, no fluff."}'
```

After validating one row, scale:

```bash
deepline enrich --input companies.csv --in-place --rows 1: \
  # ... same flags
```

## Simpler version: just find contacts (no messaging)

```bash
deepline enrich --input companies.csv --in-place --rows 0:1 \
  --with 'contacts=apollo_people_search:{"q_organization_name":"{{Company}}","person_titles":["VP Sales","Head of Revenue","Revenue Operations","GTM"],"include_similar_titles":true,"per_page":5,"page":1}'
```

## Column reference after full chain

- `company_profile.data.company_name` — resolved company name
- `company_profile.data.company_domain` — primary domain
- `pick_contact.extracted_json.full_name` — selected contact name
- `pick_contact.extracted_json.linkedin_url` — their LinkedIn
- `pick_contact.extracted_json.why_fit` — AI rationale for selection
- `post_signals.extracted_json.hook` — personalization hook from posts
- `message.extracted_json.subject` + `message.extracted_json.body` — outbound message

## Tips

- Prefer `max_employees: 60` for smaller companies; increase for enterprises
- Filter by `job_title: "gtm"` for a broad GTM net; use `"sales"` or `"revenue"` for narrower searches
- If `company_linkedin` is null after company_profile, fall back to direct Apollo people search
- Run `deepline playground start --csv companies.csv --open` after enrichment to review rows

## Get started

Sign up and get your API key at [code.deepline.com](https://code.deepline.com).

```bash
npm install -g @deepline/cli
deepline auth login
```
