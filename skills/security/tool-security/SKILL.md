---
name: tool-security
description: |
  MCPツールとAPI統合のセキュリティ設計を体系化するスキル。
  脅威整理、制御設計、設定検証を通じて安全なツール運用を支援する。

  Anchors:
  • Web Application Security / 適用: 脅威モデリング / 目的: 攻撃面の整理
  • OWASP ASVS / 適用: セキュリティ要件 / 目的: 制御の網羅性

  Trigger:
  Use when designing tool security controls, validating security configs, or reviewing secrets handling.
  tool security, threat modeling, config validation
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Tool Security

## 概要

MCPツールやAPI統合におけるセキュリティ設計を支援するスキル。脅威整理から制御設計、設定検証までを一貫した手順で提供する。

---

## ワークフロー

### Phase 1: 脅威と境界の整理

**目的**: ツール利用に伴う攻撃面と保護対象を整理する

**アクション**:

1. データフローと境界を洗い出す
2. 主要な脅威とリスクを分類する
3. 保護対象と優先順位を決める

**Task**: `agents/security-surface-analysis.md` を参照

### Phase 2: 制御設計と設定

**目的**: 脅威に対する制御を設計し、設定テンプレートを整備する

**アクション**:

1. 認証/認可/入力検証の制御を設計する
2. 設定テンプレートに反映する
3. 監査ログと鍵管理の方針を決める

**Task**: `agents/security-control-design.md` を参照

### Phase 3: 検証と監査

**目的**: セキュリティ設定の妥当性を検証し、運用監査を行う

**アクション**:

1. 設定検証スクリプトで確認する
2. 環境変数とシークレットの扱いを点検する
3. 実行記録を保存する

**Task**: `agents/security-validation.md` を参照

---

## Task仕様ナビ

| Task                      | 起動タイミング | 入力                    | 出力         |
| ------------------------- | -------------- | ----------------------- | ------------ |
| security-surface-analysis | Phase 1 開始時 | ツール構成/データフロー | 脅威整理メモ |
| security-control-design   | Phase 2 開始時 | 脅威整理/要件           | 制御設計書   |
| security-validation       | Phase 3 開始時 | 設定/監査ログ           | 検証レポート |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

---

## ベストプラクティス

### すべきこと

| 推奨事項                       | 理由                       |
| ------------------------------ | -------------------------- |
| 攻撃面と保護対象を明確にする   | 優先順位を誤らないため     |
| 設定テンプレートを統一する     | 運用ミスを減らすため       |
| 検証スクリプトで確認する       | 設定ミスを早期検出するため |
| 鍵とログの管理方針を明文化する | 監査性を確保するため       |

### 避けるべきこと

| 禁止事項                           | 問題点                     |
| ---------------------------------- | -------------------------- |
| 影響範囲を確認せずに権限を付与する | 攻撃面が拡大する           |
| 検証を省略して設定を反映する       | 設定ミスが残る             |
| ログを残さない                     | 監査や原因追跡が困難になる |

---

## リソース参照

### scripts/（決定論的処理）

| スクリプト                             | 機能                             |
| -------------------------------------- | -------------------------------- |
| `scripts/check-env-vars.mjs`           | 環境変数の安全性を点検する       |
| `scripts/validate-security-config.mjs` | セキュリティ設定を検証する       |
| `scripts/validate-skill.mjs`           | スキル構造と必須成果物を検証する |
| `scripts/log_usage.mjs`                | 実行記録を保存する               |

### references/（詳細知識）

| リソース     | パス                                                                         | 読込条件         |
| ------------ | ---------------------------------------------------------------------------- | ---------------- |
| 基礎概念     | [references/Level1_basics.md](references/Level1_basics.md)                   | Phase 1 で参照   |
| 実務パターン | [references/Level2_intermediate.md](references/Level2_intermediate.md)       | Phase 2 で参照   |
| 応用戦略     | [references/Level3_advanced.md](references/Level3_advanced.md)               | 監査時に参照     |
| エキスパート | [references/Level4_expert.md](references/Level4_expert.md)                   | 高度化時に参照   |
| APIキー管理  | [references/api-key-management.md](references/api-key-management.md)         | 認証設計時に参照 |
| 入力検証     | [references/input-validation-guide.md](references/input-validation-guide.md) | 制御設計時に参照 |
| 権限パターン | [references/permission-patterns.md](references/permission-patterns.md)       | 制御設計時に参照 |

### assets/（テンプレート・素材）

| アセット                               | 用途                         |
| -------------------------------------- | ---------------------------- |
| `assets/security-config-template.json` | セキュリティ設定テンプレート |
| `assets/audit-log-schema.json`         | 監査ログのスキーマ           |

## 変更履歴

| Version | Date       | Changes                                       |
| ------- | ---------- | --------------------------------------------- |
| 2.0.0   | 2026-01-02 | Frontmatter再設計、Task仕様と検証フローを刷新 |
| 1.0.1   | 2025-12-24 | 初期バージョン                                |
