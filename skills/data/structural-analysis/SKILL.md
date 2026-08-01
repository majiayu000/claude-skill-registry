---
name: structural-analysis
description: 'name: structural-analysis'
---

# Structural Analysis Skill

```yaml
name: structural-analysis
version: 1.0.0
category: sme
tags: [structural, mechanics, dnv, buckling, uls, als, beam-theory, stress-analysis]
created: 2026-01-06
updated: 2026-01-06
author: Claude
description: |
  Expert structural analysis for marine and offshore structures including
  beam theory, buckling, ULS/ALS limit state checks, and DNV standards.
  Covers tubular members, stiffened panels, and combined loading scenarios.
```

## When to Use This Skill

Use this skill when you need to:
- Perform structural analysis of marine structures
- Check ULS (Ultimate Limit State) and ALS (Accidental Limit State) criteria
- Analyze buckling of columns, beams, and stiffened panels
- Calculate section properties and stress distributions
- Apply DNV structural design standards
- Evaluate combined loading (axial + bending + torsion)
- Design tubular members and jacket structures
- Perform fatigue analysis integration with structural checks

## Core Knowledge Areas

### 1. Beam Theory and Section Properties

Calculate section properties for structural members:

```python
import numpy as np
from dataclasses import dataclass
from typing import Tuple

@dataclass
class SectionProperties:
    """Section properties for structural analysis."""
    area: float  # Cross-sectional area [m²]
    Ix: float  # Second moment of area about x-axis [m⁴]
    Iy: float  # Second moment of area about y-axis [m⁴]
    J: float  # Torsional constant [m⁴]
    Zx: float  # Section modulus about x-axis [m³]
    Zy: float  # Section modulus about y-axis [m³]
    rx: float  # Radius of gyration about x-axis [m]
    ry: float  # Radius of gyration about y-axis [m]

def circular_tube_properties(
    outer_diameter: float,
    wall_thickness: float
) -> SectionProperties:
    """
    Calculate section properties for circular tube.

    Args:
        outer_diameter: Outer diameter [m]
        wall_thickness: Wall thickness [m]

    Returns:
        Section properties

    Example:
        >>> props = circular_tube_properties(D=0.914, t=0.030)
        >>> print(f"Area: {props.area:.4f} m²")
        >>> print(f"Ix: {props.Ix:.6f} m⁴")
    """
    D = outer_diameter
    t = wall_thickness
    d = D - 2 * t  # Inner diameter

    # Cross-sectional area
    A = np.pi / 4 * (D**2 - d**2)

    # Second moments of area (circular symmetry: Ix = Iy)
    I = np.pi / 64 * (D**4 - d**4)

    # Torsional constant (polar moment)
    J = np.pi / 32 * (D**4 - d**4)

    # Section modulus
    Z = I / (D / 2)

    # Radius of gyration
    r = np.sqrt(I / A)

    return SectionProperties(
        area=A,
        Ix=I,
        Iy=I,
        J=J,
        Zx=Z,
        Zy=Z,
        rx=r,
        ry=r
    )

def rectangular_tube_properties(
    width: float,
    height: float,
    wall_thickness: float
) -> SectionProperties:
    """
    Calculate section properties for rectangular hollow section.

    Args:
        width: Outer width [m]
        height: Outer height [m]
        wall_thickness: Wall thickness [m]

    Returns:
        Section properties
    """
    b = width
    h = height
    t = wall_thickness

    # Inner dimensions
    bi = b - 2 * t
    hi = h - 2 * t

    # Cross-sectional area
    A = b * h - bi * hi

    # Second moments of area
    Ix = (b * h**3 - bi * hi**3) / 12
    Iy = (h * b**3 - hi * bi**3) / 12

    # Approximate torsional constant for thin-walled section
    # J ≈ 2·t·(b-t)²·(h-t)² / (b+h-2t) for t << b,h
    J = 2 * t * (b - t)**2 * (h - t)**2 / (b + h - 2 * t)

    # Section moduli
    Zx = 2 * Ix / h
    Zy = 2 * Iy / b

    # Radii of gyration
    rx = np.sqrt(Ix / A)
    ry = np.sqrt(Iy / A)

    return SectionProperties(
        area=A,
        Ix=Ix,
        Iy=Iy,
        J=J,
        Zx=Zx,
        Zy=Zy,
        rx=rx,
        ry=ry
    )

def i_beam_properties(
    flange_width: float,
    web_height: float,
    flange_thickness: float,
    web_thickness: float
) -> SectionProperties:
    """
    Calculate section properties for I-beam/H-beam.

    Args:
        flange_width: Flange width [m]
        web_height: Web height (total height - 2×flange thickness) [m]
        flange_thickness: Flange thickness [m]
        web_thickness: Web thickness [m]

    Returns:
        Section properties
    """
    bf = flange_width
    hw = web_height
    tf = flange_thickness
    tw = web_thickness
    h_total = hw + 2 * tf

    # Cross-sectional area
    A = 2 * bf * tf + hw * tw

    # Second moment about x-axis (strong axis)
    Ix = (bf * h_total**3 - (bf - tw) * hw**3) / 12

    # Second moment about y-axis (weak axis)
    Iy = (2 * tf * bf**3 + hw * tw**3) / 12

    # Approximate torsional constant
    # J ≈ Σ(b·t³/3) for thin-walled open sections
    J = (2 * bf * tf**3 + hw * tw**3) / 3

    # Section moduli
    Zx = 2 * Ix / h_total
    Zy = 2 * Iy / bf

    # Radii of gyration
    rx = np.sqrt(Ix / A)
    ry = np.sqrt(Iy / A)

    return SectionProperties(
        area=A,
        Ix=Ix,
        Iy=Iy,
        J=J,
        Zx=Zx,
        Zy=Zy,
        rx=rx,
        ry=ry
    )
```

### 2. Stress Analysis

Calculate stresses under combined loading:

