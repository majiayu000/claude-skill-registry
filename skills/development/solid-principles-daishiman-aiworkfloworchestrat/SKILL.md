---
name: solid-principles
description: |
  SOLID原則（SRP, OCP, LSP, ISP, DIP）を適用してオブジェクト指向設計の品質を評価・改善するスキル。
  アーキテクチャレビュー、リファクタリング判断、コード品質評価を支援する。

  Anchors:
  • Clean Architecture (Robert C. Martin) / 適用: 依存性逆転と層分離 / 目的: 適切な依存方向の確保
  • SOLID Principles (Robert C. Martin) / 適用: 5原則による設計評価 / 目的: 保守性・テスト容易性・柔軟性の実現
  • Refactoring (Martin Fowler) / 適用: コードの匂い検出と改善 / 目的: 段階的な設計改善

  Trigger:
  Use when evaluating code architecture, reviewing design quality, detecting SOLID violations, planning refactoring, or improving object-oriented design.
  single responsibility, open closed, liskov substitution, interface segregation, dependency inversion, architecture review, design patterns, refactoring, SOLID
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# SOLID Principles

## 概要

ロバート・C・マーティンが体系化したSOLID原則を適用し、オブジェクト指向設計の品質を評価・改善するスキル。
各原則の違反を検出し、具体的なリファクタリング方針を提示する。

## ワークフロー

```
analyze-codebase → detect-violations → evaluate-impact → plan-refactoring → validate-improvements
```

### Phase 1: コードベース分析

**目的**: 分析対象のコード構造と依存関係を把握する

**アクション**:

1. 対象ファイル・モジュールを特定する
2. クラス・関数の責務を整理する
3. 依存関係グラフを把握する

**Task**: `agents/analyze-codebase.md` を参照

### Phase 2: 違反検出

**目的**: SOLID原則の違反箇所を特定する

**アクション**:

1. 各原則に対する違反パターンをチェックする
2. `scripts/check-solid-violations.mjs` で自動検出を実行する
3. 検出結果を整理する

**Task**: `agents/detect-violations.md` を参照

### Phase 3: 影響評価

**目的**: 違反の影響度と優先度を評価する

**アクション**:

1. 各違反の影響範囲を分析する
2. 修正の緊急度と難易度を評価する
3. 優先順位を決定する

**Task**: `agents/evaluate-impact.md` を参照

### Phase 4: リファクタリング計画

**目的**: 具体的な改善計画を策定する

**アクション**:

1. 各違反に対する改善パターンを選定する
2. 段階的な修正手順を策定する
3. テスト計画を含めた実行計画を作成する

**Task**: `agents/plan-refactoring.md` を参照

## Task仕様ナビ

| Task              | 起動タイミング | 入力               | 出力                   |
| ----------------- | -------------- | ------------------ | ---------------------- |
| analyze-codebase  | Phase 1開始時  | 対象ファイルパス   | コード構造レポート     |
| detect-violations | Phase 2開始時  | コード構造レポート | 違反検出レポート       |
| evaluate-impact   | Phase 3開始時  | 違反検出レポート   | 影響評価レポート       |
| plan-refactoring  | Phase 4開始時  | 影響評価レポート   | リファクタリング計画書 |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                        | 理由                               |
| ------------------------------- | ---------------------------------- |
| 1クラス1責務を維持する（SRP）   | 変更理由の単一化で保守性向上       |
| 拡張に開き修正に閉じる（OCP）   | 既存コードを壊さず機能追加可能     |
| 派生型は基底型と置換可能（LSP） | 多態性の正しい利用を保証           |
| クライアント固有のIF分離（ISP） | 不要な依存を排除                   |
| 抽象に依存する（DIP）           | 高レベルモジュールの独立性確保     |
| 小さな改善を継続する            | 大規模リファクタリングのリスク回避 |

### 避けるべきこと

| 禁止事項                     | 問題点                     |
| ---------------------------- | -------------------------- |
| 神クラス（God Class）の作成  | 責務過多で変更影響が広範囲 |
| 継承の濫用                   | LSP違反と密結合を招く      |
| 具象クラスへの直接依存       | テスト困難と変更影響の拡大 |
| 過度な抽象化                 | 複雑性増加で可読性低下     |
| テストなしのリファクタリング | 回帰バグのリスク           |

## リソース参照

### references/（詳細知識）

| リソース             | パス                                                                       | 読込条件            |
| -------------------- | -------------------------------------------------------------------------- | ------------------- |
| 単一責務の原則       | [references/single-responsibility.md](references/single-responsibility.md) | SRP違反検出・改善時 |
| 開放閉鎖の原則       | [references/open-closed.md](references/open-closed.md)                     | OCP違反検出・改善時 |
| リスコフの置換原則   | [references/liskov-substitution.md](references/liskov-substitution.md)     | LSP違反検出・改善時 |
| インターフェース分離 | [references/interface-segregation.md](references/interface-segregation.md) | ISP違反検出・改善時 |
| 依存性逆転の原則     | [references/dependency-inversion.md](references/dependency-inversion.md)   | DIP違反検出・改善時 |

### scripts/（決定論的処理）

| スクリプト                   | 機能                | 使用例                                           |
| ---------------------------- | ------------------- | ------------------------------------------------ |
| `check-solid-violations.mjs` | SOLID違反の自動検出 | `node scripts/check-solid-violations.mjs <path>` |
| `log_usage.mjs`              | 使用記録の保存      | `node scripts/log_usage.mjs --result success`    |
| `validate-skill.mjs`         | スキル構造検証      | `node scripts/validate-skill.mjs`                |

### assets/（テンプレート）

| アセット                    | 用途                        |
| --------------------------- | --------------------------- |
| `solid-review-checklist.md` | SOLIDレビューチェックリスト |

## 変更履歴

| Version | Date       | Changes                                                    |
| ------- | ---------- | ---------------------------------------------------------- |
| 2.0.0   | 2026-01-03 | 18-skills.md仕様に完全準拠、agents追加、ワークフロー再構成 |
| 1.0.0   | 2025-12-24 | 初版作成                                                   |
