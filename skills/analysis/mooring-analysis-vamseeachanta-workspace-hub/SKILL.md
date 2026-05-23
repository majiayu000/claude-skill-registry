---
name: mooring-analysis
version: 1.0.0
description: Mooring system design, analysis, and assessment for floating offshore platforms
author: workspace-hub
category: subject-matter-expert
tags: [mooring, catenary, taut-mooring, offshore, fpso, station-keeping, api-rp-2sk, dnv]
platforms: [engineering]
---

# Mooring Analysis SME Skill

Comprehensive mooring system design and analysis expertise for floating offshore platforms including catenary, taut, and semi-taut configurations.

## When to Use This Skill

Use mooring analysis knowledge when:
- **Station-keeping design** - FPSO, semi-sub, SPAR mooring
- **Catenary analysis** - Static and dynamic behavior
- **Tension calculations** - Pretension, extreme loads
- **Fatigue assessment** - Mooring line fatigue life
- **Anchor design** - Holding capacity verification
- **Installation planning** - Pretension optimization

## Core Knowledge Areas

### 1. Mooring Types

**Catenary Mooring:**
```yaml
characteristics:
  restoring_force: "Weight of suspended line"
  typical_water_depth: "< 2000m"
  materials: ["chain", "wire", "combination"]
  advantages:
    - Simple and reliable
    - Well-proven technology
    - Good energy absorption
  disadvantages:
    - Large footprint
    - Heavy at great depths
```

**Taut Mooring:**
```yaml
characteristics:
  restoring_force: "Elastic elongation"
  typical_water_depth: "Any depth"
  materials: ["polyester", "steel wire"]
  advantages:
    - Small footprint
    - Suitable for ultra-deep water
    - Lower weight
  disadvantages:
    - Complex dynamics
    - Requires higher pretension
    - More sensitive to installation
```

### 2. Catenary Equations

**Basic Catenary:**
```python
import numpy as np

def catenary_profile(
    horizontal_tension: float,  # kN
    weight_per_length: float,   # kN/m
    length_on_seabed: float = 0  # m
) -> dict:
    """
    Calculate catenary mooring line profile.

    Catenary equations:
    - x = a * sinh(s/a)
    - z = a * (cosh(s/a) - 1)

    Where a = H/w (catenary parameter)

    Args:
        horizontal_tension: Horizontal tension at touchdown
        weight_per_length: Weight per unit length in water
        length_on_seabed: Length of line on seabed

    Returns:
        Catenary parameters
    """
    # Catenary parameter
    a = horizontal_tension / weight_per_length

    return {
        'catenary_parameter_m': a,
        'horizontal_tension_kN': horizontal_tension,
        'weight_per_length_kN_m': weight_per_length
    }

def catenary_suspended_length(
    water_depth: float,
    horizontal_distance: float,
    horizontal_tension: float,
    weight_per_length: float
) -> float:
    """
    Calculate suspended length of catenary line.

    Solve: z = a(cosh(x/a) - 1) for length s

    Args:
        water_depth: Water depth
        horizontal_distance: Horizontal distance to anchor
        horizontal_tension: Horizontal tension
        weight_per_length: Weight per length

    Returns:
        Suspended line length
    """
    from scipy.optimize import fsolve

    a = horizontal_tension / weight_per_length

    def equations(s):
        # Horizontal: x = a*sinh(s/a)
        # Vertical: z = a*(cosh(s/a) - 1)
        eq1 = a * np.sinh(s/a) - horizontal_distance
        eq2 = a * (np.cosh(s/a) - 1) - water_depth
        return [eq1, eq2]

    # Initial guess
    s0 = np.sqrt(horizontal_distance**2 + water_depth**2)

    # Solve
    solution = fsolve(equations, s0)[0]

    return solution

def catenary_top_tension(
    water_depth: float,
    horizontal_tension: float,
    weight_per_length: float
) -> float:
    """
    Calculate tension at top of catenary line.

    T_top = sqrt(H² + (w*z)²)

    Args:
        water_depth: Water depth
        horizontal_tension: Horizontal tension
        weight_per_length: Weight per length

    Returns:
        Top tension in kN
    """
    vertical_component = weight_per_length * water_depth
    T_top = np.sqrt(horizontal_tension**2 + vertical_component**2)

    return T_top
```

### 3. Mooring Line Components

