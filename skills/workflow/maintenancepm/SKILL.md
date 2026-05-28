---
name: MaintenancePM
description: |
  Preventive maintenance schedules for MNMUK machine shop equipment.
  Covers DMG MORI, CITIZEN, MITSUBISHI EDM, Haas, and support equipment.
  USE WHEN user asks 'PM schedule', 'maintenance', 'service due', 'machine maintenance',
  'what maintenance', or 'TPM checklist'.
---

# MaintenancePM - Preventive Maintenance System

**Purpose:** Protect capital equipment investment through systematic preventive maintenance.

## When to Activate

- "What's the PM schedule for NLX2500?"
- "Create maintenance checklist"
- "What's due for service?"
- "TPM checklist for Swiss machines"
- "Maintenance history for [machine]"
- "PM planning"

---

## Maintenance Philosophy

### Total Productive Maintenance (TPM)

| Level | Responsibility | Frequency | Examples |
|-------|---------------|-----------|----------|
| **Operator** | Daily/Shift | Every shift | Cleaning, lubrication, visual checks |
| **Technician** | Weekly/Monthly | Scheduled | Filter changes, calibration, adjustments |
| **Specialist** | Quarterly/Annual | Planned | Major service, rebuilds, alignments |
| **OEM** | As required | Scheduled | Warranty service, major repairs |

---

## DMG MORI Machines

### Daily Checks (Operator - Every Shift)

```markdown
# Daily PM Checklist - DMG MORI

Machine: _____________ Date: _________ Operator: _________

## Start of Shift

| Check | OK | Issue | Notes |
|-------|-----|-------|-------|
| Coolant level | ☐ | ☐ | |
| Coolant concentration (refractometer) | ☐ | ☐ | Target: ___% |
| Hydraulic oil level | ☐ | ☐ | |
| Way lube level | ☐ | ☐ | |
| Air pressure (6 bar min) | ☐ | ☐ | |
| Chip conveyor clear | ☐ | ☐ | |
| Guards/doors function | ☐ | ☐ | |
| No unusual noises | ☐ | ☐ | |
| Spindle warm-up complete | ☐ | ☐ | |

## End of Shift

| Task | Done | Notes |
|------|------|-------|
| Clean machine exterior | ☐ | |
| Remove chips from work area | ☐ | |
| Wipe down way covers | ☐ | |
| Return tools to crib | ☐ | |
| Report any issues | ☐ | |

Signature: _____________
```

### Weekly PM - DMG MORI Mills (NMV3000, DMU50, NHX500)

```markdown
# Weekly PM - DMG MORI 5-Axis Mill

Machine: _____________ Week: _________ Tech: _________

| Task | Done | Reading/Notes |
|------|------|---------------|
| Check spindle runout | ☐ | TIR: ___μm (max 5μm) |
| Inspect tool changer | ☐ | |
| Clean coolant tank strainer | ☐ | |
| Check way lube distribution | ☐ | |
| Inspect pallet changer (if equipped) | ☐ | |
| Verify probe calibration | ☐ | |
| Check air dryer/filter | ☐ | |
| Inspect chip conveyor belt | ☐ | |
| Check hydraulic filter indicator | ☐ | |
| Clean control cabinet filter | ☐ | |

## Pallet System (NMV3000/DMU50)
| Task | Done | Notes |
|------|------|-------|
| Check pallet locating surfaces | ☐ | |
| Verify pallet clamping | ☐ | |
| Lubricate pallet transfer | ☐ | |

Issues Found: ___________________________________
Action Taken: ___________________________________
```

### Weekly PM - DMG MORI Lathes (NLX2500, ALX2000)

