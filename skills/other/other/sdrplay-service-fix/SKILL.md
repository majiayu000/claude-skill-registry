---
name: sdrplay-service-fix
description: Fix stuck SDRplay API service that causes device enumeration to hang. Use when SoapySDRUtil --find hangs, SDRplay device times out, or the SDRplay RSP is unresponsive.
---

# SDRplay Service Fix for WaveCap-SDR

This skill helps diagnose and fix stuck SDRplay API service issues that prevent device enumeration.

## When to Use This Skill

Use this skill when:
- `SoapySDRUtil --find` hangs or takes more than 5 seconds
- SDRplay RSP device not detected but USB device is present
- WaveCap-SDR shows "device timeout" or "failed to open" for SDRplay
- Capture using SDRplay device won't start
- Device enumeration gets stuck

## Symptoms

1. **Hanging enumeration**: `SoapySDRUtil --find` never completes
2. **Timeout errors**: Device opens but times out during setup
3. **Service stuck**: `sdrplay_apiService` using excessive CPU or memory
4. **Device shows in USB but not in SoapySDR**: USB device present but not enumerated

## Diagnosis

### Step 1: Check if SDRplay USB Device is Connected

**macOS:**
```bash
system_profiler SPUSBDataType 2>/dev/null | grep -B5 -A10 "1df7\|SDRplay\|RSP"
```

**Linux:**
```bash
lsusb | grep -i "1df7\|sdrplay"
```

**Windows (PowerShell):**
```powershell
Get-PnpDevice -Class USB | Where-Object { $_.FriendlyName -match "SDRplay" }
```

### Step 2: Check SDRplay Service Status

**macOS:**
```bash
ps aux | grep -i sdrplay | grep -v grep
```

Expected output shows `sdrplay_apiService` running:
```
root  12345  0.0  0.1  123456  7890  ??  Ss   10:00AM  0:00.50 /Library/SDRplayAPI/3.15.1/bin/sdrplay_apiService
```

**Linux:**
```bash
systemctl status sdrplayService
# or
ps aux | grep -i sdrplay | grep -v grep
```

**Windows (PowerShell):**
```powershell
Get-Service SDRplayService
```

### Step 3: Test Device Enumeration with Timeout

**macOS/Linux:**
```bash
# Run SoapySDRUtil in background with manual timeout
SoapySDRUtil --find 2>&1 &
PID=$!
sleep 5
if ps -p $PID > /dev/null 2>&1; then
    echo "STUCK: Enumeration taking too long"
    kill $PID
else
    echo "OK: Enumeration completed"
fi
```

## Fix: Restart SDRplay Service

### macOS

**Option 1: Using launchctl kickstart (preferred, returns new PID)**
```bash
sudo /bin/launchctl kickstart -kp system/com.sdrplay.service
```
This kills the existing service and starts a fresh instance, returning the new PID.

**Option 2: Using launchctl stop/start**
```bash
sudo launchctl stop com.sdrplay.apiservice
sleep 2
sudo launchctl start com.sdrplay.apiservice
```

**Option 3: Kill and auto-restart**
```bash
sudo killall sdrplay_apiService
```
The service will auto-restart via launchd.

**To allow passwordless restart**, add to `/etc/sudoers.d/sdrplay`:
```
# Allow users to restart SDRplay service without password (kickstart is preferred)
%admin ALL=(ALL) NOPASSWD: /bin/launchctl kickstart -kp system/com.sdrplay.service
%admin ALL=(ALL) NOPASSWD: /bin/launchctl stop com.sdrplay.apiservice
%admin ALL=(ALL) NOPASSWD: /bin/launchctl start com.sdrplay.apiservice
%admin ALL=(ALL) NOPASSWD: /usr/bin/killall sdrplay_apiService
```

Create with:
```bash
sudo visudo -f /etc/sudoers.d/sdrplay
```

### Linux

**Option 1: Using systemctl (preferred)**
```bash
sudo systemctl restart sdrplayService
```

**Option 2: Kill and restart manually**
```bash
sudo killall sdrplay_apiService
sleep 1
sudo /usr/local/bin/sdrplay_apiService &
```

**To allow passwordless restart**, add to `/etc/sudoers.d/sdrplay`:
```
# Allow users to restart SDRplay service without password
%plugdev ALL=(ALL) NOPASSWD: /bin/systemctl restart sdrplayService
%plugdev ALL=(ALL) NOPASSWD: /usr/bin/killall sdrplay_apiService
```

Create with:
```bash
sudo visudo -f /etc/sudoers.d/sdrplay
```

### Windows

**Option 1: Using PowerShell (as Administrator)**
```powershell
Restart-Service SDRplayService
```

**Option 2: Using command prompt (as Administrator)**
```cmd
net stop SDRplayService
net start SDRplayService
```

**Option 3: Using Services GUI**
1. Open "Services" (services.msc)
2. Find "SDRplay API Service"
3. Right-click > Restart

## Verify Fix

After restarting the service, verify the fix:

```bash
# Check new service PID (should be different)
ps aux | grep -i sdrplay | grep -v grep

# Test enumeration (should complete in <3 seconds)
SoapySDRUtil --find
```

Expected output includes SDRplay device:
```
Found device 1
  driver = sdrplay
  label = SDRplay Dev0 RSPdx-R2 240309F070
  serial = 240309F070
```

## Alternative Fix: USB Reset

If service restart doesn't work, try physically unplugging and replugging the SDRplay USB device. Wait 3 seconds between unplug and replug.

**macOS USB port location:**
```bash
system_profiler SPUSBDataType | grep -B15 "1df7" | grep "Location ID"
```

## Prevention

The SDRplay service can get stuck when:
- Application crashes while device is open
- Multiple applications try to access the device
- USB power issues cause device reset
- macOS sleep/wake interrupts the service

To minimize issues:
- Always properly close SDR applications before starting new ones
- Use a powered USB hub for SDR devices
- Avoid USB3 ports if experiencing issues (USB2 is more stable for SDR)

## Integration with WaveCap-SDR

When WaveCap-SDR shows SDRplay device timeout:

1. Run this skill's diagnostic commands
2. Restart the SDRplay service
3. Refresh devices in WaveCap-SDR UI or restart the capture

## Files in This Skill

- `skill.md`: This file - instructions for diagnosing and fixing SDRplay service issues
