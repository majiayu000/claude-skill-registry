---
name: reactions-stoichiometry
description: Balancing chemical equations, reaction classification, stoichiometric calculations, acid-base chemistry, oxidation-reduction (redox) reactions, and thermochemistry. Covers conservation of mass, mole ratios, limiting reagents, percent yield, Bronsted-Lowry and Lewis acid-base theory, pH calculations, oxidation states, half-reaction balancing, enthalpy, Hess's law, and calorimetry. Use when solving quantitative chemistry problems involving reactions, energy changes, or solution chemistry.
type: skill
category: chemistry
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/chemistry/reactions-stoichiometry/SKILL.md
superseded_by: null
---
# Reactions and Stoichiometry

Chemical reactions transform substances by breaking and forming bonds. Stoichiometry is the quantitative bookkeeping — tracking atoms, moles, and energy through these transformations. This skill covers equation balancing, reaction classification, mole-based calculations, acid-base chemistry, redox reactions, and thermochemistry.

**Agent affinity:** lavoisier (chair, reactions and conservation of mass, primary)

**Concept IDs:** chem-balancing-equations, chem-reaction-types, chem-acids-bases, chem-oxidation-reduction, chem-thermochemistry

## Conservation of Mass and Balancing Equations

**Lavoisier's Law.** In a chemical reaction, matter is neither created nor destroyed. Every atom present in the reactants must appear in the products.

**Balancing procedure:**

1. Write the unbalanced equation with correct formulas.
2. Balance one element at a time, starting with the most complex molecule.
3. Balance hydrogen and oxygen last (they appear in many compounds).
4. Use the smallest whole-number coefficients.
5. Verify: count every element on both sides.

### Worked Example: Combustion of Propane

**Unbalanced:** C3H8 + O2 -> CO2 + H2O

**Step 1.** Balance C: 3 carbons on left, so 3 CO2 on right.
C3H8 + O2 -> 3 CO2 + H2O

**Step 2.** Balance H: 8 hydrogens on left, so 4 H2O on right.
C3H8 + O2 -> 3 CO2 + 4 H2O

**Step 3.** Balance O: Right side has 3(2) + 4(1) = 10 oxygens. Left needs 10/2 = 5 O2.
C3H8 + 5 O2 -> 3 CO2 + 4 H2O

**Verify:** C: 3 = 3. H: 8 = 8. O: 10 = 10. Balanced.

### Worked Example: Balancing a More Complex Equation

**Unbalanced:** Fe2O3 + CO -> Fe + CO2

**Step 1.** Balance Fe: 2 Fe on left, so 2 Fe on right.
Fe2O3 + CO -> 2 Fe + CO2

**Step 2.** Balance O: Left has 3 (from Fe2O3) + 1 (from CO) = 4 if 1 CO. Right has 2 from CO2. Try: 3 CO on left gives 3 + 3 = 6 oxygens total on left... Systematic approach: Fe2O3 + 3 CO -> 2 Fe + 3 CO2.

**Verify:** Fe: 2 = 2. O: 3 + 3 = 6, 3(2) = 6. C: 3 = 3. Balanced.

## The Mole Concept

**Avogadro's number:** 6.022 x 10^23 particles per mole. One mole of any element has a mass in grams equal to its atomic mass in amu.

**Molar mass.** Sum of atomic masses of all atoms in a formula. H2O: 2(1.008) + 16.00 = 18.02 g/mol.

**Three conversions every chemist uses:**

- Grams to moles: n = mass / molar mass
- Moles to particles: N = n x 6.022 x 10^23
- Moles to volume (gas at STP): V = n x 22.4 L

## Stoichiometric Calculations

Stoichiometry uses balanced equations as conversion factors. The coefficients give mole ratios.

### Worked Example: Mass-to-Mass Calculation

**Problem.** How many grams of CO2 are produced by burning 44.1 g of propane (C3H8)?

**Balanced equation:** C3H8 + 5 O2 -> 3 CO2 + 4 H2O

**Step 1.** Moles of propane: 44.1 g / 44.10 g/mol = 1.000 mol C3H8.

**Step 2.** Mole ratio: 1 mol C3H8 produces 3 mol CO2.
Moles CO2 = 1.000 x 3 = 3.000 mol.

