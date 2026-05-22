---
name: design-patterns-behavioral
description: |
  GoFの行動パターンを用いて、オブジェクト間の責務分散と通信設計を支援するスキル。
  パターン選定、実装方針、検証手順を体系化する。

  Anchors:
  • Design Patterns / 適用: 行動パターンの設計理論 / 目的: 相互作用の整理
  • Command Pattern / 適用: 操作の実行・取り消し / 目的: 実行制御の柔軟化
  • Strategy Pattern / 適用: アルゴリズム切替 / 目的: 変更容易性の確保

  Trigger:
  Use when designing flexible object collaboration, selecting behavioral patterns, or validating pattern usage in implementations.
  behavioral design patterns, strategy, command, observer, state, template method
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# design-patterns-behavioral

## 概要

GoFの行動パターンを用いて、責務分散・通信設計・検証を支援する。

## ワークフロー

### Phase 1: 要件整理

**目的**: 課題と制約を整理し、対象パターンの候補を明確化する。

**アクション**:

1. `references/Level1_basics.md` で基本概念を確認する。
2. `assets/pattern-requirements-template.md` で要件を整理する。
3. `references/requirements-index.md` で要件整合を確認する。

**Task**: `agents/analyze-pattern-requirements.md` を参照

### Phase 2: パターン設計

**目的**: 行動パターンの選定と設計方針を決定する。

**アクション**:

1. `references/pattern-selection-guide.md` で選定基準を確認する。
2. `assets/pattern-selection-checklist.md` で判断観点を揃える。
3. 個別パターンのガイドを参照する。

**Task**: `agents/design-pattern-application.md` を参照

### Phase 3: 実装と構成

**目的**: パターンの実装方針を整理し、テンプレートに反映する。

**アクション**:

1. `assets/strategy-implementation.md` を参照して構成を整理する。
2. `assets/template-method-implementation.md` を参照して設計を整理する。
3. 必要なパターンの実装メモを作成する。

**Task**: `agents/implement-pattern-solution.md` を参照

### Phase 4: 検証と記録

**目的**: 適用結果を検証し、改善サイクルを回す。

**アクション**:

1. `scripts/validate-pattern-usage.mjs` で適用を検証する。
2. `assets/pattern-evaluation-template.md` で評価を整理する。
3. `scripts/log_usage.mjs` で記録を更新する。

**Task**: `agents/validate-pattern-usage.md` を参照

## Task仕様ナビ

| Task                         | 起動タイミング | 入力         | 出力                   |
| ---------------------------- | -------------- | ------------ | ---------------------- |
| analyze-pattern-requirements | Phase 1開始時  | 課題/制約    | パターン候補、要件メモ |
| design-pattern-application   | Phase 2開始時  | 要件メモ     | 選定結果、設計方針     |
| implement-pattern-solution   | Phase 3開始時  | 設計方針     | 実装方針メモ、構成案   |
| validate-pattern-usage       | Phase 4開始時  | 実装方針メモ | 検証レポート、改善提案 |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                   | 理由                     |
| -------------------------- | ------------------------ |
| パターン選定理由を明記する | 変更時の判断が明確になる |
| 責務境界を明文化する       | 依存が過剰になるのを防ぐ |
| 検証結果を記録する         | 改善が継続する           |
| 既存設計との整合を確認する | 不整合による複雑化を防ぐ |

### 避けるべきこと

| 禁止事項             | 問題点             |
| -------------------- | ------------------ |
| 目的が曖昧なまま適用 | 過剰設計になる     |
| 似た責務の重複       | 読みにくくなる     |
| 検証を省略する       | 目的未達のまま残る |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                           | 機能                         |
| ------------------------------------ | ---------------------------- |
| `scripts/validate-pattern-usage.mjs` | パターン適用の検証           |
| `scripts/log_usage.mjs`              | 使用記録と評価メトリクス更新 |
| `scripts/validate-skill.mjs`         | スキル構造の検証             |

### references/（詳細知識）

| リソース                | パス                                                                                           | 読込条件   |
| ----------------------- | ---------------------------------------------------------------------------------------------- | ---------- |
| レベル1 基礎            | [references/Level1_basics.md](references/Level1_basics.md)                                     | 要件整理時 |
| レベル2 実務            | [references/Level2_intermediate.md](references/Level2_intermediate.md)                         | 設計時     |
| レベル3 応用            | [references/Level3_advanced.md](references/Level3_advanced.md)                                 | 実装時     |
| レベル4 専門            | [references/Level4_expert.md](references/Level4_expert.md)                                     | 改善時     |
| パターン選定            | [references/pattern-selection-guide.md](references/pattern-selection-guide.md)                 | 選定時     |
| Chain of Responsibility | [references/chain-of-responsibility-pattern.md](references/chain-of-responsibility-pattern.md) | 適用時     |
| Command                 | [references/command-pattern.md](references/command-pattern.md)                                 | 適用時     |
| Observer                | [references/observer-pattern.md](references/observer-pattern.md)                               | 適用時     |
| State                   | [references/state-pattern.md](references/state-pattern.md)                                     | 適用時     |
| Strategy                | [references/strategy-pattern.md](references/strategy-pattern.md)                               | 適用時     |
| Template Method         | [references/template-method-pattern.md](references/template-method-pattern.md)                 | 適用時     |
| 要求仕様索引            | [references/requirements-index.md](references/requirements-index.md)                           | 仕様確認時 |
| 旧スキル                | [references/legacy-skill.md](references/legacy-skill.md)                                       | 互換確認時 |

### assets/（テンプレート・素材）

| アセット                                   | 用途                            |
| ------------------------------------------ | ------------------------------- |
| `assets/pattern-requirements-template.md`  | 要件整理テンプレート            |
| `assets/pattern-selection-checklist.md`    | 選定チェックリスト              |
| `assets/pattern-evaluation-template.md`    | 検証テンプレート                |
| `assets/strategy-implementation.md`        | Strategy実装テンプレート        |
| `assets/template-method-implementation.md` | Template Method実装テンプレート |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
