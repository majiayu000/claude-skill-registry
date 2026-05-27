---
name: check-nuxt-ui-v4
description: ドキュメント内のNuxt UI v3記法を検出し、v4記法への修正を支援します。「ドキュメントをチェックして」「Nuxt UI v4の記法を確認」などで呼び出されます。
---

# Nuxt UI v4 記法チェックスキル

## 概要

このスキルは、プロジェクト内のMarkdownドキュメント（特に `docs/working/` 配下）をスキャンし、Nuxt UI v3 の古い記法を検出して、v4 記法への修正を支援します。

## 使用シーン

- 新しいドキュメントを作成した後の品質チェック
- 既存ドキュメントのメンテナンス
- プロジェクト全体の一貫性確認
- 人間が手動で書いたドキュメントのレビュー

## チェック対象

### 検出パターン

| パターン | 問題 | 修正方法 |
|---------|------|---------|
| `UFormGroup` | v3 のコンポーネント名 | `UFormField` に置換 |
| `:options=` または `options=` | v3 の属性名 | `:items=` に置換 |
| `v-bind:options=` | v3 の属性名 | `:items=` に置換 |
| `UButtonGroup` | v4 では非推奨 | `UFieldGroup` に置換 |

### チェック対象ファイル

- `docs/working/**/*.md` - 開発作業ドキュメント
- `docs/**/*.md` - 永続化ドキュメント（オプション）
- `.claude/skills/**/SKILL.md` - スキルドキュメント（オプション）

## 実行手順

このスキルが呼び出されたら、以下の手順で実行してください：

### 1. スコープの確認

ユーザーに確認します：

- **特定のディレクトリのみ** をチェックするか
- **プロジェクト全体** をチェックするか

指定がない場合は `docs/working/` をデフォルトとします。

### 2. ファイルスキャン

対象ディレクトリ内の `.md` ファイルを検索します：

```bash
find docs/working -name "*.md" -type f
```

### 3. パターン検出

各ファイルに対して、以下のパターンを検索します：

- `UFormGroup` の使用箇所
- `options=` または `:options=` の使用箇所
- `v-bind:options=` の使用箇所
- `UButtonGroup` の使用箇所

検出には `grep` コマンドまたは Grep ツールを使用します。

### 4. 結果レポート

検出結果を以下の形式でユーザーに報告します：

```markdown
## チェック結果

### 検出された問題

#### ファイル: docs/working/20251230_example/design.md

**問題1: UFormGroup の使用（行123）**
```vue
<!-- 現在 -->
<UFormGroup label="データベース">
  <USelect v-model="selected" :options="databases" />
</UFormGroup>

<!-- 修正案 -->
<UFormField label="データベース" name="database">
  <USelect v-model="selected" :items="databases" />
</UFormField>
```

**問題2: options 属性の使用（行156）**
```vue
<!-- 現在 -->
<USelectMenu v-model="selected" :options="items" />

<!-- 修正案 -->
<USelectMenu v-model="selected" :items="items" />
```

### サマリー

- チェック対象ファイル: 10件
- 問題検出ファイル: 3件
- 検出された問題: 5件
  - UFormGroup: 2件
  - options 属性: 3件
```

### 5. 修正オプションの提示

ユーザーに以下のオプションを提示します：

1. **自動修正** - 検出された問題を自動で修正する
2. **手動修正** - ファイルパスと行番号を提示し、ユーザーが手動で修正
3. **スキップ** - チェックのみ実行し、修正は行わない

### 6. 自動修正（選択された場合）

ユーザーが自動修正を選択した場合：

1. 各ファイルに対して Edit ツールを使用
2. `UFormGroup` → `UFormField` に置換
3. `:options=` → `:items=` に置換
4. `options=` → `items=` に置換
5. `UButtonGroup` → `UFieldGroup` に置換
6. 修正完了をユーザーに報告

**注意**:
- コードブロック内のみを対象とし、説明文は変更しない
- 文脈を確認し、誤検出を避ける
- バックアップを推奨する

## チェックロジック

### 検出時の考慮事項

1. **コードブロック内のみ対象**
   - ` ```vue ` ブロック内のコードを優先的にチェック
   - Markdown のコードブロック外の説明文は慎重に扱う

2. **誤検出の回避**
   - `UFormGroup` が「v3の例」として意図的に記載されている場合は除外
   - コメントで `<!-- v3 の例 -->` などと明記されている場合は除外

3. **文脈の確認**
   - `options` が Nuxt UI コンポーネントの属性として使用されているか確認
   - 他の用途（変数名、プロパティ名など）との区別

## 使用例

詳細は [examples.md](examples.md) を参照してください。

## 関連ドキュメント

- `.claude/skills/generate-working-docs/SKILL.md` - ドキュメント生成スキル
- `CLAUDE.md` - プロジェクトガイドライン

## Nuxt UI v4 記法リファレンス

### v3 → v4 移行対応表

| v3（検出対象） | v4（修正後） | 説明 |
|---------------|-------------|------|
| `UFormGroup` | `UFormField` | フォームフィールドラッパー |
| `options` 属性 | `items` 属性 | USelect, USelectMenu等の選択肢 |
| `UButtonGroup` | `UFieldGroup` | ボタングループラッパー（v4では非推奨） |

### 正しい記法（v4）

```vue
<template>
  <!-- ✅ 正しい: UFormField を使用 -->
  <UFormField label="データベース" name="database">
    <USelect v-model="selected" :items="databases" />
  </UFormField>

  <!-- ✅ 正しい: items 属性を使用 -->
  <USelectMenu v-model="selected" :items="options" />

  <!-- ✅ 正しい: UFieldGroup を使用してボタンをグループ化 -->
  <UFieldGroup>
    <UButton color="primary">INSERT</UButton>
    <UButton color="gray">UPDATE</UButton>
    <UButton color="gray">DELETE</UButton>
  </UFieldGroup>
</template>
```

### 誤った記法（v3）

```vue
<template>
  <!-- ❌ 検出される: UFormGroup（v3） -->
  <UFormGroup label="データベース">
    <USelect v-model="selected" :options="databases" />
  </UFormGroup>

  <!-- ❌ 検出される: options 属性（v3） -->
  <USelectMenu v-model="selected" :options="options" />

  <!-- ❌ 検出される: UButtonGroup（v4では非推奨） -->
  <UButtonGroup>
    <UButton color="primary">INSERT</UButton>
    <UButton color="gray">UPDATE</UButton>
    <UButton color="gray">DELETE</UButton>
  </UButtonGroup>
</template>
```
