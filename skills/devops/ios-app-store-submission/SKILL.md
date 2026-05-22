---
name: ios-app-store-submission
description: "When the user wants to submit an iOS app to the App Store. Use when the user mentions 'App Store,' 'App Store Connect,' 'TestFlight,' 'iOS submission,' 'app review,' 'EAS build,' 'eas submit,' 'Apple review,' 'app rejection,' or 'iOS release.' This skill covers the entire process from setup to App Store review approval."
---

# iOS App Store Submission

You are an expert in iOS app submission, Apple review guidelines, and build automation. Your goal is to guide users through the entire submission process efficiently, avoiding common pitfalls and rejections.

## Core Philosophy

App Store submission is not just about uploading a binary. It's about:
- Meeting Apple's technical and content requirements
- Providing accurate metadata and privacy disclosures
- Preparing for potential review questions
- **Automating the process for fast iteration**

---

## Quick Reference: Build Methods

| 方法 | 所要時間 | いつ使う |
|------|---------|---------|
| **CLI Local (推奨)** | 10-15分 | 最速。ローカルでArchive→直接アップロード |
| **Xcode GUI** | 10-15分 | CLIに慣れていない場合 |
| **EAS Build** | 15-30分+キュー | CI/CD、チーム開発、Free tierはキュー待ちあり |

---

## ⚠️ Known Issues Prevention (ビルド前に必ず確認)

過去のリジェクト事例から学んだ、**ビルド前に必ず確認すべき項目**。

### 1. Provider で `null` を返さない

**問題**: ThemeProvider等がAsyncStorage読み込み中に`null`を返すと、審査時に「黒い画面」でリジェクト。

**確認方法**:
```bash
grep -r "return null" src/providers/
```

**対処**: ローディングUIを返す
```typescript
// NG
if (!isLoaded) return null;

// OK
if (!isLoaded) {
  return (
    <View style={{ flex: 1, backgroundColor: '#1a1a2e', justifyContent: 'center', alignItems: 'center' }}>
      <ActivityIndicator size="large" color="#059669" />
    </View>
  );
}
```

### 2. ATT プラグイン設定

**問題**: `expo-tracking-transparency`をベア文字列で設定すると、ATTダイアログが表示されない。

**確認方法**:
```bash
# app.json確認
grep -A5 "expo-tracking-transparency" app.json

# prebuild後のInfo.plist確認
npx expo prebuild --clean
grep -A1 "NSUserTrackingUsageDescription" ios/*/Info.plist
```

**正しい設定**:
```json
[
  "expo-tracking-transparency",
  {
    "userTrackingPermission": "This identifier will be used to deliver personalized ads to you."
  }
]
```

### 3. UIRequiredDeviceCapabilities に telephony を入れない

**問題**: `telephony`を設定すると、Mac Apple silicon / Vision Pro で警告が出る。

**確認方法**:
```bash
grep -r "telephony" app.json
grep -r "UIRequiredDeviceCapabilities" ios/*/Info.plist
```

**対処**: iPhoneのみ対応は `supportsTablet: false` で十分。`telephony`は不要。

### 4. ビルド前検証コマンド

```bash
# 全チェックを一括実行
echo "=== Provider null check ===" && grep -r "return null" src/providers/ 2>/dev/null || echo "OK"
echo "=== ATT config check ===" && grep -A5 "expo-tracking-transparency" app.json
echo "=== telephony check ===" && grep -r "telephony" app.json 2>/dev/null || echo "OK"
```

---

## Phase 1: Initial Setup (One-time)

### 1.1 App-specific Password

CLIでアップロードするために必要。**一度作成すれば全アプリで使い回し可能**。

1. https://appleid.apple.com にアクセス
2. サインイン → **サインインとセキュリティ** → **アプリ用パスワード**
3. **+** → ラベル入力（例: `mued-apps`）→ **作成**
4. パスワードをコピー（`xxxx-xxxx-xxxx-xxxx` 形式）
5. `.env.local` に保存:
```bash
# Apple ID app-specific password
APPLE_ID=your-apple-id@example.com
APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
TEAM_ID=XXXXXXXXXX
```

### 1.2 ExportOptions.plist

プロジェクトルートに作成:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>method</key>
    <string>app-store-connect</string>
    <key>teamID</key>
    <string>YOUR_TEAM_ID</string>
    <key>uploadSymbols</key>
    <true/>
    <key>destination</key>
    <string>upload</string>
</dict>
</plist>
```

---

## Phase 2: CLI Build & Upload (推奨)

### 2.1 Full CLI Workflow

```bash
# 1. Prebuild（ネイティブプロジェクト生成）
npx expo prebuild --clean

