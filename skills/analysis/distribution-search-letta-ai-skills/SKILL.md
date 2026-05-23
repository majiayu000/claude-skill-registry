---
name: distribution-search
description: Guidance for finding probability distributions that satisfy specific statistical constraints such as KL divergence targets, entropy requirements, or moment conditions. This skill should be used when tasks involve constructing discrete or continuous probability distributions with specified divergence measures, entropy values, or other distributional properties through numerical optimization.
---

# Distribution Search

## Overview

This skill provides systematic approaches for finding probability distributions that meet specific statistical constraints. Common tasks include constructing distributions with target KL divergence values (forward or backward), specified entropy, moment constraints, or combinations thereof. The approach emphasizes mathematical analysis before implementation, efficient parameterization, modular code structure, and rigorous verification.

## When to Use This Skill

- Finding distributions with specific KL divergence values (forward or backward)
- Constructing distributions with target entropy
- Searching for distributions satisfying moment constraints
- Optimization problems involving probability mass/density functions
- Any task requiring numerical search over distribution parameters

## Methodology

### Phase 1: Mathematical Analysis Before Coding

Before writing any code, thoroughly analyze the mathematical constraints:

**1. Constraint Feasibility**
- Determine if a solution exists given the constraints
- Calculate bounds on achievable values (e.g., max entropy for given support)
- Identify necessary conditions for solution existence

**2. Degrees of Freedom Analysis**
- Count the number of free parameters needed
- Determine if simple parameterizations (e.g., two-group distributions) have sufficient flexibility
- Plan for more complex parameterizations if needed

**3. Analytical Derivations**
- Derive any closed-form relationships that constrain the search
- For KL divergence: H(P) = log(V) - D_KL(P||Q) when Q is uniform over vocabulary V
- Use analytical results to narrow the search space

### Phase 2: Efficient Parameterization

**Start Simple, Plan for Complexity**

1. **Two-group distributions**: Divide elements into high-probability and low-probability groups
   - Parameters: k (number of high-prob elements), p_high, p_low
   - Constraint: k * p_high + (V - k) * p_low = 1

2. **Multi-group distributions**: If two groups are insufficient, add more groups
   - More degrees of freedom allow satisfying more constraints

3. **Continuous parameterizations**: For smooth optimization landscapes
   - Softmax over logits
   - Exponential family parameterizations

**Computational Efficiency for Large Vocabularies**

For large vocabulary sizes (e.g., V = 150,000):
- Avoid creating full arrays when closed-form calculations exist
- Use analytical formulas for group-based distributions:
  ```
  Forward KL = k * p_high * log(p_high * V) + (V - k) * p_low * log(p_low * V)
  ```
- Only create full arrays for final verification

### Phase 3: Optimization Strategy

**Choose Appropriate Methods**

1. **Direct analytical solution**: When constraints reduce to solvable equations
2. **Root-finding (fsolve)**: When you have equations equal to zero
3. **Least squares (least_squares)**: When minimizing squared constraint violations
4. **Gradient-free optimization (Nelder-Mead)**: When derivatives are unavailable or noisy
5. **Grid search over discrete parameters**: For parameters like k (number of elements in a group)

**Implementation Pattern**

```python
def objective(params, target_forward_kl, target_backward_kl, vocab_size):
    # Extract parameters
    k, log_ratio = params
    k = int(round(k))

    # Compute probabilities
    p_high, p_low = compute_probs(k, log_ratio, vocab_size)

    # Validate probabilities
    if p_high <= 0 or p_low <= 0 or p_high > 1 or p_low > 1:
        return [1e10, 1e10]  # Infeasible

    # Compute KL divergences using closed-form formulas
    forward_kl = compute_forward_kl(k, p_high, p_low, vocab_size)
    backward_kl = compute_backward_kl(k, p_high, p_low, vocab_size)

    return [forward_kl - target_forward_kl, backward_kl - target_backward_kl]
```

**Grid Search for Discrete Parameters**

```python
best_solution = None
best_error = float('inf')

for k in range(1, vocab_size):
    # Optimize continuous parameters for this k
    result = optimize_continuous_params(k, targets, vocab_size)

    if result.error < best_error:
        best_error = result.error
        best_solution = result
```

### Phase 4: Code Organization

**Modular Structure to Prevent Inconsistencies**

Create separate, reusable functions for core computations:

```python
# Core computation functions - define ONCE, use everywhere
def forward_kl(p, q, mask=None):
    """Compute D_KL(P || Q) = sum_i p_i * log(p_i / q_i)"""
    if mask is None:
        mask = p > 1e-30
    return np.sum(p[mask] * np.log(p[mask] / q[mask]))

def backward_kl(p, q, mask=None):
    """Compute D_KL(Q || P) = sum_i q_i * log(q_i / p_i)"""
    if mask is None:
        mask = p > 1e-30
    return np.sum(q[mask] * np.log(q[mask] / p[mask]))

def entropy(p, mask=None):
    """Compute H(P) = -sum_i p_i * log(p_i)"""
    if mask is None:
        mask = p > 1e-30
    return -np.sum(p[mask] * np.log(p[mask]))
```

**Import in All Scripts**

