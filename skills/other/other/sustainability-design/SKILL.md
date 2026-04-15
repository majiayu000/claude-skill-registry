---
name: sustainability-design
description: Designing interventions, systems, and policies for sustainability. Covers renewable energy (solar, wind, hydro, geothermal), sustainable agriculture (agroecology, permaculture, integrated pest management), conservation strategies (protected areas, corridors, rewilding), lifecycle analysis, circular economy principles, and policy instruments (carbon pricing, cap-and-trade, regulation). Use when evaluating or designing interventions that aim to reduce environmental impact while maintaining human well-being.
type: skill
category: environmental
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/environmental/sustainability-design/SKILL.md
superseded_by: null
---
# Sustainability Design

Sustainability is not a property of things; it is a property of trajectories. A system is sustainable to the extent that its current operating mode can be continued without degrading the stocks — energy, materials, soil, biota, atmosphere, institutions — that the operation depends on. This skill covers the design tools for evaluating and improving that trajectory: renewable energy assessment, sustainable agriculture, conservation strategy, lifecycle analysis, circular economy principles, and policy instruments. The focus is quantitative and comparative; there is no single "sustainable" option, only options compared against alternatives on specified axes.

**Agent affinity:** wangari (reforestation, community-scale intervention), shiva (agroecology, seed sovereignty), orr (ecological literacy, education design)

**Concept IDs:** envr-renewable-energy, envr-conservation-strategies, envr-sustainable-agriculture, envr-lifecycle-analysis

## The Brundtland Definition and Its Problems

The standard definition (Brundtland, 1987): "Development that meets the needs of the present without compromising the ability of future generations to meet their own needs." It is useful as a motto but nearly useless for design, because "needs" is undefined, time horizons are unspecified, and trade-offs among needs at a single time are ignored.

Working definitions used in practice:

- **Strong sustainability** — natural capital cannot be substituted for manufactured capital. Some ecosystem services have no replacement at any cost (a stable climate, an ozone layer, pollinators).
- **Weak sustainability** — total capital stocks (natural + manufactured + human + social) must be non-declining. Substitution within the total is permitted.
- **Operational sustainability** — specific indicators (emissions, water use, biodiversity metrics) must move in a target direction on a specified timeline.

Most concrete design work uses operational definitions. Strong and weak sustainability remain philosophically divided, and the philosophical divide maps to policy disagreement about how much substitution is actually possible.

## Renewable Energy Design

### The core metrics

- **Capacity factor** — average output over a year divided by rated peak capacity. Solar PV: 15-25%. Onshore wind: 30-45%. Offshore wind: 40-55%. Hydroelectric: 30-50%. Geothermal: 70-90%. Nuclear: 85-95%. Natural gas combined cycle: 50-60% (dispatched).
- **Levelized cost of energy (LCOE)** — lifetime cost per unit energy produced. Utility-scale solar PV LCOE fell ~90% from 2010 to 2023. Onshore wind fell ~70%. These are now the cheapest new-build electricity sources in most markets.
- **Energy return on energy invested (EROI)** — energy delivered over the life of the project divided by energy used to build, operate, and decommission it. Modern wind and utility solar: EROI 10-30. Fossil fuels (at wellhead): 10-30, declining. Ethanol: often below 2, sometimes below 1.
- **Intermittency** — capacity factor captures average output, not when it occurs. Solar generates on diurnal and seasonal cycles; wind is correlated with weather systems. This creates a storage, transmission, or flexibility problem, not a resource problem.

### The intermittency problem

At low penetration (below ~20% of grid), intermittent renewables behave like fuel savers — they displace fossil generation when they run and the rest of the grid compensates. At high penetration (above ~50%), they require one of:

1. **Storage** — batteries (hours), pumped hydro (days), hydrogen or synthetic fuels (seasonal).
2. **Long-distance transmission** — spatial averaging smooths wind and solar.
3. **Flexible firm capacity** — dispatchable sources (gas, nuclear, geothermal, hydro) that fill gaps.
4. **Demand response** — shifting loads to match supply.
5. **Overbuild and curtail** — build 2-3x the average demand and accept discarded energy.

The cheapest portfolio usually combines all five. Pure-renewable scenarios that ignore intermittency produce misleading cost estimates.

### Hydropower and the siting constraint

Hydropower is the oldest and cheapest large-scale renewable, but new dam sites in developed countries are nearly exhausted, and large dams fragment rivers, displace communities, and emit methane from flooded biomass. The International Energy Agency estimates that economically and environmentally feasible new hydro globally is a small fraction of total demand growth.

