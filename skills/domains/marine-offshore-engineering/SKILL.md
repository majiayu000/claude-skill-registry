---
name: marine-offshore-engineering
version: 1.0.0
description: Marine and offshore engineering fundamentals for platform design, subsea systems, and regulatory compliance
author: workspace-hub
category: subject-matter-expert
tags: [marine-engineering, offshore, fpso, platforms, subsea, regulations, dnv, api]
platforms: [engineering]
---

# Marine and Offshore Engineering SME Skill

Comprehensive marine and offshore engineering knowledge for platform design, subsea systems, mooring, and regulatory compliance.

## When to Use This Skill

Use this SME knowledge when:
- **Platform design** - FPSOs, semi-submersibles, TLPs, SPARs
- **Subsea systems** - Templates, manifolds, pipelines, umbilicals
- **Marine operations** - Installation, commissioning, decommissioning
- **Regulatory compliance** - DNV, API, ISO standards
- **Environmental loading** - Wind, wave, current forces
- **Station-keeping** - Mooring and dynamic positioning

## Core Knowledge Areas

### 1. Platform Types

**Fixed Platforms:**
- **Jacket structures** - Steel lattice framework, common in shallow water (<150m)
- **Jack-ups** - Mobile platforms with retractable legs
- **Compliant towers** - Slender structures for deeper water (300-900m)

**Floating Platforms:**
- **Semi-submersibles** - Pontoons and columns, excellent motion characteristics
- **TLPs (Tension Leg Platforms)** - Vertically moored, minimal vertical motion
- **SPARs** - Deep draft cylindrical hull, good in ultra-deep water
- **FPSOs** - Converted/purpose-built tankers for production and storage

**Selection Criteria:**
```python
def select_platform_type(water_depth: float, field_life: float) -> str:
    """
    Platform type selection based on water depth.

    Args:
        water_depth: Water depth in meters
        field_life: Expected field life in years

    Returns:
        Recommended platform type
    """
    if water_depth < 150:
        return "Fixed platform (Jacket)"
    elif water_depth < 500:
        if field_life < 5:
            return "Jack-up (temporary)"
        else:
            return "Semi-submersible or FPSO"
    elif water_depth < 2000:
        return "Semi-submersible, SPAR, or FPSO"
    else:  # Ultra-deep water
        return "SPAR or FPSO"
```

### 2. Environmental Loading

**Wind Loading:**
- API RP 2A: V = V_1hr * (z/10)^(1/7)  # Wind profile
- Force: F = 0.5 * ρ * V² * Cd * A

**Wave Loading:**
- **Airy (Linear) Wave Theory** - Small amplitude waves
- **Stokes 2nd/3rd Order** - Finite amplitude
- **Stream Function** - Highly nonlinear waves

**Current Loading:**
```python
import numpy as np

def calculate_current_force(
    velocity: float,  # m/s
    diameter: float,   # m
    length: float,     # m
    cd: float = 1.2    # Drag coefficient
) -> float:
    """
    Calculate current force on cylinder.

    Morison equation: F = 0.5 * ρ * V² * Cd * D * L

    Args:
        velocity: Current velocity
        diameter: Member diameter
        length: Member length
        cd: Drag coefficient

    Returns:
        Force in kN
    """
    rho = 1025  # kg/m³ (seawater)
    F = 0.5 * rho * velocity**2 * cd * diameter * length
    return F / 1000  # Convert to kN
```

### 3. Mooring Systems

**Types:**
- **Catenary** - Chain/wire, relies on weight for restoring force
- **Taut** - Polyester/steel wire, high pretension
- **Semi-taut** - Hybrid configuration

**Design Standards:**
- API RP 2SK - Stationkeeping Systems
- DNV-OS-E301 - Position Mooring
- ISO 19901-7 - Stationkeeping Systems

**Safety Factors:**
```yaml
mooring_safety_factors:
  intact:
    uls: 1.67    # Ultimate Limit State
    als: 1.25    # Accidental Limit State
  damaged:
    uls: 1.25
    als: 1.05

  fatigue_design_factor: 10.0
```

### 4. Subsea Systems

**Components:**
- **Subsea trees** - Wellhead control
- **Manifolds** - Production gathering
- **Flowlines** - Fluid transport
- **Risers** - Platform connection
- **Umbilicals** - Control/power/chemical injection

