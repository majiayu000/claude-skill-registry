---
name: nyc-bsa
description: Look up Board of Standards and Appeals (BSA) variances and special permits for any NYC property. Use when checking whether a lot carries zoning relief — variances, special permits, appeals — that modifies its as-of-right envelope. NYC only; for base zoning controls use /zoning-analysis-nyc.
allowed-tools:
  - WebFetch
  - Write
  - Read
  - Bash
---

# /nyc-bsa — BSA Variances & Special Permits

Look up Board of Standards and Appeals (BSA) applications, variances, and special permits for any NYC property. Records available from 1998 to present. No API key required.

## Usage

```
/nyc-bsa 120 Broadway, Manhattan
/nyc-bsa 1000770001          (BBL)
/nyc-bsa 1001389             (BIN)
```

## Steps 1–2: Parse Input & Resolve BBL

Read `../nyc-property-report/pluto-resolution.md` (shared by all 7 NYC due-diligence skills) and follow it: parse the input (address, BBL, or BIN) and resolve via PLUTO. BSA queries key on BBL; BIN resolution is only needed when the user's input was a BIN.

## Step 3: Query BSA Applications

Dataset IDs and field names are canonical in `../nyc-property-report/socrata-reference.md` — on any disagreement, the reference wins.

Query by BBL first:
```
https://data.cityofnewyork.us/resource/yvxd-uipr.json?$where=bbl='{BBL}'&$order=date DESC
```

If no results, try address fallback:
```
https://data.cityofnewyork.us/resource/yvxd-uipr.json?$where=upper(street_name) LIKE '%{STREET}%' AND borough='{BOROUGH}'&$order=date DESC
```

Key fields: `application`, `section`, `status`, `date`, `street_number`, `street_name`, `bbl`, `borough`, `decisions_url`, `project_description`

## Step 4: Print Results

```markdown
## BSA Variances & Special Permits — {Address}

| Application # | Section | Status | Date | Description | Decisions |
|---------------|---------|--------|------|-------------|-----------|
| {application} | {section} | {status} | YYYY-MM-DD | {project_description} | {decisions_url} |

**Note:** Approved variances remain with the land. Check if conditions affect proposed work.

Source: [BSA Applications](https://data.cityofnewyork.us/City-Government/BSA-Applications-Status/yvxd-uipr)
```

If no applications found: "No BSA applications found for this property (records from 1998-present)."

### Conventions
- All dates: YYYY-MM-DD
- If Socrata returns empty array: "No results found"
- If HTTP error: note it and suggest checking the address
- If the user requests, write results to a file

## Final Step: Disclaimer + Marker (required)

This skill produces regulatory output. End every report this skill produces — printed in chat or saved to a file — with the canonical disclaimer block from `rules/professional-disclaimer.md`, followed by one blank line and the machine-readable marker, exactly as shown:

```markdown
> **Disclaimer:** This is an AI-generated analysis for preliminary planning purposes. All findings must be verified by a licensed professional before use in design, permitting, or regulatory submissions.

<!-- architecture-studio:requires-disclaimer -->
```

The marker is a single end-of-file sentinel — it appears exactly once, as the last line of the report. The `post-write-disclaimer-check` hook parses saved `.md` reports for the marker and blocks the write if the canonical disclaimer block is missing.