## Sustainable Agriculture

### The productivity-sustainability trade-off, qualified

The Green Revolution (Borlaug, Swaminathan, and others, 1950s-1970s) raised cereal yields in Asia and Latin America dramatically by combining high-yield varieties, synthetic fertilizer, irrigation, and pesticides. It fed billions who would otherwise have starved. It also depleted groundwater, degraded soils, concentrated land ownership, displaced traditional varieties, and created chronic exposure to organophosphate and organochlorine pesticides.

Vandana Shiva's critique is not that the Green Revolution failed but that its success was narrowly defined. Yield per acre of a single crop rose; yield per acre of total food and fodder from a traditional polyculture did not always fall, and often rose in farmer welfare terms. The measurement question is which yield and whose welfare.

### Alternative systems

- **Agroecology** — applies ecological principles to agricultural design. Polycultures, nitrogen-fixing rotations, habitat for natural enemies of pests.
- **Organic farming** — prohibits synthetic pesticides and fertilizers; certification standards vary by jurisdiction. Typical yields are 80-95% of conventional for most crops, with lower nitrogen leaching and higher soil carbon.
- **No-till and conservation tillage** — reduce soil disturbance to preserve structure, moisture, and organic matter.
- **Integrated pest management (IPM)** — uses monitoring and economic thresholds to time interventions, combining biological, cultural, and chemical controls. Can reduce pesticide use 50-90% while maintaining yield.
- **Permaculture** — design philosophy (Mollison and Holmgren, 1978 onward) emphasizing perennial polycultures, closed nutrient loops, and observation-led intervention.
- **Regenerative agriculture** — loosely defined bundle emphasizing soil health, cover cropping, diverse rotations, and livestock integration. Evidence base is growing but heterogeneous.

### Food system framing

Yield per acre is one metric; food system sustainability requires tracking waste (~30% of food produced globally is wasted), diet composition (livestock consume far more calories than they produce as food), transport (minor compared to production impacts for most foods, major for a few), packaging, and access. Wasted food is never sustainable food.

## Conservation Strategy

### Protected areas

The international target (Aichi 11, updated in the Kunming-Montreal Global Biodiversity Framework, 2022) is to protect 30% of land and 30% of ocean by 2030. As of 2024, protected area coverage is ~17% terrestrial and ~8% marine. The distinction between protected on paper and effectively managed is large — "paper parks" are common in underfunded systems.

Protected area design principles:

- **Representation** — every ecosystem type should be represented in the protected network.
- **Size** — large reserves retain more species and support larger viable populations.
- **Connectivity** — corridors and stepping stones allow movement among reserves.
- **Redundancy** — multiple populations of each target reduce stochastic extinction risk.
- **Management effectiveness** — budget, enforcement, and community engagement determine whether the paper status produces biological outcomes.

### Corridors and connectivity

Habitat corridors link isolated patches. Evidence from long-term experiments (Tewksbury et al., 2002 and follow-ups) shows corridors increase pollination, seed dispersal, and plant colonization. The magnitude varies by taxon and landscape resistance.

### Rewilding

Rewilding restores ecological processes, often by reintroducing keystone species that perform missing ecological functions. The Yellowstone wolf reintroduction (1995) remains the most-cited example; the trophic cascade literature from it is contested in detail but broadly holds. Rewilding is attractive because it targets process rather than species composition — letting the system find its own composition given process inputs.

### Keystone and umbrella species

Conservation focused on a keystone species (Yellowstone wolf, sea otter) targets a species whose presence shapes the community. Focus on an umbrella species (tiger, grizzly bear) targets a species whose large range incidentally protects many others. Both are strategies for leveraging limited funding.

## Lifecycle Analysis (LCA)

LCA is the structured accounting of environmental inputs and outputs over a product's life — raw material extraction, manufacturing, distribution, use, and end of life. ISO 14040/14044 specify the methodology. Steps:

1. **Goal and scope** — what product, what boundaries, what functional unit?
2. **Inventory analysis** — quantify inputs and outputs at every stage.
3. **Impact assessment** — convert inventory into impact categories (greenhouse gas, acidification, eutrophication, toxicity, water use, land use).
4. **Interpretation** — what are the results sensitive to? What can the designer change?

LCA outputs usually surprise. A cotton tote bag must be used ~130 times to match a single-use plastic bag on climate impact, because cotton agriculture is water- and chemical-intensive. A paper cup is not obviously better than a plastic cup on any single metric. Electric vehicles are better than internal combustion on greenhouse gas emissions under most grids but worse on battery-material impacts, and the ratio depends heavily on grid mix.

