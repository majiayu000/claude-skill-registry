---
name: command-advanced-patterns
description: |
  高度なコマンド設計パターンを整理し、パイプライン/メタコマンド/インタラクティブ設計を支援するスキル。
  パターン選定、テンプレート適用、検証手順を一貫して整理する。

  Anchors:
  • The Pragmatic Programmer (Andrew Hunt, David Thomas) / 適用: 実践パターン選定 / 目的: 再現性のある設計
  • Design Patterns (GoF) / 適用: パターン適用判断 / 目的: 拡張性の確保
  • User-Centered Design / 適用: インタラクティブ設計 / 目的: 誤操作の抑制

  Trigger:
  Use when designing pipeline commands, meta-commands, or interactive command flows.
  command patterns, pipeline command, meta command, interactive command
---

# command-advanced-patterns

## 概要

高度なコマンド設計パターンを整理し、複合的な起動や対話フローを設計する。

## ワークフロー

### Phase 1: 要件整理

**目的**: 適用パターンと対象範囲を明確化する。

**アクション**:

1. 対象コマンドと目的を整理する。
2. 適用パターン（パイプライン/メタ/インタラクティブ）を選定する。
3. 参照ガイドとテンプレートを確認する。

**Task**: `agents/analyze-advanced-requirements.md` を参照

### Phase 2: パターン設計

**目的**: パターン設計と実装方針を具体化する。

**アクション**:

1. 選定パターンのフローと責務を定義する。
2. テンプレートを使い設計を具体化する。
3. 例外ケースとガードレールを整理する。

**Task**: `agents/design-advanced-patterns.md` を参照

### Phase 3: 検証と記録

**目的**: 実装方針を検証し、記録を残す。

**アクション**:

1. 検証スクリプトでパターン整合を確認する。
2. レビュー結果と改善点を整理する。
3. ログと評価情報を更新する。

**Task**: `agents/validate-advanced-patterns.md` を参照

## Task仕様ナビ

| Task                          | 起動タイミング | 入力              | 出力                           |
| ----------------------------- | -------------- | ----------------- | ------------------------------ |
| analyze-advanced-requirements | Phase 1開始時  | 対象コマンド/目的 | 要件整理メモ、適用パターン一覧 |
| design-advanced-patterns      | Phase 2開始時  | 要件整理メモ      | パターン設計案、テンプレ適用案 |
| validate-advanced-patterns    | Phase 3開始時  | パターン設計案    | 検証レポート、改善方針         |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                     | 理由                   |
| ---------------------------- | ---------------------- |
| パターンを明確に選定する     | 実装ブレを防ぐため     |
| テンプレートで設計を統一する | 変更容易性が高まるため |
| 例外ケースを明記する         | 安定運用につながるため |

### 避けるべきこと

| 禁止事項                         | 問題点             |
| -------------------------------- | ------------------ |
| 複数パターンを無計画に混在させる | 挙動が不明確になる |
| 検証なしで実装する               | 不具合が残る       |
| 記録を残さない                   | 改善が続かない     |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                      | 機能                         |
| ------------------------------- | ---------------------------- |
| `scripts/validate-advanced.mjs` | 高度パターン検証             |
| `scripts/log_usage.mjs`         | 使用記録と評価メトリクス更新 |
| `scripts/validate-skill.mjs`    | スキル構造の検証             |

### references/（詳細知識）

| リソース         | パス                                                                                 | 読込条件           |
| ---------------- | ------------------------------------------------------------------------------------ | ------------------ |
| Level1 基礎      | [references/Level1_basics.md](references/Level1_basics.md)                           | 初回整理時         |
| Level2 実務      | [references/Level2_intermediate.md](references/Level2_intermediate.md)               | パターン選定時     |
| Level3 応用      | [references/Level3_advanced.md](references/Level3_advanced.md)                       | 詳細設計時         |
| Level4 専門      | [references/Level4_expert.md](references/Level4_expert.md)                           | 改善ループ時       |
| パイプライン     | [references/pipeline-pattern-guide.md](references/pipeline-pattern-guide.md)         | パイプライン設計時 |
| メタコマンド     | [references/meta-command-pattern-guide.md](references/meta-command-pattern-guide.md) | メタ設計時         |
| インタラクティブ | [references/interactive-pattern-guide.md](references/interactive-pattern-guide.md)   | 対話設計時         |
| 旧スキル         | [references/legacy-skill.md](references/legacy-skill.md)                             | 互換確認時         |

### assets/（テンプレート・素材）

| アセット                          | 用途                         |
| --------------------------------- | ---------------------------- |
| `assets/pipeline-template.md`     | パイプラインテンプレート     |
| `assets/meta-command-template.md` | メタコマンドテンプレート     |
| `assets/interactive-template.md`  | インタラクティブテンプレート |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
