---
name: device-prober
description: Probe and test SDR hardware capabilities (RTL-SDR, SDRplay, HackRF, etc.). Use when verifying device detection, discovering supported sample rates and gains, testing antenna ports, or troubleshooting SDR hardware issues.
---

# Device Prober for WaveCap-SDR

This skill helps probe SDR hardware to discover capabilities, test configurations, and troubleshoot device issues.

## When to Use This Skill

Use this skill when:
- New SDR device not detected or working
- Need to discover supported sample rates and frequencies
- Testing different antenna ports or gain settings
- Verifying device-specific features (bias-T, direct sampling, etc.)
- Troubleshooting "device not found" errors
- Comparing multiple SDR devices
- Finding optimal settings for a specific device
- Documenting device capabilities

## How It Works

The skill uses SoapySDR APIs to:

1. **Enumerate devices** - Find all connected SDR hardware
2. **Query capabilities** - Sample rates, gain ranges, antennas, frequencies
3. **Test configurations** - Verify settings work before using in WaveCap-SDR
4. **Generate reports** - Document device specs for reference

## Usage Instructions

### Step 1: List All SDR Devices

Find all connected SDR devices using SoapySDRUtil:

```bash
# Using SoapySDRUtil (if installed)
SoapySDRUtil --find

# Or use the probe script
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/device-prober/probe_device.py --list
```

Example output:
```
Found 2 devices:
  [0] driver=rtlsdr, serial=00000001
      RTL2838UHIDIR, manufacturer=Realtek, product=RTL2838UHIDIR
  [1] driver=sdrplay, serial=240309F070
      SDRplay Dev1, model=RSPdx
```

### Step 2: Probe Specific Device

Get detailed capabilities for a device:

```bash
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/device-prober/probe_device.py \
  --device "driver=rtlsdr"
```

Parameters:
- `--device`: Device selector string (e.g., "driver=rtlsdr", "driver=sdrplay,serial=ABC123")
- `--output`: Save report to JSON file
- `--test-capture`: Test actual capture (verify device works)
- `--test-duration`: Seconds for test capture (default: 2)

### Step 3: Interpret Results

The probe script outputs:

**Device Information:**
- Driver name (rtlsdr, sdrplay, hackrf, etc.)
- Hardware ID, serial number
- Manufacturer, product name

**Frequency Ranges:**
- Supported tuning ranges (e.g., 24 MHz - 1.7 GHz for RTL-SDR)
- Channel count (usually 1 for SDR receivers)

**Sample Rates:**
- Supported sample rates (e.g., 225 kHz - 3.2 MHz for RTL-SDR)
- Recommended rates for best performance

**Gain Settings:**
- Available gain elements (LNA, VGA, IF, etc.)
- Gain ranges in dB
- Automatic gain control (AGC) support

**Antenna Ports:**
- Available antenna connectors
- Default antenna selection

**Advanced Features:**
- Bias-T support (power LNA through antenna port)
- Direct sampling mode (HF reception on RTL-SDR)
- Clock references
- Sensor information (temperature, etc.)

### Step 4: Test Device Configuration

Verify a specific configuration works:

```bash
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/device-prober/probe_device.py \
  --device "driver=rtlsdr" \
  --test-capture \
  --test-duration 5
```

This performs a short capture to verify:
- Device can be opened
- Sample rate configuration works
- IQ samples are being received
- No errors or timeouts

## Common Device Configurations

### RTL-SDR (RTL2832U)

**Device String:**
```
driver=rtlsdr
```

**Typical Capabilities:**
- Frequency: 24 MHz - 1.766 GHz (with gap 1.1-1.25 GHz)
- Sample rate: 225 kHz - 3.2 MHz (optimal: 2-2.4 MHz)
- Gain: 0-50 dB (typically use 20-40 dB)
- Antennas: RX (single input)
- Features: Bias-T (some models), direct sampling (HF mode)

**Recommended Settings:**
```yaml
device_args: "driver=rtlsdr"
sample_rate: 2048000  # 2.048 MHz
gain_db: 30
```

**Direct Sampling for HF (<30 MHz):**
```yaml
device_args: "driver=rtlsdr,direct_samp=2"  # Q-branch for HF
```

### SDRplay RSP1A/RSPdx

**Device String:**
```
driver=sdrplay,serial=YOUR_SERIAL
```

**Typical Capabilities:**
- Frequency: 1 kHz - 2 GHz
- Sample rate: 62.5 kHz - 10 MHz
- Gain: LNA 0-27 dB, IF -59 to 0 dB
- Antennas: A, B, Hi-Z (RSPdx)
- Features: Bias-T, notch filters

