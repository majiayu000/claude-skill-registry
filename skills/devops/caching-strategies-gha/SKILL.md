---
name: caching-strategies-gha
description: |
  GitHub Actions のキャッシュ戦略を設計し、キー設計、パス選定、ヒット率改善、10GB制限管理を行うスキル。
  actions/cache の最適化、依存キャッシュの分割、Dockerレイヤー連携などを体系化する。

  Anchors:
  • The Pragmatic Programmer / 適用: 実践的改善 / 目的: 反復的な最適化
  • Continuous Delivery / 適用: パイプライン最適化 / 目的: 実行時間の短縮
  • Site Reliability Engineering / 適用: キャパシティ管理 / 目的: キャッシュ制限の管理

  Trigger:
  Use when optimizing GitHub Actions cache performance, designing cache keys/paths, reducing CI build time, or managing cache size limits.
allowed-tools:
  - bash
  - node
---

# GitHub Actions Caching Strategies

## 概要

GitHub Actions のキャッシュ戦略を設計し、ヒット率とサイズを最適化する。
詳細は `references/` に外部化し、必要時に参照する。

- キャッシュ例: `assets/cache-examples.yaml`

## ワークフロー

### Phase 1: キャッシュ対象の整理

**目的**: キャッシュ対象と制約を整理する

**アクション**:

1. `references/Level1_basics.md` で基本概念を確認
2. `references/cache-action.md` で actions/cache を確認
3. キャッシュ対象/頻度/制限を整理

**Task**: `agents/analyze-cache-requirements.md`

### Phase 2: キー設計

**目的**: キーとパスを設計する

**アクション**:

1. `references/cache-patterns.md` を参照
2. キーに含める入力を整理
3. restore-keys の戦略を決定

**Task**: `agents/design-cache-keys.md`

### Phase 3: 最適化と分割

**目的**: ヒット率とサイズを最適化する

**アクション**:

1. `references/cache-optimization.md` を参照
2. `scripts/estimate-cache-size.mjs` でサイズを見積もる
3. 分割/除外/レイヤー化方針を決定

**Task**: `agents/optimize-cache-strategy.md`

### Phase 4: 検証と記録

**目的**: 効果を検証し記録する

**アクション**:

1. `references/Level4_expert.md` で監査観点を確認
2. ヒット率/速度改善を確認
3. `scripts/validate-skill.mjs` で構造検証
4. `scripts/log_usage.mjs` で記録

**Task**: `agents/validate-cache-impact.md`

## Task仕様ナビ

| Task     | 役割               | 入力         | 出力         | 参照先                             | 実行タイミング |
| -------- | ------------------ | ------------ | ------------ | ---------------------------------- | -------------- |
| 対象整理 | キャッシュ対象整理 | ワークフロー | 対象メモ     | `references/cache-action.md`       | Phase 1        |
| キー設計 | キー/パス設計      | 対象メモ     | キー設計メモ | `references/cache-patterns.md`     | Phase 2        |
| 最適化   | 分割/除外方針      | キー設計メモ | 最適化メモ   | `references/cache-optimization.md` | Phase 3        |
| 検証     | 効果確認           | 最適化メモ   | 検証メモ     | `references/Level4_expert.md`      | Phase 4        |

## ベストプラクティス

### すべきこと

- キーの粒度を明確にする
- restore-keys を設定する
- 10GB制限を意識する
- 大きなキャッシュは分割する

### 避けるべきこと

- 変更頻度の高い入力をキーに含めすぎる
- ヒット率を測定しない
- キャッシュ肥大を放置する

## リソース参照

### 参照資料

- `references/Level1_basics.md`: 基礎概念
- `references/Level2_intermediate.md`: 設計ガイド
- `references/Level3_advanced.md`: 最適化
- `references/Level4_expert.md`: 監査/計測
- `references/cache-action.md`: actions/cache 仕様
- `references/cache-patterns.md`: 言語別パターン
- `references/cache-optimization.md`: 最適化戦略
- `references/legacy-skill.md`: 旧版要約（移行時のみ）

### スクリプト

- `scripts/estimate-cache-size.mjs`: サイズ見積り
- `scripts/validate-skill.mjs`: スキル構造検証
- `scripts/log_usage.mjs`: 実行ログ記録

### テンプレート

- `assets/cache-examples.yaml`: キャッシュ設定例

## 変更履歴

| Version | Date       | Changes                                  |
| ------- | ---------- | ---------------------------------------- |
| 2.1.0   | 2025-12-31 | 18-skills準拠、Task仕様追加、scripts整備 |
| 2.0.0   | 2025-12-31 | 18-skills.md仕様に完全準拠               |
| 1.0.0   | 2025-12-24 | 初版作成                                 |
