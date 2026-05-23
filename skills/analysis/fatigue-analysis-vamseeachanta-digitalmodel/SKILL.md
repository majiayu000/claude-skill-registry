---
name: fatigue-analysis
description: Perform fatigue analysis using S-N curves and damage accumulation methods.
  Supports 221 S-N curves from 17 international standards (DNV, API, BS, ABS, etc.)
  for marine and offshore structural components.
updated: '2026-01-07'
---
# Fatigue Analysis Skill

Perform fatigue analysis for marine and offshore structural components using industry-standard S-N curves and damage accumulation methods.

## Version Metadata

```yaml
version: 1.0.0
python_min_version: '3.10'
dependencies:
  signal-analysis: '>=1.0.0,<2.0.0'
  structural-analysis: '>=1.0.0,<2.0.0'
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

- Fatigue life assessment of welded joints
- S-N curve selection from international standards
- Stress concentration factor application
- Damage accumulation using Palmgren-Miner rule
- Fatigue limit evaluation
- Comparison of different standards
- Generating fatigue analysis reports

## Supported Standards

### Available S-N Curves (221 total)

| Standard | Curves | Description |
|----------|--------|-------------|
| **DNV-RP-C203** | 45+ | Offshore steel structures |
| **API RP 2A** | 15+ | Offshore platforms |
| **BS 7608** | 20+ | Fatigue design of steel structures |
| **ABS** | 18+ | Marine vessel structures |
| **Eurocode 3** | 14 | Steel structures |
| **IIW** | 12+ | Welded joints |
| **ASME** | 10+ | Pressure vessels |
| **AWS D1.1** | 8+ | Structural welding |
| **AISC** | 5 | Steel construction |
| **ISO 19902** | 12+ | Fixed offshore structures |

## Core Concepts

### S-N Curve Equation

The basic S-N relationship:
```
N = a / S^m

Where:
- N = Number of cycles to failure
- S = Stress range
- a = Intercept parameter (log scale)
- m = Slope parameter (typically 3-5 for steel)
```

### Damage Accumulation (Miner's Rule)

```
D = Σ (ni / Ni)

Where:
- D = Accumulated damage (failure at D ≥ 1.0)
- ni = Number of cycles at stress level i
- Ni = Cycles to failure at stress level i (from S-N curve)
```

## Implementation Pattern

### S-N Curve Database

```python
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import numpy as np
import logging

logger = logging.getLogger(__name__)


@dataclass
class SNCurve:
    """S-N curve parameters."""
    name: str
    standard: str
    category: str
    log_a: float          # Intercept (log10 scale)
    m: float              # Slope
    log_a_2: Optional[float] = None  # Second slope intercept
    m_2: Optional[float] = None      # Second slope
    n_transition: float = 1e7        # Transition point
    fatigue_limit: Optional[float] = None  # Endurance limit
    t_ref: float = 25.0   # Reference thickness (mm)
    k: float = 0.0        # Thickness exponent
    environment: str = "air"  # air, seawater, cathodic

    def get_cycles_to_failure(
        self,
        stress_range: float,
        thickness: float = None
    ) -> float:
        """
        Calculate cycles to failure for given stress range.

        Args:
            stress_range: Stress range in MPa
            thickness: Actual thickness in mm (for thickness correction)

        Returns:
            Number of cycles to failure
        """
        # Apply thickness correction if needed
        if thickness and thickness > self.t_ref:
            stress_range = stress_range * (thickness / self.t_ref) ** self.k

        # Check fatigue limit
        if self.fatigue_limit and stress_range < self.fatigue_limit:
            return float('inf')

        # Single slope or bi-linear
        log_s = np.log10(stress_range)

        # Calculate N for first slope
        log_n = self.log_a - self.m * log_s

        # Check if bi-linear and past transition
        if self.log_a_2 and self.m_2:
            n_first = 10 ** log_n
            if n_first > self.n_transition:
                log_n = self.log_a_2 - self.m_2 * log_s

        return 10 ** log_n


