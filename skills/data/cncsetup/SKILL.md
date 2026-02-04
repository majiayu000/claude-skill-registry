---
name: Cncsetup
description: Generate standardized CNC setup sheets for MNMUK machine shop. Covers DMG MORI mills/lathes, CITIZEN Swiss, MITSUBISHI EDM, and Haas machines. USE WHEN user says 'setup sheet', 'create setup', 'job setup', 'machine setup', 'tooling list', 'fixture setup', or 'new job' for any CNC operation.
---

# CNCSetup - MNMUK Setup Sheet Generator

**Purpose:** Standardized setup documentation to reduce setup time, prevent errors, and capture tribal knowledge.

## When to Activate
- "Create a setup sheet for [part/job]"
- "Setup for [machine name]"
- "New job setup on the NLX2500"
- "Tooling list for [operation]"
- "Document the setup for [part number]"

---

## Setup Sheet Templates by Machine Type

### DMG MORI 5-AXIS MILLS (NMV3000, DMU50, NHX500)

```markdown
# SETUP SHEET - 5-AXIS MILLING

## Job Information
| Field | Value |
|-------|-------|
| Part Number | |
| Part Name | |
| Customer | |
| Operation | |
| Machine | [ ] NMV3000  [ ] DMU50  [ ] NHX500 |
| Program Number | |
| Setup By | |
| Date | |

## Workholding
| Item | Details |
|------|---------|
| Fixture ID | |
| Fixture Location | |
| Clamping Method | |
| Clamping Torque | Nm |
| Pallet Number | |
| Datum/WCS | G54 / G55 / Other: |

## Work Offset Setup
| Axis | Value | Method |
|------|-------|--------|
| X | | Probe / Edge finder / Indicator |
| Y | | Probe / Edge finder / Indicator |
| Z | | Probe / Tool setter |
| A | | |
| B/C | | |

## Tool List
| T# | Description | Diameter | Length | Offset | Notes |
|----|-------------|----------|--------|--------|-------|
| T1 | | | | H1 D1 | |
| T2 | | | | H2 D2 | |
| T3 | | | | H3 D3 | |
| T4 | | | | H4 D4 | |
| T5 | | | | H5 D5 | |

## CELOS Settings
| Parameter | Value |
|-----------|-------|
| Spindle Warm-up | [ ] Required  [ ] Not Required |
| Coolant Type | [ ] Flood  [ ] Through-spindle  [ ] Mist |
| Coolant Pressure | bar |
| Chip Conveyor | [ ] On  [ ] Off |

## Critical Dimensions (First-Off Check)
| Feature | Nominal | Tolerance | Actual | OK |
|---------|---------|-----------|--------|-----|
| | | ± | | [ ] |
| | | ± | | [ ] |
| | | ± | | [ ] |

## Safety & Notes
- [ ] Guards in place
- [ ] Correct PPE worn
- [ ] Program proven at reduced feed

### Special Instructions:


### Known Issues / Tips:

```

---

### DMG MORI TURNING CENTRES (NLX2500, ALX2000)

