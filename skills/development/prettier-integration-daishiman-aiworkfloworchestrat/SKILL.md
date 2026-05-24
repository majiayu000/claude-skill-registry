---
name: prettier-integration
description: |
  ESLintとPrettierの統合とフォーマット自動化の専門知識を提供します。
  責務分離、競合解決、エディタ統合、保存時自動実行を設計します。

  Anchors:
  • The Pragmatic Programmer (Hunt, Thomas) / 適用: 実践的改善アプローチ、自動化の価値判断 / 目的: ツール統合の最適化指針
  • Prettier公式ドキュメント / 適用: 設定オプション選択、デフォルト値理解 / 目的: opinionatedツールの適切な活用
  • ESLint + Prettier統合ガイド / 適用: 責務分離、競合回避パターン / 目的: 適切な統合設計

  Trigger:
  Use when setting up Prettier with ESLint, resolving formatting conflicts, configuring editor integration, or implementing automated formatting workflows.
  prettier integration, eslint prettier conflict, code formatting setup, auto format on save, prettier eslint setup, formatting automation

allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
---

# Prettier統合スキル

## 概要

ESLintとPrettierの統合とフォーマット自動化の専門知識。責務分離、競合解決、エディタ統合、保存時自動実行を設計します。

## ワークフロー

### Phase 1: 初期セットアップ

**目的**: Prettierをプロジェクトに導入し、基本設定を確立

**アクション**:

1. `references/basics.md` で基本概念を確認
2. `agents/setup-prettier.md` のTask仕様に従ってセットアップを実行
3. `assets/prettierrc-base.json` を参照して設定ファイルを作成

**成果物**: .prettierrc.json, .prettierignore, package.jsonスクリプト追加

### Phase 2: 競合解決

**目的**: ESLintとPrettierのルール競合を解決

**アクション**:

1. `references/conflict-resolution.md` で競合パターンを確認
2. `agents/resolve-conflicts.md` のTask仕様に従って競合を解決
3. eslint-config-prettierで自動無効化を実施

**成果物**: 競合のないESLint設定

### Phase 3: エディタ統合

**目的**: 保存時自動フォーマットを実現

**アクション**:

1. `references/editor-integration.md` でエディタ別パターンを確認
2. `agents/integrate-editor.md` のTask仕様に従って統合を実施
3. `assets/vscode-settings.json` を参照して設定

**成果物**: エディタ設定ファイル、保存時自動フォーマット動作確認

### Phase 4: 検証と記録

**目的**: セットアップ完了を検証し、フィードバックを記録

**アクション**:

1. `scripts/format-check.mjs` でフォーマット検証を実行
2. `scripts/log_usage.mjs` で実行記録を保存

## Task仕様（ナビゲーション）

| Task              | 起動タイミング | 入力             | 出力                   |
| ----------------- | -------------- | ---------------- | ---------------------- |
| setup-prettier    | Phase 1開始時  | プロジェクト情報 | Prettier設定ファイル   |
| resolve-conflicts | Phase 2開始時  | ESLint設定       | 競合解決済みESLint設定 |
| integrate-editor  | Phase 3開始時  | エディタ情報     | エディタ統合設定       |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- ESLintとPrettierを統合する時は責務分離を明確にする
- フォーマットルールの競合を解決する時はeslint-config-prettierを使用
- エディタでの保存時自動フォーマットを設定する時はエディタ固有のパターンに従う
- デフォルト設定を優先し、カスタマイズは最小限にとどめる
- チーム全体で同じ設定を共有する

### 避けるべきこと

- ESLintのstyling rulesとPrettierルールを重複設定しない
- 手動フォーマットと自動フォーマットを混在させない
- CI/CDパイプラインなしで本番環境にPrettierを導入しない
- アンチパターンや注意点を確認せずに進めない

## リソース参照

### references/（詳細知識）

