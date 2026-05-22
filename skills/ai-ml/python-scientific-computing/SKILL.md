---
name: python-scientific-computing
version: 1.0.0
description: Python for engineering analysis, numerical computing, and scientific workflows using NumPy, SciPy, SymPy
author: workspace-hub
category: programming
tags: [python, numpy, scipy, sympy, numerical-computing, engineering, scientific-computing]
platforms: [python]
---

# Python Scientific Computing Skill

Master Python for engineering analysis, numerical simulations, and scientific workflows using industry-standard libraries.

## When to Use This Skill

Use Python scientific computing when you need:
- **Numerical analysis** - Solving equations, optimization, integration
- **Engineering calculations** - Stress, strain, dynamics, thermodynamics
- **Matrix operations** - Linear algebra, eigenvalue problems
- **Symbolic mathematics** - Analytical solutions, equation manipulation
- **Data analysis** - Statistical analysis, curve fitting
- **Simulations** - Physical systems, finite element preprocessing

**Avoid when:**
- Real-time performance critical (use C++/Fortran)
- Simple calculations (use calculator or Excel)
- No numerical computation needed

## Core Capabilities

### 1. NumPy - Numerical Arrays and Linear Algebra

**Array Operations:**
```python
import numpy as np

# Create arrays
array_1d = np.array([1, 2, 3, 4, 5])
array_2d = np.array([[1, 2, 3], [4, 5, 6]])

# Special arrays
zeros = np.zeros((3, 3))
ones = np.ones((2, 4))
identity = np.eye(3)
linspace = np.linspace(0, 10, 100)  # 100 points from 0 to 10

# Array operations (vectorized - fast!)
x = np.linspace(0, 2*np.pi, 1000)
y = np.sin(x) * np.exp(-x/10)
```

**Linear Algebra:**
```python
# Matrix operations
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# Matrix multiplication
C = A @ B  # or np.dot(A, B)

# Inverse
A_inv = np.linalg.inv(A)

# Eigenvalues and eigenvectors
eigenvalues, eigenvectors = np.linalg.eig(A)

# Solve linear system Ax = b
b = np.array([1, 2])
x = np.linalg.solve(A, b)

# Determinant
det_A = np.linalg.det(A)
```

### 2. SciPy - Scientific Computing

**Optimization:**
```python
from scipy import optimize

# Minimize function
def rosenbrock(x):
    return (1 - x[0])**2 + 100*(x[1] - x[0]**2)**2

result = optimize.minimize(rosenbrock, x0=[0, 0], method='BFGS')
print(f"Minimum at: {result.x}")

# Root finding
def equations(vars):
    x, y = vars
    eq1 = x**2 + y**2 - 4
    eq2 = x - y - 1
    return [eq1, eq2]

solution = optimize.fsolve(equations, [1, 1])
```

**Integration:**
```python
from scipy import integrate

# Numerical integration
def integrand(x):
    return x**2

result, error = integrate.quad(integrand, 0, 1)  # Integrate from 0 to 1
print(f"Result: {result}, Error: {error}")

# ODE solver
def ode_system(t, y):
    # dy/dt = -2y
    return -2 * y

solution = integrate.solve_ivp(
    ode_system,
    t_span=[0, 10],
    y0=[1],
    t_eval=np.linspace(0, 10, 100)
)
```

**Interpolation:**
```python
from scipy import interpolate

# 1D interpolation
x = np.array([0, 1, 2, 3, 4])
y = np.array([0, 0.5, 1.0, 1.5, 2.0])

f_linear = interpolate.interp1d(x, y, kind='linear')
f_cubic = interpolate.interp1d(x, y, kind='cubic')

x_new = np.linspace(0, 4, 100)
y_linear = f_linear(x_new)
y_cubic = f_cubic(x_new)

# 2D interpolation
from scipy.interpolate import griddata
points = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
values = np.array([0, 1, 1, 2])
grid_x, grid_y = np.mgrid[0:1:100j, 0:1:100j]
grid_z = griddata(points, values, (grid_x, grid_y), method='cubic')
```

