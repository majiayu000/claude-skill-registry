---
name: pie-fluid-systems
version: 1.0.0
description: "Water-based fluid system design: pipe sizing (Darcy-Weisbach, Hazen-Williams), flow rates, pressure drops, CDU selection for DTC cooling, pump curves, and ASHRAE TC 9.9 water class enforcement. Activates for cooling loop design, plumbing calculations, CDU selection, pump sizing, and hydraulic system validation."
user-invocable: true
allowed-tools: Read Grep Glob Bash
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-26"
      triggers:
        intents:
          - "pipe sizing"
          - "flow rate"
          - "pressure drop"
          - "CDU"
          - "direct-to-chip"
          - "cooling loop"
          - "pump selection"
          - "NPSH"
          - "Darcy-Weisbach"
          - "Hazen-Williams"
          - "water cooling"
          - "hydraulic"
          - "plumbing"
          - "chilled water"
          - "ASHRAE"
        contexts:
          - "data center cooling design"
          - "plumbing system design"
          - "infrastructure engineering"
          - "cooling loop sizing"
applies_to:
  - skills/physical-infrastructure/**
  - "*.calc"
  - "*.pid"
---

# Fluid Systems Skill

## At a Glance

Design and validate water-based fluid systems from household plumbing to high-density data center cooling loops.

**Activation:** InfrastructureRequest type='cooling' or type='plumbing', any CDU sizing request, pipe sizing question, flow rate calculation, or pressure drop analysis.

**Key capabilities:**

- Pipe sizing via Darcy-Weisbach (all fluids) and Hazen-Williams (water only)
- Flow rate calculation from heat load (Q = Q_heat / (rho x Cp x DT))
- Pressure drop analysis with fitting equivalent lengths
- ASHRAE TC 9.9 water class selection (W1-W5) for data center cooling
- CDU/DTC cooling selection and manifold topology
- Pump curve analysis with NPSH verification and affinity laws
- Safety boundary enforcement by safety class (residential through industrial)

> ENGINEERING DISCLAIMER: All calculations must be verified by a licensed Professional Engineer before use in construction or installation. Local plumbing codes (IPC/UPC) and pressure vessel standards (ASME B31.9) impose requirements not captured here. User assumes all responsibility for verification.

**Quick routing:** Pipe sizing method -- see Pipe Sizing. ASHRAE water class selection -- see Data Center Cooling. Pump selection and NPSH -- see Pump Selection. Full derivations -- @references/pipe-sizing.md.

---

## Pipe Sizing

### Darcy-Weisbach (All Fluids)

The general pressure drop equation for incompressible flow in pipes:

```
DeltaP = f x (L/D) x (rho x v^2 / 2)
```

| Variable | Definition | Units |
|----------|-----------|-------|
| DeltaP | Pressure drop | Pa |
| f | Darcy friction factor | dimensionless |
| L | Pipe length | m |
| D | Internal pipe diameter | m |
| rho | Fluid density | kg/m^3 |
| v | Flow velocity | m/s |

**Friction factor f:** Determined from the Moody diagram or computed via the Colebrook-White equation for turbulent flow:

```
1/sqrt(f) = -2 log( epsilon/(3.7D) + 2.51/(Re sqrt(f)) )
```

This is implicit in f and requires iteration (3-4 iterations from f=0.02 starting point converge). The Swamee-Jain explicit approximation avoids iteration -- see @references/pipe-sizing.md.

**Reynolds number:** Re = rho x v x D / mu

| Regime | Re Range | Friction Factor |
|--------|---------|-----------------|
| Laminar | < 2,300 | f = 64/Re |
| Transition | 2,300 - 4,000 | Avoid -- unstable |
| Turbulent | > 4,000 | Colebrook equation |

**Pipe roughness epsilon:**

| Material | epsilon (m) | Common Use |
|----------|------------|------------|
| Copper | 0.0000015 | Plumbing, chilled water |
| PVC | 0.0000015 | Drain, low-pressure supply |
| Galvanized steel | 0.00015 | Older installations |
| Cast iron | 0.00026 | Municipal, fire protection |
| Stainless steel | 0.000015 | Process, high-purity |

For full Colebrook equation derivation and Moody chart interpretation -- @references/pipe-sizing.md

### Hazen-Williams (Water Only)

Simpler empirical formula valid only for water at normal temperatures in turbulent flow:

```
v = 0.849 x C x R^0.63 x S^0.54
```

| Variable | Definition | Units |
|----------|-----------|-------|
| v | Velocity | m/s |
| C | Hazen-Williams coefficient | dimensionless |
| R | Hydraulic radius (D/4 for full circular pipes) | m |
| S | Slope of hydraulic grade line (DeltaP / (gamma x L)) | dimensionless |

**C coefficients:**

| Material | C Value |
|----------|---------|
| Copper | 150 |
| PEX | 150 |
| PVC | 150 |
| New steel | 145 |
| Cast iron | 130 |
| Old steel (20+ years) | 100 |

**When to use:** Water systems only, turbulent flow, not valid for viscous fluids or non-circular pipe cross-sections. Simpler than Darcy-Weisbach but less accurate; acceptable for plumbing design and preliminary sizing.

### Velocity Limits

| Application | Min (ft/s) | Max (ft/s) | Rationale |
|-------------|-----------|-----------|-----------|
| Main distribution lines | 4 | 6 | Balance pressure drop vs noise |
| Branch lines | 2 | 4 | Noise reduction near occupants |
| Data center cooling | 3 | 8 | Higher acceptable in enclosed space |
| Suction piping | 1 | 3 | NPSH protection |

Velocities below 2 ft/s risk sedimentation; above 8 ft/s risk erosion, noise, and water hammer.

### Standard Pipe Size Selection

**Process:** Calculate minimum internal diameter from velocity limits at design flow rate, then select the next larger NPS (Nominal Pipe Size).

**Standard NPS sizes:** 1/2", 3/4", 1", 1-1/4", 1-1/2", 2", 2-1/2", 3", 4", 6", 8", 10", 12"

Full OD/ID data available from engineering-constants.ts via `getPipeSize(nps, schedule)`.

**Schedule selection:**

| Schedule | Use Case | Wall Thickness |
|----------|---------|----------------|
| Schedule 40 | Standard pressure (up to ~150 PSI for smaller sizes) | Standard |
| Schedule 80 | Higher pressure, corrosive fluids | Thicker wall, smaller ID |

**Metric equivalents:** DN15 (1/2"), DN20 (3/4"), DN25 (1"), DN50 (2"), DN100 (4"), DN150 (6"), DN200 (8"), DN300 (12")

---

## Flow Rate Calculation

### From Heat Load

Primary formula for determining coolant flow rate to remove a given heat load:

```
Q_flow (L/s) = Q_heat (kW) / ( rho (kg/m^3) x Cp (kJ/(kg K)) x DeltaT (K) )
```

**Water properties:**

| Condition | rho (kg/m^3) | Cp (kJ/(kg K)) |
|-----------|-------------|-----------------|
| Water at 20C | 998 | 4.182 |
| Chilled water at 7C | 999.8 | 4.195 |
| Warm water at 45C | 990 | 4.180 |

**Typical DeltaT values:**

| Application | DeltaT (C) |
|-------------|-----------|
| Data center primary loop | 8-12 (ASHRAE recommended) |
| Server-side CDU loop | 5-8 |
| Chilled water plant | 6-8 |
| District heating return | 15-25 |

**Unit conversions:** 1 L/s = 15.85 GPM | 1 kPa = 0.145 PSI | 1 kW = 3,412 BTU/hr

### Worked Example

**Scenario:** 40 kW rack, supply 20C, return 30C, DeltaT = 10C

```
Q_flow = 40 / (998 x 4.182 x 10)
       = 40 / 41,736
       = 0.000958 m^3/s
       = 0.958 L/s
       = 15.2 GPM
```

At 6 ft/s (1.83 m/s) target velocity:

```
A = Q / v = 0.000958 / 1.83 = 0.000524 m^2
D = sqrt(4A / pi) = sqrt(4 x 0.000524 / 3.14159) = 0.0258 m = 1.02 in
```

Select next larger NPS: 1-1/4" (Schedule 40, ID = 1.38 in). Actual velocity: 3.3 ft/s -- within acceptable range.

### From Fixture Units (Plumbing)

Per UPC/IPC Table 610.3 (demand conversion):

| Fixture | Fixture Units (FU) |
|---------|-------------------|
| Water closet (flush valve) | 10 |
| Water closet (tank) | 4 |
| Lavatory (private) | 1 |
| Lavatory (public) | 2 |
| Kitchen sink | 2 |
| Shower | 2 |
| Bathtub | 4 |
| Dishwasher | 2 |
| Washing machine | 4 |

**Demand conversion:** Total fixture units mapped to design flow rate via UPC demand curve (not linear -- accounts for diversity). Approximately: 1 FU corresponds to 1 GPM demand basis at the riser.

---

## Pressure Drop Analysis

### Equivalent Length Method (Fittings)

Convert each fitting to an equivalent length of straight pipe, then sum with actual pipe length for total pressure drop calculation.

| Fitting | Equivalent Length (pipe diameters) |
|---------|-----------------------------------|
| 90 degree standard elbow | 30D |
| 90 degree long-radius elbow | 16D |
| 45 degree elbow | 16D |
| Tee (flow through branch) | 60D |
| Tee (straight through) | 20D |
| Gate valve (fully open) | 8D |
| Globe valve (fully open) | 340D |
| Check valve (swing) | 50D |
| Ball valve (fully open) | 3D |
| Strainer/filter | 50-100D (check vendor data) |

### System Curve

Total system pressure drop is the sum of all resistances:

```
DeltaP_total = DeltaP_pipe + DeltaP_fittings + DeltaP_equipment + DeltaP_elevation
```

- **Pipe losses:** Darcy-Weisbach or Hazen-Williams applied to total equivalent length
- **Equipment losses:** CDU, chiller, heat exchanger -- use vendor pressure drop curves at design flow
- **Elevation term:** DeltaP_elev = rho x g x DeltaH (Pa), where DeltaH = height change in meters
- **Design margin:** Size system to operate at 75% of available pressure differential to accommodate future expansion

### Water Hammer Check

Surge pressure from sudden valve closure:

```
DeltaP_hammer = rho x c x DeltaV
```

Where c is approximately 1,400 m/s for water in rigid pipe. Keep surge pressure below the safety class limit (see Safety Boundaries).

Mitigation: slow-closing valves (5+ second stroke), surge tanks, relief valves, VFD-controlled pumps with soft ramp-down.

---

## Data Center Cooling

### ASHRAE TC 9.9 Water Classes

| Class | Supply Temp Range | Typical Use Case | Economizer Hours/Year |
|-------|------------------|-------------------|----------------------|
| W1 | 2-17C | Legacy data centers, high-density GPU | <500 (most climates) |
| W2 | 2-27C | Mixed air + liquid cooling | ~500-2,000 |
| W3 | 2-33C | Modern liquid-cooled, moderate climates | ~3,000-5,000 |
| W4 | 2-45C | Warm water cooling, high economizer use | ~6,000+ |
| W5 | >45C | Hot water, heat recovery to district heating | ~8,000+ |

**Class selection:** Higher W class enables more free-cooling hours and lower PUE. Verify server inlet air temperature remains within ASHRAE A-class (15-35C) for mixed air+liquid environments.

Full ASHRAE TC 9.9 water class specifications -- @references/ashrae-tc9-9.md

### CDU Selection for DTC Cooling

The Coolant Distribution Unit (CDU) is the heat exchanger that isolates facility water from the server-level coolant loop.

**Sizing:** CDU rated kW >= rack peak heat load x 1.25 (design margin)

**Direct-to-chip (DTC) parameters:**

| Parameter | Typical Range | Notes |
|-----------|--------------|-------|
| Flow per cold plate | 0.5-2.0 LPM | Verify with server/GPU vendor spec |
| Server-side pressure | 50-150 kPa | CDU provides pressure isolation |
| Cold plate inlet temp | 25-45C (W3/W4 class) | Depends on water class |
| Manifold topology | Per-rack supply/return headers | Quick-disconnect fittings |

**Leak detection requirements:**

| Zone | Sensor Location | Response |
|------|----------------|----------|
| 1 - Server tray | Overflow tray in each tray | Local alert |
| 2 - CDU drain pan | Under each CDU assembly | Auto-shutoff CDU supply |
| 3 - Raised floor | Floor-mounted leak cable/sensor | Room alarm + facility shutoff |
| 4 - Building BMS | Aggregated from all zones | Facility-wide response |

**Secondary containment:** Drip pan beneath each rack assembly minimum for data center class. Guttered containment for high-density installations.

Full CDU selection criteria -- @references/ashrae-tc9-9.md

---

## Pump Selection

### Operating Point

The operating point is the intersection of the system curve (parabolic: DeltaP = k x Q^2) and the pump H-Q curve (from vendor data).

- Plot both curves on the same axes (flow rate vs head/pressure)
- Operating point must fall within the pump's stable operating region
- Avoid operating on drooping portions of the pump curve

### NPSH Verification

Net Positive Suction Head prevents cavitation:

```
NPSH_available = (P_atm - P_vapor) / (rho x g) + z_source - h_friction_suction
```

| Condition | P_vapor (kPa) |
|-----------|--------------|
| Water at 20C | 2.34 |
| Water at 40C | 7.38 |
| Water at 60C | 19.9 |
| Water at 100C | 101.3 |

**Rule:** NPSH_available must exceed NPSH_required (from vendor pump curve) by at least 0.5 m. Recommended margin: 1.0 m.

**Low NPSH remedies:** Lower pump elevation relative to source, shorten suction pipe, increase suction pipe diameter, reduce suction-side fittings.

**Cavitation consequences:** Noise, vibration, impeller erosion, loss of flow capacity, eventual pump failure.

### Pump Affinity Laws (VFD Sizing)

| Parameter | Scaling Law | Example (50% speed) |
|-----------|------------|---------------------|
| Flow Q | Q2 = Q1 x (N2/N1) | 50% flow |
| Head H | H2 = H1 x (N2/N1)^2 | 25% head |
| Power P | P2 = P1 x (N2/N1)^3 | 12.5% power |

**VFD benefit:** Reducing flow to 50% by reducing pump speed saves 87.5% of pump power. This is the primary justification for VFD on variable-flow cooling loops.

### Redundancy Configurations

| Configuration | Description | When to Use |
|---------------|------------|-------------|
| Duty/Standby | Two pumps each at 100% capacity; one runs, one standby | Critical single-loop systems |
| N+1 | N duty pumps + 1 standby with lead-lag rotation | Multi-pump parallel systems |
| 2N | Fully redundant parallel systems | Highest criticality (Tier IV) |

**Switchover:** Flow switch or differential pressure switch triggers automatic switchover within seconds. Lead-lag rotation distributes wear.

Full pump curve analysis and VFD selection -- @references/pump-selection.md

---

## Safety Boundaries

### Pressure and Temperature Limits by Safety Class

| Parameter | Residential | Commercial | Data Center | Industrial |
|-----------|-------------|-----------|-------------|-----------|
| Max working pressure | 80 PSI | 150 PSI | 150 PSI | 300+ PSI (PE required) |
| Max supply temperature | 60C | 82C | 55C (server side) | 150C+ (PE required) |
| Leak containment | Drip pan | Sensor + shutoff | Sensor + shutoff + alarm | Engineered containment |
| Pressure testing | Visual inspection | Hydrostatic 1.5x MAWP | Hydrostatic 1.5x + leak-down | Per ASME B31 code section |
| Water hammer limit | Not calculated | 25 PSI spike max | 10 PSI spike max | Per surge analysis |

### Safety Warden Integration

This skill produces CalculationRecord objects with safety margin calculations. The Safety Warden reviews these and generates SafetyFinding entries:

| Condition | Severity | Domain | Action |
|-----------|---------|--------|--------|
| Calculated pressure > safety class max | blocking | pressure | Requires human review (PE) |
| Temperature > safety class max | critical | temperature | Flag for PE review |
| NPSH_available < NPSH_required | critical | pressure | Cavitation risk -- redesign suction |
| Missing leak detection (data-center class) | warning | containment | Recommend sensor installation |

Industrial and data-center class findings with severity='critical' or 'blocking' always require PE review before construction.

---

## Reference Documents

| Reference | When to Read | Coverage |
|-----------|-------------|----------|
| @references/pipe-sizing.md | Detailed Darcy-Weisbach derivation, Moody chart, Colebrook equation | Full pipe hydraulics theory |
| @references/ashrae-tc9-9.md | Full ASHRAE TC 9.9 water class specifications, CDU selection criteria | Data center cooling standards |
| @references/pump-selection.md | Pump curve analysis, NPSH calculation, VFD sizing, affinity laws | Pump engineering |

---
*Fluid Systems Skill v1.0.0 -- Physical Infrastructure Engineering Pack*
*Phase 435-01 | References: ASHRAE TC 9.9, ASME B31.9, HI (Hydraulic Institute)*
*All outputs require verification by a licensed Professional Engineer.*
