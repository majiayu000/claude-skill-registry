---
name: thermodynamics
description: Thermodynamics from the zeroth law through statistical mechanics. Covers temperature and thermal equilibrium, heat transfer mechanisms (conduction, convection, radiation), the first law (internal energy, work, heat), PV diagrams, thermodynamic processes (isothermal, adiabatic, isobaric, isochoric), the second law (entropy, Carnot cycle, heat engines, refrigerators), Boltzmann's statistical interpretation (S = k ln W), kinetic theory of gases, the third law, phase transitions, and free energy (Helmholtz and Gibbs). Use when analyzing heat engines, energy transformations, entropy, gas behavior, or any system where temperature and energy flow are central.
type: skill
category: physics
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/physics/thermodynamics/SKILL.md
superseded_by: null
---
# Thermodynamics

Thermodynamics governs the macroscopic behavior of energy, heat, work, and entropy. Its four laws establish the framework for understanding everything from steam engines to black holes. Historically, thermodynamics emerged from practical engineering (Carnot, 1824) and was placed on statistical foundations by Boltzmann, Maxwell, and Gibbs in the late 19th century. This skill covers the four laws, thermodynamic processes, heat engines, kinetic theory, phase transitions, and free energy.

**Agent affinity:** boltzmann (thermodynamics, Sonnet)

**Concept IDs:** phys-thermodynamics, phys-work-power, phys-kinetic-potential-energy, phys-conservation-of-energy

## Thermodynamics at a Glance

| # | Topic | Key equations | Core idea |
|---|---|---|---|
| 1 | Zeroth law & temperature | Thermal equilibrium is transitive | Defines temperature as a measurable quantity |
| 2 | Heat transfer | Q = mc Delta T, Fourier/Stefan-Boltzmann | Three mechanisms: conduction, convection, radiation |
| 3 | First law | Delta U = Q - W | Energy conservation for thermal systems |
| 4 | PV diagrams | W = integral of P dV | Work = area under curve |
| 5 | Processes | Isothermal, adiabatic, isobaric, isochoric | Each constrains one variable |
| 6 | Second law | Delta S >= 0 (isolated), eta_Carnot = 1 - T_C/T_H | Entropy never decreases; efficiency is bounded |
| 7 | Carnot cycle | eta = 1 - T_C/T_H | Theoretical maximum efficiency |
| 8 | Statistical mechanics | S = k_B ln W | Entropy counts microstates |
| 9 | Kinetic theory | PV = nRT, KE_avg = (3/2)k_B T | Gas behavior from molecular motion |
| 10 | Third law | S -> 0 as T -> 0 | Absolute zero is unattainable |
| 11 | Phase transitions | Q = mL, Clausius-Clapeyron | Energy exchange at constant temperature |
| 12 | Free energy | G = H - TS, F = U - TS | Spontaneity criteria at constant T, P or T, V |

## Topic 1 — The Zeroth Law and Temperature

**Zeroth law.** If system A is in thermal equilibrium with system B, and B is in thermal equilibrium with system C, then A is in thermal equilibrium with C. This seemingly trivial statement justifies the existence of temperature as a well-defined quantity and the use of thermometers.

**Temperature scales:**
- Kelvin: T_K = T_C + 273.15 (absolute scale, zero = no molecular motion)
- Celsius: T_C = T_K - 273.15
- Fahrenheit: T_F = (9/5)T_C + 32

**Why Kelvin matters.** All thermodynamic equations involving temperature ratios (Carnot efficiency, ideal gas law, entropy calculations) require absolute temperature in Kelvin. Using Celsius or Fahrenheit in these equations produces wrong answers.

## Topic 2 — Heat Transfer

**Conduction.** Heat flows through a material due to a temperature gradient. Fourier's law: dQ/dt = -kA (dT/dx), where k is thermal conductivity, A is cross-sectional area.

**Convection.** Heat transfer via bulk fluid motion. Newton's law of cooling: dQ/dt = hA(T_surface - T_fluid), where h is the convective heat transfer coefficient.

**Radiation.** All objects emit electromagnetic radiation. Stefan-Boltzmann law: P = epsilon sigma A T^4, where sigma = 5.67 * 10^-8 W/(m^2 K^4) and epsilon is emissivity (0 to 1).

**Worked example.** *A copper rod (k = 390 W/(m K)) of length 0.5 m and cross-sectional area 10^-4 m^2 connects a 100 C reservoir to a 20 C reservoir. Find the heat flow rate.*

**Solution.** dQ/dt = kA (Delta T / L) = 390 * 10^-4 * (80/0.5) = 390 * 10^-4 * 160 = 6.24 W.

