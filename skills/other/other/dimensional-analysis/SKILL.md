---
name: pie-dimensional-analysis
version: 1.0.0
description: "Mathematical verification for physical calculations: unit tracking algebra (exponent maps), PhysicalQuantity pattern for compound units, SI/Imperial mixed-unit handling, Buckingham pi theorem for dimensionless groups, and common engineering dimensionless numbers. Activates for unit verification, dimensional consistency checks, scaling analysis, and calculation validation across all infrastructure domains."
user-invocable: true
allowed-tools: Read Grep Glob Bash
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-26"
      triggers:
        intents:
          - "unit conversion"
          - "unit tracking"
          - "dimensional analysis"
          - "dimensionless"
          - "Reynolds number"
          - "Nusselt number"
          - "Buckingham pi"
          - "scaling"
          - "unit check"
          - "SI"
          - "imperial"
          - "unit mismatch"
          - "physical quantity"
        contexts:
          - "calculation verification"
          - "infrastructure engineering"
          - "unit algebra"
          - "dimensional homogeneity"
applies_to:
  - skills/physical-infrastructure/**
  - lib/units.ts
---

# Dimensional Analysis Skill

## At a Glance

Dimensional analysis is the mathematical verification layer that ensures physical calculations are dimensionally consistent -- catching unit errors before they become calculation errors.

**When to activate:**
- Verify multi-step calculations for unit consistency
- Mix SI and Imperial units in the same calculation
- Scale experimental data to new conditions via dimensionless groups
- Identify governing parameters of a physical system
- Validate Calculator agent outputs before committing to CalculationRecord

**Key capabilities:**
- Unit tracking via exponent maps (PhysicalQuantity pattern)
- Compound unit algebra: multiply, divide, power, dimensional homogeneity
- Dimensional mismatch detection at every arithmetic step
- SI to Imperial conversion for all infrastructure engineering domains
- Buckingham pi theorem for deriving dimensionless groups
- Infrastructure dimensionless numbers: Reynolds, Nusselt, Prandtl, Grashof, Froude, Strouhal

**Integration:** Cross-cutting skill -- applies to outputs from fluid-systems, power-systems, and thermal-engineering. Acts as verification layer before Calculator agent commits to CalculationRecord.

> **NOTE:** Dimensional analysis verifies mathematical self-consistency only. It does not replace engineering judgment or safety verification. Dimensionally correct equations can still be physically wrong if incorrect constants or assumptions are used.

**Quick routing:**
- Unit conversions only --> @references/unit-algebra.md for full tables
- Pi theorem derivation --> @references/buckingham-pi.md for worked examples
- Tolerance stack-up --> see Tolerance Stack-Up Analysis section below
- Spatial fit checking --> see Spatial Constraint Verification section below

---

## Unit Tracking Algebra

### The Seven SI Base Units

| Symbol | Quantity | Notes |
|--------|----------|-------|
| m | length | meter |
| kg | mass | kilogram (only SI base unit with a prefix) |
| s | time | second |
| A | electric current | ampere |
| K | temperature | kelvin (absolute; not degrees Celsius) |
| mol | amount of substance | mole |
| cd | luminous intensity | candela (rarely used in infrastructure) |

### Compound Units as Exponent Maps

Every physical quantity carries its unit as a map of base unit exponents. This representation makes unit algebra mechanical -- multiply means add exponents, divide means subtract.

Examples:
- Velocity: 2.4 m/s --> `{ value: 2.4, units: { m: 1, s: -1 } }`
- Pressure: 101325 Pa --> `{ value: 101325, units: { kg: 1, m: -1, s: -2 } }`
- Power: 1000 W --> `{ value: 1000, units: { kg: 1, m: 2, s: -3 } }`
- Thermal conductivity: 385 W/(m*K) --> `{ value: 385, units: { kg: 1, m: 1, s: -3, K: -1 } }`

### Common Infrastructure Units -- Exponent Map Reference

| Quantity | SI Unit | Symbol | Exponent Map |
|----------|---------|--------|-------------|
| Force | Newton | N | { kg:1, m:1, s:-2 } |
| Pressure | Pascal | Pa | { kg:1, m:-1, s:-2 } |
| Energy | Joule | J | { kg:1, m:2, s:-2 } |
| Power | Watt | W | { kg:1, m:2, s:-3 } |
| Dynamic viscosity | -- | Pa*s | { kg:1, m:-1, s:-1 } |
| Heat transfer coeff | -- | W/(m^2*K) | { kg:1, s:-3, K:-1 } |
| Thermal conductivity | -- | W/(m*K) | { kg:1, m:1, s:-3, K:-1 } |

### The PhysicalQuantity Interface

The Calculator agent implements unit-safe arithmetic using this TypeScript pattern. The SKILL documents the knowledge; `lib/units.ts` provides the implementation.

```typescript
interface PhysicalQuantity {
  value: number;
  units: { [baseUnit: string]: number }; // exponent map
}

function multiply(a: PhysicalQuantity, b: PhysicalQuantity): PhysicalQuantity {
  const result: PhysicalQuantity = { value: a.value * b.value, units: { ...a.units } };
  for (const [unit, exp] of Object.entries(b.units)) {
    result.units[unit] = (result.units[unit] || 0) + exp;
  }
  // Remove zero exponents
  for (const unit of Object.keys(result.units)) {
    if (result.units[unit] === 0) delete result.units[unit];
  }
  return result;
}

function divide(a: PhysicalQuantity, b: PhysicalQuantity): PhysicalQuantity {
  const negated = { value: 1 / b.value, units: Object.fromEntries(
    Object.entries(b.units).map(([k, v]) => [k, -v])
  )};
  return multiply(a, negated);
}

function assertSameUnits(a: PhysicalQuantity, b: PhysicalQuantity): void {
  const aKeys = Object.keys(a.units).sort().join(',');
  const bKeys = Object.keys(b.units).sort().join(',');
  if (aKeys !== bKeys || !Object.entries(a.units).every(([k, v]) => b.units[k] === v)) {
    throw new Error(`Unit mismatch: [${aKeys}] vs [${bKeys}] — cannot add/subtract`);
  }
}
```

### Unit Algebra Rules

| Operation | Exponent Rule | Example |
|-----------|---------------|---------|
| Multiply | Exponents ADD | (m/s) * (m/s) = m^2/s^2 |
| Divide | Exponents SUBTRACT | J / m^3 = Pa (energy density = pressure) |
| Power n | Exponents MULTIPLY by n | (m^2)^0.5 = m |
| Add/Subtract | Units must be IDENTICAL | m + m = m; m + s = ERROR |
| Dimensionless | All exponents = 0 | `units: {}` (empty map) |

The dimensional homogeneity rule is absolute: you cannot add quantities with different units. If `assertSameUnits()` throws, the calculation has a structural error that must be fixed before proceeding.

---

## Mixed Unit Systems

Infrastructure engineering inherently mixes SI and Imperial units. This is not optional -- it is driven by standards bodies, building codes, and equipment manufacturers.

**Common mixed-unit scenarios:**
- Pipe sizes: NPS in inches (ASME B36.10 standard)
- Flow rates: GPM (US practice) or L/s (SI practice)
- Pressure: PSI (US safety codes, ASME BPVC) or kPa (SI engineering)
- Temperature: degrees F (US weather/safety) or degrees C (SI engineering)
- Power: BTU/hr (US HVAC industry) or kW (SI)
- Conductors: AWG (US NEC) or mm^2 (EU/IEC)

### Strategy: Convert Immediately, Work in SI, Convert Output

1. **Receive** mixed-unit inputs (e.g., pipe diameter in inches, flow in GPM)
2. **Convert** ALL inputs to SI at the boundary -- `lib/units.ts` handles this
3. **Calculate** entirely in SI using PhysicalQuantity arithmetic
4. **Convert** final outputs to user-preferred units for display

This eliminates mixed-unit errors in the calculation core. Conversion errors are isolated to the boundary layer where they are easy to audit.

### Common Conversions -- Quick Reference

| From | To | Factor |
|------|----|--------|
| inches | meters | x 0.0254 |
| feet | meters | x 0.3048 |
| PSI | kPa | x 6.8948 |
| GPM | L/s | x 0.06309 |
| BTU/hr | W | x 0.29307 |
| degrees F | degrees C | (F - 32) / 1.8 |
| degrees C | K | + 273.15 |
| ft/s | m/s | x 0.3048 |
| lb/ft^3 | kg/m^3 | x 16.018 |

Full conversion table for all infrastructure engineering domains --> @references/unit-algebra.md

---

## Buckingham Pi Theorem

### The Theorem

For a physical equation relating **n** dimensional variables that involve **k** independent base dimensions, the equation can be rewritten using **(n - k)** independent dimensionless groups.

This means: if you have 6 variables and 3 base dimensions, you need only 3 dimensionless groups to describe the physics -- regardless of what unit system you use. The universe is dimensionally self-consistent.

### Procedure (5 Steps)

1. **List variables** -- identify every physical quantity that could influence the outcome. Include the dependent variable.
2. **Write dimensions** -- express each variable in base units (m, kg, s, A, K).
3. **Count k** -- number of independent base dimensions appearing. Usually 2-4 for engineering problems.
4. **Choose k repeating variables** -- variables that together span all k dimensions. Avoid the dependent variable. Common choices: (rho, v, L) for fluid flows; (k, L, h) for heat transfer.
5. **Form pi groups** -- multiply each remaining variable with the repeating variables raised to unknown powers; solve exponents so that the result is dimensionless.

### Worked Example: Pipe Flow Pressure Drop

**Variables:** delta_P (pressure drop), L (pipe length), D (pipe diameter), rho (fluid density), mu (dynamic viscosity), v (flow velocity)

n = 6 variables, k = 3 base dimensions {kg, m, s}

**Repeating variables:** rho, v, D (together they contain all three dimensions: rho has kg and m, v has m and s, D has m)

**Form n - k = 3 dimensionless groups:**

| Group | Combination | Result | Name |
|-------|-------------|--------|------|
| pi_1 | delta_P * D / (rho * v^2) | dimensionless | Euler number (pressure coefficient) |
| pi_2 | rho * v * D / mu | dimensionless | Reynolds number |
| pi_3 | L / D | dimensionless | Length ratio |

**Physical law recovered:** Euler = f(Re, L/D)

This is exactly the structure of the Darcy-Weisbach equation: delta_P = f * (L/D) * (rho * v^2 / 2). Dimensional analysis recovers the equation form without any physics -- only dimensional reasoning.

For full theorem derivation, dimensional matrix method, and five infrastructure worked examples --> @references/buckingham-pi.md

### Common Infrastructure Dimensionless Groups

| Group | Formula | Physical Meaning | Activation Threshold |
|-------|---------|-----------------|---------------------|
| Reynolds | Re = rho*v*L / mu | Inertia / viscous force | Re > 4000 = turbulent flow |
| Nusselt | Nu = h*L / k | Convection / conduction | Heat transfer coefficient |
| Prandtl | Pr = mu*Cp / k | Momentum / thermal diffusivity | Nu correlation parameter |
| Grashof | Gr = g*beta*dT*L^3 / nu^2 | Buoyancy / viscous force | Natural convection indicator |
| Froude | Fr = v / sqrt(g*L) | Inertia / gravity | Open channel flow regime |
| Strouhal | St = f*L / v | Vortex shedding frequency | Pipe vibration analysis |

**Why these matter for infrastructure:**
- **Re** determines whether pipe flow is laminar or turbulent -- which selects the friction factor equation (Moody chart vs 64/Re)
- **Nu** determines convective heat transfer coefficient -- drives heat exchanger sizing
- **Pr** groups fluid thermal properties -- used in every forced convection correlation
- Dimensional analysis reveals which parameters dominate -- enables experimental scale-up (same Re = same physics at any size)

---

## Calculation Verification Workflow

The Calculator agent applies this skill as a verification pass on all numerical outputs. Every multi-step calculation follows this protocol:

### Step 1: Convert Inputs
All inputs converted to SI via `lib/units.ts`. Record each as a PhysicalQuantity with explicit exponent map.

### Step 2: Track Through Calculation
Each arithmetic step propagates units via multiply/divide rules. Intermediate results carry their units.

### Step 3: Check Dimensional Homogeneity
At each addition or subtraction, verify units match via `assertSameUnits()`. If mismatch: stop, flag error, do not proceed.

### Step 4: Verify Result Units
Final result should have expected unit exponents:
- Pipe sizing result should have units `{ m: 1 }` (a length/diameter)
- Pressure drop should have units `{ kg: 1, m: -1, s: -2 }` (Pascal)
- Flow rate should have units `{ m: 3, s: -1 }` (cubic meters per second)

If result has wrong units, something was inverted or an exponent was applied incorrectly. Flag the error.

### Step 5: Check Reasonableness
Dimensionless numbers should be in expected ranges:
- Re < 2300: laminar (unusual for data center cooling loops -- flag if unexpected)
- Re > 4000: turbulent (normal for infrastructure piping)
- Nu > 100: high convective transfer (expected for turbulent water flow; flag if < 10)
- Pr ~ 7 for water at room temperature; flag if wildly different

### Worked Multi-Step Example: Pipe Sizing Verification

**Input:** Heat load Q = 40 kW, temperature difference dT = 10 K, max velocity v_max = 2.4 m/s

**Step 1 -- Flow rate:**
```
m_dot = Q / (rho * Cp * dT)
Units: W / (kg/m^3 * J/(kg*K) * K)
     = kg*m^2/s^3 / (kg/m^3 * kg*m^2/(s^2*kg*K) * K)
     = kg*m^2/s^3 / (m^3/s^2 * 1/m^3)
     ... simplifies to m^3/s  [PASS]
```

**Step 2 -- Minimum cross-sectional area:**
```
A_min = V_dot / v_max
Units: (m^3/s) / (m/s) = m^2  [PASS]
```

**Step 3 -- Minimum diameter:**
```
D_min = sqrt(4 * A_min / pi)
Units: sqrt(m^2) = m  [PASS]
```

**Step 4 -- Pressure drop (Darcy-Weisbach):**
```
dP = f * (L/D) * (rho * v^2 / 2)
Units: dimensionless * (m/m) * (kg/m^3 * m^2/s^2) = kg/(m*s^2) = Pa  [PASS]
```

Each step is dimensionally verified before proceeding. If any step produces wrong units, the error is caught before it propagates through the rest of the calculation chain.

---

## Tolerance Stack-Up Analysis

Real manufactured components have dimensional tolerances. When multiple components assemble in series, tolerances accumulate. The critical question: does the worst-case assembly actually fit in the available space?

### Worst-Case Method (Conservative)

**Formula:** T_total = sum of |t_i| (sum of all individual tolerance magnitudes)

This assumes all tolerances are simultaneously at their worst values. It is always conservative -- the result is the absolute maximum possible deviation.

**When to use:**
- Safety-critical assemblies (pressure containment, seismic bracing)
- Small assemblies with 4 or fewer components (RSS benefit is marginal)
- Zero tolerance for field rework

**Decision rule:** If nominal_gap >= nominal_assembly + T_total, the assembly always fits regardless of manufacturing variation.

### RSS Method (Root Sum of Squares, Statistical)

**Formula:** T_total = sqrt(sum of t_i^2)

This assumes tolerances are independent, normally distributed, and centered on nominal values. The probability that all tolerances simultaneously reach their worst values is vanishingly small -- for n=5 components, P(all worst) = (0.0027)^5 = 1.4 x 10^-13.

**Result:** RSS total is typically 40-70% of worst-case total for 5 or more components. This represents significant material and space savings.

**When to use:**
- Large assemblies with 5 or more independent components
- Moderate cost of occasional interference (rework is feasible)
- Tolerances are truly independent (no shared manufacturing process)

### Choosing the Right Method

| Scenario | Method | Rationale |
|----------|--------|-----------|
| Safety-critical (pressure containment) | Worst-case | Zero tolerance for interference |
| Small assembly (<5 components) | Worst-case | RSS benefit is marginal |
| Large assembly (5+ components) | RSS | Statistical saving is significant |
| Expensive rework | RSS with verification tests | Balance economy vs risk |

### Worked Example -- Pipe Assembly in Wall Chase

**Setup:** One 2" pipe (NPS) with insulation in a field-cut wall chase.

| Component | Nominal | Tolerance |
|-----------|---------|-----------|
| Chase width | 8.000" | +/- 0.250" (field cut) |
| Pipe OD | 2.375" | +/- 0.010" (manufacturing) |
| Insulation thickness (each side) | 1.000" | +/- 0.125" (installation) |
| Required clearance (each side) | 0.500" | -- |

**Nominal assembly width:** 2.375 + 2 x 1.000 = 4.375"
**Nominal with clearances:** 4.375 + 2 x 0.500 = 5.375"

**Worst-case tolerance:** T = 0.010 + 0.125 + 0.125 = 0.260" (pipe + both insulation layers)
**Available space (worst case):** 8.000 - 0.250 = 7.750"
**Required space (worst case):** 5.375 + 0.260 = 5.635"
**Margin:** 7.750 - 5.635 = 2.115" --> **PASSES**

**Second scenario -- add a second 2" pipe:**
Total nominal assembly: 2.375 + 2.067 + 2 x 1.000 + 2 x 1.000 = 8.442"
This already exceeds the 8.000" nominal chase width --> **FAILS at nominal before tolerances are even considered.** The chase must be widened or the routing redesigned.

For statistical tolerance analysis with non-normal distributions and Monte Carlo simulation --> @references/tolerance-stack-up.md

---

## Spatial Constraint Verification

### Bounding Box Intersection Test

**AABB (Axis-Aligned Bounding Box)** -- the standard approach for infrastructure equipment placement:

Define each item by its min/max coordinates: {x_min, x_max, y_min, y_max, z_min, z_max}

Overlap test:
```
overlap = NOT (A.x_max < B.x_min OR A.x_min > B.x_max)
      AND NOT (A.y_max < B.y_min OR A.y_min > B.y_max)
      AND NOT (A.z_max < B.z_min OR A.z_min > B.z_max)
```

If no overlap on any axis, no collision -- items fit.

**OBB (Oriented Bounding Box)** -- for rotated equipment: more complex, uses the separating axis theorem. Only needed when equipment is not aligned to a 90-degree grid.

For infrastructure placement, most equipment is axis-aligned. AABB is sufficient and fast (O(1) per pair).

### Clearance Verification

After confirming no AABB overlap, verify that the gap between items meets or exceeds code-mandated minimums. Expand one bounding box by the required clearance in all directions and re-test -- if the expanded box overlaps, clearance is insufficient.

### NEC 110.26 Working Space (Electrical Panels)

| Voltage to Ground | Condition 1 (live one side) | Condition 2 (live + grounded both sides) | Condition 3 (live both sides) |
|-------------------|----------------------------|------------------------------------------|-------------------------------|
| 0-150V | 3 ft | 3 ft | 3 ft |
| 151-600V | 3 ft | 3.5 ft | 4 ft |
| 601-2500V | 4 ft | 4 ft | 5 ft |

**Width:** Minimum 30" or width of equipment, whichever is greater.
**Height:** Minimum 6.5 ft or height of equipment above floor.
**Illumination:** Required for all working spaces (NEC 110.26(D)).
**Dedicated space:** Working clearance area must not be used for storage; overhead piping and ducts are prohibited in dedicated electrical space (NEC 110.26(E)).

### Mechanical Access Clearances (General Rules)

| Equipment | Minimum Clearance | Rationale |
|-----------|------------------|-----------|
| Valve handwheel | 6" all around | Operation access |
| Valve actuator (pneumatic/electric) | 12"-18" | Maintenance and removal |
| Pump casing | 24" in shaft direction | Impeller removal |
| Heat exchanger | 100% of tube bundle length | Tube cleaning access |
| Air handler | 36" front clearance | Filter access |
| Server rack | 42"-48" front and rear | Hot aisle containment |

---

## Interference Checking

### Pipe Chase Fill

Total assembly width in a pipe chase:

```
W_required = sum(pipe_OD_i + 2 * insulation_i) + (n-1) * separation + 2 * wall_clearance
```

**Minimum pipe-to-pipe separation:** 0.5 x OD of the larger pipe (thermal expansion and installation access).

**Algorithm for n pipes in a chase of width W:**
1. Sum all pipe-plus-insulation widths
2. Add (n - 1) x minimum separation clearances
3. Add 2 x wall clearance (typically 1" each side)
4. Compare required total to chase width W
5. Apply worst-case tolerance: available = W - T_chase; required = sum + T_pipes
6. If required > available at worst case, the chase must be widened

### Cable Tray Fill (NEC 392.22)

| Cable Type | Max Fill | Notes |
|-----------|----------|-------|
| 600V multiconductor, <=2000 kcmil | 50% of tray cross-sectional area | Area = cable OD^2 x pi/4 |
| Power cables >2000 kcmil | Single layer only | No stacking; check current derating |
| Control/instrument (<=1" OD) | 50% of area | |
| Mixed power + control | 40% for control portion | Separation between power and control recommended |

**Tray fill calculation:** sum(cable cross-sectional areas) <= tray_width x tray_depth x fill_fraction

**Common trap:** Using jacket OD area instead of individual conductor area. Using jacket OD is conservative but acceptable; using conductor area is more accurate but requires knowing the cable construction.

### Minimum Bend Radius

| Material | Minimum Bend Radius |
|----------|-------------------|
| Steel pipe (Schedule 40) | 5-6 x OD |
| Copper pipe (Type L/K) | 4 x OD |
| PEX tubing | 8 x OD minimum |
| Rigid conduit (>1" trade) | 6 x trade size |
| EMT conduit | 5 x trade size |
| THWN-2 conductor | 8 x OD (NEC 300.34) |
| Armored cable (AC/MC) | 7 x smallest OD dimension |

All routing changes of direction must have adequate bend radius. Flag tight bends for field review -- undersized bends cause flow restriction in pipes and conductor damage in cables.

### Slope Requirements

| System | Minimum Slope | Notes |
|--------|--------------|-------|
| Drain/waste/vent (horizontal) | 1/4" per foot (2.08%) | IPC/UPC gravity drain |
| Storm drainage (horizontal) | 1/8" per foot (1.04%) | Minimum; more is better |
| HVAC condensate drain | 1/4" per foot | Away from air handler |
| Steam condensate return | 1/2" per foot | In direction of flow |
| Cold water supply | None required | Pressurized system |
| Hot water supply | None required | Pressurized; slope for drainability preferred |

### Safety Warden Integration

Interference checking triggers Safety Warden findings at these severity levels:

| Condition | Severity | Domain | Action |
|-----------|---------|--------|--------|
| Equipment bounding box overlap | critical | structural | Block -- cannot place overlapping equipment |
| Clearance < code minimum (electrical panel) | critical | voltage | Block until clearance verified by PE |
| Pipe chase fill > 100% at worst-case tolerance | blocking | structural | Redesign chase or reroute pipes |
| Cable tray fill > 50% | warning | structural | Review tray sizing; may need larger tray |
| Bend radius below minimum | warning | structural | Flag for field review (critical if pressure piping) |
| Missing required slope on gravity drain | warning | plumbing | Verify routing elevation changes |

---

## Reference Documents

| Reference | When to Read | Coverage |
|-----------|-------------|----------|
| @references/unit-algebra.md | Full SI/Imperial conversion tables, all infrastructure domains | Complete unit reference |
| @references/buckingham-pi.md | Full theorem derivation, dimensional matrix, five worked examples | Deep pi theorem guide |
| @references/tolerance-stack-up.md | Statistical analysis, GD&T basics, Monte Carlo simulation | Tolerance engineering |
| @references/spatial-constraints.md | OBB algorithm, full NEC 110.26 tables, cable tray details | Spatial verification |

---
*Dimensional Analysis Skill v1.0.0 -- Physical Infrastructure Engineering Pack*
*Phase 437 | References: BIPM SI Brochure (9th ed.), Buckingham (1914), Bridgman (1922), NEC 2023, ASME Y14.5*
*Dimensional verification is a mathematical check -- not a substitute for engineering judgment.*
