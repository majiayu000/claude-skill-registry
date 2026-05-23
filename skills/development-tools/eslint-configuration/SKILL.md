---
name: eslint-configuration
description: |
  ESLint設定ファイルの作成・更新、ルールセット選択、パーサー設定、プラグイン統合を行う専門スキル。
  プロジェクトの言語・フレームワークに最適化された設定を生成し、Prettierとの競合解決も行う。

  Anchors:
  • ESLint公式ドキュメント / 適用: ルール定義・設定形式 / 目的: 仕様準拠
  • typescript-eslint / 適用: TypeScript設定 / 目的: 型チェック統合
  • eslint-plugin-react / 適用: React固有ルール / 目的: JSX最適化
  • Prettier連携ガイド / 適用: 競合解決 / 目的: フォーマッタ共存

  Trigger:
  Use when creating or updating ESLint configuration, selecting rulesets, configuring parsers, integrating plugins, or resolving Prettier conflicts.
  eslint, eslintrc, flat config, typescript-eslint, react eslint, prettier conflict, lint rules, code quality

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# ESLint Configuration Skill

## 概要

ESLint設定ファイルの作成・更新を行うスキル。プロジェクトの技術スタック（言語、フレームワーク）を分析し、最適なルールセット・パーサー・プラグインを選定・設定する。

## ワークフロー

### Phase 1: プロジェクト分析

**目的**: プロジェクトの技術スタックと既存設定を把握

**アクション**:

1. package.json、tsconfig.json、既存eslint設定を確認
2. 使用言語（JavaScript/TypeScript）を特定
3. フレームワーク（React/Vue/Node等）を判定
4. 既存のlint関連設定との整合性を確認

**Task**: `agents/analyze-project.md` を参照

### Phase 2: 設定生成

**目的**: 最適なESLint設定を生成

**アクション**:

1. ベースルールセットを選定（recommended/strict等）
2. パーサー設定（@typescript-eslint/parser等）
3. プラグイン統合（react, import, boundaries等）
4. カスタムルール適用
5. Prettier競合ルールの無効化

**Task**: `agents/configure-rules.md` を参照

### Phase 3: 検証

**目的**: 生成した設定の動作確認

**アクション**:

1. 設定ファイルの構文検証
2. `eslint --print-config` で設定確認
3. サンプルファイルでlint実行
4. エラー・警告の適切性確認

**Task**: `agents/validate-config.md` を参照

## Task仕様（ナビゲーション）

| Task            | 起動タイミング | 入力               | 出力               |
| --------------- | -------------- | ------------------ | ------------------ |
| analyze-project | Phase 1開始時  | プロジェクトパス   | 技術スタック情報   |
| configure-rules | Phase 2開始時  | 技術スタック情報   | ESLint設定ファイル |
| validate-config | Phase 3開始時  | ESLint設定ファイル | 検証結果レポート   |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- Flat Config形式（eslint.config.js）を優先使用
- TypeScriptプロジェクトでは `@typescript-eslint` を使用
- Prettierと併用時は `eslint-config-prettier` を追加
- 段階的に厳格化（最初は recommended から）
- プロジェクト固有ルールは明確にコメント

### 避けるべきこと

- .eslintrc形式の新規作成（レガシー形式）
- 不要なプラグインの追加
- ルール無効化の乱用（disable コメント）
- 競合するプラグインの併用
- 型チェックルールの過剰適用（パフォーマンス低下）

## リソース参照

### references/（詳細知識）

| リソース             | パス                                                                         | 用途                      |
| -------------------- | ---------------------------------------------------------------------------- | ------------------------- |
| パーサー設定ガイド   | See [references/parser-configuration.md](references/parser-configuration.md) | TypeScript/JSパーサー設定 |
| プラグイン統合ガイド | See [references/plugin-integration.md](references/plugin-integration.md)     | プラグイン選定・設定      |
| ルール選定ガイド     | See [references/rule-selection-guide.md](references/rule-selection-guide.md) | ルールセット選択基準      |

### scripts/（決定論的処理）

| スクリプト            | 用途               | 使用例                                              |
| --------------------- | ------------------ | --------------------------------------------------- |
| `validate-config.mjs` | 設定ファイル検証   | `node scripts/validate-config.mjs eslint.config.js` |
| `log_usage.mjs`       | フィードバック記録 | `node scripts/log_usage.mjs --result success`       |

### assets/（テンプレート）

| テンプレート            | 用途                 |
| ----------------------- | -------------------- |
| `typescript-base.json`  | TypeScript基本設定   |
| `react-typescript.json` | React+TypeScript設定 |
| `nextjs.json`           | Next.js専用設定      |

## 変更履歴

| Version | Date       | Changes                            |
| ------- | ---------- | ---------------------------------- |
| 2.0.0   | 2026-01-01 | 18-skills.md完全準拠版として再構築 |
| 1.0.0   | 2025-12-24 | 初版作成                           |
