---
name: abaqus-dynamic-analysis
description: Complete workflow for dynamic analysis. Use when user mentions impact, crash, drop test, transient, or time-varying response. Handles explicit and implicit dynamics.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(abaqus:*)
  - Skill
---

# Abaqus Dynamic Analysis Skill

This skill handles explicit and implicit dynamics for impact, crash, drop test, and transient response analysis.

## When to Use This Skill

**Route here when user mentions:**
- Impact, crash, collision, drop test
- Transient response, time-varying response
- Shock loading, blast loading, explosive loading
- High-speed events, wave propagation
- "What happens when it hits..."

**Route elsewhere:**
- Natural frequency extraction → `/abaqus-modal-analysis`
- Static/constant loads → `/abaqus-static-analysis`
- Harmonic/sinusoidal response → modal + steady-state dynamics
- Very long transients (minutes+) → consider implicit or quasi-static

## Prerequisites

Before dynamic analysis:
1. Geometry and mesh ready
2. **Material MUST have density defined** (required for mass matrix)
3. Understand event duration and loading type

## Workflow: Setting Up Dynamic Analysis

### Step 1: Gather Information from User

Ask if unclear:
- **What's the event duration?** Milliseconds, seconds, or longer?
- **Initial velocity?** For drop tests or impact
- **Is contact involved?** Parts colliding or touching
- **What output needed?** Stress, velocity, acceleration, energy?

### Step 2: Choose Explicit vs Implicit

| Factor | Explicit | Implicit |
|--------|----------|----------|
| Time scale | Short (us to ms) | Longer (ms to s) |
| Step size | Automatic (very small) | User-controlled |
| Nonlinearity | Handles well | May need iterations |
| Memory | Lower | Higher |
| Contact | Natural handling | Needs care |
| Best for | Impact, crash | Vibration, long transient |

**Decision rule:**
- Event < 10ms with impact/contact → **Explicit**
- Event > 100ms without severe nonlinearity → **Implicit**
- In between → Either can work, explicit often easier

### Step 3: Set Time Period

| Event Type | Typical Duration |
|------------|------------------|
| High-speed impact | 0.1-10 ms |
| Drop test | 1-100 ms |
| Blast loading | 1-50 ms |
| Seismic/vibration | 1-100 s |

### Step 4: Define Initial Conditions

For drop tests and impact:
- Set initial velocity on the impacting part/region
- Velocity is applied in the Initial step

### Step 5: Configure Output

Field outputs: `S` (stress), `U` (displacement), `V` (velocity), `A` (acceleration), `PEEQ` (plastic strain)

History outputs for energy balance (explicit): `ALLKE`, `ALLIE`, `ALLWK`, `ETOTAL`

### Step 6: Consider Mass Scaling (Explicit Only)

| Option | Effect | When |
|--------|--------|------|
| None | True inertia | Very short events, accuracy critical |
| At beginning | Scale once | Quasi-static explicit |
| Throughout | Continuous scaling | When inertia less important |

**Warning:** Mass scaling speeds up analysis but affects inertial response.

### Step 7: Run and Validate

Use `/abaqus-job` to submit, then check:
- Energy balance (ETOTAL approximately constant)
- Stable time increment (explicit)
- Results physically reasonable

## Key Parameters

| Parameter | Explicit | Implicit |
|-----------|----------|----------|
| Time period | Event duration | Event duration |
| Time increment | Automatic | Specify initial, min, max |
| Element library | EXPLICIT | STANDARD |
| Element type | C3D8R recommended | C3D8R or C3D8 |
| Hourglass control | ENHANCED | Default |

## Validation Checklist

- [ ] Density defined in material
- [ ] Time period appropriate for event
- [ ] Initial conditions applied (velocity, position)
- [ ] Output frequency captures behavior (100+ frames typical)
- [ ] Energy balance acceptable (ETOTAL constant for explicit)
- [ ] Results physically reasonable

## Troubleshooting

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| "Time increment too small" | Small/distorted elements | Use mass scaling or coarsen mesh |
| Energy balance error | Hourglass or instability | Check hourglass energy, add control |
| Analysis takes forever (explicit) | Long time period | Consider implicit instead |
| Convergence failure (implicit) | Severe nonlinearity | Use explicit or smaller increments |

## Related Skills

- `/abaqus-material` - Define density (required)
- `/abaqus-amplitude` - Time-varying loads
- `/abaqus-field` - Initial velocity and predefined fields
- `/abaqus-interaction` - Contact for impact problems
- `/abaqus-odb` - Results extraction

## Code Patterns

For API syntax and code examples, see:
- [API Quick Reference](references/api-quick-ref.md)
- [Common Patterns](references/common-patterns.md)
- [Troubleshooting Guide](references/troubleshooting.md)