**Specific heat capacity:** Q = mc Delta T, where c is specific heat (J/(kg K)). Water: c = 4186 J/(kg K). This is why water is such an effective coolant.

## Topic 3 — The First Law of Thermodynamics

**Statement:** Delta U = Q - W, where Delta U is the change in internal energy, Q is heat added to the system, and W is work done by the system.

This is conservation of energy applied to thermal systems. Energy can enter as heat or leave as work (and vice versa), but the total is tracked by internal energy U.

**Sign conventions matter.** In the physics convention: Q > 0 means heat flows INTO the system; W > 0 means work is done BY the system. Some engineering texts reverse the sign of W. Be consistent.

**Worked example.** *A gas absorbs 500 J of heat and does 200 J of work on its surroundings. What is the change in internal energy?*

**Solution.** Delta U = Q - W = 500 - 200 = 300 J. The internal energy increases by 300 J.

## Topic 4 — PV Diagrams and Work

**Work done by a gas:** W = integral from V_i to V_f of P dV. On a PV diagram, work is the area under the curve.

**Key insight.** Work depends on the path, not just the endpoints. Different processes connecting the same initial and final states yield different amounts of work. This is why thermodynamic processes must be specified.

**Clockwise cycles** on a PV diagram represent heat engines (net work done by the system). **Counterclockwise cycles** represent refrigerators or heat pumps (net work done on the system).

## Topic 5 — Thermodynamic Processes

### Isothermal (constant T)

For an ideal gas at constant temperature: PV = nRT = constant, so P = nRT/V. Work: W = nRT ln(V_f/V_i). Since T is constant, Delta U = 0, so Q = W — all absorbed heat becomes work.

### Adiabatic (Q = 0)

No heat exchange: Delta U = -W. The gas cools when it expands, heats when compressed. PV^gamma = constant, where gamma = C_P/C_V (5/3 for monatomic, 7/5 for diatomic). TV^(gamma-1) = constant.

### Isobaric (constant P)

Work: W = P Delta V. Heat: Q = nC_P Delta T. The specific heat at constant pressure C_P exceeds C_V because the gas must also do work expanding.

### Isochoric (constant V)

No volume change, so W = 0. Delta U = Q = nC_V Delta T. All heat goes into internal energy.

**Worked example.** *One mole of an ideal monatomic gas (gamma = 5/3) at 300 K and 1 atm expands adiabatically to twice its volume. Find the final temperature.*

**Solution.** TV^(gamma-1) = constant. T_i V_i^(2/3) = T_f V_f^(2/3). So T_f = T_i (V_i/V_f)^(2/3) = 300 (1/2)^(2/3) = 300 * 0.63 = 189 K.

The gas cools by 111 K during the adiabatic expansion. No heat was exchanged — the internal energy was converted to work.

## Topic 6 — The Second Law of Thermodynamics

The second law has several equivalent formulations:

**Clausius statement:** Heat cannot spontaneously flow from a colder body to a hotter body.

**Kelvin-Planck statement:** No cyclic process can convert heat entirely into work with no other effect.

**Entropy statement:** The entropy of an isolated system never decreases: Delta S_universe >= 0.

**Entropy definition:** dS = dQ_rev / T for a reversible process. For an irreversible process, Delta S > integral of dQ/T.

**Worked example.** *500 J of heat flows from a 600 K reservoir to a 300 K reservoir. Find the entropy change of the universe.*

**Solution.** Delta S_hot = -Q/T_hot = -500/600 = -0.833 J/K. Delta S_cold = +Q/T_cold = +500/300 = +1.667 J/K. Delta S_universe = -0.833 + 1.667 = +0.833 J/K > 0. Entropy increased, confirming the process is irreversible.

## Topic 7 — The Carnot Cycle

**Carnot's theorem.** No heat engine operating between two temperatures can be more efficient than a reversible (Carnot) engine between those temperatures.

**Carnot efficiency:** eta = 1 - T_C/T_H, where T_C and T_H are the cold and hot reservoir temperatures in Kelvin.

**The Carnot cycle consists of four steps:**
1. Isothermal expansion at T_H (absorb Q_H)
2. Adiabatic expansion (cool from T_H to T_C)
3. Isothermal compression at T_C (reject Q_C)
4. Adiabatic compression (heat from T_C to T_H)

**Worked example.** *A heat engine operates between a 500 K source and a 300 K sink. It absorbs 1000 J per cycle. Find the maximum work output and the minimum heat rejected.*

**Solution.** eta_Carnot = 1 - 300/500 = 0.4 = 40%. Maximum work: W = eta * Q_H = 0.4 * 1000 = 400 J. Minimum heat rejected: Q_C = Q_H - W = 600 J.

