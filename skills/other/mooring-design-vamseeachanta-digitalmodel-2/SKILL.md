---
name: mooring-design
description: Design and analyze mooring systems including CALM and SALM buoys, catenary
  moorings, and spread mooring configurations. Covers mooring line design, safety
  factors, environmental loading, and compliance with DNV, API, and ABS standards.
updated: '2026-01-07'
---
# Mooring Design Skill

Design and analyze mooring systems for floating offshore structures, including CALM buoys, SALM buoys, and spread mooring configurations.

## Version Metadata

```yaml
version: 1.0.0
python_min_version: '3.10'
dependencies:
  orcaflex-modeling: '>=2.0.0,<3.0.0'
  hydrodynamics: '>=1.0.0,<2.0.0'
orcaflex_version: '>=11.0'
compatibility:
  tested_python:
  - '3.10'
  - '3.11'
  - '3.12'
  - '3.13'
  os:
  - Windows
  - Linux
  - macOS
```

## Changelog

### [1.0.0] - 2026-01-07

**Added:**
- Initial version metadata and dependency management
- Semantic versioning support
- Compatibility information for Python 3.10-3.13

**Changed:**
- Enhanced skill documentation structure


## When to Use

- CALM (Catenary Anchor Leg Mooring) buoy design
- SALM (Single Anchor Leg Mooring) buoy analysis
- Spread mooring configuration design
- Mooring line sizing and material selection
- Environmental load calculations
- Safety factor verification
- Mooring analysis setup for OrcaFlex

## Mooring System Types

### CALM Buoy Systems
- Tanker mooring terminal
- Multi-point catenary anchor legs
- Weathervaning capability
- Typical 4-8 anchor legs

### SALM Buoy Systems
- Single anchor leg with swivel
- Weathervaning around single point
- Suitable for deep water
- Simpler installation

### Spread Mooring
- Fixed heading systems
- Multiple mooring lines (8-16 typical)
- Semi-submersible and FPSO applications
- Symmetric or asymmetric configurations

## Implementation Pattern

### Mooring System Configuration

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
import numpy as np
import logging

logger = logging.getLogger(__name__)


class MooringType(Enum):
    CALM = "calm"
    SALM = "salm"
    SPREAD = "spread"
    TURRET = "turret"


class LineType(Enum):
    CHAIN = "chain"
    WIRE = "wire"
    POLYESTER = "polyester"
    COMBINATION = "combination"


@dataclass
class MooringLineProperties:
    """Properties of a mooring line segment."""
    line_type: LineType
    length: float            # meters
    diameter: float          # mm
    mbl: float              # Minimum Breaking Load (kN)
    weight_water: float     # Weight in water (kg/m)
    ea: float               # Axial stiffness EA (kN)
    drag_coeff: float = 2.4 # Normal drag coefficient


@dataclass
class AnchorProperties:
    """Anchor properties."""
    anchor_type: str         # drag, suction, pile
    holding_capacity: float  # kN
    location: Tuple[float, float, float]  # (x, y, z) in meters


@dataclass
class MooringLine:
    """Complete mooring line configuration."""
    line_id: str
    segments: List[MooringLineProperties]
    anchor: AnchorProperties
    fairlead_location: Tuple[float, float, float]
    pretension: float = 0.0  # kN


@dataclass
class MooringSystem:
    """Complete mooring system configuration."""
    system_type: MooringType
    water_depth: float
    lines: List[MooringLine]
    vessel_type: str
    design_life_years: float = 20.0


@dataclass
class EnvironmentalConditions:
    """Environmental loading conditions."""
    wave_hs: float           # Significant wave height (m)
    wave_tp: float           # Peak period (s)
    wave_direction: float    # degrees from North
    current_speed: float     # m/s
    current_direction: float # degrees
    wind_speed: float        # m/s at 10m
    wind_direction: float    # degrees
    return_period: float = 100  # years