### 3. SymPy - Symbolic Mathematics

**Symbolic Expressions:**
```python
from sympy import symbols, diff, integrate, solve, simplify, expand
from sympy import sin, cos, exp, log, sqrt, pi

# Define symbols
x, y, z = symbols('x y z')
t = symbols('t', real=True, positive=True)

# Create expressions
expr = x**2 + 2*x + 1
simplified = simplify(expr)
expanded = expand((x + 1)**3)

# Differentiation
f = x**3 + 2*x**2 + x
df_dx = diff(f, x)  # 3*x**2 + 4*x + 1
d2f_dx2 = diff(f, x, 2)  # 6*x + 4

# Integration
indefinite = integrate(x**2, x)  # x**3/3
definite = integrate(x**2, (x, 0, 1))  # 1/3

# Solve equations
equation = x**2 - 4
solutions = solve(equation, x)  # [-2, 2]

# System of equations
eq1 = x + y - 5
eq2 = x - y - 1
sol = solve([eq1, eq2], [x, y])  # {x: 3, y: 2}
```

## Complete Examples

### Example 1: Marine Engineering - Catenary Mooring Line

```python
import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

def catenary_mooring_analysis(
    water_depth: float,
    horizontal_distance: float,
    chain_weight: float,  # kg/m
    required_tension: float  # kN
) -> dict:
    """
    Analyze catenary mooring line configuration.

    Parameters:
        water_depth: Water depth (m)
        horizontal_distance: Horizontal distance to anchor (m)
        chain_weight: Chain weight per unit length in water (kg/m)
        required_tension: Required horizontal tension (kN)

    Returns:
        Dictionary with mooring line parameters
    """
    g = 9.81  # m/s²
    w = chain_weight * g / 1000  # Weight per unit length (kN/m)

    # Horizontal tension
    H = required_tension

    # Catenary parameter
    a = H / w

    # Catenary equation: z = a(cosh(x/a) - 1)
    # Need to find length of chain s such that:
    # - Horizontal distance = a*sinh(s/a)
    # - Vertical distance = a(cosh(s/a) - 1) = water_depth

    def equations(s):
        horizontal_eq = a * np.sinh(s/a) - horizontal_distance
        vertical_eq = a * (np.cosh(s/a) - 1) - water_depth
        return [horizontal_eq, vertical_eq]

    # Solve for chain length
    s_initial = np.sqrt(horizontal_distance**2 + water_depth**2)
    s_chain = fsolve(equations, s_initial)[0]

    # Calculate tensions
    T_bottom = H  # Horizontal tension at bottom
    T_top = np.sqrt(H**2 + (w * water_depth)**2)  # Tension at vessel

    # Chain profile
    x_profile = np.linspace(0, horizontal_distance, 100)
    z_profile = a * (np.cosh(x_profile/a) - 1)

    return {
        'chain_length': s_chain,
        'horizontal_tension': H,
        'top_tension': T_top,
        'bottom_tension': T_bottom,
        'catenary_parameter': a,
        'profile_x': x_profile,
        'profile_z': z_profile
    }

# Example usage
result = catenary_mooring_analysis(
    water_depth=1500,  # m
    horizontal_distance=2000,  # m
    chain_weight=400,  # kg/m
    required_tension=2000  # kN
)

print(f"Chain length required: {result['chain_length']:.1f} m")
print(f"Top tension: {result['top_tension']:.1f} kN")
print(f"Bottom tension: {result['bottom_tension']:.1f} kN")
```

### Example 2: Structural Dynamics - Natural Frequency

