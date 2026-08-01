---
name: nyc-property-report
description: Combined NYC property report — landmarks, DOB permits, violations, ACRIS records, HPD, and BSA variances in one document. Use when the user asks for a full property report, complete due diligence, or to "pull everything" on an NYC address. For a single dataset use the individual NYC skills.
allowed-tools:
  - WebFetch
  - Write
  - Read
  - Bash
---

# /nyc-property-report — Combined NYC Property Report

Runs all 6 NYC property data lookups and produces a combined report. For individual lookups, use the standalone skills:
- `/nyc-landmarks` — LPC landmark & historic district check
- `/nyc-dob-permits` — DOB permit & filing history
- `/nyc-dob-violations` — DOB & ECB violations
- `/nyc-acris` — ACRIS property transaction records
- `/nyc-hpd` — HPD violations, complaints & registration
- `/nyc-bsa` — BSA variances & special permits

No API key required — all queries use NYC Open Data (Socrata) with PLUTO for address resolution.

## Project Dossier

If `PROJECT.md` exists in the working directory, read it before fetching — prior lookups may already be on file. After completing, append identity facts (address, BBL, ownership), landmark status, and an open-violations summary to its **Identity** and **Zoning** sections. Update values in place (the dossier holds current state, not history), every entry with a source and date. No `PROJECT.md`? Skip silently — or mention `/project-dossier init` if the user is clearly starting a project.

## Usage

```
/nyc-property-report 120 Broadway, Manhattan
/nyc-property-report 1000770001          (BBL)
/nyc-property-report 1001389             (BIN)
```

## Steps 1–2: Parse Input & Resolve BBL/BIN

