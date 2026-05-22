---
name: generate-testing
description: 開発作業のテスト手順書（testing.md）を生成します。このスキルは単独で使用することも、generate-working-docsから呼び出されることもあります。
---

# テスト手順書生成スキル

## 概要

このスキルは、開発作業のテスト手順書（`testing.md`）を生成します。

## 使用シーン

- 設計・実装を元にテスト手順を作成するとき
- パフォーマンス改善の検証手順を作成するとき
- 既存の開発作業ディレクトリにテスト手順書を追加するとき
- テスト手順書を再生成するとき

## 必要な情報

- **ディレクトリパス**: テスト手順書を配置する `docs/working/{YYYYMMDD}_{要件名}/` のパス
- **要件名**: 英語のケバブケース（例：`query-execution`, `export-csv`, `optimize-rendering`）
- **作業タイプ** (オプション): `"feature"` (新規機能開発) または `"performance"` (パフォーマンス改善)

## 前提条件

- `requirements.md` が存在すること（推奨）
- `design.md` が存在すること（推奨）
- `tasklist.md` が存在すること（推奨）
  - テスト手順は要件定義、設計、タスクを元に作成されるため

## 実行手順

### 1. ディレクトリパスと作業タイプの確認

ユーザーまたは親スキルから以下を取得します：
- 開発作業ディレクトリパス
- 作業タイプ（指定がない場合は `"feature"` をデフォルトとする）

### 2. テンプレートの選択

作業タイプに応じてテンプレートを選択します：
- `work_type = "feature"`: 新規機能開発用テンプレート
- `work_type = "performance"`: パフォーマンス改善用テンプレート

### 3. testing.md の生成

[template.md](template.md) または [template-performance.md](template-performance.md) のテンプレートを使用して、`testing.md` を生成します。

**重要**:
- 新規機能開発の場合: 可能な限り手動操作で確認する手順を記載し、操作で確認できない項目のみ自動テストを記載します。
- パフォーマンス改善の場合: Before/After のパフォーマンス測定手順を中心に記載します。

### 3. 完了報告

生成したファイルのパスをユーザーに報告します。

## テンプレート

詳細は [template.md](template.md) を参照してください。

## 関連スキル

- `generate-working-docs` - 全ドキュメントを生成するメインスキル
- `generate-requirements` - 要件定義書生成スキル
- `generate-design` - 設計書生成スキル
- `generate-tasklist` - タスクリスト生成スキル
