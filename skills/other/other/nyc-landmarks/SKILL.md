---
name: nyc-landmarks
description: Check if a NYC building is landmarked or in a historic district using LPC data.
allowed-tools:
  - WebFetch
  - Write
  - Read
  - Bash
user-invocable: true
---

# /nyc-landmarks — LPC Landmark & Historic District Check

Check if a NYC building is individually landmarked or within a historic district using the LPC Individual Landmark & Historic District Building Database. No API key required.

## Usage

```
/nyc-landmarks 120 Broadway, Manhattan
/nyc-landmarks 1000770001          (BBL)
/nyc-landmarks 1001389             (BIN)
```

## Step 1: Parse Input

Accept one of:
- **Address + Borough/Zip** — "120 Broadway, Manhattan" or "120 Broadway 10271"
- **BBL** — 10-digit number (boro 1 + block 5 + lot 4)
- **BIN** — 7-digit Building Identification Number

Borough codes: Manhattan=1/MN, Bronx=2/BX, Brooklyn=3/BK, Queens=4/QN, Staten Island=5/SI

## Step 2: Resolve via PLUTO

Query PLUTO to get BBL, BIN, and building metadata. No API key needed.

By BBL:
```
https://data.cityofnewyork.us/resource/64uk-42ks.json?bbl={BBL}
```

By address:
```
https://data.cityofnewyork.us/resource/64uk-42ks.json?$where=upper(address) LIKE '%{STREET}%'&borough='{BORO_CODE}'&$limit=5
```

**Address normalization:** Uppercase, strip unit/apt suffixes. Borough names to codes: Manhattan=MN, Bronx=BX, Brooklyn=BK, Queens=QN, Staten Island=SI. If multiple results, ask the user to pick. If zero, try variations (ST vs STREET, AVE vs AVENUE) or suggest providing a BBL.

Store from PLUTO: `bbl`, `bin` (or `bldgbin`), `address`, `borough`, `bldgclass`, `zonedist1`, `yearbuilt`, `ownername`, `numfloors`, `lotarea`, `latitude`, `longitude`, `histdist`.

Parse BBL into: boro (1 digit), block (5 digits zero-padded), lot (4 digits zero-padded).

## Step 3: Query LPC Database

Use the Individual Landmarks dataset (`buis-pvji`). Query by BBL first:
```
https://data.cityofnewyork.us/resource/buis-pvji.json?bbl={BBL}
```

If no results, fallback by block + lot:
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
