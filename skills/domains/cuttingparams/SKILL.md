---
name: CuttingParams
description: |
  Cutting parameter lookup and optimization for CNC machining.
  Covers feeds, speeds, depths of cut for common materials and operations.
  USE WHEN user asks 'feeds and speeds', 'cutting parameters', 'SFM for', 'what RPM',
  'feed rate for', 'DOC for', or needs machining parameter guidance.
---

# CuttingParams - Machining Parameter Reference

**Purpose:** Quick lookup and calculation of cutting parameters. Starting points that work, with adjustment guidance.

## When to Activate

- "What's the SFM for 316 stainless?"
- "Feeds and speeds for 7075 aluminium"
- "What RPM for a 12mm endmill in steel?"
- "Recommended DOC for titanium roughing"
- "Help me optimize my cutting parameters"

---

## Core Formulas

### Spindle Speed (RPM)

```
RPM = (SFM × 3.82) / Diameter (inches)
RPM = (Vc × 1000) / (π × Diameter mm)
RPM = (Vc × 318.3) / Diameter (mm)

Where:
- SFM = Surface Feet per Minute
- Vc = Cutting Speed in m/min
```

### Feed Rate

**Turning:**
```
Feed (mm/min) = Feed per Rev (mm/rev) × RPM
```

**Milling:**
```
Feed (mm/min) = Feed per Tooth (mm/tooth) × Number of Teeth × RPM
```

### Metal Removal Rate (MRR)

**Turning:**
```
MRR (cm³/min) = DOC × Feed × Vc × 1000
```

**Milling:**
```
MRR (cm³/min) = WOC × DOC × Feed Rate / 1000
```

---

## Material Parameters - Turning

### Aluminium Alloys

| Material | Vc Rough (m/min) | Vc Finish (m/min) | Feed Rough (mm/rev) | Feed Finish (mm/rev) | DOC Rough (mm) |
|----------|------------------|-------------------|---------------------|----------------------|----------------|
| 6061-T6 | 300-500 | 400-600 | 0.2-0.4 | 0.08-0.15 | 2-5 |
| 7075-T6 | 250-400 | 350-500 | 0.15-0.35 | 0.08-0.12 | 2-4 |
| 2024-T3 | 250-400 | 350-500 | 0.15-0.35 | 0.08-0.12 | 2-4 |
| Cast Aluminium | 200-350 | 300-450 | 0.15-0.3 | 0.08-0.12 | 1.5-3 |

**Tool:** Uncoated carbide, polished rake face, sharp edge
**Coolant:** Flood or mist, water-soluble OK

### Carbon & Alloy Steels

| Material | Hardness | Vc Rough (m/min) | Vc Finish (m/min) | Feed Rough (mm/rev) | Feed Finish (mm/rev) | DOC Rough (mm) |
|----------|----------|------------------|-------------------|---------------------|----------------------|----------------|
| 1018 | 130 HB | 180-250 | 220-300 | 0.2-0.4 | 0.08-0.15 | 2-4 |
| 1045 | 180 HB | 150-220 | 180-260 | 0.15-0.35 | 0.08-0.12 | 1.5-3.5 |
| 4140 | 200 HB | 120-180 | 150-220 | 0.15-0.3 | 0.08-0.12 | 1.5-3 |
| 4140 | 300 HB | 80-120 | 100-150 | 0.1-0.25 | 0.05-0.1 | 1-2.5 |
| 4340 | 280 HB | 90-140 | 120-170 | 0.1-0.25 | 0.05-0.1 | 1-2.5 |

**Tool:** Coated carbide (CVD for roughing, PVD for finishing)
**Coolant:** Flood, high-pressure preferred

### Stainless Steels

