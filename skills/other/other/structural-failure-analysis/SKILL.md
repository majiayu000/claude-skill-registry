---
name: structural-failure-analysis
description: Diagnosis of why structural materials fail — ductile overload, brittle cleavage, fatigue, creep, stress-corrosion cracking, hydrogen embrittlement, and corrosion. Covers Griffith fracture mechanics, the ductile-to-brittle transition, the S-N and Paris fatigue frameworks, fractographic interpretation, and the J.E. Gordon view that strength, stiffness, and toughness are distinct properties that must be understood together to prevent collapse.
type: skill
category: materials
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/materials/structural-failure-analysis/SKILL.md
superseded_by: null
---
# Structural Failure Analysis

A structural failure is a puzzle with the answer already written on the fracture surface. The task of the failure analyst is to read it: to identify the mechanism, trace it back to a cause, and recommend a fix that prevents recurrence. This skill organizes the failure modes encountered in real structures, the mechanics that govern each, and the fractographic and mechanical-test evidence that distinguishes one from another. It is written from the perspective that J.E. Gordon championed in *The New Science of Strong Materials* and *Structures*: strength, stiffness, and toughness are independent properties, and a design that optimizes one can be catastrophically weak in another.

**Agent affinity:** gordon (Gordon's structures-and-materials perspective), cottrell (dislocation theory and ductile-brittle transition)

**Concept IDs:** materials-fracture-mechanics, materials-failure-modes, materials-fractography

## The Three Independent Properties

Strength, stiffness, and toughness are not the same thing, and confusing them is the root cause of more engineering failures than any single material defect.

- **Stiffness** is resistance to elastic deformation, measured by Young's modulus E. It has almost nothing to do with strength — a tungsten carbide ceramic and a high-strength steel can have the same E while their fracture behavior differs by orders of magnitude.
- **Strength** is resistance to plastic deformation or fracture, measured by yield stress `sigma_y`, ultimate tensile stress `sigma_u`, or fracture stress.
- **Toughness** is resistance to the propagation of a crack, measured by fracture toughness `K_IC` or the energy release rate `G_IC`. A strong material can be brittle (low toughness); a weak material can be tough (high toughness). Nylon is weaker than glass but much tougher; the Comet airliner fuselage was strong but not tough enough around its window cutouts.

## Griffith Fracture Mechanics

A.A. Griffith's 1921 paper on the fracture of glass established the framework that governs brittle fracture. A sharp crack of length `2a` in a plate under remote stress `sigma` concentrates stress at its tip. The crack propagates when the elastic energy released by extending the crack exceeds the surface energy required to create the new surfaces. The result is the Griffith criterion:

`sigma_c = sqrt(2 * E * gamma_s / (pi * a))`

where `gamma_s` is the surface energy per unit area and E is Young's modulus. The critical stress falls as the square root of the crack length: longer cracks fracture at lower stresses.

In metals, the fracture energy is dominated not by surface creation but by plastic deformation near the crack tip. Irwin's modification replaces `gamma_s` with an effective fracture energy `G_IC`, and the equation becomes `K_I = sigma * sqrt(pi * a)`, with fracture occurring when the stress intensity factor `K_I` reaches the material's plane-strain fracture toughness `K_IC`. K_IC values span four orders of magnitude across materials — glass at about 0.7 MPa*m^(1/2), ceramic tools around 5, aluminum alloys 25 to 40, mild steel 100, tough structural steels 150 to 200, pure nickel above 300.

## The Ductile-Brittle Transition

Body-centered cubic metals — mild steel above all — become brittle at low temperatures. The mechanism is dislocation-based: below a critical temperature, the stress to nucleate or move dislocations rises sharply, and the material can no longer plastically blunt a crack tip before the Griffith criterion is met. Cleavage fracture takes over.

Alan Cottrell's work in the 1950s built the dislocation theory of the transition. The Cottrell mechanism involves the interaction of dislocations at grain boundaries producing microcracks, which either blunt (ductile) or propagate (brittle) depending on the temperature-dependent dislocation mobility. The Hall-Petch grain size dependence and the effect of carbon segregation on the transition temperature both follow from the Cottrell framework.

The practical test is the **Charpy V-notch**. A notched specimen is impact-loaded over a range of temperatures and the absorbed energy is plotted versus temperature. The curve is sigmoidal, dropping from an upper shelf (ductile, absorbed energy 100 to 200 J) through a transition to a lower shelf (brittle, absorbed energy 3 to 20 J). The **ductile-to-brittle transition temperature (DBTT)** is usually defined at the 50 percent fibrous fracture appearance or at a specified energy level (27 J in many specifications).

### The Liberty Ships

In 1942 to 1946, some 200 of the 2700 Liberty Ships built by the United States during the Second World War suffered significant hull fractures; 12 broke in half. The cause was the conjunction of three factors: welded construction (eliminating riveted crack-arrest boundaries), notches at hatch corners (stress concentrators), and plate steel whose DBTT was above the cold North Atlantic service temperature. Constance Tipper at Cambridge documented the mechanism as classical brittle cleavage in the sub-DBTT regime. The post-war fix was ABS-approved steels with guaranteed Charpy impact at service temperature plus round-cornered hatch openings. Every ship steel specification in force today traces back to this set of failures.

## Fatigue

Cyclic loading causes failure at stresses well below the static yield strength. The mechanism has three stages.

### Stage I — Initiation

Surface defects, machining marks, corrosion pits, or inclusions concentrate stress. Plastic cycling at these sites produces slip bands that evolve into microcracks. Initiation consumes most of the life of a well-finished specimen in the high-cycle regime.

### Stage II — Stable propagation

Once a crack exists, each load cycle extends it by a small amount. Paris's law describes the rate:

`da/dN = C * (delta-K)^m`

where `delta-K` is the range of the cyclic stress intensity factor, and C and m are material constants. Typical values of m are around 3 to 4 for metals. The fracture surface shows **striations** (fine parallel marks) in ductile materials — each striation corresponds to one cycle, and counting them lets the analyst reconstruct the loading history.

### Stage III — Fast fracture

When the crack is long enough that `K_I >= K_IC`, it propagates to failure in one cycle. The final fracture zone is morphologically distinct — often a shear lip, dimpled or cleaved — and marks the end of the fatigue history.

### S-N curves and endurance limits

The classical **S-N curve** plots stress amplitude versus cycles to failure. Most steels exhibit an endurance limit at around 10^6 cycles — below a certain stress amplitude, the specimen lasts indefinitely. Aluminum alloys do not have a true endurance limit; their S-N curves continue to slope downward. This is the single most important fatigue difference between steel and aluminum design.

### The Comet airliner

The 1953-54 disintegrations of the de Havilland Comet — the first jet airliner — were caused by fatigue cracking at the corners of rectangular window cutouts. Repeated pressurization cycles, stress concentration at the corners, and a plate thickness insufficient to stop a crack once it had started led to sudden explosive decompression. The redesigned Comet (and every subsequent pressurized aircraft) uses oval window shapes with large radius corners, thicker skin, crack-arrest stringers, and designed-in damage tolerance.

## Creep

At temperatures above about `0.4 * T_m` (T_m in Kelvin), metals deform continuously under constant load. The classical creep curve has three regions.

- **Primary creep** — rapidly decreasing strain rate as the material work-hardens.
- **Secondary (steady-state) creep** — constant strain rate, where climb and glide of dislocations balance hardening and recovery. `epsilon_dot = A * sigma^n * exp(-Q/RT)` with n typically 3 to 5 and Q the activation energy for self-diffusion.
- **Tertiary creep** — increasing strain rate as voids nucleate at grain boundaries, coalesce, and lead to rupture.

Creep is the dominant failure mechanism in turbine blades, boiler tubes, steam-piping of thermal power plants, and fire-exposed structural steel. Nickel superalloys with gamma-prime precipitates and single-crystal casting are the ultimate creep-resistant materials — single-crystal turbine blades have no transverse grain boundaries to cavitate.

## Environmentally Assisted Cracking

Four related mechanisms cause cracks to grow at stresses far below those that would cause mechanical failure.

### Stress-corrosion cracking (SCC)

The combination of a tensile stress and a specific aggressive environment produces intergranular or transgranular cracking. Examples: chloride SCC in austenitic stainless steels (304, 316), caustic SCC in mild steel, ammonia SCC in brass. The cracks are usually branched and grow at rates driven by the environment-assisted dissolution of metal at the crack tip.

### Hydrogen embrittlement

Atomic hydrogen diffuses into high-strength steels (above about 1200 MPa tensile strength) from sources such as cathodic protection, electroplating, or cathodic cleaning. Hydrogen collects at dislocation cores, grain boundaries, and microvoids, reducing local cohesion. Cracks initiate at the crack tip or at subsurface defects, often after hours to days under static load. The classic "delayed fracture" of plated high-strength fasteners is this mechanism.

### Corrosion fatigue

Fatigue accelerated by a corrosive environment. The endurance limit observed in air often disappears in seawater or saline. Design for marine applications must assume corrosion fatigue, not air fatigue.

### Liquid metal embrittlement

A normally ductile metal fails in a brittle manner when wetted by certain molten metals. Examples: aluminum embrittled by mercury, zinc-coated steel embrittled during welding when the zinc melts into the base metal, brass embrittled by mercury. Prevention is contamination control.

## Fractographic Clues

A trained eye can usually identify the mechanism from the fracture surface alone.

| Feature | Mechanism |
|---|---|
| Cup-and-cone fracture, fibrous appearance | Ductile overload in tension |
| Flat, faceted, reflective fracture at angles to loading | Cleavage (brittle fracture in BCC metals below DBTT) |
| Beach marks (macro) and striations (micro), flat-to-shear-lip progression | Fatigue |
| Intergranular separation with elongated grain boundaries | Creep |
| Branched cracks, intergranular path | Stress-corrosion cracking |
| Intergranular with a flat brittle zone, often at threaded features | Hydrogen embrittlement |
| Dimpled rupture | Ductile microvoid coalescence |
| Chevron marks pointing to origin | Initiation site of a rapid brittle fracture |

## The Analyst's Protocol

1. **Do not touch the fracture surface.** Photograph it. Bag it. Handling destroys evidence.
2. **Document the service history.** Loads, temperatures, environments, time in service, inspection history.
3. **Identify the mechanism** from macro and micro fractography, mechanical tests, and chemistry.
4. **Identify the cause** — the combination of material, design, and operating conditions that allowed the mechanism to dominate.
5. **Recommend a fix** that targets the cause, not the mechanism. "Replace the fractured part" is not a recommendation; "replace with a grade qualified for DBTT below service temperature" is.
6. **Close the loop** with a test or inspection regime that will catch recurrence.

## Cross-References

- **gordon agent:** Primary agent for failure analysis and the Gordon structures-and-materials perspective.
- **cottrell agent:** Owns dislocation theory, ductile-brittle transition, and metallurgical aspects of brittle fracture.
- **iron-and-steel-processes skill:** Grade and process of a failed plate often determines DBTT and toughness.
- **materials-characterization skill:** Fractography, hardness mapping, and compositional analysis on the failed part.

## References

- Griffith, A. A. (1921). "The phenomena of rupture and flow in solids." *Philosophical Transactions of the Royal Society A*, 221, 163-198.
- Gordon, J. E. (1968). *The New Science of Strong Materials*. Princeton University Press.
- Gordon, J. E. (1978). *Structures, or Why Things Don't Fall Down*. Penguin.
- Cottrell, A. H. (1958). "Theory of brittle fracture in steel and similar metals." *Transactions of the Metallurgical Society of AIME*, 212, 192-203.
- Tipper, C. F. (1962). *The Brittle Fracture Story*. Cambridge University Press.
- Paris, P. C., & Erdogan, F. (1963). "A critical analysis of crack propagation laws." *Journal of Basic Engineering*, 85, 528-534.
- ASM Handbook, Volume 11: *Failure Analysis and Prevention* (2002).
