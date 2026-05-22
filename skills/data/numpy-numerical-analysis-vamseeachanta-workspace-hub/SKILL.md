---
name: numpy-numerical-analysis
version: 1.0.0
description: NumPy for matrix operations, FFT, linear algebra, and numerical computations in marine engineering
author: workspace-hub
category: programming
tags: [numpy, numerical-analysis, matrix-operations, fft, linear-algebra, engineering]
platforms: [python]
---

# NumPy Numerical Analysis Skill

Master NumPy for efficient numerical computations, matrix operations, FFT analysis, and linear algebra in marine and offshore engineering applications.

## When to Use This Skill

Use NumPy numerical analysis when you need:
- **Matrix operations** - 6DOF equations of motion, mass matrices, stiffness matrices
- **FFT analysis** - Frequency domain analysis, spectral density, response spectra
- **Linear algebra** - Solve linear systems, eigenvalue analysis, matrix decomposition
- **Array operations** - Efficient computations on large datasets
- **Numerical integration** - Time-stepping, ODE solvers
- **Signal processing** - Filtering, windowing, convolution

**Avoid when:**
- Symbolic mathematics needed (use SymPy)
- Sparse matrices dominate (use SciPy sparse)
- GPU acceleration required (use CuPy or JAX)
- Distributed computing needed (use Dask)

## Core Capabilities

### 1. Array Creation and Operations

**Array Creation:**
```python
import numpy as np

# Create arrays
zeros = np.zeros((3, 3))
ones = np.ones((3, 3))
identity = np.eye(3)
arange = np.arange(0, 10, 0.1)  # 0 to 10 with step 0.1
linspace = np.linspace(0, 10, 100)  # 100 points from 0 to 10

# From list
arr = np.array([1, 2, 3, 4, 5])

# Multi-dimensional
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])

# Random arrays
random_uniform = np.random.rand(3, 3)  # Uniform [0, 1)
random_normal = np.random.randn(3, 3)  # Standard normal
random_int = np.random.randint(0, 100, size=(3, 3))
```

**Array Operations:**
```python
# Element-wise operations
a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])

c = a + b  # [11, 22, 33, 44, 55]
d = a * b  # [10, 40, 90, 160, 250]
e = a ** 2  # [1, 4, 9, 16, 25]

# Mathematical functions
sin_a = np.sin(a)
cos_a = np.cos(a)
exp_a = np.exp(a)
log_a = np.log(a)
sqrt_a = np.sqrt(a)

# Statistical operations
mean = np.mean(a)
std = np.std(a)
var = np.var(a)
min_val = np.min(a)
max_val = np.max(a)
```

### 2. Matrix Operations

**Matrix Multiplication:**
```python
def compute_force_response(
    mass_matrix: np.ndarray,
    stiffness_matrix: np.ndarray,
    force_vector: np.ndarray
) -> np.ndarray:
    """
    Compute structural response: F = K * x
    Solve for displacement: x = K^-1 * F

    Args:
        mass_matrix: Mass matrix [M]
        stiffness_matrix: Stiffness matrix [K]
        force_vector: Applied force vector {F}

    Returns:
        Displacement vector {x}
    """
    # Static response (ignoring mass for now)
    displacement = np.linalg.solve(stiffness_matrix, force_vector)

    return displacement

# Example: 3DOF spring-mass system
K = np.array([
    [200, -100, 0],
    [-100, 200, -100],
    [0, -100, 100]
])  # Stiffness matrix (N/m)

F = np.array([1000, 0, 0])  # Force at first node (N)

x = compute_force_response(None, K, F)
print(f"Displacements: {x} m")
```