```markdown
# Weekly PM - DMG MORI Turning Centre

Machine: _____________ Week: _________ Tech: _________

| Task | Done | Reading/Notes |
|------|------|---------------|
| Check chuck clamping pressure | ☐ | Main: ___bar Sub: ___bar |
| Inspect turret indexing | ☐ | |
| Check tailstock alignment (if used) | ☐ | |
| Verify bar feeder operation | ☐ | |
| Clean chip conveyor | ☐ | |
| Check coolant nozzle positioning | ☐ | |
| Inspect sub-spindle (NLX2500) | ☐ | |
| Verify tool sensor operation | ☐ | |
| Check hydraulic pressure | ☐ | ___bar |
| Clean/replace coolant filter | ☐ | |

Live Tooling Check:
| Task | Done | Notes |
|------|------|-------|
| Check live tool runout | ☐ | TIR: ___μm |
| Lubricate live tool holders | ☐ | |
| Verify C-axis indexing | ☐ | |
```

### Monthly PM - All DMG MORI

```markdown
# Monthly PM - DMG MORI

Machine: _____________ Month: _________ Tech: _________

## Lubrication
| Task | Done | Notes |
|------|------|-------|
| Check/top up way lube reservoir | ☐ | Level: ___% |
| Verify lube pump operation | ☐ | |
| Grease linear guide wipers | ☐ | |
| Lubricate ball screws (if manual) | ☐ | |

## Hydraulics
| Task | Done | Notes |
|------|------|-------|
| Check hydraulic oil level | ☐ | |
| Inspect for leaks | ☐ | |
| Check pressure gauge accuracy | ☐ | |

## Coolant System
| Task | Done | Notes |
|------|------|-------|
| Clean coolant tank thoroughly | ☐ | |
| Replace coolant filters | ☐ | |
| Check pump operation | ☐ | |
| Verify through-spindle pressure | ☐ | ___bar |

## Electrical
| Task | Done | Notes |
|------|------|-------|
| Clean control cabinet (air blow) | ☐ | |
| Check fan operation | ☐ | |
| Inspect cables for damage | ☐ | |

## Accuracy Check
| Measurement | Spec | Actual | Pass |
|-------------|------|--------|------|
| Spindle runout | <5μm | | ☐ |
| Axis backlash X | <5μm | | ☐ |
| Axis backlash Y | <5μm | | ☐ |
| Axis backlash Z | <5μm | | ☐ |
```

### Annual PM - DMG MORI

| Task | Interval | Last Done | Next Due | Notes |
|------|----------|-----------|----------|-------|
| Ball screw inspection | Annual | | | OEM or trained tech |
| Spindle bearing check | Annual | | | Vibration analysis |
| Geometric alignment | Annual | | | Laser or ballbar |
| Hydraulic oil change | Annual/2000hr | | | |
| Way lube oil change | Annual | | | |
| Coolant full change | 6 months | | | |
| Encoder battery | 2 years | | | CRITICAL |
| Control backup | Annual | | | |

---

## HARDINGE Precision Lathe

### Daily - Operator

```markdown
# Daily PM - HARDINGE

| Check | OK | Issue |
|-------|-----|-------|
| Spindle warm-up (20 min) | ☐ | ☐ |
| Collet/chuck cleanliness | ☐ | ☐ |
| Coolant level and temp | ☐ | ☐ |
| Air pressure | ☐ | ☐ |
| No unusual vibration | ☐ | ☐ |
```

### Weekly - Precision Checks

```markdown
# Weekly PM - HARDINGE

| Task | Done | Reading |
|------|------|---------|
| Spindle runout check | ☐ | TIR: ___μm (max 2μm) |
| Temperature log start/end | ☐ | Start: ___°C End: ___°C |
| Collet concentricity | ☐ | TIR: ___μm |
| Sub-spindle alignment | ☐ | |
```

---

## CITIZEN Swiss Machines

### Daily - Operator

```markdown
# Daily PM - CITIZEN Swiss

Machine: [ ] Laser Head  [ ] LFV
Date: _________ Operator: _________

| Check | OK | Issue | Notes |
|-------|-----|-------|-------|
| Oil level | ☐ | ☐ | |
| Oil temperature | ☐ | ☐ | Target: 25-30°C |
| Guide bushing condition | ☐ | ☐ | |
| Bar stock quality | ☐ | ☐ | |
| Chip evacuation | ☐ | ☐ | |
| Air pressure (5 bar) | ☐ | ☐ | |
| Mist collector filter | ☐ | ☐ | |
| Part catcher clear | ☐ | ☐ | |
```

