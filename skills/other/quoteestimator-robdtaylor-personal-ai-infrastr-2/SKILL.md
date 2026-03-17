---
name: Quoteestimator
description: Rough cycle time and cost estimation for CNC machined parts. Uses MNMUK plant capabilities and standard estimating factors. USE WHEN user says 'quote', 'estimate', 'cycle time', 'how long', 'cost estimate', 'pricing', 'how much to make', or describes a part needing a rough quote.
---

# QuoteEstimator - MNMUK Quoting Support

**Purpose:** Rapid rough-order-of-magnitude estimates for quoting. Not a replacement for proper process planning, but gets you in the ballpark fast.

## When to Activate

- "How long to make this part?"
- "Rough quote for [part description]"
- "Estimate cycle time for..."
- "What would it cost to make 500 of these?"
- "Quick estimate for quoting"

## Disclaimer

These are **rough estimates** for quoting purposes. Actual times depend on:
- Specific geometry complexity
- Tolerance requirements
- Surface finish specs
- Fixturing approach
- Tooling availability
- Operator experience

**Always add contingency** and verify with experienced estimator for critical quotes.

---

## Machine Hourly Rates

### MNMUK Rate Card (Adjust to your actual rates)

| Machine Category | Machine | Rate (£/hr) | Notes |
|------------------|---------|-------------|-------|
| **5-Axis Mill** | NMV3000, DMU50, NHX500 | £85-95 | High capability |
| **4-Axis Mill** | Vertical VMC | £65-75 | Standard work |
| **CNC Turning** | NLX2500, ALX2000 | £60-70 | Live tooling adds £5 |
| **Precision Turning** | HARDINGE | £75-85 | ±0.003mm work |
| **Swiss** | CITIZEN | £80-90 | High volume, precision |
| **Wire EDM** | MITSUBISHI | £55-65 | Slow but precise |
| **Spark EDM** | MITSUBISHI | £50-60 | Electrode cost separate |
| **Fast Response** | Haas | £45-55 | Prototypes |

### Rate Factors

```
Base Rate × Material Factor × Tolerance Factor × Complexity Factor = Effective Rate
```

---

## Material Factors

| Material | Factor | Reasoning |
|----------|--------|-----------|
| Aluminium (6061) | 0.8 | Fast cutting, easy |
| Aluminium (7075) | 0.9 | Slightly harder |
| Brass/Bronze | 0.85 | Free machining |
| Mild Steel (1018) | 1.0 | Baseline |
| Carbon Steel (4140) | 1.1 | Harder, more wear |
| Stainless 303 | 1.2 | Free machining SS |
| Stainless 304/316 | 1.4 | Work hardening, gummy |
| 17-4PH | 1.5 | Tough stainless |
| Tool Steel (pre-hard) | 1.3 | Abrasive |
| Tool Steel (hardened) | 2.0+ | EDM only typically |
| Titanium (CP) | 1.6 | Slow speeds required |
| Titanium (6Al-4V) | 1.8 | Very slow, careful |
| Inconel 718 | 2.2 | Extreme tool wear |
| Hastelloy | 2.5 | Worst case scenario |
| Delrin/Acetal | 0.7 | Easy, watch heat |
| PEEK | 1.3 | Expensive material |
| Nylon | 0.75 | Easy, flexible |

---

## Tolerance Factors

