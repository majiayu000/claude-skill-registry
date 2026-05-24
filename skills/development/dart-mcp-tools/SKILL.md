---
name: dart-mcp-tools
description: Dart/Flutter MCP tools reference for app lifecycle, hot reload/restart, logging, widget inspection, and code analysis. Use when debugging Flutter applications.
---

# Dart MCP Tools

Dart/Flutter開発向けMCPツールリファレンス。

## Device Management

| Tool | Purpose |
|------|---------|
| `mcp__dart__list_devices` | 利用可能なデバイス/シミュレーター/エミュレーターを一覧表示 |
| `mcp__dart__list_running_apps` | 実行中のFlutterアプリを一覧表示 |

## App Lifecycle

| Tool | Purpose |
|------|---------|
| `mcp__dart__launch_app` | Flutterアプリをデバイスで起動 |
| `mcp__dart__stop_app` | 実行中のFlutterアプリを停止 |
| `mcp__dart__hot_reload` | Hot reload（状態を維持してコード反映） |
| `mcp__dart__hot_restart` | Hot restart（状態をリセットして再起動） |

## Debugging & Logs

| Tool | Purpose |
|------|---------|
| `mcp__dart__get_app_logs` | アプリケーションログを取得 |
| `mcp__dart__get_runtime_errors` | ランタイムエラーを取得 |
| `mcp__dart__connect_dart_tooling_daemon` | Dartツーリングデーモンに接続 |

## Widget Inspection

| Tool | Purpose |
|------|---------|
| `mcp__dart__get_widget_tree` | Widgetツリー構造を取得 |
| `mcp__dart__get_selected_widget` | 選択中Widgetの詳細を取得 |
| `mcp__dart__set_widget_selection_mode` | Widget選択モードを有効化 |
| `mcp__dart__get_active_location` | アクティブなコード位置を取得 |

## Code Quality

| Tool | Purpose |
|------|---------|
| `mcp__dart__analyze_files` | Dart analyzerを実行 |
| `mcp__dart__dart_fix` | 自動修正を適用 |
| `mcp__dart__run_tests` | テストを実行 |

---

## Typical Workflow

```
1. mcp__dart__list_devices        # デバイス確認
2. mcp__dart__launch_app          # アプリ起動
3. (コード変更)
4. mcp__dart__hot_restart         # 再起動
5. mcp__dart__get_app_logs        # ログ取得
6. 分析・修正・繰り返し
```

---

## Tips

### Hot Reload vs Hot Restart

| Hot Reload | Hot Restart |
|------------|-------------|
| UI変更、レイアウト調整 | initState変更、状態クラス変更 |
| 状態維持 | クリーンな状態でテスト |
| 高速 | やや遅い |

### Log Capture

1. `hot_restart` で古いログをクリア
2. 1アクションを実行
3. 即座に `get_app_logs` で取得
4. ノイズが少なく分析しやすい

### Widget Tree Debugging

1. `set_widget_selection_mode` で選択モード有効化
2. デバイス上でWidgetをタップ
3. `get_selected_widget` で詳細取得
4. `get_active_location` でソースコード位置を特定
