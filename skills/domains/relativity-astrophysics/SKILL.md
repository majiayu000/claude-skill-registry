---
name: relativity-astrophysics
description: Relativity and astrophysics from special relativity through cosmology. Covers Einstein's postulates, time dilation, length contraction, Lorentz transformations, relativistic momentum and energy (E=mc^2), spacetime diagrams, the equivalence principle, curved spacetime (conceptual), gravitational lensing, black holes (Schwarzschild solution, Chandrasekhar limit), stellar evolution (main sequence through supernova), and cosmology (Big Bang, Hubble's law, CMB, dark matter, dark energy, FLRW metric). Use when analyzing systems at relativistic speeds, strong gravitational fields, stellar lifecycles, or cosmological scales.
type: skill
category: physics
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/physics/relativity-astrophysics/SKILL.md
superseded_by: null
---
# Relativity and Astrophysics

Relativity and astrophysics together describe the universe at its most extreme — near the speed of light, near collapsed stars, and across cosmic timescales. Special relativity (Einstein, 1905) resolved the conflict between Newtonian mechanics and Maxwell's electromagnetism. General relativity (Einstein, 1915) replaced Newtonian gravity with the geometry of curved spacetime. Astrophysics applies these frameworks alongside nuclear physics and thermodynamics to explain stellar evolution, black holes, and the large-scale structure of the cosmos. This skill covers both relativities, stellar physics, and observational cosmology.

**Agent affinity:** chandrasekhar (astrophysics and relativity, Sonnet)

**Concept IDs:** phys-special-relativity, phys-cosmology, phys-gravitation

## Relativity and Astrophysics at a Glance

| # | Topic | Key equations | Core idea |
|---|---|---|---|
| 1 | Postulates of SR | c is invariant; physics is the same in all inertial frames | No preferred frame |
| 2 | Time dilation | Delta t = gamma Delta t_0 | Moving clocks run slow |
| 3 | Length contraction | L = L_0 / gamma | Moving objects are shorter |
| 4 | Lorentz transformations | x' = gamma(x - vt), t' = gamma(t - vx/c^2) | Coordinate transformations between frames |
| 5 | Relativistic momentum & energy | E^2 = (pc)^2 + (mc^2)^2 | Mass is a form of energy |
| 6 | Spacetime diagrams | ds^2 = -c^2 dt^2 + dx^2 | Geometry of Minkowski space |
| 7 | Equivalence principle | Gravity = acceleration (locally) | Foundation of general relativity |
| 8 | Curved spacetime | G_mu_nu = (8 pi G / c^4) T_mu_nu | Mass-energy curves spacetime |
| 9 | Black holes | r_s = 2GM/c^2 | Event horizons and singularities |
| 10 | Stellar evolution | Main sequence -> red giant -> remnant | Stars are nuclear fusion reactors |
| 11 | Cosmology | H_0 d = v, T_CMB = 2.725 K | The expanding universe |

## Topic 1 — Postulates of Special Relativity

**First postulate (Principle of Relativity).** The laws of physics are the same in all inertial reference frames. No experiment performed inside a sealed, uniformly moving laboratory can detect the lab's velocity.

**Second postulate (Invariance of c).** The speed of light in vacuum, c = 2.998 * 10^8 m/s, is the same for all observers regardless of the motion of the source or the observer.

**Why these are revolutionary.** In Newtonian mechanics, velocities add simply: if you walk at 5 km/h on a train moving at 100 km/h, your speed relative to the ground is 105 km/h. For light, this fails — light from a moving flashlight still travels at c. Reconciling this requires abandoning absolute time and absolute length.

**The Michelson-Morley experiment (1887).** Attempted to detect Earth's motion through the hypothesized luminiferous ether by measuring speed-of-light differences in perpendicular directions. Result: null. No ether exists; c is truly invariant.

## Topic 2 — Time Dilation

**Formula:** Delta t = gamma Delta t_0, where gamma = 1/sqrt(1 - v^2/c^2) is the Lorentz factor and Delta t_0 is the proper time (measured by a clock at rest relative to the events).

