---
name: generate-design
description: 開発作業の設計書（design.md）を生成します。このスキルは単独で使用することも、generate-working-docsから呼び出されることもあります。
---

# 設計書生成スキル

## 概要

このスキルは、開発作業の設計書（`design.md`）を生成します。

## 使用シーン

- 要件定義書を元に設計を開始するとき
- パフォーマンス改善作業の最適化設計を開始するとき
- 既存の開発作業ディレクトリに設計書を追加するとき
- 設計書を再生成するとき

## 必要な情報

- **ディレクトリパス**: 設計書を配置する `docs/working/{YYYYMMDD}_{要件名}/` のパス
- **要件名**: 英語のケバブケース（例：`query-execution`, `export-csv`, `optimize-rendering`）
- **作業タイプ** (オプション): `"feature"` (新規機能開発) または `"performance"` (パフォーマンス改善)

## 前提条件

- `requirements.md` が存在すること（推奨）
  - 設計は要件定義を元に作成されるため

## 実行手順

### 1. ディレクトリパスと作業タイプの確認

ユーザーまたは親スキルから以下を取得します：
- 開発作業ディレクトリパス
- 作業タイプ（指定がない場合は `"feature"` をデフォルトとする）

### 2. テンプレートの選択

作業タイプに応じてテンプレートを選択します：
- `work_type = "feature"`: 新規機能開発用テンプレート
- `work_type = "performance"`: パフォーマンス改善用テンプレート

### 3. design.md の生成

[template.md](template.md) または [template-performance.md](template-performance.md) のテンプレートを使用して、`design.md` を生成します。

**重要**: Nuxt UI v4 の記法を使用してください。
- `UFormField` を使用（`UFormGroup` は使用禁止）
- `items` 属性を使用（`options` 属性は使用禁止）

### 3. 完了報告

生成したファイルのパスをユーザーに報告します。

## 永続化ドキュメントの参照

**重要**: 設計書生成時は、`docs/steering/` ディレクトリにある永続化ドキュメントを参照して、既存のアーキテクチャやコーディング規約に準拠した設計にしてください。

### 参照すべきドキュメント

| ドキュメント | 参照目的 |
|------------|---------|
| `docs/steering/03_architecture_specifications.md` | 技術スタック・アーキテクチャを確認し、設計が技術方針に準拠するか検証 |
| `docs/steering/04_repository_structure.md` | ディレクトリ構造・命名規則を確認し、適切なファイル配置を決定 |
| `docs/steering/05_development_guidelines.md` | コーディング規約を確認し、設計例が規約に準拠するか検証 |
| `docs/steering/06_ubiquitous_language.md` | プロジェクト用語の正しい使用を確認し、型定義や変数名に反映 |

### 参照ルール

1. **データ構造設計時**: ユビキタス言語定義書で正しい用語を使用し、型定義を作成
2. **ファイル配置設計時**: リポジトリ構造定義書で正しいディレクトリ構造を確認
3. **コード例記載時**: 開発ガイドラインとアーキテクチャ仕様書を確認し、規約に準拠したコードを記載
4. **API設計時**: 技術仕様書で既存のAPIパターンを確認し、一貫性のある設計を行う
5. **UI設計時**: `docs/steering/05_development_guidelines.md` の「2.4 多言語対応（i18n）」セクションを確認し、全ての表示文字列を翻訳キーで管理する設計とする

## テンプレート

詳細は [template.md](template.md) を参照してください。

## 技術仕様の注意事項

### 多言語対応（i18n）

**重要**: 全てのUI要素は多言語対応が必須です。

設計書作成時は以下を必ず確認してください：

- コード例にハードコードされた文字列がないこと
- 翻訳キー構造を設計し、ja.json と en.json への追加内容を明記すること
- 動的な値はプレースホルダー（`{name}`, `{count}` 等）で対応すること

詳細は `docs/steering/05_development_guidelines.md` の「2.4 多言語対応（i18n）」セクションを参照してください。

### Nuxt UI v4 コンポーネント記法

**重要**: このプロジェクトは Nuxt UI v4 を使用しています。コード例では必ず以下の記法を使用してください。

#### v3 → v4 移行対応表

| v3（使用禁止） | v4（使用必須） | 説明 |
|---------------|---------------|------|
| `UFormGroup` | `UFormField` | フォームフィールドラッパー |
| `options` 属性 | `items` 属性 | USelect, USelectMenu等の選択肢 |

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

## 関連スキル

- `generate-working-docs` - 全ドキュメントを生成するメインスキル
- `generate-requirements` - 要件定義書生成スキル
- `generate-tasklist` - タスクリスト生成スキル
- `generate-testing` - テスト手順書生成スキル