```python
import numpy as np
from scipy.linalg import eig

def calculate_natural_frequencies(
    mass_matrix: np.ndarray,
    stiffness_matrix: np.ndarray,
    num_modes: int = 5
) -> dict:
    """
    Calculate natural frequencies and mode shapes.

    Solves eigenvalue problem: [K - ω²M]φ = 0

    Parameters:
        mass_matrix: Mass matrix [n×n]
        stiffness_matrix: Stiffness matrix [n×n]
        num_modes: Number of modes to return

    Returns:
        Dictionary with frequencies and mode shapes
    """
    # Solve generalized eigenvalue problem
    eigenvalues, eigenvectors = eig(stiffness_matrix, mass_matrix)

    # Calculate natural frequencies (rad/s)
    omega = np.sqrt(eigenvalues.real)

    # Sort by frequency
    idx = np.argsort(omega)
    omega_sorted = omega[idx]
    modes_sorted = eigenvectors[:, idx]

    # Convert to Hz
    frequencies_hz = omega_sorted / (2 * np.pi)

    # Periods
    periods = 1 / frequencies_hz

    return {
        'natural_frequencies_rad_s': omega_sorted[:num_modes],
        'natural_frequencies_hz': frequencies_hz[:num_modes],
        'periods_s': periods[:num_modes],
        'mode_shapes': modes_sorted[:, :num_modes]
    }

# Example: 3-DOF system
M = np.array([
    [100, 0, 0],
    [0, 100, 0],
    [0, 0, 100]
])  # Mass matrix (kg)

K = np.array([
    [200, -100, 0],
    [-100, 200, -100],
    [0, -100, 100]
])  # Stiffness matrix (kN/m)

result = calculate_natural_frequencies(M, K, num_modes=3)

for i, (f, T) in enumerate(zip(result['natural_frequencies_hz'], result['periods_s'])):
    print(f"Mode {i+1}: f = {f:.3f} Hz, T = {T:.3f} s")
```

### Example 3: Hydrodynamic Analysis - Wave Spectrum

```python
import numpy as np
from scipy.integrate import trapz

def jonswap_spectrum(
    frequencies: np.ndarray,
    Hs: float,
    Tp: float,
    gamma: float = 3.3
) -> np.ndarray:
    """
    Calculate JONSWAP wave spectrum.

    Parameters:
        frequencies: Frequency array (Hz)
        Hs: Significant wave height (m)
        Tp: Peak period (s)
        gamma: Peak enhancement factor (default 3.3)

    Returns:
        Spectral density S(f) in m²/Hz
    """
    fp = 1 / Tp  # Peak frequency
    omega_p = 2 * np.pi * fp
    omega = 2 * np.pi * frequencies

    # Pierson-Moskowitz spectrum
    alpha = 0.0081
    beta = 0.74
    S_PM = (alpha * 9.81**2 / omega**5) * np.exp(-beta * (omega_p / omega)**4)

    # Peak enhancement
    sigma = np.where(omega <= omega_p, 0.07, 0.09)
    r = np.exp(-(omega - omega_p)**2 / (2 * sigma**2 * omega_p**2))

    S_JONSWAP = S_PM * gamma**r

    return S_JONSWAP

def wave_statistics(spectrum: np.ndarray, frequencies: np.ndarray) -> dict:
    """
    Calculate wave statistics from spectrum.

    Parameters:
        spectrum: Spectral density S(f)
        frequencies: Frequency array (Hz)

    Returns:
        Wave statistics
    """
    df = frequencies[1] - frequencies[0]

    # Spectral moments
    m0 = trapz(spectrum, frequencies)
    m2 = trapz(spectrum * frequencies**2, frequencies)
    m4 = trapz(spectrum * frequencies**4, frequencies)

    # Characteristic wave heights
    Hm0 = 4 * np.sqrt(m0)  # Spectral significant wave height
    Tz = np.sqrt(m0 / m2)   # Zero-crossing period
    Te = np.sqrt(m0 / m4) if m4 > 0 else 0  # Energy period

    # Expected maximum (3-hour storm)
    n_waves = 3 * 3600 / Tz  # Number of waves in 3 hours
    H_max = Hm0 / 2 * np.sqrt(0.5 * np.log(n_waves))

    return {
        'Hm0': Hm0,
        'Tz': Tz,
        'Te': Te,
        'H_max': H_max,
        'm0': m0,
        'm2': m2
    }

# Example usage
frequencies = np.linspace(0.01, 2.0, 200)
spectrum = jonswap_spectrum(frequencies, Hs=8.5, Tp=12.0, gamma=3.3)
stats = wave_statistics(spectrum, frequencies)

print(f"Hm0 = {stats['Hm0']:.2f} m")
print(f"Tz = {stats['Tz']:.2f} s")
print(f"Expected maximum = {stats['H_max']:.2f} m")
```

