---
name: cosmological-observation
description: Observational cosmology from Hubble's law to the CMB. Covers redshift, Hubble expansion, the cosmological parameters, the cosmic microwave background, large-scale structure, galaxy rotation curves and dark matter, Type Ia SNe and dark energy, and the current state of Lambda-CDM. Use when reasoning about the large-scale universe, interpreting cosmological surveys, or teaching the Big Bang evidence chain.
type: skill
category: astronomy
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/astronomy/cosmological-observation/SKILL.md
superseded_by: null
---
# Cosmological Observation

Modern cosmology is the shortest path from "what can I measure?" to "how old is the universe, what is it made of, and how does it end?" This skill covers the observational pillars: Hubble's law and redshift, the cosmic microwave background (CMB), Big Bang nucleosynthesis (BBN), large-scale structure, galaxy rotation curves as evidence for dark matter, Type Ia supernovae as evidence for dark energy, and the composition and parameters of the current concordance model (Lambda-CDM). It also covers the active frontier — the Hubble tension, the S8 tension, and the tests that could break or confirm Lambda-CDM in the next decade.

**Agent affinity:** hubble (expansion and distance), rubin (dark matter), burbidge (nucleosynthesis context)

**Concept IDs:** astro-big-bang, astro-dark-matter, astro-dark-energy, astro-cmb, astro-hubbles-law

## The Four Pillars of Big Bang Cosmology

1. **Hubble expansion** — galaxies recede with velocity proportional to distance
2. **Cosmic microwave background** — blackbody radiation at 2.725 K filling all space
3. **Big Bang nucleosynthesis** — observed primordial abundances of H, D, He-3, He-4, Li-7 match hot-early-universe predictions
4. **Large-scale structure** — galaxy distribution traces initial density fluctuations amplified by gravity

Any cosmological model that breaks one of these pillars is in serious trouble. Lambda-CDM — the current concordance model — was built to fit all four and has passed increasingly sharp tests from WMAP, Planck, BOSS, DES, and many others.

## Pillar 1 — Hubble's Law

In 1929 Edwin Hubble published a plot of galaxy distances (from Cepheid period-luminosity analysis) against their radial velocities (from spectroscopic redshift). He found:

    v = H_0 * d

with H_0 estimated at 500 km/s/Mpc. The slope was too steep by a factor of seven (the distance calibration had systematic errors that were later corrected), but the linear relation was real. Hubble had discovered that the universe is expanding.

**Modern H_0.** Local measurements (Cepheid + SN Ia): 73.0 +/- 1.0 km/s/Mpc. CMB + Lambda-CDM (Planck 2018): 67.4 +/- 0.5 km/s/Mpc. The 4-5 sigma discrepancy is the **Hubble tension**.

**Redshift.** For nearby galaxies, v = c z is a good approximation with z << 1. At cosmological distances, redshift is better interpreted as scale-factor expansion:

    1 + z = a_observed / a_emitted

where a is the cosmic scale factor. A redshift of z = 1 means the universe has doubled in size since the light was emitted; z = 1100 (the CMB redshift) means the universe was 1101 times smaller.

**Hubble flow vs. peculiar motion.** For galaxies within ~50 Mpc, local gravitational infall toward mass concentrations (the Virgo cluster, the Great Attractor) contributes velocities comparable to the Hubble flow. Cosmological H_0 measurements must avoid this regime or correct for it.

## Pillar 2 — The Cosmic Microwave Background

**Discovery.** Arno Penzias and Robert Wilson (Bell Labs, 1965) detected a 2.73 K excess signal in their horn antenna that they could not eliminate — not pigeons, not anything terrestrial. Simultaneously, Robert Dicke's group at Princeton had predicted such a signal would exist if the Big Bang were real: a blackbody radiation fossil from the era of recombination, cooled by cosmic expansion. The identification was immediate. Nobel Prize in Physics, 1978.

**Spectrum.** COBE FIRAS (Mather et al. 1994) measured the CMB spectrum to exquisite precision. It is a blackbody at T = 2.725 K with deviations smaller than 50 parts per million — the most perfect blackbody ever measured.

