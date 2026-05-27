---
name: command-documentation-patterns
description: |
  コマンドのドキュメント設計（セルフドキュメンティング構造/使用例/トラブルシューティング）を整理し、説明の一貫性と読みやすさを支援するスキル。
  章構成、記述ルール、検証手順を一貫して整理する。

  Anchors:
  • Software Requirements (Karl Wiegers) / 適用: 要求の言語化と構造化 / 目的: 説明品質の安定化

  Trigger:
  Use when documenting commands, creating usage examples, or designing troubleshooting sections for command workflows.
  command documentation, usage examples, troubleshooting, self-documenting structure
---

# command-documentation-patterns

## 概要

コマンドのドキュメント設計（セルフドキュメンティング構造/使用例/トラブルシューティング）を整理し、説明の一貫性と読みやすさを支援する。

## ワークフロー

### Phase 1: 要件整理

**目的**: ドキュメントの目的と読者像を明確化する。

**アクション**:

1. 対象コマンドと読者を整理する。
2. 必要な章構成と使用例を決める。
3. 参照ガイドとテンプレートを確認する。

**Task**: `agents/analyze-documentation-requirements.md` を参照

### Phase 2: ドキュメント設計

**目的**: ドキュメント構造と記述ルールを具体化する。

**アクション**:

1. セクション構成と見出しを設計する。
2. 例とトラブルシューティングを設計する。
3. テンプレートで表現を統一する。

**Task**: `agents/design-documentation-structure.md` を参照

### Phase 3: 検証と記録

**目的**: ドキュメント品質を検証し、記録を残す。

**アクション**:

1. 検証スクリプトで完全性を確認する。
2. 検証結果と改善点を整理する。
3. ログと評価情報を更新する。

**Task**: `agents/validate-documentation.md` を参照

## Task仕様ナビ

| Task                               | 起動タイミング | 入力               | 出力                               |
| ---------------------------------- | -------------- | ------------------ | ---------------------------------- |
| analyze-documentation-requirements | Phase 1開始時  | 対象コマンド/読者  | 要件整理メモ、章構成案             |
| design-documentation-structure     | Phase 2開始時  | 要件整理メモ       | ドキュメント設計案、テンプレ適用案 |
| validate-documentation             | Phase 3開始時  | ドキュメント設計案 | 検証レポート、改善方針             |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                         | 理由                   |
| -------------------------------- | ---------------------- |
| 読者像を明確にする               | 説明粒度が合うため     |
| 例と手順を並記する               | 利用時の迷いが減るため |
| 検証スクリプトで完全性を確認する | 抜け漏れを防ぐため     |

### 避けるべきこと

| 禁止事項           | 問題点         |
| ------------------ | -------------- |
| 章構成を曖昧にする | 読みづらくなる |
| 例を省略する       | 利用者が迷う   |
| 記録を残さない     | 改善が続かない |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                   | 機能                         |
| ---------------------------- | ---------------------------- |
| `scripts/validate-docs.mjs`  | ドキュメント完全性検証       |
| `scripts/log_usage.mjs`      | 使用記録と評価メトリクス更新 |
| `scripts/validate-skill.mjs` | スキル構造の検証             |

### references/（詳細知識）

| リソース           | パス                                                                   | 読込条件     |
| ------------------ | ---------------------------------------------------------------------- | ------------ |
| レベル1 基礎       | [references/Level1_basics.md](references/Level1_basics.md)             | 初回整理時   |
| レベル2 実務       | [references/Level2_intermediate.md](references/Level2_intermediate.md) | 設計時       |
| レベル3 応用       | [references/Level3_advanced.md](references/Level3_advanced.md)         | 詳細設計時   |
| レベル4 専門       | [references/Level4_expert.md](references/Level4_expert.md)             | 改善ループ時 |
| ドキュメントガイド | [references/documentation-guide.md](references/documentation-guide.md) | 章構成設計時 |
| 要求仕様索引       | [references/requirements-index.md](references/requirements-index.md)   | 要件参照時   |
| 旧スキル           | [references/legacy-skill.md](references/legacy-skill.md)               | 互換確認時   |

### assets/（テンプレート・素材）

| アセット                          | 用途                             |
| --------------------------------- | -------------------------------- |
| `assets/command-documentation.md` | コマンドドキュメントテンプレート |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
