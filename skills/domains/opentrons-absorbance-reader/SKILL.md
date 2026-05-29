---
name: opentrons-absorbance-reader
description: Opentrons Absorbance Plate Reader Module for Flex - on-deck microplate spectrophotometry with single/multi-wavelength reading (450, 562, 600, 650nm), automated lid control, and CSV data export for ELISA, cell growth, and colorimetric assays
allowed-tools: ["*"]
---

# Opentrons Absorbance Plate Reader Module

## Overview

The **Absorbance Plate Reader Module** is an on-deck microplate spectrophotometer exclusively for Opentrons Flex. It measures light absorbance in 96-well plates at up to 6 wavelengths simultaneously, enabling automated ELISA, cell density measurements, colorimetric assays, and kinetic readings without manual plate transfers.

**Core value:** Eliminate manual plate reader transfers. Read absorbance mid-protocol to make real-time decisions or collect kinetic data with automated timing and liquid handling.

**Platform:** Opentrons Flex only (not compatible with OT-2)

## When to Use

Use the Absorbance Reader skill when:
- Running ELISA or other colorimetric assays requiring absorbance reading
- Measuring bacterial or cell culture growth (OD600)
- Performing kinetic assays with timed readings
- Collecting multi-wavelength absorbance data
- Protocols requiring real-time decision-making based on absorbance values
- Automating plate-based biochemical assays

**Don't use when:**
- Working with OT-2 robot (module is Flex-only)
- Need wavelengths outside 450, 562, 600, 650nm
- Require fluorescence or luminescence measurements
- Need higher spectral resolution or broader wavelength range

## Quick Reference

| Operation | Method | Key Parameters |
|-----------|--------|----------------|
| Load module | `protocol.load_module()` | `"absorbanceReaderV1"`, "D3" (or A3-C3) |
| Close lid | `close_lid()` | - |
| Open lid | `open_lid()` | - |
| Check lid status | `is_lid_on()` | Returns bool |
| Initialize reader | `initialize()` | mode, wavelengths, reference_wavelength |
| Read plate | `read()` | export_filename (optional) |

**Available wavelengths:** 450nm (blue), 562nm (green), 600nm (orange), 650nm (red)

## Platform Requirements

**Opentrons Flex only**
- **API version:** 2.21 or later
- **Compatible deck slots:** A3, B3, C3, D3 (column 3 only)
- **Staging area:** Column 4 (entire column reserved for lid storage)

**Important:** Cannot load any labware in column 4 (A4, B4, C4, D4) when absorbance reader is present.

## Deck Layout

```
Column 3 (Reader)  Column 4 (Staging - Reserved)
┌─────────────┐    ┌─────────────┐
│     A3      │───▶│  A4 (Lid)   │
│   Reader    │    │  Reserved   │
│   Module    │    │             │
└─────────────┘    └─────────────┘
```

**Reader occupies column 3** - Detection unit and plate holder
**Column 4 reserved** - Lid staging area (gripper moves lid here when open)

## Loading the Module

```python
from opentrons import protocol_api

metadata = {'apiLevel': '2.21'}
requirements = {"robotType": "Flex", "apiLevel": "2.21"}

def run(protocol: protocol_api.ProtocolContext):
    # Load Absorbance Reader in column 3
    reader = protocol.load_module("absorbanceReaderV1", "D3")

    # Note: Column 4 is now unavailable for labware
```

**Compatible slots:** A3, B3, C3, D3
**Recommended:** D3 (bottom-right position for easy gripper access)

## Lid Control

The gripper manages lid position automatically:

```python
# Close lid (required before initialization)
reader.close_lid()

# Check lid status
if reader.is_lid_on():
    protocol.comment("Lid is on detection unit")

# Open lid (moves to staging area in column 4)
reader.open_lid()
```

**Lid positions:**
- **Closed:** Lid covers detection unit on module
- **Open:** Lid stored in staging area (column 4)

**Critical:** Always call `close_lid()` before `initialize()`, even if lid is already closed.

