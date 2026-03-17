---
name: capture-health-check
description: End-to-end health check for WaveCap-SDR captures. Use when captures are stuck in "starting" state, spectrum analyzer not updating, audio not playing, or to verify the system is working correctly.
---

# Capture Health Check for WaveCap-SDR

This skill performs end-to-end verification of WaveCap-SDR captures, detecting stuck captures, missing audio, and spectrum issues.

## When to Use This Skill

Use this skill when:
- Spectrum analyzer shows "Starting capture" indefinitely
- Audio is not playing from a channel
- Capture is stuck in "starting" or "failed" state
- After fixing SDRplay service issues to verify captures recovered
- For general system health verification

## Quick Health Check

Run this to check all captures:

```bash
curl -s http://localhost:8087/api/v1/health | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"Overall: {data['status']}\")
print()

# Check captures
caps = data['checks'].get('captures', {})
print('Captures:')
for c in caps.get('captures', []):
    status = '✓' if c['state'] == 'running' else '✗'
    print(f\"  {status} {c['id']}: {c['state']} - {c['device_id'][:40]}...\")
print()

# Check channels
chans = data['checks'].get('channels', {})
print('Channels:')
for ch in chans.get('channels', []):
    status = '✓' if ch['state'] == 'running' else '✗'
    print(f\"  {status} {ch['id']}: {ch['state']} ({ch['mode']})\")
"
```

## Diagnosing Stuck Captures

### Check 1: Capture State

A capture stuck in "starting" for more than 5 seconds indicates a problem.

```bash
# Get detailed capture info
curl -s http://localhost:8087/api/v1/captures | python3 -c "
import sys, json
for c in json.load(sys.stdin):
    print(f\"Capture {c['id']}:\")
    print(f\"  State: {c['state']}\")
    print(f\"  Device: {c['deviceId'][:60]}...\")
    print(f\"  Antenna: {c.get('antenna') or 'NOT SET (stuck?)'}\")
    print(f\"  Error: {c.get('errorMessage') or 'None'}\")
    print()
"
```

**Indicators of stuck capture:**
- `state: starting` for >5 seconds
- `antenna: null` (device never fully initialized)
- No `errorMessage` but still not running

### Check 2: Device Availability

Verify the SDR device is accessible outside WaveCap:

```bash
# Test SoapySDR enumeration (should complete in <5 seconds)
SoapySDRUtil --find

# If this hangs, the SDRplay service is stuck - run:
sudo /bin/launchctl kickstart -kp system/com.sdrplay.service
```

### Check 3: Spectrum Data Flow

Test if spectrum data is being generated:

```bash
# Fetch spectrum snapshot
curl -s http://localhost:8087/api/v1/captures/c1/spectrum/snapshot | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    power = data.get('power', [])
    if power:
        print(f'Spectrum OK: {len(power)} bins, range {min(power):.1f} to {max(power):.1f} dB')
    else:
        print('ERROR: No spectrum data')
except:
    print('ERROR: Invalid response')
"
```

### Check 4: Audio Flow

Test if audio is being demodulated:

```bash
# Check channel metrics (should have signal power)
curl -s http://localhost:8087/api/v1/channels | python3 -c "
import sys, json
for ch in json.load(sys.stdin):
    rssi = ch.get('rssiDb')
    audio_rms = ch.get('audioRmsDb')
    status = '✓' if rssi and audio_rms else '?'
    print(f\"{status} {ch['id']}: RSSI={rssi or 'N/A'} dB, Audio RMS={audio_rms or 'N/A'} dB\")
"
```

## Common Issues and Fixes

### Issue: Capture Stuck in "starting" (SDRplay)

**Cause:** SDRplay API service was stuck when capture tried to start.

**Fix:**
1. Restart SDRplay service:
   ```bash
   sudo /bin/launchctl kickstart -kp system/com.sdrplay.service
   ```
