---
name: nyc-landmarks
description: Check whether a NYC building is landmarked or in a historic district using LPC data. Use when the user asks "is this building landmarked", whether a site sits in a historic district, or whether LPC review applies. NYC only.
allowed-tools:
  - WebFetch
  - Write
  - Read
  - Bash
---

# /nyc-landmarks — LPC Landmark & Historic District Check

Check if a NYC building is individually landmarked or within a historic district using the LPC Individual Landmark & Historic District Building Database. No API key required.

## Usage

```
/nyc-landmarks 120 Broadway, Manhattan
/nyc-landmarks 1000770001          (BBL)
/nyc-landmarks 1001389             (BIN)
```

## Steps 1–2: Parse Input & Resolve BBL

Read `../nyc-property-report/pluto-resolution.md` (shared by all 7 NYC due-diligence skills) and follow it: parse the input (address, BBL, or BIN) and resolve via PLUTO.

**This skill's extra:** also store `histdist` from PLUTO — used in Step 3.

## Step 3: Query LPC Database

Dataset IDs and field names are canonical in `../nyc-property-report/socrata-reference.md` — on any disagreement, the reference wins.

Use the Individual Landmarks dataset (`buis-pvji`). Query by BBL first:
```
https://data.cityofnewyork.us/resource/buis-pvji.json?bbl={BBL}
```

If no results, fallback by block + lot. **This dataset stores block/lot WITHOUT zero-padding** (e.g. block `47`, lot `7501`) — strip leading zeros from the parsed BBL components:
```
https://data.cityofnewyork.us/resource/buis-pvji.json?$where=block='{BLOCK}' AND lot='{LOT}' AND borough='{BOROUGH}'
```

Key fields: `lpc_name`, `lpc_lpnumb`, `desdate`, `landmarkty`, `lpc_sitede`, `lpc_sitest`, `lpc_altern`, `address`, `url_report`

Also check PLUTO's `histdist` field from Step 2 — if it has a value, the property is in a historic district even if not individually listed in the LPC dataset.

## Step 4: Print Results

```markdown
## Landmark Status — {Address}

**Status: LANDMARKED / IN HISTORIC DISTRICT / NOT DESIGNATED**

| Field | Value |
|-------|-------|
| LP Number | {lpc_lpnumb} |
| Name | {lpc_name} |
| Designation Date | {desdate} |
| Type | {landmarkty} |
| Site Description | {lpc_sitede} |
| Site Style | {lpc_sitest} |
| Also Known As | {lpc_altern} |
| LPC Report | {url_report} |
| Historic District | {histdist from PLUTO} |

**Implications:** Exterior alterations require LPC Certificate of Appropriateness before DOB permit.

Source: [LPC Individual Landmarks](https://data.cityofnewyork.us/Housing-Development/Individual-Landmarks/buis-pvji)
```

If not landmarked and not in a historic district: "No landmark designation found for this property."

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
