---
name: Spc
description: Implement SPC charting, process capability analysis, and control chart interpretation. Covers control chart selection, capability indices, and out-of-control rules. USE WHEN user says 'SPC', 'Cpk', 'Ppk', 'control chart', 'process capability', 'X-bar R', 'statistical control', or 'out of control'. Integrates with ControlPlan, MSA, and AutomotiveManufacturing skills.
---

# Statistical Process Control (SPC)

## When to Activate This Skill
- "Set up SPC for [characteristic]"
- "Calculate Cpk for [process]"
- "What control chart should I use?"
- "Is this process in control?"
- "Interpret out-of-control pattern"
- "Conduct capability study"
- "What's the difference between Cp and Cpk?"

## Purpose of SPC

SPC uses statistical methods to monitor, control, and improve processes by distinguishing between:
- **Common cause variation** - Normal, inherent process variation
- **Special cause variation** - Abnormal, assignable causes requiring action

### Why SPC Matters

**Without SPC:**
- React only when defects occur
- Cannot predict process behavior
- May over-adjust stable processes
- Miss early warning signs

**With SPC:**
- Detect problems before defects
- Understand process capability
- Make data-driven decisions
- Continuously improve

---

## Control Chart Selection

### Variable Data Charts (Measurements)

| Chart | Data Type | When to Use |
|-------|-----------|-------------|
| **X-bar/R** | Subgroups n=2-9 | Standard variable control chart |
| **X-bar/S** | Subgroups n≥10 | Large subgroups |
| **I-MR** | Individual measurements | Low volume, long cycle, destructive test |

### Attribute Data Charts (Counts/Categories)

| Chart | Data Type | When to Use |
|-------|-----------|-------------|
| **p chart** | Proportion defective | Variable sample size, defective/not |
| **np chart** | Count of defectives | Fixed sample size, defective/not |
| **c chart** | Defects per unit | Fixed area/unit, count defects |
| **u chart** | Defects per unit | Variable area/unit, count defects |

---

## X-bar/R Chart

### Setup

| Parameter | Guideline |
|-----------|-----------|
| Subgroup size (n) | 3-5 typical, 5 preferred |
| Subgroup frequency | Rational subgrouping - within-subgroup should be homogeneous |
| Minimum data points | 20-25 subgroups before calculating limits |

### Control Limit Formulas

**X-bar Chart:**
```
UCL = X̄̄ + A₂ × R̄
CL = X̄̄
LCL = X̄̄ - A₂ × R̄
```

**R Chart:**
```
UCL = D₄ × R̄
CL = R̄
LCL = D₃ × R̄
```

### Constants (A₂, D₃, D₄)

| n | A₂ | D₃ | D₄ |
|---|-----|-----|-----|
| 2 | 1.880 | 0 | 3.267 |
| 3 | 1.023 | 0 | 2.575 |
| 4 | 0.729 | 0 | 2.282 |
| 5 | 0.577 | 0 | 2.115 |
| 6 | 0.483 | 0 | 2.004 |

---

## Individual/Moving Range (I-MR) Chart

### When to Use
- Long cycle time
- Destructive testing
- Expensive testing
- Batch processes

### Control Limit Formulas

**I Chart:**
```
UCL = X̄ + 2.66 × MR̄
CL = X̄
LCL = X̄ - 2.66 × MR̄
```

**MR Chart:**
```
UCL = 3.267 × MR̄
CL = MR̄
LCL = 0
```

---

## Out-of-Control Rules

### Western Electric Rules (Standard)

| Rule | Pattern | Indicates |
|------|---------|-----------|
| **Rule 1** | 1 point beyond 3σ | Sudden shift |
| **Rule 2** | 9 points in a row on same side of CL | Process shift |
| **Rule 3** | 6 points in a row trending (up or down) | Trend/drift |
| **Rule 4** | 14 points in a row alternating up/down | Over-adjustment |

### Nelson Rules (Extended)

| Rule | Pattern |
|------|---------|
| **Rule 5** | 2 of 3 points beyond 2σ (same side) |
| **Rule 6** | 4 of 5 points beyond 1σ (same side) |
| **Rule 7** | 15 points in a row within 1σ of CL |
| **Rule 8** | 8 points beyond 1σ (both sides) |

### MNMUK Standard

Use Rules 1-4 (Western Electric) as standard. Apply Nelson rules for critical characteristics or detailed analysis.

---

## Process Capability

### Indices Overview

| Index | Measures | Formula |
|-------|----------|---------|
| **Cp** | Potential capability (spread) | (USL - LSL) / 6σ |
| **Cpk** | Actual capability (considers centering) | Min(Cpu, Cpl) |
| **Pp** | Process performance (spread) | (USL - LSL) / 6s |
| **Ppk** | Process performance (considers centering) | Min(Ppu, Ppl) |

### Key Difference: Cp/Cpk vs Pp/Ppk

| Aspect | Cp/Cpk | Pp/Ppk |
|--------|--------|--------|
| Variation estimate | Within-subgroup (R̄/d₂ or S̄/c₄) | Overall (sample std dev) |
| Represents | Process potential | Process performance |
| Use when | Process in control | Initial assessment |
| Typically | Higher | Lower |

### Capability Formulas

**Cp (Process Potential):**
```
Cp = (USL - LSL) / 6σ

Where σ = R̄/d₂ (within-subgroup estimate)
```