**Recommended Settings:**
```yaml
device_args: "driver=sdrplay,serial=240309F070"
sample_rate: 2000000  # 2 MHz
gain_db: 40
antenna: "Antenna A"
```

### HackRF One

**Device String:**
```
driver=hackrf
```

**Typical Capabilities:**
- Frequency: 1 MHz - 6 GHz
- Sample rate: 2-20 MHz
- Gain: LNA 0-40 dB, VGA 0-62 dB
- TX capable (not used in WaveCap-SDR)

**Recommended Settings:**
```yaml
device_args: "driver=hackrf"
sample_rate: 8000000  # 8 MHz
gain_db: 32  # Combined LNA+VGA
```

### Airspy R2/Mini

**Device String:**
```
driver=airspy
```

**Typical Capabilities:**
- Frequency: 24 MHz - 1.8 GHz
- Sample rate: 2.5 or 10 MHz
- Gain: Multiple stages, 0-21 dB total
- High dynamic range

## Troubleshooting Device Issues

### Issue: Device Not Detected

**Diagnosis:**
```bash
# Check if SoapySDR sees the device
SoapySDRUtil --find

# Check USB devices (Linux)
lsusb | grep -E "RTL|Realtek|Airspy|HackRF"

# Check kernel modules (Linux)
lsmod | grep -E "rtl|sdr"
```

**Solutions:**
- Install SoapySDR driver for your device
- Check USB cable (try different port/cable)
- Verify device permissions (udev rules on Linux)
- Update firmware (SDRplay, Airspy, etc.)

### Issue: "Failed to open device"

**Diagnosis:**
```bash
# Check if another process is using the device
lsof | grep SDR
ps aux | grep -E "gqrx|sdr|cubic"
```

**Solutions:**
- Close other SDR software (GQRX, SDR#, CubicSDR)
- Kill zombie processes: `pkill -f sdr`
- Unplug and replug device
- Reboot system

### Issue: Poor Signal Quality

**Diagnosis:**
```bash
# Test with known good frequency (FM broadcast)
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/device-prober/probe_device.py \
  --device "driver=rtlsdr" \
  --test-capture \
  --test-duration 5
```

**Solutions:**
- Check antenna connection (tight SMA connector)
- Try different antenna (appropriate for frequency)
- Adjust gain (too high = overload, too low = weak signal)
- Move away from interference sources (computers, USB3)
- Use shielded USB cable

### Issue: Sample Rate Not Supported

**Diagnosis:**
```bash
# Query supported rates
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/device-prober/probe_device.py \
  --device "driver=rtlsdr"
```

Look for "Sample Rates" section.

**Solutions:**
- Use supported sample rate from device capabilities
- RTL-SDR: Use 2.048 MHz or 2.4 MHz (avoid 2.8-3.2 MHz unless needed)
- SDRplay: Use 2 MHz for compatibility
- HackRF: Use 8 MHz or 10 MHz

## Advanced: Device-Specific Settings

### RTL-SDR Bias-T

Enable bias-T to power LNA through antenna port:

```yaml
device_args: "driver=rtlsdr,bias_tee=1"
```

**Warning:** Only use with LNA that expects bias-T. Can damage amplifiers not designed for it.

### SDRplay Antenna Selection

Select antenna port (RSPdx):

```yaml
device_args: "driver=sdrplay,serial=240309F070"
antenna: "Antenna B"  # or "Antenna A", "Hi-Z"
```

### SDRplay Notch Filters

Enable FM/DAB notch filters:

```yaml
device_args: "driver=sdrplay,rfnotch_ctrl=1,dabnotch_ctrl=1"
```

### HackRF Amplifier

Enable RX amplifier:

```yaml
device_args: "driver=hackrf,amp=1"
```

## Integration with WaveCap-SDR

After probing device, update `backend/config/wavecapsdr.yaml`:

```yaml
device:
  driver: soapy  # Use SoapySDR driver
  device_args:
    - "driver=rtlsdr"  # Or device string from probe

presets:
  my_device:
    center_hz: 100000000  # From frequency range
    sample_rate: 2048000  # From supported rates
    gain_db: 30  # From gain range
    antenna: "RX"  # From available antennas
```

## Files in This Skill

- `SKILL.md`: This file - instructions for using the skill
- `probe_device.py`: Device capability probe script

## Notes

- Always check device permissions on Linux (udev rules)
- Some features require specific firmware versions
- Direct sampling (RTL-SDR HF mode) has reduced performance
- Gain is device-specific (RTL-SDR uses single gain, SDRplay uses LNA+IF)
- Sample rates outside native range may have degraded performance
- Use `SoapySDRUtil --probe=driver=xxx` for maximum detail