**Chain:**
```python
def chain_properties(
    diameter: float,  # mm
    grade: str = "R4"
) -> dict:
    """
    Get chain properties.

    Args:
        diameter: Nominal chain diameter
        grade: Chain grade (R3, R4, R5)

    Returns:
        Chain properties
    """
    # Minimum Breaking Load (MBL) for studless chain
    # API RP 2SK Table 4-1
    grade_factors = {
        'R3': 0.0219,  # tonnes/mm²
        'R4': 0.0246,
        'R5': 0.0273
    }

    k = grade_factors.get(grade, 0.0246)
    MBL = k * diameter**2  # tonnes

    # Weight in air (approximate)
    weight_air = 0.0218 * diameter**2  # kg/m

    # Weight in water (steel in seawater)
    submerged_factor = (7.85 - 1.025) / 7.85  # Steel in seawater
    weight_water = weight_air * submerged_factor  # kg/m

    return {
        'diameter_mm': diameter,
        'grade': grade,
        'MBL_tonnes': MBL,
        'MBL_kN': MBL * 9.81,
        'weight_air_kg_m': weight_air,
        'weight_water_kg_m': weight_water
    }
```

**Wire Rope:**
```python
def wire_rope_properties(
    diameter: float,  # mm
    construction: str = "6x36"
) -> dict:
    """
    Get wire rope properties.

    Args:
        diameter: Wire rope diameter
        construction: Wire construction (6x36, 6x19, etc.)

    Returns:
        Wire properties
    """
    # Approximate MBL (6x36 IWRC)
    MBL = 0.0175 * diameter**2  # tonnes

    # Weight in air
    weight_air = 0.040 * diameter**2  # kg/m (steel core)

    # Weight in water
    submerged_factor = (7.85 - 1.025) / 7.85
    weight_water = weight_air * submerged_factor

    return {
        'diameter_mm': diameter,
        'construction': construction,
        'MBL_tonnes': MBL,
        'MBL_kN': MBL * 9.81,
        'weight_air_kg_m': weight_air,
        'weight_water_kg_m': weight_water
    }
```

**Polyester Rope:**
```python
def polyester_rope_properties(
    diameter: float,  # mm
    linear_density: float = None  # kg/m
) -> dict:
    """
    Get polyester rope properties.

    Args:
        diameter: Rope diameter
        linear_density: Mass per unit length (if known)

    Returns:
        Polyester properties
    """
    # Approximate MBL
    MBL = 0.0048 * diameter**2  # tonnes

    # Weight in air (if not provided)
    if linear_density is None:
        linear_density = 0.0045 * diameter**2  # kg/m

    # Weight in water (polyester is neutrally buoyant in seawater)
    # Specific gravity ~1.38, seawater ~1.025
    submerged_factor = (1.38 - 1.025) / 1.38
    weight_water = linear_density * submerged_factor

    # Axial stiffness (EA)
    EA = 850 * MBL  # kN (approximate)

    return {
        'diameter_mm': diameter,
        'MBL_tonnes': MBL,
        'MBL_kN': MBL * 9.81,
        'weight_air_kg_m': linear_density,
        'weight_water_kg_m': weight_water,
        'EA_kN': EA
    }
```

### 4. Design Standards and Criteria

**Safety Factors (API RP 2SK):**
```yaml
safety_factors:
  intact_condition:
    ULS:  # Ultimate Limit State
      permanent_mooring: 1.67
      temporary_mooring: 1.50
    ALS:  # Accidental Limit State
      permanent: 1.25
      temporary: 1.15

  damaged_condition:  # One line failed
    ULS:
      permanent: 1.40
      temporary: 1.25
    ALS:
      permanent: 1.15
      temporary: 1.05

  fatigue:
    design_factor: 10.0
```

**Design Load Cases:**
```yaml
load_cases:
  operating:
    return_period: "1 year"
    vessel_offset: "Normal operation"
    mooring_check: "Fatigue dominant"

  extreme:
    return_period: "100 year"
    vessel_offset: "Maximum excursion"
    mooring_check: "ULS"

  survival:
    return_period: "10,000 year"
    vessel_offset: "Survival condition"
    mooring_check: "ALS"

  damaged:
    condition: "One line failed"
    environment: "100 year"
    mooring_check: "Damaged ULS"
```

### 5. Installation and Pretensioning

