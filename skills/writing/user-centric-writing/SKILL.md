---
name: user-centric-writing
description: |
  ユーザー中心のドキュメント・文章作成を専門とするスキル。
  読者のニーズと理解度に合わせた明確で効果的なコンテンツを作成する。

  Anchors:
  • Badass: Making Users Awesome (Kathy Sierra) / 適用: ユーザー成功の視点 / 目的: 読者を成功させる文章設計
  • Plain Language Guidelines / 適用: 明確で簡潔な文章 / 目的: 理解しやすいコンテンツ

  Trigger:
  Use when creating user documentation, writing help content, drafting user guides,
  improving content readability, designing persona-based content, or reviewing text for clarity.
version: 1.1.0
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# User-Centric Writing

## 概要

ユーザー中心のドキュメント・文章作成を専門とするスキル。キャシー・シエラの『Badass: Making Users Awesome』の考え方を適用し、読者が目的を達成できるコンテンツを設計・作成する。

## ワークフロー

### Phase 1: ペルソナ分析

**目的**: 読者のニーズ、スキルレベル、目標を理解する

**Task**: `agents/persona-analysis.md`

**入力**:

- 対象読者の情報、プロダクトの文脈

**出力**:

- ペルソナ定義、読者のゴール

### Phase 2: コンテンツ設計・作成

**目的**: ペルソナに最適化されたコンテンツを作成する

**Task**: `agents/content-drafting.md`

**入力**:

- ペルソナ定義、コンテンツ要件

**出力**:

- ドキュメント草稿

### Phase 3: 読みやすさレビュー

**目的**: コンテンツの明確さと読みやすさを検証・改善する

**Task**: `agents/readability-review.md`

**入力**:

- ドキュメント草稿

**出力**:

- 改善されたドキュメント、読みやすさスコア

## Task仕様（ナビゲーション）

| Task                  | 役割               | 参照先                         |
| --------------------- | ------------------ | ------------------------------ |
| persona-analysis.md   | ペルソナ分析       | `agents/persona-analysis.md`   |
| content-drafting.md   | コンテンツ作成     | `agents/content-drafting.md`   |
| readability-review.md | 読みやすさレビュー | `agents/readability-review.md` |

## ベストプラクティス

### すべきこと

- **読者優先**: 読者が何を達成したいかを最初に考える
- **シンプルな言葉**: 専門用語は避け、必要な場合は説明を追加
- **構造化**: 見出し、箇条書き、短い段落で情報を整理
- **アクション指向**: 読者が次に何をすべきかを明確に
- **一貫性**: 用語、スタイル、トーンを統一

### 避けるべきこと

- 読者のレベルを考慮せずに専門用語を多用
- 一文に複数の概念を詰め込む
- 受動態の多用（能動態を優先）
- 曖昧な指示や説明

## リソース参照

### references/（詳細知識）

| リソース       | パス                                                                     | 読込条件             |
| -------------- | ------------------------------------------------------------------------ | -------------------- |
| Level1 基礎    | [references/Level1_basics.md](references/Level1_basics.md)               | 初回整理時           |
| Level2 実務    | [references/Level2_intermediate.md](references/Level2_intermediate.md)   | Phase実行中          |
| Level3 応用    | [references/Level3_advanced.md](references/Level3_advanced.md)           | 複雑な状況時         |
| Level4 専門    | [references/Level4_expert.md](references/Level4_expert.md)               | 大規模プロジェクト時 |
| Plain Language | [references/plain-language-guide.md](references/plain-language-guide.md) | Phase 3実行時        |

### スクリプト（scripts/）

| スクリプト                | 用途               | 実行タイミング |
| ------------------------- | ------------------ | -------------- |
| `measure-readability.mjs` | 読みやすさ測定     | Phase 3完了後  |
| `validate-skill.mjs`      | スキル構造検証     | スキル更新後   |
| `log_usage.mjs`           | 使用記録・自動評価 | 各Phase完了後  |

### アセット（assets/）

| アセット              | 用途                     | 使用タイミング |
| --------------------- | ------------------------ | -------------- |
| `persona-template.md` | ペルソナ定義テンプレート | Phase 1実行時  |

## 変更履歴

| Version | Date       | Changes                                             |
| ------- | ---------- | --------------------------------------------------- |
| 1.1.0   | 2026-01-01 | 18-skills.md仕様準拠、agents/作成、ワークフロー改善 |
| 1.0.0   | 2025-12-24 | Spec alignment and required artifacts added         |
