---
name: stellar-spectroscopy
description: Stellar spectral analysis from first light to chemical abundance. Covers continuum emission and absorption, the OBAFGKM classification sequence, luminosity classes, line identification, Doppler shifts, curve-of-growth abundance analysis, and the astrophysical conclusions that follow from a spectrum. Use when classifying a star, measuring radial velocity, inferring composition or temperature, or teaching why the Sun is mostly hydrogen.
type: skill
category: astronomy
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/astronomy/stellar-spectroscopy/SKILL.md
superseded_by: null
---
# Stellar Spectroscopy

A stellar spectrum is the single most information-dense observation in astronomy. From a dispersed beam of starlight you can read temperature, luminosity, surface gravity, chemical composition, radial velocity, rotation speed, magnetic field strength, and binary companionship. This skill covers the core techniques for turning a spectrum into astrophysics: how the continuum forms, how absorption lines are produced, how to classify a star on the OBAFGKM sequence, how to identify and measure lines, how to extract Doppler velocity, and how to run a curve-of-growth abundance analysis. Cecilia Payne-Gaposchkin's 1925 dissertation — the first analysis to show that stars are mostly hydrogen — is the worked example at the end.

**Agent affinity:** payne-gaposchkin (composition analysis), burbidge (nucleosynthesis signatures)

**Concept IDs:** astro-hr-diagram, astro-stellar-classification, astro-nuclear-fusion

## Where a Spectrum Comes From

A star's spectrum has three components, each produced by a different physical process:

1. **Continuous spectrum (continuum)** — thermal emission from the hot, dense gas below the photosphere, approximately a blackbody with small deviations.
2. **Absorption lines** — cooler gas in the photosphere absorbs specific wavelengths as electrons jump between bound energy levels.
3. **Emission lines** (less common in stars) — hot tenuous gas re-emits at specific wavelengths, most prominent in Be stars, Wolf-Rayets, and the solar chromosphere.

Kirchhoff's laws (1859) describe this: a hot dense gas produces a continuous spectrum; a hot diffuse gas produces emission lines; a cool gas in front of a continuum source produces absorption lines. The Sun shows all three depending on where you look.

## The Continuum and Temperature

The continuum is approximately blackbody, so the shape of the continuum encodes temperature through the Wien displacement law:

    lambda_max * T ~ 2.9 x 10^-3 m K

For the Sun (T ~ 5800 K), lambda_max ~ 500 nm, in the middle of the visible. For an O star (T ~ 30,000 K), lambda_max ~ 100 nm, in the far UV. For an M dwarf (T ~ 3000 K), lambda_max ~ 1 micron, in the near IR.

**Color as a temperature proxy.** Photometric indices like B-V (blue minus visual magnitude) map to temperature without requiring a full spectrum. A B-V of 0.0 corresponds to T ~ 10,000 K (A0V); a B-V of 1.5 corresponds to T ~ 3600 K (M0V). But color alone cannot separate temperature from reddening by interstellar dust, so photometric classification is always uncertain until you have a spectrum.

## The OBAFGKM Spectral Sequence

Stellar spectra are classified into seven primary types based on which absorption lines dominate:

| Type | T (K) | Color | Dominant features | Example |
|---|---|---|---|---|
| O | 30,000-50,000 | blue | He II, ionized metals, weak H | 10 Lac |
| B | 10,000-30,000 | blue-white | He I strong, H stronger | Rigel, Spica |
| A | 7,500-10,000 | white | H lines maximum, weak metals | Sirius, Vega |
| F | 6,000-7,500 | yellow-white | H weakening, Ca II H and K strong | Procyon |
| G | 5,200-6,000 | yellow | Metal lines strong, Ca II dominant, G-band (CH) | Sun |
| K | 3,700-5,200 | orange | Metal lines very strong, molecular bands appear | Arcturus |
| M | 2,400-3,700 | red | TiO molecular bands dominate | Betelgeuse, Proxima |

Each type subdivides 0-9, so the Sun is G2. Later additions extended the sequence to **L** (brown dwarfs, metal hydrides), **T** (methane brown dwarfs), **Y** (coolest brown dwarfs, below 500 K).

**Why the sequence is not temperature alphabetical.** Annie Jump Cannon, working at Harvard between 1896 and 1924, classified over 350,000 stellar spectra and discovered that the alphabetical ordering from Secchi's earlier system did not match temperature. She reordered the types as OBAFGKM (mnemonic: "Oh Be A Fine Girl/Guy, Kiss Me") — the sequence that has stood for a century.

**The ionization-excitation interpretation.** Cecilia Payne-Gaposchkin (1925) used Saha's ionization equation and Boltzmann's excitation equation to show that the spectral sequence reflects temperature through the physics of atomic excitation and ionization, not the abundances of elements. Hydrogen lines peak at type A not because A stars have more hydrogen but because A-star temperatures put the most hydrogen atoms in the n=2 level from which the Balmer lines are absorbed.

## Luminosity Classes (Morgan-Keenan)

