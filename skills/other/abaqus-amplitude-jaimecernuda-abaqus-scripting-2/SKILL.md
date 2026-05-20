---
name: abaqus-amplitude
description: Define time-varying amplitudes. Use when user mentions ramp, time-varying, cyclic, pulse, or gradually increasing loads. Does NOT handle static constant loads.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(abaqus:*)
---

# Abaqus Amplitude Skill

This skill defines time-varying load and boundary condition profiles in Abaqus. Amplitudes act as multipliers that scale loads/BCs over time.

## When to Use This Skill

**Route here when user mentions:**
- "Gradually increase the load", "ramp up the force"
- "Cyclic loading", "sinusoidal excitation"
- "Pulse load", "impulse", "impact loading"
- "Time-varying boundary condition", "loading history"
- "Smooth transition", "avoid sudden load application"
- "Earthquake input", "harmonic excitation"

**Route elsewhere:**
- Constant static loads (no amplitude needed) → `/abaqus-load`
- Initial conditions, predefined fields → `/abaqus-field`
- Dynamic analysis setup → `/abaqus-dynamic-analysis`

## Workflow: Defining Amplitudes

### Step 1: Understand User's Load Profile

Ask if unclear:
- **What shape?** Ramp, sinusoidal, pulse, decay, custom?
- **What timing?** Duration, frequency, peak time?
- **What magnitude?** Amplitude is a multiplier (0.0-1.0 typical)

### Step 2: Choose Amplitude Type

| User Describes | Amplitude Type | Key Parameters |
|----------------|----------------|----------------|
| Linear increase/decrease | TabularAmplitude | Time-value pairs |
| Smooth transition (no shock) | SmoothStepAmplitude | Time-value pairs |
| Sinusoidal/harmonic | PeriodicAmplitude | Frequency, coefficients |
| Exponential decay | DecayAmplitude | Initial, decayTime |
| Custom time history | TabularAmplitude | User-provided data |
| Sudden on/off | TabularAmplitude | Step-like data points |

**Most common:** TabularAmplitude with linear ramp (0,0) to (1,1)

### Step 3: Determine Time Reference

| Setting | When to Use |
|---------|-------------|
| `timeSpan=STEP` | Time relative to current step start (most common) |
| `timeSpan=TOTAL` | Time from analysis beginning (multi-step analyses) |

### Step 4: Define Data Points

For TabularAmplitude and SmoothStepAmplitude:
- Data is (time, amplitude_factor) pairs
- Time values must be strictly increasing
- Factor typically ranges 0.0 to 1.0 (can exceed if needed)
- Factor multiplies the load/BC magnitude

### Step 5: Apply to Load or BC

Amplitudes are referenced by name when creating:
- Loads: ConcentratedForce, Pressure, Gravity, etc.
- BCs: DisplacementBC, VelocityBC, etc.

## Key Decisions

### Common Load Profiles

| Profile | Data Pattern | Use Case |
|---------|--------------|----------|
| Linear ramp | (0,0), (1,1) | Quasi-static loading |
| Ramp up/down | (0,0), (0.5,1), (1,0) | Load cycle |
| Hold at peak | (0,0), (0.1,1), (1,1) | Ramp then sustain |
| Triangular pulse | (0,0), (0.001,1), (0.002,0) | Impact/impulse |
| Step function | (0,0), (0,1), (1,1) | Sudden application |

### Smooth vs. Tabular

| Use SmoothStepAmplitude when | Use TabularAmplitude when |
|------------------------------|---------------------------|
| Dynamic analysis (avoid shocks) | Static analysis |
| Convergence issues from sudden loads | Exact load profile needed |
| Continuous derivatives required | Step functions needed |

## What to Ask User

| Input | Required | How to Get |
|-------|----------|------------|
| Load profile shape | YES | Ask: "How should the load vary over time?" |
| Peak time | YES | Ask: "When should the load reach its maximum?" |
| Duration | YES | Typically matches step time |
| Frequency (if cyclic) | If periodic | Ask: "What frequency in Hz?" |
| Smooth or sudden | Recommended | Ask if dynamic analysis |

## Validation Checklist

After defining amplitude:
- [ ] Time values are strictly increasing
- [ ] Factor range is appropriate (usually 0.0-1.0)
- [ ] timeSpan matches analysis intent (STEP vs TOTAL)
- [ ] Amplitude name matches what load/BC references
- [ ] For dynamic: smooth transitions to avoid numerical shocks
- [ ] For periodic: frequency and coefficients are correct

## Troubleshooting

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| "Amplitude not monotonic in time" | Time values not increasing | Fix time sequence |
| Convergence issues with sudden load | Discontinuity in profile | Use SmoothStepAmplitude |
| Load too high/low | Misunderstanding multiplier | Amplitude is factor; adjust load magnitude |
| Wrong timing in multi-step | STEP vs TOTAL confusion | Check timeSpan setting |

## Code Patterns

For API syntax and code examples, see:
- [API Quick Reference](references/api-quick-ref.md) - Full parameter details
- [Common Patterns](references/common-patterns.md) - Ready-to-use snippets
- [Troubleshooting Guide](references/troubleshooting.md) - Error solutions
