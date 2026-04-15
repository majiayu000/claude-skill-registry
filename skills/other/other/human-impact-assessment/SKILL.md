---
name: human-impact-assessment
description: Assessing anthropogenic environmental impacts — pollution pathways, habitat destruction and fragmentation, land-use change, invasive species, overharvest, and extinction debt. Covers environmental impact assessment (EIA) methodology, exposure-effect relationships, population viability analysis, IPAT and ecological footprint frameworks, and strategic environmental assessment. Use when quantifying or forecasting human impacts on ecosystems, designing monitoring programs, or evaluating a proposed intervention against a baseline.
type: skill
category: environmental
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/environmental/human-impact-assessment/SKILL.md
superseded_by: null
---
# Human Impact Assessment

Human activity shapes the biosphere on every scale from local toxic discharge to planetary climate forcing. This skill covers the structured methods for measuring and forecasting those impacts: the pollution pathways that move chemicals from source to receptor, the geometry of habitat destruction and fragmentation, the demographics of overharvest and extinction debt, and the formal frameworks — Environmental Impact Assessment (EIA), population viability analysis (PVA), IPAT, ecological footprint — that regulators and scientists use to make impact visible. The goal is forecast, not lament.

**Agent affinity:** carson (chemical pathways, persistence), shiva (biodiversity loss, agrochemical impacts), commoner (systems view of impacts)

**Concept IDs:** envr-pollution-types, envr-habitat-destruction, envr-invasive-species, envr-climate-forcing

## The Assessment Question

Every impact assessment answers some version of four questions:

1. **What is the baseline?** What would the system look like without the proposed action?
2. **What is the stressor?** Chemical, physical, biological, or combination; magnitude, duration, frequency.
3. **What is the receptor?** Which species, populations, communities, or processes are exposed?
4. **What is the response?** Dose-response, threshold, lag, cumulative, or synergistic with other stressors?

Answer all four and you have an impact assessment. Skip any and you have an advocacy document.

## Pollution Types and Pathways

### The five classical pollution categories

| Category | Example pollutants | Primary receptors | Key metric |
|---|---|---|---|
| Air | PM2.5, ozone, NOx, SO2, VOCs, HAPs | Human lungs, vegetation, surfaces | µg/m^3, ppbv |
| Water | Nutrients, pathogens, metals, organic micropollutants | Aquatic life, drinking water users | mg/L, CFU/100 mL |
| Soil | Heavy metals, pesticides, PAHs, PFAS | Soil biota, crops, groundwater | mg/kg |
| Light | Broadband, blue-rich LED, skyglow | Nocturnal species, human sleep | Lux, mcd/m^2 |
| Noise | Traffic, aircraft, seismic, marine sonar | Fauna communication, human stress | dB, Lden |

### The source-pathway-receptor model

A chemical released at a source reaches a receptor only if a complete pathway connects the two. Break any link and the risk vanishes. This is why remediation strategies that look superficially identical (cap a landfill vs. dig it up) can have very different outcomes — they target different links in the pathway.

```
Source -> Release -> Transport -> Fate/Transformation -> Exposure -> Effect
  |         |           |              |                   |          |
  |         |           |              |                   |         cumulative +
  |         |           |              |                   |         chronic or acute
  |         |           |              |                 dose, route, duration
  |         |           |            partition (soil, water, biota),
  |         |           |            transformation, degradation
  |         |        advection, diffusion, deposition
  |       emission rate, episodic vs. continuous
concentration and form at origin
```

### Persistent organic pollutants

Carson's case against DDT rests on four properties that make an organic chemical persistent and dangerous:

1. **Stability** — does not degrade quickly in the environment (half-life in soil: years to decades)
2. **Lipophilicity** — partitions into fat tissue rather than water
3. **Bioaccumulation** — organisms concentrate it over their lifetime
4. **Biomagnification** — concentration rises at each trophic step (see `ecosystem-dynamics`)

The Stockholm Convention (2001) uses these four criteria to classify POPs. Current listings include PCBs, dioxins, several organochlorine pesticides, brominated flame retardants, and PFOS/PFOA — the latter with environmental half-lives measured in centuries.

## Habitat Destruction and Fragmentation

### Destruction vs. fragmentation

