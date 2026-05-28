---
name: ship-dynamics-6dof
version: 1.0.0
description: 6DOF ship dynamics, equations of motion, seakeeping analysis, and natural frequency calculations
author: workspace-hub
category: subject-matter-expert
tags: [6dof, ship-dynamics, seakeeping, equations-of-motion, natural-frequency, vessel-motions]
platforms: [engineering]
---

# Ship Dynamics (6DOF) SME Skill

Comprehensive 6 degrees of freedom ship dynamics expertise including equations of motion, seakeeping analysis, natural frequencies, and coupled motion analysis.

## When to Use This Skill

Use 6DOF ship dynamics when:
- **Equations of motion** - Set up and solve 6DOF coupled equations
- **Natural frequencies** - Calculate natural periods for all DOFs
- **Seakeeping analysis** - Predict vessel motions in waves
- **Coupled dynamics** - Analyze roll-heave-pitch coupling
- **Time-domain simulation** - Integrate equations of motion
- **Frequency-domain analysis** - RAO-based motion prediction

## Core Knowledge Areas

### 1. 6 Degrees of Freedom

**DOF Definition:**
```yaml
translations:
  surge:    # X-direction (longitudinal)
    positive: "Forward"
    typical_natural_period: "50-150 seconds"

  sway:     # Y-direction (lateral)
    positive: "Port"
    typical_natural_period: "50-150 seconds"

  heave:    # Z-direction (vertical)
    positive: "Upward"
    typical_natural_period: "6-15 seconds"

rotations:
  roll:     # Rotation about X-axis
    positive: "Starboard down"
    typical_natural_period: "15-30 seconds"

  pitch:    # Rotation about Y-axis
    positive: "Bow up"
    typical_natural_period: "6-12 seconds"

  yaw:      # Rotation about Z-axis
    positive: "Bow to starboard"
    typical_natural_period: "60-200 seconds"
```

### 2. Equations of Motion

**General Form:**
```
[M + A(ω)]{ẍ} + [B(ω)]{ẋ} + [C]{x} = {F(t)}

Where:
- [M] = Mass/inertia matrix (6x6)
- [A] = Added mass matrix (6x6, frequency-dependent)
- [B] = Damping matrix (6x6, frequency-dependent)
- [C] = Hydrostatic restoring matrix (6x6)
- {F} = External force vector (6x1)
- {x} = Displacement vector [surge, sway, heave, roll, pitch, yaw]
```

**Mass Matrix:**
```python
import numpy as np

def create_mass_matrix(
    mass: float,
    radii_of_gyration: dict,
    center_of_gravity: np.ndarray = None
) -> np.ndarray:
    """
    Create 6x6 mass matrix for vessel.

    Args:
        mass: Vessel mass (tonnes)
        radii_of_gyration: {'Rxx': roll, 'Ryy': pitch, 'Rzz': yaw} (m)
        center_of_gravity: [x, y, z] from origin (m)

    Returns:
        6x6 mass matrix
    """
    if center_of_gravity is None:
        center_of_gravity = np.zeros(3)

    xg, yg, zg = center_of_gravity

    # Convert to kg
    m = mass * 1000

    # Moments of inertia
    Ixx = m * radii_of_gyration['Rxx']**2  # Roll
    Iyy = m * radii_of_gyration['Ryy']**2  # Pitch
    Izz = m * radii_of_gyration['Rzz']**2  # Yaw

    # Mass matrix (including CG offset coupling)
    M = np.array([
        [m,  0,  0,    0,      m*zg,  -m*yg],
        [0,  m,  0,   -m*zg,   0,      m*xg],
        [0,  0,  m,    m*yg,  -m*xg,   0   ],
        [0, -m*zg, m*yg,  Ixx,    0,     0   ],
        [m*zg, 0, -m*xg,  0,     Iyy,    0   ],
        [-m*yg, m*xg, 0,  0,      0,     Izz ]
    ])

    return M

# Example: FPSO mass matrix
M_fpso = create_mass_matrix(
    mass=150000,  # tonnes
    radii_of_gyration={
        'Rxx': 22,   # Roll radius of gyration
        'Ryy': 95,   # Pitch radius of gyration
        'Rzz': 95    # Yaw radius of gyration
    },
    center_of_gravity=np.array([160, 0, 15])  # From aft perpendicular
)

print("Mass Matrix:")
print(M_fpso)
```

### 3. Natural Frequencies and Periods

