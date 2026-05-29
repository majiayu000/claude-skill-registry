---
name: materials-and-fit
description: Materials and fit for the trades — how wood, metal, stone, fabric, and composite materials behave, how they move with humidity and temperature, and how "fit" between parts is achieved in the presence of material behavior. Covers moisture content, thermal expansion, grain and fiber direction, elastic and plastic deformation, corrosion and finish interaction, and the traditional allowances that experienced tradespeople build into their work. Use when specifying materials, diagnosing a failed fit, or teaching a learner why traditional allowances exist.
type: skill
category: trades
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/trades/materials-and-fit/SKILL.md
superseded_by: null
---
# Materials and Fit

Materials are alive. Wood moves with humidity, metal moves with temperature, stone settles under load, fabric stretches and relaxes, and modern composites have behaviors that surprise people who expect them to behave like traditional materials. "Fit" between parts — whether a drawer slides smoothly for a century or binds after the first humid summer — depends on understanding this movement and designing for it rather than against it. This skill covers the core physical behaviors that every trade has to respect.

**Agent affinity:** vitruvius (Roman material discipline), nasmyth (metallurgy and machine tolerances), brunel-tr (material selection in shipwork)

**Concept IDs:** trades-material-movement, trades-fit-allowance, trades-material-failure

## Why Materials Move

Almost every material used in the trades changes dimension in response to its environment. The two dominant mechanisms are thermal expansion and moisture exchange.

**Thermal expansion** is the dimensional change of a material with temperature. Metals expand and contract by coefficients on the order of tens of parts per million per degree Celsius — small per degree, large across a day or a season. A thirty-foot steel beam changes length by about a quarter-inch between a winter night and a summer afternoon. Wood and stone expand thermally too, but less. Plastics expand much more.

**Moisture exchange** is the dimensional change of a material with the moisture content of its surroundings. Wood is the champion here: a piece of wood can change width by several percent between a dry winter shop and a humid summer one. Leather, paper, cloth, and concrete all move with humidity to varying degrees. Metals mostly do not, but ferrous metals rust in wet air, which is a different kind of movement — dimensional growth by corrosion product.

A tradesperson who ignores these movements produces work that looks correct at the moment of assembly and fails afterward, often months later when the first seasonal cycle completes. A tradesperson who designs for these movements produces work that is loose at assembly time (by a deliberate margin) and tight after equilibration.

## Wood — The Moisture-Dominant Material

Wood shrinks and swells far more than almost any other material in response to humidity. The magnitude depends on the grain direction:

- **Longitudinally** (along the grain): almost no movement. Shrinkage is often below 0.1% from green to bone-dry. For most purposes it can be ignored.
- **Radially** (perpendicular to the growth rings, toward the center of the tree): about 4–8% from green to bone-dry.
- **Tangentially** (perpendicular to the grain, along the growth rings): about 8–14% from green to bone-dry.

The ratio of tangential to radial movement is the reason for wood's tendency to cup, twist, and check. A flat-sawn board (tangential) moves roughly twice as much as a quarter-sawn board (radial) of the same species. Historically, quarter-sawn lumber was preferred for stable work — drawer sides, wide panels, joinery surfaces — for this reason. Quarter-sawn lumber is more expensive to produce and is wasteful of the log, which is why much modern work is done in flat-sawn lumber with allowances built in for the greater movement.

### The "frame and panel" solution

Traditional furniture is full of frame-and-panel construction, and the reason is material movement. A flat wide panel of wood will change width by a significant fraction of an inch across a season. If that panel is rigidly attached at both edges, something has to give — the panel cracks, or the attachment fails, or the surrounding structure warps. Frame-and-panel lets the panel float inside a frame. The frame is sized for the extreme wide case; the panel is free to slide in its grooves as it moves. The construction is five hundred years old and is still the right answer whenever a wide wood panel has to be used. Modern furniture that uses wide panels rigidly attached is furniture that fails.

### Equilibrium moisture content

Wood reaches an equilibrium with the air around it. In a heated indoor space in a cold dry climate, the equilibrium is around 6–8%. In a humid summer, it may be 10–14% or higher. Wood that is installed at the wrong moisture content will move toward equilibrium over weeks to months. Traditional practice is to acclimate wood in its destination space before using it — leaving planks stacked in the room for two to four weeks before the work begins. Modern practice is to use a moisture meter and verify.

## Metals — The Thermal-Dominant Materials

Metals move with temperature. The coefficients are small but the effect is large because the distances involved are often large and the forces involved are often very large.

### Thermal expansion coefficients (approximate, per degree C)

- Aluminum: 23 × 10⁻⁶
- Copper: 17 × 10⁻⁶
- Steel (mild): 12 × 10⁻⁶
- Stainless steel: 17 × 10⁻⁶
- Cast iron: 11 × 10⁻⁶
- Titanium: 8 × 10⁻⁶
- Invar (iron-nickel alloy): 1.2 × 10⁻⁶ (engineered for minimal thermal movement)

A machinist cutting a steel part at 18°C and measuring it against a steel gauge at 22°C is measuring a part that has grown relative to the gauge. For precision work (tenths of a thousandth), temperature control is mandatory. For normal shop work (thousandths), it can be ignored most of the time but becomes relevant at the extremes.

### Dissimilar metal fits

