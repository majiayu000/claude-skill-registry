---
name: clean-code-practices
description: |
  Clean Code の原則に基づき、命名・関数分割・重複排除などのコード品質改善を支援するスキル。
  可読性と保守性の向上、リファクタリング方針の整理を扱う。

  Anchors:
  • Clean Code (Robert C. Martin) / 適用: 命名と関数設計 / 目的: 可読性の向上
  • Refactoring (Martin Fowler) / 適用: 改善手順の整理 / 目的: 安全な改善
  • The Pragmatic Programmer (Hunt/Thomas) / 適用: DRYと意図表現 / 目的: 保守性の向上

  Trigger:
  Use when improving naming, splitting large functions, removing duplication, or validating clean code quality.
  clean code, naming, small functions, duplication, refactoring, readability
---

# clean-code-practices

## 概要

Clean Code 原則に沿ってコード品質を診断し、改善方針と検証を一貫して進める。

## ワークフロー

### Phase 1: 現状把握

**目的**: 品質課題と対象範囲を明確化する。

**アクション**:

1. 対象コードと制約を整理する。
2. 命名・関数サイズ・重複の課題を抽出する。
3. 参照すべき要件とレビュー基準を確認する。

**Task**: `agents/analyze-clean-code-issues.md` を参照

### Phase 2: 改善設計

**目的**: 改善方針とリファクタリング計画を作る。

**アクション**:

1. 命名と関数分割の方針を決める。
2. DRY原則とコメント方針を整理する。
3. レビューチェックリストを更新する。

**Task**: `agents/design-refactoring-plan.md` を参照

### Phase 3: 検証と記録

**目的**: 改善効果を検証し、記録を残す。

**アクション**:

1. 品質測定スクリプトで検証する。
2. 変更点と改善点をレポート化する。
3. ログと評価情報を更新する。

**Task**: `agents/validate-clean-code-improvements.md` を参照

## Task仕様ナビ

| Task                             | 起動タイミング | 入力            | 出力                           |
| -------------------------------- | -------------- | --------------- | ------------------------------ |
| analyze-clean-code-issues        | Phase 1開始時  | 対象コード/制約 | 課題一覧、対象範囲メモ         |
| design-refactoring-plan          | Phase 2開始時  | 課題一覧        | 改善方針、リファクタリング計画 |
| validate-clean-code-improvements | Phase 3開始時  | 改善方針        | 検証レポート、改善ログ         |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                         | 理由                   |
| -------------------------------- | ---------------------- |
| 改善対象を限定して進める         | 影響範囲を抑えるため   |
| 命名と関数分割をセットで検討する | 可読性が高まるため     |
| 検証結果を記録する               | 再発防止につながるため |

### 避けるべきこと

| 禁止事項                 | 問題点               |
| ------------------------ | -------------------- |
| 一括で大規模変更を行う   | レビュー負荷が増える |
| ルールを決めずに改善する | 一貫性が失われる     |
| 測定なしで効果判断する   | 改善が曖昧になる     |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                         | 機能                         |
| ---------------------------------- | ---------------------------- |
| `scripts/measure-code-quality.mjs` | コード品質の測定             |
| `scripts/log_usage.mjs`            | 使用記録と評価メトリクス更新 |
| `scripts/validate-skill.mjs`       | スキル構造の検証             |

### references/（詳細知識）

| リソース       | パス                                                                                 | 読込条件           |
| -------------- | ------------------------------------------------------------------------------------ | ------------------ |
| Level1 基礎    | [references/Level1_basics.md](references/Level1_basics.md)                           | 初回整理時         |
| Level2 実務    | [references/Level2_intermediate.md](references/Level2_intermediate.md)               | 設計時             |
| Level3 応用    | [references/Level3_advanced.md](references/Level3_advanced.md)                       | 詳細確認時         |
| Level4 専門    | [references/Level4_expert.md](references/Level4_expert.md)                           | 改善ループ時       |
| 意味のある命名 | [references/meaningful-names.md](references/meaningful-names.md)                     | 命名改善時         |
| 小さな関数     | [references/small-functions.md](references/small-functions.md)                       | 関数分割時         |
| DRY原則        | [references/dry-principle.md](references/dry-principle.md)                           | 重複排除時         |
| コメント方針   | [references/comments-and-documentation.md](references/comments-and-documentation.md) | ドキュメント整理時 |
| 要求索引       | [references/requirements-index.md](references/requirements-index.md)                 | 要件参照時         |
| 旧スキル       | [references/legacy-skill.md](references/legacy-skill.md)                             | 互換確認時         |

### assets/（テンプレート・素材）

| アセット                          | 用途                         |
| --------------------------------- | ---------------------------- |
| `assets/code-review-checklist.md` | コードレビューチェックリスト |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
