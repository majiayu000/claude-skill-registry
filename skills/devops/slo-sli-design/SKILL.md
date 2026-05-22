---
name: slo-sli-design
description: |
  SLO（Service Level Objective）とSLI（Service Level Indicator）の設計、
  エラーバジェット管理、信頼性目標の策定を支援するスキル。
  Googleの SRE プラクティスに基づき、適切な信頼性目標を設計する。

  Anchors:
  • Site Reliability Engineering (Google) / 適用: SLO/SLI設計原則 / 目的: 信頼性目標の最適化
  • The Site Reliability Workbook (Google) / 適用: 実践的なSLO実装 / 目的: 運用可能なSLO設計
  • Implementing Service Level Objectives (Hidalgo) / 適用: SLO成熟度モデル / 目的: 段階的導入

  Trigger:
  Use when designing SLOs, defining SLIs, calculating error budgets, or establishing reliability targets.
  SLO design, SLI definition, error budget, reliability target, service level objective
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
---

# SLO/SLI Design

## 概要

SLO/SLI設計とエラーバジェット管理を支援するスキル。
サービスの信頼性目標を適切に設計し、運用可能な形で定義する。

---

## ワークフロー

```
identify-cuj → design-sli → set-slo → calculate-budget → define-policy
                                              ↓
                         review-slo ← monitor-budget
```

### Task 1: CUJ特定（identify-cuj）

Critical User Journey（重要なユーザージャーニー）を特定する。

**Task**: `agents/identify-cuj.md` を参照

### Task 2: SLI設計（design-sli）

測定可能なService Level Indicatorを設計する。

**Task**: `agents/design-sli.md` を参照

### Task 3: SLO設定（set-slo）

適切なService Level Objectiveを設定する。

**Task**: `agents/set-slo.md` を参照

### Task 4: エラーバジェット計算（calculate-budget）

エラーバジェットを計算し、消費率を追跡する。

**Task**: `agents/calculate-budget.md` を参照

### Task 5: ポリシー定義（define-policy）

エラーバジェット消費時のポリシーを定義する。

**Task**: `agents/define-policy.md` を参照

### Task 6: SLOレビュー（review-slo）

既存のSLOをレビューし、改善点を特定する。

**Task**: `agents/review-slo.md` を参照

---

## Task仕様（ナビゲーション）

| Task             | 責務                 | 入力                  | 出力                     |
| ---------------- | -------------------- | --------------------- | ------------------------ |
| identify-cuj     | CUJ特定              | サービス概要          | CUJ一覧                  |
| design-sli       | SLI設計              | CUJ一覧               | SLI定義書                |
| set-slo          | SLO設定              | SLI定義書             | SLO定義書                |
| calculate-budget | エラーバジェット計算 | SLO定義書・実績データ | エラーバジェットレポート |
| define-policy    | ポリシー定義         | SLO定義書             | バジェットポリシー       |
| review-slo       | SLOレビュー          | 既存SLO・実績データ   | 改善提案レポート         |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照
**注記**: 1 Task = 1 責務。CUJ特定から順番に実行することを推奨。

---

## ベストプラクティス

### すべきこと

| 推奨事項                                 | 理由                               |
| ---------------------------------------- | ---------------------------------- |
| ユーザー視点でCUJを定義する              | 技術指標ではなくユーザー体験を測定 |
| 測定可能で自動化可能なSLIを設計する      | 継続的なモニタリングを可能にする   |
| 現実的で達成可能なSLOを設定する          | 100%は目標としない                 |
| エラーバジェットポリシーを事前に定義する | 消費時のアクションを明確にする     |
| 定期的にSLOをレビューする                | ビジネス要件の変化に対応           |

### 避けるべきこと

| 禁止事項                               | 問題点                       |
| -------------------------------------- | ---------------------------- |
| 100%の可用性を目標にする               | 非現実的で改善余地がなくなる |
| 技術指標のみでSLIを設計する            | ユーザー体験と乖離するリスク |
| エラーバジェットを無視して開発を続ける | 信頼性の低下                 |
| 単一のSLOで全てをカバーしようとする    | 重要な指標の見落とし         |

---

## リソース参照

### scripts/（決定論的処理）

| スクリプト                   | 用途                 | 使用例                                                           |
| ---------------------------- | -------------------- | ---------------------------------------------------------------- |
| `calculate-error-budget.mjs` | エラーバジェット計算 | `node scripts/calculate-error-budget.mjs --slo 99.9 --period 30` |
| `log_usage.mjs`              | フィードバック記録   | `node scripts/log_usage.mjs --result success`                    |

### references/（詳細知識）

| リソース             | パス                                                                           | 読込条件                       |
| -------------------- | ------------------------------------------------------------------------------ | ------------------------------ |
| SLI設計ガイド        | [references/sli-design-guide.md](references/sli-design-guide.md)               | SLI設計の詳細が必要時          |
| エラーバジェット管理 | [references/error-budget-management.md](references/error-budget-management.md) | エラーバジェットの詳細が必要時 |

### assets/（テンプレート）

| アセット                              | 用途                |
| ------------------------------------- | ------------------- |
| `assets/slo-definition-template.yaml` | SLO定義テンプレート |

---

## 変更履歴

| Version | Date       | Changes                        |
| ------- | ---------- | ------------------------------ |
| 2.0.0   | 2026-01-02 | 18-skills.md仕様準拠で全面改訂 |
| 1.0.0   | 2025-12-24 | 初版作成                       |
