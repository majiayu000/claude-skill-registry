---
name: mfe-reality
description: "Physical applications of mathematics. Constants, quantum mechanics, measurement — where abstract meets embodied."
user-invocable: false
allowed-tools: Read Grep Glob
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-26"
      triggers:
        intents:
          - "physics"
          - "constant"
          - "quantum"
          - "particle"
          - "energy"
          - "momentum"
          - "wave function"
          - "measurement"
          - "uncertainty"
        contexts:
          - "mathematical problem solving"
          - "math reasoning"
---

# Reality

## Summary

**Reality** (Part V: Grounding)
Chapters: 15, 16, 17
Plane Position: (0.3, -0.4) radius 0.35
Primitives: 44

Physical applications of mathematics. Constants, quantum mechanics, measurement — where abstract meets embodied.

**Key Concepts:** Quantum Operators (Observables), Planck's Constant, Wave Function, Dimensional Analysis, Atomic Number and Mass

## Key Primitives



**Quantum Operators (Observables)** (definition): Observables in quantum mechanics are represented by Hermitian (self-adjoint) operators on Hilbert space. Position: X_hat psi = x*psi. Momentum: P_hat psi = -i*hbar*d/dx psi. The eigenvalues of an observable are the possible measurement outcomes.
  - Represent a physical measurement mathematically
  - Find the possible outcomes of a quantum measurement
  - Determine whether two observables can be measured simultaneously

**Planck's Constant** (axiom): Planck's constant h = 6.62607015 x 10^{-34} J*s (exact, SI definition). The reduced Planck constant hbar = h/(2*pi). It is the quantum of action, setting the scale where quantum effects become significant.
  - Determine the scale at which quantum effects matter
  - Compute photon energy from frequency
  - Calculate the de Broglie wavelength of a particle

**Wave Function** (definition): The wave function psi(x,t) is a complex-valued function that completely describes the quantum state of a system. The probability of finding the particle between x and x+dx is |psi(x,t)|^2 dx. The wave function must be normalized: integral |psi|^2 dx = 1.
  - Describe the state of a quantum particle
  - Compute probabilities of measurement outcomes
  - Determine the time evolution of a quantum system

**Dimensional Analysis** (technique): Every physical equation must be dimensionally consistent: both sides must have the same dimensions in terms of fundamental quantities (length L, mass M, time T, charge Q, temperature Theta). A quantity Q has dimensions [Q] = L^a M^b T^c Q^d Theta^e.
  - Check if a physics equation is dimensionally consistent
  - Derive the functional form of a physical relationship from dimensional constraints
  - Determine which variables a physical quantity can depend on

**Atomic Number and Mass** (definition): The atomic number Z is the number of protons in an atom's nucleus, uniquely identifying the element. The mass number A = Z + N where N is the number of neutrons. Atomic mass is measured in unified atomic mass units (u ≈ 1.661 x 10^{-27} kg).
  - Identify an element from its number of protons
  - Determine the number of electrons in a neutral atom
  - Calculate atomic mass from isotope data

**Quantum Numbers** (definition): Each electron in an atom is described by four quantum numbers: principal n (1,2,3,...), angular momentum l (0,...,n-1), magnetic m_l (-l,...,+l), and spin m_s (+1/2 or -1/2). No two electrons can share all four quantum numbers (Pauli exclusion).
  - Describe the state of an electron in an atom
  - Determine the number of electrons in each shell and subshell
  - Predict orbital shapes and orientations

**Electron Configuration (Aufbau Principle)** (algorithm): The Aufbau principle states that electrons fill orbitals in order of increasing energy: 1s, 2s, 2p, 3s, 3p, 4s, 3d, 4p, 5s, 4d, ... The filling order follows the (n+l) rule: lower n+l fills first; for equal n+l, lower n fills first.
  - Determine the electron configuration of an element
  - Predict chemical properties from electron arrangement
  - Understand the structure of the periodic table

**Speed of Light** (axiom): The speed of light in vacuum is a universal constant: c = 299,792,458 m/s exactly. It is the maximum speed for information transfer and the conversion factor between space and time: E = mc^2.
  - Convert between mass and energy
  - Compute relativistic effects at high velocities
  - Set the scale for electromagnetic phenomena

**Elementary Charge** (axiom): The elementary charge e = 1.602176634 x 10^{-19} C (exact, SI definition) is the magnitude of the charge of the electron and proton. It is the fundamental quantum of electric charge.
  - Compute electromagnetic forces between charged particles
  - Convert between energy in joules and electron-volts
  - Quantize charge in atomic and molecular systems

**Physical Quantity** (axiom): A physical quantity Q is the product of a numerical value {Q} and a unit [Q]: Q = {Q} x [Q]. The numerical value depends on the choice of unit, but the physical quantity is invariant. Examples: length l = 5 m, energy E = 3.2 eV.
  - Represent a measurable physical quantity with units
  - Convert between different unit systems
  - Ensure calculations preserve physical meaning

## Composition Patterns

- Dimensional Analysis + reality-buckingham-pi -> Systematic derivation of dimensionless groups governing a physical system (sequential)
- Buckingham Pi Theorem + reality-dimensional-analysis -> Complete dimensional reduction of any physical problem to dimensionless form (sequential)
- Speed of Light + reality-plancks-constant -> Photon energy: E = hc/lambda, linking quantum and electromagnetic scales (sequential)
- Planck's Constant + reality-speed-of-light -> Natural unit system where hbar = c = 1 (parallel)
- Gravitational Constant + reality-speed-of-light -> Schwarzschild radius: r_s = 2GM/c^2, boundary of a black hole (sequential)
- Boltzmann Constant + reality-plancks-constant -> Planck distribution: n(omega) = 1/(exp(hbar*omega/(k_B*T)) - 1), quantum statistics (sequential)
- Elementary Charge + reality-plancks-constant -> Fine structure constant: alpha = e^2/(4*pi*epsilon_0*hbar*c) ≈ 1/137, strength of electromagnetic interaction (sequential)
- Fine Structure Constant + reality-quantum-numbers -> Hydrogen energy levels: E_n = -13.6 eV / n^2, with fine structure corrections of order alpha^2 (sequential)
- Natural Units (Planck Units) + reality-gravitational-constant -> Planck scales: the natural units of quantum gravity where l_P, m_P, t_P emerge (parallel)
- Dimensional Homogeneity + reality-dimensional-analysis -> Error detection: identify physically impossible equations before computing (parallel)

## Cross-Domain Links

- **structure**: Compatible domain for composition and cross-referencing
- **waves**: Compatible domain for composition and cross-referencing
- **foundations**: Compatible domain for composition and cross-referencing
- **synthesis**: Compatible domain for composition and cross-referencing

## Activation Patterns

- physics
- constant
- quantum
- particle
- energy
- momentum
- wave function
- measurement
- uncertainty
