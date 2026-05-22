---
name: mobile-debug-tools
description: Cross-platform Mobile-MCP tools for device interaction, screenshots, touch simulation, and UI inspection. Works with iOS Simulator and Android Emulator for any mobile app (Flutter, native, React Native).
---

# Mobile Debug Tools

クロスプラットフォーム対応のMobile-MCPツールリファレンス。iOS Simulator、Android Emulatorで動作。

## Device & App Management

| Tool | Purpose |
|------|---------|
| `mcp__mobile-mcp__mobile_list_available_devices` | 利用可能なデバイスを一覧表示 |
| `mcp__mobile-mcp__mobile_list_apps` | インストール済みアプリを一覧表示 |
| `mcp__mobile-mcp__mobile_launch_app` | バンドルIDでアプリを起動 |
| `mcp__mobile-mcp__mobile_terminate_app` | 実行中のアプリを終了 |
| `mcp__mobile-mcp__mobile_install_app` | パスからアプリをインストール |
| `mcp__mobile-mcp__mobile_uninstall_app` | アプリをアンインストール |

## Screen Capture

| Tool | Purpose |
|------|---------|
| `mcp__mobile-mcp__mobile_take_screenshot` | スクリーンショット取得（base64） |
| `mcp__mobile-mcp__mobile_save_screenshot` | スクリーンショットをファイル保存 |
| `mcp__mobile-mcp__mobile_get_screen_size` | 画面サイズを取得 |

## Touch Interaction

| Tool | Purpose |
|------|---------|
| `mcp__mobile-mcp__mobile_click_on_screen_at_coordinates` | 指定座標をタップ |
| `mcp__mobile-mcp__mobile_double_tap_on_screen` | ダブルタップ |
| `mcp__mobile-mcp__mobile_long_press_on_screen_at_coordinates` | 長押し |
| `mcp__mobile-mcp__mobile_swipe_on_screen` | スワイプ操作 |

## UI Inspection

| Tool | Purpose |
|------|---------|
| `mcp__mobile-mcp__mobile_list_elements_on_screen` | 画面上のUI要素を一覧表示 |

## Input & Navigation

| Tool | Purpose |
|------|---------|
| `mcp__mobile-mcp__mobile_type_keys` | テキスト入力 |
| `mcp__mobile-mcp__mobile_press_button` | ハードウェアボタン押下（Back, Home等） |
| `mcp__mobile-mcp__mobile_open_url` | URLを開く（ディープリンクテスト） |

## Device Settings

| Tool | Purpose |
|------|---------|
| `mcp__mobile-mcp__mobile_set_orientation` | 画面の向きを設定 |
| `mcp__mobile-mcp__mobile_get_orientation` | 現在の向きを取得 |

---

## Typical Workflows

### Visual Bug Investigation

```
1. mobile_take_screenshot           # 現状確認
2. mobile_list_elements_on_screen   # UI要素の位置特定
3. mobile_click_on_screen_at_coordinates  # 操作実行
4. mobile_take_screenshot           # 結果確認
```

### Form Input Testing

```
1. mobile_list_elements_on_screen   # 入力フィールド位置特定
2. mobile_click_on_screen_at_coordinates  # フィールドをタップ
3. mobile_type_keys                 # テキスト入力
4. mobile_click_on_screen_at_coordinates  # 送信ボタンタップ
5. mobile_take_screenshot           # 結果確認
```

### Scroll & Navigation

```
1. mobile_swipe_on_screen           # スクロール
2. mobile_take_screenshot           # 表示確認
3. mobile_press_button              # 戻るボタン等
```

---

## Tips

### Coordinate Finding

1. `mobile_list_elements_on_screen` で要素のboundsを取得
2. 中心座標を計算: `x = left + width/2`, `y = top + height/2`
3. スクロール: 画面中央から端へスワイプ

### Screenshot Strategy

1. 操作前にスクリーンショット（Before）
2. 操作を実行
3. 操作後にスクリーンショット（After）
4. 視覚的に差分を比較

### Element Selection

`mobile_list_elements_on_screen` の結果から：
- `label` や `identifier` で要素を特定
- `frame` から座標を計算
- accessibility identifierがあれば最も確実
