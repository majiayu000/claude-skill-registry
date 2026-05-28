---
name: ecosystem-dynamics
description: Ecological organization, energy flow, food webs, biodiversity, succession, and species interactions. Covers trophic structure, primary productivity, nutrient transfer efficiency, keystone and foundation species, ecosystem services, carrying capacity, disturbance regimes, primary and secondary succession, and resilience metrics. Use when analyzing how living communities are organized, how energy and matter move through ecosystems, how disturbance and recovery shape landscapes, or why biodiversity matters for ecosystem function.
type: skill
category: environmental
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/environmental/ecosystem-dynamics/SKILL.md
superseded_by: null
---
# Ecosystem Dynamics

An ecosystem is the functional unit of ecology — a community of organisms together with the physical environment they share, bounded loosely by patterns of energy flow and nutrient cycling. This skill covers the organizing principles of ecosystem structure and dynamics: how energy enters through primary production, how it dissipates through trophic levels, how communities assemble and recover from disturbance, and why species richness functions as insurance against change. The focus is on mechanisms and measurable quantities, not ideology.

**Agent affinity:** leopold (land ethic, ecological integrity), muir (wilderness, undisturbed systems), commoner (laws of ecology)

**Concept IDs:** envr-ecosystem-organization, envr-food-webs, envr-biodiversity-resilience, envr-succession

## The Levels of Ecological Organization

Ecology operates at nested scales. Claims at one scale rarely transfer directly to another, and confusing scales is the most common reasoning error in environmental argumentation.

| Level | Unit | Example question |
|---|---|---|
| Individual | One organism | What is this salmon's metabolic rate? |
| Population | Conspecific individuals in a place | How many pikas live on this talus slope? |
| Community | Interacting populations | What species occupy this tide pool? |
| Ecosystem | Community plus abiotic environment | How much carbon does this bog sequester per year? |
| Landscape | Mosaic of ecosystems | How does fragmentation affect this watershed? |
| Biome | Climatically similar regions | How productive is temperate rainforest globally? |
| Biosphere | All living systems | What is Earth's net primary production? |

When someone says "the ecosystem is collapsing," ask: which level, which unit, what is actually being measured? Vague claims rarely survive the question.

## Energy Flow and Trophic Structure

### Primary production

Primary producers (autotrophs) convert solar or chemical energy into organic compounds. **Gross primary production** (GPP) is the total carbon fixed per unit area per unit time. **Net primary production** (NPP) is GPP minus the producer's own respiration, and it is the energy available to the rest of the food web. Global NPP is roughly 104 petagrams of carbon per year, split near-evenly between marine and terrestrial systems despite the two covering very different areas.

Productivity varies by three orders of magnitude across biomes. Tropical rainforest and estuarine marsh cluster near 2000 g C / m^2 / yr; boreal forest sits near 500; open ocean and desert fall below 100. These numbers anchor almost every downstream calculation — carbon budgets, carrying capacity, harvest sustainability.

### The 10% rule and trophic efficiency

Energy transfer between trophic levels averages about 10% efficient, meaning roughly 90% is lost as heat, respiration, and unconsumed biomass at each step. This has profound consequences:

- Food webs rarely exceed 4 or 5 levels because the energy base vanishes.
- Top predators are vastly outnumbered by their prey.
- A diet shift from beef to grain feeds roughly ten times as many people from the same land.
- Biomagnification of persistent pollutants (DDT, mercury, PCBs) occurs because toxins accumulate at each step while energy dissipates.

Actual efficiencies range from 2% to 25% depending on ectothermy, digestibility, and behavior. The 10% figure is a working average, not a law.

### Worked example — Silent Spring's apex

Rachel Carson's *Silent Spring* (1962) documented DDT biomagnification: water concentrations near 0.00005 ppm yielded plankton at 0.04 ppm, minnows at 0.5 ppm, large fish at 2 ppm, and fish-eating birds (osprey, brown pelican, bald eagle) at 25 ppm or higher. The result was eggshell thinning and reproductive failure. DDT was not acutely toxic at water concentrations — the mechanism required understanding that toxins ride up the food chain while energy flows out of it. Carson's argument was a trophic-structure argument first.

## Food Webs

A food web is a directed graph of feeding relationships. Nodes are species (or functional groups); edges are "eats." Unlike the simple linear food chain of textbook diagrams, real webs are dense, reticulated, and contain both strong and weak interactions.

### Key concepts