# 2. Archive
xcodebuild -workspace ios/YourApp.xcworkspace \
  -scheme YourApp \
  -configuration Release \
  -archivePath build/YourApp.xcarchive \
  -destination "generic/platform=iOS" \
  DEVELOPMENT_TEAM=YOUR_TEAM_ID \
  CODE_SIGN_STYLE=Automatic \
  -allowProvisioningUpdates \
  archive

# 3. Export & Upload（一発でApp Store Connectへ）
xcodebuild -exportArchive \
  -archivePath build/YourApp.xcarchive \
  -exportPath build \
  -exportOptionsPlist ExportOptions.plist \
  -allowProvisioningUpdates
```

### 2.2 よくあるエラーと対処

| エラー | 原因 | 対処 |
|-------|------|------|
| `No profiles found` | プロビジョニング未設定 | `-allowProvisioningUpdates` を追加 |
| `Signing requires development team` | チームID未指定 | `DEVELOPMENT_TEAM=XXXX` を追加 |
| `No provider associated` | Apple ID未認証 | Xcode → Preferences → Accounts で認証 |

### 2.3 Upload後の確認

1. [App Store Connect](https://appstoreconnect.apple.com) を開く
2. My Apps → Your App → **TestFlight**
3. ビルドが「処理中」→「利用可能」になるまで5-15分待つ
4. **App Store** タブ → ビルドを選択 → **審査に提出**

---

## Phase 3: Xcode GUI Build (Alternative)

CLIが苦手な場合の代替手順。

```bash
# 1. Prebuild
npx expo prebuild --clean

# 2. Xcodeで開く
open ios/YourApp.xcworkspace
```

### Xcode内の操作

1. **Signing**: Automatically manage signing → Team選択
2. **Device**: "Any iOS Device (arm64)" を選択
3. **Product → Archive**
4. Archiveウィンドウ → **Distribute App**
5. **App Store Connect** → **Upload**

---

## Phase 4: EAS Build (Cloud)

チーム開発やCI/CDで使用。Free tierはキュー待ちあり（数十分〜数時間）。

```bash
# Build
eas build --platform ios --profile production

# Submit
eas submit --platform ios --latest
```

### eas.json 設定

```json
{
  "cli": {
    "version": ">= 16.0.0",
    "appVersionSource": "remote"
  },
  "build": {
    "production": {
      "ios": {
        "autoIncrement": "buildNumber"
      }
    }
  },
  "submit": {
    "production": {
      "ios": {
        "appleId": "your-apple-id@example.com",
        "ascAppId": "1234567890",
        "appleTeamId": "XXXXXXXXXX"
      }
    }
  }
}
```

---

## Phase 5: App Store Connect Setup

### 5.1 App Information

| Field | Requirements |
|-------|--------------|
| **Name** | 30 chars max, unique on App Store |
| **Subtitle** | 30 chars max, optional |
| **Category** | Primary + optional secondary |
| **Age Rating** | Complete questionnaire |

### 5.2 App Privacy (Critical!)

App Store Connect → App Privacy → Get Started

**AdMob使用時の宣言:**

| Data Type | Collected | Linked | Tracking |
|-----------|-----------|--------|----------|
| Device ID | Yes | Yes | Yes (if ATT granted) |
| Product Interaction | Yes | No | No |
| Advertising Data | Yes | Yes | Yes |
| Crash Data | Yes | No | No |

### 5.3 Screenshots

| Device | Size (pixels) | Required |
|--------|---------------|----------|
| 6.7" iPhone | 1290 x 2796 | Yes |
| 6.5" iPhone | 1284 x 2778 | Yes |
| 12.9" iPad Pro | 2048 x 2732 | If supports iPad |

---

## Phase 6: Privacy Requirements

### 6.1 App Tracking Transparency (ATT)

AdMob等の広告SDKを使う場合は必須。

**app.json設定（プラグイン経由が推奨）:**
```json
{
  "plugins": [
    [
      "expo-tracking-transparency",
      {
        "userTrackingPermission": "This identifier will be used to deliver personalized ads to you."
      }
    ]
  ]
}
```

⚠️ **注意**: `infoPlist`に直接書くのではなく、プラグイン設定を使う。prebuild時にInfo.plistに正しく反映される。

**コード実装:**
```typescript
import { requestTrackingPermissionsAsync } from 'expo-tracking-transparency';

async function requestTracking() {
  const { status } = await requestTrackingPermissionsAsync();
  // 'granted' | 'denied' | 'undetermined'
}
```

### 6.2 ATT設定の検証

```bash
npx expo prebuild --clean
grep -A1 "NSUserTrackingUsageDescription" ios/YourApp/Info.plist
```

---

## Phase 7: App Review

### 7.1 Review Timeline

| Type | Typical Duration |
|------|------------------|
| New App | 24-48 hours |
| Update | 24 hours |
| Expedited Review | 24 hours (request required) |

### 7.2 Common Rejection Reasons & Fixes

#### 1. **Guideline 2.1 - App Completeness**
> "Your app crashed during review" / "Black screen on launch"

**原因:**
- Provider（ThemeProvider等）がローディング中に`null`を返している
- AsyncStorage読み込み中に画面が真っ黒

**Fix:**
```typescript
// Before (NG)
if (!isLoaded) {
  return null;
}

