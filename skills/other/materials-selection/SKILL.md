---
name: materials-selection
description: Systematic materials selection for engineering design using performance indices, Ashby charts, multi-constraint optimization, and case-based reasoning. Covers the five-step Ashby method — function, objective, constraint, free variable, index — with worked examples for stiffness-limited beams, strength-limited ties, thermally shocked vessels, and minimum-cost components. Use when choosing among metals, polymers, ceramics, and composites under competing objectives.
type: skill
category: materials
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/materials/materials-selection/SKILL.md
superseded_by: null
---
# Materials Selection

Every engineered artifact is the intersection of a function, a shape, a process, and a material. Of those four, the material is the one most often chosen under conditions of incomplete information — thousands of candidate materials, dozens of potentially relevant properties, several competing objectives, and hard constraints on geometry, process, cost, and environmental impact. Materials selection is the discipline that turns this combinatorial mess into a defensible, auditable choice.

**Agent affinity:** ashby (Ashby charts and performance indices), bessemer (process-material coupling)

**Concept IDs:** materials-property-space, materials-performance-indices, materials-process-coupling

## The Ashby Five-Step Method

The selection procedure used throughout this skill was formalized by Michael Ashby and has become the reference approach in the field. It reduces selection to five questions that can be asked of any design problem.

1. **Function.** What does the component do? A tie carries tension. A beam resists bending. A panel resists buckling. A shaft transmits torque. A pressure vessel contains a fluid. Function determines which mechanical or physical response matters.
2. **Objective.** What is to be minimized or maximized? Mass, cost, energy, environmental impact, or a weighted combination. A single-objective problem is easier; multi-objective problems require trade-off analysis.
3. **Constraints.** What must the component satisfy absolutely? Stiffness above a threshold, strength above a threshold, fracture toughness above a threshold, operating temperature within a range, corrosion resistance in a given environment, electrical conductivity, biocompatibility, availability in a given form.
4. **Free variables.** What can the designer vary? Usually the material choice, sometimes one geometric dimension (the section radius of a beam, the thickness of a panel). A variable that is free opens optimization; a variable that is fixed becomes a constraint.
5. **Performance index.** A group of material properties whose maximum (or minimum) identifies the best material. For a light, stiff beam of fixed length and minimum mass, the index is `E^(1/2) / rho`. For a light, strong tie, the index is `sigma_f / rho`. The index is derived, not chosen — it falls out of the equations when the constraint is substituted into the objective.

## Deriving Performance Indices

Index derivation is the heart of the method. The recipe is always the same: write the objective as a function of the free variable and material properties, write the constraint as another equation, eliminate the free variable, and read off the group of material properties that appears in the objective.

### Worked example — Light, stiff beam

**Setup.** A rectangular cantilever beam of length L (fixed) carries a tip load F. The stiffness S = F/delta must exceed S0. The beam has square section of side t (free variable). Minimize mass.

**Mass.** `m = rho * L * t^2`.

**Stiffness constraint.** For a cantilever in bending, `S = C * E * I / L^3 = C * E * t^4 / (12 * L^3)`, where C is a geometric constant. Rearranging for t^2 and substituting into the mass expression gives `m = (12 * S0 * L^5 / C)^(1/2) * (rho / E^(1/2))`.

**Reading off the index.** The term in parentheses is fixed by the problem. The term `rho / E^(1/2)` is the material-dependent group. To minimize mass, **maximize `E^(1/2) / rho`**. This is the light-stiff-beam index, denoted M_1.

### Worked example — Light, strong tie

**Setup.** A tie of length L (fixed) carries tension F0. The material must not yield. Cross-section A is free. Minimize mass.

**Mass.** `m = rho * L * A`.

**Yield constraint.** `F0 / A <= sigma_f`, so `A >= F0 / sigma_f`.

**Substitution.** `m >= rho * L * F0 / sigma_f = L * F0 * (rho / sigma_f)`.

**Index.** Maximize `sigma_f / rho`. Strong, light ties want high specific strength.

### Worked example — Thermally shocked vessel

