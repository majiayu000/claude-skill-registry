---
name: quantum-mechanics
description: Quantum mechanics from wave-particle duality through entanglement and measurement. Covers the photoelectric effect, de Broglie wavelength, Heisenberg uncertainty principle, the Schrodinger equation (time-dependent and time-independent), wave functions and probability, quantum states and superposition, the hydrogen atom (energy levels, quantum numbers), spin, Pauli exclusion principle, quantum tunneling, Feynman path integrals (conceptual), QED basics, entanglement (Bell's theorem), the measurement problem, and Dirac notation. Use when analyzing phenomena at atomic or subatomic scales where classical physics breaks down.
type: skill
category: physics
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/physics/quantum-mechanics/SKILL.md
superseded_by: null
---
# Quantum Mechanics

Quantum mechanics describes the behavior of matter and energy at atomic and subatomic scales. It replaced classical mechanics for small systems after a series of experimental crises in the early 20th century — blackbody radiation (Planck, 1900), the photoelectric effect (Einstein, 1905), the Bohr model (1913), and the full wave mechanics of Schrodinger and Heisenberg (1925-26). The theory is probabilistic, non-local, and profoundly counterintuitive, yet it is the most precisely tested theory in all of science. This skill covers the foundational concepts, mathematical framework, and key applications of non-relativistic quantum mechanics, with pointers to relativistic extensions.

**Agent affinity:** feynman (quantum mechanics, Opus)

**Concept IDs:** phys-quantum-basics, phys-nuclear-physics, phys-special-relativity

## Quantum Mechanics at a Glance

| # | Topic | Key equations | Core idea |
|---|---|---|---|
| 1 | Wave-particle duality | E = hf, p = h/lambda | Matter and light have both wave and particle properties |
| 2 | Photoelectric effect | KE_max = hf - phi | Light comes in quanta (photons) |
| 3 | de Broglie wavelength | lambda = h/p = h/(mv) | Particles have associated wavelengths |
| 4 | Uncertainty principle | Delta x Delta p >= hbar/2 | Conjugate variables cannot both be precisely known |
| 5 | Schrodinger equation | H psi = E psi | Wave equation for quantum states |
| 6 | Wave functions | P = |psi|^2 | Probability from amplitude squared |
| 7 | Hydrogen atom | E_n = -13.6 eV / n^2 | Quantized energy levels |
| 8 | Spin & Pauli exclusion | s = 1/2 for electrons | No two identical fermions in same state |
| 9 | Quantum tunneling | T ~ exp(-2 kappa L) | Particles penetrate classically forbidden barriers |
| 10 | Path integrals | K = sum over all paths of exp(iS/hbar) | All histories contribute |
| 11 | Entanglement | Bell inequality violation | Non-local correlations without signaling |
| 12 | Measurement problem | Collapse vs. decoherence vs. many-worlds | Interpretation remains open |

## Topic 1 — Wave-Particle Duality

**The central mystery.** Light behaves as a wave in interference and diffraction experiments (Young's double slit, 1801), yet it behaves as a particle in the photoelectric effect and Compton scattering. Matter behaves as particles in everyday life, yet electrons and even large molecules produce interference patterns. Wave-particle duality is not a defect of the theory — it is a fundamental feature of nature.

**Planck's relation:** E = hf, where h = 6.626 * 10^-34 J s is Planck's constant and f is frequency.

**de Broglie's relation:** lambda = h/p, where p is momentum. This connects the wave and particle descriptions.

**Complementarity (Bohr).** Wave and particle aspects are complementary — an experiment reveals one or the other, never both simultaneously. The double-slit experiment with which-path detectors demonstrates this: detecting which slit the particle passes through destroys the interference pattern.

## Topic 2 — The Photoelectric Effect

**Experimental facts (Hertz, 1887; Lenard, 1902):**
1. Light below a threshold frequency produces no electrons, regardless of intensity.
2. Above threshold, electrons appear instantly (no delay).
3. Increasing intensity increases the number of electrons, not their maximum energy.
4. Maximum kinetic energy increases linearly with frequency.

**Einstein's explanation (1905):** Light consists of photons, each carrying energy E = hf. A photon ejects an electron only if hf >= phi (the work function). The maximum kinetic energy of the ejected electron is KE_max = hf - phi.

**Worked example.** *Ultraviolet light of wavelength 200 nm strikes a sodium surface (phi = 2.28 eV). Find the maximum kinetic energy of emitted electrons.*

**Solution.** Photon energy: E = hc/lambda = (6.626e-34)(3e8)/(200e-9) = 9.94e-19 J = 6.21 eV. KE_max = 6.21 - 2.28 = 3.93 eV.

**Stopping voltage.** The maximum KE can be measured by applying a retarding voltage: eV_stop = KE_max, so V_stop = 3.93 V.

## Topic 3 — de Broglie Wavelength

**de Broglie's hypothesis (1924):** Every particle with momentum p has an associated wavelength lambda = h/p. This was experimentally confirmed by Davisson and Germer (1927), who observed electron diffraction from nickel crystals.

**Worked example.** *Find the de Broglie wavelength of an electron accelerated through 100 V.*

**Solution.** Kinetic energy: KE = eV = 1.6e-19 * 100 = 1.6e-17 J. Momentum: p = sqrt(2mKE) = sqrt(2 * 9.11e-31 * 1.6e-17) = sqrt(2.916e-47) = 5.4e-24 kg m/s. Wavelength: lambda = h/p = 6.626e-34 / 5.4e-24 = 1.23e-10 m = 0.123 nm.

This is comparable to atomic spacings, which is why electrons can be diffracted by crystal lattices. For a baseball (0.15 kg at 40 m/s), lambda = 1.1e-34 m — immeasurably small, which is why baseballs don't diffract.

## Topic 4 — The Heisenberg Uncertainty Principle

**Statement:** Delta x Delta p >= hbar/2, where hbar = h/(2 pi) = 1.055 * 10^-34 J s.

**Energy-time form:** Delta E Delta t >= hbar/2.

**What it means.** The uncertainty principle is not about measurement limitations or experimental clumsiness. It is a fundamental property of wave-like systems: a wave packet that is localized in position must be spread in wavelength (and hence momentum), and vice versa. This is a mathematical consequence of Fourier analysis.

**Worked example.** *An electron is confined to a region of width 10^-10 m (approximately an atomic diameter). What is the minimum uncertainty in its momentum and the corresponding minimum kinetic energy?*

**Solution.** Delta p >= hbar/(2 Delta x) = 1.055e-34 / (2 * 1e-10) = 5.28e-25 kg m/s. Minimum KE ~ (Delta p)^2/(2m) = (5.28e-25)^2/(2 * 9.11e-31) = 2.79e-49 / 1.82e-30 = 1.53e-19 J = 0.96 eV.

This is on the order of atomic binding energies — the uncertainty principle explains why electrons in atoms have characteristic energy scales of a few eV.

**What it does NOT mean.** The uncertainty principle does not say "observation disturbs the system" (though it can). It says that the state itself does not possess simultaneously precise position and momentum. This is a statement about nature, not about instruments.

## Topic 5 — The Schrodinger Equation

**Time-dependent Schrodinger equation:**

i hbar d psi/dt = H psi

where H = -(hbar^2)/(2m) nabla^2 + V(x) is the Hamiltonian operator.

**Time-independent Schrodinger equation** (for stationary states with definite energy):

H psi = E psi, or equivalently: -(hbar^2)/(2m) d^2 psi/dx^2 + V(x) psi = E psi

**Particle in a box (infinite square well).** A particle confined between x = 0 and x = L with infinite potential walls.

Solutions: psi_n(x) = sqrt(2/L) sin(n pi x / L), E_n = n^2 pi^2 hbar^2 / (2mL^2), n = 1, 2, 3, ...

**Worked example.** *An electron in a 1D box of width L = 1 nm. Find the energy of the ground state (n = 1).*

**Solution.** E_1 = pi^2 hbar^2 / (2mL^2) = pi^2 (1.055e-34)^2 / (2 * 9.11e-31 * (1e-9)^2) = 1.097e-67 * 9.87 / (1.822e-48) = 6.02e-20 J = 0.376 eV.

**Key features:** Energy is quantized (only discrete E_n allowed). The ground state energy is nonzero (zero-point energy). The wave function has n-1 nodes. Higher energy states oscillate more rapidly.

## Topic 6 — Wave Functions and Probability

**Born's rule (1926):** The probability of finding a particle in the interval [x, x + dx] is P(x) dx = |psi(x)|^2 dx. The wave function psi is a probability amplitude; its modulus squared is the probability density.

**Normalization:** integral from -infinity to +infinity of |psi|^2 dx = 1. The particle must be found somewhere.

**Expectation values:** <x> = integral of x |psi|^2 dx. <p> = integral of psi* (-i hbar d/dx) psi dx. These give the average result of measuring position or momentum over many identically prepared systems.

**Superposition.** If psi_1 and psi_2 are valid states, then c_1 psi_1 + c_2 psi_2 is also a valid state. Measurement collapses the superposition: the probability of finding the system in state psi_n is |c_n|^2.

## Topic 7 — The Hydrogen Atom

**Energy levels:** E_n = -13.6 eV / n^2, n = 1, 2, 3, ...

**Quantum numbers:**
- Principal: n = 1, 2, 3, ... (determines energy)
- Orbital angular momentum: l = 0, 1, ..., n-1 (determines orbital shape: s, p, d, f)
- Magnetic: m_l = -l, ..., 0, ..., +l (determines orbital orientation)
- Spin: m_s = +1/2 or -1/2

**Degeneracy.** For hydrogen, all states with the same n have the same energy (2n^2 states per level, including spin). In multi-electron atoms, this degeneracy is broken by electron-electron interactions.

**Worked example.** *Find the wavelength of light emitted when a hydrogen atom transitions from n = 3 to n = 2 (the H-alpha line).*

**Solution.** Delta E = -13.6(1/9 - 1/4) = -13.6(-5/36) = 1.889 eV = 3.025e-19 J. lambda = hc/Delta E = (6.626e-34)(3e8)/(3.025e-19) = 6.57e-7 m = 657 nm. This is red light — the prominent red line in the hydrogen emission spectrum, first measured by Balmer in 1885.

**Spectral series:** Lyman (to n=1, UV), Balmer (to n=2, visible), Paschen (to n=3, IR), Brackett (to n=4, IR).

## Topic 8 — Spin and the Pauli Exclusion Principle

**Spin.** Electrons possess an intrinsic angular momentum called spin, with quantum number s = 1/2. The spin component along any axis has two values: m_s = +1/2 ("spin up") or m_s = -1/2 ("spin down"). Spin has no classical analog — it is not the electron "spinning" on an axis.

**The Stern-Gerlach experiment (1922).** A beam of silver atoms passing through an inhomogeneous magnetic field splits into exactly two beams, demonstrating the quantization of angular momentum and the existence of spin.

**Pauli exclusion principle.** No two identical fermions (particles with half-integer spin, including electrons, protons, neutrons) can occupy the same quantum state simultaneously. This principle explains:
- The periodic table (electron shell filling)
- The stability of matter (electrons cannot all collapse to the ground state)
- White dwarf stars (electron degeneracy pressure supports against gravity)
- Neutron stars (neutron degeneracy pressure)

**Worked example.** *How many electrons can occupy the n = 3 shell of an atom?*

**Solution.** For n = 3: l = 0, 1, 2. For each l, m_l ranges from -l to +l, giving (2l+1) values. Each (n, l, m_l) state holds 2 electrons (spin up and down). Total: 2(1 + 3 + 5) = 2(9) = 18 electrons.

## Topic 9 — Quantum Tunneling

**The phenomenon.** A quantum particle can penetrate a potential energy barrier even when its kinetic energy is less than the barrier height. Classically, this is forbidden — a ball rolling toward a hill with insufficient energy always rolls back. Quantum mechanically, the wave function decays exponentially inside the barrier but does not reach zero, so there is a nonzero probability of appearing on the other side.

**Transmission coefficient (rectangular barrier):** T ~ exp(-2 kappa L), where kappa = sqrt(2m(V_0 - E)) / hbar, L is the barrier width, and V_0 - E is the energy deficit.

**Worked example.** *An electron (E = 5 eV) encounters a barrier of height V_0 = 10 eV and width L = 0.5 nm. Estimate the tunneling probability.*

**Solution.** kappa = sqrt(2 * 9.11e-31 * 5 * 1.6e-19) / 1.055e-34 = sqrt(1.457e-48) / 1.055e-34 = 1.207e-24 / 1.055e-34 = 1.144e10 m^-1.

2 kappa L = 2 * 1.144e10 * 5e-10 = 11.44.

T ~ exp(-11.44) = 1.07 * 10^-5, or about 1 in 100,000.

**Applications.** Tunneling is not exotic — it is essential to:
- **Alpha decay:** Alpha particles tunnel out of the nuclear potential well
- **Scanning tunneling microscope (STM):** Electrons tunnel across a vacuum gap; current depends exponentially on distance
- **Tunnel diodes and flash memory:** Technological applications of controlled tunneling
- **Nuclear fusion in stars:** Protons tunnel through their Coulomb barrier at temperatures far below the classical threshold

## Topic 10 — Feynman Path Integrals (Conceptual)

**The path integral formulation (Feynman, 1948).** Instead of solving the Schrodinger equation directly, compute the propagator K(b, a) as a sum over all possible paths from point a to point b:

K(b, a) = sum over all paths of exp(i S[path] / hbar)

where S is the classical action (integral of the Lagrangian along the path).

**Key insights:**
- Every path contributes, not just the classical path.
- Paths near the classical path have similar phases and reinforce (constructive interference).
- Paths far from the classical path have wildly varying phases and cancel (destructive interference).
- In the classical limit (hbar -> 0), only the classical path survives — this recovers Newton's mechanics from quantum mechanics.

**Why it matters.** The path integral formulation is mathematically equivalent to the Schrodinger equation but provides deeper physical intuition and extends naturally to quantum field theory and QED. Feynman diagrams arise from this framework.

## Topic 11 — Entanglement and Bell's Theorem

**Entanglement.** Two particles are entangled when their quantum state cannot be written as a product of individual states. Measuring one particle instantaneously determines the state of the other, regardless of distance.

**The EPR argument (Einstein, Podolsky, Rosen, 1935).** If quantum mechanics is complete, then measuring one particle instantaneously affects a distant particle (non-locality). Einstein called this "spooky action at a distance" and argued that quantum mechanics must be incomplete — there must be hidden variables determining the outcomes in advance.

**Bell's theorem (1964).** John Bell derived an inequality that any local hidden variable theory must satisfy. Quantum mechanics predicts violations of this inequality.

**Experimental verdict (Aspect, 1982; and many since).** Bell's inequality is violated — nature is non-local in the quantum sense. No local hidden variable theory can reproduce quantum mechanics.

**No-signaling theorem.** Despite non-local correlations, entanglement cannot be used to send information faster than light. The correlations are only visible when you compare measurements from both particles, which requires classical communication.

## Topic 12 — The Measurement Problem

**The problem.** The Schrodinger equation is deterministic and linear — superpositions evolve into superpositions. Yet measurement always yields a definite outcome. How does a deterministic wave equation produce probabilistic results? This is the measurement problem.

**Major interpretations:**
- **Copenhagen (Bohr, Heisenberg):** Measurement causes "collapse" of the wave function. Pragmatic but silent on the mechanism.
- **Many-worlds (Everett, 1957):** No collapse occurs. The universe branches at every measurement. All outcomes happen in different branches.
- **Decoherence program:** Interaction with the environment causes interference terms to vanish practically (though not in principle). Explains why macroscopic superpositions are unobservable without invoking collapse.
- **Pilot wave (de Broglie-Bohm):** Particles have definite trajectories guided by the wave function. Deterministic but non-local.

**Current status.** All interpretations make identical experimental predictions for all known experiments. The measurement problem remains open.

## Dirac Notation Basics

**Kets and bras.** A quantum state is written as |psi> (a "ket"). The dual vector is <psi| (a "bra"). The inner product is <phi|psi> (a "bracket").

**Observables as operators.** An observable A acts on kets: A|psi> = a|psi> means |psi> is an eigenstate of A with eigenvalue a.

**Completeness:** sum over n of |n><n| = I (the identity), where {|n>} is a complete set of eigenstates. This allows expanding any state as |psi> = sum of c_n |n>, where c_n = <n|psi>.

**Why Dirac notation matters.** It abstracts away the specific representation (position, momentum, energy) and makes the linear-algebraic structure of quantum mechanics transparent. It is the standard language of graduate-level and research quantum mechanics.

## When to Use This Skill

- Any problem at atomic, molecular, or subatomic scales
- Phenomena involving quantization (energy levels, spectral lines)
- Tunneling, barrier penetration, radioactive decay rates
- Entanglement, quantum information, and quantum computing discussions
- Problems where classical physics gives wrong answers (ultraviolet catastrophe, stability of atoms, specific heats at low temperature)

## When NOT to Use This Skill

- **Macroscopic mechanics problems:** Use the classical-mechanics skill. Quantum effects are negligible for objects larger than molecules.
- **Electromagnetic waves and circuits:** Use the electromagnetism skill unless photon-level behavior is involved.
- **Relativistic quantum mechanics (Dirac equation, QFT):** This skill covers non-relativistic QM. For relativistic effects, combine with the relativity-astrophysics skill.
- **Thermal/statistical behavior of many-body quantum systems:** Use the thermodynamics skill, supplemented by this skill for quantum statistics (Bose-Einstein, Fermi-Dirac).

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Treating wave functions as physical waves | psi is a probability amplitude, not a physical displacement | Always interpret |psi|^2 as probability density |
| Confusing uncertainty with measurement error | The uncertainty principle is about the state, not the instrument | Uncertainty is intrinsic to quantum states |
| Adding probabilities instead of amplitudes | Quantum interference requires adding amplitudes first, then squaring | P = |c_1 + c_2|^2, not |c_1|^2 + |c_2|^2 |
| Assuming measurement reveals a pre-existing value | Measurement produces outcomes; the value did not necessarily exist before | Use the Born rule and state preparation language |
| Using non-relativistic QM for high-energy particles | Schrodinger equation fails when v approaches c | Use Dirac equation or QFT for relativistic particles |
| Ignoring normalization | Unnormalized wave functions give meaningless probabilities | Always verify integral of |psi|^2 = 1 |

## Cross-References

- **feynman agent:** Primary agent for quantum mechanics. Opus-class, deep problem-solving with physical intuition.
- **curie agent:** Department chair, coordinates quantum problems that touch other physics domains.
- **chandrasekhar agent:** For quantum mechanics in astrophysical contexts (stellar interiors, neutron star matter).
- **faraday agent:** Pedagogy specialist — can explain quantum concepts using analogies and thought experiments.
- **electromagnetism skill:** For the electromagnetic context of quantum phenomena (photons, radiation, atomic transitions).
- **relativity-astrophysics skill:** For relativistic quantum mechanics and the quantum aspects of cosmology.
- **experimental-methods skill:** For quantum measurement techniques and the design of quantum experiments.

## References

- Griffiths, D. J., & Schroeter, D. F. (2018). *Introduction to Quantum Mechanics*. 3rd edition. Cambridge University Press.
- Sakurai, J. J., & Napolitano, J. (2020). *Modern Quantum Mechanics*. 3rd edition. Cambridge University Press.
- Feynman, R. P., & Hibbs, A. R. (1965). *Quantum Mechanics and Path Integrals*. McGraw-Hill. (Emended edition, Dover, 2010.)
- Feynman, R. P., Leighton, R. B., & Sands, M. (1965). *The Feynman Lectures on Physics*, Vol. III. Addison-Wesley.
- Dirac, P. A. M. (1930). *The Principles of Quantum Mechanics*. Oxford University Press.
- Bell, J. S. (1964). "On the Einstein Podolsky Rosen Paradox." *Physics*, 1(3), 195-200.
- Aspect, A., Dalibard, J., & Roger, G. (1982). "Experimental realization of Einstein-Podolsky-Rosen-Bohm Gedankenexperiment." *PRL*, 49, 1804-1807.
- Einstein, A. (1905). "Uber einen die Erzeugung und Verwandlung des Lichtes betreffenden heuristischen Gesichtspunkt." *Annalen der Physik*, 17, 132-148.
