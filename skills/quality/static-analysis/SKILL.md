---
name: static-analysis
description: |
  静的コード解析と品質メトリクスの設定、複雑度評価、Code Smell検出を支援するスキル。
  品質基準の策定から改善優先度付けまでを一貫して整理する。

  Anchors:
  • Clean Code / 適用: 品質基準 / 目的: コード品質の判定
  • Code Complete / 適用: 複雑度管理 / 目的: 認知負荷の低減

  Trigger:
  Use when configuring static analysis, defining quality gates, measuring complexity, or triaging code smells.
  static analysis, complexity metrics, code smells, quality gate
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# static-analysis

## 概要

静的解析の対象範囲と指標を定義し、解析結果を改善優先度へ落とし込む。

---

## ワークフロー

### Phase 1: 対象範囲と指標の決定

**目的**: 解析対象と閾値を確定する

**アクション**:

1. `references/Level1_basics.md` で基礎指針を確認する
2. `references/threshold-guidelines.md` で閾値を決める
3. 解析対象の範囲と除外条件を整理する

**Task**: `agents/sa-001-metric-scope.md` を参照

### Phase 2: 解析実行と検出

**目的**: メトリクス測定とCode Smell検出を実行する

**アクション**:

1. `scripts/analyze-complexity.mjs` を実行する
2. `references/complexity-metrics.md` を参照し指標を解釈する
3. `references/code-smells.md` でSmellを分類する

**Task**: `agents/sa-002-run-analysis.md` を参照

### Phase 3: トリアージと改善計画

**目的**: 改善優先度と対応方針を整理する

**アクション**:

1. `references/Level2_intermediate.md` と `references/Level3_advanced.md` を参照する
2. 影響範囲と修正コストを評価する
3. 改善計画を作成する

**Task**: `agents/sa-003-triage-findings.md` を参照

---

## Task仕様ナビ

| Task                   | 起動タイミング | 入力                     | 出力         |
| ---------------------- | -------------- | ------------------------ | ------------ |
| sa-001-metric-scope    | Phase 1開始時  | 対象コード情報、品質目標 | 指標設定表   |
| sa-002-run-analysis    | Phase 2開始時  | 指標設定表、対象コード   | 解析結果一覧 |
| sa-003-triage-findings | Phase 3開始時  | 解析結果一覧、チーム制約 | 改善優先度表 |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照
**注記**: Task名は目的に合わせて定義する

---

## ベストプラクティス

### すべきこと

| 推奨事項                 | 理由                         |
| ------------------------ | ---------------------------- |
| 閾値の根拠を明文化する   | 合意形成と運用が安定する     |
| 言語特性を考慮する       | 不適切な一律基準を避けられる |
| 結果をカテゴリで整理する | 改善の優先度が明確になる     |
| 定期的に再計測する       | 技術的債務の再発を防ぐ       |

### 避けるべきこと

| 禁止事項           | 問題点                     |
| ------------------ | -------------------------- |
| 根拠のない閾値設定 | 評価基準がぶれる           |
| 解析結果の放置     | 技術的債務が蓄積する       |
| 目的外の解析拡張   | ノイズが増え優先度が下がる |
| 修正計画の不在     | 実行に移せなくなる         |

---

## リソース参照

### scripts/（決定論的処理）

| スクリプト                       | 機能             |
| -------------------------------- | ---------------- |
| `scripts/analyze-complexity.mjs` | 複雑度分析の実行 |
| `scripts/validate-skill.mjs`     | スキル構造の検証 |
| `scripts/log_usage.mjs`          | 使用記録の保存   |

### references/（詳細知識）

| リソース   | パス                                                                     | 読込条件         |
| ---------- | ------------------------------------------------------------------------ | ---------------- |
| 基礎指針   | [references/Level1_basics.md](references/Level1_basics.md)               | 導入時           |
| 実務指針   | [references/Level2_intermediate.md](references/Level2_intermediate.md)   | 実務適用時       |
| 応用指針   | [references/Level3_advanced.md](references/Level3_advanced.md)           | CI/CD統合時      |
| 専門指針   | [references/Level4_expert.md](references/Level4_expert.md)               | 高度な調整時     |
| Code Smell | [references/code-smells.md](references/code-smells.md)                   | Smell分類時      |
| 複雑度指標 | [references/complexity-metrics.md](references/complexity-metrics.md)     | メトリクス解釈時 |
| 閾値ガイド | [references/threshold-guidelines.md](references/threshold-guidelines.md) | 閾値設定時       |

### assets/（テンプレート・素材）

| アセット                     | 用途               |
| ---------------------------- | ------------------ |
| `assets/basic-metrics.json`  | 基本メトリクス定義 |
| `assets/strict-metrics.json` | 厳格メトリクス定義 |
