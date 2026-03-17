---
name: docs
description: "Generates documentation files including NotebookLM YAML and slide content. Use when user mentions ドキュメント, document, YAML, NotebookLM, スライド, slide, プレゼン. Do NOT load for: 実装作業, コード修正, レビュー, デプロイ."
allowed-tools: ["Read", "Write", "Edit"]
metadata:
  skillport:
    category: docs
    tags: [documentation, yaml, notebooklm, slides]
    alwaysApply: false
---

# Docs Skills

ドキュメント生成を担当するスキル群です。

## 含まれる小スキル

| スキル | 用途 |
|--------|------|
| notebooklm-yaml | NotebookLM 用 YAML 生成 |
| docs-notebooklm-slide-yaml | スライド用 YAML 生成 |

## ルーティング

- NotebookLM YAML: notebooklm-yaml/doc.md
- スライド YAML: docs-notebooklm-slide-yaml/doc.md

## 実行手順

1. ユーザーのリクエストを分類
2. 適切な小スキルの doc.md を読む
3. その内容に従って生成
