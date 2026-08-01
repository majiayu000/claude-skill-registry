---
name: mobile-security
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: mobile-security
description: >-
  Mobile application security testing for Android and iOS including static analysis
  (APK/IPA decompilation), dynamic analysis (Frida instrumentation), certificate
  pinning bypass, insecure data storage detection, API traffic interception, root/
  jailbreak detection bypass, OWASP MASTG/MASVS compliance, and mobile threat defense.
domain: cybersecurity
subdomain: mobile-security
tags:
  - android
  - ios
  - frida
  - mobile-pentesting
  - owasp-masvs
  - apk-analysis
  - certificate-pinning
  - objection
  - mobile-threat-defense
version: "1.0"
author: defconxt
license: AGPL-3.0
compatibility: Designed for Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI, and any agentskills.io-compatible agent.
metadata:
  mitre-attack: ["T1407", "T1409", "T1414", "T1417", "T1422"]
  owasp-mobile: ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10"]
  frameworks: ["OWASP MASVS v2", "OWASP MASTG", "NIST SP 800-163"]
---

# Mobile Security

## When to Use

Activate when the operator asks about Android/iOS security testing, mobile app
pentesting, Frida, certificate pinning bypass, mobile OWASP, APK analysis,
or mobile threat defense.

Mode: `[MODE: RED]` for mobile pentesting; `[MODE: BLUE]` for mobile device management; `[MODE: ARCHITECT]` for secure mobile design.

## Quick Reference

| Task | Tool / Command | Platform |
|------|---------------|----------|
| APK decompile | `apktool d target.apk -o output/` | Android |
| Java decompile | `jadx -d output/ target.apk` | Android |
| IPA decrypt | `frida-ios-dump -u -H host target` | iOS |
| Frida hook | `frida -U -f com.target.app -l hook.js` | Both |
| Objection explore | `objection -g com.target.app explore` | Both |
| SSL pinning bypass | `objection -g com.target.app explore -s "android sslpinning disable"` | Both |
| Traffic intercept | Burp + proxy settings on device | Both |
| Root detection bypass | `objection -g com.target.app explore -s "android root disable"` | Android |
| File system browse | `objection -g com.target.app explore -s "env"` | Both |
| Keychain dump | `objection -g com.target.app explore -s "ios keychain dump"` | iOS |

## Workflow

### 1. Static Analysis

```bash
# Android APK decompilation
apktool d target.apk -o decompiled/
jadx -d java_src/ target.apk

# Search for secrets and misconfigurations
grep -rn "api_key\|password\|secret\|token\|firebase" java_src/
grep -rn "http://" java_src/  # Cleartext HTTP
grep -rn "MODE_WORLD_READABLE\|MODE_WORLD_WRITEABLE" java_src/
grep -rn "\.db\|\.sqlite" java_src/  # Database files

# AndroidManifest.xml review
# Check: exported components, debuggable flag, backup allowed,
#         cleartext traffic, permissions
grep -E "exported=\"true\"|debuggable=\"true\"|allowBackup=\"true\"|usesCleartextTraffic" decompiled/AndroidManifest.xml

# MobSF automated scan
docker run -it -p 8000:8000 opensecurity/mobile-security-framework-mobsf
# Upload APK/IPA via web interface

# iOS IPA analysis
unzip target.ipa -d extracted/
# Check Info.plist for ATS exceptions, URL schemes
plutil -convert xml1 extracted/Payload/App.app/Info.plist
grep -A5 "NSAppTransportSecurity" extracted/Payload/App.app/Info.plist
```

### 2. Dynamic Analysis (Frida)

```javascript
// Frida script: Hook encryption function
Java.perform(function() {
    var cipher = Java.use('javax.crypto.Cipher');
    cipher.doFinal.overload('[B').implementation = function(data) {
        console.log('Cipher.doFinal input: ' + byteArrayToHex(data));
        var result = this.doFinal(data);
        console.log('Cipher.doFinal output: ' + byteArrayToHex(result));
        return result;
    };
});

// Hook SharedPreferences writes
Java.perform(function() {
    var editor = Java.use('android.content.SharedPreferences$Editor');
    editor.putString.implementation = function(key, value) {
        console.log('SharedPrefs PUT: ' + key + ' = ' + value);
        return this.putString(key, value);
    };
});

// iOS: Hook NSURLSession for network inspection
if (ObjC.available) {
    var NSURLSession = ObjC.classes.NSURLSession;
    Interceptor.attach(NSURLSession['- dataTaskWithRequest:completionHandler:'].implementation, {
        onEnter: function(args) {
            var request = ObjC.Object(args[2]);
            console.log('URL: ' + request.URL().absoluteString());
        }
    });
}
```

### 3. Certificate Pinning Bypass

```bash
# Objection (easiest)
objection -g com.target.app explore -s "android sslpinning disable"
objection -g com.target.app explore -s "ios sslpinning disable"

# Frida script for custom pinning bypass
frida -U -f com.target.app -l ssl_bypass.js --no-pause

# Magisk + TrustUserCerts module (Android 7+)
# System-level CA installation for intercepting all traffic
```

### 4. OWASP MASVS Checklist

```
MASVS-STORAGE: Data storage and privacy
├── No sensitive data in logs
├── No sensitive data in backups
├── No sensitive data in cleartext (SharedPrefs, NSUserDefaults)
├── Keychain/Keystore used for sensitive data
└── Clipboard cleared for sensitive fields

MASVS-CRYPTO: Cryptographic practices
├── No hardcoded keys
├── No deprecated algorithms (MD5, SHA1, DES, RC4)
├── Proper key management (Android Keystore, iOS Keychain)
└── TLS 1.2+ enforced

MASVS-AUTH: Authentication and authorization
├── Session management server-side
├── Biometric auth backed by Keystore/Keychain
├── Re-authentication for sensitive operations
└── Token expiry enforced

MASVS-NETWORK: Network communication
├── TLS for all connections
├── Certificate pinning implemented
├── ATS enabled (iOS) / cleartext traffic disabled (Android)
└── No custom certificate validation that weakens security

MASVS-RESILIENCE: Reverse engineering resilience
├── Root/jailbreak detection
├── Debugger detection
├── Code obfuscation (ProGuard/R8 for Android)
└── Integrity verification
```

## Verification

- [ ] Static analysis complete (secrets, misconfigurations, permissions)
- [ ] Dynamic analysis complete (data storage, network, crypto)
- [ ] Certificate pinning tested and bypass documented
- [ ] OWASP MASVS categories assessed
- [ ] API traffic intercepted and tested for vulnerabilities
- [ ] Root/jailbreak detection evaluated
- [ ] Sensitive data not stored in plaintext on device