| Material | Vc Rough (m/min) | Vc Finish (m/min) | Feed Rough (mm/rev) | Feed Finish (mm/rev) | DOC Rough (mm) |
|----------|------------------|-------------------|---------------------|----------------------|----------------|
| 303 | 120-180 | 150-220 | 0.15-0.3 | 0.08-0.12 | 1.5-3 |
| 304 | 100-150 | 120-180 | 0.12-0.25 | 0.06-0.1 | 1-2.5 |
| 316 | 80-130 | 100-160 | 0.1-0.22 | 0.05-0.1 | 1-2 |
| 316L | 80-120 | 100-150 | 0.1-0.2 | 0.05-0.1 | 1-2 |
| 17-4PH (H1025) | 70-110 | 90-140 | 0.1-0.2 | 0.05-0.08 | 0.8-1.8 |
| 17-4PH (H900) | 50-80 | 70-100 | 0.08-0.15 | 0.04-0.08 | 0.5-1.5 |

**Tool:** PVD coated carbide (TiAlN, AlTiN), positive rake
**Coolant:** High-pressure flood essential, don't let it rub
**Warning:** Work hardens - stay aggressive, don't dwell

### Tool Steels

| Material | Condition | Vc Rough (m/min) | Vc Finish (m/min) | Feed Rough (mm/rev) | Feed Finish (mm/rev) |
|----------|-----------|------------------|-------------------|---------------------|----------------------|
| D2 | Annealed | 60-100 | 80-120 | 0.1-0.2 | 0.05-0.1 |
| D2 | Hardened (58-62 HRC) | CBN/Ceramic only | 80-150 | 0.05-0.12 | 0.03-0.08 |
| H13 | Annealed | 80-120 | 100-150 | 0.12-0.22 | 0.06-0.1 |
| H13 | Hardened (48-52 HRC) | 40-70 | 60-100 | 0.08-0.15 | 0.04-0.08 |
| A2 | Annealed | 70-110 | 90-140 | 0.1-0.2 | 0.05-0.1 |
| S7 | Annealed | 80-120 | 100-150 | 0.12-0.22 | 0.06-0.1 |

**Tool:** For hardened - CBN or ceramic inserts
**Coolant:** Often dry for hardened (CBN), flood for annealed

### Titanium Alloys

| Material | Vc Rough (m/min) | Vc Finish (m/min) | Feed Rough (mm/rev) | Feed Finish (mm/rev) | DOC Rough (mm) |
|----------|------------------|-------------------|---------------------|----------------------|----------------|
| CP Grade 2 | 60-90 | 80-120 | 0.15-0.25 | 0.08-0.12 | 1-2.5 |
| Ti-6Al-4V | 40-70 | 55-90 | 0.1-0.2 | 0.06-0.1 | 0.8-2 |
| Ti-6Al-4V (aged) | 35-55 | 45-75 | 0.08-0.15 | 0.05-0.08 | 0.5-1.5 |

**Tool:** Uncoated or PVD carbide, sharp edge, positive rake
**Coolant:** HIGH-PRESSURE flood (70+ bar), copious amounts
**Warning:** Fire risk with chips, poor thermal conductivity

### Superalloys

| Material | Vc Rough (m/min) | Vc Finish (m/min) | Feed Rough (mm/rev) | Feed Finish (mm/rev) | DOC Rough (mm) |
|----------|------------------|-------------------|---------------------|----------------------|----------------|
| Inconel 718 | 25-45 | 35-60 | 0.1-0.18 | 0.05-0.1 | 0.5-1.5 |
| Inconel 625 | 25-40 | 35-55 | 0.08-0.15 | 0.05-0.08 | 0.5-1.2 |
| Hastelloy C-276 | 20-35 | 30-50 | 0.08-0.15 | 0.04-0.08 | 0.4-1 |
| Waspaloy | 20-40 | 30-55 | 0.08-0.15 | 0.05-0.08 | 0.5-1.2 |

**Tool:** Ceramic (roughing), CBN (finishing), or whisker-reinforced
**Coolant:** High-pressure flood or dry with ceramic
**Warning:** Extreme tool wear, work hardens badly

### Plastics