```

### Catenary Analysis

```python
class CatenaryAnalyzer:
    """Analyze catenary mooring line geometry and tensions."""

    def __init__(self, water_depth: float):
        self.water_depth = water_depth

    def solve_catenary(
        self,
        line: MooringLineProperties,
        horizontal_tension: float,
        touchdown_distance: float = None
    ) -> Dict:
        """
        Solve catenary equations for mooring line.

        Args:
            line: Line properties
            horizontal_tension: Horizontal tension at fairlead (kN)
            touchdown_distance: Distance to touchdown point (m)

        Returns:
            Dictionary with catenary geometry and tensions
        """
        w = line.weight_water * 9.81 / 1000  # kN/m
        H = horizontal_tension

        # Catenary parameter
        a = H / w

        # Calculate geometry
        # Vertical height from seabed
        z = self.water_depth

        # Arc length from touchdown to fairlead
        s = a * np.sinh(z / a) if z / a < 20 else a * np.exp(z / a) / 2

        # Horizontal distance from touchdown to fairlead
        x = a * np.arccosh(1 + z / a) if z / a < 20 else a * np.log(2 * z / a)

        # Tension at fairlead
        T_fairlead = np.sqrt(H**2 + (w * s)**2)

        # Tension at touchdown (vertical = 0)
        T_touchdown = H

        # Angle at fairlead
        angle_fairlead = np.degrees(np.arctan(w * s / H))

        return {
            'horizontal_tension': H,
            'fairlead_tension': T_fairlead,
            'touchdown_tension': T_touchdown,
            'arc_length': s,
            'horizontal_distance': x,
            'fairlead_angle': angle_fairlead,
            'catenary_parameter': a,
            'grounded_length': max(0, line.length - s)
        }

    def calculate_stiffness(
        self,
        line: MooringLineProperties,
        catenary_result: Dict
    ) -> float:
        """
        Calculate horizontal stiffness of mooring line.

        Args:
            line: Line properties
            catenary_result: Result from solve_catenary

        Returns:
            Horizontal stiffness (kN/m)
        """
        H = catenary_result['horizontal_tension']
        w = line.weight_water * 9.81 / 1000
        a = catenary_result['catenary_parameter']
        x = catenary_result['horizontal_distance']

        # Geometric stiffness
        k_geom = w * np.cosh(x / a) / np.sinh(x / a)**2

        # Elastic stiffness contribution
        s = catenary_result['arc_length']
        k_elastic = line.ea / s

        # Combined (series)
        k_total = 1 / (1/k_geom + 1/k_elastic) if k_elastic > 0 else k_geom

        return k_total
```

### Mooring Design Calculations

```python
@dataclass
class DesignLoadCase:
    """Design load case for mooring analysis."""
    name: str
    condition: str  # intact, damaged, transient
    environment: EnvironmentalConditions
    safety_factor_required: float


@dataclass
class MooringDesignResult:
    """Results from mooring design analysis."""
    line_id: str
    load_case: str
    max_tension: float        # kN
    min_mbl: float           # Required MBL (kN)
    safety_factor: float
    utilization: float
    passes: bool


