---
name: circuit-analysis-dc-ac
description: Systematic analysis of DC and AC linear circuits using Ohm's law, Kirchhoff's laws, node and mesh methods, Thevenin and Norton equivalents, phasor analysis, and Bode plots. Covers series and parallel reduction, superposition, source transformation, impedance in the frequency domain, first and second order transient response, and the conversion between time domain and phasor representations. Use when quantitatively predicting voltages, currents, power, gain, phase, or time response of any lumped-element linear circuit.
type: skill
category: electronics
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/electronics/circuit-analysis-dc-ac/SKILL.md
superseded_by: null
---
# Circuit Analysis: DC and AC

Circuit analysis is the engineering discipline of predicting the behavior of a network of resistors, capacitors, inductors, voltage and current sources, and dependent sources using a small catalog of laws and transformations. Everything downstream — amplifier design, filter design, power supply design, feedback stability, oscillator start-up — ultimately reduces to getting the underlying DC bias and AC small-signal analysis right. This skill catalogs the core techniques in the order they are typically applied and shows how to move fluently between the time domain, the phasor (frequency) domain, and the Laplace domain.

**Agent affinity:** shockley (device bias and load lines), horowitz (intuition building and worked examples)

**Concept IDs:** elec-ohms-law-fundamentals, elec-passive-component-behavior, elec-signal-ac-analysis

## The Core Laws

Every linear circuit obeys three laws. Everything else in this skill is a consequence of how these three are applied.

| # | Law | Statement | Use for |
|---|---|---|---|
| 1 | Ohm's law | V = IR for resistors; V = IZ for general impedances | Relating voltage and current across a single element |
| 2 | Kirchhoff's voltage law (KVL) | The sum of voltage drops around any closed loop is zero | Writing one equation per mesh |
| 3 | Kirchhoff's current law (KCL) | The sum of currents entering any node equals the sum leaving | Writing one equation per node |

KVL is conservation of energy around a loop. KCL is conservation of charge at a node. Ohm's law is the constitutive relation. A correct analysis uses exactly as many independent equations as there are unknown node voltages or mesh currents.

## Technique 1 — Series and Parallel Reduction

**Pattern:** Collapse runs of resistors (or impedances) using R_series = R_1 + R_2 + ... and 1/R_parallel = 1/R_1 + 1/R_2 + ... until the circuit is reduced to a single element seen by the source.

**Worked example.** A 10 kΩ resistor in series with the parallel combination of 20 kΩ and 30 kΩ.

The parallel combination is (20 * 30) / (20 + 30) = 600 / 50 = 12 kΩ. The total is 10 kΩ + 12 kΩ = 22 kΩ. If the source is 11 V, the total current is 0.5 mA, the drop across the 10 kΩ resistor is 5 V, and the remaining 6 V appears across the parallel pair.

**When to use.** First pass on every problem. If the circuit reduces cleanly, you may not need any further technique. Reduction fails as soon as a branch contains a non-grounded source or a dependent source whose controlling variable lives inside the region being collapsed.

## Technique 2 — Voltage and Current Dividers

**Voltage divider.** Two resistors R_1 and R_2 in series across a source V_s produce V_out = V_s * R_2 / (R_1 + R_2) across R_2. Loaded dividers require including the load resistance in parallel with R_2.

**Current divider.** Two parallel resistors split a total current I_total such that the current through R_1 is I_total * R_2 / (R_1 + R_2). The lower-resistance branch gets more current.

**Practical rule.** A voltage divider driving a load needs its Thevenin source resistance small compared to the load (typically at least 10x smaller) for the divider ratio to hold within a few percent. Ignoring this rule is the most common first-year error.

## Technique 3 — Nodal Analysis

**Pattern:** Pick a reference node (ground). Label every other node with a voltage variable. Write KCL at each labeled node in terms of node voltages and the conductances connecting them. Solve the resulting linear system.

**Worked example.** Three nodes labeled A, B, and ground. A 10 V source drives node A through a 1 kΩ resistor; a 2 kΩ resistor connects A to B; a 3 kΩ resistor connects B to ground. KCL at A: (10 - V_A)/1k = (V_A - V_B)/2k. KCL at B: (V_A - V_B)/2k = V_B/3k. Solving the 2x2 system yields V_A ≈ 6.92 V and V_B ≈ 4.15 V.

