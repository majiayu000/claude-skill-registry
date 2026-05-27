---
name: audio-analysis
description: Audio analysis with Tone.js and Web Audio API including FFT, frequency data extraction, amplitude measurement, and waveform analysis. Use when extracting audio data for visualizations, beat detection, or any audio-reactive features.
---

# Audio Analysis

FFT, frequency extraction, and audio data analysis.

## Quick Start

```javascript
import * as Tone from 'tone';

// Create analyzer
const analyser = new Tone.Analyser('fft', 256);
const player = new Tone.Player('/audio/music.mp3');

player.connect(analyser);
player.toDestination();

// Get frequency data
const frequencyData = analyser.getValue(); // Float32Array
```

## Analyzer Types

### FFT Analyzer

```javascript
// FFT (Fast Fourier Transform) - frequency spectrum
const fftAnalyser = new Tone.Analyser({
  type: 'fft',
  size: 256,        // Must be power of 2: 32, 64, 128, 256, 512, 1024, 2048
  smoothing: 0.8    // 0-1, higher = smoother transitions
});

// Returns Float32Array of dB values (typically -100 to 0)
const fftData = fftAnalyser.getValue();
```

### Waveform Analyzer

```javascript
// Waveform - time domain data
const waveformAnalyser = new Tone.Analyser({
  type: 'waveform',
  size: 1024
});

// Returns Float32Array of amplitude values (-1 to 1)
const waveformData = waveformAnalyser.getValue();
```

### Meter (Volume Level)

```javascript
// Meter - overall volume level
const meter = new Tone.Meter({
  smoothing: 0.9,
  normalRange: false  // true for 0-1, false for dB
});

player.connect(meter);

// Get current level
const level = meter.getValue(); // dB or 0-1
```

### FFT Size Impact

| Size | Frequency Resolution | Time Resolution | Use Case |
|------|---------------------|-----------------|----------|
| 32 | Low | High | Beat detection |
| 128 | Medium | Medium | General visualization |
| 256 | Good | Good | Balanced (default) |
| 1024 | High | Low | Detailed spectrum |
| 2048 | Very High | Very Low | Audio analysis tools |

## Frequency Bands

### Manual Band Extraction

```javascript
const analyser = new Tone.Analyser('fft', 256);

function getFrequencyBands() {
  const data = analyser.getValue();
  const binCount = data.length;

  // Define frequency band ranges (approximate for 44.1kHz sample rate)
  // Each bin = (sampleRate / 2) / binCount Hz
  const bands = {
    sub: average(data, 0, Math.floor(binCount * 0.03)),      // ~20-60 Hz
    bass: average(data, Math.floor(binCount * 0.03), Math.floor(binCount * 0.08)),  // ~60-250 Hz
    lowMid: average(data, Math.floor(binCount * 0.08), Math.floor(binCount * 0.15)), // ~250-500 Hz
    mid: average(data, Math.floor(binCount * 0.15), Math.floor(binCount * 0.3)),     // ~500-2000 Hz
    highMid: average(data, Math.floor(binCount * 0.3), Math.floor(binCount * 0.5)),  // ~2000-4000 Hz
    high: average(data, Math.floor(binCount * 0.5), binCount)                         // ~4000+ Hz
  };

  return bands;
}

function average(data, start, end) {
  let sum = 0;
  for (let i = start; i < end; i++) {
    sum += data[i];
  }
  return sum / (end - start);
}
```

### Normalized Band Values

```javascript
function getNormalizedBands() {
  const bands = getFrequencyBands();

  // Convert dB to 0-1 range (assuming -100 to 0 dB range)
  const normalize = (db) => Math.max(0, Math.min(1, (db + 100) / 100));

  return {
    sub: normalize(bands.sub),
    bass: normalize(bands.bass),
    lowMid: normalize(bands.lowMid),
    mid: normalize(bands.mid),
    highMid: normalize(bands.highMid),
    high: normalize(bands.high)
  };
}
```

## Beat Detection

### Simple Peak Detection

