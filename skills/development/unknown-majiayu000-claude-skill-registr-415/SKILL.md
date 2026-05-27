---
name: harness-runner
description: Run WaveCap-SDR test harness with automated parameter sweeps and validation. Use when regression testing, validating audio quality across configurations, testing SDR hardware, or benchmarking demodulation performance.
---

# Harness Runner for WaveCap-SDR

This skill helps run the WaveCap-SDR test harness with automated parameter sweeps, result collection, and regression testing.

## When to Use This Skill

Use this skill when:
- Running regression tests after code changes
- Validating audio quality across different configurations
- Testing SDR hardware (RTL-SDR, SDRplay, etc.)
- Benchmarking demodulation modes (FM, AM, SSB)
- Comparing different AGC or filter settings
- Testing with multiple frequencies or channels
- Automated CI/CD testing
- Generating test reports for documentation

## How It Works

The WaveCap-SDR harness (`backend/wavecapsdr/harness.py`) is a production-ready test tool that:

1. **Starts a server** (optional) with specified configuration
2. **Creates a capture** with SDR device or fake driver
3. **Adds channels** with specified demodulation settings
4. **Captures audio** for a duration and measures quality metrics
5. **Returns results** with RMS levels, peak levels, and pass/fail status

This skill wraps the harness for automated testing scenarios.

## Usage Instructions

### Basic Harness Usage

**Test with Fake Driver (Offline Testing):**
```bash
cd backend
PYTHONPATH=. .venv/bin/python -m wavecapsdr.harness \
  --start-server \
  --driver fake \
  --preset kexp \
  --duration 3
```

**Test with Real SDR (RTL-SDR):**
```bash
cd backend
PYTHONPATH=. .venv/bin/python -m wavecapsdr.harness \
  --start-server \
  --driver soapy \
  --device-args "driver=rtlsdr" \
  --preset kexp \
  --duration 5 \
  --out harness_out
```

**Test with SDRplay:**
```bash
cd backend
PYTHONPATH=. .venv/bin/python -m wavecapsdr.harness \
  --start-server \
  --driver soapy \
  --device-args "driver=sdrplay,serial=240309F070" \
  --preset marine \
  --duration 5
```

### Advanced: Parameter Sweeps

Use the included script to run parameter sweeps:

```bash
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/harness-runner/run_harness.py \
  --preset kexp \
  --duration 3 \
  --driver fake \
  --sweep gain --gain-values 10 20 30 40
```

Parameters:
- `--preset`: Preset name (kexp, marine, aviation, tone, etc.)
- `--duration`: Seconds to capture per test (default: 3)
- `--driver`: Driver to use (fake, soapy, rtl)
- `--device-args`: Device selector string
- `--output-dir`: Directory for results (default: harness_results)
- `--sweep`: Parameter to sweep (gain, bandwidth, frequency)
- `--gain-values`: List of gain values to test (for gain sweep)
- `--bandwidth-values`: List of bandwidth values (for bandwidth sweep)
- `--frequency-offsets`: List of frequency offsets (for frequency sweep)
- `--parallel`: Run tests in parallel (default: sequential)
- `--report`: Generate HTML/JSON report

### Example Workflows

**1. Regression Testing After Code Changes:**

```bash
# Run quick smoke test with fake driver
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/harness-runner/run_harness.py \
  --preset kexp \
  --duration 2 \
  --driver fake \
  --output-dir regression_test_$(date +%Y%m%d_%H%M%S) \
  --report
```

Expected: All channels should have audio RMS > -40 dB (validates demodulation works)

**2. Find Optimal Gain for SDR Device:**

```bash
# Sweep gain from 0 to 50 dB in 10 dB steps
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/harness-runner/run_harness.py \
  --preset kexp \
  --duration 5 \
  --driver soapy \
  --device-args "driver=rtlsdr" \
  --sweep gain \
  --gain-values 0 10 20 30 40 50 \
  --output-dir gain_sweep_kexp \
  --report
```

Review report to find gain with best audio level (typically -20 to -10 dB RMS)

**3. Test All Presets with Fake Driver:**

```bash
# Test each preset to ensure they work
for preset in kexp marine aviation noaa tone; do
  echo "Testing preset: $preset"
  PYTHONPATH=backend backend/.venv/bin/python -m wavecapsdr.harness \
    --start-server \
    --driver fake \
    --preset $preset \
    --duration 3 \
    --out harness_out_$preset
done
```

**4. Compare FM Demodulation Quality:**

```bash
# Test FM demodulation with different configurations
# (Requires modifying harness to support demod parameter sweep)
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/harness-runner/run_harness.py \
  --preset kexp \
  --driver fake \
  --duration 5 \
  --output-dir fm_demod_test \
  --report
```

**5. Hardware Stress Test:**

