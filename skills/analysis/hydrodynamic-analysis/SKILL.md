---
name: hydrodynamic-analysis
version: 1.0.0
description: Hydrodynamic analysis using BEM, RAOs, added mass, damping, and wave loads for offshore structures
author: workspace-hub
category: subject-matter-expert
tags: [hydrodynamics, bem, rao, added-mass, damping, wave-loads, wamit, aqwa, orcawave]
platforms: [engineering]
---

# Hydrodynamic Analysis SME Skill

Comprehensive hydrodynamic analysis expertise for offshore floating structures including BEM theory, RAO calculations, added mass/damping, and integration with industry-standard software.

## When to Use This Skill

Use hydrodynamic analysis knowledge when:
- **RAO calculation** - Response Amplitude Operators for vessel motions
- **Added mass & damping** - Frequency-dependent hydrodynamic coefficients
- **Wave loading** - Diffraction, Froude-Krylov, radiation forces
- **BEM analysis** - Boundary Element Method for potential flow
- **Software integration** - WAMIT, AQWA, OrcaWave workflows
- **Frequency domain** - Linear wave theory analysis
- **Time domain** - Convolution for time-domain simulations

## Core Knowledge Areas

### 1. Boundary Element Method (BEM)

**Potential Flow Theory:**
```
Governing Equation: ∇²φ = 0 (Laplace equation)

Where:
- φ = velocity potential
- Pressure: p = -ρ ∂φ/∂t - ρgz (Bernoulli)
- Velocity: v = ∇φ
```

**BEM Principles:**
```python
def bem_panel_method_concept():
    """
    Conceptual explanation of BEM panel method.

    Key Steps:
    1. Discretize wetted surface into panels
    2. Apply Green's function (source/dipole distribution)
    3. Satisfy boundary conditions on each panel
    4. Solve linear system for unknown potentials
    5. Calculate forces from pressure integration
    """
    pass

# Radiation Problem:
# - Forced oscillation in calm water
# - Calculates added mass and damping
# - 6 DOFs → 6 radiation potentials

# Diffraction Problem:
# - Fixed body in waves
# - Calculates wave excitation forces
# - Different wave headings analyzed
```

**Panel Mesh Quality:**
```yaml
mesh_requirements:
  panel_size:
    general: "< λ/6"  # Lambda = wavelength
    critical_areas: "< λ/10"  # Bow, stern, sharp edges

  aspect_ratio:
    maximum: 3.0
    preferred: 1.5

  panel_count:
    minimum: 2000  # Small vessels
    typical: 5000-10000  # FPSOs
    large: 20000+  # Complex geometries

  symmetry:
    use_if_possible: true  # Reduces computational cost by 50%
    check: "Ensure port-starboard symmetry"
```

### 2. Response Amplitude Operators (RAOs)

**RAO Definition:**
```
RAO(ω) = Response Amplitude / Wave Amplitude

Units:
- Translation (surge, sway, heave): m/m
- Rotation (roll, pitch, yaw): rad/m or deg/m
```

**RAO Calculation:**
```python
import numpy as np

def calculate_rao_from_hydrodynamic_coefficients(
    omega: float,
    mass_matrix: np.ndarray,
    added_mass: np.ndarray,
    damping: np.ndarray,
    stiffness: np.ndarray,
    wave_excitation: np.ndarray
) -> np.ndarray:
    """
    Calculate RAO at frequency omega.

    Equation of motion (frequency domain):
    [-ω²(M + A(ω)) + iω·B(ω) + K]·RAO = F_wave

    Args:
        omega: Wave frequency (rad/s)
        mass_matrix: 6x6 mass matrix
        added_mass: 6x6 added mass matrix at omega
        damping: 6x6 damping matrix at omega
        stiffness: 6x6 hydrostatic stiffness
        wave_excitation: 6x1 complex wave excitation force

    Returns:
        6x1 complex RAO (amplitude and phase)
    """
    # Dynamic stiffness matrix (complex)
    K_dynamic = (
        -omega**2 * (mass_matrix + added_mass) +
        1j * omega * damping +
        stiffness
    )

    # Solve for RAO
    rao_complex = np.linalg.solve(K_dynamic, wave_excitation)

    return rao_complex

# Example: Calculate heave RAO
omega = 2 * np.pi / 10  # T = 10s
M = np.diag([150000, 150000, 150000, 1e7, 1e7, 5e6])  # Mass matrix
A = np.diag([15000, 15000, 50000, 1e6, 1e6, 5e5])     # Added mass
B = np.diag([50000, 50000, 100000, 5e5, 5e5, 2e5])    # Damping
K = np.diag([0, 0, 3000, 0, 0, 0])                    # Hydrostatic stiffness

# Wave excitation (heave dominant)
F_wave = np.array([100000, 0, 500000, 0, 1e6, 0]) + 0j

rao = calculate_rao_from_hydrodynamic_coefficients(omega, M, A, B, K, F_wave)

# Heave RAO amplitude
heave_rao_amplitude = np.abs(rao[2])
heave_rao_phase = np.angle(rao[2], deg=True)

print(f"Heave RAO: {heave_rao_amplitude:.3f} m/m at {heave_rao_phase:.1f}°")
```

