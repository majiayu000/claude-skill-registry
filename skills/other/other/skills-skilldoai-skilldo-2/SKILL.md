---
name: scipy
description: python library
version: 1.17.1
ecosystem: python
license: BSD-3-Clause
generated_with: claude-sonnet-4-5-20250929
---

## Imports

```python
import scipy
import numpy as np

# Sparse matrices
from scipy import sparse
from scipy.sparse import coo_array, csr_array, csc_array, bsr_array
from scipy.sparse import dia_array, dok_array, lil_array
from scipy.sparse import linalg as splinalg
from scipy.sparse import csgraph

# FFT operations
from scipy import fft
from scipy.fft import fft, ifft, fft2, ifft2

# Optimization
from scipy import optimize
from scipy.optimize import minimize, differential_evolution

# Linear algebra
from scipy import linalg

# Signal processing
from scipy import signal

# Statistics
from scipy import stats

# Integration
from scipy import integrate

# Interpolation
from scipy import interpolate

# Image processing
from scipy import ndimage

# Special functions
from scipy import special

# Orthogonal Distance Regression
from scipy import odr
from scipy.odr import Data, RealData, Model, ODR
from scipy.odr import multilinear, exponential, polynomial, unilinear, quadratic

# Spatial algorithms
from scipy import spatial

# Constants
from scipy import constants

# I/O
from scipy import io

# Clustering
from scipy import cluster

# Datasets
from scipy import datasets

# Differentiation
from scipy import differentiate
```

## Core Concepts

### Subpackages

SciPy is organized into subpackages, each focused on a specific domain:

- **cluster**: Clustering algorithms (k-means, hierarchical)
- **constants**: Physical and mathematical constants
- **datasets**: Example datasets for testing
- **differentiate**: Finite difference differentiation
- **fft**: Fast Fourier Transform algorithms
- **integrate**: Integration and ODE solvers
- **interpolate**: Interpolation and smoothing
- **io**: Data input/output (MATLAB, WAV, etc.)
- **linalg**: Linear algebra routines
- **ndimage**: N-dimensional image processing
- **odr**: Orthogonal Distance Regression
- **optimize**: Optimization and root finding
- **signal**: Signal processing
- **sparse**: Sparse matrix support
- **spatial**: Spatial data structures and algorithms
- **special**: Special mathematical functions
- **stats**: Statistical functions and distributions

### Lazy Loading

SciPy uses lazy loading - submodules are imported only when first accessed to reduce startup time.

## Core Patterns

### Sparse Matrix Workflow

```python
from scipy import sparse
import numpy as np

# Pattern: Build → Convert → Compute
# 1. Build in COO or DOK format
row = np.array([0, 1, 2, 0])
col = np.array([0, 1, 2, 2])
data = np.array([1, 2, 3, 4])
coo = sparse.coo_array((data, (row, col)), shape=(3, 3))

# 2. Convert to efficient format for operations
csr = coo.tocsr()
csr.sum_duplicates()
csr.eliminate_zeros()

# 3. Perform computations
result = csr @ csr.T
```

### Optimization Workflow

```python
from scipy import optimize

# Pattern: Define → Initialize → Optimize → Validate
# 1. Define objective and constraints
def objective(x):
    return (x[0] - 1)**2 + (x[1] - 2.5)**2

def constraint(x):
    return x[0] + x[1] - 2

# 2. Initialize
x0 = [0, 0]
cons = {'type': 'ineq', 'fun': constraint}
bounds = [(0, None), (0, None)]

# 3. Optimize
result = optimize.minimize(objective, x0, 
                          method='SLSQP',
                          constraints=cons,
                          bounds=bounds)

# 4. Validate
if result.success:
    print(f"Solution: {result.x}")
```

### ODR Workflow

```python
from scipy import odr
import numpy as np

# Pattern: Model → Data → Fit → Analyze
# 1. Define model
def model_func(B, x):
    return B[0] * x + B[1]

# 2. Prepare data with errors
x = np.array([1, 2, 3, 4, 5])
y = np.array([2.1, 3.9, 6.2, 7.8, 10.1])
sx = np.array([0.1, 0.1, 0.1, 0.1, 0.1])
sy = np.array([0.2, 0.2, 0.2, 0.2, 0.2])

data = odr.RealData(x, y, sx=sx, sy=sy)
model = odr.Model(model_func)

# 3. Fit
odr_obj = odr.ODR(data, model, beta0=[1., 0.])
output = odr_obj.run()

# 4. Analyze results
output.pprint()
print(f"Chi-square: {output.res_var}")
```

