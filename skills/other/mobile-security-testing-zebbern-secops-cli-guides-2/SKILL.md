---
name: Mobile Application Security Testing
description: This skill should be used when the user asks to "perform mobile application penetration testing", "test Android app security", "bypass SSL pinning", "analyze APK files", "reverse engineer mobile apps", "test for insecure data storage", or "assess mobile app vulnerabilities". It provides comprehensive techniques for Android application security assessment.
version: 1.0.0
tags: [mobile, android, apk, frida, objection, reverse-engineering, ssl-pinning]
---

# Mobile Application Security Testing

## Purpose

Conduct comprehensive security assessments of Android mobile applications through static and dynamic analysis. This skill covers APK reverse engineering, code analysis, runtime manipulation, SSL pinning bypass, root detection bypass, and identification of OWASP Mobile Top 10 vulnerabilities.

## Prerequisites

### Required Tools
```bash
# Android Debug Bridge
sudo apt-get install adb

# Jadx-GUI (Java Decompiler)
wget https://github.com/skylot/jadx/releases/download/v1.4.7/jadx-1.4.7.zip
unzip jadx-1.4.7.zip

# Apktool
sudo apt-get install apktool

# Frida
pip3 install frida-tools

# Objection
pip3 install objection

# MobSF (Docker)
docker pull opensecurity/mobile-security-framework-mobsf

# Drozer
docker pull fsecurelabs/drozer
```

### Required Hardware
- Android device or emulator (Genymotion recommended)
- USB debugging cable
- Computer with 8GB+ RAM for emulation

### Required Knowledge
- Android application architecture
- Java/Kotlin programming basics
- HTTP/HTTPS protocols
- Basic reverse engineering concepts

### Required Access
- Target APK file
- Written authorization for testing
- Root access on test device (for some tests)

## Outputs and Deliverables

1. **Mobile Security Assessment Report** - Comprehensive vulnerability findings
2. **Static Analysis Results** - Hardcoded secrets, misconfigurations, code issues
3. **Dynamic Analysis Results** - Runtime vulnerabilities, API issues
4. **Proof of Concept Exploits** - Demonstrated vulnerabilities with evidence

## Core Workflow

### Phase 1: Lab Setup

Configure the testing environment:

```bash
# Verify ADB connection
adb devices

# Enable USB debugging on device
# Settings > Developer Options > USB Debugging

# Connect over network
adb tcpip 5555
adb connect DEVICE_IP:5555

# Install Frida server on device
wget https://github.com/frida/frida/releases/download/16.0.8/frida-server-16.0.8-android-x86.xz
unxz frida-server-16.0.8-android-x86.xz
mv frida-server-16.0.8-android-x86 frida-server
adb push frida-server /data/local/tmp/
adb shell chmod +x /data/local/tmp/frida-server
adb shell /data/local/tmp/frida-server &

# Verify Frida connection
frida-ps -U
```

### Phase 2: Reconnaissance

Gather information about the target application:

```bash
# App store research
- Developer information
- Version history and patch notes
- User reviews (bug reports)
- Required permissions
- Related apps from same developer

# Extract APK from device
adb shell pm list packages | grep target
adb shell pm path com.target.app
adb pull /data/app/com.target.app-1/base.apk target.apk

# Basic APK info
aapt dump badging target.apk
```

### Phase 3: APK Structure Analysis

Understand APK file contents:

```bash
# APK is a ZIP archive containing:
# - AndroidManifest.xml (app configuration)
# - classes.dex (compiled code)
# - resources.arsc (compiled resources)
# - res/ (resource files)
# - lib/ (native libraries)
# - META-INF/ (signatures)
# - assets/ (raw assets)

# Extract APK contents
unzip target.apk -d target_extracted/

# View manifest with aapt
aapt dump xmltree target.apk AndroidManifest.xml
```

### Phase 4: Static Analysis with Jadx

Decompile and analyze source code:

```bash
# Launch Jadx-GUI
./jadx-gui

# Open APK file and analyze:
# 1. AndroidManifest.xml - permissions, components, settings
# 2. Source code - hardcoded secrets, API keys
# 3. Resources - strings.xml, configuration files

# Search for sensitive data
# - API keys: grep -r "api_key\|apikey\|API_KEY"
# - Passwords: grep -r "password\|passwd\|secret"
# - URLs: grep -r "http://\|https://"
# - Firebase: grep -r "firebaseio.com"
```

Key areas to analyze:

```java
// AndroidManifest.xml checks
android:debuggable="true"     // Debuggable app - VULNERABLE
android:allowBackup="true"    // Backup allowed - DATA EXPOSURE
android:exported="true"       // Exported components - ACCESS CONTROL

// Hardcoded credentials
String apiKey = "AIzaSyAB1234567890";  // VULNERABLE
String password = "admin123";           // VULNERABLE

// Insecure HTTP
URL url = new URL("http://api.example.com");  // VULNERABLE

// Weak cryptography
Cipher.getInstance("DES");     // WEAK
Cipher.getInstance("AES/ECB"); // WEAK
```

