---
name: structural-analysis
description: Perform structural analysis including stress calculations, buckling checks,
  and capacity verification per DNV, API, and ISO standards. Covers Von Mises stress,
  plate buckling, member capacity, and safety factor reporting.
updated: '2026-01-07'
---
# Structural Analysis Skill

Perform structural analysis for offshore and marine structures including stress calculations, buckling checks, and capacity verification.

## Version Metadata

```yaml
version: 1.0.0
python_min_version: '3.10'
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

- Von Mises stress calculations
- Plate buckling checks (DNV, API standards)
- Member capacity verification
- Combined loading assessment
- Weld strength verification
- Safety factor reporting
- Standards compliance documentation

## Supported Standards

| Standard | Application |
|----------|-------------|
| **DNV-RP-C201** | Buckling strength of plated structures |
| **DNV-RP-C202** | Buckling strength of shells |
| **DNV-RP-C203** | Fatigue design |
| **API RP 2A** | Fixed offshore platforms |
| **ISO 19902** | Fixed steel offshore structures |
| **AISC 360** | Steel construction |
| **Eurocode 3** | Steel structures |

## Implementation Pattern

### Stress Calculations

```python
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import numpy as np
import logging

logger = logging.getLogger(__name__)


@dataclass
class StressState:
    """Complete stress state at a point."""
    sigma_x: float = 0.0    # Normal stress in x direction (MPa)
    sigma_y: float = 0.0    # Normal stress in y direction (MPa)
    sigma_z: float = 0.0    # Normal stress in z direction (MPa)
    tau_xy: float = 0.0     # Shear stress xy (MPa)
    tau_xz: float = 0.0     # Shear stress xz (MPa)
    tau_yz: float = 0.0     # Shear stress yz (MPa)

    def von_mises(self) -> float:
        """Calculate Von Mises equivalent stress."""
        return np.sqrt(
            0.5 * (
                (self.sigma_x - self.sigma_y)**2 +
                (self.sigma_y - self.sigma_z)**2 +
                (self.sigma_z - self.sigma_x)**2 +
                6 * (self.tau_xy**2 + self.tau_xz**2 + self.tau_yz**2)
            )
        )

    def principal_stresses(self) -> Tuple[float, float, float]:
        """Calculate principal stresses."""
        # Build stress tensor
        tensor = np.array([
            [self.sigma_x, self.tau_xy, self.tau_xz],
            [self.tau_xy, self.sigma_y, self.tau_yz],
            [self.tau_xz, self.tau_yz, self.sigma_z]
        ])

        # Eigenvalues are principal stresses
        eigenvalues = np.linalg.eigvalsh(tensor)
        return tuple(sorted(eigenvalues, reverse=True))

    def max_shear(self) -> float:
        """Calculate maximum shear stress."""
        s1, s2, s3 = self.principal_stresses()
        return (s1 - s3) / 2


@dataclass
class MaterialProperties:
    """Material properties for structural analysis."""
    yield_strength: float     # MPa
    ultimate_strength: float  # MPa
    youngs_modulus: float     # MPa
    poissons_ratio: float
    density: float            # kg/m³
    name: str = "Steel"


# Common materials
STEEL_S355 = MaterialProperties(
    yield_strength=355,
    ultimate_strength=510,
    youngs_modulus=210000,
    poissons_ratio=0.3,
    density=7850,
    name="S355"
)

STEEL_S420 = MaterialProperties(
    yield_strength=420,
    ultimate_strength=520,
    youngs_modulus=210000,
    poissons_ratio=0.3,
    density=7850,
    name="S420"
)


