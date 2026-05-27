---
name: contact-to-email
description: |
  Find and verify email addresses for contacts. Handles three common starting points:
  name + company, LinkedIn URL, or name + domain (with pattern matching).

  Triggers:
  - "find email for [name] at [company]"
  - "get email addresses for my contact list"
  - "email enrichment"
  - "I have LinkedIn URLs and need emails"

  Requires: Deepline CLI — https://code.deepline.com
---

# Contact → Email

Three workflows depending on what you already have. Always validate at the end.

## Which workflow to use?

| Starting data | Use |
|---|---|
| First name + last name + company | [Workflow A](#workflow-a-name--company) |
| LinkedIn profile URL | [Workflow B](#workflow-b-linkedin-url) |
| First name + last name + domain | [Workflow C](#workflow-c-pattern-matching) |

---

## Workflow A: Name + Company

Tries Apollo → Crustdata → PDL in order, stops at first match:

```bash
deepline enrich --input leads.csv --in-place --rows 0:1 \
  --with-waterfall "email" \
  --type email \
  --result-getters '["data.email","email","data.0.email"]' \
  --with 'apollo=apollo_people_match:{"first_name":"{{First Name}}","last_name":"{{Last Name}}","organization_name":"{{Company}}"}' \
  --with 'crustdata=crustdata_person_enrichment:{"linkedinProfileUrl":"{{LinkedIn}}","fields":["email","current_employers"],"enrichRealtime":true}' \
  --with 'pdl=peopledatalabs_enrich_contact:{"first_name":"{{First Name}}","last_name":"{{Last Name}}","domain":"{{Company Domain}}"}' \
  --end-waterfall \
  --with 'validation=leadmagic_email_validation:{"email":"{{email}}"}'
```

Required columns: `First Name`, `Last Name`, `Company`

Optional columns: `LinkedIn`, `Company Domain` (improves match rate)

---

## Workflow B: LinkedIn URL

When you have LinkedIn profile URLs but no email:

```bash
deepline enrich --input leads.csv --in-place --rows 0:1 \
  --with-waterfall "email" \
  --type email \
  --result-getters '["data.0.email","data.email","emails.0.address"]' \
  --with 'apollo=apollo_people_match:{"first_name":"{{First Name}}","last_name":"{{Last Name}}","organization_name":"{{Company}}","domain":"{{Company Domain}}"}' \
  --with 'crustdata=crustdata_person_enrichment:{"linkedinProfileUrl":"{{LinkedIn URL}}","fields":["email","current_employers"],"enrichRealtime":true}' \
  --with 'pdl=peopledatalabs_enrich_contact:{"linkedin_url":"{{LinkedIn URL}}","first_name":"{{First Name}}","last_name":"{{Last Name}}","domain":"{{Company Domain}}"}' \
  --end-waterfall \
  --with 'validation=leadmagic_email_validation:{"email":"{{email}}"}'
```

Required columns: `LinkedIn URL`

Optional columns: `First Name`, `Last Name`, `Company`, `Company Domain`

---

## Workflow C: Pattern matching

When you have name + domain but no LinkedIn. Generates common email patterns (first.last, flast, etc.) and validates each. Most cost-effective for bulk lists:

```bash
deepline enrich --input leads.csv --in-place --rows 0:1 \
  --with 'patterns=run_javascript:{"code":"const f=(row[\"First Name\"]||\"\").trim().toLowerCase(); const l=(row[\"Last Name\"]||\"\").trim().toLowerCase(); const d=(row[\"Domain\"]||\"\").trim().toLowerCase(); if(!f||!l||!d) return {}; return {p1:`${f}.${l}@${d}`,p2:`${f[0]}${l}@${d}`,p3:`${f}${l[0]}@${d}`,p4:`${f}@${d}`};"}' \
  --with-waterfall "email" \
  --type email \
  --result-getters '["data.email","email","data.0.email"]' \
  --with 'v1=leadmagic_email_validation:{"email":"{{patterns.p1}}"}' \
  --with 'v2=leadmagic_email_validation:{"email":"{{patterns.p2}}"}' \
  --with 'v3=leadmagic_email_validation:{"email":"{{patterns.p3}}"}' \
  --with 'v4=leadmagic_email_validation:{"email":"{{patterns.p4}}"}' \
  --with 'apollo=apollo_people_match:{"first_name":"{{First Name}}","last_name":"{{Last Name}}","organization_name":"{{Company}}","domain":"{{Domain}}"}' \
  --end-waterfall \
  --with 'final_validation=leadmagic_email_validation:{"email":"{{email}}"}'
```

Required columns: `First Name`, `Last Name`, `Domain`

---

## Understanding validation results

After validation, check `validation.data.email_status`:

| Status | Meaning | Action |
|---|---|---|
| `valid` | Deliverable | Use for outreach |
| `catch_all` | Domain accepts all — inconclusive | Use with caution |
| `invalid` | Not deliverable | Skip or try another workflow |
| `unknown` | Could not verify | Try pattern matching as backup |

> **Note:** `catch_all` is not a failure — many business domains use catch-all. Continue with outreach, just expect slightly higher bounce rates.

---

## Scale after pilot

```bash
# After reviewing --rows 0:1 output, run remaining rows:
deepline enrich --input leads.csv --in-place --rows 1: \
  # ... same flags as pilot
```

## Get started

Sign up and get your API key at [code.deepline.com](https://code.deepline.com).

```bash
npm install -g @deepline/cli
deepline auth login
```