**Coefficient of performance (refrigerator):** COP = Q_C / W = T_C / (T_H - T_C) for a Carnot refrigerator.

**Why 100% efficiency is impossible.** The Carnot formula shows eta = 1 only if T_C = 0 K, which the third law says is unattainable. Real engines achieve 30-60% of Carnot efficiency.

## Topic 8 — Statistical Mechanics (Boltzmann)

**Boltzmann's entropy formula:** S = k_B ln W, where W is the number of microstates consistent with the macrostate and k_B = 1.38 * 10^-23 J/K.

**Microstates and macrostates.** A macrostate is defined by bulk properties (T, P, V). A microstate specifies the position and momentum of every particle. The second law emerges because systems overwhelmingly evolve toward macrostates with more microstates — that is, higher entropy is just more probable.

**Worked example.** *Four coins are flipped. Compare the entropy of "all heads" vs. "two heads, two tails."*

**Solution.** Macrostate "all heads": W = 1 (HHHH). S = k_B ln(1) = 0. Macrostate "two heads, two tails": W = C(4,2) = 6. S = k_B ln(6) = 1.79 k_B.

The "mixed" macrostate has higher entropy because more microstates produce it. This is why mixed states are overwhelmingly more likely in systems with 10^23 particles.

**Maxwell-Boltzmann speed distribution.** In a gas at temperature T, molecular speeds follow f(v) proportional to v^2 exp(-mv^2 / (2k_B T)). Most probable speed: v_p = sqrt(2k_B T / m). RMS speed: v_rms = sqrt(3k_B T / m). Mean speed: v_mean = sqrt(8k_B T / (pi m)).

## Topic 9 — Kinetic Theory of Gases

**Ideal gas law:** PV = nRT = Nk_B T, where n = moles, R = 8.314 J/(mol K), N = number of molecules, k_B = R/N_A.

**Pressure from molecular collisions.** Gas pressure arises from molecular impacts on container walls. Kinetic theory derives P = (1/3)(N/V)m v_rms^2.

**Average kinetic energy:** KE_avg = (3/2)k_B T per molecule. This is independent of molecular mass — all ideal gases at the same temperature have the same average kinetic energy per molecule.

**Equipartition theorem.** Each quadratic degree of freedom contributes (1/2)k_B T to the average energy. Monatomic gas: 3 translational DOF, so U = (3/2)nRT. Diatomic gas: 5 DOF (3 translational + 2 rotational), so U = (5/2)nRT. This predicts C_V = (3/2)R (monatomic) and C_V = (5/2)R (diatomic).

**Worked example.** *Find the RMS speed of nitrogen molecules (M = 28 g/mol = 0.028 kg/mol) at room temperature (300 K).*

**Solution.** v_rms = sqrt(3RT/M) = sqrt(3 * 8.314 * 300 / 0.028) = sqrt(2.67 * 10^5) = 517 m/s.

Nitrogen molecules at room temperature move at roughly half a kilometer per second. Despite this, diffusion is slow because molecules collide billions of times per second and follow a random walk.

## Topic 10 — The Third Law

**Nernst's statement:** The entropy of a perfect crystal at absolute zero is exactly zero: S(T = 0) = 0.

**Consequence.** Absolute zero (0 K) is unattainable in a finite number of steps. You can get arbitrarily close but never reach it. Each successive halving of temperature requires more work than the last.

**Practical impact.** The third law sets the zero point for entropy calculations. Absolute entropies can be computed by integrating C/T from 0 to T.

## Topic 11 — Phase Transitions

**Latent heat:** Q = mL, where L is the latent heat of the transition. During a phase transition, temperature remains constant despite continuous heat input — all energy goes into breaking or forming intermolecular bonds.

- Latent heat of fusion (solid to liquid): L_f = 334 kJ/kg for water
- Latent heat of vaporization (liquid to gas): L_v = 2260 kJ/kg for water

**Clausius-Clapeyron equation:** dP/dT = L / (T Delta v), where Delta v is the specific volume change. This gives the slope of phase boundaries on a PT diagram.

**Worked example.** *How much energy is needed to convert 2 kg of ice at -10 C to steam at 100 C?*

**Solution.** Four stages:
1. Heat ice from -10 C to 0 C: Q_1 = mc_ice Delta T = 2 * 2090 * 10 = 41,800 J
2. Melt ice: Q_2 = mL_f = 2 * 334,000 = 668,000 J
3. Heat water from 0 C to 100 C: Q_3 = mc_water Delta T = 2 * 4186 * 100 = 837,200 J
4. Boil water: Q_4 = mL_v = 2 * 2,260,000 = 4,520,000 J

