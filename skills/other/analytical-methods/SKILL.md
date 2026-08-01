---
name: analytical-methods
description: Spectroscopy, chromatography, titration, elemental analysis, X-ray crystallography, and mass spectrometry for chemical identification and quantitation. Covers UV-Vis and IR spectroscopy, NMR fundamentals, gas and liquid chromatography, gravimetric and volumetric analysis, diffraction methods, separation techniques, and quantitative error analysis. Use when identifying unknown substances, determining purity, measuring concentrations, or interpreting analytical data.
type: skill
category: chemistry
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/chemistry/analytical-methods/SKILL.md
superseded_by: null
---
# Analytical Methods

Analytical chemistry answers two questions: "What is it?" (qualitative analysis) and "How much is there?" (quantitative analysis). The methods range from classical wet chemistry — gravimetry, titration, and separation — to instrumental techniques that exploit the interaction of matter with electromagnetic radiation, electric fields, and crystal lattices. This skill covers the major techniques with worked examples of data interpretation.

**Agent affinity:** hodgkin (analytical/structural chemistry, primary)

**Concept IDs:** chem-mixtures-pure-substances, chem-physical-chemical-properties, chem-density

## Mixtures vs. Pure Substances

Understanding what you are analyzing starts with classification:

| Category | Subcategory | Characteristics | Example |
|---|---|---|---|
| Pure substance | Element | Cannot be decomposed further | Gold (Au), oxygen (O2) |
| Pure substance | Compound | Fixed composition, decomposable | Water (H2O), NaCl |
| Mixture | Homogeneous (solution) | Uniform composition, single phase | Saltwater, air, brass |
| Mixture | Heterogeneous | Non-uniform, multiple phases | Granite, oil-and-water |

Analytical methods separate mixtures into components and identify/quantify each.

## Physical and Chemical Properties in Analysis

**Physical properties** are observed without changing composition: density, melting point, boiling point, color, refractive index, solubility. These are the basis of physical methods of separation and identification.

**Chemical properties** describe how a substance reacts: flammability, reactivity with acids, oxidation tendency. Chemical tests (flame tests, precipitation reactions, pH indicators) exploit these.

**Intensive properties** (independent of amount: density, melting point, refractive index) are especially useful for identification because they are characteristic of the substance itself.

## Density and Its Analytical Uses

Density (rho) = mass / volume. Units: g/mL or g/cm^3 for liquids and solids; g/L for gases.

**Worked example.** *A mineral sample has mass ite ite ite 15.6 g and displaces 5.20 mL of water. Identify it.*

rho = 15.6 g / 5.20 mL = 3.00 g/mL.

Consulting a density table: calcite = 2.71, fluorite = 3.18, apatite = 3.19. The value 3.00 does not match common minerals exactly — further analysis (XRD, elemental) is needed. But the density narrows the field dramatically. This illustrates why density alone is a screening tool, not definitive identification.

**Worked example.** *Determine whether a gold ring (mass 19.3 g, volume 1.50 mL) is pure gold.*

rho = 19.3 / 1.50 = 12.9 g/mL. Pure gold = 19.3 g/mL. This ring is NOT pure gold — likely an alloy. The density is too low by 33%.

## Separation Techniques

### Filtration

Separates an insoluble solid from a liquid. Gravity filtration for routine work; vacuum filtration for faster throughput and drier precipitates.

### Distillation

Separates liquids by boiling point differences. Simple distillation works when boiling points differ by more than 25 C. Fractional distillation (using a fractionating column) resolves closer boiling points by providing multiple vaporization-condensation cycles.

### Extraction

Separates compounds by differential solubility in two immiscible solvents (typically water and an organic solvent). The partition coefficient K = [solute in organic layer] / [solute in aqueous layer] governs the distribution.

**Worked example.** *Caffeine has K = 4.6 between dichloromethane and water. If 100 mg of caffeine is dissolved in 100 mL water, how much is extracted by a single 100 mL portion of DCM?*

Mass in DCM = K x mass-in-water. Total mass = mass-in-DCM + mass-in-water.
Let x = mass in water after extraction. mass-in-DCM = 100 - x.
K = (100 - x)/100 / (x/100) = (100 - x) / x = 4.6.
100 - x = 4.6x. 100 = 5.6x. x = 17.9 mg in water.

