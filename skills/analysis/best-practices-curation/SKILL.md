---
name: best-practices-curation
description: |
  ベストプラクティスの収集・評価・統合・更新を体系化するスキル。
  情報源の信頼性評価、品質スコアリング、統合パターンを用いて知識ベースを改善する。

  Anchors:
  • The Pragmatic Programmer / 適用: 実践的改善 / 目的: 継続的な品質向上
  • Evidence-Based Management / 適用: 評価基準 / 目的: 判断の一貫性を担保
  • Knowledge Management (Nonaka) / 適用: 知識統合 / 目的: 暗黙知の体系化

  Trigger:
  Use when collecting best practices, assessing source credibility, scoring quality, integrating guidance, or updating knowledge bases.
allowed-tools:
  - bash
  - node
---

# Best Practices Curation

## 概要

ベストプラクティスの収集から統合・更新までを一貫して整理する。
詳細は `references/` に外部化し、必要時に参照する。

- 評価チェックリスト: `assets/evaluation-checklist.md`

## ワークフロー

### Phase 1: スコープと情報源整理

**目的**: 収集対象と情報源の優先度を決める

**アクション**:

1. `references/Level1_basics.md` で基礎方針を確認
2. `references/information-source-evaluation.md` で情報源を分類
3. 対象テーマと採用基準を整理

**Task**: `agents/analyze-curation-scope.md`

### Phase 2: 評価とスコアリング

**目的**: 信頼性と品質を評価する

**アクション**:

1. `references/quality-scoring.md` を参照
2. `assets/evaluation-checklist.md` で採点
3. 補完が必要な情報を整理

**Task**: `agents/evaluate-source-quality.md`

### Phase 3: 統合と更新

**目的**: ベストプラクティスを統合し更新する

**アクション**:

1. `references/integration-strategies.md` で統合パターンを選択
2. 重複排除と一貫性チェックを実施
3. 更新内容を整理

**Task**: `agents/integrate-best-practice.md`

### Phase 4: 検証と記録

**目的**: 更新内容の妥当性を検証し記録する

**アクション**:

1. `references/Level4_expert.md` の監査観点を確認
2. `scripts/validate-skill.mjs` で構造検証
3. `scripts/log_usage.mjs` で記録

**Task**: `agents/validate-curation-update.md`

## Task仕様ナビ

| Task         | 役割             | 入力         | 出力         | 参照先                                 | 実行タイミング |
| ------------ | ---------------- | ------------ | ------------ | -------------------------------------- | -------------- |
| スコープ整理 | 収集対象の定義   | テーマ/目的  | スコープメモ | `references/Level1_basics.md`          | Phase 1        |
| 品質評価     | 情報源評価       | 情報源リスト | 評価スコア   | `references/quality-scoring.md`        | Phase 2        |
| 統合         | 重複排除と統合   | 評価スコア   | 統合メモ     | `references/integration-strategies.md` | Phase 3        |
| 検証         | 更新の妥当性確認 | 統合メモ     | 検証メモ     | `references/Level4_expert.md`          | Phase 4        |

## ベストプラクティス

### すべきこと

- 情報源を一次/二次/三次で分類する
- 評価基準を定義してスコア化する
- 統合パターンを明示する
- 更新履歴を必ず残す

### 避けるべきこと

- 評価基準を持たずに採用する
- 重複や矛盾を放置する
- 更新履歴を省略する

## リソース参照

### 参照資料

- `references/Level1_basics.md`: 基礎概念
- `references/Level2_intermediate.md`: 評価と整合の運用
- `references/Level3_advanced.md`: 統合と改善の高度化
- `references/Level4_expert.md`: 監査と継続改善
- `references/information-source-evaluation.md`: 情報源評価
- `references/quality-scoring.md`: 品質スコアリング
- `references/integration-strategies.md`: 統合戦略
- `references/legacy-skill.md`: 旧版要約（移行時のみ）

### スクリプト

- `scripts/validate-skill.mjs`: スキル構造検証
- `scripts/log_usage.mjs`: 実行ログ記録

### テンプレート

- `assets/evaluation-checklist.md`: 評価チェックリスト

## 変更履歴

| Version | Date       | Changes                                  |
| ------- | ---------- | ---------------------------------------- |
| 2.1.0   | 2025-12-31 | 18-skills準拠、Task仕様追加、scripts整備 |
| 2.0.0   | 2025-12-31 | 18-skills.md仕様に完全準拠               |
| 1.0.0   | 2025-12-24 | 初版作成                                 |
