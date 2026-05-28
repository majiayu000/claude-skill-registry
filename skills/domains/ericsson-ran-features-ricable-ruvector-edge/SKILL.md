---
name: ericsson-ran-features
description: >
  Ericsson LTE/NR RAN feature knowledge base: 593 features, 9432 parameters,
  3368 counters, 752 MO classes, 199 KPIs, 118 technical documents, 49 releases.
  Query by: acronym (IFLB, DUAC, MCPC, ANR, MSM, CA, DRX), FAJ/CXC codes,
  parameter names (lbTpNonQualFraction, sleepMode, mimoMode), counter patterns
  (pmLbEval, pmMimo, pmHo), MO classes (EUtranCellFDD, NRCellDU, MimoSleepFunction),
  document type (hardware, troubleshooting, configuration, installation, safety).

  Feature domains: Carrier Aggregation (89) - inter/intra-band CA, UL/DL CA,
  NR-DC; Radio Resource Management (64) - load balancing, admission control,
  scheduling, congestion; NR/5G (57) - NSA/SA, EN-DC, DSS, NR carrier config;
  Transport (52) - fronthaul, backhaul, X2/Xn/S1/NG interfaces, Ethernet;
  MIMO & Antenna (40) - massive MIMO, beamforming, TM modes, antenna config;
  Mobility (36) - handover, ANR, neighbor relations, RRC state transitions;
  Energy Saving (29) - cell/MIMO sleep, micro sleep TX, power control;
  Coverage & Capacity (28) - cell config, sector management, extended range;
  Voice & IMS (21) - VoLTE, VoNR, CSFB, speech codecs; UE Handling (11) -
  paging, DRX/DTX, idle mode; QoS (8) - priority scheduling, GBR bearers;
  Interference (5) - ICIC, eICIC, CoMP; Timing (5) - IEEE 1588, GPS sync;
  Security (3) - MACsec, encryption; SON (2) - self-optimization.

  Use for: deployment planning, activation/deactivation procedures, cmedit
  CLI command generation, parameter tuning, dependency analysis, KPI
  troubleshooting, release tracking, feature comparison.
---

# Ericsson RAN Features

Knowledge base for Ericsson Radio Access Network features from official documentation.

## Quick Start

### 1. Quick Lookup (Most Common)

```bash
# Brief structured output (3-5 lines with key facts)
python3 scripts/search.py --acronym IFLB --brief
python3 scripts/search.py --faj "121 4219" --brief
python3 scripts/search.py --cxc CXC4011911 --brief
```

### 2. Technical Deep Dive

```bash
# Full markdown technical brief with cmedit commands
python3 scripts/search.py --acronym IFLB --markdown

# Detailed text output
python3 scripts/search.py --acronym IFLB --verbose
```

### 3. Search Modes

```bash
# By acronym (e.g., IFLB, DUAC, MCPC, ANR, CA, MIMO)
python3 scripts/search.py --acronym IFLB

# By feature name (with typo tolerance using --fuzzy)
python3 scripts/search.py --name "load balancing"
python3 scripts/search.py --name "lod blancng" --fuzzy

# By FAJ/CXC code
python3 scripts/search.py --faj "121 4219"
python3 scripts/search.py --cxc "CXC4011911"

# By parameter name
python3 scripts/search.py --param "lbTpNonQualFraction"

# By counter/KPI
python3 scripts/search.py --counter "pmLbEval"

# By MO class
python3 scripts/search.py --mo "EUtranCellFDD"

# Boolean keyword search (AND, OR, NOT)
python3 scripts/search.py --keyword "MIMO AND sleep"
python3 scripts/search.py --keyword "load OR balancing"
python3 scripts/search.py --keyword "handover NOT LTE"

# By access type or release
python3 scripts/search.py --access NR
python3 scripts/search.py --release "24.Q4"

# By event name (INTERNAL_EVENT_*, EVENT_PARAM_*)
python3 scripts/search.py --event "INTERNAL_EVENT_MIMO"
python3 scripts/search.py --event "UE_MOBILITY"

# By KPI name or description
python3 scripts/search.py --kpi "Success Rate"
python3 scripts/search.py --kpi "throughput"

# By functional domain/category
python3 scripts/search.py --domain "Energy Saving"
python3 scripts/search.py --domain "Carrier Aggregation"
python3 scripts/search.py --list-domains  # Show all available domains

# By document type (non-feature technical docs)
python3 scripts/search.py --doc-type hardware --limit 5
python3 scripts/search.py --doc-type troubleshooting --limit 5
python3 scripts/search.py --doc-type configuration --limit 5
python3 scripts/search.py --list-doc-types  # Show all document categories

# By document title
python3 scripts/search.py --doc-title "Paging" --limit 5
python3 scripts/search.py --doc-title "Random Access" --limit 5

# Export results
python3 scripts/search.py --access LTE --export csv > lte_features.csv
python3 scripts/search.py --domain "MIMO" --export json > mimo_features.json
```