```python
@dataclass
class LoadCase:
    """Loading case for structural member."""
    axial_force: float  # Axial force [N] (tension positive)
    bending_moment_x: float  # Bending moment about x-axis [N·m]
    bending_moment_y: float  # Bending moment about y-axis [N·m]
    shear_force_x: float  # Shear force in x-direction [N]
    shear_force_y: float  # Shear force in y-direction [N]
    torsional_moment: float  # Torsional moment [N·m]

def calculate_stresses(
    load: LoadCase,
    section: SectionProperties,
    distance_x: float = None,
    distance_y: float = None
) -> dict:
    """
    Calculate stresses at a point in the cross-section.

    Args:
        load: Load case
        section: Section properties
        distance_x: Distance from neutral axis in x-direction [m]
        distance_y: Distance from neutral axis in y-direction [m]

    Returns:
        Dictionary with stress components [Pa]

    Example:
        >>> load = LoadCase(
        ...     axial_force=1000e3,
        ...     bending_moment_x=500e3,
        ...     bending_moment_y=0,
        ...     shear_force_x=0,
        ...     shear_force_y=100e3,
        ...     torsional_moment=50e3
        ... )
        >>> section = circular_tube_properties(0.914, 0.030)
        >>> stresses = calculate_stresses(load, section, 0, 0.457)
        >>> print(f"Axial stress: {stresses['axial']/1e6:.1f} MPa")
    """
    # Axial stress: σ_axial = N/A
    sigma_axial = load.axial_force / section.area

    # Bending stress: σ_bending = M·y/I
    if distance_y is not None:
        sigma_bending_x = load.bending_moment_x * distance_y / section.Ix
    else:
        # Maximum bending stress at extreme fiber
        sigma_bending_x = abs(load.bending_moment_x) / section.Zx

    if distance_x is not None:
        sigma_bending_y = load.bending_moment_y * distance_x / section.Iy
    else:
        sigma_bending_y = abs(load.bending_moment_y) / section.Zy

    # Total normal stress
    sigma_total = sigma_axial + sigma_bending_x + sigma_bending_y

    # Shear stress from torsion: τ = T·r/J
    if distance_x is not None and distance_y is not None:
        r = np.sqrt(distance_x**2 + distance_y**2)
        tau_torsion = load.torsional_moment * r / section.J
    else:
        # Maximum torsional shear stress at outer fiber
        # For circular tube: r = D/2
        # Approximate for other sections
        tau_torsion = load.torsional_moment / (section.J / np.sqrt(section.rx**2 + section.ry**2))

    # Shear stress from transverse loads (approximate)
    # For rectangular sections: τ_avg = V/A
    tau_shear_x = load.shear_force_x / section.area
    tau_shear_y = load.shear_force_y / section.area

    # Total shear stress (vectorial sum)
    tau_total = np.sqrt((tau_torsion + tau_shear_x)**2 + tau_shear_y**2)

    # Von Mises equivalent stress
    sigma_vm = np.sqrt(sigma_total**2 + 3 * tau_total**2)

    return {
        'axial': sigma_axial,
        'bending_x': sigma_bending_x,
        'bending_y': sigma_bending_y,
        'normal_total': sigma_total,
        'shear_torsion': tau_torsion,
        'shear_transverse_x': tau_shear_x,
        'shear_transverse_y': tau_shear_y,
        'shear_total': tau_total,
        'von_mises': sigma_vm
    }

def calculate_principal_stresses(
    sigma_x: float,
    sigma_y: float,
    tau_xy: float
) -> Tuple[float, float, float]:
    """
    Calculate principal stresses and maximum shear stress.

    Args:
        sigma_x: Normal stress in x-direction [Pa]
        sigma_y: Normal stress in y-direction [Pa]
        tau_xy: Shear stress [Pa]

    Returns:
        Tuple of (sigma_1, sigma_2, tau_max) [Pa]

    Example:
        >>> sigma_1, sigma_2, tau_max = calculate_principal_stresses(
        ...     sigma_x=100e6, sigma_y=-50e6, tau_xy=30e6
        ... )
        >>> print(f"σ₁ = {sigma_1/1e6:.1f} MPa")
        >>> print(f"σ₂ = {sigma_2/1e6:.1f} MPa")
        >>> print(f"τ_max = {tau_max/1e6:.1f} MPa")
    """
    # Center of Mohr's circle
    sigma_avg = (sigma_x + sigma_y) / 2

    # Radius of Mohr's circle
    R = np.sqrt(((sigma_x - sigma_y) / 2)**2 + tau_xy**2)

    # Principal stresses
    sigma_1 = sigma_avg + R  # Maximum principal stress
    sigma_2 = sigma_avg - R  # Minimum principal stress

    # Maximum shear stress
    tau_max = R

    return sigma_1, sigma_2, tau_max
```

### 3. Column Buckling Analysis

Euler buckling and DNV buckling checks:

```python
def euler_buckling_load(
    E: float,
    I: float,
    L: float,
    K: float = 1.0
) -> float:
    """
    Calculate Euler critical buckling load.

    Args:
        E: Young's modulus [Pa]
        I: Second moment of area [m⁴]
        L: Column length [m]
        K: Effective length factor (1.0 = pinned-pinned)
            K = 0.5 (fixed-fixed)
            K = 0.7 (fixed-pinned)
            K = 1.0 (pinned-pinned)
            K = 2.0 (fixed-free)

    Returns:
        Critical buckling load [N]

    Example:
        >>> E_steel = 210e9  # Pa
        >>> section = circular_tube_properties(0.914, 0.030)
        >>> L = 30.0  # m
        >>> P_cr = euler_buckling_load(E_steel, section.Ix, L, K=1.0)
        >>> print(f"Critical load: {P_cr/1e6:.1f} MN")
    """
    # Effective length
    Le = K * L

    # Euler critical load: P_cr = π²EI/Le²
    P_cr = np.pi**2 * E * I / Le**2

    return P_cr

def slenderness_ratio(
    L: float,
    r: float,
    K: float = 1.0
) -> float:
    """
    Calculate slenderness ratio.

    Args:
        L: Column length [m]
        r: Radius of gyration [m]
        K: Effective length factor

    Returns:
        Slenderness ratio λ (dimensionless)
    """
    Le = K * L
    lambda_ratio = Le / r
    return lambda_ratio

def dnv_column_buckling_check(
    axial_force: float,
    E: float,
    fy: float,
    A: float,
    I: float,
    L: float,
    K: float = 1.0,
    gamma_M: float = 1.15
) -> dict:
    """
    DNV column buckling check (DNV-OS-C101, DNV-RP-C201).

    Args:
        axial_force: Applied axial force [N] (compression positive)
        E: Young's modulus [Pa]
        fy: Yield strength [Pa]
        A: Cross-sectional area [m²]
        I: Second moment of area [m⁴]
        L: Column length [m]
        K: Effective length factor
        gamma_M: Material safety factor (1.15 for ULS)

    Returns:
        Dictionary with buckling check results

    Example:
        >>> result = dnv_column_buckling_check(
        ...     axial_force=5000e3,
        ...     E=210e9,
        ...     fy=355e6,
        ...     A=0.082,
        ...     I=0.0135,
        ...     L=30.0,
        ...     K=1.0
        ... )
        >>> print(f"Unity check: {result['unity_check']:.3f}")
        >>> print(f"Status: {result['status']}")
    """
    Le = K * L
    r = np.sqrt(I / A)
    lambda_ratio = Le / r

    # Reduced slenderness ratio
    lambda_bar = lambda_ratio * np.sqrt(fy / E) / np.pi

    # Buckling reduction factor (European column curves)
    # Using curve 'a' for welded tubular sections
    alpha = 0.21  # Imperfection factor for curve 'a'
    phi = 0.5 * (1 + alpha * (lambda_bar - 0.2) + lambda_bar**2)
    chi = min(1.0, 1 / (phi + np.sqrt(phi**2 - lambda_bar**2)))

    # Design buckling resistance
    N_b_Rd = chi * A * fy / gamma_M

    # Unity check
    unity_check = axial_force / N_b_Rd

    # Critical buckling load (Euler)
    P_cr = np.pi**2 * E * I / Le**2

    status = "PASS" if unity_check <= 1.0 else "FAIL"

    return {
        'slenderness_ratio': lambda_ratio,
        'reduced_slenderness': lambda_bar,
        'buckling_reduction_factor': chi,
        'design_resistance': N_b_Rd,
        'applied_force': axial_force,
        'unity_check': unity_check,
        'critical_load_euler': P_cr,
        'status': status
    }
```

