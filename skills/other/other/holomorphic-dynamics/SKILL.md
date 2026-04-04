---
name: holomorphic-dynamics
description: >
  Educational pack for holomorphic dynamics, complex iteration, fractal
  geometry, and data-driven dynamics (DMD/Koopman). Use this skill when
  the user asks about: complex dynamics, iteration on the complex plane,
  Julia sets, Mandelbrot sets, fixed points and stability, period doubling,
  bifurcation, topology of the complex plane, DMD (Dynamic Mode Decomposition),
  Koopman operator theory, skill dynamics as a dynamical system, fractal
  rendering, escape-time algorithms, or connections between dynamics and
  deep learning.
user-invocable: true
---

# Holomorphic Dynamics Educational Pack

## Overview

This educational pack teaches holomorphic dynamics from first principles
through ten progressive modules. Starting with iteration on the complex
plane (HD-01) and building through fixed points, fractal sets, topology,
and deep learning connections, the pack culminates in data-driven dynamics
with Dynamic Mode Decomposition (HD-09) and Koopman operator theory (HD-10).

The pack is self-contained: all complex arithmetic, iteration engines,
fractal renderers, and DMD algorithms are implemented from scratch with
no external math libraries. Every algorithm is transparent and educational
rather than optimized for production performance.

**What you will learn:**

- How iteration of simple functions on the complex plane produces fractal
  structures of extraordinary complexity
- The classification of fixed points by their multiplier and what each
  classification means dynamically
- Why the Mandelbrot set is the "atlas" of all quadratic Julia sets
- The Fatou-Julia dichotomy: stable domains versus chaotic boundaries
- How period doubling cascades lead to chaos through Feigenbaum universality
- The topological properties that constrain what dynamical systems can do
- The surprising bridge between holomorphic dynamics and deep learning
- How skill-creator itself can be modeled as a dynamical system on the
  complex plane, with skills as orbits converging to fixed points
- Data-driven dynamics: extracting coherent spatiotemporal modes from
  snapshot data using DMD and its variants
- The Koopman operator: lifting nonlinear dynamics into an infinite-
  dimensional linear framework where spectral analysis applies

**Who this is for:**

Developers, mathematicians, and curious minds who want to understand
the mathematics behind fractals, chaos, and data-driven modeling. No
prior knowledge of complex analysis is assumed; each module builds on
the previous one.

## Quick Start

Import any function directly from the holomorphic barrel:

```typescript
import {
  computeOrbit, renderMandelbrot, classifyFixedPoint,
  dmd, classifyDMDEigenvalue, bridgeDMDToSkillDynamics,
} from '../src/holomorphic';
```

Each module in `src/holomorphic/modules/HD-XX/` contains:

- **content.md** -- Educational text explaining the mathematics
- **try-session.ts** -- Interactive TypeScript code to experiment with
  (some modules also have try-session.py for Python/PyDMD examples)

To run a try-session, import and call its exported function:

```typescript
import { runTrySession } from '../src/holomorphic/modules/HD-01/try-session';
runTrySession();
```

## Module Guide

### HD-01: Iteration on the Complex Plane

The foundation. Defines orbits of the quadratic map f(z) = z^2 + c,
escape radius, escape time, and the four fundamental orbit behaviors
(converging, periodic, chaotic, escaping). Introduces the computational
engine behind all of holomorphic dynamics.

**Path:** `src/holomorphic/modules/HD-01/`

### HD-02: Fixed Points and Stability

Analyzes what happens when orbits converge. Classifies fixed points
by their multiplier lambda: superattracting (|lambda| = 0), attracting
(|lambda| < 1), indifferent (|lambda| = 1), and repelling (|lambda| > 1).
Covers the linearization theorem and basins of attraction.

**Path:** `src/holomorphic/modules/HD-02/`

### HD-03: The Mandelbrot Set

The parameter space of the quadratic family. Defines the Mandelbrot set
M as the set of c-values for which the critical orbit remains bounded.
Covers the cardioid and period bulbs, the relationship between M and
Julia sets, and escape-time rendering algorithms.

**Path:** `src/holomorphic/modules/HD-03/`

### HD-04: Julia Sets and Fatou Sets