### Iterative Solver Pattern

```python
from scipy.sparse import linalg as splinalg
from scipy import sparse
import numpy as np

# Pattern: Precondition → Solve → Check Convergence
A = sparse.csr_array([[3, 0, 1], [0, 4, 0], [1, 0, 2]])
b = np.array([1, 2, 3])

# 1. Create preconditioner
M = sparse.diags(1.0 / A.diagonal())

# 2. Solve with callback
def callback(xk):
    print(f"Residual: {np.linalg.norm(A @ xk - b)}")

x, info = splinalg.cg(A, b, M=M, callback=callback, tol=1e-5)

# 3. Check convergence
if info == 0:
    print("Converged successfully")
elif info > 0:
    print(f"Converged after {info} iterations")
else:
    print("Failed to converge")
```

### Signal Processing Pipeline

```python
from scipy import signal
import numpy as np

# Pattern: Design → Filter → Analyze
# 1. Design filter
fs = 1000  # Sample rate
b, a = signal.butter(4, [10, 100], btype='band', fs=fs)

# 2. Apply filter
data = np.random.randn(10000)
filtered = signal.filtfilt(b, a, data)

# 3. Analyze
f, Pxx = signal.welch(filtered, fs=fs)
peaks, _ = signal.find_peaks(Pxx, height=0.1)
```

## Sparse Matrices

### Creating Sparse Arrays

```python
import numpy as np
from scipy import sparse

# COO (Coordinate) format - good for construction
row = np.array([0, 1, 2, 0])
col = np.array([0, 1, 2, 2])
data = np.array([1, 2, 3, 4])
coo = sparse.coo_array((data, (row, col)), shape=(3, 3))

# CSR (Compressed Sparse Row) - efficient row operations
csr = sparse.csr_array([[1, 0, 2], [0, 3, 0]])

# CSC (Compressed Sparse Column) - efficient column operations
csc = sparse.csc_array([[1, 0, 2], [0, 3, 0]])

# DOK (Dictionary of Keys) - incremental construction
dok = sparse.dok_array((5, 5))
dok[0, 0] = 1
dok[1, 2] = 2

# LIL (List of Lists) - incremental construction
lil = sparse.lil_array((10, 10))
lil[0, :5] = 1
lil[1, 5:] = 2

# From dense array
dense = np.eye(100)
sparse_eye = sparse.csr_array(dense)
```

### Format Conversion

```python
# Convert between formats
coo = sparse.coo_array([[1, 0], [0, 2]])
csr = coo.tocsr()
csc = coo.tocsc()
dense = coo.toarray()

# Each format has different strengths:
# - COO: construction, converting to other formats
# - CSR: row slicing, matrix-vector products
# - CSC: column slicing, matrix-vector products
# - DOK: element access and incremental construction
# - LIL: incremental construction, changing sparsity structure
```

### Sparse Array Operations

```python
from scipy import sparse
import numpy as np

# Create sparse matrices
a = sparse.csr_array([[1, 0, 2], [0, 3, 0]])
b = sparse.csr_array([[0, 1], [2, 0], [0, 3]])

# Matrix multiplication
c = a @ b  # or a.dot(b)

# Element-wise operations
doubled = a * 2
added = a + a

# Reduction operations
total = a.sum()
row_max = a.max(axis=1)
col_mean = a.mean(axis=0)

# Indexing (CSR/CSC formats)
element = a[0, 2]
row = a[1, :]
submatrix = a[:2, :2]

# Eliminate explicit zeros
a.eliminate_zeros()

# Sum duplicate entries
a.sum_duplicates()
```

### Sparse Linear Algebra

```python
from scipy.sparse import linalg as splinalg
from scipy import sparse
import numpy as np

# Create a sparse system
A = sparse.csr_array([[3, 0, 1], [0, 4, 0], [1, 0, 2]])
b = np.array([1, 2, 3])

# Solve linear system Ax = b
x = splinalg.spsolve(A, b)

# Iterative solvers for large systems
x, info = splinalg.cg(A, b)  # Conjugate gradient
x, info = splinalg.gmres(A, b)  # GMRES

# Eigenvalue problems
eigenvalues, eigenvectors = splinalg.eigs(A, k=2)

# Matrix norms
norm = splinalg.norm(A)
```

