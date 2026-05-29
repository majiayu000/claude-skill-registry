---
name: command-activation-mechanisms
description: |
  コマンド起動の仕組みを整理し、明示起動/自動起動/Extended Thinkingの設計と検証を支援するスキル。
  起動フロー、トリガー設計、検証手順を一貫して整理する。

  Anchors:
  • The Pragmatic Programmer (Andrew Hunt, David Thomas) / 適用: 手順設計 / 目的: 実行フローの最適化
  • Human-Computer Interaction (Dix et al.) / 適用: 起動UX設計 / 目的: 誤起動の抑制
  • Automation Patterns / 適用: 自動起動設計 / 目的: 安定運用

  Trigger:
  Use when designing command activation flows, defining auto-invocation triggers, or validating command execution paths.
  command activation, auto invocation, extended thinking, slashcommand, execution flow
---

# command-activation-mechanisms

## 概要

コマンド起動のフロー設計とトリガー設計を整理し、誤起動を防ぎながら運用可能にする。

## ワークフロー

### Phase 1: 要件整理

**目的**: 起動条件と対象範囲を明確化する。

**アクション**:

1. 起動パターン（明示/自動/Extended Thinking）を整理する。
2. 対象コマンドと制約条件を整理する。
3. 参照すべきフロー資料を選定する。

**Task**: `agents/analyze-activation-requirements.md` を参照

### Phase 2: 起動設計

**目的**: 起動トリガーとフローを設計する。

**アクション**:

1. 起動トリガーと条件を設計する。
2. 実行フロー図とテンプレートを整備する。
3. 例外ケースと安全策を定義する。

**Task**: `agents/design-activation-flow.md` を参照

### Phase 3: 検証と記録

**目的**: 起動メカニズムを検証し記録する。

**アクション**:

1. 検証スクリプトで起動条件を確認する。
2. レビュー結果と改善点を記録する。
3. ログと評価情報を更新する。

**Task**: `agents/validate-activation-mechanisms.md` を参照

## Task仕様ナビ

| Task                            | 起動タイミング | 入力          | 出力                     |
| ------------------------------- | -------------- | ------------- | ------------------------ |
| analyze-activation-requirements | Phase 1開始時  | 起動条件/制約 | 要件整理メモ、参照一覧   |
| design-activation-flow          | Phase 2開始時  | 要件整理メモ  | フロー設計、トリガー設計 |
| validate-activation-mechanisms  | Phase 3開始時  | フロー設計    | 検証レポート、改善方針   |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項             | 理由                     |
| -------------------- | ------------------------ |
| 起動条件を明文化する | 誤起動を防ぐため         |
| フロー図を更新する   | 運用の再現性を高めるため |
| 例外ケースを整理する | 想定外の挙動を防ぐため   |

### 避けるべきこと

| 禁止事項               | 問題点                 |
| ---------------------- | ---------------------- |
| トリガーを増やしすぎる | 誤起動が増える         |
| 検証なしで運用する     | 不具合が継続する       |
| 記録を残さない         | 改善サイクルが回らない |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                        | 機能                         |
| --------------------------------- | ---------------------------- |
| `scripts/validate-activation.mjs` | 起動メカニズム検証           |
| `scripts/log_usage.mjs`           | 使用記録と評価メトリクス更新 |
| `scripts/validate-skill.mjs`      | スキル構造の検証             |

### references/（詳細知識）

| リソース           | パス                                                                                 | 読込条件       |
| ------------------ | ------------------------------------------------------------------------------------ | -------------- |
| Level1 基礎        | [references/Level1_basics.md](references/Level1_basics.md)                           | 初回整理時     |
| Level2 実務        | [references/Level2_intermediate.md](references/Level2_intermediate.md)               | 起動設計時     |
| Level3 応用        | [references/Level3_advanced.md](references/Level3_advanced.md)                       | 詳細検討時     |
| Level4 専門        | [references/Level4_expert.md](references/Level4_expert.md)                           | 改善ループ時   |
| 実行フロー         | [references/execution-flow-diagrams.md](references/execution-flow-diagrams.md)       | フロー設計時   |
| Extended Thinking  | [references/extended-thinking-triggers.md](references/extended-thinking-triggers.md) | トリガー設計時 |
| SlashCommandガイド | [references/slashcommand-tool-guide.md](references/slashcommand-tool-guide.md)       | 自動起動設計時 |
| 明示起動パターン   | [references/user-explicit-activation.md](references/user-explicit-activation.md)     | 明示起動設計時 |
| 要求索引           | [references/requirements-index.md](references/requirements-index.md)                 | 要件参照時     |
| 旧スキル           | [references/legacy-skill.md](references/legacy-skill.md)                             | 互換確認時     |

### assets/（テンプレート・素材）

| アセット                               | 用途                          |
| -------------------------------------- | ----------------------------- |
| `assets/auto-invocation-template.md`   | 自動起動テンプレート          |
| `assets/extended-thinking-template.md` | Extended Thinkingテンプレート |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