Total: Q = 41,800 + 668,000 + 837,200 + 4,520,000 = 6,067,000 J = 6.07 MJ.

Note that vaporization dominates — it takes more energy to boil the water than to do all the other steps combined.

## Topic 12 — Free Energy

**Helmholtz free energy:** F = U - TS. At constant temperature and volume, a spontaneous process decreases F. Equilibrium at minimum F.

**Gibbs free energy:** G = H - TS = U + PV - TS. At constant temperature and pressure, a spontaneous process decreases G. Equilibrium at minimum G.

**Decision criterion:** Delta G < 0: spontaneous. Delta G = 0: equilibrium. Delta G > 0: non-spontaneous (requires external energy).

**Worked example.** *At 298 K, a reaction has Delta H = -100 kJ and Delta S = -200 J/K. Is it spontaneous?*

**Solution.** Delta G = Delta H - T Delta S = -100,000 - 298(-200) = -100,000 + 59,600 = -40,400 J = -40.4 kJ. Since Delta G < 0, the reaction is spontaneous at 298 K.

**Temperature crossover.** At T = Delta H / Delta S = 100,000/200 = 500 K, Delta G = 0. Above 500 K, Delta G > 0 and the reaction becomes non-spontaneous. Exothermic reactions that decrease entropy are spontaneous only at low enough temperatures.

## When to Use This Skill

- Heat engine and refrigerator efficiency calculations
- Energy balance problems (first law applications)
- Entropy calculations and spontaneity determinations
- Gas behavior (ideal gas law, molecular speeds)
- Phase transition problems (melting, boiling, sublimation)
- PV diagram analysis and work calculations
- Problems involving temperature, heat flow, or thermal equilibrium

## When NOT to Use This Skill

- **Mechanics problems without heat or temperature:** Use the classical-mechanics skill.
- **Electromagnetic heating (Joule heating, induction heating):** Start with the electromagnetism skill; bring in thermodynamics only for the thermal consequences.
- **Blackbody radiation at the quantum level:** Use the quantum-mechanics skill for Planck's law derivation and photon statistics.
- **Relativistic thermodynamics (black hole entropy):** Use the relativity-astrophysics skill.

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Using Celsius in Carnot efficiency | eta = 1 - T_C/T_H requires Kelvin | Always convert to Kelvin for ratio-based formulas |
| Confusing Q and W sign conventions | Physics and engineering conventions differ | Pick one convention and use it consistently throughout |
| Forgetting latent heat during phase changes | Temperature is constant during transitions | Break the problem into segments; include Q = mL at each phase boundary |
| Treating all expansions as isothermal | Adiabatic, isobaric, and isochoric follow different rules | Identify the constraint (constant T, Q, P, or V) before applying equations |
| Equating entropy decrease with impossibility | Local entropy can decrease if the universe's total increases | Only the TOTAL entropy of system + surroundings must increase |
| Applying equipartition at very low T | Quantum effects freeze out rotational and vibrational modes | Equipartition works above characteristic temperatures for each mode |

## Cross-References

- **boltzmann agent:** Primary agent for thermodynamics and statistical mechanics. Sonnet-class.
- **curie agent:** Department chair, coordinates thermodynamics with other physics domains.
- **faraday agent:** Pedagogy specialist — intuitive explanations of entropy and energy flow.
- **classical-mechanics skill:** For the mechanical work component (PV work is force times displacement at the molecular level).
- **quantum-mechanics skill:** For the quantum foundations of specific heats and blackbody radiation (where classical thermodynamics fails).
- **experimental-methods skill:** For calorimetry measurements and uncertainty in thermal experiments.

## References

- Schroeder, D. V. (2021). *An Introduction to Thermal Physics*. 2nd edition. Oxford University Press.
- Callen, H. B. (1985). *Thermodynamics and an Introduction to Thermostatistics*. 2nd edition. Wiley.
- Reif, F. (1965). *Fundamentals of Statistical and Thermal Physics*. McGraw-Hill.
- Kittel, C., & Kroemer, H. (1980). *Thermal Physics*. 2nd edition. W. H. Freeman.
- Feynman, R. P., Leighton, R. B., & Sands, M. (1963). *The Feynman Lectures on Physics*, Vol. I, Chapters 39-46. Addison-Wesley.
- Carnot, S. (1824). *Reflexions sur la puissance motrice du feu*. Bachelier.
- Boltzmann, L. (1877). "Uber die Beziehung zwischen dem zweiten Hauptsatze der mechanischen Warmetheorie und der Wahrscheinlichkeitsrechnung." *Wiener Berichte*, 76, 373-435.