### Phase 5: Static Analysis with MobSF

Automated static analysis:

```bash
# Start MobSF
docker run -it --rm -p 8000:8000 opensecurity/mobile-security-framework-mobsf:latest

# Access at http://127.0.0.1:8000
# Upload APK for analysis

# MobSF checks:
# - Security score
# - Permissions analysis
# - Code analysis
# - Manifest analysis
# - Binary analysis
# - Hardcoded secrets
# - Insecure configurations
```

### Phase 6: Reverse Engineering with Apktool

Decompile, modify, and recompile APK:

```bash
# Decompile APK
apktool d target.apk -o target_decompiled/

# Analyze smali code
ls target_decompiled/smali/

# Modify smali code (example: disable root detection)
# Find and modify relevant smali files

# Recompile APK
apktool b target_decompiled/ -o modified.apk

# Sign the APK
keytool -genkey -v -keystore my-release-key.keystore -alias alias_name -keyalg RSA -keysize 2048 -validity 10000
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore my-release-key.keystore modified.apk alias_name

# Install modified APK
adb install modified.apk
```

### Phase 7: Dynamic Analysis Setup

Configure traffic interception:

```bash
# Install Burp CA certificate on device
# 1. Export Burp CA certificate
# 2. Push to device: adb push burp-ca.cer /sdcard/
# 3. Install: Settings > Security > Install from storage

# Configure proxy on device
# Settings > Wi-Fi > Modify Network > Proxy > Manual
# Host: Your IP, Port: 8080

# For apps targeting API 24+
# System CA certificates are not trusted
# Use Frida/Objection for SSL bypass
```

### Phase 8: SSL Pinning Bypass

Bypass certificate pinning:

```bash
# Using Objection
objection -g com.target.app explore

# Disable SSL pinning
objection> android sslpinning disable

# Using Frida with codeshare script
frida -U -f com.target.app -l ssl_pinning_bypass.js --no-pause

# Universal SSL bypass script
# https://codeshare.frida.re/@pcipolloni/universal-android-ssl-pinning-bypass-with-frida/
frida -U --codeshare pcipolloni/universal-android-ssl-pinning-bypass-with-frida -f com.target.app
```

### Phase 9: Root Detection Bypass

Bypass root/jailbreak detection:

```bash
# Using Objection
objection -g com.target.app explore
objection> android root disable

# Using Frida
frida -U -f com.target.app -l root_bypass.js --no-pause

# Common root detection methods:
# - Check for su binary
# - Check for root management apps
# - Check for modified system files
# - SafetyNet attestation
```

Example Frida script for root bypass:

```javascript
Java.perform(function() {
    var RootCheck = Java.use("com.target.app.RootCheck");
    RootCheck.isRooted.implementation = function() {
        console.log("Root check bypassed");
        return false;
    };
});
```

### Phase 10: Vulnerability Testing with Drozer

Test Android components:

```bash
# Start Drozer agent on device
# Forward port
adb forward tcp:31415 tcp:31415

# Connect Drozer console
drozer console connect

# List attack surface
dz> run app.package.attacksurface com.target.app

# Enumerate activities
dz> run app.activity.info -a com.target.app

# Start exported activity
dz> run app.activity.start --component com.target.app com.target.app.HiddenActivity

# Enumerate content providers
dz> run app.provider.info -a com.target.app

# Query content providers
dz> run app.provider.query content://com.target.app.provider/users

# SQL injection in content provider
dz> run app.provider.query content://com.target.app.provider/users --projection "* FROM users--"

# Enumerate broadcast receivers
dz> run app.broadcast.info -a com.target.app

# Send broadcast
dz> run app.broadcast.send --action com.target.app.CUSTOM_ACTION --extra string message "test"
```

## Quick Reference

### OWASP Mobile Top 10 Tests

| Vulnerability | Test Method |
|--------------|-------------|
| M1: Improper Platform Usage | Check exported components, permissions |
| M2: Insecure Data Storage | Check SharedPrefs, SQLite, files, logs |
| M3: Insecure Communication | Check for HTTP, weak TLS, missing pinning |
| M4: Insecure Authentication | Test auth bypass, session handling |
| M5: Insufficient Cryptography | Analyze crypto implementations |
| M6: Insecure Authorization | Test privilege escalation, IDOR |
| M7: Client Code Quality | Static analysis for code issues |
| M8: Code Tampering | Test integrity checks, repackaging |
| M9: Reverse Engineering | Assess obfuscation, anti-tampering |
| M10: Extraneous Functionality | Find debug code, hidden features |

