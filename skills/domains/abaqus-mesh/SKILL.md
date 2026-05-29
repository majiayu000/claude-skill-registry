---
name: abaqus-mesh
description: Generate finite element meshes. Use when user mentions mesh, elements, nodes, refine mesh, mesh size, or asks about element types like C3D8R, C3D10, S4R.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(abaqus:*)
---

# Abaqus Mesh Skill

Generate finite element meshes for Abaqus models. Discretizes geometry into elements and nodes for analysis.

## When to Use This Skill

**Route here when user mentions:**
- "Mesh the part", "generate mesh"
- "Element size", "mesh size", "refine mesh"
- "Element type", "C3D8R", "C3D10", "S4R"
- "Too many nodes", "Learning Edition limit"
- "Mesh quality", "check elements"

**Route elsewhere:**
- Creating or modifying geometry → `/abaqus-geometry`
- Creating partitions for loads/BCs → `/abaqus-geometry`
- Extracting mesh-based results → `/abaqus-odb`

## Prerequisites

Before meshing:
1. Geometry must be complete
2. Sections should be assigned (material assignment)

## Workflow: Generating a Mesh

### Step 1: Understand User's Goal

Ask if unclear:
- **Target mesh size?** Coarse (fast) or fine (accurate)?
- **Hex or tet elements?** Simple geometry → hex; complex → tet
- **Local refinement?** Stress concentrations need finer mesh

### Step 2: Choose Element Type

| Geometry | Recommended | Code | Notes |
|----------|-------------|------|-------|
| Simple box/prism | Hex, reduced | C3D8R | Fast, accurate, try first |
| Complex freeform | Tet, quadratic | C3D10 | Meshes anything |
| Thin-walled (t/L < 0.1) | Shell | S4R | Plates, shells |
| Slender beams (L/d > 10) | Beam | B31 | Frames, trusses |

**Decision guidance:**
- Can it be hex-meshed? → Try C3D8R first
- Complex shape or holes? → Use C3D10 (tet)
- Thin structure? → Use S4R shell
- Explicit dynamics? → C3D8R works well

### Step 3: Choose Mesh Size

| Use Case | Element Size | Guideline |
|----------|--------------|-----------|
| Quick feasibility | 10-20mm | 5+ elements across model |
| General analysis | 3-5mm | 10+ elements across smallest dimension |
| Stress concentrations | 1-2mm | 5+ elements in high-gradient regions |
| Topology optimization | 2-5mm | 3-5 elements across expected members |

**Rule of thumb:** At least 3 elements across any feature you care about.

### Step 4: Check Learning Edition Limits

Learning Edition allows max 1000 nodes.

| Box Dimensions (mm) | Max Element Size |
|--------------------|------------------|
| 100 x 100 x 100 | 20mm |
| 100 x 50 x 30 | 10mm |
| 50 x 50 x 50 | 12mm |
| 200 x 100 x 50 | 25mm |

**Estimation formula:** `nodes ≈ (L/size + 1) × (W/size + 1) × (H/size + 1)`

### Step 5: Apply Local Refinement (If Needed)

Refine mesh near:
- Holes and notches (stress concentrations)
- Fillets and sharp corners
- Load/BC application points

Options:
- Edge seeds with smaller size
- Edge seeds with specific element count
- Biased mesh (graded density)

### Step 6: Generate and Verify

After mesh generation, check:
- [ ] Node count within limits
- [ ] Element count reasonable
- [ ] No mesh quality warnings
- [ ] Elements exist in all regions

## Element Type Reference

### 3D Solid Elements

| Code | Type | Nodes | Use Case |
|------|------|-------|----------|
| C3D8R | Hex, reduced | 8 | General purpose (recommended) |
| C3D8 | Hex, full | 8 | Bending-dominated, no hourglass |
| C3D20R | Hex, quadratic | 20 | High accuracy, expensive |
| C3D4 | Tet, linear | 4 | Complex geometry (less accurate) |
| C3D10 | Tet, quadratic | 10 | Complex geometry (better accuracy) |

### Shell Elements

| Code | Type | Nodes | Use Case |
|------|------|-------|----------|
| S4R | Quad, reduced | 4 | General purpose (recommended) |
| S4 | Quad, full | 4 | No hourglass |
| S3 | Triangle | 3 | Complex surfaces |

## Mesh Quality Guidelines

| Metric | Target | Warning | Failure |
|--------|--------|---------|---------|
| Aspect ratio | < 5:1 | 5-10:1 | > 10:1 |
| Jacobian | > 0.5 | 0.1-0.5 | < 0.1 |
| Min angle (quad) | > 45° | 30-45° | < 30° |

## Troubleshooting

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| "Cannot mesh region" | Geometry too complex for hex | Switch to TET with FREE technique |
| "Element distortion" | Poor element shapes | Refine locally or fix geometry |
| "Exceeded node limit" | Mesh too fine | Increase element size |
| "No mesh controls" | Missing mesh technique | Set mesh controls before generating |
| Mesh won't generate | Gaps in geometry | Check geometry, merge if needed |

## Code Patterns

For API syntax and code examples, see:
- [API Quick Reference](references/api-quick-ref.md)
- [Common Patterns](references/common-patterns.md)
- [Element Library](references/element-library.md)
