---
name: approval-gates
description: |
  承認ゲートの設計・評価・運用を体系化し、変更管理とリリース判断を安全に進めるスキル。
  リスク評価に基づくゲート条件、手動承認と自動検証の分離、監査可能な記録設計を支援します。

  Anchors:
  • The Pragmatic Programmer / 適用: 品質ゲートの段階化 / 目的: 変更の安全性を段階的に高める
  • リスク評価フレームワーク / 適用: 影響度と発生確率の分類 / 目的: ゲート条件の科学的根拠を整える
  • ITIL Change Enablement / 適用: 変更承認フロー / 目的: 監査可能な意思決定を実現する

  Trigger:
  Use when designing approval gates, change control checkpoints, release readiness criteria, or governance workflows that require risk-based approvals and audit trails.
allowed-tools:
  - bash
  - node
---

# Approval Gates

## 概要

承認ゲート（approval gates）は、変更・リリース・運用判断が事前定義の条件を満たしていることを確認するチェックポイントです。
本スキルは、リスク評価からゲート仕様策定、実装・検証までを一貫して設計するための手順と参照資料を提供します。

- ゲート仕様のたたき台は `assets/approval-gate-spec-template.md` を使用
- 詳細知識は `references/` に外部化（必要時のみ読む）

## ワークフロー

### Phase 1: リスク整理と対象タスク理解

**目的**: 変更対象の影響度と優先度を明確化し、ゲート必要度を判定する

**アクション**:

1. `references/Level1_basics.md` で基本概念と分類軸を確認
2. `references/requirements-index.md` で適用対象のルール・基準を整理
3. 変更内容、影響範囲、失敗時の影響を整理し、リスク階層を決定

**Task**: `agents/risk-assessment.md` を参照

### Phase 2: ゲート設計と自動化判断

**目的**: リスク評価に基づき、ゲート構成と判定条件を設計する

**アクション**:

1. `references/Level2_intermediate.md` で設計パターンを選定
2. `assets/approval-gate-spec-template.md` でゲート仕様を起案
3. `references/Level3_advanced.md` で自動化候補と判定ロジックを整理

**Task**:

- `agents/gate-design.md`
- `agents/automation-check.md`

### Phase 3: 検証と運用設計

**目的**: ゲート仕様の妥当性を確認し、運用・監査に耐える形へ整える

**アクション**:

1. `scripts/validate-skill.mjs --spec <gate-spec>` で仕様テンプレの必須項目を検証
2. `references/Level4_expert.md` で例外運用・監査要件を確認
3. `scripts/log_usage.mjs` で改善フィードバックを記録

**Task**: `agents/implementation-review.md` を参照

## Task仕様ナビ

| Task         | 役割                         | 入力                     | 出力                     | 参照先                                  | 実行タイミング |
| ------------ | ---------------------------- | ------------------------ | ------------------------ | --------------------------------------- | -------------- |
| リスク評価   | 影響度・発生確率の評価       | 変更内容、影響範囲       | リスク分類表、ゲート推奨 | `references/Level1_basics.md`           | Phase 1        |
| ゲート設計   | ゲート条件と承認ルールの設計 | リスク分類表、組織ルール | ゲート仕様書             | `assets/approval-gate-spec-template.md` | Phase 2 前半   |
| 自動化判定   | 自動検査と手動承認の切り分け | ゲート仕様書             | 自動化可能項目一覧       | `references/Level3_advanced.md`         | Phase 2 後半   |
| 実装レビュー | 実装・運用の最終確認         | ゲート仕様書、運用制約   | 検証チェックリスト       | `references/Level4_expert.md`           | Phase 3        |

## ベストプラクティス

### すべきこと

- 影響度と頻度の2軸でリスク階層を整理する
- ゲート条件は「自動化可能」か「人間判断」かを明示する
- 失敗時の復旧策（ロールバック/停止条件）をゲート仕様に含める
- ゲートの目的（品質、セキュリティ、法令）を明文化する
- ゲート実行ログを残し、改善の根拠にする

### 避けるべきこと

- リスク評価なしでゲートを過剰に増やす
- 承認権限や責任範囲を曖昧にする
- 自動検証の失敗時に代替手段を用意しない
- ゲート条件を頻繁に変更して運用の信頼性を下げる
- 例外扱いを恒常化する

## リソース参照

### 参照資料

- `references/Level1_basics.md`: 承認ゲートの基礎とリスク分類
- `references/Level2_intermediate.md`: ゲート設計パターンと条件定義
- `references/Level3_advanced.md`: 自動化・評価メトリクス・段階適用
- `references/Level4_expert.md`: 監査・例外運用・継続改善
- `references/requirements-index.md`: 本リポジトリの適用基準の索引

### スクリプト

- `scripts/validate-skill.mjs`: ゲート仕様テンプレの必須項目チェック
- `scripts/log_usage.mjs`: 実行ログ記録（LOGS.md / EVALS.json を自動生成）

### テンプレート

- `assets/approval-gate-spec-template.md`: ゲート仕様書テンプレ

## 変更履歴

| Version | Date       | Changes                                                 |
| ------- | ---------- | ------------------------------------------------------- |
| 2.1.0   | 2025-12-31 | ワークフロー再設計、agents/assets/scripts整備、参照整理 |
| 2.0.0   | 2025-12-31 | 18-skills.md仕様へのアップグレード、Task仕様ナビ追加    |
| 1.0.0   | 2025-12-24 | 初版作成、基本ワークフローとベストプラクティス定義      |