**When to use.** Circuits with many nodes and few loops; circuits where node voltages are the natural output (e.g., amplifier outputs). Nodal analysis is also the basis of modified nodal analysis, the core algorithm in SPICE.

## Technique 4 — Mesh Analysis

**Pattern:** Identify independent loops (meshes). Assign a clockwise mesh current to each. Write KVL around each mesh in terms of mesh currents and the impedances in each branch. Solve the linear system.

**Worked example.** A two-mesh circuit with mesh currents I_1 and I_2 sharing a 4 kΩ resistor. Mesh 1 has a 12 V source, a 2 kΩ resistor, and the shared 4 kΩ resistor. Mesh 2 has the shared 4 kΩ and a 6 kΩ to ground. KVL mesh 1: 12 = 2k * I_1 + 4k * (I_1 - I_2). KVL mesh 2: 0 = 4k * (I_2 - I_1) + 6k * I_2. Solving yields I_1 ≈ 2.4 mA and I_2 ≈ 0.96 mA.

**When to use.** Circuits with few loops and many nodes; circuits where branch currents are the natural output. For planar circuits the number of mesh equations equals the number of independent loops.

## Technique 5 — Superposition

**Pattern:** For a linear circuit with multiple independent sources, compute the response due to each source alone (with all other independent sources set to zero — voltage sources shorted, current sources opened), then sum the individual responses.

**Worked example.** A circuit with a 5 V source and a 2 mA current source. Compute the voltage across a target resistor with only the 5 V source present, then again with only the current source present, then add. The total is the true steady-state voltage.

**Restrictions.** Superposition applies only to linear elements. It does not apply to power (power is quadratic), and it does not apply when the circuit contains nonlinear elements in the region of operation being analyzed.

## Technique 6 — Thevenin and Norton Equivalents

**Thevenin.** Any linear two-terminal network is equivalent, from the terminals' perspective, to a single voltage source V_th in series with a resistance R_th. V_th is the open-circuit voltage; R_th is the ratio V_open / I_short (or the resistance seen looking in with independent sources zeroed).

**Norton.** The dual: a single current source I_n in parallel with R_n, where I_n is the short-circuit current and R_n = R_th.

**Worked example.** A voltage divider made of R_1 = 10 kΩ and R_2 = 10 kΩ across a 10 V source has V_th = 5 V (open-circuit midpoint) and R_th = 5 kΩ (parallel combination of R_1 and R_2 with the source shorted). A 5 kΩ load then sees 5 V * 5k / (5k + 5k) = 2.5 V.

**When to use.** Any time you need to understand what a complicated sub-circuit "looks like" to whatever is connected at its terminals. Thevenin/Norton reduction is the single most useful technique in practical design.

## Technique 7 — Phasor Analysis (AC Steady State)

**Pattern:** Replace sinusoidal sources with their complex amplitude (phasor). Replace capacitors with impedance 1/(jωC) and inductors with jωL. The circuit becomes an algebraic problem in complex impedances, solvable by any DC technique (nodal, mesh, Thevenin).

**Worked example.** A 1 kΩ resistor in series with a 1 μF capacitor driven by a 1 V amplitude sinusoid at ω = 1000 rad/s. The capacitor impedance is 1 / (j * 1000 * 1e-6) = -j * 1000 Ω. The total impedance is 1000 - j1000 Ω, with magnitude √2 * 1000 Ω and phase -45°. The current phasor is V / Z = 1 / (1000√2 ∠ -45°) = (1/(1000√2)) ∠ +45°. The current leads the voltage by 45° — the classic first-order RC response at the corner frequency.

**When to use.** Any sinusoidal steady-state problem. Phasor analysis is the bridge between time-domain differential equations and the intuitive frequency-domain picture used in filter design and amplifier characterization.

## Technique 8 — Transient Analysis

