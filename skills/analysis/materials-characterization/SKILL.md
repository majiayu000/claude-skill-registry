---
name: materials-characterization
description: Measurement techniques for identifying composition, microstructure, and properties of engineering materials — optical and electron microscopy, x-ray diffraction, EDS and WDS spectroscopy, thermal analysis, mechanical testing, and fractography. Covers when to use which technique, sample-preparation pitfalls, and how to build a characterization plan that answers a specific engineering question rather than accumulating data for its own sake.
type: skill
category: materials
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/materials/materials-characterization/SKILL.md
superseded_by: null
---
# Materials Characterization

Every materials-engineering question eventually becomes a characterization question. "Why did this fail?" becomes "what is on the fracture surface, what is the microstructure underneath, and what is the chemistry of the included phases?" "Will this alloy meet specification?" becomes "what is the grain size, the precipitate distribution, the hardness, and the tensile behavior?" "What is this stuff?" becomes a choice among the two dozen measurement techniques that can answer compositional and structural questions. This skill surveys the core techniques, identifies the question each is best at answering, and warns of the sample-preparation and interpretation mistakes that waste instrument time.

**Agent affinity:** cottrell (dislocation and microstructure imaging), gordon (failure-surface characterization)

**Concept IDs:** materials-measurement, materials-microstructure, materials-composition-analysis

## The Characterization Plan

A plan is more important than a technique. Instruments are expensive and time-limited; characterization that does not answer a specific question is a waste. The plan has three components.

1. **The question.** Written in a single sentence, in engineering language. "Is the precipitate distribution in this aged 2024-T3 consistent with a properly solution-treated and aged specimen?" is a question; "characterize this alloy" is not.
2. **The measurement that can answer it.** For that specific question: TEM of carbon-extraction replicas, supported by hardness and electrical-conductivity measurements on the bulk sample.
3. **The sample.** What location, what orientation, what preparation, what size. Bad sample selection wastes good measurement.

Characterization reports that cannot be traced back to a question are a sign of drift and should be returned to the plan-writing stage.

## Hierarchy of Resolution

Techniques span a huge range of length scales. A working map:

| Length scale | Technique | Question answered |
|---|---|---|
| ~mm and up | Visual, stereo microscopy | Gross features, fracture morphology, corrosion extent |
| 1 to 1000 um | Optical microscopy | Grain size, phase distribution, inclusions, cracks |
| 100 nm to 100 um | SEM (secondary + backscatter) | Surface topography, phase contrast, fractography |
| 10 nm to 10 um | SEM EDS/WDS | Local composition, elemental mapping |
| 0.1 nm to 100 nm | TEM (bright, dark, diffraction) | Dislocations, precipitates, interfaces, phase identification |
| 0.05 nm | HRTEM, atom probe tomography | Atomic structure, composition at single-atom resolution |
| Macroscale (bulk) | XRD, neutron diffraction | Phase fractions, texture, residual stress, lattice parameter |

Match the technique to the feature size. Looking for precipitates smaller than the SEM resolution with an SEM is a waste of time; looking at a millimeter-scale fracture with a TEM is absurd.

## Optical Microscopy

The oldest materials characterization technique and still the most cost-effective. Reflected-light optical microscopes with trained operators resolve down to about 0.5 um.

### Sample preparation (metallography)

The preparation is usually more important than the microscope. Steps:

1. **Sectioning** with an abrasive cut-off wheel, cooled to prevent microstructural change.
2. **Mounting** in a thermosetting (bakelite, epoxy) or cold-mount (acrylic) puck.
3. **Grinding** through progressively finer SiC papers (typically 240, 400, 600, 800, 1200 grit).
4. **Polishing** with diamond suspensions (typically 6, 3, 1, 0.25 um) on cloth.
5. **Etching** with a composition-appropriate reagent — nital (nitric in ethanol) for carbon steels, Keller's reagent for aluminum, Kalling's for copper, oxalic acid for stainless.