**Key insight.** Moving clocks run slow as observed from a stationary frame. This is not an illusion or a mechanical effect — time itself passes more slowly for the moving observer.

**Worked example.** *A muon (mean lifetime tau_0 = 2.2 microseconds) is created in the upper atmosphere at 0.995c. How far can it travel before decaying?*

**Solution.** Without time dilation: d = v tau_0 = 0.995 * 3e8 * 2.2e-6 = 656 m. This is far too short to reach the ground from typical creation altitudes of 10-15 km.

With time dilation: gamma = 1/sqrt(1 - 0.995^2) = 1/sqrt(1 - 0.990025) = 1/sqrt(0.009975) = 10.01. Dilated lifetime: tau = gamma tau_0 = 10.01 * 2.2e-6 = 22.0 microseconds. Distance: d = 0.995 * 3e8 * 22.0e-6 = 6568 m = 6.57 km.

Muons do reach the ground, confirming time dilation. This was one of the first direct experimental verifications (Rossi and Hall, 1941).

**The twin paradox.** One twin travels at high speed and returns younger than the twin who stayed home. This is not a paradox — the traveling twin accelerates (changes frames), breaking the symmetry. The resolution involves careful accounting of spacetime intervals.

## Topic 3 — Length Contraction

**Formula:** L = L_0 / gamma, where L_0 is the proper length (measured in the object's rest frame).

**Key insight.** Objects moving relative to an observer are measured to be shorter along the direction of motion. Like time dilation, this is a real physical effect, not an optical illusion.

**Worked example.** *A spaceship has a proper length of 100 m and travels at 0.8c relative to Earth. What is its length as measured by an Earth observer?*

**Solution.** gamma = 1/sqrt(1 - 0.64) = 1/sqrt(0.36) = 1/0.6 = 5/3. L = 100 / (5/3) = 60 m.

**The muon example, from the muon's frame.** In the muon's rest frame, the muon lives for 2.2 microseconds but the atmosphere is length-contracted. The 6.57 km of atmosphere (in the Earth frame) contracts to 6.57 km / 10.01 = 656 m in the muon's frame, which it can traverse in its proper lifetime. Both frames agree on the physics — the muon reaches the ground.

## Topic 4 — Lorentz Transformations

**The transformation equations** (for frames moving at relative velocity v along x):

x' = gamma(x - vt)
t' = gamma(t - vx/c^2)
y' = y
z' = z

**Inverse transformations:** Replace v with -v and swap primed/unprimed.

**Relativistic velocity addition:** u' = (u - v) / (1 - uv/c^2). This ensures that if u = c, then u' = c regardless of v.

**Worked example.** *Spaceship A moves at 0.6c relative to Earth. Spaceship B moves at 0.8c relative to Earth in the same direction. What is B's velocity relative to A?*

**Solution.** u' = (u - v)/(1 - uv/c^2) = (0.8c - 0.6c)/(1 - 0.48) = 0.2c / 0.52 = 0.385c.

Classical addition would give 0.2c. Relativistic addition gives 0.385c — larger because of the denominator correction, but still less than c.

## Topic 5 — Relativistic Momentum and Energy

**Relativistic momentum:** p = gamma m v. As v -> c, gamma -> infinity and p -> infinity, which is why massive objects cannot reach c.

**Total relativistic energy:** E = gamma mc^2.

**Rest energy:** E_0 = mc^2. Mass is a form of energy. A 1 kg object at rest contains 9 * 10^16 J of energy — equivalent to about 21 megatons of TNT.

**Energy-momentum relation:** E^2 = (pc)^2 + (mc^2)^2. This is the fundamental relation. For photons (m = 0): E = pc.

**Kinetic energy:** KE = (gamma - 1)mc^2. At low speeds, this reduces to the classical (1/2)mv^2 (verify by Taylor expanding gamma for v << c).

**Worked example.** *A proton (m_p = 938.3 MeV/c^2) is accelerated to 0.99c. Find its total energy, kinetic energy, and momentum.*

**Solution.** gamma = 1/sqrt(1 - 0.9801) = 1/sqrt(0.0199) = 7.09.

Total energy: E = gamma m_p c^2 = 7.09 * 938.3 = 6653 MeV.
Kinetic energy: KE = (gamma - 1)m_p c^2 = 6.09 * 938.3 = 5714 MeV.
Momentum: p = gamma m_p v = gamma m_p * 0.99c, or from E^2 = (pc)^2 + (m_p c^2)^2: pc = sqrt(6653^2 - 938.3^2) = sqrt(44.26e6 - 0.88e6) = sqrt(43.38e6) = 6586 MeV. So p = 6586 MeV/c.

## Topic 6 — Spacetime Diagrams

**Minkowski spacetime.** Space and time are unified into a 4-dimensional manifold. The invariant interval is ds^2 = -c^2 dt^2 + dx^2 + dy^2 + dz^2 (using the -+++ signature convention).

**Classification of intervals:**
- ds^2 < 0: timelike (events can be causally connected; a massive particle can travel between them)
- ds^2 = 0: lightlike / null (light signals connect them)
- ds^2 > 0: spacelike (no causal connection possible; events are "simultaneous" in some frame)

**Light cones.** At any event, the set of all lightlike intervals forms a cone in spacetime. The interior of the future light cone contains all events that can be influenced by the event. The interior of the past light cone contains all events that could have influenced it.

**Worldlines.** The trajectory of a particle through spacetime. Massive particles have timelike worldlines (always inside the light cone). Photons follow null worldlines (on the light cone). No physical worldline can be spacelike.

## Topic 7 — The Equivalence Principle

**Einstein's equivalence principle (1907).** A uniform gravitational field is locally indistinguishable from a uniformly accelerating reference frame. An observer in a closed elevator cannot determine whether they are standing on the surface of the Earth or accelerating at g in empty space.

**Consequences:**
- **Gravitational redshift:** Light climbing out of a gravitational field loses energy and shifts to longer wavelengths. Delta f / f = -g Delta h / c^2.
- **Gravitational time dilation:** Clocks in stronger gravitational fields run slower. GPS satellites must correct for this — without general relativistic corrections, GPS would drift by about 10 km per day.
- **Light bending:** Light follows curved paths in a gravitational field. Observed during the 1919 solar eclipse (Eddington), confirming general relativity.

**Worked example.** *By how much does a clock at the top of a 100 m tower run faster than a clock at the base? Use g = 9.8 m/s^2.*

**Solution.** Fractional time difference: Delta t / t = g Delta h / c^2 = 9.8 * 100 / (9e16) = 1.09 * 10^-14. In one day (86400 s): Delta t = 86400 * 1.09e-14 = 9.4 * 10^-10 s = 0.94 nanoseconds. Small, but measurable with atomic clocks (Pound-Rebka experiment, 1959).

## Topic 8 — Curved Spacetime and General Relativity

**Einstein's field equations:** G_mu_nu = (8 pi G / c^4) T_mu_nu.

The left side (Einstein tensor G) describes the curvature of spacetime. The right side (stress-energy tensor T) describes the distribution of mass-energy. In Wheeler's phrase: "Spacetime tells matter how to move; matter tells spacetime how to curve."

**Geodesics.** In curved spacetime, free-falling particles follow geodesics — the straightest possible paths. What we call "gravity" is the curvature of these paths. A planet orbiting a star is following a straight path through curved spacetime.

**Schwarzschild metric (1916).** The exact solution for the spacetime geometry outside a spherically symmetric, non-rotating mass M:

ds^2 = -(1 - r_s/r)c^2 dt^2 + (1 - r_s/r)^-1 dr^2 + r^2 d Omega^2

where r_s = 2GM/c^2 is the Schwarzschild radius.

**Gravitational lensing.** Massive objects curve spacetime, bending light from background sources. This produces multiple images, arcs, and Einstein rings. Gravitational lensing is now a major observational tool for mapping dark matter and discovering exoplanets.

## Topic 9 — Black Holes

**Schwarzschild black hole.** When an object's radius is less than its Schwarzschild radius r_s = 2GM/c^2, it becomes a black hole — a region of spacetime from which nothing, not even light, can escape.

**Event horizon.** The surface at r = r_s. It is not a physical surface but a causal boundary. An observer falling through the event horizon notices nothing locally (equivalence principle), but can never return or send signals outward.

**Chandrasekhar limit.** A white dwarf cannot exceed approximately 1.4 solar masses. Beyond this, electron degeneracy pressure cannot support the star against gravity, leading to collapse into a neutron star or black hole. Subrahmanyan Chandrasekhar derived this in 1930 at age 19.

**Worked example.** *Find the Schwarzschild radius of the Sun (M = 2 * 10^30 kg).*

**Solution.** r_s = 2GM/c^2 = 2 * 6.674e-11 * 2e30 / (9e16) = 2.67e20 / 9e16 = 2964 m, approximately 3 km. The Sun's actual radius is 696,000 km, so it is not a black hole.

**Hawking radiation (1974).** Black holes emit thermal radiation due to quantum effects near the event horizon. The temperature is T = hbar c^3 / (8 pi G M k_B). For stellar-mass black holes, this temperature is negligible (nanokelvins), but for microscopic black holes it could be significant.

## Topic 10 — Stellar Evolution

**Main sequence.** Stars spend most of their lives fusing hydrogen to helium in their cores. The mass-luminosity relation L proportional to M^3.5 governs their brightness and lifetime. The Sun's main sequence lifetime is about 10 billion years; a 10 solar-mass star lives only about 20 million years.

**Post-main-sequence evolution depends on mass:**

**Low mass (< 8 M_sun):**
1. Hydrogen exhaustion -> core contracts, shell hydrogen burning
2. Red giant phase (helium flash for stars < 2 M_sun)
3. Helium burning in core -> carbon/oxygen core
4. Planetary nebula ejected; core becomes a white dwarf

**High mass (> 8 M_sun):**
1. Successive fusion stages: H -> He -> C -> Ne -> O -> Si -> Fe
2. Iron core cannot fuse (iron has the highest binding energy per nucleon)
3. Core collapse -> supernova explosion (Type II)
4. Remnant: neutron star (< ~3 M_sun) or black hole (> ~3 M_sun)

**Worked example.** *The Sun converts about 4 million tonnes of matter to energy every second. How long can it sustain this? Take the Sun's mass as 2 * 10^30 kg and assume 10% of its hydrogen is available for fusion.*

**Solution.** Available mass for conversion: 0.1 * 2e30 = 2e29 kg. But only 0.7% of hydrogen mass is converted to energy in fusion: mass converted per lifetime = 0.007 * 2e29 = 1.4e27 kg. At 4e9 kg/s: lifetime = 1.4e27 / 4e9 = 3.5e17 s = 11.1 billion years. (The Sun is about 4.6 billion years old — it is roughly halfway through its main sequence life.)

## Topic 11 — Cosmology

**Hubble's law (1929):** v = H_0 d, where v is the recession velocity of a galaxy, d is its distance, and H_0 is the Hubble constant (approximately 70 km/s/Mpc). The universe is expanding.

**The Big Bang.** Extrapolating the expansion backward: the universe began in a hot, dense state approximately 13.8 billion years ago. Key evidence:
1. **Hubble expansion:** Galaxies recede in proportion to distance.
2. **Cosmic Microwave Background (CMB):** Thermal radiation at T = 2.725 K permeating all of space, released when the universe became transparent at about 380,000 years old (Penzias and Wilson, 1965).
3. **Big Bang nucleosynthesis:** Predicted abundances of hydrogen (75%), helium (25%), and trace lithium match observations.

**Dark matter.** Galaxy rotation curves, gravitational lensing, and CMB anisotropies all require about 5 times more matter than we can see. Dark matter interacts gravitationally but not electromagnetically. Its nature remains unknown.

**Dark energy.** The expansion of the universe is accelerating (discovered via Type Ia supernovae, Riess and Perlmutter, 1998). Dark energy constitutes about 68% of the total energy density of the universe. In the simplest model, it is a cosmological constant Lambda in Einstein's field equations.

**The cosmic inventory:** 68% dark energy, 27% dark matter, 5% ordinary (baryonic) matter.

**FLRW metric (conceptual).** The Friedmann-Lemaitre-Robertson-Walker metric describes a homogeneous, isotropic, expanding universe:

ds^2 = -c^2 dt^2 + a(t)^2 [dr^2/(1 - kr^2) + r^2 d Omega^2]

where a(t) is the scale factor (grows with time) and k = -1, 0, +1 determines spatial curvature (open, flat, closed). Observations strongly favor k = 0 (flat universe).

## When to Use This Skill

- Any problem involving speeds above about 0.1c
- Gravitational fields near compact objects (neutron stars, black holes)
- Stellar lifecycle and nucleosynthesis questions
- Cosmological questions (expansion, age of universe, CMB)
- E = mc^2 and mass-energy equivalence calculations
- GPS, particle accelerator, and muon decay problems (relativistic corrections)

## When NOT to Use This Skill

- **Everyday mechanics at low speeds:** Use the classical-mechanics skill. Relativistic corrections are negligible below 0.1c.
- **Quantum mechanics at non-relativistic scales:** Use the quantum-mechanics skill. This skill covers where they overlap (Dirac equation, Hawking radiation) only conceptually.
- **Circuit analysis or optics without relativistic context:** Use the electromagnetism skill.
- **Thermal systems without gravitational or cosmological context:** Use the thermodynamics skill.

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Using gamma < 1 | gamma = 1/sqrt(1 - v^2/c^2) is always >= 1 | If you get gamma < 1, check your algebra |
| Adding velocities classically at high speeds | v_total > c would violate relativity | Use relativistic velocity addition formula |
| Confusing proper time with coordinate time | Proper time is measured by the object's own clock | Identify whose clock measures each interval |
| Applying Newtonian gravity near black holes | Newtonian gravity breaks down at r comparable to r_s | Use the Schwarzschild metric or post-Newtonian corrections |
| Claiming the Big Bang happened "at a point" | The Big Bang happened everywhere simultaneously | The expansion is of space itself, not an explosion into pre-existing space |
| Confusing redshift with Doppler shift | Cosmological redshift is due to space expansion, not source motion | Use z = Delta lambda / lambda and the scale factor relation 1 + z = a_now / a_then |

## Cross-References

- **chandrasekhar agent:** Primary agent for relativity and astrophysics. Sonnet-class, broad coverage of stellar physics and GR.
- **curie agent:** Department chair, coordinates problems that bridge relativity with other domains.
- **feynman agent:** For the quantum-relativistic interface (Dirac equation, Hawking radiation, QFT concepts).
- **faraday agent:** Pedagogy specialist — intuitive explanations of time dilation, curved spacetime, and cosmic expansion.
- **classical-mechanics skill:** For the Newtonian limit of gravitational problems (weak fields, low speeds).
- **quantum-mechanics skill:** For quantum effects in astrophysical contexts (tunneling in stellar fusion, black hole radiation).
- **thermodynamics skill:** For stellar interiors (nuclear fusion energy balance, radiation pressure, stellar structure equations).

## References

- Carroll, S. M. (2019). *Spacetime and Geometry: An Introduction to General Relativity*. 2nd edition. Cambridge University Press.
- Hartle, J. B. (2003). *Gravity: An Introduction to Einstein's General Relativity*. Pearson.
- Schutz, B. (2009). *A First Course in General Relativity*. 2nd edition. Cambridge University Press.
- Weinberg, S. (2008). *Cosmology*. Oxford University Press.
- Carroll, B. W., & Ostlie, D. A. (2017). *An Introduction to Modern Astrophysics*. 2nd edition. Cambridge University Press.
- Misner, C. W., Thorne, K. S., & Wheeler, J. A. (1973). *Gravitation*. W. H. Freeman.
- Einstein, A. (1905). "Zur Elektrodynamik bewegter Korper." *Annalen der Physik*, 17, 891-921.
- Einstein, A. (1915). "Die Feldgleichungen der Gravitation." *Sitzungsberichte der Preussischen Akademie der Wissenschaften*, 844-847.
- Chandrasekhar, S. (1931). "The Maximum Mass of Ideal White Dwarfs." *Astrophysical Journal*, 74, 81-82.
- Hawking, S. W. (1974). "Black hole explosions?" *Nature*, 248, 30-31.