**Pipeline Design:**
```python
def pipeline_wall_thickness(
    diameter: float,  # mm
    pressure: float,  # MPa
    yield_stress: float,  # MPa
    design_factor: float = 0.72  # API 5L
) -> float:
    """
    Calculate required pipeline wall thickness.

    Barlow's formula: t = P*D / (2*σ*F)

    Args:
        diameter: Outer diameter
        pressure: Design pressure
        yield_stress: Material yield stress
        design_factor: Design factor

    Returns:
        Wall thickness in mm
    """
    t = (pressure * diameter) / (2 * yield_stress * design_factor)

    # Add corrosion allowance
    corrosion_allowance = 3.0  # mm
    t_total = t + corrosion_allowance

    return t_total
```

### 5. Regulatory Framework

**Classification Societies:**
- **DNV** (Det Norske Veritas) - Norwegian
- **ABS** (American Bureau of Shipping) - American
- **Lloyd's Register** - British
- **Bureau Veritas** - French

**Key Standards:**
```yaml
standards:
  structural:
    - DNV-OS-C101: Design of Offshore Steel Structures
    - API RP 2A-WSD: Fixed Offshore Platforms
    - ISO 19902: Fixed Steel Structures

  floating:
    - DNV-OS-C103: Floating Structures
    - API RP 2FPS: Planning, Designing, Constructing Floating Production Systems

  mooring:
    - DNV-OS-E301: Position Mooring
    - API RP 2SK: Stationkeeping Systems
    - ISO 19901-7: Stationkeeping Systems

  subsea:
    - API 17D: Subsea Wellhead and Christmas Tree Equipment
    - API 17J: Unbonded Flexible Pipe
    - DNV-OS-F101: Submarine Pipeline Systems

  operations:
    - DNV-RP-H103: Modelling and Analysis of Marine Operations
    - ISO 19901-6: Marine Operations
```

### 6. Marine Operations

**Installation Methods:**
- **Heavy Lift** - Crane vessels for topsides
- **Float-over** - Deck floated over substructure
- **Pipelaying** - S-lay, J-lay, reel-lay methods

**Weather Windows:**
```python
def calculate_weather_window(
    sea_states: list,
    operation_limit: dict,
    duration_required: float  # hours
) -> list:
    """
    Identify suitable weather windows for marine operations.

    Args:
        sea_states: List of sea state forecasts
        operation_limit: Limits (Hs_max, Tp_range, current_max)
        duration_required: Required continuous calm period

    Returns:
        List of suitable time windows
    """
    windows = []
    current_window_start = None
    current_window_duration = 0

    for i, state in enumerate(sea_states):
        # Check if conditions are suitable
        suitable = (
            state['Hs'] <= operation_limit['Hs_max'] and
            state['current'] <= operation_limit['current_max']
        )

        if suitable:
            if current_window_start is None:
                current_window_start = i
            current_window_duration += state['time_step']

            # Check if window is long enough
            if current_window_duration >= duration_required:
                windows.append({
                    'start': current_window_start,
                    'duration': current_window_duration,
                    'conditions': 'suitable'
                })
        else:
            # Window ended
            current_window_start = None
            current_window_duration = 0

    return windows
```

## Practical Applications

### Application 1: FPSO Preliminary Design

```yaml
fpso_design:
  vessel:
    hull:
      type: "conversion"  # or "newbuild"
      length_pp: 320  # m
      beam: 58  # m
      depth: 32  # m
      draft_design: 22  # m

    capacity:
      oil_storage: 2000000  # barrels
      production: 100000  # bopd
      water_injection: 200000  # bwpd

  topsides:
    modules:
      - production_manifold
      - separation
      - gas_compression
      - water_injection
      - utilities
    weight: 25000  # tonnes

  mooring:
    type: "spread"
    lines: 12
    configuration: "3x4"  # 3 bundles, 4 lines each

  design_codes:
    - ABS MODU
    - API RP 2FPS
    - DNV-OS-C103
```

### Application 2: Environmental Load Calculation

