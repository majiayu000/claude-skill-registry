---
name: signal-processing-dsp-basics
description: Foundations of digital signal processing — sampling, aliasing, the Nyquist criterion, quantization, convolution, the discrete Fourier transform, FFT, FIR and IIR filter design, windowing, spectral leakage, and practical issues in fixed-point versus floating-point implementation. Use when designing filters, analyzing spectra, choosing sample rates, reasoning about aliasing, or implementing DSP algorithms on a microcontroller, DSP chip, or host CPU.
type: skill
category: electronics
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/electronics/signal-processing-dsp-basics/SKILL.md
superseded_by: null
---
# Signal Processing: DSP Basics

Digital signal processing is what happens after an ADC and before a DAC — or inside the world of purely discrete-time signals like audio files, sensor logs, and computed waveforms. The core ideas of DSP are deceptively simple (sample, add, multiply, feed back) but the traps are numerous (aliasing, leakage, numerical underflow, phase distortion, quantization noise). This skill covers the fundamentals every embedded or systems engineer needs to avoid making expensive analog problems digital.

**Agent affinity:** shima (DSP architecture and fixed-point implementation), horowitz (intuition and practical filter examples)

**Concept IDs:** elec-data-conversion-dsp, elec-signal-ac-analysis

## Sampling and the Nyquist Criterion

A continuous-time signal x(t) is sampled by taking its value at evenly spaced instants T_s apart, producing the discrete-time sequence x[n] = x(n * T_s). The sample rate f_s = 1 / T_s.

**The Nyquist-Shannon sampling theorem.** A band-limited signal whose frequency content is strictly below f_s / 2 can be perfectly reconstructed from its samples. Any frequency content above f_s / 2 gets aliased — folded back into the band from 0 to f_s / 2 — and becomes indistinguishable from legitimate signal content at the aliased frequency.

**The critical corollary.** The sample rate must be at least twice the highest frequency of interest. For audio at up to 20 kHz, the minimum is 40 kHz (compact disc uses 44.1 kHz, professional audio 48 or 96 kHz). For a temperature sensor whose highest frequency of interest is 1 Hz, 10 Hz is plenty.

**Anti-aliasing filters.** Before the ADC, an analog low-pass filter must attenuate everything above f_s / 2 below the noise floor of the ADC. No amount of post-processing can undo aliasing; once two frequencies fold onto each other, they are indistinguishable.

## Technique 1 — Quantization

An ADC represents each sample as one of 2^N levels, where N is the bit depth. The rounding error at each sample is a **quantization error**, uniformly distributed in the interval (-q/2, q/2) where q is the step size. Its RMS value is q / sqrt(12), and the resulting signal-to-quantization-noise ratio (SQNR) is approximately 6.02 * N + 1.76 dB.

**Practical numbers:**

| Bits | SQNR (dB) |
|---|---|
| 8 | 50 |
| 10 | 62 |
| 12 | 74 |
| 16 | 98 |
| 24 | 146 |

16-bit audio provides about 98 dB of dynamic range, which is near the limit of what consumer headphones can resolve. 24-bit audio is used in professional recording for headroom, not because the last eight bits are audible.

**Dithering.** Adding a small amount of random noise before quantization decorrelates the quantization error from the signal, trading distortion for noise. This is why 16-bit masters sound better than naive 16-bit truncation of a 24-bit original.

## Technique 2 — The Discrete Fourier Transform

The DFT of a length-N sequence x[n] is:

    X[k] = sum over n=0..N-1 of x[n] * exp(-j * 2π * k * n / N)

It represents the sequence as a sum of N complex exponentials at frequencies k * f_s / N. The magnitude |X[k]| shows how much energy is at each frequency; the phase shows the relative timing.

**The FFT.** The fast Fourier transform is an O(N log N) algorithm for computing the DFT; the naive computation is O(N^2). For N = 1024 the FFT is 100x faster, and the ratio grows with N.

**Worked example.** A 1024-sample buffer sampled at 48 kHz has frequency resolution 48000 / 1024 ≈ 46.9 Hz per bin. Bin k = 100 corresponds to 4.69 kHz. To resolve adjacent musical notes near 440 Hz (about 26 Hz apart between half-steps), a longer window is needed — e.g., 4096 samples gives 11.7 Hz resolution.

**Real vs complex.** A real-valued signal has conjugate-symmetric FFT: X[N-k] = conj(X[k]). Only the first N/2 + 1 bins carry independent information. DSP libraries provide real-FFT variants that exploit this for 2x speedup.

## Technique 3 — Windowing and Spectral Leakage

The DFT implicitly assumes the sequence is periodic with period N. If the actual signal is not an integer number of cycles in the window, the discontinuity at the boundary spreads energy across all frequency bins — **spectral leakage**.

**Windowing** multiplies the sequence by a tapered function that smoothly decays to zero at both ends of the buffer, suppressing the boundary discontinuity. Common windows:

| Window | Main lobe width | Side lobe level | Use |
|---|---|---|---|
| Rectangular | narrow | -13 dB | Baseline; worst leakage |
| Hann | medium | -31 dB | General-purpose |
| Hamming | medium | -43 dB | Speech analysis |
| Blackman-Harris | wide | -92 dB | Strong tones near weak tones |
| Kaiser (tunable) | variable | variable | When trade-off must be exact |

**Trade-off.** Narrower main lobe means better frequency resolution but worse side-lobe rejection. Tapered windows sacrifice some resolution for enormously better leakage suppression.

