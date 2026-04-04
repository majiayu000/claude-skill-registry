---
name: pie-thermal-engineering
version: 1.0.0
description: "Thermal engineering for infrastructure: heat transfer (conduction, convection, radiation), cooling load analysis for data centers, heat exchanger sizing via LMTD and e-NTU, PUE/TUE/WUE efficiency metrics, and airflow management patterns. Activates for thermal analysis, data center cooling design, heat exchanger sizing, efficiency calculations, and airflow management."
user-invocable: true
allowed-tools: Read Grep Glob Bash
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-26"
      triggers:
        intents:
          - "heat transfer"
          - "thermal"
          - "conduction"
          - "convection"
          - "radiation"
          - "cooling load"
          - "heat exchanger"
          - "LMTD"
          - "NTU"
          - "PUE"
          - "TUE"
          - "WUE"
          - "airflow"
          - "hot aisle"
          - "cold aisle"
          - "data center cooling"
          - "BTU"
        contexts:
          - "data center thermal analysis"
          - "infrastructure cooling design"
          - "thermal system optimization"
applies_to:
  - skills/physical-infrastructure/**
  - "*.calc"
---

# Thermal Engineering Skill

## At a Glance

Calculate heat transfer rates, size heat exchangers, and analyze data center thermal performance from component-level junction temperatures to facility-wide efficiency metrics.

**Activation:** InfrastructureRequest type='thermal', any heat exchanger sizing request, PUE/WUE calculation, airflow management design, or cooling load analysis.

**Key capabilities:**

- Three-mode heat transfer: conduction (Fourier), convection (Newton), radiation (Stefan-Boltzmann)
- Thermal resistance networks (series/parallel, analogous to electrical circuits)
- Data center cooling load breakdown (IT, UPS, lighting, fans, envelope)
- Heat exchanger sizing via LMTD and epsilon-NTU methods
- PUE/TUE/WUE/CUE efficiency metric calculations with target benchmarks
- Airflow management: hot/cold aisle containment, raised floor, economizer modes

**Integration:** Works in tandem with pie-fluid-systems: the fluid skill sizes cooling loop pipes and pumps; this skill quantifies the heat and determines exchanger performance.

> ENGINEERING DISCLAIMER: All calculations must be verified by a licensed Professional Engineer before use in construction or installation. HVAC and mechanical codes (ASHRAE 90.1, IMC) impose requirements not captured here. User assumes all responsibility for verification.

**Quick routing:** Heat transfer modes -- see Heat Transfer Fundamentals. Resistance networks -- see Thermal Resistance Networks. Data center loads -- see Data Center Cooling Load. Exchanger sizing -- see Heat Exchanger Sizing. PUE/WUE metrics -- see Efficiency Metrics. Airflow layout -- see Airflow Management.

---

## Heat Transfer Fundamentals

### Conduction -- Fourier's Law

Heat flow through a solid material by molecular vibration:

```
q = -k x A x (dT/dx)
```

| Variable | Definition | Units |
|----------|-----------|-------|
| q | Heat flow rate | W |
| k | Thermal conductivity | W/(m K) |
| A | Cross-sectional area perpendicular to heat flow | m^2 |
| dT/dx | Temperature gradient | K/m |

The negative sign indicates heat flows from hot to cold (opposite to the temperature gradient).

**Thermal resistance (conduction):** R_cond = L / (k x A), analogous to electrical resistance R = rho L / A.

**Thermal conductivity reference values:**

| Material | k (W/(m K)) | Application |
|----------|------------|-------------|
| Copper | 385 | Heat sinks, cold plates |
| Aluminum | 205 | Enclosures, fins, cold plates |
| Carbon steel | 50 | Structural, pressure piping |
| Stainless steel 304 | 16 | Corrosion-resistant piping |
| Concrete | 1.4 | Building structure |
| Gypsum board | 0.16 | Wall construction |
| Mineral wool | 0.04 | Pipe insulation |
| Polyurethane foam | 0.025 | Refrigeration insulation |
| Thermal paste (TIM) | 1-8 | CPU/GPU mounting |

### Convection -- Newton's Law of Cooling

Heat transfer between a surface and a moving fluid:

```
q = h x A x (T_surface - T_fluid)
```

| Variable | Definition | Units |
|----------|-----------|-------|
| q | Heat flow rate | W |
| h | Convective heat transfer coefficient | W/(m^2 K) |
| A | Surface area exposed to fluid | m^2 |

**Thermal resistance (convection):** R_conv = 1 / (h x A)

**Convective coefficient reference values:**

| Flow Type | Medium | h (W/(m^2 K)) |
|-----------|--------|---------------|
| Natural convection | Air | 5-25 |
| Forced convection | Air | 25-250 |
| Forced convection | Water (low velocity) | 500-2,000 |
| Forced convection | Water (high velocity) | 2,000-10,000 |
| Boiling | Water | 3,000-60,000 |
| Condensing | Steam | 5,000-100,000 |

For convection correlations (Nusselt number, Reynolds, Prandtl relationships) -- @references/heat-transfer.md

### Radiation -- Stefan-Boltzmann Law

Heat transfer by electromagnetic emission between surfaces:

```
q = epsilon x sigma x A x (T1^4 - T2^4)
```

| Variable | Definition | Units |
|----------|-----------|-------|
| epsilon | Surface emissivity (0 = perfect reflector, 1 = blackbody) | dimensionless |
| sigma | Stefan-Boltzmann constant = 5.67e-8 | W/(m^2 K^4) |
| T1, T2 | Surface temperatures | K (Kelvin only) |

**CRITICAL:** Temperatures MUST be in Kelvin for radiation calculations. K = C + 273.15.

**Emissivity reference values:**

| Surface | epsilon | Notes |
|---------|--------|-------|
| Blackbody (ideal) | 1.0 | Theoretical maximum |
| Painted steel | 0.9 | Most painted surfaces |
| Oxidized copper | 0.7 | Aged copper surfaces |
| Glass | 0.9 | Window and enclosure glass |
| Polished aluminum | 0.04 | Reflective radiation shield |
| Anodized aluminum | 0.8 | Common enclosure finish |

**When radiation matters:** High temperatures (>200C), large temperature differentials, or vacuum/low-pressure environments. Usually negligible for data center operating temperatures (15-55C); important for outdoor equipment and industrial processes.

---

## Thermal Resistance Networks

The thermal-electrical analogy maps heat transfer directly onto circuit analysis:

| Thermal Domain | Electrical Domain |
|---------------|-------------------|
| Heat flow q (W) | Current I (A) |
| Temperature difference DeltaT (K) | Voltage V (V) |
| Thermal resistance R (K/W) | Electrical resistance R (ohm) |

### Series Network (Heat Path Stack)

When heat flows through sequential layers, resistances add:

```
R_total = R1 + R2 + R3 + ...
q = (T_hot - T_cold) / R_total
```

**Example: server die to coolant path:**

```
R_total = R_die_spreading + R_TIM + R_cold_plate_wall + R_cold_plate_convection

R_die_spreading   = t_die / (k_silicon x A_die)
R_TIM             = t_TIM / (k_paste x A_contact)
R_cold_plate_wall = t_wall / (k_copper x A_plate)
R_cold_plate_conv = 1 / (h_coolant x A_internal)
```

Temperature rise check: DeltaT_junction = q x R_total. Verify T_junction < TjMax (typically 95-105C for modern CPUs/GPUs).

### Parallel Network (Multiple Heat Paths)

When heat has multiple simultaneous paths, resistances combine as parallels:

```
1/R_total = 1/R1 + 1/R2 + 1/R3
```

Use when heat splits between paths: fins parallel to base, combined air cooling + liquid cooling, multiple heat sinks on a shared substrate. The path with lowest resistance carries the most heat.

### Contact and Interface Resistance

Real surfaces have microscopic asperities -- actual contact area is only 1-2% of nominal area.

```
R_contact = 1 / (h_c x A)
```

**Thermal interface material (TIM) specific resistance:**

| TIM Type | R (K cm^2/W) | Application |
|----------|-------------|-------------|
| Bare metal contact | 0.5-5.0 | Avoid -- poor performance |
| Thermal grease | 0.1-0.5 | Standard CPU mounting |
| Phase-change pad | 0.05-0.2 | Factory-applied, consistent |
| Solder/braze | 0.02-0.1 | Permanent, best performance |

Reduce contact resistance by: smoother surfaces, higher clamping force, higher-conductivity TIM.

### Mathematical Connection

Heat flow against a temperature gradient follows the same mathematical structure as gradient descent in machine learning:

```
Heat:  q = -k nabla(T)                         (heat flows opposite to temperature gradient)
ML:    theta_n+1 = theta_n - alpha nabla(L)     (parameters move opposite to loss gradient)
```

Both describe movement opposing the direction of increasing potential. The temperature field T(x,y,z) in a data center is a scalar field whose gradient points from cold to hot. Heat flows against it. The student who has trained neural networks already understands the physics of heat conduction.

For thermal network examples and contact resistance data -- @references/heat-transfer.md

---

## Data Center Cooling Load

### Load Components

**IT equipment load** (dominant term, typically 60-80% of total):

```
Q_IT = sum(server_nameplate_TDP) x diversity_factor
     = rack_count x avg_density_kW x utilization
```

Diversity factor: 0.7-0.9 (servers rarely sustain nameplate power continuously). Maximum demand method (NEC 220.87 adapted): use measured 15-minute peak power x 1.25.

**Lighting:** 10-20 W/m^2 for LED (was 50 W/m^2 for fluorescent). All lighting converts to heat -- add to cooling load.

**UPS losses:** Heat generated by power conversion inefficiency:

| UPS Type | Loss at 50% Load | Loss at 100% Load |
|----------|------------------|-------------------|
| Online double-conversion (VRLA) | 4-6% | 2-3% |
| Online double-conversion (Li-ion) | 1.5-2% | 1-1.5% |
| Line-interactive | 2-4% | 1-2% |

**Fan and pump power:** CRAC/CRAH fan power typically 5-15% of served IT load; pump power <3% of IT load. Add to heat balance as these also convert to heat within the space.

**Envelope loads:** Usually <5% for well-insulated interior data halls. Include solar gain if windows or poorly insulated walls face direct sun. Q_envelope = U x A x CLTD (cooling load temperature difference; typically 5-15C for insulated walls).

### Total Cooling Load

```
Q_cooling = Q_IT x (1 + UPS_loss_fraction) + Q_lighting + Q_fans + Q_envelope
```

Add 15-20% safety margin for future expansion.

### Per-Rack Analysis

| Era/Type | Typical Density | Cooling Approach |
|----------|----------------|------------------|
| Legacy (2010s) | 5 kW/rack | Air cooling (raised floor CRAC/CRAH) |
| Modern enterprise | 10-15 kW/rack | Air cooling with in-row or rear-door units |
| High-performance | 15-30 kW/rack | Rear-door heat exchangers or in-row cooling |
| AI/GPU dense | 30-50+ kW/rack | Direct liquid cooling (DTC, CDU required) |
| Ultra-dense AI | 80-120+ kW/rack | Full immersion or multi-CDU per rack |

Cooling approach by density:
- < 10 kW/rack: air cooling (raised floor CRAC/CRAH sufficient)
- 10-30 kW/rack: rear-door heat exchangers or in-row cooling units
- > 30 kW/rack: direct liquid cooling (DTC) per ASHRAE TC 9.9 guidelines

---

## Heat Exchanger Sizing

### LMTD Method

Use when both inlet and outlet temperatures are known (rating existing equipment or fixed design conditions).

```
Q = U x A x F x LMTD
```

**Log Mean Temperature Difference:**

```
LMTD = (DeltaT1 - DeltaT2) / ln(DeltaT1 / DeltaT2)
```

For counterflow: DeltaT1 = T_h,in - T_c,out; DeltaT2 = T_h,out - T_c,in

For parallel flow: DeltaT1 = T_h,in - T_c,in; DeltaT2 = T_h,out - T_c,out

**F = LMTD correction factor:** F = 1.0 for pure counterflow (ideal). F = 0.7-0.95 for shell-and-tube and crossflow arrangements. If F < 0.75, consider adding shell passes or switching to counterflow.

**Required area:** A = Q / (U x F x LMTD)

**Typical overall heat transfer coefficient U:**

| Application | U (W/(m^2 K)) | Notes |
|-------------|--------------|-------|
| Water-to-water plate HX | 3,000-8,000 | Compact, high efficiency |
| CDU (server-side) | 1,000-3,000 | Data center cooling |
| Water-to-air coil | 30-300 | Depends on air velocity |
| Shell-and-tube (water) | 800-2,500 | Industrial standard |
| Finned tube (air-cooled) | 20-60 | Dry cooler, condenser |

### Epsilon-NTU Method

Preferred when only inlet temperatures and desired capacity are known (sizing new equipment).

**Effectiveness:**

```
epsilon = Q_actual / Q_max = Q_actual / (C_min x (T_h,in - T_c,in))
```

**Number of Transfer Units:**

```
NTU = U x A / C_min
```

**Heat capacity rates:**

```
C_hot  = m_dot_hot x Cp_hot    (W/K)
C_cold = m_dot_cold x Cp_cold  (W/K)
C_min  = min(C_hot, C_cold)
C_r    = C_min / C_max
```

**Epsilon-NTU relationships:**

| Flow Arrangement | Effectiveness Formula |
|-----------------|----------------------|
| Counterflow (Cr != 1) | epsilon = (1 - e^(-NTU(1-Cr))) / (1 - Cr x e^(-NTU(1-Cr))) |
| Counterflow (Cr = 1) | epsilon = NTU / (1 + NTU) |
| Parallel flow | epsilon = (1 - e^(-NTU(1+Cr))) / (1 + Cr) |
| Condenser/evaporator (Cr = 0) | epsilon = 1 - e^(-NTU) |

**Design process:** Choose target epsilon (typically 0.7-0.85), solve for NTU, then A = NTU x C_min / U.

**When to use each method:**
- LMTD: rating existing equipment or when both inlet AND outlet temperatures are specified
- Epsilon-NTU: sizing new equipment when only inlet temperatures and desired capacity are known

For LMTD correction factor charts and epsilon-NTU tables for all flow arrangements -- @references/heat-exchangers.md

---

## Efficiency Metrics

### PUE -- Power Usage Effectiveness

```
PUE = Total Facility Power / IT Equipment Power
```

Total includes: IT, UPS, cooling (chillers, pumps, fans, towers), lighting, power conditioning, security. Excludes non-data-center loads on the same meter.

**Measurement:** Annual average (preferred for reporting), not instantaneous. Use 15-minute interval samples for trending.

| PUE | Overhead | Typical Configuration |
|-----|----------|----------------------|
| 1.03 | 3% | Hyperscale, outdoor/direct air |
| 1.1 | 10% | Modern enterprise, water-side economizer |
| 1.2 | 20% | Typical new build, air-side economizer |
| 1.5 | 50% | Older facilities, legacy cooling |
| 2.0 | 100% | Very old/inefficient facilities |

### TUE -- Total Usage Effectiveness

```
TUE = IT Equipment Energy / (Total Energy - Energy Reused Externally)
```

Accounts for heat recovery: district heating, absorption chillers, aquifer thermal storage.

```
TUE = PUE x (1 - reuse_fraction)
```

If heat recovery reuses 25% of total energy and PUE = 1.3: TUE = 1.3 x 0.75 = 0.975. TUE < 1.0 is achievable when heat recovery is substantial. TUE <= PUE always; equality holds when no heat is reused.

### WUE -- Water Usage Effectiveness

```
WUE = Annual Site Water Usage (L) / Annual IT Equipment Energy (kWh)
```

Sources of water use: cooling tower evaporation (~90%), humidifiers, chiller heat rejection.

| WUE (L/kWh) | Rating | Notes |
|-------------|--------|-------|
| < 1.0 | World-class | Air-side economizer or dry cooling |
| 1.0-2.0 | Good | Moderate evaporative cooling |
| 2.0-3.0 | Average | Standard cooling tower operation |
| > 3.0 | Investigate | Excessive water consumption |

Trade-off: air-side economizer uses zero water; evaporative cooling uses more water but delivers lower PUE.

### CUE -- Carbon Usage Effectiveness

```
CUE = Annual Total CO2 Emissions (kg) / Annual IT Energy (kWh)
CUE = PUE x local_grid_carbon_intensity (kg CO2/kWh)
```

| Region | Grid Carbon Intensity (kg CO2/kWh) |
|--------|-----------------------------------|
| Norway (hydro) | 0.024 |
| France (nuclear) | 0.085 |
| EU average | 0.28 |
| US average | 0.39 |
| Coal-heavy grids | 0.82 |

Reduce CUE by: renewable energy procurement (PPAs, RECs), carbon-aware workload scheduling, on-site generation, heat recovery (reduces total energy via TUE).

For PUE measurement methodology (Green Grid Annex A), TUE derivation, and WUE water budget -- @references/dc-efficiency-metrics.md

---

## Airflow Management

### Hot/Cold Aisle Layout

Servers face into the cold aisle (front intakes aligned), exhaust into the hot aisle. This is the foundational airflow pattern for all air-cooled data centers.

- **Cold aisle supply:** 15-27C (ASHRAE A-class), delivered from raised floor tiles or overhead diffusers
- **Hot aisle return:** 35-45C, returned to CRAC/CRAH inlets -- never allow recirculation back to cold aisle
- **Row spacing:** cold aisles 4 ft (1.2 m) minimum, hot aisles 3 ft (0.9 m) minimum

### Containment Systems

| Type | Description | PUE Improvement | Preferred When |
|------|-------------|----------------|----------------|
| Cold aisle containment (CAC) | Physical barriers + ceiling panels enclose cold aisle | 0.1-0.2 PUE reduction | Easier retrofit to existing hall |
| Hot aisle containment (HAC) | Physical barriers enclose hot aisle; ducts to CRAC return | 0.15-0.25 PUE reduction | New build; highest efficiency |
| Full containment | Both CAC + HAC | 0.2-0.3 PUE reduction | New high-density builds |

CAC captures supply air; HAC captures exhaust air. HAC is generally preferred for new builds because it prevents hot air mixing with the room and allows higher CRAC supply temperatures.

### Raised Floor Airflow

- **Plenum height:** 12 inches minimum, 18-24 inches recommended for high-density deployments
- **Perforated tiles:** 150-500 CFM per tile at 0.05 inches water gauge plenum pressure
- **Tile placement rules:** cold aisle only; no tiles in hot aisles or under power/network equipment
- **Blanking panels:** fill ALL empty rack U-spaces to prevent hot air recirculation -- highest ROI single action for thermal management
- **Cable management:** route cables to avoid blocking plenum airflow; use overhead trays where possible

### Economizer Modes

| Mode | Mechanism | Water Use | Best Climate |
|------|-----------|-----------|-------------|
| Air-side (direct) | Outdoor air when T_outdoor < T_supply setpoint | Zero | Cool/dry climates |
| Water-side (indirect) | Cooling tower free cooling when T_wetbulb allows | Moderate | Temperate climates |
| Evaporative (adiabatic) | Pre-cool supply air via evaporation | High | Hot/dry climates |

Air-side economizer requires air filtration and humidity control. Water-side economizer avoids contamination risk by keeping outdoor air outside. Evaporative saves compressor energy but increases WUE.

---

## Reference Documents

| Reference | When to Read | Coverage |
|-----------|-------------|----------|
| @references/heat-transfer.md | Convection correlations, radiation view factors, contact resistance | Deep heat transfer theory |
| @references/heat-exchangers.md | LMTD F-factor charts, epsilon-NTU tables, fouling factors, U values | Heat exchanger engineering |
| @references/dc-efficiency-metrics.md | PUE measurement protocol, TUE derivation, WUE water budget | Data center KPI methodology |

---
*Thermal Engineering Skill v1.0.0 -- Physical Infrastructure Engineering Pack*
*Phase 435-02 | References: ASHRAE 90.1, ASHRAE TC 9.9, Green Grid WP#32, ASHRAE Fundamentals 2021*
*All outputs require verification by a licensed Professional Engineer.*