### Example 4: Numerical Integration - Velocity to Displacement

```python
import numpy as np
from scipy.integrate import cumtrapz

def integrate_motion_time_history(
    time: np.ndarray,
    acceleration: np.ndarray
) -> dict:
    """
    Integrate acceleration to get velocity and displacement.

    Parameters:
        time: Time array (s)
        acceleration: Acceleration time history (m/s²)

    Returns:
        Dictionary with velocity and displacement
    """
    # Integrate acceleration to get velocity
    velocity = cumtrapz(acceleration, time, initial=0)

    # Integrate velocity to get displacement
    displacement = cumtrapz(velocity, time, initial=0)

    # Remove drift (if needed)
    # Fit linear trend and subtract
    from numpy.polynomial import polynomial as P
    coef_vel = P.polyfit(time, velocity, 1)
    velocity_detrended = velocity - P.polyval(time, coef_vel)

    coef_disp = P.polyfit(time, displacement, 1)
    displacement_detrended = displacement - P.polyval(time, coef_disp)

    return {
        'velocity': velocity,
        'displacement': displacement,
        'velocity_detrended': velocity_detrended,
        'displacement_detrended': displacement_detrended
    }

# Example: Process vessel motion
dt = 0.05  # Time step (s)
duration = 100  # Duration (s)
time = np.arange(0, duration, dt)

# Simulated acceleration (heave motion)
omega = 2 * np.pi / 10  # 10 second period
acceleration = 2 * np.sin(omega * time)

result = integrate_motion_time_history(time, acceleration)

print(f"Max velocity: {np.max(np.abs(result['velocity'])):.3f} m/s")
print(f"Max displacement: {np.max(np.abs(result['displacement'])):.3f} m")
```

### Example 5: Optimization - Mooring Pretension

```python
from scipy.optimize import minimize
import numpy as np

def optimize_mooring_pretension(
    num_lines: int,
    water_depth: float,
    target_offset: float,
    max_tension: float
) -> dict:
    """
    Optimize mooring line pretensions to achieve target offset.

    Parameters:
        num_lines: Number of mooring lines
        water_depth: Water depth (m)
        target_offset: Target vessel offset (m)
        max_tension: Maximum allowable tension (kN)

    Returns:
        Optimized pretensions
    """
    # Objective: Minimize difference from target offset
    def objective(pretensions):
        # Simplified model: offset = f(pretension)
        # In reality, would use catenary equations
        total_restoring = np.sum(pretensions) / water_depth
        predicted_offset = target_offset / (1 + total_restoring * 0.001)
        return (predicted_offset - target_offset)**2

    # Constraints: All pretensions > 0 and < max_tension
    bounds = [(100, max_tension) for _ in range(num_lines)]

    # Constraint: Symmetric pretensions (pairs equal)
    def constraint_symmetry(pretensions):
        if num_lines % 2 == 0:
            diffs = []
            for i in range(num_lines // 2):
                diffs.append(pretensions[i] - pretensions[i + num_lines//2])
            return np.array(diffs)
        return np.array([0])

    constraints = {'type': 'eq', 'fun': constraint_symmetry}

    # Initial guess: Equal pretensions
    x0 = np.ones(num_lines) * 1000  # kN

    # Optimize
    result = minimize(
        objective,
        x0,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )

    return {
        'optimized_pretensions': result.x,
        'success': result.success,
        'final_offset': target_offset,
        'optimization_message': result.message
    }

# Example usage
result = optimize_mooring_pretension(
    num_lines=12,
    water_depth=1500,
    target_offset=50,
    max_tension=3000
)

print("Optimized pretensions (kN):")
for i, tension in enumerate(result['optimized_pretensions']):
    print(f"  Line {i+1}: {tension:.1f} kN")
```