## Technique 4 — Convolution and FIR Filters

A finite impulse response filter has output:

    y[n] = sum over k=0..M-1 of h[k] * x[n - k]

where h[k] are the filter coefficients (the impulse response). This is a discrete convolution. FIR filters are always stable (no feedback, no poles) and can have exactly linear phase if the coefficients are symmetric — meaning all frequencies are delayed by the same amount, preserving waveform shape.

**Design methods:**

- **Window method.** Compute the ideal impulse response (sinc for a low-pass), truncate to M taps, multiply by a window.
- **Parks-McClellan (equiripple).** Optimize coefficients to minimize maximum error in the pass and stop bands.
- **Least-squares.** Minimize the sum of squared errors instead of the maximum error.

**Practical note.** FIR filter computation is dominated by multiply-accumulate (MAC) operations. DSP chips like TI's C6000 and ARM Cortex-M with DSP extensions can do one MAC per cycle, which is why they are called "DSP."

## Technique 5 — IIR Filters

Infinite impulse response filters use feedback:

    y[n] = sum over k=0..M-1 of b[k] * x[n - k] - sum over k=1..N-1 of a[k] * y[n - k]

IIR filters can achieve a given frequency response with far fewer coefficients than an equivalent FIR filter — the trade-off is that feedback introduces nonlinear phase and potential instability.

**Common IIR prototypes:**

| Prototype | Characteristic | Use |
|---|---|---|
| Butterworth | Maximally flat passband | General audio, control |
| Chebyshev I | Equiripple passband, monotonic stopband | Steeper rolloff than Butterworth |
| Chebyshev II | Monotonic passband, equiripple stopband | Steeper rolloff without passband ripple |
| Elliptic (Cauer) | Equiripple both | Steepest transition for given order |
| Bessel | Maximally flat group delay | Preserving waveform shape |

**Stability.** An IIR filter is stable iff all poles (roots of the denominator polynomial) lie strictly inside the unit circle. Quantizing IIR coefficients can move poles outside the unit circle — always verify stability after implementing a design in fixed-point.

## Technique 6 — Fixed-Point vs Floating-Point

Low-power microcontrollers without floating-point hardware use fixed-point arithmetic: integers are interpreted as having a fixed number of fractional bits. A Q15 format uses 1 sign bit and 15 fractional bits in a 16-bit word.

**Key traps:**

- **Overflow.** Adding two Q15 numbers can exceed the range. Either saturate (clip to ±1) or use Q1.14 intermediate format.
- **Rounding.** Multiplying two Q15 numbers produces a Q30 result; truncating to Q15 loses the lower bits, introducing noise.
- **Coefficient quantization.** Quantizing filter coefficients can move IIR poles near or outside the unit circle, destabilizing the filter.

**Decision rule.** Use floating-point if the hardware supports it (Cortex-M4F, Cortex-M7, any modern DSP). Use Q15 or Q31 only when the compute budget demands it.

## Technique 7 — Decimation and Interpolation

**Decimation.** Reducing the sample rate by a factor M. Must low-pass filter first to f_s / (2M) to prevent aliasing, then discard M-1 of every M samples.

**Interpolation.** Increasing the sample rate by a factor L. Insert L-1 zeros between samples, then low-pass filter to f_s / 2 (in the original scale) to remove the spectral images.

**Resampling.** Rational factor L / M is implemented as interpolation by L followed by decimation by M. The intermediate rate is L * f_s, which may be very high; efficient implementations (polyphase filters) avoid ever computing the full upsampled signal.

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| No anti-aliasing filter | Above-Nyquist content aliases | Always include analog low-pass before ADC |
| Undersampling assuming signal is band-limited | Signal has high-frequency content you forgot about | Verify with a sweep and oversampled capture |
| Using rectangular window for spectrum analysis | Strong leakage into adjacent bins | Apply Hann or better window before FFT |
| Implementing IIR without stability check | Coefficient quantization moves poles outside unit circle | Always verify poles after coefficient quantization |
| Multiplying Q15 values and truncating | Accumulates noise rapidly | Accumulate in Q30 or Q31, round once at the end |
| Assuming FFT bins correspond to integer frequencies | Bin resolution is f_s / N, rarely integer | Report frequencies in Hz, not bin indices |
| Ignoring filter group delay | Time alignment between channels breaks | Use linear-phase FIR if phase matters |

## Cross-References

- **circuit-analysis-dc-ac skill:** Provides the analog front-end and anti-aliasing filter context.
- **microcontroller-firmware skill:** Platform for running DSP in real time.
- **shima agent:** Primary agent for DSP architecture and fixed-point implementation questions.
- **horowitz agent:** Primary agent for intuition and worked filter examples.

## References

- Oppenheim, A. V. & Schafer, R. W. (2010). *Discrete-Time Signal Processing*. 3rd ed. Pearson.
- Smith, S. W. (1997). *The Scientist and Engineer's Guide to Digital Signal Processing*. California Technical Publishing. (Open access.)
- Lyons, R. G. (2010). *Understanding Digital Signal Processing*. 3rd ed. Prentice Hall.
- Horowitz, P. & Hill, W. (2015). *The Art of Electronics*. 3rd ed. Cambridge University Press, chapter 13.
- Parks, T. W. & Burrus, C. S. (1987). *Digital Filter Design*. Wiley.