Read `pluto-resolution.md` (in this skill's directory) and follow it: parse the input (address, BBL, or BIN), resolve via PLUTO, and resolve BIN via Building Footprints.

**This skill's extras:** in addition to the base PLUTO field set, store `zipcode`, `cd`, `bldgarea`, `unitstotal`, `histdist`, `numbldgs`.

## Step 3: Query All 6 Domains

Query each domain in sequence. If any query fails, note the error and continue with the next domain.

Read `socrata-reference.md` (in this skill's directory) — it is the single source of truth for every dataset ID and field name below. If a query here ever disagrees with it, the reference wins.

### Domain 1: Landmarks

By BBL: `https://data.cityofnewyork.us/resource/buis-pvji.json?bbl={BBL}`
Fallback by block + lot (NOT zero-padded): `https://data.cityofnewyork.us/resource/buis-pvji.json?$where=block='{BLOCK}' AND lot='{LOT}' AND borough='{BOROUGH}'`

Also check PLUTO `histdist` field — if set, property is in a historic district.

Key fields: `lpc_name`, `lpc_lpnumb`, `desdate`, `landmarkty`, `lpc_sitede`, `lpc_sitest`, `lpc_altern`, `address`, `url_report`

### Domain 2: DOB Permits

**IMPORTANT:** Legacy datasets use `bin__` (double underscore). DOB NOW uses `bin`.

Legacy permits: `https://data.cityofnewyork.us/resource/ipu4-2q9a.json?$where=bin__='{BIN}'&$order=issuance_date DESC&$limit=30`
Legacy filings: `https://data.cityofnewyork.us/resource/ic3t-wcy2.json?$where=bin__='{BIN}'&$order=latest_action_date DESC&$limit=30`
DOB NOW permits: `https://data.cityofnewyork.us/resource/rbx6-tga4.json?$where=bin='{BIN}'&$order=approved_date DESC&$limit=30`
DOB NOW filings: `https://data.cityofnewyork.us/resource/w9ak-ipjd.json?$where=bin='{BIN}'&$order=filing_date DESC&$limit=30`

Merge, sort by date DESC, group by job type (NB, A1, A2, A3, DM, Other).

### Domain 3: DOB Violations

DOB violations: `https://data.cityofnewyork.us/resource/3h2n-5cm9.json?$where=bin='{BIN}'&$order=issue_date DESC&$limit=50`
ECB violations: `https://data.cityofnewyork.us/resource/6bgk-3dad.json?$where=bin='{BIN}'&$order=issue_date DESC&$limit=50`
Active violations: `https://data.cityofnewyork.us/resource/sjhj-bc8q.json?$where=bin='{BIN}'`

Flag open violations with ⚠. Show ECB penalties.

### Domain 4: ACRIS

**Requires BBL** (not BIN). Uses separate borough/block/lot fields.

Step A — Legals: `https://data.cityofnewyork.us/resource/8h5j-fqxa.json?borough={boro}&block={block}&lot={lot}&$order=good_through_date DESC&$limit=20`
Step B — Master: `https://data.cityofnewyork.us/resource/bnx9-e6tj.json?$where=document_id IN ('{id1}','{id2}',...)&$order=document_date DESC` (fields: `document_date`, `document_amt`, `recorded_datetime`)
Step C — Parties: `https://data.cityofnewyork.us/resource/636b-3b5g.json?$where=document_id IN ('{id1}','{id2}',...)`
Step D — Doc codes: `https://data.cityofnewyork.us/resource/7isb-wh4c.json?$limit=200`

Join by document_id. Party type 1=Grantor, 2=Grantee. Group by doc type (Deeds, Mortgages, Other).

### Domain 5: HPD

**First check `bldgclass`** — HPD only applies to residential (classes starting with A, B, C, D, R, S). If non-residential, skip with note.

**Uses `boroid`** (not `borough`) and separate block/lot fields.

Violations: `https://data.cityofnewyork.us/resource/wvxf-dwi5.json?$where=boroid='{boro}' AND block='{block}' AND lot='{lot}'&$order=inspectiondate DESC&$limit=50`
Open violations: `https://data.cityofnewyork.us/resource/csn4-vhvf.json?$where=boroid='{boro}' AND block='{block}' AND lot='{lot}'`
Complaints (uses `borough` as TEXT — "MANHATTAN", "BROOKLYN", … — not `boroid`): `https://data.cityofnewyork.us/resource/ygpa-z7cr.json?$where=borough='{BOROUGH_NAME}' AND block='{block}' AND lot='{lot}'&$order=received_date DESC&$limit=30`
Registrations: `https://data.cityofnewyork.us/resource/tesw-yqqr.json?$where=boroid='{boro}' AND block='{block}' AND lot='{lot}'`
Registration contacts (owner names — registrations dataset has none): `https://data.cityofnewyork.us/resource/feu5-w2e2.json?$where=registrationid='{registrationid}'`

Flag Class C violations with ⚠ (immediately hazardous).

### Domain 6: BSA

By BBL: `https://data.cityofnewyork.us/resource/yvxd-uipr.json?$where=bbl='{BBL}'&$order=date DESC`
Address fallback: `https://data.cityofnewyork.us/resource/yvxd-uipr.json?$where=upper(street_name) LIKE '%{STREET}%' AND borough='{BOROUGH}'&$order=date DESC`

## Step 4: Write Report

Write to working directory as `property-{address-slug}.md`.

```markdown
# NYC Property Report — {Address}

**Generated:** {date}
**BBL:** {bbl} | **BIN:** {bin}
**Source:** NYC Open Data (Socrata)

---

## 1. Property Identification

| Field | Value |
|-------|-------|
| BBL | {bbl} |
| BIN | {bin} |
| Borough | {borough} |
| Block | {block} |
| Lot | {lot} |
| ZIP | {zip} |
| Community District | {cd} |
| Building Class | {bldgclass} |
| Zoning | {zonedist1} |
| Year Built | {yearbuilt} |
| Floors | {numfloors} |
| Lot Area | {lotarea} SF |
| Building Area | {bldgarea} SF |
| Owner | {ownername} |
| Coordinates | {lat}, {lon} |

---

## 2. Landmark Status
{LANDMARKED / IN HISTORIC DISTRICT / NOT DESIGNATED}
{If landmarked: LP number, name, date, district, architect, style}
{Implications note if designated}

---

## 3. DOB Permits & Filings
**Total found:** {count} ({x} legacy, {y} DOB NOW)
{Tables grouped by NB, A1, A2/A3, DM, Other}

---

## 4. DOB Violations
### ⚠ Open Violations: {count}
{Open violations table}
### All DOB Violations
{Table}
### ECB Violations
{Table with penalties}
**Total penalties assessed:** ${amount}

---

## 5. Property Records (ACRIS)
### Deeds (Ownership)
{Table — current owner from most recent deed}
### Mortgages
{Table}
### Other Documents
{Table}

---

## 6. HPD — Housing Preservation & Development
{If non-residential: "Building class {X} — HPD records not applicable."}
{If residential: Registration, open violations by class, complaints}

---

## 7. BSA — Board of Standards and Appeals
{Applications table or "No BSA applications found (records from 1998-present)."}

---

*Generated by /nyc-property-report — NYC Open Data*
*Data currency varies by dataset. Verify critical findings with source agencies.*
```

## Step 5: Summary

After writing the file, print a brief inline summary:

```
Property report written: property-120-broadway.md

Key findings:
- Landmark: Not designated
- DOB Permits: 47 found (3 active filings)
- Open Violations: 2 (1 ECB with $25,000 penalty)
- Owner: {name} (per ACRIS deed YYYY-MM-DD)
- HPD: N/A (commercial building)
- BSA: 1 approved variance (2004)

Run /zoning-analysis-nyc for zoning envelope data.
```

## Conventions

- All dates: YYYY-MM-DD
- Dollar amounts: comma-separated
- Open/active items flagged with ⚠
- If a domain returns no results, say so explicitly (don't omit the section)
- If a domain query fails (network error, rate limit), note the error and continue
- Always include the "Data currency varies" caveat

## Edge Cases

- **Rate limited (HTTP 429):** Wait 5 seconds, retry once. If still 429, note error and suggest setting `NYC_SOCRATA_TOKEN`.
- **ACRIS with many documents:** Limit to 20 most recent. Note if truncated.
- **Condo lots:** ACRIS keys on individual unit lots. Note to search parent condo lot too.
- **Pre-1989 buildings:** Pre-BIS DOB records not digitized. Note if few permits for old building.
- **Multiple BINs:** If PLUTO shows `numbldgs` > 1, note that lot has multiple buildings.
- **No results from any API:** State clearly per section. Don't fail the whole report.

## Final Step: Disclaimer + Marker (required)

This skill produces regulatory output. End every report this skill produces — printed in chat or saved to a file — with the canonical disclaimer block from `rules/professional-disclaimer.md`, followed by one blank line and the machine-readable marker, exactly as shown:

```markdown
> **Disclaimer:** This is an AI-generated analysis for preliminary planning purposes. All findings must be verified by a licensed professional before use in design, permitting, or regulatory submissions.

<!-- architecture-studio:requires-disclaimer -->
```

The marker is a single end-of-file sentinel — it appears exactly once, as the last line of the report. The `post-write-disclaimer-check` hook parses saved `.md` reports for the marker and blocks the write if the canonical disclaimer block is missing.