| Material | Vc (m/min) | Feed (mm/rev) | DOC (mm) | Notes |
|----------|------------|---------------|----------|-------|
| Delrin/Acetal | 200-400 | 0.1-0.3 | 1-4 | Sharp tools, watch heat |
| Nylon | 150-300 | 0.1-0.25 | 1-3 | Flexible, support well |
| PEEK | 100-200 | 0.08-0.2 | 0.5-2 | Expensive, careful |
| PTFE | 150-300 | 0.1-0.25 | 1-3 | Very flexible |
| Polycarbonate | 150-300 | 0.1-0.2 | 0.5-2 | Stress cracking risk |

**Tool:** Sharp, polished, uncoated carbide or PCD
**Coolant:** Air blast or mist (avoid flooding most plastics)

### Brass & Bronze

| Material | Vc Rough (m/min) | Vc Finish (m/min) | Feed Rough (mm/rev) | Feed Finish (mm/rev) |
|----------|------------------|-------------------|---------------------|----------------------|
| Free-cutting Brass | 200-400 | 300-500 | 0.15-0.35 | 0.08-0.15 |
| Naval Brass | 150-250 | 200-350 | 0.12-0.28 | 0.06-0.12 |
| Phosphor Bronze | 100-180 | 150-250 | 0.1-0.22 | 0.05-0.1 |
| Aluminium Bronze | 80-140 | 120-200 | 0.1-0.2 | 0.05-0.1 |

**Tool:** Uncoated carbide, neutral or slightly negative rake for brass
**Coolant:** Often dry, light mist for finish

---

## Material Parameters - Milling

### Aluminium Alloys

| Material | Vc (m/min) | Fz Rough (mm/tooth) | Fz Finish (mm/tooth) | Ae Rough | Ap Rough |
|----------|------------|---------------------|----------------------|----------|----------|
| 6061-T6 | 300-600 | 0.1-0.2 | 0.05-0.1 | 50-70% | 1-2×D |
| 7075-T6 | 250-500 | 0.08-0.18 | 0.04-0.08 | 50-70% | 1-1.5×D |

**Tool:** 2-3 flute, polished, high helix (45°), uncoated or ZrN

### Steels

| Material | Hardness | Vc (m/min) | Fz Rough (mm/tooth) | Fz Finish (mm/tooth) | Ae Rough | Ap Rough |
|----------|----------|------------|---------------------|----------------------|----------|----------|
| 1018 | 130 HB | 150-250 | 0.08-0.15 | 0.04-0.08 | 40-60% | 0.5-1×D |
| 4140 | 200 HB | 100-180 | 0.06-0.12 | 0.03-0.06 | 30-50% | 0.5-1×D |
| 4140 | 300 HB | 60-100 | 0.04-0.1 | 0.02-0.05 | 25-40% | 0.3-0.7×D |

**Tool:** 4+ flute, AlTiN or TiAlN coated, variable helix

### Stainless Steels

| Material | Vc (m/min) | Fz Rough (mm/tooth) | Fz Finish (mm/tooth) | Ae Rough | Ap Rough |
|----------|------------|---------------------|----------------------|----------|----------|
| 304 | 80-140 | 0.05-0.1 | 0.03-0.06 | 30-50% | 0.3-0.8×D |
| 316 | 60-120 | 0.04-0.09 | 0.02-0.05 | 25-45% | 0.3-0.7×D |
| 17-4PH | 50-100 | 0.04-0.08 | 0.02-0.05 | 25-40% | 0.3-0.6×D |

**Tool:** 5+ flute, AlTiN coated, variable pitch, through-coolant
**Strategy:** High-efficiency milling (HEM) / trochoidal preferred

### Titanium

| Material | Vc (m/min) | Fz (mm/tooth) | Ae | Ap | Notes |
|----------|------------|---------------|-----|-----|-------|
| Ti-6Al-4V | 40-70 | 0.05-0.1 | 10-20% | 1-2×D | HEM essential |

**Tool:** 5+ flute, variable helix, through-coolant, sharp
**Strategy:** Light radial, deep axial, high-pressure coolant

### Superalloys

