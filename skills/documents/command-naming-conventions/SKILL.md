---
name: command-naming-conventions
description: |
  コマンド命名規則（動詞ベース命名/kebab-case/名前空間/発見可能性）を整理し、一貫した命名設計と見直しを支援するスキル。
  命名ルール、チェックリスト運用、検証手順を一貫して整理する。

  Anchors:
  • The Pragmatic Programmer (Andrew Hunt, David Thomas) / 適用: 命名規則の一貫性 / 目的: 実践的な命名の安定化
  • Clean Code (Robert C. Martin) / 適用: 意図が伝わる命名 / 目的: 自己説明性の向上

  Trigger:
  Use when defining command naming conventions, reviewing naming consistency, or designing namespace structures.
  command naming, kebab-case, verb-based naming, namespace design, discoverability
---

# command-naming-conventions

## 概要

コマンド命名規則（動詞ベース命名/kebab-case/名前空間/発見可能性）を整理し、一貫した命名設計と見直しを支援する。

## ワークフロー

### Phase 1: 要件整理

**目的**: 命名の目的と制約を明確化する。

**アクション**:

1. 対象コマンドと命名対象を整理する。
2. 既存命名の傾向と制約を整理する。
3. 参照ガイドとチェックリストを確認する。

**Task**: `agents/analyze-naming-requirements.md` を参照

### Phase 2: 命名設計

**目的**: 命名ルールと命名パターンを具体化する。

**アクション**:

1. 動詞/名詞/名前空間の構造を定義する。
2. 命名ルールと例外を整理する。
3. チェックリストで整合性を確認する。

**Task**: `agents/design-naming-conventions.md` を参照

### Phase 3: 検証と記録

**目的**: 命名の整合性を検証し、記録を残す。

**アクション**:

1. 命名検証スクリプトで整合性を確認する。
2. 検証結果と改善点を整理する。
3. ログと評価情報を更新する。

**Task**: `agents/validate-naming-conventions.md` を参照

## Task仕様ナビ

| Task                        | 起動タイミング | 入力          | 出力                   |
| --------------------------- | -------------- | ------------- | ---------------------- |
| analyze-naming-requirements | Phase 1開始時  | 命名対象/制約 | 要件整理メモ、命名候補 |
| design-naming-conventions   | Phase 2開始時  | 要件整理メモ  | 命名ルール、例外方針   |
| validate-naming-conventions | Phase 3開始時  | 命名ルール    | 検証レポート、改善方針 |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                   | 理由                   |
| -------------------------- | ---------------------- |
| 命名の意図を明確にする     | 誤解を減らすため       |
| 既存命名との整合を確認する | 一貫性を保つため       |
| 例外ルールを記録する       | 変更時の混乱を防ぐため |

### 避けるべきこと

| 禁止事項           | 問題点               |
| ------------------ | -------------------- |
| ルールを曖昧にする | 命名のばらつきが出る |
| チェックを省略する | 意図しない命名になる |
| 記録を残さない     | 改善が続かない       |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                    | 機能                         |
| ----------------------------- | ---------------------------- |
| `scripts/validate-naming.mjs` | 命名規則検証                 |
| `scripts/log_usage.mjs`       | 使用記録と評価メトリクス更新 |
| `scripts/validate-skill.mjs`  | スキル構造の検証             |

### references/（詳細知識）

| リソース     | パス                                                                   | 読込条件     |
| ------------ | ---------------------------------------------------------------------- | ------------ |
| レベル1 基礎 | [references/Level1_basics.md](references/Level1_basics.md)             | 初回整理時   |
| レベル2 実務 | [references/Level2_intermediate.md](references/Level2_intermediate.md) | 命名設計時   |
| レベル3 応用 | [references/Level3_advanced.md](references/Level3_advanced.md)         | 詳細設計時   |
| レベル4 専門 | [references/Level4_expert.md](references/Level4_expert.md)             | 改善ループ時 |
| 命名ルール   | [references/naming-rules.md](references/naming-rules.md)               | ルール確認時 |
| 要求仕様索引 | [references/requirements-index.md](references/requirements-index.md)   | 要件参照時   |
| 旧スキル     | [references/legacy-skill.md](references/legacy-skill.md)               | 互換確認時   |

### assets/（テンプレート・素材）

| アセット                     | 用途               |
| ---------------------------- | ------------------ |
| `assets/naming-checklist.md` | 命名チェックリスト |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
