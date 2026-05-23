---
name: requirements-triage
description: |
  複数の要件や要望を体系的に分析・評価し、実装する項目を決定するスキル。
  MoSCoW分類、優先度スコアリング、影響分析を提供する。
  プロジェクト初期段階での要件整理から、開発中の追加要望への対応まで幅広く活用できる。

  Anchors:
  • Software Requirements (Karl Wiegers) / 適用: 要件優先順位付け / 目的: リソース最適配分
  • Lean Analytics (Alistair Croll) / 適用: ビジネス価値評価 / 目的: 戦略的決定支援
  • Prioritization Frameworks / 適用: MoSCoW, RICE, Kano / 目的: 体系的な優先順位決定

  Trigger:
  Use when triaging multiple requirements, prioritizing features, defining scope, or making resource allocation decisions.
  requirements triage, priority scoring, MoSCoW classification, scope management, feature prioritization, 要件トリアージ, 優先順位付け

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# 要件トリアージスキル

## 概要

複数の要望や要件が存在する場合に、体系的に分析・評価し、実装するべき項目を決定するスキル。MoSCoW分類、優先度スコアリング、ビジネス価値・実現可能性・リスク・コストの評価を通じて、限られたリソースで最大の価値を提供する要件セットを確定する。

## ワークフロー

### Phase 1: 要件収集と前提条件の確認

**目的**: トリアージに必要な情報を整理し、評価基準を設定する

**アクション**:

1. すべての要件・要望をリストアップする
2. プロジェクトの制約（期限、予算、人員、技術制約）を確認
3. ビジネス目標と成功基準を明確にする
4. ステークホルダーの期待値を整理する

**Task**: `agents/collect-requirements.md` を参照

### Phase 2: 要件の分析と優先順位付け

**目的**: MoSCoW分類とスコアリングにより、要件を階層化する

**アクション**:

1. 各要件をMust/Should/Could/Won'tに分類する
2. ビジネス価値、実現可能性、リスク、コストを評価する
3. `scripts/calculate-priority.mjs` で優先度スコアを計算
4. `assets/triage-matrix.md` を使用して結果を可視化する
5. 重要な判断根拠をドキュメント化する

**Task**: `agents/prioritize-requirements.md` を参照

### Phase 3: 決定の検証と記録

**目的**: 評価の妥当性を確認し、実行可能な要件セットを確定する

**アクション**:

1. MoSCoW分類が適切か、ステークホルダーと共に検証する
2. 現実的なスケジュールとリソース配分を確認する
3. 依存関係と実装順序を整理する
4. `scripts/log_usage.mjs` で使用記録と評価を実施
5. 最終的な要件セットをプロジェクト計画に反映する

**Task**: `agents/validate-decisions.md` を参照

## Task仕様（ナビゲーション）

| Task                    | 起動タイミング | 入力                                     | 出力               |
| ----------------------- | -------------- | ---------------------------------------- | ------------------ |
| collect-requirements    | Phase 1開始時  | 要望リスト、制約条件                     | 整理済み要件一覧   |
| prioritize-requirements | Phase 2開始時  | 整理済み要件、評価基準                   | スコア付き優先度表 |
| validate-decisions      | Phase 3開始時  | スコア付き優先度表、ステークホルダー意見 | 確定済み要件セット |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- 早期に全要望をリストアップし、優先度を付ける
- ビジネス価値、技術難易度、リスク、コストの4観点から評価する
- 重要な優先度判断について、ステークホルダーとの合意を取る
- 判断根拠を明確に記録し、後からの変更要求に対応できる準備をする
- 定期的に優先度の再評価を検討する

### 避けるべきこと

- 定量的根拠なしの感覚的な優先度付け
- すべてをMustと判定（バランスの取れた分類を目指す）
- ステークホルダー合意なしの決定
- リソース見積の過度な楽観
- 要件記録の省略（「なぜそこが優先されたのか」を追跡できない状態）

## リソース参照

### references/（詳細知識）

| リソース             | パス                                                                                   | 用途             |
| -------------------- | -------------------------------------------------------------------------------------- | ---------------- |
| MoSCoWフレームワーク | See [references/moscow-framework.md](references/moscow-framework.md)                   | 分類基準と実践例 |
| 優先度評価ガイド     | See [references/priority-evaluation-guide.md](references/priority-evaluation-guide.md) | スコアリング詳細 |
| ステークホルダー管理 | See [references/stakeholder-alignment.md](references/stakeholder-alignment.md)         | 合意形成の手法   |

### scripts/（決定論的処理）

| スクリプト               | 用途               | 使用例                                            |
| ------------------------ | ------------------ | ------------------------------------------------- |
| `calculate-priority.mjs` | 優先度スコア計算   | `node scripts/calculate-priority.mjs <json-file>` |
| `log_usage.mjs`          | フィードバック記録 | `node scripts/log_usage.mjs --result success`     |

### assets/（テンプレート）

| テンプレート       | 用途                                          |
| ------------------ | --------------------------------------------- |
| `triage-matrix.md` | 4象限マトリクス（ビジネス価値 vs 実現可能性） |

## 変更履歴

| Version | 日付       | 変更内容                                                   |
| ------- | ---------- | ---------------------------------------------------------- |
| 2.0.0   | 2026-01-02 | 18-skills.md仕様v2に完全準拠、agents/追加、references/整理 |
| 1.0.0   | 2025-12-31 | 18-skills.md仕様に準拠、Task仕様ナビ追加、全文日本語化     |
