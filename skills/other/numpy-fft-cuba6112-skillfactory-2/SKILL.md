---
name: numpy-fft
description: Discrete Fourier Transform routines for spectral analysis, signal filtering, and frequency-domain operations. Triggers: fft, fourier transform, spectral analysis, rfft, fftshift, ifft.
---

## Overview
NumPy's `fft` module provides routines for computing Discrete Fourier Transforms (DFT). It is widely used for signal processing, image frequency analysis, and solving differential equations in the frequency domain.

## When to Use
- Analyzing the frequency components of a time-series signal.
- Applying low-pass or high-pass filters to digital signals.
- Accelerating convolutions by performing them in the frequency domain.
- Visualizing centered frequency spectra in 2D image processing.

## Decision Tree
1. Is your input purely real?
   - Use `np.fft.rfft` for better efficiency and halved output size.
2. Do you want the 0Hz component in the center of the plot?
   - Use `np.fft.fftshift` on the transform result.
3. Performance is slow?
   - Zero-pad input to a power of 2 (e.g., 256, 1024).

## Workflows
1. **Frequency Domain Analysis**
   - Take a real-valued signal 'a'.
   - Compute the positive frequencies using `np.fft.rfft(a)`.
   - Generate matching frequency bins with `np.fft.rfftfreq(len(a))`.
   - Plot the magnitude spectrum using `np.abs(spectrum)`.

2. **FFT-Based Signal Filtering**
   - Transform the signal into the frequency domain with `np.fft.fft`.
   - Zero out specific frequency components in the complex spectrum.
   - Transform back to the time domain using `np.fft.ifft` and take the real part.

3. **Visualizing Centered Spectra**
   - Compute a 2D FFT of an image using `np.fft.fft2`.
   - Apply `np.fft.fftshift` to move the low-frequency components to the image center.
   - Visualize the log-magnitude of the shifted spectrum.

## Non-Obvious Insights
- **Real Symmetry:** `rfft` is faster because real-input transforms are Hermitian (symmetric); it skips redundant computations.
- **Precision Upcasting:** NumPy FFT routines automatically upcast `float32` to `float64` and `complex64` to `complex128`.
- **Optimal Sizes:** Algorithms are most efficient when the signal length $n$ is a power of 2.

## Evidence
- "When the input is purely real... The family of rfft functions is designed to operate on real inputs, and exploits this symmetry by computing only the positive frequency components." [Source](https://numpy.org/doc/stable/reference/routines.fft.html)
- "The routine np.fft.fftshift(A) shifts transforms and their frequencies to put the zero-frequency components in the middle." [Source](https://numpy.org/doc/stable/reference/routines.fft.html)

## Scripts
- `scripts/numpy-fft_tool.py`: Routines for spectral analysis and rfft frequency mapping.
- `scripts/numpy-fft_tool.js`: Simulated complex magnitude logic.

## Dependencies
- `numpy` (Python)

## References
- [references/README.md](references/README.md)