class MooringDesigner:
    """Design and verify mooring systems."""

    # Safety factors per DNV-OS-E301
    SAFETY_FACTORS = {
        'intact': {
            'quasi-static': 2.0,
            'dynamic': 1.67
        },
        'damaged': {
            'quasi-static': 1.43,
            'dynamic': 1.25
        },
        'transient': {
            'quasi-static': 1.10,
            'dynamic': 1.05
        }
    }

    def __init__(self, system: MooringSystem):
        self.system = system
        self.analyzer = CatenaryAnalyzer(system.water_depth)

    def calculate_environmental_loads(
        self,
        vessel_data: Dict,
        environment: EnvironmentalConditions
    ) -> Dict:
        """
        Calculate environmental loads on vessel.

        Args:
            vessel_data: Vessel particulars
            environment: Environmental conditions

        Returns:
            Dictionary with load components
        """
        # Wave drift force (simplified)
        Lbp = vessel_data.get('length', 200)
        B = vessel_data.get('beam', 40)
        draft = vessel_data.get('draft', 15)

        # Mean wave drift (Newman approximation)
        Hs = environment.wave_hs
        rho = 1025  # kg/m³
        g = 9.81

        # Drift force coefficient (approximate)
        Cwd = 0.5
        F_wave_drift = Cwd * rho * g * Hs**2 * B / 2 / 1000  # kN

        # Current force
        Cd_current = 1.0
        A_current = Lbp * draft
        V_current = environment.current_speed
        F_current = 0.5 * rho * Cd_current * A_current * V_current**2 / 1000  # kN

        # Wind force
        rho_air = 1.225
        Cd_wind = 1.0
        A_wind = vessel_data.get('windage_area', 5000)  # m²
        V_wind = environment.wind_speed
        F_wind = 0.5 * rho_air * Cd_wind * A_wind * V_wind**2 / 1000  # kN

        return {
            'wave_drift': F_wave_drift,
            'current': F_current,
            'wind': F_wind,
            'total': F_wave_drift + F_current + F_wind
        }

    def analyze_intact_condition(
        self,
        vessel_offset: Tuple[float, float, float],
        environment: EnvironmentalConditions
    ) -> List[MooringDesignResult]:
        """
        Analyze mooring system in intact condition.

        Args:
            vessel_offset: Vessel offset (x, y, rotation)
            environment: Environmental conditions

        Returns:
            List of design results per line
        """
        results = []
        sf_required = self.SAFETY_FACTORS['intact']['dynamic']

        for line in self.system.lines:
            # Calculate line tension (simplified)
            # In practice, use OrcaFlex or similar
            fairlead = np.array(line.fairlead_location)
            anchor = np.array(line.anchor.location)

            # Apply vessel offset
            offset_x, offset_y, rotation = vessel_offset
            fairlead[0] += offset_x
            fairlead[1] += offset_y

            # Calculate horizontal distance
            h_dist = np.sqrt(
                (fairlead[0] - anchor[0])**2 +
                (fairlead[1] - anchor[1])**2
            )

            # Total line length
            total_length = sum(seg.length for seg in line.segments)

            # Estimate tension (catenary)
            main_segment = line.segments[0]
            catenary = self.analyzer.solve_catenary(
                main_segment,
                horizontal_tension=line.pretension
            )

            max_tension = catenary['fairlead_tension'] * 1.5  # Approximate dynamic factor

            # Calculate safety factor
            mbl = min(seg.mbl for seg in line.segments)
            sf_actual = mbl / max_tension if max_tension > 0 else float('inf')

            results.append(MooringDesignResult(
                line_id=line.line_id,
                load_case='intact',
                max_tension=max_tension,
                min_mbl=max_tension * sf_required,
                safety_factor=sf_actual,
                utilization=1 / sf_actual if sf_actual > 0 else 1.0,
                passes=sf_actual >= sf_required
            ))

        return results

    def analyze_damaged_condition(
        self,
        damaged_line_id: str,
        vessel_offset: Tuple[float, float, float],
        environment: EnvironmentalConditions
    ) -> List[MooringDesignResult]:
        """
        Analyze mooring system with one line failed.

        Args:
            damaged_line_id: ID of failed line
            vessel_offset: Vessel offset
            environment: Environmental conditions

        Returns:
            List of design results for remaining lines
        """
        results = []
        sf_required = self.SAFETY_FACTORS['damaged']['dynamic']

        remaining_lines = [l for l in self.system.lines if l.line_id != damaged_line_id]

        # Recalculate with increased loads on remaining lines
        load_increase_factor = len(self.system.lines) / len(remaining_lines)

        for line in remaining_lines:
            main_segment = line.segments[0]
            catenary = self.analyzer.solve_catenary(
                main_segment,
                horizontal_tension=line.pretension * load_increase_factor
            )

            max_tension = catenary['fairlead_tension'] * 1.5 * load_increase_factor

            mbl = min(seg.mbl for seg in line.segments)
            sf_actual = mbl / max_tension if max_tension > 0 else float('inf')

            results.append(MooringDesignResult(
                line_id=line.line_id,
                load_case=f'damaged_{damaged_line_id}',
                max_tension=max_tension,
                min_mbl=max_tension * sf_required,
                safety_factor=sf_actual,
                utilization=1 / sf_actual if sf_actual > 0 else 1.0,
                passes=sf_actual >= sf_required
            ))

        return results
```

### OrcaFlex Model Generator

```python
class OrcaFlexModelGenerator:
    """Generate OrcaFlex model files for mooring analysis."""

    def __init__(self, system: MooringSystem):
        self.system = system

    def generate_line_data(self, line: MooringLine) -> Dict:
        """Generate OrcaFlex line data for a mooring line."""
        line_data = {
            'Name': line.line_id,
            'LineType': [],
            'Length': [],
            'TargetSegmentLength': [],
            'EndAConnection': 'Fixed',
            'EndAX': line.anchor.location[0],
            'EndAY': line.anchor.location[1],
            'EndAZ': line.anchor.location[2],
            'EndBConnection': 'Vessel1',
            'EndBX': line.fairlead_location[0],
            'EndBY': line.fairlead_location[1],
            'EndBZ': line.fairlead_location[2],
        }

        # Add segments
        for i, seg in enumerate(line.segments):
            line_data['LineType'].append(self._get_line_type_name(seg))
            line_data['Length'].append(seg.length)
            line_data['TargetSegmentLength'].append(min(10, seg.length / 20))

        return line_data

    def _get_line_type_name(self, seg: MooringLineProperties) -> str:
        """Generate line type name."""
        return f"{seg.line_type.value}_{seg.diameter}mm"

    def generate_line_type(self, seg: MooringLineProperties) -> Dict:
        """Generate OrcaFlex line type definition."""
        return {
            'Name': self._get_line_type_name(seg),
            'Category': seg.line_type.value.capitalize(),
            'OD': seg.diameter / 1000,  # Convert to meters
            'MassPerUnitLength': seg.weight_water + 1025 * np.pi * (seg.diameter/2000)**2,
            'EA': seg.ea * 1000,  # Convert to N
            'EI': 0,  # Flexible line
            'NormalDragCoefficient': seg.drag_coeff,
            'AxialDragCoefficient': 0.1,
        }

    def generate_model_yml(self, output_path: str) -> str:
        """
        Generate YAML configuration for OrcaFlex model.

        Args:
            output_path: Path to save YAML file

        Returns:
            Path to generated file
        """
        import yaml

        model = {
            'General': {
                'WaterDepth': self.system.water_depth,
                'UnitsSystem': 'SI',
            },
            'Environment': {
                'WaterDensity': 1025,
                'KinematicViscosity': 1.19e-6,
            },
            'LineTypes': [],
            'Lines': [],
        }

        # Collect unique line types
        line_types_seen = set()
        for line in self.system.lines:
            for seg in line.segments:
                type_name = self._get_line_type_name(seg)
                if type_name not in line_types_seen:
                    model['LineTypes'].append(self.generate_line_type(seg))
                    line_types_seen.add(type_name)

        # Add lines
        for line in self.system.lines:
            model['Lines'].append(self.generate_line_data(line))

        with open(output_path, 'w') as f:
            yaml.dump(model, f, default_flow_style=False)

        return output_path