**Habitat loss** removes habitat outright. **Fragmentation** breaks continuous habitat into smaller, more isolated patches while potentially preserving total area. These have different effects and require different metrics.

### Area effects — the species-area relationship

S = cA^z, where S is species richness, A is habitat area, c is a habitat-specific constant, and z is typically 0.15-0.35 for mainland habitats and 0.20-0.40 for true islands. The implication: halving habitat area loses roughly 10-20% of species in mainland systems and 15-30% in island systems. This is the core calculation behind extinction forecasts from tropical deforestation.

### Edge effects

Fragmented habitat has more edge per unit area. Edges differ from interior in microclimate (drier, warmer, windier), predator density (edge specialists prey on interior species), and invasion by edge-associated species. For temperate forests, edge influence typically extends 50-200 m into the fragment. A 10-hectare circular patch with 100 m edge influence has no true interior habitat.

### Minimum viable populations and extinction debt

**Minimum viable population (MVP)** is the smallest population size that has a specified probability (usually 95%) of persisting for a specified time (usually 100 or 1000 years) given demographic, environmental, and genetic stochasticity. For vertebrates, effective MVPs are typically in the thousands — not dozens — because genetic drift and inbreeding compound demographic risk.

**Extinction debt** is the delayed loss of species after habitat destruction. A forest cleared today loses its large mammals within decades, its ground-nesting birds within a generation, and its old-growth-dependent invertebrates over a century. The species list at time zero overstates the population that will persist — a substantial fraction is already committed to extinction, they just have not finished dying yet. Tropical forest fragments in Brazil show clear extinction debt with characteristic half-times of 20-100 years.

## Invasive Species

Not every introduced species becomes invasive; most fail to establish. The Williamson "tens rule" (rough approximation): of 1000 introduced species, 100 establish, 10 become widespread, and 1 causes major damage. Invasiveness depends on propagule pressure, empty niche, enemy release, and hybridization potential.

### Invasion pathways

- **Intentional introduction** — agriculture, horticulture, biological control, pets
- **Stowaway** — ballast water, packing material, hull fouling
- **Corridor** — canals, roads, trade routes
- **Unassisted** — range shifts driven by climate or natural dispersal

### Impact mechanisms

Invasives cause damage through competition (zebra mussels outcompete native bivalves), predation (brown tree snakes on Guam eliminated nine native forest bird species), habitat alteration (cheatgrass changes fire regimes in the Great Basin), hybridization (mallards swamping native duck genomes), disease vectoring (chestnut blight, Dutch elm), and ecosystem engineering (European earthworms in North American deciduous forests consume the organic layer native forest floors evolved under).

Management costs: the U.S. spends roughly $120 billion per year on invasive species damage and control. The most cost-effective intervention is prevention at the border; once established, eradication is rare and expensive.

## Overharvest

Overharvest is the simplest impact to model and the hardest to govern. The maximum sustainable yield (MSY) of a population following logistic growth is rK/4, achieved at N = K/2. Harvests above MSY drive the population toward extinction; harvests at MSY are unstable to any negative environmental shock.