### 4. Beam Bending and Deflection

```python
def simply_supported_beam_deflection(
    load_type: str,
    E: float,
    I: float,
    L: float,
    load_magnitude: float,
    x: float = None
) -> dict:
    """
    Calculate deflection for simply supported beam.

    Args:
        load_type: 'point_center', 'uniform', 'point_arbitrary'
        E: Young's modulus [Pa]
        I: Second moment of area [m⁴]
        L: Beam length [m]
        load_magnitude: Load magnitude [N] or [N/m]
        x: Position along beam [m] (for arbitrary point load)

    Returns:
        Dictionary with max deflection and location

    Example:
        >>> result = simply_supported_beam_deflection(
        ...     load_type='uniform',
        ...     E=210e9,
        ...     I=0.0135,
        ...     L=30.0,
        ...     load_magnitude=10e3  # 10 kN/m
        ... )
        >>> print(f"Max deflection: {result['max_deflection']*1000:.1f} mm")
    """
    if load_type == 'point_center':
        # Point load at center: δ_max = PL³/(48EI)
        P = load_magnitude
        delta_max = P * L**3 / (48 * E * I)
        x_max = L / 2

    elif load_type == 'uniform':
        # Uniformly distributed load: δ_max = 5wL⁴/(384EI)
        w = load_magnitude
        delta_max = 5 * w * L**4 / (384 * E * I)
        x_max = L / 2

    elif load_type == 'point_arbitrary' and x is not None:
        # Point load at distance 'a' from left support
        # δ_max at x = sqrt(L² - a²)/sqrt(3) (approximate)
        P = load_magnitude
        a = x
        b = L - a
        # Maximum deflection (at x position)
        delta_at_a = P * a**2 * b**2 / (3 * E * I * L)
        delta_max = delta_at_a
        x_max = a
    else:
        raise ValueError(f"Unknown load_type: {load_type}")

    # Allowable deflection (L/360 for general structures)
    delta_allowable = L / 360

    unity_check = delta_max / delta_allowable
    status = "PASS" if unity_check <= 1.0 else "FAIL"

    return {
        'max_deflection': delta_max,
        'location': x_max,
        'allowable_deflection': delta_allowable,
        'unity_check': unity_check,
        'status': status
    }

def cantilever_beam_deflection(
    load_type: str,
    E: float,
    I: float,
    L: float,
    load_magnitude: float
) -> dict:
    """
    Calculate deflection for cantilever beam (fixed at one end).

    Args:
        load_type: 'point_end', 'uniform'
        E: Young's modulus [Pa]
        I: Second moment of area [m⁴]
        L: Beam length [m]
        load_magnitude: Load magnitude [N] or [N/m]

    Returns:
        Dictionary with max deflection
    """
    if load_type == 'point_end':
        # Point load at free end: δ_max = PL³/(3EI)
        P = load_magnitude
        delta_max = P * L**3 / (3 * E * I)

    elif load_type == 'uniform':
        # Uniformly distributed load: δ_max = wL⁴/(8EI)
        w = load_magnitude
        delta_max = w * L**4 / (8 * E * I)
    else:
        raise ValueError(f"Unknown load_type: {load_type}")

    # Allowable deflection (L/180 for cantilever)
    delta_allowable = L / 180

    unity_check = delta_max / delta_allowable
    status = "PASS" if unity_check <= 1.0 else "FAIL"

    return {
        'max_deflection': delta_max,
        'allowable_deflection': delta_allowable,
        'unity_check': unity_check,
        'status': status
    }
```

### 5. Tubular Joint Design (DNV)

