---
name: spectrum-analyzer-debug
description: Debug spectrum analyzer and waterfall display issues in WaveCap-SDR. Use when spectrum is not updating, shows incorrect frequencies, has poor resolution, excessive noise floor, or performance problems with FFT visualization.
---

# Spectrum Analyzer Debugger for WaveCap-SDR

This skill helps diagnose and fix issues with the spectrum analyzer and waterfall display in WaveCap-SDR.

## When to Use This Skill

Use this skill when:
- Spectrum display not updating or frozen
- Frequency labels are incorrect or misaligned
- FFT resolution too coarse or too fine
- Excessive noise floor obscuring signals
- Performance issues (low frame rate, high CPU usage)
- Waterfall colors incorrect or washed out
- Zoom/pan functionality not working properly
- WebSocket spectrum stream disconnecting

## Common Issues and Solutions

### Issue 1: Spectrum Not Updating

**Symptoms:**
- Spectrum display frozen
- Waterfall not scrolling
- "No data" or blank display

**Diagnosis Steps:**

1. **Check if capture is running:**
```bash
curl http://127.0.0.1:8087/api/v1/captures | jq '.[] | {id, status, center_hz}'
```
Look for `"status": "started"`. If stopped, start it:
```bash
curl -X POST http://127.0.0.1:8087/api/v1/captures/{capture_id}/start
```

2. **Check WebSocket connection:**
Open browser DevTools → Network → WS tab
- Should see active WebSocket to `/api/v1/stream/spectrum/...`
- Check for disconnect errors or 404s
- Verify correct capture ID in URL

3. **Verify spectrum stream endpoint:**
```bash
# List available captures
curl http://127.0.0.1:8087/api/v1/captures | jq

# Check spectrum snapshot (includes metadata: centerHz, sampleRate, fft_bins)
curl http://127.0.0.1:8087/api/v1/captures/{capture_id}/spectrum/snapshot | jq
```

4. **Check browser console for errors:**
- Open DevTools → Console
- Look for WebSocket errors, React errors, or data parsing issues
- Common: "WebSocket closed", "JSON parse error", "Undefined fft_bins"

**Solutions:**
- Restart capture if stopped
- Refresh browser to reconnect WebSocket
- Check server logs for spectrum streaming errors
- Verify `useSpectrumData` hook is properly configured in `SpectrumAnalyzer.react.tsx`

---

### Issue 2: Frequency Labels Incorrect

**Symptoms:**
- Frequency axis shows wrong values
- Signals appear at wrong frequencies
- Axis doesn't match center frequency

**Diagnosis:**

1. **Check capture center frequency:**
```bash
curl http://127.0.0.1:8087/api/v1/captures/{capture_id} | jq '.center_hz, .sample_rate'
```

2. **Verify FFT bin calculation:**
The spectrum should span from `(center_hz - sample_rate/2)` to `(center_hz + sample_rate/2)`

Example:
- Center: 100 MHz (100,000,000 Hz)
- Sample rate: 2 MHz (2,000,000 Hz)
- Spectrum range: 99 MHz to 101 MHz

3. **Check frontend frequency calculation:**
In `SpectrumAnalyzer.react.tsx`, verify:
```typescript
const startFreq = centerHz - (sampleRate / 2)
const endFreq = centerHz + (sampleRate / 2)
const freqPerBin = sampleRate / fftBins
```

**Solutions:**
- Update `centerHz` and `sampleRate` props passed to SpectrumAnalyzer
- Verify spectrum metadata includes correct `center_hz` and `sample_rate`
- Check for integer overflow in frequency calculations (use BigInt if needed)
- Ensure frequency labels use Hz → MHz/GHz conversion correctly

---

### Issue 3: Poor FFT Resolution

**Symptoms:**
- Spectrum looks "blocky" or pixelated
- Can't distinguish closely spaced signals
- Not enough detail in spectrum

**Diagnosis:**

1. **Check FFT size:**
```bash
curl http://127.0.0.1:8087/api/v1/captures/{capture_id}/spectrum/snapshot | jq '.power | length'
```

