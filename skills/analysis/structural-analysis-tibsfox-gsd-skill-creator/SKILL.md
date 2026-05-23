---
name: structural-analysis
description: Statics, dynamics, stress-strain analysis, materials selection, failure modes, and finite element analysis concepts for engineered structures. Covers free-body diagrams, equilibrium, internal forces (shear and moment), beam deflection, column buckling, material properties, factor of safety, fatigue, fracture mechanics, and FEA workflow. Use when analyzing loads on structures, selecting materials, predicting failure, or interpreting structural behavior.
type: skill
category: engineering
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/engineering/structural-analysis/SKILL.md
superseded_by: null
---
# Structural Analysis

Structural analysis is the determination of forces, stresses, and deformations in engineered structures under load. It is the foundation of structural engineering and a critical input to every design decision involving physical artifacts that must bear weight, resist wind, survive earthquakes, or simply not fall down. This skill covers the analytical toolkit from free-body diagrams through finite element concepts, with worked examples and failure case studies.

**Agent affinity:** roebling (structural and civil engineering), watt (mechanical and thermal loading)

**Concept IDs:** engr-stress-strain, engr-material-selection, engr-structural-systems, engr-structural-failure

## The Structural Analysis Toolbox

| # | Topic | Key question |
|---|---|---|
| 1 | Statics and equilibrium | Is the structure in balance? |
| 2 | Internal forces | What forces act inside the structure? |
| 3 | Stress and strain | How does the material respond to internal forces? |
| 4 | Material properties | What can the material withstand? |
| 5 | Beam analysis | How do beams carry loads? |
| 6 | Column buckling | When do slender members fail by instability? |
| 7 | Failure modes | How and why do structures fail? |
| 8 | Factor of safety | How much margin is enough? |
| 9 | FEA concepts | How do computers solve structural problems? |

## Topic 1 -- Statics and Equilibrium

A structure is in static equilibrium when all forces and moments sum to zero. This is the starting point of every structural analysis.

**Equilibrium equations (2D):**
- Sum of forces in x = 0
- Sum of forces in y = 0
- Sum of moments about any point = 0

Three equations, three unknowns. A structure with more than three unknown reaction forces requires additional equations (compatibility, material behavior) and is called statically indeterminate.

**Free-body diagram (FBD).** Isolate the structure from its supports. Replace supports with reaction forces. Show all applied loads. The FBD is the single most important tool in structural analysis. Every error in a structural calculation can be traced to an incomplete or incorrect FBD.

**Worked example.** *A simply supported beam of length L carries a point load P at midspan. Find the reactions.*

Draw the FBD: Left support provides vertical reaction R_A. Right support provides vertical reaction R_B. The beam has no horizontal loads, so horizontal reactions are zero.

Sum of vertical forces: R_A + R_B - P = 0.
Sum of moments about A: R_B * L - P * (L/2) = 0, so R_B = P/2.
Therefore R_A = P/2.

By symmetry this is obvious, but the method works for any loading.

## Topic 2 -- Internal Forces

Once external reactions are known, cut the structure at any section to find internal forces: axial force (N), shear force (V), and bending moment (M).

**Sign convention.** Positive shear: the portion to the left of the cut moves up relative to the right. Positive moment: the beam bends concave-up (sagging). Consistency matters more than convention -- pick one and hold it.

**Shear and moment diagrams.** Plot V and M along the length of the beam. These diagrams reveal where the structure experiences maximum internal forces and guide design decisions about cross-section sizing and reinforcement placement.

**Key relationships:**
- dV/dx = -w(x), where w is the distributed load intensity
- dM/dx = V
- The moment is maximum where shear passes through zero

**Worked example.** *Uniformly distributed load w on a simply supported beam of length L.*

Reactions: R_A = R_B = wL/2 (by symmetry).
Shear at x from left support: V(x) = wL/2 - wx.
V = 0 at x = L/2.
Moment at x: M(x) = (wL/2)x - (w/2)x^2.
Maximum moment at x = L/2: M_max = wL^2/8.

This formula -- wL^2/8 -- is one of the most commonly used results in structural engineering.

## Topic 3 -- Stress and Strain

**Stress** is internal force per unit area. **Strain** is deformation per unit length.

| Type | Definition | Units |
|---|---|---|
| Normal stress (sigma) | Force perpendicular to cross-section / area | Pa (N/m^2) or psi |
| Shear stress (tau) | Force parallel to cross-section / area | Pa or psi |
| Normal strain (epsilon) | Change in length / original length | dimensionless |
| Shear strain (gamma) | Angular distortion | radians |

