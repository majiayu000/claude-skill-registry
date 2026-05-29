---
name: claude-light
description: Expert assistant for conducting remote experiments with Claude-Light - a web-accessible RGB LED and spectral sensor instrument for statistics, regression, optimization, and design of experiments
allowed-tools: "*"
---

# Claude-Light Experimental Skills

You are an expert assistant for designing and conducting experiments with Claude-Light, a remote laboratory instrument that controls RGB LEDs and measures spectral response. Help users perform statistical analysis, regression modeling, optimization, and design of experiments workflows.

## What is Claude-Light?

Claude-Light is a Raspberry Pi-based remote experimental instrument that:
- Controls RGB LEDs (inputs: R, G, B values from 0 to 1)
- Measures light intensity across 10 spectral channels
- Provides web interfaces and REST API for remote access
- Enables hands-on learning of experimental methods and data science

**Key Features:**
- No special software required (web browser or Python requests)
- Automatic logging of all experiments
- Camera documentation of LED states
- Multiple sophistication levels (web forms, API, Python scripting)

## Installation

No installation needed for basic API usage - just use Python's `requests` library.

```bash
# Basic requirement
pip install requests

# For data analysis
pip install numpy pandas matplotlib scipy scikit-learn
```

## API Access

### Endpoint

```
https://claude-light.cheme.cmu.edu/api
```

### Parameters

- **R**: Red channel (0.0 to 1.0)
- **G**: Green channel (0.0 to 1.0)
- **B**: Blue channel (0.0 to 1.0)

### Response Format

Returns JSON with:
- Input parameters (R, G, B)
- Spectral measurements at 10 channels:
  - `415nm`, `445nm`, `480nm`, `515nm`, `555nm`, `590nm`, `630nm`, `680nm`
  - `clear` (total intensity)
  - `nir` (near-infrared)

### Basic Usage

```python
import requests

# Send experiment
response = requests.get('https://claude-light.cheme.cmu.edu/api',
                       params={'R': 0.5, 'G': 0.3, 'B': 0.8})

# Get data
data = response.json()
print(data)

# Access specific wavelength
intensity_515 = data['out']['515nm']
```

## Experimental Workflows

### 1. Reproducibility and Statistics

**Goal**: Assess measurement variability and statistical properties

```python
import requests
import numpy as np

# Repeat same measurement multiple times
R, G, B = 0.5, 0.5, 0.5
measurements = []

for i in range(30):
    resp = requests.get('https://claude-light.cheme.cmu.edu/api',
                       params={'R': R, 'G': G, 'B': B})
    data = resp.json()
    measurements.append(data['out']['515nm'])

# Calculate statistics
measurements = np.array(measurements)
print(f"Mean: {np.mean(measurements):.2f}")
print(f"Std Dev: {np.std(measurements):.2f}")
print(f"Median: {np.median(measurements):.2f}")
print(f"95% CI: {np.percentile(measurements, [2.5, 97.5])}")
```

**Analysis Tasks:**
- Compute mean, median, standard deviation
- Plot histograms and assess normality
- Calculate confidence intervals
- Determine measurement precision

### 2. Linear Regression (Single Variable)

**Goal**: Establish input-output relationship

```python
import requests
import numpy as np
from scipy.stats import linregress

# Vary one input, keep others constant
R_values = np.linspace(0, 1, 11)
outputs = []

for R in R_values:
    resp = requests.get('https://claude-light.cheme.cmu.edu/api',
                       params={'R': R, 'G': 0, 'B': 0})
    data = resp.json()
    outputs.append(data['out']['630nm'])  # Red wavelength

# Fit linear model
slope, intercept, r_value, p_value, std_err = linregress(R_values, outputs)

print(f"Slope: {slope:.2f}")
print(f"Intercept: {intercept:.2f}")
print(f"R²: {r_value**2:.4f}")
print(f"Std Error: {std_err:.2f}")

# Predict input for target output
target_output = 25000
predicted_R = (target_output - intercept) / slope
print(f"Predicted R for output {target_output}: {predicted_R:.3f}")
```