Typical FFT sizes: 512, 1024, 2048, 4096

2. **Calculate frequency resolution:**
```
Frequency resolution = sample_rate / fft_bins
```

Example:
- Sample rate: 2 MHz
- FFT bins: 1024
- Resolution: 2,000,000 / 1024 ≈ 1953 Hz per bin

**Solutions:**

- **Increase FFT size** for better frequency resolution (but slower updates):
  - Edit `backend/wavecapsdr/capture.py`
  - Look for `fft_size` or `nperseg` parameter in spectrum generation
  - Increase from 1024 to 2048 or 4096

- **Trade-offs:**
  - Larger FFT = better frequency resolution, slower update rate
  - Smaller FFT = faster updates, coarser frequency resolution
  - Typical good value: 2048 bins for SDR

- **Alternative: Use zoom feature** (if implemented)
  - Zoom into frequency range of interest
  - Higher effective resolution in zoomed view

---

### Issue 4: Excessive Noise Floor

**Symptoms:**
- Spectrum appears very "noisy"
- Weak signals buried in noise
- Hard to distinguish signal from noise

**Diagnosis:**

1. **Check if this is SDR noise or visualization artifact:**
```bash
# Capture audio and check actual signal quality
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/audio-quality-checker/analyze_audio_stream.py \
  --duration 3
```

2. **Verify dB scale:**
Check if spectrum is using proper dB scaling:
```python
# Should be: 20 * log10(magnitude) or 10 * log10(power)
spectrum_db = 20 * np.log10(np.abs(fft_result) + 1e-10)
```

**Solutions:**

- **Adjust SDR gain:**
  - If noise is from SDR, reduce RF gain
  - Update `gain_db` in capture configuration
  - Too much gain = overload and noise

- **Apply averaging:**
  - Average multiple FFT frames to reduce noise
  - Edit spectrum generation code to implement exponential smoothing:
    ```python
    smoothed_spectrum = alpha * new_spectrum + (1 - alpha) * smoothed_spectrum
    ```
  - Typical alpha: 0.3 (30% new, 70% old)

- **Adjust dB floor:**
  - Clip minimum dB value to improve visualization:
    ```python
    spectrum_db = np.clip(spectrum_db, -100, 0)  # Floor at -100 dB
    ```

- **Use windowing function:**
  - Apply Hann, Hamming, or Blackman window to reduce spectral leakage
  - Check if `scipy.signal.get_window()` is used in FFT computation

---

### Issue 5: Performance Problems

**Symptoms:**
- Spectrum updates slowly or stutters
- High CPU usage
- Browser tab freezes or lags

**Diagnosis:**

1. **Check FFT computation rate:**
```bash
# Monitor WebSocket data rate (requires WebSocket client like wscat)
# Install wscat: npm install -g wscat
wscat -c ws://127.0.0.1:8087/api/v1/stream/captures/{capture_id}/spectrum

# Count messages per second
```

2. **Profile frontend rendering:**
- Open React DevTools → Profiler
- Record spectrum display for 5 seconds
- Look for slow component renders
- Check if `SpectrumAnalyzer` or `WaterfallDisplay` re-rendering too often

3. **Check WebSocket message size:**
Large FFT bins = large messages
- 4096 bins × 4 bytes = 16 KB per frame
- At 10 FPS = 160 KB/s bandwidth

**Solutions:**

- **Reduce FFT update rate:**
  - Lower spectrum frame rate from 30 FPS to 10-15 FPS
  - Edit `capture.py` to throttle spectrum generation

- **Optimize React rendering:**
  - Use `React.memo()` for SpectrumAnalyzer component
  - Avoid recreating canvas on every update
  - Use `useRef()` for canvas element
  - Only redraw when new data arrives

- **Reduce FFT size:**
  - Use 1024 bins instead of 4096 for lower CPU usage
  - Consider dynamic FFT size based on zoom level

- **Use RequestAnimationFrame:**
  - Batch canvas redraws using `requestAnimationFrame()`
  - Prevents excessive rendering

- **Implement downsampling:**
  - If FFT has 4096 bins but canvas is 800px wide, downsample to ~800 points
  - Reduces rendering workload