```

## YAML Configuration

```yaml
# config/mooring_design.yaml

system:
  type: calm
  water_depth: 100.0
  design_life_years: 20

vessel:
  type: tanker
  length: 280.0
  beam: 46.0
  draft: 17.5
  windage_area: 6000.0

mooring_pattern:
  n_lines: 6
  anchor_radius: 450.0
  first_line_heading: 30.0  # degrees

line_configuration:
  segments:
    - type: chain
      length: 400.0
      diameter: 84.0
      grade: R4
    - type: polyester
      length: 200.0
      diameter: 140.0

anchors:
  type: suction_pile
  capacity: 5000.0  # kN

environment:
  100_year:
    wave_hs: 8.5
    wave_tp: 12.5
    current_speed: 1.2
    wind_speed: 25.0

analysis:
  load_cases:
    - name: intact_100yr
      condition: intact
      environment: 100_year
    - name: damaged_100yr
      condition: damaged
      environment: 100_year
```

## Usage Examples

### Basic Design

```python
from mooring_design import (
    MooringSystem, MooringLine, MooringLineProperties,
    AnchorProperties, MooringType, LineType, MooringDesigner
)

# Define line segments
chain = MooringLineProperties(
    line_type=LineType.CHAIN,
    length=400.0,
    diameter=84.0,
    mbl=8500.0,
    weight_water=145.0,
    ea=850000.0
)

# Define anchor
anchor = AnchorProperties(
    anchor_type="suction",
    holding_capacity=5000.0,
    location=(400.0, 0.0, -100.0)
)

# Create mooring line
line1 = MooringLine(
    line_id="ML1",
    segments=[chain],
    anchor=anchor,
    fairlead_location=(20.0, 0.0, -10.0),
    pretension=500.0
)

# Create system
system = MooringSystem(
    system_type=MooringType.CALM,
    water_depth=100.0,
    lines=[line1],  # Add more lines
    vessel_type="tanker"
)

# Analyze
designer = MooringDesigner(system)
results = designer.analyze_intact_condition(
    vessel_offset=(10.0, 5.0, 5.0),
    environment=env
)

for result in results:
    print(f"{result.line_id}: SF={result.safety_factor:.2f} ({'PASS' if result.passes else 'FAIL'})")
```

### Generate OrcaFlex Model

```python
from mooring_design import OrcaFlexModelGenerator

generator = OrcaFlexModelGenerator(system)
generator.generate_model_yml('models/mooring_analysis.yml')
```

## Standards Reference

### DNV-OS-E301 (Position Mooring)
- Safety factors for ULS and ALS
- Line tension limits
- Fatigue requirements

### API RP 2SK (Station Keeping)
- Design criteria
- Environmental loads
- Analysis methods

### ABS (Position Mooring Systems)
- Material specifications
- Testing requirements
- Survey requirements

## Best Practices

### Design Principles
- Provide redundancy (n+1 or n+2 lines)
- Consider full range of environmental directions
- Account for manufacturing tolerances
- Include fatigue in line sizing

### Analysis Approach
- Perform quasi-static and dynamic analysis
- Check all intact and damaged conditions
- Verify anchor capacity
- Include VIM/VIV effects if applicable

### Documentation
- Document all assumptions
- Include environmental data sources
- Provide clear load case definitions
- Show safety factor compliance

## Related Skills

- [fatigue-analysis](../fatigue-analysis/SKILL.md) - Mooring line fatigue
- [structural-analysis](../structural-analysis/SKILL.md) - Buoy structure
- [engineering-report-generator](../../.claude/skills/development/engineering-report-generator/SKILL.md) - Analysis reports
