---
name: prototyping-fabrication
description: CAD fundamentals, 3D printing (FDM/SLA/SLS), CNC machining, workshop skills, rapid prototyping methodology, and testing of physical prototypes. Covers fidelity levels, material selection for prototypes, dimensional tolerancing, assembly planning, and the iterate-test loop. Use when building prototypes, selecting fabrication methods, planning physical tests, or choosing between prototyping technologies.
type: skill
category: engineering
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/engineering/prototyping-fabrication/SKILL.md
superseded_by: null
---
# Prototyping and Fabrication

Prototyping is the bridge between design intent and physical reality. A prototype is a testable embodiment of a design idea -- it answers questions that analysis alone cannot. This skill covers the full range of prototyping methods from cardboard mockups to CNC-machined metal parts, with emphasis on choosing the right fidelity level, the right fabrication method, and the right test plan for each stage of the design cycle.

**Agent affinity:** lovelace-e (materials and fabrication expertise), watt (mechanical systems and testing)

**Concept IDs:** engr-rapid-prototyping, engr-testing-methodology, engr-data-from-experiments, engr-failure-analysis

## Prototyping Strategy

### Fidelity Levels

| Level | Purpose | Typical materials | Time | Cost |
|---|---|---|---|---|
| **Proof of concept** | Does the idea work at all? | Cardboard, foam, tape, Arduino | Hours | $1-50 |
| **Form study** | Does it look and feel right? | 3D-printed plastic, clay | Hours to days | $10-200 |
| **Functional prototype** | Does it perform as designed? | 3D print, laser-cut, machined parts | Days to weeks | $100-5,000 |
| **Pre-production** | Can it be manufactured? | Production materials, production-intent processes | Weeks to months | $1,000-50,000+ |

**The cardinal rule.** Build the lowest-fidelity prototype that answers the question. A cardboard mockup that proves a mechanism works in 30 minutes is worth more than a machined prototype that proves the same thing in 3 weeks. Save high-fidelity prototyping for questions that require it: material strength, precision fit, thermal behavior.

### What Question Does This Prototype Answer?

Before building anything, write down the question:

- "Will the gear train fit in the housing?" (form study)
- "Can the mechanism produce the required force?" (functional prototype)
- "Does the user understand the interface?" (proof of concept + user test)
- "Will the part survive 10,000 cycles?" (functional prototype with production materials)

A prototype without a question is a hobby project. An engineering prototype has a test plan before the first cut is made.

## CAD Fundamentals

Computer-Aided Design is the standard tool for defining geometry before fabrication.

### CAD Workflow

1. **Sketch** in 2D: Define profiles with dimensions and constraints.
2. **Feature** in 3D: Extrude, revolve, sweep, loft, or shell the sketch into solid geometry.
3. **Assembly:** Mate parts together with constraints (coincident, concentric, parallel, distance).
4. **Drawing:** Generate 2D engineering drawings from the 3D model with dimensions and tolerances.
5. **Export:** STL for 3D printing, DXF for laser cutting, G-code for CNC, STEP/IGES for interchange.

### Parametric vs. Direct Modeling

| Approach | How it works | Best for |
|---|---|---|
| Parametric | Features linked by a history tree; change a dimension and everything updates | Production parts with revision control |
| Direct | Push/pull faces without history; faster for quick exploration | Proof-of-concept and form studies |

**Common mistake.** Over-constraining sketches. A fully constrained sketch turns black/green in most CAD systems. Under-constrained sketches move unexpectedly. Over-constrained sketches refuse to update. The goal is exactly constrained.

## 3D Printing

### Fused Deposition Modeling (FDM)

| Parameter | Typical value |
|---|---|
| Layer height | 0.1 - 0.3 mm |
| Materials | PLA, ABS, PETG, Nylon, TPU |
| Accuracy | +/- 0.5 mm |
| Strength | Moderate (anisotropic -- weak between layers) |
| Cost per part | Low |
| Build volume | 200x200x200 mm (desktop) to 500+ mm (large format) |

**Best for:** Proof of concept, form studies, jigs and fixtures, low-load functional parts.

**Limitations:** Anisotropic strength (layers are the weak point), visible layer lines, limited material properties compared to machined or injection-molded parts.

### Stereolithography (SLA/DLP)

| Parameter | Typical value |
|---|---|
| Layer height | 0.025 - 0.1 mm |
| Materials | Standard resin, engineering resin, flexible resin, castable resin |
| Accuracy | +/- 0.1 mm |
| Strength | Moderate to high (isotropic) |
| Cost per part | Moderate |
| Build volume | 130x80x150 mm (desktop) to 300+ mm (large format) |

**Best for:** High-detail form studies, snap-fit prototypes, investment casting patterns, dental/medical models.

**Limitations:** Post-curing required, resin handling (gloves, ventilation), UV sensitivity of uncured parts, higher material cost than FDM.

### Selective Laser Sintering (SLS)

| Parameter | Typical value |
|---|---|
| Layer height | 0.1 mm |
| Materials | Nylon (PA12, PA11), glass-filled nylon, TPU |
| Accuracy | +/- 0.3 mm |
| Strength | High (near isotropic) |
| Cost per part | High |
| Build volume | 250x250x300 mm typical |