### Weekly - Swiss Specific

```markdown
# Weekly PM - CITIZEN Swiss

| Task | Done | Notes |
|------|------|-------|
| Clean guide bushing area | ☐ | |
| Check guide bushing wear | ☐ | |
| Inspect collet condition | ☐ | |
| Verify gang tool alignment | ☐ | |
| Check back-working tools | ☐ | |
| Clean oil filter | ☐ | |
| Verify LFV operation (if equipped) | ☐ | |
| Check laser alignment (if equipped) | ☐ | |
| Inspect bar feeder | ☐ | |
| Check sub-spindle pickup | ☐ | |

Oil Analysis (Monthly):
| Parameter | Spec | Actual | Pass |
|-----------|------|--------|------|
| Contamination | <NAS 8 | | ☐ |
| Water content | <0.1% | | ☐ |
| Viscosity | ±10% | | ☐ |
```

### Monthly - CITIZEN

| Task | Done | Notes |
|------|------|-------|
| Full oil tank clean | ☐ | |
| Replace oil filter element | ☐ | |
| Guide bushing replacement (if worn) | ☐ | |
| Check Z-axis gibs | ☐ | |
| Verify spindle accuracy | ☐ | |
| Clean electrical cabinet | ☐ | |

---

## MITSUBISHI EDM

### Daily - Wire EDM

```markdown
# Daily PM - MITSUBISHI Wire EDM

Date: _________ Operator: _________

| Check | OK | Issue |
|-------|-----|-------|
| Dielectric level | ☐ | ☐ |
| Dielectric conductivity | ☐ | ☐ | Reading: ___μS |
| Wire path clear | ☐ | ☐ |
| Filter pressure | ☐ | ☐ |
| Wire guides condition | ☐ | ☐ |
| Flushing nozzles clear | ☐ | ☐ |
| Wire tension | ☐ | ☐ |
| Auto-threader operation | ☐ | ☐ |
```

### Daily - Spark EDM

```markdown
# Daily PM - MITSUBISHI Spark EDM

Date: _________ Operator: _________

| Check | OK | Issue |
|-------|-----|-------|
| Dielectric level | ☐ | ☐ |
| Dielectric clarity | ☐ | ☐ |
| Filter condition | ☐ | ☐ |
| Electrode holder clean | ☐ | ☐ |
| Flush pump operation | ☐ | ☐ |
| Fire suppression OK | ☐ | ☐ |
```

### Weekly - Both EDM Types

| Task | Done | Notes |
|------|------|-------|
| Check dielectric conductivity | ☐ | Target: 20-40μS |
| Clean/replace filters | ☐ | |
| Inspect wire guides (wire) | ☐ | |
| Check AWT roller condition (wire) | ☐ | |
| Verify axis accuracy | ☐ | |
| Clean work tank | ☐ | |
| Check resin condition | ☐ | |

### Monthly - EDM

| Task | Done | Notes |
|------|------|-------|
| Full dielectric change | ☐ | If contaminated |
| Replace deionizing resin | ☐ | When conductivity rises |
| Wire guide replacement | ☐ | Every 200-400 hrs |
| Power feed contact check | ☐ | |
| Geometric accuracy check | ☐ | |

---

## Haas Fast Response Cell

### Daily - Operator

```markdown
# Daily PM - Haas

Machine: [ ] Mini Mill  [ ] Tool Room Lathe

| Check | OK | Issue |
|-------|-----|-------|
| Coolant level | ☐ | ☐ |
| Way lube level | ☐ | ☐ |
| Chip tray clear | ☐ | ☐ |
| Air pressure | ☐ | ☐ |
| Tool changer cycle | ☐ | ☐ |
| Spindle warm-up | ☐ | ☐ |
```

