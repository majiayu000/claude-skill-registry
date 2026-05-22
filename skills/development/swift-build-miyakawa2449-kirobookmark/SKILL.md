---
name: swift-build
description: "SwiftプロジェクトのビルドとテストをXcodeコマンドラインで実行（iOS/macOS対応）。Use when: ビルド、テスト、xcodebuild、swift test を依頼された時。"
---

# Swift ビルド＆テスト（iOS / macOS 対応）

## プラットフォーム別コマンド

### iOS Simulator
```bash
xcodebuild build -scheme YourApp -destination 'platform=iOS Simulator,name=iPhone 16e'
xcodebuild test -scheme YourApp -destination 'platform=iOS Simulator,name=iPhone 16e'
```

### macOS
```bash
xcodebuild build -scheme YourApp -destination 'platform=macOS'
xcodebuild test -scheme YourApp -destination 'platform=macOS'
```

### Mac Catalyst
```bash
xcodebuild build -scheme YourApp -destination 'platform=macOS,variant=Mac Catalyst'
```

## 実行手順

1. スキーム確認: `xcodebuild -list`
2. フォーマットチェック: `swift-format lint -r Sources/`
3. ビルド: 上記プラットフォーム別コマンド
4. ユニットテスト: 上記プラットフォーム別コマンド
5. 静的解析: `swiftlint lint`

## Universal Binary（macOS）

```bash
# arm64 + x86_64 のユニバーサルビルド
xcodebuild build -scheme YourApp -destination 'platform=macOS' \
  ARCHS="arm64 x86_64" ONLY_ACTIVE_ARCH=NO
```

## クリーンビルド

```bash
xcodebuild clean build -scheme YourApp -destination 'platform=macOS'
```

## アーカイブ（リリース用）

### iOS
```bash
xcodebuild archive -scheme YourApp -archivePath ./build/YourApp.xcarchive \
  -destination 'generic/platform=iOS'
```

### macOS
```bash
xcodebuild archive -scheme YourApp -archivePath ./build/YourApp.xcarchive \
  -destination 'platform=macOS'
```

## トラブルシューティング

### シミュレーター一覧
```bash
xcrun simctl list devices available
```

### 利用可能なデスティネーション
```bash
xcodebuild -showdestinations -scheme YourApp
```
