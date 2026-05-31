---
name: nyc-property-report
description: Combined NYC property report — landmarks, DOB permits, violations, ACRIS records, HPD, and BSA variances.
allowed-tools:
  - WebFetch
  - Write
  - Read
  - Bash
user-invocable: true
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

## Usage

```
/nyc-property-report 120 Broadway, Manhattan
/nyc-property-report 1000770001          (BBL)
/nyc-property-report 1001389             (BIN)
```

## Step 1: Parse Input

Accept one of:
- **Address + Borough/Zip** — "120 Broadway, Manhattan" or "120 Broadway 10271"
- **BBL** — 10-digit number (boro 1 + block 5 + lot 4)
- **BIN** — 7-digit Building Identification Number

Borough codes: Manhattan=1/MN, Bronx=2/BX, Brooklyn=3/BK, Queens=4/QN, Staten Island=5/SI

Strip apartment/unit/floor suffixes. Handle hyphenated Queens addresses.

## Step 2: Resolve via PLUTO

By BBL:
```
https://data.cityofnewyork.us/resource/64uk-42ks.json?bbl={BBL}
```

By address:
```
https://data.cityofnewyork.us/resource/64uk-42ks.json?$where=upper(address) LIKE '%{STREET}%'&borough='{BORO_CODE}'&$limit=5
```

**Address normalization:** Uppercase, strip unit/apt. Borough names to codes: Manhattan=MN, Bronx=BX, Brooklyn=BK, Queens=QN, Staten Island=SI. If multiple results, ask user to pick. If zero, try variations or suggest BBL.

Store: `bbl`, `bin`/`bldgbin`, `address`, `borough`, `zipcode`, `cd`, `bldgclass`, `zonedist1`, `yearbuilt`, `ownername`, `numfloors`, `lotarea`, `bldgarea`, `unitstotal`, `histdist`, `latitude`, `longitude`.

Parse BBL: boro (1 digit), block (5 digits zero-padded), lot (4 digits zero-padded).

## Step 3: Query All 6 Domains

Query each domain in sequence. If any query fails, note the error and continue with the next domain.

Read `socrata-reference.md` (in this skill's directory) for the full API reference with field names and SoQL patterns.

### Domain 1: Landmarks

By BIN: `https://data.cityofnewyork.us/resource/7mgd-s57w.json?bin_number={BIN}`
Fallback by BBL: `https://data.cityofnewyork.us/resource/7mgd-s57w.json?bbl={BBL}`

Also check PLUTO `histdist` field — if set, property is in a historic district.

Key fields: `lpc_name`, `lpc_number`, `date_designated`, `building_type`, `style`, `architect`, `historic_district_name`, `status`

### Domain 2: DOB Permits

**IMPORTANT:** Legacy datasets use `bin__` (double underscore). DOB NOW uses `bin`.

Legacy permits: `https://data.cityofnewyork.us/resource/ipu4-2q9a.json?$where=bin__='{BIN}'&$order=issuance_date DESC&$limit=30`
Legacy filings: `https://data.cityofnewyork.us/resource/ic3t-wcy2.json?$where=bin__='{BIN}'&$order=latest_action_date DESC&$limit=30`
DOB NOW permits: `https://data.cityofnewyork.us/resource/rbx6-tga4.json?$where=bin='{BIN}'&$order=approved_date DESC&$limit=30`
DOB NOW filings: `https://data.cityofnewyork.us/resource/w9ak-ipjd.json?$where=bin='{BIN}'&$order=filing_date DESC&$limit=30`

Merge, sort by date DESC, group by job type (NB, A1, A2, A3, DM, Other).

### Domain 3: DOB Violations

DOB violations: `https://data.cityofnewyork.us/resource/3h2n-5cm9.json?$where=bin='{BIN}'&$order=issue_date DESC&$limit=50`
ECB violations: `https://data.cityofnewyork.us/resource/6bgk-3dad.json?$where=bin='{BIN}'&$order=violation_date DESC&$limit=50`
Active violations: `https://data.cityofnewyork.us/resource/sjhj-bc8q.json?$where=bin='{BIN}'`

Flag open violations with ⚠. Show ECB penalties.

### Domain 4: ACRIS

**Requires BBL** (not BIN). Uses separate borough/block/lot fields.

Step A — Legals: `https://data.cityofnewyork.us/resource/8h5j-fqxa.json?borough={boro}&block={block}&lot={lot}&$order=good_through_date DESC&$limit=20`
Step B — Master: `https://data.cityofnewyork.us/resource/bnx9-e6tj.json?$where=document_id IN ('{id1}','{id2}',...)&$order=doc_date DESC`
Step C — Parties: `https://data.cityofnewyork.us/resource/636b-3b5g.json?$where=document_id IN ('{id1}','{id2}',...)`
Step D — Doc codes: `https://data.cityofnewyork.us/resource/7isb-wh4c.json?$limit=200`

Join by document_id. Party type 1=Grantor, 2=Grantee. Group by doc type (Deeds, Mortgages, Other).

### Domain 5: HPD

**First check `bldgclass`** — HPD only applies to residential (classes starting with A, B, C, D, R, S). If non-residential, skip with note.

**Uses `boroid`** (not `borough`) and separate block/lot fields.

Violations: `https://data.cityofnewyork.us/resource/wvxf-dwi5.json?$where=boroid='{boro}' AND block='{block}' AND lot='{lot}'&$order=inspectiondate DESC&$limit=50`
Open violations: `https://data.cityofnewyork.us/resource/csn4-vhvf.json?$where=boroid='{boro}' AND block='{block}' AND lot='{lot}'`
Complaints: `https://data.cityofnewyork.us/resource/ygpa-z7cr.json?$where=boroid='{boro}' AND block='{block}' AND lot='{lot}'&$order=receiveddate DESC&$limit=30`
Registrations: `https://data.cityofnewyork.us/resource/tesw-yqqr.json?$where=boroid='{boro}' AND block='{block}' AND lot='{lot}'`

Flag Class C violations with ⚠ (immediately hazardous).

### Domain 6: BSA

By BBL: `https://data.cityofnewyork.us/resource/yvxd-uipr.json?$where=bbl='{BBL}'&$order=calendar_date DESC`
Address fallback: `https://data.cityofnewyork.us/resource/yvxd-uipr.json?$where=upper(premises_address) LIKE '%{STREET}%' AND borough='{BOROUGH}'&$order=calendar_date DESC`

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