Extracted: 100 - 17.9 = 82.1 mg (82.1% recovery in one extraction).

**Multiple smaller extractions are more efficient.** Three 33.3 mL portions recover more than one 100 mL portion — a fundamental principle of liquid-liquid extraction.

### Chromatography

All chromatographic methods separate components based on differential interaction with a stationary phase and a mobile phase.

| Method | Stationary phase | Mobile phase | Analytes |
|---|---|---|---|
| Paper chromatography | Cellulose paper | Solvent (water/organic mix) | Dyes, amino acids |
| Thin-layer (TLC) | Silica/alumina on plate | Organic solvent | Quick screening |
| Column chromatography | Silica/alumina in column | Organic solvent | Preparative separations |
| Gas chromatography (GC) | Coated capillary column | Carrier gas (He, N2) | Volatile organics |
| HPLC | Packed column (C18, silica) | Liquid solvent gradient | Non-volatile organics, biologics |
| Ion chromatography | Ion-exchange resin | Buffer solution | Ions in water |

**Retention factor (Rf) for TLC:** Rf = distance traveled by spot / distance traveled by solvent front. Each compound has a characteristic Rf under given conditions.

**Worked example.** *A TLC plate shows three spots at distances 2.1, 3.5, and 4.8 cm. The solvent front traveled 6.0 cm. Calculate Rf values.*

Rf1 = 2.1 / 6.0 = 0.35. Rf2 = 3.5 / 6.0 = 0.58. Rf3 = 4.8 / 6.0 = 0.80.

The spot at Rf = 0.80 is least polar (traveled farthest in a normal-phase system where silica is polar and the mobile phase is organic).

## Spectroscopic Methods

### UV-Visible Spectroscopy

**Principle.** Molecules absorb UV or visible light, promoting electrons from bonding/nonbonding orbitals to antibonding orbitals. Conjugated systems (alternating single and double bonds) absorb at longer wavelengths (lower energy).

**Beer-Lambert Law:** A = epsilon x b x c, where A is absorbance, epsilon is the molar absorptivity (L/mol-cm), b is path length (cm), and c is concentration (mol/L).

**Worked example.** *A solution of KMnO4 has an absorbance of 0.750 at 525 nm in a 1.00 cm cell. If epsilon = 2455 L/mol-cm, what is the concentration?*

c = A / (epsilon x b) = 0.750 / (2455 x 1.00) = 3.06 x 10^-4 mol/L = 0.306 mM.

**Applications.** Quantitative analysis of colored solutions, enzyme kinetics (following absorbance change over time), determining concentration of DNA/proteins (A260 and A280 nm).

### Infrared (IR) Spectroscopy

**Principle.** Molecules absorb IR radiation, causing bonds to vibrate (stretch, bend). Each functional group absorbs at characteristic frequencies.

**Key absorptions (wavenumber in cm^-1):**

| Functional group | Absorption range | Appearance |
|---|---|---|
| O-H (alcohol) | 3200-3550 | Broad |
| O-H (carboxylic acid) | 2500-3300 | Very broad |
| N-H | 3300-3500 | Medium, 1 or 2 peaks |
| C-H (sp3) | 2850-2960 | Strong |
| C=O (carbonyl) | 1650-1750 | Strong, sharp |
| C=C | 1600-1680 | Medium |
| C-O | 1000-1260 | Strong |

**Worked example.** *An IR spectrum shows a strong broad absorption at 3300 cm^-1 and a strong sharp peak at 1710 cm^-1. What functional groups are present?*

3300 broad = O-H stretch (carboxylic acid pattern, given the breadth). 1710 = C=O stretch. Together: carboxylic acid (-COOH). The broad O-H from 2500-3300 overlapping with C-H is the signature "acid O-H."

### Nuclear Magnetic Resonance (NMR)

**Principle.** Nuclei with spin (1H, 13C) in a magnetic field absorb radio-frequency radiation. The absorption frequency depends on the electronic environment — shielded nuclei absorb at different frequencies than deshielded ones.

**1H NMR key concepts:**

- **Chemical shift (delta, ppm):** Position on the spectrum. TMS = 0 ppm reference. Alkyl H near 0-2 ppm; adjacent to electronegative groups 2-5 ppm; aromatic H 6-8 ppm; aldehyde H near 9-10 ppm; carboxylic acid H near 10-12 ppm.
- **Integration:** Area under each peak is proportional to the number of equivalent H atoms.
- **Splitting (multiplicity):** n+1 rule — a signal split by n equivalent neighboring H atoms appears as n+1 peaks (singlet, doublet, triplet, quartet, etc.).