### Sparse Graph Algorithms

```python
from scipy.sparse import csgraph
from scipy import sparse
import numpy as np

# Create adjacency matrix
graph = sparse.csr_array([
    [0, 1, 2, 0],
    [1, 0, 0, 1],
    [2, 0, 0, 3],
    [0, 1, 3, 0]
])

# Shortest paths
dist_matrix = csgraph.dijkstra(graph, indices=0)
all_pairs = csgraph.floyd_warshall(graph)

# Minimum spanning tree
mst = csgraph.minimum_spanning_tree(graph)

# Connected components
n_components, labels = csgraph.connected_components(graph)

# Breadth-first search
bfs_tree = csgraph.breadth_first_tree(graph, 0)

# Depth-first search
dfs_tree = csgraph.depth_first_tree(graph, 0)
```

## Fast Fourier Transform

```python
from scipy import fft
import numpy as np

# 1D FFT
x = np.array([1.0, 2.0, 1.0, -1.0, 1.5])
y = fft.fft(x)
x_recovered = fft.ifft(y)

# Real FFT (more efficient for real input)
y = fft.rfft(x)
x_recovered = fft.irfft(y)

# 2D FFT
image = np.random.rand(100, 100)
freq = fft.fft2(image)
image_recovered = fft.ifft2(freq)

# FFT with shifting
freq_shifted = fft.fftshift(freq)
freq_unshifted = fft.ifftshift(freq_shifted)

# Frequency bins
freqs = fft.fftfreq(len(x), d=0.1)  # d is sample spacing
```

## Optimization

### Minimization

```python
from scipy import optimize
import numpy as np

# Define objective function
def rosenbrock(x):
    return sum(100.0 * (x[1:] - x[:-1]**2)**2 + (1 - x[:-1])**2)

# Unconstrained minimization
x0 = np.array([1.3, 0.7, 0.8, 1.9, 1.2])
result = optimize.minimize(rosenbrock, x0, method='BFGS')
print(result.x, result.fun)

# With constraints
def constraint(x):
    return x[0] + x[1] - 1

cons = {'type': 'eq', 'fun': constraint}
result = optimize.minimize(rosenbrock, x0, method='SLSQP', constraints=cons)

# With bounds
bounds = [(0, None), (0, None), (0, None), (0, None), (0, None)]
result = optimize.minimize(rosenbrock, x0, method='L-BFGS-B', bounds=bounds)
```

### Global Optimization

```python
from scipy.optimize import differential_evolution
import numpy as np

# Define function to minimize
def objective(x):
    return x[0]**2 + x[1]**2

# Global optimization
bounds = [(-5, 5), (-5, 5)]
result = differential_evolution(objective, bounds)
print(result.x, result.fun)

# With more control
result = differential_evolution(
    objective, 
    bounds,
    strategy='best1bin',
    maxiter=1000,
    popsize=15,
    tol=0.01,
    mutation=(0.5, 1),
    recombination=0.7,
    workers=4  # Parallel execution
)
```

### Root Finding

```python
from scipy import optimize

# Find root of scalar function
def f(x):
    return x**3 - 1

root = optimize.brentq(f, -2, 2)

# Newton's method
root = optimize.newton(f, x0=0.5)

# System of equations
def equations(vars):
    x, y = vars
    return [x**2 + y**2 - 1, x - y]

solution = optimize.fsolve(equations, [1, 1])
```

### Curve Fitting

```python
from scipy import optimize
import numpy as np

# Data
xdata = np.array([0, 1, 2, 3, 4])
ydata = np.array([1, 3, 5, 7, 9])

# Define model
def model(x, a, b):
    return a * x + b

# Fit
params, cov = optimize.curve_fit(model, xdata, ydata)
print(f"a={params[0]}, b={params[1]}")
```

## Orthogonal Distance Regression

ODR fits models to data with errors in both x and y coordinates.

### Basic ODR Usage

