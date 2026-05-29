---
name: appstore-prep
description: "App Store申請前のチェックリスト。プライバシーポリシー、権限説明、アイコン、スクリーンショットを確認。Use when: 申請、リリース、App Store、審査 を依頼された時。"
---

# App Store 申請準備

## 必須チェック項目

### Info.plist 権限説明
- [ ] NSCameraUsageDescription（カメラ使用時）
- [ ] NSPhotoLibraryUsageDescription（写真アクセス時）
- [ ] NSLocationWhenInUseUsageDescription（位置情報使用時）
→ 説明文は具体的に「なぜ必要か」を記載

### プライバシー
- [ ] プライバシーポリシーURLが有効
- [ ] App Privacy の回答が正確

### アセット
- [ ] App Iconが全サイズ揃っている（1024x1024含む）
- [ ] スクリーンショットが各デバイスサイズ分ある

### ビルド設定
- [ ] Release設定でビルドできる
- [ ] デバッグコード・テストコードが含まれていない
```

---

### ディレクトリ構成例
```
~/.claude/skills/           # 個人（全プロジェクト共通）
├── swift-build/
│   └── SKILL.md
└── ios-security/
    └── SKILL.md

your-project/.claude/skills/  # プロジェクト固有
├── swiftui-review/
│   └── SKILL.md
└── appstore-prep/
    └── SKILL.md