**Matrix Properties:**
```python
def analyze_matrix_properties(matrix: np.ndarray) -> dict:
    """
    Analyze matrix properties for structural analysis.

    Args:
        matrix: Input matrix (mass or stiffness)

    Returns:
        Dictionary with matrix properties
    """
    properties = {}

    # Determinant
    properties['determinant'] = np.linalg.det(matrix)

    # Condition number (numerical stability indicator)
    properties['condition_number'] = np.linalg.cond(matrix)

    # Rank
    properties['rank'] = np.linalg.matrix_rank(matrix)

    # Eigenvalues and eigenvectors
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    properties['eigenvalues'] = eigenvalues
    properties['eigenvectors'] = eigenvectors

    # Is symmetric?
    properties['is_symmetric'] = np.allclose(matrix, matrix.T)

    # Is positive definite? (all eigenvalues > 0)
    properties['is_positive_definite'] = np.all(eigenvalues > 0)

    return properties

# Example: Check stiffness matrix properties
K = np.array([
    [200, -100, 0],
    [-100, 200, -100],
    [0, -100, 100]
])

props = analyze_matrix_properties(K)
print(f"Determinant: {props['determinant']:.2f}")
print(f"Condition number: {props['condition_number']:.2f}")
print(f"Eigenvalues: {props['eigenvalues']}")
print(f"Positive definite: {props['is_positive_definite']}")
```

### 3. 6DOF Equations of Motion

**6DOF Dynamics:**
```python
def solve_6dof_equation_of_motion(
    mass_matrix: np.ndarray,
    damping_matrix: np.ndarray,
    stiffness_matrix: np.ndarray,
    force_vector: np.ndarray,
    displacement: np.ndarray,
    velocity: np.ndarray,
    dt: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Solve 6DOF equation of motion using Newmark-Beta method.

    [M]{ẍ} + [C]{ẋ} + [K]{x} = {F}

    Args:
        mass_matrix: 6x6 mass matrix [M]
        damping_matrix: 6x6 damping matrix [C]
        stiffness_matrix: 6x6 stiffness matrix [K]
        force_vector: 6x1 force vector {F}
        displacement: Current displacement {x_n}
        velocity: Current velocity {ẋ_n}
        dt: Time step

    Returns:
        (acceleration, velocity, displacement) at next time step
    """
    # Newmark-Beta parameters
    beta = 0.25  # Constant average acceleration
    gamma = 0.5

    # Effective stiffness
    K_eff = (
        mass_matrix / (beta * dt**2) +
        damping_matrix * gamma / (beta * dt) +
        stiffness_matrix
    )

    # Effective force at next time step
    F_eff = (
        force_vector +
        mass_matrix @ (
            displacement / (beta * dt**2) +
            velocity / (beta * dt)
        ) +
        damping_matrix @ (
            displacement * gamma / (beta * dt) -
            velocity * (1 - gamma / beta)
        )
    )

    # Solve for displacement at next time step
    displacement_next = np.linalg.solve(K_eff, F_eff)

    # Calculate velocity at next time step
    velocity_next = (
        gamma / (beta * dt) * (displacement_next - displacement) +
        (1 - gamma / beta) * velocity
    )

    # Calculate acceleration at next time step
    acceleration_next = (
        (displacement_next - displacement) / (beta * dt**2) -
        velocity / (beta * dt)
    )

    return acceleration_next, velocity_next, displacement_next

# Example: Single time step for floating vessel
M = np.diag([100000, 100000, 100000, 5e6, 5e6, 5e6])  # Mass matrix
C = np.diag([50000, 50000, 50000, 2e5, 2e5, 2e5])    # Damping
K = np.diag([1000, 1000, 2000, 5e4, 5e4, 1e4])       # Restoring

F = np.array([1e6, 0, 0, 0, 0, 0])  # Surge force 1 MN
x = np.zeros(6)  # Initial displacement
v = np.zeros(6)  # Initial velocity

a, v_new, x_new = solve_6dof_equation_of_motion(M, C, K, F, x, v, dt=0.01)

print(f"Acceleration: {a}")
print(f"Velocity: {v_new}")
print(f"Displacement: {x_new}")
```

### 4. FFT and Frequency Analysis

