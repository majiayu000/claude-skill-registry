---
name: physical-chemistry
description: Chemical equilibrium, chemical kinetics, and electrochemistry — the quantitative core of physical chemistry. Covers equilibrium constants (Keq, Kc, Kp), Le Chatelier's principle, ICE tables, buffers and the Henderson-Hasselbalch equation, solubility product (Ksp) and the common-ion effect, rate laws, reaction order, integrated rate laws, half-life, the Arrhenius equation and activation energy, catalysis, redox reactions, galvanic and electrolytic cells, standard cell potentials, and the Nernst equation. Use when solving quantitative problems about how far a reaction goes (equilibrium), how fast it goes (kinetics), or how it converts chemical energy to electrical energy (electrochemistry).
type: skill
category: chemistry
status: stable
origin: tibsfox
modified: false
first_seen: 2026-07-06
first_path: examples/skills/chemistry/physical-chemistry/SKILL.md
superseded_by: null
---
# Physical Chemistry

Physical chemistry answers three quantitative questions about a reaction: how far does it go, how fast does it go, and how much electrical work can it do? These map to equilibrium, kinetics, and electrochemistry. This skill covers the equations and problem-solving methods for all three, with worked examples throughout.

**Agent affinity:** pauling (bonding and molecular energetics, primary), lavoisier (conservation, reaction bookkeeping, routing)

**Concept IDs:** chem-equilibrium, chem-le-chatelier, chem-buffers-ksp, chem-kinetics, chem-arrhenius, chem-electrochemistry

## Chemical Equilibrium

At equilibrium, the forward and reverse reaction rates are equal and the concentrations of reactants and products stop changing (though both reactions continue — equilibrium is dynamic, not static).

### The Equilibrium Constant

For the general reaction aA + bB <=> cC + dD, the equilibrium constant is:

Kc = ([C]^c [D]^d) / ([A]^a [B]^b)

where each concentration is the equilibrium value. Pure solids and pure liquids are omitted (their activity is 1).

- **Kc** uses molar concentrations.
- **Kp** uses partial pressures (for gases): Kp = Kc (RT)^(delta-n), where delta-n = (moles gas products) - (moles gas reactants), R = 0.08206 L-atm/mol-K.
- **K >> 1:** products favored. **K << 1:** reactants favored. **K near 1:** appreciable amounts of both.

**Reaction quotient Q.** Same expression as K, but with current (non-equilibrium) concentrations. Comparing Q to K predicts direction:

- Q < K: reaction proceeds forward (toward products).
- Q > K: reaction proceeds reverse (toward reactants).
- Q = K: system is at equilibrium.

### Le Chatelier's Principle

If a system at equilibrium is disturbed, it shifts to partially counteract the disturbance.

| Disturbance | Shift |
|---|---|
| Add reactant | Toward products (consume the added species) |
| Add product | Toward reactants |
| Remove product | Toward products |
| Increase pressure (decrease volume) | Toward the side with fewer moles of gas |
| Increase temperature (endothermic rxn, delta-H > 0) | Toward products (heat is a "reactant") |
| Increase temperature (exothermic rxn, delta-H < 0) | Toward reactants |
| Add a catalyst | No shift (speeds both directions equally) |

Note: temperature is the only disturbance that changes the value of K. Concentration and pressure changes shift the position but leave K unchanged.

### ICE Tables

An ICE table (Initial, Change, Equilibrium) organizes an equilibrium calculation.

**Worked example.** *For N2O4(g) <=> 2 NO2(g), Kc = 4.6 x 10^-3. If 0.100 M N2O4 is placed in a flask, find the equilibrium concentrations.*

| | N2O4 | 2 NO2 |
|---|---|---|
| Initial | 0.100 | 0 |
| Change | -x | +2x |
| Equilibrium | 0.100 - x | 2x |

Kc = (2x)^2 / (0.100 - x) = 4.6 x 10^-3.

