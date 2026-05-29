---
name: reusable-workflows
description: |
  GitHub Actions再利用可能ワークフローの専門スキル。
  ワークフロー共有、入力・出力設計、シークレット管理を提供します。

  Anchors:
  • 『Continuous Delivery』（Jez Humble） / 適用: CI/CD / 目的: パイプライン設計と自動化戦略

  Trigger:
  GitHub Actions再利用可能ワークフロー作成時、共通CI/CDパイプライン設計時に使用
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Reusable Workflows Skill

## 概要

GitHub Actions再利用可能ワークフローの設計と実装スキルです。`workflow_call` イベント、入力/出力/シークレット定義、呼び出しパターン、ワークフロー合成・継承・チェーンパターンなどの専門知識を提供します。

このスキルを使用して、以下の課題に対応できます：

- 複数のリポジトリやワークフロー間で共通のCI/CDロジックを再利用したい
- 複雑なパイプラインをモジュール化し、保守性を向上させたい
- エンタープライズ規模のワークフロー設計と管理を実施したい

詳細は `references/` ディレクトリのレベル別ガイドを参照してください。

## ワークフロー

### Phase 1: 目的と前提の整理

**目的**: タスクの目的と前提条件を明確にする

**アクション**:

1. `references/Level1_basics.md` と `references/Level2_intermediate.md` を確認
2. 必要な references/scripts/templates を特定
3. 既存のワークフロー実装パターンを確認

### Phase 2: スキル適用

**目的**: スキルの指針に従って具体的な作業を進める

**アクション**:

1. 関連リソースやテンプレートを参照しながら作業を実施
2. 重要な判断点をメモとして残す
3. ワークフロー呼び出しの構造を設計・実装する

### Phase 3: 検証と記録

**目的**: 成果物の検証と実行記録の保存

**アクション**:

1. `scripts/validate-skill.mjs` でスキル構造を確認
2. `scripts/validate-reusable.mjs` でワークフロー構文を検証
3. 成果物が目的に合致するか確認
4. `scripts/log_usage.mjs` を実行して記録を残す

## Task仕様ナビ

| Task                         | 説明                                                | 対応フェーズ | リソース                | テンプレート           |
| ---------------------------- | --------------------------------------------------- | ------------ | ----------------------- | ---------------------- |
| 基本的なワークフロー呼び出し | `workflow_call` の基本構文と使用方法                | Phase 1-2    | Level1_basics.md        | reusable-workflow.yaml |
| 入力・出力・シークレット定義 | workflow_call での入力/出力/シークレット の定義方法 | Phase 1-2    | Level2_intermediate.md  | reusable-workflow.yaml |
| Callerワークフロー実装       | 再利用可能なワークフローを呼び出すワークフロー実装  | Phase 2      | caller-patterns.md      | caller-workflow.yaml   |
| ワークフロー合成パターン     | 複数の再利用可能ワークフローを組み合わせる          | Phase 2      | Level3_advanced.md      | design-patterns.md     |
| ワークフロー継承・チェーン   | 親子関係を持つワークフロー設計                      | Phase 2-3    | Level3_advanced.md      | design-patterns.md     |
| エンタープライズ設計         | 大規模組織向けのワークフロー設計戦略                | Phase 1-3    | Level4_expert.md        | -                      |
| ワークフロー検証             | YAML構文とロジックの検証                            | Phase 3      | workflow-call-syntax.md | validate-reusable.mjs  |

## ベストプラクティス

### すべきこと

- `references/Level1_basics.md` を参照し、適用範囲を明確にする
- `references/Level2_intermediate.md` を参照し、実務手順を整理する
- テンプレートを活用して一貫性のあるワークフロー設計を心がける
- `workflow_call` の入力値は明確に型定義し、ドキュメント化する
- ワークフロー間の依存関係を最小化し、疎結合を保つ
- 再利用可能なワークフローの出力値をメタデータとして提供する
- `scripts/validate-reusable.mjs` で定期的にワークフロー構造を検証する

