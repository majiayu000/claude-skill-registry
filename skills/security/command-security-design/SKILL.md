---
name: command-security-design
description: |
  コマンドのセキュリティ設計（allowed-tools制限/disable-model-invocation/機密情報保護）を整理し、安全な実行フローと権限制御を支援するスキル。
  セキュリティ要件、検証手順、テンプレート運用を一貫して整理する。

  Anchors:
  • Web Application Security (Andrew Hoffman) / 適用: 脅威モデリング / 目的: セキュア設計指針
  • OWASP Top 10 / 適用: 一般的脅威の整理 / 目的: リスク評価基準

  Trigger:
  Use when designing secure command execution, restricting tools, or preventing unsafe automated operations.
  command security, allowed-tools, disable-model-invocation, secret protection
---

# command-security-design

## 概要

コマンドのセキュリティ設計（allowed-tools制限/disable-model-invocation/機密情報保護）を整理し、安全な実行フローと権限制御を支援する。

## ワークフロー

### Phase 1: 要件整理

**目的**: セキュリティ要件とリスクを明確化する。

**アクション**:

1. 対象コマンドとリスクを整理する。
2. 制限すべきツールや自動実行条件を整理する。
3. 参照ガイドとテンプレートを確認する。

**Task**: `agents/analyze-security-requirements.md` を参照

### Phase 2: セキュリティ設計

**目的**: 制限ルールと対策を具体化する。

**アクション**:

1. allowed-tools と disable-model-invocation の方針を定義する。
2. 機密情報保護と監査方針を整理する。
3. テンプレートで表現を統一する。

**Task**: `agents/design-security-controls.md` を参照

### Phase 3: 検証と記録

**目的**: セキュリティ設計を検証し、記録を残す。

**アクション**:

1. セキュリティ検証スクリプトで整合性を確認する。
2. 検証結果と改善点を整理する。
3. ログと評価情報を更新する。

**Task**: `agents/validate-security-design.md` を参照

## Task仕様ナビ

| Task                          | 起動タイミング | 入力         | 出力                   |
| ----------------------------- | -------------- | ------------ | ---------------------- |
| analyze-security-requirements | Phase 1開始時  | 対象/リスク  | 要件整理メモ、制限候補 |
| design-security-controls      | Phase 2開始時  | 要件整理メモ | 制限ルール、対策方針   |
| validate-security-design      | Phase 3開始時  | 制限ルール   | 検証レポート、改善方針 |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                 | 理由                 |
| ------------------------ | -------------------- |
| リスクと制限を明確にする | 誤操作を防ぐため     |
| 自動実行防止を検討する   | 重大事故を避けるため |
| 検証と記録を実施する     | 改善が継続できるため |

### 避けるべきこと

| 禁止事項               | 問題点                 |
| ---------------------- | ---------------------- |
| 制限ルールを曖昧にする | 事故の原因になる       |
| 機密対策を省略する     | 情報漏洩のリスクがある |
| 記録を残さない         | 改善が続かない         |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                   | 機能                         |
| ---------------------------- | ---------------------------- |
| `scripts/audit-security.mjs` | セキュリティ監査             |
| `scripts/log_usage.mjs`      | 使用記録と評価メトリクス更新 |
| `scripts/validate-skill.mjs` | スキル構造の検証             |

### references/（詳細知識）

| リソース         | パス                                                                   | 読込条件     |
| ---------------- | ---------------------------------------------------------------------- | ------------ |
| レベル1 基礎     | [references/Level1_basics.md](references/Level1_basics.md)             | 初回整理時   |
| レベル2 実務     | [references/Level2_intermediate.md](references/Level2_intermediate.md) | 設計時       |
| レベル3 応用     | [references/Level3_advanced.md](references/Level3_advanced.md)         | 詳細設計時   |
| レベル4 専門     | [references/Level4_expert.md](references/Level4_expert.md)             | 改善ループ時 |
| セキュリティ指針 | [references/security-guidelines.md](references/security-guidelines.md) | 制限設計時   |
| 旧スキル         | [references/legacy-skill.md](references/legacy-skill.md)               | 互換確認時   |

### assets/（テンプレート・素材）

| アセット                   | 用途                         |
| -------------------------- | ---------------------------- |
| `assets/secure-command.md` | セキュアコマンドテンプレート |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
