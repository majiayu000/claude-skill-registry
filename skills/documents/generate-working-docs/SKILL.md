---
name: generate-working-docs
description: 開発作業ドキュメントを自動生成します。YYYYMMDD_要件名の形式でディレクトリを作成し、requirements.md、design.md、tasklist.md、testing.mdを生成します。「開発作業ドキュメント作成」「新規開発のドキュメント作って」「ドキュメント生成」などで呼び出されます。
---

# 開発作業ドキュメント生成スキル

## 概要

このスキルは、プロジェクトの開発ガイドライン（`CLAUDE.md`の開発作業ドキュメント構成）に準拠した開発作業ドキュメント群を `docs/working/{YYYYMMDD}_{要件名}/` 配下に自動生成します。

**対応する作業タイプ**：
- 新規機能開発
- パフォーマンス改善・最適化作業

## 使用シーン

### 新規機能開発
- 新規開発作業の開始時
- 要件定義から実装までを体系的に進めたいとき
- ドキュメント構成を統一したいとき

### パフォーマンス改善
- パフォーマンスボトルネックの調査・改善時
- 計測→分析→実装→検証のサイクルを進めたいとき
- ベンチマーク結果を記録したいとき

## 生成ファイル

| ファイル | 内容（新規機能開発） | 内容（パフォーマンス改善） |
|---------|------|------|
| `requirements.md` | 要件定義書。この開発作業で実現したいことを記載 | 改善要件定義書。現状の問題点と目標値を記載 |
| `design.md` | 設計書。実装方針、データ構造、テストコードを記載 | 最適化設計書。ベンチマーク、ボトルネック分析、最適化方針を記載 |
| `tasklist.md` | タスクリスト。作業項目と進捗状況を管理 | タスクリスト。計測→分析→実装→検証の進捗を管理 |
| `task_{タスクID}.md` | 各タスクの詳細ドキュメント。必要に応じて作成 | 各タスクの詳細ドキュメント。必要に応じて作成 |
| `testing.md` | テスト手順書。操作手順で確認する方法を記載 | 検証手順書。before/after性能比較の方法を記載 |

## 実行手順

このスキルが呼び出されたら、以下の手順で実行してください：

### 1. 作業タイプの判定

ユーザーの要求から作業タイプを判定します：
- WBSに「パフォーマンス改善」「高速化」等のキーワードがある → **パフォーマンス改善**
- それ以外 → **新規機能開発**

**注意**: ユーザーに明示的に確認する必要はありません。コンテキストから判断してください。

### 2. 要件名の確認

ユーザーに要件名を確認します。要件名は英語のケバブケース（例：`query-execution`, `export-csv`, `optimize-rendering`）を推奨します。

### 3. ディレクトリ作成

本日の日付（YYYYMMDD形式）と要件名を組み合わせてディレクトリを作成します：

```bash
mkdir -p docs/working/{YYYYMMDD}_{要件名}
```

### 4. サブスキルの順次実行

以下のサブスキルを**順次**実行します（並列実行禁止）：

1. `generate-requirements` - 要件定義書生成
   - パラメータ: `directory_path`, `requirement_name`, `work_type`（"feature" または "performance"）
   - ディレクトリパスと要件名、作業タイプを渡す
2. `generate-design` - 設計書生成
   - パラメータ: `directory_path`, `requirement_name`, `work_type`（"feature" または "performance"）
   - ディレクトリパスと要件名、作業タイプを渡す
   - requirements.md を参照して設計を作成
3. `generate-tasklist` - タスクリスト生成
   - パラメータ: `directory_path`, `requirement_name`, `work_type`（"feature" または "performance"）
   - ディレクトリパスと要件名、作業タイプを渡す
   - requirements.md と design.md を参照してタスクを作成
4. `generate-testing` - テスト手順書生成
   - パラメータ: `directory_path`, `requirement_name`, `work_type`（"feature" または "performance"）
   - ディレクトリパスと要件名、作業タイプを渡す
   - requirements.md、design.md、tasklist.md を参照してテスト手順を作成