class SNCurveDatabase:
    """Database of S-N curves from various standards."""

    def __init__(self):
        self.curves: Dict[str, SNCurve] = {}
        self._load_standard_curves()

    def _load_standard_curves(self):
        """Load standard S-N curves."""
        # DNV-RP-C203 curves (air)
        dnv_curves = [
            ("B1", 15.117, 4.0, 17.146, 5.0, "Base metal"),
            ("B2", 14.885, 4.0, 16.856, 5.0, "Base metal"),
            ("C", 13.640, 3.5, 16.081, 5.0, "Butt welds"),
            ("C1", 13.365, 3.5, 15.606, 5.0, "Butt welds"),
            ("C2", 13.091, 3.5, 15.132, 5.0, "Butt welds"),
            ("D", 12.592, 3.0, 15.606, 5.0, "Fillet welds"),
            ("E", 12.301, 3.0, 15.106, 5.0, "Fillet welds"),
            ("F", 12.049, 3.0, 14.656, 5.0, "Complex joints"),
            ("F1", 11.801, 3.0, 14.206, 5.0, "Complex joints"),
            ("F3", 11.546, 3.0, 13.756, 5.0, "Attachments"),
            ("G", 11.299, 3.0, 13.306, 5.0, "Attachments"),
            ("W1", 11.051, 3.0, 12.856, 5.0, "Tubular joints"),
            ("W2", 10.806, 3.0, 12.406, 5.0, "Tubular joints"),
            ("W3", 10.561, 3.0, 11.956, 5.0, "Tubular joints"),
            ("T", 12.164, 3.0, 15.606, 5.0, "Tubular T/Y"),
        ]

        for name, log_a, m, log_a_2, m_2, category in dnv_curves:
            curve_id = f"DNV_{name}"
            self.curves[curve_id] = SNCurve(
                name=name,
                standard="DNV-RP-C203",
                category=category,
                log_a=log_a,
                m=m,
                log_a_2=log_a_2,
                m_2=m_2,
                n_transition=1e7,
                t_ref=25.0,
                k=0.25,
                environment="air"
            )

        # API RP 2A curves
        api_curves = [
            ("X", 11.08, 3.74, "Tubular joints"),
            ("X'", 10.78, 3.74, "Weld root"),
        ]

        for name, log_a, m, category in api_curves:
            curve_id = f"API_{name}"
            self.curves[curve_id] = SNCurve(
                name=name,
                standard="API RP 2A",
                category=category,
                log_a=log_a,
                m=m,
                environment="air"
            )

    def get_curve(self, curve_id: str) -> SNCurve:
        """Get S-N curve by ID."""
        if curve_id not in self.curves:
            available = ', '.join(self.curves.keys())
            raise ValueError(f"Unknown curve: {curve_id}. Available: {available}")
        return self.curves[curve_id]

    def list_curves(self, standard: str = None) -> List[str]:
        """List available curve IDs, optionally filtered by standard."""
        if standard:
            return [k for k, v in self.curves.items() if v.standard == standard]
        return list(self.curves.keys())

    def get_by_category(self, category: str) -> List[SNCurve]:
        """Get curves matching a joint category."""
        return [v for v in self.curves.values() if category.lower() in v.category.lower()]
```

### Fatigue Calculator

```python
@dataclass
class StressBlock:
    """Stress range block for fatigue analysis."""
    stress_range: float  # MPa
    cycles: int          # Number of cycles


@dataclass
class FatigueResult:
    """Results of fatigue analysis."""
    total_damage: float
    fatigue_life_years: float
    design_life_years: float
    utilization: float
    damage_by_block: List[float]
    curve_used: str
    passes: bool

    def summary(self) -> str:
        """Generate summary string."""
        status = "PASS" if self.passes else "FAIL"
        return (
            f"Fatigue Analysis Result: {status}\n"
            f"  S-N Curve: {self.curve_used}\n"
            f"  Total Damage: {self.total_damage:.4f}\n"
            f"  Fatigue Life: {self.fatigue_life_years:.1f} years\n"
            f"  Design Life: {self.design_life_years:.1f} years\n"
            f"  Utilization: {self.utilization:.1%}"
        )