### 4. Compare Features

```bash
# Side-by-side comparison table
python3 scripts/search.py --access LTE --compare --limit 5
python3 scripts/compare.py IFLB DUAC MSM
python3 scripts/compare.py IFLB DUAC --deps    # With dependency overlap
python3 scripts/compare.py IFLB DUAC --params  # With parameter differences
```

### 5. Data Quality Audit

```bash
python3 scripts/audit.py            # Full audit report
python3 scripts/audit.py --stats    # Statistics only
python3 scripts/audit.py --gaps     # Missing data analysis
```

### Dependency Commands

```bash
# Show all dependencies for a feature
python3 scripts/deps.py "FAJ 121 4219"

# Show features that depend on this one
python3 scripts/deps.py --reverse "FAJ 121 3009"

# List all features with conflicts
python3 scripts/deps.py --conflicts

# Compute activation order for multiple features (topological sort)
python3 scripts/deps.py --activation-order IFLB DUAC MSM
```

### Validation Commands

```bash
# Check if features can coexist (no conflicts)
python3 scripts/validate.py IFLB DUAC MSM

# Validate with detailed analysis (shows missing prerequisites)
python3 scripts/validate.py IFLB DUAC --verbose

# Check by FAJ codes
python3 scripts/validate.py --faj "121 3009" "121 4219"

# JSON output for automation
python3 scripts/validate.py --json IFLB DUAC
```

### 6. Cross-Reference Queries

```bash
# Find all features that depend on this FAJ (have it as prerequisite)
python3 scripts/search.py --depends-on "121 4219"

# Find all prerequisites (features required by) this FAJ
python3 scripts/search.py --required-by "121 4219"

# Find all conflicting features
python3 scripts/search.py --conflicts-with "121 4219"
```

### 7. Deployment Scripts

```bash
# Generate full activation script with prerequisites and cmedit commands
python3 scripts/search.py --acronym IFLB --activation-script

# Generate post-activation verification commands
python3 scripts/search.py --acronym IFLB --verification-script
```

### 8. Dependency Visualization

```bash
# Generate mermaid diagram for dependency visualization
python3 scripts/deps.py --mermaid IFLB
```

Output can be rendered in markdown viewers or pasted into https://mermaid.live

---

## Decision Tree: Which Command to Use

### By Identifier Type

| Have | Use | Example |
|------|-----|---------|
| Acronym (IFLB, DUAC) | `--acronym` | `--acronym IFLB` |
| FAJ code | `--faj` | `--faj "121 4219"` |
| CXC code | `--cxc` | `--cxc CXC4011911` |
| Parameter name | `--param` | `--param lbTp` |
| Counter pattern | `--counter` | `--counter pmLb` |
| Event name | `--event` | `--event INTERNAL_EVENT_MIMO` |
| KPI name | `--kpi` | `--kpi "Success Rate"` |
| MO class | `--mo` | `--mo EUtranCellFDD` |
| Domain/category | `--domain` | `--domain "Energy Saving"` |
| Keywords/text | `--keyword` | `--keyword "load AND balance"` |
| Access type | `--access` | `--access LTE` |
| Release version | `--release` | `--release "24.Q4"` |

### By Output Need

| Need | Flag | Result |
|------|------|--------|
| Quick facts (3-5 lines) | `--brief` | Concise summary |
| Full technical doc | `--markdown` | Complete brief with cmedit |
| Commands only | `--cmedit` | ENM cmedit commands |
| Feature comparison | `--compare` | Side-by-side table |
| CSV export | `--export csv` | Spreadsheet format |
| JSON export | `--export json` | Machine-readable |

### Common Workflows

