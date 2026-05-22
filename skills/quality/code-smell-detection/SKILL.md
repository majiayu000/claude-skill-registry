---
name: code-smell-detection
description: |
  コードスメルとアーキテクチャ・アンチパターンを整理し、レビューと改善対象の特定を支援するスキル。
  クラス/メソッドのスメル検出、改善優先度の整理、レポート化を扱う。

  Anchors:
  • Clean Code (Robert C. Martin) / 適用: コード品質レビュー / 目的: 意図の明確化
  • Refactoring (Martin Fowler) / 適用: スメル検出と改善 / 目的: 安全な修正
  • Working Effectively with Legacy Code (Michael Feathers) / 適用: 改善対象の特定 / 目的: リスク最小化

  Trigger:
  Use when detecting code smells, identifying refactoring targets, analyzing technical debt, or documenting anti-patterns.
  code smells, anti-patterns, refactoring targets, technical debt, architecture review
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# code-smell-detection

## 概要

コードスメルとアンチパターンを検出し、改善対象の優先度と対応方針を整理する。

## ワークフロー

### Phase 1: 現状把握

**目的**: スメルの種類と対象範囲を明確化する。

**アクション**:

1. 対象コードと検出対象（クラス/メソッド/構造）を整理する。
2. 参照すべきスメル定義を選定する。
3. 出力レポートの形式を確認する。

**Task**: `agents/analyze-smell-scope.md` を参照

### Phase 2: スメル検出

**目的**: 検出結果と改善優先度をまとめる。

**アクション**:

1. 検出スクリプトとレビューでスメルを抽出する。
2. 影響度と優先度を評価する。
3. 改善対象と対応方針を整理する。

**Task**: `agents/design-smell-remediation.md` を参照

### Phase 3: 検証と記録

**目的**: レポートを確定し、ログと評価を更新する。

**アクション**:

1. レポート内容を検証する。
2. 改善計画をレポートに反映する。
3. ログと評価情報を更新する。

**Task**: `agents/validate-smell-report.md` を参照

## Task仕様ナビ

| Task                     | 起動タイミング | 入力                | 出力                           |
| ------------------------ | -------------- | ------------------- | ------------------------------ |
| analyze-smell-scope      | Phase 1開始時  | 対象コード/検出対象 | 対象範囲メモ、参照一覧         |
| design-smell-remediation | Phase 2開始時  | 検出結果            | 優先度付きスメル一覧、改善方針 |
| validate-smell-report    | Phase 3開始時  | レポート草案        | 確定レポート、ログ更新内容     |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                     | 理由                 |
| ---------------------------- | -------------------- |
| スメル定義を統一して検出する | 判定ブレを防ぐため   |
| 改善優先度を明記する         | 対応順が明確になる   |
| レポートを更新する           | 改善活動の継続に必要 |

### 避けるべきこと

| 禁止事項                 | 問題点               |
| ------------------------ | -------------------- |
| スメルの定義を曖昧にする | 誤検出が増える       |
| 影響度を評価しない       | 重要度が判断できない |
| レポートなしで改善する   | 追跡が困難になる     |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                       | 機能                         |
| -------------------------------- | ---------------------------- |
| `scripts/detect-code-smells.mjs` | コードスメル検出             |
| `scripts/log_usage.mjs`          | 使用記録と評価メトリクス更新 |
| `scripts/validate-skill.mjs`     | スキル構造の検証             |

### references/（詳細知識）

| リソース                     | パス                                                                               | 読込条件         |
| ---------------------------- | ---------------------------------------------------------------------------------- | ---------------- |
| Level1 基礎                  | [references/Level1_basics.md](references/Level1_basics.md)                         | 初回整理時       |
| Level2 実務                  | [references/Level2_intermediate.md](references/Level2_intermediate.md)             | 検出準備時       |
| Level3 応用                  | [references/Level3_advanced.md](references/Level3_advanced.md)                     | 詳細分析時       |
| Level4 専門                  | [references/Level4_expert.md](references/Level4_expert.md)                         | 改善ループ時     |
| アーキテクチャアンチパターン | [references/architecture-antipatterns.md](references/architecture-antipatterns.md) | 構造問題の分析時 |
| クラススメル                 | [references/class-smells.md](references/class-smells.md)                           | クラス分析時     |
| メソッドスメル               | [references/method-smells.md](references/method-smells.md)                         | メソッド分析時   |
| 旧スキル                     | [references/legacy-skill.md](references/legacy-skill.md)                           | 互換確認時       |

### assets/（テンプレート・素材）

| アセット                      | 用途               |
| ----------------------------- | ------------------ |
| `assets/code-smell-report.md` | スメル検出レポート |

### 運用ファイル

| ファイル     | 目的                       |
| ------------ | -------------------------- |
| `EVALS.json` | レベル評価・メトリクス管理 |
| `LOGS.md`    | 実行ログの蓄積             |

## 変更履歴

| Version | Date       | Changes                                    |
| ------- | ---------- | ------------------------------------------ |
| 1.1.0   | 2026-01-06 | class-smells.mdにGod Component検出事例追加 |
| 1.0.0   | 2025-12-31 | 初版作成                                   |
