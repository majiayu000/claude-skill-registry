---
name: flutter-mobile-automation
description: FlutterアプリのE2Eテストとモバイル自動化の知見。Maestro、Mobile MCP、Dart MCPを使用したテスト作成・実行時に使用。
---

# Flutter Mobile Automation

E2Eテスト自動化と開発ワークフロー自動化の両方をカバー。

## 推奨構成: Maestro MCP + Dart MCP

FlutterアプリのE2Eテストと開発自動化には **Maestro MCP + Dart MCP** の組み合わせが最適。

## Dart MCP vs CLI 使い分け

**原則: DTD接続が必要な操作はMCP、それ以外はCLI**

### MCP推奨（CLIで代替不可）

| 操作 | ツール | 理由 |
|------|--------|------|
| アプリ起動 | `launch_app` | DTD URI取得が必要 |
| DTD接続 | `connect_dart_tooling_daemon` | MCP専用 |
| ホットリロード | `hot_reload` | DTD経由で実行 |
| ホットリスタート | `hot_restart` | DTD経由で実行 |
| ウィジェットツリー | `get_widget_tree` | DTD経由でのみ取得可能 |
| ランタイムエラー | `get_runtime_errors` | DTD経由でのみ取得可能 |
| アプリログ | `get_app_logs` | 起動中アプリのログ取得 |

### CLI推奨（MCPより効率的）

| 操作 | CLI コマンド | 理由 |
|------|-------------|------|
| デバイス一覧 | `flutter devices` | 出力がシンプル |
| テスト実行 | `flutter test` | 出力が見やすい、オプション豊富 |
| 静的解析 | `dart analyze` | 出力が見やすい |
| フォーマット | `dart format .` | 高速、差分表示 |
| 依存関係追加 | `flutter pub add <pkg>` | インタラクティブ |
| 依存関係取得 | `flutter pub get` | 高速 |
| プロジェクト作成 | `flutter create` | オプション豊富 |
| ビルド | `flutter build ios/apk` | 詳細な出力 |

### 典型的なワークフロー

```bash
# 1. CLI: ビルド・インストール
flutter build ios --simulator
xcrun simctl install booted build/ios/iphonesimulator/Runner.app

# 2. MCP: アプリ起動・DTD接続
# → launch_app → connect_dart_tooling_daemon

# 3. MCP: 開発中のデバッグ
# → get_widget_tree, get_runtime_errors, hot_reload

# 4. CLI: テスト・解析
flutter test
dart analyze
```

## ツール概要

### Maestro / Maestro MCP
- Flutter第一級サポートのE2Eテストフレームワーク
- **CLI**: YAMLでテストを記述 (`maestro test .maestro/test.yaml`)
- **MCP**: Claude Codeから対話的に操作（YAML不要）
  - スクリーンショット取得
  - タップ操作（テキスト/id指定、座標計算不要）
  - view hierarchy取得

### Dart MCP Server
- Flutter開発連携用MCPサーバー
- ウィジェットツリー取得（Flutter内部構造）
- ホットリロード/リスタート
- ランタイムエラー取得

### Mobile MCP（参考）
- Maestro MCPで代替可能なため通常は不要
- 座標ベースの操作が必要な特殊ケースでのみ使用

## Claude Code セットアップ

### 推奨設定（.claude/settings.json）

プロジェクト共通の許可設定はリポジトリに含めて共有：

```json
{
  "permissions": {
    "allow": [
      "Bash(flutter:*)",
      "Bash(dart:*)",
      "Bash(adb:*)",
      "Bash(xcrun simctl:*)",
      "Bash(maestro:*)",
      "Bash(MAESTRO_DRIVER_STARTUP_TIMEOUT=* maestro:*)",
      "Bash(git:*)",
      "Bash(gh:*)",
      "WebSearch",
      "WebFetch(domain:github.com)",
      "WebFetch(domain:docs.maestro.dev)",
      "mcp__dart-mcp__*",
      "mcp__maestro__*"
    ]
  }
}
```

### ローカル設定（.claude/settings.local.json）

ユーザー固有の設定は`.gitignore`に追加してローカルのみ：

```json
{
  "permissions": {
    "additionalDirectories": [
      "/Users/<user>/.maestro/tests"
    ]
  }
}
```

### Maestroテスト出力ディレクトリ

Maestro CLIはテスト結果を`~/.maestro/tests/`に出力する。
Claude Codeでエラーログを確認するには、このディレクトリを追加：

