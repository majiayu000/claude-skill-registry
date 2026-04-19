---
name: climate-science
description: Climate physics, forcing, feedback, and attribution. Covers the greenhouse effect and radiative forcing, climate sensitivity, fast and slow feedbacks, the paleoclimate record, detection and attribution science, regional climate impacts, and the distinction between weather, climate variability, and forced climate change. Use when reasoning about global warming mechanisms, interpreting temperature or CO2 records, evaluating attribution claims for extreme events, or distinguishing signal from natural variability.
type: skill
category: environmental
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/environmental/climate-science/SKILL.md
superseded_by: null
---
# Climate Science

Climate science is the intersection of atmospheric physics, oceanography, paleoclimatology, and statistics, unified by the question of how Earth's energy budget behaves across scales from weather to billions of years. This skill covers the core machinery: the greenhouse effect, radiative forcing, climate sensitivity, feedbacks, the paleoclimate record, detection and attribution, and regional impacts. The content is grounded in the published IPCC literature and avoids both dismissal and catastrophism.

**Agent affinity:** commoner (systems and feedbacks), leopold (ecological consequences at land scale), carson (persistent perturbations and their pathways)

**Concept IDs:** envr-greenhouse-effect, envr-climate-feedbacks, envr-climate-evidence, envr-attribution-science

## The Planetary Energy Budget