The tragedy of the commons (Hardin, 1968; Ostrom's corrections, 1990) explains why open-access resources tend to be overharvested: the individual captures the full benefit of harvesting but shares the cost with all other users. Solutions include private property, tradable quotas, community governance (Ostrom showed hundreds of successful examples), and regulation. Which works depends on the resource, the community, and the information environment.

### Fisheries collapse

The Atlantic cod fishery is the paradigmatic case. Catches rose through the 1950s, peaked around 1968 at 810,000 tonnes, then collapsed in the early 1990s despite intensified effort. Canada closed the fishery in 1992; 30 years later, most populations remain below recovery targets. The collapse was predicted by stock assessment science a decade before it happened and was attributed to political unwillingness to cut quotas, not scientific uncertainty.

## Climate Change as Impact Multiplier

Climate change does not usually appear as the first cause of local extinction or degradation. It acts as a multiplier on other stressors — habitat loss, invasives, disease, extreme events — by shifting the baseline conditions those stressors operate against. A species surviving in a small reserve may persist until a drought year it cannot absorb because habitat fragmentation removed the refugia it would otherwise have used.

This is why impact assessments should not evaluate stressors in isolation. Cumulative impact assessment (CIA) and strategic environmental assessment (SEA) are designed to capture interactions among stressors and across scales.

## Frameworks

### IPAT

I = P * A * T, where I is environmental impact, P is population, A is affluence (consumption per person), and T is technology (impact per unit consumption). The equation is an identity, not a theory — it cannot be wrong, but what you put into each term determines what it tells you. Most honest applications decompose observed impact changes into P, A, and T contributions over time (Kaya decomposition for CO2 is the canonical example).

### Ecological footprint

The Global Footprint Network's method converts consumption into equivalent biologically productive land area ("global hectares"). As of 2023, humanity's footprint is roughly 1.75 Earths — we consume resources at 1.75x the rate Earth regenerates them. The framework is widely criticized for opaque weighting and for treating fossil CO2 as a land-area equivalent, but it provides a single accessible number.

### Environmental Impact Assessment (EIA)

Formal EIA emerged from the U.S. National Environmental Policy Act (1970). A modern EIA contains:

1. **Screening** — does the project require assessment?
2. **Scoping** — which impacts matter enough to study?
3. **Baseline study** — what is the system now?
4. **Impact prediction** — what will change under each alternative?
5. **Mitigation** — what reduces impact?
6. **Monitoring plan** — what is measured after the project begins?
7. **Public review** — stakeholder input on all of the above.

The quality of an EIA is judged by its baseline and its monitoring plan. Projects that omit monitoring cannot learn from their own impacts.

### Population viability analysis (PVA)

PVA combines demographic data (age structure, survival, reproduction), environmental stochasticity, and genetic risk to estimate extinction probability over a specified horizon. Outputs are probability distributions, not single numbers, and the honest practitioner reports ranges and sensitivities. Used for listing decisions under the U.S. Endangered Species Act and the IUCN Red List.

## When to Use This Skill

- Structuring a formal environmental impact assessment
- Tracing a pollutant from source to receptor
- Computing extinction debt or species-area losses for a cleared area
- Evaluating an invasive species' likely pathway and impact
- Setting monitoring indicators for a project or policy
- Decomposing observed environmental change into population, consumption, and technology drivers
- Reasoning about cumulative or synergistic stressors

## When NOT to Use This Skill

- Foundational ecology without a human impact question — use `ecosystem-dynamics`
- Global element cycles without a specific human intervention — use `biogeochemical-cycles`
- Climate physics and attribution — use `climate-science`
- Solution design and evaluation — use `sustainability-design`
- Distributional framing and equity analysis — use `environmental-justice`

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Omitting the baseline | Cannot say what changed | Spend proportional effort on pre-project characterization |
| Single-stressor analysis | Stressors interact | Explicitly model at least one interaction |
| Ignoring extinction debt | Current species list is misleading | Report both current and projected species lists |
| Assuming MSY is safe | MSY is unstable to shocks | Use reference points below MSY (F_msy * 0.8, etc.) |
| Treating "carbon footprint" as sufficient | One indicator hides trade-offs | Report at least 3 impact categories |
| Monitoring after the fact | Cannot attribute change without pre-data | Establish monitoring before the stressor begins |

## Cross-References

- **carson agent:** Chemical pathway reasoning, persistence, biomagnification
- **shiva agent:** Agricultural impact assessment, biodiversity loss
- **commoner agent:** Systems view of coupled impacts
- **ecosystem-dynamics skill:** The baseline that impacts are measured against
- **biogeochemical-cycles skill:** The substrate of pollution pathways
- **sustainability-design skill:** Mitigation and remediation options

## References

- Canter, L. W. (1996). *Environmental Impact Assessment*. 2nd edition. McGraw-Hill.
- Carson, R. (1962). *Silent Spring*. Houghton Mifflin.
- Tilman, D., et al. (1994). "Habitat destruction and the extinction debt." *Nature*, 371, 65-66.
- Williamson, M. (1996). *Biological Invasions*. Chapman and Hall.
- Ostrom, E. (1990). *Governing the Commons*. Cambridge University Press.
- Hardin, G. (1968). "The Tragedy of the Commons." *Science*, 162(3859), 1243-1248.
- Ehrlich, P. R., & Holdren, J. P. (1971). "Impact of Population Growth." *Science*, 171(3977), 1212-1217.
- Stockholm Convention on Persistent Organic Pollutants. (2001, updated regularly). United Nations Environment Programme.