| Material | Vc (m/min) | Fz (mm/tooth) | Ae | Ap | Notes |
|----------|------------|---------------|-----|-----|-------|
| Inconel 718 | 20-45 | 0.03-0.08 | 10-15% | 0.5-1.5×D | Ceramic or CBN |

**Tool:** Ceramic endmills for roughing, CBN for finishing
**Strategy:** Light engagement, rigid setup essential

---

## Drilling Parameters

| Material | Vc (m/min) | Feed (mm/rev) | Peck Depth | Notes |
|----------|------------|---------------|------------|-------|
| Aluminium | 80-150 | 0.15-0.3 | 3×D | Through-coolant preferred |
| Mild Steel | 25-40 | 0.1-0.25 | 1-2×D | Flood coolant |
| Stainless | 15-30 | 0.08-0.18 | 0.5-1×D | High-pressure, frequent peck |
| Titanium | 12-25 | 0.06-0.12 | 0.3-0.5×D | Through-coolant essential |
| Inconel | 8-15 | 0.04-0.1 | 0.2-0.3×D | Carbide or CBN |

### Peck Drilling Guide

| Hole Depth | Peck Frequency | Retract |
|------------|----------------|---------|
| < 3×D | No peck needed | - |
| 3-5×D | Every 1×D | Full retract |
| 5-10×D | Every 0.5×D | Full retract |
| > 10×D | Gundrilling | - |

---

## Threading Parameters

### Single-Point Threading (Turning)

| Material | Vc (m/min) | Infeed Method | Passes |
|----------|------------|---------------|--------|
| Aluminium | 100-200 | Flank/Modified | 4-6 |
| Steel | 60-100 | Modified flank | 6-10 |
| Stainless | 40-80 | Modified flank | 8-12 |
| Titanium | 25-50 | Radial | 10-15 |

**DOC per pass:** Start at 0.2-0.3mm, reduce progressively

### Thread Milling

| Material | Vc (m/min) | Fz (mm/tooth) |
|----------|------------|---------------|
| Aluminium | 150-300 | 0.05-0.1 |
| Steel | 80-150 | 0.03-0.08 |
| Stainless | 50-100 | 0.02-0.06 |
| Titanium | 30-60 | 0.02-0.05 |

### Tapping

| Material | Vc (m/min) | Notes |
|----------|------------|-------|
| Aluminium | 20-40 | Spiral flute, flood |
| Steel | 10-25 | Spiral point, flood |
| Stainless | 5-15 | Form tap or spiral flute |
| Titanium | 3-8 | Spiral flute, high-pressure |

---

## Insert Selection Guide

### Turning Insert Grades

| Material | Roughing | Finishing |
|----------|----------|-----------|
| Aluminium | Uncoated, polished | PCD or uncoated polished |
| Steel (<300 HB) | CVD coated | PVD coated |
| Steel (>300 HB) | Ceramic/CBN | CBN |
| Stainless | PVD (TiAlN) | PVD (AlTiN) |
| Titanium | Uncoated or PVD | Uncoated sharp |
| Inconel | Ceramic | CBN or ceramic |

### Insert Geometry

| Application | Nose Radius | Rake | Lead Angle |
|-------------|-------------|------|------------|
| Heavy roughing | 1.2-1.6mm | Negative | 45° |
| Light roughing | 0.8mm | Neutral | 90° |
| Finishing | 0.4mm | Positive | 90° |
| Precision finish | 0.2mm | Positive | 90° |
| Interrupted cut | 0.8-1.2mm | Negative | 45° |

---

## Troubleshooting Parameters

### Problem: Poor Surface Finish

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Rough, torn | Speed too low | Increase Vc 20% |
| Feed marks visible | Feed too high | Reduce feed 20% |
| Chatter marks | Vibration | Reduce DOC, increase feed |
| Built-up edge | Wrong speed/material | Increase speed, change insert |
| Smearing | Rubbing | Sharper insert, increase feed |

### Problem: Rapid Tool Wear

