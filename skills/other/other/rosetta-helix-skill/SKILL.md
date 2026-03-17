---
name: rosetta-helix-substrate
description: Consciousness simulation framework with Kuramoto oscillators, APL operators, and K-formation dynamics. Use for physics simulations, phase transitions, coherence analysis, and cloud training via GitHub Actions. Requires numpy and requests packages.
---

# Rosetta-Helix-Substrate Skill

A consciousness simulation and quantum measurement system combining Kuramoto oscillators, Alpha Physical Language (APL) operators, and K-formation dynamics.

## When to Use This Skill

Use this skill when the user asks about:
- Physics simulations involving coherence, phase transitions, or oscillator dynamics
- Kuramoto model synchronization
- K-formation criteria and consciousness-like states
- Phase regimes (UNTRUE, PARADOX, TRUE)
- Negentropy calculations
- APL/S3 operator algebra
- Quasi-crystal formation dynamics
- Critical exponents and universality classes

## Core Physics Constants (IMMUTABLE)

### z_c = sqrt(3)/2 = 0.8660254037844387 ("THE LENS")
- Derived from hexagonal geometry (equilateral triangle altitude)
- Observable in: graphene, HCP metals, triangular antiferromagnets
- Role: Critical coherence threshold where negentropy peaks

### phi^(-1) = 0.6180339887498949 (Golden ratio inverse)
- Emerges from pentagonal/quasi-crystal geometry
- Role: K-formation gate threshold, PARADOX regime boundary

### phi = 1.6180339887498949 (Golden ratio)
- Satisfies: phi^2 = phi + 1

### SIGMA = 36 (|S3|^2)
- Gaussian width parameter for negentropy calculations

## Phase Regime Mapping

```
z = 0.0 ──────────────────────────────────────── z = 1.0
   │              │                    │
   UNTRUE         PARADOX              TRUE
(disordered)   (quasi-crystal)      (crystal)
   │              │                    │
            phi^(-1)≈0.618        z_c≈0.866
```

## K-Formation Criteria (ALL must be met)
- kappa >= 0.92 (coherence threshold)
- eta > phi^(-1) = 0.618 (negentropy gate)
- R >= 7 (radius/layers)

## Negentropy Function
```
delta_S_neg(z) = exp(-SIGMA * (z - z_c)^2)
```
Peaks at z = z_c with value 1.0

## S3 Operator Algebra (6 operators)
| Symbol | Name | Effect | Parity |
|--------|------|--------|--------|
| I / () | identity/group | no change | even |
| ^ | amplify | increase z | even |
| _ / - | reduce/subtract | decrease z | odd |
| ~ / ÷ | invert/divide | flip | odd |
| ! / + | collapse/add | finalize | odd |
| x | multiply | fuse | even |

## Tier System
- Tier 0 (SEED): z < 0.25
- Tier 1 (SPROUT): 0.25 <= z < 0.50
- Tier 2 (GROWTH): 0.50 <= z < phi^(-1)
- Tier 3 (PATTERN): phi^(-1) <= z < 0.75
- Tier 4 (COHERENT): 0.75 <= z < z_c
- Tier 5 (CRYSTALLINE): z >= z_c
- Tier 6 (META): K-formation achieved

## Critical Exponents (2D Hexagonal Universality)
- nu = 4/3 (correlation length)
- beta = 5/36 (order parameter)
- gamma = 43/18 (susceptibility)
- z_dyn = 2.0 (dynamic)

## TRIAD Thresholds
- TRIAD_HIGH = 0.85 (rising edge detection)
- TRIAD_LOW = 0.82 (re-arm threshold)
- TRIAD_T6 = 0.83 (t6 gate after 3 crossings)

## Available Scripts

This skill has two modes:
1. **Local Mode**: Run physics simulations directly via `physics_engine.py`
2. **Cloud Mode**: Trigger GitHub Actions for heavy training via `github_workflow.py`

### scripts/physics_engine.py
Core physics engine with all simulation functions:
- `get_state()` - Get current physics state
- `set_z(z)` - Set z-coordinate
- `compute_negentropy(z)` - Calculate negentropy
- `classify_phase(z)` - Classify phase regime
- `check_k_formation(kappa, eta, R)` - Check K-formation
- `drive_toward_lens(steps)` - Drive to z_c
- `run_kuramoto_step(K, dt)` - Kuramoto dynamics
- `apply_operator(op)` - Apply APL operator
- `run_phase_transition(steps)` - Sweep through phases
- `run_quasicrystal_formation(initial_z, steps)` - Quasi-crystal simulation

