---
name: database-seeding
description: |
  データベースの初期データ投入を安全に設計・実装・検証するスキル。
  開発/テスト/本番のデータ分離、シード戦略、再現性の確保を整理する。

  Anchors:
  • Designing Data-Intensive Applications / 適用: データ整合性 / 目的: 参照整合性の担保
  • Database Reliability Engineering / 適用: 運用設計 / 目的: 本番投入の安全性
  • Data Quality Principles / 適用: データ品質 / 目的: 再現性と検証性の確保

  Trigger:
  Use when planning database seeding, generating test fixtures, separating datasets by environment, or validating seed data quality.
  database seeding, test data, fixtures, seed strategy, environment separation, data validation
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# database-seeding

## 概要

シーディング要件の整理から設計・実装・検証までを一貫して支援し、環境ごとのデータ投入を安全に運用する。

## ワークフロー

### Phase 1: 要件整理

**目的**: 目的と制約を整理し、シード対象と優先度を明確化する。

**アクション**:

1. 目的別に対象データと投入範囲を整理する。
2. `assets/seeding-requirements-template.md` で要件を記録する。
3. `references/seed-strategies.md` で戦略の候補を整理する。

**Task**: `agents/seed-strategy-selection.md` を参照

### Phase 2: 設計

**目的**: 環境分離とデータ生成ルールを設計する。

**アクション**:

1. `references/environment-separation.md` で分離方針を確認する。
2. `references/data-generation.md` で生成ルールを整理する。
3. `assets/seed-file-template.ts` に沿って構成を決める。

**Task**: `agents/environment-separation.md` を参照

### Phase 3: 実装

**目的**: シードスクリプトを実装し、投入を実行する。

**アクション**:

1. `assets/seed-file-template.ts` を基にシードを実装する。
2. `scripts/seed-runner.mjs` で投入フローを確認する。
3. 重要な変更点を記録する。

**Task**: `agents/test-data-setup.md` を参照

### Phase 4: 検証と運用

**目的**: データ品質と再現性を検証し、改善記録を残す。

**アクション**:

1. `assets/seeding-validation-checklist.md` で検証する。
2. `agents/data-validation.md` の観点で品質を確認する。
3. `scripts/log_usage.mjs` で記録を更新する。

**Task**: `agents/data-validation.md` を参照

## Task仕様ナビ

| Task                    | 起動タイミング | 入力       | 出力                       |
| ----------------------- | -------------- | ---------- | -------------------------- |
| seed-strategy-selection | Phase 1開始時  | 要件メモ   | シード戦略案、優先度       |
| environment-separation  | Phase 2開始時  | 戦略案     | 環境分離方針、投入条件     |
| test-data-setup         | Phase 3開始時  | 設計方針   | テストデータ、投入結果     |
| fixture-management      | Phase 3開始時  | テスト要件 | フィクスチャ一覧、更新方針 |
| production-initial-data | Phase 3開始時  | 本番要件   | 本番初期データ計画         |
| data-validation         | Phase 4開始時  | 投入結果   | 検証レポート、改善提案     |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                     | 理由                   |
| ---------------------------- | ---------------------- |
| 環境別にシードを分離する     | 本番誤投入を防ぐ       |
| 参照整合性を先に設計する     | 投入順序の破綻を防ぐ   |
| テストデータを再現可能にする | テストの信頼性が上がる |
| 検証結果を必ず記録する       | 再現と改善が容易になる |

### 避けるべきこと

| 禁止事項                   | 問題点                 |
| -------------------------- | ---------------------- |
| 本番データを開発に流用する | 機密漏えいリスクが高い |
| シード手順を手作業に依存   | 再現性が失われる       |
| 変更履歴を残さない         | 原因調査が困難になる   |
| 検証を省略する             | 破綻したデータが残る   |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                   | 機能                         |
| ---------------------------- | ---------------------------- |
| `scripts/seed-runner.mjs`    | シード実行フロー支援         |
| `scripts/validate-skill.mjs` | スキル構造の検証             |
| `scripts/log_usage.mjs`      | 使用記録と評価メトリクス更新 |

### references/（詳細知識）

| リソース     | パス                                                                         | 読込条件     |
| ------------ | ---------------------------------------------------------------------------- | ------------ |
| レベル1 基礎 | [references/Level1_basics.md](references/Level1_basics.md)                   | 要件整理時   |
| レベル2 実務 | [references/Level2_intermediate.md](references/Level2_intermediate.md)       | 設計時       |
| レベル3 応用 | [references/Level3_advanced.md](references/Level3_advanced.md)               | 実装時       |
| レベル4 専門 | [references/Level4_expert.md](references/Level4_expert.md)                   | 検証時       |
| シード戦略   | [references/seed-strategies.md](references/seed-strategies.md)               | 戦略選定時   |
| データ生成   | [references/data-generation.md](references/data-generation.md)               | データ生成時 |
| 環境分離     | [references/environment-separation.md](references/environment-separation.md) | 分離設計時   |
| 要求仕様索引 | [references/requirements-index.md](references/requirements-index.md)         | 仕様確認時   |
| 旧スキル     | [references/legacy-skill.md](references/legacy-skill.md)                     | 互換確認時   |

### assets/（テンプレート・素材）

| アセット                                  | 用途                 |
| ----------------------------------------- | -------------------- |
| `assets/seed-file-template.ts`            | シードファイルの雛形 |
| `assets/seeding-requirements-template.md` | 要件整理テンプレート |
| `assets/seeding-validation-checklist.md`  | 検証チェックリスト   |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