```python
def calculate_total_environmental_load(
    vessel_data: dict,
    environment: dict
) -> dict:
    """
    Calculate combined wind, wave, and current loads.

    Args:
        vessel_data: Vessel dimensions and coefficients
        environment: Environmental parameters

    Returns:
        Total forces and moments
    """
    import numpy as np

    # Wind force
    rho_air = 1.225  # kg/m³
    V_wind = environment['wind_speed']
    A_projected = vessel_data['frontal_area']
    Cd_wind = vessel_data['wind_drag_coef']
    F_wind = 0.5 * rho_air * V_wind**2 * Cd_wind * A_projected / 1000  # kN

    # Wave drift force (simplified)
    rho_water = 1025  # kg/m³
    Hs = environment['wave_Hs']
    F_wave_drift = 0.5 * rho_water * 9.81 * Hs**2 * vessel_data['waterplane_area'] / 1000

    # Current force
    V_current = environment['current_speed']
    A_underwater = vessel_data['underwater_area']
    Cd_current = vessel_data['current_drag_coef']
    F_current = 0.5 * rho_water * V_current**2 * Cd_current * A_underwater / 1000

    # Total horizontal force
    theta_wind = np.radians(environment['wind_direction'])
    theta_wave = np.radians(environment['wave_direction'])
    theta_current = np.radians(environment['current_direction'])

    Fx = (F_wind * np.cos(theta_wind) +
          F_wave_drift * np.cos(theta_wave) +
          F_current * np.cos(theta_current))

    Fy = (F_wind * np.sin(theta_wind) +
          F_wave_drift * np.sin(theta_wave) +
          F_current * np.sin(theta_current))

    return {
        'Fx_kN': Fx,
        'Fy_kN': Fy,
        'F_total_kN': np.sqrt(Fx**2 + Fy**2),
        'direction_deg': np.degrees(np.arctan2(Fy, Fx))
    }
```

## Key Calculations

### 1. Buoyancy and Stability

```python
def calculate_metacentric_height(
    displacement: float,  # tonnes
    waterplane_area: float,  # m²
    center_of_buoyancy_height: float,  # m
    center_of_gravity_height: float  # m
) -> float:
    """
    Calculate metacentric height (GM) for stability.

    GM = KB + BM - KG

    Where:
    - KB = Center of buoyancy above keel
    - BM = Metacentric radius = I/V
    - KG = Center of gravity above keel

    Args:
        displacement: Vessel displacement
        waterplane_area: Area at waterline
        center_of_buoyancy_height: KB
        center_of_gravity_height: KG

    Returns:
        Metacentric height in meters
    """
    rho = 1.025  # t/m³
    volume = displacement / rho

    # Second moment of area (simplified for rectangular waterplane)
    I = waterplane_area**1.5 / 12  # Approximation

    # Metacentric radius
    BM = I / volume

    # Metacentric height
    GM = center_of_buoyancy_height + BM - center_of_gravity_height

    return GM
```

### 2. Riser Stress

```python
def calculate_riser_stress(
    top_tension: float,  # kN
    weight_per_length: float,  # kg/m
    water_depth: float,  # m
    diameter: float,  # mm
    wall_thickness: float  # mm
) -> dict:
    """
    Calculate riser stresses.

    Args:
        top_tension: Top tension
        weight_per_length: Riser weight in water
        water_depth: Water depth
        diameter: Outer diameter
        wall_thickness: Wall thickness

    Returns:
        Stress components
    """
    # Cross-sectional area
    D_outer = diameter / 1000  # Convert to m
    D_inner = D_outer - 2 * wall_thickness / 1000
    A = np.pi * (D_outer**2 - D_inner**2) / 4  # m²

    # Effective tension at bottom
    w = weight_per_length * 9.81 / 1000  # kN/m
    bottom_tension = top_tension - w * water_depth

    # Axial stress (top)
    sigma_axial_top = top_tension * 1000 / (A * 1e6)  # MPa

    # Axial stress (bottom)
    sigma_axial_bottom = bottom_tension * 1000 / (A * 1e6)  # MPa

    return {
        'top_stress_MPa': sigma_axial_top,
        'bottom_stress_MPa': sigma_axial_bottom,
        'bottom_tension_kN': bottom_tension
    }
```

## Design Process

### Typical Project Phases:

1. **Feasibility Study**
   - Concept selection
   - Preliminary sizing
   - Cost estimation

2. **FEED (Front End Engineering Design)**
   - Detailed concept
   - Specifications
   - Major equipment selection

3. **Detailed Engineering**
   - Construction drawings
   - Procurement
   - Fabrication specifications

4. **Fabrication & Installation**
   - Yard fabrication
   - Loadout and seafastening
   - Offshore installation

5. **Commissioning & Operations**
   - System testing
   - Production startup
   - Life of field operations

## Resources

- **DNV Standards**: https://www.dnv.com/
- **API Standards**: https://www.api.org/
- **ISO Standards**: https://www.iso.org/
- **NORSOK Standards**: https://www.standard.no/en/sectors/energi-og-klima/petroleum/norsok-standards/

---

**Use this skill for all marine and offshore engineering design decisions in DigitalModel!**