```python
def tubular_joint_capacity_check(
    chord_diameter: float,
    chord_thickness: float,
    brace_diameter: float,
    brace_thickness: float,
    brace_angle: float,
    fy_chord: float,
    fy_brace: float,
    axial_load: float = 0,
    in_plane_bending: float = 0,
    out_plane_bending: float = 0,
    joint_type: str = 'T'
) -> dict:
    """
    Tubular joint capacity check per DNV-RP-C203.

    Args:
        chord_diameter: Chord outer diameter [m]
        chord_thickness: Chord wall thickness [m]
        brace_diameter: Brace outer diameter [m]
        brace_thickness: Brace wall thickness [m]
        brace_angle: Angle between brace and chord [degrees]
        fy_chord: Chord yield strength [Pa]
        fy_brace: Brace yield strength [Pa]
        axial_load: Axial load in brace [N]
        in_plane_bending: In-plane bending moment [N·m]
        out_plane_bending: Out-of-plane bending moment [N·m]
        joint_type: 'T', 'Y', 'K', 'X'

    Returns:
        Dictionary with joint capacity check

    Example:
        >>> result = tubular_joint_capacity_check(
        ...     chord_diameter=1.5,
        ...     chord_thickness=0.050,
        ...     brace_diameter=0.914,
        ...     brace_thickness=0.030,
        ...     brace_angle=90,
        ...     fy_chord=355e6,
        ...     fy_brace=355e6,
        ...     axial_load=2000e3,
        ...     in_plane_bending=500e3,
        ...     out_plane_bending=0,
        ...     joint_type='T'
        ... )
        >>> print(f"Unity check: {result['unity_check']:.3f}")
    """
    D = chord_diameter
    T = chord_thickness
    d = brace_diameter
    t = brace_thickness
    theta = np.radians(brace_angle)

    # Geometric parameters
    beta = d / D  # Diameter ratio
    gamma = D / (2 * T)  # Chord slenderness
    tau = t / T  # Thickness ratio

    # Validity range checks
    validity_checks = {
        'beta_range': 0.2 <= beta <= 1.0,
        'gamma_range': 10 <= gamma <= 50,
        'theta_range': np.degrees(theta) >= 30
    }

    if not all(validity_checks.values()):
        warnings = [k for k, v in validity_checks.items() if not v]
        print(f"Warning: Out of validity range: {warnings}")

    # Chord stress function (simplified - depends on chord loading)
    # Typically need to account for chord utilization
    Qf = 1.0  # Assume no chord pre-stress for simplicity

    # Strength function depends on joint type and loading
    if joint_type == 'T' or joint_type == 'Y':
        # Axial capacity
        if axial_load >= 0:  # Tension
            # Tension capacity
            Qu = 5.2 * gamma**(-0.2) * beta**0.5 * (1 + beta)**(-0.9) * Qf
        else:  # Compression
            # Compression capacity (punching shear)
            Qu = (2.8 + 14.2 * beta**2) * gamma**(-0.9) * Qf / np.sin(theta)

        # Nominal capacity
        N_capacity = Qu * fy_chord * T**2 / np.sin(theta)

        # In-plane bending capacity
        Qf_ipb = 1.3 * gamma**(-0.4) * beta**0.2 * Qf
        M_ipb_capacity = Qf_ipb * fy_chord * T**2 * d / np.sin(theta)

        # Out-of-plane bending capacity
        Qf_opb = 1.3 * gamma**(-0.4) * beta**0.2 * Qf
        M_opb_capacity = Qf_opb * fy_chord * T**2 * d

    else:
        raise NotImplementedError(f"Joint type {joint_type} not implemented")

    # Interaction check
    # DNV uses: (N/N_cap)^p + (M_ipb/M_ipb_cap)^p + (M_opb/M_opb_cap)^p ≤ 1
    # where p typically = 1.0 or 2.0
    p = 2.0

    unity_check = (
        (abs(axial_load) / N_capacity)**p +
        (abs(in_plane_bending) / M_ipb_capacity)**p +
        (abs(out_plane_bending) / M_opb_capacity)**p
    )**(1/p)

    status = "PASS" if unity_check <= 1.0 else "FAIL"

    return {
        'beta': beta,
        'gamma': gamma,
        'tau': tau,
        'axial_capacity': N_capacity,
        'ipb_capacity': M_ipb_capacity,
        'opb_capacity': M_opb_capacity,
        'applied_axial': axial_load,
        'applied_ipb': in_plane_bending,
        'applied_opb': out_plane_bending,
        'unity_check': unity_check,
        'status': status,
        'validity_checks': validity_checks
    }
```

### 6. ULS and ALS Limit State Checks

```python
def uls_combined_loading_check(
    axial_force: float,
    bending_moment_y: float,
    bending_moment_z: float,
    fy: float,
    section: SectionProperties,
    gamma_M: float = 1.15,
    load_factors: dict = None
) -> dict:
    """
    Ultimate Limit State (ULS) check for combined loading per DNV.

    Args:
        axial_force: Axial force [N] (tension positive)
        bending_moment_y: Bending moment about y-axis [N·m]
        bending_moment_z: Bending moment about z-axis [N·m]
        fy: Yield strength [Pa]
        section: Section properties
        gamma_M: Material safety factor (1.15 for ULS)
        load_factors: Dictionary with partial safety factors

    Returns:
        Dictionary with ULS check results

    Example:
        >>> section = circular_tube_properties(0.914, 0.030)
        >>> result = uls_combined_loading_check(
        ...     axial_force=-5000e3,  # Compression
        ...     bending_moment_y=1200e3,
        ...     bending_moment_z=0,
        ...     fy=355e6,
        ...     section=section
        ... )
        >>> print(f"Unity check: {result['unity_check']:.3f}")
    """
    if load_factors is None:
        # Default DNV load factors for ULS
        load_factors = {
            'axial': 1.3,
            'bending': 1.3
        }

    # Apply load factors
    Sd_axial = abs(axial_force) * load_factors['axial']
    Sd_My = abs(bending_moment_y) * load_factors['bending']
    Sd_Mz = abs(bending_moment_z) * load_factors['bending']

    # Design resistances
    N_Rd = section.area * fy / gamma_M
    My_Rd = section.Zy * fy / gamma_M
    Mz_Rd = section.Zx * fy / gamma_M

    # Interaction check (DNV-OS-C101)
    # For members with axial force and bending:
    # N/N_Rd + My/My_Rd + Mz/Mz_Rd ≤ 1.0 (conservative linear interaction)
    # More accurate: (N/N_Rd)^α + (My/My_Rd + Mz/Mz_Rd)^β ≤ 1.0

    # Conservative linear interaction
    unity_check_linear = (
        Sd_axial / N_Rd +
        Sd_My / My_Rd +
        Sd_Mz / Mz_Rd
    )

    # Eurocode interaction formula (more accurate)
    # For Class 1 and 2 cross-sections
    alpha = 2.0
    beta = 1.0
    unity_check_eurocode = (Sd_axial / N_Rd)**alpha + (
        (Sd_My / My_Rd + Sd_Mz / Mz_Rd)**beta
    )

    # Use conservative check
    unity_check = max(unity_check_linear, unity_check_eurocode)

    status = "PASS" if unity_check <= 1.0 else "FAIL"

    # Calculate utilization ratios
    utilization = {
        'axial': Sd_axial / N_Rd,
        'bending_y': Sd_My / My_Rd,
        'bending_z': Sd_Mz / Mz_Rd
    }

    return {
        'design_axial_force': Sd_axial,
        'design_moment_y': Sd_My,
        'design_moment_z': Sd_Mz,
        'axial_resistance': N_Rd,
        'moment_resistance_y': My_Rd,
        'moment_resistance_z': Mz_Rd,
        'unity_check_linear': unity_check_linear,
        'unity_check_eurocode': unity_check_eurocode,
        'unity_check': unity_check,
        'utilization': utilization,
        'status': status
    }

def als_dented_pipe_check(
    D: float,
    t: float,
    dent_depth: float,
    internal_pressure: float,
    fy: float,
    safety_factor: float = 1.0
) -> dict:
    """
    Accidental Limit State (ALS) check for dented pipe per DNV-RP-F110.

    Args:
        D: Outer diameter [m]
        t: Wall thickness [m]
        dent_depth: Dent depth [m]
        internal_pressure: Internal pressure [Pa]
        fy: Yield strength [Pa]
        safety_factor: Safety factor for ALS (typically 1.0)

    Returns:
        Dictionary with ALS check for dented pipe

    Example:
        >>> result = als_dented_pipe_check(
        ...     D=0.660,
        ...     t=0.020,
        ...     dent_depth=0.030,
        ...     internal_pressure=15e6,
        ...     fy=450e6
        ... )
        >>> print(f"Status: {result['status']}")
    """
    # Dent depth ratio
    delta_ratio = dent_depth / D

    # DNV acceptance criteria for dented pipes
    # For dent depth < 6% D: acceptable for continued operation
    # For 6% < dent depth < 20% D: engineering assessment required
    # For dent depth > 20% D: repair or replacement required

    if delta_ratio < 0.06:
        category = "Acceptable"
    elif delta_ratio < 0.20:
        category = "Engineering Assessment Required"
    else:
        category = "Repair/Replacement Required"

    # Burst pressure reduction factor due to dent
    # Simplified model: reduction proportional to dent depth
    f_dent = max(0, 1 - 5 * delta_ratio)

    # Burst pressure (Barlow's formula with reduction)
    # P_burst = 2·t·fy / D
    P_burst_intact = 2 * t * fy / D
    P_burst_dented = f_dent * P_burst_intact

    # Design pressure
    P_design = internal_pressure * safety_factor

    # Unity check
    unity_check = P_design / P_burst_dented if P_burst_dented > 0 else float('inf')

    status = "PASS" if unity_check <= 1.0 else "FAIL"

    return {
        'dent_depth_ratio': delta_ratio,
        'category': category,
        'burst_pressure_intact': P_burst_intact,
        'burst_pressure_dented': P_burst_dented,
        'design_pressure': P_design,
        'reduction_factor': f_dent,
        'unity_check': unity_check,
        'status': status
    }
```