The dynamical plane partition. For each c, the Julia set J(f) is the
boundary between chaos and stability, while the Fatou set F(f) is the
complement of stable, predictable behavior. Covers the Fatou-Julia
dichotomy, connected versus Cantor dust Julia sets, and the relationship
between the Mandelbrot set and Julia set topology.

**Path:** `src/holomorphic/modules/HD-04/`

### HD-05: Cycles and Period Doubling

Periodic orbits and the route to chaos. Covers period-n cycles, the
period-doubling cascade, Feigenbaum's universal constant (delta = 4.669...),
and bifurcation diagrams. Shows how simple parameter changes drive a
system from order through period doubling into chaos.

**Path:** `src/holomorphic/modules/HD-05/`

### HD-06: Topology of the Complex Plane

The geometric and topological properties that constrain dynamics. Covers
connectedness, simple connectedness, the Riemann sphere, conformal maps,
and how topology determines the possible behaviors of holomorphic maps.
Includes references to Meyerson, Greene-Lobb, and the MAT327 course.

**Path:** `src/holomorphic/modules/HD-06/`

### HD-07: From Dynamics to Deep Learning

The bridge between holomorphic dynamics and neural networks. Shows how
deep learning can be viewed as iterated function composition, how
activation functions relate to holomorphic maps, and how concepts like
fixed points, stability, and bifurcation appear in the training dynamics
of neural networks.

**Path:** `src/holomorphic/modules/HD-07/`

### HD-08: Skill-Creator as a Dynamical System

Maps the skill-creator system onto the complex plane. Skills are
modeled as points z = r * e^(i*theta) where r is distance from mastery
and theta encodes the skill domain. Skill iteration is a contractive
affine map f(z) = alpha*z + beta. Classifies skill dynamics using the
same fixed-point taxonomy from HD-02: superattracting (compiled skills),
attracting (converging skills), indifferent (stalled skills), and
repelling (degrading skills). The Fatou-Julia classification separates
stable skill domains from chaotic boundary regions.

**Path:** `src/holomorphic/modules/HD-08/`

### HD-09: Dynamic Mode Decomposition

Data-driven dynamics extraction. DMD takes snapshot matrices of
observed system states and extracts spatiotemporal modes with associated
eigenvalues (growth/decay rates and frequencies). Covers the standard
DMD algorithm with SVD, eigenvalue classification on the unit circle,
and four variants: DMDc (control inputs), mrDMD (multi-resolution
time-scale separation), piDMD (physics-informed constraints), and
BOP-DMD (robust bootstrap optimization). Includes Python try-session
using PyDMD.

**Path:** `src/holomorphic/modules/HD-09/`

### HD-10: Koopman Operator Theory

The theoretical foundation for data-driven dynamics. The Koopman
operator K acts on observable functions rather than state vectors,
lifting nonlinear dynamics into an infinite-dimensional linear space
where spectral decomposition applies. Covers Extended DMD (EDMD) as
a finite-dimensional approximation to K, dictionary-based lifting
with polynomial and RBF observables, and the bridge from DMD eigenvalues
to skill dynamics classifications. Includes Python try-session.

**Path:** `src/holomorphic/modules/HD-10/`

## Core API

### Complex Arithmetic (`complex/arithmetic.ts`)

| Function | Signature | Description |
|----------|-----------|-------------|
| `add` | `(a, b) => ComplexNumber` | Complex addition |
| `sub` | `(a, b) => ComplexNumber` | Complex subtraction |
| `mul` | `(a, b) => ComplexNumber` | Complex multiplication |
| `div` | `(a, b) => ComplexNumber` | Complex division |
| `magnitude` | `(z) => number` | Absolute value \|z\| |
| `argument` | `(z) => number` | Phase angle arg(z) |
| `conjugate` | `(z) => ComplexNumber` | Complex conjugate |
| `cexp` | `(z) => ComplexNumber` | Complex exponential e^z |
| `cpow` | `(z, n) => ComplexNumber` | Complex power z^n |

Constants: `ZERO`, `ONE`, `I`

### Iteration Engine (`complex/iterate.ts`)