**RAO Peak Period:**
```python
def find_rao_peak_period(
    frequencies: np.ndarray,
    rao_amplitude: np.ndarray
) -> dict:
    """
    Find peak RAO period and resonance characteristics.

    Args:
        frequencies: Frequency array (rad/s)
        rao_amplitude: RAO amplitude array

    Returns:
        Peak information
    """
    # Find peak
    peak_idx = np.argmax(rao_amplitude)
    peak_omega = frequencies[peak_idx]
    peak_period = 2 * np.pi / peak_omega
    peak_rao = rao_amplitude[peak_idx]

    return {
        'peak_frequency_rad_s': peak_omega,
        'peak_period_s': peak_period,
        'peak_rao': peak_rao,
        'resonance_detected': peak_rao > 2.0  # Typical threshold
    }

# Example
frequencies = np.linspace(0.1, 2.0, 100)
rao_amplitudes = 1.5 / np.sqrt((1 - (frequencies/0.5)**2)**2 + (0.1*frequencies/0.5)**2)

peak_info = find_rao_peak_period(frequencies, rao_amplitudes)
print(f"Natural period: {peak_info['peak_period_s']:.2f} s")
print(f"Peak RAO: {peak_info['peak_rao']:.2f} m/m")
```

### 3. Added Mass and Damping

**Frequency-Dependent Coefficients:**
```python
def interpolate_hydrodynamic_coefficients(
    omega_target: float,
    omega_data: np.ndarray,
    coefficient_data: np.ndarray
) -> np.ndarray:
    """
    Interpolate added mass or damping at target frequency.

    Args:
        omega_target: Target frequency (rad/s)
        omega_data: Frequency data from BEM
        coefficient_data: Coefficient matrix (n_freq x 6 x 6)

    Returns:
        Interpolated 6x6 coefficient matrix
    """
    from scipy.interpolate import interp1d

    # Interpolate each element
    coefficient_interp = np.zeros((6, 6))

    for i in range(6):
        for j in range(6):
            # Extract time series for this coefficient
            coef_series = coefficient_data[:, i, j]

            # Create interpolator
            interpolator = interp1d(
                omega_data,
                coef_series,
                kind='cubic',
                fill_value='extrapolate'
            )

            # Interpolate
            coefficient_interp[i, j] = interpolator(omega_target)

    return coefficient_interp

# Example usage
omega_data = np.array([0.1, 0.5, 1.0, 1.5, 2.0])  # rad/s
added_mass_data = np.random.rand(5, 6, 6) * 10000  # Sample data

# Interpolate at T = 8s (omega = 0.785 rad/s)
A_interp = interpolate_hydrodynamic_coefficients(
    omega_target=2*np.pi/8,
    omega_data=omega_data,
    coefficient_data=added_mass_data
)

print(f"Added mass at T=8s:")
print(A_interp)
```

**Infinite Frequency Added Mass:**
```python
def calculate_infinite_frequency_added_mass(
    omega_data: np.ndarray,
    added_mass_data: np.ndarray
) -> np.ndarray:
    """
    Estimate infinite frequency added mass (A_inf).

    A_inf = lim(ω→∞) A(ω)

    Args:
        omega_data: Frequency array
        added_mass_data: Added mass array (n_freq x 6 x 6)

    Returns:
        6x6 infinite frequency added mass
    """
    # Use highest frequency values and extrapolate
    # Typically: fit A(ω) = A_inf + C/ω²

    A_inf = np.zeros((6, 6))

    for i in range(6):
        for j in range(6):
            # Take average of highest 3 frequencies
            A_inf[i, j] = np.mean(added_mass_data[-3:, i, j])

    return A_inf
```

