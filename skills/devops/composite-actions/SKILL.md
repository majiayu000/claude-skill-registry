---
name: composite-actions
description: |
  GitHub Actions の Composite Actions 設計と実装を支援するスキル。
  action.yml の構造、入出力設計、再利用性、検証手順を整理する。

  Anchors:
  • 『The Pragmatic Programmer』（Andrew Hunt, David Thomas） / 適用: 自動化設計 / 目的: 再利用可能な処理の整理
  • 『GitHub Actions公式ドキュメント』 / 適用: Composite Actions 実装 / 目的: 構文仕様の準拠
  • 『The Twelve-Factor App』 / 適用: 設定と可搬性 / 目的: アクションの独立性確保
  • 『Release It!』（Michael Nygard） / 適用: エラーハンドリング / 目的: 安定運用の設計

  Trigger:
  Use when designing composite actions, validating action.yml structure, or integrating reusable GitHub Actions steps.
  composite actions, action.yml, reusable action, inputs outputs, github actions
---

# composite-actions

## 概要

Composite Actions を設計・実装・検証し、再利用可能な自動化コンポーネントを構築する。

## ワークフロー

### Phase 1: 要件整理

**目的**: 目的・入出力・制約を明確化する。

**アクション**:

1. 目的と適用範囲を整理する。
2. 入力・出力・環境変数を整理する。
3. 成功条件と制約を整理する。

**Task**: `agents/analyze-composite-requirements.md` を参照

### Phase 2: 設計

**目的**: action.yml の構成と検証方針を定義する。

**アクション**:

1. ステップ構成と実行条件を定義する。
2. inputs/outputs の設計を確定する。
3. エラーハンドリングと検証手順を整理する。

**Task**: `agents/design-composite-action.md` を参照

### Phase 3: 検証と記録

**目的**: 構造と構文を検証し記録を更新する。

**アクション**:

1. `scripts/validate-skill.mjs` で構造を検証する。
2. `scripts/validate-action.mjs` で action.yml を検証する。
3. `scripts/log_usage.mjs` で記録を更新する。

**Task**: `agents/validate-composite-action.md` を参照

## Task仕様ナビ

| Task                           | 起動タイミング | 入力            | 出力                        |
| ------------------------------ | -------------- | --------------- | --------------------------- |
| analyze-composite-requirements | Phase 1開始時  | 目的/制約       | 要件整理メモ、成功条件一覧  |
| design-composite-action        | Phase 2開始時  | 要件整理メモ    | action.yml 草案、実装ガイド |
| validate-composite-action      | Phase 3開始時  | action.yml 草案 | 検証レポート、ログ更新内容  |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                    | 理由                     |
| --------------------------- | ------------------------ |
| 目的を明確にする            | 責務の肥大化を防ぐため   |
| inputs/outputs を明文化する | 再利用性を高めるため     |
| 失敗時の挙動を定義する      | 障害時の再現性を保つため |
| テンプレートを参照する      | 構文ミスを防ぐため       |

### 避けるべきこと

| 禁止事項           | 問題点             |
| ------------------ | ------------------ |
| 複数目的を詰め込む | 保守性が低下する   |
| 入出力を曖昧にする | 利用側の混乱を招く |
| 検証を省略する     | 失敗の検知が遅れる |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                    | 機能                         |
| ----------------------------- | ---------------------------- |
| `scripts/validate-skill.mjs`  | スキル構造の検証             |
| `scripts/validate-action.mjs` | action.yml 構文検証          |
| `scripts/log_usage.mjs`       | 使用記録と評価メトリクス更新 |

### references/（詳細知識）

| リソース           | パス                                                                   | 読込条件       |
| ------------------ | ---------------------------------------------------------------------- | -------------- |
| レベル1 基礎       | [references/Level1_basics.md](references/Level1_basics.md)             | 初回整理時     |
| レベル2 実務       | [references/Level2_intermediate.md](references/Level2_intermediate.md) | 設計時         |
| レベル3 応用       | [references/Level3_advanced.md](references/Level3_advanced.md)         | 詳細設計時     |
| レベル4 専門       | [references/Level4_expert.md](references/Level4_expert.md)             | 改善ループ時   |
| 構文リファレンス   | [references/action-syntax.md](references/action-syntax.md)             | 構成設計時     |
| ベストプラクティス | [references/best-practices.md](references/best-practices.md)           | 設計方針整理時 |
| 旧スキル           | [references/legacy-skill.md](references/legacy-skill.md)               | 互換確認時     |

### assets/（テンプレート・素材）

| アセット                             | 用途                          |
| ------------------------------------ | ----------------------------- |
| `assets/composite-action/action.yml` | Composite Action テンプレート |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