**Pretension Optimization:**
```python
def calculate_pretension(
    water_depth: float,
    horizontal_distance: float,
    target_touchdown_tension: float,
    weight_per_length: float
) -> dict:
    """
    Calculate required pretension for target touchdown tension.

    Args:
        water_depth: Water depth
        horizontal_distance: Horizontal distance to anchor
        target_touchdown_tension: Desired horizontal tension at seabed
        weight_per_length: Line weight per length

    Returns:
        Required pretension
    """
    # Calculate catenary profile
    a = target_touchdown_tension / weight_per_length

    # Suspended length
    s = catenary_suspended_length(
        water_depth,
        horizontal_distance,
        target_touchdown_tension,
        weight_per_length
    )

    # Top tension
    vertical_load = weight_per_length * water_depth
    pretension = np.sqrt(target_touchdown_tension**2 + vertical_load**2)

    return {
        'pretension_kN': pretension,
        'touchdown_tension_kN': target_touchdown_tension,
        'suspended_length_m': s,
        'catenary_parameter_m': a
    }
```

### 6. Dynamic Analysis Considerations

**Low Frequency Motion:**
```python
def estimate_low_frequency_offset(
    mean_wave_drift: float,  # kN
    mooring_stiffness: float  # kN/m
) -> float:
    """
    Estimate vessel low-frequency offset.

    Simple static approximation:
    offset = Force / Stiffness

    Args:
        mean_wave_drift: Mean wave drift force
        mooring_stiffness: Total horizontal stiffness

    Returns:
        Offset in meters
    """
    return mean_wave_drift / mooring_stiffness

def calculate_mooring_stiffness(
    num_lines: int,
    pretension: float,  # kN per line
    fairlead_depth: float,
    weight_per_length: float,
    line_azimuth: list  # degrees for each line
) -> float:
    """
    Calculate total horizontal mooring stiffness.

    Args:
        num_lines: Number of mooring lines
        pretension: Pretension per line
        fairlead_depth: Depth of fairlead below waterline
        weight_per_length: Weight per unit length
        line_azimuth: Azimuth of each line

    Returns:
        Total horizontal stiffness in kN/m
    """
    # Simplified: K = (T/a) for catenary
    # where a = H/w
    stiffness_per_line = weight_per_length * pretension / fairlead_depth

    # Resolve in each direction
    total_stiffness = 0
    for azimuth in line_azimuth:
        # Component in surge direction
        component = stiffness_per_line * np.cos(np.radians(azimuth))
        total_stiffness += component

    return total_stiffness
```

## Practical Applications

### Application 1: FPSO 12-Line Mooring

```yaml
mooring_configuration:
  vessel: "FPSO"
  water_depth: 1500  # m
  number_of_lines: 12
  configuration: "3x4 spread"  # 3 bundles, 4 lines each

  line_composition:
    upper_chain:
      length: 500  # m
      diameter: 127  # mm
      grade: "R4"
    wire_rope:
      length: 1000  # m
      diameter: 120  # mm
      construction: "6x36 IWRC"
    lower_chain:
      length: 500  # m
      diameter: 127  # mm
      grade: "R4"

  pretension:
    target: 2000  # kN per line
    tolerance: "+/-10%"

  anchor:
    type: "drag_embedment"
    capacity: 5000  # kN
    safety_factor: 2.0
```

### Application 2: Mooring Integrity Check

```python
def mooring_integrity_check(
    tension: float,  # kN
    MBL: float,      # kN
    safety_factor: float
) -> dict:
    """
    Check mooring line integrity against criteria.

    Args:
        tension: Applied tension
        MBL: Minimum Breaking Load
        safety_factor: Required safety factor

    Returns:
        Check results
    """
    utilization = tension / (MBL / safety_factor)
    passed = utilization <= 1.0

    return {
        'tension_kN': tension,
        'MBL_kN': MBL,
        'allowable_tension_kN': MBL / safety_factor,
        'utilization': utilization,
        'passed': passed,
        'margin': (1.0 - utilization) * 100  # Percent
    }
```

## Key Design Steps

1. **Preliminary Sizing**
   - Water depth
   - Vessel offset limits
   - Environmental criteria

2. **Configuration Selection**
   - Number of lines
   - Line composition
   - Anchor type

3. **Static Analysis**
   - Catenary profile
   - Pretension
   - Touchdown loads

4. **Dynamic Analysis**
   - Vessel motions
   - Line tensions
   - Fatigue damage

5. **Integrity Assessment**
   - ULS/ALS checks
   - Fatigue life
   - Installation feasibility

## Resources

- **API RP 2SK**: Stationkeeping Systems
- **DNV-OS-E301**: Position Mooring
- **ISO 19901-7**: Stationkeeping Systems
- **OCIMF**: Mooring Equipment Guidelines

---

**Use this skill for all mooring system design and analysis in DigitalModel!**