class StressCalculator:
    """Calculate stresses in structural members."""

    def __init__(self, material: MaterialProperties):
        self.material = material

    def beam_stress(
        self,
        axial_force: float,
        moment_y: float,
        moment_z: float,
        area: float,
        I_y: float,
        I_z: float,
        y: float,
        z: float
    ) -> float:
        """
        Calculate bending stress in a beam.

        Args:
            axial_force: Axial force (N)
            moment_y: Moment about y-axis (N·m)
            moment_z: Moment about z-axis (N·m)
            area: Cross-sectional area (m²)
            I_y: Moment of inertia about y (m⁴)
            I_z: Moment of inertia about z (m⁴)
            y: Distance from neutral axis in y (m)
            z: Distance from neutral axis in z (m)

        Returns:
            Normal stress (MPa)
        """
        sigma_axial = axial_force / area / 1e6  # Convert to MPa
        sigma_bending_y = moment_y * z / I_y / 1e6
        sigma_bending_z = moment_z * y / I_z / 1e6

        return sigma_axial + sigma_bending_y + sigma_bending_z

    def shear_stress(
        self,
        shear_force: float,
        Q: float,
        I: float,
        t: float
    ) -> float:
        """
        Calculate shear stress using VQ/It formula.

        Args:
            shear_force: Shear force (N)
            Q: First moment of area (m³)
            I: Moment of inertia (m⁴)
            t: Thickness at section (m)

        Returns:
            Shear stress (MPa)
        """
        return shear_force * Q / (I * t) / 1e6

    def torsional_stress(
        self,
        torque: float,
        r: float,
        J: float
    ) -> float:
        """
        Calculate torsional shear stress.

        Args:
            torque: Applied torque (N·m)
            r: Radial distance from center (m)
            J: Polar moment of inertia (m⁴)

        Returns:
            Shear stress (MPa)
        """
        return torque * r / J / 1e6

    def hoop_stress(
        self,
        pressure: float,
        radius: float,
        thickness: float
    ) -> float:
        """
        Calculate hoop stress in thin-walled cylinder.

        Args:
            pressure: Internal pressure (MPa)
            radius: Inner radius (m)
            thickness: Wall thickness (m)

        Returns:
            Hoop stress (MPa)
        """
        return pressure * radius / thickness

    def longitudinal_stress(
        self,
        pressure: float,
        radius: float,
        thickness: float
    ) -> float:
        """
        Calculate longitudinal stress in thin-walled cylinder.

        Args:
            pressure: Internal pressure (MPa)
            radius: Inner radius (m)
            thickness: Wall thickness (m)

        Returns:
            Longitudinal stress (MPa)
        """
        return pressure * radius / (2 * thickness)
```

### Buckling Analysis

```python
@dataclass
class PlateGeometry:
    """Plate geometry for buckling analysis."""
    length: float       # a (mm)
    width: float        # b (mm)
    thickness: float    # t (mm)


@dataclass
class BucklingResult:
    """Results from buckling analysis."""
    critical_stress: float    # MPa
    applied_stress: float     # MPa
    utilization: float
    safety_factor: float
    mode: str
    passes: bool