A bad mount, a scratched polish, or an over-etched surface produces artifacts that can be mistaken for real microstructure. A good optical metallurgist spends two or three times as much time on preparation as on image acquisition.

### What optical answers

Grain size (ASTM E112 linear intercept or equivalent-area methods), phase volume fractions, inclusion rating, surface heat treatment (case depth), macroscale cracks, porosity, and weld structure. Bright-field contrast comes from etching; dark-field, polarized-light, and differential-interference contrast add sensitivity for specific phase combinations.

## Scanning Electron Microscopy (SEM)

The SEM raster-scans a focused electron beam across a conductive sample and collects secondary electrons (topography), backscattered electrons (atomic-number contrast), or characteristic x-rays (composition). Resolution depends on the instrument: tungsten-filament SEMs reach ~5 nm, field-emission SEMs reach ~1 nm.

### Secondary-electron imaging

Produces topographic images with a three-dimensional appearance. The standard mode for fractography — surfaces are usually conductive (metals) or made conductive (sputter coating with gold or carbon). Dimples, striations, cleavage facets, and secondary cracks are all visible.

### Backscatter imaging

Backscatter yield rises with atomic number. Phases with different mean atomic numbers appear at different brightness — an austenitic region next to a ferritic region is distinguishable without etching. Backscatter is also the mode for electron backscatter diffraction (EBSD), which identifies crystallographic orientation at each pixel and produces grain-orientation maps.

### EDS and WDS

**Energy-dispersive spectroscopy (EDS)** collects all emitted x-rays simultaneously and sorts by energy. Fast, semi-quantitative, sensitive to about 0.1 weight percent, poor resolution for neighboring elements (overlapping lines). Good first-look tool.

**Wavelength-dispersive spectroscopy (WDS)** uses crystal diffractometers to resolve individual x-ray lines. Slower, quantitatively accurate to ~0.01 weight percent, separates overlapping lines. The reference tool for precise chemistry.

A typical SEM workflow on a failed part: collect low-magnification secondary-electron images of the fracture surface; zoom in to features of interest; acquire EDS spectra at inclusions, corrosion product, and matrix points; correlate with metallographic cross-sections of the same part.

## Transmission Electron Microscopy (TEM)

The TEM passes electrons through a thin (~100 nm) specimen. The transmitted beam is imaged to give structural and compositional information at near-atomic resolution. Modern aberration-corrected TEMs resolve individual atomic columns.

### Sample preparation

Thin sections are required. Techniques:

- **Electropolishing** (jet polishing) for conductive metals — makes a hole; the thin region around the hole is electron-transparent.
- **Ion milling** for nonconductive or brittle samples.
- **Focused ion beam (FIB)** lift-out — site-specific preparation, essential for semiconductor devices and for extracting TEM foils from a specific location on a failed part.
- **Carbon replicas** for precipitate extraction — evaporate carbon onto the polished and etched surface, dissolve the matrix, the precipitates come away on the carbon film.

### What TEM answers

Dislocation density and arrangement, precipitate size and identity, grain and subgrain structure at scales below SEM resolution, phase identification via selected-area electron diffraction (SAED), local composition via STEM-EDS. For age-hardened aluminum alloys, TEM is the definitive technique for showing whether the specified precipitate structure is actually present.

## X-Ray Diffraction (XRD)

A bulk technique that reveals crystal structure, phase composition, texture, and residual stress. A monochromatic x-ray beam is scattered from the sample, and Bragg's law (`n*lambda = 2*d*sin(theta)`) converts diffraction angles to interplanar spacings. Each crystalline phase produces a fingerprint pattern matchable against reference databases (ICDD, PDF).

Typical uses:

- **Phase identification.** Is this ferrite-pearlite, ferrite-bainite, tempered martensite, or retained austenite? XRD tells you.
- **Quantitative phase analysis** via Rietveld refinement of the full pattern.
- **Residual stress** via the sin^2(psi) method, tracking peak shifts as the sample is tilted.
- **Texture** via pole figures and orientation distribution functions.
- **Lattice parameter** to high precision, for alloying or solid-solution studies.