**Uncoupled Natural Frequency:**
```python
def calculate_natural_frequency_uncoupled(
    mass: float,
    stiffness: float
) -> dict:
    """
    Calculate natural frequency for single DOF.

    ω_n = sqrt(K / M)
    T_n = 2π / ω_n

    Args:
        mass: Mass or moment of inertia
        stiffness: Stiffness or restoring coefficient

    Returns:
        Natural frequency and period
    """
    omega_n = np.sqrt(stiffness / mass)
    period_n = 2 * np.pi / omega_n
    frequency_hz = omega_n / (2 * np.pi)

    return {
        'omega_rad_s': omega_n,
        'frequency_hz': frequency_hz,
        'period_s': period_n
    }

# Example: Heave natural period
m = 150000 * 1000  # kg
A33 = 50000 * 1000  # Added mass in heave (kg)
K33 = 1025 * 9.81 * 15000  # Heave stiffness (N/m)

heave_freq = calculate_natural_frequency_uncoupled(
    mass=m + A33,
    stiffness=K33
)

print(f"Heave natural period: {heave_freq['period_s']:.2f} seconds")
```

**Coupled Natural Frequencies:**
```python
def calculate_coupled_natural_frequencies(
    mass_matrix: np.ndarray,
    stiffness_matrix: np.ndarray
) -> dict:
    """
    Calculate coupled natural frequencies from eigenvalue problem.

    det([K] - ω²[M]) = 0

    Args:
        mass_matrix: 6x6 mass matrix (including added mass)
        stiffness_matrix: 6x6 stiffness matrix

    Returns:
        Natural frequencies for all modes
    """
    # Solve generalized eigenvalue problem
    eigenvalues, eigenvectors = np.linalg.eig(
        np.linalg.solve(mass_matrix, stiffness_matrix)
    )

    # Natural frequencies
    omega_n = np.sqrt(eigenvalues.real)
    periods = 2 * np.pi / omega_n

    # Sort by period
    sort_idx = np.argsort(periods)
    periods = periods[sort_idx]
    omega_n = omega_n[sort_idx]
    eigenvectors = eigenvectors[:, sort_idx]

    dof_names = ['Surge', 'Sway', 'Heave', 'Roll', 'Pitch', 'Yaw']

    return {
        'periods_s': periods,
        'frequencies_rad_s': omega_n,
        'frequencies_hz': omega_n / (2*np.pi),
        'mode_shapes': eigenvectors,
        'dof_names': dof_names
    }

# Example
M_total = M_fpso + np.diag([15000e3, 15000e3, 50000e3, 1e9, 1e9, 5e8])  # With added mass
K = np.diag([0, 0, 150e6, 5e9, 8e9, 0])  # Hydrostatic stiffness

natural_freq = calculate_coupled_natural_frequencies(M_total, K)

print("Natural Periods:")
for i, (dof, T) in enumerate(zip(natural_freq['dof_names'], natural_freq['periods_s'])):
    print(f"  {dof}: {T:.2f} seconds")
```

### 4. Hydrostatic Restoring

**Complete Stiffness Matrix:**
```python
def calculate_complete_hydrostatic_stiffness(
    rho: float,
    g: float,
    displacement: float,
    waterplane_area: float,
    waterplane_inertia: dict,
    center_of_buoyancy: np.ndarray,
    center_of_gravity: np.ndarray,
    metacentric_height: dict
) -> np.ndarray:
    """
    Calculate complete 6x6 hydrostatic stiffness matrix.

    Args:
        rho: Water density (kg/m³)
        g: Gravity (m/s²)
        displacement: Volume displacement (m³)
        waterplane_area: Waterplane area (m²)
        waterplane_inertia: {'Ixx': Ixx, 'Iyy': Iyy} second moments (m⁴)
        center_of_buoyancy: [xb, yb, zb] (m)
        center_of_gravity: [xg, yg, zg] (m)
        metacentric_height: {'GMT': transverse, 'GML': longitudinal} (m)

    Returns:
        6x6 hydrostatic stiffness matrix
    """
    xb, yb, zb = center_of_buoyancy
    xg, yg, zg = center_of_gravity

    C = np.zeros((6, 6))

    # C33: Heave stiffness
    C[2, 2] = rho * g * waterplane_area

    # C44: Roll stiffness
    C[3, 3] = rho * g * displacement * metacentric_height['GMT']

    # C55: Pitch stiffness
    C[4, 4] = rho * g * displacement * metacentric_height['GML']

    # Coupling terms
    # C35, C53: Heave-pitch
    C[2, 4] = -rho * g * waterplane_area * xb
    C[4, 2] = C[2, 4]

    # C34, C43: Heave-roll
    C[2, 3] = -rho * g * waterplane_area * yb
    C[3, 2] = C[2, 3]

    # C45, C54: Roll-pitch
    C[3, 4] = -rho * g * displacement * (zg - zb)
    C[4, 3] = C[3, 4]

    return C

# Example: FPSO hydrostatic stiffness
C_hydro = calculate_complete_hydrostatic_stiffness(
    rho=1025,
    g=9.81,
    displacement=150000,  # m³
    waterplane_area=15000,  # m²
    waterplane_inertia={'Ixx': 5e5, 'Iyy': 3e7},  # m⁴
    center_of_buoyancy=np.array([160, 0, -10]),
    center_of_gravity=np.array([160, 0, 15]),
    metacentric_height={'GMT': 3.0, 'GML': 5.0}
)

print("Hydrostatic Stiffness Matrix (diagonal terms):")
print(np.diag(C_hydro))
```