```markdown
# SETUP SHEET - CNC TURNING

## Job Information
| Field | Value |
|-------|-------|
| Part Number | |
| Part Name | |
| Customer | |
| Operation | OP10 / OP20 / Complete |
| Machine | [ ] NLX2500 Twin  [ ] NLX2500 Single  [ ] ALX2000 |
| Program Number | |
| Setup By | |
| Date | |

## Material & Stock
| Item | Details |
|------|---------|
| Material | |
| Stock Type | [ ] Bar  [ ] Billet  [ ] Forging  [ ] Casting |
| Stock Size | Ø x L mm |
| Bar Feeder | [ ] Yes  [ ] No |
| Bar Stop Position | mm from chuck face |

## Workholding - Main Spindle
| Item | Details |
|------|---------|
| Chuck Type | [ ] 3-jaw  [ ] Collet  [ ] Special |
| Chuck ID/Size | |
| Jaw Type | [ ] Hard  [ ] Soft  [ ] Pie jaws |
| Jaw Bore | Ø mm |
| Grip Length | mm |
| Clamping Pressure | bar |

## Workholding - Sub Spindle (if applicable)
| Item | Details |
|------|---------|
| Chuck Type | [ ] 3-jaw  [ ] Collet |
| Jaw Type | [ ] Hard  [ ] Soft |
| Grip Length | mm |
| Part-off Position | mm |
| Transfer Method | |

## Work Offset Setup
| Offset | Value | Method |
|--------|-------|--------|
| Z (Face) | | Touch-off / Probe |
| X (Diameter) | | Test cut / Probe |

## Tool List - Turret
| T# | Station | Description | Insert | Orientation | Offset | Notes |
|----|---------|-------------|--------|-------------|--------|-------|
| T1 | | | | | | |
| T2 | | | | | | |
| T3 | | | | | | |
| T4 | | | | | | |

## Live Tooling (if applicable)
| T# | Station | Description | RPM | Notes |
|----|---------|-------------|-----|-------|
| | | | | |

## Cutting Parameters Reference
| Operation | Speed (m/min) | Feed (mm/rev) | DOC (mm) |
|-----------|---------------|---------------|----------|
| Rough OD | | | |
| Finish OD | | | |
| Rough ID | | | |
| Finish ID | | | |
| Thread | | | |
| Part-off | | | |

## Coolant Settings
| Parameter | Value |
|-----------|-------|
| Coolant Type | [ ] Flood  [ ] High-pressure |
| HP Coolant Pressure | bar |
| Chip Conveyor | [ ] On  Direction: |

## Critical Dimensions (First-Off)
| Feature | Nominal | Tolerance | Actual | OK |
|---------|---------|-----------|--------|-----|
| OD 1 | Ø | ± | | [ ] |
| OD 2 | Ø | ± | | [ ] |
| Length | | ± | | [ ] |
| Thread | | Class | | [ ] |

## Cycle Time
| Phase | Time |
|-------|------|
| Load | sec |
| Cut Cycle | sec |
| Unload | sec |
| **Total** | sec |

### Special Instructions:


### Known Issues / Tips:

```

---

### HARDINGE TWIN SPINDLE TURNING

```markdown
# SETUP SHEET - HARDINGE TURNING

## Job Information
| Field | Value |
|-------|-------|
| Part Number | |
| Part Name | |
| Operation | |
| Program Number | |
| Setup By | |
| Date | |

## Stock
| Item | Details |
|------|---------|
| Material | |
| Stock Size | Ø x L mm |
| Bar Feed | [ ] Yes  [ ] No |

## Workholding
| Spindle | Chuck | Collet/Jaw | Grip | Pressure |
|---------|-------|------------|------|----------|
| Main | | | mm | bar |
| Sub | | | mm | bar |

## Precision Notes (±0.003mm capability)
| Parameter | Setting |
|-----------|---------|
| Warm-up Cycle | [ ] Required - Run time: min |
| Temperature Stability | [ ] Verified |
| Probe Calibration | [ ] Verified |

## Tool List
| T# | Description | Insert | Offset | Notes |
|----|-------------|--------|--------|-------|
| | | | | |

## Critical Dimensions
| Feature | Nominal | Tol | Gage | Method |
|---------|---------|-----|------|--------|
| | | ±0.003 | | |

### Precision Tips:
- Allow 20-min spindle warm-up for best tolerance
- Verify coolant temperature stable
- Use in-process gauging for critical features

```

---

### CITIZEN SWISS-TYPE (Sliding Head)