```bash
# Claude Codeで以下を実行
/add-dir ~/.maestro/tests
```

または`.claude/settings.local.json`に追加：

```json
{
  "permissions": {
    "additionalDirectories": [
      "/Users/<user>/.maestro/tests"
    ]
  }
}
```

## Maestro CLI プラットフォーム選択

### 推奨: iOSシミュレーター

Maestro CLIは**iOSシミュレーター**での実行を推奨。

| プラットフォーム | launchApp | 安定性 | 備考 |
|---|---|---|---|
| **iOS 18.x** | ✅ | ⭐⭐⭐ | 推奨 |
| Android API 30 | ⚠️ | ⭐ | 初回のみ動作、以降不安定 |
| Android API 34+ | ❌ | - | TCP forwarding / timeout エラー |

### 既知の問題（Maestro 2.0.10）

- [Issue #2839](https://github.com/mobile-dev-inc/Maestro/issues/2839): launchAppが最初の1回しか動作しない
- [Issue #1927](https://github.com/mobile-dev-inc/maestro/issues/1927): Maestro Studio起動中はlaunchApp失敗

### iOS E2Eテスト実行

```bash
# iOSシミュレーター起動
xcrun simctl boot "iPhone 16 Pro"

# iOSアプリビルド・インストール
flutter build ios --simulator
xcrun simctl install booted build/ios/iphonesimulator/Runner.app

# テスト実行（タイムアウト増加推奨）
MAESTRO_DRIVER_STARTUP_TIMEOUT=120000 \
maestro --device "<DEVICE_ID>" \
  test -e APP_ID=com.example.flutterE2eInvestigation \
  .maestro/test.yaml
```

### Bundle ID の違い

iOS/Androidでbundle IDが異なる場合、環境変数で切り替え：

```yaml
# .maestro/test.yaml
appId: ${APP_ID}
---
- launchApp:
    clearState: true
```

```bash
# iOS
maestro test -e APP_ID=com.example.flutterE2eInvestigation .maestro/test.yaml

# Android
maestro test -e APP_ID=com.example.flutter_e2e_investigation .maestro/test.yaml
```

## Flutterビルドモードの使い分け

### ビルドモード比較

| モード | 用途 | ホットリロード | パフォーマンス |
|--------|------|---------------|---------------|
| **debug** | 機能開発・iOSテスト | ✅ | 低速 |
| **profile** | パフォーマンス計測 | ❌ | 高速 |
| **release** | 本番 | ❌ | 最速 |

### ビルドコマンド

```bash
# 機能開発用・iOSテスト（debug）
flutter run
flutter build ios --simulator

# パフォーマンス計測（profile）- Androidのみ
flutter build apk --profile

# 本番用（release）
flutter build apk --release
flutter build ios --release
```

### ワークフロー推奨

```
開発中:
  debug ビルド → Dart MCP で起動 → hot reload で変更反映

E2Eテスト:
  iOS シミュレーター → debug ビルド → Maestro CLI でテスト実行
```

## Maestro + Flutter ベストプラクティス

### Semanticsウィジェットの活用

Maestroは要素をセマンティクス情報で認識する。Flutterでは`Semantics`ウィジェットでアクセシビリティ情報を提供：

```dart
// ラベルで識別可能にする
Semantics(
  label: 'submit-button',
  child: ElevatedButton(
    onPressed: _submit,
    child: Text('Submit'),
  ),
)

// identifier属性を使用（Flutter 3.19+）
Semantics(
  identifier: 'login-button',
  child: ElevatedButton(...),
)
```

### Maestroでの要素指定

```yaml
# tooltipテキストで認識（FloatingActionButtonなど）
- tapOn: "Increment"

# テキストで認識
- tapOn: "Submit"

# 正規表現
- tapOn:
    text: ".*Login.*"

# identifier使用時（推奨）
- tapOn:
    id: "login-button"
```

### テストファイル構造

```
.maestro/
├── login_test.yaml
├── cart_test.yaml
└── checkout_flow.yaml
```

### 基本的なテスト例

```yaml
appId: com.example.myapp
---
- launchApp
- assertVisible: "Welcome"
- tapOn: "Login"
- inputText:
    id: "email-field"
    text: "test@example.com"
- tapOn: "Submit"
- assertVisible: "Dashboard"
```

## トラブルシューティング

### 要素が見つからない場合

1. `maestro hierarchy` でUI階層を確認
2. Semanticsウィジェットでラベル/識別子を追加
3. テキストマッチングを正規表現に変更

### Flutterウィジェットが認識されない場合

- `Semantics`ウィジェットでラップ
- `excludeSemantics: false`を確認
- `MergeSemantics`で子要素を統合

## ツール使い分けガイド

### 機能比較表

| 機能 | Dart MCP | Maestro MCP |
|------|----------|-------------|
| ウィジェットツリー | ✅ 詳細（Flutter内部） | - |
| アクセシビリティ情報 | - | ✅ accessibilityText |
| スクリーンショット | - | ✅ |
| 要素一覧 | - | ✅ CSV形式 |
| タップ操作 | ⚠️ 要設定 | ✅ テキスト/id指定 |
| ホットリロード | ✅ | - |
| ランタイムエラー | ✅ | - |
| E2Eシナリオ記述 | - | ✅ YAML / 対話的 |

### 推奨される使い分け

**Maestro MCP** (UI操作・確認)
- スクリーンショット取得
- タップ操作（テキスト指定、座標計算不要）
- view hierarchy確認
- E2Eテストシナリオ作成・実行

**Dart MCP** (開発・デバッグ)
- ウィジェットツリーの詳細確認
- ランタイムエラーの取得
- ホットリロード/リスタート
- アプリ起動とDTD接続

### 典型的なワークフロー

```
1. Dart MCP: アプリ起動 → DTD接続
2. Dart MCP: ウィジェットツリーでUI構造確認
3. Maestro MCP: スクリーンショットで視覚確認
4. Maestro MCP: 対話的にタップ操作
5. Maestro CLI: E2Eテストシナリオ作成・実行
6. Dart MCP: エラー時はランタイムエラー確認
```

### Dart MCP flutter_driver使用時

アプリ側に設定が必要：

```dart
// lib/driver_main.dart
import 'package:flutter_driver/driver_extension.dart';
import 'main.dart' as app;

void main() {
  enableFlutterDriverExtension();
  app.main();
}
```

## 実践知見（TODOアプリ検証）

### Semantics identifier → Android resource-id

`Semantics.identifier`はAndroidで`resource-id`として認識される：

```dart
Semantics(
  identifier: 'todo-fab-add',  // → resource-id=todo-fab-add
  label: 'Add new todo',       // → accessibilityText
  child: FloatingActionButton(...),
)
```

view hierarchy出力例：
```
accessibilityText=Add new todo; resource-id=todo-fab-add; class=android.widget.Button
```

### 動的IDパターン

リスト要素には動的IDを使用：

```dart
Semantics(
  identifier: 'todo-tile-${todo.id}',      // 例: todo-tile-5cd04af0-9019...
  identifier: 'todo-checkbox-${todo.id}',  // 例: todo-checkbox-5cd04af0-...
  ...
)
```

Maestroでの指定方法：
```yaml
# 動的IDはテキストマッチングで対応
- tapOn:
    text: "Mark Buy groceries as done"  # accessibilityTextで指定
```

### Semantics命名規則（実証済み）

```
パターン: {機能}-{要素タイプ}[-{動的ID}]

静的要素:
- todo-fab-add       # FAB
- search-field       # 検索フィールド
- save-button        # 保存ボタン
- category-chip-work # カテゴリチップ

動的要素:
- todo-tile-{uuid}     # Todoタイル
- todo-checkbox-{uuid} # チェックボックス
```

### Maestro MCPの制限事項

1. **日本語入力非対応**: `inputText`でUnicodeエラー
   ```
   Failed to input text: Unicode not supported: 買い物に行く
   ```
   → 英語でテストするか、Maestro CLIを使用

2. **動的ID指定**: `id:`では動的UUIDを直接指定できない
   → `text:`（accessibilityText）で代替

3. **スクロール操作**: `run_flow`でスワイプを使用
   ```yaml
   appId: any
   ---
   - swipe:
       start: 50%, 80%
       end: 50%, 30%
   ```

### 動画録画

E2Eテストの視覚的検証用に動画を録画する方法：

**xcrun simctl（推奨）**
```bash
# 録画開始（バックグラウンド）
xcrun simctl io <device_id> recordVideo --codec=h264 /path/to/video.mp4 &

# 録画停止
kill <pid>  # または Ctrl+C
```

**Maestro MCP**
```yaml
# フロー内で録画
- startRecording: recording_name
- tapOn: "Button"
- stopRecording
# → ~/.maestro/tests/ に保存
```

| 方法 | 利点 | 欠点 |
|------|------|------|
| xcrun simctl | 保存先自由、軽量 | 別プロセス管理が必要 |
| Maestro | フロー内完結 | 保存先固定 |

### エミュレーターへの画像追加

ギャラリー画像テスト用：
```bash
# 画像をエミュレーターにプッシュ
adb -s emulator-5554 push /path/to/image.png /sdcard/Pictures/

# メディアスキャンでギャラリーに認識させる
adb -s emulator-5554 shell am broadcast \
  -a android.intent.action.MEDIA_SCANNER_SCAN_FILE \
  -d file:///sdcard/Pictures/image.png
```

### Riverpod + SharedPreferences構成

検証済みの構成：
```
lib/
├── main.dart                 # ProviderScope設定
├── app.dart                  # MaterialApp
└── features/todo/
    ├── data/
    │   ├── models/           # Todo, Category
    │   └── repositories/     # SharedPreferences操作
    ├── providers/            # AsyncNotifierProvider
    └── ui/
        ├── screens/          # 画面
        └── widgets/          # Semantics付きウィジェット
```

### 動作確認済みワークフロー

```
1. Dart MCP: launch_app → connect_dart_tooling_daemon
2. Dart MCP: get_widget_tree でSemantics配置確認
3. Maestro MCP: inspect_view_hierarchy で状態確認（軽量）
4. Maestro MCP: tap_on (id/text指定) でUI操作
5. Maestro MCP: take_screenshot で視覚確認（必要時のみ）
6. Maestro CLI: YAMLテスト作成・自動実行
```

### 効率的な状態確認パターン

**推奨: アクセシビリティ情報優先**

画面の状態確認は以下の順序で行う：

1. **inspect_view_hierarchy（第一優先）**
   - 軽量で高速
   - resource-id、accessibilityText、bounds情報を取得
   - 操作対象の要素特定に十分

2. **take_screenshot（必要時のみ）**
   - 視覚的確認が必要な場合のみ使用
   - レイアウト崩れ、色、画像の確認
   - ユーザーへの結果報告

```
❌ 非効率: screenshot → 確認 → 操作 → screenshot → ...
✅ 効率的: hierarchy → 操作 → hierarchy → ... → screenshot（最終確認）
```

**view hierarchy出力例:**
```csv
element_num,bounds,attributes
54,"[53,1788][1028,2313]","accessibilityText=Attached image; resource-id=image-attachment-field; class=android.widget.ImageView"
67,"[53,2201][1028,2348]","accessibilityText=Save todo; resource-id=save-button; class=android.view.View"
```

この情報だけで要素の存在確認と操作が可能。

## 開発フロー

### 機能実装の流れ

```
1. 計画（Plan Mode）
   - EnterPlanMode で設計開始
   - 不明点は AskUserQuestion で確認
   - 計画ファイルに実装詳細を記述
   - ExitPlanMode で承認を得る

2. 実装
   - TodoWrite でタスク分解・進捗管理
   - 1タスク完了ごとに completed に更新
   - コード変更は最小限に

3. E2Eテスト
   - Dart MCP: アプリ起動・DTD接続
   - Maestro MCP: inspect_view_hierarchy で状態確認（軽量）
   - Maestro MCP: tap_on / input_text で操作
   - Maestro MCP: take_screenshot で視覚確認（必要時のみ）

4. コミット・プッシュ
   - Conventional Commits 形式
   - 機能単位でコミット
   - 適切なタイミングでプッシュ
```

### E2Eテスト時の状態確認パターン

```
✅ 推奨フロー:
   hierarchy → 操作 → hierarchy → 操作 → ... → screenshot（最終確認）

❌ 非効率フロー:
   screenshot → 操作 → screenshot → 操作 → ...
```

### Git運用

```bash
# コミット
git add -A && git commit -m "type(scope): description"

# プッシュ
git push

# リモート設定（初回のみ）
git remote add origin git@github.com:USER/REPO.git
git push -u origin main
```

## 参考リンク

- [Maestro Flutter Testing](https://docs.maestro.dev/platform-support/flutter)
- [Mobile MCP](https://github.com/mobile-next/mobile-mcp)
- [Dart MCP Server](https://github.com/dart-lang/ai/tree/main/pkgs/dart_mcp_server)