**Worked example.** *A compound C3H6O shows two 1H NMR signals: a singlet at 2.1 ppm (3H) and a singlet at 9.8 ppm (1H). Two signals total, but only 4H accounted for. The remaining 2H? Identify the compound.*

Wait — C3H6O has 6 H total. Let me re-examine: singlet at 2.1 ppm (3H) and another signal. If the spectrum shows a triplet at 2.4 ppm (2H) and a singlet at 9.8 ppm (1H) — that is propanal (CH3CH2CHO). But the problem states two singlets. A singlet at 2.1 ppm (3H) suggests a methyl not adjacent to any H. A singlet at 9.8 ppm (1H) is an aldehyde H. Possible structure: methylglyoxal? No — let us reconsider. C3H6O with a singlet at 2.1 (3H): this is actually the pattern of acetone if there is only one signal. With an aldehyde signal, the compound is likely propanal with the 2.1 ppm being the terminal methyl. In practice, the CH2 between them would show coupling. Let me correct: for a clean two-signal spectrum of C3H6O, the compound is acetone (CH3COCH3) — one singlet at 2.1 ppm (6H, two equivalent methyls). The 9.8 ppm signal would not appear. This illustrates why careful signal counting is critical in NMR interpretation.

### Mass Spectrometry (MS)

**Principle.** Molecules are ionized and fragmented. Fragments are separated by mass-to-charge ratio (m/z). The molecular ion peak (M+) gives the molecular weight; fragmentation pattern reveals structure.

**Key features:**

- **Molecular ion (M+):** Highest significant m/z value (excluding isotope peaks). Gives molecular formula.
- **Base peak:** Most intense peak (most stable fragment). Set to 100% relative intensity.
- **Common losses:** -15 (CH3), -18 (H2O), -28 (CO or C2H4), -29 (CHO), -31 (CH2OH), -45 (C2H5O).

**Worked example.** *A mass spectrum shows M+ at m/z = 60 and a strong peak at m/z = 42 (loss of 18). What does this suggest?*

Loss of 18 = loss of H2O. A molecule of molecular weight 60 that loses water likely contains an -OH group. Possible compound: 1-propanol (MW 60, C3H8O) or acetic acid (MW 60, C2H4O2). The loss of H2O from acetic acid is less characteristic; 1-propanol is the better candidate. Further fragmentation analysis (e.g., m/z = 31 from CH2OH+) would confirm.

## X-ray Crystallography

**Principle.** X-rays diffract off the electron clouds of atoms arranged in a crystal lattice. The diffraction pattern (angles and intensities) is mathematically transformed (Fourier transform) to produce a 3D electron density map, revealing atomic positions.

**Bragg's Law:** n-lambda = 2d-sin(theta), where lambda is X-ray wavelength, d is the spacing between crystal planes, and theta is the diffraction angle.

**Historical significance.** Dorothy Hodgkin (Nobel 1964) determined the structures of penicillin, vitamin B12, and insulin by X-ray crystallography. Rosalind Franklin's Photo 51 X-ray diffraction image of DNA was critical evidence for the double helix structure.

**Modern use.** Protein crystallography (synchrotron sources) determines 3D structures of enzymes and drug targets at atomic resolution. The Protein Data Bank (PDB) contains over 200,000 structures solved primarily by X-ray methods.

## Quantitative Analysis and Error

### Accuracy vs. Precision

**Accuracy:** How close a measurement is to the true value.
**Precision:** How close repeated measurements are to each other.

High precision + low accuracy = systematic error (calibration problem).
Low precision = random error (technique problem).

### Significant Figures in Analytical Results

Analytical results must report the correct number of significant figures. The limiting factor is the least precise measurement in the calculation.

**Worked example.** *A buret reads 23.45 mL (4 sig figs). A balance reads 0.1052 g (4 sig figs). The calculated molarity involves dividing mass by (molar mass x volume). Report to 4 sig figs.*

### Standard Deviation and Confidence

For n replicate measurements, the standard deviation s quantifies spread:

s = sqrt( sum(xi - x_mean)^2 / (n - 1) )