Amorphous samples give broad humps, not sharp peaks — the absence of sharp peaks is itself useful information.

## Thermal Analysis

Properties as functions of temperature.

- **Differential scanning calorimetry (DSC).** Measures heat flow as a specimen is heated or cooled. Detects phase transformations, glass transitions, melting, precipitate dissolution, and reaction kinetics.
- **Thermogravimetric analysis (TGA).** Measures mass as a function of temperature. Detects decomposition, dehydration, oxidation.
- **Thermomechanical analysis (TMA) and dilatometry.** Measures length change. Used for coefficient of thermal expansion and phase-transformation-induced volume changes (e.g., austenite to martensite in steel).

The characteristic trace of each technique on each material family is itself a database — a DSC of a polymer shows glass transition, crystallization, and melting peaks that classify the polymer to within a subfamily.

## Mechanical Testing

Controlled destruction to measure properties.

- **Tensile test.** The universal test. Produces yield stress, ultimate tensile stress, elongation, reduction in area, and Young's modulus if extensometry is used. Sample geometry (round or flat, standard gauge length) governs comparability.
- **Hardness.** Rockwell, Vickers, Brinell, Knoop, nanoindentation. Fast and nondestructive on a flat surface. Hardness correlates approximately with tensile strength in steels and some aluminum alloys; the correlation is not universal.
- **Impact (Charpy V-notch, Izod).** Measures energy absorbed in breaking a notched bar. Used for ductile-brittle transition characterization.
- **Fracture toughness (K_IC).** Measured on precracked specimens (compact tension or single-edge notched bend) according to ASTM E399.
- **Fatigue.** S-N tests for high-cycle life, strain-controlled tests for low-cycle life, growth-rate tests for `da/dN` curves.
- **Creep.** Constant-load or constant-stress tests at elevated temperature, often lasting thousands of hours.

A characterization report that claims yield strength from hardness alone without a direct tensile test should be treated with suspicion. Correlations are not measurements.

## Characterization Anti-Patterns

- **Technique-shopping.** Running every available technique and looking for a story. Waste of instrument time, produces internally contradictory data.
- **No blank.** Any comparison needs a reference sample prepared and measured identically.
- **Preparation artifacts mistaken for features.** Ion-milling pits, EDX peaks from the Cu grid or C coating, stitching artifacts in BSE mosaics — the analyst must know what preparation can introduce.
- **Acceptance of a single image as representative.** Microstructure varies; five fields of view are a minimum, twenty are better.
- **Single-point EDS spectra reported as bulk composition.** EDS interaction volume is ~1 to 5 um cube. A spectrum from one location is not a bulk composition.

## Cross-References

- **cottrell agent:** Primary agent for dislocation imaging, grain-size measurement, and microstructure interpretation.
- **gordon agent:** Failure-analysis agent — characterization in the service of diagnosing why something broke.
- **structural-failure-analysis skill:** Fractography as the first characterization step in any failure investigation.
- **iron-and-steel-processes skill:** Metallography and XRD on steels are standard quality-control characterizations.
- **nanomaterials-and-carbon skill:** TEM, Raman, and XRD techniques critical to nanomaterials work.

## References

- Vander Voort, G. F. (1999). *Metallography: Principles and Practice*. ASM International.
- Williams, D. B., & Carter, C. B. (2009). *Transmission Electron Microscopy: A Textbook for Materials Science*. 2nd edition. Springer.
- Goldstein, J. I., Newbury, D. E., Michael, J. R., et al. (2017). *Scanning Electron Microscopy and X-Ray Microanalysis*. 4th edition. Springer.
- Cullity, B. D., & Stock, S. R. (2001). *Elements of X-Ray Diffraction*. 3rd edition. Prentice Hall.
- ASM Handbook, Volume 10: *Materials Characterization* (2019).
- ASTM E112, E3, E407 — standards for grain size measurement, metallographic preparation, and etching.