**Setup.** A vessel must tolerate a step temperature change delta-T without cracking.

**Constraint.** The thermally induced stress must not exceed fracture toughness divided by crack length: `E * alpha * delta-T <= sigma_th`, where sigma_th is the threshold stress for thermal shock. Rearranging: `delta-T <= sigma_f / (E * alpha)`.

**Index.** Maximize `sigma_f / (E * alpha)` for maximum tolerable temperature swing. Glasses lose; cordierite ceramics and graphite win.

### Common indices, tabulated

| Function + objective | Index |
|---|---|
| Stiff, light tie | `E / rho` |
| Stiff, light beam | `E^(1/2) / rho` |
| Stiff, light panel | `E^(1/3) / rho` |
| Strong, light tie | `sigma_f / rho` |
| Strong, light beam | `sigma_f^(2/3) / rho` |
| Minimum cost, stiff beam | `E^(1/2) / (rho * C_m)` |
| Thermal shock resistance | `sigma_f / (E * alpha)` |
| Spring energy density | `sigma_f^2 / E` |
| Safe pressure vessel | `K_IC / sigma_f` |
| Thermally efficient insulation | `1 / (lambda * rho * c_p)^(1/2)` |

C_m is cost per unit mass, lambda is thermal conductivity, c_p is specific heat, K_IC is plane-strain fracture toughness.

## Ashby Charts

An Ashby chart is a log-log plot of one material property against another, with every engineering material placed as a bubble sized roughly by its property range. The surprising and useful fact is that materials cluster — metals form one envelope, polymers another, ceramics another, woods and natural materials another, composites another — and performance indices appear as straight lines on the chart.

### Reading a chart

On a plot of Young's modulus `E` (vertical) against density `rho` (horizontal), both logarithmic:

- **Ceramics** sit in the upper right: high modulus, high density.
- **Metals** sit in the upper middle: high modulus, high density, wide range.
- **Polymers** sit in the lower left: low modulus, low density.
- **Elastomers** sit in the far lower left: very low modulus, moderate density.
- **Woods** sit along a diagonal line from low E / low rho to moderate E / moderate rho, grain-direction-dependent.
- **Foams** sit in the far lower-left corner: very low E, very low rho.
- **Composites** sit wherever their parents take them — CFRP near metals, GFRP below.

A line of constant `E / rho` has slope 1. A line of constant `E^(1/2) / rho` has slope 2. A line of constant `E^(1/3) / rho` has slope 3. Higher slopes reward materials in the upper left corner. The intersection of the constraint envelope with the highest-index line is the winning material.

### The selection move

Draw the chart. Overlay all constraint lines (minimum strength, maximum density, operating temperature range, etc.). The intersection is a feasible region. Within that region, draw lines of constant index. Push the index line toward higher values until it just touches one material class. That class — and the specific grades within it — is the answer.

## Handling Multiple Objectives

Real problems rarely have one objective. Minimum mass and minimum cost usually compete. Two canonical approaches.

### Weighted sum / utility function

Define a scalar objective `U = a * m + b * C`, where a and b are user-supplied weights. Choose the material minimizing U. Limitations: the weights are rarely known, and the answer is sensitive to them. Best used for comparing a short list.

### Pareto front

Plot candidate materials on a scatter of objective 1 versus objective 2 (e.g., mass versus cost). The Pareto front is the set of materials for which no other candidate beats them on both objectives simultaneously. Everything off the Pareto front is dominated and can be eliminated without further thought. The final choice sits somewhere on the front; moving along the front trades one objective for another at known rates.

## Constraint Filtering

Before any optimization, eliminate materials that cannot possibly satisfy a hard constraint.

1. **Temperature range.** Discard materials whose maximum service temperature is below the operating temperature, or whose ductile-brittle transition is above the minimum operating temperature.
2. **Corrosion resistance.** Discard materials that fail in the working environment (chlorides for stainless steels in specific grades, UV for polymers, alkaline environments for aluminum).
3. **Toxicity and biocompatibility.** Medical, food-contact, and children's-product applications carry absolute bans on certain compositions (lead, cadmium, hexavalent chromium, some nickels).
4. **Processability.** Cannot cast tungsten carbide, cannot forge thermosets, cannot extrude glass. The geometry and production method predetermine which processes are viable, which in turn limits materials.
5. **Availability.** A perfect material that is unobtainable, export-controlled, or available only as a laboratory curiosity is not a material.

