---
name: abaqus-bc
description: Define boundary conditions - fixed supports, displacements, symmetry. Use when user mentions fixed, pinned, clamped, supported, or constrained. Does NOT handle loads or forces.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(abaqus:*)
---

# Abaqus Boundary Conditions Skill

This skill defines boundary conditions (BCs) in Abaqus models. BCs constrain motion and prevent rigid body movement.

## When to Use This Skill

**Route here when user mentions:**
- "fixed", "encastre", "clamped", "welded"
- "pinned", "hinged", "simply supported"
- "roller", "sliding support"
- "symmetry", "half model", "quarter model"
- "constrain", "prevent movement"
- "prescribed displacement", "move by X mm"
- "rigid body motion error"

**Route elsewhere:**
- Forces, pressures, gravity → `/abaqus-load`
- Contact between parts → `/abaqus-interaction`
- Initial temperature/stress → `/abaqus-field`

## Key Decisions

### Step 1: What Type of Support?

| User Describes | BC Type | DOFs Constrained | Physical Meaning |
|----------------|---------|------------------|------------------|
| "Fixed", "clamped", "welded" | Encastre | All 6 | Fully rigid connection |
| "Pinned", "hinged" | DisplacementBC | U1, U2, U3 only | Rotation allowed |
| "Roller", "sliding" | DisplacementBC | 1 translation | Free in-plane motion |
| "Half model", "symmetric" | XsymmBC/YsymmBC/ZsymmBC | Normal + 2 rotations | Symmetry plane |
| "Move it 5mm" | DisplacementBC | Specified value | Prescribed motion |

**Default choice:** Encastre for fixed supports (most common).

### Step 2: Which Step to Apply?

| BC Purpose | Apply In | Reason |
|------------|----------|--------|
| Fixed support | Initial | Active before loads |
| Prescribed displacement | Load step | Applied with loading |
| Released BC | Later step | Use FREED to release |

**Default:** Apply supports in 'Initial' step.

### Step 3: Rigid Body Motion Check

For 3D static analysis, constrain at least 6 DOFs total:
- 3 translations (X, Y, Z)
- 3 rotations (about X, Y, Z axes)

| Configuration | Stability |
|---------------|-----------|
| One face Encastre | Fully constrained |
| Three pinned points (non-collinear) | Fully constrained |
| One vertex + symmetry planes | May be sufficient |

**"Zero pivot" error = insufficient constraints.**

### Step 4: Symmetry Plane Selection

| Symmetry BC | Apply When | Constrains |
|-------------|------------|------------|
| XsymmBC | Symmetric about YZ plane (X=const) | U1, UR2, UR3 |
| YsymmBC | Symmetric about XZ plane (Y=const) | U2, UR1, UR3 |
| ZsymmBC | Symmetric about XY plane (Z=const) | U3, UR1, UR2 |

Apply symmetry BC to the face AT the symmetry plane.

## What to Ask User

If unclear, ask:

1. **Where is it supported?**
   - "Which face/edge is fixed?"
   - "Where does it mount to the frame?"

2. **What type of support?**
   - "Fully fixed (welded) or can it rotate (pinned)?"
   - "Free to slide in any direction?"

3. **Is the model symmetric?**
   - "Can we use half symmetry to reduce model size?"
   - "Is the loading also symmetric?"

4. **Any prescribed motion?**
   - "Does anything move by a known amount?"
   - "Is this a displacement-controlled test?"

## Validation Checklist

Before running analysis:
- [ ] At least one region has fixed support
- [ ] All 6 rigid body modes constrained
- [ ] BCs applied in correct step
- [ ] Symmetry planes match actual symmetry (geometry AND loads)
- [ ] No conflicting BCs on same DOF

After analysis:
- [ ] Reaction forces at supports balance applied loads
- [ ] No "zero pivot" or "rigid body motion" warnings
- [ ] Displacements at fixed regions are zero

## Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Missing BC | Zero pivot error | Add Encastre to a face |
| Over-constraint | Warning in .dat file | Remove redundant BC |
| BC on wrong region | Model flies away | Verify findAt coordinates |
| Symmetry without symmetric load | Wrong results | Ensure loads are also symmetric |
| Pinned beam (no rotation) | Unrealistic stress | Use Encastre or add rotational stiffness |

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| "Zero pivot" | Insufficient constraints | Add more BCs |
| "Negative eigenvalue" | Unstable / buckling | Check supports, may need stabilization |
| "Face not found" | Wrong findAt coordinates | Use bounding box method |
| "Over-constraint" | Conflicting BCs | Remove duplicate BC on same DOF |

## Code Patterns

For API syntax and code examples, see:
- [API Quick Reference](references/api-quick-ref.md)
- [Common Patterns](references/common-patterns.md)
- [Troubleshooting Guide](references/troubleshooting.md)