**Best for:** Functional prototypes requiring durability, complex geometries (no support structures needed), living hinges, production-intent parts in nylon.

**Limitations:** Grainy surface finish, limited material palette, expensive machines (service bureaus common).

### Choosing a Print Technology

| Question | FDM | SLA | SLS |
|---|---|---|---|
| Cost-sensitive? | Best | Moderate | Expensive |
| Need fine detail? | No | Yes | Moderate |
| Need strong parts? | Moderate | Moderate | Best |
| Complex internal geometry? | Needs supports | Needs supports | No supports |
| Large parts? | Yes | Limited | Moderate |

## CNC Machining

CNC (Computer Numerical Control) removes material from a solid block to create the desired shape. It produces parts from real engineering materials (aluminum, steel, titanium, engineering plastics) with tight tolerances.

### CNC Process Types

| Process | How it works | Typical tolerance |
|---|---|---|
| Milling | Rotating cutter, workpiece fixed | +/- 0.025 mm |
| Turning (lathe) | Workpiece rotates, cutter fixed | +/- 0.013 mm |
| Wire EDM | Electrical discharge cuts along a wire path | +/- 0.005 mm |

### Design for CNC

- **Avoid deep narrow pockets.** Tool length/diameter ratio should not exceed 4:1 without special tooling.
- **Use standard radii.** Inside corners require a radius equal to the cutter radius. Specify standard cutter sizes.
- **Minimize setups.** Each time the part is repositioned introduces error. Design features accessible from as few orientations as possible.
- **Specify tolerances only where needed.** Tight tolerances cost money. Default tolerance (+/- 0.1 mm) is fine for most features; tighten only at functional interfaces.

## Workshop Skills

Even in the age of digital fabrication, manual workshop skills are essential for rapid prototyping.

### Core Competencies

| Skill | Tools | When used |
|---|---|---|
| Measuring | Calipers, micrometers, height gauges | Dimensional verification of all prototypes |
| Cutting | Band saw, hacksaw, snips, utility knife | Rough shaping of stock material |
| Filing and deburring | Files, deburring tools, sandpaper | Finishing edges and removing sharp burrs |
| Drilling | Drill press, hand drill, step drill | Hole-making in any material |
| Fastening | Taps, dies, wrenches, screwdrivers | Assembly of multi-part prototypes |
| Soldering/brazing | Soldering iron, torch | Electrical connections, metal joining |
| Adhesive bonding | Epoxy, cyanoacrylate, contact cement | Joining dissimilar materials |

### Safety

Workshop safety is non-negotiable:

- **Eye protection** whenever cutting, drilling, grinding, or machining.
- **Hearing protection** with power tools above 85 dB.
- **No loose clothing, jewelry, or long hair** near rotating machinery.
- **Know the emergency stop** location on every machine before using it.
- **Never work alone** in a workshop with power tools.

## Testing Prototypes

### Test Planning

Before fabrication, write the test plan:

1. **Objective:** What question does the test answer?
2. **Setup:** How is the prototype mounted and loaded?
3. **Instrumentation:** What is measured (force, displacement, temperature, time)?
4. **Procedure:** Step-by-step test execution instructions.
5. **Success criteria:** What result constitutes pass/fail?
6. **Data recording:** How is data captured and stored?

### Common Test Types for Prototypes

| Test | What it reveals |
|---|---|
| Fit check | Do parts assemble correctly? |
| Load test | Does the structure carry the design load? |
| Cycle test | Does the mechanism survive repeated operation? |
| Drop test | Does the product survive impact? |
| Thermal test | Does performance change with temperature? |
| User test | Can the intended user operate it? |

### Failure Analysis of Prototypes

When a prototype fails -- and it should, because that is how learning happens -- analyze the failure:

1. **What failed?** Identify the failure location and mode.
2. **Why did it fail?** Root cause: design error, material deficiency, fabrication defect, or test error?
3. **What does the failure teach?** Update the design, material selection, or analysis.
4. **What is the fix?** Specific design change, with verification plan.

**The mindset.** A prototype that does not fail is either over-designed (wasted resources) or under-tested (missed knowledge). Failures in prototyping are cheap lessons that prevent failures in production.

## Cross-References

- **lovelace-e agent:** Primary agent for materials, fabrication methods, and manufacturing process selection.
- **watt agent:** Mechanical prototype testing, thermal testing, and mechanism analysis.
- **brunel agent:** Prototyping within the broader design cycle, prototype planning at design reviews.
- **design-process skill:** Prototyping is Phase 6 of the design cycle.
- **structural-analysis skill:** Predicting prototype structural behavior before testing.
- **technical-communication skill:** Documenting prototype test results and failure analyses.

## References

- Ulrich, K. T., & Eppinger, S. D. (2020). *Product Design and Development*. 7th edition. McGraw-Hill.
- Thompson, R. (2007). *Manufacturing Processes for Design Professionals*. Thames & Hudson.
- Chua, C. K., Leong, K. F., & Lim, C. S. (2010). *Rapid Prototyping: Principles and Applications*. 3rd edition. World Scientific.
- Redwood, B., Schoffer, F., & Garret, B. (2017). *The 3D Printing Handbook*. 3D Hubs.
- Oberg, E., et al. (2020). *Machinery's Handbook*. 31st edition. Industrial Press.