### 避けるべきこと

- アンチパターンや注意点を確認せずに進めることを避ける
- 再利用可能なワークフロー内での `secrets.GITHUB_TOKEN` の無制限使用を避ける
- 過度に複雑なワークフロー合成パターンを避け、保守性を優先する
- `workflow_call` での必須入力を多すぎないようにし、デフォルト値を活用する
- ワークフロー間での循環依存を避ける
- セキュリティ上の理由から、シークレット値を出力値として公開しない

## リソース参照

### レベル別ガイド

| レベル | ファイル                            | 対象者       | 学習時間 |
| ------ | ----------------------------------- | ------------ | -------- |
| 基礎   | `references/Level1_basics.md`       | 初心者       | 1-2時間  |
| 実務   | `references/Level2_intermediate.md` | 開発者       | 2-3時間  |
| 応用   | `references/Level3_advanced.md`     | 上級者       | 3-4時間  |
| 専門   | `references/Level4_expert.md`       | アーキテクト | 4-5時間  |

### デザインパターン・リソース

- `references/caller-patterns.md`: Callerワークフローの実装パターン集
- `references/design-patterns.md`: ワークフロー設計パターン（合成、継承、チェーン）
- `references/workflow-call-syntax.md`: workflow_call 構文リファレンス

### スクリプトとツール

| スクリプト                      | 用途                 | コマンド                                    |
| ------------------------------- | -------------------- | ------------------------------------------- |
| `scripts/validate-skill.mjs`    | スキル構造検証       | `node scripts/validate-skill.mjs`           |
| `scripts/validate-reusable.mjs` | ワークフロー構文検証 | `node scripts/validate-reusable.mjs [file]` |
| `scripts/log_usage.mjs`         | 使用記録・自動評価   | `node scripts/log_usage.mjs --help`         |

### テンプレート

- `assets/reusable-workflow.yaml`: 再利用可能なワークフロー基本テンプレート
- `assets/caller-workflow.yaml`: Callerワークフロー実装テンプレート

### その他

- `references/legacy-skill.md`: 旧SKILL.mdの全文（参考）

## コマンドリファレンス

### リソース読み取り

```bash
# レベル別ガイドの確認
cat .claude/skills/reusable-workflows/references/Level1_basics.md
cat .claude/skills/reusable-workflows/references/Level2_intermediate.md
cat .claude/skills/reusable-workflows/references/Level3_advanced.md
cat .claude/skills/reusable-workflows/references/Level4_expert.md

# デザインパターン・リソースの確認
cat .claude/skills/reusable-workflows/references/caller-patterns.md
cat .claude/skills/reusable-workflows/references/design-patterns.md
cat .claude/skills/reusable-workflows/references/workflow-call-syntax.md
cat .claude/skills/reusable-workflows/references/legacy-skill.md
```

### スクリプト実行

```bash
# スキル構造検証
node .claude/skills/reusable-workflows/scripts/validate-skill.mjs

# ワークフロー構文検証
node .claude/skills/reusable-workflows/scripts/validate-reusable.mjs [workflow-file]

# 使用記録と評価
node .claude/skills/reusable-workflows/scripts/log_usage.mjs --help
```

### テンプレート参照

```bash
# テンプレートの確認
cat .claude/skills/reusable-workflows/assets/reusable-workflow.yaml
cat .claude/skills/reusable-workflows/assets/caller-workflow.yaml
```

## 変更履歴

| Version | Date       | Changes                                                                                                                         |
| ------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------- |
| 1.1.0   | 2025-12-31 | 18-skills.md仕様に完全対応：YAML frontmatter（allowed-tools追加）、Task仕様ナビ、リソース参照テーブル化、ベストプラクティス拡充 |
| 1.0.0   | 2025-12-24 | Spec alignment and required artifacts added                                                                                     |
