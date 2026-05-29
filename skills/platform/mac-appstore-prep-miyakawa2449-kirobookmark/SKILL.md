---
name: mac-appstore-prep
description: "Mac App Store申請前のチェックリスト。Sandbox必須、スクリーンショット、Notarization、権限説明を確認。Use when: Mac App Store、macOS申請、Mac審査 を依頼された時。"
---

# Mac App Store 申請準備

## 必須チェック項目

### Sandbox 必須
- [ ] com.apple.security.app-sandbox = true（Mac App Storeでは必須）
- [ ] 不要な Entitlements を削除
- [ ] Temporary Exception Entitlements の説明を準備（使用時）

### Info.plist 権限説明（macOS固有）
- [ ] NSCameraUsageDescription（カメラ使用時）
- [ ] NSMicrophoneUsageDescription（マイク使用時）
- [ ] NSAppleEventsUsageDescription（AppleScript使用時）
- [ ] NSSystemAdministrationUsageDescription（管理者権限使用時）
- [ ] NSDesktopFolderUsageDescription（デスクトップアクセス時）
- [ ] NSDocumentsFolderUsageDescription（書類フォルダアクセス時）
- [ ] NSDownloadsFolderUsageDescription（ダウンロードフォルダアクセス時）

### スクリーンショット要件
| サイズ | 解像度 | 備考 |
|--------|--------|------|
| 1280 x 800 | 非Retina | 最小サイズ |
| 1440 x 900 | 非Retina | 推奨 |
| 2560 x 1600 | Retina | 推奨 |
| 2880 x 1800 | Retina | 最大サイズ |

※ 最低1枚、最大10枚

### アセット
- [ ] App Icon（1024x1024、角丸なし）
- [ ] macOS用アイコンセット（16x16 〜 512x512@2x）

### ビルド設定
- [ ] Release 設定でビルド可能
- [ ] Deployment Target が適切（最低サポートOS）
- [ ] Architectures に arm64 と x86_64 を含む（Universal Binary推奨）

## App Store Connect 設定

### カテゴリ
- [ ] 適切なカテゴリを選択
- [ ] サブカテゴリの設定（該当時）

### 価格と配信
- [ ] 価格設定
- [ ] 配信国/地域の設定

### App Privacy
- [ ] データ収集の回答
- [ ] プライバシーポリシーURL

## 審査対策

### よくあるリジェクト理由（macOS固有）
1. Sandbox 違反
2. 不必要な Entitlements の使用
3. プライベートAPIの使用
4. 適切でない Temporary Exception の使用

### テスト確認
```bash
# Sandbox テスト
sandbox-exec -f /path/to/profile YourApp.app/Contents/MacOS/YourApp

# Entitlements 確認
codesign -d --entitlements :- YourApp.app
```
