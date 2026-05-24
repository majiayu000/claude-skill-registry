---
name: verify-dark
description: Verify dark earthquake claims against fault databases. Use when checking if a candidate earthquake is truly "dark" (unmapped fault) or just pre-historical (known fault). Triggers on "verify dark", "check fault database", "is this dark", "audit earthquake claim".
---

# /verify-dark - Fault Database Verification Skill

## Purpose

Verify if a candidate "dark earthquake" claim is truly dark (unmapped source fault) or pre-historical (known fault, no written record). This skill automates the DARK_EARTHQUAKE_AUDIT.md workflow.

## Usage

```
/verify-dark <lat> <lon> <date_CE> [region]
```

**Examples:**
```
/verify-dark 44.2 8.1 1394 italy
/verify-dark 32.7 -117.2 1741 california
/verify-dark -16.5 -44.8 96 brazil
/verify-dark 22.4 -84.0 1400 caribbean
```

## Workflow

### Step 1: Identify Region & Databases

Based on coordinates, determine which fault databases to check:

| Region | Primary Database | Secondary Databases |
|--------|-----------------|---------------------|
| **Italy** | DISS v3.3.1 (INGV) | ITHACA, EFSM20, GEM SHARE |
| **California** | SCEC CFM v7.0 | CGS FER, USGS Quaternary |
| **Caribbean/C. America** | GEM CCAF-DB | USGS |
| **Brazil** | GEM SARA | (Note: Brazil EXCLUDED from SARA) |
| **Middle East** | EMME | GEM, Hessami (2003) |
| **Romania** | RODASEF | ESHM20, SHARE |
| **Turkey** | AFAD | GEM, Emre et al. |

### Step 2: Search Fault Databases

For each database, search within 50km and 100km radius:

1. **Use calc_distance MCP tool** to compute distances from candidate to known faults
2. **Query database** (WFS endpoint if available, or web search for geojson)
3. **Record all faults found** with strike, slip type, distance

**Example search pattern:**
```
# Check DISS v3.3.1 for Italy
WebFetch: https://diss.ingv.it/diss330/download/DISS330_ISS.geojson
Filter: features within 100km of (lat, lon)

# Check SCEC CFM for California
WebFetch: https://www.scec.org/research/cfm
Search for fault traces near coordinates
```

### Step 3: Check Recent Literature (2010+)

Search for recent fault mapping publications:

1. **WebSearch**: "[region] fault mapping [year range]"
2. **WebSearch**: "paleoseismic trench [fault name]"
3. **WebSearch**: "[coordinates] seismogenic source"

Look for:
- New fault discoveries
- Offshore/submarine fault extensions
- DEM-based lineament studies
- Paleoseismic trenching results

### Step 4: Run DEM Lineament Check (if available)

If DEM data exists for the region:
- Check `dem_tiles/` for existing analysis
- Reference `DEM_LINEAMENT_FINDINGS.md` or similar
- Note any unmapped structures identified

### Step 5: Generate Verification Table

Create markdown table summarizing findings:

```markdown
| Database | Checked | Faults within 50km | Faults within 100km | Notes |
|----------|---------|-------------------|---------------------|-------|
| DISS v3.3.1 | ✅ | [fault names] | [fault names] | [details] |
| ITHACA | ✅ | ... | ... | ... |
| EFSM20 | ✅ | ... | ... | ... |
| GEM | ✅ | ... | ... | ... |
| Recent lit | ✅ | ... | ... | [citations] |
```

### Step 6: Classify Event

Based on findings, classify as:

| Classification | Criteria |
|----------------|----------|
| **TRUE DARK** | No mapped fault in ANY database (like Italy 1394, Brazil events) |
| **PRE-HISTORICAL** | Known fault exists, but earthquake predates written records (like California 1741) |
| **PRE-COLUMBIAN** | Event in Americas before 1492 (no records possible) |
| **PRE-INSTRUMENTAL** | Event before seismometer network (varies by region) |
| **VALIDATION** | Known earthquake used to test methodology (like Cuba 1766) |
| **DATABASE ARTIFACT** | "Missing" due to incomplete database, fault IS mapped elsewhere |

### Step 7: Update DARK_EARTHQUAKE_AUDIT.md

Add new section to `paleoseismic_caves/DARK_EARTHQUAKE_AUDIT.md`:

```markdown
### ✅ [Region]: [Date] - **[CLASSIFICATION]**

**Date verified**: [today's date]
**Classification**: **[CLASSIFICATION]** ([explanation])

**Databases checked**:
- ✅ **[Database 1]** - [findings]
- ✅ **[Database 2]** - [findings]
...

**Key findings**:
[Summary of what was found]

**Conclusion**: [Why this classification]

**Likelihood of database artifact**: **[HIGH/LOW/ZERO]** - [explanation]
```

## Classification Decision Tree

```
Is there a mapped fault within 100km in ANY database?
├─ YES → Is earthquake in historical catalogs?
│        ├─ YES → VALIDATION EVENT
│        └─ NO → PRE-HISTORICAL (known fault, no record)
│                 └─ If Americas pre-1492 → PRE-COLUMBIAN
│                 └─ If pre-seismometer → PRE-INSTRUMENTAL
└─ NO → Does a fault database exist for this region?
         ├─ NO (e.g., Brazil) → TRUE DARK (no database = genuine gap)
         └─ YES → Did DEM analysis find unmapped structure?
                  ├─ YES → TRUE DARK (candidate)
                  └─ NO → UNATTRIBUTED (needs more research)
```

## Output Format

The skill will output:

1. **Summary box** at top with classification
2. **Verification table** with all databases checked
3. **Key findings** with quotes/evidence
4. **Classification rationale** explaining decision
5. **Update to DARK_EARTHQUAKE_AUDIT.md** (with approval)

## Database URLs Reference

**Italy:**
- DISS v3.3.1: https://diss.ingv.it/
- ITHACA: http://ithaca.rm.ingv.it/
- EFSM20: https://seismofaults.eu/

**California:**
- SCEC CFM: https://www.scec.org/research/cfm
- CGS FER: https://maps.conservation.ca.gov/cgs/fer/

**Caribbean:**
- GEM CCAF-DB: https://github.com/GEMScienceTools/CCAF-DB

**Middle East:**
- EMME: https://www.emme-gem.org/

**Global:**
- GEM Global Active Faults: https://github.com/GEMScienceTools/gem-global-active-faults

## Important Notes

1. **USGS Quaternary Fault Database has 9-27 year lag** - never use as sole source
2. **Brazil is excluded from GEM SARA** - stable continental interiors have no fault databases
3. **"Dark" means UNMAPPED FAULT, not just "no written record"**
4. **Always check 3+ databases** before classifying as TRUE DARK
5. **DEM lineament analysis** strengthens case for unmapped structures