**First-order RC and RL circuits.** The response to a step input has the form v(t) = v_∞ + (v_0 - v_∞) * exp(-t / τ), where τ is the time constant (RC for a capacitor, L/R for an inductor), v_0 is the initial value, and v_∞ is the final value. Solve for initial conditions by inspecting the circuit just before the step; solve for final conditions by treating capacitors as open circuits and inductors as short circuits in DC steady state.

**Second-order RLC circuits.** The response depends on damping. Underdamped (ζ < 1) rings with decaying sinusoidal envelope. Critically damped (ζ = 1) reaches final value fastest without overshoot. Overdamped (ζ > 1) approaches monotonically. The natural frequency ω_n and damping factor ζ follow directly from the characteristic polynomial of the circuit's differential equation.

**Worked example.** A 1 kΩ resistor in series with a 1 μF capacitor, initially uncharged, suddenly connected to a 5 V source. τ = 1 ms. The capacitor voltage follows 5 * (1 - exp(-t / 1 ms)). After one time constant (1 ms) it reaches 3.16 V; after five time constants (5 ms) it is within 1% of the final 5 V.

## Technique 9 — Bode Plots

**Pattern:** Plot magnitude (in dB) and phase (in degrees) of the transfer function H(jω) versus log frequency. Each pole contributes a -20 dB/decade magnitude slope above its corner frequency and a -90° phase shift spread over two decades. Each zero contributes +20 dB/decade and +90°.

**Worked example.** A first-order low-pass filter with corner frequency f_c = 1 kHz has magnitude flat at 0 dB below f_c, rolling off at -20 dB/decade above f_c, and passing through -3 dB at f_c itself. The phase is 0° well below f_c, -90° well above, and -45° at f_c.

**When to use.** Visualizing amplifier bandwidth, filter response, feedback loop stability (where the gain and phase margins are read directly off the Bode plot), and noise spectrum shaping.

## Decision Guidance — Which Technique First?

1. **Is the circuit resistive and DC?** Try series/parallel reduction first. If that fails, use nodal or mesh analysis.
2. **Does the circuit have many nodes, few loops?** Use nodal analysis.
3. **Does the circuit have few nodes, many loops?** Use mesh analysis.
4. **Are there multiple independent sources and you want the response due to one of them?** Use superposition.
5. **Do you need to understand a sub-circuit's behavior at its terminals?** Find the Thevenin/Norton equivalent.
6. **Is the input sinusoidal at a known frequency?** Convert to phasors.
7. **Is the input a step or pulse?** Set up the differential equation and solve as a first- or second-order transient.
8. **Are you interested in the system's response across all frequencies?** Compute the transfer function and draw a Bode plot.

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Ignoring load on a voltage divider | Divider ratio changes when loaded | Include load in parallel with R_2 |
| Mixing phasors and instantaneous values | Units and phase conventions differ | Convert everything to phasors first, then solve |
| Zeroing dependent sources in superposition | Dependent sources must stay active | Only independent sources are zeroed |
| Forgetting initial conditions in transient analysis | The constant of integration is set by t=0+ | Always evaluate v(0+) and v(∞) before writing the response |
| Assuming the corner frequency is exactly -3 dB on a Bode asymptote | Asymptotes are approximations | Use the asymptote for intuition, the exact formula for design |
| Applying superposition to power | Power is nonlinear (P = V * I) | Compute V and I via superposition, then multiply |

## Cross-References

- **shockley agent:** Applies circuit analysis to transistor bias point and small-signal models.
- **horowitz agent:** Teaches the intuition-first perspective from Art of Electronics.
- **semiconductor-device-physics skill:** Explains the I-V relationships of nonlinear devices that appear as small-signal resistances.
- **signal-processing-dsp-basics skill:** Picks up where Bode plots leave off, adding sampling, quantization, and discrete-time filters.

## References

- Horowitz, P. & Hill, W. (2015). *The Art of Electronics*. 3rd ed. Cambridge University Press.
- Sedra, A. & Smith, K. (2015). *Microelectronic Circuits*. 7th ed. Oxford.
- Nilsson, J. & Riedel, S. (2019). *Electric Circuits*. 11th ed. Pearson.
- Irwin, J. D. & Nelms, R. M. (2020). *Basic Engineering Circuit Analysis*. 12th ed. Wiley.