2. Delete and recreate the stuck capture:
   ```bash
   curl -X DELETE http://localhost:8087/api/v1/captures/c2
   curl -X POST http://localhost:8087/api/v1/captures \
     -H "Content-Type: application/json" \
     -d '{"deviceId": "driver=sdrplay,serial=YOUR_SERIAL", "centerHz": 90300000, "sampleRate": 1000000}'
   ```
3. If still stuck, restart the WaveCap server (device reference may be stale)

### Issue: Capture Stuck in "starting" (After Service Fix)

**Cause:** Server has stale device reference from previous failed capture.

**Fix:** Restart the WaveCap server:
```bash
# Find and kill the server
pkill -f "python.*wavecapsdr"
# Restart (from project root)
./start-app.sh
```

### Issue: Spectrum Shows Noise Only

**Possible causes:**
- Antenna not connected
- Wrong antenna port selected
- Gain too low

**Check:**
```bash
curl -s http://localhost:8087/api/v1/captures/c1 | python3 -c "
import sys, json
c = json.load(sys.stdin)
print(f\"Antenna: {c.get('antenna')}\")
print(f\"Gain: {c.get('gain')} dB\")
"
```

### Issue: No Audio Despite Good Spectrum

**Possible causes:**
- Channel not started
- Wrong offset (channel not on signal)
- Squelch too high

**Check:**
```bash
curl -s http://localhost:8087/api/v1/channels | python3 -c "
import sys, json
for ch in json.load(sys.stdin):
    print(f\"{ch['id']}: state={ch['state']}, offset={ch['offsetHz']}Hz, squelch={ch.get('squelchDb')}dB, rssi={ch.get('rssiDb')}dB\")
"
```

## Full E2E Verification Script

Save this as a script for complete system verification:

```bash
#!/bin/bash
echo "=== WaveCap-SDR E2E Health Check ==="
echo

# 1. Check server is responding
echo "1. Server status:"
if curl -s http://localhost:8087/api/v1/health > /dev/null 2>&1; then
    echo "   ✓ Server responding"
else
    echo "   ✗ Server not responding"
    exit 1
fi

# 2. Check devices
echo
echo "2. SDR Devices:"
curl -s http://localhost:8087/api/v1/devices | python3 -c "
import sys, json
devs = json.load(sys.stdin)
for d in devs:
    print(f\"   ✓ {d['driver']}: {d['label']}\")
if not devs:
    print('   ✗ No devices found')
"

# 3. Check captures
echo
echo "3. Captures:"
STUCK=$(curl -s http://localhost:8087/api/v1/captures | python3 -c "
import sys, json
stuck = 0
for c in json.load(sys.stdin):
    status = '✓' if c['state'] == 'running' else '✗'
    antenna = c.get('antenna') or 'N/A'
    print(f\"   {status} {c['id']}: {c['state']} (antenna: {antenna})\")
    if c['state'] == 'starting':
        stuck += 1
print(stuck)
" | tail -1)

if [ "$STUCK" -gt 0 ]; then
    echo
    echo "   WARNING: $STUCK capture(s) stuck in 'starting' state!"
fi

# 4. Check channels and audio
echo
echo "4. Channels (audio flow):"
curl -s http://localhost:8087/api/v1/channels | python3 -c "
import sys, json
for ch in json.load(sys.stdin):
    rssi = ch.get('rssiDb')
    audio = ch.get('audioRmsDb')
    if ch['state'] != 'running':
        status = '✗'
        note = 'not running'
    elif rssi is None:
        status = '?'
        note = 'no RSSI (capture not running?)'
    elif audio is None or audio < -80:
        status = '~'
        note = 'weak/no audio'
    else:
        status = '✓'
        note = f'RSSI={rssi:.0f}dB, audio={audio:.0f}dB'
    print(f\"   {status} {ch['id']}: {note}\")
"

echo
echo "=== Check Complete ==="
```

## Integration with Claude Code

When Claude Code encounters capture issues:

1. First run the quick health check
2. If captures are stuck, check device availability
3. If SDRplay device times out, run the sdrplay-service-fix skill
4. After fixing SDRplay, restart stuck captures or the server if needed
5. Verify fix with the full E2E script