```python
from scipy import odr
import numpy as np

# Define model function
def linear_func(B, x):
    return B[0] * x + B[1]

# Create data
x = np.array([0., 1., 2., 3., 4., 5.])
y = np.array([1.2, 2.9, 5.1, 6.8, 8.9, 11.2])

# Create ODR objects
data = odr.Data(x, y)
model = odr.Model(linear_func)
odr_obj = odr.ODR(data, model, beta0=[1., 0.])

# Run fit
output = odr_obj.run()
print(f"Fitted parameters: {output.beta}")
print(f"Standard errors: {output.sd_beta}")
print(f"Covariance: {output.cov_beta}")
```

### ODR with Measurement Errors

```python
from scipy import odr
import numpy as np

# Data with uncertainties
x = np.array([0., 0.9, 1.8, 2.6, 3.3, 4.4, 5.2, 6.1, 6.5, 7.4])
y = np.array([5.9, 5.4, 4.4, 4.6, 3.5, 3.7, 2.8, 2.8, 2.4, 1.5])
x_err = np.array([0.03, 0.03, 0.04, 0.035, 0.07, 0.11, 0.13, 0.22, 0.74, 1.])
y_err = np.array([1., 0.74, 0.5, 0.35, 0.22, 0.22, 0.12, 0.12, 0.1, 0.04])

# Define model
def func(B, x):
    return B[0] * x + B[1]

# Create RealData with errors
data = odr.RealData(x, y, sx=x_err, sy=y_err)
model = odr.Model(func)
odr_obj = odr.ODR(data, model, beta0=[0., 1.])

# Run and get output
output = odr_obj.run()
output.pprint()
```

### Built-in ODR Models

```python
from scipy import odr
import numpy as np

# Linear model
x = np.linspace(0.0, 5.0)
y = 10.0 + 5.0 * x
data = odr.Data(x, y)
odr_obj = odr.ODR(data, odr.multilinear)
output = odr_obj.run()
print(f"Linear fit: {output.beta}")  # [10.0, 5.0]

# Exponential model: y = B[0] + exp(B[1] * x)
y = -10.0 + np.exp(0.5 * x)
data = odr.Data(x, y)
odr_obj = odr.ODR(data, odr.exponential)
output = odr_obj.run()
print(f"Exponential fit: {output.beta}")  # [-10.0, 0.5]

# Quadratic model: y = B[0]*x^2 + B[1]*x + B[2]
y = 1.0 * x**2 + 2.0 * x + 3.0
data = odr.Data(x, y)
odr_obj = odr.ODR(data, odr.quadratic)
output = odr_obj.run()
print(f"Quadratic fit: {output.beta}")  # [1.0, 2.0, 3.0]

# Polynomial of arbitrary degree
y = 1.0 + 2.0 * x + 3.0 * x**2 + 4.0 * x**3
poly_model = odr.polynomial(3)  # degree 3
data = odr.Data(x, y)
odr_obj = odr.ODR(data, poly_model)
output = odr_obj.run()
print(f"Polynomial fit: {output.beta}")  # [1.0, 2.0, 3.0, 4.0]
```

### Advanced ODR Features

```python
from scipy import odr
import numpy as np

# Define model with Jacobians for better performance
def func(B, x):
    return B[0] + B[1] * np.power(np.exp(B[2]*x) - 1.0, 2)

def fjacb(B, x):
    """Jacobian with respect to parameters"""
    eBx = np.exp(B[2]*x)
    return np.vstack([
        np.ones(x.shape[-1]),
        np.power(eBx - 1.0, 2),
        B[1] * 2.0 * (eBx - 1.0) * eBx * x
    ])

def fjacd(B, x):
    """Jacobian with respect to data"""
    eBx = np.exp(B[2]*x)
    return B[1] * 2.0 * (eBx - 1.0) * B[2] * eBx

# Create model with Jacobians
model = odr.Model(func, fjacb=fjacb, fjacd=fjacd)

# Data with fixed points
x = np.array([0., 0., 5., 7., 7.5, 10., 16., 26., 30., 34., 34.5, 100.])
y = np.array([1265., 1263.6, 1258., 1254., 1253., 1249.8, 
              1237., 1218., 1220.6, 1213.8, 1215.5, 1212.])
ifixx = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]  # Fix middle points

data = odr.Data(x, y)
odr_obj = odr.ODR(data, model, beta0=[1500., -50., -0.1], ifixx=ifixx)

# Control job parameters
odr_obj.set_job(fit_type=0)  # Explicit ODR
odr_obj.set_iprint(init=0, iter=0, final=0)  # Suppress output

# Run
output = odr_obj.run()
```