| Wear Type | Cause | Fix |
|-----------|-------|-----|
| Flank wear | Speed too high | Reduce Vc 15-20% |
| Crater wear | Heat/chemical | Better coating, reduce speed |
| Notch wear | Work hardening | Vary DOC, change lead angle |
| Chipping | Interrupted/shock | Tougher grade, reduce feed |
| Built-up edge | Speed too low | Increase Vc, better coating |

### Problem: Chatter/Vibration

| Cause | Solution |
|-------|----------|
| Tool overhang | Reduce stickout, larger shank |
| Light cut | Increase feed or DOC |
| Wrong speed | Adjust RPM (try ±20%) |
| Part not rigid | Better workholding, steadies |
| Insert nose radius | Smaller radius |

### Problem: Chip Control

| Issue | Material | Solution |
|-------|----------|----------|
| Bird's nest | Stainless, aluminium | Chipbreaker, increase feed |
| Stringy chips | Ductile materials | Higher feed, chipbreaker |
| Long chips | Low carbon steel | Increase feed, DOC |
| Chip packing | Deep holes | Peck drilling, through-coolant |
| Welding to tool | Aluminium, stainless | Increase speed, better coating |

---

## Swiss Machine Parameters (CITIZEN)

### Small Diameter Work (Ø3-10mm)

| Material | Vc (m/min) | Feed (mm/rev) | DOC (mm) |
|----------|------------|---------------|----------|
| 303SS | 80-120 | 0.02-0.06 | 0.2-0.8 |
| 316SS | 60-100 | 0.02-0.05 | 0.15-0.6 |
| Brass | 150-250 | 0.03-0.08 | 0.3-1.0 |
| Aluminium | 200-350 | 0.03-0.08 | 0.3-1.2 |
| Ti-6Al-4V | 30-50 | 0.01-0.04 | 0.1-0.4 |

### LFV Settings (CITIZEN LFV)

| Material | Use LFV? | Frequency | Amplitude |
|----------|----------|-----------|-----------|
| 316SS | Yes | 10-20 Hz | 0.05-0.15mm |
| 304SS | Yes | 10-20 Hz | 0.05-0.15mm |
| Titanium | Yes | 8-15 Hz | 0.03-0.1mm |
| Aluminium | Rarely | - | - |
| Brass | No | - | - |
| Plastics | Sometimes | 5-10 Hz | 0.02-0.08mm |

**LFV Benefits:** Breaks chips into small segments, eliminates bird-nesting, improves surface finish on gummy materials

---

## Quick Reference Cards

### Turning - Starting Points

```
ALUMINIUM:  Vc=400  Feed=0.2   DOC=3mm
STEEL:      Vc=180  Feed=0.2   DOC=2mm
STAINLESS:  Vc=100  Feed=0.15  DOC=1.5mm
TITANIUM:   Vc=50   Feed=0.12  DOC=1mm
INCONEL:    Vc=30   Feed=0.1   DOC=0.8mm
```

### Milling - Starting Points

```
ALUMINIUM:  Vc=400  Fz=0.15  Ae=50%  Ap=1×D
STEEL:      Vc=150  Fz=0.08  Ae=40%  Ap=0.7×D
STAINLESS:  Vc=90   Fz=0.06  Ae=30%  Ap=0.5×D
TITANIUM:   Vc=50   Fz=0.06  Ae=15%  Ap=1.5×D (HEM)
INCONEL:    Vc=30   Fz=0.05  Ae=10%  Ap=1×D (HEM)
```

### RPM Quick Calc (metric)

```
RPM = (Vc × 318) / Diameter(mm)

Examples @ Vc=100 m/min:
Ø6mm  = 5,300 RPM
Ø10mm = 3,180 RPM
Ø12mm = 2,650 RPM
Ø16mm = 1,990 RPM
Ø20mm = 1,590 RPM
Ø25mm = 1,270 RPM
Ø50mm = 636 RPM
```

---

## Integration

- **CNCSetup:** Auto-populate cutting parameters in setup sheets
- **TribalKnowledge:** Store proven parameters that beat book values
- **QuoteEstimator:** More accurate cycle times with real parameters
- **PlantCapability:** Material-specific machine recommendations
