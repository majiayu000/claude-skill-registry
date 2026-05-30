---
name: atomic-structure
description: Atomic theory, periodic table organization, electron configuration, periodic trends, and isotopes/radioactivity. Covers Dalton through quantum mechanical models, electron shell filling (Aufbau, Hund, Pauli), periodic law and block structure, trend prediction (electronegativity, ionization energy, atomic radius, electron affinity), isotope notation, nuclear stability, and radioactive decay modes. Use when teaching, problem-solving, or reasoning about atomic-level chemistry.
type: skill
category: chemistry
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/chemistry/atomic-structure/SKILL.md
superseded_by: null
---
# Atomic Structure

All chemistry rests on atoms. Understanding how atoms are built — their subatomic particles, electron arrangements, and position in the periodic table — is the foundation for predicting chemical behavior. This skill covers atomic models from Dalton to quantum mechanics, electron configuration rules, periodic table organization, periodic trends, and isotopes with radioactivity.

**Agent affinity:** mendeleev (periodic/inorganic chemistry, primary), curie-m (nuclear/radiochemistry, for isotope and decay topics)

**Concept IDs:** chem-atomic-structure, chem-periodic-table-organization, chem-periodic-trends, chem-isotopes-radioactivity

## Historical Atomic Models

| # | Model | Year | Key idea | Limitation |
|---|---|---|---|---|
| 1 | Dalton | 1803 | Indivisible solid spheres | No internal structure |
| 2 | Thomson | 1897 | "Plum pudding" — electrons in positive matrix | No nucleus |
| 3 | Rutherford | 1911 | Dense positive nucleus, electrons orbit | Classical orbits radiate energy, collapse |
| 4 | Bohr | 1913 | Quantized circular orbits, energy levels | Only works for hydrogen |
| 5 | Quantum mechanical | 1926 | Probability orbitals (Schrodinger equation) | Full model — currently accepted |

Each model was displaced by experimental evidence the previous model could not explain. Rutherford's gold foil experiment demolished Thomson's model. Bohr's model explained hydrogen line spectra but failed for multi-electron atoms. The quantum mechanical model, based on the Schrodinger equation, treats electrons as probability clouds (orbitals) rather than particles on fixed paths.

## Subatomic Particles

| Particle | Symbol | Charge | Mass (amu) | Location |
|---|---|---|---|---|
| Proton | p+ | +1 | 1.0073 | Nucleus |
| Neutron | n0 | 0 | 1.0087 | Nucleus |
| Electron | e- | -1 | 0.00055 | Electron cloud |

**Atomic number (Z):** Number of protons. Defines the element. Carbon is always Z = 6.

**Mass number (A):** Protons + neutrons. Written as superscript-left: 12-C or carbon-12.

**Charge:** Protons minus electrons. Neutral atom: protons = electrons.

## Quantum Numbers and Orbitals

Each electron in an atom is described by four quantum numbers:

| Quantum number | Symbol | Values | Describes |
|---|---|---|---|
| Principal | n | 1, 2, 3, ... | Energy level (shell) |
| Angular momentum | l | 0 to n-1 | Orbital shape (s, p, d, f) |
| Magnetic | m_l | -l to +l | Orbital orientation |
| Spin | m_s | +1/2 or -1/2 | Electron spin direction |

**Orbital shapes:** s = spherical (l=0), p = dumbbell (l=1), d = cloverleaf (l=2), f = complex multi-lobed (l=3).

**Capacity per subshell:** 2(2l + 1). So s holds 2, p holds 6, d holds 10, f holds 14.

## Electron Configuration Rules

Three rules govern how electrons fill orbitals:

**1. Aufbau Principle.** Electrons fill the lowest-energy orbitals first. The filling order follows increasing (n + l), with lower n breaking ties:

1s, 2s, 2p, 3s, 3p, 4s, 3d, 4p, 5s, 4d, 5p, 6s, 4f, 5d, 6p, 7s, 5f, 6d, 7p

**2. Pauli Exclusion Principle.** No two electrons in the same atom can have all four quantum numbers identical. Each orbital holds at most 2 electrons with opposite spins.

**3. Hund's Rule.** Within a subshell of equal-energy orbitals, electrons occupy empty orbitals first (one per orbital, same spin) before pairing.

### Worked Example: Electron Configuration of Iron (Z = 26)

**Problem.** Write the full electron configuration and orbital diagram for iron.

**Solution.** Fill orbitals in Aufbau order, distributing 26 electrons:

1s^2 2s^2 2p^6 3s^2 3p^6 4s^2 3d^6

Check: 2 + 2 + 6 + 2 + 6 + 2 + 6 = 26. Correct.

**Noble gas shorthand:** [Ar] 4s^2 3d^6, where [Ar] = 1s^2 2s^2 2p^6 3s^2 3p^6 (18 electrons).

