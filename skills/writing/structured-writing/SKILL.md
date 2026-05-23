---
name: structured-writing
description: |
  構造化ライティングを実践するためのスキル。DITAやトピックベースの原則に沿って文書を分割・再利用し、手順/概念/参照の役割を明確にする。

  Anchors:
  • DITA 1.3 Specification / 適用: トピック設計 / 目的: 文書構造の標準化
  • Information Architecture for the World Wide Web / 適用: 情報設計 / 目的: 探しやすさの向上
  • Topic-Based Authoring / 適用: 再利用設計 / 目的: モジュール化と保守性の改善

  Trigger:
  Use when designing topic-based documentation, modular content, or reusable docs with clear task/concept/reference separation.
  structured writing, DITA, topic-based authoring, content reuse, documentation structure
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Structured Writing

## 概要

文書をトピック単位に分割し、再利用可能な構造で設計・検証するスキル。目的と読者に合わせて情報を整理し、保守性を高める。

詳細は `references/Level1_basics.md` から段階的に参照する。

## ワークフロー

### Phase 1: 目的と読者の整理

**目的**: 文書の目的・読者・利用シーンを明確化する。

**アクション**:

1. 利用目的（学習/運用/仕様参照）を整理する。
2. 読者の経験レベルを定義する。
3. トピック種別（Concept/Task/Reference）を決める。

### Phase 2: トピック構造設計

**目的**: 文書構造と再利用単位を設計する。

**アクション**:

1. `assets/topic-map-template.md` で全体構造を作成する。
2. トピックテンプレートを選定する。
3. 再利用・分割のルールを決める。

### Phase 3: 検証と改善

**目的**: トピック構造の整合性を検証する。

**アクション**:

1. `scripts/validate-topic-structure.mjs` で必須見出しを確認する。
2. `scripts/analyze-structure.mjs` で全体構造を分析する。
3. 指摘を反映して文書を更新する。

## Task仕様ナビ

| Phase | Task | 目的 | 入力 | 出力 |
| --- | --- | --- | --- | --- |
| 1 | 目的・読者整理 | 目的/読者/トピック種別を定義 | ユーザー要求 | 要件メモ |
| 2 | トピック設計 | トピック構造と再利用単位を設計 | 要件メモ | トピック設計書 |
| 3 | 構造検証 | トピックの整合性を検証 | 文書セット | 検証レポート |

## ベストプラクティス

### すべきこと

- トピック種別ごとに役割を明確に分離する。
- 再利用単位を先に設計してから執筆する。
- 見出し順序を統一する。
- テンプレートで品質を均一化する。

### 避けるべきこと

- 1トピックに複数の目的を詰め込まない。
- 手順と概念を混在させない。
- 再利用の前提を持たずに長文化しない。

## リソース/スクリプト参照

### references/

- `references/Level1_basics.md`: 基礎指針
- `references/Level2_intermediate.md`: 実務パターン
- `references/Level3_advanced.md`: 高度な設計指針
- `references/Level4_expert.md`: 専門領域の注意点
- `references/dita-principles.md`: DITA原則
- `references/dita-topic-model.md`: DITAトピックモデル
- `references/topic-types.md`: トピック種別ガイド
- `references/section-ordering.md`: 見出し順序
- `references/reuse-strategies.md`: 再利用戦略
- `references/content-reuse.md`: コンテンツ再利用
- `references/modular-design.md`: モジュール設計
- `references/information-architecture.md`: 情報設計

### assets/

- `assets/topic-map-template.md`: トピックマップテンプレート
- `assets/concept-topic-template.md`: Conceptテンプレート
- `assets/task-topic-template.md`: Taskテンプレート
- `assets/reference-topic-template.md`: Referenceテンプレート
- `assets/concept-topic.md`: Concept例
- `assets/task-topic.md`: Task例
- `assets/reference-topic.md`: Reference例

### scripts/

- `scripts/validate-topic-structure.mjs`: トピック構造検証
- `scripts/analyze-structure.mjs`: 文書構造分析

## 変更履歴

| Version | Date | Changes |
| --- | --- | --- |
| 2.0.0 | 2026-01-02 | 18-skills.md 仕様に準拠した構造へ更新 |