**Cpk (Process Capability):**
```
Cpu = (USL - X̄̄) / 3σ
Cpl = (X̄̄ - LSL) / 3σ
Cpk = Min(Cpu, Cpl)
```

**Pp (Process Performance):**
```
Pp = (USL - LSL) / 6s

Where s = sample standard deviation
```

**Ppk (Process Performance Index):**
```
Ppu = (USL - X̄) / 3s
Ppl = (X̄ - LSL) / 3s
Ppk = Min(Ppu, Ppl)
```

### d₂ Constants

| n | d₂ |
|---|-----|
| 2 | 1.128 |
| 3 | 1.693 |
| 4 | 2.059 |
| 5 | 2.326 |
| 6 | 2.534 |

---

## Capability Targets

### Automotive Industry Standards

| Index | Minimum | Preferred | For CC |
|-------|---------|-----------|--------|
| Cpk | 1.33 | 1.67 | 1.67 |
| Ppk | 1.33 | 1.67 | 1.67 |

### Interpretation

| Cpk Value | PPM (one tail) | Interpretation |
|-----------|----------------|----------------|
| 0.67 | 22,750 | Poor, not capable |
| 1.00 | 1,350 | Barely capable |
| 1.33 | 32 | Capable (minimum automotive) |
| 1.50 | 3.4 | Good |
| 1.67 | 0.3 | Very good (CC target) |
| 2.00 | 0.001 | Excellent |

---

## Capability Study Process

### Step 1: Plan the Study
- Identify characteristic
- Select measurement system (verify MSA)
- Determine sample size (minimum 30, prefer 50-100)
- Define sampling method

### Step 2: Collect Data
- Collect samples under normal conditions
- Record in time order
- Document any special events

### Step 3: Analyze Data
- Create histogram (check distribution)
- Check normality
- Calculate statistics
- Create control chart
- Check for statistical control

### Step 4: Calculate Capability
- If in control: Calculate Cp, Cpk
- If not in control: Address special causes first, or report Pp, Ppk only
- Compare to requirements

### Step 5: Interpret and Act
- Is capability adequate?
- What actions needed?
- Document results

---

## Pre-Control (Alternative to SPC)

### When to Use Pre-Control
- Very capable processes (Cpk >1.33)
- Short runs
- Quick setup verification
- Simpler than SPC

### Pre-Control Zones

```
┌─────────────────────────────────────────────┐
│               RED ZONE                       │ → Stop, adjust
├─────────────────────────────────────────────┤
│             YELLOW ZONE                      │ → Caution
├─────────────────────────────────────────────┤
│       GREEN ZONE (Middle 50%)                │ → OK
├─────────────────────────────────────────────┤
│             YELLOW ZONE                      │ → Caution
├─────────────────────────────────────────────┤
│               RED ZONE                       │ → Stop, adjust
└─────────────────────────────────────────────┘
      LSL           Target           USL
```

### Pre-Control Rules
1. **Startup:** 5 consecutive in Green = run production
2. **Running:**
   - Both in Green → Continue
   - One Yellow → Check again immediately
   - Both Yellow → Investigate/adjust
   - Red → Stop, investigate

---

## Output Format

When generating SPC content:

```markdown
# SPC Analysis

## Characteristic Information
| Field | Value |
|-------|-------|
| **Characteristic** | [Description] |
| **Specification** | [LSL - USL] |
| **Target** | [Nominal] |
| **Chart Type** | [X-bar/R, I-MR, etc.] |

## Control Chart Data
| Subgroup | X̄ (or X) | R (or MR) |
|----------|----------|-----------|
| 1 | | |
| ... | | |

## Control Limits
| Chart | LCL | CL | UCL |
|-------|-----|----|----|
| X-bar | | | |
| R | | | |

## Process Capability
| Index | Value | Requirement | Status |
|-------|-------|-------------|--------|
| Cpk | | ≥1.33 | PASS/FAIL |
| Ppk | | ≥1.33 | PASS/FAIL |

## Assessment
- In Control: Yes / No
- Capable: Yes / No
- Actions Required: [List]
```

---

## Integration with Related Skills

### ControlPlan
Control Plan specifies SPC requirements:
- Which characteristics require SPC
- Sample size and frequency
- Reaction to out-of-control

**Load:** `read ~/.claude/skills/Controlplan/SKILL.md`

### MSA
SPC validity requires adequate measurement system:
- ndc ≥5 for meaningful SPC
- Poor MSA = poor SPC decisions
- Verify MSA before starting SPC

**Load:** `read ~/.claude/skills/Msa/SKILL.md`

### AutomotiveManufacturing
Work instructions should include SPC procedures:
- How to collect data
- How to plot points
- How to interpret charts
- What to do when out of control

**Load:** `read ~/.claude/skills/Automotivemanufacturing/SKILL.md`

---

## Supplementary Resources

For detailed guidance:
`read ~/.claude/skills/Spc/CLAUDE.md`

For capability study template:
`read ~/.claude/skills/Spc/templates/capability-study.md`

For control chart selection:
`read ~/.claude/skills/Spc/reference/control-chart-selection.md`

For capability indices:
`read ~/.claude/skills/Spc/reference/capability-indices.md`

For out-of-control rules:
`read ~/.claude/skills/Spc/reference/out-of-control-rules.md`
