---
name: qa_repair_geometry
description: |
  Automated geometry repair using RasFixit and quality validation using RasCheck.
  Handles blocked obstructions, generates before/after visualizations, and
  creates audit trails. Use when fixing geometry errors, repairing obstructions,
  validating models, or ensuring FEMA compliance.
  Triggers: fix, repair, geometry, blocked obstruction, validate, check, RasCheck, RasFixit, FEMA, quality assurance, QA, overlapping, obstruction overlap, elevation envelope, geometry error.
version: 2.0.0
---

# Repairing Geometry Issues

**Lightweight skill for navigating ras-commander's geometry checking and repair capabilities.**

This skill provides quick navigation to primary sources for RasCheck (validation) and RasFixit (repair). **Do not duplicate content from primary sources** - this file serves as an index only.

## Primary Sources (Read These First)

### Quality Validation (RasCheck)
**C:\GH\ras-commander\ras_commander\check\CLAUDE.md** (262 lines)
- 5 comprehensive checks (NT, XS, Structure, Floodway, Profiles)
- FEMA/USACE standards implementation
- Custom thresholds and state-specific surcharge limits
- Report generation (HTML, CSV, JSON)

### Automated Repair (RasFixit)
**C:\GH\ras-commander\ras_commander\fixit\AGENTS.md** (119 lines)
- Blocked obstruction repair algorithm
- 0.02-unit gap insertion requirement
- Elevation envelope details
- Module organization and patterns

### Complete Workflows
**C:\GH\ras-commander\examples\200_fixit_blocked_obstructions.ipynb**
- RasFixit demonstration with visualizations
- Before/after comparison workflow
- Engineering review requirements

**C:\GH\ras-commander\examples\300_quality_assurance_rascheck.ipynb**
- RasCheck validation workflow
- Multi-check execution and reporting
- Custom threshold configuration

## Quick Start Patterns

### Check → Fix → Verify Workflow

```python
from ras_commander import RasCheck, RasFixit

# 1. CHECK: Detect issues
results = RasCheck.run_all("01")
print(f"Errors: {results.get_error_count()}")
print(f"Warnings: {results.get_warning_count()}")

# 2. FIX: Repair blocked obstructions (if detected)
fix_results = RasFixit.fix_blocked_obstructions(
    "model.g01",
    backup=True,      # ALWAYS create timestamped backup
    visualize=True    # ALWAYS generate verification PNGs
)
print(f"Fixed {fix_results.total_xs_fixed} cross sections")

# 3. VERIFY: Confirm repairs
verify_results = RasCheck.run_all("01")
```

### Detection Only (Non-Destructive)

```python
# Detect overlaps without modifying files
detect_results = RasFixit.detect_obstruction_overlaps("model.g01")
print(f"Cross sections with overlaps: {detect_results.total_xs_fixed}")

# Review affected stations
for msg in detect_results.messages:
    print(f"RS {msg.station}: {msg.original_count} → {msg.fixed_count}")
```

### Custom Validation Thresholds

```python
from ras_commander.check import create_custom_thresholds

# Override FEMA defaults for stricter standards
custom = create_custom_thresholds({
    'mannings_n.overbank_max': 0.150,        # Stricter limit
    'reach_length.max_length_ft': 2000.0,    # More conservative
    'floodway.surcharge_ft': 0.5,            # USACE standard (vs 1.0 ft FEMA)
})

results = RasCheck.run_all("01", thresholds=custom)
```

### State-Specific Standards

```python
from ras_commander.check import get_state_surcharge_limit

# Use state-specific floodway surcharge limits
il_limit = get_state_surcharge_limit('IL')  # Returns 0.1 ft (vs FEMA 1.0 ft)

results = RasCheck.run_all(
    "01",
    floodway_profile="Floodway",
    surcharge=il_limit
)
```

### Report Generation

```python
from ras_commander.check import ReportMetadata

# Generate HTML report with metadata
metadata = ReportMetadata(
    project_name=ras.project_name,
    plan_number="01",
    checked_by="Engineer Name"
)
results.to_html("validation_report.html", metadata=metadata)

# Export to CSV for Excel analysis
df = results.to_dataframe()
df.to_csv("validation_messages.csv", index=False)
```

## Critical Technical Details

### Blocked Obstruction Algorithm (Elevation Envelope)

**Source**: `C:\GH\ras-commander\ras_commander\fixit\AGENTS.md` (lines 40-60)

**CRITICAL WARNING - 0.02-Unit Gap Requirement**:
- HEC-RAS **REQUIRES** minimum 0.02-unit separation between adjacent obstructions
- This is a hard requirement in the HEC-RAS geometry preprocessor
- The gap size is defined in `obstructions.py` as `GAP_SIZE = 0.02`
- **DO NOT modify this constant** - changing it will cause preprocessing failures