When two different metals are fit together, the fit changes with temperature because the coefficients differ. A bronze bushing in an aluminum housing will be tight at room temperature and loose at high temperature because aluminum grows faster. An aluminum piston in an iron cylinder (as in many engines) requires a designed-in clearance that accounts for the expected operating temperature. Get this wrong and the engine seizes.

### Welding distortion

Welding applies intense local heat. The metal expands under the torch, the surrounding metal constrains it, and when cooling the weld contracts — but the surrounding metal has shifted. The result is a distortion that can be significant. Experienced welders sequence their welds to distribute the distortion, clamp to restrain it, or pre-deform the work so that the finished piece springs back to correct shape.

## Stone — The Settlement-Dominant Material

Stone is dimensionally stable compared to wood and metal, but it has two behaviors that matter for trades: settlement under load, and differential behavior across the course of a building.

**Settlement** is the slow, cumulative deformation of stonework under its own weight. A stone wall that is plumb at construction time can be slightly out of plumb a decade later because the mortar joints compress and the stone courses redistribute. Traditional practice compensates for this by over-building in the direction of expected settlement.

**Differential weathering** is the different rate at which different parts of a stone structure weather. Exposed south-facing walls weather differently from sheltered north-facing walls. Softer stones weather faster than harder ones. A wall built of mixed stones will, over centuries, develop a texture that reveals the weathering differential.

Masonry is the slowest of the trades in a sense — the work is not finished when the wall is up; it is finished over the decades during which the structure settles into its final relationship with its site.

## Fabric and Fiber — The Elastic Materials

Textile trades work with materials whose dimensional behavior is dominated by elasticity. A piece of woven cloth stretches under tension, relaxes when released, and has different behavior along the warp, weft, and bias. A skilled tailor cuts on the bias when the intended drape requires stretch, cuts on the warp when dimensional stability is required, and compensates for the difference between dry and washed dimensions (the "takeup" of the first washing, which can be several percent).

Modern synthetic fibers behave differently: less takeup, more dimensional stability, but also different thermal and chemical responses. A polyester thread in a cotton fabric shrinks less than the fabric and can cause puckering after the first wash. This is craft knowledge that has to be learned material by material.

## Fit Allowances

A "fit allowance" is a deliberate amount by which a part is made different from its nominal dimension in order to account for known material behavior. The allowance is not slop; it is engineering.

### Typical allowances by trade

- **Woodworking:** tenons sized a hair under the mortise to allow for seasonal swelling; panel grooves deeper than the panel extends to allow for panel expansion; drawers fit slightly loose in winter so they do not bind in summer.
- **Machining:** press fits designed with interference; slip fits designed with clearance; running fits with specific clearance for lubrication and thermal growth. ISO and ANSI standards codify these allowances in H/h, K/k, etc. notation.
- **Masonry:** expansion joints at regular intervals; control joints to direct where cracks will occur (because cracks will occur); weep holes for moisture movement.
- **Concrete:** control joints at spacing determined by the mix and the conditions; rebar placement that allows for thermal movement; curing compounds that slow moisture loss.
- **Welding:** joint gap allowance for weld shrinkage; root gap for full penetration; pre-deformation to spring back to correct shape.

Each allowance is a piece of craft knowledge that takes time to learn. Learners under time pressure skip allowances because they "look wasteful" — and then the work fails in the first seasonal cycle.

## Fit Verification

A fit cannot be judged by measurement alone. Two parts that measure correctly can still fit badly if the tolerances accumulate in the wrong direction, if the reference surfaces are not the ones assumed, or if the material has moved since measurement. Skilled tradespeople verify fits empirically:

- **Trial fit without adhesive or fastener.** The parts are brought into their intended relationship and observed.
- **Dry assembly of subsystems.** Before committing to final assembly, the subsystem is assembled and disassembled to catch problems.
- **Witness marks.** Small marks at reference points that show whether the parts are returning to the same relative position each time.
- **Feeler gauges and scribing.** For precise fits, the actual gap or interference is measured rather than calculated from part dimensions.

The verification habit is one of the clearest markers of experience. Learners measure. Journeymen assemble. Masters verify.

## Failure Modes by Material

- **Wood:** cracks from restrained movement, rot from undrained water, fastener loosening from cyclic humidity.
- **Metal:** fatigue from cyclic load, corrosion in wet or chemically active environments, galvanic corrosion between dissimilar metals, seizure from thermal mismatch.
- **Stone:** spalling from water freeze-thaw, staining from salt or biological growth, settling from inadequate foundation.
- **Concrete:** cracking (always, everywhere, the question is only where and how much), spalling from rebar corrosion, surface wear in high-traffic areas.
- **Fabric:** wear from abrasion, ultraviolet degradation, mildew in damp storage, shrinkage from hot washing.
- **Composite:** delamination at interfaces, creep under sustained load, chemical attack from solvents that did not exist when the material was developed.

Understanding a material means knowing how it fails as much as knowing how it succeeds. The craft tradition of a given material is in large part a catalog of failures that previous practitioners encountered and learned to avoid.

## References

- Bruce Hoadley, *Understanding Wood* (2000) — definitive reference on wood behavior
- John E. Traister, *Handbook of Construction Materials* (1990) — cross-material reference
- David Pye, *The Nature and Art of Workmanship* (1968) — allowances and the workmanship of risk
- Vitruvius, *De Architectura*, Books II and VII — Roman material selection and finishing
