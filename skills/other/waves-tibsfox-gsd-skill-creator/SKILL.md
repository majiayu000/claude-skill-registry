---
name: mfe-waves
description: "Periodic phenomena and frequency analysis. How repetition creates structure — from simple oscillation to Fourier decomposition."
user-invocable: false
allowed-tools: Read Grep Glob
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-26"
      triggers:
        intents:
          - "wave"
          - "frequency"
          - "harmonic"
          - "oscillation"
          - "period"
          - "amplitude"
          - "resonance"
          - "standing wave"
          - "Fourier"
          - "spectrum"
        contexts:
          - "mathematical problem solving"
          - "math reasoning"
---

# Waves

## Summary

**Waves** (Part II: Hearing)
Chapters: 4, 5, 6, 7
Plane Position: (-0.4, 0) radius 0.4
Primitives: 50

Periodic phenomena and frequency analysis. How repetition creates structure — from simple oscillation to Fourier decomposition.

**Key Concepts:** Simple Harmonic Motion, Frequency, Wave Function, Superposition Principle, Wave Equation

## Key Primitives



**Simple Harmonic Motion** (definition): Simple harmonic motion (SHM) is periodic motion where the restoring force is proportional to displacement: F = -kx. The solution is x(t) = A*cos(omega*t + phi) where omega = sqrt(k/m).
  - modeling back-and-forth motion of a pendulum or spring
  - any system with a linear restoring force proportional to displacement

**Frequency** (definition): The frequency f of a periodic phenomenon is the number of complete cycles per unit time. f = 1/T where T is the period. Measured in hertz (Hz = cycles/second).
  - determining how many oscillations occur per second
  - relating pitch of a sound to its physical frequency

**Wave Function** (definition): The general sinusoidal wave function is y(x,t) = A*sin(kx - omega*t + phi), describing a traveling wave with amplitude A, wave number k, angular frequency omega, and phase offset phi.
  - describing a sinusoidal disturbance propagating through a medium
  - modeling light, sound, or any traveling periodic signal

**Superposition Principle** (theorem): For linear systems, the net response at a given point caused by two or more stimuli is the sum of the responses that would have been caused by each stimulus individually. For waves: y_total(x,t) = y_1(x,t) + y_2(x,t) + ...
  - adding together multiple wave sources to find the combined effect
  - analyzing interference patterns from multiple coherent sources

**Wave Equation** (definition): The one-dimensional wave equation is the second-order partial differential equation: d^2u/dt^2 = c^2 * d^2u/dx^2, where c is the wave propagation speed and u(x,t) is the displacement field.
  - modeling wave propagation in strings, air columns, or electromagnetic fields
  - predicting how disturbances travel through a medium

**Harmonic Series** (definition): The harmonic series of a fundamental frequency f_1 consists of integer multiples: f_n = n * f_1 for n = 1, 2, 3, ... The nth harmonic has frequency n times the fundamental.
  - determining the frequency content of a vibrating string or air column
  - understanding why different instruments sound different even playing the same note

**Fundamental Frequency** (definition): The fundamental frequency f_1 is the lowest resonant frequency of a vibrating system. For a string of length L with wave speed v: f_1 = v/(2L). All higher harmonics are integer multiples of f_1.
  - finding the lowest pitch produced by a vibrating string or air column
  - tuning musical instruments to a specific pitch

**Separation of Variables for Waves** (technique): Separation of variables assumes the solution to a PDE is a product of functions of individual variables: u(x,t) = X(x)*T(t). Substituting into the wave equation and dividing by X*T yields two ODEs: X''/X = T''/(c^2*T) = -lambda (separation constant).
  - solving the wave equation on a bounded domain with fixed or free boundary conditions
  - finding the natural vibration modes of a physical system

**Standing Wave** (definition): A standing wave is a wave pattern that does not propagate through space but oscillates in place. It is formed by the superposition of two identical waves traveling in opposite directions: 2A*sin(kx)*cos(omega*t).
  - analyzing vibration patterns on strings, membranes, or in cavities
  - determining where resonant systems have maximum and minimum displacement

**Period** (definition): The period T of a periodic function f is the smallest positive value such that f(t + T) = f(t) for all t. T is the duration of one complete cycle.
  - measuring the time for one complete oscillation cycle
  - determining how long before a periodic system returns to its initial state

## Composition Patterns

- Simple Harmonic Motion + waves-frequency -> Complete SHM description with temporal period and spatial amplitude (parallel)
- Frequency + waves-wavelength -> Wave speed: v = f * lambda, connecting temporal and spatial periodicity (parallel)
- Period + waves-frequency -> Complete temporal characterization: T = 1/f, f = 1/T (parallel)
- Angular Frequency + perception-radian-measure -> Natural sinusoidal parameterization: sin(omega*t) cycles at frequency f = omega/(2*pi) (nested)
- Wave Function + waves-wave-number -> Complete space-time wave description: y(x,t) = A*sin(kx - omega*t) (parallel)
- Wavelength + waves-frequency -> Wave speed relation: v = lambda * f (parallel)
- Sum-to-Product Formulas + waves-superposition-principle -> Analysis of combined waves: sum of two sinusoids reveals beat and carrier frequencies (sequential)
- Product-to-Sum Formulas + waves-sum-to-product -> Complete toolkit for converting between product and sum forms of trigonometric expressions (parallel)
- Superposition Principle + waves-constructive-destructive-interference -> Complete interference analysis: constructive when in-phase, destructive when out-of-phase (sequential)
- Phasor Representation + waves-superposition-principle -> Adding sinusoids by vector addition of their phasors (sequential)

## Cross-Domain Links

- **perception**: Compatible domain for composition and cross-referencing
- **change**: Compatible domain for composition and cross-referencing
- **reality**: Compatible domain for composition and cross-referencing
- **mapping**: Compatible domain for composition and cross-referencing
- **synthesis**: Compatible domain for composition and cross-referencing

## Activation Patterns

- wave
- frequency
- harmonic
- oscillation
- period
- amplitude
- resonance
- standing wave
- Fourier
- spectrum
