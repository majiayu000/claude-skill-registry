---
name: command-basic-patterns
description: |
  基本実装パターン（シンプル指示/ステップバイステップ/条件分岐/ファイル参照）を整理し、パターン選定とテンプレート適用を支援するスキル。
  選定基準、実装の骨格、検証手順を一貫して整理する。

  Anchors:
  • The Pragmatic Programmer (Andrew Hunt, David Thomas) / 適用: コマンド設計 / 目的: 実践的な手順設計パターンの習得

  Trigger:
  Use when selecting or reviewing basic command patterns, or structuring workflows for simple/step/conditional/file-reference commands.
  command basic patterns, simple command, step-by-step, conditional command, file reference
---

# command-basic-patterns

## 概要

基本実装パターン（シンプル指示/ステップバイステップ/条件分岐/ファイル参照）を整理し、パターン選定とテンプレート適用を支援する。

## ワークフロー

### Phase 1: 要件整理

**目的**: 適用パターンと対象範囲を明確化する。

**アクション**:

1. 対象コマンドの目的と制約を整理する。
2. パターン選定ガイドで候補を絞る。
3. 参照ガイドとテンプレートを確認する。

**Task**: `agents/analyze-basic-patterns.md` を参照

### Phase 2: パターン設計

**目的**: パターン設計と実装方針を具体化する。

**アクション**:

1. 選定パターンの構造とステップを設計する。
2. テンプレートを使い設計を具体化する。
3. 例外ケースとガードレールを整理する。

**Task**: `agents/design-basic-patterns.md` を参照

### Phase 3: 検証と記録

**目的**: パターン整合を検証し、記録を残す。

**アクション**:

1. パターン検証スクリプトで整合性を確認する。
2. 検証結果と改善点を整理する。
3. ログと評価情報を更新する。

**Task**: `agents/validate-basic-patterns.md` を参照

## Task仕様ナビ

| Task                    | 起動タイミング | 入力              | 出力                           |
| ----------------------- | -------------- | ----------------- | ------------------------------ |
| analyze-basic-patterns  | Phase 1開始時  | 対象コマンド/目的 | 要件整理メモ、適用パターン候補 |
| design-basic-patterns   | Phase 2開始時  | 要件整理メモ      | パターン設計案、テンプレ適用案 |
| validate-basic-patterns | Phase 3開始時  | パターン設計案    | 検証レポート、改善方針         |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                     | 理由                   |
| ---------------------------- | ---------------------- |
| パターンを明確に選定する     | 実装ブレを防ぐため     |
| テンプレートで設計を統一する | 読みやすさが保てるため |
| 検証スクリプトを実行する     | 逸脱を検知するため     |

### 避けるべきこと

| 禁止事項                         | 問題点               |
| -------------------------------- | -------------------- |
| 複数パターンを無計画に混在させる | 挙動が不明確になる   |
| 例外処理を後回しにする           | 失敗時に対応できない |
| 記録を残さない                   | 改善が続かない       |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                      | 機能                         |
| ------------------------------- | ---------------------------- |
| `scripts/validate-patterns.mjs` | 基本パターン検証             |
| `scripts/log_usage.mjs`         | 使用記録と評価メトリクス更新 |
| `scripts/validate-skill.mjs`    | スキル構造の検証             |

### references/（詳細知識）

| リソース     | パス                                                                           | 読込条件       |
| ------------ | ------------------------------------------------------------------------------ | -------------- |
| レベル1 基礎 | [references/Level1_basics.md](references/Level1_basics.md)                     | 初回整理時     |
| レベル2 実務 | [references/Level2_intermediate.md](references/Level2_intermediate.md)         | パターン選定時 |
| レベル3 応用 | [references/Level3_advanced.md](references/Level3_advanced.md)                 | 詳細設計時     |
| レベル4 専門 | [references/Level4_expert.md](references/Level4_expert.md)                     | 改善ループ時   |
| パターン選定 | [references/pattern-selection-guide.md](references/pattern-selection-guide.md) | パターン選定時 |
| 旧スキル     | [references/legacy-skill.md](references/legacy-skill.md)                       | 互換確認時     |

### assets/（テンプレート・素材）

| アセット                                | 用途                             |
| --------------------------------------- | -------------------------------- |
| `assets/simple-instruction-template.md` | シンプル指示テンプレート         |
| `assets/step-by-step-template.md`       | ステップバイステップテンプレート |
| `assets/conditional-template.md`        | 条件分岐テンプレート             |
| `assets/file-reference-template.md`     | ファイル参照テンプレート         |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