### Implicit Models

```python
from scipy import odr
import numpy as np

# Implicit model: f(B, x) = 0
# Example: ellipse equation
def implicit_func(B, x):
    """Ellipse: B[2]*(x[0]-B[0])^2 + 2*B[3]*(x[0]-B[0])*(x[1]-B[1]) + B[4]*(x[1]-B[1])^2 - 1 = 0"""
    return (B[2] * np.power(x[0] - B[0], 2) +
            2.0 * B[3] * (x[0] - B[0]) * (x[1] - B[1]) +
            B[4] * np.power(x[1] - B[1], 2) - 1.0)

# Create implicit model
model = odr.Model(implicit_func, implicit=1)

# 2D data (two rows for x and y coordinates)
x_data = np.array([[0.5, 1.2, 1.6, 1.86, 2.12, 2.36, 2.44],
                   [-0.12, -0.6, -1.0, -1.4, -2.54, -3.36, -4.0]])
y_data = np.ones(7)  # Dummy y for implicit models

data = odr.Data(x_data, y_data)
odr_obj = odr.ODR(data, model, beta0=[1., 1., 1., 1., 1.])
output = odr_obj.run()
```

## Linear Algebra

```python
from scipy import linalg
import numpy as np

# Matrix operations
A = np.array([[1, 2], [3, 4]])
b = np.array([5, 6])

# Solve linear system
x = linalg.solve(A, b)

# Matrix inverse
A_inv = linalg.inv(A)

# Determinant
det = linalg.det(A)

# Eigenvalues and eigenvectors
eigenvalues, eigenvectors = linalg.eig(A)

# Singular Value Decomposition
U, s, Vh = linalg.svd(A)

# QR decomposition
Q, R = linalg.qr(A)

# Cholesky decomposition (for positive definite matrices)
L = linalg.cholesky(A @ A.T)

# Matrix exponential
exp_A = linalg.expm(A)

# Matrix square root
sqrt_A = linalg.sqrtm(A)
```

## Integration

```python
from scipy import integrate
import numpy as np

# Integrate a function
def f(x):
    return x**2

result, error = integrate.quad(f, 0, 1)  # ∫₀¹ x² dx = 1/3

# Multiple integration
def f(y, x):
    return x * y

result = integrate.dblquad(f, 0, 1, 0, 1)  # Double integral

# Integrate samples (trapezoid rule)
x = np.linspace(0, 1, 100)
y = x**2
result = integrate.trapezoid(y, x)

# Simpson's rule
result = integrate.simpson(y, x=x)

# Solve ODE
def deriv(y, t):
    return -2 * y

y0 = 1
t = np.linspace(0, 5, 100)
solution = integrate.odeint(deriv, y0, t)
```

## Interpolation

```python
from scipy import interpolate
import numpy as np

# 1D interpolation
x = np.array([0, 1, 2, 3, 4])
y = np.array([0, 2, 1, 3, 2])

# Linear interpolation
f = interpolate.interp1d(x, y)
y_new = f(1.5)

# Cubic spline
f = interpolate.interp1d(x, y, kind='cubic')
x_new = np.linspace(0, 4, 100)
y_new = f(x_new)

# 2D interpolation
x = y = np.arange(0, 5, 1)
z = np.random.rand(5, 5)
f = interpolate.interp2d(x, y, z, kind='cubic')
z_new = f(1.5, 2.5)

# Spline fitting
tck = interpolate.splrep(x, y, s=0)  # s=0 means interpolation
y_new = interpolate.splev(x_new, tck)

# B-splines
tck, u = interpolate.splprep([x, y], s=0)
x_new, y_new = interpolate.splev(np.linspace(0, 1, 100), tck)
```

## Signal Processing

