---
name: command-placement-priority
description: |
  コマンドの配置場所と優先順位（プロジェクト/ユーザー/MCP、名前空間、競合解決）を整理し、配置判断と移行方針を支援するスキル。
  配置基準、優先順位ルール、移行フローを一貫して整理する。

  Anchors:
  • The Pragmatic Programmer (Andrew Hunt, David Thomas) / 適用: 配置判断の実務 / 目的: 運用の一貫性確保
  • Priority Resolution Protocol / 適用: 同名競合の解決 / 目的: 優先順位の明確化

  Trigger:
  Use when determining command placement, resolving command priority conflicts, or migrating commands between project/user/MCP layers.
  command placement, priority resolution, namespace design, project vs user commands, MCP integration
---

# command-placement-priority

## 概要

コマンドの配置場所と優先順位（プロジェクト/ユーザー/MCP、名前空間、競合解決）を整理し、配置判断と移行方針を支援する。

## ワークフロー

### Phase 1: 要件整理

**目的**: 配置対象と制約を明確化する。

**アクション**:

1. 対象コマンドと利用者を整理する。
2. 配置候補と制約を洗い出す。
3. 参照ガイドとテンプレートを確認する。

**Task**: `agents/analyze-placement-requirements.md` を参照

### Phase 2: 配置設計

**目的**: 配置基準と優先順位ルールを具体化する。

**アクション**:

1. 配置オプションと選定基準を整理する。
2. 優先順位と名前空間の方針を定義する。
3. 移行方針をテンプレートに落とし込む。

**Task**: `agents/design-placement-strategy.md` を参照

### Phase 3: 検証と記録

**目的**: 配置方針を検証し、記録を残す。

**アクション**:

1. 配置検証スクリプトで整合性を確認する。
2. 検証結果と改善点を整理する。
3. ログと評価情報を更新する。

**Task**: `agents/validate-placement.md` を参照

## Task仕様ナビ

| Task                           | 起動タイミング | 入力          | 出力                     |
| ------------------------------ | -------------- | ------------- | ------------------------ |
| analyze-placement-requirements | Phase 1開始時  | 配置対象/制約 | 要件整理メモ、配置候補   |
| design-placement-strategy      | Phase 2開始時  | 要件整理メモ  | 配置方針、優先順位ルール |
| validate-placement             | Phase 3開始時  | 配置方針      | 検証レポート、改善方針   |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                   | 理由                         |
| -------------------------- | ---------------------------- |
| 配置目的と対象を明確にする | 誤配置を防ぐため             |
| 優先順位ルールを明文化する | 競合時の判断が容易になるため |
| 移行手順を記録する         | 変更の再現性が保てるため     |

### 避けるべきこと

| 禁止事項               | 問題点             |
| ---------------------- | ------------------ |
| 配置基準を曖昧にする   | 競合が増える       |
| 例外ルールを記録しない | 運用が不安定になる |
| 記録を残さない         | 改善が続かない     |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                       | 機能                         |
| -------------------------------- | ---------------------------- |
| `scripts/validate-placement.mjs` | 配置方針検証                 |
| `scripts/log_usage.mjs`          | 使用記録と評価メトリクス更新 |
| `scripts/validate-skill.mjs`     | スキル構造の検証             |

### references/（詳細知識）

| リソース       | パス                                                                     | 読込条件       |
| -------------- | ------------------------------------------------------------------------ | -------------- |
| レベル1 基礎   | [references/Level1_basics.md](references/Level1_basics.md)               | 初回整理時     |
| レベル2 実務   | [references/Level2_intermediate.md](references/Level2_intermediate.md)   | 配置設計時     |
| レベル3 応用   | [references/Level3_advanced.md](references/Level3_advanced.md)           | 詳細設計時     |
| レベル4 専門   | [references/Level4_expert.md](references/Level4_expert.md)               | 改善ループ時   |
| 配置オプション | [references/placement-options.md](references/placement-options.md)       | 配置判断時     |
| 優先順位       | [references/priority-resolution.md](references/priority-resolution.md)   | 競合解決時     |
| 名前空間       | [references/namespace-strategies.md](references/namespace-strategies.md) | 名前空間設計時 |
| 移行ガイド     | [references/migration-guide.md](references/migration-guide.md)           | 移行設計時     |
| 旧スキル       | [references/legacy-skill.md](references/legacy-skill.md)                 | 互換確認時     |

### assets/（テンプレート・素材）

| アセット                             | 用途                             |
| ------------------------------------ | -------------------------------- |
| `assets/project-command-template.md` | プロジェクトコマンドテンプレート |
| `assets/user-command-template.md`    | ユーザーコマンドテンプレート     |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