class FatigueCalculator:
    """Perform fatigue damage calculations."""

    def __init__(self, sn_database: SNCurveDatabase = None):
        self.db = sn_database or SNCurveDatabase()

    def calculate_damage(
        self,
        curve_id: str,
        stress_blocks: List[StressBlock],
        design_life_years: float = 25.0,
        scf: float = 1.0,
        thickness: float = None,
        dff: float = 1.0
    ) -> FatigueResult:
        """
        Calculate cumulative fatigue damage.

        Args:
            curve_id: S-N curve identifier
            stress_blocks: List of stress range blocks
            design_life_years: Design fatigue life
            scf: Stress concentration factor
            thickness: Actual thickness for thickness correction
            dff: Design fatigue factor (safety factor)

        Returns:
            FatigueResult with damage and life calculations
        """
        curve = self.db.get_curve(curve_id)

        total_damage = 0.0
        damage_by_block = []

        for block in stress_blocks:
            # Apply SCF
            effective_stress = block.stress_range * scf

            # Get cycles to failure
            n_failure = curve.get_cycles_to_failure(effective_stress, thickness)

            # Calculate damage for this block
            if n_failure == float('inf'):
                block_damage = 0.0
            else:
                block_damage = block.cycles / n_failure

            damage_by_block.append(block_damage)
            total_damage += block_damage

        # Apply design fatigue factor
        total_damage *= dff

        # Calculate life
        if total_damage > 0:
            fatigue_life_years = design_life_years / total_damage
        else:
            fatigue_life_years = float('inf')

        utilization = total_damage

        return FatigueResult(
            total_damage=total_damage,
            fatigue_life_years=fatigue_life_years,
            design_life_years=design_life_years,
            utilization=utilization,
            damage_by_block=damage_by_block,
            curve_used=curve_id,
            passes=total_damage <= 1.0
        )

    def compare_standards(
        self,
        curve_ids: List[str],
        stress_blocks: List[StressBlock],
        design_life_years: float = 25.0,
        scf: float = 1.0
    ) -> Dict[str, FatigueResult]:
        """Compare fatigue damage across different S-N curves."""
        results = {}
        for curve_id in curve_ids:
            try:
                results[curve_id] = self.calculate_damage(
                    curve_id=curve_id,
                    stress_blocks=stress_blocks,
                    design_life_years=design_life_years,
                    scf=scf
                )
            except ValueError as e:
                logger.warning(f"Skipping {curve_id}: {e}")
        return results
```

### Stress Spectrum Generator

```python
def generate_weibull_spectrum(
    n_blocks: int = 20,
    max_stress: float = 100.0,
    shape: float = 1.0,
    total_cycles: int = 1e7
) -> List[StressBlock]:
    """
    Generate stress spectrum using Weibull distribution.

    Args:
        n_blocks: Number of stress blocks
        max_stress: Maximum stress range (MPa)
        shape: Weibull shape parameter
        total_cycles: Total number of cycles

    Returns:
        List of StressBlock objects
    """
    blocks = []

    # Generate stress levels (evenly spaced)
    stress_levels = np.linspace(max_stress, max_stress * 0.1, n_blocks)

    # Calculate probability for each level (Weibull)
    scale = max_stress / (-np.log(1 - 0.632)) ** (1/shape)
    probabilities = np.exp(-(stress_levels / scale) ** shape)

    # Normalize to get cycle distribution
    prob_diff = np.diff(np.concatenate([[0], probabilities, [1]]))
    cycles_per_block = (prob_diff[:-1] * total_cycles).astype(int)

    for stress, cycles in zip(stress_levels, cycles_per_block):
        if cycles > 0:
            blocks.append(StressBlock(stress_range=stress, cycles=cycles))

    return blocks


def generate_rainflow_spectrum(
    time_history: np.ndarray,
    bin_edges: np.ndarray = None
) -> List[StressBlock]:
    """
    Generate stress spectrum from time history using rainflow counting.

    Args:
        time_history: Array of stress values over time
        bin_edges: Edges for binning stress ranges

    Returns:
        List of StressBlock objects
    """
    # Simple rainflow implementation
    # For production, use fatpack or similar library

    if bin_edges is None:
        max_range = np.ptp(time_history)
        bin_edges = np.linspace(0, max_range, 21)

    # Identify reversals (peaks and valleys)
    reversals = []
    for i in range(1, len(time_history) - 1):
        if ((time_history[i] > time_history[i-1] and
             time_history[i] > time_history[i+1]) or
            (time_history[i] < time_history[i-1] and
             time_history[i] < time_history[i+1])):
            reversals.append(time_history[i])

    # Count ranges (simplified 4-point algorithm)
    ranges = []
    i = 0
    while i < len(reversals) - 3:
        s1 = abs(reversals[i+1] - reversals[i])
        s2 = abs(reversals[i+2] - reversals[i+1])
        s3 = abs(reversals[i+3] - reversals[i+2])

        if s2 <= s1 and s2 <= s3:
            ranges.append(s2)
            del reversals[i+1:i+3]
        else:
            i += 1

    # Bin the ranges
    counts, _ = np.histogram(ranges, bins=bin_edges)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    blocks = []
    for stress, cycles in zip(bin_centers, counts):
        if cycles > 0:
            blocks.append(StressBlock(stress_range=stress, cycles=int(cycles)))

    return blocks
