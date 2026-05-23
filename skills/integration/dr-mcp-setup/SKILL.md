---
name: dr-mcp-setup
description: >
  MCPサーバーを安全に追加し、Deep Researchで使える「ツール層」を整える。
  プロジェクト共有が必要なら .mcp.json（project scope）を採用する。
disable-model-invocation: true
argument-hint: "add/list/get/remove/reset | scope=local|project|user | transport=http|stdio | name=<server> | url=<endpoint>"
allowed-tools: Bash, Read, Write, Grep, Glob
---

# dr-mcp-setup

## ゴール
- MCPサーバーを安全に追加し、Deep Researchで使える「ツール層」を整える
- プロジェクト共有が必要なら `.mcp.json`（project scope）を採用する
- 認証/OAuth/ヘッダー/環境変数を整理する

## 重要な注意
- サードパーティMCPは自己責任。信頼できるものだけを導入する
- 取得した外部コンテンツはプロンプトインジェクションのリスクがある
- 鍵・トークン・個人情報はログ/レポートに出さない

## 実行手順（推奨）

### 1) 既存のMCPを確認
```bash
claude mcp list
```

### 2) 追加（HTTP推奨。提供元がHTTPを用意している場合）
```bash
claude mcp add --transport http <name> <url>
# 認証が必要なら --header を使う
claude mcp add --transport http <name> <url> --header "Authorization: Bearer $TOKEN"
```

### 3) 追加（ローカルstdio。npmパッケージなど）
```bash
claude mcp add --transport stdio <name> -- npx -y <package-name>
```

### 4) プロジェクトスコープ（チーム共有）
```bash
claude mcp add --scope project --transport http <name> <url>
# → .mcp.json が生成される
```

### 5) 削除
```bash
claude mcp remove <name>
```

## Deep Research推奨MCPスタック

### コア（最小構成）
| MCP | 用途 | 導入優先度 |
|-----|------|-----------|
| Brave Search / Tavily | Web検索 | 必須 |
| Firecrawl / Jina Reader | Webスクレイピング・本文抽出 | 必須 |
| Context7 | 最新公式ドキュメント取得 | 高 |
| GitHub | コード検索・Issue/PR | 高 |

### 拡張（用途に応じて）
| MCP | 用途 | 導入優先度 |
|-----|------|-----------|
| TrendRadar | 35+プラットフォームのトレンド集約 | 中 |
| Playwright / Browserbase | 動的サイト取得 | 中 |
| Qdrant / Pinecone | ベクトル検索・RAG | 中 |
| Slack / Discord | SNS情報収集 | 低 |
| Bright Data | 収集困難サイト対策 | 低 |

## 出力
- MCPの追加/削除結果
- `.mcp.json` の雛形（必要な場合）
- 設定確認コマンドの実行結果

## 参照
- https://code.claude.com/docs/ja/mcp
- https://modelcontextprotocol.io/