Spectral type alone gives temperature. To separate a cool dwarf from a cool giant (very different luminosities but similar temperatures), the MK system adds a luminosity class:

| Class | Name | Example |
|---|---|---|
| Ia | Bright supergiant | Rigel (B8Ia) |
| Ib | Supergiant | Betelgeuse (M1-M2 Ia-Iab) |
| II | Bright giant | Polaris (F7Ib-II) |
| III | Giant | Arcturus (K1.5III) |
| IV | Subgiant | Procyon (F5IV-V) |
| V | Main sequence (dwarf) | Sun (G2V) |
| VI | Subdwarf | Kapteyn's Star |
| VII | White dwarf | Sirius B |

**How luminosity is read from a spectrum.** Giants have lower surface gravity than dwarfs. Low gravity means lower photospheric pressure, which narrows pressure-broadened lines and strengthens certain ionization stages relative to neutrals. Specific ratios (e.g., Sr II 4077 / Fe I 4045) are calibrated luminosity indicators. The analyst compares these to standard spectra to assign a class.

## Line Identification

Identifying which element produced which line is the first step in any quantitative analysis.

**Procedure:**

1. **Calibrate wavelength.** Use an arc lamp (Fe-Ar, Th-Ar) taken in the same instrument setting. Residuals after calibration should be under 0.01 A for high-resolution work.
2. **Correct for radial velocity.** Measure the Doppler shift from known stellar features (see next section) and transform the observed wavelengths to the rest frame.
3. **Match against a line list.** Standard references: the Moore Multiplet Tables, the VALD database (Vienna Atomic Line Database), NIST ASD.
4. **Check oscillator strength and excitation potential.** A "possible identification" must also be physically plausible given the star's temperature.
5. **Blend handling.** Many lines overlap. Fitting requires deconvolution or exclusion of blended features.

**Typical features to recognize:**

- **Balmer series** — H-alpha 6563, H-beta 4861, H-gamma 4340, H-delta 4102. Hydrogen absorption in A-type and hot F stars.
- **Ca II H and K** — 3969 and 3934. Strongest in late-type stars (G, K).
- **Na I D doublet** — 5890, 5896. The famous yellow sodium feature.
- **Fe I multiplets** — hundreds of lines throughout the optical, dominant in G and K stars.
- **TiO bands** — broad molecular absorption at 4954, 5167, 6159 and elsewhere, the defining feature of M stars.
- **He I 5876** — present in A and earlier types, absent in cool stars.

## Doppler Shift and Radial Velocity

If a star moves toward or away from the observer, every spectral line shifts by the same proportional amount:

    (lambda_observed - lambda_rest) / lambda_rest = v_r / c

where v_r is positive for recession (redshift) and negative for approach (blueshift), and c is the speed of light.

**Measurement.** Identify a well-calibrated line and measure its observed wavelength to sub-angstrom precision (modern echelle spectrographs can do 1 m/s with careful analysis). Compute the shift. For high precision, correlate the whole spectrum against a template (Doppler cross-correlation) rather than relying on one line.

**Applications:**

- **Binary orbits.** A spectroscopic binary reveals itself through periodic RV variation.
- **Exoplanet detection.** The reflex motion of a star pulled by an orbiting planet produces sub-m/s RV signals.
- **Cluster membership.** Stars sharing a common RV are likely physical members of a cluster.
- **Galactic kinematics.** RVs of thousands of stars map the rotation curve of the Milky Way.

## Stellar Rotation from Line Broadening

A rotating star's lines are broadened because different parts of the disk approach and recede at different speeds. The broadening parameter is **v sin i** — the projected rotation velocity, where i is the unknown inclination angle.

**Measurement.** Fit the shape of a rotationally broadened line to a theoretical profile. The full width is proportional to v sin i divided by c. Typical values: Sun ~ 2 km/s, Vega ~ 20 km/s, rapidly rotating Be stars over 300 km/s.

Rotation broadening coexists with other broadening mechanisms: thermal Doppler broadening (proportional to sqrt(T)), pressure (Stark) broadening, microturbulence, and instrumental broadening. Disentangling them requires iterative spectral synthesis.

## Equivalent Width and the Curve of Growth

The **equivalent width** (EW) of an absorption line is the width of a rectangular block of zero-intensity absorption that would remove the same amount of flux:

    EW = integral of (1 - F_lambda / F_continuum) d-lambda

It has units of angstroms. EW is a convenient single number that captures how much an absorption line "bites out" of the continuum.

**The curve of growth** plots log(EW) against log(N * f * lambda) where N is the column density of absorbers in the lower level and f is the oscillator strength. The curve has three regimes:

1. **Linear regime** — weak lines. EW grows linearly with N. Small columns.
2. **Saturation (flat) regime** — line center goes to zero absorption. Growth is slow with N.
3. **Damping (square-root) regime** — strong lines. Damping wings dominate and EW grows as sqrt(N).

**Abundance measurement.** Observe many lines of the same ion. Plot log(EW/lambda) against log(gf) + excitation potential correction. Match to a theoretical curve of growth for an assumed temperature and microturbulence. Adjusting the assumed abundance slides the observed points vertically until they fit. The best-fit abundance is your answer.

