---
name: clean-architecture-principles
description: |
  Clean Architecture の依存関係ルールとレイヤー境界設計を整理し、設計レビューと違反検出を支援するスキル。
  アーキテクチャのレイヤー構成、境界インターフェース、依存違反の是正を扱う。

  Anchors:
  • Clean Architecture (Robert C. Martin) / 適用: レイヤー設計と依存ルール / 目的: 依存違反の防止
  • Domain-Driven Design (Eric Evans) / 適用: ドメイン境界設計 / 目的: 内部モデルの保護
  • Accelerate (Forsgren/Humble/Kim) / 適用: 変更容易性と品質 / 目的: 継続的改善の指標化

  Trigger:
  Use when reviewing architecture layers, enforcing dependency rules, designing boundaries, or validating layer compliance.
  clean architecture, dependency rule, layer violation, boundary interface, architecture review
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# clean-architecture-principles

## 概要

Clean Architecture のレイヤー設計と依存関係ルールを整理し、境界の設計と違反検出を一貫して進める。

## ワークフロー

### Phase 1: 要件整理

**目的**: 対象範囲と設計目的を明確化する。

**アクション**:

1. 対象システムの目的と制約を整理する。
2. レイヤー構成と対象境界を定義する。
3. 参照すべき要件文書を特定する。

**Task**: `agents/analyze-architecture-requirements.md` を参照

### Phase 2: レイヤー設計

**目的**: 依存関係ルールと境界設計を具体化する。

**アクション**:

1. 依存関係ルールと許容例外を整理する。
2. 境界インターフェースと責務分担を設計する。
3. レビュー用チェックリストを整備する。

**Task**: `agents/design-layer-boundaries.md` を参照

### Phase 3: 検証と記録

**目的**: レイヤー違反を検出し、改善点を記録する。

**アクション**:

1. 違反検出スクリプトで現状を確認する。
2. レビュー結果と改善方針をまとめる。
3. ログと評価情報を更新する。

**Task**: `agents/validate-layer-compliance.md` を参照

## Task仕様ナビ

| Task                              | 起動タイミング | 入力               | 出力                         |
| --------------------------------- | -------------- | ------------------ | ---------------------------- |
| analyze-architecture-requirements | Phase 1開始時  | 目的/制約/対象範囲 | 要件整理メモ、参照要件一覧   |
| design-layer-boundaries           | Phase 2開始時  | 要件整理メモ       | レイヤー設計案、境界設計案   |
| validate-layer-compliance         | Phase 3開始時  | レイヤー設計案     | 検証レポート、改善アクション |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                         | 理由                         |
| -------------------------------- | ---------------------------- |
| 依存関係ルールを先に固定する     | 違反検出の基準が明確になる   |
| 境界インターフェースを明文化する | 技術詳細の漏出を防ぐ         |
| 検証結果をログに残す             | 改善サイクルを回しやすくする |

### 避けるべきこと

| 禁止事項                   | 問題点                 |
| -------------------------- | ---------------------- |
| 例外ルールを無制限に増やす | ルールが形骸化する     |
| 境界設計を省略する         | 依存違反が検出しづらい |
| レビューを省略して実装する | 手戻りが増える         |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                          | 機能                         |
| ----------------------------------- | ---------------------------- |
| `scripts/check-layer-violation.mjs` | レイヤー違反検出             |
| `scripts/log_usage.mjs`             | 使用記録と評価メトリクス更新 |
| `scripts/validate-skill.mjs`        | スキル構造の検証             |

### references/（詳細知識）

| リソース         | パス                                                                                   | 読込条件         |
| ---------------- | -------------------------------------------------------------------------------------- | ---------------- |
| Level1 基礎      | [references/Level1_basics.md](references/Level1_basics.md)                             | 初回整理時       |
| Level2 実務      | [references/Level2_intermediate.md](references/Level2_intermediate.md)                 | 設計時           |
| Level3 応用      | [references/Level3_advanced.md](references/Level3_advanced.md)                         | 情報量が多い時   |
| Level4 専門      | [references/Level4_expert.md](references/Level4_expert.md)                             | 改善ループ時     |
| 依存関係ルール   | [references/dependency-rule.md](references/dependency-rule.md)                         | 依存設計時       |
| レイヤー構造     | [references/layer-structure.md](references/layer-structure.md)                         | レイヤー定義時   |
| 境界設計         | [references/boundary-interfaces.md](references/boundary-interfaces.md)                 | 境界設計時       |
| ハイブリッド対応 | [references/hybrid-architecture-mapping.md](references/hybrid-architecture-mapping.md) | 既存構成の変換時 |
| 要求索引         | [references/requirements-index.md](references/requirements-index.md)                   | 要件参照時       |
| 旧スキル         | [references/legacy-skill.md](references/legacy-skill.md)                               | 互換確認時       |

### assets/（テンプレート・素材）

| アセット                                  | 用途                   |
| ----------------------------------------- | ---------------------- |
| `assets/architecture-review-checklist.md` | レビューチェックリスト |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
