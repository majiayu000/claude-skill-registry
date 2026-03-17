---
name: abaqus-contact-analysis
description: Analyze multi-body contact. Use when user mentions parts touching, friction between surfaces, bolt-plate contact, press fit, or assembly with contact.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(abaqus:*)
  - Skill
---

# Abaqus Contact Analysis Workflow

This skill guides multi-body contact analysis setup. It's a **workflow skill** - use it when analyzing assemblies where surfaces touch, slide, or separate.

## When to Use This Skill

**Route here when user mentions:**
- "Parts touching each other"
- "Contact between surfaces"
- "Friction between parts"
- "Bolt and plate contact"
- "Press fit / interference fit"
- "Multi-body assembly"
- "Parts sliding on each other"
- "Impact analysis"
- "Bearing contact"

**Route elsewhere:**
- Single-body analysis → `/abaqus-static-analysis`
- Just defining contact properties → `/abaqus-interaction`
- Only boundary conditions → `/abaqus-bc`

## Prerequisites

Before contact analysis setup:
1. Separate parts exist (at least two bodies)
2. Parts are positioned in assembly with appropriate gap/interference
3. Material properties defined for all parts
4. Basic understanding of which surfaces will touch

## Workflow Steps

### Step 1: Identify Contact Pairs

Ask the user:
- Which surfaces will touch?
- Is there an initial gap or interference?
- Will surfaces slide or remain bonded?

### Step 2: Determine Master vs Slave

| Role | Should Be |
|------|-----------|
| Master | Stiffer material, coarser mesh |
| Slave | Softer material, finer mesh |

**Rule:** Slave surface nodes cannot penetrate master surface.

### Step 3: Choose Contact Type

| Scenario | Approach |
|----------|----------|
| Permanently bonded surfaces | Tie constraint (no slip/separation) |
| Sliding with friction | Surface-to-surface contact |
| Frictionless contact | Surface-to-surface, no tangential |
| Many bodies touching | General contact (auto detection) |
| Surface folding on itself | Self-contact |

### Step 4: Define Contact Property

Configure normal behavior:
- **Hard contact** - Most cases, no penetration allowed
- **Soft contact** - For rubber, foam, or gradual engagement

Configure tangential behavior (if not tied):
- **Frictionless** - Lubricated surfaces
- **Friction (Coulomb)** - Specify coefficient

### Step 5: Set Friction Coefficient

| Interface | Typical Value |
|-----------|---------------|
| Frictionless | 0.0 |
| Lubricated steel | 0.1-0.2 |
| Dry steel-on-steel | 0.3-0.5 |
| Rubber on metal | 0.5-0.8 |

Ask user if unsure about their specific interface.

### Step 6: Create Analysis Step

Contact analysis typically requires:
- Nonlinear geometry (nlgeom=ON)
- Smaller initial increment (0.1)
- More increments allowed (100+)
- Minimum increment for convergence (1e-8)

### Step 7: Request Contact Outputs

Essential output variables:
- CSTRESS - Contact pressure and shear
- CDISP - Contact displacement
- COPEN - Gap opening distance
- CSLIP - Accumulated slip

## Key Decisions

| User Need | Configuration |
|-----------|---------------|
| Bonded joint (welded, glued) | Tie constraint |
| Bolted connection | Friction contact + preload |
| Press fit | Interference + friction |
| Bearing load | Frictionless or low friction |
| Impact/crash | Explicit dynamics + general contact |

## What to Ask User

1. **Surfaces:** Which surfaces will touch?
2. **Motion:** Will parts slide, separate, or stay bonded?
3. **Friction:** Dry contact, lubricated, or frictionless?
4. **Gap/interference:** Initial configuration?
5. **Loading:** What pushes the parts together?

## Validation Checklist

After setup, verify:
- [ ] Master/slave assigned correctly (stiffer = master)
- [ ] Contact property has normal behavior defined
- [ ] Tangential behavior set (friction or frictionless)
- [ ] nlgeom=ON in analysis step
- [ ] Contact outputs requested (CSTRESS, CDISP)
- [ ] Boundary conditions don't overconstrain

## Troubleshooting

| Problem | Likely Cause | Solution |
|---------|--------------|----------|
| "Severe discontinuity" | Contact chattering | Add stabilization, smaller increments |
| "Too much penetration" | Wrong master/slave | Swap roles, refine slave mesh |
| "Contact not detected" | Surfaces too far apart | Use adjust=ON or reduce gap |
| "Convergence failure" | Difficult nonlinearity | Smaller increments, check friction |

## Code Patterns

For API syntax and code examples, see:
- [Contact API Reference](references/contact-api.md)
- [Common Contact Patterns](references/contact-patterns.md)
- [Contact Examples](references/contact-examples.md)

## Related Skills

- `/abaqus-interaction` - Contact property details
- `/abaqus-bc` - Boundary conditions
- `/abaqus-step` - Nonlinear step settings
- `/abaqus-dynamic-analysis` - For impact problems