```python
# In optimization script
from kl_utils import forward_kl, backward_kl

# In verification script - use SAME functions
from kl_utils import forward_kl, backward_kl
```

### Phase 5: Verification

**Verification Checklist**

For the final solution, verify:

```
Distribution Properties:
[ ] All probabilities are positive
[ ] All probabilities are <= 1
[ ] Sum of probabilities equals 1.0 (within floating-point tolerance)
[ ] No NaN or Inf values

Constraint Satisfaction:
[ ] Forward KL divergence within tolerance
[ ] Backward KL divergence within tolerance
[ ] Other constraints (entropy, moments) within tolerance

Numerical Precision:
[ ] Tolerance requirements are met (e.g., |error| < 1e-6)
[ ] Floating-point sum is acceptably close to 1.0
```

**Verification Script Structure**

```python
def verify_distribution(p, q, target_forward, target_backward, tol=1e-6):
    print(f"Sum of probabilities: {np.sum(p)}")
    print(f"Min probability: {np.min(p)}")
    print(f"Max probability: {np.max(p)}")
    print(f"Any NaN: {np.any(np.isnan(p))}")
    print(f"Any Inf: {np.any(np.isinf(p))}")

    fwd = forward_kl(p, q)
    bwd = backward_kl(p, q)

    print(f"\nForward KL: {fwd:.10f} (target: {target_forward}, error: {abs(fwd - target_forward):.2e})")
    print(f"Backward KL: {bwd:.10f} (target: {target_backward}, error: {abs(bwd - target_backward):.2e})")

    fwd_ok = abs(fwd - target_forward) < tol
    bwd_ok = abs(bwd - target_backward) < tol

    print(f"\nForward KL within tolerance: {'PASS' if fwd_ok else 'FAIL'}")
    print(f"Backward KL within tolerance: {'PASS' if bwd_ok else 'FAIL'}")

    return fwd_ok and bwd_ok
```

## Common Pitfalls

### Pitfall 1: Full Array Creation for Large Vocabularies
**Problem**: Creating arrays of size V = 150,000 elements causes memory issues and timeouts
**Solution**: Use closed-form formulas for group-based distributions; only create full arrays for final verification

### Pitfall 2: Inconsistent Formula Implementations
**Problem**: Different scripts implement KL divergence formulas differently, leading to discrepancies
**Solution**: Define core computation functions once and import them everywhere

### Pitfall 3: Incorrect Masking in KL Divergence
**Problem**: Masking logic differs between forward and backward KL, or mask sum is incorrectly used
**Solution**: Use consistent masking (p > 1e-30) and sum over masked elements, not multiply by mask count

### Pitfall 4: Insufficient Degrees of Freedom
**Problem**: Simple parameterizations cannot satisfy all constraints simultaneously
**Solution**: Analyze degrees of freedom before implementation; plan for more flexible parameterizations

### Pitfall 5: Syntax Errors from Truncated Writes
**Problem**: File writes are truncated, leaving incomplete code
**Solution**: Verify file content after every write by reading it back or attempting to import/execute

### Pitfall 6: No Feasibility Analysis
**Problem**: Attempting optimization without verifying a solution exists
**Solution**: Mathematically analyze constraints to establish feasibility before coding

### Pitfall 7: Convergence to Local Minima
**Problem**: Optimization finds a local minimum that doesn't satisfy constraints
**Solution**: Try multiple initializations; use grid search over discrete parameters; verify final solution

### Pitfall 8: Floating-Point Precision Issues
**Problem**: Probability sum not exactly 1.0 due to floating-point arithmetic
**Solution**: Use appropriate tolerances; normalize probabilities after construction; verify precision is acceptable for the task

## KL Divergence Reference

### Definitions

**Forward KL (information projection)**:
```
D_KL(P || Q) = sum_i P(i) * log(P(i) / Q(i))
```

**Backward KL (moment projection)**:
```
D_KL(Q || P) = sum_i Q(i) * log(Q(i) / P(i))
```

### Properties

- KL divergence is non-negative: D_KL >= 0
- KL divergence is asymmetric: D_KL(P || Q) != D_KL(Q || P) in general
- When Q is uniform over V elements: D_KL(P || Q) = log(V) - H(P)
- KL divergence can be infinite if P has support where Q is zero

### Closed-Form for Two-Group Distributions

For P with k elements at probability p_high and (V-k) elements at probability p_low, with Q uniform:

```
D_KL(P || Q) = k * p_high * log(p_high * V) + (V - k) * p_low * log(p_low * V)
D_KL(Q || P) = (1/V) * [k * log(1 / (V * p_high)) + (V - k) * log(1 / (V * p_low))]
             = (1/V) * [-k * log(V * p_high) - (V - k) * log(V * p_low)]
```

## Iterative Refinement Pattern

When initial approaches fail:

1. **Diagnose the failure**: Understand why constraints aren't satisfied
2. **Check mathematical feasibility**: Re-verify that a solution exists
3. **Increase flexibility**: Add more parameters or groups
4. **Adjust optimization method**: Try different solvers or initialization strategies
5. **Verify incrementally**: Test each component in isolation before integration

Avoid completely rewriting from scratch each time; instead, modularly modify specific components.
