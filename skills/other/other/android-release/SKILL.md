---
name: android-release
description: Build, sign, and prepare Android APK and AAB for release. Handles version bumping, building, zipalign (APK), and signing with JKS keystore. Outputs DecentPaste_x.x.x.apk for GitHub releases and signed AAB for Play Console.
---

# Android Release

Build signed APK (GitHub) and AAB (Play Console).

## 1. Gather Info

Ask user for: version (x.x.x), JKS keystore path, keystore alias.
**Never ask for password** - user enters it during signing.

## 2. Update Versions

Use `/bump-version` workflow to update all 4 config files.

## 3. Build

```bash
cd decentpaste-app && yarn tauri android build && cd ..
```

Outputs (from project root):
- APK: `decentpaste-app/src-tauri/gen/android/app/build/outputs/apk/universal/release/app-universal-release-unsigned.apk`
- AAB: `decentpaste-app/src-tauri/gen/android/app/build/outputs/bundle/universalRelease/app-universal-release.aab`

## 4. Sign APK

**Zipalign BEFORE signing** (Claude runs):
```bash
zipalign -v 4 <unsigned-apk> DecentPaste_VERSION_aligned.apk
```

Signing (user runs - contains password):
```bash
apksigner sign --ks <keystore> --ks-key-alias <alias> --out DecentPaste_VERSION.apk DecentPaste_VERSION_aligned.apk
```

After user confirms, delete aligned file.

## 5. Sign AAB

**Use `jarsigner` not `apksigner`** - AABs are JAR-like bundles. No zipalign needed.

User runs:
```bash
jarsigner -verbose -sigalg SHA256withRSA -digestalg SHA-256 -keystore <keystore> <aab-path> <alias>
cp <aab-path> DecentPaste_VERSION.aab
```

## 6. Verify & Report

```bash
apksigner verify --verbose DecentPaste_VERSION.apk
jarsigner -verify -verbose DecentPaste_VERSION.aab
```

Report: files created, versions updated, next steps (commit, tag, upload).