```markdown
# SETUP SHEET - CITIZEN SWISS

## Job Information
| Field | Value |
|-------|-------|
| Part Number | |
| Part Name | |
| Machine | [ ] Citizen Laser Head  [ ] Citizen LFV |
| Program Number | |
| Setup By | |
| Date | |

## Material & Bar Stock
| Item | Details |
|------|---------|
| Material | |
| Bar Diameter | Ø mm (max Ø38.1mm) |
| Bar Length | mm |
| Bar Supplier/Heat | |

## Guide Bushing Setup
| Parameter | Value |
|-----------|-------|
| Guide Bushing Size | Ø mm |
| Bushing Type | [ ] Rotating  [ ] Fixed |
| Bushing Material | [ ] Carbide  [ ] Bronze |
| Z-axis Reference | mm |

## Main Spindle Collet
| Parameter | Value |
|-----------|-------|
| Collet Size | Ø mm |
| Clamping Pressure | bar |
| Stock Stick-out | mm |

## Sub Spindle Setup
| Parameter | Value |
|-----------|-------|
| Collet Size | Ø mm |
| Pickup Position | Z = mm |
| Grip Length | mm |

## Tool List - Gang Slide
| Position | Tool | Insert/Size | Offset | Notes |
|----------|------|-------------|--------|-------|
| | | | | |
| | | | | |
| | | | | |

## Tool List - Back Working
| Position | Tool | Insert/Size | Notes |
|----------|------|-------------|-------|
| | | | |
| | | | |

## LFV Settings (if LFV machine)
| Parameter | Value |
|-----------|-------|
| LFV Mode | [ ] On  [ ] Off |
| Oscillation Frequency | Hz |
| Amplitude | mm |
| Applied To | [ ] OD  [ ] ID  [ ] Drilling |

## Laser Head Settings (if Laser machine)
| Parameter | Value |
|-----------|-------|
| Laser Operation | [ ] Marking  [ ] Cutting  [ ] N/A |
| Power | W |
| Program | |

## Coolant
| Type | Setting |
|------|---------|
| Oil Type | |
| Pressure | bar |
| Mist | [ ] On  [ ] Off |

## Critical Dimensions (±0.003mm capability)
| Feature | Nominal | Tol | Method |
|---------|---------|-----|--------|
| | | ± | |
| | | ± | |

## Cycle Time Target
| | Time |
|--|------|
| Cycle | sec |
| Parts/Hour | |

### Swiss-Specific Tips:
- Verify guide bushing alignment before production
- Check oil level and filtration
- LFV excellent for 316SS and titanium chip breaking
- Monitor bar remnant length

```

---

### MITSUBISHI EDM (Wire & Spark)

```markdown
# SETUP SHEET - EDM

## Job Information
| Field | Value |
|-------|-------|
| Part Number | |
| Part Name | |
| Machine | [ ] Wire EDM  [ ] Spark EDM |
| Program Number | |
| Setup By | |
| Date | |

## Workpiece
| Item | Details |
|------|---------|
| Material | |
| Hardness | HRC |
| Dimensions | L x W x H mm |
| Weight | kg |

---

## WIRE EDM SETUP

### Wire Settings
| Parameter | Value |
|-----------|-------|
| Wire Type | [ ] Brass  [ ] Coated  [ ] Other: |
| Wire Diameter | mm |
| Wire Tension | g |
| Wire Speed | m/min |

### Workholding
| Item | Details |
|------|---------|
| Fixture Type | |
| Leveling | [ ] Verified |
| Start Hole | X: Y: (if applicable) |

### Cutting Parameters
| Pass | Power | On-Time | Off-Time | Wire Speed | Offset |
|------|-------|---------|----------|------------|--------|
| Rough | | μs | μs | m/min | mm |
| Semi | | μs | μs | m/min | mm |
| Finish | | μs | μs | m/min | mm |
| Skim | | μs | μs | m/min | mm |

### Flushing
| Parameter | Value |
|-----------|-------|
| Upper Nozzle | mm gap |
| Lower Nozzle | mm gap |
| Flushing Pressure | bar |
| Submerged | [ ] Yes  [ ] No |

---

## SPARK EDM (SINKER) SETUP

### Electrode
| Parameter | Value |
|-----------|-------|
| Electrode Material | [ ] Copper  [ ] Graphite |
| Electrode ID | |
| Undersize | mm |
| Polarity | [ ] +  [ ] - |

### Cutting Parameters
| Phase | Current | On-Time | Off-Time | Depth |
|-------|---------|---------|----------|-------|
| Rough | A | μs | μs | mm |
| Semi | A | μs | μs | mm |
| Finish | A | μs | μs | mm |

### Flushing
| Method | Setting |
|--------|---------|
| Type | [ ] Jet  [ ] Suction  [ ] Orbital |
| Pressure | bar |
| Retract Height | mm |
| Jump Frequency | |

---

## Dielectric
| Parameter | Value |
|-----------|-------|
| Type | |
| Level | [ ] Verified |
| Filter Status | [ ] OK |
| Conductivity | μS |

## Critical Dimensions (Wire: ±0.004mm, Spark: ±0.050mm)
| Feature | Nominal | Tol | Actual | OK |
|---------|---------|-----|--------|-----|
| | | ± | | [ ] |

### EDM Tips:
- Wire: Check wire path and guides before start
- Spark: Verify electrode alignment with workpiece
- Monitor dielectric condition
- Log electrode wear for repeat jobs

```