**Step 3.** Mass of CO2: 3.000 mol x 44.01 g/mol = 132.0 g CO2.

### Limiting Reagent and Percent Yield

**Limiting reagent.** The reactant that runs out first, determining the maximum product. The other reactant(s) are in excess.

**Worked example.** *10.0 g of hydrogen reacts with 10.0 g of oxygen to form water. Which is limiting?*

2 H2 + O2 -> 2 H2O

Moles H2: 10.0 / 2.016 = 4.96 mol. Moles O2: 10.0 / 32.00 = 0.3125 mol.

From stoichiometry: 4.96 mol H2 requires 4.96/2 = 2.48 mol O2. We only have 0.3125 mol O2. Oxygen is limiting.

Moles H2O produced: 0.3125 mol O2 x (2 mol H2O / 1 mol O2) = 0.625 mol H2O.

Mass H2O: 0.625 x 18.02 = 11.3 g.

**Percent yield** = (actual yield / theoretical yield) x 100%. If the experiment produced 10.5 g: (10.5 / 11.3) x 100% = 92.9%.

## Reaction Types

### The Five Classical Types

| Type | Pattern | Example |
|---|---|---|
| Synthesis (combination) | A + B -> AB | 2 Na + Cl2 -> 2 NaCl |
| Decomposition | AB -> A + B | 2 HgO -> 2 Hg + O2 |
| Single replacement | A + BC -> AC + B | Zn + CuSO4 -> ZnSO4 + Cu |
| Double replacement (metathesis) | AB + CD -> AD + CB | AgNO3 + NaCl -> AgCl + NaNO3 |
| Combustion | CxHy + O2 -> CO2 + H2O | CH4 + 2 O2 -> CO2 + 2 H2O |

**Activity series for single replacement.** A metal replaces another in solution only if it is more active (higher on the activity series). Li > K > Ba > Ca > Na > Mg > Al > Zn > Fe > Ni > Sn > Pb > H > Cu > Ag > Pt > Au. Zinc replaces copper; copper does not replace zinc.

### Precipitation Reactions

A double replacement reaction where an insoluble product (precipitate) forms. Use solubility rules:

**Soluble:** All Na+, K+, NH4+ salts. All nitrates. Most chlorides (except AgCl, PbCl2).

**Insoluble:** Most carbonates, phosphates, sulfides (except Group 1 and NH4+).

**Worked example.** *Write the net ionic equation for mixing AgNO3(aq) and NaCl(aq).*

Full molecular: AgNO3(aq) + NaCl(aq) -> AgCl(s) + NaNO3(aq)

Full ionic: Ag+(aq) + NO3-(aq) + Na+(aq) + Cl-(aq) -> AgCl(s) + Na+(aq) + NO3-(aq)

Net ionic (cancel spectators Na+ and NO3-): Ag+(aq) + Cl-(aq) -> AgCl(s)

The net ionic equation captures the chemistry — silver and chloride ions combine to form the insoluble precipitate.

## Acids and Bases

### Three Definitions

| Theory | Acid | Base |
|---|---|---|
| Arrhenius | Produces H+ in water | Produces OH- in water |
| Bronsted-Lowry | Proton (H+) donor | Proton (H+) acceptor |
| Lewis | Electron pair acceptor | Electron pair donor |

Each definition is progressively more general. Bronsted-Lowry is the workhorse for aqueous chemistry. Lewis acid-base theory extends to non-aqueous and coordination chemistry.

### Conjugate Pairs

Every Bronsted-Lowry acid has a conjugate base (what remains after donating H+), and every base has a conjugate acid (what forms after accepting H+).

HCl + H2O -> Cl- + H3O+

Acid: HCl. Conjugate base: Cl-. Base: H2O. Conjugate acid: H3O+.

**Strong acids** (completely dissociate): HCl, HBr, HI, HNO3, H2SO4, HClO4.
**Strong bases** (completely dissociate): Group 1 hydroxides (NaOH, KOH), Ba(OH)2, Ca(OH)2.

### pH Scale

pH = -log[H3O+]. At 25 C: pH 7 is neutral, pH < 7 is acidic, pH > 7 is basic.