### 4. Wave Forces

**Froude-Krylov Force:**
```python
def calculate_froude_krylov_force(
    wave_amplitude: float,
    omega: float,
    waterplane_area: float,
    center_of_buoyancy_depth: float,
    rho: float = 1025
) -> float:
    """
    Calculate Froude-Krylov force (undisturbed wave pressure).

    F_FK = ρ g ζ_a A_wp e^(k z_b)

    Args:
        wave_amplitude: Wave amplitude (m)
        omega: Wave frequency (rad/s)
        waterplane_area: Waterplane area (m²)
        center_of_buoyancy_depth: Depth of center of buoyancy (m)
        rho: Water density (kg/m³)

    Returns:
        Froude-Krylov force amplitude (N)
    """
    g = 9.81

    # Wave number (deep water approximation)
    k = omega**2 / g

    # Froude-Krylov force
    F_FK = rho * g * wave_amplitude * waterplane_area * np.exp(k * center_of_buoyancy_depth)

    return F_FK

# Example
F_FK = calculate_froude_krylov_force(
    wave_amplitude=2.0,  # 2m amplitude (Hs = 4m)
    omega=2*np.pi/10,    # 10s period
    waterplane_area=15000,  # m²
    center_of_buoyancy_depth=-10  # 10m below waterline
)

print(f"Froude-Krylov force: {F_FK/1e6:.2f} MN")
```

**Diffraction Force:**
```python
def calculate_diffraction_coefficient(
    diameter: float,
    wavelength: float
) -> float:
    """
    Estimate diffraction coefficient.

    Diffraction important when D/λ > 0.2 (MacCamy-Fuchs)

    Args:
        diameter: Characteristic diameter
        wavelength: Wave length

    Returns:
        Diffraction importance factor
    """
    D_over_lambda = diameter / wavelength

    if D_over_lambda < 0.1:
        regime = "Morison (small body)"
    elif D_over_lambda < 0.2:
        regime = "Transition"
    else:
        regime = "Diffraction (large body)"

    print(f"D/λ = {D_over_lambda:.3f} → {regime}")

    return D_over_lambda

# Example: FPSO hull
D = 58  # Beam = 58m
T = 10  # Wave period
wavelength = 9.81 * T**2 / (2 * np.pi)  # Deep water

diffraction_coef = calculate_diffraction_coefficient(D, wavelength)
```

### 5. Hydrostatic Stiffness

**Stiffness Matrix:**
```python
def calculate_hydrostatic_stiffness(
    waterplane_area: float,
    center_of_buoyancy: np.ndarray,
    metacentric_height_long: float,
    metacentric_height_trans: float,
    displacement: float,
    rho: float = 1025
) -> np.ndarray:
    """
    Calculate 6x6 hydrostatic stiffness matrix.

    Args:
        waterplane_area: Waterplane area (m²)
        center_of_buoyancy: [x, y, z] position (m)
        metacentric_height_long: Longitudinal GM (m)
        metacentric_height_trans: Transverse GM (m)
        displacement: Vessel displacement (tonnes)
        rho: Water density (kg/m³)

    Returns:
        6x6 hydrostatic stiffness matrix
    """
    g = 9.81
    mass = displacement * 1000  # kg

    K = np.zeros((6, 6))

    # Heave stiffness: K_33 = ρ g A_wp
    K[2, 2] = rho * g * waterplane_area

    # Roll stiffness: K_44 = ρ g ∇ GM_T
    K[3, 3] = mass * g * metacentric_height_trans

    # Pitch stiffness: K_55 = ρ g ∇ GM_L
    K[4, 4] = mass * g * metacentric_height_long

    # Heave-pitch coupling
    K[2, 4] = -rho * g * waterplane_area * center_of_buoyancy[0]
    K[4, 2] = K[2, 4]

    # Heave-roll coupling
    K[2, 3] = -rho * g * waterplane_area * center_of_buoyancy[1]
    K[3, 2] = K[2, 3]

    return K

# Example: FPSO hydrostatic stiffness
K_hydro = calculate_hydrostatic_stiffness(
    waterplane_area=15000,  # m²
    center_of_buoyancy=np.array([160, 0, -10]),  # m
    metacentric_height_long=5.0,  # m
    metacentric_height_trans=3.0,  # m
    displacement=150000  # tonnes
)

print("Hydrostatic Stiffness Matrix:")
print(K_hydro)
```