```python
from scipy import signal
import numpy as np

# Filter design
b, a = signal.butter(4, 0.1)  # 4th order Butterworth
sos = signal.butter(4, 0.1, output='sos')  # Second-order sections

# Apply filter
data = np.random.randn(1000)
filtered = signal.filtfilt(b, a, data)

# Convolution
x = np.array([1, 2, 3])
h = np.array([0, 1, 0.5])
y = signal.convolve(x, h)

# Correlation
corr = signal.correlate(x, h)

# Find peaks
peaks, properties = signal.find_peaks(data, height=0.5, distance=10)

# Spectrograms
f, t, Sxx = signal.spectrogram(data, fs=1000)

# Windows
window = signal.windows.hann(50)
```

## Statistics

```python
from scipy import stats
import numpy as np

# Distributions
norm = stats.norm(loc=0, scale=1)  # Normal distribution

# PDF, CDF, quantiles
pdf = norm.pdf(0)
cdf = norm.cdf(1.96)
quantile = norm.ppf(0.975)

# Random samples
samples = norm.rvs(size=1000)

# Statistical tests
data1 = np.random.randn(100)
data2 = np.random.randn(100) + 0.5

# T-test
statistic, pvalue = stats.ttest_ind(data1, data2)

# Kolmogorov-Smirnov test
statistic, pvalue = stats.kstest(data1, 'norm')

# Chi-square test
observed = np.array([10, 20, 30])
expected = np.array([15, 15, 30])
statistic, pvalue = stats.chisquare(observed, expected)

# Correlation
corr, pvalue = stats.pearsonr(data1[:50], data2[:50])

# Descriptive statistics
mean = np.mean(data1)
std = np.std(data1)
desc = stats.describe(data1)
```

## Image Processing

```python
from scipy import ndimage
import numpy as np

# Create sample image
image = np.random.rand(100, 100)

# Filters
smoothed = ndimage.gaussian_filter(image, sigma=2)
edges = ndimage.sobel(image)
median = ndimage.median_filter(image, size=5)

# Morphological operations
binary = image > 0.5
dilated = ndimage.binary_dilation(binary)
eroded = ndimage.binary_erosion(binary)

# Rotation
rotated = ndimage.rotate(image, 45)

# Zoom
zoomed = ndimage.zoom(image, 2.0)

# Label connected components
labeled, num_features = ndimage.label(binary)

# Measurements
sizes = ndimage.sum_labels(image, labeled, range(num_features + 1))
```

## Spatial Algorithms

```python
from scipy import spatial
import numpy as np

# Distance calculations
points1 = np.array([[0, 0], [1, 1]])
points2 = np.array([[2, 2], [3, 3]])

# Euclidean distance
dist = spatial.distance.euclidean(points1[0], points2[0])

# Distance matrix
dist_matrix = spatial.distance.cdist(points1, points2)

# K-D Tree for nearest neighbor search
points = np.random.rand(1000, 2)
tree = spatial.KDTree(points)

# Query nearest neighbors
distances, indices = tree.query([0.5, 0.5], k=5)

# Convex hull
hull = spatial.ConvexHull(points)

# Delaunay triangulation
tri = spatial.Delaunay(points)

# Voronoi diagram
vor = spatial.Voronoi(points)
```

## Constants

```python
from scipy import constants

# Physical constants
c = constants.c  # Speed of light
h = constants.h  # Planck constant
e = constants.e  # Elementary charge
G = constants.G  # Gravitational constant

# Mathematical constants
pi = constants.pi
golden = constants.golden

# Unit conversions
mile_in_meters = constants.mile
hour_in_seconds = constants.hour
eV_in_joules = constants.eV

# Prefix values
kilo = constants.kilo  # 1000
mega = constants.mega  # 1000000
```

## Pitfalls

### Sparse Array Indexing

```python
# ❌ Wrong: DIA format doesn't support indexing
from scipy import sparse
dia = sparse.dia_array([[1, 2], [3, 4]])
value = dia[0, 0]  # Raises error

# ✅ Right: Convert to CSR first
csr = dia.tocsr()
value = csr[0, 0]
```

### Duplicate Entries

```python
# ❌ Wrong: Duplicates stored separately
from scipy import sparse
row = [0, 1, 1]
col = [0, 1, 1]
data = [1, 2, 3]
```

## References

- [homepage](https://scipy.org/)
- [documentation](https://docs.scipy.org/doc/scipy/)
- [source](https://github.com/scipy/scipy)
- [download](https://github.com/scipy/scipy/releases)
- [tracker](https://github.com/scipy/scipy/issues)
