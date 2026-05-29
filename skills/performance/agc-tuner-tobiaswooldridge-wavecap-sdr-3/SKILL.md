---
name: agc-tuner
description: Analyze and optimize AGC (Automatic Gain Control) parameters for WaveCap-SDR channels. Use when audio is too quiet, too loud, has pumping artifacts, or when tuning AGC attack/release/target settings for FM/AM/SSB modes.
---

# AGC Tuner for WaveCap-SDR

This skill helps analyze audio dynamics and optimize AGC (Automatic Gain Control) parameters for different demodulation modes.

## When to Use This Skill

Use this skill when:
- Audio output is too quiet or too loud
- Audio has "pumping" or "breathing" artifacts (AGC responding too fast/slow)
- Setting up AGC for a new demodulation mode (AM, SSB, digital)
- Comparing AGC behavior between channels
- Debugging why AGC isn't controlling gain properly
- Finding optimal attack_time, release_time, and target_level

## How It Works

The skill provides tools to:

1. **Analyze audio dynamics** - Measure RMS levels, peak levels, crest factor over time
2. **Visualize AGC behavior** - Plot gain adjustments, signal envelope, output level
3. **Suggest optimal parameters** - Recommend attack/release times based on signal characteristics
4. **Compare settings** - A/B test different AGC configurations

## AGC Background

WaveCap-SDR's AGC (in `backend/wavecapsdr/dsp/agc.py`) maintains consistent audio output level:

```python
class AGC:
    def __init__(self, attack_time: float, release_time: float, target_level: float):
        self.attack_alpha = 1.0 - np.exp(-1.0 / (attack_time * sample_rate))
        self.release_alpha = 1.0 - np.exp(-1.0 / (release_time * sample_rate))
        self.target_level = target_level
        self.current_gain = 1.0
```

**Key Parameters:**
- `attack_time`: How quickly AGC responds to increases in signal level (seconds)
- `release_time`: How quickly AGC responds to decreases in signal level (seconds)
- `target_level`: Desired RMS output level (0.0 to 1.0, typically 0.1-0.3)

## Usage Instructions

### Step 1: Identify Channel to Analyze

Find the channel you want to optimize:

```bash
curl http://127.0.0.1:8087/api/v1/captures | jq '.[] | .channels'
```

Note the channel ID (e.g., "ch1") and current AGC settings.

### Step 2: Capture Audio and Analyze Dynamics

Run the AGC analyzer to capture audio and measure dynamics:

```bash
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/agc-tuner/agc_analyzer.py \
  --channel ch1 \
  --duration 10 \
  --port 8087
```

Parameters:
- `--channel`: Channel ID to analyze (default: ch1)
- `--duration`: Seconds of audio to capture (default: 10)
- `--port`: Server port (default: 8087)
- `--host`: Server host (default: 127.0.0.1)
- `--attack`: Test attack time in seconds (default: current AGC setting)
- `--release`: Test release time in seconds (default: current AGC setting)
- `--target`: Test target level 0.0-1.0 (default: current AGC setting)
- `--plot`: Generate plots of AGC behavior
- `--output`: Save plots to file

### Step 3: Interpret Results

The script outputs:

**Signal Characteristics:**
- **RMS Level**: Average signal power over time
- **Peak Level**: Maximum amplitude
- **Crest Factor**: Peak/RMS ratio (high = dynamic, low = compressed)
- **Dynamic Range**: Difference between loudest and quietest parts

**AGC Behavior:**
- **Gain Variation**: How much AGC is adjusting gain
- **Settling Time**: How long AGC takes to stabilize
- **Overshoot**: Does AGC overcorrect?
- **Pumping Detection**: Rapid gain changes indicating poor settings

**Recommendations:**
The script suggests optimal attack/release times based on signal type.

### Step 4: Typical AGC Settings by Mode

**FM Broadcast (Music/Talk):**
```python
attack_time = 0.010   # 10ms - respond quickly to peaks
release_time = 0.500  # 500ms - slow release to avoid pumping
target_level = 0.2    # 20% RMS output
```

**AM/SSB Voice:**
```python
attack_time = 0.005   # 5ms - fast attack for speech peaks
release_time = 0.300  # 300ms - moderate release
target_level = 0.25   # 25% RMS output (voice needs more headroom)
```

**Digital Modes (P25, DMR):**
```python
attack_time = 0.001   # 1ms - very fast attack
release_time = 0.100  # 100ms - fast release
target_level = 0.3    # 30% RMS output (digital is pre-compressed)
```

