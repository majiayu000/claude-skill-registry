---
name: pylops
description: |
  Linear operators for large-scale inverse problems with matrix-free representations.
  Use when Claude needs to: (1) Define linear operators for forward/adjoint operations,
  (2) Solve inverse problems (deconvolution, imaging, tomography), (3) Apply signal
  processing transforms (FFT, convolution, derivatives), (4) Compose operators for
  complex workflows, (5) Perform regularized inversion with smoothness or sparsity
  constraints, (6) Process seismic or image data at scale.
version: 1.0.0
author: Geoscience Skills
license: MIT
tags: [Linear Operators, Inverse Problems, Deconvolution, Signal Processing]
dependencies: [pylops>=2.0.0, numpy, scipy]
complements: [devito, simpeg, segyio]
workflow_role: modelling
---

# PyLops - Linear Operators Library

## Quick Reference

```python
import numpy as np
import pylops

# Create operator and apply forward/adjoint
A = pylops.FirstDerivative(n=100, dtype='float64')
y = A @ x        # Forward: y = A @ x
x_adj = A.H @ y  # Adjoint: x = A.H @ y
x_est = A / y    # Solve inverse problem
```

## Key Classes

| Class | Purpose |
|-------|---------|
| `LinearOperator` | Base class for all operators |
| `VStack/HStack` | Vertical/horizontal operator stacking |
| `BlockDiag` | Block diagonal operator composition |

## Essential Operations

### Basic Operators
```python
# Diagonal operator
D = pylops.Diagonal(np.array([1., 2., 3.]))
y = D @ x; x_adj = D.H @ y

# Derivatives
D1 = pylops.FirstDerivative(n, dtype='float64')
D2 = pylops.SecondDerivative(n, dtype='float64')
G = pylops.Gradient(dims=(64, 64), dtype='float64')
```

### Convolution
```python
wavelet = np.sin(np.linspace(0, 2*np.pi, 21)) * np.hanning(21)
C = pylops.signalprocessing.Convolve1D(n, h=wavelet, offset=10)
y = C @ x      # Convolve
x_adj = C.H @ y  # Correlation (adjoint)
```

### Compose and Stack Operators
```python
# Chain: y = C @ B @ A @ x
composed = pylops.Smoothing1D(5, n) @ pylops.FirstDerivative(n) @ pylops.Identity(n)

# Stack operators
V = pylops.VStack([A, B])     # Vertical: (2n, n)
H = pylops.HStack([A, B])     # Horizontal: (n, 2n)
BD = pylops.BlockDiag([A, B]) # Block diagonal: (2n, 2n)
```

### Solve Inverse Problems
```python
# Simple least squares
x_est = A / y

# Normal equations
x_est = pylops.optimization.leastsquares.NormalEquationsInversion(A, None, y)

# Regularized inversion with smoothness
Reg = pylops.SecondDerivative(n)
x_est = pylops.optimization.leastsquares.RegularizedInversion(
    A, [Reg], y, epsRs=[0.1]
)
```

### Iterative Solvers
```python
x_lsqr = pylops.optimization.solver.lsqr(A, y, iter_lim=100)[0]
x_cgls = pylops.optimization.solver.cgls(A, y, niter=100)[0]
```

### Sparsity-Promoting Inversion
```python
x_l1 = pylops.optimization.sparsity.fista(A, y, niter=100, eps=0.1)[0]
```

## Verify Adjoint (Dot Test)

```python
A = pylops.FirstDerivative(100)
pylops.utils.dottest(A, 100, 100, verb=True)  # Dot test passed!
```

## Common Patterns

### Seismic Deconvolution
```python
C = pylops.signalprocessing.Convolve1D(n, h=wavelet, offset=len(wavelet)//2)
seismic = C @ reflectivity

# Deconvolve (regularized)
Reg = pylops.SecondDerivative(n)
reflectivity_est = pylops.optimization.leastsquares.RegularizedInversion(
    C, [Reg], seismic, epsRs=[0.01]
)
```

### Image Denoising with TV
```python
ny, nx = image.shape
G = pylops.Gradient(dims=(ny, nx))
x_tv = pylops.optimization.sparsity.splitbregman(
    pylops.Identity(ny*nx), G, image.ravel(),
    niter_inner=5, niter_outer=10, mu=1.0, epsRL1s=[0.1]
)[0].reshape(ny, nx)
```

## When to Use vs Alternatives

| Scenario | Recommendation |
|----------|---------------|
| Matrix-free linear operators for large inverse problems | **PyLops** - purpose-built, memory efficient |
| Sparse matrix operations with known structure | **scipy.sparse** - standard, well-documented |
| Simple convolution/deconvolution | **PyLops** - clean API with `Convolve1D` |
| Custom operators for small problems | **Custom NumPy/SciPy** - no extra dependency |
| GPU-accelerated linear algebra | **PyLops** - pass CuPy arrays for automatic GPU |
| Seismic deconvolution or imaging operators | **PyLops** - rich signal processing operator library |

**Choose PyLops when**: You need matrix-free linear operators that scale to large problems
without forming explicit matrices. Its operator algebra (`@`, `VStack`, `BlockDiag`) and
built-in solvers (LSQR, FISTA, Split Bregman) make inverse problem workflows concise.

**Avoid PyLops when**: Your problem is small enough for explicit matrices (use NumPy/SciPy),
or you need nonlinear operators (PyLops is strictly linear).

## Common Workflows

### Regularized seismic deconvolution

- [ ] Define wavelet array and create `Convolve1D` operator
- [ ] Generate or load seismic trace data
- [ ] Run dot test to verify operator adjoint: `pylops.utils.dottest()`
- [ ] Set up regularization operator (e.g., `SecondDerivative` for smoothness)
- [ ] Run `RegularizedInversion(C, [Reg], data, epsRs=[eps])`
- [ ] Compare estimated reflectivity against true (if available)
- [ ] Tune `epsRs` parameter: higher = smoother, lower = sharper
- [ ] For sparse solutions, use `pylops.optimization.sparsity.fista()` instead

## Tips

1. **Never form full matrix** - Use `.matvec()` and `.rmatvec()` for memory efficiency
2. **Check shapes** - Operators have `.shape` attribute like matrices
3. **Verify adjoint** - Always run `pylops.utils.dottest()` for custom operators
4. **Start simple** - Test on small problems before scaling up
5. **Use GPU** - Pass CuPy arrays for automatic GPU acceleration

## References

- **[Operators Reference](references/operators.md)** - Complete list of available operators
- **[Solvers Reference](references/solvers.md)** - Solver methods and configuration options

## Scripts

- **[scripts/deconvolution.py](scripts/deconvolution.py)** - Seismic deconvolution example