### 5. Time-Domain Simulation

**Newmark-Beta Integration:**
```python
def newmark_beta_integration(
    M: np.ndarray,
    C: np.ndarray,
    K: np.ndarray,
    F_t: np.ndarray,
    x0: np.ndarray,
    v0: np.ndarray,
    t: np.ndarray,
    beta: float = 0.25,
    gamma: float = 0.5
) -> dict:
    """
    Newmark-Beta time integration for 6DOF dynamics.

    Args:
        M: Mass matrix (6x6)
        C: Damping matrix (6x6)
        K: Stiffness matrix (6x6)
        F_t: Force time series (n_steps x 6)
        x0: Initial displacement (6,)
        v0: Initial velocity (6,)
        t: Time array
        beta: Newmark beta parameter (0.25 = const accel)
        gamma: Newmark gamma parameter (0.5)

    Returns:
        Dictionary with motion time series
    """
    n_steps = len(t)
    dt = t[1] - t[0]

    # Initialize
    x = np.zeros((n_steps, 6))
    v = np.zeros((n_steps, 6))
    a = np.zeros((n_steps, 6))

    x[0] = x0
    v[0] = v0

    # Initial acceleration
    a[0] = np.linalg.solve(M, F_t[0] - C @ v[0] - K @ x[0])

    # Effective stiffness
    K_eff = K + gamma/(beta*dt) * C + 1/(beta*dt**2) * M

    # Time stepping
    for i in range(n_steps - 1):
        # Effective force
        F_eff = (
            F_t[i+1] +
            M @ (x[i]/(beta*dt**2) + v[i]/(beta*dt) + (0.5/beta - 1)*a[i]) +
            C @ (gamma/(beta*dt)*x[i] + (gamma/beta - 1)*v[i] + dt*(gamma/(2*beta) - 1)*a[i])
        )

        # Solve for displacement
        x[i+1] = np.linalg.solve(K_eff, F_eff)

        # Update velocity and acceleration
        a[i+1] = (x[i+1] - x[i])/(beta*dt**2) - v[i]/(beta*dt) - (0.5/beta - 1)*a[i]
        v[i+1] = v[i] + dt*((1-gamma)*a[i] + gamma*a[i+1])

    return {
        'time': t,
        'displacement': x,
        'velocity': v,
        'acceleration': a
    }

# Example: Simulate heave response to wave force
t = np.linspace(0, 100, 10000)
dt = t[1] - t[0]

# Simplified system (heave only)
M_simple = np.diag([0, 0, 200e6, 0, 0, 0])  # Heave mass
C_simple = np.diag([0, 0, 100e6, 0, 0, 0])  # Heave damping
K_simple = np.diag([0, 0, 150e6, 0, 0, 0])  # Heave stiffness

# Wave force (10s period, 1 MN amplitude)
F = np.zeros((len(t), 6))
F[:, 2] = 1e6 * np.sin(2*np.pi*t / 10)

# Simulate
result = newmark_beta_integration(
    M_simple, C_simple, K_simple, F,
    x0=np.zeros(6), v0=np.zeros(6), t=t
)

print(f"Max heave: {np.max(np.abs(result['displacement'][:, 2])):.2f} m")
```

### 6. Seakeeping Analysis

