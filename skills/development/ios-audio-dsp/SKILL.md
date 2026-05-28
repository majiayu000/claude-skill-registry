---
name: ios-audio-dsp
description: Expert knowledge for iOS audio processing, pitch detection algorithms (HPS, YIN, FFT), DSP implementation, and AudioKit integration. Use this when implementing pitch detection, debugging audio accuracy issues, working with AVAudioEngine, or optimizing audio DSP performance for mobile.
---

# iOS Audio DSP Expert Guidance

Use these instructions when working with iOS audio processing, pitch detection, DSP algorithms, or AudioKit integration in the saxjaxTunerIntelligent project.

## Algorithm Recommendations

### Professional Tuner Apps Reference
- **Peterson iStroboSoft** (0.1 cent accuracy): FFT + Enhanced spectrum analyzer with strobe simulation
- **Cleartune** (1-2 cent accuracy): FFT + Zero-crossing hybrid approach

### Recommended Algorithms for Guitar/Instrument Tuners
1. **HPS (Harmonic Product Spectrum)** - BEST for harmonic instruments
2. **FFT Direct Peak** - Fast, good for strong fundamentals  
3. **YIN** - Academic reference, harder to implement correctly

**Avoid:** Pure time-domain autocorrelation (too slow for mobile)

## HPS (Harmonic Product Spectrum) - RECOMMENDED

### Algorithm Steps
1. Compute FFT of windowed signal (Hann window)
2. Downsample spectrum by factors: 2, 3, 4, 5
3. Multiply all downsampled spectra together
4. Find peak (harmonics align at fundamental)
5. Apply parabolic interpolation for sub-bin accuracy

### Strengths
- ✅ Robust to missing fundamental
- ✅ Easy to implement correctly
- ✅ Real-time capable on mobile
- ✅ Good accuracy (1-3 cents achievable)

### Weaknesses
- ⚠️ Can have octave errors (detectable and filterable)
- ⚠️ Less effective below 50 Hz (not issue for guitar)

### Implementation
```swift
// After FFT, for each bin i:
let compressed2 = spectrum[i/2]
let compressed3 = spectrum[i/3]
let compressed4 = spectrum[i/4]
let compressed5 = spectrum[i/5]

hpsSpectrum[i] = spectrum[i] * compressed2 * compressed3 * compressed4 * compressed5

// Find peak, then parabolic interpolation for sub-bin accuracy
```

## YIN Algorithm - Complex Implementation

### WARNING
FFT-based YIN is complex and error-prone. Consider HPS instead.

### Key Issues
1. **Factor-of-2 Confusion**: FFT zero-padding changes normalization semantics
2. **Windowing Ambiguity**: Windowing can make accuracy WORSE for autocorrelation
3. **Sample Rate**: Always capture once at initialization from `AVAudioSession.sharedInstance().sampleRate`
4. **Parabolic Interpolation**: Essential for sub-sample accuracy
5. **CMNDF**: Must be implemented correctly: `d'(tau) = d(tau) * tau / sum(d[1..tau])`

### Empirical Reality
- Theory says one thing, practice shows another
- "Mathematically correct" implementations often fail
- Empirical corrections (e.g., `tau * 1.003`) often work better

## FFT Implementation Details

### Window Functions
**Periodic (for FFT):** `w(n) = 0.5 * (1 - cos(2πn/N))` for n = 0..N-1
**Symmetric (for filter design):** `w(n) = 0.5 * (1 - cos(2πn/(N-1)))` for n = 0..N-1

**When to use:**
- FFT spectral analysis (HPS, direct peak): Use PERIODIC
- Time-domain autocorrelation: Use SYMMETRIC
- FFT-based autocorrelation: Test both, use what works

### Buffer Sizing
- Power of 2 required (1024, 2048, 4096)
- YIN autocorrelation: Use 2x buffer size for zero-padding
- HPS: Standard FFT size = buffer size

### Parabolic Interpolation
```swift
func parabolicInterpolation(_ bins: [Float], _ peakIndex: Int) -> Float {
    guard peakIndex > 0 && peakIndex < bins.count - 1 else {
        return Float(peakIndex)
    }
    
    let alpha = bins[peakIndex - 1]
    let beta = bins[peakIndex]
    let gamma = bins[peakIndex + 1]
    
    let denominator = alpha - 2.0 * beta + gamma
    guard denominator != 0 else { return Float(peakIndex) }
    
    let p = 0.5 * (alpha - gamma) / denominator
    return Float(peakIndex) + p
}
```

## AVAudioSession Configuration

### For Real-Time Tuner Apps
```swift
let session = AVAudioSession.sharedInstance()
try session.setCategory(.playAndRecord, mode: .measurement, options: [])
try session.setPreferredIOBufferDuration(0.005) // ~5ms latency
try session.setActive(true)

// Capture ONCE at init
let sampleRate = AVAudioSession.sharedInstance().sampleRate // Usually 48000.0
```

## Common Accuracy Issues

### Error Patterns
1. **Constant Offset**: Sample rate mismatch or tau calculation off-by-one
2. **Frequency-Dependent Drift**: FFT circular correlation bias or incorrect interpolation
3. **Octave Errors**: Tau search range too narrow or harmonic stronger than fundamental

### Debugging Strategy
1. Gather test data across frequency range (Low: A1-55Hz, Mid: A3-220Hz, High: A5-880Hz)
2. Identify error pattern (Hz offset vs cents offset vs frequency-dependent)
3. Apply ONE targeted fix and test
4. Verify across octaves (target: ±1-2 cents, acceptable: ±5 cents)

## AudioKit Integration

```swift
import AudioKit
import AudioKitEX

let mic = AudioEngine.InputNode()
let tap = PitchTap(mic) { pitch, amp in
    // Process here
}

let sampleRate = Settings.sampleRate // Usually 48000.0
try AudioKit.start()
tap.start()
```

## Production Checklist
- [ ] Tested across 3+ octaves (low/mid/high)
- [ ] Accuracy ±2 cents or better at A440
- [ ] Sample rate captured correctly from AVAudioSession
- [ ] Confidence threshold prevents false positives
- [ ] Handles silence gracefully
- [ ] No production debug logging
- [ ] Works on physical device (not just simulator)

## Code Quality
- Use `Float` for audio buffers (vDSP optimized)
- Use `Double` for frequency calculations (precision matters)
- Comment all empirical correction factors with rationale

## Tuning Standards (A440)
- A0: 27.5 Hz, A1: 55 Hz, A2: 110 Hz, A3: 220 Hz
- A4: 440 Hz (reference)
- A5: 880 Hz, A6: 1760 Hz, A7: 3520 Hz

**Cent Calculation:** `cents = 1200 × log₂(f_detected / f_expected)`
**Acceptable Errors:** Professional: ±1-2 cents, Good: ±3-5 cents, Human perception: ~5-6 cents