**FFT for Spectral Analysis:**
```python
def compute_fft_spectrum(
    time_series: np.ndarray,
    dt: float,
    window: str = 'hann'
) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute FFT spectrum of time series.

    Args:
        time_series: Time series data
        dt: Time step
        window: Window function ('hann', 'hamming', 'blackman')

    Returns:
        (frequencies, amplitude_spectrum)
    """
    n = len(time_series)

    # Apply window
    if window == 'hann':
        windowed = time_series * np.hanning(n)
    elif window == 'hamming':
        windowed = time_series * np.hamming(n)
    elif window == 'blackman':
        windowed = time_series * np.blackman(n)
    else:
        windowed = time_series

    # Compute FFT
    fft_result = np.fft.fft(windowed)

    # Compute frequencies
    frequencies = np.fft.fftfreq(n, d=dt)

    # Amplitude spectrum (single-sided)
    amplitude = np.abs(fft_result)[:n//2] * 2 / n
    frequencies_positive = frequencies[:n//2]

    return frequencies_positive, amplitude

# Example: Analyze wave elevation time series
import numpy as np

# Generate sample wave elevation (3 components)
t = np.linspace(0, 100, 10000)  # 100 seconds, 10000 points
dt = t[1] - t[0]

# Wave components: 6s, 8s, 10s periods
wave = (
    2.0 * np.sin(2*np.pi*t / 6) +
    1.5 * np.sin(2*np.pi*t / 8) +
    1.0 * np.sin(2*np.pi*t / 10)
)

# Add noise
wave += 0.2 * np.random.randn(len(t))

# Compute spectrum
freq, amplitude = compute_fft_spectrum(wave, dt, window='hann')

# Find peaks
peak_indices = np.argsort(amplitude)[-3:]  # Top 3 peaks
peak_frequencies = freq[peak_indices]
peak_periods = 1 / peak_frequencies

print("Detected wave periods:")
for period in sorted(peak_periods, reverse=True):
    print(f"  T = {period:.2f} s")
```

**Power Spectral Density:**
```python
def compute_power_spectral_density(
    time_series: np.ndarray,
    dt: float,
    nfft: int = None
) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute power spectral density using Welch's method.

    Args:
        time_series: Time series data
        dt: Time step
        nfft: FFT length (None = length of time series)

    Returns:
        (frequencies, PSD)
    """
    from scipy import signal

    # Compute PSD using Welch's method
    frequencies, psd = signal.welch(
        time_series,
        fs=1/dt,
        nperseg=nfft or len(time_series)//8,
        window='hann'
    )

    return frequencies, psd

# Example: Wave spectral analysis
t = np.linspace(0, 3600, 36000)  # 1 hour, 10 Hz sampling
dt = t[1] - t[0]

# JONSWAP spectrum simulation (simplified)
wave_elevation = np.random.randn(len(t)) * 2.0  # Simplified

freq, psd = compute_power_spectral_density(wave_elevation, dt)

# Calculate Hs from PSD
m0 = np.trapz(psd, freq)  # Zero-order moment
Hs = 4 * np.sqrt(m0)

print(f"Significant wave height: {Hs:.2f} m")
```

### 5. Linear Algebra Operations

**Eigenvalue Analysis:**
```python
def natural_frequency_analysis(
    mass_matrix: np.ndarray,
    stiffness_matrix: np.ndarray
) -> dict:
    """
    Perform eigenvalue analysis to find natural frequencies and mode shapes.

    [K]{ϕ} = ω²[M]{ϕ}

    Args:
        mass_matrix: Mass matrix [M]
        stiffness_matrix: Stiffness matrix [K]

    Returns:
        Dictionary with natural frequencies and mode shapes
    """
    # Solve generalized eigenvalue problem
    eigenvalues, eigenvectors = np.linalg.eig(
        np.linalg.solve(mass_matrix, stiffness_matrix)
    )

    # Natural frequencies (rad/s)
    natural_frequencies_rad = np.sqrt(eigenvalues)

    # Natural frequencies (Hz)
    natural_frequencies_hz = natural_frequencies_rad / (2 * np.pi)

    # Sort by frequency
    sort_indices = np.argsort(natural_frequencies_hz)
    natural_frequencies_hz = natural_frequencies_hz[sort_indices]
    eigenvectors = eigenvectors[:, sort_indices]

    # Periods
    periods = 1 / natural_frequencies_hz

    return {
        'frequencies_hz': natural_frequencies_hz,
        'frequencies_rad_s': natural_frequencies_rad[sort_indices],
        'periods_s': periods,
        'mode_shapes': eigenvectors
    }

# Example: FPSO natural frequencies
# 6DOF system
M = np.diag([150000, 150000, 150000, 1e7, 1e7, 5e6])  # Mass matrix (tonnes, tonne-m²)
K = np.diag([500, 500, 3000, 5e5, 5e5, 1e5])          # Stiffness (kN/m, kN-m/rad)

results = natural_frequency_analysis(M, K)

print("Natural Frequencies:")
for i, (freq, period) in enumerate(zip(results['frequencies_hz'], results['periods_s'])):
    dof_names = ['Surge', 'Sway', 'Heave', 'Roll', 'Pitch', 'Yaw']
    print(f"  Mode {i+1} ({dof_names[i]}): f = {freq:.4f} Hz, T = {period:.2f} s")
```