pOH = -log[OH-]. pH + pOH = 14.00 at 25 C.

**Worked example.** *Calculate the pH of 0.025 M HCl.*

HCl is a strong acid — complete dissociation: [H3O+] = 0.025 M.

pH = -log(0.025) = -log(2.5 x 10^-2) = -(log 2.5 + log 10^-2) = -(0.398 - 2) = 1.60.

### Worked Example: Weak Acid Equilibrium

**Problem.** Calculate the pH of 0.10 M acetic acid (Ka = 1.8 x 10^-5).

CH3COOH <=> CH3COO- + H+

Let x = [H+] at equilibrium. Ka = x^2 / (0.10 - x). Since Ka is small, assume 0.10 - x is approximately 0.10.

x^2 = 1.8 x 10^-5 x 0.10 = 1.8 x 10^-6.

x = 1.34 x 10^-3 M. Check assumption: 1.34 x 10^-3 / 0.10 = 1.3% < 5%. Valid.

pH = -log(1.34 x 10^-3) = 2.87.

### Titration and Equivalence Point

At the equivalence point, moles of acid = moles of base. For a strong acid + strong base titration, the equivalence point pH is 7.00. For a weak acid + strong base, the equivalence point pH is above 7 (conjugate base in solution is basic).

**Buffer solutions.** Mixtures of a weak acid and its conjugate base (or weak base and conjugate acid) resist pH changes. Henderson-Hasselbalch equation: pH = pKa + log([A-]/[HA]).

## Oxidation-Reduction (Redox)

### Oxidation States

Rules for assigning oxidation states (priority order):

1. Free elements: 0 (Na, O2, P4 all have oxidation state 0)
2. Monatomic ions: equal to charge (Na+ = +1, Cl- = -1)
3. Hydrogen: +1 (except in metal hydrides: -1)
4. Oxygen: -2 (except in peroxides: -1, and OF2: +2)
5. Fluorine: always -1
6. Sum of oxidation states = charge of species

**Oxidation** = increase in oxidation state (loss of electrons). **Reduction** = decrease in oxidation state (gain of electrons). Mnemonic: OIL RIG (Oxidation Is Loss, Reduction Is Gain).

### Half-Reaction Method (Acidic Solution)

**Worked example.** *Balance: MnO4- + Fe^2+ -> Mn^2+ + Fe^3+ in acidic solution.*

**Step 1.** Write half-reactions:
- Oxidation: Fe^2+ -> Fe^3+
- Reduction: MnO4- -> Mn^2+

**Step 2.** Balance atoms other than O and H:
- Fe^2+ -> Fe^3+ (Fe balanced)
- MnO4- -> Mn^2+ (Mn balanced)

**Step 3.** Balance O with H2O:
- MnO4- -> Mn^2+ + 4 H2O

**Step 4.** Balance H with H+:
- 8 H+ + MnO4- -> Mn^2+ + 4 H2O

**Step 5.** Balance charge with electrons:
- Fe^2+ -> Fe^3+ + e- (charge: +2 -> +3, add 1 e- to right)
- 5 e- + 8 H+ + MnO4- -> Mn^2+ + 4 H2O (charge: 5(-1) + 8(+1) + (-1) = +2 on left; +2 on right)

**Step 6.** Equalize electrons: multiply Fe half-reaction by 5.
- 5 Fe^2+ -> 5 Fe^3+ + 5 e-
- 5 e- + 8 H+ + MnO4- -> Mn^2+ + 4 H2O

**Step 7.** Add half-reactions (electrons cancel):
MnO4- + 5 Fe^2+ + 8 H+ -> Mn^2+ + 5 Fe^3+ + 4 H2O

**Verify:** Mn: 1 = 1. Fe: 5 = 5. O: 4 = 4. H: 8 = 8. Charge: (-1) + 5(+2) + 8(+1) = +17 on left; (+2) + 5(+3) + 0 = +17 on right.

### Electrochemistry Connection

Standard reduction potentials (E-zero) predict spontaneous redox reactions. A positive cell potential (E-zero-cell = E-zero-cathode - E-zero-anode) means the reaction is spontaneous. This connects stoichiometry to electrical energy — the basis of batteries and electrolysis.