**Motion Statistics:**
```python
def calculate_seakeeping_statistics(
    motion_time_series: np.ndarray,
    dt: float,
    dof_name: str = "Motion"
) -> dict:
    """
    Calculate seakeeping statistics from motion time series.

    Args:
        motion_time_series: Time series of motion
        dt: Time step
        dof_name: Name of DOF

    Returns:
        Statistical parameters
    """
    # Basic statistics
    mean = np.mean(motion_time_series)
    std = np.std(motion_time_series)

    # Significant amplitude (1/3 highest)
    sorted_amplitudes = np.sort(np.abs(motion_time_series))
    n_third = len(sorted_amplitudes) // 3
    significant_amplitude = np.mean(sorted_amplitudes[-n_third:])

    # Maximum
    max_amplitude = np.max(np.abs(motion_time_series))

    # Zero crossing period
    zero_crossings = np.where(np.diff(np.sign(motion_time_series)))[0]
    if len(zero_crossings) > 1:
        Tz = np.mean(np.diff(zero_crossings)) * dt * 2  # Up and down
    else:
        Tz = np.nan

    # RMS
    rms = np.sqrt(np.mean(motion_time_series**2))

    return {
        'dof': dof_name,
        'mean': mean,
        'std_dev': std,
        'rms': rms,
        'significant_amplitude': significant_amplitude,
        'max_amplitude': max_amplitude,
        'zero_crossing_period': Tz
    }

# Example
heave_motion = result['displacement'][:, 2]
heave_stats = calculate_seakeeping_statistics(heave_motion, dt, 'Heave')

print(f"Heave Statistics:")
print(f"  Significant amplitude: {heave_stats['significant_amplitude']:.2f} m")
print(f"  Max amplitude: {heave_stats['max_amplitude']:.2f} m")
print(f"  Zero-crossing period: {heave_stats['zero_crossing_period']:.2f} s")
```

**Motion Sickness Incidence (MSI):**
```python
def calculate_motion_sickness_incidence(
    acceleration_rms: float,
    frequency_hz: float,
    duration_hours: float = 2
) -> float:
    """
    Calculate Motion Sickness Incidence (MSI) using ISO 2631-1.

    MSI = % of people experiencing motion sickness

    Args:
        acceleration_rms: RMS vertical acceleration (m/s²)
        frequency_hz: Dominant frequency (Hz)
        duration_hours: Exposure duration (hours)

    Returns:
        MSI percentage
    """
    # Weighting factor (ISO 2631-1)
    # Peak sensitivity at 0.16 Hz
    if 0.1 <= frequency_hz <= 0.5:
        weighting = 1.0
    else:
        weighting = 0.5

    # Weighted acceleration
    a_w = acceleration_rms * weighting

    # Time factor
    time_factor = (duration_hours / 2) ** 0.5

    # MSI calculation (simplified O'Hanlon-McCauley)
    msdv = a_w * time_factor  # Motion Sickness Dose Value

    # Convert to percentage (empirical correlation)
    MSI = 100 * (1 / (1 + np.exp(-(msdv - 3.5) / 0.7)))

    return MSI

# Example: Calculate MSI for heave acceleration
a_heave = np.std(np.diff(result['velocity'][:, 2]) / dt)
freq_heave = 1 / heave_stats['zero_crossing_period']

msi = calculate_motion_sickness_incidence(a_heave, freq_heave, duration_hours=2)
print(f"Motion Sickness Incidence (2 hours): {msi:.1f}%")
```

## Complete Examples

### Example 1: Full 6DOF Simulation