**Algorithm Steps**:
1. **Collect critical stations**: All start/end points of obstructions
2. **Maximum elevation wins**: In overlap zones, use highest elevation (hydraulically conservative)
3. **Merge adjacent segments**: Combine segments with same elevation
4. **Insert 0.02-unit gaps**: Minimum separation where elevations differ

**Example**:
```
Original (overlapping):
  Segment 1: 100.0 - 200.0 ft, elev 35.0
  Segment 2: 150.0 - 250.0 ft, elev 36.0

Fixed (elevation envelope with 0.02 gap):
  Segment 1: 100.0 - 150.0 ft, elev 35.0
  Segment 2: 150.02 - 250.0 ft, elev 36.0  # 0.02 gap inserted
```

### Fixed-Width FORTRAN Parsing

**Source**: `C:\GH\ras-commander\ras_commander\fixit\AGENTS.md` (lines 53-56)

- HEC-RAS geometry files use 8-character fixed-width columns
- `FIELD_WIDTH = 8` constant must not be changed
- Overflow handled with asterisks (`********`)
- Section terminators: `Bank Sta=`, `#XS Ineff=`, `#Mann=`, `XS Rating Curve=`, `XS HTab`, `Exp/Cntr=`

## When to Use This Skill

**Use for**:
- HEC-RAS geometry preprocessing failures
- FEMA/USACE model validation
- Fixing overlapping blocked obstructions
- Preparing models for peer review or submission
- FEMA Base Level Engineering (BLE) compliance
- Detecting Manning's n or cross section issues
- Validating structure (bridge/culvert) geometry
- Checking floodway surcharge limits
- Creating audit trails for engineering review

**Don't use for**:
- Simple file I/O operations (use basic ras-commander patterns)
- Model execution (use RasCmdr patterns)
- Data extraction (use HDF classes)

## RasCheck Validation Categories

**Source**: `C:\GH\ras-commander\ras_commander\check\CLAUDE.md` (lines 13-60)

| Check Type | Function | Validates |
|------------|----------|-----------|
| **NT Check** | `check_nt()` | Manning's n, transition coefficients, land cover standards |
| **XS Check** | `check_xs()` | Cross section spacing, station ordering, reach lengths, bank stations |
| **Structure Check** | `check_structures()` | Bridges, culverts, inline weirs, low chord elevations, pier spacing |
| **Floodway Check** | `check_floodways()` | Surcharge limits, conveyance reduction, encroachment methods |
| **Profiles Check** | `check_profiles()` | WSE ordering, discharge consistency, critical depth transitions |

**Run all checks**:
```python
results = RasCheck.run_all("01")  # Executes all 5 checks
```

**Run individual check**:
```python
# Get HDF path from plan
plan_row = ras.plan_df[ras.plan_df['plan_number'] == "01"].iloc[0]
geom_hdf = Path(plan_row['Geom Path']).with_suffix('.hdf')

# Run specific check
nt_results = RasCheck.check_nt(geom_hdf)
xs_results = RasCheck.check_xs(geom_hdf)
```

## RasFixit Repair Capabilities

**Source**: `C:\GH\ras-commander\ras_commander\fixit\AGENTS.md` (complete file)

**Current Fix Types**:
- `fix_blocked_obstructions()` - Repair overlapping/adjacent blocked obstructions
- `detect_obstruction_overlaps()` - Non-destructive detection only

**Fix Results**:
```python
# FixResults dataclass contains:
# - total_xs_checked: Cross sections scanned
# - total_xs_fixed: Cross sections modified
# - messages: List of FixMessage objects
# - backup_path: Path to timestamped backup
# - visualization_folder: Path to PNG folder

# FixMessage contains:
# - station: River station (e.g., "12345.67")
# - action: FixAction enum (OVERLAP_RESOLVED, GAP_INSERTED, etc.)
# - original_data: List of original (start, end, elev) tuples
# - fixed_data: List of fixed (start, end, elev) tuples
# - original_count: Number of original obstructions
# - fixed_count: Number of fixed obstructions
```

**Export to DataFrame**:
```python
df = fix_results.to_dataframe()
df.to_csv("obstruction_fixes.csv", index=False)
```

## Engineering Review Requirements

**CRITICAL**: All automated fixes MUST be reviewed by a licensed professional engineer before use in production models.

### Required Documentation

1. **Timestamped backups**: Always use `backup=True`
2. **Before/after visualizations**: Always use `visualize=True`
3. **Audit trail**: Export `FixResults.to_dataframe()` to CSV
4. **Algorithm documentation**: Include elevation envelope algorithm description

### Verification Steps

1. **Visual inspection**: Review all PNG visualizations
2. **Compare hydraulics**: Run model with original and fixed geometry
3. **Spot check**: Manually verify critical cross sections in HEC-RAS GUI
4. **Professional judgment**: Ensure fixes align with engineering intent

## Module Organization