```javascript
class BeatDetector {
  constructor(threshold = 0.7, decay = 0.98) {
    this.threshold = threshold;
    this.decay = decay;
    this.peak = 0;
    this.lastBeat = 0;
    this.minInterval = 200; // Minimum ms between beats
  }

  detect(analyser) {
    const data = analyser.getValue();

    // Focus on bass frequencies for beat detection
    const bassEnergy = this.getBassEnergy(data);

    // Decay the peak
    this.peak *= this.decay;

    // Update peak if higher
    if (bassEnergy > this.peak) {
      this.peak = bassEnergy;
    }

    // Detect beat
    const now = Date.now();
    const threshold = this.peak * this.threshold;

    if (bassEnergy > threshold && now - this.lastBeat > this.minInterval) {
      this.lastBeat = now;
      return true;
    }

    return false;
  }

  getBassEnergy(data) {
    // Average of low frequency bins
    let sum = 0;
    const bassRange = Math.floor(data.length * 0.1);
    for (let i = 0; i < bassRange; i++) {
      // Convert dB to linear and sum
      sum += Math.pow(10, data[i] / 20);
    }
    return sum / bassRange;
  }
}

// Usage
const beatDetector = new BeatDetector();
const analyser = new Tone.Analyser('fft', 256);

function update() {
  if (beatDetector.detect(analyser)) {
    console.log('Beat!');
    // Trigger visual effect
  }
  requestAnimationFrame(update);
}
```

### Energy History Beat Detection

```javascript
class EnergyBeatDetector {
  constructor(historySize = 43, sensitivity = 1.3) {
    this.history = new Array(historySize).fill(0);
    this.sensitivity = sensitivity;
    this.historyIndex = 0;
  }

  detect(analyser) {
    const data = analyser.getValue();
    const currentEnergy = this.calculateEnergy(data);

    // Calculate average energy from history
    const avgEnergy = this.history.reduce((a, b) => a + b) / this.history.length;

    // Update history
    this.history[this.historyIndex] = currentEnergy;
    this.historyIndex = (this.historyIndex + 1) % this.history.length;

    // Beat if current energy exceeds average by sensitivity factor
    return currentEnergy > avgEnergy * this.sensitivity;
  }

  calculateEnergy(data) {
    let energy = 0;
    for (let i = 0; i < data.length; i++) {
      const amplitude = Math.pow(10, data[i] / 20);
      energy += amplitude * amplitude;
    }
    return energy;
  }
}
```

## Amplitude Analysis

### RMS (Root Mean Square)

```javascript
function getRMS(analyser) {
  const waveform = analyser.getValue(); // Waveform analyzer

  let sum = 0;
  for (let i = 0; i < waveform.length; i++) {
    sum += waveform[i] * waveform[i];
  }

  return Math.sqrt(sum / waveform.length);
}
```

### Peak Amplitude

```javascript
function getPeakAmplitude(analyser) {
  const waveform = analyser.getValue();
  let peak = 0;

  for (let i = 0; i < waveform.length; i++) {
    const abs = Math.abs(waveform[i]);
    if (abs > peak) peak = abs;
  }

  return peak;
}
```

## Smoothing Techniques

### Exponential Smoothing

```javascript
class SmoothValue {
  constructor(smoothing = 0.9) {
    this.value = 0;
    this.smoothing = smoothing;
  }

  update(newValue) {
    this.value = this.smoothing * this.value + (1 - this.smoothing) * newValue;
    return this.value;
  }
}

// Usage
const smoothBass = new SmoothValue(0.85);
const bassLevel = smoothBass.update(rawBassLevel);
```

### Moving Average

```javascript
class MovingAverage {
  constructor(size = 10) {
    this.size = size;
    this.values = [];
  }

  update(value) {
    this.values.push(value);
    if (this.values.length > this.size) {
      this.values.shift();
    }
    return this.values.reduce((a, b) => a + b) / this.values.length;
  }
}
```

## Complete Analysis System