### Data Storage Locations

| Location | Path | Risk |
|----------|------|------|
| SharedPreferences | `/data/data/<pkg>/shared_prefs/` | Plaintext storage |
| SQLite Databases | `/data/data/<pkg>/databases/` | Unencrypted DB |
| Internal Storage | `/data/data/<pkg>/files/` | Accessible with root |
| External Storage | `/sdcard/` | World-readable |
| Logs | `adb logcat` | Sensitive data in logs |

### Essential Frida Commands

```bash
# List running apps
frida-ps -Ua

# Attach to running app
frida -U com.target.app

# Spawn and attach
frida -U -f com.target.app --no-pause

# Load script
frida -U -f com.target.app -l script.js

# Use codeshare script
frida -U --codeshare author/script-name -f com.target.app
```

### Essential Objection Commands

```bash
# Start objection
objection -g com.target.app explore

# Common commands
objection> android sslpinning disable
objection> android root disable
objection> android hooking list classes
objection> android hooking list class_methods <class>
objection> android hooking watch class <class>
objection> android intent launch_activity <activity>
objection> sqlite connect <database>
objection> env
```

### ADB Commands

| Command | Purpose |
|---------|---------|
| `adb devices` | List connected devices |
| `adb shell` | Open device shell |
| `adb install app.apk` | Install APK |
| `adb pull /path/file` | Download file |
| `adb push file /path/` | Upload file |
| `adb logcat` | View device logs |
| `adb shell pm list packages` | List installed packages |
| `adb shell dumpsys activity` | Dump activity info |

## Constraints and Limitations

### Legal Requirements
- Only test applications you own or have authorization to test
- Do not distribute modified APKs
- Respect app store terms of service
- Document all testing activities

### Technical Limitations
- Some obfuscation may prevent static analysis
- Anti-tampering may detect modifications
- SafetyNet can detect rooted/modified devices
- iOS requires different tooling (not covered here)

### Environmental Factors
- Emulators may behave differently than real devices
- Some apps detect emulator environments
- API behavior may differ in production vs staging

## Examples

### Example 1: Insecure Data Storage

**Scenario:** Check for sensitive data in local storage

```bash
# Access app data directory
adb shell
su
cd /data/data/com.target.app/

# Check SharedPreferences
cat shared_prefs/*.xml
# Look for: passwords, tokens, PII

# Check SQLite databases
sqlite3 databases/app.db
.tables
SELECT * FROM users;
# Look for: unencrypted credentials

# Check internal files
ls -la files/
cat files/config.json
# Look for: API keys, secrets
```

### Example 2: Exported Activity Exploitation

**Scenario:** Access hidden admin activity

```bash
# Using Drozer
dz> run app.package.attacksurface com.target.app
# Attack Surface:
#   3 activities exported
#   1 content providers exported

dz> run app.activity.info -a com.target.app
# com.target.app.AdminActivity (exported)

dz> run app.activity.start --component com.target.app com.target.app.AdminActivity
# Admin panel opened without authentication!
```

### Example 3: API Key Extraction

**Scenario:** Find hardcoded API keys

```bash
# Decompile with jadx
jadx -d output/ target.apk

# Search for API keys
grep -rn "api_key\|API_KEY\|apiKey" output/
# Found: String API_KEY = "sk_live_1234567890abcdef"

grep -rn "firebase" output/
# Found: google-services.json with Firebase config

# Check strings.xml
cat output/resources/res/values/strings.xml | grep -i key
```

## Troubleshooting

### Frida Connection Failed

**Problem:** Cannot connect Frida to device

**Solutions:**
1. Verify Frida server is running: `adb shell ps | grep frida`
2. Check architecture match (ARM vs x86)
3. Verify USB debugging is enabled
4. Try: `adb kill-server && adb start-server`
5. Use correct Frida version matching server

### SSL Pinning Bypass Fails

**Problem:** SSL bypass not working

**Solutions:**
1. Try multiple bypass scripts
2. App may use custom pinning implementation
3. Check for certificate transparency
4. Analyze pinning code and create custom bypass
5. Use Frida to hook specific pinning functions

### App Crashes on Modified APK

**Problem:** Recompiled APK crashes

**Solutions:**
1. Check for integrity verification
2. Verify signing is correct
3. Look for anti-tampering mechanisms
4. Use zipalign: `zipalign -v 4 modified.apk aligned.apk`
5. Try different signing method

### Root Detection Bypass Fails

**Problem:** App still detects root

**Solutions:**
1. Use Magisk Hide
2. Combine multiple bypass techniques
3. Analyze detection method and create custom bypass
4. Check for SafetyNet attestation
5. Use virtual environment like VMOS