### 6. Wave Spectra and Irregular Seas

**JONSWAP Spectrum:**
```python
def jonswap_spectrum(
    frequencies: np.ndarray,
    Hs: float,
    Tp: float,
    gamma: float = 3.3
) -> np.ndarray:
    """
    Calculate JONSWAP wave spectrum.

    S(f) = α g² (2π)^-4 f^-5 exp[-5/4(f/fp)^-4] γ^exp[-(f-fp)²/(2σ²fp²)]

    Args:
        frequencies: Frequency array (Hz)
        Hs: Significant wave height (m)
        Tp: Peak period (s)
        gamma: Peak enhancement factor (default 3.3)

    Returns:
        Spectral density S(f) (m²/Hz)
    """
    g = 9.81
    fp = 1 / Tp  # Peak frequency

    # Phillips constant
    alpha = 5.0 / 16.0 * Hs**2 * fp**4 / g**2

    # Spectral width parameter
    sigma = np.where(frequencies <= fp, 0.07, 0.09)

    # JONSWAP spectrum
    S_PM = alpha * g**2 * (2*np.pi)**(-4) * frequencies**(-5) * \
           np.exp(-5/4 * (frequencies / fp)**(-4))

    # Peak enhancement
    gamma_factor = gamma ** np.exp(-(frequencies - fp)**2 / (2 * sigma**2 * fp**2))

    S_JONSWAP = S_PM * gamma_factor

    return S_JONSWAP

# Example: Generate JONSWAP spectrum
freq = np.linspace(0.01, 0.5, 500)  # Hz
S = jonswap_spectrum(freq, Hs=8.5, Tp=12.0, gamma=3.3)

# Check Hs from spectrum
m0 = np.trapz(S, freq)  # Zero-order moment
Hs_calculated = 4 * np.sqrt(m0)

print(f"Input Hs: 8.5 m")
print(f"Calculated Hs from spectrum: {Hs_calculated:.2f} m")
```

**Response Spectrum:**
```python
def calculate_response_spectrum(
    wave_spectrum: np.ndarray,
    rao_amplitude: np.ndarray,
    frequencies: np.ndarray
) -> tuple[np.ndarray, dict]:
    """
    Calculate response spectrum from wave spectrum and RAO.

    S_response(ω) = |RAO(ω)|² * S_wave(ω)

    Args:
        wave_spectrum: Wave spectral density
        rao_amplitude: RAO amplitude (m/m)
        frequencies: Frequency array

    Returns:
        (response_spectrum, statistics)
    """
    # Response spectrum
    S_response = rao_amplitude**2 * wave_spectrum

    # Calculate statistics
    m0 = np.trapz(S_response, frequencies)  # Variance
    m2 = np.trapz(S_response * frequencies**2, frequencies)

    # Response statistics
    stats = {
        'variance': m0,
        'std_dev': np.sqrt(m0),
        'significant_amplitude': 2 * np.sqrt(m0),  # ≈ H_1/3 for motions
        'zero_crossing_period': 2 * np.pi * np.sqrt(m0 / m2)
    }

    return S_response, stats

# Example
freq = np.linspace(0.01, 0.5, 500)
S_wave = jonswap_spectrum(freq, Hs=8.5, Tp=12.0)

# Sample heave RAO
rao_heave = 1.2 / np.sqrt((1 - (2*np.pi*freq / 0.6)**2)**2 + (0.1 * 2*np.pi*freq / 0.6)**2)

S_heave, stats_heave = calculate_response_spectrum(S_wave, rao_heave, freq)

print(f"Significant heave amplitude: {stats_heave['significant_amplitude']:.2f} m")
print(f"Heave zero-crossing period: {stats_heave['zero_crossing_period']:.2f} s")
```

## Practical Applications

### Application 1: Complete RAO Analysis

