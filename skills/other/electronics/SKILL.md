---
name: electronics
description: Electronics Educational Pack — routes queries to 15 modules covering Ohm's law through PCB design
triggers:
  - electronics
  - circuit
  - voltage
  - current
  - resistor
  - capacitor
  - inductor
  - amplifier
  - transistor
  - diode
  - op-amp
  - digital logic
  - PCB
  - power supply
  - microcontroller
  - sensor
  - DSP
  - filter
  - ADC
  - DAC
---

# Electronics Educational Pack

Comprehensive electronics curriculum grounded in *The Art of Electronics* (Horowitz & Hill, 3rd ed., 2015). Covers 15 modules across 4 tiers, from Ohm's law through PCB design, with interactive labs powered by MNA circuit simulation and digital logic simulation.

## Routing

Given a user topic, this skill routes to the appropriate module by matching trigger keywords against the 14 domain skills defined in `chipset.yaml`.

### routeToModule(topic: string): string | null

Accepts a topic string (user query or keyword) and returns the target module directory name, or `null` if no match is found.

**Algorithm:**
1. Normalize the topic string (lowercase, trim whitespace)
2. Match against each skill's `triggers` array from `chipset.yaml`
3. If multiple skills match, prefer the most specific match (longest matching trigger string)
4. Return the matched skill's `module` field (e.g., `"01-the-circuit"`)
5. For `industrial-and-applied` (multi-module skill), return the best-fit module from `[13-plc, 14-off-grid-power, 15-pcb-design]` based on the specific trigger matched
6. If no trigger matches, return `null`

**Keyword-to-Module Routing Table:**

| Keyword | Module | Skill |
|---------|--------|-------|
| voltage, current, resistance, ohm, kirchhoff, power, series, parallel, divider | 01-the-circuit | circuit-fundamentals |
| capacitor, inductor, RC, RL, RLC, filter, resonance, thevenin, norton, impedance | 02-passive-components | passive-components |
| AC, frequency, bode, decibel, dB, noise, signal, coupling, spectrum, waveform | 03-the-signal | signal-analysis |
| diode, rectifier, zener, LED, shockley, clamping, bridge, I-V curve | 04-diodes | diode-circuits |
| transistor, BJT, MOSFET, amplifier, common-emitter, emitter-follower, current-mirror, beta, gain | 05-transistors | transistor-circuits |
| op-amp, operational amplifier, inverting, non-inverting, integrator, differentiator, comparator, golden rules, active filter | 06-op-amps | op-amp-circuits |
| power supply, regulator, buck, boost, switching, linear, 7805, LDO, ripple, thermal, battery | 07-power-supplies | power-supply-design |
| logic gate, boolean, AND, OR, NOT, NAND, NOR, XOR, CMOS, truth table, K-map, de morgan | 07a-logic-gates | logic-gate-design |
| flip-flop, counter, register, state machine, clock, latch, moore, mealy, SRAM, memory | 08-sequential-logic | sequential-logic |
| ADC, DAC, sampling, nyquist, quantization, R-2R, SAR, sigma-delta, aliasing | 09-data-conversion | data-conversion |
| DSP, FIR, IIR, FFT, DFT, filter design, convolution, windowing, fixed-point | 10-dsp | dsp-fundamentals |
| microcontroller, MCU, GPIO, UART, SPI, I2C, interrupt, PWM, Arduino, ESP32 | 11-microcontrollers | microcontroller-systems |
| sensor, actuator, Wheatstone, H-bridge, stepper, thermocouple, optocoupler, strain gauge, instrumentation amplifier | 12-sensors-actuators | sensor-actuator-systems |
| PLC, ladder logic, off-grid, solar, MPPT, PCB, layout, Gerber, PID, Modbus, NEC | 13-plc / 14-off-grid-power / 15-pcb-design | industrial-and-applied |

## Modules

| # | Module | Tier | Topics |
|---|--------|------|--------|
| 1 | The Circuit | 1 | V, I, R, Ohm's law, KVL/KCL, voltage dividers, power |
| 2 | Passive Components | 1 | Capacitors, inductors, RC/RL/RLC, filters, Thevenin/Norton |
| 3 | The Signal | 1 | AC, frequency response, Bode plots, dB, noise |
| 4 | Diodes | 2 | I-V curves, rectification, Zener, LEDs, Shockley equation |
| 5 | Transistors | 2 | BJT, MOSFET, amplifiers, common-emitter, current mirrors |
| 6 | Op-Amps | 2 | Golden rules, inverting/non-inverting, active filters, integrators |
| 7 | Power Supplies | 2 | Linear/switching regulators, buck/boost, LDO, thermal |
| 7A | Logic Gates | 3 | Boolean algebra, CMOS, truth tables, K-maps, De Morgan's |
| 8 | Sequential Logic | 3 | Flip-flops, counters, state machines, registers, memory |
| 9 | Data Conversion | 3 | ADC/DAC, sampling, Nyquist, quantization, aliasing |
| 10 | DSP | 3 | FIR/IIR, FFT/DFT, convolution, windowing, fixed-point |
| 11 | Microcontrollers | 4 | MCU, GPIO, UART/SPI/I2C, interrupts, PWM |
| 12 | Sensors & Actuators | 4 | Wheatstone, H-bridge, stepper, thermocouples, inst. amps |
| 13 | PLC | 4 | Ladder logic, PID, structured text, Modbus, IEC 61131-3 |
| 14 | Off-Grid Power | 4 | Solar PV, MPPT, batteries, charge controllers, NEC |
| 15 | PCB Design | 4 | Layout, design rules, EMI, Gerber files, soldering |

## Learning Progression

The curriculum follows a 4-tier pipeline, where each tier builds on the previous:

**Tier 1 (Foundations)** -- Modules 1-3
Voltage, current, resistance, passive components, and AC signals. No active devices. All labs use passive circuits only. Safety: Annotate mode.

**Tier 2 (Active Devices)** -- Modules 4-7
Semiconductors (diodes, transistors), op-amps, and power supplies. Introduces nonlinear behavior and active circuit design. Safety: Gate mode for higher voltages.

**Tier 3 (Digital & Mixed-Signal)** -- Modules 7A, 8, 9, 10
Logic gates, sequential circuits, data conversion, and DSP. Bridges analog and digital domains. Safety: Annotate (logic) to Gate (mixed-signal).

**Tier 4 (Applied Systems)** -- Modules 11-15
Microcontrollers, sensors, PLCs, off-grid power, and PCB design. Real-world applications combining all previous tiers. Safety: Gate to Redirect mode for industrial/high-voltage.

## Configuration

See `chipset.yaml` for detailed skill triggers, agent assignments, and pipeline topology.
See `metadata.yaml` for pack identity, version, and tier structure.
See `references/bibliography.md` for H&H citation conventions.
See `references/hh-chapter-map.md` for chapter-to-module mapping.
