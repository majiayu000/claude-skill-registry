---
name: project-architecture-integration
description: |
  プロジェクト固有のアーキテクチャ設計原則を統合するスキル。ハイブリッドアーキテクチャ（shared/features）、Clean Architecture依存関係ルール、データベース設計、REST API、テスト戦略、エラーハンドリング、CI/CD原則をエージェント設計に適用する。

  Anchors:
  • Clean Architecture / 適用: 依存関係ルールと境界設計 / 目的: アーキテクチャ層の分離と依存方向制御
  • Hybrid Architecture (shared/features) / 適用: ドメイン分離と再利用設計 / 目的: 循環依存回避と単一責任維持
  • docs/00-requirements/ / 適用: プロジェクト技術スタック仕様 / 目的: 要求仕様との整合性確保

  Trigger:
  Use when designing agents that generate project-specific files, database operations, API integrations, test strategies, error handling, or CI/CD workflows. Apply when determining file placement (shared/ vs features/), enforcing dependency rules, or ensuring architecture compliance.
  architecture compliance, hybrid structure, shared features, dependency rules, agent file generation, database design, REST API, testing strategy
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Project Architecture Integration

## 概要

プロジェクト固有のアーキテクチャ設計原則に基づいてエージェント設計を支援するスキル。Clean Architectureの依存関係ルールとHybrid Architecture（shared/features）パターンを統合し、プロジェクト構造に準拠したファイル生成、データベース設計、API連携を実現する。

## ワークフロー

### Phase 1: アーキテクチャ分析

**目的**: プロジェクト構造とアーキテクチャ要件を分析し、適用すべきパターンを特定

**アクション**:

1. エージェントの役割と責務を分析し、ドメイン依存性を判定
2. 生成対象ファイルの種類を特定（UI/ビジネスロジック/データアクセス層）
3. 既存プロジェクト構造を確認し、shared/とfeatures/の現状を把握
4. 依存関係ルールに基づいて配置先を決定

**Task**: `agents/architecture-analysis.md` を参照

### Phase 2: 準拠性検証

**目的**: 生成されたファイルやエージェント設計がアーキテクチャ原則に準拠しているか検証

**アクション**:

1. ファイル配置の妥当性を検証
2. 依存方向の正当性を確認（shared/ → features/ 禁止、features/ → features/ 禁止）
3. `scripts/check-architecture-compliance.mjs` で自動検証
4. 違反項目をリストアップし、修正提案を作成

**Task**: `agents/compliance-check.md` を参照

### Phase 3: 統合と記録

**目的**: アーキテクチャ原則をエージェント設計に統合し、実行記録を保存

**アクション**:

1. 検証済みアーキテクチャ設計をエージェント仕様に統合
2. アーキテクチャドキュメントを更新
3. `scripts/log_usage.mjs` で使用記録を保存

**Task**: `agents/integration.md` を参照

## Task仕様ナビ

| Task                  | 起動タイミング                | 入力                       | 出力                           |
| --------------------- | ----------------------------- | -------------------------- | ------------------------------ |
| architecture-analysis | Phase 1開始時                 | エージェント仕様、構造情報 | アーキテクチャパターン、配置先 |
| compliance-check      | Phase 2開始時、ファイル生成後 | ファイルパス、依存関係情報 | 準拠性レポート、修正提案       |
| integration           | Phase 3開始時、検証完了後     | 検証済み設計、統合対象     | 統合完了設計、実行記録         |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- エージェントがプロジェクト構造に準拠したファイルを生成する時に適用
- データベース操作、API連携、テスト実行、デプロイ関連エージェント設計時に使用
- shared/ と features/ の配置判断に迷った時は必ず Task を起動
- 依存関係ルールの違反チェックを必ず実行
- ドメイン非依存のコード（汎用UI、ユーティリティ）は shared/ に配置
- ビジネスロジックは features/ に配置し、Bounded Contextで分離

### 避けるべきこと

- shared/ から features/ への依存（循環依存の原因）
- features/ 間の直接依存（shared/ を経由すること）
- ドメインロジックを shared/ に配置しない
- アーキテクチャ検証をスキップしない
- 曖昧な命名（utils/、helpers/など）を避ける

