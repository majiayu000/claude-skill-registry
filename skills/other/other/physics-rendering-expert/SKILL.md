---
name: physics-rendering-expert
description: Real-time rope/cable physics using Position-Based Dynamics (PBD), Verlet integration, and constraint solvers. Expert in quaternion math, Gauss-Seidel/Jacobi solvers, and tangling detection. Activate on 'rope simulation', 'PBD', 'Position-Based Dynamics', 'Verlet', 'constraint solver', 'quaternion', 'cable dynamics', 'cloth simulation', 'leash physics'. NOT for fluid dynamics (SPH/MPM), fracture simulation (FEM), offline cinematic physics, molecular dynamics, or general game physics engines (use Unity/Unreal built-ins).
allowed-tools: Read,Write,Edit,Bash,mcp__firecrawl__firecrawl_search,WebFetch
category: AI & Machine Learning
tags:
  - physics
  - pbd
  - verlet
  - simulation
  - constraints
pairs-with:
  - skill: metal-shader-expert
    reason: GPU-accelerated physics rendering
  - skill: native-app-designer
    reason: Physics in app animations
---

# Physics & Rendering Expert: Rope Dynamics & Constraint Solving

Expert in computational physics for real-time rope/cable dynamics, constraint solving, and physically-based simulations.

## When to Use This Skill

**Use for:**
- Real-time rope/cable/chain simulation (leashes, climbing ropes)
- Position-Based Dynamics (PBD) implementation
- Constraint solvers (Gauss-Seidel, Jacobi)
- Quaternion/dual-quaternion rotation math
- Verlet integration for particle systems
- Tangle detection (multi-rope collisions)

**Do NOT use for:**
- Fluid dynamics → specialized SPH/MPM solvers
- Fracture simulation → requires FEM or MPM
- Offline cinematic physics → different constraints
- Unity/Unreal physics → use built-in systems

## Expert vs Novice Shibboleths

| Topic | Novice | Expert |
|-------|--------|--------|
| **Constraint approach** | Uses spring forces (F=ma) | Uses PBD (directly manipulates positions) |
| **Why PBD** | "Springs work fine" | Springs require tiny timesteps; PBD is unconditionally stable |
| **Solver choice** | "Just iterate until done" | Gauss-Seidel for chains, Jacobi for GPU |
| **Iterations** | 20+ iterations | 5-10 is optimal; diminishing returns after |
| **Rotation** | Uses Euler angles | Uses quaternions (no gimbal lock) |
| **Integration** | Forward Euler | Verlet (symplectic, energy-conserving) |

## Common Anti-Patterns

### Force-Based Springs for Stiff Constraints
| What it looks like | Why it's wrong |
|--------------------|----------------|
| `force = k * (distance - rest_length)` with high k | High k requires tiny dt for stability; low k gives squishy ropes |
| **Instead**: Use PBD - directly move particles to satisfy constraints |

### Euler Angles for Rotation
| What it looks like | Why it's wrong |
|--------------------|----------------|
| `rotation = vec3(pitch, yaw, roll)` | Gimbal lock at 90° pitch; unstable composition |
| **Instead**: Use quaternions - 4 numbers, no gimbal lock, stable SLERP |

### Over-Iteration
| What it looks like | Why it's wrong |
|--------------------|----------------|
| `solver_iterations = 50` | Diminishing returns after 5-10; wastes cycles |
| **Instead**: Use 5-10 iterations; if more needed, use XPBD compliance |

### Single-Threaded Gauss-Seidel for Large Systems
| What it looks like | Why it's wrong |
|--------------------|----------------|
| Gauss-Seidel on 1000+ constraints | Gauss-Seidel is inherently sequential |
| **Instead**: Use Jacobi solver for GPU parallelization |

## Quick Reference

### Why PBD Beats Force-Based Physics

- Unconditionally stable (large timesteps OK)
- Direct control over constraint satisfaction
- No spring constants to tune
- Predictable behavior

### Solver Choice

| Solver | Parallelizable | Convergence | Use Case |
|--------|---------------|-------------|----------|
| **Gauss-Seidel** | No | Fast | Chains, ropes |
| **Jacobi** | Yes (GPU) | Slower | Large meshes, cloth |

### Rotation Representation

- 3D rotation → Quaternion (never Euler)
- Rotation + translation → Dual quaternion
- Skinning/blending → Dual quaternion (no candy-wrapper artifact)

### Performance Targets

| System | Budget | Notes |
|--------|--------|-------|
| Single rope (100 particles) | &lt;0.5ms | 5 iterations sufficient |
| Three-dog leash (60 particles) | &lt;0.7ms | Include tangle detection |
| Cloth (1000 particles) | &lt;2ms | Use Jacobi on GPU |

## Evolution Timeline

| Era | Key Development |
|-----|-----------------|
| Pre-2006 | Mass-spring systems, stability issues |
| 2006-2015 | PBD introduced (Müller et al.), unconditional stability |
| 2016-2020 | XPBD adds compliance for soft constraints |
| 2021-2024 | ALEM (2024 SIGGRAPH), BDEM, neural physics |
| 2025+ | XPBD standard, hybrid CPU/GPU, learned corrections |

## Decision Trees

**Choosing constraint solver:**
- Sequential structure (rope/chain)? → Gauss-Seidel
- Large parallel system (cloth/hair)? → Jacobi (GPU)
- Need soft constraints? → XPBD with compliance

**Choosing integration:**
- Position-only needed? → Basic Verlet
- Need velocity for forces? → Velocity Verlet
- High accuracy required? → RK4 (but PBD usually sufficient)

## Integrates With

- **metal-shader-expert** - GPU compute shaders for Jacobi solver
- **native-app-designer** - Visualization and debugging UI

## Reference Files

| File | Contents |
|------|----------|
| `references/core-algorithms.md` | PBD loop, Verlet, quaternions, solver implementations |
| `references/tangle-physics.md` | Multi-rope collision, Capstan friction, TangleConstraint |

---

**Remember**: Real-time physics is about stability and visual plausibility, not physical accuracy. PBD with 5-10 iterations at 60fps looks great and runs fast.