| Function | Description |
|----------|-------------|
| `computeOrbit` | Iterate f from z_0, collecting orbit points until escape or max iterations |
| `detectPeriod` | Detect periodicity in an orbit using Floyd's algorithm |
| `computeMultiplier` | Compute the derivative multiplier at a fixed point |
| `classifyFixedPoint` | Classify a fixed point by its multiplier magnitude |
| `isRationalMultipleOfPi` | Check if an angle is a rational multiple of pi |

### Fractal Renderer (`renderer/core.ts`, `renderer/helpers.ts`)

| Function | Description |
|----------|-------------|
| `renderMandelbrot` | Render the Mandelbrot set as an escape-time grid |
| `renderJulia` | Render a Julia set for parameter c as an escape-time grid |
| `renderBifurcation` | Render a bifurcation diagram over a parameter range |
| `renderOrbitPlot` | Render an orbit as a sequence of (re, im) points |
| `renderPhasePortrait` | Render a phase portrait for a region of the complex plane |
| `pixelToComplex` | Map pixel coordinates to complex plane coordinates |
| `applyZoom` | Compute zoomed bounds centered on a complex point |
| `colorMap` | Map escape time to RGB color |
| `colorFromScheme` | Map a normalized value to a color using a named scheme |

### Eigenvalue Visualization (`renderer/eigenvalue-plot.ts`)

| Function | Description |
|----------|-------------|
| `plotEigenvaluesOnUnitCircle` | Plot DMD eigenvalues on the unit circle with classification colors |

### Skill Dynamics (`dynamics/skill-dynamics.ts`)

| Function | Description |
|----------|-------------|
| `classifySkillDynamics` | Classify a skill's dynamical behavior from its position |
| `computeSkillOrbit` | Compute the orbit of a skill under the contractive affine map |
| `detectSkillFixedPoint` | Find the convergence point of a skill orbit |
| `computeSkillMultiplier` | Compute the multiplier at a skill's fixed point |
| `classifyFatouJulia` | Classify a skill as Fatou (stable) or Julia (boundary/chaotic) |
| `clampAngularVelocity` | Clamp angular velocity to prevent unrealistic skill jumps |

### DMD Core (`dmd/dmd-core.ts`)

| Function | Description |
|----------|-------------|
| `dmd` | Standard Dynamic Mode Decomposition via SVD |
| `svd` | Educational SVD using power iteration with deflation |
| `classifyDMDEigenvalue` | Classify eigenvalue: stable, unstable, neutral, oscillatory |
| `reconstructFromDMD` | Reconstruct snapshot matrix from DMD result |

### DMD Variants

| Function | Module | Description |
|----------|--------|-------------|
| `dmdc` | `dmd/dmd-control.ts` | DMDc: DMD with control inputs |
| `mrdmd` | `dmd/dmd-multiresolution.ts` | mrDMD: multi-resolution time-scale separation |
| `pidmd` | `dmd/dmd-physics.ts` | piDMD: physics-informed constraints on eigenvalues |
| `bopdmd` | `dmd/dmd-robust.ts` | BOP-DMD: robust bootstrap optimization |
| `edmd` | `dmd/koopman.ts` | EDMD: Extended DMD for Koopman approximation |
| `liftDictionary` | `dmd/koopman.ts` | Lift state vectors into dictionary function space |

### Bridge (`dmd/skill-dmd-bridge.ts`)

| Function | Description |
|----------|-------------|
| `bridgeDMDToSkillDynamics` | Map DMD eigenvalues to skill dynamics classifications |

## Learning Path

The recommended progression through the modules follows the mathematical
dependency chain. Each module builds on concepts from previous ones:

```
HD-01: Iteration on the Complex Plane
  |
  v
HD-02: Fixed Points and Stability
  |
  v
HD-03: The Mandelbrot Set  -->  HD-04: Julia Sets and Fatou Sets
  |                                |
  v                                v
HD-05: Cycles and Period Doubling
  |
  v
HD-06: Topology of the Complex Plane
  |
  v
HD-07: From Dynamics to Deep Learning
  |
  v
HD-08: Skill-Creator as a Dynamical System
  |
  v
HD-09: Dynamic Mode Decomposition
  |
  v
HD-10: Koopman Operator Theory
```