## Complete Examples

### Example 1: Tubular Member Design for Jacket Structure

```python
import numpy as np

def design_jacket_leg(
    water_depth: float,
    environmental_load: dict,
    material: dict,
    safety_factors: dict
) -> dict:
    """
    Complete design of jacket leg tubular member.

    Args:
        water_depth: Water depth [m]
        environmental_load: Environmental loading
        material: Material properties
        safety_factors: Safety factors for design

    Returns:
        Design results with all checks

    Example:
        >>> environmental_load = {
        ...     'wave_force': 1500e3,  # N
        ...     'current_force': 300e3,
        ...     'wind_force': 200e3,
        ...     'bending_moment': 50e6  # N·m
        ... }
        >>> material = {
        ...     'E': 210e9,  # Pa
        ...     'fy': 355e6,
        ...     'density': 7850  # kg/m³
        ... }
        >>> safety_factors = {
        ...     'gamma_F': 1.35,  # Load factor
        ...     'gamma_M': 1.15   # Material factor
        ... }
        >>> result = design_jacket_leg(
        ...     water_depth=100,
        ...     environmental_load=environmental_load,
        ...     material=material,
        ...     safety_factors=safety_factors
        ... )
        >>> print(f"Required diameter: {result['diameter']:.3f} m")
        >>> print(f"Wall thickness: {result['thickness']*1000:.1f} mm")
    """
    # Initial sizing based on experience
    # For jacket legs: D typically 0.8-2.0 m, t typically 20-80 mm
    D = 1.5  # m
    t = 0.050  # m

    # Calculate section properties
    section = circular_tube_properties(D, t)

    # Length of member (assume from seabed to mean water level + freeboard)
    L = water_depth + 15  # m (15 m freeboard)

    # Combined loading
    # Axial force (self-weight + buoyancy + vertical environmental)
    # Estimate self-weight
    volume = section.area * L
    weight = volume * material['density'] * 9.81

    # Buoyancy (submerged length)
    rho_water = 1025  # kg/m³
    volume_submerged = section.area * water_depth
    buoyancy = volume_submerged * rho_water * 9.81

    # Net axial force (compression from self-weight, reduced by buoyancy)
    axial_force = weight - buoyancy

    # Add environmental axial component (compression from topside weight)
    topside_reaction = 5000e3  # N (example)
    axial_force += topside_reaction

    # Bending moment from lateral loads
    bending_moment = environmental_load['bending_moment']

    # Apply load factors
    Sd_axial = axial_force * safety_factors['gamma_F']
    Sd_moment = bending_moment * safety_factors['gamma_F']

    # 1. ULS Combined Loading Check
    uls_result = uls_combined_loading_check(
        axial_force=-Sd_axial,  # Compression
        bending_moment_y=Sd_moment,
        bending_moment_z=0,
        fy=material['fy'],
        section=section,
        gamma_M=safety_factors['gamma_M']
    )

    # 2. Buckling Check
    buckling_result = dnv_column_buckling_check(
        axial_force=Sd_axial,
        E=material['E'],
        fy=material['fy'],
        A=section.area,
        I=section.Ix,
        L=L,
        K=1.0,  # Pinned-pinned assumption
        gamma_M=safety_factors['gamma_M']
    )

    # 3. Deflection Check (serviceability)
    # Lateral load
    lateral_load = (
        environmental_load['wave_force'] +
        environmental_load['current_force'] +
        environmental_load['wind_force']
    )

    deflection_result = cantilever_beam_deflection(
        load_type='point_end',
        E=material['E'],
        I=section.Ix,
        L=L,
        load_magnitude=lateral_load
    )

    # Overall design check
    all_checks_pass = (
        uls_result['status'] == 'PASS' and
        buckling_result['status'] == 'PASS' and
        deflection_result['status'] == 'PASS'
    )

    return {
        'diameter': D,
        'thickness': t,
        'length': L,
        'section_properties': section,
        'loads': {
            'axial_design': Sd_axial,
            'moment_design': Sd_moment,
            'lateral_load': lateral_load
        },
        'uls_check': uls_result,
        'buckling_check': buckling_result,
        'deflection_check': deflection_result,
        'overall_status': 'PASS' if all_checks_pass else 'FAIL',
        'critical_unity_check': max(
            uls_result['unity_check'],
            buckling_result['unity_check'],
            deflection_result['unity_check']
        )
    }

# Run design
environmental_load = {
    'wave_force': 1500e3,
    'current_force': 300e3,
    'wind_force': 200e3,
    'bending_moment': 50e6
}

material = {
    'E': 210e9,
    'fy': 355e6,
    'density': 7850
}

safety_factors = {
    'gamma_F': 1.35,
    'gamma_M': 1.15
}

design_result = design_jacket_leg(
    water_depth=100,
    environmental_load=environmental_load,
    material=material,
    safety_factors=safety_factors
)

print("=" * 70)
print("JACKET LEG DESIGN SUMMARY")
print("=" * 70)
print(f"Diameter: {design_result['diameter']:.3f} m")
print(f"Wall Thickness: {design_result['thickness']*1000:.1f} mm")
print(f"Length: {design_result['length']:.1f} m")
print(f"\nSection Properties:")
print(f"  Area: {design_result['section_properties'].area:.4f} m²")
print(f"  Ix: {design_result['section_properties'].Ix:.6f} m⁴")
print(f"\nDesign Loads:")
print(f"  Axial (design): {design_result['loads']['axial_design']/1e6:.1f} MN")
print(f"  Moment (design): {design_result['loads']['moment_design']/1e6:.1f} MN·m")
print(f"\nULS Check: {design_result['uls_check']['status']}")
print(f"  Unity Check: {design_result['uls_check']['unity_check']:.3f}")
print(f"\nBuckling Check: {design_result['buckling_check']['status']}")
print(f"  Unity Check: {design_result['buckling_check']['unity_check']:.3f}")
print(f"  Slenderness Ratio: {design_result['buckling_check']['slenderness_ratio']:.1f}")
print(f"\nDeflection Check: {design_result['deflection_check']['status']}")
print(f"  Max Deflection: {design_result['deflection_check']['max_deflection']*1000:.1f} mm")
print(f"  Allowable: {design_result['deflection_check']['allowable_deflection']*1000:.1f} mm")
print(f"\n{'='*70}")
print(f"OVERALL DESIGN STATUS: {design_result['overall_status']}")
print(f"Critical Unity Check: {design_result['critical_unity_check']:.3f}")
print(f"{'='*70}")
```