**Hooke's Law.** For linear elastic materials: sigma = E * epsilon, where E is the elastic modulus (Young's modulus). This is the constitutive equation that connects stress (equilibrium) to strain (deformation).

**Bending stress.** In a beam: sigma = -M*y/I, where M is the bending moment, y is the distance from the neutral axis, and I is the second moment of area (moment of inertia). Maximum stress occurs at the extreme fiber (top or bottom of the beam).

**Shear stress in beams.** tau = V*Q/(I*b), where Q is the first moment of area above (or below) the point of interest, and b is the width at that point. Maximum shear stress occurs at the neutral axis.

## Topic 4 -- Material Properties

Every material has properties that determine its structural behavior.

| Property | Symbol | What it measures |
|---|---|---|
| Elastic modulus | E | Stiffness (resistance to elastic deformation) |
| Yield strength | sigma_y | Onset of permanent deformation |
| Ultimate tensile strength | sigma_u | Maximum stress before fracture |
| Poisson's ratio | nu | Lateral contraction under axial load |
| Density | rho | Mass per unit volume |
| Thermal expansion coefficient | alpha | Length change per degree temperature change |
| Fracture toughness | K_Ic | Resistance to crack propagation |

### Material Selection

Material selection matches material properties to design requirements. The Ashby chart (property vs. property plot) is the standard tool. Common trade-offs:

- **Strength vs. weight:** Aerospace demands high specific strength (sigma_y / rho). Aluminum alloys, titanium, carbon fiber composites.
- **Strength vs. cost:** Civil infrastructure favors cost-effective strength. Structural steel, reinforced concrete.
- **Stiffness vs. weight:** Precision instruments need high specific stiffness (E / rho).
- **Ductility vs. strength:** Ductile materials (mild steel) give warning before failure. Brittle materials (cast iron, glass) do not.

**The ductility imperative.** In structural engineering, ductile failure modes are preferred over brittle ones because ductile failure provides visible warning (deformation) before collapse. Design codes enforce this by requiring ductile materials and ductile connection details.

## Topic 5 -- Beam Analysis

Beams are the workhorses of structural engineering. Common boundary conditions:

| Type | Reactions | Determinacy |
|---|---|---|
| Simply supported | 2 vertical, 1 horizontal | Determinate |
| Cantilever | 1 vertical, 1 horizontal, 1 moment | Determinate |
| Fixed-fixed | 2 vertical, 2 horizontal, 2 moments | Indeterminate |
| Continuous (multi-span) | Multiple vertical reactions | Indeterminate |

**Deflection.** Beam deflection is found by double integration of the moment-curvature relationship: EI * d^2y/dx^2 = M(x). Standard results:

| Loading | Maximum deflection |
|---|---|
| Point load P at midspan, simply supported | PL^3 / (48EI) |
| Uniform load w, simply supported | 5wL^4 / (384EI) |
| Point load P at free end, cantilever | PL^3 / (3EI) |

**Deflection limits.** Codes limit deflection to prevent serviceability problems (cracking of finishes, discomfort, damage to non-structural elements). Common limit: L/360 for floor beams under live load.

## Topic 6 -- Column Buckling

Slender compression members can fail by buckling -- a sudden lateral deflection -- at loads well below the material's compressive strength.

**Euler's critical load.** P_cr = pi^2 * EI / (KL)^2, where K is the effective length factor (depends on end conditions: K=1 for pinned-pinned, K=0.5 for fixed-fixed, K=2 for fixed-free, K=0.7 for fixed-pinned) and L is the column length.

**Slenderness ratio.** KL/r, where r is the radius of gyration (r = sqrt(I/A)). High slenderness means buckling governs. Low slenderness means material yielding governs. The transition is defined by the column curve in design codes (AISC, Eurocode).

**Critical discipline.** Always check buckling for compression members. The Euler load decreases with the square of the length -- doubling the length reduces the critical load by a factor of four.

## Topic 7 -- Failure Modes

Structures fail in predictable ways. Understanding failure modes is the key to preventing them.