```python
def simulate_vessel_6dof_in_waves(
    vessel_properties: dict,
    wave_conditions: dict,
    duration: float = 3600,
    dt: float = 0.1
) -> dict:
    """
    Complete 6DOF vessel simulation in irregular waves.

    Args:
        vessel_properties: Vessel mass, stiffness, damping
        wave_conditions: Hs, Tp, heading
        duration: Simulation duration (s)
        dt: Time step (s)

    Returns:
        Complete motion results
    """
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    # Time array
    t = np.arange(0, duration, dt)
    n_steps = len(t)

    # Extract properties
    M = vessel_properties['mass_matrix']
    C_damp = vessel_properties['damping_matrix']
    K = vessel_properties['stiffness_matrix']

    # Generate wave forces (simplified JONSWAP spectrum)
    Hs = wave_conditions['Hs']
    Tp = wave_conditions['Tp']
    heading = wave_conditions['heading']  # degrees

    # Wave force time series (simplified)
    omega_p = 2 * np.pi / Tp
    F_wave = np.zeros((n_steps, 6))

    # Generate forces for each DOF based on heading
    if heading == 0:  # Head seas
        F_wave[:, 0] = Hs * 1e5 * np.sin(omega_p * t)  # Surge
        F_wave[:, 2] = Hs * 5e5 * np.sin(omega_p * t)  # Heave
        F_wave[:, 4] = Hs * 1e6 * np.sin(omega_p * t)  # Pitch
    elif heading == 90:  # Beam seas
        F_wave[:, 1] = Hs * 1e5 * np.sin(omega_p * t)  # Sway
        F_wave[:, 3] = Hs * 2e6 * np.sin(omega_p * t)  # Roll

    # Add random component for irregular seas
    for i in range(6):
        F_wave[:, i] += np.random.randn(n_steps) * 0.2 * np.std(F_wave[:, i])

    # Run simulation
    result = newmark_beta_integration(
        M, C_damp, K, F_wave,
        x0=np.zeros(6), v0=np.zeros(6), t=t
    )

    # Calculate statistics for all DOFs
    dof_names = ['Surge', 'Sway', 'Heave', 'Roll', 'Pitch', 'Yaw']
    statistics = {}

    for i, dof in enumerate(dof_names):
        statistics[dof] = calculate_seakeeping_statistics(
            result['displacement'][:, i], dt, dof
        )

    # Create visualization
    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=dof_names
    )

    for i, dof in enumerate(dof_names):
        row = i // 3 + 1
        col = i % 3 + 1

        fig.add_trace(
            go.Scatter(
                x=t,
                y=result['displacement'][:, i],
                name=dof,
                showlegend=False
            ),
            row=row, col=col
        )

    fig.update_layout(
        title=f'6DOF Vessel Motions (Hs={Hs}m, Tp={Tp}s, Heading={heading}°)',
        height=800
    )

    fig.write_html('reports/6dof_simulation.html')

    return {
        'time': t,
        'motions': result,
        'statistics': statistics,
        'wave_conditions': wave_conditions
    }

# Example usage
vessel = {
    'mass_matrix': M_fpso,
    'damping_matrix': np.diag([50e6, 50e6, 100e6, 5e8, 5e8, 2e8]),
    'stiffness_matrix': C_hydro
}

waves = {
    'Hs': 8.5,
    'Tp': 12.0,
    'heading': 0  # Head seas
}

results = simulate_vessel_6dof_in_waves(vessel, waves, duration=600, dt=0.1)

print("Motion Statistics:")
for dof, stats in results['statistics'].items():
    print(f"{dof}: Sig = {stats['significant_amplitude']:.2f}, Max = {stats['max_amplitude']:.2f}")
```

### Example 2: Natural Frequency Sensitivity Study

```python
def natural_frequency_sensitivity_study(
    base_properties: dict,
    parameter_ranges: dict
) -> dict:
    """
    Sensitivity study of natural frequencies to design parameters.

    Args:
        base_properties: Base vessel properties
        parameter_ranges: Parameters to vary

    Returns:
        Sensitivity results
    """
    import plotly.graph_objects as go

    results = {}

    for param_name, param_values in parameter_ranges.items():
        natural_periods = []

        for value in param_values:
            # Update property
            props = base_properties.copy()

            if param_name == 'GMT':
                # Update roll stiffness
                props['K'][3, 3] *= value / base_properties['GMT']
            elif param_name == 'Rxx':
                # Update roll inertia
                m = props['M'][0, 0]
                props['M'][3, 3] = m * value**2

            # Calculate natural frequencies
            freq_result = calculate_coupled_natural_frequencies(
                props['M'], props['K']
            )

            natural_periods.append(freq_result['periods_s'][3])  # Roll period

        results[param_name] = {
            'values': param_values,
            'roll_periods': natural_periods
        }

    # Plot sensitivity
    fig = go.Figure()

    for param_name, data in results.items():
        fig.add_trace(go.Scatter(
            x=data['values'],
            y=data['roll_periods'],
            name=param_name,
            mode='lines+markers'
        ))

    fig.update_layout(
        title='Roll Natural Period Sensitivity',
        xaxis_title='Parameter Value',
        yaxis_title='Roll Natural Period (s)'
    )

    fig.write_html('reports/sensitivity_analysis.html')

    return results

# Example
base = {
    'M': M_fpso,
    'K': C_hydro,
    'GMT': 3.0
}

param_ranges = {
    'GMT': np.linspace(1.0, 5.0, 20),  # m
    'Rxx': np.linspace(18, 26, 20)     # m
}

sensitivity = natural_frequency_sensitivity_study(base, param_ranges)
```

## Resources

- **Principles of Naval Architecture**: SNAME
- **Ship Hydrostatics and Stability**: Adrian Biran
- **Seakeeping: Ship Behaviour in Rough Weather**: A.R.J.M. Lloyd
- **DNV-RP-C205**: Environmental Conditions and Environmental Loads
- **ISO 2631-1**: Mechanical vibration and shock

---

**Use this skill for all 6DOF dynamics analysis in DigitalModel!**