```bash
# Long-duration test to check for memory leaks or crashes
PYTHONPATH=backend backend/.venv/bin/python -m wavecapsdr.harness \
  --start-server \
  --driver soapy \
  --device-args "driver=rtlsdr" \
  --preset kexp \
  --duration 300 \
  --out stress_test
```

Monitor server logs and system resources during test.

## Interpreting Harness Results

The harness outputs JSON reports with channel statistics:

```json
{
  "captureId": "cap_abc123",
  "channels": [
    {
      "channelId": "ch1",
      "label": "KEXP 90.3 FM",
      "offsetHz": -600000,
      "rmsDb": -18.5,
      "peakDb": -6.2,
      "status": "PASS"
    },
    {
      "channelId": "ch2",
      "label": "KNHC 89.5 FM",
      "offsetHz": 800000,
      "rmsDb": -65.2,
      "peakDb": -58.1,
      "status": "FAIL"
    }
  ]
}
```

**Pass/Fail Criteria:**
- **PASS**: RMS > -40 dB (audio is present and audible)
- **FAIL**: RMS < -40 dB (silence, noise, or tuning issue)
- **CLIP**: Peak > -0.5 dB (clipping detected, reduce gain)

**Typical Good Audio Levels:**
- RMS: -20 to -10 dB (strong, clear audio)
- RMS: -30 to -20 dB (moderate audio, acceptable)
- RMS: -40 to -30 dB (weak audio, may have noise)
- RMS: < -40 dB (too quiet, indicates problem)

## Common Presets

**KEXP (FM Broadcast):**
- Center: 90.3 MHz
- Sample rate: 2 MHz
- Channels: KEXP 90.3, KNHC 89.5
- Use for: FM demodulation testing

**Marine VHF:**
- Center: 156.8 MHz (Channel 16)
- Sample rate: 250 kHz
- Channels: Ch 16, Ch 9, Ch 6
- Use for: Narrowband FM testing

**Aviation:**
- Center: 118-137 MHz
- Channels: Tower, ATIS, Ground
- Use for: AM demodulation testing

**NOAA Weather:**
- Center: 162.550 MHz
- Channels: WX1, WX2
- Use for: Continuous broadcast testing

**Tone (Test Signal):**
- Fake driver generates 1 kHz test tone
- Use for: Offline testing without SDR hardware

## Harness Command-Line Options

```
--start-server       Start embedded server (required for offline testing)
--driver             Driver: fake, soapy, rtl (default: soapy)
--device-args        Device selector (e.g., "driver=rtlsdr")
--preset             Preset name (kexp, marine, aviation, etc.)
--center-hz          Override center frequency
--sample-rate        Override sample rate
--offset             Channel offset Hz (repeatable)
--duration           Seconds to capture (default: 10)
--gain               RF gain in dB
--bandwidth          RF bandwidth in Hz
--out                Output directory for WAV files
--auto-gain          Auto-select optimal gain
--probe-seconds      Seconds for auto-gain probing (default: 2)
```

## Integration with CI/CD

**GitHub Actions Example:**

```yaml
name: Test Harness
on: [push, pull_request]

jobs:
  harness:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          python -m venv .venv
          .venv/bin/pip install -e .
      - name: Run harness tests
        run: |
          cd backend
          PYTHONPATH=. .venv/bin/python -m wavecapsdr.harness \
            --start-server \
            --driver fake \
            --preset kexp \
            --duration 3
      - name: Check exit code
        run: |
          if [ $? -eq 0 ]; then
            echo "Harness tests PASSED"
          else
            echo "Harness tests FAILED"
            exit 1
          fi
```

## Troubleshooting

**Issue: Harness fails with "No audio detected"**
- Check if preset exists in config: `cat backend/config/wavecapsdr.yaml | grep -A 10 "preset-name"`
- Verify device connection: `SoapySDRUtil --find`
- Check antenna is connected
- Try fake driver first: `--driver fake`

**Issue: RMS levels very low (< -60 dB)**
- Increase gain: `--gain 30`
- Use auto-gain: `--auto-gain`
- Check if frequency is correct
- Verify antenna tuned for frequency range

**Issue: Clipping (peak > -0.5 dB)**
- Reduce gain: `--gain 10`
- Check for strong nearby signals
- Use AGC in demodulation

**Issue: Server port already in use**
- Change port: `--port 8088`
- Kill existing server: `pkill -f wavecapsdr`

## Files in This Skill

- `SKILL.md`: This file - instructions for using the skill
- `run_harness.py`: Parameter sweep automation script

## Notes

- Harness always returns non-zero exit code if any channel fails
- Use `--duration 3` for quick tests, `--duration 10+` for reliable results
- Fake driver is deterministic (same output every time)
- Real SDR results vary based on signal conditions
- Save WAV files with `--out` for manual inspection
- Auto-gain feature requires multiple iterations (slower but finds optimal gain)