class PlateBucklingAnalyzer:
    """
    Plate buckling analysis per DNV-RP-C201.
    """

    def __init__(self, material: MaterialProperties):
        self.material = material
        self.E = material.youngs_modulus
        self.nu = material.poissons_ratio
        self.fy = material.yield_strength

    def elastic_buckling_stress(
        self,
        plate: PlateGeometry,
        boundary_conditions: str = "simply_supported"
    ) -> float:
        """
        Calculate elastic buckling stress.

        Args:
            plate: Plate geometry
            boundary_conditions: Boundary condition type

        Returns:
            Elastic buckling stress (MPa)
        """
        a = plate.length
        b = plate.width
        t = plate.thickness

        # Aspect ratio
        alpha = a / b

        # Buckling coefficient (simply supported, uniform compression)
        if alpha < 1:
            k = (alpha + 1/alpha)**2
        else:
            k = 4.0

        # Elastic buckling stress
        sigma_e = k * np.pi**2 * self.E / (12 * (1 - self.nu**2)) * (t / b)**2

        return sigma_e

    def reduced_slenderness(
        self,
        plate: PlateGeometry
    ) -> float:
        """
        Calculate reduced slenderness parameter.

        Args:
            plate: Plate geometry

        Returns:
            Reduced slenderness (lambda_p)
        """
        sigma_e = self.elastic_buckling_stress(plate)
        return np.sqrt(self.fy / sigma_e)

    def johnson_ostenfeld(
        self,
        sigma_e: float
    ) -> float:
        """
        Apply Johnson-Ostenfeld correction for inelastic buckling.

        Args:
            sigma_e: Elastic buckling stress

        Returns:
            Critical buckling stress
        """
        if sigma_e <= 0.5 * self.fy:
            return sigma_e
        else:
            return self.fy * (1 - self.fy / (4 * sigma_e))

    def check_plate_buckling(
        self,
        plate: PlateGeometry,
        sigma_x: float,
        sigma_y: float = 0.0,
        tau: float = 0.0,
        gamma_m: float = 1.15
    ) -> BucklingResult:
        """
        Check plate buckling under combined loading.

        Args:
            plate: Plate geometry
            sigma_x: Compressive stress in x (MPa, positive = compression)
            sigma_y: Compressive stress in y (MPa)
            tau: Shear stress (MPa)
            gamma_m: Material factor

        Returns:
            BucklingResult with utilization
        """
        # Calculate individual buckling stresses
        b = plate.width
        t = plate.thickness

        # Compressive buckling
        sigma_e_x = self.elastic_buckling_stress(plate)
        sigma_cr_x = self.johnson_ostenfeld(sigma_e_x)

        # Shear buckling
        k_tau = 5.34 + 4 * (b / plate.length)**2
        tau_e = k_tau * np.pi**2 * self.E / (12 * (1 - self.nu**2)) * (t / b)**2
        tau_cr = self.johnson_ostenfeld(tau_e)

        # Combined check (interaction formula)
        util_x = sigma_x / (sigma_cr_x / gamma_m) if sigma_cr_x > 0 else 0
        util_tau = (tau / (tau_cr / gamma_m))**2 if tau_cr > 0 else 0

        total_util = util_x + util_tau

        return BucklingResult(
            critical_stress=sigma_cr_x,
            applied_stress=sigma_x,
            utilization=total_util,
            safety_factor=1 / total_util if total_util > 0 else float('inf'),
            mode="plate_buckling",
            passes=total_util <= 1.0
        )


class ColumnBucklingAnalyzer:
    """
    Column buckling analysis per Eurocode 3.
    """

    def __init__(self, material: MaterialProperties):
        self.material = material
        self.E = material.youngs_modulus
        self.fy = material.yield_strength

    def euler_buckling_load(
        self,
        I: float,
        L_eff: float
    ) -> float:
        """
        Calculate Euler critical buckling load.

        Args:
            I: Moment of inertia (mm⁴)
            L_eff: Effective length (mm)

        Returns:
            Critical load (N)
        """
        return np.pi**2 * self.E * I / L_eff**2

    def slenderness_ratio(
        self,
        L_eff: float,
        r: float
    ) -> float:
        """
        Calculate slenderness ratio.

        Args:
            L_eff: Effective length (mm)
            r: Radius of gyration (mm)

        Returns:
            Slenderness ratio
        """
        return L_eff / r

    def reduction_factor(
        self,
        lambda_bar: float,
        buckling_curve: str = "b"
    ) -> float:
        """
        Calculate buckling reduction factor per EC3.

        Args:
            lambda_bar: Non-dimensional slenderness
            buckling_curve: EC3 buckling curve (a0, a, b, c, d)

        Returns:
            Reduction factor chi
        """
        # Imperfection factors
        alpha_dict = {
            "a0": 0.13,
            "a": 0.21,
            "b": 0.34,
            "c": 0.49,
            "d": 0.76
        }
        alpha = alpha_dict.get(buckling_curve, 0.34)

        # Calculate reduction factor
        phi = 0.5 * (1 + alpha * (lambda_bar - 0.2) + lambda_bar**2)
        chi = 1 / (phi + np.sqrt(phi**2 - lambda_bar**2))

        return min(chi, 1.0)

    def check_column_buckling(
        self,
        axial_force: float,
        area: float,
        I_min: float,
        L_eff: float,
        buckling_curve: str = "b",
        gamma_m: float = 1.0
    ) -> BucklingResult:
        """
        Check column buckling capacity.

        Args:
            axial_force: Applied axial force (N)
            area: Cross-sectional area (mm²)
            I_min: Minimum moment of inertia (mm⁴)
            L_eff: Effective length (mm)
            buckling_curve: EC3 curve
            gamma_m: Material factor

        Returns:
            BucklingResult
        """
        # Calculate slenderness
        r = np.sqrt(I_min / area)
        lambda_1 = np.pi * np.sqrt(self.E / self.fy)
        lambda_bar = (L_eff / r) / lambda_1

        # Get reduction factor
        chi = self.reduction_factor(lambda_bar, buckling_curve)

        # Design capacity
        N_cr = chi * area * self.fy / gamma_m

        # Utilization
        util = axial_force / N_cr if N_cr > 0 else float('inf')

        return BucklingResult(
            critical_stress=chi * self.fy / gamma_m,
            applied_stress=axial_force / area,
            utilization=util,
            safety_factor=1 / util if util > 0 else float('inf'),
            mode="column_buckling",
            passes=util <= 1.0
        )
