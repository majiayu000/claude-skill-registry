---
name: code-style-guides
description: |
  主要コードスタイルガイドの比較と適用を整理し、チーム規約の統一と移行を支援するスキル。
  Airbnb/Google/Standardの選定、カスタマイズ、移行計画を扱う。

  Anchors:
  • Clean Code (Robert C. Martin) / 適用: 命名と意図の明確化 / 目的: 可読性の向上
  • Style Guide Comparison / 適用: ガイド選定 / 目的: 適合性評価
  • Migration Patterns / 適用: 移行計画 / 目的: 変更影響の最小化

  Trigger:
  Use when selecting or migrating style guides, unifying team conventions, or customizing linting rules.
  code style guide, ESLint config, Prettier rules, migration, coding conventions
---

# code-style-guides

## 概要

主要スタイルガイドの比較と適用方針を整理し、設定と運用の一貫性を確保する。

## ワークフロー

### Phase 1: 現状整理

**目的**: 現行スタイルと要件を明確化する。

**アクション**:

1. 既存コードのスタイル傾向を把握する。
2. チームの規約と制約を整理する。
3. 比較対象となるガイドを選定する。

**Task**: `agents/analyze-style-requirements.md` を参照

### Phase 2: 適用設計

**目的**: 選定ガイドの適用方針と移行計画を作る。

**アクション**:

1. ガイドの差分と適用ルールを整理する。
2. カスタマイズ方針と例外ルールを定義する。
3. 移行ステップとレビュー基準を決める。

**Task**: `agents/design-style-adoption.md` を参照

### Phase 3: 検証と記録

**目的**: 設定適用の検証と記録を行う。

**アクション**:

1. スタイル検出スクリプトで現状を確認する。
2. 設定差分と影響範囲を整理する。
3. ログと評価情報を更新する。

**Task**: `agents/validate-style-rollout.md` を参照

## Task仕様ナビ

| Task                       | 起動タイミング | 入力            | 出力                       |
| -------------------------- | -------------- | --------------- | -------------------------- |
| analyze-style-requirements | Phase 1開始時  | 既存コード/規約 | 要件整理メモ、比較対象一覧 |
| design-style-adoption      | Phase 2開始時  | 要件整理メモ    | 適用方針、移行計画         |
| validate-style-rollout     | Phase 3開始時  | 適用方針        | 検証レポート、記録更新内容 |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                   | 理由                     |
| -------------------------- | ------------------------ |
| 既存規約と差分を明確化する | 影響範囲を把握するため   |
| 例外ルールを最小化する     | ガイドの一貫性を保つため |
| 移行計画を段階化する       | 変更負荷を下げるため     |

### 避けるべきこと

| 禁止事項                 | 問題点               |
| ------------------------ | -------------------- |
| ルール変更を一括適用する | レビュー負荷が増える |
| 例外を無制限に追加する   | ルールが形骸化する   |
| 検証を省略する           | 不整合が残る         |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                   | 機能                         |
| ---------------------------- | ---------------------------- |
| `scripts/detect-style.mjs`   | 既存スタイルの検出           |
| `scripts/log_usage.mjs`      | 使用記録と評価メトリクス更新 |
| `scripts/validate-skill.mjs` | スキル構造の検証             |

### references/（詳細知識）

| リソース     | パス                                                                         | 読込条件     |
| ------------ | ---------------------------------------------------------------------------- | ------------ |
| Level1 基礎  | [references/Level1_basics.md](references/Level1_basics.md)                   | 初回整理時   |
| Level2 実務  | [references/Level2_intermediate.md](references/Level2_intermediate.md)       | 適用設計時   |
| Level3 応用  | [references/Level3_advanced.md](references/Level3_advanced.md)               | 詳細比較時   |
| Level4 専門  | [references/Level4_expert.md](references/Level4_expert.md)                   | 改善ループ時 |
| 比較ガイド   | [references/style-guide-comparison.md](references/style-guide-comparison.md) | ガイド選定時 |
| カスタマイズ | [references/customization-patterns.md](references/customization-patterns.md) | 例外設計時   |
| 移行戦略     | [references/migration-strategies.md](references/migration-strategies.md)     | 移行計画時   |
| 旧スキル     | [references/legacy-skill.md](references/legacy-skill.md)                     | 互換確認時   |

### assets/（テンプレート・素材）

| アセット                  | 用途               |
| ------------------------- | ------------------ |
| `assets/airbnb-base.json` | Airbnb設定ベース   |
| `assets/google.json`      | Google設定ベース   |
| `assets/standard.json`    | Standard設定ベース |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