```python
def complete_rao_analysis(
    bem_results_file: str,
    wave_headings: np.ndarray = None,
    output_dir: str = 'reports/rao_analysis'
) -> dict:
    """
    Complete RAO analysis from BEM results.

    Args:
        bem_results_file: Path to BEM results (WAMIT .out or AQWA .lis)
        wave_headings: Wave heading array (degrees)
        output_dir: Output directory

    Returns:
        RAO results dictionary
    """
    import pandas as pd
    from pathlib import Path

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if wave_headings is None:
        wave_headings = np.arange(0, 360, 30)

    # Load BEM results (example format)
    # In reality, parse WAMIT .out or AQWA results
    frequencies = np.linspace(0.1, 2.0, 50)  # rad/s
    periods = 2 * np.pi / frequencies

    # Sample RAO data (6 DOFs x n_frequencies x n_headings)
    raos = {}
    dof_names = ['Surge', 'Sway', 'Heave', 'Roll', 'Pitch', 'Yaw']

    for heading in wave_headings:
        for i, dof in enumerate(dof_names):
            # Simplified RAO calculation
            # In practice, read from BEM output
            if heading == 0:  # Head seas
                if dof == 'Surge':
                    rao = 0.8 * np.ones_like(frequencies)
                elif dof == 'Heave':
                    rao = 1.2 / np.sqrt((1 - (frequencies/0.6)**2)**2 + (0.1*frequencies/0.6)**2)
                elif dof == 'Pitch':
                    rao = 0.05 * frequencies / (1 + (frequencies/0.6)**2)
                else:
                    rao = np.zeros_like(frequencies)
            else:
                # Simplified for other headings
                rao = np.random.rand(len(frequencies)) * 0.5

            raos[(heading, dof)] = rao

    # Export RAOs to CSV
    for dof in dof_names:
        df_rao = pd.DataFrame({
            'Period_s': periods,
            **{f'Heading_{h}deg': raos[(h, dof)] for h in wave_headings}
        })

        df_rao.to_csv(output_path / f'RAO_{dof}.csv', index=False)

    # Create polar plot
    import plotly.graph_objects as go

    fig = go.Figure()

    for dof in ['Surge', 'Heave', 'Pitch']:
        rao_at_peak = [raos[(h, dof)][25] for h in wave_headings]  # At T=10s

        fig.add_trace(go.Scatterpolar(
            r=rao_at_peak,
            theta=wave_headings,
            name=dof,
            mode='lines+markers'
        ))

    fig.update_layout(
        title='RAO Polar Plot (T = 10s)',
        polar=dict(radialaxis=dict(visible=True))
    )

    fig.write_html(output_path / 'RAO_polar.html')

    print(f"✓ RAO analysis complete")
    print(f"  Output: {output_dir}")

    return raos

# Usage
rao_results = complete_rao_analysis(
    bem_results_file='data/processed/wamit_results.out',
    wave_headings=np.array([0, 45, 90, 135, 180])
)
```

### Application 2: Motion Prediction in Irregular Seas

```python
def predict_vessel_motions_irregular_seas(
    Hs: float,
    Tp: float,
    heading: float,
    rao_data: dict,
    duration: float = 3600
) -> dict:
    """
    Predict vessel motions in irregular seas.

    Args:
        Hs: Significant wave height (m)
        Tp: Peak period (s)
        heading: Wave heading (degrees)
        rao_data: RAO dictionary from BEM analysis
        duration: Simulation duration (s)

    Returns:
        Motion statistics
    """
    # Frequency array
    freq_hz = np.linspace(0.01, 0.5, 500)
    omega = 2 * np.pi * freq_hz

    # Wave spectrum
    S_wave = jonswap_spectrum(freq_hz, Hs, Tp)

    # Calculate response spectra
    dof_names = ['Surge', 'Sway', 'Heave', 'Roll', 'Pitch', 'Yaw']
    motion_stats = {}

    for dof in dof_names:
        # Get RAO for this heading and DOF
        # Simplified: use constant RAO
        rao_amplitude = np.interp(
            omega,
            np.linspace(0.1, 2.0, 50),
            rao_data.get((heading, dof), np.zeros(50))
        )

        # Response spectrum
        S_response, stats = calculate_response_spectrum(S_wave, rao_amplitude, freq_hz)

        motion_stats[dof] = {
            'std_dev': stats['std_dev'],
            'significant_amplitude': stats['significant_amplitude'],
            'max_expected': stats['significant_amplitude'] * 1.86  # Rayleigh distribution
        }

    return motion_stats

# Example
motion_predictions = predict_vessel_motions_irregular_seas(
    Hs=8.5,
    Tp=12.0,
    heading=0,  # Head seas
    rao_data=rao_results,
    duration=10800  # 3 hours
)

print("Predicted Motion Statistics:")
for dof, stats in motion_predictions.items():
    print(f"{dof}:")
    print(f"  Significant amplitude: {stats['significant_amplitude']:.2f}")
    print(f"  Max expected (3hr): {stats['max_expected']:.2f}")
```