At equilibrium, the energy Earth absorbs from the Sun equals the energy Earth radiates to space. The global mean incoming solar flux at the top of atmosphere is 340 W/m^2 (the solar constant ~1361 W/m^2 divided by 4 for the Earth's sphere-to-disk ratio). Of that:

- ~100 W/m^2 is reflected back to space (planetary albedo ~0.3, from clouds, ice, and surfaces).
- ~240 W/m^2 is absorbed by the atmosphere and surface.
- ~240 W/m^2 must leave as longwave infrared for energy balance to hold.

If only the surface radiated to space directly, the mean surface temperature required to balance 240 W/m^2 would be about 255 K (-18 C). Earth's actual mean surface temperature is about 288 K (+15 C). The 33-kelvin difference is the greenhouse effect.

## The Greenhouse Effect

Greenhouse gases — water vapor, CO2, CH4, N2O, O3, and halocarbons — absorb outgoing infrared radiation and re-emit it in all directions. The net effect is that radiation to space originates from higher, colder layers of the atmosphere, so the surface must warm to drive enough upward radiation to restore balance.

### Why some molecules absorb infrared and others do not

Symmetric diatomic molecules (N2, O2) have no permanent or changing dipole moment during vibration, so they do not absorb or emit in the infrared. Polyatomic molecules (H2O, CO2, CH4) have vibrational modes that change the dipole moment and therefore couple to IR radiation. This is why 99% of the atmosphere (N2 + O2) is transparent to outgoing longwave, and a few hundred parts per million of CO2 dominates the outgoing radiation budget at specific wavelengths.

### Current contributions

Of the 33-kelvin natural greenhouse effect, roughly 50% is water vapor, 25% is clouds, 20% is CO2, and 5% is other gases (CH4, N2O, O3). Water vapor is the largest contributor but is a **feedback**, not a forcing — its concentration depends on temperature (Clausius-Clapeyron: saturation vapor pressure rises exponentially with temperature). CO2, CH4, and other long-lived gases are **forcings**: their concentration is set by sources and sinks that operate largely independently of the year-to-year temperature.

## Radiative Forcing and Climate Sensitivity

### Radiative forcing

Radiative forcing (RF) is the change in net irradiance at the tropopause when an external perturbation is applied and the stratosphere is allowed to reach radiative equilibrium while surface and troposphere are held fixed. Units: W/m^2.

| Agent | Pre-industrial to 2020 RF (W/m^2) |
|---|---|
| CO2 | +2.16 |
| CH4 | +0.54 |
| N2O | +0.21 |
| Halocarbons | +0.41 |
| Tropospheric O3 | +0.47 |
| Aerosol (total) | -1.1 (large uncertainty) |
| Land-use albedo | -0.15 |
| Solar | +0.05 |
| Total anthropogenic | ~+2.7 |

Aerosols provide a cooling offset to the greenhouse forcing, and their uncertainty dominates the total forcing uncertainty.

### Climate sensitivity

Two numbers summarize how much the planet warms per unit forcing:

- **Equilibrium climate sensitivity (ECS)** — the steady-state surface temperature change for a doubling of CO2 (from 280 to 560 ppm). IPCC AR6 likely range: 2.5-4.0 C, best estimate 3.0 C.
- **Transient climate response (TCR)** — the surface temperature change at the time of CO2 doubling under a 1%/year CO2 increase. IPCC AR6 likely range: 1.4-2.2 C, best estimate 1.8 C.

TCR is smaller than ECS because the ocean takes centuries to warm, so the observed warming at any given time is smaller than the equilibrium commitment for the forcing then in place. This is why observed warming lags forcing.

## Feedbacks

Feedbacks are processes that amplify or damp the response to forcing. The sign convention: positive feedbacks increase sensitivity; negative feedbacks decrease it.

### Fast feedbacks (years to decades)

| Feedback | Mechanism | Sign |
|---|---|---|
| Water vapor | Warmer atmosphere holds more water vapor, amplifying the greenhouse effect | Strongly positive |
| Lapse rate | Warming is larger aloft in tropics, increasing outgoing IR efficiency | Negative |
| Cloud | Complex — low clouds cool, high clouds warm | Weakly positive (net) |
| Surface albedo | Sea ice and snow retreat reduce reflectivity | Positive |
| Planck | Warmer surface radiates more | Strongly negative (the baseline restoring force) |

Net fast feedbacks are positive — they roughly double the no-feedback warming from a CO2 doubling.

### Slow feedbacks (centuries to millennia)

- **Ice sheet albedo** — loss of Greenland and Antarctic ice caps reduces planetary albedo and raises sea level.
- **Vegetation** — biome shifts change land-surface albedo and evapotranspiration.
- **Permafrost carbon release** — thawing releases stored CO2 and CH4.
- **Ocean circulation** — thermohaline slowing changes heat transport and CO2 uptake.

ECS as defined above includes fast feedbacks but not slow. **Earth system sensitivity** (ESS) includes slow feedbacks and is typically 50% larger than ECS.

## The Paleoclimate Record

Quaternary ice core records (up to ~800,000 years) and older proxy records establish that climate is sensitive to small forcings over long times. Key facts:

- Glacial-interglacial CO2 ranged 180-280 ppm. The 2024 value of 425 ppm is outside the range of the last 3 million years.
- The Last Glacial Maximum (~20,000 years ago) was about 6 C colder globally, driven by a combination of orbital forcing, reduced CO2, and ice-albedo feedback. That forcing was roughly -7 W/m^2.
- The Paleocene-Eocene Thermal Maximum (55 million years ago) saw rapid warming of ~5-8 C over a few thousand years, associated with a massive carbon release. Recovery required >100,000 years.
- Milankovitch cycles (orbital eccentricity, obliquity, precession) pace glacial cycles by shifting summer insolation at high latitudes, but the temperature and CO2 response is too large to be explained by insolation alone — amplification by CO2 feedback is required.

## Detection and Attribution

Detection establishes that the climate has changed beyond natural variability. Attribution determines what caused the change. Both are statistical exercises.

### Observed global temperature

HadCRUT5, NOAA, Berkeley Earth, and Japan Meteorological Agency datasets independently show ~1.2 C of global warming since 1850-1900. The datasets differ in coverage, homogenization, and reference period but converge on the same trend.

### Attribution approaches

1. **Fingerprinting** — compare the observed spatial and temporal pattern of change to the pattern expected from different forcings (greenhouse gases vs. solar vs. volcanic). Greenhouse warming has distinctive fingerprints: tropospheric warming with stratospheric cooling, greater Arctic warming than global mean, larger nighttime than daytime warming. Solar warming would produce tropospheric and stratospheric warming together.
2. **Attribution fraction** — with and without anthropogenic forcing, how much more likely is an observed event? Probabilistic event attribution (Stott, Allen, and others from ~2004 onward) now routinely quantifies this for heat waves, heavy precipitation, and droughts within weeks of the event.
3. **Optimal fingerprinting** — a regression approach that accounts for internal variability.

IPCC AR6 (2021) states: "It is unequivocal that human influence has warmed the atmosphere, ocean, and land." The certainty language is based on detection-and-attribution results.

## Regional Impacts and Decomposition

Global mean temperature is one number; regional impacts are many. Some robust regional findings:

- **Arctic amplification** — warming at ~2-4x the global rate, driven by ice-albedo feedback and boundary-layer processes.
- **Land-ocean contrast** — land warms ~1.5x as fast as ocean, due to thermal inertia and moisture availability.
- **Mediterranean drying** — southern Mediterranean basin, southwestern U.S., and Chile are drying with high confidence.
- **Intensification of extreme precipitation** — Clausius-Clapeyron scaling of ~7% per degree C, with some regions showing larger increases from dynamic changes.
- **Sea level rise** — ~20 cm since 1900, accelerating since 1993 (now ~4.5 mm/yr). Projections to 2100 range from 0.3 to 1.0 m under current pathways, with larger values possible if ice sheet dynamics accelerate.

## Weather vs. Climate vs. Climate Change

Three regimes often get conflated:

- **Weather** — the state of the atmosphere at a place and time. Chaotic, predictable only days ahead.
- **Climate variability** — statistical distributions of weather over decades, driven by internal modes like ENSO, NAO, PDO, and volcanic forcing.
- **Forced climate change** — shifts in the climate distribution driven by external forcings (greenhouse gases, solar, aerosols).

A single heat wave is weather. A decade of increasing frequency of heat waves at a station is climate variability plus climate change. Separating the two requires statistical tools, not casual observation.

## When to Use This Skill

- Explaining the greenhouse effect or radiative forcing
- Interpreting temperature, CO2, or sea-level records
- Reasoning about climate sensitivity, feedbacks, or committed warming
- Evaluating attribution claims for specific extreme events
- Distinguishing regional impacts from global mean changes
- Clarifying weather, variability, and climate change confusions
- Reading ice core or paleoclimate proxy data

## When NOT to Use This Skill

- Ecosystem- or population-level biology — use `ecosystem-dynamics`
- Element cycles (carbon, nitrogen) in more than their climatic role — use `biogeochemical-cycles`
- Local pollution or habitat impact assessment — use `human-impact-assessment`
- Mitigation policy and intervention design — use `sustainability-design`
- Distributional burden and climate justice — use `environmental-justice`

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Pointing to a cold snap to dispute warming | Cold extremes persist in a warming mean | Compare distributions, not single events |
| Equating TCR with ECS | TCR is smaller by construction | State which sensitivity you mean |
| Ignoring slow feedbacks | Long-term sensitivity is higher | Distinguish ECS from ESS |
| Citing a single temperature dataset | Multiple datasets reduce systematic error | Quote at least two independently constructed datasets |
| Treating model projections as prediction | Models are scenarios under assumed forcings | Label pathway (RCP, SSP) explicitly |
| Confusing forcing with warming | Warming lags forcing due to ocean inertia | Report forcing and committed warming separately |

## Cross-References

- **commoner agent:** Systems view of climate as coupled feedback network
- **leopold agent:** Climate as the driver of biome and land community
- **carson agent:** Long-lived, persistent perturbations across systems
- **biogeochemical-cycles skill:** Greenhouse gas cycles that drive forcing
- **ecosystem-dynamics skill:** Ecological responses to climate shift
- **human-impact-assessment skill:** Climate as impact multiplier

## References

- IPCC AR6 WG1. (2021). *Climate Change 2021: The Physical Science Basis*. Cambridge University Press.
- Pierrehumbert, R. T. (2010). *Principles of Planetary Climate*. Cambridge University Press.
- Hansen, J., et al. (2013). "Climate sensitivity, sea level and atmospheric carbon dioxide." *Philosophical Transactions of the Royal Society A*, 371, 20120294.
- Stott, P. A., et al. (2016). "Attribution of extreme weather and climate-related events." *WIREs Climate Change*, 7(1), 23-41.
- Mann, M. E., Bradley, R. S., & Hughes, M. K. (1998). "Global-scale temperature patterns and climate forcing over the past six centuries." *Nature*, 392, 779-787.
- Forster, P., et al. (2021). "The Earth's Energy Budget, Climate Feedbacks, and Climate Sensitivity." In *IPCC AR6 WG1*, Chapter 7.
- Jouzel, J., et al. (2007). "Orbital and millennial Antarctic climate variability over the past 800,000 years." *Science*, 317, 793-796.
