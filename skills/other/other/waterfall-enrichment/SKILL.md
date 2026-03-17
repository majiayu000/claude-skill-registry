---
name: waterfall-enrichment
description: |
  Enrich a CSV with any data field using a waterfall pattern: try multiple providers
  in sequence, stop at the first successful match. Prevents paying for duplicate
  lookups and maximizes fill rates.

  Triggers:
  - "enrich my lead list"
  - "add [field] to my CSV"
  - "waterfall enrichment"
  - "try multiple providers to find [data]"

  Requires: Deepline CLI — https://code.deepline.com
---

# Waterfall Enrichment

The waterfall pattern runs multiple enrichment providers in sequence and stops as soon as one returns a valid result. This maximizes coverage while minimizing cost — you only pay for lookups that actually run.

## Key concepts

- `--with-waterfall <NAME>` — start a waterfall block named `<NAME>`
- `--type` — what you're looking for: `email`, `phone`, `linkedin`, `first_name`, `last_name`, `full_name`
- `--result-getters` — JSON path(s) where to find the value in provider output
- `--end-waterfall` — close the block; the waterfall name becomes a column with the resolved value
- After `--end-waterfall`, use `{{<waterfall_name>}}` to reference the resolved scalar

## Always pilot first

```bash
deepline enrich --input leads.csv --in-place --rows 0:1 \
  --with-waterfall "email" \
  --type email \
  --result-getters '["data.email","email","data.0.email"]' \
  --with 'provider_a=tool_name:{"param":"{{Column}}"}' \
  --with 'provider_b=tool_name:{"param":"{{Column}}"}' \
  --end-waterfall
```

Review output, then scale to `--rows 1:` for remaining rows.

## Phone waterfall

```bash
deepline enrich --input leads.csv --in-place --rows 0:1 \
  --with-waterfall "phone" \
  --type phone \
  --result-getters '["data.phone","phone","mobile","data.mobile"]' \
  --with 'mobile_finder=leadmagic_mobile_finder:{"email":"{{Email}}","first_name":"{{First Name}}","last_name":"{{Last Name}}","company":"{{Company}}"}' \
  --end-waterfall
```

## Email waterfall (name + company)

```bash
deepline enrich --input leads.csv --in-place --rows 0:1 \
  --with-waterfall "email" \
  --type email \
  --result-getters '["data.email","email","data.0.email"]' \
  --with 'apollo_match=apollo_people_match:{"first_name":"{{First Name}}","last_name":"{{Last Name}}","organization_name":"{{Company}}"}' \
  --with 'crust_profile=crustdata_person_enrichment:{"linkedinProfileUrl":"{{LinkedIn}}","fields":["email","current_employers"],"enrichRealtime":true}' \
  --with 'pdl_enrich=peopledatalabs_enrich_contact:{"first_name":"{{First Name}}","last_name":"{{Last Name}}","domain":"{{Company Domain}}"}' \
  --end-waterfall \
  --with 'email_validation=leadmagic_email_validation:{"email":"{{email}}"}'
```

## LinkedIn URL waterfall

```bash
deepline enrich --input leads.csv --in-place --rows 0:1 \
  --with-waterfall "linkedin" \
  --type linkedin \
  --result-getters '["linkedin_url","data.linkedin_url","data.0.linkedin_url"]' \
  --with 'apollo_match=apollo_people_match:{"first_name":"{{First Name}}","last_name":"{{Last Name}}","organization_name":"{{Company}}"}' \
  --with 'pdl_identify=peopledatalabs_person_identify:{"first_name":"{{First Name}}","last_name":"{{Last Name}}","company":"{{Company}}"}' \
  --end-waterfall
```

## Hard rules

- Always end with `leadmagic_email_validation` when the waterfall resolves email
- Use `--rows 0:1` pilot before any full run
- Do not reuse an existing output CSV path
- Chain one waterfall at a time; close `--end-waterfall` before starting another
- Use canonical `--type` values: `email | phone | linkedin | first_name | last_name | full_name`

## After a waterfall run

The Playground auto-opens for inspection:

```bash
deepline playground start --csv leads.csv --open
```

Use `--rows 0:1` in the playground to re-run a single block for debugging.

## Get started

Sign up and get your API key at [code.deepline.com](https://code.deepline.com).

```bash
npm install -g @deepline/cli
deepline auth login
```