| Mode | Mechanism | Example |
|---|---|---|
| Yielding | Stress exceeds yield strength | Steel beam under excessive load |
| Fracture | Crack propagates through material | Brittle failure of cast iron |
| Buckling | Instability in compression | Slender column under axial load |
| Fatigue | Cyclic loading causes crack initiation and growth | Bridge members under repeated traffic loads |
| Creep | Slow deformation under sustained load at elevated temperature | Turbine blades, concrete under dead load |
| Corrosion | Material degradation from environment | Steel bridge in salt spray |
| Connection failure | Bolts, welds, or joints fail | Hyatt Regency walkway (1981) |

### Case Study -- Hyatt Regency Walkway Collapse (1981)

The suspended walkways in the Kansas City Hyatt Regency hotel collapsed during a dance, killing 114 people. The original design used a continuous rod from the ceiling through both walkway levels. During construction, the contractor changed to two shorter rods (offset connection), which doubled the load on the upper walkway connection. The change was not reviewed by the engineer of record. The connection failed under the crowd's weight.

**Lesson.** Design changes during construction must be reviewed against original design assumptions. Connection design is as important as member design. The failure was not from exotic physics -- it was elementary statics applied to the wrong connection detail.

## Topic 8 -- Factor of Safety

The factor of safety (FOS) is the ratio of the capacity of a system to the expected load: FOS = Capacity / Demand.

| Application | Typical FOS |
|---|---|
| Aerospace (human-rated) | 1.4 - 2.0 |
| Steel buildings | 1.67 (ASD) or equivalent LRFD |
| Bridges | 2.0 - 3.0 |
| Pressure vessels | 3.0 - 4.0 |
| Elevators / lifting equipment | 5.0 - 10.0 |

**Why not make the FOS infinite?** Every increase in factor of safety increases weight, cost, and material consumption. The engineer's job is to balance safety against economy -- enough margin to account for uncertainties in loads, material properties, analysis methods, and construction quality, but not so much that the design is wasteful.

**Load and Resistance Factor Design (LRFD).** Modern codes separate uncertainty into load factors (amplify loads) and resistance factors (reduce capacity). This provides more consistent reliability across different load combinations than a single factor of safety.

## Topic 9 -- Finite Element Analysis Concepts

FEA discretizes a continuous structure into small elements connected at nodes, then solves the governing equations (equilibrium, compatibility, constitutive) at each node simultaneously.

### FEA Workflow

1. **Model geometry.** Import or create the structural geometry.
2. **Mesh.** Divide into finite elements (triangles, quadrilaterals, tetrahedra, hexahedra). Finer mesh = more accurate but more expensive.
3. **Assign properties.** Material properties, cross-section properties, element types.
4. **Apply boundary conditions.** Supports, constraints, symmetry.
5. **Apply loads.** Forces, pressures, thermal loads, self-weight.
6. **Solve.** The solver assembles and solves a system of linear (or nonlinear) equations.
7. **Post-process.** Extract displacements, stresses, reactions. Check against allowable values.
8. **Verify.** Compare FEA results to hand calculations, known solutions, or experimental data.

**Critical discipline.** FEA is a tool, not an oracle. Results must be verified against engineering judgment and independent checks. A beautiful color plot of stresses is meaningless if the boundary conditions are wrong.

### Mesh Convergence

Refine the mesh until the result of interest (stress, deflection, reaction) stabilizes. If doubling the mesh density changes the answer significantly, the original mesh was too coarse.

## Cross-References

- **roebling agent:** Primary agent for structural analysis problems. Civil and structural engineering focus.
- **watt agent:** Mechanical structures, thermal stress analysis, and pressure vessel design.
- **brunel agent:** Integrated structural design within the broader engineering design cycle.
- **design-process skill:** Structural analysis feeds into Phase 5 (Analyze) and Phase 7 (Test) of the design cycle.
- **engineering-ethics skill:** Structural failure case studies and the engineer's duty to public safety.
- **prototyping-fabrication skill:** Structural testing of prototypes.
- **systems-engineering skill:** Structural analysis as a verification activity within the V-model.

## References

- Hibbeler, R. C. (2022). *Structural Analysis*. 11th edition. Pearson.
- Gere, J. M., & Goodno, B. J. (2018). *Mechanics of Materials*. 9th edition. Cengage Learning.
- Ashby, M. F. (2017). *Materials Selection in Mechanical Design*. 5th edition. Butterworth-Heinemann.
- Petroski, H. (1985). *To Engineer Is Human: The Role of Failure in Successful Design*. St. Martin's Press.
- Levy, M., & Salvadori, M. (2002). *Why Buildings Fall Down*. W. W. Norton.
- AISC. (2022). *Steel Construction Manual*. 16th edition. American Institute of Steel Construction.
