---
name: generate-requirements
description: 開発作業の要件定義書（requirements.md）を生成します。このスキルは単独で使用することも、generate-working-docsから呼び出されることもあります。
---

# 要件定義書生成スキル

## 概要

このスキルは、開発作業の要件定義書（`requirements.md`）を生成します。

## 使用シーン

- 新規開発作業の要件定義を開始するとき
- パフォーマンス改善作業の要件定義を開始するとき
- 既存の開発作業ディレクトリに要件定義書を追加するとき
- 要件定義書を再生成するとき

## 必要な情報

- **ディレクトリパス**: 要件定義書を配置する `docs/working/{YYYYMMDD}_{要件名}/` のパス
- **要件名**: 英語のケバブケース（例：`query-execution`, `export-csv`, `optimize-rendering`）
- **作業タイプ** (オプション): `"feature"` (新規機能開発) または `"performance"` (パフォーマンス改善)

## 実行手順

### 1. ディレクトリパスと作業タイプの確認

ユーザーまたは親スキルから以下を取得します：
- 既存の開発作業ディレクトリパス、または要件名（新規の場合は本日の日付と組み合わせてディレクトリを作成）
- 作業タイプ（指定がない場合は `"feature"` をデフォルトとする）

### 2. テンプレートの選択

作業タイプに応じてテンプレートを選択します：
- `work_type = "feature"`: 新規機能開発用テンプレート
- `work_type = "performance"`: パフォーマンス改善用テンプレート

### 3. requirements.md の生成

[template.md](template.md) または [template-performance.md](template-performance.md) のテンプレートを使用して、`requirements.md` を生成します。

### 3. 完了報告

生成したファイルのパスをユーザーに報告します。

## テンプレート

詳細は [template.md](template.md) を参照してください。

## 関連スキル

- `generate-working-docs` - 全ドキュメントを生成するメインスキル
- `generate-design` - 設計書生成スキル
- `generate-tasklist` - タスクリスト生成スキル
- `generate-testing` - テスト手順書生成スキル