## Initialization

The `initialize()` method configures the reader with measurement parameters.

### Single Wavelength Reading

Simplest mode - read at one wavelength:

```python
# Initialize for single wavelength
reader.close_lid()
reader.initialize(mode="single", wavelengths=[450])
reader.open_lid()
```

**Use case:** OD600 bacterial growth, single-color ELISA

### Single Wavelength with Reference

Normalize readings against a reference wavelength:

```python
# Initialize with reference wavelength
reader.close_lid()
reader.initialize(
    mode="single",
    wavelengths=[450],
    reference_wavelength=562
)
reader.open_lid()
```

**Use case:** Reduce background noise, normalize for plate artifacts

### Multi-Wavelength Reading

Read up to 6 wavelengths simultaneously:

```python
# Initialize for multiple wavelengths
reader.close_lid()
reader.initialize(
    mode="multi",
    wavelengths=[450, 562, 600, 650]
)
reader.open_lid()
```

**Use case:** Multi-analyte assays, spectral analysis, dual-wavelength ELISA

**Available wavelengths:**
- **450nm** - Blue (common ELISA substrate TMB)
- **562nm** - Green (BCA protein assay)
- **600nm** - Orange (bacterial growth OD600)
- **650nm** - Red (alternative reference wavelength)

**Maximum:** 6 wavelengths per reading

## Reading Plates

### Basic Reading

```python
# Move plate to reader with gripper
protocol.move_labware(assay_plate, reader, use_gripper=True)

# Close lid
reader.close_lid()

# Read plate
absorbance_data = reader.read()

# Open lid
reader.open_lid()

# Move plate off reader
protocol.move_labware(assay_plate, "C1", use_gripper=True)
```

### Reading with CSV Export

```python
# Read and export data
absorbance_data = reader.read(export_filename="experiment_001_plate1")

# CSV file saved to robot and accessible via Opentrons App
```

**Export format:** CSV file with plate layout, metadata (wavelengths, serial number, timestamps)

### Accessing Reading Results

Results are returned as nested dictionary: `{wavelength: {well: absorbance}}`

```python
# Read plate at 450nm
data = reader.read()

# Access specific well at 450nm
absorbance_a1 = data[450]["A1"]

protocol.comment(f"Well A1 absorbance at 450nm: {absorbance_a1}")

# Iterate through all wells at 600nm
for well_name, absorbance in data[600].items():
    protocol.comment(f"{well_name}: {absorbance}")
```

**Value range:** 0.0 - 4.0 OD (optical density)

### Multi-Wavelength Data Access

```python
# Initialize with multiple wavelengths
reader.initialize(mode="multi", wavelengths=[450, 600])

# Read plate
data = reader.read()

# Access different wavelengths
od450_a1 = data[450]["A1"]
od600_a1 = data[600]["A1"]

protocol.comment(f"A1: OD450={od450_a1}, OD600={od600_a1}")

# Calculate ratio
if od600_a1 > 0:
    ratio = od450_a1 / od600_a1
    protocol.comment(f"450/600 ratio: {ratio}")
```

## Data Formats

### In-Protocol Dictionary Format

```python
{
    450: {
        "A1": 0.123,
        "A2": 0.145,
        "A3": 0.167,
        # ... all 96 wells
        "H12": 0.089
    },
    600: {
        "A1": 0.456,
        # ... all 96 wells
    }
}
```

**Structure:**
- Top level: Wavelengths (450, 562, 600, 650)
- Second level: Well names ("A1" - "H12")
- Values: Absorbance (0.0 - 4.0 OD)

### CSV Export Format

```csv
Opentrons Flex Absorbance Plate Reader
Serial: ABC123456
Wavelength: 450nm
Date: 2024-11-09
Time: 14:32:01

    1      2      3      4      5      6  ...  12
A  0.123  0.145  0.167  0.189  0.201  0.223  ...  0.089
B  0.234  0.256  0.278  0.290  0.312  0.334  ...  0.190
C  0.345  0.367  0.389  0.401  0.423  0.445  ...  0.291
...
H  0.456  0.478  0.490  0.512  0.534  0.556  ...  0.392
```