- **Producers / consumers / decomposers.** The fundamental roles. Decomposers return nutrients to the soil pool; without them, nutrient cycling would halt within a few decades.
- **Trophic levels.** Functional positions in the energy chain, usually numbered from primary producers (level 1) up to apex predators.
- **Keystone species.** Species whose removal triggers disproportionate community change relative to their biomass. Paine's classic 1966 experiment on Pacific Northwest tide pools removed the sea star *Pisaster ochraceus* and watched mussel monocultures collapse the entire community.
- **Foundation species.** Species that physically structure habitat. Redwoods, kelp, reef-building corals, beavers. Unlike keystones, their effect scales with their biomass.
- **Ecological niche.** The n-dimensional resource space a species occupies. The fundamental niche is the set of conditions a species can tolerate; the realized niche is the subset it actually occupies given competition and predation.

### Interaction types

| Interaction | Species A | Species B | Example |
|---|---|---|---|
| Mutualism | + | + | Pollinator and flower |
| Commensalism | + | 0 | Cattle egret and grazing cow |
| Parasitism | + | - | Tapeworm in host |
| Predation | + | - | Wolf on elk |
| Competition | - | - | Two warblers for the same insect |
| Amensalism | 0 | - | Walnut juglone on understory plants |
| Neutralism | 0 | 0 | Rare; usually an artifact of aggregation |

## Biodiversity and Resilience

### Measuring diversity

**Species richness** counts how many species are present. **Species evenness** measures how uniformly abundance is distributed among them. Richness without evenness is misleading — a forest with 40 tree species but one of them 95% of the stems is less diverse than a forest with 10 evenly-distributed species. The Shannon index H = -sum(p_i ln p_i) combines both, and Simpson's D = sum(p_i^2) weights dominance.

### Why diversity matters functionally

1. **Insurance.** Diverse communities have more species capable of performing the same function, so disturbance loses one and another compensates.
2. **Complementarity.** Species use resources in slightly different ways, so total resource use is higher in diverse systems.
3. **Facilitation.** Some species improve conditions for others (nitrogen fixers, shade providers, mycorrhizal partners).
4. **Stability over time.** The portfolio effect — aggregated variation is lower than component variation, just as in finance.

Vandana Shiva's work on agricultural biodiversity rests on these points. Monocultures maximize yield in good years but collapse in bad ones. Traditional polycultures accept lower peak yield in exchange for variance reduction and resilience. Whether that trade favors the farmer depends on how much variance the farmer can absorb.

### The biodiversity-function relationship

Empirical experiments (Tilman, Loreau, Hector, and others) find a saturating curve: adding species increases productivity and stability at low richness, with diminishing returns at high richness. The curve's shape depends on the function measured and the species pool involved. No single number captures it.

## Succession

Succession is the directional, more-or-less predictable sequence of community change following disturbance. It is not a teleological march toward a climax — that framing by Clements in 1916 has been largely abandoned — but a probabilistic trajectory shaped by colonization, facilitation, competition, and chance.

### Primary vs. secondary

**Primary succession** starts from bare substrate with no soil or legacy biota: a new volcanic island, a glacial moraine, a fresh landslide. Pioneer species (lichens, mosses, nitrogen-fixing pioneers) build soil over decades to centuries before woody vegetation can establish.

**Secondary succession** starts from a disturbed but not sterile site: an abandoned field, a clear-cut, a burned forest. Legacy soil, seed banks, and resprouting individuals mean recovery proceeds in years to decades rather than centuries.

### Mechanisms (Connell and Slatyer, 1977)

1. **Facilitation.** Early species alter conditions in ways that allow later species to invade.
2. **Tolerance.** Early species neither help nor hinder later species; later species are simply better competitors at equilibrium conditions.
3. **Inhibition.** Early species resist replacement until disturbance or senescence opens the door.

Real successional sequences usually mix all three. Whether a burned site returns to pre-disturbance community depends on intensity, scale, seed sources, climate during recovery, and pure luck.

### Worked example — Mount St. Helens (1980-)

The 1980 eruption created every category of disturbance in one event: pyroclastic flow zones (primary succession starting from scratch), lahars (mixed), blown-down forest (secondary from legacy root systems), and ashfall (near-intact soil). Four decades later, pyroclastic zones are still early-successional meadows; blowdown zones are 20-meter-tall closed canopy. Scale and starting conditions dominate the trajectory.