// After (OK)
if (!isLoaded) {
  return (
    <View style={{ flex: 1, backgroundColor: '#1a1a2e', justifyContent: 'center', alignItems: 'center' }}>
      <ActivityIndicator size="large" color="#059669" />
    </View>
  );
}
```

#### 2. **Guideline 5.1.2 - ATT Not Shown**
> "App doesn't show ATT dialog"

**原因:**
- `expo-tracking-transparency`がベア文字列でプラグイン設定されている
- `NSUserTrackingUsageDescription`がInfo.plistに含まれていない

**Fix:**
```json
// Before (NG)
"plugins": ["expo-tracking-transparency"]

// After (OK)
"plugins": [
  [
    "expo-tracking-transparency",
    {
      "userTrackingPermission": "This identifier will be used to deliver personalized ads to you."
    }
  ]
]
```

#### 3. **Guideline 2.3 - Accurate Metadata**
> "Screenshots don't match app functionality"

**Fix:**
- スクリーンショットを最新版に更新
- 存在しない機能を表示しない

### 7.3 Responding to Rejection

1. **Resolution Centerで返信** (App Store Connect → Your App → Resolution Center)
2. **修正内容を具体的に説明**
3. **再ビルド→再アップロード→再提出**

### 7.4 Resolution Center コメントテンプレート

審査員に修正内容を伝えるコメント。**英語で、具体的に**書く。

#### Black Screen / Crash 修正時
```
We have addressed the issue identified in the previous review:

**[Issue description] (fixed)**
- Root cause: [Technical explanation of what was wrong]
- Fix: [What was changed]
- File changed: [File path]

Build [N] contains this fix. Thank you for your review.
```

#### ATT Not Shown 修正時
```
We have addressed the ATT (App Tracking Transparency) issue:

**ATT dialog not shown (fixed)**
- Root cause: `expo-tracking-transparency` was configured as a bare string, causing `NSUserTrackingUsageDescription` to not be included in Info.plist
- Fix: Changed plugin configuration to include `userTrackingPermission` parameter
- Verified: Confirmed the description is now present in Info.plist via prebuild

Build [N] contains this fix. Thank you for your review.
```

#### UIRequiredDeviceCapabilities 警告修正時
```
We have addressed the compatibility warning:

**Mac/Vision Pro compatibility (fixed)**
- Removed `UIRequiredDeviceCapabilities: ["telephony"]` from Info.plist
- The app targets iPhone only via `supportsTablet: false` setting

Build [N] contains this fix. Thank you for your review.
```

**ポイント:**
- 何が問題だったか（Root cause）
- 何を変更したか（Fix）
- どのビルドに含まれているか（Build N）
- 簡潔に、技術的に正確に

### 7.5 Requesting Expedited Review

緊急時のみ:
1. App Store Connect → Your App → App Review
2. Contact Us → Request Expedited Review
3. 理由を明確に説明

---

## Checklist: Pre-Submission

### Technical
- [ ] `ExportOptions.plist` 作成済み
- [ ] `app.json` の `bundleIdentifier`, `version` 設定済み
- [ ] ATTプラグイン設定済み（広告使用時）
- [ ] ローディング状態でUIを表示（`null`を返さない）
- [ ] 実機でテスト済み

### App Store Connect
- [ ] App Privacy 設定済み
- [ ] Screenshots アップロード済み
- [ ] Description, Keywords 設定済み
- [ ] Support URL 設定済み

---

## Quick Commands Reference

```bash
# === CLI Build (推奨) ===
npx expo prebuild --clean
xcodebuild -workspace ios/App.xcworkspace -scheme App -configuration Release \
  -archivePath build/App.xcarchive -destination "generic/platform=iOS" \
  DEVELOPMENT_TEAM=XXXX CODE_SIGN_STYLE=Automatic -allowProvisioningUpdates archive
xcodebuild -exportArchive -archivePath build/App.xcarchive -exportPath build \
  -exportOptionsPlist ExportOptions.plist -allowProvisioningUpdates

# === EAS Build ===
eas build --platform ios --profile production
eas submit --platform ios --latest

# === Debugging ===
grep -A1 "NSUserTrackingUsageDescription" ios/App/Info.plist  # ATT確認
eas build:view BUILD_ID --json  # ビルドステータス確認
```

---

## Related Skills

- **android-play-store-submission**: Google Play Store submission
- **launch-strategy**: App launch planning
- **marketing-psychology**: App Store optimization (ASO)
