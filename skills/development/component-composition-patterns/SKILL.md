---
name: component-composition-patterns
description: |
  コンポーネント合成パターンを用いた再利用可能なUI構造設計を支援するスキル。
  Compound Components、Polymorphic Components、Slot Pattern の選定と設計手順を整理する。

  Anchors:
  • Don't Make Me Think / 適用: UI設計・ユーザビリティ / 目的: 再利用性と保守性向上
  • Atomic Design / 適用: コンポーネント階層設計 / 目的: 構造の一貫性確保
  • React Patterns / 適用: 合成設計 / 目的: APIの一貫性

  Trigger:
  Use when designing component composition patterns, selecting compound/polymorphic/slot patterns, or validating reusable UI structures.
  component composition patterns, compound components, polymorphic components, slot pattern, reusable UI
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# component-composition-patterns

## 概要

コンポーネント合成パターンと再利用可能なUI構造設計を支援する。Compound Components、Polymorphic Components、Slot Pattern の選定と設計手順を整理する。

## ワークフロー

### Phase 1: 要件整理

**目的**: 目的・制約・期待APIを明確化する。

**アクション**:

1. `references/Level1_basics.md` で基本概念を確認する。
2. `assets/composition-requirements-template.md` で要件を整理する。
3. `references/requirements-index.md` で要件整合を確認する。

**Task**: `agents/analyze-composition-requirements.md` を参照

### Phase 2: 合成設計

**目的**: 合成パターンとAPI設計を確定する。

**アクション**:

1. `references/compound-components-guide.md` でCompound設計を確認する。
2. `references/polymorphic-components.md` で型設計を確認する。
3. `references/slot-pattern-guide.md` でSlot設計を確認する。
4. `assets/composition-review-checklist.md` で設計観点を揃える。

**Task**: `agents/design-composition-patterns.md` を参照

### Phase 3: 実装とプロトタイプ

**目的**: 合成パターンの実装方針を形にする。

**アクション**:

1. `assets/compound-component-template.tsx` でCompound構成を作成する。
2. `assets/polymorphic-component-template.tsx` で型とPropsを整備する。
3. `assets/slot-component-template.tsx` でSlot構成を整備する。

**Task**: `agents/implement-composition-patterns.md` を参照

### Phase 4: 検証と記録

**目的**: 合成パターンの適合性を検証し記録する。

**アクション**:

1. `scripts/analyze-composition.mjs` で構造を分析する。
2. `scripts/validate-skill.mjs` でスキル構造を検証する。
3. `scripts/log_usage.mjs` で記録を更新する。

**Task**: `agents/validate-composition-patterns.md` を参照

## Task仕様ナビ

| Task                             | 起動タイミング | 入力               | 出力                           |
| -------------------------------- | -------------- | ------------------ | ------------------------------ |
| analyze-composition-requirements | Phase 1開始時  | 要件/制約          | 合成要件整理メモ、パターン候補 |
| design-composition-patterns      | Phase 2開始時  | 合成要件整理メモ   | 合成パターン設計書、API設計    |
| implement-composition-patterns   | Phase 3開始時  | 合成パターン設計書 | 実装方針メモ、試作構成         |
| validate-composition-patterns    | Phase 4開始時  | 実装方針メモ       | 検証レポート、ログ更新内容     |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                    | 理由                         |
| --------------------------- | ---------------------------- |
| 目的と制約を先に整理する    | 過度な抽象化を防ぐため       |
| パターン選定を明文化する    | 意図と再利用範囲を揃えるため |
| APIと型設計を早期に確定する | 破綻を防ぐため               |
| テンプレートで構成を揃える  | 実装の一貫性を保つため       |

### 避けるべきこと

| 禁止事項                   | 問題点               |
| -------------------------- | -------------------- |
| 目的に合わないパターン採用 | 保守性が低下する     |
| Props設計の後回し          | 実装の破綻につながる |
| 合成の責務混在             | 再利用性が低下する   |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                        | 機能                         |
| --------------------------------- | ---------------------------- |
| `scripts/analyze-composition.mjs` | 合成パターン分析             |
| `scripts/log_usage.mjs`           | 使用記録と評価メトリクス更新 |
| `scripts/validate-skill.mjs`      | スキル構造の検証             |

### references/（詳細知識）

| リソース           | パス                                                                               | 読込条件          |
| ------------------ | ---------------------------------------------------------------------------------- | ----------------- |
| レベル1 基礎       | [references/Level1_basics.md](references/Level1_basics.md)                         | 初回整理時        |
| レベル2 実務       | [references/Level2_intermediate.md](references/Level2_intermediate.md)             | 設計時            |
| レベル3 応用       | [references/Level3_advanced.md](references/Level3_advanced.md)                     | 実装時            |
| レベル4 専門       | [references/Level4_expert.md](references/Level4_expert.md)                         | 改善時            |
| Compound ガイド    | [references/compound-components-guide.md](references/compound-components-guide.md) | Compound設計時    |
| Polymorphic ガイド | [references/polymorphic-components.md](references/polymorphic-components.md)       | Polymorphic設計時 |
| Slot ガイド        | [references/slot-pattern-guide.md](references/slot-pattern-guide.md)               | Slot設計時        |
| 要求仕様索引       | [references/requirements-index.md](references/requirements-index.md)               | 仕様確認時        |
| 旧スキル           | [references/legacy-skill.md](references/legacy-skill.md)                           | 互換確認時        |

### assets/（テンプレート・素材）

| アセット                                      | 用途                               |
| --------------------------------------------- | ---------------------------------- |
| `assets/composition-requirements-template.md` | 要件整理テンプレート               |
| `assets/composition-review-checklist.md`      | 設計チェックリスト                 |
| `assets/compound-component-template.tsx`      | Compound Component テンプレート    |
| `assets/polymorphic-component-template.tsx`   | Polymorphic Component テンプレート |
| `assets/slot-component-template.tsx`          | Slot Component テンプレート        |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