**Analysis Tasks:**
- Fit linear models
- Calculate R², RMSE, MAE
- Quantify parameter uncertainties
- Validate predictions experimentally

### 3. Multivariate Regression

**Goal**: Model multiple inputs affecting multiple outputs

```python
import requests
import numpy as np
from sklearn.linear_model import LinearRegression

# Design of experiments - grid sampling
R_vals = np.linspace(0.1, 0.9, 5)
G_vals = np.linspace(0.1, 0.9, 5)

# Collect data
X = []  # Inputs
y_515 = []  # Output at 515nm
y_630 = []  # Output at 630nm

for R in R_vals:
    for G in G_vals:
        resp = requests.get('https://claude-light.cheme.cmu.edu/api',
                           params={'R': R, 'G': G, 'B': 0})
        data = resp.json()

        X.append([R, G])
        y_515.append(data['out']['515nm'])
        y_630.append(data['out']['630nm'])

X = np.array(X)
y_515 = np.array(y_515)

# Fit model
model = LinearRegression()
model.fit(X, y_515)

print(f"R coefficient: {model.coef_[0]:.2f}")
print(f"G coefficient: {model.coef_[1]:.2f}")
print(f"Intercept: {model.intercept_:.2f}")
print(f"R² score: {model.score(X, y_515):.4f}")

# Predict inputs for target output
target = 30000
# Solve: target = coef[0]*R + coef[1]*G + intercept
```

**Analysis Tasks:**
- Multi-input, multi-output modeling
- Feature importance analysis
- Interaction effects
- Simultaneous constraint satisfaction

### 4. Optimization

**Goal**: Find inputs that produce desired outputs

```python
import requests
import numpy as np
from scipy.optimize import minimize

def objective(inputs):
    """Minimize difference from target output."""
    R, G, B = inputs

    # Constrain to valid range
    R = np.clip(R, 0, 1)
    G = np.clip(G, 0, 1)
    B = np.clip(B, 0, 1)

    resp = requests.get('https://claude-light.cheme.cmu.edu/api',
                       params={'R': R, 'G': G, 'B': B})
    data = resp.json()

    # Target specific outputs at different wavelengths
    target_515 = 30000
    target_630 = 20000

    actual_515 = data['out']['515nm']
    actual_630 = data['out']['630nm']

    # Squared error
    error = (actual_515 - target_515)**2 + (actual_630 - target_630)**2
    return error

# Optimize
initial_guess = [0.5, 0.5, 0.5]
result = minimize(objective, initial_guess,
                 bounds=[(0, 1), (0, 1), (0, 1)],
                 method='Nelder-Mead')

print(f"Optimal R, G, B: {result.x}")
print(f"Final error: {result.fun}")
```

**Optimization Methods:**
- Scipy.optimize (Nelder-Mead, Powell, L-BFGS-B)
- Bayesian optimization (scikit-optimize)
- Grid search with interpolation
- Active learning approaches

### 5. Design of Experiments (DOE)

**Goal**: Efficient experimental design for maximum information

```python
import requests
import numpy as np
from scipy.stats import qmc

# Latin Hypercube Sampling
sampler = qmc.LatinHypercube(d=3)  # 3 dimensions: R, G, B
n_samples = 20
sample = sampler.random(n=n_samples)

# Scale to [0, 1]
samples = qmc.scale(sample, [0, 0, 0], [1, 1, 1])

# Run experiments
results = []
for R, G, B in samples:
    resp = requests.get('https://claude-light.cheme.cmu.edu/api',
                       params={'R': R, 'G': G, 'B': B})
    data = resp.json()
    results.append({
        'R': R, 'G': G, 'B': B,
        'output_515': data['out']['515nm'],
        'output_630': data['out']['630nm']
    })

# Analyze space-filling design
import pandas as pd
df = pd.DataFrame(results)
```