### Example 6: Symbolic Mathematics - Beam Deflection

```python
from sympy import symbols, diff, integrate, simplify, lambdify
from sympy import Function, Eq, dsolve
import numpy as np
import matplotlib.pyplot as plt

def beam_deflection_symbolic():
    """
    Solve beam deflection equation symbolically.

    Beam equation: EI * d⁴y/dx⁴ = q(x)
    """
    # Define symbols
    x, E, I, L, q0 = symbols('x E I L q0', real=True, positive=True)

    # Simply supported beam with uniform load
    # Boundary conditions: y(0) = 0, y(L) = 0, y''(0) = 0, y''(L) = 0

    # Load function
    q = q0  # Uniform load

    # Integrate beam equation four times
    # EI * d⁴y/dx⁴ = q
    # EI * d³y/dx³ = qx + C1 (shear force)
    # EI * d²y/dx² = qx²/2 + C1*x + C2 (bending moment)
    # EI * dy/dx = qx³/6 + C1*x²/2 + C2*x + C3 (slope)
    # EI * y = qx⁴/24 + C1*x³/6 + C2*x²/2 + C3*x + C4 (deflection)

    # For simply supported: C2 = 0, C4 = 0
    # Apply boundary conditions to find C1, C3
    # y(L) = 0: q0*L⁴/24 + C1*L³/6 + C3*L = 0
    # y'(0) = 0 is not required for simply supported

    # Deflection equation
    y = q0*x**2*(L**2 - 2*L*x + x**2)/(24*E*I)

    # Maximum deflection (at center x = L/2)
    y_max = y.subs(x, L/2)
    y_max_simplified = simplify(y_max)

    # Slope
    slope = diff(y, x)

    # Bending moment
    M = -E*I*diff(y, x, 2)
    M_simplified = simplify(M)

    return {
        'deflection': y,
        'max_deflection': y_max_simplified,
        'slope': slope,
        'bending_moment': M_simplified
    }

# Get symbolic solutions
solution = beam_deflection_symbolic()

print("Beam Deflection (Simply Supported, Uniform Load):")
print(f"y(x) = {solution['deflection']}")
print(f"y_max = {solution['max_deflection']}")
print(f"M(x) = {solution['bending_moment']}")

# Numerical example
from sympy import symbols
x_sym, E_sym, I_sym, L_sym, q0_sym = symbols('x E I L q0')

# Create numerical function
y_numeric = lambdify(
    (x_sym, E_sym, I_sym, L_sym, q0_sym),
    solution['deflection'],
    'numpy'
)

# Parameters
E_val = 200e9  # Pa (steel)
I_val = 1e-4   # m⁴
L_val = 10     # m
q0_val = 10000 # N/m

# Calculate deflection along beam
x_vals = np.linspace(0, L_val, 100)
y_vals = y_numeric(x_vals, E_val, I_val, L_val, q0_val)

print(f"\nNumerical example:")
print(f"Max deflection: {-np.min(y_vals)*1000:.2f} mm")
```

## Best Practices

### 1. Use Vectorization
```python
# ❌ Slow: Loop
result = []
for x in x_array:
    result.append(np.sin(x) * np.exp(-x))

# ✅ Fast: Vectorized
result = np.sin(x_array) * np.exp(-x_array)
```

### 2. Choose Right Data Type
```python
# Use appropriate precision
float32_array = np.array([1, 2, 3], dtype=np.float32)  # Less memory
float64_array = np.array([1, 2, 3], dtype=np.float64)  # More precision

# Use integer when possible
int_array = np.array([1, 2, 3], dtype=np.int32)
```

