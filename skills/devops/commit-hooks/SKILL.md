---
name: commit-hooks
description: |
  Git commit フック（pre-commit/commit-msg/pre-push）の設計・実装・検証を体系化するスキル。
  Husky と lint-staged を軸に、品質ゲートと運用ルールを整理する。

  Anchors:
  • Pro Git / 適用: Git Hooks設計 / 目的: フック運用の基礎
  • Clean Code / 適用: 品質ゲート設計 / 目的: コミット品質の維持
  • Accelerate / 適用: フィードバックループ / 目的: 継続改善

  Trigger:
  Use when designing commit hooks, integrating husky/lint-staged, enforcing commit message rules, or validating pre-push checks.
  commit hooks, husky, lint-staged, commit-msg, pre-commit, pre-push
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# commit-hooks

## 概要

Git commit フックの設計から実装・検証までを整理し、品質ゲートと運用ルールを一貫して支援する。

## ワークフロー

### Phase 1: 要件整理

**目的**: 対象フック、品質要件、制約を明確化する。

**アクション**:

1. `references/Level1_basics.md` で基本概念を確認する。
2. `assets/hook-requirements-template.md` で要件を整理する。
3. `references/requirements-index.md` で要件整合を確認する。

**Task**: `agents/analyze-hook-requirements.md` を参照

### Phase 2: フック設計

**目的**: Husky と lint-staged の構成を設計し、品質ゲートを定義する。

**アクション**:

1. `references/husky-configuration.md` で導入前提を確認する。
2. `references/lint-staged-patterns.md` で対象範囲を設計する。
3. `assets/hook-policy-checklist.md` で設計観点を整理する。

**Task**: `agents/design-hook-configuration.md` を参照

### Phase 3: 実装と準備

**目的**: フック設定を実装し、検証に備える。

**アクション**:

1. `assets/pre-commit-basic.sh` で pre-commit を整備する。
2. `assets/commit-msg-template.sh` で commit-msg を整備する。
3. `assets/pre-push-template.sh` で pre-push を整備する。
4. `assets/lint-staged-advanced.js` で lint-staged を整備する。

**Task**: `agents/implement-hook-setup.md` を参照

### Phase 4: 検証と運用

**目的**: フックの動作を検証し、改善サイクルを回す。

**アクション**:

1. `scripts/test-hooks.mjs` で動作検証する。
2. `references/performance-optimization.md` で改善観点を確認する。
3. `scripts/log_usage.mjs` で記録を更新する。

**Task**: `agents/validate-hook-setup.md` を参照

## Task仕様ナビ

| Task                      | 起動タイミング | 入力         | 出力                         |
| ------------------------- | -------------- | ------------ | ---------------------------- |
| analyze-hook-requirements | Phase 1開始時  | 対象/要件    | 要件整理メモ、品質ゲート一覧 |
| design-hook-configuration | Phase 2開始時  | 要件整理メモ | フック設計、検証ルール       |
| implement-hook-setup      | Phase 3開始時  | フック設計   | 導入手順、設定案             |
| validate-hook-setup       | Phase 4開始時  | 設定案       | 検証レポート、改善提案       |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                    | 理由                 |
| --------------------------- | -------------------- |
| フックごとに目的を定義する  | 冗長な検証を避ける   |
| lint-stagedで対象を限定する | 実行時間を安定させる |
| commit-msg規約を明文化する  | 品質と履歴を揃える   |
| 検証結果を記録する          | 改善が継続する       |

### 避けるべきこと

| 禁止事項                   | 問題点             |
| -------------------------- | ------------------ |
| すべてのファイルを処理する | コミットが遅くなる |
| 依存ツールなしで有効化する | 失敗が続く         |
| 目的の重複                 | フックが冗長化する |
| 記録を残さない             | 改善が途切れる     |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                   | 機能                         |
| ---------------------------- | ---------------------------- |
| `scripts/test-hooks.mjs`     | フック動作テスト             |
| `scripts/log_usage.mjs`      | 使用記録と評価メトリクス更新 |
| `scripts/validate-skill.mjs` | スキル構造の検証             |

### references/（詳細知識）

| リソース     | パス                                                                             | 読込条件          |
| ------------ | -------------------------------------------------------------------------------- | ----------------- |
| レベル1 基礎 | [references/Level1_basics.md](references/Level1_basics.md)                       | 要件整理時        |
| レベル2 実務 | [references/Level2_intermediate.md](references/Level2_intermediate.md)           | 設計時            |
| レベル3 応用 | [references/Level3_advanced.md](references/Level3_advanced.md)                   | 実装時            |
| レベル4 専門 | [references/Level4_expert.md](references/Level4_expert.md)                       | 改善時            |
| Husky設定    | [references/husky-configuration.md](references/husky-configuration.md)           | Husky設計時       |
| lint-staged  | [references/lint-staged-patterns.md](references/lint-staged-patterns.md)         | lint-staged設計時 |
| 最適化       | [references/performance-optimization.md](references/performance-optimization.md) | 改善時            |
| 要求仕様索引 | [references/requirements-index.md](references/requirements-index.md)             | 仕様確認時        |
| 旧スキル     | [references/legacy-skill.md](references/legacy-skill.md)                         | 互換確認時        |

### assets/（テンプレート・素材）

| アセット                               | 用途                          |
| -------------------------------------- | ----------------------------- |
| `assets/hook-requirements-template.md` | 要件整理テンプレート          |
| `assets/hook-policy-checklist.md`      | 設計チェックリスト            |
| `assets/pre-commit-basic.sh`           | pre-commit フックテンプレート |
| `assets/commit-msg-template.sh`        | commit-msg フックテンプレート |
| `assets/pre-push-template.sh`          | pre-push フックテンプレート   |
| `assets/lint-staged-advanced.js`       | lint-staged 設定テンプレート  |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
