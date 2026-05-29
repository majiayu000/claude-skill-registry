---
name: command-best-practices
description: |
  コマンド設計のベストプラクティス（単一責任/合成可能性/冪等性/DRY/保守性）を整理し、設計レビューと改善方針を支援するスキル。
  原則の適用判断、チェックリスト運用、検証手順を一貫して整理する。

  Anchors:
  • The Pragmatic Programmer (Andrew Hunt, David Thomas) / 適用: 設計原則の実務適用 / 目的: 実装品質の安定化

  Trigger:
  Use when reviewing command design best practices, refactoring command structure, or validating maintainability and composability.
  command best practices, single responsibility, composability, idempotency, DRY, maintainable commands
---

# command-best-practices

## 概要

コマンド設計のベストプラクティス（単一責任/合成可能性/冪等性/DRY/保守性）を整理し、設計レビューと改善方針を支援する。

## ワークフロー

### Phase 1: 現状整理

**目的**: 現行コマンドの課題と改善対象を整理する。

**アクション**:

1. 対象コマンドの目的と責務を整理する。
2. 原則適用の観点を選定する。
3. 参照ガイドとチェックリストを確認する。

**Task**: `agents/analyze-best-practices.md` を参照

### Phase 2: 改善設計

**目的**: 改善方針と適用原則を具体化する。

**アクション**:

1. 単一責任/合成可能性の観点で改善案を作る。
2. 冪等性/DRY/保守性の観点で補強案を作る。
3. チェックリストで設計を具体化する。

**Task**: `agents/design-best-practices.md` を参照

### Phase 3: 検証と記録

**目的**: 改善案を検証し、記録を残す。

**アクション**:

1. ベストプラクティス検証スクリプトで整合性を確認する。
2. 検証結果と改善点を整理する。
3. ログと評価情報を更新する。

**Task**: `agents/validate-best-practices.md` を参照

## Task仕様ナビ

| Task                    | 起動タイミング | 入力              | 出力                           |
| ----------------------- | -------------- | ----------------- | ------------------------------ |
| analyze-best-practices  | Phase 1開始時  | 対象コマンド/課題 | 要件整理メモ、原則適用候補     |
| design-best-practices   | Phase 2開始時  | 要件整理メモ      | 改善方針、チェックリスト適用案 |
| validate-best-practices | Phase 3開始時  | 改善方針          | 検証レポート、改善方針         |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                       | 理由                       |
| ------------------------------ | -------------------------- |
| 単一責任の観点で責務を整理する | 変更容易性が高まるため     |
| 合成可能性を意識して分割する   | 再利用性が高まるため       |
| 検証と記録をセットで行う       | 改善の継続が可能になるため |

### 避けるべきこと

| 禁止事項                   | 問題点           |
| -------------------------- | ---------------- |
| 複数責務をひとつに押し込む | 変更影響が広がる |
| 検証前に適用を進める       | 不整合が残る     |
| 記録を残さない             | 改善が続かない   |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                         | 機能                         |
| ---------------------------------- | ---------------------------- |
| `scripts/check-best-practices.mjs` | ベストプラクティス検証       |
| `scripts/log_usage.mjs`            | 使用記録と評価メトリクス更新 |
| `scripts/validate-skill.mjs`       | スキル構造の検証             |

### references/（詳細知識）

| リソース     | パス                                                                                           | 読込条件     |
| ------------ | ---------------------------------------------------------------------------------------------- | ------------ |
| レベル1 基礎 | [references/Level1_basics.md](references/Level1_basics.md)                                     | 初回整理時   |
| レベル2 実務 | [references/Level2_intermediate.md](references/Level2_intermediate.md)                         | 改善設計時   |
| レベル3 応用 | [references/Level3_advanced.md](references/Level3_advanced.md)                                 | 適用深化時   |
| レベル4 専門 | [references/Level4_expert.md](references/Level4_expert.md)                                     | 改善ループ時 |
| 単一責任     | [references/single-responsibility-principle.md](references/single-responsibility-principle.md) | 責務整理時   |
| 合成可能性   | [references/composability-principle.md](references/composability-principle.md)                 | 分割検討時   |
| 旧スキル     | [references/legacy-skill.md](references/legacy-skill.md)                                       | 互換確認時   |

### assets/（テンプレート・素材）

| アセット                            | 用途                             |
| ----------------------------------- | -------------------------------- |
| `assets/best-practice-checklist.md` | ベストプラクティスチェックリスト |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
