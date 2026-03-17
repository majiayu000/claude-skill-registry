---
name: dsp-filter-designer
description: Design and test DSP filters (highpass, lowpass, bandpass, notch) for WaveCap-SDR. Use when adding filters to demodulation pipeline, debugging filter response, or tuning cutoff frequencies and rolloff characteristics.
---

# DSP Filter Designer for WaveCap-SDR

This skill helps design, test, and visualize digital filters for the WaveCap-SDR DSP pipeline.

## When to Use This Skill

Use this skill when:
- Designing new filters for demodulation pipelines (FM, AM, SSB)
- Testing filter parameters (cutoff frequencies, order, rolloff)
- Debugging filter response issues (not cutting enough, too much ripple)
- Visualizing frequency and phase response of existing filters
- Optimizing filter performance vs computational cost
- Adding notch filters to remove interference

## How It Works

The skill provides an interactive filter design tool that:

1. **Designs filters** using scipy.signal (Butterworth, Chebyshev, Elliptic)
2. **Visualizes response** - frequency response, phase response, impulse response
3. **Tests performance** - applies filter to test signals to verify behavior
4. **Exports code** - generates Python code ready for wavecapsdr/dsp/filters.py

## Usage Instructions

### Step 1: Identify Filter Requirements

Determine what you need:
- **Filter type**: highpass, lowpass, bandpass, notch
- **Cutoff frequency**: Where filter should start attenuating
- **Sample rate**: Audio sample rate (typically 48000 Hz)
- **Filter order**: Higher = steeper rolloff but more CPU
- **Passband ripple**: Acceptable variation in passband (dB)

### Step 2: Run the Filter Designer

Use the provided script to interactively design filters:

```bash
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/dsp-filter-designer/filter_designer.py \
  --type lowpass \
  --cutoff 15000 \
  --sample-rate 48000 \
  --order 5
```

Parameters:
- `--type`: Filter type (lowpass, highpass, bandpass, notch)
- `--cutoff`: Cutoff frequency in Hz (or low,high for bandpass/notch)
- `--sample-rate`: Sample rate in Hz (default: 48000)
- `--order`: Filter order 1-10 (default: 5)
- `--filter-design`: butterworth, chebyshev1, chebyshev2, elliptic (default: butterworth)
- `--ripple`: Passband ripple in dB for Chebyshev/Elliptic (default: 0.5)
- `--output`: Save plots to file instead of displaying
- `--export-code`: Generate Python code for wavecapsdr/dsp/filters.py

### Step 3: Interpret Results

The script outputs:

**Frequency Response:**
- Shows magnitude response in dB vs frequency
- Verify cutoff is where expected (-3 dB point)
- Check stopband attenuation is sufficient
- Look for passband ripple

**Phase Response:**
- Shows phase shift vs frequency
- Linear phase = no distortion (difficult to achieve with IIR)
- Non-linear phase can cause audio artifacts

**Impulse Response:**
- Shows filter's time-domain behavior
- Long impulse response = more "ringing"
- Short impulse response = faster transient response

**Filter Coefficients:**
- Prints b (numerator) and a (denominator) coefficients
- These can be used directly with scipy.signal.lfilter()

### Step 4: Test with Real Signals

Test the filter with actual audio:

```bash
# Generate test code that applies filter to a signal
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/dsp-filter-designer/filter_designer.py \
  --type lowpass \
  --cutoff 15000 \
  --sample-rate 48000 \
  --order 5 \
  --export-code
```

This generates code like:

```python
from scipy.signal import butter, lfilter

def apply_lowpass_filter(signal, sample_rate=48000):
    """Apply 15000 Hz lowpass filter (5th order Butterworth)"""
    nyquist = sample_rate / 2
    cutoff_norm = 15000 / nyquist
    b, a = butter(5, cutoff_norm, btype='low', analog=False)
    return lfilter(b, a, signal)
```

### Step 5: Integrate into WaveCap-SDR

Add the filter to `backend/wavecapsdr/dsp/filters.py`:

```python
def lowpass_filter(signal: np.ndarray, cutoff_hz: float, sample_rate: int, order: int = 5) -> np.ndarray:
    """Apply Butterworth lowpass filter"""
    from scipy.signal import butter, lfilter

    nyquist = sample_rate / 2
    cutoff_norm = cutoff_hz / nyquist
    b, a = butter(order, cutoff_norm, btype='low', analog=False)
    return lfilter(b, a, signal)
```

Then use in demodulation pipeline (e.g., `wavecapsdr/dsp/fm.py`):

```python
# After demodulation, apply de-emphasis filter
audio = lowpass_filter(audio, cutoff_hz=15000, sample_rate=audio_rate)
```

## Common Filter Use Cases

### 1. FM De-emphasis Filter
```bash
# 15 kHz lowpass for FM broadcast de-emphasis
.claude/skills/dsp-filter-designer/filter_designer.py \
  --type lowpass --cutoff 15000 --order 5
```

### 2. SSB Audio Bandpass
```bash
# 300-3000 Hz bandpass for SSB voice
.claude/skills/dsp-filter-designer/filter_designer.py \
  --type bandpass --cutoff 300,3000 --order 4
```

### 3. DC Blocking Highpass
```bash
# 20 Hz highpass to remove DC offset
.claude/skills/dsp-filter-designer/filter_designer.py \
  --type highpass --cutoff 20 --order 2
```

### 4. Notch Filter for Interference
```bash
# 60 Hz notch to remove AC hum
.claude/skills/dsp-filter-designer/filter_designer.py \
  --type notch --cutoff 60 --order 4
```

## Filter Design Trade-offs

**Filter Order:**
- Higher order = steeper rolloff, better frequency selectivity
- Higher order = more CPU, potential instability, longer transients
- Typical: 4-6 for audio, 2-3 for computational efficiency

**Filter Type:**
- **Butterworth**: Maximally flat passband, gentle rolloff (most common)
- **Chebyshev Type I**: Steeper rolloff, passband ripple
- **Chebyshev Type II**: Steeper rolloff, stopband ripple
- **Elliptic**: Steepest rolloff, both passband and stopband ripple

**Analog vs Digital:**
- All filters in WaveCap-SDR are digital (discrete-time)
- Design in normalized frequency (0 to 1, where 1 = Nyquist)
- Nyquist frequency = sample_rate / 2

## Technical Details

**Filter Implementation:**
WaveCap-SDR uses scipy.signal IIR filters (Infinite Impulse Response):

```python
from scipy.signal import butter, lfilter

# Design filter (returns coefficients)
b, a = butter(N=order, Wn=cutoff_normalized, btype='low')

# Apply filter (stateless, per-chunk processing)
filtered = lfilter(b, a, signal)
```

**Stateful Filtering:**
For streaming applications, maintain filter state between chunks:

```python
from scipy.signal import lfilter_zi

# Initialize state
zi = lfilter_zi(b, a) * signal[0]

# Apply filter with state
filtered, zi = lfilter(b, a, signal, zi=zi)
```

**Frequency Normalization:**
- Cutoff frequencies are normalized to Nyquist (sample_rate / 2)
- Example: 15 kHz cutoff at 48 kHz sample rate → 15000 / 24000 = 0.625

## Files in This Skill

- `SKILL.md`: This file - instructions for using the skill
- `filter_designer.py`: Interactive filter design and visualization tool

## Notes

- Always test filters with real audio before deployment
- Check for numerical instability (very high orders can be unstable)
- Consider FIR filters for linear phase requirements (not yet implemented)
- Profile CPU usage when adding filters to real-time pipeline
- Use `matplotlib` for visualization (interactive plots)