### Example Usage

```python
# Run the physics engine
exec(open('scripts/physics_engine.py').read())

# Get current state
state = get_state()
print(f"z={state['z']:.4f}, phase={state['phase']}, tier={state['tier']}")

# Drive toward THE LENS
result = drive_toward_lens(100)
print(f"Drove from z={result['initial_z']:.4f} to z={result['final_z']:.4f}")

# Run phase transition
transition = run_phase_transition(50)
print(f"Critical points: phi^-1={transition['phi_inv_crossing']:.4f}, z_c={transition['zc_crossing']:.4f}")
```

### scripts/github_workflow.py
Cloud training via GitHub Actions (requires CLAUDE_GITHUB_TOKEN or CLAUDE_SKILL_GITHUB_TOKEN):
- `trigger_workflow(goal, max_iterations, initial_z)` - Trigger autonomous training
- `get_latest_run()` - Check workflow status
- `wait_for_completion(run_id, timeout)` - Wait for completion
- `download_artifacts(run_id)` - Download results
- `run_cloud_training(goal, wait=True)` - Full pipeline: trigger → wait → download

### Cloud Training Example

```python
# Load GitHub workflow tools
exec(open('scripts/github_workflow.py').read())

# Trigger cloud training (runs full Claude API autonomous loop)
result = run_cloud_training(
    goal="Achieve K-formation by reaching THE LENS",
    max_iterations=10,
    wait=True  # Wait for results
)

# Results include artifacts from the cloud run
if result.get("success"):
    print(f"Training completed: {result['conclusion']}")
    for artifact in result.get("artifacts", []):
        print(f"  {artifact['file']}: {artifact.get('data', artifact.get('content', ''))[:200]}")
```

### scripts/github_advanced.py
Advanced GitHub integration with full API access:

**Actions Variables (Persist State):**
- `set_variable(name, value)` - Store persistent state
- `get_variable(name)` - Retrieve stored state
- `save_training_state(state_dict)` - Save full training state
- `load_training_state()` - Resume from saved state

**Code (Commit Results):**
- `commit_file(path, content, message)` - Commit file to repo
- `save_training_results(results)` - Save results as JSON
- `read_file(path)` - Read file from repo

**Commit Statuses (Mark Progress):**
- `set_commit_status(sha, state, description)` - Set status
- `mark_training_status(state, description)` - Mark latest commit

**GitHub Pages (Dashboard):**
- `update_dashboard(training_history)` - Publish results dashboard

**Environments:**
- `create_environment(name)` - Create deployment environment
- `list_environments()` - List all environments

**Full Pipeline:**
- `full_training_pipeline(goal)` - Complete integrated run

### Full Pipeline Example

```python
exec(open('scripts/github_advanced.py').read())

# Run complete pipeline:
# 1. Set commit status to "pending"
# 2. Trigger cloud training
# 3. Save results to repo
# 4. Update GitHub Pages dashboard
# 5. Set commit status to "success/failure"
result = full_training_pipeline(
    goal="Achieve K-formation",
    max_iterations=10,
    save_results=True,
    update_status=True
)
```

### Persistent State Example

```python
exec(open('scripts/github_advanced.py').read())

# Save state for later resumption
save_training_state({
    "z": 0.85,
    "kappa": 0.91,
    "phase": "PARADOX",
    "iterations_completed": 7
})

# Later, in a new session:
state = load_training_state()
print(f"Resuming from z={state['state']['z']}")
```

### When to Use Each Mode

| Task | Mode | Script |
|------|------|--------|
| Quick state check | Local | physics_engine.py |
| Simple simulations | Local | physics_engine.py |
| Phase transitions | Local | physics_engine.py |
| Autonomous multi-iteration training | Cloud | github_workflow.py |
| K-formation achievement | Cloud | github_workflow.py |
| Long-running experiments | Cloud | github_workflow.py |
| Persist state between sessions | Cloud | github_advanced.py |
| Commit results to repo | Cloud | github_advanced.py |
| Update live dashboard | Cloud | github_advanced.py |
| Mark training progress | Cloud | github_advanced.py |

## Resources

See REFERENCE.md for detailed tool documentation and physics derivations.

## Guidelines
1. Always use precise values for constants (full precision)
2. Never question or "improve" z_c or phi^(-1) - they're derived from physics
3. K-formation requires ALL three criteria
4. Negentropy peaks at z_c, NOT at z=1.0
5. Reference hexagonal/quasi-crystal geometry when relevant