```javascript
class AudioAnalysisSystem {
  constructor() {
    this.fftAnalyser = new Tone.Analyser('fft', 256);
    this.waveformAnalyser = new Tone.Analyser('waveform', 1024);
    this.meter = new Tone.Meter({ smoothing: 0.9 });

    this.smoothers = {
      bass: new SmoothValue(0.85),
      mid: new SmoothValue(0.9),
      high: new SmoothValue(0.9),
      volume: new SmoothValue(0.95)
    };

    this.beatDetector = new BeatDetector();
  }

  connect(source) {
    source.connect(this.fftAnalyser);
    source.connect(this.waveformAnalyser);
    source.connect(this.meter);
    source.toDestination();
  }

  getAnalysis() {
    const fft = this.fftAnalyser.getValue();
    const waveform = this.waveformAnalyser.getValue();
    const volume = this.meter.getValue();

    const bands = this.extractBands(fft);

    return {
      // Raw data
      fft,
      waveform,

      // Smoothed bands (0-1)
      bass: this.smoothers.bass.update(bands.bass),
      mid: this.smoothers.mid.update(bands.mid),
      high: this.smoothers.high.update(bands.high),

      // Volume
      volume: this.smoothers.volume.update(this.normalizeDb(volume)),
      volumeDb: volume,

      // Beat
      isBeat: this.beatDetector.detect(this.fftAnalyser),

      // Waveform metrics
      rms: this.getRMS(waveform),
      peak: this.getPeak(waveform)
    };
  }

  extractBands(fft) {
    const len = fft.length;
    return {
      bass: this.normalizeDb(this.avgRange(fft, 0, len * 0.1)),
      mid: this.normalizeDb(this.avgRange(fft, len * 0.1, len * 0.5)),
      high: this.normalizeDb(this.avgRange(fft, len * 0.5, len))
    };
  }

  avgRange(data, start, end) {
    let sum = 0;
    const s = Math.floor(start);
    const e = Math.floor(end);
    for (let i = s; i < e; i++) sum += data[i];
    return sum / (e - s);
  }

  normalizeDb(db) {
    return Math.max(0, Math.min(1, (db + 100) / 100));
  }

  getRMS(waveform) {
    let sum = 0;
    for (let i = 0; i < waveform.length; i++) {
      sum += waveform[i] * waveform[i];
    }
    return Math.sqrt(sum / waveform.length);
  }

  getPeak(waveform) {
    let peak = 0;
    for (let i = 0; i < waveform.length; i++) {
      const abs = Math.abs(waveform[i]);
      if (abs > peak) peak = abs;
    }
    return peak;
  }

  dispose() {
    this.fftAnalyser.dispose();
    this.waveformAnalyser.dispose();
    this.meter.dispose();
  }
}
```

## Temporal Collapse Usage

```javascript
class TemporalAudioAnalysis extends AudioAnalysisSystem {
  getCountdownData() {
    const analysis = this.getAnalysis();

    return {
      // For bloom intensity
      glowIntensity: analysis.bass * 0.5 + analysis.volume * 0.5,

      // For particle speed
      particleEnergy: analysis.mid,

      // For chromatic aberration
      distortion: analysis.high * 0.3,

      // For digit pulse
      pulse: analysis.isBeat ? 1 : 0,

      // For background intensity
      ambientLevel: analysis.rms
    };
  }
}
```

## Performance Tips

```javascript
// 1. Use appropriate FFT size
const analyser = new Tone.Analyser('fft', 128); // Smaller = faster

// 2. Don't analyze every frame if not needed
let frameCount = 0;
function update() {
  if (frameCount % 2 === 0) { // Every other frame
    const data = analyser.getValue();
  }
  frameCount++;
}

// 3. Reuse arrays
const dataArray = new Float32Array(256);
analyser.getValue(dataArray); // Pass in array to avoid allocation

// 4. Use smoothing to reduce visual jitter
const smoothedValue = smoother.update(rawValue);
```

## Reference

- See `audio-playback` for loading and playing audio
- See `audio-reactive` for connecting analysis to visuals
- See `audio-router` for audio domain routing
