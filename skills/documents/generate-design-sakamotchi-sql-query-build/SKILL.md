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

## テンプレート

詳細は [template.md](template.md) を参照してください。

## 技術仕様の注意事項

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
