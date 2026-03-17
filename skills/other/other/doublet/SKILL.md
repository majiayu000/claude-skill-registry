---
name: doublet
description: Validates code and provides physics reasoning for the 2-D injection-production doublet model using streamline methods. Use when modifying streamline geometry, transport calculations (hydrodynamic, chemical, thermal), breakthrough curves, or Green's function kernels. Also use when debugging simulation behavior or explaining physics concepts.
allowed-tools: Read, Grep, Glob, Bash
---

# Doublet Streamline Model Physics Knowledge

This skill provides physics knowledge for the 2-D doublet (injection-production well pair) model using streamline methods. The model solves advection-reaction-dispersion problems along circular streamlines in a potential flow field.

## When This Skill Applies

- Modifying streamline geometry calculations (bipolar coordinates)
- Changing transport solvers (hydrodynamic, chemical, thermal)
- Implementing or modifying breakthrough curve integration
- Working with Green's function kernels for thermal transport
- Debugging unexpected breakthrough behavior
- Planning changes to physics-related code
- Explaining why the model behaves a certain way

## Core Physics Reference

The model tracks transport in a 2-D potential flow field between an injector (+a, 0) and producer (-a, 0):

| Module | Transport Type | Solution Method |
|--------|----------------|-----------------|
| Hydrodynamic | Pure advection | Time-of-flight along streamlines |
| Chemical | Advection + capacity-limited reaction | Logistic traveling wave |
| Thermal | Advection + fluid-matrix exchange | Bessel-function Green's kernel |

Key state variables:

| Variable | Symbol | Meaning | Units |
|----------|--------|---------|-------|
| Take-off angle | β | Angle at which streamline leaves injector | rad |
| Time-of-flight | τ(β) | Travel time from injector to producer | s |
| Arc position | φ | Angle along circular streamline | rad |
| Concentration | C(φ,t) | Solute mass fraction | kg/kg |
| Capacity | S(φ,t) | Remaining reaction capacity | kg/kg |
| Fluid temperature | Tf(φ,t) | Fluid temperature along streamline | °C |
| Matrix temperature | Tm(φ,t) | Rock matrix temperature | °C |

For detailed equations, see [EQUATIONS.md](EQUATIONS.md).
For symbol definitions and units, see [SYMBOLS.md](SYMBOLS.md).
For derivation logic, see [DERIVATIONS.md](DERIVATIONS.md).
For edge cases and sanity checks, see [SANITY_CHECKS.md](SANITY_CHECKS.md).

---

## Workflow A: Physics Validation

Use this workflow when reviewing or planning code changes.

### Step 1: Identify affected transport type

Determine which transport physics is affected:
- **Hydrodynamic**: Streamline geometry, time-of-flight, velocity field
- **Chemical**: Capacity-limited reaction, logistic traveling wave
- **Thermal**: Fluid-matrix exchange, Bessel function kernel

### Step 2: Check coordinate system consistency

The model uses multiple coordinate systems:
- Cartesian (x, y) for plotting
- Bipolar (ξ, β) for streamline parameterization
- Polar about streamline center (R, φ) for local calculations

Verify transformations are applied correctly.

### Step 3: Verify breakthrough integration

Breakthrough curves integrate over all streamlines:
```
C_prod(t) = (1/π) ∫_0^π C(β, t) dβ
```

Check that:
- Integration weights are correct (trapezoidal or custom)
- β limits span [0, π] (or arrived streamlines only)
- Singularities at β → 0, π are handled

### Step 4: Check Green's function stability (thermal)

For thermal transport, the Bessel kernel G(τ, t) can overflow:
- Verify exponent recentering is applied
- Check that i1e (scaled Bessel I1) is used instead of i1
- Verify prefix integrals use cumulative_trapezoid

### Step 5: Report findings

Summarize:
- Which transport type is affected
- Any coordinate transformation issues
- Any integration boundary issues
- Any numerical stability concerns
- Recommendations for correction

---

## Workflow B: Physics Reasoning

Use this workflow when explaining behavior, debugging, or proposing solutions.

### For explaining physics concepts:

1. Identify the relevant equations and parameters
2. State the physical interpretation
3. Explain cause-and-effect relationships
4. Use the derivation steps from [DERIVATIONS.md](DERIVATIONS.md) to show connections

### For debugging simulation issues:

1. Identify which transport type shows unexpected behavior
2. Check if the issue relates to:
   - Breakthrough timing (τ calculation)
   - Front retardation (reaction capacity)
   - Thermal lag (fluid-matrix exchange rates)
3. Trace through the analytical solution
4. Check edge cases against [SANITY_CHECKS.md](SANITY_CHECKS.md)

### For proposing physics-consistent changes:

1. Identify which equations are affected
2. Show how new terms integrate into the transport equations
3. Demonstrate that mass/energy balance is preserved
4. Identify any new sanity checks needed

---

## Quick Reference: Module Structure

| Module | Purpose | Key Functions |
|--------|---------|---------------|
| `doublet.py` | Main model (streamlines, chemical, thermal) | `Tf`, `Ctf`, `Cxf`, `Ttf`, `Txf`, `breakthrough` |
| `streamlines.py` | Bipolar coordinate streamlines | `streamline_bipolar`, `streamtube_width` |
| `diffusion.py` | Green's kernel solver with diffusion | `solve_kernel_capacity`, `cxfD`, `ctDf` |
| `thermal.py` | Thermal kernel (alternative impl.) | `thermal_kernel_Tf_Tm_xvec_t` |
| `thermal2.py` | Optimized thermal solver | `G_grid_efficient`, `run_breakthrough`, `Tprodf` |
| `notebook_widgets.py` | Interactive Jupyter visualizations | `visualize_*` functions |

---

## Key Physical Constraints

These must always hold:

1. **Streamline geometry**: Streamlines are circular arcs through (±a, 0)
2. **Travel time bounds**: T(β=0) = 4πna²/(3Q) is minimum arrival time
3. **Velocity singularity**: v → ∞ at wells (handled by coordinate transformation)
4. **Conservation**: Integrated flux across all streamlines equals Q
5. **Retardation**: Chemical front travels at speed v·C_inj/(C_inj + S_0)
6. **Thermal equilibrium**: As t → ∞, Tf → Tm → T_inj (behind the front)

---

## Transport Type Classification

| Transport | Governing Equation | Solution Type |
|-----------|-------------------|---------------|
| Hydrodynamic | ∂C/∂t + v·∇C = 0 | Method of characteristics |
| Chemical (no diffusion) | ∂C/∂t + v·∇C = -kCS | Logistic traveling wave |
| Chemical (with diffusion) | ∂C/∂t + v·∇C = D∇²C - kCS | Green's function convolution |
| Thermal | ∂Tf/∂t + v·∇Tf = -γ(Tf - Tm) | Bessel kernel (Eq. 47) |
| Matrix | ∂Tm/∂t = β(Tf - Tm) | Exponential convolution (Eq. 48) |

---

## Dimensionless Groups

| Group | Definition | Physical Meaning |
|-------|------------|------------------|
| Retardation R | (C_inj + S_0)/C_inj | Front slowdown factor |
| Damköhler Da | k·τ | Reaction extent over travel time |
| Péclet Pe | v·L/D | Advection vs diffusion |
| β·τ | (exchange rate)·(travel time) | Matrix equilibration extent |
| γ·τ | (exchange rate)·(travel time) | Fluid cooling extent |