```

### Capacity Verification

```python
@dataclass
class CapacityResult:
    """Results from capacity check."""
    capacity: float
    demand: float
    utilization: float
    governing_mode: str
    passes: bool
    details: Dict


class MemberCapacityChecker:
    """
    Check member capacity for combined loading.
    """

    def __init__(self, material: MaterialProperties):
        self.material = material
        self.stress_calc = StressCalculator(material)
        self.plate_buckling = PlateBucklingAnalyzer(material)
        self.column_buckling = ColumnBucklingAnalyzer(material)

    def check_tension_member(
        self,
        axial_force: float,
        area_gross: float,
        area_net: float,
        gamma_m0: float = 1.0,
        gamma_m2: float = 1.25
    ) -> CapacityResult:
        """
        Check tension capacity per EC3.

        Args:
            axial_force: Applied tension (N)
            area_gross: Gross area (mm²)
            area_net: Net area at connections (mm²)
            gamma_m0: Material factor (yield)
            gamma_m2: Material factor (ultimate)

        Returns:
            CapacityResult
        """
        # Plastic capacity
        N_pl = area_gross * self.material.yield_strength / gamma_m0

        # Ultimate capacity at net section
        N_u = 0.9 * area_net * self.material.ultimate_strength / gamma_m2

        # Governing capacity
        N_Rd = min(N_pl, N_u)
        governing = "plastic" if N_pl <= N_u else "net_section"

        util = axial_force / N_Rd if N_Rd > 0 else float('inf')

        return CapacityResult(
            capacity=N_Rd,
            demand=axial_force,
            utilization=util,
            governing_mode=governing,
            passes=util <= 1.0,
            details={'N_pl': N_pl, 'N_u': N_u}
        )

    def check_combined_loading(
        self,
        N: float,
        M_y: float,
        M_z: float,
        area: float,
        W_pl_y: float,
        W_pl_z: float,
        N_cr_y: float,
        N_cr_z: float,
        gamma_m1: float = 1.0
    ) -> CapacityResult:
        """
        Check member under combined axial and bending.

        Args:
            N: Axial force (N, positive = compression)
            M_y: Moment about y-axis (N·mm)
            M_z: Moment about z-axis (N·mm)
            area: Cross-sectional area (mm²)
            W_pl_y: Plastic section modulus y (mm³)
            W_pl_z: Plastic section modulus z (mm³)
            N_cr_y: Critical buckling load y (N)
            N_cr_z: Critical buckling load z (N)
            gamma_m1: Material factor

        Returns:
            CapacityResult
        """
        fy = self.material.yield_strength

        # Capacities
        N_Rk = area * fy
        M_y_Rk = W_pl_y * fy
        M_z_Rk = W_pl_z * fy

        # Reduction factors
        chi_y = N_cr_y / N_Rk if N_Rk > 0 else 1.0
        chi_z = N_cr_z / N_Rk if N_Rk > 0 else 1.0
        chi = min(chi_y, chi_z, 1.0)

        # Interaction check (simplified)
        util_N = N / (chi * N_Rk / gamma_m1) if N > 0 else 0
        util_My = M_y / (M_y_Rk / gamma_m1)
        util_Mz = M_z / (M_z_Rk / gamma_m1)

        # Combined utilization (simplified linear)
        util_combined = util_N + util_My + util_Mz

        return CapacityResult(
            capacity=chi * N_Rk / gamma_m1,
            demand=N,
            utilization=util_combined,
            governing_mode="combined",
            passes=util_combined <= 1.0,
            details={
                'util_N': util_N,
                'util_My': util_My,
                'util_Mz': util_Mz
            }
        )