Constraint filtering typically cuts the candidate set from thousands to tens. Optimization on the remainder is tractable.

## Process-Material Coupling

Materials and processes are not independent. Casting favors fluid-phase materials with reasonable shrinkage, melting temperatures accessible to foundry equipment, and low reactivity. Forging favors ductile materials at elevated temperatures. Powder metallurgy opens refractory materials unreachable by melting. Injection molding demands thermoplastics with a window between glass transition and decomposition. Selection must include process-material compatibility as a filter.

The Bessemer process is a historical reminder: the industrial availability of mild steel depended on a process breakthrough, not a materials breakthrough. For most of history, iron was cast iron (brittle, high carbon) or wrought iron (soft, low carbon). Mild steel — strong, tough, weldable — was a laboratory curiosity until Bessemer's converter made it cheap in 1856. Materials selection in 1850 and 1870 produced different answers for the same problem because the process landscape had changed.

## Cost, Embodied Energy, and Environmental Metrics

Modern selection treats cost and embodied energy as first-class properties. Both enter through performance indices like `E^(1/2) / (rho * C_m)` for cost-minimized stiff beams or `E^(1/2) / (rho * H_m)` for energy-minimized equivalents, where H_m is embodied energy per kilogram.

Recycled content, end-of-life recyclability, and process-chain emissions become constraints or soft objectives in environmentally aware selection. Aluminum recycled from scrap consumes roughly 5 percent of the energy of primary aluminum; steel from electric-arc-furnace scrap consumes roughly 30 percent of BOF steel. These are material decisions masquerading as process decisions.

## Failure Modes of the Method

**Ignoring uncertainty.** Property values in handbooks are ranges, not points. A selection that depends on a 2 percent difference in Young's modulus is inside the noise floor and should be resolved by testing, not by the chart.

**Over-constraining early.** Piling every nice-to-have into the constraint list collapses the feasible region to empty. Distinguish musts from wants; push wants into the objective as weighted terms.

**Coupling geometry to selection.** Choosing a section shape at the same time as choosing the material creates an optimization with twice the variables and half the clarity. Fix the shape class (solid rectangular beam, I-beam, thin-walled tube), then select the material for that shape, then re-optimize dimensions.

**Blind trust in the chart.** A material plotted in an Ashby chart represents a generic class. Specific alloys and grades within the class may differ by a factor of 2 in any property. Once a class wins, the selection continues within the class using grade-level data, not chart-level data.

## Cross-References

- **ashby agent:** Primary agent for selection problems. Constructs performance indices, reads Ashby charts, delivers selection reports.
- **bessemer agent:** Chair and router; also owns process-material coupling knowledge from his steelmaking history.
- **iron-and-steel-processes skill:** The steelmaking background needed to read "steel" selections at grade level.
- **nonferrous-alloys skill:** Aluminum, copper, titanium, nickel, and magnesium alloy families beyond the ferrous defaults.
- **materials-characterization skill:** When selection depends on a property outside the handbook range, measurement is required before selection can close.

## References

- Ashby, M. F. (2016). *Materials Selection in Mechanical Design*. 5th edition. Butterworth-Heinemann. (The reference text for the method in this skill.)
- Ashby, M. F., & Cebon, D. (1993). "Materials selection in mechanical design." *Journal de Physique IV*, 3, 1-9.
- Gordon, J. E. (2006). *The New Science of Strong Materials*. Princeton University Press. (Originally 1968.)
- Callister, W. D., & Rethwisch, D. G. (2018). *Materials Science and Engineering: An Introduction*. 10th edition. Wiley.
- Cottrell, A. H. (1964). *The Mechanical Properties of Matter*. Wiley.