---

### HAAS FAST RESPONSE CELL (Mini Mill & Tool Room Lathe)

```markdown
# SETUP SHEET - HAAS FAST RESPONSE

## Job Information
| Field | Value |
|-------|-------|
| Part Number | |
| Part Name | |
| Machine | [ ] Mini Mill  [ ] Tool Room Lathe |
| Program Number | |
| Setup By | |
| Date | |
| Priority | [ ] Urgent  [ ] Standard |

## Purpose
[ ] Prototype  [ ] First Article  [ ] Repair  [ ] One-off  [ ] Prove-out

---

## MINI MILL SETUP

### Workholding
| Item | Details |
|------|---------|
| Vice/Fixture | |
| Parallels | Height: mm |
| Stop Position | |
| WCS | G54 |

### Tool List
| T# | Description | Diameter | Length | Notes |
|----|-------------|----------|--------|-------|
| T1 | | | | |
| T2 | | | | |
| T3 | | | | |

### Work Offsets
| Axis | Value | Method |
|------|-------|--------|
| X | | Edge finder |
| Y | | Edge finder |
| Z | | Tool touch |

---

## TOOL ROOM LATHE SETUP

### Workholding
| Item | Details |
|------|---------|
| Chuck | [ ] 3-jaw  [ ] Collet  [ ] Other |
| Stock | Ø x L mm |
| Stick-out | mm |

### Tool List
| T# | Description | Offset | Notes |
|----|-------------|--------|-------|
| T1 | | | |
| T2 | | | |
| T3 | | | |

---

## Notes (±0.050mm typical tolerance)

### Special Instructions:


### For Production Transfer:
Machine recommended:
Key learnings from prototype:

```

---

## Setup Sheet Best Practices

### Before Setup
1. Review drawing and previous setup sheets
2. Gather all tooling, fixtures, gages
3. Verify program revision matches drawing
4. Check raw material matches specification

### During Setup
1. Follow setup sheet step-by-step
2. Document any deviations
3. Verify tool lengths and offsets
4. Run first part at reduced feed (50%)

### After Setup
1. First-off inspection - all critical dimensions
2. Update setup sheet with any changes
3. Record actual cycle time
4. Note any issues or improvements

### Continuous Improvement
- Add "Tips" from experienced operators
- Update tooling recommendations based on results
- Photo key setup steps for complex jobs
- Track setup time for benchmarking

---

## Output Format

When generating a setup sheet, I will:
1. Ask which machine/job if not specified
2. Generate appropriate template
3. Pre-fill known information
4. Highlight fields requiring operator input
5. Include relevant tips from tribal knowledge

---

## Integration with Other Skills

- **PlantCapability**: Verify machine selection before setup
- **AutomotiveManufacturing**: Link setup sheets to work instructions
- **TribalKnowledge**: Pull tips and known issues into setup sheets
