---
name: semiconductor-device-physics
description: Physical principles underlying diodes, bipolar junction transistors, and MOSFETs — carrier concentrations, drift and diffusion, the pn junction, forward and reverse bias, the Shockley diode equation, BJT operating regions, MOSFET threshold and saturation, small-signal models, and temperature effects. Use when reasoning about device-level behavior, designing bias networks, selecting transistor operating points, interpreting datasheets, or diagnosing nonlinear device failures.
type: skill
category: electronics
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/electronics/semiconductor-device-physics/SKILL.md
superseded_by: null
---
# Semiconductor Device Physics

Before a transistor can be used, it must be biased. Before it can be biased correctly, its underlying physics must be understood well enough to predict what happens when temperature changes, when the supply sags, or when the input drives it out of its intended operating region. This skill provides the bridge between the linear, idealized circuit analysis of the previous skill and the messy, nonlinear, temperature-sensitive reality of actual silicon.

**Agent affinity:** shockley (junction physics and bias), bardeen (surface physics and transistor action), brattain (experimental device characterization)

**Concept IDs:** elec-diode-rectification, elec-transistor-amplifiers, elec-semiconductor-physics

## What a Semiconductor Is

A semiconductor is a crystalline material (silicon, germanium, gallium arsenide) whose conductivity lies between that of a metal and that of an insulator, and — crucially — can be controlled by doping with impurities and by applied electric fields. At absolute zero, pure silicon has a filled valence band and an empty conduction band separated by a 1.12 eV bandgap. Above zero temperature, a small number of electrons are thermally excited into the conduction band, leaving holes behind in the valence band. Both electrons and holes act as mobile charge carriers.

Doping introduces atoms with either one extra valence electron (donors, producing n-type material) or one fewer (acceptors, producing p-type material). The equilibrium carrier concentrations satisfy the mass-action law n * p = n_i^2, where n_i is the intrinsic carrier concentration (≈ 1.5e10 cm^-3 for silicon at room temperature).

Current flows by two mechanisms: **drift** (carriers accelerated by an electric field, limited by mobility) and **diffusion** (carriers moving from regions of high to low concentration). The diffusion coefficient and mobility are related by the Einstein relation D = μ * kT / q.

## The pn Junction at Thermal Equilibrium

When p-type and n-type silicon are brought into contact, holes diffuse from the p side into the n side and electrons diffuse the other way. The diffused carriers leave behind uncompensated ionized dopants, forming a depletion region with a built-in electric field that opposes further diffusion. At equilibrium, drift and diffusion exactly cancel, and a built-in potential V_bi ≈ (kT/q) * ln(N_A * N_D / n_i^2) appears across the junction (typically 0.6-0.8 V for silicon).

**Key geometric facts:**

- The depletion region width scales as 1/sqrt(N_dopant). Heavily doped junctions have narrow depletion regions.
- The junction capacitance C_j scales as sqrt(1/(V_bi - V_applied)). Forward bias shrinks the depletion region and increases capacitance; reverse bias widens it and decreases capacitance.
- Almost all the applied voltage drops across the depletion region because the bulk semiconductor has low resistance.

## Technique 1 — Forward and Reverse Bias

**Forward bias.** Apply a positive voltage to the p side relative to the n side. The applied field opposes the built-in field, shrinking the depletion region and allowing majority carriers to diffuse across the junction. Current rises exponentially with voltage above the turn-on point (~0.6 V for silicon, ~0.3 V for germanium, ~1.8 V for blue LEDs).

**Reverse bias.** Apply a negative voltage. The applied field reinforces the built-in field, widening the depletion region. Only a tiny saturation current flows, dominated by minority carrier diffusion and thermal generation.

**Breakdown.** At sufficiently high reverse voltage the junction breaks down via avalanche multiplication (above ~6 V) or Zener tunneling (below ~6 V). Breakdown is non-destructive as long as the total power dissipated stays within the device's rating — this is how Zener diodes produce precise reference voltages.

## Technique 2 — The Shockley Diode Equation

The ideal diode I-V relationship is:

    I = I_s * (exp(V / (n * V_T)) - 1)

where V_T = kT/q ≈ 25.85 mV at room temperature, I_s is the reverse saturation current, and n is the ideality factor (1 for ideal diffusion, 2 for recombination-dominated).

**Worked example.** A silicon diode has I_s = 1e-14 A and n = 1. What voltage corresponds to 1 mA of forward current?

    V = V_T * ln(I / I_s + 1) ≈ 0.02585 * ln(1e11) ≈ 0.655 V

The characteristic curve is very steep: the voltage changes by only about 60 mV per decade of current change (V_T * ln(10) ≈ 59.5 mV). This is why a diode is often approximated as a 0.7 V drop in first-pass analysis.

**Temperature dependence.** I_s roughly doubles every 10 °C. At fixed current, the forward voltage drops by about -2 mV/°C. This is the dominant temperature effect in transistor circuits and must be compensated in precision designs.

## Technique 3 — Bipolar Junction Transistor (BJT) Operation

A BJT has three terminals (emitter, base, collector) and two junctions. In an NPN device, the base is a thin p-type region between two n-type regions. With the base-emitter junction forward biased and the base-collector junction reverse biased, electrons injected from the emitter diffuse across the thin base and are swept into the collector by the reverse field.

**Operating regions:**

| Region | V_BE | V_CE | I_C relationship |
|---|---|---|---|
| Cutoff | < 0.5 V | any | ≈ 0 (both junctions off) |
| Active | ≈ 0.7 V | > 0.2 V | I_C = β * I_B = I_S * exp(V_BE / V_T) |
| Saturation | ≈ 0.7-0.8 V | < 0.2 V | V_CE pinned ≈ 0.1-0.2 V, large I_B |
| Reverse active | (rarely used) | | |