**Metadata included:**
- Module serial number
- Wavelength(s) measured
- Timestamp
- Plate layout with row/column labels

## Complete Workflow Pattern

### Standard Reading Workflow

```python
# 1. Load and setup
reader = protocol.load_module("absorbanceReaderV1", "D3")
plate = protocol.load_labware("corning_96_wellplate_360ul_flat", "B1")
pipette = protocol.load_instrument("flex_8channel_1000", "left")

# 2. Initialize reader (empty)
reader.close_lid()
reader.initialize(mode="single", wavelengths=[450])
reader.open_lid()

# 3. Prepare samples
# ... pipetting operations ...

# 4. Move plate to reader
protocol.move_labware(plate, reader, use_gripper=True)

# 5. Read plate
reader.close_lid()
data = reader.read(export_filename="my_assay_data")
reader.open_lid()

# 6. Process results or continue protocol
for well in plate.wells():
    if data[450][well.well_name] > 1.0:
        protocol.comment(f"{well.well_name} is positive")

# 7. Move plate off reader
protocol.move_labware(plate, "C1", use_gripper=True)
```

## Common Patterns

### ELISA Protocol

```python
# Setup
reader = protocol.load_module("absorbanceReaderV1", "D3")
elisa_plate = protocol.load_labware("corning_96_wellplate_360ul_flat", "C2")
pipette = protocol.load_instrument("flex_8channel_1000", "left")

# Initialize reader
reader.close_lid()
reader.initialize(mode="single", wavelengths=[450], reference_wavelength=562)
reader.open_lid()

# 1. Coat plate, incubate, wash (not shown)

# 2. Add samples
pipette.transfer(100, samples, elisa_plate.wells()[:24])

# 3. Incubate
protocol.delay(minutes=60)

# 4. Wash steps
for _ in range(3):
    # Wash logic (not shown)
    pass

# 5. Add substrate
pipette.transfer(100, substrate, elisa_plate.wells()[:24])

# 6. Incubate
protocol.delay(minutes=15)

# 7. Add stop solution
pipette.transfer(50, stop_solution, elisa_plate.wells()[:24])

# 8. Read plate
protocol.move_labware(elisa_plate, reader, use_gripper=True)
reader.close_lid()
elisa_data = reader.read(export_filename="elisa_450nm_results")
reader.open_lid()

# 9. Analyze results
for well in elisa_plate.wells()[:24]:
    od450 = elisa_data[450][well.well_name]
    if od450 > 0.5:
        protocol.comment(f"{well.well_name}: POSITIVE (OD450={od450:.3f})")
    else:
        protocol.comment(f"{well.well_name}: NEGATIVE (OD450={od450:.3f})")
```

### Bacterial Growth Kinetics

```python
# Setup
reader = protocol.load_module("absorbanceReaderV1", "D3")
culture_plate = protocol.load_labware("corning_96_wellplate_360ul_flat", "C2")
hs_mod = protocol.load_module("heaterShakerModuleV1", "D1")

# Initialize reader for OD600
reader.close_lid()
reader.initialize(mode="single", wavelengths=[600])
reader.open_lid()

# Inoculate cultures (not shown)

# Kinetic reading loop
for timepoint in range(8):  # 8 timepoints
    # Incubate on heater-shaker
    protocol.move_labware(culture_plate, hs_mod, use_gripper=True)
    hs_mod.set_and_wait_for_temperature(37)
    hs_mod.close_labware_latch()
    hs_mod.set_and_wait_for_shake_speed(300)
    protocol.delay(hours=1)
    hs_mod.deactivate_shaker()
    hs_mod.deactivate_heater()
    hs_mod.open_labware_latch()

    # Read OD600
    protocol.move_labware(culture_plate, reader, use_gripper=True)
    reader.close_lid()
    od_data = reader.read(export_filename=f"growth_curve_t{timepoint}")
    reader.open_lid()

    # Log growth
    for well in culture_plate.wells()[:8]:
        od600 = od_data[600][well.well_name]
        protocol.comment(f"T{timepoint}h {well.well_name}: OD600={od600:.3f}")

# Return plate to deck
protocol.move_labware(culture_plate, "B1", use_gripper=True)
```

