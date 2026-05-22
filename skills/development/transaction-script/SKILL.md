---
name: transaction-script
description: |
  マーティン・ファウラーのPofEAAに基づくトランザクションスクリプトパターンを専門とするスキル。
  シンプルなビジネスロジックを手続き型で組織化し、CRUDベースのアプリケーション開発を効率化します。

  Anchors:
  • Patterns of Enterprise Application Architecture (Martin Fowler) / 適用: パターン定義と適用条件 / 目的: 適切なパターン選択
  • Designing Data-Intensive Applications (Martin Kleppmann) / 適用: データモデリング / 目的: 手続き型アプローチの妥当性検証

  Trigger:
  Use when implementing simple business logic, CRUD operations, building quick prototypes, or when domain model overhead is not justified.
  transaction script, executor pattern, procedural business logic, simple CRUD, PofEAA

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Transaction Script

## 概要

マーティン・ファウラーのPofEAAに基づくトランザクションスクリプトパターンを専門とするスキル。
ビジネスロジックを手続き型で組織化し、各リクエストに対して一つのスクリプトが直接処理を実行するパターンを提供します。

## ワークフロー

### Phase 1: 要件分析

**目的**: ビジネス要件がトランザクションスクリプトに適しているか判断

**アクション**:

1. ビジネス要件の複雑度を評価
2. CRUD操作の比率を確認
3. `references/pattern-overview.md` でパターン適用条件を確認
4. `references/domain-model-comparison.md` で代替パターンと比較

**Task**: `agents/analyze-requirements.md` を参照

### Phase 2: Executor設計

**目的**: トランザクションスクリプトの具体的な設計を行う

**アクション**:

1. スクリプトの入出力インターフェースを定義
2. 処理フロー（検証→取得→ロジック→永続化→返却）を設計
3. `references/executor-pattern.md` で実装パターンを参照
4. `assets/executor-template.md` をベースに設計

**Task**: `agents/design-executor.md` を参照

### Phase 3: 実装

**目的**: 設計に基づいてトランザクションスクリプトを実装

**アクション**:

1. Executorクラス/関数を実装
2. エラーハンドリングを追加
3. `scripts/analyze-executor.mjs` で設計検証
4. `scripts/validate-skill.mjs` でスキル構造を確認

**Task**: `agents/implement-executor.md` を参照

## Task仕様（ナビゲーション）

| Task                 | 起動タイミング | 入力             | 出力               |
| -------------------- | -------------- | ---------------- | ------------------ |
| analyze-requirements | Phase 1開始時  | ビジネス要件     | パターン適用判断書 |
| design-executor      | Phase 2開始時  | パターン適用判断 | Executor設計書     |
| implement-executor   | Phase 3開始時  | Executor設計書   | 実装済みスクリプト |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- 一つのスクリプトは一つのトランザクション
- 明確な関数名でトランザクションを表現（例: `processOrder`, `cancelSubscription`）
- 共通ロジックは関数に抽出
- 処理フローを上から下へ読める形で記述

### 避けるべきこと

- 巨大なスクリプト（100行超）
- 深いネスト（3段階超）
- 過度な抽象化（シンプルさを維持）
- ドメインモデルが必要なほど複雑なロジック

## リソース参照

### references/（詳細知識）

| リソース         | パス                                                                           | 読込条件                   |
| ---------------- | ------------------------------------------------------------------------------ | -------------------------- |
| Level1 基礎      | [references/Level1_basics.md](references/Level1_basics.md)                     | 初回整理時                 |
| Level2 実務      | [references/Level2_intermediate.md](references/Level2_intermediate.md)         | 設計時                     |
| Level3 応用      | [references/Level3_advanced.md](references/Level3_advanced.md)                 | 詳細分析時                 |
| Level4 専門      | [references/Level4_expert.md](references/Level4_expert.md)                     | 改善ループ時               |
| パターン概要     | [references/pattern-overview.md](references/pattern-overview.md)               | 構造・実装・適用条件確認時 |
| Executor Pattern | [references/executor-pattern.md](references/executor-pattern.md)               | Executor実装時             |
| Domain Model比較 | [references/domain-model-comparison.md](references/domain-model-comparison.md) | 代替パターン検討時         |

### scripts/（決定論的処理）

| スクリプト             | 用途               | 使用例                                            |
| ---------------------- | ------------------ | ------------------------------------------------- |
| `analyze-executor.mjs` | Executor設計の検証 | `node scripts/analyze-executor.mjs --path <file>` |
| `validate-skill.mjs`   | スキル構造検証     | `node scripts/validate-skill.mjs`                 |
| `log_usage.mjs`        | 使用記録           | `node scripts/log_usage.mjs --result success`     |

### assets/（テンプレート）

| テンプレート           | 用途                     |
| ---------------------- | ------------------------ |
| `executor-template.md` | Executor実装テンプレート |

## 変更履歴

| Version | Date       | Changes                                                 |
| ------- | ---------- | ------------------------------------------------------- |
| 2.0.0   | 2026-01-01 | 18-skills.md準拠、Anchors/Trigger追加、ワークフロー改善 |
| 1.0.0   | 2025-12-24 | Spec alignment and required artifacts added             |