### RasCheck (check subpackage)
```
check/
├── __init__.py         # Exports RasCheck, CheckMessage, etc.
├── RasCheck.py         # Main static class (448 KB)
├── messages.py         # CheckMessage templates (106 KB)
├── report.py           # Report generation (23 KB)
├── thresholds.py       # CheckThresholds configuration (18 KB)
└── CLAUDE.md           # Primary source documentation (262 lines)
```

### RasFixit (fixit subpackage)
```
fixit/
├── __init__.py         # Exports RasFixit, FixResults, FixMessage, FixAction
├── RasFixit.py         # Main static class with fix methods
├── obstructions.py     # BlockedObstruction and elevation envelope algorithm
├── results.py          # FixAction enum, FixMessage, FixResults dataclasses
├── visualization.py    # Lazy-loaded matplotlib PNG generation
├── log_parser.py       # HEC-RAS compute log parsing
└── AGENTS.md           # Primary source documentation (119 lines)
```

## Common Issues and Solutions

### Issue: Geometry preprocessing fails with obstruction errors

```python
# 1. Detect obstructions
results = RasFixit.detect_obstruction_overlaps("model.g01")
if results.total_xs_fixed > 0:
    # 2. Fix obstructions
    fix_results = RasFixit.fix_blocked_obstructions(
        "model.g01",
        backup=True,
        visualize=True
    )
    print(f"Fixed {fix_results.total_xs_fixed} cross sections")
```

### Issue: FEMA validation warnings

```python
# Run validation and generate report
results = RasCheck.run_all("01")
results.to_html("fema_validation.html")

# Address errors (severity=ERROR)
df = results.to_dataframe()
errors = df[df['severity'] == 'ERROR']
print(errors[['station', 'message']])
```

### Issue: Manning's n out of range

```python
# Run NT check
nt_results = RasCheck.check_nt(geom_hdf)
df = nt_results.to_dataframe()

# Filter Manning's n issues
n_issues = df[df['message_id'].str.startswith('NT_RC')]
print(n_issues[['station', 'message']])
```

### Issue: Cross section spacing too large

```python
# Run XS check with custom threshold
custom = create_custom_thresholds({
    'reach_length.max_length_ft': 1500.0  # More conservative
})
xs_results = RasCheck.check_xs(geom_hdf, thresholds=custom)
```

## Log Parsing for Automated Workflows

**Source**: `C:\GH\ras-commander\ras_commander\fixit\AGENTS.md` (line 18)

```python
from ras_commander.fixit import log_parser

# Parse HEC-RAS compute log
with open("compute.log", 'r') as f:
    log_content = f.read()

# Detect obstruction errors
if log_parser.has_obstruction_errors(log_content):
    errors = log_parser.detect_obstruction_errors(log_content)
    stations = log_parser.extract_cross_section_ids(log_content)

    # Generate error report
    report = log_parser.generate_error_report(errors)
    print(report)
```

## Performance Characteristics

**RasCheck**:
- Typical 1D model: 5-15 seconds
- Large 2D model: 30-60 seconds
- Low memory footprint (suitable for 10,000+ cross sections)
- Parallel checking supported for multiple plans

**RasFixit**:
- < 1 second per cross section repair
- Visualization: 2-3 seconds per PNG (optional)

## Navigation Map

**For validation questions** → Read `C:\GH\ras-commander\ras_commander\check\CLAUDE.md`

**For repair questions** → Read `C:\GH\ras-commander\ras_commander\fixit\AGENTS.md`

**For workflow examples** → See notebooks:
- `examples\200_fixit_blocked_obstructions.ipynb`
- `examples\300_quality_assurance_rascheck.ipynb`

**For API details** → Read source code docstrings:
- `ras_commander\check\RasCheck.py`
- `ras_commander\fixit\RasFixit.py`

## Related Skills

- **quality-assurance subagent**: `.claude\agents\quality-assurance\SUBAGENT.md`
- **Testing approach**: `.claude\rules\testing\tdd-approach.md`

## State-Specific Floodway Surcharge Limits

**Source**: `C:\GH\ras-commander\ras_commander\check\CLAUDE.md` (lines 198-220)

States with non-standard surcharge limits (vs FEMA default 1.0 ft):
- **IL**: 0.1 ft
- **WI**: 0.0 ft (no surcharge allowed)
- **MN**: 0.5 ft
- **NJ**: 0.2 ft
- **MI, IN, OH**: 0.5 ft
- **Default (TX, most states)**: 1.0 ft

```python
from ras_commander.check import get_state_surcharge_limit

# Get state-specific limit
limit = get_state_surcharge_limit('IL')  # Returns 0.1
results = RasCheck.run_all("01", surcharge=limit)
```

---

**Total Lines**: ~390 (target: 300-400)

**Primary sources contain**: 262 + 119 = 381 lines of authoritative documentation
**This skill**: Lightweight index with critical warnings and navigation guidance
