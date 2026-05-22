---
name: macos-security
description: "macOSアプリのセキュリティレビュー。Notarization、Hardened Runtime、Sandbox、コード署名をチェック。Use when: macOS、公証、Notarization、Sandbox、署名 を依頼された時。"
---

# macOS セキュリティレビュー

## Notarization（公証）チェック

### 前提条件
- [ ] Apple Developer Program に登録済み
- [ ] Developer ID Application 証明書を所持
- [ ] xcrun notarytool が利用可能

### Hardened Runtime
- [ ] Hardened Runtime が有効化されている
- [ ] 必要最小限の Entitlements のみ設定
- [ ] com.apple.security.cs.disable-library-validation は使用しない（特別な理由がない限り）

## Sandbox チェック

### Entitlements 確認
```bash
# Entitlements 一覧表示
codesign -d --entitlements - YourApp.app
```

### 必要な権限のみ許可
- [ ] com.apple.security.app-sandbox = true
- [ ] ネットワーク: com.apple.security.network.client（必要時のみ）
- [ ] ファイルアクセス: 必要最小限のスコープ
- [ ] カメラ/マイク: 使用時のみ

## コード署名検証

```bash
# 署名確認
codesign --verify --deep --strict YourApp.app

# Notarization 確認
spctl --assess --verbose=4 --type execute YourApp.app

# Gatekeeper テスト
spctl --assess --type exec -v YourApp.app
```

## macOS 固有のセキュリティパターン

### Keychain アクセス
- [ ] kSecAttrAccessible の適切な設定
- [ ] Access Group の適切な設定
- [ ] Keychain Sharing Entitlement（必要時のみ）

### IPC / XPC
- [ ] XPC サービスの適切な権限分離
- [ ] Mach サービスのセキュリティ検証

### ファイルシステム
- [ ] ユーザーデータは ~/Library/Application Support/ に保存
- [ ] 一時ファイルは NSTemporaryDirectory() を使用
- [ ] Security-scoped bookmarks の適切な使用