### Example 2: Tubular Joint Analysis

```python
def analyze_tubular_joint_with_fatigue(
    chord_diameter: float,
    chord_thickness: float,
    brace_diameter: float,
    brace_thickness: float,
    brace_angle: float,
    static_loads: dict,
    cyclic_loads: dict,
    material: dict,
    design_life: float = 25.0
) -> dict:
    """
    Complete tubular joint analysis including static and fatigue checks.

    Args:
        chord_diameter: Chord OD [m]
        chord_thickness: Chord wall thickness [m]
        brace_diameter: Brace OD [m]
        brace_thickness: Brace wall thickness [m]
        brace_angle: Angle [degrees]
        static_loads: Static loading
        cyclic_loads: Cyclic loading for fatigue
        material: Material properties
        design_life: Design life [years]

    Returns:
        Complete analysis results

    Example:
        >>> static_loads = {
        ...     'axial': 2500e3,
        ...     'ipb': 800e3,
        ...     'opb': 0
        ... }
        >>> cyclic_loads = {
        ...     'stress_range': 80e6,  # Pa
        ...     'cycles_per_year': 1e6
        ... }
        >>> material = {
        ...     'fy_chord': 355e6,
        ...     'fy_brace': 355e6,
        ...     'sn_curve': 'D'
        ... }
        >>> result = analyze_tubular_joint_with_fatigue(
        ...     chord_diameter=1.5,
        ...     chord_thickness=0.050,
        ...     brace_diameter=0.914,
        ...     brace_thickness=0.030,
        ...     brace_angle=45,
        ...     static_loads=static_loads,
        ...     cyclic_loads=cyclic_loads,
        ...     material=material,
        ...     design_life=25.0
        ... )
        >>> print(f"Static UC: {result['static_check']['unity_check']:.3f}")
        >>> print(f"Fatigue Life: {result['fatigue_life']:.1f} years")
    """
    # Static capacity check
    static_check = tubular_joint_capacity_check(
        chord_diameter=chord_diameter,
        chord_thickness=chord_thickness,
        brace_diameter=brace_diameter,
        brace_thickness=brace_thickness,
        brace_angle=brace_angle,
        fy_chord=material['fy_chord'],
        fy_brace=material['fy_brace'],
        axial_load=static_loads['axial'],
        in_plane_bending=static_loads['ipb'],
        out_plane_bending=static_loads['opb'],
        joint_type='Y'
    )

    # Fatigue analysis
    # Get S-N curve (using same function as fatigue-analysis skill)
    from fatigue_analysis import get_dnv_sn_curve, calculate_fatigue_damage

    sn_params = get_dnv_sn_curve(
        curve_class=material['sn_curve'],
        thickness=chord_thickness * 1000  # Convert to mm
    )

    # Total cycles over design life
    N_total = cyclic_loads['cycles_per_year'] * design_life

    # Fatigue damage
    stress_range = cyclic_loads['stress_range']
    damage = calculate_fatigue_damage(
        stress_range=stress_range / 1e6,  # Convert to MPa
        cycles=N_total,
        sn_params=sn_params
    )

    # Fatigue life
    if damage > 0:
        fatigue_life = design_life / damage
    else:
        fatigue_life = float('inf')

    fatigue_status = "PASS" if damage <= 1.0 else "FAIL"

    # Hot spot stress concentration factor (SCF) for tubular joints
    # Simplified - actual SCF depends on joint geometry and load type
    beta = brace_diameter / chord_diameter
    gamma = chord_diameter / (2 * chord_thickness)
    tau = brace_thickness / chord_thickness

    # Axial SCF (simplified Efthymiou equations)
    SCF_axial = gamma**0.2 * beta**(-0.5) * (1.2 + 0.1 * beta)

    # Combined hot spot stress
    hot_spot_stress = SCF_axial * stress_range

    return {
        'static_check': static_check,
        'fatigue_damage': damage,
        'fatigue_life': fatigue_life,
        'fatigue_status': fatigue_status,
        'scf': {
            'axial': SCF_axial,
            'hot_spot_stress': hot_spot_stress
        },
        'joint_parameters': {
            'beta': beta,
            'gamma': gamma,
            'tau': tau
        },
        'overall_status': (
            'PASS' if static_check['status'] == 'PASS' and fatigue_status == 'PASS'
            else 'FAIL'
        )
    }

# Run analysis
static_loads = {
    'axial': 2500e3,
    'ipb': 800e3,
    'opb': 0
}

cyclic_loads = {
    'stress_range': 80e6,
    'cycles_per_year': 1e6
}

material = {
    'fy_chord': 355e6,
    'fy_brace': 355e6,
    'sn_curve': 'D'
}

joint_result = analyze_tubular_joint_with_fatigue(
    chord_diameter=1.5,
    chord_thickness=0.050,
    brace_diameter=0.914,
    brace_thickness=0.030,
    brace_angle=45,
    static_loads=static_loads,
    cyclic_loads=cyclic_loads,
    material=material,
    design_life=25.0
)

print("=" * 70)
print("TUBULAR JOINT ANALYSIS")
print("=" * 70)
print(f"\nStatic Capacity Check: {joint_result['static_check']['status']}")
print(f"  Unity Check: {joint_result['static_check']['unity_check']:.3f}")
print(f"  Axial Capacity: {joint_result['static_check']['axial_capacity']/1e6:.1f} MN")
print(f"  Applied Axial: {joint_result['static_check']['applied_axial']/1e6:.1f} MN")
print(f"\nFatigue Analysis: {joint_result['fatigue_status']}")
print(f"  Fatigue Damage: {joint_result['fatigue_damage']:.3f}")
print(f"  Fatigue Life: {joint_result['fatigue_life']:.1f} years")
print(f"\nStress Concentration:")
print(f"  SCF (axial): {joint_result['scf']['axial']:.2f}")
print(f"  Hot Spot Stress: {joint_result['scf']['hot_spot_stress']/1e6:.1f} MPa")
print(f"\n{'='*70}")
print(f"OVERALL STATUS: {joint_result['overall_status']}")
print(f"{'='*70}")
```