**DOE Strategies:**
- Latin hypercube sampling
- Factorial designs (full, fractional)
- Response surface methodology
- Optimal design criteria (D-optimal, A-optimal)

### 6. Machine Learning Approaches

**Goal**: Use advanced ML models for prediction

```python
import requests
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline

# Collect training data (use previous methods)
X_train = # Input RGB values
y_train = # Output measurements

# Random Forest
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
print(f"RF R² score: {rf.score(X_train, y_train):.4f}")

# Neural Network
mlp = MLPRegressor(hidden_layer_sizes=(50, 30), max_iter=1000)
mlp.fit(X_train, y_train)
print(f"MLP R² score: {mlp.score(X_train, y_train):.4f}")

# Polynomial regression
poly_model = Pipeline([
    ('poly', PolynomialFeatures(degree=2)),
    ('linear', LinearRegression())
])
poly_model.fit(X_train, y_train)
```

**ML Models to Try:**
- Linear models with regularization (Ridge, Lasso)
- Decision trees and random forests
- Neural networks (MLPRegressor)
- Gaussian processes
- XGBoost, LightGBM
- Support vector regression

### 7. Uncertainty Quantification

**Goal**: Quantify confidence in predictions

```python
import requests
import numpy as np
from scipy import stats

# Bootstrap uncertainty estimation
def bootstrap_regression(X, y, n_bootstrap=1000):
    slopes = []
    intercepts = []

    for _ in range(n_bootstrap):
        # Resample with replacement
        indices = np.random.choice(len(X), size=len(X), replace=True)
        X_boot = X[indices]
        y_boot = y[indices]

        # Fit model
        slope, intercept, _, _, _ = stats.linregress(X_boot, y_boot)
        slopes.append(slope)
        intercepts.append(intercept)

    return np.array(slopes), np.array(intercepts)

# Use bootstrap results for confidence intervals
slopes, intercepts = bootstrap_regression(R_values, outputs)
print(f"Slope: {np.mean(slopes):.2f} ± {np.std(slopes):.2f}")
print(f"95% CI: {np.percentile(slopes, [2.5, 97.5])}")
```

**Uncertainty Methods:**
- Bootstrap resampling
- Prediction intervals
- Parameter covariance matrices
- Cross-validation
- Monte Carlo simulation

## Best Practices

### Data Management

```python
# Save experiments to CSV
import pandas as pd

experiments = []
for R in np.linspace(0, 1, 10):
    resp = requests.get('https://claude-light.cheme.cmu.edu/api',
                       params={'R': R, 'G': 0, 'B': 0})
    data = resp.json()
    experiments.append({
        'R': R, 'G': 0, 'B': 0,
        **data['out']  # Unpack all spectral measurements
    })

df = pd.DataFrame(experiments)
df.to_csv('experiments.csv', index=False)
```

### Background Subtraction

```python
# Measure ambient light
def get_background():
    resp = requests.get('https://claude-light.cheme.cmu.edu/api',
                       params={'R': 0, 'G': 0, 'B': 0})
    return resp.json()['out']

bg = get_background()

# Subtract from measurements
def corrected_measurement(R, G, B):
    resp = requests.get('https://claude-light.cheme.cmu.edu/api',
                       params={'R': R, 'G': G, 'B': B})
    data = resp.json()

    corrected = {}
    for wavelength in data['out']:
        corrected[wavelength] = data['out'][wavelength] - bg[wavelength]

    return corrected
```

### Averaging for Noise Reduction

```python
def averaged_measurement(R, G, B, n_repeats=5):
    """Take multiple measurements and return average."""
    measurements = []

    for _ in range(n_repeats):
        resp = requests.get('https://claude-light.cheme.cmu.edu/api',
                           params={'R': R, 'G': G, 'B': B})
        data = resp.json()
        measurements.append(data['out'])

    # Average all wavelengths
    avg = {}
    for wavelength in measurements[0]:
        values = [m[wavelength] for m in measurements]
        avg[wavelength] = np.mean(values)

    return avg
```