| リソース     | パス                                                                           | 説明                         |
| ------------ | ------------------------------------------------------------------------------ | ---------------------------- |
| 基本概念     | See [references/basics.md](references/basics.md)                               | Prettier概要、責務分離の原則 |
| 統合パターン | See [references/patterns.md](references/patterns.md)                           | 実践的な統合パターン集       |
| 競合解決     | See [references/conflict-resolution.md](references/conflict-resolution.md)     | ESLint競合解決戦略           |
| エディタ統合 | See [references/editor-integration.md](references/editor-integration.md)       | エディタ別統合パターン       |
| 自動化戦略   | See [references/automation-strategies.md](references/automation-strategies.md) | CI/CD統合、自動化レベル      |

### scripts/（決定論的処理）

| スクリプト         | 用途                     | 使用例                                                          |
| ------------------ | ------------------------ | --------------------------------------------------------------- |
| `format-check.mjs` | Prettierフォーマット検証 | `node scripts/format-check.mjs --path ./src`                    |
| `log_usage.mjs`    | 使用記録・自動評価       | `node scripts/log_usage.mjs --result success --phase "Phase 3"` |

### assets/（テンプレート）

| テンプレート           | 用途                         |
| ---------------------- | ---------------------------- |
| `prettierrc-base.json` | 基本Prettier設定テンプレート |
| `vscode-settings.json` | VS Code設定テンプレート      |

## 主要概念

### 責務分離の原則

**ESLint 役割**:

- コード品質の検証
- バグの検出
- ベストプラクティスの強制

**Prettier 役割**:

- コードフォーマットの統一
- スタイルの自動修正
- チーム全体のコード一貫性

### 統合戦略

1. **eslint-config-prettier使用**: Prettierと競合するESLintルールを自動無効化
2. **実行順序の制御**: Prettier → ESLint --fix の順で実行
3. **エディタ統合**: 保存時に自動フォーマットを実行
4. **CI/CD統合**: PRレビュー時にフォーマットチェックを実施

## クイックスタート

### 1. Prettierインストール

```bash
pnpm add -D prettier eslint-config-prettier
```

### 2. Prettier設定作成

`.prettierrc.json`:

```json
{
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false,
  "semi": true,
  "singleQuote": true,
  "trailingComma": "es5"
}
```

### 3. ESLint設定更新

`.eslintrc.json`:

```json
{
  "extends": ["eslint:recommended", "prettier"]
}
```

### 4. package.jsonスクリプト追加

```json
{
  "scripts": {
    "format": "prettier --write .",
    "format:check": "prettier --check ."
  }
}
```

### 5. VS Code設定

`.vscode/settings.json`:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode"
}
```

## トラブルシューティング

### ESLintとPrettierの競合

**症状**: ESLintエラーを修正するとPrettier警告が出る

**解決**:

1. `eslint-config-prettier` をインストール
2. `.eslintrc.json` の `extends` 最後に `"prettier"` を追加
3. 競合チェック: `npx eslint-config-prettier .eslintrc.json`

### 保存時フォーマットが動作しない

**症状**: ファイル保存時に自動フォーマットされない

**解決**:

1. Prettier拡張機能がインストールされているか確認
2. `.vscode/settings.json` で `editor.defaultFormatter` を設定
3. `.prettierrc` がプロジェクトルートにあるか確認

### lint-stagedでエラー

**症状**: pre-commit hookが失敗する

**解決**:

```json
{
  "lint-staged": {
    "*.{ts,tsx,js,jsx}": ["prettier --write", "eslint --fix"]
  }
}
```

## 変更履歴

| Version | Date       | Changes                                                        |
| ------- | ---------- | -------------------------------------------------------------- |
| 3.0.0   | 2026-01-02 | 18-skills.md完全準拠：references階層化廃止、Task仕様書形式統一 |
| 2.0.0   | 2026-01-02 | 18-skills.md仕様準拠：frontmatter更新、references統合          |
| 1.1.0   | 2025-12-31 | YAML frontmatter拡張、Task仕様ナビ追加                         |
| 1.0.0   | 2025-12-24 | Spec alignment and required artifacts added                    |
