---
name: acceptance-criteria-writing
description: |
  Given-When-Then 形式の受け入れ基準を整理し、テスト可能な完了条件の定義を支援する。
  要件の明確化、シナリオ設計、検証手順を一貫して整理する。

  Anchors:
  • Software Requirements (Karl Wiegers) / 適用: 要件分析・仕様化 / 目的: テスト可能な要件定義
  • BDD in Action (John Ferguson Smart) / 適用: Given-When-Then / 目的: 振る舞い駆動開発
  • The Art of Software Testing (Glenford Myers) / 適用: テスト設計 / 目的: 検証可能性の確保

  Trigger:
  受け入れ基準の作成、ユーザーストーリーの仕様化、テスト可能な要件定義を行う場合に使用。
  acceptance criteria, user story, GWT, Given-When-Then, testable requirements, definition of done
---

# acceptance-criteria-writing

## 概要

Given-When-Then 形式の受け入れ基準を整理し、テスト可能な完了条件の定義を支援する。

## ワークフロー

```
Phase 1: 要件整理
analyze-requirements → [validate-schema]
            ↓
Phase 2: 基準設計
design-criteria → [validate-schema]
            ↓
Phase 3: 検証
validate-criteria → [log-usage]
```

凡例: [script] = Script Task, 無印 = LLM Task

### Phase 1: 要件整理

**目的**: 受け入れ基準の前提と要件を明確化する

**アクション**:

1. ユーザーストーリーと目的を整理する
2. 前提条件と制約を洗い出す
3. 曖昧な表現をリスト化する

**Task**: `agents/analyze-criteria-requirements.md` を参照
**完了条件**: 要件整理メモと前提一覧が出力されている

### Phase 2: 基準設計

**目的**: Given-When-Then 形式の基準を設計する

**アクション**:

1. 正常系とエッジケースのシナリオを整理する
2. テスト可能性の観点で基準を設計する
3. テンプレートで表現を統一する

**Task**: `agents/design-acceptance-criteria.md` を参照
**完了条件**: GWTシナリオとエッジケース一覧が出力されている

### Phase 3: 検証

**目的**: 受け入れ基準を検証し、記録を残す

**アクション**:

1. 検証スクリプトで品質を確認する
2. 検証結果と改善点を整理する
3. ログを更新する

**Task**: `agents/validate-acceptance-criteria.md` を参照
**完了条件**: 検証レポートが出力されている

## Task仕様（ナビゲーション）

| Task                          | 責務               | 実行パターン | 入力         | 出力                       |
| ----------------------------- | ------------------ | ------------ | ------------ | -------------------------- |
| analyze-criteria-requirements | 要件と前提の明確化 | seq          | 要件/制約    | 要件整理メモ、前提一覧     |
| design-acceptance-criteria    | GWT形式の基準設計  | seq          | 要件整理メモ | 受け入れ基準、シナリオ一覧 |
| validate-acceptance-criteria  | 基準の検証と記録   | seq          | 受け入れ基準 | 検証レポート               |

**実行パターン凡例**:

- `seq`: シーケンシャル（前のTaskに依存）

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                       | 理由                     |
| ------------------------------ | ------------------------ |
| Given/When/Then を明確に分ける | 検証可能性が高まるため   |
| 正常系とエッジケースを分ける   | 抜け漏れが減るため       |
| 具体的な数値・条件を記述する   | テスト自動化が容易になる |
| 検証スクリプトで品質確認する   | 一貫した品質を担保できる |

### 避けるべきこと

| 禁止事項                           | 問題点               |
| ---------------------------------- | -------------------- |
| 曖昧な表現（「正しく」「適切に」） | テストが困難になる   |
| 実装方法を指定する                 | 要件が硬直化する     |
| 複数のアクションを1つのWhenに      | シナリオが複雑化する |
| 1つのThenに複数の期待結果          | 検証が曖昧になる     |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                                 | 機能                         |
| ------------------------------------------ | ---------------------------- |
| `scripts/validate-acceptance-criteria.mjs` | 受け入れ基準の品質検証       |
| `scripts/log_usage.mjs`                    | 使用記録と評価メトリクス更新 |
| `scripts/quick_validate.mjs`               | スキル構造の検証             |

### references/（詳細知識）

| リソース             | パス                                                                 | 読込条件       |
| -------------------- | -------------------------------------------------------------------- | -------------- |
| GWTパターン          | [references/gwt-patterns.md](references/gwt-patterns.md)             | パターン選定時 |
| テスト可能性ガイド   | [references/testability-guide.md](references/testability-guide.md)   | 4特性確認時    |
| エッジケースパターン | [references/edge-case-patterns.md](references/edge-case-patterns.md) | 例外設計時     |

### assets/（テンプレート・素材）

| アセット                                 | 用途                     |
| ---------------------------------------- | ------------------------ |
| `assets/acceptance-criteria-template.md` | 受け入れ基準テンプレート |

### 運用ファイル

| ファイル     | 目的               |
| ------------ | ------------------ |
| `EVALS.json` | 評価メトリクス管理 |
| `LOGS.md`    | 実行ログの蓄積     |