LCA is a tool for avoiding intuition errors, not a source of simple answers. Its main failure mode is boundary-drawing: where you draw the system boundary determines the result.

## Circular Economy

The circular economy reframes waste as a design failure. Instead of linear take-make-use-dispose flows, materials loop through reuse, remanufacturing, recycling, and composting. The target is to decouple economic activity from virgin resource consumption.

Principles (Ellen MacArthur Foundation and others):

1. **Design out waste and pollution** — designers choose materials and assemblies for end-of-life as well as use.
2. **Keep products and materials in use** — extend product life; reuse before recycle.
3. **Regenerate natural systems** — return organic nutrients; restore degraded ecosystems.

Circularity is difficult in practice. Most materials degrade with each cycle (paper fibers shorten; plastic polymers oxidize). Some materials (phosphorus, rare earths) are diluted through use and cannot be recovered economically. Energy is required to close loops, and if that energy is fossil-derived, circularity can increase greenhouse emissions.

## Policy Instruments

- **Command and control** — specify technology or emission limits by regulation. Historically effective for point-source pollution (Clean Air Act, NOx limits). Rigid and expensive when pollution is diffuse.
- **Carbon pricing** — taxes or cap-and-trade that put a price on emissions. Theoretical gold standard for externality correction; politically difficult. EU ETS, British Columbia carbon tax, and RGGI are the most-studied working examples.
- **Subsidies and tax credits** — pay for desired outcomes. U.S. Inflation Reduction Act (2022) is the largest climate subsidy program to date.
- **Standards** — fuel economy, building efficiency, appliance efficiency. Simple to enforce, politically durable, economically less efficient than prices but often more popular.
- **Information disclosure** — require labeling (energy labels, toxic release inventory). Weak as the sole instrument but complements others.
- **Procurement** — governments buying green goods create markets.

No single instrument works for all problems. Real policy bundles combine several, targeting different segments of the pollutant's pathway.

## When to Use This Skill

- Designing a renewable energy project or portfolio
- Evaluating an agricultural intervention against baselines
- Structuring a conservation strategy for a landscape
- Running or critiquing a lifecycle analysis
- Designing a circular-economy product or process
- Evaluating climate, biodiversity, or environmental policy options
- Comparing sustainability claims across alternatives

## When NOT to Use This Skill

- Characterizing ecosystems or biodiversity without an intervention — use `ecosystem-dynamics`
- Biogeochemistry at the pool-and-flux level — use `biogeochemical-cycles`
- Climate physics and attribution — use `climate-science`
- Baseline impact assessment without intervention options — use `human-impact-assessment`
- Distributional analysis and equity — use `environmental-justice`

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Sustainable without context | "Sustainable" is a comparison, not a category | Compare to at least one alternative and a baseline |
| Ignoring intermittency in renewable scenarios | Storage, transmission, or firm capacity matter | Include at least one balance mechanism |
| Single-metric comparisons | Reductive and misleading | Report at least 3 impact categories |
| LCA with unstated boundaries | Boundary choice drives the result | State the functional unit and system boundary clearly |
| "Organic is always better" | Trade-offs by crop, region, and metric | Report yield, water, chemical, and soil outcomes together |
| Circular claims without energy accounting | Closing loops costs energy | Include energy balance with circularity claim |

## Cross-References

- **wangari agent:** Community-scale reforestation and intervention
- **shiva agent:** Agroecology, biodiversity in agriculture, seed sovereignty
- **orr agent:** Ecological design as pedagogical practice
- **ecosystem-dynamics skill:** What is being conserved
- **climate-science skill:** Climate targets that design must meet
- **human-impact-assessment skill:** Baseline that sustainability interventions are measured against

## References

- WCED (Brundtland Commission). (1987). *Our Common Future*. Oxford University Press.
- Meadows, D. H. (2008). *Thinking in Systems*. Chelsea Green.
- IPCC WG3 AR6. (2022). *Climate Change 2022: Mitigation of Climate Change*. Cambridge University Press.
- Altieri, M. A. (1995). *Agroecology: The Science of Sustainable Agriculture*. 2nd edition. Westview.
- Mollison, B., & Holmgren, D. (1978). *Permaculture One*. Transworld.
- ISO 14040:2006 and ISO 14044:2006. *Environmental management — Life cycle assessment*.
- Ellen MacArthur Foundation. (2013). *Towards the Circular Economy*. EMF.
- Jackson, T. (2017). *Prosperity Without Growth*. 2nd edition. Routledge.
- Shiva, V. (1991). *The Violence of the Green Revolution*. Zed Books.
