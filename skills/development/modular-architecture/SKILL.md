---
name: modular-architecture
description: |
  モジュラーアーキテクチャとコンポーネント分割の設計スキル。
  高凝集・低結合の原則に基づいたシステム設計、依存関係管理、
  スケーラブルなアーキテクチャパターンの実装を支援する。

  Anchors:
  • Clean Architecture (Robert C. Martin) / 適用: レイヤー分離 / 目的: ビジネスロジックとインフラの分離
  • Domain-Driven Design (Eric Evans) / 適用: 境界づけられたコンテキスト / 目的: ドメインモデルの凝集性
  • SOLID Principles / 適用: モジュール設計原則 / 目的: 保守性と拡張性の向上

  Trigger:
  Use when designing modular architecture, splitting system into components, managing dependencies, or applying high cohesion low coupling principles.
  modular, architecture, component, module, cohesion, coupling, dependency, layer, separation
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Modular Architecture

## 概要

モジュラーアーキテクチャとコンポーネント分割の設計スキル。高凝集・低結合の原則に基づいたシステム設計、依存関係管理、スケーラブルなアーキテクチャパターンの実装を支援する。

## ワークフロー

### Phase 1: アーキテクチャ分析

**目的**: システム要件を理解し、適切なモジュール分割を決定する

**アクション**:

1. システム要件とドメイン境界を明確化
2. 機能的凝集性と技術的凝集性を分析
3. モジュール境界の候補を特定
4. 既存コードベースの依存関係を把握

**Task**: `agents/analyze-architecture.md` を参照

### Phase 2: モジュール設計

**目的**: モジュールの責務と依存関係を定義する

**アクション**:

1. 各モジュールの責務と境界を定義
2. モジュール間インターフェースを設計
3. 依存関係の方向性を決定（依存性逆転）
4. レイヤー構造を設計

**Task**: `agents/design-modules.md` を参照

### Phase 3: 実装と検証

**目的**: 設計に基づいてモジュールを実装し、品質を確認する

**アクション**:

1. モジュール構造を実装
2. 循環依存をチェック
3. `scripts/validate-dependencies.mjs` で検証
4. テストを作成

**Task**: `agents/implement-validate.md` を参照

## Task仕様ナビ

| Task                 | 起動タイミング | 入力             | 出力                 |
| -------------------- | -------------- | ---------------- | -------------------- |
| analyze-architecture | Phase 1開始時  | システム要件     | 分析レポート         |
| design-modules       | Phase 2開始時  | 分析レポート     | モジュール設計書     |
| implement-validate   | Phase 3開始時  | モジュール設計書 | 実装コード、検証結果 |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                         | 理由             |
| -------------------------------- | ---------------- |
| ビジネスロジックとインフラを分離 | 変更容易性の確保 |
| 各モジュールに単一責任を持たせる | 凝集性の向上     |
| 依存性逆転の原則を適用           | 疎結合の実現     |
| インターフェースを明示的に定義   | 契約の明確化     |
| 依存関係を一方向に保つ           | 循環依存の防止   |

### 避けるべきこと

| 禁止事項                           | 問題点                 |
| ---------------------------------- | ---------------------- |
| 神クラス・ゴッドオブジェクトの作成 | 凝集性の低下           |
| 複数関心事を1モジュールに混在      | 責務の曖昧化           |
| 具体実装への直接依存               | 変更時の影響範囲拡大   |
| 循環依存の放置                     | ビルド・テストの困難化 |
| レイヤー飛び越えアクセス           | アーキテクチャ崩壊     |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                          | 機能                     |
| ----------------------------------- | ------------------------ |
| `scripts/validate-dependencies.mjs` | 依存関係と循環依存の検証 |
| `scripts/log_usage.mjs`             | 使用記録の保存           |

### references/（詳細知識）

| リソース     | パス                                                                     | 読込条件     |
| ------------ | ------------------------------------------------------------------------ | ------------ |
| 基本概念     | [references/basics.md](references/basics.md)                             | 初回利用時   |
| 設計パターン | [references/patterns.md](references/patterns.md)                         | 設計時       |
| レイヤー設計 | [references/layered-architecture.md](references/layered-architecture.md) | 高度な設計時 |

## 変更履歴

| Version | Date       | Changes                                |
| ------- | ---------- | -------------------------------------- |
| 2.0.0   | 2026-01-02 | 18-skills.md仕様完全準拠版として再構築 |
| 1.0.0   | 2025-12-31 | 初版作成                               |