**重要**: 各スキルは前のスキルの成果物に依存するため、必ず順次実行してください。

**注意**:
- `task_{タスクID}.md` は初期生成せず、開発中に必要に応じて作成します。
- `work_type` パラメータは、各サブスキルが適切なテンプレートを選択するために使用されます。

### 5. 完了報告

生成したディレクトリとファイル一覧をユーザーに報告します。
作業タイプ（新規機能開発 または パフォーマンス改善）も明示します。

## 使用例

詳細は [examples.md](examples.md) を参照してください。

## 関連スキル

- `generate-requirements` - 要件定義書生成スキル
- `generate-design` - 設計書生成スキル
- `generate-tasklist` - タスクリスト生成スキル
- `generate-testing` - テスト手順書生成スキル

## 関連ドキュメント

- `CLAUDE.md` - 開発作業ドキュメントの構成ルール
- `docs/` - 永続化ドキュメント群

## 技術仕様の注意事項

### 永続化ドキュメントの参照

**重要**: ドキュメント生成時は、`docs/steering/` ディレクトリにある永続化ドキュメントを参照してください。

#### 参照すべきドキュメント

| ドキュメント | 参照目的 |
|------------|---------|
| `docs/steering/01_product_requirements.md` | プロダクト全体の要件・機能を確認 |
| `docs/steering/02_functional_design.md` | 既存の画面・機能設計を参照 |
| `docs/steering/03_architecture_specifications.md` | 技術スタック・アーキテクチャを確認 |
| `docs/steering/04_repository_structure.md` | ディレクトリ構造・命名規則を確認 |
| `docs/steering/05_development_guidelines.md` | コーディング規約を確認 |
| `docs/steering/06_ubiquitous_language.md` | プロジェクト用語の正しい使用 |
| `docs/steering/features/*.md` | 関連機能の詳細仕様を確認 |

#### 参照ルール

1. **要件定義書生成時**: プロダクト要求定義書と関連する機能詳細仕様を参照
2. **設計書生成時**: 技術仕様書、リポジトリ構造定義書、開発ガイドラインを参照
3. **コード例記載時**: ユビキタス言語定義書で用語を確認
4. **全ドキュメント生成時**: 既存の永続化ドキュメントとの整合性を保つ

### Nuxt UI v4 コンポーネント記法

**重要**: このプロジェクトは Nuxt UI v4 を使用しています。ドキュメント内のコード例では必ず以下の記法を使用してください。

#### v3 → v4 移行対応表

| v3（使用禁止） | v4（使用必須） | 説明 |
|---------------|---------------|------|
| `UFormGroup` | `UFormField` | フォームフィールドラッパー |
| `options` 属性 | `items` 属性 | USelect, USelectMenu等の選択肢 |
| `v-model` | `v-model` | 同じだが、itemsとの組み合わせに注意 |

#### 正しい記法例（v4）

```vue
<template>
  <!-- ✅ 正しい: UFormField + items -->
  <UFormField label="データベース" name="database">
    <USelect v-model="selected" :items="databases" />
  </UFormField>

  <!-- ✅ 正しい: USelectMenu + items -->
  <USelectMenu v-model="selected" :items="options" />
</template>
```

#### 誤った記法例（v3）

```vue
<template>
  <!-- ❌ 間違い: UFormGroup（v3） -->
  <UFormGroup label="データベース">
    <USelect v-model="selected" :options="databases" />
  </UFormGroup>

  <!-- ❌ 間違い: options 属性（v3） -->
  <USelectMenu v-model="selected" :options="options" />
</template>
```

### ドキュメント生成時のルール

1. **コード例には必ず Nuxt UI v4 の記法を使用する**
2. **v3 の記法（UFormGroup, options 属性）は絶対に使用しない**
3. **既存の `CLAUDE.md` に記載された技術スタック情報を参照する**