**Matrix Decomposition:**
```python
def lu_decomposition_solve(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Solve linear system using LU decomposition.

    Args:
        A: Coefficient matrix
        b: Right-hand side vector

    Returns:
        Solution vector x
    """
    from scipy.linalg import lu

    # LU decomposition
    P, L, U = lu(A)

    # Solve Ly = Pb
    y = np.linalg.solve(L, P @ b)

    # Solve Ux = y
    x = np.linalg.solve(U, y)

    return x

# Example
A = np.array([[4, -1, 0],
              [-1, 4, -1],
              [0, -1, 3]])
b = np.array([15, 10, 10])

x = lu_decomposition_solve(A, b)
print(f"Solution: {x}")
```

### 6. Numerical Integration

**Time-Stepping Integration:**
```python
def runge_kutta_4th_order(
    derivative_func,
    y0: np.ndarray,
    t: np.ndarray
) -> np.ndarray:
    """
    4th-order Runge-Kutta integration.

    Args:
        derivative_func: Function dy/dt = f(t, y)
        y0: Initial conditions
        t: Time array

    Returns:
        Solution array
    """
    n = len(t)
    y = np.zeros((n, len(y0)))
    y[0] = y0

    for i in range(n - 1):
        dt = t[i+1] - t[i]

        k1 = derivative_func(t[i], y[i])
        k2 = derivative_func(t[i] + dt/2, y[i] + k1*dt/2)
        k3 = derivative_func(t[i] + dt/2, y[i] + k2*dt/2)
        k4 = derivative_func(t[i] + dt, y[i] + k3*dt)

        y[i+1] = y[i] + (dt/6) * (k1 + 2*k2 + 2*k3 + k4)

    return y

# Example: Simple harmonic oscillator
# m*x'' + k*x = 0
# y = [x, v], dy/dt = [v, -k/m*x]

def oscillator_derivatives(t, y):
    """Simple harmonic oscillator."""
    m = 1.0  # Mass
    k = 4.0  # Stiffness (omega = 2 rad/s, T = pi s)

    x, v = y
    dxdt = v
    dvdt = -k/m * x

    return np.array([dxdt, dvdt])

# Initial conditions
y0 = np.array([1.0, 0.0])  # x = 1, v = 0

# Time array
t = np.linspace(0, 10, 1000)

# Solve
solution = runge_kutta_4th_order(oscillator_derivatives, y0, t)

print(f"Final position: {solution[-1, 0]:.4f}")
print(f"Final velocity: {solution[-1, 1]:.4f}")
```

**Trapezoidal Integration:**
```python
def integrate_spectrum(
    frequencies: np.ndarray,
    spectral_density: np.ndarray
) -> float:
    """
    Integrate spectral density to get variance.

    m_0 = ∫ S(f) df

    Args:
        frequencies: Frequency array
        spectral_density: Spectral density array

    Returns:
        Integral (variance)
    """
    variance = np.trapz(spectral_density, frequencies)

    return variance

# Example: Calculate significant wave height from spectrum
freq = np.linspace(0.05, 0.5, 100)  # Hz
S = 10 * freq**(-5)  # Simplified spectrum

m0 = integrate_spectrum(freq, S)
Hs = 4 * np.sqrt(m0)

print(f"Significant wave height: {Hs:.2f} m")
```