```

## YAML Configuration

```yaml
# config/fatigue_analysis.yaml

analysis:
  name: "Riser Girth Weld Fatigue"
  design_life_years: 25
  design_fatigue_factor: 3.0

joint:
  type: "girth_weld"
  sn_curve: "DNV_D"
  thickness_mm: 32.0
  scf: 1.25
  environment: "seawater_cp"

stress_spectrum:
  type: "weibull"
  max_stress_mpa: 150.0
  shape_parameter: 1.0
  total_cycles: 1.0e8

# Alternative: direct blocks
# stress_blocks:
#   - stress_range: 150.0
#     cycles: 1000
#   - stress_range: 100.0
#     cycles: 10000
#   - stress_range: 50.0
#     cycles: 100000

output:
  report_path: "reports/fatigue_analysis.html"
  include_comparison: true
  comparison_curves:
    - "DNV_D"
    - "DNV_E"
    - "API_X"
```

## Usage Examples

### Basic Analysis

```python
from fatigue_analysis import FatigueCalculator, StressBlock

calc = FatigueCalculator()

# Define stress spectrum
blocks = [
    StressBlock(stress_range=150.0, cycles=1000),
    StressBlock(stress_range=100.0, cycles=10000),
    StressBlock(stress_range=75.0, cycles=50000),
    StressBlock(stress_range=50.0, cycles=200000),
    StressBlock(stress_range=25.0, cycles=1000000),
]

# Calculate fatigue damage
result = calc.calculate_damage(
    curve_id="DNV_D",
    stress_blocks=blocks,
    design_life_years=25,
    scf=1.2,
    dff=3.0
)

print(result.summary())
```

### Compare Standards

```python
calc = FatigueCalculator()

# Compare across standards
results = calc.compare_standards(
    curve_ids=["DNV_D", "DNV_E", "API_X"],
    stress_blocks=blocks,
    design_life_years=25,
    scf=1.2
)

for curve_id, result in results.items():
    print(f"{curve_id}: Damage = {result.total_damage:.4f}")
```

### Generate Report

```python
from fatigue_analysis import FatigueCalculator
from engineering_report_generator import generate_report
import pandas as pd

# Run analysis
calc = FatigueCalculator()
result = calc.calculate_damage(...)

# Create data for visualization
df = pd.DataFrame({
    'Block': range(1, len(blocks) + 1),
    'Stress Range': [b.stress_range for b in blocks],
    'Cycles': [b.cycles for b in blocks],
    'Damage': result.damage_by_block
})

# Generate report
generate_report(
    df=df,
    output_path='reports/fatigue_report.html',
    title='Fatigue Analysis Report',
    sections={
        'summary': f'Total Damage: {result.total_damage:.4f}',
        'charts': [
            {'type': 'bar', 'x': 'Block', 'y': 'Damage', 'title': 'Damage by Block'},
            {'type': 'scatter', 'x': 'Stress Range', 'y': 'Cycles', 'title': 'S-N Spectrum'}
        ]
    }
)
```

## Best Practices

### S-N Curve Selection
- Select curves based on joint type and fabrication quality
- Consider environment (air, seawater, cathodic protection)
- Apply appropriate thickness corrections
- Use design curves (mean minus 2 standard deviations)

### Stress Analysis
- Include all stress concentration effects
- Consider mean stress correction if needed
- Account for multiaxial stresses
- Include weld misalignment effects

### Safety Factors
- DNV recommends DFF of 1.0 to 10.0 depending on consequence
- API uses single safety factor approach
- Consider inspection accessibility
- Account for consequences of failure

### Reporting
- Document S-N curve selection rationale
- Include stress spectrum derivation
- Show damage distribution
- Compare with alternative standards

## Related Skills

- [mooring-design](../mooring-design/SKILL.md) - Mooring system analysis
- [structural-analysis](../structural-analysis/SKILL.md) - Stress calculations
- [engineering-report-generator](../../.claude/skills/development/engineering-report-generator/SKILL.md) - Report generation
