---
name: bounded-context
description: |
  ドメイン駆動設計における境界付けられたコンテキストの特定、境界定義、コンテキストマップ作成、統合戦略設計を支援するスキル。
  チーム責務の整理、モデルの分離、連携方式の選定を体系化する。

  Anchors:
  • Domain-Driven Design / 適用: 境界設計 / 目的: ドメイン境界の明確化
  • Implementing Domain-Driven Design / 適用: コンテキストマップ / 目的: 統合パターンの適用
  • Context Mapping (Brandolini) / 適用: 境界調整 / 目的: チーム間協調の整理

  Trigger:
  Use when defining domain boundaries, creating context maps, choosing integration strategies, or clarifying team ownership for services/modules.
allowed-tools:
  - bash
  - node
---

# Bounded Context

## 概要

境界付けられたコンテキストを定義し、コンテキストマップと統合戦略を整理する。
詳細は `references/` に外部化し、必要時に参照する。

- コンテキストマップテンプレ: `assets/context-map-template.md`

## ワークフロー

### Phase 1: コンテキスト特定

**目的**: ドメイン境界の候補を整理する

**アクション**:

1. `references/Level1_basics.md` で基礎概念を確認
2. `references/context-identification.md` で特定手法を確認
3. ドメインの用語境界と責務を整理

**Task**: `agents/analyze-domain-contexts.md`

### Phase 2: コンテキストマッピング

**目的**: コンテキスト間の関係性を可視化する

**アクション**:

1. `references/context-mapping-patterns.md` を参照
2. `assets/context-map-template.md` でコンテキストマップを作成
3. 境界衝突や共有領域を整理

**Task**: `agents/design-context-map.md`

### Phase 3: 統合戦略設計

**目的**: 境界間の連携方式を定義する

**アクション**:

1. `references/integration-strategies.md` を参照
2. 同期/非同期の統合方式を選定
3. 共有カーネルやACL方針を整理

**Task**: `agents/define-integration-contracts.md`

### Phase 4: 検証と記録

**目的**: 境界設計の妥当性を確認し記録する

**アクション**:

1. `scripts/analyze-context-boundaries.mjs` で境界候補を分析
2. `references/Level4_expert.md` を確認
3. `scripts/validate-skill.mjs` で構造検証
4. `scripts/log_usage.mjs` で記録

**Task**: `agents/validate-context-design.md`

## Task仕様ナビ

| Task | 役割 | 入力 | 出力 | 参照先 | 実行タイミング |
| --- | --- | --- | --- | --- | --- |
| コンテキスト特定 | 境界候補整理 | ドメイン情報 | 候補メモ | `references/context-identification.md` | Phase 1 |
| コンテキストマップ | 関係整理 | 候補メモ | コンテキストマップ | `assets/context-map-template.md` | Phase 2 |
| 統合設計 | 連携方式整理 | コンテキストマップ | 統合方針 | `references/integration-strategies.md` | Phase 3 |
| 検証 | 境界妥当性確認 | 統合方針 | 検証メモ | `references/Level4_expert.md` | Phase 4 |

## ベストプラクティス

### すべきこと

- 用語境界を明確にする
- コンテキスト間の依存を可視化する
- 統合方式の責任分担を定義する
- 共有領域を最小限に抑える

### 避けるべきこと

- 境界の根拠を曖昧にする
- 共有カーネルを過剰に広げる
- 統合方式を決めずに実装する

## リソース参照

### 参照資料

- `references/Level1_basics.md`: 基礎概念
- `references/Level2_intermediate.md`: 運用設計
- `references/Level3_advanced.md`: 併用戦略
- `references/Level4_expert.md`: 監査と最適化
- `references/context-identification.md`: コンテキスト特定
- `references/context-mapping-patterns.md`: コンテキストマップ
- `references/integration-strategies.md`: 統合戦略
- `references/legacy-skill.md`: 旧版要約（移行時のみ）

### スクリプト

- `scripts/analyze-context-boundaries.mjs`: 境界分析
- `scripts/validate-skill.mjs`: スキル構造検証
- `scripts/log_usage.mjs`: 実行ログ記録

### テンプレート

- `assets/context-map-template.md`: コンテキストマップ

## 変更履歴

| Version | Date       | Changes                                             |
| ------- | ---------- | --------------------------------------------------- |
| 2.1.0   | 2025-12-31 | 18-skills準拠、Task仕様追加、scripts整備            |
| 2.0.0   | 2025-12-31 | 18-skills.md仕様に完全準拠                           |
| 1.0.0   | 2025-12-24 | 初版作成                                            |
