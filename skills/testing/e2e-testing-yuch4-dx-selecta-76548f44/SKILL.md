---
name: e2e-testing
description: chrome-devtools MCPサーバーを使ったE2Eテストの実施・デバッグを行う。「E2Eテストを実施」「画面をテスト」「ユーザーフローを確認」「ブラウザで動作確認」「画面の表示を検証」などの依頼時に使用。ログインフロー、フォーム送信、ページ遷移などのユーザー操作をインタラクティブにテストする。
---

# E2E Testing Skill

chrome-devtools MCPサーバーを使用したE2Eテストの実施を支援する。

## 概要

このスキルはchrome-devtools MCPサーバーを使い、実際のブラウザを操作してE2Eテストを実施する。Playwrightなどのテストフレームワークではなく、MCPツールを直接使用してインタラクティブにテストを行う。

## 前提条件

- 開発サーバーが起動していること（`pnpm dev`）
- chrome-devtools MCPサーバーが有効であること
- Chromeブラウザが利用可能であること

## テスト実施ワークフロー

### 1. 開発サーバー起動確認

```bash
# サーバーが起動しているか確認、なければ起動
pnpm dev
```

### 2. ブラウザツールの有効化

テスト開始前に必要なツールカテゴリを有効化:

- `activate_browser_navigation_tools` - ページ作成・遷移
- `activate_snapshot_and_screenshot_tools` - スクリーンショット・スナップショット
- `activate_form_interaction_tools` - フォーム入力・キー操作
- `activate_element_interaction_tools` - ドラッグ・ホバー

### 3. テスト実施フロー

```
1. ページを開く/遷移する
2. スナップショットで要素のuidを取得
3. 要素を操作（クリック、入力など）
4. 結果を検証（テキスト確認、スクリーンショット）
5. 次のステップへ
```

## 主要MCPツール

### ナビゲーション系（activate_browser_navigation_tools）

| ツール | 用途 |
|--------|------|
| ページ作成 | 新しいブラウザページを開く |
| URL遷移 | 指定URLへ移動 |
| ページ一覧 | 開いているページを確認 |
| ページ選択 | 操作対象ページを切り替え |

### スナップショット系（activate_snapshot_and_screenshot_tools）

| ツール | 用途 |
|--------|------|
| `mcp_chrome-devtoo_take_screenshot` | スクリーンショット撮影 |
| テキストスナップショット | ページ構造とuid取得（操作に必須） |

### 操作系

| ツール | 用途 |
|--------|------|
| `mcp_chrome-devtoo_click` | 要素をクリック |
| `mcp_chrome-devtoo_fill` | テキスト入力・セレクト選択 |
| `mcp_chrome-devtoo_wait_for` | テキスト出現まで待機 |
| `mcp_chrome-devtoo_evaluate_script` | JavaScript実行 |

### その他

| ツール | 用途 |
|--------|------|
| `mcp_chrome-devtoo_emulate` | ネットワーク・位置情報エミュレート |
| `mcp_chrome-devtoo_resize_page` | 画面サイズ変更（レスポンシブ確認） |
| `mcp_chrome-devtoo_handle_dialog` | ダイアログ処理 |
| `mcp_chrome-devtoo_upload_file` | ファイルアップロード |

## テストパターン

### パターン1: ページ表示確認

```
1. activate_browser_navigation_tools でナビゲーションツール有効化
2. ページを http://localhost:3000/[path] に遷移
3. activate_snapshot_and_screenshot_tools でスナップショットツール有効化
4. テキストスナップショットで内容確認
5. 期待する要素・テキストが存在するか検証
6. 必要に応じてスクリーンショット撮影
```

### パターン2: フォーム入力・送信

```
1. 対象ページに遷移
2. テキストスナップショットでフォーム要素のuidを取得
3. mcp_chrome-devtoo_fill で各フィールドに値を入力
   - uid: スナップショットから取得した要素ID
   - value: 入力する値
4. mcp_chrome-devtoo_click で送信ボタンをクリック
5. mcp_chrome-devtoo_wait_for で結果表示を待機
6. 結果を検証
```

### パターン3: 認証フロー