### Multi-Wavelength Protein Assay

```python
# Setup for BCA or Bradford assay
reader = protocol.load_module("absorbanceReaderV1", "D3")
assay_plate = protocol.load_labware("corning_96_wellplate_360ul_flat", "C2")

# Initialize for multi-wavelength
reader.close_lid()
reader.initialize(mode="multi", wavelengths=[562, 600])
reader.open_lid()

# Prepare standard curve + samples (not shown)

# Incubate
protocol.delay(minutes=30)

# Read at multiple wavelengths
protocol.move_labware(assay_plate, reader, use_gripper=True)
reader.close_lid()
absorbance = reader.read(export_filename="protein_assay_multi_wl")
reader.open_lid()

# Calculate protein concentrations using standard curve
for well in assay_plate.wells()[:24]:
    od562 = absorbance[562][well.well_name]
    od600 = absorbance[600][well.well_name]

    # Example: simple linear standard curve
    protein_conc = od562 * 100  # µg/mL (simplified)
    protocol.comment(f"{well.well_name}: {protein_conc:.1f} µg/mL")
```

### Real-Time Decision Making

```python
# Read plate and perform conditional operations
protocol.move_labware(screening_plate, reader, use_gripper=True)
reader.close_lid()
screen_data = reader.read()
reader.open_lid()
protocol.move_labware(screening_plate, "C1", use_gripper=True)

# Identify hits and cherry-pick
hit_wells = []
for well_name, absorbance in screen_data[450].items():
    if absorbance > 2.0:  # Hit threshold
        hit_wells.append(screening_plate.wells_by_name()[well_name])
        protocol.comment(f"HIT: {well_name} (OD450={absorbance:.3f})")

# Transfer hits to new plate for follow-up
if hit_wells:
    pipette.transfer(50, hit_wells, hit_plate.wells()[:len(hit_wells)])
    protocol.comment(f"Found {len(hit_wells)} hits - transferred for validation")
```

## Best Practices

1. **Always close lid before initialization** - Even if already closed
2. **Export data with descriptive filenames** - Include experiment ID, date, plate number
3. **Use reference wavelengths** - Reduces background and plate artifacts
4. **Read blank wells** - Establish baseline for background subtraction
5. **Include standard curves** - For quantitative assays
6. **Plan deck layout carefully** - Column 4 is reserved for lid storage
7. **Protect column 4** - Never attempt to load labware in staging area
8. **Allow plate equilibration** - Brief delay after moving to reader prevents condensation issues
9. **Check gripper compatibility** - Ensure plates have grippable geometry
10. **Document wavelength selection** - Comment why specific wavelengths were chosen

## Common Mistakes

**❌ Initializing with lid open:**
```python
reader.initialize(mode="single", wavelengths=[450])  # Error: lid must be closed
```

**✅ Correct:**
```python
reader.close_lid()
reader.initialize(mode="single", wavelengths=[450])
reader.open_lid()
```

**❌ Loading labware in column 4:**
```python
reader = protocol.load_module("absorbanceReaderV1", "D3")
tips = protocol.load_labware("opentrons_flex_96_tiprack_1000ul", "D4")  # Error: reserved
```

**✅ Correct:**
```python
reader = protocol.load_module("absorbanceReaderV1", "D3")
tips = protocol.load_labware("opentrons_flex_96_tiprack_1000ul", "D2")  # Use different column
```

**❌ Reading without closing lid:**
```python
protocol.move_labware(plate, reader, use_gripper=True)
data = reader.read()  # Error: lid must be closed for reading
```

**✅ Correct:**
```python
protocol.move_labware(plate, reader, use_gripper=True)
reader.close_lid()
data = reader.read()
reader.open_lid()
```

