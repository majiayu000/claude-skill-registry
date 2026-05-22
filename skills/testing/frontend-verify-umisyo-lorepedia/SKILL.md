---
name: frontend-verify
description: agent-browserを使用したフロントエンド実装の検証スキル。UI実装後の動作確認、インタラクションテスト、アクセシビリティ確認に使用。「フロントエンドを検証」「UIを確認」「/frontend-verify」「画面の動作確認」などで使用。UI実装完了時に自律的にトリガーする。
---

# Frontend Verify

agent-browserを使用してローカル開発サーバーのフロントエンドを検証するスキル。

## 前提条件

- 開発サーバーが起動していること（`pnpm dev`）
- `agent-browser` がインストール済み

## 基本ワークフロー

### 1. サーバー接続確認

```bash
agent-browser open http://localhost:3000
```

接続エラー時は開発サーバーの起動を促す。

### 2. スナップショット取得

```bash
agent-browser snapshot -i
```

インタラクティブ要素のアクセシビリティツリーを取得。出力例：
```
@e1 button "ログイン"
@e2 input[type="email"] placeholder="メールアドレス"
@e3 input[type="password"] placeholder="パスワード"
```

### 3. スクリーンショット取得

```bash
agent-browser screenshot --full /tmp/verify-$(date +%s).png
```

### 4. インタラクション実行

refを使って操作：
```bash
agent-browser fill @e2 "test@example.com"
agent-browser fill @e3 "password123"
agent-browser click @e1
```

### 5. 結果確認

```bash
agent-browser wait --load networkidle
agent-browser snapshot -i
agent-browser screenshot /tmp/result.png
```

## 使用シナリオ

### 基本検証（引数なし）

```
/frontend-verify
```

1. `http://localhost:3000` へアクセス
2. スナップショット取得
3. フルページスクリーンショット取得
4. 結果を報告

### パス指定検証

```
/frontend-verify /auth/signup
```

1. `http://localhost:3000/auth/signup` へアクセス
2. スナップショット取得
3. スクリーンショット取得
4. フォーム要素を特定して報告

### インタラクティブ検証

```
/frontend-verify --interact
```

1. ページへアクセス
2. スナップショットから操作可能な要素を特定
3. ユーザーに操作シナリオを確認
4. シナリオを実行（例：フォーム入力→送信→結果確認）
5. 各ステップでスクリーンショット取得

## 主要コマンド（クイックリファレンス）

| 操作 | コマンド |
|------|---------|
| ページ移動 | `open <url>` |
| スナップショット | `snapshot -i` |
| スクリーンショット | `screenshot [--full] <path>` |
| クリック | `click <ref>` |
| 入力 | `fill <ref> <text>` |
| 待機 | `wait --text "..." / --load networkidle` |
| 状態確認 | `is visible <ref>` |

詳細は [references/agent-browser-commands.md](references/agent-browser-commands.md) を参照。

## セッション管理

複数ステップの検証では同一セッションを維持：

```bash
export AGENT_BROWSER_SESSION="verify-session"
agent-browser open http://localhost:3000/auth/login
agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password"
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i  # ログイン後の状態を確認
```

## エラーハンドリング

| エラー | 対応 |
|--------|------|
| 接続エラー | 「開発サーバーを起動してください: pnpm dev」 |
| 要素が見つからない | スナップショットを再取得してrefを確認 |
| タイムアウト | `wait` コマンドで明示的に待機 |

## /rams との使い分け

| スキル | 用途 |
|--------|------|
| `/frontend-verify` | 詳細な動作検証、インタラクションテスト、デバッグ |
| `/rams` | アクセシビリティ・ビジュアルデザインのレビュー |

UI実装後は両方を実行することを推奨：
1. `/frontend-verify` で動作確認
2. `/rams` でデザイン・アクセシビリティレビュー