## Complete Examples

### Example 1: 6DOF Time-Domain Simulation

```python
import numpy as np
import plotly.graph_objects as go

def simulate_6dof_vessel_motion(
    mass_matrix: np.ndarray,
    damping_matrix: np.ndarray,
    stiffness_matrix: np.ndarray,
    force_time_series: np.ndarray,
    time: np.ndarray
) -> dict:
    """
    Complete 6DOF time-domain simulation of vessel motion.

    Args:
        mass_matrix: 6x6 mass matrix
        damping_matrix: 6x6 damping matrix
        stiffness_matrix: 6x6 stiffness matrix
        force_time_series: Force time series (n_steps x 6)
        time: Time array

    Returns:
        Dictionary with motion time series
    """
    n_steps = len(time)
    dt = time[1] - time[0]

    # Initialize arrays
    displacement = np.zeros((n_steps, 6))
    velocity = np.zeros((n_steps, 6))
    acceleration = np.zeros((n_steps, 6))

    # Initial conditions (at rest)
    displacement[0] = np.zeros(6)
    velocity[0] = np.zeros(6)

    # Time-stepping loop
    for i in range(n_steps - 1):
        a, v, d = solve_6dof_equation_of_motion(
            mass_matrix,
            damping_matrix,
            stiffness_matrix,
            force_time_series[i],
            displacement[i],
            velocity[i],
            dt
        )

        acceleration[i+1] = a
        velocity[i+1] = v
        displacement[i+1] = d

    return {
        'time': time,
        'displacement': displacement,
        'velocity': velocity,
        'acceleration': acceleration
    }

# Define FPSO properties
M = np.diag([150000, 150000, 150000, 1e7, 1e7, 5e6])  # Mass
C = np.diag([50000, 50000, 100000, 5e5, 5e5, 2e5])    # Damping
K = np.diag([500, 500, 3000, 5e4, 5e4, 1e4])          # Stiffness

# Simulate wave forces (simplified)
time = np.linspace(0, 100, 10000)
dt = time[1] - time[0]

# Wave force in surge (1 MN amplitude, 10s period)
F = np.zeros((len(time), 6))
F[:, 0] = 1e6 * np.sin(2*np.pi*time / 10)

# Simulate
results = simulate_6dof_vessel_motion(M, C, K, F, time)

# Plot results
fig = go.Figure()

dof_names = ['Surge', 'Sway', 'Heave', 'Roll', 'Pitch', 'Yaw']
for i in range(3):  # Plot first 3 DOFs
    fig.add_trace(go.Scatter(
        x=results['time'],
        y=results['displacement'][:, i],
        name=dof_names[i],
        mode='lines'
    ))

fig.update_layout(
    title='Vessel Motion - Translation DOFs',
    xaxis_title='Time (s)',
    yaxis_title='Displacement (m)',
    hovermode='x unified'
)

fig.write_html('reports/vessel_motion_6dof.html')

# Print statistics
print("Motion Statistics:")
for i, name in enumerate(dof_names):
    print(f"{name}:")
    print(f"  Max: {np.max(np.abs(results['displacement'][:, i])):.3f}")
    print(f"  Std: {np.std(results['displacement'][:, i]):.3f}")
```

### Example 2: RAO Calculation from FFT

