---
name: generate-tasklist
description: 開発作業のタスクリスト（tasklist.md）を生成します。このスキルは単独で使用することも、generate-working-docsから呼び出されることもあります。
---

# タスクリスト生成スキル

## 概要

このスキルは、開発作業のタスクリスト（`tasklist.md`）を生成します。

## 使用シーン

- 設計書を元にタスク分割を開始するとき
- 既存の開発作業ディレクトリにタスクリストを追加するとき
- タスクリストを再生成するとき

## 必要な情報

- **ディレクトリパス**: タスクリストを配置する `docs/working/{YYYYMMDD}_{要件名}/` のパス
- **要件名**: 英語のケバブケース（例：`query-execution`, `export-csv`）

## 前提条件

- `requirements.md` が存在すること（推奨）
- `design.md` が存在すること（推奨）
  - タスク分割は要件定義と設計を元に作成されるため

## 実行手順

### 1. ディレクトリパスの確認

ユーザーから開発作業ディレクトリパスを取得します。

### 2. tasklist.md の生成

[template.md](template.md) のテンプレートを使用して、`tasklist.md` を生成します。

### 3. 完了報告

生成したファイルのパスをユーザーに報告します。

## テンプレート

詳細は [template.md](template.md) を参照してください。

## 関連スキル

- `generate-working-docs` - 全ドキュメントを生成するメインスキル
- `generate-requirements` - 要件定義書生成スキル
- `generate-design` - 設計書生成スキル
- `generate-testing` - テスト手順書生成スキル