---

### Issue 6: Waterfall Colors Incorrect

**Symptoms:**
- Waterfall too bright/dark
- Can't see weak signals
- Colors washed out or oversaturated

**Solutions:**

1. **Adjust color map range:**
```typescript
// In WaterfallDisplay.react.tsx
const minDb = -90  // Adjust to lowest dB value to show
const maxDb = -20  // Adjust to highest dB value to show

// Normalize to 0-255 range
const normalized = ((value - minDb) / (maxDb - minDb)) * 255
```

2. **Change color palette:**
- Common SDR palettes: "viridis", "plasma", "inferno", "turbo"
- Or custom: blue (weak) → green → yellow → red (strong)

3. **Apply gamma correction:**
```typescript
const gamma = 0.5  // <1 = brighter, >1 = darker
const corrected = Math.pow(normalized / 255, gamma) * 255
```

---

### Issue 7: WebSocket Disconnections

**Symptoms:**
- Spectrum updates then stops
- Frequent reconnections
- "WebSocket closed" in console

**Diagnosis:**

1. **Check server logs for errors:**
```bash
# Run server in foreground to see errors
cd backend
PYTHONPATH=. .venv/bin/python -m wavecapsdr.app
```

2. **Monitor WebSocket health:**
```javascript
// In browser console
window.addEventListener('beforeunload', () => {
  console.log('WebSocket state:', ws.readyState)
})
```

**Solutions:**

- **Implement reconnection logic:**
  - Auto-reconnect on disconnect with exponential backoff
  - Check `useSpectrumData` hook for reconnection handling

- **Add ping/pong:**
  - Send periodic ping messages to keep connection alive
  - Detect dead connections and reconnect

- **Check network issues:**
  - Firewall blocking WebSocket
  - Proxy/load balancer timeout
  - Network instability

---

## Spectrum Analyzer Technical Details

**FFT Pipeline:**
```
IQ samples → Windowing → FFT → Magnitude → dB conversion → Smoothing → WebSocket
```

**Key Files:**
- Backend: `backend/wavecapsdr/api.py` (spectrum WebSocket endpoint)
- Frontend: `frontend/src/components/primitives/SpectrumAnalyzer.react.tsx`
- Frontend: `frontend/src/components/primitives/WaterfallDisplay.react.tsx`
- Hook: `frontend/src/hooks/useSpectrumData.ts`

**FFT Parameters:**
- `nperseg`: FFT size (512, 1024, 2048, 4096)
- `window`: Window function (Hann, Hamming, Blackman)
- `noverlap`: Overlap between segments (0 to nperseg-1)
- `scaling`: 'spectrum' or 'density'

**Typical Good Settings:**
- FFT size: 2048
- Window: Hann
- Overlap: 50% (nperseg / 2)
- Update rate: 10-15 FPS
- Averaging: alpha = 0.3

## Useful Commands

**Monitor spectrum WebSocket:**
```bash
# Using wscat
npm install -g wscat
wscat -c ws://127.0.0.1:8087/api/v1/stream/spectrum/{capture_id}
```

**Test FFT generation:**
```python
# Quick FFT test in Python
import numpy as np
from scipy import signal

sample_rate = 2_000_000
iq_data = np.random.randn(sample_rate) + 1j * np.random.randn(sample_rate)

f, t, Sxx = signal.spectrogram(
    iq_data,
    fs=sample_rate,
    window='hann',
    nperseg=2048,
    noverlap=1024,
    scaling='spectrum',
    mode='magnitude'
)

print(f"Freq bins: {len(f)}, Time bins: {len(t)}")
print(f"Freq resolution: {(f[1] - f[0]) / 1e3:.2f} kHz")
```

## Files in This Skill

- `SKILL.md`: This file - diagnostic instructions and solutions

## Notes

- Always check backend logs when debugging spectrum issues
- Use browser DevTools Network tab to inspect WebSocket traffic
- Profile frontend with React DevTools before optimizing
- Spectrum quality depends on SDR tuning and antenna
- Consider implementing adjustable FFT parameters in UI for flexibility