This is the classical method. Modern work uses full spectral synthesis — generating a synthetic spectrum for an assumed model atmosphere and composition, convolving to the instrument resolution, and fitting the observed spectrum line by line. The physics is the same.

## Worked Example — Payne-Gaposchkin 1925

Cecilia Payne's Harvard PhD dissertation *Stellar Atmospheres* (1925) is the founding document of quantitative stellar spectroscopy.

**The puzzle.** Classical spectral analysis (before the Saha-Boltzmann framework) had concluded that the Sun had roughly terrestrial composition — iron, silicon, oxygen, and so on. This was wrong, but the error was invisible because it was baked into the methodology.

**The insight.** Payne applied Meghnad Saha's 1920 ionization equation to stellar photospheres. Saha's formula tells you, at a given temperature and electron pressure, what fraction of atoms of each element are in each ionization state. Combined with the Boltzmann distribution over excitation levels, you get the number of atoms in the specific quantum state from which a given absorption line originates.

**The calculation.** Payne observed that hydrogen and helium lines were strong despite being in the "wrong" excitation states for their visibility. When she worked backward from line strengths through Saha-Boltzmann to total elemental abundance, she got hydrogen and helium abundances a million times higher than the "heavy elements."

**The reception.** Payne's advisor Henry Norris Russell initially rejected the result as "clearly impossible" and persuaded her to soften the conclusion in her dissertation. Four years later Russell independently confirmed it and is sometimes miscredited with the discovery. Payne's result — that the universe is overwhelmingly hydrogen and helium — is the foundation on which stellar structure, Big Bang nucleosynthesis, and cosmic chemical evolution all rest.

**Lesson for the skill.** Getting the abundance right required applying the correct atomic physics to a correctly classified spectrum. Classification without physics gave terrestrial-like composition. Classification plus physics gave the actual universe.

## Strategy Selection Heuristics

| Question | Method |
|---|---|
| What kind of star is this? | Spectral type from line ratios; luminosity class from pressure-sensitive diagnostics |
| How fast is it moving toward or away? | Doppler shift of well-calibrated lines |
| Is it a binary? | Look for double lines, or monitor RV for periodic variation |
| How fast is it rotating? | v sin i from rotationally broadened line profiles |
| What is its composition? | Curve-of-growth or synthetic spectrum fitting |
| Does it have a magnetic field? | Zeeman splitting at high resolution |

## When NOT to Trust a Spectrum

- **Low S/N.** Noise near the continuum swamps weak lines and fakes features. For reliable line measurements, S/N > 100 per resolution element.
- **Blending.** Lines from different ions at the same wavelength cannot be separated without higher resolution.
- **Non-LTE effects.** The Saha-Boltzmann framework assumes local thermodynamic equilibrium. Hot stars, low-gravity giants, and some line-forming regions require non-LTE treatment.
- **Stellar activity.** Starspots, flares, and chromospheric emission contaminate the photospheric spectrum, especially for M dwarfs.
- **Interstellar contamination.** Interstellar Na I and Ca II absorption can mimic stellar features.

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Using line strength as abundance directly | Ignores Saha-Boltzmann | Run curve of growth or full synthesis |
| Single-line RV | One line, one chance to be wrong | Cross-correlate many lines |
| Ignoring telluric absorption | Atmospheric O2 and H2O mimic stellar features | Divide by a telluric standard |
| Confusing luminosity class with distance | Class gives radius, not distance | Combine with parallax or bolometric flux |
| Assuming solar abundance for everything | Metal-poor halo stars, s-process giants break this | Always verify against actual measurement |

## Cross-References

- **payne-gaposchkin agent:** The definitive specialist for composition analysis and Saha-Boltzmann application.
- **burbidge agent:** Nucleosynthesis signatures (s-process, r-process, alpha-element patterns).
- **hubble agent:** Cross-references between spectral classification and redshift-based galaxy work.
- **distance-ladder skill:** Spectroscopic parallax as a distance estimator using spectral type + apparent brightness.
- **naked-eye-observing skill:** Visual estimation of color as a crude temperature proxy before any spectrograph.

## References

- Payne, C. H. (1925). *Stellar Atmospheres: A Contribution to the Observational Study of High Temperature in the Reversing Layers of Stars*. Harvard College Observatory Monograph No. 1. (The Ph.D. dissertation.)
- Gray, D. F. (2005). *The Observation and Analysis of Stellar Photospheres*. 3rd edition. Cambridge University Press.
- Gray, R. O., & Corbally, C. J. (2009). *Stellar Spectral Classification*. Princeton University Press.
- Morgan, W. W., Keenan, P. C., & Kellman, E. (1943). *An Atlas of Stellar Spectra*. University of Chicago Press.
- Saha, M. N. (1920). "Ionization in the solar chromosphere." *Philosophical Magazine*, 40, 472.
- Mihalas, D. (1978). *Stellar Atmospheres*. 2nd edition. W. H. Freeman.