**Orbital diagram for 3d subshell (Hund's rule):**

3d: [up/down] [up/down] [up] [up] [up] — this is wrong. Let me re-count. 3d^6 means 6 electrons in 5 d orbitals. By Hund's rule, fill each of the 5 orbitals with one electron first (5 electrons, all spin-up), then the 6th pairs in the first orbital:

3d: [up/down] [up] [up] [up] [up]

Iron has 4 unpaired electrons, making it paramagnetic.

### Worked Example: Exception — Chromium (Z = 24)

**Problem.** Predict and correct the electron configuration of chromium.

**Expected by Aufbau:** [Ar] 4s^2 3d^4

**Actual:** [Ar] 4s^1 3d^5

**Why.** A half-filled d subshell (d^5) has extra stability due to exchange energy — the quantum mechanical stabilization from having all five d orbitals singly occupied with parallel spins. Chromium "steals" one electron from 4s to achieve this. Copper (Z = 29) does the same: [Ar] 4s^1 3d^10 rather than 4s^2 3d^9, preferring the fully filled d^10.

## Periodic Table Organization

**Periodic Law.** When elements are arranged by increasing atomic number, their physical and chemical properties repeat periodically. This is the single most powerful organizing principle in chemistry.

**Structure:**

| Feature | Description |
|---|---|
| Period (row) | Elements in the same period have the same highest principal quantum number n |
| Group (column) | Elements in the same group have the same valence electron configuration pattern |
| s-block | Groups 1-2 + He: filling s orbitals |
| p-block | Groups 13-18: filling p orbitals |
| d-block | Groups 3-12: filling d orbitals (transition metals) |
| f-block | Lanthanides + actinides: filling f orbitals (inner transition metals) |

**Group names worth knowing:** Group 1 = alkali metals, Group 2 = alkaline earth metals, Group 17 = halogens, Group 18 = noble gases.

**Metals, nonmetals, metalloids.** Metals dominate the left and center (lose electrons, conduct). Nonmetals cluster in the upper right (gain electrons, insulate). Metalloids straddle the staircase line (B, Si, Ge, As, Sb, Te) — semiconducting properties.

## Periodic Trends

Five trends follow directly from nuclear charge and electron shielding:

### Trend 1 — Atomic Radius

**Across a period (left to right):** Decreases. More protons pull the same-shell electrons inward.

**Down a group:** Increases. Each period adds a new shell farther from the nucleus.

**Worked example.** *Rank Na, Mg, K in order of increasing atomic radius.*

Na and Mg are in period 3; K is in period 4. Down group 1: K > Na. Across period 3: Na > Mg (more protons, same shell). Order: Mg < Na < K.

### Trend 2 — Ionization Energy (IE)

**Definition.** Energy required to remove the highest-energy electron from a gaseous atom. Always positive (endothermic).

**Across a period:** Increases (electrons held more tightly as Z_eff grows).

**Down a group:** Decreases (valence electrons farther from nucleus, more shielding).

**Worked example.** *Why is the first ionization energy of oxygen (1314 kJ/mol) lower than that of nitrogen (1402 kJ/mol), despite oxygen being further right?*

Nitrogen has a half-filled 2p^3 configuration (exchange energy stabilization). Oxygen's 2p^4 has one paired electron — electron-electron repulsion in the paired orbital makes that electron easier to remove. This is the classic "dip" in the IE trend at Group 16.

### Trend 3 — Electronegativity

**Definition.** Tendency of an atom in a bond to attract shared electrons. Pauling scale: F = 4.0 (highest), Cs = 0.79 (lowest of main group).

**Across a period:** Increases. **Down a group:** Decreases.

**Practical consequence.** Electronegativity differences predict bond type: less than 0.4 = nonpolar covalent, 0.4 to 1.7 = polar covalent, greater than 1.7 = ionic (approximate guidelines).

### Trend 4 — Electron Affinity

**Definition.** Energy change when a gaseous atom gains an electron. More negative = more favorable.

**General trend.** Becomes more negative (more exothermic) moving right across a period and up a group. Halogens have the most negative electron affinities. Noble gases have near-zero or positive (unfavorable) electron affinities — their shells are already full.

### Trend 5 — Metallic Character

**Across a period:** Decreases. **Down a group:** Increases.

This mirrors electronegativity inverted — the most metallic elements are in the lower left (Cs, Fr), the least metallic in the upper right (F, O, N).

### Summary Table

| Trend | Across period (L to R) | Down group |
|---|---|---|
| Atomic radius | Decreases | Increases |
| Ionization energy | Increases (with dips at Groups 3, 16) | Decreases |
| Electronegativity | Increases | Decreases |
| Electron affinity | More negative (generally) | Less negative |
| Metallic character | Decreases | Increases |

## Effective Nuclear Charge

**Z_eff = Z - S**, where Z is the atomic number and S is the shielding constant (estimated by Slater's rules). Z_eff is the net positive charge "felt" by a valence electron after inner electrons partially cancel the nuclear pull.

**Worked example.** *Estimate Z_eff for a 3s electron in sodium (Z = 11).*

Using Slater's rules: the 10 inner electrons (1s^2 2s^2 2p^6) shield approximately 0.85 each from 2s/2p and 1.00 each from 1s. For the 3s electron: S = (8 x 0.85) + (2 x 1.00) = 8.80. Z_eff = 11 - 8.80 = 2.20.

This explains why sodium's valence electron is easy to remove — it experiences a net pull of only about +2.2 from a nucleus with 11 protons.

## Isotopes and Radioactivity

**Isotopes** are atoms of the same element (same Z) with different numbers of neutrons (different A). Chemical properties are nearly identical (same electron configuration), but nuclear stability varies.

### Notation

Carbon-12: 12/6-C (mass number 12, atomic number 6, 6 neutrons)
Carbon-14: 14/6-C (mass number 14, atomic number 6, 8 neutrons)

**Atomic mass** on the periodic table is the weighted average of naturally occurring isotopes.

**Worked example.** *Chlorine has two stable isotopes: Cl-35 (75.77%, mass 34.969 amu) and Cl-37 (24.23%, mass 36.966 amu). Calculate the atomic mass.*

Atomic mass = (0.7577)(34.969) + (0.2423)(36.966) = 26.50 + 8.96 = 35.45 amu. This matches the periodic table value.

### Nuclear Stability

**Band of stability.** Plotting neutron number (N) vs. proton number (Z) reveals a belt where stable nuclei cluster. Light stable nuclei have N/Z near 1.0; heavy stable nuclei drift toward N/Z near 1.5. Nuclei outside this band are radioactive.

**Magic numbers.** Nuclei with 2, 8, 20, 28, 50, 82, or 126 protons or neutrons are exceptionally stable (analogous to noble gas electron configurations). Doubly magic: He-4 (2p, 2n), O-16 (8p, 8n), Ca-40 (20p, 20n), Pb-208 (82p, 126n).

### Radioactive Decay Modes

| Mode | Symbol | Particle emitted | Change in Z | Change in A |
|---|---|---|---|---|
| Alpha | alpha | He-4 nucleus (2p + 2n) | -2 | -4 |
| Beta-minus | beta- | Electron + antineutrino | +1 | 0 |
| Beta-plus | beta+ | Positron + neutrino | -1 | 0 |
| Gamma | gamma | High-energy photon | 0 | 0 |
| Electron capture | EC | Inner electron absorbed | -1 | 0 |

**Worked example.** *Uranium-238 undergoes alpha decay. Write the nuclear equation.*

238/92-U -> 234/90-Th + 4/2-He

Check: 238 = 234 + 4 (mass numbers balance). 92 = 90 + 2 (atomic numbers balance). The product is thorium-234.

### Half-Life

**Definition.** Time for half of a radioactive sample to decay. After n half-lives, the fraction remaining is (1/2)^n.

**Worked example.** *Iodine-131 has a half-life of 8.02 days. A patient receives 100 mg. How much remains after 24.06 days?*

Number of half-lives: 24.06 / 8.02 = 3.0. Remaining: 100 x (1/2)^3 = 100 x 1/8 = 12.5 mg.

**Carbon-14 dating.** C-14 has a half-life of 5,730 years. Living organisms maintain a constant C-14/C-12 ratio through respiration. At death, C-14 decays without replenishment. Measuring the remaining C-14 fraction gives the time since death. Effective range: up to about 50,000 years.

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Confusing atomic number and mass number | Z = protons only; A = protons + neutrons | Z defines the element; A identifies the isotope |
| Ignoring Hund's rule | Pairing electrons before filling empty orbitals violates exchange energy minimization | Fill each orbital in a subshell with one electron first |
| Forgetting Aufbau exceptions | Cr and Cu configurations are exam staples | Memorize half-filled (d^5) and fully filled (d^10) exceptions |
| Reversing trend directions | Radius and IE trend oppositely | Atomic radius decreases left-to-right; IE increases left-to-right |
| Confusing isotopes and ions | Isotopes differ in neutrons; ions differ in electrons | An isotope changes A; an ion changes charge |
| Using integer mass for calculations | Atomic mass is a weighted average of isotopes | Use the decimal value from the periodic table |

## Cross-References

- **mendeleev agent:** Periodic table organization, inorganic chemistry, trend prediction. Primary agent for this skill.
- **curie-m agent:** Nuclear chemistry, radioactive decay, isotope applications. Activated for decay and dating problems.
- **chemical-bonding skill:** Electron configurations determine bonding behavior — ionic vs. covalent depends on electronegativity and IE.
- **reactions-stoichiometry skill:** Atomic mass and isotope concepts feed directly into molar mass and stoichiometric calculations.
- **analytical-methods skill:** Mass spectrometry uses isotope patterns for elemental identification.

## References

- Zumdahl, S. S. & Zumdahl, S. A. (2017). *Chemistry*. 10th edition. Cengage Learning.
- Atkins, P. & de Paula, J. (2014). *Atkins' Physical Chemistry*. 10th edition. Oxford University Press.
- IUPAC. (2021). Periodic Table of the Elements. International Union of Pure and Applied Chemistry.
- National Nuclear Data Center. *NuDat 3.0*. Brookhaven National Laboratory. (Interactive nuclear data.)
- Slater, J. C. (1930). "Atomic Shielding Constants." *Physical Review*, 36(1), 57-64.
- Moseley, H. G. J. (1913). "The High-Frequency Spectra of the Elements." *Philosophical Magazine*, 26(156), 1024-1034.