### Caching Results

```python
import pickle
from pathlib import Path

def cached_experiment(R, G, B, cache_dir='experiments_cache'):
    """Cache experiments to avoid redundant API calls."""
    Path(cache_dir).mkdir(exist_ok=True)

    # Create unique filename
    cache_file = Path(cache_dir) / f"R{R:.3f}_G{G:.3f}_B{B:.3f}.pkl"

    if cache_file.exists():
        with open(cache_file, 'rb') as f:
            return pickle.load(f)

    # Perform experiment
    resp = requests.get('https://claude-light.cheme.cmu.edu/api',
                       params={'R': R, 'G': G, 'B': B})
    data = resp.json()

    # Cache result
    with open(cache_file, 'wb') as f:
        pickle.dump(data, f)

    return data
```

## Visualization

```python
import matplotlib.pyplot as plt

# Plot spectral response
def plot_spectrum(R, G, B):
    resp = requests.get('https://claude-light.cheme.cmu.edu/api',
                       params={'R': R, 'G': G, 'B': B})
    data = resp.json()

    wavelengths = ['415nm', '445nm', '480nm', '515nm',
                   '555nm', '590nm', '630nm', '680nm']
    intensities = [data['out'][wl] for wl in wavelengths]
    wl_values = [int(wl.replace('nm', '')) for wl in wavelengths]

    plt.figure(figsize=(10, 6))
    plt.plot(wl_values, intensities, 'o-')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Intensity')
    plt.title(f'Spectrum for R={R}, G={G}, B={B}')
    plt.grid(True)
    plt.show()

# Plot input-output relationship
def plot_response_curve(channel='R', wavelength='515nm'):
    values = np.linspace(0, 1, 20)
    outputs = []

    for val in values:
        params = {'R': 0, 'G': 0, 'B': 0}
        params[channel] = val

        resp = requests.get('https://claude-light.cheme.cmu.edu/api', params=params)
        data = resp.json()
        outputs.append(data['out'][wavelength])

    plt.figure(figsize=(10, 6))
    plt.plot(values, outputs, 'o-')
    plt.xlabel(f'{channel} Input')
    plt.ylabel(f'Output at {wavelength}')
    plt.title(f'{channel} Response at {wavelength}')
    plt.grid(True)
    plt.show()
```

## Common Experimental Patterns

### Pattern 1: Single Variable Sweep

```python
# Systematically vary one input
for value in np.linspace(0, 1, 10):
    data = get_measurement(R=value, G=0, B=0)
    analyze(data)
```

### Pattern 2: Factorial Design

```python
# Test all combinations
for R in [0, 0.5, 1]:
    for G in [0, 0.5, 1]:
        for B in [0, 0.5, 1]:
            data = get_measurement(R, G, B)
```

### Pattern 3: Gradient Descent

```python
# Iteratively approach target
current = [0.5, 0.5, 0.5]
learning_rate = 0.1

for iteration in range(10):
    gradient = estimate_gradient(current)
    current = current - learning_rate * gradient
```

## Error Handling

```python
import requests
from requests.exceptions import Timeout, ConnectionError

def safe_experiment(R, G, B, max_retries=3):
    """Robust experiment with retry logic."""
    for attempt in range(max_retries):
        try:
            resp = requests.get(
                'https://claude-light.cheme.cmu.edu/api',
                params={'R': R, 'G': G, 'B': B},
                timeout=10
            )
            resp.raise_for_status()
            return resp.json()

        except (Timeout, ConnectionError) as e:
            if attempt == max_retries - 1:
                raise
            print(f"Attempt {attempt + 1} failed, retrying...")
            continue
```

## Resources

- GitHub Repository: https://github.com/jkitchin/claude-light
- API Endpoint: https://claude-light.cheme.cmu.edu/api
- Web Interface: https://claude-light.cheme.cmu.edu/rgb
- See `examples/` for complete experimental workflows
- See `references/` for detailed methodology guides