**Anisotropy.** The CMB is remarkably uniform but not perfectly so. After removing the dipole (from Earth's motion through the CMB rest frame) and the galactic plane foreground, anisotropies of order 10^-5 remain. These are the seeds from which all structure in the universe grew.

**Power spectrum.** Decompose the temperature anisotropies into spherical harmonics. The resulting power spectrum C_l has a series of **acoustic peaks** corresponding to sound waves in the photon-baryon plasma at recombination. The positions and heights of the peaks encode:

- **First peak angular scale:** total energy density / curvature (flat universe)
- **Relative heights of first and second peaks:** baryon density
- **Third peak:** matter density including dark matter
- **Damping tail:** helium fraction, neutrino background

WMAP (2001-2010) and Planck (2009-2013) have measured the CMB power spectrum from l ~ 2 to l ~ 2500 with percent-level precision, giving the parameters of Lambda-CDM to a few percent.

**Polarization.** The CMB is polarized at ~10% the level of the temperature anisotropies. E-mode polarization is produced by scalar density perturbations. B-mode polarization at large scales could come from primordial gravitational waves — a generic prediction of inflation — and its detection is a major target.

## Pillar 3 — Big Bang Nucleosynthesis (BBN)

At 1 second to 3 minutes after the Big Bang, the universe was hot enough for nuclear reactions but cooling rapidly. Protons and neutrons fused into light elements before the window closed. The predicted abundances depend on the baryon density:

- **He-4:** about 24% by mass
- **Deuterium (D):** D/H about 2.5 x 10^-5
- **He-3:** He-3/H about 10^-5
- **Li-7:** Li/H about 10^-10

These abundances are measured today in low-metallicity systems (to avoid stellar contamination) and the observed values match the BBN predictions when the baryon density is set to the value that the CMB also prefers. The agreement is one of the strongest confirmations that we understand the first few minutes of the universe.

**Lithium problem.** The observed Li-7 in metal-poor stars is lower than BBN predicts by about a factor of three. This is an unresolved tension — possibly stellar depletion, possibly new physics.

## Pillar 4 — Large-Scale Structure

Galaxies are not distributed randomly. Large redshift surveys (2dF, SDSS, BOSS, DES) have mapped millions of galaxies and revealed:

- **Filaments, walls, and voids** — a web-like structure on scales of 10-100 Mpc
- **Clusters** — dense knots at filament intersections
- **Baryon acoustic oscillations (BAO)** — a characteristic scale around 150 Mpc imprinted by sound waves at recombination, visible as a bump in the two-point correlation function

BAO is the CMB acoustic-peak physics seen in the galaxy distribution at late times. Measuring the BAO scale at different redshifts gives a standard ruler for distance, providing a distance measurement that does not rely on the Cepheid-SN Ia ladder.

## Dark Matter — Rotation Curves and Beyond

**Rotation curves.** Vera Rubin, working with Kent Ford at the Carnegie Institution in the 1970s and 1980s, measured rotation curves of spiral galaxies using optical emission lines. If mass were distributed like the visible light, rotation velocity should decrease at large radii (Keplerian fall-off). Instead, Rubin found that rotation curves stay flat out to the last measured points — implying that galaxies sit in extended halos of unseen mass.

**Quantitative.** For the Milky Way, visible mass accounts for about 6 x 10^10 solar masses. Dynamical mass inferred from rotation curves and satellite kinematics is about 10^12 solar masses. The ratio is roughly 15-20 times more total mass than luminous.

**Other evidence:**

- **Gravitational lensing.** Strong lensing arcs in galaxy clusters, weak lensing surveys of the cosmic shear field. Mass maps inferred from lensing do not track the light.
- **Bullet Cluster** (Clowe et al. 2006). A merging cluster where hot X-ray gas is slowed by ram pressure while the dark matter (traced by lensing) passes through unimpeded. The spatial separation is a direct demonstration that the gravitating mass is not baryonic.
- **CMB.** The relative heights of the first and third acoustic peaks require non-baryonic cold matter at the level of 27% of the critical density.

**What is it?** Not stars, not gas, not black holes (excluded by microlensing surveys). Candidates: WIMPs (undetected so far in direct-detection experiments), axions, primordial black holes, sterile neutrinos, or something still unguessed.

## Dark Energy — Accelerating Expansion

In 1998-1999, two independent teams (Riess et al., Perlmutter et al.) used Type Ia supernovae as standard candles to measure the expansion rate at cosmological distances. They expected a decelerating expansion (gravity pulling matter back together). They found acceleration.

**Interpretation.** Something with negative pressure — often called "dark energy" — dominates the cosmic energy budget. In Lambda-CDM, this is a cosmological constant (Einstein's Lambda from 1917, reinstated after his "greatest blunder" dismissal). Its energy density is about 68% of the critical density.

**The cosmological constant problem.** The value of Lambda (~10^-123 in Planck units) is dramatically smaller than quantum field theory naively predicts. This is one of the deepest unsolved problems in theoretical physics.

**Alternative models.** Quintessence (dynamical scalar field). Modified gravity (f(R), MOND-like extensions). Interacting dark sector. None have been confirmed or ruled out by current data.

## Lambda-CDM — The Concordance Model

Current best-fit parameters (Planck 2018 + BAO):

| Parameter | Value | Meaning |
|---|---|---|
| H_0 | 67.4 +/- 0.5 km/s/Mpc | Hubble constant |
| Omega_m | 0.315 +/- 0.007 | Matter density (fraction of critical) |
| Omega_Lambda | 0.685 +/- 0.007 | Dark energy density |
| Omega_b | 0.0493 +/- 0.0006 | Baryon density |
| Omega_c | 0.265 +/- 0.007 | Cold dark matter density |
| sigma_8 | 0.811 +/- 0.006 | Amplitude of matter clustering at 8 Mpc/h |
| n_s | 0.965 +/- 0.004 | Scalar spectral index |
| t_0 | 13.8 +/- 0.02 Gyr | Age of the universe |

**Flat universe.** Omega_total = 1.000 +/- 0.010. Space is flat to within observational precision.

**Matter composition.** 85% dark matter, 15% baryons, of which ~75% of baryons are hydrogen by mass and most of the rest is helium.

## Current Tensions

### Hubble tension

Local (Cepheid + SN Ia) H_0 = 73.0 vs. CMB H_0 = 67.4. 4-5 sigma discrepancy. Candidate resolutions: systematic in Cepheid distances (disfavored by TRGB-based independent local measurements), new physics before recombination (early dark energy), modified recombination, unknown systematics in Planck. Active research.

### S8 tension

Weak lensing surveys (KiDS, DES, HSC) measure a parameter S8 = sigma_8 * sqrt(Omega_m/0.3) that is slightly lower than Planck's prediction from the CMB. The significance is 2-3 sigma and growing as surveys improve.

### Lithium problem

BBN predicts more Li-7 than observed in metal-poor stars.

Each tension is small individually, but the pattern suggests Lambda-CDM may need modification. The next decade of data from Euclid, LSST, DESI, and CMB-S4 should settle the question.

## Strategy Selection Heuristics

| Question | Method |
|---|---|
| How fast is space expanding? | Hubble constant via SN Ia + Cepheids or CMB |
| How old is the universe? | Lambda-CDM age formula + CMB parameters |
| How much dark matter in galaxy X? | Rotation curve or lensing |
| What was the baryon density at z = 1100? | CMB acoustic peak fit |
| Is there primordial gravitational wave signal? | B-mode polarization in CMB |
| How did structure grow? | N-body simulations anchored to initial conditions from CMB |

## When to Doubt a Cosmological Claim

- **Single-probe results.** Any claim should be cross-checked against at least two independent probes.
- **Cosmic variance.** On the largest scales, there are few modes — statistical errors can be irreducible.
- **Foreground contamination.** CMB work especially requires sophisticated foreground subtraction.
- **Calibration systematics.** SN Ia distances depend on chains of calibration.
- **Model-dependence.** "The universe is 13.8 billion years old" assumes Lambda-CDM. A different model gives a different age.

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Treating v = cz as velocity at high z | Cosmological redshift is not Doppler | Use scale-factor interpretation |
| Assuming Hubble flow for local galaxies | Peculiar motions dominate at d < 50 Mpc | Use direct distance methods |
| Confusing dark matter with dark energy | Different physics, different evidence | DM clusters, DE accelerates |
| Quoting H_0 without method | Hubble tension is real | State whether local or CMB value |
| Over-interpreting isolated tensions | Statistical fluctuations happen | Wait for independent replication |

## Cross-References

- **hubble agent:** The namesake chair for observational cosmology.
- **rubin agent:** Dark matter evidence from rotation curves.
- **burbidge agent:** Nucleosynthesis context for BBN and stellar element production.
- **distance-ladder skill:** The calibration chain for H_0.
- **stellar-spectroscopy skill:** Redshift measurement techniques.

## References

- Hubble, E. (1929). "A relation between distance and radial velocity among extra-galactic nebulae." *PNAS*, 15, 168.
- Penzias, A. A., & Wilson, R. W. (1965). "A measurement of excess antenna temperature at 4080 Mc/s." *ApJ*, 142, 419.
- Mather, J. C., et al. (1994). "Measurement of the cosmic microwave background spectrum by the COBE FIRAS instrument." *ApJ*, 420, 439.
- Planck Collaboration (2020). "Planck 2018 results. VI. Cosmological parameters." *A&A*, 641, A6.
- Riess, A. G., et al. (1998). "Observational evidence from supernovae for an accelerating universe and a cosmological constant." *AJ*, 116, 1009.
- Perlmutter, S., et al. (1999). "Measurements of Omega and Lambda from 42 high-redshift supernovae." *ApJ*, 517, 565.
- Rubin, V. C., Ford, W. K., & Thonnard, N. (1980). "Rotational properties of 21 SC galaxies with a large range of luminosities and radii." *ApJ*, 238, 471.
- Clowe, D., et al. (2006). "A direct empirical proof of the existence of dark matter." *ApJL*, 648, L109.