### Example 3: Stiffened Panel Buckling

```python
def stiffened_panel_buckling_analysis(
    plate_width: float,
    plate_length: float,
    plate_thickness: float,
    stiffener_spacing: float,
    stiffener_height: float,
    stiffener_thickness: float,
    applied_stress: float,
    E: float = 210e9,
    nu: float = 0.3,
    fy: float = 355e6
) -> dict:
    """
    Buckling analysis for stiffened panel (ship hull, deck, etc.).

    Args:
        plate_width: Panel width (between supports) [m]
        plate_length: Panel length [m]
        plate_thickness: Plate thickness [m]
        stiffener_spacing: Spacing between stiffeners [m]
        stiffener_height: Stiffener web height [m]
        stiffener_thickness: Stiffener web thickness [m]
        applied_stress: Applied compressive stress [Pa]
        E: Young's modulus [Pa]
        nu: Poisson's ratio
        fy: Yield strength [Pa]

    Returns:
        Buckling analysis results

    Example:
        >>> result = stiffened_panel_buckling_analysis(
        ...     plate_width=4.0,
        ...     plate_length=12.0,
        ...     plate_thickness=0.012,
        ...     stiffener_spacing=0.8,
        ...     stiffener_height=0.200,
        ...     stiffener_thickness=0.010,
        ...     applied_stress=150e6,
        ...     E=210e9,
        ...     fy=355e6
        ... )
        >>> print(f"Panel buckling UC: {result['panel_buckling_uc']:.3f}")
        >>> print(f"Column buckling UC: {result['column_buckling_uc']:.3f}")
    """
    # Plate panel dimensions
    a = plate_length  # Length
    b = stiffener_spacing  # Width (between stiffeners)
    t = plate_thickness

    # Plate buckling coefficient
    # For simply supported rectangular plate under uniaxial compression:
    # σ_cr = k · π²E / (12(1-ν²)) · (t/b)²
    # where k depends on aspect ratio a/b

    aspect_ratio = a / b

    # Buckling coefficient k (for simply supported edges)
    if aspect_ratio >= 1:
        k = 4.0  # Long plate (a/b ≥ 1)
    else:
        k = (1 + aspect_ratio**2)**2 / aspect_ratio**2  # Short plate

    # Critical buckling stress for plate panel
    sigma_cr_plate = (
        k * np.pi**2 * E / (12 * (1 - nu**2)) * (t / b)**2
    )

    # Panel buckling unity check
    panel_buckling_uc = applied_stress / sigma_cr_plate

    # Stiffener + effective plate as column
    # Effective width of plate (participating in column buckling)
    # DNV: b_eff = min(b, 30·t·sqrt(E/fy))
    b_eff = min(b, 30 * t * np.sqrt(E / fy))

    # Stiffener section properties (T-section: flange = effective plate, web = stiffener)
    # Flange (effective plate)
    A_flange = b_eff * t
    y_flange = stiffener_height + t / 2

    # Web (stiffener)
    A_web = stiffener_height * stiffener_thickness
    y_web = stiffener_height / 2

    # Total area
    A_total = A_flange + A_web

    # Centroid location (from baseline of stiffener)
    y_c = (A_flange * y_flange + A_web * y_web) / A_total

    # Second moment of area about neutral axis
    # Flange contribution
    I_flange = (
        b_eff * t**3 / 12 +
        A_flange * (y_flange - y_c)**2
    )

    # Web contribution
    I_web = (
        stiffener_thickness * stiffener_height**3 / 12 +
        A_web * (y_web - y_c)**2
    )

    I_total = I_flange + I_web

    # Radius of gyration
    r = np.sqrt(I_total / A_total)

    # Column buckling (Euler)
    # Assume effective length = panel length
    L_eff = plate_length
    lambda_ratio = L_eff / r

    # Critical buckling stress (Euler)
    sigma_cr_column = np.pi**2 * E / lambda_ratio**2

    # Column buckling unity check
    column_buckling_uc = applied_stress / sigma_cr_column

    # Overall buckling check (most critical)
    overall_uc = max(panel_buckling_uc, column_buckling_uc)

    status = "PASS" if overall_uc <= 1.0 else "FAIL"

    return {
        'plate_buckling_stress': sigma_cr_plate,
        'panel_buckling_uc': panel_buckling_uc,
        'column_buckling_stress': sigma_cr_column,
        'column_buckling_uc': column_buckling_uc,
        'overall_unity_check': overall_uc,
        'status': status,
        'stiffener_properties': {
            'area': A_total,
            'moment_of_inertia': I_total,
            'radius_of_gyration': r,
            'slenderness_ratio': lambda_ratio
        },
        'plate_properties': {
            'aspect_ratio': aspect_ratio,
            'buckling_coefficient': k,
            'effective_width': b_eff
        }
    }

# Run analysis
panel_result = stiffened_panel_buckling_analysis(
    plate_width=4.0,
    plate_length=12.0,
    plate_thickness=0.012,
    stiffener_spacing=0.8,
    stiffener_height=0.200,
    stiffener_thickness=0.010,
    applied_stress=150e6,
    E=210e9,
    fy=355e6
)

print("=" * 70)
print("STIFFENED PANEL BUCKLING ANALYSIS")
print("=" * 70)
print(f"\nPlate Panel Buckling:")
print(f"  Critical Stress: {panel_result['plate_buckling_stress']/1e6:.1f} MPa")
print(f"  Unity Check: {panel_result['panel_buckling_uc']:.3f}")
print(f"  Buckling Coefficient k: {panel_result['plate_properties']['buckling_coefficient']:.2f}")
print(f"  Aspect Ratio: {panel_result['plate_properties']['aspect_ratio']:.2f}")
print(f"\nStiffener Column Buckling:")
print(f"  Critical Stress: {panel_result['column_buckling_stress']/1e6:.1f} MPa")
print(f"  Unity Check: {panel_result['column_buckling_uc']:.3f}")
print(f"  Slenderness Ratio: {panel_result['stiffener_properties']['slenderness_ratio']:.1f}")
print(f"\n{'='*70}")
print(f"OVERALL STATUS: {panel_result['status']}")
print(f"Critical Unity Check: {panel_result['overall_unity_check']:.3f}")
print(f"{'='*70}")
```

