---
name: context-window-optimization
description: |
  コンテキストウィンドウの制約内で情報を最適整理するためのスキル。
  トークン計測、優先順位付け、圧縮、検証の一連フローを提供する。

  Anchors:
  • High Performance Browser Networking / 適用: 計測とレイテンシ意識 / 目的: 予算内最適化
  • Designing Data-Intensive Applications / 適用: リソース制約下の設計 / 目的: 効率的な構造化
  • Progressive Disclosure パターン / 適用: 段階的情報開示 / 目的: 過剰読み込みの回避

  Trigger:
  Use when optimizing context window usage, measuring token budgets, prioritizing context elements, or applying compression techniques.
  context window optimization, token budget, context prioritization, compression, summarization
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# context-window-optimization

## 概要

コンテキストウィンドウの制約内で情報を整理し、必要な内容を確実に保持しながらトークン使用量を最適化する。

## ワークフロー

### Phase 1: 要件整理と計測

**目的**: 目的・制約・トークン予算を明確化する。

**アクション**:

1. 目的と成果物を整理する。
2. 現在のトークン使用量を見積もる。
3. 必須情報と除外候補を洗い出す。

**Task**: `agents/analyze-context-window-requirements.md` を参照

### Phase 2: 優先順位と戦略設計

**目的**: 参照順序と削減方針を設計する。

**アクション**:

1. 優先度分類を行う。
2. 圧縮・削減の方針を決める。
3. 出力形式を統一する。

**Task**: `agents/design-context-window-strategy.md` を参照

### Phase 3: 圧縮実装

**目的**: 圧縮と整理を実施する。

**アクション**:

1. 重要情報を抽出する。
2. 圧縮ルールに従って要約する。
3. 参照形式を整形する。

**Task**: `agents/implement-context-window-compression.md` を参照

### Phase 4: 検証と記録

**目的**: 構造と品質を検証し、学習を記録する。

**アクション**:

1. `scripts/validate-skill.mjs` で構造を検証する。
2. トークン削減率と品質を確認する。
3. `scripts/log_usage.mjs` で記録を更新する。

**Task**: `agents/validate-context-window-usage.md` を参照

## Task仕様ナビ

| Task                                 | 起動タイミング | 入力             | 出力                         |
| ------------------------------------ | -------------- | ---------------- | ---------------------------- |
| analyze-context-window-requirements  | Phase 1開始時  | 目的/制約        | トークン予算メモ、情報棚卸し |
| design-context-window-strategy       | Phase 2開始時  | トークン予算メモ | 最適化戦略書、優先順位表     |
| implement-context-window-compression | Phase 3開始時  | 最適化戦略書     | 圧縮サマリ、削除/保持一覧    |
| validate-context-window-usage        | Phase 4開始時  | 圧縮サマリ       | 検証レポート、ログ更新内容   |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項             | 理由                       |
| -------------------- | -------------------------- |
| 計測から開始する     | 客観的な削減判断を行うため |
| 優先順位を明文化する | 必須情報を守るため         |
| 圧縮ルールを統一する | 再現性を高めるため         |
| テンプレートを使う   | 出力の一貫性を保つため     |

### 避けるべきこと

| 禁止事項             | 問題点                 |
| -------------------- | ---------------------- |
| 計測せずに削減する   | 影響範囲が判断できない |
| 必須情報の削除       | 品質の劣化を招く       |
| 圧縮理由を記録しない | 再現性が失われる       |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                   | 機能                         |
| ---------------------------- | ---------------------------- |
| `scripts/validate-skill.mjs` | スキル構造の検証             |
| `scripts/log_usage.mjs`      | 使用記録と評価メトリクス更新 |

### references/（詳細知識）

| リソース     | パス                                                                         | 読込条件       |
| ------------ | ---------------------------------------------------------------------------- | -------------- |
| レベル1 基礎 | [references/Level1_basics.md](references/Level1_basics.md)                   | 初回整理時     |
| レベル2 実務 | [references/Level2_intermediate.md](references/Level2_intermediate.md)       | 戦略設計時     |
| レベル3 応用 | [references/Level3_advanced.md](references/Level3_advanced.md)               | 圧縮実装時     |
| レベル4 専門 | [references/Level4_expert.md](references/Level4_expert.md)                   | 検証改善時     |
| トークン計測 | [references/token-counting-guide.md](references/token-counting-guide.md)     | 予算見積もり時 |
| 優先順位付け | [references/context-prioritization.md](references/context-prioritization.md) | 重要度分類時   |
| 圧縮技法     | [references/compression-techniques.md](references/compression-techniques.md) | 圧縮実装時     |
| 要求仕様索引 | [references/requirements-index.md](references/requirements-index.md)         | 仕様確認時     |
| 旧スキル     | [references/legacy-skill.md](references/legacy-skill.md)                     | 互換確認時     |

### assets/（テンプレート・素材）

| アセット                                 | 用途                               |
| ---------------------------------------- | ---------------------------------- |
| `assets/context-window-plan-template.md` | トークン予算と方針整理テンプレート |
| `assets/context-priority-matrix.md`      | 優先順位付けマトリクス             |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