**❌ Using unsupported wavelength:**
```python
reader.initialize(mode="single", wavelengths=[550])  # Error: not supported
```

**✅ Correct:**
```python
reader.initialize(mode="single", wavelengths=[562])  # Use 450, 562, 600, or 650
```

**❌ Accessing wrong wavelength in data:**
```python
reader.initialize(mode="single", wavelengths=[450])
data = reader.read()
od600 = data[600]["A1"]  # Error: only 450nm was measured
```

**✅ Correct:**
```python
reader.initialize(mode="single", wavelengths=[450])
data = reader.read()
od450 = data[450]["A1"]  # Access wavelength that was measured
```

## Troubleshooting

**Module not loading:**
- Verify API version is 2.21 or later
- Check `robotType: "Flex"` in requirements
- Ensure module is in column 3 slot (A3-D3)

**Lid errors:**
- Always call `close_lid()` before `initialize()`
- Ensure column 4 staging area is clear
- Check gripper is functioning properly

**Reading errors:**
- Verify lid is closed before `read()`
- Check plate is on module
- Ensure wavelengths match those set in `initialize()`

**Data access errors:**
- Access wavelengths that were initialized
- Use correct well names ("A1" not "a1")
- Check data type (dict, not list)

**Gripper cannot move plate:**
- Verify plate has grippable geometry
- Ensure reader lid is open before moving plate onto/off module
- Check plate is compatible with reader (96-well plates)

## Integration with Other Modules

### With Heater-Shaker Module

```python
# Incubate with shaking, read absorbance
hs_mod = protocol.load_module("heaterShakerModuleV1", "D1")
reader = protocol.load_module("absorbanceReaderV1", "D3")

# Setup plate on heater-shaker
protocol.move_labware(assay_plate, hs_mod, use_gripper=True)
hs_mod.set_and_wait_for_temperature(37)
hs_mod.close_labware_latch()
hs_mod.set_and_wait_for_shake_speed(400)
protocol.delay(minutes=30)
hs_mod.deactivate_shaker()
hs_mod.deactivate_heater()
hs_mod.open_labware_latch()

# Move to reader
protocol.move_labware(assay_plate, reader, use_gripper=True)
reader.close_lid()
data = reader.read()
reader.open_lid()
```

### With Temperature Module

```python
# Cool samples, then read
temp_mod = protocol.load_module("temperature module gen2", "D1")
reader = protocol.load_module("absorbanceReaderV1", "C3")

# Cool plate
protocol.move_labware(assay_plate, temp_mod, use_gripper=True)
temp_mod.set_temperature(4)
protocol.delay(minutes=5)

# Read cooled plate
protocol.move_labware(assay_plate, reader, use_gripper=True)
reader.close_lid()
data = reader.read()
reader.open_lid()

temp_mod.deactivate()
```

## CSV Data Export

Exported CSV files are stored on the robot and accessible via the Opentrons App:

1. Complete protocol run
2. Open Opentrons App
3. Navigate to completed protocol run
4. Download exported CSV files
5. Analyze in Excel, Python, R, or other tools

**File naming:** Use descriptive `export_filename` parameter for easy identification

```python
data = reader.read(export_filename=f"experiment_{exp_id}_plate_{plate_num}_timepoint_{t}")
```

## API Version Requirements

- **Minimum API version:** 2.21
- **Robot type:** Opentrons Flex only
- **Recommended:** Latest API version for full feature support

## Additional Resources

- **Module Documentation:** https://docs.opentrons.com/v2/modules/absorbance_plate_reader.html
- **Opentrons Support:** https://support.opentrons.com/
- **Protocol Examples:** https://protocols.opentrons.com/

## Related Skills

- `opentrons` - Main Opentrons Python API skill
- `opentrons-gripper` - Automated labware movement (required for plate reader)
- `opentrons-heater-shaker` - Temperature control with mixing (common integration)
- `opentrons-temperature-module` - Temperature control for assays
