---
name: bluestacks-burp-interception
description: |
  Intercept Android app HTTPS traffic using BlueStacks and Burp Suite on macOS.
  Use when: (1) Need to analyze Android app API calls, (2) App ignores HTTP proxy,
  (3) App uses SSL pinning that blocks interception, (4) Need to install Burp CA
  as system certificate. Covers ADB setup, proxy configuration, Zygisk SSL unpinning,
  and Magisk trustusercerts module for system CA installation.
author: Claude Code
version: 1.0.0
date: 2026-01-24
---

# BlueStacks + Burp Suite HTTPS Traffic Interception

## Problem
You want to intercept HTTPS traffic from an Android app running in BlueStacks to analyze
API calls, but the app either ignores the proxy or uses SSL certificate pinning.

## Context / Trigger Conditions
- Running BlueStacks on macOS with Burp Suite
- App traffic not appearing in Burp Suite
- App crashes or refuses to connect when proxy is set
- Need to bypass SSL pinning for security testing/research

## Prerequisites
- BlueStacks with Magisk (kitsune variant) and root enabled
- Zygisk-SSL-Unpinning module installed
- trustusercerts Magisk module installed
- Android SDK installed (for ADB)
- Burp Suite running on port 8080

## Solution

### Step 1: Connect ADB to BlueStacks

```bash
# ADB location on macOS (Android SDK)
ADB=~/Library/Android/sdk/platform-tools/adb

# Connect to BlueStacks
$ADB connect localhost:5555

# Verify connection
$ADB devices
# Should show: emulator-5554 or localhost:5555
```

Note: BlueStacks runs **arm64-v8a** (not x86 as you might expect).

### Step 2: Set HTTP Proxy

Use your Mac's WiFi IP address (not 10.0.2.2 or localhost):

```bash
# Get Mac WiFi IP
IP=$(ipconfig getifaddr en0)

# Set proxy (Burp default port 8080)
$ADB shell settings put global http_proxy ${IP}:8080

# Verify
$ADB shell settings get global http_proxy

# Disable proxy when done
$ADB shell settings put global http_proxy :0
```

### Step 3: Configure SSL Unpinning for Target App

```bash
# Find app package name
$ADB shell pm list packages | grep <keyword>

# Edit config
$ADB shell "su -c 'cat > /data/local/tmp/zyg.ssl/config.json << EOF
{
    \"targets\": [
        {
            \"pkg_name\" : \"com.example.app\",
            \"enable\": true,
            \"start_safe\": true,
            \"start_delay\": 1000
        }
    ]
}
EOF'"

# Restart the app
$ADB shell am force-stop com.example.app
$ADB shell monkey -p com.example.app -c android.intent.category.LAUNCHER 1

# Verify SSL unpinning is active
$ADB shell "logcat -d | grep -i ZygiskSSL | tail -10"
# Should show: "App detected: com.example.app" and "[*] SSL UNPINNING [#]"
```

### Step 4: Install Burp CA as System Certificate

```bash
# Download Burp CA cert
curl -x http://127.0.0.1:8080 http://burp/cert -o /tmp/burp-cert.der

# Convert to PEM
openssl x509 -inform DER -in /tmp/burp-cert.der -out /tmp/burp-cert.pem

# Get hash for Android cert store naming
HASH=$(openssl x509 -inform PEM -subject_hash_old -in /tmp/burp-cert.pem | head -1)
cp /tmp/burp-cert.pem /tmp/${HASH}.0

# Push to device
$ADB push /tmp/${HASH}.0 /sdcard/

# Install via trustusercerts Magisk module
$ADB shell "su -c 'cp /sdcard/${HASH}.0 /data/adb/modules/trustusercerts/system/etc/security/cacerts/'"
$ADB shell "su -c 'chmod 644 /data/adb/modules/trustusercerts/system/etc/security/cacerts/${HASH}.0'"

# Reboot required for Magisk overlay
$ADB shell "su -c 'reboot'"

# After reboot, verify cert is in system store
$ADB shell "su -c 'ls /system/etc/security/cacerts/${HASH}.0'"
```

### Step 5: Test Interception

1. Re-enable proxy after reboot: `$ADB shell settings put global http_proxy ${IP}:8080`
2. Launch target app
3. Check Burp Suite → Proxy → HTTP history for requests

## Verification

- Proxy set: `adb shell settings get global http_proxy` returns `<ip>:8080`
- SSL unpinning active: `logcat | grep ZygiskSSL` shows "SSL UNPINNING"
- Burp CA installed: `ls /system/etc/security/cacerts/<hash>.0` exists
- Traffic visible in Burp Suite HTTP history

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| No traffic in Burp | Proxy not set | Check `settings get global http_proxy` |
| App shows SSL error | Cert not installed | Verify cert in system store, reboot |
| SSL unpinning not working | Config not loaded | Force-stop app, check config.json syntax |
| ADB connection refused | BlueStacks ADB disabled | Enable in BlueStacks Settings → Advanced |
| Wrong cert hash | Using wrong openssl flag | Use `subject_hash_old` not `subject_hash` |

## Notes

- BlueStacks runs arm64-v8a, so Zygisk modules need arm64 support
- The trustusercerts module copies certs at boot via Magisk overlay
- System partition is read-only; use Magisk modules instead of direct mounting
- Burp cert hash is typically `9a5ba575` but verify for your instance
- Some apps may use additional protections (root detection, Frida detection)

## Quick Reference

```bash
# Set proxy
adb shell settings put global http_proxy <ip>:8080

# Disable proxy
adb shell settings put global http_proxy :0

# Check SSL unpinning logs
adb shell "logcat -d | grep -i ZygiskSSL"

# Force restart app
adb shell am force-stop <package> && adb shell monkey -p <package> -c android.intent.category.LAUNCHER 1
```

## References
- [Zygisk-SSL-Unpinning](https://github.com/m0szy/Zygisk-SSL-Unpinning)
- [MagiskTrustUserCerts](https://github.com/NVISOsecurity/MagiskTrustUserCerts)
- [Burp Suite Documentation](https://portswigger.net/burp/documentation)
