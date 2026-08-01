---
name: nyc-hpd
description: Look up HPD violations, complaints, and building registration for NYC residential buildings. Use when the user asks about housing-code violations, tenant complaints, or HPD registration at an address. NYC only; for DOB and ECB violations use /nyc-dob-violations.
allowed-tools:
  - WebFetch
  - Write
  - Read
  - Bash
---

# /nyc-hpd — HPD Violations, Complaints & Registration

Look up HPD (Housing Preservation & Development) violations, complaints, and building registration for NYC residential buildings. Only applies to residential building classes. No API key required.

## Usage

```
/nyc-hpd 1055 Bergen Street, Brooklyn
/nyc-hpd 3012120065          (BBL)
/nyc-hpd 3030348             (BIN)
```

## Steps 1–2: Parse Input & Resolve BBL

Read `../nyc-property-report/pluto-resolution.md` (shared by all 7 NYC due-diligence skills) and follow it: parse the input (address, BBL, or BIN — e.g. "1055 Bergen Street, Brooklyn") and resolve via PLUTO. HPD queries key on boro/block/lot, so BIN resolution is only needed when the user's input was a BIN.

### Check Building Class

**Before querying HPD**, check `bldgclass` from PLUTO. HPD only applies to residential buildings — classes starting with A, B, C, D, R, or S.

If the building class does NOT start with one of those letters, print:
> "Building class {X} — HPD records not applicable (non-residential)."

And stop. Do not query HPD APIs.

## Step 3: Query HPD Datasets

Dataset IDs and field names are canonical in `../nyc-property-report/socrata-reference.md` — on any disagreement, the reference wins.

**IMPORTANT:** HPD violations/registrations use `boroid` (not `borough`). And `block`/`lot` are separate fields — not a combined BBL.

### HPD Violations
```
https://data.cityofnewyork.us/resource/wvxf-dwi5.json?$where=boroid='{boro}' AND block='{block}' AND lot='{lot}'&$order=inspectiondate DESC&$limit=50
```
Key fields: `violationid`, `class` (violation class — NOT `violationclass`), `inspectiondate`, `approveddate`, `originalcertifybydate`, `novdescription`, `currentstatus`

### Open HPD Violations
```
https://data.cityofnewyork.us/resource/csn4-vhvf.json?$where=boroid='{boro}' AND block='{block}' AND lot='{lot}'
```
Pre-filtered to currently open violations.

### Complaints

**Note:** The complaints dataset uses `borough` (text like "MANHATTAN", "BRONX", "BROOKLYN", "QUEENS", "STATEN ISLAND") — NOT `boroid`. Map boro codes: 1→MANHATTAN, 2→BRONX, 3→BROOKLYN, 4→QUEENS, 5→STATEN ISLAND.

```
https://data.cityofnewyork.us/resource/ygpa-z7cr.json?$where=borough='{BOROUGH_NAME}' AND block='{block}' AND lot='{lot}'&$order=received_date DESC&$limit=30
```
Key fields: `complaint_id`, `received_date`, `complaint_status`, `complaint_status_date`, `major_category`, `minor_category`, `problem_status`

### Registrations
```
https://data.cityofnewyork.us/resource/tesw-yqqr.json?$where=boroid='{boro}' AND block='{block}' AND lot='{lot}'
```
Key fields: `registrationid`, `buildingid`, `bin`, `registrationenddate`, `lastregistrationdate`

**Note:** The registrations dataset has NO owner-name fields. Get owner/agent names from Registration Contacts (`feu5-w2e2`), keyed by `registrationid`:
```
https://data.cityofnewyork.us/resource/feu5-w2e2.json?$where=registrationid='{registrationid}'
```
Key fields: `type` (CorporateOwner / Agent / HeadOfficer / IndividualOwner), `firstname`, `lastname`, `corporationname`

## Step 4: Print Results

```markdown
## HPD — {Address}

### Registration
| Field | Value |
|-------|-------|
| Registration ID | ... |
| Owner | {corporationname or firstname lastname, from registration contacts} |
| Registration Expiry | YYYY-MM-DD |

### ⚠ Open Violations: {count}
**Class C (Immediately Hazardous):** {count} ⚠
**Class B (Hazardous):** {count}
**Class A (Non-Hazardous):** {count}

| Violation ID | Class | Inspection Date | Description | Certify By |
|-------------|-------|-----------------|-------------|------------|
| ... | C ⚠ | YYYY-MM-DD | ... | YYYY-MM-DD |

### All Violations ({count} total, showing 50 most recent)
| Violation ID | Class | Inspection Date | Approved Date | Description |
|-------------|-------|-----------------|---------------|-------------|

### Recent Complaints ({count} total, showing 30 most recent)
| Complaint ID | Received | Category | Status | Status Date |
|-------------|----------|--------|-------------|

Source: [HPD Violations](https://data.cityofnewyork.us/Housing-Development/Housing-Maintenance-Code-Violations/wvxf-dwi5) | [HPD Complaints](https://data.cityofnewyork.us/Housing-Development/Housing-Maintenance-Code-Complaints-and-Problems/ygpa-z7cr)
```

If no results: "No HPD violations, complaints, or registrations found for this property."

### Conventions
- All dates: YYYY-MM-DD
- Class C violations always flagged with ⚠ (immediately hazardous — must be corrected within 24 hours)
- Open/active items listed first
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