## Ecosystem Services

"Ecosystem services" is the accounting language ecologists adopted to make ecological value legible to economics. The Millennium Ecosystem Assessment (2005) categorizes four classes:

1. **Provisioning** — food, timber, fiber, fresh water, pharmaceuticals.
2. **Regulating** — climate regulation, flood control, pollination, water purification, pest regulation.
3. **Cultural** — recreation, aesthetic, spiritual, scientific, educational.
4. **Supporting** — primary production, soil formation, nutrient cycling. These underlie the other three.

The framework is useful but imperfect. Monetizing cultural services is contested, supporting services are double-counted if added to the others, and marginal pricing fails for life-support functions that have no substitute at any price.

## Carrying Capacity

K, the carrying capacity, is the population size a habitat can sustain given its resources. Logistic growth dN/dt = rN(1 - N/K) is the textbook model. In practice, K is not a constant — it varies with climate, disturbance, and resource pulses. Over-simplified K-based reasoning ("we've exceeded carrying capacity") usually hides assumptions about technology, consumption, and substitutability.

For a wolf pack in Yellowstone, K is constrained by elk density, which in turn depends on winter severity and riparian vegetation. For humans, K depends on diet, energy source, agricultural productivity, and institutional capacity. The same 2.5 acres supports one person on an industrial meat diet, five on an industrial grain diet, or ten on a traditional plant diet — and that ignores freshwater, minerals, and sinks.

## When to Use This Skill

- Analyzing a food web, trophic cascade, or energy budget
- Explaining why keystone species matter disproportionately to their biomass
- Estimating productivity, biomass, or population carrying capacity
- Diagnosing succession stage and predicting trajectory after disturbance
- Evaluating biodiversity metrics (richness, evenness, Shannon, Simpson)
- Framing ecosystem services for policy or accounting
- Reasoning about biomagnification of persistent pollutants

## When NOT to Use This Skill

- Pure climate or atmospheric-physics questions — use `climate-science`
- Biogeochemistry questions about carbon, nitrogen, or water cycles — use `biogeochemical-cycles`
- Human impact assessments focused on pollution pathways or land-use change — use `human-impact-assessment`
- Sustainability design at the intervention or policy level — use `sustainability-design`
- Environmental justice framings of disproportionate burden — use `environmental-justice`

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Confusing trophic levels with food chains | Real webs are reticulated, not linear | Draw the full web; count shared prey and shared predators |
| Citing a single biodiversity number | Richness and evenness mean different things | Report at least richness + one dominance index |
| Assuming climax equilibrium | Disturbance is the norm, not the exception | Ask which disturbance regime the system evolved under |
| Treating K as constant | K varies with resources, climate, and management | State the conditions under which K was measured |
| Applying temperate-forest intuition to the tropics | Nutrient cycling and succession differ | Check the system's biogeography before transferring concepts |
| "Ecosystem services" as final word | Many services have no substitute | Distinguish marginal from absolute value |

## Cross-References

- **leopold agent:** Land ethic, ecological integrity, community-level reasoning
- **muir agent:** Wilderness character, undisturbed reference systems
- **commoner agent:** Four laws of ecology, systems thinking, nothing disappears
- **biogeochemical-cycles skill:** The chemical substrate that energy flow runs on
- **climate-science skill:** Climate as the driver of biome distribution and productivity
- **human-impact-assessment skill:** Disturbance as anthropogenic perturbation

## References

- Odum, E. P., & Barrett, G. W. (2005). *Fundamentals of Ecology*. 5th edition. Thomson Brooks/Cole.
- Ricklefs, R. E., & Relyea, R. (2018). *Ecology: The Economy of Nature*. 8th edition. Freeman.
- Paine, R. T. (1966). "Food web complexity and species diversity." *American Naturalist*, 100(910), 65-75.
- Connell, J. H., & Slatyer, R. O. (1977). "Mechanisms of succession in natural communities." *American Naturalist*, 111(982), 1119-1144.
- Tilman, D., Reich, P. B., & Knops, J. M. H. (2006). "Biodiversity and ecosystem stability in a decade-long grassland experiment." *Nature*, 441, 629-632.
- Millennium Ecosystem Assessment. (2005). *Ecosystems and Human Well-being: Synthesis*. Island Press.
- Carson, R. (1962). *Silent Spring*. Houghton Mifflin.
- Leopold, A. (1949). *A Sand County Almanac*. Oxford University Press.