### 3. Avoid Matrix Inverse When Possible
```python
# ❌ Slower and less stable
x = np.linalg.inv(A) @ b

# ✅ Faster and more stable
x = np.linalg.solve(A, b)
```

### 4. Use Broadcasting
```python
# Broadcasting allows operations on arrays of different shapes
A = np.array([[1, 2, 3],
              [4, 5, 6]])  # Shape (2, 3)

b = np.array([10, 20, 30])  # Shape (3,)

# Broadcast adds b to each row of A
C = A + b  # Shape (2, 3)
```

### 5. Check Numerical Stability
```python
# Check condition number
cond = np.linalg.cond(A)
if cond > 1e10:
    print("Warning: Matrix is ill-conditioned")

# Use appropriate solver for symmetric positive definite
if np.allclose(A, A.T) and np.all(np.linalg.eigvals(A) > 0):
    x = np.linalg.solve(A, b)  # Can use Cholesky internally
```

## Common Patterns

### Pattern 1: Load and Process Engineering Data
```python
import numpy as np

# Load CSV data
data = np.loadtxt('../data/measurements.csv', delimiter=',', skiprows=1)

# Extract columns
time = data[:, 0]
temperature = data[:, 1]
pressure = data[:, 2]

# Process
mean_temp = np.mean(temperature)
std_temp = np.std(temperature)
max_pressure = np.max(pressure)
```

### Pattern 2: Solve System of Equations
```python
from scipy.optimize import fsolve

def system(vars):
    x, y, z = vars
    eq1 = x + y + z - 6
    eq2 = 2*x - y + z - 1
    eq3 = x + 2*y - z - 3
    return [eq1, eq2, eq3]

solution = fsolve(system, [1, 1, 1])
```

### Pattern 3: Curve Fitting
```python
from scipy.optimize import curve_fit

def model(x, a, b, c):
    return a * np.exp(-b * x) + c

# Fit data
params, covariance = curve_fit(model, x_data, y_data)
a_fit, b_fit, c_fit = params
```

## Installation

```bash
# Using pip
pip install numpy scipy sympy matplotlib

# Using UV (faster)
uv pip install numpy scipy sympy matplotlib

# Specific versions
pip install numpy==1.26.0 scipy==1.11.0 sympy==1.12
```

## Integration with DigitalModel

### CSV Data Processing
```python
import numpy as np

# Load OrcaFlex results
data = np.loadtxt('../data/processed/orcaflex_results.csv',
                   delimiter=',', skiprows=1)

# Process time series
time = data[:, 0]
tension = data[:, 1]

# Statistics
max_tension = np.max(tension)
mean_tension = np.mean(tension)
std_tension = np.std(tension)
```

### YAML Configuration Integration
```python
import yaml
import numpy as np

def run_analysis_from_config(config_file: str):
    with open(config_file) as f:
        config = yaml.safe_load(f)

    # Extract parameters
    L = config['geometry']['length']
    E = config['material']['youngs_modulus']

    # Run numerical analysis
    result = calculate_natural_frequency(L, E)

    return result
```

## Resources

- **NumPy Documentation**: https://numpy.org/doc/
- **SciPy Documentation**: https://docs.scipy.org/doc/scipy/
- **SymPy Documentation**: https://docs.sympy.org/
- **NumPy for MATLAB Users**: https://numpy.org/doc/stable/user/numpy-for-matlab-users.html
- **SciPy Lecture Notes**: https://scipy-lectures.org/

## Performance Tips

1. **Use NumPy's built-in functions** - They're optimized in C
2. **Avoid Python loops** - Use vectorization
3. **Use views instead of copies** when possible
4. **Choose appropriate algorithms** - O(n) vs O(n²)
5. **Profile your code** - Find bottlenecks with `cProfile`

---

**Use this skill for all numerical engineering calculations in DigitalModel!**
