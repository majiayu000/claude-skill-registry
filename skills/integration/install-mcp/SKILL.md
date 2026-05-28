---
name: install-mcp
description: MCP サーバーをインストールする。「MCP インストール」「MCP を追加」「MCP サーバー追加」「mcp add」「MCP を入れて」「MCP サーバーをインストール」「新しい MCP」などで起動。
allowed-tools: [Bash, AskUserQuestion]
---

# Install MCP

MCP サーバーをインストールします。

## 実行手順

1. ユーザーに以下を確認:
   - MCP サーバー名（例: github, filesystem, puppeteer）
   - スコープ（user または project）
2. `claude mcp add <name> --scope <scope>` コマンドを実行
3. 必要に応じて環境変数の設定を案内
4. インストール完了メッセージを表示

### 人気の MCP サーバー

| 名前 | 説明 | 必要な環境変数 |
|------|------|----------------|
| github | GitHub API 操作 | GITHUB_PERSONAL_ACCESS_TOKEN |
| filesystem | ファイルシステム操作 | なし |
| puppeteer | ブラウザ自動化 | なし |
| postgres | PostgreSQL 操作 | DATABASE_URL |
| sqlite | SQLite 操作 | なし |

### インストール確認フォーマット

```markdown
## MCP サーバーインストール

以下の設定でインストールしますか？

| 項目 | 値 |
|------|-----|
| サーバー名 | github |
| スコープ | user |

実行するコマンド:
\`\`\`bash
claude mcp add github --scope user
\`\`\`
```

### 出力フォーマット（インストール完了時）

```markdown
## インストール完了

MCP サーバー「github」をインストールしました。

### 環境変数の設定

このサーバーには以下の環境変数が必要です:

| 変数名 | 説明 |
|--------|------|
| GITHUB_PERSONAL_ACCESS_TOKEN | GitHub パーソナルアクセストークン |

設定方法:
\`\`\`bash
export GITHUB_PERSONAL_ACCESS_TOKEN="your_token_here"
\`\`\`

または `.claude/settings.json` の `env` セクションに追加してください。
```

### 重要な注意事項

- ✅ インストール前に確認を求める
- ✅ 必要な環境変数を案内
- ✅ スコープの選択肢を提示
- ❌ 環境変数の値自体は設定しない（セキュリティ上の理由）