**NOAA Weather Radio:**
```python
attack_time = 0.020   # 20ms - moderate attack
release_time = 0.800  # 800ms - very slow release (steady signal)
target_level = 0.15   # 15% RMS output (avoid distortion)
```

### Step 5: Update Channel AGC Settings

Update AGC parameters via API:

```bash
# Update AGC settings for channel
curl -X PATCH http://127.0.0.1:8087/api/v1/channels/ch1 \
  -H "Content-Type: application/json" \
  -d '{
    "agcAttackMs": 10,
    "agcReleaseMs": 500,
    "agcTargetDb": -20
  }'

# Note: Channel settings can be updated while running (no restart needed)
```

Or update in `backend/config/wavecapsdr.yaml` presets/recipes.

## Common AGC Issues and Solutions

### Issue: Audio Too Quiet
**Symptoms**: Output barely audible even at full volume
**Diagnosis**: Target level too low, or source signal very weak
**Solution**:
- Increase `target_level` from 0.1 to 0.3
- Check if antenna/tuning is good (use audio-quality-checker skill)
- Verify channel is started and streaming

### Issue: Audio Pumping/Breathing
**Symptoms**: Volume swells up and down, "breathing" artifacts
**Diagnosis**: Release time too fast for signal characteristics
**Solution**:
- Increase `release_time` (e.g., 0.1 → 0.5 seconds)
- For steady signals (NOAA weather), use very slow release (0.8-1.0s)
- For music, use 0.3-0.5s release

### Issue: Clipping/Distortion
**Symptoms**: Audio sounds distorted, harsh, broken up
**Diagnosis**: Target level too high, or attack time too slow
**Solution**:
- Decrease `target_level` (e.g., 0.3 → 0.15)
- Decrease `attack_time` to catch peaks faster (e.g., 0.02 → 0.005)
- Check for overmodulation at source (reduce SDR gain)

### Issue: Slow Response to Level Changes
**Symptoms**: AGC doesn't adjust quickly enough when switching between quiet/loud
**Diagnosis**: Attack time too slow
**Solution**:
- Decrease `attack_time` (e.g., 0.05 → 0.01 seconds)
- Be careful not to go too fast or AGC will respond to individual waveforms

## Advanced: Testing Parameter Sweeps

Test multiple AGC configurations and compare:

```bash
# Test attack times from 1ms to 50ms
for attack in 0.001 0.005 0.010 0.020 0.050; do
  echo "Testing attack_time=$attack"
  PYTHONPATH=backend backend/.venv/bin/python .claude/skills/agc-tuner/agc_analyzer.py \
    --channel ch1 \
    --duration 5 \
    --attack $attack \
    --release 0.5 \
    --target 0.2 \
    --output "agc_test_attack_${attack}.png"
done
```

Compare the output plots to find optimal settings.

## Technical Details

**AGC Algorithm:**
The AGC uses exponential smoothing to track signal envelope:

```python
# Compute signal envelope (RMS)
envelope = sqrt(mean(signal^2))

# Compute desired gain
desired_gain = target_level / envelope

# Smooth gain changes
if desired_gain < current_gain:
    # Attack: signal increased, reduce gain quickly
    current_gain += attack_alpha * (desired_gain - current_gain)
else:
    # Release: signal decreased, increase gain slowly
    current_gain += release_alpha * (desired_gain - current_gain)

# Apply gain
output = signal * current_gain
```

**Time Constants:**
Attack/release times are converted to smoothing factors (alpha):
```python
alpha = 1.0 - exp(-1.0 / (time_constant * sample_rate))
```

- Larger time constant → slower response (smaller alpha)
- Smaller time constant → faster response (larger alpha)

**Headroom:**
AGC maintains headroom to avoid clipping:
- Target level of 0.2 means output RMS is 20% of full scale
- This leaves ~14 dB of headroom for peaks (crest factor ~5)

## Files in This Skill

- `SKILL.md`: This file - instructions for using the skill
- `agc_analyzer.py`: Audio dynamics analyzer and AGC simulator

## Notes

- AGC operates on demodulated audio (after FM/AM demodulation)
- For best results, test with real signals (not test tones)
- AGC settings are per-channel, not global
- Extremely fast attack times (<1ms) can cause distortion
- Very slow release times (>2s) can make AGC unresponsive
- Target level around 0.2 (20%) is a good starting point
