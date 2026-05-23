---
name: prompt-versioning-management
description: |
  プロンプトのライフサイクル管理を専門とするスキル。バージョン管理、デプロイ戦略、ロールバック、変更追跡により、本番環境で安全かつ効率的なプロンプト運用を実現します。

  Anchors:
  • The Pragmatic Programmer (Andrew Hunt, David Thomas) / 適用: 手順設計と実践的改善 / 目的: 体系的なバージョン管理
  • Continuous Delivery (Jez Humble) / 適用: デプロイパイプラインとロールバック戦略 / 目的: 安全なリリースプロセス
  • Semantic Versioning 2.0.0 / 適用: バージョン番号付けルール / 目的: 変更の影響範囲の明確化

  Trigger:
  Use when managing prompt versions, deploying prompts to production, implementing rollback strategies, tracking prompt changes, or establishing prompt lifecycle management.
  Keywords: prompt versioning, semantic versioning, deployment strategy, rollback, change tracking, prompt lifecycle, blue-green deployment
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Prompt Versioning Management

## 概要

プロンプトのライフサイクル管理を専門とするスキル。セマンティックバージョニングに基づくバージョン管理、Blue-Green/Canaryデプロイ戦略、迅速なロールバック、変更追跡により、本番環境で安全かつ効率的なプロンプト運用を実現します。

## ワークフロー

### Phase 1: バージョン計画

**目的**: プロンプト変更を分類し、適切なバージョン番号と影響範囲を決定

**Task**: `agents/version-planning.md`

**入力**:

- 現在のバージョン
- 変更内容の詳細
- 依存関係情報

**出力**:

- バージョン計画書（新バージョン・変更タイプ）
- 影響分析レポート
- デプロイ計画

**実行タイミング**: プロンプト変更時、リリース計画策定時

### Phase 2: デプロイ実行

**目的**: 計画に基づき安全にデプロイを実行し、段階的ロールアウトを管理

**Task**: `agents/deployment-execution.md`

**入力**:

- Phase 1 のバージョン計画書
- デプロイ対象環境
- ロールアウト設定

**出力**:

- デプロイログ
- ヘルスチェック結果
- ロールアウト進捗記録

**実行タイミング**: バージョン計画完了後、本番デプロイ時

### Phase 3: ロールバック・監査

**目的**: 問題発生時の迅速な復旧と、すべての変更の追跡・監査

**Task**: `agents/rollback-audit.md`

**入力**:

- デプロイログ
- ヘルスチェック結果
- 前バージョン情報

**出力**:

- ロールバック記録
- インシデントレポート
- 監査ログ
- ポストモーテム

**実行タイミング**: デプロイ問題発生時、定期監査時

## Task仕様

| Task                 | 起動タイミング | 入力                   | 出力                         |
| -------------------- | -------------- | ---------------------- | ---------------------------- |
| version-planning     | Phase 1開始時  | 変更内容・現バージョン | バージョン計画・影響分析     |
| deployment-execution | Phase 2開始時  | 計画書・環境設定       | デプロイログ・ヘルスチェック |
| rollback-audit       | Phase 3開始時  | デプロイログ・問題詳細 | ロールバック記録・監査ログ   |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

- [agents/version-planning.md](agents/version-planning.md)
- [agents/deployment-execution.md](agents/deployment-execution.md)
- [agents/rollback-audit.md](agents/rollback-audit.md)

## ベストプラクティス

### すべきこと

- セマンティックバージョニング（x.y.z）を厳格に適用
- 変更の影響範囲を事前に分析
- 段階的ロールアウト（10% → 25% → 50% → 100%）を実施
- ロールバック手順を事前に準備
- すべての変更を監査可能な形で記録
- ポストモーテムで学習を蓄積

### 避けるべきこと

- 一度に100%へのロールアウト
- ヘルスチェックなしのデプロイ
- ロールバック計画なしのリリース
- 変更履歴の記録漏れ
- 問題発生時の責任追及（ブレームレス文化を推進）

## リソース参照

### references/（詳細知識）

| リソース                   | パス                                                                       | 内容                         |
| -------------------------- | -------------------------------------------------------------------------- | ---------------------------- |
| 基礎知識                   | [references/Level1_basics.md](references/Level1_basics.md)                 | 基礎概念と用語               |
| 実務パターン               | [references/Level2_intermediate.md](references/Level2_intermediate.md)     | 実務での適用                 |
| 高度な戦略                 | [references/Level3_advanced.md](references/Level3_advanced.md)             | 高度なデプロイ戦略           |
| 専門トラブルシューティング | [references/Level4_expert.md](references/Level4_expert.md)                 | 専門的な問題解決             |
| バージョニング戦略         | [references/versioning-strategies.md](references/versioning-strategies.md) | セマンティックバージョニング |
| デプロイパターン           | [references/deployment-patterns.md](references/deployment-patterns.md)     | Blue-Green/Canary            |
| ロールバック手順           | [references/rollback-procedures.md](references/rollback-procedures.md)     | 復旧手順と監査               |

### scripts/（決定論的処理）

| スクリプト           | 用途         | 使用例                                                         |
| -------------------- | ------------ | -------------------------------------------------------------- |
| `log_usage.mjs`      | 使用履歴記録 | `node scripts/log_usage.mjs --result success --phase planning` |
| `validate-skill.mjs` | 構造検証     | `node scripts/validate-skill.mjs`                              |

### assets/（テンプレート）

| テンプレート              | 用途                     |
| ------------------------- | ------------------------ |
| `changelog-template.md`   | チェンジログ作成         |
| `deployment-checklist.md` | デプロイ前チェックリスト |

## 変更履歴

| Version | Date       | Changes                                                   |
| ------- | ---------- | --------------------------------------------------------- |
| 3.0.0   | 2026-01-02 | 18-skills.md仕様完全準拠: 3 Tasks追加、ワークフロー体系化 |
| 1.0.0   | 2025-12-24 | 初版: 基本構造とリソース整備                              |
