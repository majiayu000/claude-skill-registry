---
name: backup-recovery
description: |
  データベースバックアップ戦略、RPO/RTO設計、復旧ランブック作成、検証運用を体系化するスキル。
  多層防御と復旧演習を通じて、復旧準備の抜け漏れを防ぐ。

  Anchors:
  • Database Reliability Engineering / 適用: 信頼性設計 / 目的: 失敗前提の運用整理
  • Backup & Recovery (W. Curtis Preston) / 適用: バックアップ戦略 / 目的: 復旧可能性の担保
  • Site Reliability Engineering / 適用: RTO/RPO設計 / 目的: 目標と検証の整合

  Trigger:
  Use when designing backup strategies, defining RPO/RTO, drafting recovery runbooks, planning DR drills, or verifying backup readiness.
  backup strategy, rpo rto, recovery runbook, disaster recovery, backup validation
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# backup-recovery

## 概要

バックアップ戦略、復旧目標、復旧手順、検証サイクルを一貫して整理し、復旧準備の抜け漏れを防ぐ。

## ワークフロー

### Phase 1: 要件整理

**目的**: スコープと依存関係を整理し、復旧要件を明確化する。

**アクション**:

1. 対象システムと依存関係を整理する。
2. `references/Level1_basics.md` で基礎概念を確認する。
3. `references/requirements-index.md` で要件と整合を確認する。

**Task**: `agents/analyze-recovery-requirements.md` を参照

### Phase 2: 目標と戦略設計

**目的**: RPO/RTOとバックアップ戦略を設計する。

**アクション**:

1. `references/rpo-rto-design.md` で目標を定義する。
2. `references/backup-strategy-layers.md` で多層戦略を整理する。
3. `assets/backup-policy-template.md` にポリシーを記載する。

**Task**: `agents/define-rpo-rto.md` を参照

### Phase 3: ランブック作成

**目的**: 復旧手順を整理し、運用ドキュメントを作成する。

**アクション**:

1. `references/disaster-recovery-planning.md` でDR方針を確認する。
2. `assets/recovery-runbook-template.md` で復旧手順を整理する。
3. `references/recovery-procedures.md` でシナリオ別手順を確認する。

**Task**: `agents/create-recovery-runbook.md` を参照

### Phase 4: 検証と運用

**目的**: 復旧準備を検証し、改善記録を残す。

**アクション**:

1. `scripts/verify-backup.mjs` でバックアップ検証を行う。
2. `assets/recovery-validation-checklist.md` で検証観点を確認する。
3. `scripts/log_usage.mjs` で記録を更新する。

**Task**: `agents/validate-recovery-readiness.md` を参照

## Task仕様ナビ

| Task                          | 起動タイミング | 入力         | 出力                 |
| ----------------------------- | -------------- | ------------ | -------------------- |
| analyze-recovery-requirements | Phase 1開始時  | システム概要 | 要件サマリ、依存一覧 |
| define-rpo-rto                | Phase 2開始時  | 要件サマリ   | RPO/RTO表            |
| design-backup-strategy        | Phase 2開始時  | RPO/RTO表    | バックアップ戦略     |
| create-recovery-runbook       | Phase 3開始時  | 戦略メモ     | 復旧ランブック       |
| validate-recovery-readiness   | Phase 4開始時  | ランブック   | 検証レポート         |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                     | 理由                     |
| ---------------------------- | ------------------------ |
| RPO/RTOを数値で明示する      | 目標が曖昧になるのを防ぐ |
| 多層バックアップを前提にする | 復旧手段が増える         |
| ランブックを更新し続ける     | 復旧手順の劣化を防ぐ     |
| 定期検証を実施する           | 復旧可能性を維持できる   |

### 避けるべきこと

| 禁止事項                 | 問題点                 |
| ------------------------ | ---------------------- |
| 検証を省略する           | 復旧失敗のリスクが高い |
| RPO/RTOを口頭で共有する  | 誤解が起きる           |
| ランブックを放置する     | 手順が陳腐化する       |
| DR計画を未承認のまま運用 | 責任が不明確になる     |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                   | 機能                         |
| ---------------------------- | ---------------------------- |
| `scripts/verify-backup.mjs`  | バックアップ検証             |
| `scripts/validate-skill.mjs` | スキル構造検証               |
| `scripts/log_usage.mjs`      | 使用記録と評価メトリクス更新 |

### references/（詳細知識）

| リソース         | パス                                                                                 | 読込条件         |
| ---------------- | ------------------------------------------------------------------------------------ | ---------------- |
| レベル1 基礎     | [references/Level1_basics.md](references/Level1_basics.md)                           | 要件整理時       |
| レベル2 実務     | [references/Level2_intermediate.md](references/Level2_intermediate.md)               | 目標設計時       |
| レベル3 応用     | [references/Level3_advanced.md](references/Level3_advanced.md)                       | ランブック作成時 |
| レベル4 専門     | [references/Level4_expert.md](references/Level4_expert.md)                           | 検証時           |
| バックアップ戦略 | [references/backup-strategy-layers.md](references/backup-strategy-layers.md)         | 戦略設計時       |
| DR計画           | [references/disaster-recovery-planning.md](references/disaster-recovery-planning.md) | 設計時           |
| 復旧手順         | [references/recovery-procedures.md](references/recovery-procedures.md)               | 検証時           |
| RPO/RTO設計      | [references/rpo-rto-design.md](references/rpo-rto-design.md)                         | 目標設計時       |
| Turso運用        | [references/turso-backup-guide.md](references/turso-backup-guide.md)                 | Turso利用時      |
| 要求仕様索引     | [references/requirements-index.md](references/requirements-index.md)                 | 仕様確認時       |
| 旧スキル         | [references/legacy-skill.md](references/legacy-skill.md)                             | 互換確認時       |

### assets/（テンプレート・素材）

| アセット                                  | 用途                 |
| ----------------------------------------- | -------------------- |
| `assets/backup-policy-template.md`        | バックアップポリシー |
| `assets/recovery-runbook-template.md`     | 復旧ランブック       |
| `assets/recovery-validation-checklist.md` | 検証チェックリスト   |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