**Deployment Checklist:**
```bash
# 1. Identify the feature
python3 scripts/search.py --acronym IFLB --brief

# 2. Check prerequisites
python3 scripts/deps.py "FAJ 121 4219"

# 3. Generate deployment commands
python3 scripts/cmedit_generator.py --faj "121 4219" --format script --site "PARIS_01"
```

**Troubleshooting:**
```bash
# 1. Feature not activating? Check prerequisites first
python3 scripts/deps.py "FAJ 121 4219"

# 2. Conflict error? Validate coexistence
python3 scripts/validate.py IFLB DUAC --verbose

# 3. No counter data? Check source file
python3 scripts/search.py --acronym IFLB --markdown | grep -A5 "Counters"

# 4. Find related features by counter
python3 scripts/search.py --counter "pmXxx"

# 5. Check data quality/missing fields
python3 scripts/audit.py --gaps
```

**Feature Analysis:**
```bash
# Compare multiple features
python3 scripts/compare.py IFLB DUAC MCPC --all

# Find all energy saving features
python3 scripts/search.py --domain "Energy Saving" --export csv
```

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "No feature found with FAJ code" | Invalid FAJ | Check catalog.md or use `--name` search |
| "No feature found with acronym" | Unknown acronym | Use `--name` with partial match |
| "No features found for access type" | Type not in dataset | Only LTE, NR, GSM supported |
| "0 results" for keyword | Too specific query | Use OR, try broader terms |
| "cannot be empty" error | Empty query string | Provide valid search term |

**Tips:**
- If exact match fails, add `--fuzzy` flag for typo tolerance
- Use `--list-domains` to see available categories
- Use `--list-releases` to see available releases
- For boolean searches, test each term separately first

---

### cmedit Command Generation

Generate ready-to-use ENM cmedit CLI commands for feature configuration:

```bash
# Generate cmedit commands for a feature (grouped by MO class)
python3 scripts/search.py --acronym IFLB --cmedit

# Markdown output automatically includes cmedit commands
python3 scripts/search.py --acronym IFLB --markdown

# Standalone cmedit generator with different output formats
python3 scripts/cmedit_generator.py --faj "121 4219"                    # Text output
python3 scripts/cmedit_generator.py --faj "121 4219" --format markdown  # Markdown
python3 scripts/cmedit_generator.py --faj "121 4219" --format script    # Shell script
python3 scripts/cmedit_generator.py --faj "121 4219" --format json      # JSON

# Collection-scoped commands
python3 scripts/cmedit_generator.py --faj "121 4219" --scope collection --collection-name "paris_cells"
```

#### Generated Command Types

| Command | Description |
|---------|-------------|
| `cmedit get` | Read current parameter values (grouped by MO class) |
| `cmedit set` | Modify parameter values (grouped by MO class) |
| `FeatureState` check | Verify feature state, license, and service status |
| Activation | Activate feature via FeatureState MO |
| Deactivation | Deactivate feature via FeatureState MO |

#### Example Output

```bash
# MIMO Sleep Mode [MSM]
# FAJ: FAJ 121 3094 | CXC: CXC4011808

## Check Feature State
cmedit get <SITE_NAME> FeatureState=CXC4011808 featureState,licenseState,serviceState

## Read Parameters (grouped by MO Class)
# MimoSleepFunction (17 params)
cmedit get <SITE_NAME> MimoSleepFunction.(sleepMode,sleepStartTime,sleepEndTime,...)

## Modify Parameters (grouped by MO Class)
# MimoSleepFunction - Set 17 params on MimoSleepFunction
cmedit set <SITE_NAME> MimoSleepFunction sleepMode=<value>,sleepStartTime=<value>,...

## Activation
cmedit set <SITE_NAME> FeatureState=CXC4011808 featureState=ACTIVATED

## Deactivation
cmedit set <SITE_NAME> FeatureState=CXC4011808 featureState=DEACTIVATED
```

## Markdown Output Format

Use `--markdown` or `-m` flag to get comprehensive technical brief output:

```markdown
## Feature Name [ACRONYM]

**FAJ:** FAJ 121 XXXX | **CXC:** CXCXXXXXXX | **Access:** LTE | **License:** Required

Summary description...

### Dependencies
- **Prerequisites:** Feature Name (FAJ XXX XXXX)
- **Related:** Feature1, Feature2 (+N more)
- **Conflicts:** Conflicting Feature

### Network Impact
**Capacity/Performance:** Impact description...
**Other Network Elements:** Network effects...

### Activation
**Prerequisites:**
- License key is installed
- CCTR active for one week

**Steps:**
1. Set FeatureState.featureState to ACTIVATED in FeatureState=CXCXXXXXXX

**After:** Keep CCTR active for one week

### Deactivation
1. Set FeatureState.featureState to DEACTIVATED in FeatureState=CXCXXXXXXX

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| MO.attribute | Introduced | Short description |

### Counters

| Counter | MO Class |
|---------|----------|
| pmCounterName | EUtranCellFDD |

### KPIs

| KPI | Description |
|-----|-------------|
| Mobility Success Rate | The Mobility Success Rate KPI... |

### Engineering Guidelines
Configuration recommendations and formulas...
**Sections:** Configuration, Tuning Parameters

### Change History

| Release | Change |
|---------|--------|
| 24.Q4 | Enhancement for EN-DC Support |
| 23.Q2 | Added new parameter |

**Source:** `path/to/file.md`
```

## Reference Files

| File | Purpose |
|------|---------|
| `references/features.json` | All feature metadata with full details |
| `references/parameters.json` | Parameter → features reverse index |
| `references/counters.json` | Counter → features reverse index (with descriptions, units, types) |
| `references/mo_classes.json` | MO class → features/params/counters index |
| `references/releases.json` | Release version → changes index |
| `references/dependency_graph.json` | Feature dependency graph with activation order |
| `references/events.json` | Event → features reverse index |
| `references/kpis.json` | KPI → features reverse index |
| `references/index_acronym.json` | O(1) acronym → FAJ lookup |
| `references/index_cxc.json` | O(1) CXC → FAJ lookup |
| `references/index_categories.json` | Feature domain categorization |
| `references/index_guidelines.json` | Engineering guidelines subsections index |
| `references/index_search.json` | Inverted search index |
| `references/catalog.md` | Quick scan of all features |

## Source Files

Feature source markdown files are in `source/` directory (symlink to `../elex_features/`).

The `file` field in features.json contains the relative path from source directory:
```
"file": "en_lzn7931040_r50f_batch3/461_22104-LZA7016014_1Uen.AN33B.md"
```

To read a feature's full source:
```bash
# From skill directory
cat source/<file_path>

# Example for UTTM
cat source/en_lzn7931040_r50f_batch3/461_22104-LZA7016014_1Uen.AN33B.md
```

**Note:** Most queries can be answered directly from features.json without reading source files. Only read source files when you need:
- Full engineering guidelines text
- Detailed feature operation explanations
- Complete parameter descriptions
- Images or diagrams referenced in the document

## Feature Document Structure

Each feature markdown file contains these sections:

| Section | Content |
|---------|---------|
| **Overview** | Feature name, FAJ, Value Package, Access Type, Licensing |
| **Dependencies** | Prerequisites, Related features, Conflicts |
| **Feature Operation** | How the feature works technically |
| **Network Impact** | Capacity, performance, interface effects |
| **Parameters** | MO.attribute names with types |
| **Performance** | KPIs, PM counters, Events |
| **Activate** | Activation procedure with CXC code |
| **Deactivate** | Deactivation procedure |
| **Engineering Guidelines** | Configuration recommendations |
| **Appendix: Change History** | Release-specific changes (23.Q4, 24.Q3.0, etc.) |

## Key Identifiers

| ID Type | Format | Example | Purpose |
|---------|--------|---------|---------|
| **Acronym** | 2-6 letters | IFLB, DUAC, MCPC | Quick feature lookup |
| **FAJ** | FAJ XXX XXXX | FAJ 121 4219 | Feature identity |
| **CXC** | CXC4XXXXXX | CXC4011911 | Activation code (FeatureState MO) |
| **Parameter** | MO.attribute | EUtranCellFDD.lbTpNonQualFraction | Configuration |
| **Counter** | MO.pmXxx | EUtranCellFDD.pmLbEvalExpiredUe | Performance measurement |

## Common Acronyms

| Acronym | Feature Name |
|---------|--------------|
| IFLB | Inter-Frequency Load Balancing |
| DUAC | Dynamic UE Admission Control |
| MCPC | Mobility Control at Poor Coverage |
| ANR | Automated Neighbor Relations |
| CA | Carrier Aggregation |
| MIMO | Multiple-Input Multiple-Output |
| TTI | Transmission Time Interval |
| DRX | Discontinuous Reception |
| CSFB | CS Fallback |
| VoLTE | Voice over LTE |

