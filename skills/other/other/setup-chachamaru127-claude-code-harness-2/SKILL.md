---
name: setup
description: "Unified setup hub: project init, tool setup, 2-agent config, harness-mem, codex CLI, and rule localization. Use when user mentions setup, initialization, new projects, workflow files, CI setup, LSP setup, MCP setup, codex setup, opencode setup, 2-Agent setup, PM coordination, Cursor setup, harness-mem, claude-mem integration, cross-session memory, localize rules, adapt rules. Do NOT load for: implementation work, reviews, build verification, or deployments."
description-en: "Unified setup hub: project init, tool setup, 2-agent config, harness-mem, codex CLI, and rule localization. Use when user mentions setup, initialization, new projects, workflow files, CI setup, LSP setup, MCP setup, codex setup, opencode setup, 2-Agent setup, PM coordination, Cursor setup, harness-mem, claude-mem integration, cross-session memory, localize rules, adapt rules. Do NOT load for: implementation work, reviews, build verification, or deployments."
description-ja: "統合セットアップハブ: プロジェクト初期化、ツール設定、2エージェント構成、harness-mem、Codex CLI、ルールローカライズ。Use when user mentions setup, initialization, new projects, workflow files, CI setup, LSP setup, MCP setup, codex setup, opencode setup, 2-Agent setup, PM coordination, Cursor setup, harness-mem, claude-mem integration, cross-session memory, localize rules, adapt rules. Do NOT load for: implementation work, reviews, build verification, or deployments."
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
argument-hint: "[ci|dev-tools|lsp|mcp|opencode|codex|webhook|remotion|skills|2agent|harness-mem|localize-rules]"
---

# Setup Skills

プロジェクトセットアップ、ツール設定、ワークフロー構成を一元管理するスキル群です。

## ルーティングテーブル

ユーザーの意図に応じて適切な reference にルーティングします。

### プロジェクト初期化

| 機能 | 詳細 |
|------|------|
| **適応的セットアップ** | See [references/adaptive-setup.md](references/adaptive-setup.md) |
| **スキャフォールディング** | See [references/project-scaffolding.md](references/project-scaffolding.md) |
| **ワークフローファイル** | See [references/workflow-files.md](references/workflow-files.md) |
| **設定ファイル** | See [references/claude-settings.md](references/claude-settings.md) |
| **プロジェクト種別確認** | See [references/project-type-detection.md](references/project-type-detection.md) |

### ツールセットアップ

| サブコマンド | 詳細 |
|------------|------|
| **CI/CD** | See [references/ci-setup.md](references/ci-setup.md) |
| **開発ツール (AST-Grep + LSP)** | See [references/dev-tools-setup.md](references/dev-tools-setup.md) |
| **LSP** | See [references/lsp-setup.md](references/lsp-setup.md) |
| **MCP サーバー** | See [references/mcp-setup.md](references/mcp-setup.md) |
| **OpenCode.ai** | See [references/opencode-setup.md](references/opencode-setup.md) |
| **Codex CLI** | See [references/codex-setup.md](references/codex-setup.md) |
| **Webhook** | See [references/webhook-setup.md](references/webhook-setup.md) |
| **Remotion** | See [references/remotion-setup.md](references/remotion-setup.md) |

### 2-Agent ワークフロー

| 機能 | 詳細 |
|------|------|
| **初期設定** | See [references/2agent-setup.md](references/2agent-setup.md) |
| **ファイル更新** | See [references/2agent-updating.md](references/2agent-updating.md) |
| **Cursor連携** | See [references/cursor-setup.md](references/cursor-setup.md) |

### メモリ・ルール

| 機能 | 詳細 |
|------|------|
| **Harness-Mem セットアップ** | See [references/harness-mem.md](references/harness-mem.md) |
| **ルールローカライズ** | See [references/localize-rules.md](references/localize-rules.md) |

## 実行手順

1. ユーザーのリクエストを分類
2. 上記の「ルーティングテーブル」から適切な参照ファイルを読む
3. その内容に従って実行