```
1. /login ページに遷移
2. スナップショットでメール/パスワード入力欄のuidを取得
3. mcp_chrome-devtoo_fill でメールアドレス入力
4. mcp_chrome-devtoo_fill でパスワード入力
5. mcp_chrome-devtoo_click でログインボタンクリック
6. mcp_chrome-devtoo_wait_for でダッシュボード表示を待機
7. URL・表示内容を検証
```

### パターン4: ナビゲーション検証

```
1. 起点ページに遷移
2. スナップショットでリンク要素のuidを取得
3. mcp_chrome-devtoo_click でリンクをクリック
4. 遷移先URLを確認
5. スナップショットで遷移先の内容を検証
```

### パターン5: レスポンシブ確認

```
1. mcp_chrome-devtoo_resize_page でサイズ変更
   - モバイル: width=375, height=667
   - タブレット: width=768, height=1024
   - デスクトップ: width=1280, height=800
2. スクリーンショットで表示確認
3. レイアウト崩れがないか検証
```

## 検証方法

### テキスト検証

```
1. テキストスナップショットを取得
2. 期待するテキストが含まれているか確認
3. または mcp_chrome-devtoo_wait_for で特定テキストの出現を待機
```

### 視覚的検証

```
1. mcp_chrome-devtoo_take_screenshot でスクリーンショット取得
2. 表示を目視確認
3. 必要に応じてファイルに保存（filePath指定）
```

### JavaScript実行による検証

```javascript
// mcp_chrome-devtoo_evaluate_script で実行
() => {
  return {
    title: document.title,
    url: window.location.href,
    elementExists: !!document.querySelector('[data-testid="target"]'),
    inputValue: document.querySelector('input[name="email"]')?.value
  };
}
```

## このプロジェクトの主要テスト対象

| 機能 | パス | 主要シナリオ |
|------|------|-------------|
| ログイン | `/login` | メール認証、エラー表示 |
| 診断フロー | `/dashboard/diagnosis` | 6ステップ入力、送信 |
| 検索 | `/dashboard/search` | キーワード検索、結果表示 |
| 比較 | `/dashboard/compare` | 製品選択、比較表示 |
| 提案書 | `/dashboard/proposal` | 生成、エクスポート |

## よくある問題と対処

| 症状 | 原因 | 対処 |
|------|------|------|
| 要素が見つからない | uidが古い | スナップショット再取得 |
| クリックが効かない | 要素が非表示/覆われている | スクロール or 待機 |
| 入力できない | 要素タイプ不正 | fillではなくevaluate_script使用 |
| タイムアウト | 処理遅延 | wait_for で明示的に待機 |
| ダイアログで停止 | 未処理のalert/confirm | handle_dialog で処理 |

## テスト実施チェックリスト

- [ ] 開発サーバーが起動しているか
- [ ] 必要なツールカテゴリを有効化したか
- [ ] 操作前にスナップショットでuidを取得したか
- [ ] 非同期処理後はwait_forで待機したか
- [ ] エラーケースもテストしたか
- [ ] スクリーンショットで結果を記録したか

## このプロジェクトの主要テスト対象

| 機能 | パス | 主要シナリオ |
|------|------|-------------|
| ログイン | `/login` | メール認証、エラー表示 |
| 診断フロー | `/dashboard/diagnosis` | 6ステップ入力、送信 |
| 検索 | `/dashboard/search` | キーワード検索、結果表示 |
| 比較 | `/dashboard/compare` | 製品選択、比較表示 |
| 提案書 | `/dashboard/proposal` | 生成、エクスポート |

## よくある問題と対処

| 症状 | 原因 | 対処 |
|------|------|------|
| 要素が見つからない | uidが古い | スナップショット再取得 |
| クリックが効かない | 要素が非表示/覆われている | スクロール or 待機 |
| 入力できない | 要素タイプ不正 | fillではなくevaluate_script使用 |
| タイムアウト | 処理遅延 | wait_for で明示的に待機 |
| ダイアログで停止 | 未処理のalert/confirm | handle_dialog で処理 |

## テスト実施チェックリスト

- [ ] 開発サーバーが起動しているか
- [ ] 必要なツールカテゴリを有効化したか
- [ ] 操作前にスナップショットでuidを取得したか
- [ ] 非同期処理後はwait_forで待機したか
- [ ] エラーケースもテストしたか
- [ ] スクリーンショットで結果を記録したか