### Application 3: Added Mass Convergence Check

```python
def check_added_mass_convergence(
    panel_counts: list,
    added_mass_results: list
) -> dict:
    """
    Check convergence of added mass with panel count.

    Args:
        panel_counts: List of panel counts
        added_mass_results: List of 6x6 added mass matrices

    Returns:
        Convergence assessment
    """
    import plotly.graph_objects as go

    # Check heave added mass convergence
    A33_values = [A[2, 2] for A in added_mass_results]

    # Calculate relative change
    relative_changes = [
        abs(A33_values[i] - A33_values[i-1]) / A33_values[i-1] * 100
        for i in range(1, len(A33_values))
    ]

    # Plot convergence
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=panel_counts,
        y=A33_values,
        name='A33 (Heave Added Mass)',
        mode='lines+markers'
    ))

    fig.update_layout(
        title='Added Mass Convergence Study',
        xaxis_title='Panel Count',
        yaxis_title='A33 (tonnes)',
        hovermode='x unified'
    ))

    fig.write_html('reports/added_mass_convergence.html')

    # Convergence criteria: < 1% change
    converged = relative_changes[-1] < 1.0 if relative_changes else False

    return {
        'converged': converged,
        'final_value': A33_values[-1],
        'relative_change_percent': relative_changes[-1] if relative_changes else 0,
        'recommended_panels': panel_counts[-1] if converged else 'Increase further'
    }

# Example
panel_counts = [1000, 2000, 5000, 10000, 15000]
A_results = [
    np.diag([15000, 15000, 45000, 1e6, 1e6, 5e5]),
    np.diag([15000, 15000, 48000, 1e6, 1e6, 5e5]),
    np.diag([15000, 15000, 49500, 1e6, 1e6, 5e5]),
    np.diag([15000, 15000, 50000, 1e6, 1e6, 5e5]),
    np.diag([15000, 15000, 50100, 1e6, 1e6, 5e5])
]

convergence = check_added_mass_convergence(panel_counts, A_results)
print(f"Converged: {convergence['converged']}")
print(f"Recommended panels: {convergence['recommended_panels']}")
```

## Integration with Software

### WAMIT Workflow

```yaml
wamit_workflow:
  step_1_geometry:
    tool: "Rhino, GHS, or MultiSurf"
    output: "geometry.gdf"
    requirements:
      - "Waterline at z=0"
      - "Wetted surface only"
      - "Right-hand coordinate system"

  step_2_panel_mesh:
    tool: "WAMIT-PGEN or Multisurf"
    output: "vessel.gdf"
    quality_checks:
      - "Panel aspect ratio < 3:1"
      - "Panel size < λ/6"
      - "Use symmetry if applicable"

  step_3_run_wamit:
    input_files:
      - "vessel.frc"  # Force control
      - "vessel.pot"  # Potential control
      - "vessel.gdf"  # Geometry
    output_files:
      - "vessel.out"  # Main output
      - "vessel.1"    # Added mass/damping
      - "vessel.3"    # Wave excitation

  step_4_post_processing:
    tools:
      - "WAMIT-VIEW"
      - "Python (read .1, .3 files)"
      - "OrcaFlex (import RAOs)"
```

### AQWA Workflow

```yaml
aqwa_workflow:
  step_1_geometry:
    tool: "ANSYS DesignModeler or SpaceClaim"
    output: "geometry.scdoc"

  step_2_mesh:
    tool: "AQWA-GS (meshing)"
    output: "vessel.anl"
    settings:
      element_size: "Auto or manual"
      symmetry: "Use if applicable"

  step_3_analysis:
    solver: "AQWA-NAUT or AQWA-LINE"
    analysis_types:
      - "Hydrodynamic diffraction"
      - "Response calculation"

  step_4_results:
    output: "vessel.LIS"
    exports:
      - "RAOs → CSV"
      - "Added mass/damping → CSV"
      - "OrcaFlex YML"
```

## Resources

- **WAMIT User Manual**: https://www.wamit.com/
- **AQWA Documentation**: ANSYS Help System
- **OrcaWave Manual**: Orcina documentation
- **DNV-RP-C205**: Environmental Conditions and Environmental Loads
- **DNV-RP-H103**: Modelling and Analysis of Marine Operations
- **Lloyd's Register**: Guidance on wave loading

---

**Use this skill for all hydrodynamic analysis in DigitalModel!**