Since Kc is small, assume 0.100 - x is approximately 0.100:

4x^2 = 4.6 x 10^-3 x 0.100 = 4.6 x 10^-4, so x^2 = 1.15 x 10^-4, x = 1.07 x 10^-2.

Check: 0.0107 / 0.100 = 10.7% > 5%, so the approximation is marginal. Solving the full quadratic 4x^2 + 4.6e-3 x - 4.6e-4 = 0 gives x = 1.02 x 10^-2.

[N2O4] = 0.100 - 0.0102 = 0.090 M; [NO2] = 2(0.0102) = 0.0204 M.

### Buffers and the Henderson-Hasselbalch Equation

A **buffer** is a solution of a weak acid and its conjugate base (or weak base and conjugate acid) that resists pH change on addition of small amounts of acid or base.

Henderson-Hasselbalch equation:

pH = pKa + log([A-] / [HA])

where [A-] is the conjugate base and [HA] the weak acid. When [A-] = [HA], pH = pKa — the buffer is most effective within +/-1 pH unit of pKa.

**Worked example.** *A buffer contains 0.20 M acetic acid (pKa = 4.74) and 0.30 M sodium acetate. Find the pH.*

pH = 4.74 + log(0.30 / 0.20) = 4.74 + log(1.5) = 4.74 + 0.18 = 4.92.

### Solubility Product (Ksp) and the Common-Ion Effect

For a sparingly soluble salt, the dissolution equilibrium has a solubility product. For AgCl(s) <=> Ag+(aq) + Cl-(aq):

Ksp = [Ag+][Cl-]

**Molar solubility from Ksp.** *Ksp(AgCl) = 1.8 x 10^-10. Find the molar solubility s in pure water.*

[Ag+] = [Cl-] = s, so Ksp = s^2 = 1.8 x 10^-10, s = 1.34 x 10^-5 M.

**Common-ion effect.** Adding an ion already present in the equilibrium suppresses solubility (Le Chatelier). *Find the solubility of AgCl in 0.10 M NaCl.*

Now [Cl-] is approximately 0.10 M (from NaCl). Ksp = s(0.10) = 1.8 x 10^-10, so s = 1.8 x 10^-9 M — roughly 7,000x less soluble than in pure water.

**Predicting precipitation.** Compute the ion product Q for the salt. If Q > Ksp, a precipitate forms; if Q < Ksp, the solution is unsaturated.

## Chemical Kinetics

Kinetics is the study of reaction rates — how fast concentrations change — and the mechanisms that control them.

### Rate Laws and Reaction Order

For aA + bB -> products, the experimentally determined rate law is:

rate = k [A]^m [B]^n

- **k** is the rate constant (temperature-dependent).
- **m** and **n** are the reaction orders in A and B (determined experimentally, not from coefficients).
- **Overall order** = m + n.

Units of k depend on overall order: zero order = M/s; first order = 1/s; second order = 1/(M-s).

**Method of initial rates.** Determine order by comparing runs where one concentration changes.

**Worked example.** *Given the data, find the rate law.*

| Run | [A] (M) | [B] (M) | Initial rate (M/s) |
|---|---|---|---|
| 1 | 0.10 | 0.10 | 2.0 x 10^-3 |
| 2 | 0.20 | 0.10 | 4.0 x 10^-3 |
| 3 | 0.10 | 0.20 | 8.0 x 10^-3 |

Runs 1->2: [A] doubles, rate doubles => first order in A (m = 1).
Runs 1->3: [B] doubles, rate quadruples => second order in B (n = 2).

rate = k [A][B]^2, overall third order. Solve for k from run 1: k = 2.0e-3 / (0.10 x 0.10^2) = 2.0 M^-2 s^-1.

### Integrated Rate Laws and Half-Life

Integrated rate laws give concentration as a function of time. A linear plot identifies the order.

