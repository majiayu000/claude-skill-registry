---
name: setup
description: "Sets up new projects and generates workflow files like CLAUDE.md, AGENTS.md, Plans.md. Use when user mentions セットアップ, setup, 初期化, initialize, 新規プロジェクト, ワークフローファイル生成. Do NOT load for: 実装作業, レビュー, ビルド検証, デプロイ."
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
user-invocable: false
metadata:
  skillport:
    category: setup
    tags: [setup, initialize, workflow, project]
    alwaysApply: false
---

# Setup Skills

プロジェクトセットアップとワークフローファイル生成を担当するスキル群です。

## 含まれる小スキル

| スキル | 用途 |
|--------|------|
| adaptive-setup | プロジェクト状況に応じた適応的セットアップ |
| project-scaffolder | 新規プロジェクトのスキャフォールディング |
| generate-workflow-files | CLAUDE.md, AGENTS.md, Plans.md 生成 |
| generate-claude-settings | .claude/settings.json 生成 |
| ask-project-type | 曖昧ケースでユーザーに新規/既存を質問 |

## ルーティング

- 適応的セットアップ: adaptive-setup/doc.md
- スキャフォールディング: project-scaffolder/doc.md
- ワークフローファイル: generate-workflow-files/doc.md
- 設定ファイル: generate-claude-settings/doc.md
- プロジェクト種別確認: ask-project-type/doc.md

## 実行手順

1. ユーザーのリクエストを分類
2. 適切な小スキルの doc.md を読む
3. その内容に従ってセットアップ