## Thermochemistry

### Enthalpy (delta-H)

**Exothermic:** delta-H < 0 (releases heat). Combustion reactions, most neutralizations.
**Endothermic:** delta-H > 0 (absorbs heat). Photosynthesis, dissolving NH4NO3 in water.

### Hess's Law

If a reaction can be expressed as the sum of two or more steps, the overall delta-H is the sum of the delta-H values of the steps. Enthalpy is a state function — only initial and final states matter, not the path.

**Worked example.** *Calculate delta-H for: C(s) + 1/2 O2(g) -> CO(g), given:*

(1) C(s) + O2(g) -> CO2(g), delta-H1 = -393.5 kJ
(2) CO(g) + 1/2 O2(g) -> CO2(g), delta-H2 = -283.0 kJ

**Solution.** We need C + 1/2 O2 -> CO. Take reaction (1) as-is and reverse reaction (2):

(1) C + O2 -> CO2, delta-H = -393.5 kJ
(2 reversed) CO2 -> CO + 1/2 O2, delta-H = +283.0 kJ

Sum: C + O2 + CO2 -> CO2 + CO + 1/2 O2. Cancel CO2 and simplify O2:
C + 1/2 O2 -> CO, delta-H = -393.5 + 283.0 = -110.5 kJ.

### Calorimetry

q = m x c x delta-T, where q is heat (J), m is mass (g), c is specific heat capacity (J/g-C), and delta-T is temperature change.

**Worked example.** *50.0 g of water at 25.0 C absorbs 2,092 J. What is the final temperature?*

c(water) = 4.184 J/g-C.

delta-T = q / (m x c) = 2092 / (50.0 x 4.184) = 10.0 C.

T_final = 25.0 + 10.0 = 35.0 C.

### Standard Enthalpy of Formation (delta-Hf-zero)

delta-H-rxn = sum(delta-Hf-zero products) - sum(delta-Hf-zero reactants).

Elements in their standard states have delta-Hf-zero = 0 by definition.

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Unbalanced equations in stoichiometry | Wrong mole ratios give wrong answers | Always verify atom and charge balance before calculating |
| Ignoring limiting reagent | Assuming all reactants are fully consumed | Calculate moles of product from each reactant; the smaller result identifies the limiter |
| Forgetting to convert grams to moles | Stoichiometry works in moles, not grams | Always convert mass to moles before using coefficients |
| pH from weak acid = -log(initial concentration) | Weak acids do not fully dissociate | Use Ka equilibrium expression to find [H+] |
| Wrong sign on reversed Hess's law step | Reversing a reaction flips the sign of delta-H | Keep careful track of sign changes |
| Confusing oxidation and reduction | Leads to incorrect electron transfer | OIL RIG: Oxidation Is Loss, Reduction Is Gain |

## Cross-References

- **lavoisier agent:** Conservation of mass, reaction classification, stoichiometric calculations. Primary agent for this skill.
- **atomic-structure skill:** Atomic mass and mole concept derive from isotope-weighted averages.
- **chemical-bonding skill:** Bond energies provide an alternative route to estimating enthalpy changes.
- **analytical-methods skill:** Titration is a quantitative analytical technique rooted in acid-base and redox stoichiometry.
- **organic-chemistry skill:** Organic reactions (combustion, substitution, addition) follow the same stoichiometric principles.

## References

- Zumdahl, S. S. & Zumdahl, S. A. (2017). *Chemistry*. 10th edition. Cengage Learning.
- Silberberg, M. S. (2018). *Chemistry: The Molecular Nature of Matter and Change*. 8th edition. McGraw-Hill.
- Atkins, P. & de Paula, J. (2014). *Atkins' Physical Chemistry*. 10th edition. Oxford University Press.
- Lavoisier, A. L. (1789). *Traite Elementaire de Chimie*. (Translated: *Elements of Chemistry*.)
- Bronsted, J. N. (1923). "Some Remarks on the Concept of Acids and Bases." *Recueil des Travaux Chimiques*, 42, 718-728.
- Hess, G. H. (1840). "Recherches Thermochimiques." *Bulletin de l'Academie des Sciences de Saint-Petersbourg*, 8, 257-272.