**Core track (HD-01 through HD-06):** Pure mathematics of holomorphic
dynamics, building from iteration through topology.

**Application track (HD-07 through HD-08):** Connections to deep learning
and skill-creator modeling.

**Data-driven track (HD-09 through HD-10):** Modern data-driven dynamics
methods that connect classical spectral theory to practical computation.

## Connections

### Skill-Creator Integration (HD-08)

The skill-creator system maps naturally onto holomorphic dynamics. Each
skill occupies a position z = r * e^(i*theta) on the complex plane,
where r measures distance from mastery (r = 0 is fully compiled) and
theta encodes the skill's domain. Iteration of the contractive affine
map f(z) = alpha*z + beta models how skills evolve through practice.

The fixed-point classification from HD-02 directly maps to skill states:

| Dynamics | Skill State | Meaning |
|----------|-------------|---------|
| Superattracting | Compiled | Skill is fully internalized, zero effort |
| Attracting | Converging | Skill is improving with practice |
| Rationally indifferent | Stalled | Skill is stuck at a plateau |
| Irrationally indifferent | Oscillating | Skill quality fluctuates unpredictably |
| Repelling | Degrading | Skill is being forgotten faster than practiced |

The Fatou-Julia classification from HD-04 separates stable skill domains
(predictable improvement) from chaotic boundary regions (unpredictable
skill dynamics at the edge of competence).

### Deep Learning (HD-07)

Neural network training can be viewed as iteration of a high-dimensional
map on parameter space. Learning rate acts like the parameter c in the
quadratic family: too small and training converges slowly (attracting
fixed point), too large and it diverges (escaping orbit), and at
critical values the system exhibits period doubling and chaos.

### Bounded Learning (piDMD)

Physics-informed DMD (piDMD) constrains eigenvalues to lie on the unit
circle, enforcing conservation laws. This is analogous to bounded
learning in skill-creator: the system cannot grow without bound or
decay to zero, but must preserve certain invariants during evolution.

## References

### Textbooks and Courses

- **Milnor, J.** *Dynamics in One Complex Variable* (3rd ed., Princeton
  University Press, 2006). The definitive graduate text on holomorphic
  dynamics, covering iteration theory, the Mandelbrot set, and Julia
  sets with full proofs.

- **MAT327: Introduction to Topology** (University of Toronto). Covers
  the topological foundations used in HD-06: connectedness, compactness,
  the fundamental group, and covering spaces.

### Papers

- **Schmid, P.J.** "Dynamic mode decomposition of numerical and
  experimental data." *Journal of Fluid Mechanics* 656 (2010): 5-28.
  The foundational DMD paper.

- **Tu, J.H., et al.** "On dynamic mode decomposition: theory and
  applications." *Journal of Computational Dynamics* 1.2 (2014): 391-421.
  Rigorous connection between DMD and the Koopman operator.

- **Kutz, J.N., et al.** *Dynamic Mode Decomposition: Data-Driven
  Modeling of Complex Systems.* SIAM, 2016. Comprehensive treatment
  of DMD variants including DMDc, mrDMD, and applications.

- **Brunton, S.L., et al.** "Discovering governing equations from data
  by sparse identification of nonlinear dynamical systems." *PNAS*
  113.15 (2016): 3932-3937. SINDy framework connecting to Koopman.

- **Baddoo, P.J., et al.** "Physics-informed dynamic mode decomposition
  (piDMD)." *Proceedings of the Royal Society A* 479.2271 (2023).
  Constraining DMD eigenvalues using physical invariants.

### Video

- **Parker, M.** "The Mandelbrot Set" (Numberphile). Accessible
  introduction to the Mandelbrot set for general audiences.

### Software

- **PyDMD** (https://github.com/mathLab/PyDMD). Python library for
  DMD and its variants. Used in the HD-09 and HD-10 Python try-sessions
  for comparison with the educational TypeScript implementations.

### Project References

Detailed reference notes are available in module directories:

- `modules/HD-06/references/` -- Meyerson, Greene-Lobb, MAT327
- `modules/HD-09/references/` -- PyDMD library documentation