```python
def calculate_rao_from_time_series(
    wave_elevation: np.ndarray,
    vessel_response: np.ndarray,
    dt: float
) -> tuple[np.ndarray, np.ndarray]:
    """
    Calculate Response Amplitude Operator (RAO) from time series.

    RAO(ω) = |Response(ω)| / |Wave(ω)|

    Args:
        wave_elevation: Wave elevation time series
        vessel_response: Vessel response time series
        dt: Time step

    Returns:
        (frequencies, RAO)
    """
    # FFT of wave and response
    freq_wave, amplitude_wave = compute_fft_spectrum(wave_elevation, dt)
    freq_response, amplitude_response = compute_fft_spectrum(vessel_response, dt)

    # Calculate RAO
    # Avoid division by zero
    rao = np.where(
        amplitude_wave > 1e-6,
        amplitude_response / amplitude_wave,
        0
    )

    return freq_wave, rao

# Example: Calculate heave RAO
time = np.linspace(0, 100, 10000)
dt = time[1] - time[0]

# Regular wave (Hs = 2m, T = 8s)
wave = 1.0 * np.sin(2*np.pi*time / 8)

# Vessel heave response (with RAO ~1.5)
heave = 1.5 * np.sin(2*np.pi*time / 8 - np.pi/6)  # 30° phase lag

# Calculate RAO
freq, rao = calculate_rao_from_time_series(wave, heave, dt)

# Plot
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=freq,
    y=rao,
    name='Heave RAO',
    mode='lines'
))

fig.update_layout(
    title='Heave Response Amplitude Operator',
    xaxis_title='Frequency (Hz)',
    yaxis_title='RAO (m/m)',
    xaxis_range=[0, 0.5]
)

fig.write_html('reports/heave_rao.html')

# Find peak
peak_idx = np.argmax(rao[freq < 0.5])
peak_freq = freq[peak_idx]
peak_period = 1 / peak_freq

print(f"Peak RAO: {rao[peak_idx]:.2f} at T = {peak_period:.2f} s")
```

### Example 3: Mooring Stiffness Matrix

```python
def calculate_mooring_stiffness_matrix(
    num_lines: int,
    pretension: float,
    fairlead_radius: float,
    fairlead_depth: float,
    line_azimuth: np.ndarray,
    weight_per_length: float
) -> np.ndarray:
    """
    Calculate mooring system stiffness matrix.

    Args:
        num_lines: Number of mooring lines
        pretension: Pretension per line (kN)
        fairlead_radius: Horizontal distance from center to fairlead (m)
        fairlead_depth: Depth of fairlead below waterline (m)
        line_azimuth: Azimuth angle of each line (degrees)
        weight_per_length: Line weight per unit length (kN/m)

    Returns:
        6x6 mooring stiffness matrix
    """
    K_mooring = np.zeros((6, 6))

    # Individual line stiffness
    # Simplified: K_line = w * T / d
    k_line = weight_per_length * pretension / fairlead_depth

    for i in range(num_lines):
        theta = np.radians(line_azimuth[i])

        # Direction cosines
        cx = np.cos(theta)
        cy = np.sin(theta)

        # Surge-surge
        K_mooring[0, 0] += k_line * cx**2

        # Sway-sway
        K_mooring[1, 1] += k_line * cy**2

        # Surge-sway coupling
        K_mooring[0, 1] += k_line * cx * cy
        K_mooring[1, 0] += k_line * cx * cy

        # Yaw-yaw (moment = force * lever arm)
        K_mooring[5, 5] += k_line * fairlead_radius**2

        # Surge-yaw coupling
        K_mooring[0, 5] += k_line * fairlead_radius * cy
        K_mooring[5, 0] += k_line * fairlead_radius * cy

        # Sway-yaw coupling
        K_mooring[1, 5] -= k_line * fairlead_radius * cx
        K_mooring[5, 1] -= k_line * fairlead_radius * cx

    return K_mooring

# Example: 12-line spread mooring
num_lines = 12
azimuths = np.array([0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330])

K = calculate_mooring_stiffness_matrix(
    num_lines=12,
    pretension=2000,  # kN
    fairlead_radius=100,  # m
    fairlead_depth=25,  # m
    line_azimuth=azimuths,
    weight_per_length=1.2  # kN/m
)

print("Mooring Stiffness Matrix:")
print(K)

# Check symmetry
print(f"\nIs symmetric: {np.allclose(K, K.T)}")
```

### Example 4: Statistical Analysis of Extremes

