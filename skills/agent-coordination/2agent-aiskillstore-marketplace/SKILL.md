---
name: 2agent
description: "Configures 2-Agent workflow between PM and implementation roles. Use when user mentions 2-Agent, 2エージェント, PM連携設定, Cursor設定, Cursor連携, 2-agent運用. Do NOT load for: 単独運用, ワークフロー実行, ハンドオフ処理."
allowed-tools: ["Read", "Write", "Edit", "Bash"]
metadata:
  skillport:
    category: 2agent
    tags: [2agent, pm, cursor, workflow-setup]
    alwaysApply: false
---

# 2-Agent Skills

2-Agent ワークフローの設定を担当するスキル群です。

## 含まれる小スキル

| スキル | 用途 |
|--------|------|
| setup-2agent-files | 2-Agent 運用用ファイル設定 |
| update-2agent-files | 2-Agent ファイルの更新 |
| setup-cursor | Cursor 連携セットアップ |

## ルーティング

- 初期設定: setup-2agent-files/doc.md
- ファイル更新: update-2agent-files/doc.md
- Cursor連携: setup-cursor/doc.md

## 実行手順

1. ユーザーのリクエストを分類
2. 適切な小スキルの doc.md を読む
3. その内容に従って設定