**Key parameters:**

- β (current gain, also called h_FE): typically 50-500, varies with device, temperature, and I_C. Wide tolerance is the main reason BJT designs use emitter degeneration.
- V_BE(on): ≈ 0.6-0.7 V, temperature coefficient -2 mV/°C.
- V_CE(sat): ≈ 0.1-0.2 V when driven hard into saturation.
- I_S: exponentially temperature-dependent; the active-region current equation is more reliably temperature-stable than it first appears because β roughly tracks.

## Technique 4 — MOSFET Operation

A MOSFET has a gate separated from the channel by a thin oxide. Applying voltage to the gate accumulates or depletes carriers in the channel beneath it, modulating its conductivity. Unlike the BJT, the gate draws no steady-state current (the oxide is an insulator).

**N-channel enhancement MOSFET regions:**

| Region | V_GS vs V_T | V_DS | I_D relationship |
|---|---|---|---|
| Cutoff | < V_T | any | ≈ 0 |
| Triode (linear) | > V_T | < V_GS - V_T | I_D = k * [(V_GS - V_T) * V_DS - V_DS^2 / 2] |
| Saturation | > V_T | > V_GS - V_T | I_D = (k/2) * (V_GS - V_T)^2 * (1 + λ * V_DS) |

Here k = μ * C_ox * W / L is the transconductance parameter, V_T is the threshold voltage (typically 0.5-1.5 V for modern devices), and λ captures channel-length modulation (small, analogous to the BJT's Early effect).

**Key parameters:**

- Threshold voltage V_T: drifts with temperature (-2 to -4 mV/°C) but the drain current is more temperature-stable than a BJT because the exponential is replaced by a square law.
- No base current to worry about: the gate can be driven from a high-impedance source.
- Body effect: if the source is not at the same potential as the body terminal, V_T shifts. Important in cascoded or stacked designs.

## Technique 5 — Small-Signal Models

For amplifier design, replace each device with a linear model valid for small deviations around a chosen DC operating point (the Q point).

**Diode.** Small-signal resistance r_d = n * V_T / I_D. At 1 mA with n = 1, r_d ≈ 26 Ω.

**BJT hybrid-π model.**

- g_m = I_C / V_T (transconductance — at I_C = 1 mA, g_m ≈ 40 mA/V)
- r_π = β / g_m (base-emitter resistance — at β = 100 and g_m = 40 mA/V, r_π = 2.5 kΩ)
- r_o = V_A / I_C (output resistance — with V_A = 100 V Early voltage at 1 mA, r_o = 100 kΩ)

**MOSFET small-signal model.**

- g_m = k * (V_GS - V_T) = sqrt(2 * k * I_D)
- r_o = 1 / (λ * I_D)
- Gate resistance r_π = ∞ (or very large, set by leakage)

## Technique 6 — Bias Point Selection

A good bias point places the device in its active (BJT) or saturation (MOSFET) region with enough headroom that expected input signal swings do not drive it into cutoff or triode. Emitter degeneration (a resistor between emitter and ground) stabilizes I_C against β variations and temperature; source degeneration does the same for MOSFETs.

**BJT rule of thumb.** Set V_E to about 10% of V_CC. Set V_C to about halfway between V_CC and V_E to maximize output swing. Choose R_B1 and R_B2 as a stiff divider (I_divider ≈ 10 * I_B).

**MOSFET rule of thumb.** Set V_GS comfortably above V_T. Choose R_D and R_S such that the DC drain voltage sits near the middle of the supply minus the saturation headroom.

## Temperature Effects and Failure Modes

| Effect | Cause | Mitigation |
|---|---|---|
| V_BE(on) drifts -2 mV/°C | I_S temperature dependence | Emitter degeneration, matched transistor pair with shared thermal mass |
| Thermal runaway in power BJTs | I_C rises with T, I_C * V_CE heats device, V_BE drops, I_C rises more | Emitter degeneration, thermal feedback to bias circuit |
| β spread 3:1 typical | Process variation | Never design around a specific β; use emitter degeneration |
| MOSFET gate oxide breakdown | Electrostatic discharge or overvoltage | Input protection diodes, ESD handling procedures |
| BJT second breakdown | Hot spot forms at a point on the die | Stay within the safe operating area (SOA) curve |
| Reverse breakdown of a junction | Exceeded V_reverse rating | Clamp diodes across inductive loads |

## Cross-References

- **circuit-analysis-dc-ac skill:** Provides the linear DC bias framework on top of which small-signal models live.
- **shockley agent:** Named for the Shockley equation; primary agent for junction and bias questions.
- **bardeen agent:** Primary agent for transistor action and superconductivity questions.
- **brattain agent:** Primary agent for experimental device characterization and surface physics.
- **test-and-measurement skill:** Explains how to measure the quantities predicted by these equations.

## References

- Horowitz, P. & Hill, W. (2015). *The Art of Electronics*. 3rd ed. Cambridge University Press.
- Sedra, A. & Smith, K. (2015). *Microelectronic Circuits*. 7th ed. Oxford.
- Streetman, B. & Banerjee, S. (2015). *Solid State Electronic Devices*. 7th ed. Pearson.
- Shockley, W. (1949). "The theory of p-n junctions in semiconductors and p-n junction transistors." *Bell System Technical Journal*, 28(3), 435-489.
- Bardeen, J. & Brattain, W. (1948). "The transistor, a semi-conductor triode." *Physical Review*, 74(2), 230-231.
