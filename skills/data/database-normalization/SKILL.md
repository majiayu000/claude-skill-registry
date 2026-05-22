---
name: database-normalization
description: |
  正規化設計の要件整理、正規形判定、非正規化判断を体系化するスキル。
  1NF〜5NFの適用とパフォーマンス要件のトレードオフを整理する。

  Anchors:
  • データベース実践講義 / 適用: 正規化理論 / 目的: 正規形の判断基準を明確化
  • Designing Data-Intensive Applications / 適用: データモデリング / 目的: 性能と一貫性の整理
  • Database Reliability Engineering / 適用: 運用設計 / 目的: 変更の安全性担保

  Trigger:
  Use when evaluating normalization levels, designing relational schemas, documenting denormalization decisions, or reviewing schema trade-offs.
  database normalization, 1nf 2nf 3nf, schema review, denormalization decision
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# database-normalization

## 概要

正規化の要件整理から設計・実装・検証までを一貫して支援し、整合性と性能のバランスを保つ。

## ワークフロー

### Phase 1: 要件整理

**目的**: スキーマの目的と制約を整理し、対象範囲を確定する。

**アクション**:

1. `references/Level1_basics.md` で基本概念を確認する。
2. `assets/normalization-assessment-template.md` で要件を記録する。
3. `references/requirements-index.md` で全体要件との整合を確認する。

**Task**: `agents/analyze-normalization-requirements.md` を参照

### Phase 2: 設計

**目的**: 正規形の適用レベルと非正規化判断を設計する。

**アクション**:

1. `references/normalization-levels-detail.md` で正規形を評価する。
2. `assets/denormalization-decision-template.md` で非正規化判断を記録する。
3. `scripts/analyze-normalization.mjs` で現状の構造を確認する。

**Task**: `agents/design-normalization-plan.md` を参照

### Phase 3: 実装

**目的**: 正規化の変更を反映し、実装差分を整理する。

**アクション**:

1. 正規化変更を反映し、影響範囲を記録する。
2. `scripts/analyze-normalization.mjs` で再評価する。
3. 変更点をメモに残す。

**Task**: `agents/implement-normalization-changes.md` を参照

### Phase 4: 検証と運用

**目的**: 正規化/非正規化判断の妥当性を検証し、記録を残す。

**アクション**:

1. `assets/normalization-review-checklist.md` で検証する。
2. `agents/validate-normalization-quality.md` の観点で評価する。
3. `scripts/log_usage.mjs` で記録を更新する。

**Task**: `agents/validate-normalization-quality.md` を参照

## Task仕様ナビ

| Task                               | 起動タイミング | 入力         | 出力                     |
| ---------------------------------- | -------------- | ------------ | ------------------------ |
| analyze-normalization-requirements | Phase 1開始時  | スキーマ情報 | 要件メモ、対象範囲       |
| design-normalization-plan          | Phase 2開始時  | 要件メモ     | 正規化設計、非正規化判断 |
| implement-normalization-changes    | Phase 3開始時  | 設計メモ     | 実装差分、影響一覧       |
| validate-normalization-quality     | Phase 4開始時  | 実装差分     | 検証レポート、改善提案   |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                   | 理由                   |
| -------------------------- | ---------------------- |
| 正規形を段階的に評価する   | 影響範囲を最小化できる |
| 非正規化判断を文書化する   | 保守と監査が容易になる |
| 変更の影響を明示する       | レビューがしやすい     |
| 検証チェックを必ず実施する | 不整合を防止できる     |

### 避けるべきこと

| 禁止事項                 | 問題点               |
| ------------------------ | -------------------- |
| 正規形を飛ばして設計する | 不整合が発生しやすい |
| 非正規化の根拠を残さない | 追跡不能になる       |
| 影響範囲を確認しない     | 破壊的変更のリスク   |
| 検証を省略する           | 品質低下につながる   |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                          | 機能                         |
| ----------------------------------- | ---------------------------- |
| `scripts/analyze-normalization.mjs` | 正規化分析                   |
| `scripts/validate-skill.mjs`        | スキル構造検証               |
| `scripts/log_usage.mjs`             | 使用記録と評価メトリクス更新 |

### references/（詳細知識）

| リソース     | パス                                                                                   | 読込条件   |
| ------------ | -------------------------------------------------------------------------------------- | ---------- |
| レベル1 基礎 | [references/Level1_basics.md](references/Level1_basics.md)                             | 要件整理時 |
| レベル2 実務 | [references/Level2_intermediate.md](references/Level2_intermediate.md)                 | 設計時     |
| レベル3 応用 | [references/Level3_advanced.md](references/Level3_advanced.md)                         | 実装時     |
| レベル4 専門 | [references/Level4_expert.md](references/Level4_expert.md)                             | 検証時     |
| 正規形詳細   | [references/normalization-levels-detail.md](references/normalization-levels-detail.md) | 設計時     |
| 要求仕様索引 | [references/requirements-index.md](references/requirements-index.md)                   | 仕様確認時 |
| 旧スキル     | [references/legacy-skill.md](references/legacy-skill.md)                               | 互換確認時 |

### assets/（テンプレート・素材）

| アセット                                      | 用途                 |
| --------------------------------------------- | -------------------- |
| `assets/normalization-assessment-template.md` | 要件整理テンプレート |
| `assets/denormalization-decision-template.md` | 非正規化判断記録     |
| `assets/normalization-review-checklist.md`    | 検証チェックリスト   |

## 変更履歴

| Version | Date       | Changes                                                    |
| ------- | ---------- | ---------------------------------------------------------- |
| 2.0.0   | 2026-01-04 | 18-skills.md仕様完全準拠版に再構築、運用ファイル形式を統一 |
| 1.0.0   | 2025-12-24 | 初版作成                                                   |