| Order | Integrated law | Linear plot | Half-life |
|---|---|---|---|
| Zero | [A] = [A]0 - kt | [A] vs t | t(1/2) = [A]0 / 2k |
| First | ln[A] = ln[A]0 - kt | ln[A] vs t | t(1/2) = 0.693 / k |
| Second | 1/[A] = 1/[A]0 + kt | 1/[A] vs t | t(1/2) = 1 / (k[A]0) |

The first-order half-life is constant (independent of starting concentration) — the signature of first-order kinetics, and the basis of radioactive decay.

**Worked example.** *A first-order reaction has k = 0.0231 min^-1. How long until 90% of the reactant is consumed?*

90% consumed means [A]/[A]0 = 0.10. ln(0.10) = -kt, so t = -ln(0.10) / 0.0231 = 2.303 / 0.0231 = 99.7 min.

### Arrhenius Equation and Activation Energy

The rate constant increases with temperature per the Arrhenius equation:

k = A e^(-Ea / RT)

where A is the pre-exponential (frequency) factor, Ea is the activation energy, R = 8.314 J/mol-K, T in kelvin. Taking the natural log: ln k = ln A - Ea/(RT), a straight line of ln k versus 1/T with slope -Ea/R.

**Two-temperature form.** ln(k2/k1) = -(Ea/R)(1/T2 - 1/T1).

**Worked example.** *A reaction's rate constant doubles from 300 K to 310 K. Find Ea.*

ln(2) = -(Ea/8.314)(1/310 - 1/300) = -(Ea/8.314)(-1.075 x 10^-4).

0.693 = Ea x 1.293 x 10^-5, so Ea = 5.36 x 10^4 J/mol = 53.6 kJ/mol.

### Catalysis

A **catalyst** speeds a reaction by providing an alternative pathway with lower activation energy. It is regenerated (not consumed) and does not shift the equilibrium position — it accelerates forward and reverse reactions equally, so the system reaches the same equilibrium faster.

- **Homogeneous catalyst:** same phase as reactants (e.g., aqueous acid catalyzing ester hydrolysis).
- **Heterogeneous catalyst:** different phase (e.g., solid Pt surface in a catalytic converter).
- **Enzymes:** biological catalysts with high specificity; described by Michaelis-Menten kinetics.

## Electrochemistry

Electrochemistry links redox chemistry to electrical energy through the flow of electrons in cells.

### Redox Review

**Oxidation** is loss of electrons (oxidation state increases); **reduction** is gain of electrons (oxidation state decreases). Mnemonic: OIL RIG. The species oxidized is the reducing agent; the species reduced is the oxidizing agent.

### Galvanic (Voltaic) vs. Electrolytic Cells

| | Galvanic cell | Electrolytic cell |
|---|---|---|
| Energy | Spontaneous rxn produces electricity | Electricity drives a nonspontaneous rxn |
| E-cell | Positive | Negative (external voltage applied) |
| Anode | Negative terminal | Positive terminal |
| Cathode | Positive terminal | Negative terminal |

In every cell, oxidation occurs at the anode and reduction at the cathode ("An Ox, Red Cat"). Cell notation: anode | anode solution || cathode solution | cathode, e.g. Zn(s) | Zn2+(aq) || Cu2+(aq) | Cu(s).

### Standard Cell Potentials

Standard reduction potentials (E-zero, measured against the standard hydrogen electrode, SHE = 0.00 V) rank species by their tendency to be reduced. The standard cell potential is:

E-zero-cell = E-zero-cathode - E-zero-anode

(both taken as reduction potentials from a table). A positive E-zero-cell means the reaction is spontaneous.

**Worked example.** *A cell uses Zn2+/Zn (E-zero = -0.76 V) and Cu2+/Cu (E-zero = +0.34 V). Find E-zero-cell and identify the electrodes.*

Copper has the higher (more positive) reduction potential, so Cu2+ is reduced — copper is the cathode; zinc is the anode.

E-zero-cell = 0.34 - (-0.76) = +1.10 V. Positive, so the reaction Zn + Cu2+ -> Zn2+ + Cu is spontaneous.

