---
name: abaqus-shape-optimization
description: Optimize fillet/notch geometry. Use when user mentions stress concentration, fillet optimization, reshaping surfaces, or reducing peak stress. Moves surfaces only.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(abaqus:*)
  - Skill
---

# Abaqus Shape Optimization Skill

Optimize surface geometry to reduce stress concentrations. Shape optimization moves existing surfaces without adding or removing material.

## When to Use This Skill

**Route here when user mentions:**
- "stress concentration", "reduce peak stress"
- "fillet optimization", "optimize fillet radius"
- "reshape surface", "smooth geometry"
- "improve fatigue life", "notch optimization"

**Route elsewhere:**
- Adding/removing material (holes, organic forms) → `/abaqus-topology-optimization`
- Low-level optimization setup → `/abaqus-optimization`
- Running the optimization job → `/abaqus-job`

## Shape vs Topology Optimization

| Aspect | Shape Optimization | Topology Optimization |
|--------|-------------------|----------------------|
| What changes | Surface positions | Material presence |
| Result | Smooth surfaces | Holes, organic forms |
| Manufacturing | Traditional machining | Often needs AM/casting |
| Design freedom | Limited | High |
| Best for | Refine existing design | Conceptual design |

**Rule of thumb:** Use shape optimization when you have a good design with local stress issues. Use topology when starting fresh or need major redesign.

## Prerequisites

Before shape optimization:
1. ✅ Working static analysis that converges
2. ✅ Identified high-stress surface region
3. ✅ Full Abaqus license with Tosca (not Learning Edition)

## Workflow: Shape Optimization

### Step 1: Run Baseline Analysis

Run static analysis to identify stress concentrations. Note peak stress location and magnitude for comparison baseline.

### Step 2: Identify Design Surfaces

Ask user if unclear: Which surfaces can be modified? Which must remain fixed?

Only select surfaces that can be modified in manufacturing, are not functional interfaces, and don't have attached features.

### Step 3: Define Movement Limits

Get maximum growth/shrink (mm). Typical values: 3-10mm depending on part size.

### Step 4: Choose Objective

| User Goal | Objective | Design Response |
|-----------|-----------|-----------------|
| Reduce stress concentration | MINIMIZE_MAXIMUM | STRESS (MISES) |
| Uniform stress distribution | MINIMIZE_MAXIMUM | MAX_PRINCIPAL_STRESS |
| Maximize stiffness | MINIMIZE_MAXIMUM | STRAIN_ENERGY |

### Step 5: Add Constraints and Geometric Restrictions

Protect critical regions: BC surfaces, load surfaces, mating interfaces, precision features.

Common constraints: volume ≤ initial, maintain planar surfaces, mesh quality.

### Step 6: Run Optimization

Set design cycles (20-30) and submit the optimization process.

## Key Parameters

| Parameter | Recommended | Notes |
|-----------|-------------|-------|
| Max movement | 3-10mm | Based on part size |
| Design cycles | 20-30 | More for complex shapes |
| Mesh quality | MEDIUM | Balance speed/quality |
| Smoothing | LAPLACIAN | Prevents mesh distortion |

## What to Ask User

If not specified, clarify:
1. **Which surface to reshape?** - "The inner fillet at the L-bracket corner"
2. **Maximum allowed movement?** - "Up to 5mm growth, 3mm shrink"
3. **Stress reduction target?** - "Reduce from 450 MPa to under 300 MPa"
4. **Volume constraint?** - "Keep volume within 5% of original"

## Validation Checklist

After optimization completes, verify:
- [ ] Peak stress reduced at critical location
- [ ] Volume constraint satisfied
- [ ] Geometry still manufacturable
- [ ] No mesh distortion warnings
- [ ] Results converged (objective stable)

## Post-Processing

1. Compare initial vs optimized stress contours
2. Export modified geometry if needed
3. Run final validation FEA on optimized shape
4. Check manufacturability with CAM or manufacturing engineer

## Troubleshooting

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| Mesh distortion | Movement limits too large | Reduce max growth/shrink |
| No improvement | Wrong design surfaces | Verify surface selection |
| Convergence failure | Aggressive optimization | Add smoothing, smaller steps |
| Volume increase | No volume constraint | Add volume ≤ initial constraint |
| "License error" | No Tosca module | Requires full Abaqus |

## Code Patterns

For actual API syntax and code examples, see:
- [Shape Optimization API](references/shape-optimization-api.md)
- [Design Variable Setup](references/design-variables.md)
- [Geometric Restrictions](references/geometric-restrictions.md)

## Related Skills

- `/abaqus-optimization` - Base optimization API and concepts
- `/abaqus-topology-optimization` - For material removal optimization
- `/abaqus-static-analysis` - Required baseline analysis