## Dependency Types

| Type | Meaning |
|------|---------|
| **Prerequisite** | Must be activated before this feature |
| **Related** | Works together, may affect behavior |
| **Conflicting** | Cannot be used simultaneously |

## Parameter Types

| Type | Meaning |
|------|---------|
| **Introduced** | New parameter specific to this feature |
| **Affecting** | Existing parameter that influences this feature |
| **Affected** | Parameter modified by this feature |

## Workflow: Answer Feature Questions

1. **Search** - Use `search.py` to find relevant features
2. **Read** - Load the source markdown file for full details
3. **Synthesize** - Combine information from multiple features if needed

```bash
# User asks: "What parameters control load balancing?"
python3 scripts/search.py --param "lb" --limit 20
```

## Workflow: Activation Procedure

1. **Find feature** - Search by name or FAJ code
2. **Check prerequisites** - Use `deps.py` to see required features
3. **Get CXC code** - From search results or source file
4. **Read activation section** - Use `--markdown` flag for full details

```bash
# Get feature with full activation procedure
python3 scripts/search.py --name "IFLB" --markdown

# Check what needs to be activated first
python3 scripts/deps.py "FAJ 121 4219"
```

## Workflow: Feature Deployment with cmedit

1. **Find feature** - Search by name, acronym, or FAJ code
2. **Generate cmedit commands** - Use `--cmedit` flag to get ready-to-use commands
3. **Check current state** - Run the FeatureState check command
4. **Review parameters** - Read current values with GET commands
5. **Configure** - Modify parameters with SET commands (replace `<value>` placeholders)
6. **Activate** - Run the activation command

```bash
# Step 1-2: Get feature info with cmedit commands
python3 scripts/search.py --acronym MSM --cmedit

# Or generate a deployment script
python3 scripts/cmedit_generator.py --faj "121 3094" --format script --site "PARIS_NORTH_LTE" > deploy_msm.sh

# For collection operations
python3 scripts/cmedit_generator.py --faj "121 3094" --scope collection --collection-name "northern_sites"
```

## Statistics

- **Features**: 530 indexed
- **Parameters**: 3834 tracked
- **Counters**: 3124 unique (with descriptions, units, types where available)
- **MO Classes**: 629 indexed
- **Releases**: 49 tracked (from 17.Q3 to 25.Q2)
- **Events**: 103 features with event data (19.4%)
- **KPIs**: 93 features with KPI data (17.5%)
- **Engineering Guidelines**: 266 features (50.2%)
- **Access Types**: LTE, NR, WCDMA, GSM

## Claude Output Guidelines

When answering user questions about Ericsson RAN features:

### Quick Questions
*"What is IFLB?", "What's the CXC for MIMO Sleep?"*

Use `--brief` output for concise technical summary:
```bash
python3 scripts/search.py --acronym IFLB --brief
```

Output format (3-5 lines):
```
Inter-Frequency Load Balancing [IFLB]
FAJ 121 3009 | CXC4011319 | LTE | License: Yes
Params: 26 | Counters: 23 | Prereqs: Coverage-Trigger
Activate: cmedit set <SITE> FeatureState=CXC4011319 featureState=ACTIVATED
```

### How-To Questions
*"How to activate IFLB?", "How to configure load balancing?"*

Use `--markdown` for full technical brief with activation steps:
```bash
python3 scripts/search.py --acronym IFLB --markdown
```

Focus on Activation and Parameters sections in response.

### Comparison Questions
*"Difference between IFLB and DUAC?", "Which load balancing feature?"*

Use `--compare` for side-by-side table:
```bash
python3 scripts/compare.py IFLB DUAC --deps
```

### Troubleshooting
*"Why is IFLB not working?", "Feature activation failed"*

Check dependencies and prerequisites:
```bash
python3 scripts/deps.py "FAJ 121 3009"
```

List relevant counters for monitoring.

### Parameter/Counter Lookup
*"What parameters control load balancing?"*

Use parameter or counter search:
```bash
python3 scripts/search.py --param "lb" --brief
python3 scripts/search.py --counter "pmLb" --brief
```

### Response Style
- Use technical, concise language
- Include FAJ/CXC codes for reference
- Provide cmedit commands when deployment-related
- Mention prerequisites before activation steps
- Reference source file for detailed documentation