```python
def extreme_value_statistics(
    data: np.ndarray,
    method: str = '3hr_max'
) -> dict:
    """
    Perform extreme value statistical analysis.

    Args:
        data: Time series data
        method: '3hr_max' or 'annual_max'

    Returns:
        Statistical parameters
    """
    if method == '3hr_max':
        # Extract 3-hour maxima
        chunk_size = int(3 * 3600 / 0.1)  # Assuming 0.1s time step
        n_chunks = len(data) // chunk_size

        maxima = np.array([
            np.max(data[i*chunk_size:(i+1)*chunk_size])
            for i in range(n_chunks)
        ])

    elif method == 'annual_max':
        maxima = data  # Assume already annual maxima

    # Fit Gumbel distribution
    # μ = mean, σ = std
    mu = np.mean(maxima)
    sigma = np.std(maxima)

    # Gumbel parameters
    beta = sigma * np.sqrt(6) / np.pi
    mu_gumbel = mu - 0.5772 * beta

    # Extreme values for different return periods
    return_periods = np.array([1, 10, 100, 10000])  # years
    extreme_values = mu_gumbel - beta * np.log(-np.log(1 - 1/return_periods))

    return {
        'mean': mu,
        'std': sigma,
        'gumbel_location': mu_gumbel,
        'gumbel_scale': beta,
        'return_periods': return_periods,
        'extreme_values': extreme_values
    }

# Example
# Generate sample tension data
time = np.linspace(0, 86400, 864000)  # 24 hours, 0.1s timestep
tension = 2000 + 500 * np.random.rayleigh(scale=1.0, size=len(time))

stats = extreme_value_statistics(tension, method='3hr_max')

print("Extreme Value Statistics:")
print(f"Mean: {stats['mean']:.1f} kN")
print(f"Std: {stats['std']:.1f} kN")
print("\nExtreme Values:")
for T, val in zip(stats['return_periods'], stats['extreme_values']):
    print(f"  {T:>5} year: {val:.1f} kN")
```

### Example 5: Convolution for Impulse Response

```python
def convolve_impulse_response(
    impulse_response: np.ndarray,
    force_time_series: np.ndarray,
    dt: float
) -> np.ndarray:
    """
    Convolve impulse response with force time series.

    Response(t) = ∫ h(τ) * F(t-τ) dτ

    Args:
        impulse_response: Impulse response function
        force_time_series: Force time series
        dt: Time step

    Returns:
        Response time series
    """
    # Convolution
    response = np.convolve(impulse_response, force_time_series, mode='same') * dt

    return response

# Example: System response to random force
t = np.linspace(0, 10, 1000)
dt = t[1] - t[0]

# Impulse response (damped oscillator)
omega = 2 * np.pi  # 1 Hz natural frequency
zeta = 0.1  # 10% damping
h = np.exp(-zeta * omega * t) * np.sin(omega * np.sqrt(1 - zeta**2) * t)

# Random force
F = np.random.randn(len(t))

# Compute response
response = convolve_impulse_response(h, F, dt)

print(f"Max response: {np.max(np.abs(response)):.3f}")
print(f"Std response: {np.std(response):.3f}")
```

## Best Practices

### 1. Use Vectorization

```python
# ❌ Bad: Loop
result = np.zeros(len(x))
for i in range(len(x)):
    result[i] = x[i]**2 + y[i]**2

# ✅ Good: Vectorized
result = x**2 + y**2
```

### 2. Avoid Unnecessary Copies

```python
# ❌ Bad: Creates copies
a = np.array([1, 2, 3])
b = a
b[0] = 10  # Modifies original

# ✅ Good: Explicit copy when needed
a = np.array([1, 2, 3])
b = a.copy()
b[0] = 10  # Original unchanged
```

### 3. Use In-Place Operations

```python
# ❌ Bad: Creates new array
a = a + 1

# ✅ Good: In-place
a += 1
```

### 4. Choose Appropriate Data Types

```python
# Use float32 for large arrays when precision allows
large_array = np.zeros((10000, 10000), dtype=np.float32)  # 400 MB instead of 800 MB
```

## Resources

- **NumPy Documentation**: https://numpy.org/doc/
- **NumPy for MATLAB Users**: https://numpy.org/doc/stable/user/numpy-for-matlab-users.html
- **Linear Algebra**: https://numpy.org/doc/stable/reference/routines.linalg.html
- **FFT Module**: https://numpy.org/doc/stable/reference/routines.fft.html
- **SciPy (extends NumPy)**: https://scipy.org/

---

**Use this skill for all numerical computations in DigitalModel!**
