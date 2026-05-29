---
name: deployment-environments-gha
description: |
  GitHub Actions の environments 設計、承認フロー、シークレット運用を体系化するスキル。
  複数環境の保護ルールと段階的デプロイを整理する。

  Anchors:
  • Release It! / 適用: 環境分離 / 目的: 本番保護
  • GitHub Actions / 適用: environments と approval / 目的: 標準的な運用設計
  • The Pragmatic Programmer / 適用: 自動化 / 目的: 手順の一貫性

  Trigger:
  Use when setting up multi-environment deployments, approval gates, protection rules, or environment-specific secrets in GitHub Actions.
  github actions environments, approval workflow, deployment gates, environment secrets
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# deployment-environments-gha

## 概要

GitHub Actions の環境設計から承認・シークレット・デプロイ戦略までを一貫して支援する。

## ワークフロー

### Phase 1: 環境セットアップ

**目的**: 環境と保護ルールを整理する。

**アクション**:

1. `references/environment-config.md` で設定方法を確認する。
2. `assets/environment-setup-checklist.md` で要件を整理する。
3. `references/requirements-index.md` で要件整合を確認する。

**Task**: `agents/environment-setup.md` を参照

### Phase 2: 承認フロー設計

**目的**: 承認ゲートとデプロイ条件を設計する。

**アクション**:

1. `references/approval-workflows.md` で承認パターンを確認する。
2. `assets/approval-workflow-template.md` でフローを整理する。
3. 例外条件を記録する。

**Task**: `agents/approval-workflow-design.md` を参照

### Phase 3: シークレット管理

**目的**: 環境別シークレットと変数を整理する。

**アクション**:

1. `assets/secrets-plan-template.md` で要件を整理する。
2. シークレットの管理方針を記録する。
3. ローテーション計画を整理する。

**Task**: `agents/secrets-management.md` を参照

### Phase 4: デプロイ戦略設計

**目的**: 段階的デプロイと検証フローを設計する。

**アクション**:

1. `assets/deployment-workflow.yaml` で実装例を確認する。
2. `agents/deployment-strategy.md` の観点で設計する。
3. `scripts/log_usage.mjs` で記録を更新する。

**Task**: `agents/deployment-strategy.md` を参照

## Task仕様ナビ

| Task                     | 起動タイミング | 入力     | 出力             |
| ------------------------ | -------------- | -------- | ---------------- |
| environment-setup        | Phase 1開始時  | 要件     | 環境設定メモ     |
| approval-workflow-design | Phase 2開始時  | 環境設定 | 承認フロー設計   |
| secrets-management       | Phase 3開始時  | 設定方針 | シークレット計画 |
| deployment-strategy      | Phase 4開始時  | 設計メモ | デプロイ戦略     |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                       | 理由                   |
| ------------------------------ | ---------------------- |
| 環境ごとに保護ルールを設定する | 誤デプロイを防止できる |
| 承認フローを明文化する         | 運用ミスを減らせる     |
| シークレットを分離する         | 情報漏えいを防げる     |
| デプロイ戦略を段階化する       | 影響を最小化できる     |

### 避けるべきこと

| 禁止事項               | 問題点             |
| ---------------------- | ------------------ |
| 全環境を同一設定で運用 | 本番保護が弱い     |
| 承認手順を省略         | 誤変更のリスク     |
| シークレットの共通化   | 露出リスクが増える |
| 戻し手順を省略         | 障害対応が遅れる   |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                      | 機能                         |
| ------------------------------- | ---------------------------- |
| `scripts/check-environment.mjs` | 環境設定チェック             |
| `scripts/validate-skill.mjs`    | スキル構造検証               |
| `scripts/log_usage.mjs`         | 使用記録と評価メトリクス更新 |

### references/（詳細知識）

| リソース     | パス                                                                   | 読込条件           |
| ------------ | ---------------------------------------------------------------------- | ------------------ |
| レベル1 基礎 | [references/Level1_basics.md](references/Level1_basics.md)             | 要件整理時         |
| レベル2 実務 | [references/Level2_intermediate.md](references/Level2_intermediate.md) | 承認設計時         |
| レベル3 応用 | [references/Level3_advanced.md](references/Level3_advanced.md)         | シークレット管理時 |
| レベル4 専門 | [references/Level4_expert.md](references/Level4_expert.md)             | 運用時             |
| 承認フロー   | [references/approval-workflows.md](references/approval-workflows.md)   | 承認設計時         |
| 環境設定     | [references/environment-config.md](references/environment-config.md)   | 設定時             |
| 要求仕様索引 | [references/requirements-index.md](references/requirements-index.md)   | 仕様確認時         |
| 旧スキル     | [references/legacy-skill.md](references/legacy-skill.md)               | 互換確認時         |

### assets/（テンプレート・素材）

| アセット                                | 用途             |
| --------------------------------------- | ---------------- |
| `assets/deployment-workflow.yaml`       | デプロイYAML例   |
| `assets/environment-setup-checklist.md` | 環境設定チェック |
| `assets/approval-workflow-template.md`  | 承認フロー整理   |
| `assets/secrets-plan-template.md`       | シークレット計画 |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
