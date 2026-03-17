---
name: auth-login
description: Google OAuth 認証を実行する。「Google ログイン」「認証して」「ログインして」「Google 認証」「アカウント追加」などで起動。
allowed-tools: [Read, Bash]
---

# Auth Login

Google OAuth 認証を実行してトークンを取得・保存します。

## 実行方法

### 基本的な認証（デフォルトプロファイル）

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_auth.py login
```

### プロファイルを指定して認証

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_auth.py login --profile work
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_auth.py login --profile personal
```

## 前提条件

- クライアント設定ファイルが `~/.config/shiiman-google/clients/default.json` に配置されていること
- 未配置の場合は「OAuth 設定」と言って手順を確認してください

## トークン保存先

- `~/.config/shiiman-google/tokens/{profile}.json`

## 注意事項

- ブラウザが自動で開き、Google 認証画面が表示されます
- 認証完了後、ブラウザを閉じてください
- トークンは自動的に保存され、次回から再認証不要です
