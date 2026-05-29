---
name: command-arguments-system
description: |
  コマンド引数（$ARGUMENTS、位置引数）の設計と検証を整理し、引数仕様・検証・エラー設計を一貫して支援するスキル。
  引数設計方針、検証ルール、テンプレート運用を段階化する。

  Anchors:
  • The Pragmatic Programmer (Andrew Hunt, David Thomas) / 適用: 引数仕様と検証の設計 / 目的: 堅牢な引数システムの確立

  Trigger:
  Use when adding command arguments, defining $ARGUMENTS or positional arguments, or designing argument validation/error handling.
  command arguments, $ARGUMENTS, positional arguments, argument validation, error message design
---

# command-arguments-system

## 概要

コマンド引数（$ARGUMENTS、位置引数）の設計と検証を整理し、引数仕様・検証・エラー設計を一貫して支援する。

## ワークフロー

### Phase 1: 要件整理

**目的**: 引数要件と利用シナリオを明確化する。

**アクション**:

1. 引数の目的と対象操作を整理する。
2. 必須/任意/位置引数の範囲を確認する。
3. 参照ガイドとテンプレートを選定する。

**Task**: `agents/analyze-argument-requirements.md` を参照

### Phase 2: 引数設計

**目的**: 引数仕様と検証方針を具体化する。

**アクション**:

1. 引数形式とデフォルト値を定義する。
2. 検証ルールとエラーメッセージ方針を設計する。
3. テンプレートを使い設計を具体化する。

**Task**: `agents/design-argument-schema.md` を参照

### Phase 3: 検証と記録

**目的**: 引数設計を検証し、記録を残す。

**アクション**:

1. 引数検証スクリプトで整合性を確認する。
2. 検証結果と改善点を記録する。
3. ログと評価情報を更新する。

**Task**: `agents/validate-argument-system.md` を参照

## Task仕様ナビ

| Task                          | 起動タイミング | 入力                  | 出力                             |
| ----------------------------- | -------------- | --------------------- | -------------------------------- |
| analyze-argument-requirements | Phase 1開始時  | 引数要求/利用シナリオ | 要件整理メモ、引数一覧           |
| design-argument-schema        | Phase 2開始時  | 要件整理メモ          | 引数仕様、検証方針、エラールール |
| validate-argument-system      | Phase 3開始時  | 引数仕様              | 検証レポート、改善方針           |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                                 | 理由                     |
| ---------------------------------------- | ------------------------ |
| 引数の目的と利用者を明確にする           | 仕様のブレを防ぐため     |
| 検証ルールとエラーメッセージを先に決める | 実装漏れを防ぐため       |
| テンプレートで表現を統一する             | 説明の一貫性が保てるため |

### 避けるべきこと

| 禁止事項                     | 問題点             |
| ---------------------------- | ------------------ |
| 引数仕様を口頭だけで済ませる | 実装が曖昧になる   |
| 検証を省略する               | 不正入力に弱くなる |
| 記録を残さない               | 改善が続かない     |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                       | 機能                         |
| -------------------------------- | ---------------------------- |
| `scripts/validate-arguments.mjs` | 引数設計の検証               |
| `scripts/log_usage.mjs`          | 使用記録と評価メトリクス更新 |
| `scripts/validate-skill.mjs`     | スキル構造の検証             |

### references/（詳細知識）

| リソース         | パス                                                                   | 読込条件     |
| ---------------- | ---------------------------------------------------------------------- | ------------ |
| レベル1 基礎     | [references/Level1_basics.md](references/Level1_basics.md)             | 初回整理時   |
| レベル2 実務     | [references/Level2_intermediate.md](references/Level2_intermediate.md) | 引数設計時   |
| レベル3 応用     | [references/Level3_advanced.md](references/Level3_advanced.md)         | 仕様深化時   |
| レベル4 専門     | [references/Level4_expert.md](references/Level4_expert.md)             | 改善ループ時 |
| 引数リファレンス | [references/arguments-reference.md](references/arguments-reference.md) | 仕様確認時   |
| 旧スキル         | [references/legacy-skill.md](references/legacy-skill.md)               | 互換確認時   |

### assets/（テンプレート・素材）

| アセット                      | 用途                         |
| ----------------------------- | ---------------------------- |
| `assets/command-with-args.md` | 引数付きコマンドテンプレート |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