## Best Practices

### 1. Material Selection

```python
# Standard marine structural steels
MATERIALS = {
    'S355': {
        'fy': 355e6,  # Pa
        'fu': 490e6,
        'E': 210e9,
        'nu': 0.3,
        'density': 7850,  # kg/m³
        'description': 'High strength structural steel (DNV-OS-B101)'
    },
    'S420': {
        'fy': 420e6,
        'fu': 530e6,
        'E': 210e9,
        'nu': 0.3,
        'density': 7850,
        'description': 'Very high strength structural steel'
    },
    'API 5L X65': {
        'fy': 448e6,  # 65 ksi
        'fu': 530e6,
        'E': 210e9,
        'nu': 0.3,
        'density': 7850,
        'description': 'Pipeline steel grade'
    }
}
```

### 2. Safety Factors (DNV)

```python
# DNV safety factors
SAFETY_FACTORS = {
    'ULS': {
        'gamma_F': 1.3,  # Load factor (permanent loads)
        'gamma_F_variable': 1.5,  # Load factor (variable loads)
        'gamma_M': 1.15  # Material factor
    },
    'ALS': {
        'gamma_F': 1.0,  # Load factor
        'gamma_M': 1.0   # Material factor (yield)
    },
    'FLS': {
        'gamma_F': 1.0,  # Load factor
        'gamma_Mf': 1.0  # Fatigue material factor
    },
    'SLS': {
        'gamma_F': 1.0,  # Load factor
        'gamma_M': 1.0   # Material factor
    }
}
```

### 3. Design Workflow

```python
def structural_design_workflow(
    geometry: dict,
    loads: dict,
    material: dict,
    design_codes: list
) -> dict:
    """
    Complete structural design workflow following DNV standards.

    Workflow:
    1. Define geometry and loads
    2. Calculate section properties
    3. ULS checks (strength)
    4. ALS checks (accidental loads)
    5. FLS checks (fatigue)
    6. SLS checks (deflection, vibration)
    7. Optimize if needed
    8. Generate design report

    Args:
        geometry: Geometric parameters
        loads: Load cases
        material: Material properties
        design_codes: List of applicable codes

    Returns:
        Complete design results
    """
    results = {
        'geometry': geometry,
        'section_properties': None,
        'uls_checks': [],
        'als_checks': [],
        'fls_checks': [],
        'sls_checks': [],
        'optimization': None,
        'status': 'PENDING'
    }

    # Step 1: Calculate section properties
    # (implementation depends on geometry type)

    # Step 2: ULS checks
    # (check all ULS load combinations)

    # Step 3: ALS checks
    # (check accidental scenarios)

    # Step 4: FLS checks
    # (fatigue assessment)

    # Step 5: SLS checks
    # (deflections, vibrations)

    # Step 6: Overall assessment
    all_checks_pass = True  # Logic to verify all checks

    results['status'] = 'PASS' if all_checks_pass else 'FAIL'

    return results
```

### 4. Code Compliance Documentation

```python
def generate_design_report(
    design_results: dict,
    project_info: dict,
    applicable_codes: list
) -> str:
    """
    Generate design calculation report with code references.

    Args:
        design_results: Results from design calculations
        project_info: Project information
        applicable_codes: List of codes used

    Returns:
        Formatted design report (Markdown or HTML)
    """
    report = f"""
# Structural Design Calculation Report

## Project Information
- Project: {project_info['name']}
- Location: {project_info['location']}
- Design Date: {project_info['date']}
- Engineer: {project_info['engineer']}

## Applicable Codes and Standards
{chr(10).join(['- ' + code for code in applicable_codes])}

## Design Criteria
- Design Life: {project_info['design_life']} years
- ULS Safety Factors: γ_F = {SAFETY_FACTORS['ULS']['gamma_F']}, γ_M = {SAFETY_FACTORS['ULS']['gamma_M']}
- Material: {project_info['material']}

## Structural Member Details
[Section properties, dimensions, etc.]

## Load Cases
[ULS, ALS, FLS load combinations]

## Design Checks
### ULS Checks
[Results with unity checks]

### Buckling Checks
[Results with slenderness ratios]

### Fatigue Checks
[Fatigue life calculations]

## Conclusions
Overall Design Status: {design_results['status']}

## Revisions
[Revision history]
"""
    return report
```

## Resources

### DNV Standards

- **DNV-OS-C101**: Design of Offshore Steel Structures, General (LRFD Method)
- **DNV-RP-C201**: Buckling Strength of Plated Structures
- **DNV-RP-C203**: Fatigue Design of Offshore Steel Structures
- **DNV-RP-C205**: Environmental Conditions and Environmental Loads
- **DNV-RP-C206**: Fatigue Methodology of Offshore Ships
- **DNV-ST-0126**: Support Structures for Wind Turbines
- **DNV-OS-E301**: Position Mooring

### API Standards

- **API RP 2A**: Planning, Designing and Constructing Fixed Offshore Platforms
- **API RP 2FPS**: Planning, Designing, and Constructing Floating Production Systems
- **API RP 2SK**: Design and Analysis of Stationkeeping Systems for Floating Structures
- **API Spec 2B**: Fabrication of Structural Steel Pipe

### Other Standards

- **ISO 19902**: Petroleum and natural gas industries - Fixed steel offshore structures
- **Eurocode 3**: Design of steel structures (EN 1993)
- **AISC 360**: Specification for Structural Steel Buildings

### Textbooks and References

- Chakrabarti, S.K. (2005). *Handbook of Offshore Engineering*
- Bai, Y., Bai, Q. (2014). *Subsea Structural Engineering Handbook*
- Marshall, P.W. (1992). *Design of Welded Tubular Connections*
- Young, W.C., Budynas, R.G. (2002). *Roark's Formulas for Stress and Strain*

### Software Tools

- **SACS**: Structural Analysis Computer System (offshore jackets)
- **ANSYS**: Finite element analysis
- **STAAD.Pro**: Structural analysis and design
- **OrcaFlex**: Dynamic analysis (can export loads for structural checks)
- **SESAM**: DNV's integrated software for marine structures

---

**Use this skill for:** Structural design and analysis of marine and offshore structures with full DNV/API code compliance.