## リソース参照

### references/（詳細知識）

| リソース             | パス                                                                                   | 内容                           |
| -------------------- | -------------------------------------------------------------------------------------- | ------------------------------ |
| 基礎知識             | See [references/basics.md](references/basics.md)                                       | アーキテクチャ基本概念         |
| 実装パターン         | See [references/patterns.md](references/patterns.md)                                   | 具体的な実装例とアンチパターン |
| Hybrid Architecture  | See [references/hybrid-architecture-guide.md](references/hybrid-architecture-guide.md) | shared/features構造詳細        |
| 要件仕様インデックス | See [references/requirements-index.md](references/requirements-index.md)               | プロジェクト要求仕様との同期   |
| Level 1（基礎）      | See [references/Level1_basics.md](references/Level1_basics.md)                         | スキル適用タイミングと最小要件 |
| Level 2（実務）      | See [references/Level2_intermediate.md](references/Level2_intermediate.md)             | テンプレート運用と実践手順     |
| Level 3（応用）      | See [references/Level3_advanced.md](references/Level3_advanced.md)                     | 複雑なアーキテクチャパターン   |
| Level 4（専門）      | See [references/Level4_expert.md](references/Level4_expert.md)                         | カスタムパターン設計           |

### scripts/（決定論的処理）

| スクリプト                          | 用途                   | 使用例                                                         |
| ----------------------------------- | ---------------------- | -------------------------------------------------------------- |
| `check-architecture-compliance.mjs` | アーキテクチャ準拠検証 | `node scripts/check-architecture-compliance.mjs --path src`    |
| `log_usage.mjs`                     | 使用記録と自動評価     | `node scripts/log_usage.mjs --result success --phase analysis` |
| `validate-skill.mjs`                | スキル構造検証         | `node scripts/validate-skill.mjs`                              |

### assets/（テンプレート）

| テンプレート                           | 用途                             |
| -------------------------------------- | -------------------------------- |
| `architecture-compliance-checklist.md` | アーキテクチャ準拠チェックリスト |

## クイックスタート

```bash
# 1. 基礎知識を理解
cat references/basics.md
cat references/hybrid-architecture-guide.md

# 2. アーキテクチャ分析 Task を起動（詳細は agents/architecture-analysis.md）
# Task内で配置先と依存関係を決定

# 3. 準拠性チェックを実行
node scripts/check-architecture-compliance.mjs --path <target-files>

# 4. 使用記録を保存
node scripts/log_usage.mjs --result success --phase integration
```

## 学習パス

```bash
# 初心者向け
cat references/basics.md              # 基本概念
cat references/hybrid-architecture-guide.md  # 構造理解

# 中級者向け
cat references/patterns.md            # 実装パターン
node scripts/check-architecture-compliance.mjs --help  # 検証ツール

# 上級者向け
cat references/Level3_advanced.md     # 複雑なパターン適用

# 専門家向け
cat references/Level4_expert.md       # カスタムパターン設計
```

## 依存関係ルールまとめ

### ✅ 許可される依存

- **features → shared**: ビジネスロジックが汎用コンポーネントを使用
- **features → features（同一フィーチャー内）**: フィーチャー内の内部依存
- **pages → features**: ページが機能を使用
- **pages → shared**: ページが汎用コンポーネントを使用

### ❌ 禁止される依存

- **shared → features**: 循環依存を引き起こす
- **features → features（異なるフィーチャー間）**: 境界を破壊する

**解決策**: 共通ロジックをshared/に移動し、依存方向を一方向に保つ

## 変更履歴

| Version | Date       | Changes                                              |
| ------- | ---------- | ---------------------------------------------------- |
| 3.0.0   | 2026-01-02 | 18-skills.md仕様完全準拠、SKILL.md簡潔化、知識外部化 |
| 2.0.0   | 2025-12-31 | Anchors/Trigger統合、agents/追加、description更新    |
| 1.0.0   | 2025-12-24 | 初版作成                                             |
