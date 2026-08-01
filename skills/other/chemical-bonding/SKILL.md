---
name: chemical-bonding
description: Ionic, covalent, and metallic bonding, Lewis structures, VSEPR theory, molecular geometry, polarity, and intermolecular forces. Covers octet rule and exceptions, formal charge, resonance, sigma/pi bonds, orbital hybridization, electronegativity-driven bond classification, VSEPR electron-domain and molecular geometries, dipole moments, and the four intermolecular force types (London dispersion, dipole-dipole, hydrogen bonding, ion-dipole). Use when predicting molecular shapes, bond properties, or physical behavior from molecular structure.
type: skill
category: chemistry
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/chemistry/chemical-bonding/SKILL.md
superseded_by: null
---
# Chemical Bonding

Atoms bond to achieve lower energy states. The type of bond — ionic, covalent, or metallic — depends on the electronegativity difference and metallic character of the atoms involved. Once bonds form, the three-dimensional arrangement of atoms determines molecular shape, polarity, and physical properties. This skill covers bond formation, Lewis structures, VSEPR geometry prediction, hybridization, and the intermolecular forces that govern bulk behavior.

**Agent affinity:** pauling (bonding/molecular chemistry, primary)

**Concept IDs:** chem-ionic-bonding, chem-covalent-bonding, chem-molecular-geometry, chem-intermolecular-forces

## Bond Type Classification

| Bond type | Electronegativity difference | Electron behavior | Example |
|---|---|---|---|
| Nonpolar covalent | < 0.4 | Shared equally | H-H, Cl-Cl |
| Polar covalent | 0.4 - 1.7 | Shared unequally | H-Cl, O-H |
| Ionic | > 1.7 | Transferred | NaCl, MgO |
| Metallic | Between metals | Delocalized "sea" | Fe, Cu, Al |

These boundaries are guidelines, not sharp cutoffs. Bond character exists on a continuum.

## Ionic Bonding

**Mechanism.** Metal atoms lose electrons to form cations; nonmetal atoms gain electrons to form anions. The electrostatic attraction between oppositely charged ions forms the ionic bond.

