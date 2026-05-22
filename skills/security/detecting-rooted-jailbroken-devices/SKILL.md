<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: detecting-rooted-jailbroken-devices
description: >-
  Evaluate and bypass root/jailbreak detection mechanisms in mobile applications.
  Covers common detection techniques, Frida/objection bypass methods, Magisk
  hide, and recommendations for implementing robust device integrity checks.
domain: cybersecurity
subdomain: mobile-security
tags:
  - root-detection
  - jailbreak-detection
  - magisk
  - frida
  - objection
  - safetynet
  - device-integrity
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1407", "T1398"]
  owasp-mobile: ["M8", "M9"]
  tools: ["frida", "objection", "magisk", "liberty-lite", "shadow"]
---

# Detecting Rooted/Jailbroken Devices

## Overview

Root/jailbreak detection attempts to identify compromised device environments.
Testing evaluates detection robustness from offensive (bypass) and defensive
(implementation hardening) perspectives. Common checks include file existence,
binary availability, system property inspection, and attestation APIs.

## Prerequisites

```bash
pip install frida-tools objection
# Rooted Android device with Magisk
# Jailbroken iOS device with Frida
```

## Key Concepts

### Common Android Root Detection Checks

| Check | Method | Bypass Difficulty |
|-------|--------|-------------------|
| Su binary | `which su`, file exists check | Easy |
| Magisk files | `/data/adb/magisk` | Medium (MagiskHide) |
| Test keys | `Build.TAGS.contains("test-keys")` | Easy |
| RW system | Mount check for `/system` rw | Easy |
| SafetyNet/Play Integrity | Google attestation API | Hard |
| Root apps | Check for SuperSU, Magisk Manager | Medium |
| Busybox | Check for busybox binary | Easy |

### Common iOS Jailbreak Detection Checks

| Check | Method | Bypass Difficulty |
|-------|--------|-------------------|
| Cydia.app | File exists at `/Applications/Cydia.app` | Easy |
| Substrate | Check for MobileSubstrate | Easy |
| Fork | `fork()` succeeds on jailbroken | Medium |
| Sandbox escape | Write to `/private/` | Medium |
| URL schemes | `canOpenURL(cydia://)` | Easy |
| Dyld images | Check loaded libraries | Hard |

## Workflow

### Step 1: Identify Detection Methods

```bash
# Android: search for root detection in decompiled source
grep -rn 'isRooted\|RootBeer\|SafetyNet\|isDeviceRooted' jadx_out/
grep -rn 'su\b.*which\|/system/xbin/su\|/sbin/su' jadx_out/
grep -rn 'test-keys\|Build\.TAGS' jadx_out/
grep -rn 'com.topjohnwu.magisk\|eu.chainfire.supersu' jadx_out/
grep -rn 'PlayIntegrity\|SafetyNetClient\|Attestation' jadx_out/

# iOS: search for jailbreak detection
grep -rn 'isJailbroken\|Cydia\|MobileSubstrate\|jailbreak' ios_source/
grep -rn 'canOpenURL.*cydia\|fileExistsAtPath.*sbin' ios_source/
grep -rn 'fork()\|svc.*0x80' ios_source/
```

### Step 2: Bypass with Objection

```bash
# Android root detection bypass
objection -g com.target.app explore -s "android root disable"

# Simulate non-rooted environment
objection -g com.target.app explore -s "android root simulate"

# iOS jailbreak detection bypass
objection -g com.target.app explore -s "ios jailbreak disable"

# Simulate non-jailbroken environment
objection -g com.target.app explore -s "ios jailbreak simulate"
```

### Step 3: Frida Bypass Scripts

```javascript
// Android: Universal root detection bypass
Java.perform(function() {
    // File.exists bypass
    var File = Java.use('java.io.File');
    File.exists.implementation = function() {
        var path = this.getAbsolutePath();
        var rootPaths = ['/system/xbin/su', '/sbin/su', '/system/su',
                         '/data/local/xbin/su', '/data/local/su'];
        if (rootPaths.some(p => path === p)) {
            console.log('[*] Blocked root file check: ' + path);
            return false;
        }
        return this.exists();
    };

    // Runtime.exec bypass for 'which su'
    var Runtime = Java.use('java.lang.Runtime');
    Runtime.exec.overload('java.lang.String').implementation = function(cmd) {
        if (cmd.indexOf('su') !== -1) {
            console.log('[*] Blocked exec: ' + cmd);
            throw Java.use('java.io.IOException').$new('not found');
        }
        return this.exec(cmd);
    };

    // Build.TAGS bypass
    var Build = Java.use('android.os.Build');
    Build.TAGS.value = 'release-keys';
});
```

```javascript
// iOS: Universal jailbreak detection bypass
if (ObjC.available) {
    // fileExistsAtPath bypass
    var fm = ObjC.classes.NSFileManager;
    Interceptor.attach(fm['- fileExistsAtPath:'].implementation, {
        onEnter: function(args) {
            this.path = ObjC.Object(args[2]).toString();
        },
        onLeave: function(retval) {
            var jbPaths = ['/Applications/Cydia.app', '/usr/sbin/sshd',
                           '/bin/bash', '/usr/bin/ssh', '/etc/apt',
                           '/Library/MobileSubstrate'];
            if (jbPaths.some(p => this.path.includes(p))) {
                retval.replace(0x0);
            }
        }
    });

    // canOpenURL bypass
    var app = ObjC.classes.UIApplication;
    Interceptor.attach(app['- canOpenURL:'].implementation, {
        onEnter: function(args) {
            this.url = ObjC.Object(args[2]).toString();
        },
        onLeave: function(retval) {
            if (this.url.includes('cydia')) {
                retval.replace(0x0);
            }
        }
    });
}
```

### Step 4: Magisk-Based Bypass

```bash
# MagiskHide (deprecated in newer Magisk, use Shamiko/Zygisk DenyList)
magisk --hide enable
magisk --hide add com.target.app

# Zygisk DenyList
# Settings > Magisk > Enable Zygisk
# Configure DenyList > Add target app

# Hide Magisk Manager
# Magisk > Settings > Hide the Magisk app (randomize package name)
```

## Detection Opportunities

| Signal | Source | Description |
|--------|--------|-------------|
| Frida port open | Network | Port 27042 on device |
| Hook detection | Integrity check | PLT/GOT modification |
| SafetyNet fail | Play Integrity | Device attestation failure |
| Substrate loaded | Dyld check | MobileSubstrate in image list |

```yaml
title: Rooted Jailbroken Devices Detection
id: d29e7f98-8166-4263-b698-86cafead687f
status: experimental
description: Detects suspicious activity related to detecting rooted jailbroken devices techniques in mobile security context
logsource:
  category: application
  product: android
detection:
  selection:
    EventType: error
  condition: selection
level: medium
tags:
  - attack.t1407
  - attack.t1398
  - attack.initial_access
falsepositives:
  - Mobile device management platform enforcing security policies
```

## Verification

- [ ] Root/jailbreak detection methods identified in source
- [ ] Detection bypassed via objection or Frida scripts
- [ ] Magisk/Zygisk-level bypass tested
- [ ] SafetyNet/Play Integrity attestation evaluated
- [ ] Hardening recommendations documented

## References

- [OWASP MASTG — Root/Jailbreak Detection](https://mas.owasp.org/MASTG/techniques/android/MASTG-TECH-0012/)
- [RootBeer](https://github.com/nicehash/RootBeer)
- [Magisk](https://github.com/topjohnwu/Magisk)
- [MITRE T1407](https://attack.mitre.org/techniques/T1407/)