### Weekly

| Task | Done | Notes |
|------|------|-------|
| Check spindle runout | ☐ | |
| Verify tool changer alignment | ☐ | |
| Clean coolant tank | ☐ | |
| Check way covers | ☐ | |
| Grease as required | ☐ | |

---

## Maintenance Schedule Summary

### Daily (Every Shift)

| Machine | Key Checks |
|---------|------------|
| All | Fluid levels, air pressure, visual inspection |
| Mills | Spindle warm-up, tool changer |
| Lathes | Chuck pressure, bar feeder |
| Swiss | Oil temp, guide bushing |
| EDM | Dielectric level/conductivity |

### Weekly

| Machine | Key Tasks |
|---------|-----------|
| All | Accuracy checks, filter inspection |
| Mills | Pallet system, probe calibration |
| Lathes | Turret, live tooling |
| Swiss | Guide bushing wear, oil filter |
| EDM | Wire guides, filter change |

### Monthly

| Machine | Key Tasks |
|---------|-----------|
| All | Full cleaning, lubrication top-up |
| Mills | Coolant change, accuracy verification |
| Lathes | Hydraulic check, tailstock alignment |
| Swiss | Oil tank clean, full inspection |
| EDM | Resin check, geometric accuracy |

### Quarterly

| Machine | Key Tasks |
|---------|-----------|
| All | Major filter replacements |
| Mills | Ballbar test |
| Lathes | Spindle bearing analysis |
| Swiss | OEM service items |
| EDM | Full calibration |

### Annual

| Machine | Key Tasks |
|---------|-----------|
| All | Full OEM service, geometry check, major PM |
| All | Backup all programs and parameters |
| All | Hydraulic/lube oil change |

---

## Maintenance Log Template

```markdown
# Maintenance Log

Machine: _____________
Machine ID: ___________

| Date | Type | Hours | Description | Parts Used | Tech | Time |
|------|------|-------|-------------|------------|------|------|
| | PM | | | | | |
| | Repair | | | | | |
| | PM | | | | | |
```

---

## Spare Parts Stock

### Critical Spares (Keep on-site)

| Machine | Item | Qty | Lead Time | Supplier |
|---------|------|-----|-----------|----------|
| All | Coolant filters | 10 | 2 days | |
| All | Way lube filters | 5 | 2 days | |
| Swiss | Guide bushings (common sizes) | 5 ea | 5 days | |
| Swiss | Collets | 3 ea | 3 days | |
| EDM | Wire guides | 2 sets | 5 days | |
| EDM | Resin | 1 unit | 3 days | |
| EDM | Filters | 10 | 2 days | |
| All | Encoder batteries | 2 | 3 days | CRITICAL |

### Order Lead Times

| Supplier | Type | Typical Lead |
|----------|------|--------------|
| DMG MORI | Spare parts | 3-10 days |
| CITIZEN | Spare parts | 5-14 days |
| MITSUBISHI | EDM parts | 3-7 days |
| Haas | Spare parts | 3-7 days |

---

## Downtime Tracking

```markdown
# Downtime Log - [Month]

| Date | Machine | Start | End | Hours | Cause | Action | Category |
|------|---------|-------|-----|-------|-------|--------|----------|
| | | | | | | | PM/Breakdown/Setup |

## Monthly Summary

| Category | Hours | % of Total |
|----------|-------|------------|
| Planned PM | | |
| Breakdown | | |
| Waiting Parts | | |
| Other | | |
| **Total** | | |

## Machine Availability

| Machine | Available Hrs | Downtime | Availability % |
|---------|---------------|----------|----------------|
| | | | |

Target: >95% Availability
```

---

## Integration

- **PlantCapability:** Factor maintenance windows into capacity
- **SkillsMatrix:** Who is trained for which PM tasks
- **TribalKnowledge:** Capture maintenance tips and tricks
- **OEETracker:** Availability component of OEE