### Connecting Potential, Free Energy, and K

The cell potential ties to thermodynamics and equilibrium:

delta-G-zero = -n F E-zero-cell     and     E-zero-cell = (RT / nF) ln K

where n is moles of electrons transferred and F = 96,485 C/mol (Faraday's constant). A positive E-zero-cell gives negative delta-G-zero (spontaneous) and K > 1.

### The Nernst Equation

Cell potential under non-standard conditions:

E-cell = E-zero-cell - (RT / nF) ln Q

At 25 C, substituting constants and converting to log base 10:

E-cell = E-zero-cell - (0.0592 / n) log Q

where Q is the reaction quotient. As the reaction proceeds, Q rises, E-cell falls, and at equilibrium (Q = K) E-cell = 0 — the battery is "dead."

**Worked example.** *For the Zn/Cu cell (E-zero-cell = 1.10 V, n = 2), find E-cell when [Zn2+] = 1.0 M and [Cu2+] = 0.010 M.*

Q = [Zn2+] / [Cu2+] = 1.0 / 0.010 = 100.

E-cell = 1.10 - (0.0592 / 2) log(100) = 1.10 - (0.0296)(2) = 1.10 - 0.0592 = 1.04 V.

Lowering the product-favoring reactant (Cu2+) lowers the cell potential, as expected.

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Reading reaction order off the coefficients | Order is experimental, not stoichiometric | Determine m, n from initial-rate or integrated-plot data |
| Including solids/liquids in K expressions | Pure condensed phases have activity 1 | Write only gases and aqueous species in Kc/Kp |
| Applying the 5% approximation without checking | Fails when x is not small vs. initial | Verify x/[initial] < 5%; else solve the quadratic |
| Thinking a catalyst shifts equilibrium | It speeds both directions equally | A catalyst changes rate, never K or the equilibrium position |
| Forgetting to convert temperature to kelvin in Arrhenius | Celsius gives nonsense in e^(-Ea/RT) | Always use absolute temperature (K) |
| Wrong sign in E-zero-cell = E-cathode - E-anode | Both values are reduction potentials | Subtract the anode's reduction potential; do not flip its sign twice |
| Using the wrong n in Nernst/delta-G | n is electrons transferred in the balanced cell reaction | Balance the redox half-reactions first to get n |

## Cross-References

- **reactions-stoichiometry skill:** Balancing, redox half-reactions, and acid-base equilibria are prerequisites for equilibrium and electrochemistry problems.
- **atomic-structure skill:** Ionization energy and electron affinity underlie reduction-potential trends.
- **chemical-bonding skill:** Bond energies and molecular stability inform activation energy and reaction thermodynamics.
- **analytical-methods skill:** Potentiometric titration and electroanalysis apply the Nernst equation directly.
- **pauling agent:** Molecular energetics and mechanisms — primary agent for kinetics and equilibrium reasoning.
- **lavoisier agent:** Reaction bookkeeping, conservation, and routing across the department.

## References

- Atkins, P. & de Paula, J. (2014). *Atkins' Physical Chemistry*. 10th edition. Oxford University Press.
- Zumdahl, S. S. & Zumdahl, S. A. (2017). *Chemistry*. 10th edition. Cengage Learning.
- Silberberg, M. S. (2018). *Chemistry: The Molecular Nature of Matter and Change*. 8th edition. McGraw-Hill.
- Arrhenius, S. (1889). "Uber die Reaktionsgeschwindigkeit bei der Inversion von Rohrzucker durch Sauren." *Zeitschrift fur Physikalische Chemie*, 4, 226-248.
- Nernst, W. (1889). "Die elektromotorische Wirksamkeit der Ionen." *Zeitschrift fur Physikalische Chemie*, 4, 129-181.
- Le Chatelier, H. (1884). "Sur un enonce general des lois des equilibres chimiques." *Comptes Rendus*, 99, 786-789.
