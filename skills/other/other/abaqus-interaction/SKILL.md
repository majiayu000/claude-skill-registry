---
name: abaqus-interaction
description: Define contact and interactions - contact pairs, tie constraints, connectors. Use when user mentions contact, friction, tie, parts touching, or bonded surfaces.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(abaqus:*)
---

# Abaqus Interaction Skill

Define contact pairs, tie constraints, coupling, and connectors between parts in an assembly.

## When to Use This Skill

**Route here when user mentions:**
- "Contact between surfaces"
- "Friction", "sliding contact", "frictionless"
- "Tie constraint", "bonded surfaces", "welded"
- "Parts touching", "parts can separate"
- "Coupling", "connector", "spring element"
- "Join different meshes"

**Route elsewhere:**
- Complete contact analysis workflow → `/abaqus-contact-analysis`
- Fixed supports or displacements → `/abaqus-bc`
- Applied forces or pressures → `/abaqus-load`

## Key Decisions

### 1. What Type of Connection?

| User Describes | Interaction Type | Key Feature |
|----------------|------------------|-------------|
| Welded, glued, bonded | Tie constraint | Permanent, no relative motion |
| Parts can slide and separate | Surface-to-surface contact | Friction, gap allowed |
| Load from point to surface | Coupling | Reference point control |
| Spring, damper, hinge | Connector | Stiffness/damping behavior |
| Adhesive, delamination | Cohesive | Damage initiation criteria |

### 2. Contact Formulation

| Formulation | When to Use |
|-------------|-------------|
| Surface-to-surface | General contact (recommended default) |
| Node-to-surface | Legacy compatibility, special cases |
| General contact | Automatic detection (explicit dynamics) |
| Self-contact | Folding, buckling, large deformation |

### 3. Typical Friction Coefficients

| Surface Pair | Friction Coefficient |
|--------------|---------------------|
| Frictionless | 0.0 |
| Lubricated metal | 0.1 - 0.3 |
| Dry metal-to-metal | 0.3 - 0.5 |
| Rubber on surface | 0.5 - 0.8 |
| No slip (rough) | Use ROUGH formulation |

## What to Ask User

If unclear, ask:

1. **Bonded or sliding?**
   - Bonded (no relative motion) → Tie constraint
   - Sliding allowed → Contact with friction

2. **Friction coefficient?**
   - If not specified, suggest typical value for material pair
   - Frictionless is valid for lubricated or normal-dominant cases

3. **Which surface is master/slave?**
   - User may not know - guide them (see below)

4. **Can surfaces separate?**
   - Yes → `allowSeparation=ON`
   - No (always in contact) → `allowSeparation=OFF`

## Master/Slave Selection Guidelines

| Criterion | Master Surface | Slave Surface |
|-----------|----------------|---------------|
| Stiffness | Stiffer body | Softer body |
| Mesh density | Coarser mesh | Finer mesh |
| Size | Larger surface | Smaller surface |
| Geometry | Flat/convex | Curved/concave |

**When in doubt:** The coarser mesh should be master.

## Workflow: Setting Up Interactions

### Step 1: Identify Contact Pairs

List all surfaces that interact. For each pair determine:
- Type (contact vs tie)
- Master and slave assignment
- Friction requirements

### Step 2: Create Surfaces

Surfaces must be defined on assembly instances before creating interactions.

### Step 3: Define Contact Properties

For contact interactions, define:
- **Normal behavior:** Hard contact, allow separation
- **Tangential behavior:** Friction formulation and coefficient

### Step 4: Create Interaction

Assign contact property to surface pair in appropriate step.

### Step 5: Verify Setup

Check for:
- Correct master/slave assignment
- Appropriate initial gap/overclosure
- Contact pair is active in correct step

## Common Gotchas

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| Contact not detected | Surfaces too far apart | Use `adjust=ON` or reduce initial gap |
| Severe discontinuity warnings | Contact chattering | Add stabilization, use smaller increments |
| Negative eigenvalue | Wrong master/slave | Swap master and slave surfaces |
| Overclosure too large | Initial interference | Use shrink fit option or adjust geometry |
| Tie not working | Surfaces not close enough | Increase position tolerance |

## Validation Checklist

Before running analysis:
- [ ] All contacting surface pairs identified
- [ ] Master/slave correctly assigned
- [ ] Contact properties defined (normal + tangential)
- [ ] Interaction assigned to correct step
- [ ] Initial gaps/overclosures within tolerance
- [ ] Friction coefficient appropriate for materials

## Code Patterns

For API syntax and code examples, see:
- [API Quick Reference](references/api-quick-ref.md)
- [Common Patterns](references/common-patterns.md)
- [Troubleshooting Guide](references/troubleshooting.md)