**Lattice energy.** The energy released when gaseous ions assemble into a crystal lattice. Higher lattice energy means a more stable compound. Lattice energy increases with higher ion charges and smaller ion radii (Coulomb's law: E proportional to q1*q2/r).

**Worked example.** *Predict the formula of the compound formed by aluminum and oxygen.*

Aluminum (Group 3) loses 3 electrons: Al^3+. Oxygen (Group 16) gains 2 electrons: O^2-. To balance charges: 2(Al^3+) + 3(O^2-) gives total charge = 2(+3) + 3(-2) = 0. Formula: Al2O3.

**Properties of ionic compounds.** High melting points, brittle, conduct electricity when molten or dissolved (ions free to move), do not conduct as solids (ions locked in lattice).

## Covalent Bonding

**Mechanism.** Nonmetal atoms share electron pairs to achieve stable electron configurations. A single bond shares 2 electrons, a double bond shares 4, a triple bond shares 6.

**Bond order, length, and energy relationship:**

| Bond | Bond order | Approximate length (pm) | Approximate energy (kJ/mol) |
|---|---|---|---|
| C-C | 1 | 154 | 347 |
| C=C | 2 | 134 | 614 |
| C-triple-C | 3 | 120 | 839 |

Higher bond order means shorter, stronger bonds. This pattern holds across all elements.

## Lewis Structures

Lewis structures show valence electrons as dots or lines (bonding pairs). The systematic procedure:

**Step 1.** Count total valence electrons. Add electrons for negative charges; subtract for positive charges.

**Step 2.** Connect atoms with single bonds. The least electronegative atom is usually central (H is always terminal).

**Step 3.** Distribute remaining electrons as lone pairs, completing octets on terminal atoms first, then the central atom.

**Step 4.** If the central atom lacks an octet, convert lone pairs on adjacent atoms to multiple bonds.

**Step 5.** Calculate formal charges: FC = (valence electrons) - (lone pair electrons) - (1/2 bonding electrons). Minimize formal charges; negative FC should be on more electronegative atoms.

### Worked Example: Lewis Structure of CO2

**Step 1.** C has 4, each O has 6. Total: 4 + 6 + 6 = 16 valence electrons.

**Step 2.** O-C-O uses 4 electrons for two single bonds. Remaining: 12.

**Step 3.** Place 6 electrons (3 lone pairs) on each O: 12 used. Carbon has only 4 electrons around it — incomplete octet.

**Step 4.** Convert one lone pair from each O into a bonding pair: O=C=O. Carbon now has 8 electrons (two double bonds). Each O has 4 lone pair electrons + 4 bonding electrons = 8. All octets satisfied.

**Step 5.** Formal charges: C = 4 - 0 - 4 = 0. Each O = 6 - 4 - 2 = 0. All zero — optimal.

### Worked Example: Lewis Structure of NO3- (Nitrate)

**Step 1.** N has 5, each O has 6, plus 1 for the negative charge. Total: 5 + 18 + 1 = 24.

**Step 2.** Three N-O single bonds use 6 electrons. Remaining: 18.

**Step 3.** Place 6 electrons on each O (18 total). N has only 6 electrons — needs 2 more.

**Step 4.** Convert one lone pair from one O to a double bond. N=O with two N-O. N now has 8 electrons.

**Step 5.** Formal charges: N = 5 - 0 - 4 = +1. Double-bonded O = 6 - 4 - 2 = 0. Each single-bonded O = 6 - 6 - 1 = -1. Total: +1 + 0 + (-1) + (-1) = -1. Correct.

**Resonance.** The double bond could be on any of the three O atoms. Three equivalent resonance structures exist. The true structure is a hybrid — each N-O bond has bond order 4/3.

## Octet Rule Exceptions

| Exception type | Example | Explanation |
|---|---|---|
| Incomplete octet | BF3 (B has 6 e-) | Boron is electron-deficient; stable with 6 |
| Expanded octet | SF6 (S has 12 e-) | Period 3+ elements use d orbitals |
| Odd electron | NO (11 e- total) | Free radical — unpaired electron on N |

**Critical rule.** Only elements in period 3 or below can exceed the octet. Never draw expanded octets for C, N, O, or F.

## VSEPR Theory

Valence Shell Electron Pair Repulsion: electron domains (bonding pairs and lone pairs) around a central atom arrange themselves to maximize separation, determining molecular geometry.

### Electron Domain Count to Geometry

| Electron domains | Electron geometry | Bond angle(s) |
|---|---|---|
| 2 | Linear | 180 deg |
| 3 | Trigonal planar | 120 deg |
| 4 | Tetrahedral | 109.5 deg |
| 5 | Trigonal bipyramidal | 90 deg, 120 deg |
| 6 | Octahedral | 90 deg |

**Key distinction.** Electron geometry counts ALL domains (bonding + lone pairs). Molecular geometry describes only the atom positions. Lone pairs are "invisible" in molecular geometry but still affect shape.

### VSEPR Decision Table

| Electron domains | Bonding pairs | Lone pairs | Molecular geometry | Example |
|---|---|---|---|---|
| 2 | 2 | 0 | Linear | CO2, BeCl2 |
| 3 | 3 | 0 | Trigonal planar | BF3 |
| 3 | 2 | 1 | Bent | SO2, O3 |
| 4 | 4 | 0 | Tetrahedral | CH4 |
| 4 | 3 | 1 | Trigonal pyramidal | NH3 |
| 4 | 2 | 2 | Bent | H2O |
| 5 | 5 | 0 | Trigonal bipyramidal | PCl5 |
| 5 | 4 | 1 | Seesaw | SF4 |
| 5 | 3 | 2 | T-shaped | ClF3 |
| 5 | 2 | 3 | Linear | XeF2 |
| 6 | 6 | 0 | Octahedral | SF6 |
| 6 | 5 | 1 | Square pyramidal | BrF5 |
| 6 | 4 | 2 | Square planar | XeF4 |

### Worked Example: Molecular Geometry of Water (H2O)

**Step 1.** Lewis structure: O has 2 bonding pairs (to H) and 2 lone pairs. Total electron domains = 4.

**Step 2.** Electron geometry: tetrahedral (4 domains).

**Step 3.** Molecular geometry: bent (2 bonding pairs visible, 2 lone pairs hidden).

**Step 4.** Bond angle: approximately 104.5 deg (compressed from ideal 109.5 deg because lone pairs occupy more space than bonding pairs).

### Worked Example: Molecular Geometry of XeF4

**Step 1.** Xe has 8 valence electrons, 4 F atoms contribute 4 bonds (8 electrons), leaving 2 lone pairs on Xe. Total electron domains = 6.

**Step 2.** Electron geometry: octahedral.

**Step 3.** Molecular geometry: square planar (lone pairs occupy opposing axial positions to minimize repulsion).

**Step 4.** Bond angles: 90 deg. The molecule is flat and symmetric.

## Hybridization

Orbital hybridization explains observed geometries by mixing atomic orbitals:

| Hybrid | Orbitals mixed | Geometry | Angle | Example |
|---|---|---|---|---|
| sp | 1s + 1p | Linear | 180 deg | BeCl2, CO2 (C) |
| sp2 | 1s + 2p | Trigonal planar | 120 deg | BF3, C2H4 (each C) |
| sp3 | 1s + 3p | Tetrahedral | 109.5 deg | CH4, NH3, H2O |
| sp3d | 1s + 3p + 1d | Trigonal bipyramidal | 90/120 deg | PCl5 |
| sp3d2 | 1s + 3p + 2d | Octahedral | 90 deg | SF6 |

**Shortcut.** The number of hybrid orbitals equals the number of electron domains. 4 domains = sp3. 3 domains = sp2. 2 domains = sp.

**Sigma and pi bonds.** A single bond = 1 sigma bond. A double bond = 1 sigma + 1 pi. A triple bond = 1 sigma + 2 pi. Sigma bonds form from head-on orbital overlap; pi bonds form from side-by-side p orbital overlap.

**Worked example.** *Determine the hybridization of each carbon in CH3CHO (acetaldehyde).*

The CH3 carbon has 4 electron domains (3 C-H bonds + 1 C-C bond) = sp3 hybridized, tetrahedral.

The CHO carbon has 3 electron domains (1 C-H bond + 1 C-C bond + 1 C=O double bond; the double bond counts as 1 domain) = sp2 hybridized, trigonal planar.

## Molecular Polarity

A molecule is polar if (1) it contains polar bonds AND (2) the bond dipoles do not cancel by symmetry.

**Worked example.** *Is CO2 polar?*

Each C=O bond is polar (electronegativity difference = 1.0). But CO2 is linear with identical bonds pointing in opposite directions. The dipoles cancel. CO2 is nonpolar.

**Worked example.** *Is H2O polar?*

Each O-H bond is polar. H2O is bent (104.5 deg), so the dipoles do not cancel. The net dipole points from the H atoms toward the O atom. H2O is polar (dipole moment = 1.85 D).

**Symmetry test.** Molecules with identical surrounding atoms and no lone pairs on the central atom (CO2, BF3, CH4, SF6, XeF4) are typically nonpolar even with polar bonds. Lone pairs on the central atom usually break symmetry and create polarity (NH3, H2O, SO2).

## Intermolecular Forces

Intermolecular forces (IMFs) act between molecules. They are much weaker than intramolecular bonds but determine physical properties: boiling point, melting point, viscosity, surface tension, and solubility.

### The Four Types (Weakest to Strongest)

**1. London Dispersion Forces (LDF).** Present in ALL molecules. Arise from instantaneous dipoles created by electron motion. Strength increases with molar mass and surface area (more electrons = more polarizable). These are the ONLY forces in nonpolar molecules (He, N2, CH4).

**2. Dipole-Dipole Forces.** Between polar molecules. The positive end of one molecule attracts the negative end of another. Strength increases with dipole moment.

**3. Hydrogen Bonding.** Special strong case of dipole-dipole. Requires H bonded to F, O, or N (the three most electronegative small atoms) interacting with a lone pair on F, O, or N of a neighboring molecule. Approximately 5-30 kJ/mol — about 10x a typical dipole-dipole interaction.

**4. Ion-Dipole Forces.** Between ions and polar molecules. Strongest IMF type. Responsible for the dissolution of ionic compounds in water (hydration of ions).

### Worked Example: Ranking Boiling Points

**Problem.** Rank the following by increasing boiling point: CH4, CH3OH, CH3CH3, CH3Cl.

**Analysis.**

- CH4 (16 g/mol): Nonpolar. Only LDF. Lowest BP.
- CH3CH3 (30 g/mol): Nonpolar. Only LDF. Slightly higher than CH4 (more electrons).
- CH3Cl (50.5 g/mol): Polar. LDF + dipole-dipole. Higher than CH3CH3.
- CH3OH (32 g/mol): Polar with O-H bond. LDF + dipole-dipole + hydrogen bonding. Highest BP despite lower molar mass than CH3Cl.

**Order:** CH4 (-161 C) < CH3CH3 (-89 C) < CH3Cl (-24 C) < CH3OH (65 C).

The hydrogen bonding in methanol overcomes its lower molar mass — this is the signature anomaly of H-bonding.

### Worked Example: Why Ice Floats

Water's hydrogen bonding network forces molecules into an open hexagonal lattice when frozen. This lattice has more space between molecules than liquid water, making ice less dense than liquid water (0.917 g/mL vs. 1.000 g/mL). This is anomalous — most solids are denser than their liquids. The ecological consequence is enormous: ice floats, insulating bodies of water from above and allowing aquatic life to survive winter.

## Metallic Bonding

**Electron sea model.** Metal atoms release valence electrons into a delocalized "sea" shared by all atoms in the lattice. The positive metal ion cores sit in this sea.

**Properties explained:** Electrical conductivity (electrons flow freely), thermal conductivity (electrons transfer kinetic energy), malleability/ductility (layers slide without breaking bonds — the electron sea reforms around shifted atoms), luster (free electrons absorb and re-emit photons).

**Band theory.** A more complete model — overlapping atomic orbitals form continuous energy bands. Metals have partially filled bands allowing electron mobility. Insulators have a large band gap. Semiconductors have a small band gap bridgeable by thermal energy or doping.

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Expanded octets for period 2 | C, N, O, F have no accessible d orbitals | Only period 3+ elements can exceed 8 |
| Confusing electron geometry with molecular geometry | Lone pairs affect shape but are "invisible" | Count ALL domains for electron geometry; show only atoms for molecular |
| Forgetting lone pairs in VSEPR count | Undercounting domains gives wrong geometry | Always draw the Lewis structure first |
| Calling CO2 polar | Symmetric cancellation of dipoles | Linear + identical bonds = nonpolar |
| Hydrogen bond to any H | H-bonding requires H-F, H-O, or H-N | H-C bonds do NOT form hydrogen bonds |
| Ignoring LDF for polar molecules | Polar molecules still have LDF too | LDF is always present; other forces add on top |

## Cross-References

- **pauling agent:** Bonding analysis, molecular geometry, hybridization. Primary agent for this skill.
- **atomic-structure skill:** Electron configurations determine bonding capacity and electronegativity.
- **reactions-stoichiometry skill:** Bond energies feed into enthalpy calculations (Hess's law via bond energies).
- **organic-chemistry skill:** Carbon bonding, hybridization, and functional groups build directly on covalent bonding concepts.
- **materials-chemistry skill:** Intermolecular forces determine phase behavior and material properties.

## References

- Pauling, L. (1960). *The Nature of the Chemical Bond*. 3rd edition. Cornell University Press.
- Gillespie, R. J. & Hargittai, I. (2012). *The VSEPR Model of Molecular Geometry*. Dover Publications.
- Zumdahl, S. S. & Zumdahl, S. A. (2017). *Chemistry*. 10th edition. Cengage Learning.
- Atkins, P. & de Paula, J. (2014). *Atkins' Physical Chemistry*. 10th edition. Oxford University Press.
- Lewis, G. N. (1916). "The Atom and the Molecule." *Journal of the American Chemical Society*, 38(4), 762-785.
- Pauling, L. (1931). "The Nature of the Chemical Bond." *Journal of the American Chemical Society*, 53(4), 1367-1400.
