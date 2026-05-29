---
name: concurrency-control
description: |
  GitHub Actions の並行実行制御を設計し、レースコンディションを防止するスキル。
  concurrency.group と cancel-in-progress を用いた競合回避と検証手順を整理する。

  Anchors:
  • The Pragmatic Programmer / 適用: 並行実行制御と品質維持 / 目的: 実践的な改善原則の適用
  • GitHub Actions Concurrency 仕様 / 適用: group と cancel-in-progress の設定 / 目的: レースコンディション防止
  • CI/CD Pipeline パターン / 適用: ワークフロー設計と実行管理 / 目的: 安全なパイプライン構築

  Trigger:
  Use when implementing concurrency control in GitHub Actions workflows, preventing race conditions, or designing group-based cancellation strategies.
  concurrency control, github actions, group, cancel-in-progress, race condition
---

# concurrency-control

## 概要

GitHub Actions の並行実行制御を設計し、競合やレースコンディションを防止する。

## ワークフロー

### Phase 1: 要件整理

**目的**: 目的・競合・制約を明確化する。

**アクション**:

1. 対象ワークフローと競合シナリオを整理する。
2. group 設計の前提を整理する。
3. 成功条件と制約を整理する。

**Task**: `agents/analyze-concurrency-requirements.md` を参照

### Phase 2: 戦略設計

**目的**: group 設計とキャンセル方針を定義する。

**アクション**:

1. group の粒度と命名を設計する。
2. cancel-in-progress の方針を決める。
3. 検証手順と監視項目を整理する。

**Task**: `agents/design-concurrency-strategy.md` を参照

### Phase 3: 検証と記録

**目的**: 構成と設定を検証し記録する。

**アクション**:

1. `scripts/validate-skill.mjs` で構造を検証する。
2. `scripts/check-concurrency.mjs` で設定を検証する。
3. `scripts/log_usage.mjs` で記録を更新する。

**Task**: `agents/validate-concurrency-setup.md` を参照

## Task仕様ナビ

| Task                             | 起動タイミング | 入力               | 出力                           |
| -------------------------------- | -------------- | ------------------ | ------------------------------ |
| analyze-concurrency-requirements | Phase 1開始時  | 目的/競合          | 要件整理メモ、成功条件一覧     |
| design-concurrency-strategy      | Phase 2開始時  | 要件整理メモ       | concurrency 設計書、検証ガイド |
| validate-concurrency-setup       | Phase 3開始時  | concurrency 設計書 | 検証レポート、ログ更新内容     |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                        | 理由                         |
| ------------------------------- | ---------------------------- |
| 競合シナリオを整理する          | group 設計の根拠になるため   |
| group 命名を統一する            | 競合の把握が容易になるため   |
| cancel-in-progress を明文化する | 実行中断の影響を制御するため |
| テンプレートを参照する          | 設定漏れを防ぐため           |

### 避けるべきこと

| 禁止事項                 | 問題点                 |
| ------------------------ | ---------------------- |
| group を曖昧にする       | 競合が再発する         |
| 検証なしで運用する       | 失敗検知が遅れる       |
| キャンセル方針を省略する | 重要ジョブが中断される |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                      | 機能                         |
| ------------------------------- | ---------------------------- |
| `scripts/check-concurrency.mjs` | concurrency 設定の検証       |
| `scripts/validate-skill.mjs`    | スキル構造の検証             |
| `scripts/log_usage.mjs`         | 使用記録と評価メトリクス更新 |

### references/（詳細知識）

| リソース         | パス                                                                   | 読込条件     |
| ---------------- | ---------------------------------------------------------------------- | ------------ |
| レベル1 基礎     | [references/Level1_basics.md](references/Level1_basics.md)             | 初回整理時   |
| レベル2 実務     | [references/Level2_intermediate.md](references/Level2_intermediate.md) | 設計時       |
| レベル3 応用     | [references/Level3_advanced.md](references/Level3_advanced.md)         | 詳細設計時   |
| レベル4 専門     | [references/Level4_expert.md](references/Level4_expert.md)             | 改善ループ時 |
| concurrency 構文 | [references/concurrency-syntax.md](references/concurrency-syntax.md)   | 構成設計時   |
| 競合パターン     | [references/race-conditions.md](references/race-conditions.md)         | 競合整理時   |
| 旧スキル         | [references/legacy-skill.md](references/legacy-skill.md)               | 互換確認時   |

### assets/（テンプレート・素材）

| アセット                           | 用途                         |
| ---------------------------------- | ---------------------------- |
| `assets/concurrency-workflow.yaml` | concurrency 設定テンプレート |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