```

## YAML Configuration

```yaml
# config/structural_analysis.yaml

material:
  name: S355
  yield_strength: 355  # MPa
  ultimate_strength: 510
  youngs_modulus: 210000
  poissons_ratio: 0.3

plates:
  - id: bottom_plate
    length: 2000
    width: 1000
    thickness: 20
    loading:
      sigma_x: 150
      sigma_y: 0
      tau: 30

  - id: side_plate
    length: 3000
    width: 1500
    thickness: 16
    loading:
      sigma_x: 200
      sigma_y: 50
      tau: 40

columns:
  - id: leg_1
    area: 15000  # mm²
    I_min: 5.0e7  # mm⁴
    L_eff: 8000  # mm
    buckling_curve: b
    axial_force: 2500000  # N

safety_factors:
  gamma_m0: 1.0
  gamma_m1: 1.0
  gamma_m2: 1.25

output:
  report_path: reports/structural_analysis.html
  include_plots: true
```

## Usage Examples

### Stress Analysis

```python
from structural_analysis import StressState, StressCalculator, STEEL_S355

# Create stress state
stress = StressState(
    sigma_x=150.0,
    sigma_y=50.0,
    tau_xy=30.0
)

# Calculate Von Mises
vm = stress.von_mises()
print(f"Von Mises stress: {vm:.1f} MPa")

# Check against yield
sf = STEEL_S355.yield_strength / vm
print(f"Safety factor: {sf:.2f}")
```

### Buckling Check

```python
from structural_analysis import (
    PlateBucklingAnalyzer, PlateGeometry, STEEL_S355
)

analyzer = PlateBucklingAnalyzer(STEEL_S355)

plate = PlateGeometry(
    length=2000,
    width=1000,
    thickness=20
)

result = analyzer.check_plate_buckling(
    plate=plate,
    sigma_x=150,
    tau=30,
    gamma_m=1.15
)

print(f"Utilization: {result.utilization:.2%}")
print(f"Status: {'PASS' if result.passes else 'FAIL'}")
```

### Combined Capacity Check

```python
from structural_analysis import MemberCapacityChecker, STEEL_S355

checker = MemberCapacityChecker(STEEL_S355)

result = checker.check_combined_loading(
    N=2500000,  # N
    M_y=500e6,  # N·mm
    M_z=200e6,  # N·mm
    area=15000,
    W_pl_y=2.5e6,
    W_pl_z=1.5e6,
    N_cr_y=8e6,
    N_cr_z=6e6
)

print(f"Combined utilization: {result.utilization:.2%}")
```

## Best Practices

### Analysis Approach
- Start with simple hand calculations
- Verify FEA results with analytical methods
- Check all load combinations
- Include manufacturing tolerances

### Safety Factors
- Use code-specified factors
- Document any deviations
- Consider consequence of failure
- Account for inspection limitations

### Documentation
- Clearly state assumptions
- Reference applicable standards
- Show detailed calculations
- Include sensitivity checks

## Related Skills

- [fatigue-analysis](../fatigue-analysis/SKILL.md) - Fatigue assessment
- [mooring-design](../mooring-design/SKILL.md) - Mooring structures
- [engineering-report-generator](../../.claude/skills/development/engineering-report-generator/SKILL.md) - Analysis reports