| Tolerance Band | Factor | Notes |
|----------------|--------|-------|
| ±0.25mm (±0.010") | 0.9 | Loose, fast |
| ±0.125mm (±0.005") | 1.0 | Standard |
| ±0.05mm (±0.002") | 1.2 | Careful work |
| ±0.025mm (±0.001") | 1.4 | Precision |
| ±0.012mm (±0.0005") | 1.7 | High precision |
| ±0.005mm (±0.0002") | 2.0 | Grinding territory |
| ±0.003mm | 2.5 | Swiss/HARDINGE only |

---

## Complexity Factors

| Complexity | Factor | Examples |
|------------|--------|----------|
| Simple | 0.8 | Round part, few features |
| Standard | 1.0 | Typical machined part |
| Moderate | 1.3 | Multiple setups, tight tolerances mixed with loose |
| Complex | 1.6 | 5-axis, multiple operations, thin walls |
| Very Complex | 2.0+ | Extreme geometry, exotic material + tight tolerance |

---

## Cycle Time Estimation

### Turning Operations

#### OD Turning
```
Time (min) = (Length × Passes × π × Diameter) / (Feed × Speed × 1000)

Simplified:
Rough: Volume removed (cm³) × 0.5 min/cm³
Finish: Surface area (cm²) × 0.02 min/cm²
```

**Quick Estimates - OD Turning:**

| Part Size | Rough | Finish | Total |
|-----------|-------|--------|-------|
| Ø25 × 50mm | 0.5 min | 0.3 min | 0.8 min |
| Ø50 × 100mm | 2 min | 1 min | 3 min |
| Ø100 × 150mm | 6 min | 2.5 min | 8.5 min |
| Ø150 × 200mm | 12 min | 4 min | 16 min |

#### ID Boring
```
Multiply OD time × 1.5 (slower, less rigid)
Deep bores (L/D > 4): × 2.0
```

#### Threading
```
Single-point: 0.3 min per 25mm thread length (standard pitch)
Thread milling: 0.5 min per thread
Tapping: 0.1 min per hole (standard)
```

#### Grooving/Parting
```
Grooving: 0.2 min per groove
Part-off: Diameter (mm) × 0.01 min
```

### Milling Operations

#### Face Milling
```
Time = (Area / (Width of Cut × Feed Rate)) + Approach

Quick: Area (cm²) × 0.02 min/cm² for roughing
       Area (cm²) × 0.01 min/cm² for finishing
```

#### Pocket Milling
```
Volume (cm³) × 0.8 min/cm³ (aluminium)
Volume (cm³) × 1.5 min/cm³ (steel)
Volume (cm³) × 3.0 min/cm³ (stainless/titanium)

Add 50% for finishing passes
```

#### Drilling
```
Standard drill: Depth (mm) × 0.02 min/mm
Peck drilling: Depth (mm) × 0.04 min/mm
Deep hole (>5xD): Depth (mm) × 0.08 min/mm
```

#### 5-Axis Contouring
```
Surface area (cm²) × 0.15 min/cm² (aluminium)
Surface area (cm²) × 0.3 min/cm² (steel)
Surface area (cm²) × 0.5 min/cm² (titanium)

Complex surfaces: Add 50-100%
```

### Swiss Operations

```
Small precision parts (Ø3-10mm):
- Simple: 30-60 sec/part
- Standard: 60-120 sec/part
- Complex: 120-300 sec/part

Medium parts (Ø10-25mm):
- Simple: 60-120 sec/part
- Standard: 120-240 sec/part
- Complex: 240-480 sec/part
```

### EDM Operations

#### Wire EDM
```
Cut length (mm) × thickness (mm) × 0.003 min/mm² (roughing)
Add 50% per skim pass (typically 2-4 skim passes)

Example: 100mm perimeter × 25mm thick
- Rough: 100 × 25 × 0.003 = 7.5 min
- 3 skims: 7.5 × 1.5 × 1.5 × 1.5 = 25 min total
```

#### Spark EDM
```
Volume to remove (cm³) × 30-60 min/cm³
Roughing faster, finishing much slower
Electrode making: Add 1-4 hours depending on complexity
```

---

## Setup Time Estimates

| Operation Type | First Setup | Repeat Setup |
|----------------|-------------|--------------|
| Simple turning | 30 min | 15 min |
| Complex turning (live tooling) | 60 min | 30 min |
| Swiss | 90 min | 45 min |
| 3-axis milling | 30 min | 15 min |
| 4-axis milling | 45 min | 20 min |
| 5-axis milling | 60-90 min | 30 min |
| Wire EDM | 30 min | 15 min |
| Spark EDM | 60 min + electrode | 30 min |
| Multiple operations | Sum of each | Sum × 0.7 |

---

## Quick Quote Formula

```
Total Cost = (Setup Cost) + (Run Cost × Quantity) + (Material Cost) + (Secondary Ops)

Where:
- Setup Cost = Setup Time × Hourly Rate
- Run Cost = Cycle Time × Hourly Rate × Material Factor × Tolerance Factor
- Material Cost = Weight × £/kg × Waste Factor (typically 1.3-1.5)
- Secondary Ops = Finishing, heat treat, plating, inspection (get quotes)
```

### Quantity Breaks

| Quantity | Multiplier | Notes |
|----------|------------|-------|
| 1-5 | 1.5 | Prototype pricing |
| 6-25 | 1.2 | Small batch |
| 26-100 | 1.0 | Standard |
| 101-500 | 0.9 | Efficiency gains |
| 500+ | 0.8 | Volume pricing |

---

## Estimation Workflow

### Step 1: Feasibility (Use PlantCapability)
- Can we make it?
- Which machine?
- Any showstoppers?

### Step 2: Operation Breakdown
```markdown
| Op# | Description | Machine | Setup | Cycle |
|-----|-------------|---------|-------|-------|
| 10 | | | min | min |
| 20 | | | min | min |
| 30 | | | min | min |
```

### Step 3: Apply Factors
```markdown
Base cycle time: X min
× Material factor (Y): X × Y = Z min
× Tolerance factor (T): Z × T = A min
× Complexity factor (C): A × C = B min
Adjusted cycle time: B min
```

### Step 4: Calculate Costs
```markdown
Setup: [time] × £[rate] = £____
Run: [cycle] × [qty] × £[rate/60] = £____
Material: [weight] × £[per kg] × 1.3 = £____
Secondary: £____
Subtotal: £____
Margin (25-40%): £____
**Quote: £____**
```

---

## Quote Output Template

```markdown
# ROUGH QUOTE ESTIMATE

**Date:** YYYY-MM-DD
**Customer:**
**Part:**
**Quantity:**

---

## Part Summary
- Material:
- Envelope: L × W × H mm
- Weight (est): kg
- Key tolerances:
- Surface finish:

## Feasibility
- [x] Within capability
- Machine(s):
- Risks:

---

## Operations Breakdown

| Op | Description | Machine | Setup (min) | Cycle (min) |
|----|-------------|---------|-------------|-------------|
| 10 | | | | |
| 20 | | | | |
| 30 | | | | |
| **Total** | | | **X** | **Y** |

---

## Factors Applied

| Factor | Value | Reasoning |
|--------|-------|-----------|
| Material | × | |
| Tolerance | × | |
| Complexity | × | |
| **Combined** | **×** | |

**Adjusted cycle:** Y × [combined] = Z min/part

---

## Cost Calculation

| Item | Calculation | Cost |
|------|-------------|------|
| Setup | X min × £[rate]/60 | £ |
| Run (× qty) | Z min × [qty] × £[rate]/60 | £ |
| Material | [wt] × £[/kg] × [qty] × 1.3 | £ |
| Secondary ops | [detail] | £ |
| **Subtotal** | | **£** |
| Margin ([%]) | | £ |
| **Quote Total** | | **£** |

**Per Part:** £ each at qty [X]

---

## Assumptions & Exclusions

### Assumptions
-

### Exclusions
-

### Validity
- Quote valid for: 30 days
- Lead time estimate: X weeks

---

## Notes

### Risks
-

### Alternatives
-

---

*Rough estimate only. Final quote subject to drawing review and process planning.*
```

---

## Quick Reference Tables

### Cycle Time Rules of Thumb

| Part Type | Quick Estimate |
|-----------|----------------|
| Simple turned (Ø25-50) | 2-5 min |
| Complex turned (Ø50-100) | 8-20 min |
| Swiss part (small) | 1-3 min |
| Simple prismatic (milled) | 5-15 min |
| 5-axis component | 20-60 min |
| Wire EDM profile | 30-120 min |

### Setup Time Rules of Thumb

| Scenario | Estimate |
|----------|----------|
| Repeat job, tooling available | 15-30 min |
| New job, simple | 30-45 min |
| New job, complex | 60-120 min |
| New job, 5-axis or Swiss | 90-180 min |

### Cost Sanity Checks

| Part Type | £/part Range (qty 100) |
|-----------|------------------------|
| Simple turned bushing | £2-8 |
| Complex turned shaft | £15-50 |
| Swiss precision pin | £3-15 |
| Milled bracket (aluminium) | £10-40 |
| 5-axis aerospace part | £50-500 |
| EDM detail | £30-200 |

---

## Example Estimates

### Example 1: Turned Shaft

**Part:** Ø50 × 150mm shaft, 4140 steel, ±0.025mm on bearing diameters
**Qty:** 100

```
Operations:
- OP10: Face, turn OD, drill center (NLX2500)
- OP20: Flip, face to length, finish bearing seats

Cycle estimate:
- Rough turning: 4 min
- Finish turning: 2 min
- Total: 6 min base

Factors:
- Material (4140): × 1.1
- Tolerance (±0.025): × 1.4
- Complexity (standard): × 1.0
- Combined: × 1.54

Adjusted cycle: 6 × 1.54 = 9.2 min

Costs (at £65/hr):
- Setup: 45 min × £65/60 = £49
- Run: 9.2 min × 100 × £65/60 = £997
- Material: 2.3kg × £3/kg × 100 × 1.3 = £897
- Subtotal: £1,943
- Margin (30%): £583
- Quote: £2,526 (£25.26/part)
```

### Example 2: Swiss Medical Pin

**Part:** Ø4 × 20mm pin, 316SS, ±0.01mm, qty 1000
**Machine:** CITIZEN LFV

```
Cycle estimate: 90 sec base (complex small part)

Factors:
- Material (316SS): × 1.4
- Tolerance (±0.01): × 1.5
- Complexity (moderate): × 1.3
- Combined: × 2.73

Adjusted cycle: 90 × 2.73 = 246 sec = 4.1 min

Costs (at £85/hr):
- Setup: 90 min × £85/60 = £128
- Run: 4.1 min × 1000 × £85/60 = £5,808
- Material: 0.02kg × £8/kg × 1000 × 1.3 = £208
- Subtotal: £6,144
- Margin (30%): £1,843
- Quote: £7,987 (£7.99/part)
```

---

## Integration

- **PlantCapability:** Check feasibility before estimating
- **CNCSetup:** Setup times based on actual setup sheet complexity
- **TribalKnowledge:** Adjust factors based on captured experience
- **AutomotiveManufacturing:** Link to PPAP/APQP costing requirements