The 95% confidence interval: x_mean plus/minus t x s / sqrt(n), where t is the Student's t-value for n-1 degrees of freedom.

**Worked example.** *Three titration volumes: 25.34, 25.38, 25.31 mL. Calculate the mean, standard deviation, and 95% CI.*

Mean = (25.34 + 25.38 + 25.31) / 3 = 25.343 mL.

s = sqrt( (0.003^2 + 0.037^2 + 0.033^2) / 2 ) = sqrt( (0.000009 + 0.001369 + 0.001089) / 2 ) = sqrt(0.001234) = 0.035 mL.

For n = 3, df = 2, t(95%) = 4.303.

95% CI = 25.343 plus/minus 4.303 x 0.035 / sqrt(3) = 25.343 plus/minus 0.087 mL.

Report: 25.34 plus/minus 0.09 mL (95% confidence).

## Gravimetric Analysis

**Principle.** Convert the analyte to an insoluble precipitate of known composition, filter, dry, and weigh.

**Worked example.** *Determine the percent chloride in a 0.5000 g sample. The sample is dissolved and treated with excess AgNO3. The AgCl precipitate, after drying, weighs 0.7234 g.*

Moles AgCl = 0.7234 / 143.32 = 5.047 x 10^-3 mol.

Since each AgCl contains one Cl: moles Cl = 5.047 x 10^-3.

Mass Cl = 5.047 x 10^-3 x 35.45 = 0.1789 g.

Percent Cl = (0.1789 / 0.5000) x 100% = 35.78%.

## Volumetric Analysis (Titration)

**Principle.** Measure the volume of a standard solution (known concentration) needed to react completely with the analyte.

**Worked example.** *25.00 mL of an unknown HCl solution is titrated with 0.1025 M NaOH. The endpoint is reached at 31.42 mL NaOH. What is the HCl concentration?*

HCl + NaOH -> NaCl + H2O (1:1 mole ratio).

Moles NaOH = 0.1025 x 0.03142 = 3.221 x 10^-3 mol = moles HCl.

[HCl] = 3.221 x 10^-3 / 0.02500 = 0.1288 M.

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Reporting more sig figs than the data supports | Creates false impression of precision | Track sig figs through all calculations |
| Confusing absorption and transmission | A = 2 - log(%T); they are inversely related | Higher absorbance = lower transmission |
| Reading NMR chemical shifts backward | Higher delta = more deshielded (downfield) | Electronegative groups increase delta |
| Ignoring the blank in spectroscopy | Solvent and cuvette absorb too | Always subtract blank absorbance |
| Assuming one technique is enough | Complex mixtures need multiple methods | Combine separation (chromatography) with identification (MS, NMR) |
| Confusing accuracy and precision | Different sources of error require different fixes | Systematic errors affect accuracy; random errors affect precision |

## Cross-References

- **hodgkin agent:** Analytical and structural chemistry. Primary agent for all analytical method problems.
- **reactions-stoichiometry skill:** Titration stoichiometry, mole calculations, and limiting reagent analysis.
- **atomic-structure skill:** Mass spectrometry isotope patterns relate to isotopic abundances.
- **organic-chemistry skill:** Spectroscopic identification (IR, NMR, MS) is the primary organic structure determination workflow.
- **chemical-bonding skill:** IR absorptions reflect bond vibrations; bond strength determines absorption frequency.

## References

- Skoog, D. A., West, D. M., Holler, F. J., & Crouch, S. R. (2014). *Fundamentals of Analytical Chemistry*. 9th edition. Cengage Learning.
- Harris, D. C. (2016). *Quantitative Chemical Analysis*. 9th edition. W. H. Freeman.
- Silverstein, R. M., Webster, F. X., & Kiemle, D. J. (2014). *Spectrometric Identification of Organic Compounds*. 8th edition. Wiley.
- Hodgkin, D. C. (1965). "The X-ray Analysis of Complicated Molecules." Nobel Lecture.
- Pavia, D. L., Lampman, G. M., Kriz, G. S., & Vyvyan, J. A. (2015). *Introduction to Spectroscopy*. 5th edition. Cengage Learning.
- Bragg, W. L. (1913). "The Diffraction of Short Electromagnetic Waves by a Crystal." *Proceedings of the Cambridge Philosophical Society*, 17, 43-57.
